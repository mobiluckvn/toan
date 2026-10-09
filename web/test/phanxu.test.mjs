/**
 * CỔNG · CHẤM VIẾT "LỖI ∥ KHEN", VÀ LƯỢT NÓI MƠ HỒ BỎ PHIẾU (việc V10).
 *
 * ── VIỆC NÀY LÀM GÌ ──
 * Hai nửa, cùng một mẫu #3 Parallelization:
 *   A · chấm viết tách bước tìm lỗi thành HAI lượt song song (lỗi ∥ khen), rồi gộp
 *       hai danh sách BẰNG MÃ;
 *   B · lượt nói có điểm trong [5, 7] và có một từ cùng unit ở gần thì đem hỏi hai
 *       phiếu mô hình; chỉ nhất trí 2/2 mới nhích điểm ±1.
 *
 * ── CÁI DỄ HỎNG, VÀ VÌ SAO CẦN CỔNG ──
 * Cả hai nửa đều là chỗ MỘT CON SỐ TỪ NGOÀI MẠNG ĐI VÀO ĐIỂM CỦA BÉ. Mà điểm nói
 * thì quyết "đạt / chưa đạt" (ngưỡng `DAT` = 6), tức quyết bé có phải làm lại chặng
 * hay không. Nên mọi đường đi tới điểm phải đóng được bằng phép thử chạy bằng
 * `node`, không cần mạng:
 *
 *   · phiếu 1–1, một phiếu hỏng, cả hai hỏng → PHẢI giữ nguyên điểm;
 *   · phiếu nhất trí → chỉ được ±1, và KHÔNG ĐƯỢC ra khỏi [5, 7];
 *   · ngoài vùng ấy → KHÔNG ĐƯỢC GỌI MẠNG lần nào;
 *   · lời khen phải là câu bé THẬT SỰ viết, và không được khen đúng câu đang bị sửa.
 *
 * ── ĐẢO CHIỀU THỬ ──
 * Mỗi phép dưới đây đều có một ca ĐÁNG LẼ PHẢI ĐỎ đi kèm — cổng xanh mà không canh
 * ai thì tệ hơn không có cổng, vì nó làm người ta tin.
 *
 * ── TIÊM HÀM, KHÔNG MOCK MODULE ──
 * `phanXu` nhận `taoClient`, `nhoPhanXu` nhận `{goi}`. Không tệp nào ở đây chạm
 * mạng, và cũng không tệp nào vá vào lòng module khác.
 */
import {
  soiGoiPhanXu, loiDanPhanXu, khungPhanXu, doiNhan, gopPhieu, phanXu,
  SO_PHIEU, NHIET_PHIEU, TOI_DA_CHU, TOKEN_PHAN_XU, LoiGoi,
} from '../functions/src/phanxu.js';
import {
  gopKhen, loiDanTimKhen, loiDanSua, khungCham,
  KHEN_TOI_DA, KHEN_TOI_DA_CHU, TOKEN_TIM_KHEN,
} from '../functions/src/chamviet.js';
import { PHIEN_BAN_MAU } from '../functions/src/vantay.js';
import {
  chamTu, chamCau, moHoCanBoPhieu, apDungPhieu, bacCua, loiKhen,
  VUNG_MO_HO, GAN_NHAU, DAT,
} from '../src/mon/tienganh/lib/chamnoi.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const nem = (f, ma) => {
  try { f(); return false; } catch (e) { return e instanceof LoiGoi && (!ma || e.ma === ma); }
};

/* Máy giả: trả sẵn một nhãn cho mỗi phiếu, và ĐẾM số lượt gọi. Đếm mới là phần
   quan trọng — "không gọi khi ngoài vùng" chỉ chứng minh được bằng con số 0. */
function mayGia(nhanDs, { nem: neml = false } = {}) {
  const log = [];
  return {
    log,
    tao: () => ({
      chat: {
        completions: {
          create: async ({ messages, temperature }) => {
            const i = log.length;
            log.push({ nhiet: temperature, dan: messages[0].content });
            if (neml) throw new Error('mạng hỏng');
            const n = nhanDs[i];
            if (n == null) throw new Error('hết nhãn');
            return { choices: [{ message: { content: JSON.stringify({ gan: n }) } }] };
          },
        },
      },
    }),
  };
}

console.log('\n── A · SOI GÓI PHÂN XỬ ──\n');

{
  const g = soiGoiPhanXu({ nghe: ' nain ', dich: 'nine', canhTranh: 'name' });
  t('gói đúng thì cắt khoảng trắng và trả ba trường',
    g.nghe === 'nain' && g.dich === 'nine' && g.canhTranh === 'name');
  t('KHÔNG trả `lop` — trường không ai đọc thì không chuyền',
    !('lop' in g));

  t('thiếu `nghe` → bác', nem(() => soiGoiPhanXu({ dich: 'a', canhTranh: 'b' }), 'thieu-nghe'));
  t('thiếu `dich` → bác', nem(() => soiGoiPhanXu({ nghe: 'a', canhTranh: 'b' }), 'thieu-dich'));
  t('thiếu `canhTranh` → bác',
    nem(() => soiGoiPhanXu({ nghe: 'a', dich: 'b' }), 'thieu-canh-tranh'));
  t('chuỗi dài quá trần → bác',
    nem(() => soiGoiPhanXu({ nghe: 'x'.repeat(TOI_DA_CHU + 1), dich: 'a', canhTranh: 'b' }),
      'qua-dai'));
  /* HAI CHỮ TRÙNG NHAU: không có gì phân xử, mà nếu để qua thì mô hình vẫn trả một
     nhãn, hai phiếu vẫn nhất trí, và điểm bé bị chỉnh vì một câu hỏi vô nghĩa. */
  t('hai chữ trùng nhau → bác (kể cả khác chữ hoa)',
    nem(() => soiGoiPhanXu({ nghe: 'dok', dich: 'Dog', canhTranh: 'dog' }), 'hai-chu-trung'));
  /* Đảo chiều: hai chữ KHÁC nhau thì phải qua. */
  t('đảo chiều — hai chữ khác nhau thì KHÔNG bác',
    !nem(() => soiGoiPhanXu({ nghe: 'dok', dich: 'dog', canhTranh: 'duck' })));
}

console.log('\n── B · LỜI DẶN KHÔNG ĐƯỢC LỘ ĐÂU LÀ TỪ ĐÍCH ──\n');

{
  const dan = loiDanPhanXu({ nghe: 'nain', dich: 'nine', canhTranh: 'name' });
  const dao = loiDanPhanXu({ nghe: 'nain', dich: 'nine', canhTranh: 'name', daoChieu: true });

  /* Đây là chốt của cả việc: nói ra chữ nào là chữ đang hỏi thì mô hình lấy lòng,
     và hai phiếu "nhất trí" chỉ còn là tiếng vang của lời dặn. */
  for (const [ten, d] of [['xuôi', dan], ['đảo', dao]]) {
    t(`lời dặn ${ten} KHÔNG chứa chữ "đích"/"cần đọc"/"yêu cầu"`,
      !/đích|cần đọc|yêu cầu|phải đọc|đáp án/i.test(d));
    t(`lời dặn ${ten} có đủ cả hai chữ`, d.includes('nine') && d.includes('name'));
    t(`lời dặn ${ten} đòi đúng một khối JSON`, /MỘT KHỐI JSON/.test(d));
    t(`lời dặn ${ten} cho phép trả "khac"`, /"khac"/.test(d));
  }

  /* ĐẢO CHIỀU THẬT: A của phiếu một phải là B của phiếu hai. */
  const viTriA = (d) => d.indexOf('A. ') + 3;
  t('đảo chiều đổi THẬT vị trí hai chữ',
    dan.slice(viTriA(dan), viTriA(dan) + 4).startsWith('nine')
    && dao.slice(viTriA(dao), viTriA(dao) + 4).startsWith('name'));
  t('hai chiều cho hai lời dặn KHÁC nhau', dan !== dao);

  /* Khung vân tay phải gồm CẢ CẶP — sửa một chiều mà vân tay không đổi là bảng so
     ΔC gom lẫn hai mẫu. Đúng cái bẫy `khungCham` đã dính ở V4. */
  const khung = khungPhanXu();
  t('khung vân tay gồm CẢ HAI chiều',
    khung.split('MÁY NGHE ĐƯỢC').length - 1 === 2);
  t('khung KHÔNG chứa chữ nào của bé',
    !khung.includes('nine') && !khung.includes('name') && !khung.includes('nain'));
}

console.log('\n── C · ĐỔI NHÃN A/B → VAI ──\n');

{
  t('xuôi: A là từ đích', doiNhan('A', false) === 'dich');
  t('xuôi: B là từ cạnh tranh', doiNhan('B', false) === 'canhTranh');
  t('đảo: A là từ cạnh tranh', doiNhan('A', true) === 'canhTranh');
  t('đảo: B là từ đích', doiNhan('B', true) === 'dich');
  t('chữ thường cũng nhận', doiNhan('a', false) === 'dich');
  t('nhãn lạ → "khac"', doiNhan('C', false) === 'khac' && doiNhan(null, false) === 'khac');
  /* Đảo chiều: nếu `doiNhan` bỏ qua `daoChieu` thì hai dòng dưới bằng nhau — và
     cả phép đảo chiều của hai phiếu thành vô nghĩa mà không gì kêu. */
  t('đảo chiều — `daoChieu` thật sự đổi kết quả',
    doiNhan('A', false) !== doiNhan('A', true));
}

console.log('\n── D · GỘP PHIẾU: CHỈ NHẤT TRÍ 2/2 MỚI ĐỔI ĐIỂM ──\n');

{
  t('2 phiếu "canhTranh" → −1',
    JSON.stringify(gopPhieu(['canhTranh', 'canhTranh']))
      === JSON.stringify({ gan: 'canhTranh', dieuChinh: -1, nhatTri: true }));
  t('2 phiếu "dich" → +1', gopPhieu(['dich', 'dich']).dieuChinh === 1);
  t('1–1 → GIỮ', gopPhieu(['dich', 'canhTranh']).dieuChinh === 0);
  t('1–1 không được coi là nhất trí', gopPhieu(['dich', 'canhTranh']).nhatTri === false);
  t('một phiếu "khac" cũng đủ làm cả cặp mất hiệu lực',
    gopPhieu(['dich', 'khac']).dieuChinh === 0);
  t('cả hai "khac" → GIỮ (nhất trí rằng không phải chữ nào)',
    gopPhieu(['khac', 'khac']).dieuChinh === 0 && gopPhieu(['khac', 'khac']).nhatTri === true);
  t('thiếu phiếu (một lượt hỏng) → GIỮ', gopPhieu(['dich']).dieuChinh === 0);
  t('không phiếu nào → GIỮ', gopPhieu([]).dieuChinh === 0 && gopPhieu(null).dieuChinh === 0);
  t('nhãn rác bị loại rồi mới gộp → GIỮ', gopPhieu(['dich', 'bua']).dieuChinh === 0);
  /* Đảo chiều: nếu ai nới `gopPhieu` thành "đa số tương đối" thì dòng 1–1 ở trên
     sẽ ra ±1 — nên giữ thêm một phép khẳng định mức điều chỉnh CHỈ nhận ba giá trị. */
  for (const p of [['dich', 'dich'], ['canhTranh', 'canhTranh'], ['dich', 'khac'], []]) {
    t(`mức điều chỉnh của [${p}] nằm trong {−1,0,1}`,
      [-1, 0, 1].includes(gopPhieu(p).dieuChinh));
  }
}

console.log('\n── E · PHÂN XỬ THẬT: HAI LƯỢT, HAI NHIỆT, HAI CHIỀU ──\n');

{
  const du = { nghe: 'nain', dich: 'nine', canhTranh: 'name' };

  /* Hai phiếu đều nghiêng về từ CẠNH TRANH. Phiếu xuôi trả "B", phiếu đảo trả "A"
     — hai nhãn KHÁC nhau mà cùng chỉ một chữ. Đó chính là điều phép đảo chiều phải
     làm được, và là ca mà một bản dựng bỏ qua `daoChieu` sẽ đọc thành 1–1. */
  {
    const m = mayGia(['B', 'A']);
    const kq = await phanXu(du, m.tao);
    t('hai phiếu cùng chỉ từ cạnh tranh → −1', kq.dieuChinh === -1 && kq.gan === 'canhTranh');
    t('gọi ĐÚNG hai lượt', m.log.length === SO_PHIEU);
    t('hai lượt dùng HAI NHIỆT khác nhau',
      m.log[0].nhiet === NHIET_PHIEU[0] && m.log[1].nhiet === NHIET_PHIEU[1]
      && NHIET_PHIEU[0] !== NHIET_PHIEU[1]);
    t('hai lượt dùng HAI LỜI DẶN khác nhau', m.log[0].dan !== m.log[1].dan);
    t('trả về vân tay có số phiên bản mẫu',
      kq.phienBanMau === PHIEN_BAN_MAU.phanxu && kq.phienBanMau >= 1);
  }

  /* Hai phiếu cùng chỉ từ ĐÍCH. */
  {
    const kq = await phanXu(du, mayGia(['A', 'B']).tao);
    t('hai phiếu cùng chỉ từ đích → +1', kq.dieuChinh === 1 && kq.gan === 'dich');
  }

  /* 1–1: cả hai trả "A" — nhưng "A" của phiếu đảo là chữ kia, nên đây là lệch. */
  {
    const kq = await phanXu(du, mayGia(['A', 'A']).tao);
    t('cả hai trả cùng NHÃN nhưng khác CHỮ → giữ điểm',
      kq.dieuChinh === 0 && kq.nhatTri === false);
  }

  /* Hỏng: mọi lượt ném. §7 — "lỗi → giữ", và KHÔNG được ném lên trên. */
  {
    const kq = await phanXu(du, mayGia([], { nem: true }).tao);
    t('cả hai lượt hỏng → giữ điểm, không ném', kq.dieuChinh === 0);
    t('đếm được số phiếu hỏng', kq.soPhieuHong === SO_PHIEU);
  }

  /* Trả rác thay vì JSON → coi như không có phiếu. */
  {
    const tao = () => ({ chat: { completions: { create: async () => ({
      choices: [{ message: { content: 'tôi nghĩ là chữ A nhé' } }],
    }) } } });
    const kq = await phanXu(du, tao);
    t('mô hình trả chữ trần, không JSON → giữ điểm', kq.dieuChinh === 0);
  }

  /* Gói sai thì VẪN PHẢI NÉM — đó là lỗi của máy con, che đi là che lỗi lập trình. */
  {
    let nemRa = false;
    try { await phanXu({ nghe: '', dich: 'a', canhTranh: 'b' }, mayGia(['A', 'B']).tao); }
    catch (e) { nemRa = e instanceof LoiGoi; }
    t('gói sai → NÉM (khác hẳn lỗi mạng)', nemRa);
  }

  t('trần token là hằng xuất ra và nhỏ', TOKEN_PHAN_XU > 0 && TOKEN_PHAN_XU <= 400);
}

console.log('\n── F · VÙNG MƠ HỒ: AI ĐƯỢC GỌI, AI KHÔNG ──\n');

{
  t('VUNG_MO_HO là [5, 7]', VUNG_MO_HO[0] === 5 && VUNG_MO_HO[1] === 7);
  /* Ngưỡng đạt phải NẰM TRONG vùng — ngoài vùng thì phiếu không lật được gì, và cả
     việc V10 thành một phép chỉnh điểm không ai thấy. */
  t('ngưỡng DAT nằm TRONG vùng mơ hồ', DAT > VUNG_MO_HO[0] && DAT < VUNG_MO_HO[1]);

  /* Từ cạnh tranh ở gần → có phiếu. */
  const mo = chamTu('nine', 'nain', { doiThu: ['name'] });
  t('điểm trong vùng + đối thủ ở gần → CẦN phiếu', moHoCanBoPhieu(mo) === true);
  t('`doiThuGan` nói rõ chữ nào', mo.doiThuGan?.tu === 'name');

  /* Đảo chiều — ba ca ĐÁNG LẼ PHẢI ĐỎ nếu điều kiện bị nới: */
  t('nói đúng hẳn (điểm 10) → KHÔNG phiếu',
    moHoCanBoPhieu(chamTu('dog', 'dog', { doiThu: ['duck'] })) === false);
  t('không có đối thủ nào → KHÔNG phiếu',
    moHoCanBoPhieu(chamTu('nine', 'nain', { doiThu: [] })) === false);
  t('máy không nghe thấy gì → KHÔNG phiếu',
    moHoCanBoPhieu(chamTu('dog', '', { doiThu: ['duck'] })) === false);
  t('đã bắt được nhầm từ (`nhamTu`, trần 3 điểm) → KHÔNG phiếu nữa',
    moHoCanBoPhieu(chamTu('three', 'tree', { doiThu: ['tree'] })) === false);
  t('bài CÂU không có đối thủ nên không bao giờ cần phiếu',
    moHoCanBoPhieu(chamCau('I have a dog', 'I have a dock')) === false);

  /* `GAN_NHAU` phải thật sự là cái quyết định — đặt một đối thủ XA thì phải tắt. */
  t('GAN_NHAU là hằng xuất ra', typeof GAN_NHAU === 'number' && GAN_NHAU > 0);
  t('đối thủ ở XA → `doiThuGan` rỗng',
    chamTu('nine', 'nain', { doiThu: ['elephant'] }).doiThuGan == null);

  /* ⚠ BÁO RA ĐỐI THỦ KHÔNG ĐƯỢC ĐỔI ĐIỂM. Đây là chỗ dễ hỏng nhất của phần thêm
     vào `chamTu`: nếu điểm tụt đi một tí thì cả 711 câu đã đo của bốn quyển lệch. */
  const coDoiThu = chamTu('nine', 'nain', { doiThu: ['name'] });
  const khongDoiThu = chamTu('nine', 'nain', { doiThu: [] });
  t('thêm đối thủ KHÔNG làm điểm đổi', coDoiThu.diem === khongDoiThu.diem);
}

console.log('\n── G · ÁP PHIẾU: ±1, VÀ KHÔNG RA KHỎI [5,7] ──\n');

{
  t('6 −1 → 5', apDungPhieu(6, -1) === 5);
  t('6 +1 → 7', apDungPhieu(6, 1) === 7);
  /* HAI CHỐT CỦA §7: không bao giờ hạ dưới 5 hay nâng trên 7 bằng bỏ phiếu. */
  t('5 −1 → VẪN 5 (không hạ dưới đáy vùng)', apDungPhieu(5, -1) === 5);
  t('7 +1 → VẪN 7 (không nâng trên đỉnh vùng)', apDungPhieu(7, 1) === 7);
  t('ngoài vùng thì phiếu vô hiệu — 9 −1 → 9', apDungPhieu(9, -1) === 9);
  t('ngoài vùng thì phiếu vô hiệu — 2 +1 → 2', apDungPhieu(2, 1) === 2);
  t('mức 0 → giữ', apDungPhieu(6, 0) === 6);
  /* Mức bất thường chỉ được kéo đúng MỘT bậc, không được nhân lên. */
  t('mức +5 vẫn chỉ nhích một bậc', apDungPhieu(5, 5) === 6);
  t('mức −5 vẫn chỉ nhích một bậc', apDungPhieu(7, -5) === 6);

  /* ⚠ `Number(null) === 0` và `Number.isFinite(0) === true` — cái bẫy đã cắn hai
     lần ở `hocba.js`. Điểm chưa có mà đi qua phép kẹp thì ra 0, và 0 trông như một
     điểm thật: bé "được" 0 điểm cho một lượt chưa chấm. */
  t('điểm null → trả lại null, KHÔNG thành 0', apDungPhieu(null, -1) === null);
  t('điểm undefined → trả lại undefined', apDungPhieu(undefined, -1) === undefined);
  t('mức null → giữ điểm', apDungPhieu(6, null) === 6);
  t('mức NaN → giữ điểm', apDungPhieu(6, NaN) === 6);

  /* Bậc phải dựng lại cho khớp điểm mới, nếu không thì thẻ hiện một điểm mà cô nói
     câu của bậc khác.

     ⚠ MỐC BẬC KHÔNG TRÙNG MỐC ĐIỂM: `bacCua` cắt ở ≥5 · ≥7 · ≥9, nên 5 và 6 CÙNG
     bậc "kha" — chỗ phiếu đổi được bậc chỉ là 6→7 (và 7→6 chiều ngược). Bản đầu
     của cổng này đòi "6 xuống 5 thì lời cô đổi" và đỏ, mà mã thì đúng. Nên soi
     TÍNH CHẤT, không soi một cặp số đoán sẵn: bậc phải luôn khớp điểm sau khi áp
     phiếu, ở MỌI mốc trong vùng. */
  t('bacCua xuất ra và khớp mốc', bacCua(7) === 'tot' && bacCua(5) === 'kha');
  let bacLech = 0, soCaBacDoi = 0;
  for (let d = VUNG_MO_HO[0]; d <= VUNG_MO_HO[1]; d += 1) {
    for (const b of [-1, 0, 1]) {
      const moi = apDungPhieu(d, b);
      /* Hai thẻ cho CÙNG điểm mới: một dựng bậc đúng (như `NutNoi` làm), một để
         bậc CŨ lại (lỗi mà phép dựng lại bậc đi chữa). Chúng phải khác nhau ở mọi
         ca điểm vượt mốc bậc — nếu không thì việc dựng lại bậc là vô ích. */
      const dung = { diem: moi, bac: bacCua(moi), lyDo: null, dich: 'nine', nghe: 'nain' };
      const bacCu = { ...dung, bac: bacCua(d) };
      if (bacCua(d) === bacCua(moi)) continue;   // phiếu không vượt mốc bậc nào
      soCaBacDoi += 1;
      /* Chỉ soi `chinh`: `sao` được `loiKhen` tính từ `diem`, không từ `bac`, nên
         nó đúng ở cả hai thẻ — soi nó là soi một thứ không liên quan, và bản đầu
         của cổng này đỏ vì đúng lý do ấy. */
      if (loiKhen(dung).chinh === loiKhen(bacCu).chinh) bacLech += 1;
    }
  }
  /* ⚠ Vòng trên `continue` phần lớn các ca, nên phải khẳng định nó CÓ chạy — không
     thì `bacLech === 0` chỉ nói rằng chẳng ca nào được xét. Đúng cái bẫy "ngưỡng
     phần trăm che lỗ thủng". */
  t('vòng soi bậc có ít nhất hai ca vượt mốc để xét', soCaBacDoi >= 2);
  t('để bậc CŨ lại thì lời cô lệch — nên phải dựng lại bậc', bacLech === 0);
  /* Và ca 6→7 phải THẬT SỰ đổi lời — nếu không thì vòng trên không canh gì cả. */
  const sau = { diem: 7, bac: bacCua(7), lyDo: null, dich: 'nine', nghe: 'nain' };
  const nam = { ...sau, diem: 6, bac: bacCua(6) };
  t('6 lên 7 thì cả lời cô và số sao đều đổi theo',
    loiKhen(sau).chinh !== loiKhen(nam).chinh && loiKhen(sau).sao !== loiKhen(nam).sao);
}

console.log('\n── H · CHẤM VIẾT: GỘP "LỖI ∥ KHEN" BẰNG MÃ ──\n');

{
  const viet = 'I have two cat. The cat is black. I like my cat.';
  const loi = [{ cau: 'I have two cat.', loai: 'thieuTu', ghiChu: 'thiếu s' }];

  /* 1 · KHEN MỘT CÂU BÉ KHÔNG HỀ VIẾT — mô hình tự sửa rồi khen bản đã sửa. */
  t('bỏ câu khen không có trong bài',
    gopKhen([], [{ cau: 'I have two cats.', vi: 'đúng số nhiều' }], viet).length === 0);
  t('đảo chiều — câu CÓ trong bài thì giữ',
    gopKhen([], [{ cau: 'I like my cat.', vi: 'nói được điều thích' }], viet).length === 1);

  /* 2 · CÙNG MỘT CÂU VỪA KHEN VỪA BỊ LIỆT LỖI → LỖI THẮNG. */
  t('câu đang bị sửa thì KHÔNG được khen',
    gopKhen(loi, [{ cau: 'I have two cat.', vi: 'dùng đúng từ cat' }], viet).length === 0);
  t('đảo chiều — câu khác thì vẫn khen được',
    gopKhen(loi, [{ cau: 'The cat is black.', vi: 'đúng mẫu màu sắc' }], viet).length === 1);

  /* 3 · So bằng bản XẾP PHẲNG, không so nguyên văn: hai mắt xích trích cùng một
     câu có thể lệch nhau dấu chấm hay chữ hoa. */
  t('khác dấu chấm / chữ hoa vẫn nhận ra là một câu',
    gopKhen([{ cau: 'i have two cat' }],
      [{ cau: 'I have two cat.', vi: 'x' }], viet).length === 0);
  t('trùng nhau thì chỉ giữ một',
    gopKhen([], [{ cau: 'I like my cat.', vi: 'a' }, { cau: 'I like my cat', vi: 'b' }],
      viet).length === 1);

  /* 4 · Trần số mục và trần độ dài. */
  const nhieu = Array.from({ length: 9 }, () => ({ cau: 'The cat is black.', vi: 'x' }))
    .map((k, i) => ({ cau: i % 2 ? 'I like my cat.' : 'The cat is black.', vi: `lời ${i}` }));
  t(`giữ nhiều nhất ${KHEN_TOI_DA} mục`, gopKhen([], nhieu, viet).length <= KHEN_TOI_DA);
  t('cắt lời khen dài quá trần',
    gopKhen([], [{ cau: 'I like my cat.', vi: 'y'.repeat(500) }], viet)[0].vi.length
      === KHEN_TOI_DA_CHU);

  /* 5 · Mục thiếu chữ thì bỏ hẳn, không đẩy một mục rỗng sang mắt xích 2. */
  t('mục thiếu `vi` → bỏ',
    gopKhen([], [{ cau: 'I like my cat.', vi: '' }], viet).length === 0);
  t('mục thiếu `cau` → bỏ', gopKhen([], [{ cau: '', vi: 'hay lắm' }], viet).length === 0);
  t('danh sách rỗng / null → mảng rỗng',
    gopKhen([], [], viet).length === 0 && gopKhen(null, null, viet).length === 0);
}

console.log('\n── I · LỜI DẶN TÌM KHEN, VÀ KHUNG VÂN TAY BỐN MẮT XÍCH ──\n');

{
  const goi = { de: 'Tả con mèo', viet: 'I have a cat.', vonTu: [{ tu: 'cat' }],
    mauCau: ['I have a …'], lop: 3 };

  const dan = loiDanTimKhen(goi);
  /* Mắt xích 1b CẤM SỬA, y như mắt xích 1 — cho nó viết câu đúng là mở lại đúng
     cửa cho chữ ngoài vốn mà cả V4 sinh ra để đóng. */
  t('lời dặn tìm khen CẤM sửa', /KHÔNG SỬA/.test(dan));
  t('lời dặn tìm khen CẤM chấm điểm', /KHÔNG SỬA, KHÔNG CHẤM ĐIỂM/.test(dan));
  t('lời dặn tìm khen đòi NGUYÊN VĂN câu bé viết', /NGUYÊN VĂN/.test(dan));
  t('lời dặn tìm khen cho phép trả rỗng', /"khen": \[\]/.test(dan));
  t('lời dặn tìm khen có bài viết của bé', dan.includes('I have a cat.'));
  t('trần token tìm khen là hằng xuất ra, nhỏ hơn mắt xích sửa',
    TOKEN_TIM_KHEN > 0 && TOKEN_TIM_KHEN < 700);

  /* Mắt xích 2 có HAI nhánh luật 1 — có danh sách khen thì phải bám vào nó. */
  const khong = loiDanSua(goi, [], [], []);
  const co = loiDanSua(goi, [], [], [{ cau: 'I have a cat.', vi: 'đúng mẫu câu' }]);
  t('không có danh sách khen → luật 1 như cũ', /Khen CỤ THỂ/.test(khong));
  t('có danh sách khen → luật 1 bắt bám vào danh sách',
    /KHÔNG thêm chỗ đáng khen nào ngoài danh sách/.test(co));
  t('danh sách khen đi vào lời dặn', co.includes('đúng mẫu câu'));
  /* Rỗng thì KHÔNG dựng dòng nào: nói "không có gì đáng khen" là mời nó bịa. */
  t('danh sách rỗng thì không dựng mục khen nào',
    !/CHỖ BÉ LÀM ĐƯỢC/.test(khong));
  t('hai nhánh cho hai lời dặn khác nhau', khong !== co);

  /* Khung vân tay phải gồm MỌI mắt xích, CẢ HAI nhánh của mắt xích 2. */
  const khung = khungCham(3, true);
  t('khung có mắt xích tìm khen', /KHÔNG SỬA, KHÔNG CHẤM ĐIỂM/.test(khung));
  t('khung có CẢ HAI nhánh luật 1 của mắt xích sửa',
    /Khen CỤ THỂ/.test(khung) && /KHÔNG thêm chỗ đáng khen nào ngoài danh sách/.test(khung));
  t('khung KHÔNG chứa chữ nào của bé',
    !khung.includes('I have a cat.') && !khung.includes('Tả con mèo'));

  /* Sửa lời dặn thì PHẢI tăng số phiên bản — chốt của §0. */
  t('PHIEN_BAN_MAU.chamviet đã tăng lên 3', PHIEN_BAN_MAU.chamviet >= 3);
  t('PHIEN_BAN_MAU có mẫu phanxu', PHIEN_BAN_MAU.phanxu >= 1);
}

console.log('\n── J · TẦNG MẠNG MÁY CON: KHÔNG BAO GIỜ NÉM, VÀ CÓ TRẦN GIỜ ──\n');

{
  const { nhoPhanXu, CHO_TOI_DA_MS, LOI_PHAN_XU } = await import('../src/mon/tienganh/lib/goiPhanXu.js');
  const du = { nghe: 'nain', dich: 'nine', canhTranh: 'name' };
  const tra = (d) => async () => ({ data: d });

  t('trần giờ là hằng xuất ra, và trong khoảng dùng được',
    CHO_TOI_DA_MS >= 1000 && CHO_TOI_DA_MS <= 10000);

  t('máy chủ trả −1 → chuyền đúng −1',
    (await nhoPhanXu(du, { goi: tra({ gan: 'canhTranh', dieuChinh: -1, nhatTri: true }) }))
      .dieuChinh === -1);
  t('máy chủ trả +1 → chuyền đúng +1',
    (await nhoPhanXu(du, { goi: tra({ gan: 'dich', dieuChinh: 1, nhatTri: true }) }))
      .dieuChinh === 1);

  /* Máy chủ chỉ trả ±1, nhưng mức điều chỉnh là con số DUY NHẤT từ ngoài mạng đi
     thẳng vào điểm của bé — nên nó không được tin một tầng. */
  t('máy chủ trả −7 (bất thường) → kẹp về −1',
    (await nhoPhanXu(du, { goi: tra({ gan: 'canhTranh', dieuChinh: -7 }) })).dieuChinh === -1);
  t('máy chủ trả chữ "−1" → kẹp về −1',
    (await nhoPhanXu(du, { goi: tra({ gan: 'canhTranh', dieuChinh: '-1' }) })).dieuChinh === -1);
  t('máy chủ trả rác → giữ',
    (await nhoPhanXu(du, { goi: tra({ gan: 'x', dieuChinh: 'abc' }) })).dieuChinh === 0);
  t('máy chủ trả rỗng → giữ',
    (await nhoPhanXu(du, { goi: tra(null) })).dieuChinh === 0);
  t('máy chủ báo chưa có khoá → giữ',
    (await nhoPhanXu(du, { goi: tra({ dieuChinh: 0, thieuKhoa: true }) })).dieuChinh === 0);

  /* ── KHÔNG BAO GIỜ NÉM — chốt của cả tệp ấy ──
     `NutNoi` gọi xong là hiện điểm cho bé; không ai bắt hộ. Một lời ném ở đây là
     một dòng đỏ trên màn hình bé về một việc bé không biết là có. */
  let coNem = false;
  try {
    await nhoPhanXu(du, { goi: () => { throw new Error('mất mạng'); } });
  } catch { coNem = true; }
  t('hàm gọi ném đồng bộ → KHÔNG ném ra ngoài', !coNem);
  try {
    await nhoPhanXu(du, { goi: async () => { throw new Error('máy chủ 500'); } });
  } catch { coNem = true; }
  t('hàm gọi ném bất đồng bộ → KHÔNG ném ra ngoài', !coNem);
  t('ném thì trả về mức 0',
    (await nhoPhanXu(du, { goi: async () => { throw new Error('x'); } })).dieuChinh === 0);

  /* Thiếu trường thì KHÔNG gọi mạng lần nào — chứng minh bằng con số 0. */
  let soGoi = 0;
  const dem = async () => { soGoi += 1; return { data: { dieuChinh: -1, gan: 'canhTranh' } }; };
  await nhoPhanXu({ nghe: '', dich: 'nine', canhTranh: 'name' }, { goi: dem });
  await nhoPhanXu({ nghe: 'nain', dich: '', canhTranh: 'name' }, { goi: dem });
  await nhoPhanXu({ nghe: 'nain', dich: 'nine', canhTranh: '' }, { goi: dem });
  /* Hai chữ trùng nhau: bác ngay tại máy con, đừng tốn một lượt để máy chủ bác hộ. */
  await nhoPhanXu({ nghe: 'dok', dich: 'Dog', canhTranh: 'dog' }, { goi: dem });
  t('gói thiếu / hai chữ trùng → KHÔNG gọi mạng lần nào', soGoi === 0);
  /* Đảo chiều: gói ĐỦ thì phải gọi đúng một lượt — nếu không thì con số 0 ở trên
     chỉ chứng minh rằng hàm này chẳng bao giờ gọi ai. */
  await nhoPhanXu(du, { goi: dem });
  t('đảo chiều — gói đủ thì gọi ĐÚNG một lượt', soGoi === 1);

  /* ── TRẦN GIỜ ──
     Lượt gọi treo thì nút "Đang chấm…" treo theo. Thử bằng một lời gọi không bao
     giờ nhả, và đo thời gian thật: phải về trước khi bé kịp bỏ đi. */
  const batDau = Date.now();
  const treo = await nhoPhanXu(du, { goi: () => new Promise(() => {}) });
  const ton = Date.now() - batDau;
  t('lời gọi treo → về với mức 0', treo.dieuChinh === 0);
  t(`về trong khoảng trần giờ (tốn ${ton} ms, trần ${CHO_TOI_DA_MS} ms)`,
    ton >= CHO_TOI_DA_MS - 100 && ton < CHO_TOI_DA_MS + 1500);
  t('đếm được lượt quá giờ', LOI_PHAN_XU.quaGio >= 1);

  /* Trả lời MUỘN (sau trần giờ) không được đổi gì nữa — bé đã thấy điểm rồi. */
  const muon = await nhoPhanXu(du, {
    goi: () => new Promise((xong) => setTimeout(
      () => xong({ data: { dieuChinh: -1, gan: 'canhTranh' } }), CHO_TOI_DA_MS + 400)),
  });
  t('trả lời tới SAU trần giờ thì bị bỏ, không đổi điểm', muon.dieuChinh === 0);
}

console.log(`\n${pass} PASS · ${fail} FAIL\n`);
process.exit(fail ? 1 : 0);
