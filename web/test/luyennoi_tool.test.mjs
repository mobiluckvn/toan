/**
 * CỔNG · NHÁNH ReAct CHO LƯỢT BÉ HỎI LẠI (việc V11).
 *
 * ── VIỆC NÀY LÀM GÌ ──
 * Khi nhãn lượt là `hoiLai` và bé từ lớp 3, cô giáo máy được TRA trước khi đáp: bốn
 * tool thuần chạy trên gói `kho` máy con gửi lên (vốn từ · mẫu câu · tóm tắt mức
 * thạo). Trần 3 bước, bắt lặp, kết quả tool ≤ 300 ký tự.
 *
 * ── CÁI DỄ HỎNG, VÀ VÌ SAO CẦN CỔNG ──
 * Vòng ReAct hỏng theo đúng một kiểu: mô hình gọi tool, đọc kết quả, rồi gọi lại
 * chính tool ấy. Nó KHÔNG treo — nó cứ chạy, tốn lượt gọi mạng trả tiền thật, và bé
 * ngồi nhìn. Mà một vòng lặp thì không cổng nào bắt được bằng cách đọc mã: phải
 * dựng một mô hình giả CỐ TÌNH lặp rồi đếm số lượt gọi.
 *
 * Ba chỗ nữa chỉ đếm mới thấy:
 *   · lượt chốt phải BỎ `tools` — còn để thì mô hình gọi tiếp và ta phải bỏ câu
 *     trả lời, tức tốn một lượt mà không được gì;
 *   · lượt `assistant` kèm `tool_calls` phải được giữ trong gói TRƯỚC kết quả tool
 *     — bỏ nó thì Groq bác cả gói, và chỉ bác khi mô hình THẬT SỰ gọi tool;
 *   · chữ ngoài bài phải bị tool bác VÀ nói thẳng "đừng tự dịch" — thiếu câu sau
 *     thì mô hình vẫn dạy bé chữ ấy bằng nghĩa nó tự biết.
 *
 * ── ĐẢO CHIỀU THỬ ──
 * Mỗi phép dưới đây có một ca ĐÁNG LẼ PHẢI ĐỎ đi kèm.
 *
 * ── TIÊM HÀM, KHÔNG MOCK MODULE ──
 * `hoiMayCoTool` nhận `taoClient`; `hoiCoGiao` nhận `{ goi, goiTool }`.
 */
import {
  TOOLS, TEN_TOOL, BUOC_TOI_DA, KET_QUA_TOI_DA_CHU, chayTool, chuKyTool, soiKho,
  TOI_DA_TU_KHO, TOI_DA_CAU_KHO, TOI_DA_CHU_TOM_TAT, LOI_TOOL,
  TOOLS_GUI, TOOL_TRA_LOI, TEN_TRA_LOI,
} from '../functions/src/tool_phongnoi.js';
import { hoiMayCoTool, LoiGoi } from '../functions/src/luyennoi.js';
import {
  canHoiCo, dungKho, tomTatMucThao, tuCanPhat, LOP_TOI_THIEU, BAT_NHANH_TRA,
  TOM_TAT_TOI_DA_CHU, TU_KHO_TOI_DA, CAU_KHO_TOI_DA,
} from '../src/mon/tienganh/lib/hoico.js';
import { NGUONG_THAO, NGUONG_YEU } from '../src/mon/tienganh/lib/zpd.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

const KHO = {
  vonTu: [{ tu: 'dog', nghia: 'con chó' }, { tu: 'cat', nghia: 'con mèo' }],
  mauCau: ['I have a + [Noun].'],
  mucThaoTomTat: 'chữ con đã chắc: dog · chữ con còn ngại: cat',
};
const DAN = [{ role: 'system', content: 'You are a teacher.' },
  { role: 'user', content: 'co oi dog la gi?' }];

/**
 * Mô hình giả. `kichBan` là mảng: mỗi mục là mảng lời gọi tool, hay một chuỗi
 * (câu trả lời cuối). Hết kịch bản thì trả JSON mặc định.
 *
 * ⚠ CHỤP LẠI `tools` của TỪNG lượt — đó là cách duy nhất chứng minh lượt chốt đã
 * bỏ `tools`, và nó là một trong ba chốt chống vòng lặp.
 */
function mayGia(kichBan = []) {
  const daGoi = [];
  const tao = () => ({ chat: { completions: { create: async (o) => {
    const i = daGoi.length;
    daGoi.push(o);
    const x = kichBan[i];
    /* ⚠ KHÔNG PHÁT `tool_calls` KHI LƯỢT ẤY KHÔNG KHAI `tools`.
       Fixture của §8 nói "client giả LUÔN trả tool_call tra_tu('dog')", và bản đầu
       của tệp này làm đúng thế — kể cả ở lượt chốt. Nhưng lượt chốt bỏ `tools` khỏi
       gói, nên một mô hình THẬT không có cách nào trả về lời gọi tool ở đó: cái máy
       giả ấy không phải mô hình, nó là một cỗ máy bất khả. Và nó làm phép thử đỏ vì
       một lý do không bao giờ xảy ra trên bản chạy.
       Nên "luôn gọi tool" hiểu đúng là: luôn gọi, CHỪNG NÀO còn được phép gọi. */
    if (Array.isArray(x) && o.tools?.length) {
      return { choices: [{ message: {
        content: '',
        tool_calls: x.map((c, j) => ({
          id: `c${i}_${j}`,
          type: 'function',
          function: { name: c[0], arguments: JSON.stringify(c[1] ?? {}) },
        })),
      } }] };
    }
    /* ⚠ `typeof x === 'string'`, KHÔNG phải `x ?? mặc định`. Mục kịch bản của một
       lượt TRA là một mảng; tới lượt chốt (không khai `tools`) thì mảng ấy rơi
       xuống đây, và `x ?? …` đem thẳng cái MẢNG ra làm `content`. Lỗi hiện ra tận
       trong `hoiMayCoTool` dưới dạng `chu.trim is not a function` — một thông báo
       chẳng chỉ về phía bộ giả chút nào. */
    const chu = typeof x === 'string' ? x : '{"en":"I have a dog.","vi":"Cô nói nhé."}';
    return { choices: [{ message: { content: chu } }] };
  } } } });
  tao.daGoi = daGoi;
  return tao;
}

console.log('\n── A · BỐN TOOL, VÀ CHÚNG THUẦN ──\n');

{
  t('đúng bốn tool TRA', TOOLS.length === 4);
  /* ── KÊNH TRẢ LỜI LÀ TOOL THỨ NĂM, VÀ NÓ KHÔNG PHẢI TOOL TRA ──
     Đo thật: 19/20 lượt chết vì mô hình trả lời qua một tool nó tự đặt tên `json`.
     Khai đúng tool ấy thì hết. Nhưng nó KHÔNG được nằm trong `TOOLS`: `chayTool`
     chạy mọi tên trong `TOOLS`, và cho câu trả lời của cô đi qua đó thì nó biến
     thành chuỗi "there is no tool called…". */
  t('gửi lên NĂM tool: bốn tra + một kênh trả lời', TOOLS_GUI.length === 5);
  t('kênh trả lời KHÔNG nằm trong TOOLS', !TEN_TOOL.includes(TEN_TRA_LOI));
  t('kênh trả lời đòi đủ {en, vi}',
    JSON.stringify(TOOL_TRA_LOI.function.parameters.required.sort()) === '["en","vi"]');
  /* Đảo chiều: nếu ai đó gộp nó vào `TOOLS` thì `chayTool` phải nói "không có tool
     ấy" — tức câu trả lời của cô mất. Khẳng định luôn hành vi ấy để người sau thấy
     hậu quả chứ không phải chỉ thấy một lời dặn. */
  t('cho kênh trả lời qua chayTool thì MẤT câu trả lời (vì sao nó tách ra)',
    /no tool called/i.test(chayTool(TEN_TRA_LOI, { en: 'x', vi: 'y' }, KHO)));
  t('tên khớp bản thiết kế',
    JSON.stringify(TEN_TOOL) === JSON.stringify(['tra_tu', 'mau_cau_cua_unit', 'muc_thao', 'nghe_lai']));
  /* `TEN_TOOL` phải RÚT TỪ `TOOLS`, không phải một danh sách viết lại — hai danh
     sách thì sớm muộn lệch, và lệch kiểu "khai một tool mà không ai gọi được". */
  t('mọi tool khai đủ schema', TOOLS.every((x) => x.type === 'function'
    && x.function?.name && x.function?.description && x.function?.parameters?.type === 'object'));
  /* ⚠ MÔ TẢ PHẢI NÓI RÕ GIỚI HẠN. "Tra nghĩa một từ" thì mô hình gọi nó cho mọi từ
     tiếng Anh trên đời rồi nhận "không có trong bài" ba lần và hết lượt. */
  for (const ten of ['tra_tu', 'nghe_lai']) {
    const d = TOOLS.find((x) => x.function.name === ten).function.description;
    t(`mô tả "${ten}" nói rõ CHỈ từ của bài`, /only|not in this lesson/i.test(d));
  }

  t('tra_tu trả nghĩa trong kho',
    chayTool('tra_tu', { tu: 'dog' }, KHO).includes('con chó'));
  t('tra_tu không phân biệt chữ hoa',
    chayTool('tra_tu', { tu: ' DOG ' }, KHO).includes('con chó'));
  /* Hai chốt cho chữ ngoài bài, và chốt thứ hai mới là chốt thật. */
  const ngoai = chayTool('tra_tu', { tu: 'elephant' }, KHO);
  t('tra_tu bác chữ ngoài bài', /NOT in this lesson/i.test(ngoai));
  t('và dặn thẳng ĐỪNG TỰ DỊCH', /not translate it yourself/i.test(ngoai));
  t('mau_cau_cua_unit trả mẫu câu',
    chayTool('mau_cau_cua_unit', {}, KHO).includes('I have a + [Noun].'));
  t('muc_thao trả tóm tắt', chayTool('muc_thao', {}, KHO).includes('dog'));
  t('nghe_lai công nhận chữ của bài',
    /will hear "dog"/.test(chayTool('nghe_lai', { tu: 'dog' }, KHO)));
  t('nghe_lai bác chữ ngoài bài',
    /NOT in this lesson/i.test(chayTool('nghe_lai', { tu: 'zebra' }, KHO)));

  /* KHÔNG NÉM, bao giờ cũng trả CHUỖI: một tool ném là cả vòng đổ, bé mất lượt. */
  for (const [ten, a] of [['tra_tu', {}], ['nghe_lai', {}], ['tool_la', {}],
    ['tra_tu', null], ['muc_thao', undefined]]) {
    let ok = false;
    try { ok = typeof chayTool(ten, a, KHO) === 'string'; } catch { ok = false; }
    t(`chayTool("${ten}") không ném, trả chuỗi`, ok);
  }
  t('kho rỗng vẫn trả câu tử tế',
    chayTool('mau_cau_cua_unit', {}, { vonTu: [], mauCau: [] }).includes('no sentence patterns'));
  t('tên tool lạ → nói không có tool ấy',
    /no tool called/i.test(chayTool('xoa_het', {}, KHO)));

  /* ── CẮT 300 KÝ TỰ ── Kết quả tool đi THẲNG vào ngữ cảnh lượt sau, nên một kết
     quả dài là một lời dặn thứ hai không ai soi. */
  const dai = {
    vonTu: [{ tu: 'dog', nghia: 'x'.repeat(900) }],
    mauCau: Array.from({ length: 60 }, (_, i) => `pattern number ${i} + [Noun].`),
    mucThaoTomTat: 'y'.repeat(900),
  };
  for (const ten of TEN_TOOL) {
    const ra = chayTool(ten, { tu: 'dog' }, dai);
    t(`"${ten}" cắt về ≤ ${KET_QUA_TOI_DA_CHU} ký tự`, ra.length <= KET_QUA_TOI_DA_CHU);
  }
  /* Đảo chiều: nếu phép cắt bị gỡ thì dòng trên xanh hay đỏ? Phải đỏ — nên khẳng
     định luôn là CÓ ca thật sự bị cắt, không phải mọi ca đều ngắn sẵn. */
  t('đảo chiều — có ca thật sự dài tới mức phải cắt',
    chayTool('tra_tu', { tu: 'dog' }, dai).length === KET_QUA_TOI_DA_CHU);
}

console.log('\n── B · SOI GÓI kho ──\n');

{
  const nem = (ma, loi) => { throw new LoiGoi(ma, loi); };
  const g = soiKho(KHO, nem);
  t('gói đúng thì qua', g.vonTu.length === 2 && g.mauCau.length === 1);
  /* ⚠ GÓI RỖNG KHÔNG ĐƯỢC NÉM: nhánh phải chạy được với một bài chưa có mẫu câu.
     Ném thì bé mất cả lượt vì một thứ bé không biết là có. */
  let coNem = false;
  try { soiKho(null, nem); } catch { coNem = true; }
  t('gói rỗng KHÔNG ném', !coNem);
  t('gói rỗng cho ba trường rỗng', soiKho(undefined, nem).vonTu.length === 0);
  t('mục thiếu `tu` bị bỏ',
    soiKho({ vonTu: [{ nghia: 'x' }, { tu: 'dog', nghia: 'con chó' }] }, nem).vonTu.length === 1);
  t('tóm tắt dài bị cắt',
    soiKho({ mucThaoTomTat: 'z'.repeat(900) }, nem).mucThaoTomTat.length === TOI_DA_CHU_TOM_TAT);
  /* Gói BẤT THƯỜNG thì phải bác — đó là gói sai của máy con, không phải gói nghèo. */
  try { soiKho({ vonTu: Array(TOI_DA_TU_KHO + 1).fill({ tu: 'a' }) }, nem); coNem = false; }
  catch (e) { coNem = e instanceof LoiGoi && e.ma === 'kho-qua-lon'; }
  t('vốn từ quá trần → bác', coNem);
  try { soiKho({ mauCau: Array(TOI_DA_CAU_KHO + 1).fill('x') }, nem); coNem = false; }
  catch (e) { coNem = e instanceof LoiGoi && e.ma === 'kho-qua-lon'; }
  t('mẫu câu quá trần → bác', coNem);

  /* ── HAI TRẦN HAI BÊN PHẢI BẰNG NHAU ──
     `src/` và `functions/` KHÔNG được nhập chéo (cổng `ranh_gioi`), nên mỗi bên một
     hằng. Lệch nhau thì máy con dựng gói mà máy chủ bác — và bác CẢ LƯỢT, trong khi
     không ai sửa gì cả. Nên: hai hằng, một phép kiểm. */
  t('trần vốn từ hai bên bằng nhau', TU_KHO_TOI_DA === TOI_DA_TU_KHO);
  t('trần mẫu câu hai bên bằng nhau', CAU_KHO_TOI_DA === TOI_DA_CAU_KHO);
  t('trần tóm tắt hai bên bằng nhau', TOM_TAT_TOI_DA_CHU === TOI_DA_CHU_TOM_TAT);
}

console.log('\n── C · TRẦN BƯỚC VÀ BẮT LẶP ──\n');

{
  /* Mô hình giả LUÔN gọi `tra_tu('dog')` — đúng fixture của §8. */
  {
    const may = mayGia([[['tra_tu', { tu: 'dog' }]], [['tra_tu', { tu: 'dog' }]],
      [['tra_tu', { tu: 'dog' }]], [['tra_tu', { tu: 'dog' }]]]);
    const r = await hoiMayCoTool({ messages: DAN, kho: KHO }, may);
    t(`gọi create ≤ ${BUOC_TOI_DA + 1} lượt`, may.daGoi.length <= BUOC_TOI_DA + 1);
    /* "Dừng SỚM vì lặp ở lần 2": hai lượt tra + một lượt chốt = 3, chứ không phải 4. */
    t('dừng sớm vì lặp — đúng 3 lượt, không chạy hết trần', may.daGoi.length === 3);
    t('lý do dừng ghi là "lap"', r.lyDoDung === 'lap');
    t('chỉ chạy 2 bước tool', r.buocTool.length === 2);
  }

  /* Mỗi lượt một tool KHÁC nhau → không lặp, nên phải chạy hết trần. */
  {
    const may = mayGia([[['tra_tu', { tu: 'dog' }]], [['tra_tu', { tu: 'cat' }]],
      [['mau_cau_cua_unit', {}]], [['muc_thao', {}]]]);
    const r = await hoiMayCoTool({ messages: DAN, kho: KHO }, may);
    t('không lặp thì chạy hết trần rồi chốt', may.daGoi.length === BUOC_TOI_DA + 1);
    t('lý do dừng ghi là "het-buoc"', r.lyDoDung === 'het-buoc');
    t(`đúng ${BUOC_TOI_DA} bước tool`, r.buocTool.length === BUOC_TOI_DA);
  }

  /* ── LƯỢT CHỐT PHẢI BỎ `tools` ── */
  {
    const may = mayGia([[['tra_tu', { tu: 'dog' }]], [['tra_tu', { tu: 'dog' }]]]);
    await hoiMayCoTool({ messages: DAN, kho: KHO }, may);
    const chot = may.daGoi[may.daGoi.length - 1];
    t('lượt chốt KHÔNG có `tools`', !('tools' in chot) || chot.tools == null);
    t('lượt chốt ÉP json_object', chot.response_format?.type === 'json_object');
    t('mấy lượt tra thì CÓ đủ `tools`',
      may.daGoi.slice(0, -1).every((o) => o.tools?.length === TOOLS_GUI.length));
    /* Và mấy lượt tra KHÔNG ép JSON — `tools` + `response_format` cùng gói là chỗ
       Groq hay bác, ta đã dính một lần đúng kiểu ấy. */
    t('mấy lượt tra KHÔNG ép JSON',
      may.daGoi.slice(0, -1).every((o) => o.response_format == null));
    /* ── GÓI GỬI LÊN PHẢI ĐÚNG HÌNH DẠNG ──
       Lượt `assistant` kèm `tool_calls` phải đứng TRƯỚC mỗi lượt `role: 'tool'`.
       Bỏ nó thì Groq bác cả gói, mà chỉ bác khi mô hình THẬT SỰ gọi tool. */
    const ds = chot.messages;
    let hopLe = true;
    ds.forEach((m, i) => {
      if (m.role !== 'tool') return;
      const truoc = ds.slice(0, i).reverse().find((x) => x.role === 'assistant');
      if (!truoc?.tool_calls?.length) hopLe = false;
      if (!m.tool_call_id) hopLe = false;
    });
    t('mỗi lượt `tool` đều có lượt `assistant` kèm tool_calls đi trước', hopLe);
    t('kết quả tool THẬT SỰ nằm trong gói chốt',
      ds.some((m) => m.role === 'tool' && m.content.includes('con chó')));
    t('lượt chốt có dòng dặn ĐỪNG gọi tool nữa',
      /Do not call any more tools/i.test(ds[ds.length - 1].content));
  }

  /* Trả lời ngay, có dạng JSON → KHÔNG tốn lượt chốt. */
  {
    const may = mayGia(['{"en":"A dog.","vi":"Con chó."}']);
    const r = await hoiMayCoTool({ messages: DAN, kho: KHO }, may);
    t('trả lời ngay bằng JSON → chỉ 1 lượt gọi', may.daGoi.length === 1);
    t('lý do dừng ghi là "tra-loi-ngay"', r.lyDoDung === 'tra-loi-ngay');
    t('không bước tool nào', r.buocTool.length === 0);
    t('chữ đi ra nguyên vẹn', r.chu.includes('A dog.'));
  }

  /* Trả lời ngay nhưng KHÔNG phải JSON → phải có lượt chốt. */
  {
    const may = mayGia(['Chữ dog nghĩa là con chó nhé con.']);
    const r = await hoiMayCoTool({ messages: DAN, kho: KHO }, may);
    t('trả lời không phải JSON → gọi thêm lượt chốt', may.daGoi.length === 2);
    t('lý do dừng ghi rõ', r.lyDoDung === 'tra-loi-khong-phai-json');
  }

  /* Hai tool trong MỘT lượt — mô hình làm thế thật. */
  {
    const may = mayGia([[['tra_tu', { tu: 'dog' }], ['nghe_lai', { tu: 'dog' }]]]);
    const r = await hoiMayCoTool({ messages: DAN, kho: KHO }, may);
    t('hai tool một lượt đều chạy', r.buocTool.length === 2);
    t('và đều có kết quả', r.buocTool.every((b) => typeof b.ra === 'string' && b.ra));
  }

  /* Trả lời RỖNG ở LƯỢT CHỐT → phải NÓI RA, đừng trả chuỗi rỗng.
     ⚠ Rỗng phải nằm đúng ở mục thứ BA của kịch bản: hai lượt tra (lượt hai lặp nên
     dừng sớm) rồi mới tới lượt chốt. Đặt rỗng ở mục thứ hai thì nó thành "mô hình
     trả lời không phải JSON" — một ca khác hẳn, và lượt chốt vẫn trả JSON mặc định
     nên chẳng có gì ném. Bản đầu của phép thử này đặt sai chỗ và đỏ vì thế. */
  {
    const may = mayGia([[['tra_tu', { tu: 'dog' }]], [['tra_tu', { tu: 'dog' }]], '']);
    let ma = null;
    try { await hoiMayCoTool({ messages: DAN, kho: KHO }, may); }
    catch (e) { ma = e instanceof LoiGoi ? e.ma : 'khac'; }
    t('lượt chốt trả rỗng → ném "tra-loi-rong"', ma === 'tra-loi-rong');
  }

  /* Gói sai thì bác TRƯỚC khi gọi mạng — chứng minh bằng con số 0. */
  {
    const may = mayGia([]);
    let ma = null;
    try { await hoiMayCoTool({ messages: [], kho: KHO }, may); }
    catch (e) { ma = e instanceof LoiGoi ? e.ma : 'khac'; }
    t('gói lời rỗng → bác', ma === 'thieu-loi');
    t('và KHÔNG gọi mạng lần nào', may.daGoi.length === 0);
  }

  t('vân tay nhánh tool khác nhánh thường', (await (async () => {
    const a = await hoiMayCoTool({ messages: DAN, kho: KHO }, mayGia(['{"en":"x","vi":"y"}']));
    const { hoiMay } = await import('../functions/src/luyennoi.js');
    const b = await hoiMay({ messages: DAN }, mayGia(['{"en":"x","vi":"y"}']));
    return a.vanTayPrompt !== b.vanTayPrompt;
  })()));

  t('chuKyTool phân biệt tham số',
    chuKyTool('tra_tu', { tu: 'dog' }) !== chuKyTool('tra_tu', { tu: 'cat' }));
  /* HAI LỜI GỌI khác nhau, trùng tham số: đây chính là phép kiểm tính ổn định,
     không phải so một biến với chính nó. Tách ra hai biến cho ESLint thấy rõ —
     và đọc cũng rõ hơn. */
  const ky1 = chuKyTool('tra_tu', { tu: 'dog' });
  const ky2 = chuKyTool('tra_tu', { tu: 'dog' });
  t('chuKyTool ổn định với cùng tham số', ky1 === ky2);
  t('bộ đếm có ghi lại lượt lặp', LOI_TOOL.lap >= 1 && LOI_TOOL.goi >= 1);
}

console.log('\n── E · CÂU TRẢ LỜI ĐI QUA KÊNH TOOL ──\n');

{
  /* Trả lời NGAY bằng kênh tool → một lượt gọi, không cần lượt chốt. Đây là đường
     rẻ nhất, và là đường mô hình thật đi. */
  {
    const may = mayGia([[[TEN_TRA_LOI, { en: 'A dog.', vi: 'Con chó nhé.' }]]]);
    const r = await hoiMayCoTool({ messages: DAN, kho: KHO }, may);
    t('trả lời qua kênh tool → chỉ 1 lượt gọi', may.daGoi.length === 1);
    t('lý do dừng là "tra-loi-ngay"', r.lyDoDung === 'tra-loi-ngay');
    t('dựng lại đúng khối JSON máy con vẫn bóc',
      JSON.parse(r.chu).en === 'A dog.' && JSON.parse(r.chu).vi === 'Con chó nhé.');
    t('kênh trả lời KHÔNG bị tính là một bước tra', r.buocTool.length === 0);
  }

  /* TRA rồi mới trả lời — đường mẫu ReAct mong muốn. */
  {
    const may = mayGia([[['tra_tu', { tu: 'dog' }]],
      [[TEN_TRA_LOI, { en: 'A dog.', vi: 'dog nghĩa là con chó.' }]]]);
    const r = await hoiMayCoTool({ messages: DAN, kho: KHO }, may);
    t('tra rồi trả lời → 2 lượt, không có lượt chốt', may.daGoi.length === 2);
    t('lý do dừng là "tra-roi-tra-loi"', r.lyDoDung === 'tra-roi-tra-loi');
    t('bước tra được ghi lại', r.buocTool.length === 1 && r.buocTool[0].ten === 'tra_tu');
    t('lời cô mang nghĩa tra được', JSON.parse(r.chu).vi.includes('con chó'));
  }

  /* Gọi kênh trả lời mà RỖNG RUỘT → đừng trả bong bóng trắng cho bé. */
  {
    const may = mayGia([[[TEN_TRA_LOI, {}]]]);
    const r = await hoiMayCoTool({ messages: DAN, kho: KHO }, may);
    t('kênh trả lời rỗng → xuống lượt chốt', may.daGoi.length === 2);
    t('lý do dừng ghi rõ', r.lyDoDung === 'tra-loi-rong-o-tool');
  }

  /* Gọi kênh trả lời CÙNG LÚC với một tool tra: câu trả lời thắng, và tool tra
     trong cùng lượt ấy không được chạy — chạy rồi thì kết quả chẳng đi đâu. */
  {
    const may = mayGia([[['tra_tu', { tu: 'dog' }],
      [TEN_TRA_LOI, { en: 'A dog.', vi: 'Con chó.' }]]]);
    const r = await hoiMayCoTool({ messages: DAN, kho: KHO }, may);
    t('trả lời chung lượt với tool tra → nhận câu trả lời', JSON.parse(r.chu).en === 'A dog.');
    t('và dừng ngay, không tốn lượt nào nữa', may.daGoi.length === 1);
  }
}

console.log('\n── D · LUẬT RẼ, VÀ GÓI kho CỦA MÁY CON ──\n');

{
  t(`lớp tối thiểu là ${LOP_TOI_THIEU}`, LOP_TOI_THIEU === 3);

  /* ── CỜ MẶC ĐỊNH TẮT, VÀ CỔNG PHẢI CANH CẢ HAI TRẠNG THÁI ──
     Đo bằng Groq thật trên 25 lượt: nhánh tra KHÔNG hơn nhánh cũ chỗ nào (10/10 vs
     10/10 ở cả hai bộ), tool chỉ được gọi 4/25 lượt, và `nghe_lai` 0/5 kể cả khi bé
     hỏi đúng về âm. Lý lẽ đầy đủ ở `BAT_NHANH_TRA` trong `hoico.js`.
     Một cờ chỉ thử được ở trạng thái mặc định là một cờ mà nửa đường còn lại không
     ai canh — nên mọi ca dưới đây đi qua `bat` tường minh. */
  t('cờ mặc định TẮT', BAT_NHANH_TRA === false);
  t('cờ tắt thì KHÔNG rẽ, dù mọi điều kiện khác đủ',
    canHoiCo({ nhan: 'hoiLai', lop: 5 }) === false);

  t('BẬT + hoiLai + lớp 3 → rẽ', canHoiCo({ nhan: 'hoiLai', lop: 3, bat: true }) === true);
  t('BẬT + hoiLai + lớp 5 → rẽ', canHoiCo({ nhan: 'hoiLai', lop: 5, bat: true }) === true);
  /* Năm ca ĐÁNG LẼ PHẢI ĐỎ nếu điều kiện bị nới — thử với cờ ĐÃ BẬT, nếu không thì
     chúng xanh chỉ vì cờ tắt, và cổng chẳng canh điều kiện nào cả. */
  t('BẬT + hoiLai + lớp 2 → KHÔNG rẽ', canHoiCo({ nhan: 'hoiLai', lop: 2, bat: true }) === false);
  t('BẬT + nhãn khác + lớp 5 → KHÔNG rẽ',
    canHoiCo({ nhan: 'thieuTu', lop: 5, bat: true }) === false);
  t('BẬT + bài tả tranh → KHÔNG rẽ',
    canHoiCo({ nhan: 'hoiLai', lop: 5, laTranh: true, bat: true }) === false);
  t('BẬT + thiếu lớp → KHÔNG rẽ', canHoiCo({ nhan: 'hoiLai', bat: true }) === false);
  t('BẬT + lớp là chữ rác → KHÔNG rẽ',
    canHoiCo({ nhan: 'hoiLai', lop: 'ba', bat: true }) === false);
  t('gọi rỗng → KHÔNG rẽ', canHoiCo() === false);

  const von = {
    loi: { tu: [{ tu: 'dog', nghia: 'con chó' }, { tu: 'cat', nghia: 'con mèo' }],
      cau: [{ cau: 'I have a dog.', congThuc: 'I have a + [Noun].' }] },
    on: [{ tu: [{ tu: 'dog', nghia: 'con chó' }, { tu: 'fish', nghia: 'con cá' }],
      cau: [{ cau: 'I like fish.', congThuc: 'I like + [Noun].' }] }],
  };
  const kho = dungKho({ von });
  t('gói gồm đúng ba trường',
    JSON.stringify(Object.keys(kho).sort()) === '["mauCau","mucThaoTomTat","vonTu"]');
  t('trộn cả phần ôn', kho.vonTu.some((v) => v.tu === 'fish'));
  t('bỏ chữ trùng giữa bài và phần ôn',
    kho.vonTu.filter((v) => v.tu === 'dog').length === 1);
  /* CÔNG THỨC, không phải câu ví dụ: câu ví dụ đã điền sẵn một chữ vào ô trống. */
  t('mẫu câu là CÔNG THỨC', kho.mauCau.includes('I have a + [Noun].'));
  t('không lẫn câu ví dụ đã điền', !kho.mauCau.includes('I have a dog.'));
  t('gói rỗng không ném', dungKho({}).vonTu.length === 0 && dungKho().mauCau.length === 0);

  /* ── TÓM TẮT MỨC THẠO: KHÔNG SỐ ──
     Câu này đi vào kết quả tool, mô hình đọc rồi viết lời cho bé NGHE. Có số trong
     đó thì sớm muộn cô nói "con thạo chữ này tám mươi phần trăm". */
  const doThi = { nut: { v_u1_dog: { n: 'dog — con chó' }, v_u1_cat: { n: 'cat — con mèo' },
    v_u9_zebra: { n: 'zebra — con ngựa vằn' } } };
  const mucThao = { v_u1_dog: { p: NGUONG_THAO + 0.05 }, v_u1_cat: { p: NGUONG_YEU - 0.1 },
    v_u9_zebra: { p: 0.1 } };
  const tt = tomTatMucThao({ von, mucThao, doThi });
  t('tóm tắt nêu chữ đã chắc', /dog/.test(tt));
  t('tóm tắt nêu chữ còn ngại', /cat/.test(tt));
  t('KHÔNG có chữ số nào', !/[0-9]/.test(tt));
  t('không nhắc chữ ngoài vốn buổi này', !/zebra/.test(tt));
  t('cắt về đúng trần', tomTatMucThao({
    von: { loi: { tu: Array.from({ length: 40 }, (_, i) => ({ tu: `w${i}` })), cau: [] }, on: [] },
    mucThao: Object.fromEntries(Array.from({ length: 40 }, (_, i) => [`n${i}`, { p: 0.99 }])),
    doThi: { nut: Object.fromEntries(Array.from({ length: 40 }, (_, i) => [`n${i}`, { n: `w${i} — x` }])) },
  }).length <= TOM_TAT_TOI_DA_CHU);
  /* Thiếu dữ liệu → RỖNG, đừng đoán. */
  t('thiếu doThi → rỗng', tomTatMucThao({ von, mucThao }) === '');
  t('thiếu mucThao → rỗng', tomTatMucThao({ von, doThi }) === '');
  t('mức thạo không phải số → bỏ qua, không coi là 0',
    !/dog/.test(tomTatMucThao({ von, doThi, mucThao: { v_u1_dog: { p: null } } })));

  /* ── CHỮ CẦN PHÁT ── */
  t('nghe_lai hợp lệ → trả chữ',
    tuCanPhat([{ ten: 'nghe_lai', args: { tu: 'dog' }, ra: 'OK — the child will hear "dog"' }])
      === 'dog');
  t('không có nghe_lai → null',
    tuCanPhat([{ ten: 'tra_tu', args: { tu: 'dog' }, ra: 'x' }]) === null);
  t('danh sách rỗng / null → null', tuCanPhat([]) === null && tuCanPhat(null) === null);
  /* Chữ tool đã BÁC thì đừng phát: clip của chữ ngoài bài không có, và nút nghe sẽ
     im lặng vô cớ. */
  t('chữ tool đã bác → null',
    tuCanPhat([{ ten: 'nghe_lai', args: { tu: 'zebra' },
      ra: '"zebra" is NOT in this lesson, so it cannot be played.' }]) === null);
  /* CHỈ MỘT chữ, chữ ĐẦU: hai clip nối nhau thì bé không kịp nghe chữ nào. */
  t('hai lần nghe_lai → chỉ lấy chữ đầu',
    tuCanPhat([{ ten: 'nghe_lai', args: { tu: 'dog' }, ra: 'will hear "dog"' },
      { ten: 'nghe_lai', args: { tu: 'cat' }, ra: 'will hear "cat"' }]) === 'dog');
}

console.log(`\n${pass} PASS · ${fail} FAIL\n`);
process.exit(fail ? 1 : 0);
