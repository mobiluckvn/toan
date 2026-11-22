/**
 * CỔNG · PHÂN LOẠI LƯỢT CỦA BÉ (mẫu Routing, việc V2).
 *
 * Trước bản này cô giáo máy nhận MỘT lời dặn cho mọi tình huống, nên lượt nào cũng
 * ra một lời khen chung chung rồi đi tiếp — kể cả lượt bé vừa trượt. Nay việc chọn
 * lời dặn là việc của CODE, và code thì đếm được.
 *
 * Tệp này canh năm thứ, cả năm chạy bằng `node` không cần mạng:
 *   1. chín nhãn, mỗi nhãn ra đúng nhãn ấy — kèm `doTin` và `chiTiet`;
 *   2. chín nhãn có chín lời dặn, không nhãn nào rỗng, không lời nào quá trần;
 *   3. lời dặn tổng (chung + nhãn) vẫn dưới trần máy chủ với VỐN THẬT lớp 3·5;
 *   4. nhãn SAI thì việc của lượt GIỮ NGUYÊN câu bé đang tập — và có trần;
 *   5. chữ của bé KHÔNG lọt vào vân tay prompt.
 *
 * ⚠ Phép canh thứ 5 soi TÍNH CHẤT, không soi chính tả: nó đem từng giá trị trong
 * `chiTiet` đi tìm trong phần `locKhung` còn giữ lại. Soi theo tên dòng (`CHILD:`)
 * thì thêm một nhãn mới viết dòng riêng kiểu khác là cổng vẫn xanh — đúng cái bẫy
 * "cổng ghim chính tả thay vì tính chất".
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  NHAN, NHAN_GIU_VIEC, NHAN_TRONG_KICH_BAN, nhanLuot, chotTin,
  TIN_CHAC, TIN_DOAN, NGUONG_TIN,
} from '../src/mon/tienganh/lib/nhanluot.js';
import {
  LOI_DAN_THEO_NHAN, dongTheoNhan, DAN_NHAN_TOI_DA_CHU,
} from '../src/mon/tienganh/lib/loidan_nhan.js';
import {
  vonTu, loiDan, viecTiepTheo, XUNG_HO_CAM, SUA_TOI_DA, KIEU_VIEC, cauHopLe,
} from '../src/mon/tienganh/lib/phongnoi.js';
import { locKhung, PHIEN_BAN_MAU } from '../functions/src/vantay.js';
import { TOI_DA_CHU_LOI_DAN } from '../functions/src/luyennoi.js';

const bai = (id, tu, cau) => ({
  id,
  title: `Unit ${id}`,
  knowledgeCore: {
    vocabulary: tu.map((t) => ({ tu: t, nghia: `nghĩa ${t}`, ipa: `/${t}/` })),
    mauCauDs: cau.map((c) => (Array.isArray(c)
      ? { cau: c[0], congThuc: c[1], dungDe: 'để nói' }
      : { cau: c, congThuc: c, dungDe: 'để nói' })),
  },
});
const B01 = bai('B01', ['ball', 'bike', 'book'], [["Hi, I'm Bill.", "Hi, I'm + [Name]."]]);
const VON = vonTu({ baiNay: B01 });

/* ═══════════ 1 · CHÍN NHÃN ═══════════ */

test('chín nhãn, mỗi nhãn một ca — nhãn đúng, doTin đủ, chiTiet đúng', () => {
  const ca = [
    ['lịch sử chưa có lượt bé nào được chấm', null, NHAN.moDau],
    ['bấm nút mà không nói gì', { chu: '', diem: 0, mau: 'Hello!' }, NHAN.imLang],
    ['nói trắng khoảng', { chu: '   ', diem: 0, mau: 'Hello!' }, NHAN.imLang],
    ['nói đúng', { chu: 'hello', diem: 9, mau: 'Hello!' }, NHAN.dung],
    ['sót chữ', { chu: 'im bo', diem: 4, thieu: ['hi'], mau: "Hi, I'm Bo." }, NHAN.thieuTu],
    ['đủ chữ mà đảo thứ tự', { chu: 'bo im hi', diem: 4, thieu: [], mau: "Hi, I'm Bo." }, NHAN.saiThuTu],
    ['nhầm sang chữ khác của bài', { chu: 'duck', diem: 3, thieu: [], mau: 'dog', nhamThanh: 'duck' }, NHAN.nhamTu],
    ['nói tiếng Việt', { chu: 'cô ơi con không biết', diem: 0, mau: 'Hello!' }, NHAN.tiengViet],
    ['hỏi lại', { chu: 'cô ơi dog là gì?', diem: 0, mau: 'Hello!' }, NHAN.hoiLai],
    ['nói một thứ không ăn vào việc nào', { chu: 'xyz zzz', diem: 0, thieu: [], mau: null }, NHAN.lacDe],
  ];
  for (const [ten, luotBe, mong] of ca) {
    const kq = nhanLuot(luotBe, { von: VON });
    assert.equal(kq.nhan, mong, `${ten}: ra nhãn "${kq.nhan}"`);
    assert.ok(kq.doTin >= TIN_DOAN, `${ten}: doTin ${kq.doTin} thấp hơn ${TIN_DOAN}`);
  }
  /* `chiTiet` là thứ lời dặn PHẢI trích lại được — thiếu nó thì lời sửa quay về
     chung chung, đúng chỗ V2 sinh ra để chữa. */
  const t = nhanLuot({ chu: 'im bo', diem: 4, thieu: ['hi'], mau: "Hi, I'm Bo." }, { von: VON });
  assert.deepEqual(t.chiTiet.thieu, ['hi']);
  assert.equal(t.chiTiet.dich, "Hi, I'm Bo.");
  assert.equal(t.chiTiet.beNoi, 'im bo');
  const n = nhanLuot({ chu: 'duck', diem: 3, mau: 'dog', nhamThanh: 'duck' }, { von: VON });
  assert.equal(n.chiTiet.nham, 'duck');
  assert.equal(n.chiTiet.dich, 'dog');
});

/**
 * ⚠ "cô ơi" KHÔNG ĐƯỢC LÀM DẤU HIỆU HỎI LẠI, dù bản nháp §7 có ghi.
 * Hai ví dụ của chính bản rà đều mở đầu bằng "cô ơi" — một cái hỏi, một cái không.
 * Thứ có ở CẢ HAI bên thì không phân biệt được bên nào; ghim nó vào là nhãn
 * `tiengViet` chết hẳn, vì bé sáu tuổi gọi "cô ơi" trước gần như mọi câu.
 */
test('"cô ơi" không phải dấu hiệu hỏi — dấu hiệu là CÂU HỎI', () => {
  const n = (chu) => nhanLuot({ chu, diem: 0, mau: 'Hello!' }, { von: VON }).nhan;
  assert.equal(n('cô ơi con không biết'), NHAN.tiengViet);
  assert.equal(n('cô ơi con mệt rồi'), NHAN.tiengViet);
  assert.equal(n('cô ơi dog là gì?'), NHAN.hoiLai);
  assert.equal(n('dog nghĩa là gì'), NHAN.hoiLai);
  assert.equal(n('con nói thế nào ạ'), NHAN.hoiLai);
});

test('lượt CHƯA CHẤM ĐƯỢC không bị vu là đảo thứ tự', () => {
  /* `diem == null` ở những bước không có câu mẫu để so (bé kể tự do). Để nó lọt
     xuống nhánh `saiThuTu` là cô đi sửa thứ tự của một câu chẳng ai đặt ra. */
  const kq = nhanLuot({ chu: 'i like my school', diem: null, mau: 'Hello!' }, { von: VON });
  assert.equal(kq.nhan, NHAN.lacDe);
});

test('chotTin HẠ nhãn yếu về lacDe — gọi thẳng, không chờ nhánh thật', () => {
  /* Với chín nhánh hiện có thì hàm này không bao giờ đổi được nhãn nào (nhánh thấp
     nhất là 0,6 > 0,5). Gọi thẳng để nó đừng thành mã chết: thêm một nhánh đoán
     mới là nó có việc ngay, và lúc ấy phải biết nó còn chạy đúng. */
  const ha = chotTin({ nhan: NHAN.nhamTu, doTin: 0.2, chiTiet: { nham: 'duck' } });
  assert.equal(ha.nhan, NHAN.lacDe);
  assert.equal(ha.haTu, NHAN.nhamTu, 'phải nói ra nó vừa hạ từ nhãn nào');
  assert.equal(chotTin({ nhan: NHAN.dung, doTin: TIN_CHAC }).nhan, NHAN.dung);
  assert.ok(TIN_DOAN > NGUONG_TIN, 'nhánh đoán phải còn trên ngưỡng, không thì mọi nhãn về lacDe');
});

/* ═══════════ 2 · CHÍN LỜI DẶN ═══════════ */

const CTX = {
  beNoi: 'im bo', dich: "Hi, I'm Bo.", thieu: ['hi'], nham: 'duck', tenBe: 'Lan',
};

test('chín nhãn có chín lời dặn, không nhãn nào rỗng', () => {
  assert.deepEqual(
    Object.keys(LOI_DAN_THEO_NHAN).sort(), Object.keys(NHAN).sort(),
    'khoá lệch nhau → một nhãn không có lời dặn, và lượt ấy rơi về chuỗi rỗng câm',
  );
  for (const nhan of Object.keys(NHAN)) {
    const s = dongTheoNhan(nhan, CTX);
    assert.equal(typeof s, 'string');
    assert.ok(s.trim().length > 40, `nhãn ${nhan}: lời dặn ngắn bất thường`);
  }
  assert.equal(dongTheoNhan('mot-nhan-chua-co', CTX), '',
    'nhãn lạ phải ra chuỗi rỗng, KHÔNG được ném — một nhãn khai thiếu không đáng làm bé mất lượt nói');
});

test('mỗi lời dặn: dưới trần, một việc duy nhất, không gọi bé sai', () => {
  for (const nhan of Object.keys(NHAN)) {
    const s = dongTheoNhan(nhan, CTX);
    assert.ok(s.length <= DAN_NHAN_TOI_DA_CHU,
      `nhãn ${nhan}: ${s.length} ký tự, quá trần ${DAN_NHAN_TOI_DA_CHU}`);
    /* MỘT việc cho một lượt — bé sáu tuổi không giữ được ba việc cùng lúc. */
    assert.match(s, /\bONE\b|\bone\b/, `nhãn ${nhan}: không nói rõ CHỈ MỘT việc`);
    /* ⚠ Soi theo TIẾNG, không theo chuỗi con: "them" · "remember" · "temple" đều
       chứa "em". Soi bằng `includes` là cổng bắt oan rồi ép người ta viết vòng
       vèo cho cổng xanh — cùng bẫy với `cong-ghim-chinh-ta-thay-vi-tinh-chat`.
       Dùng đúng phép so của `loiVietHopLe`. */
    for (const x of XUNG_HO_CAM) {
      assert.ok(!new RegExp(`(?<![\\p{L}])${x}(?![\\p{L}])`, 'iu').test(s),
        `nhãn ${nhan}: gọi bé bằng "${x}"`);
    }
  }
});

test('lời dặn theo nhãn KHÔNG mang bảng vốn — bảng vốn ở khối chung', () => {
  /* Lặp bảng vốn vào đây là lời dặn phình gấp đôi, và hai bản sớm muộn lệch nhau. */
  for (const nhan of Object.keys(NHAN)) {
    const s = dongTheoNhan(nhan, CTX);
    for (const t of ['ball', 'bike', 'book']) {
      assert.ok(!s.includes(t), `nhãn ${nhan} lọt từ vựng "${t}" — bảng vốn phải ở khối chung`);
    }
  }
});

/* ═══════════ 3 · LỜI DẶN TỔNG VẪN DƯỚI TRẦN MÁY CHỦ ═══════════ */

const _ct = JSON.parse(readFileSync(
  new URL('../public/content/chuong_trinh.json', import.meta.url), 'utf8'));
const QUYEN_TA = Object.values(_ct.chuongTrinh)
  .filter((c) => c.mon === 'tienganh').map((c) => c.ma);
const baiTrong = (ma, id) => JSON.parse(readFileSync(
  new URL(`../public/content/${ma}/${id}.json`, import.meta.url), 'utf8'));

test('lời dặn tổng dưới trần máy chủ với VỐN THẬT, kể cả lúc mở rộng hết', () => {
  /* ⚠ Phải thử ở chế độ MỞ RỘNG (`daDat: true`): lúc ấy vốn từ gộp thêm ba unit cũ
     và cả bài tiên quyết, tức lời dặn DÀI NHẤT. Thử bằng một bài lẻ ở chế độ hẹp
     là thử đúng cái ca không bao giờ vỡ. */
  let dai = 0; let cho = '';
  for (const ma of QUYEN_TA) {
    const ds = JSON.parse(readFileSync(
      new URL(`../public/content/${ma}/kichban_noi.json`, import.meta.url), 'utf8'))
      .map((k) => k.bai.replace('DL:', 'DL_').replace(/\./g, '_'));
    const moi = ds.map((id) => baiTrong(ma, id));
    for (let i = 0; i < moi.length; i += 1) {
      const von = vonTu({
        /* `baiTQ` = mọi bài khác của quyển: cận trên của tiên quyết. Bản cũ không
           đắp tiên quyết nên chưa bao giờ thử ca dài nhất (đo ra gần 14.000 ký tự
           trước khi `vonTu` có trần `TIEN_QUYET_TOI_DA`). */
        baiNay: moi[i], baiCu: moi.slice(0, i), baiTQ: moi.filter((_, j) => j !== i),
        daDat: true, datCu: () => true,
      });
      for (const nhan of Object.keys(NHAN)) {
        const d = loiDan({
          von, tenBe: 'Lan', lop: Number(ma[2]) || 1, nhan, chiTiet: CTX,
          viec: viecTiepTheo({ von, lichSu: [], nhan }),
          hoSo: { thich: von.loi.tu[0]?.tu, mucNam: 'yeu' },
          unit: { ten: 'x', muc_tieu: 'y', tinh_huong: 'z' },
        });
        if (d.length > dai) { dai = d.length; cho = `${ma}/${moi[i].id}/${nhan}`; }
        assert.ok(d.length <= TOI_DA_CHU_LOI_DAN,
          `${ma}/${moi[i].id} nhãn ${nhan}: lời dặn ${d.length} ký tự, quá trần ${TOI_DA_CHU_LOI_DAN}`);
      }
    }
  }
  assert.ok(dai > 1000, 'lời dặn ngắn bất thường — có phải đã lọc mất cả khối luật?');
  /* In ra để lần sau còn biết còn dư bao nhiêu chỗ. */
  assert.ok(dai < TOI_DA_CHU_LOI_DAN, `dài nhất: ${dai} ký tự ở ${cho}`);
});

/* ═══════════ 4 · NHÃN SAI THÌ GIỮ NGUYÊN CÂU BÉ ĐANG TẬP ═══════════ */

const luotCo = (en) => ({ vai: 'may', chu: en, en, vi: 'x', buoc: 'mau' });
const luotBe = (o) => ({ vai: 'be', chu: 'x', diem: 4, mau: "Hi, I'm Bo.", thieu: ['hi'], ...o });

test('nhãn thieuTu → việc của lượt GIỮ NGUYÊN câu bé đang tập', () => {
  const lichSu = [luotCo("Hi, I'm Bo."), luotBe({})];
  const v = viecTiepTheo({ von: VON, lichSu, nhan: NHAN.thieuTu });
  assert.equal(v.kieu, KIEU_VIEC.mau);
  /* Câu đích là `luotBe.mau` — ĐÚNG câu bé đang cố nói, không phải câu cô vừa nói.
     Hai thứ ấy khác nhau ở mọi bước hỏi–đáp: cô hỏi, bé phải đáp. */
  assert.equal(v.mau.cau, "Hi, I'm Bo.");
  assert.equal(v.mau.congThuc, null, 'không có công thức thì không ai điền bừa vào');
  assert.equal(v.giuViec, true);

  /* Không có nhãn thì vẫn xoay vòng như cũ — V2 không được đổi hành vi cũ. */
  const cu = viecTiepTheo({ von: VON, lichSu });
  assert.equal(cu.giuViec, undefined);
});

test('BẢY nhãn giữ việc, HAI nhãn đi tới — việc chỉ tiến khi bé nói đúng', () => {
  assert.equal(NHAN_GIU_VIEC.size, 7);
  for (const n of [NHAN.dung, NHAN.moDau]) {
    assert.ok(!NHAN_GIU_VIEC.has(n), `${n} phải được đi tới việc mới`);
  }
  const lichSu = [luotCo("Hi, I'm Bo."), luotBe({})];
  for (const n of NHAN_GIU_VIEC) {
    assert.equal(viecTiepTheo({ von: VON, lichSu, nhan: n })?.giuViec, true, `nhãn ${n}`);
  }
  /* `dung` thì KHÔNG giữ — giữ lại là bé nói đúng rồi vẫn phải nói lại. */
  assert.equal(viecTiepTheo({ von: VON, lichSu, nhan: NHAN.dung })?.giuViec, undefined);
});

test('GIỮ VIỆC CÓ TRẦN — trượt quá SUA_TOI_DA thì nhường đường cho vòng luyện', () => {
  /* ⚠ Đây là cái bẫy nhánh kịch bản đã sập một lần: bé đuối thì kịch bản đứng yên,
     lượt sửa chen lên trước, và cả hai mươi phút chỉ còn một câu — "mười lượt liền
     đều là Hello!" (ghi ở `buocSua`). Giữ việc vô hạn là dựng lại đúng cái bẫy ấy. */
  const ds = [luotCo("Hi, I'm Bo.")];
  for (let n = 1; n <= SUA_TOI_DA + 2; n += 1) {
    ds.push(luotBe({}));
    const v = viecTiepTheo({ von: VON, lichSu: ds, nhan: NHAN.thieuTu });
    if (n <= SUA_TOI_DA) {
      assert.equal(v.giuViec, true, `lượt trượt thứ ${n}: còn trong trần, phải giữ`);
    } else {
      assert.notEqual(v.giuViec, true,
        `lượt trượt thứ ${n}: quá trần ${SUA_TOI_DA} mà vẫn giữ — bé bị kẹt một câu`);
    }
    ds.push(luotCo("Hi, I'm Bo."));
  }
});

/* ═══════════ 5 · CHỮ CỦA BÉ KHÔNG LỌT VÀO VÂN TAY ═══════════ */

test('mọi giá trị trong chiTiet đều bị locKhung bỏ khỏi khung', () => {
  /* Soi TÍNH CHẤT: đem từng mẩu dữ liệu của bé đi tìm trong phần khung còn giữ
     lại. Không soi tên dòng — thêm một nhãn mới viết dòng riêng kiểu khác thì phép
     soi theo tên vẫn xanh, còn phép soi này thì đỏ ngay. */
  const rieng = {
    beNoi: 'con noi im bo roi', dich: 'Hi, I am Bobby.', thieu: ['hithere'],
    nham: 'duckling', tenBe: 'Quynhanh',
  };
  for (const nhan of Object.keys(NHAN)) {
    const khung = locKhung(dongTheoNhan(nhan, rieng));
    for (const [k, v] of Object.entries(rieng)) {
      for (const mau of (Array.isArray(v) ? v : [v])) {
        assert.ok(!khung.includes(mau),
          `nhãn ${nhan}: khung còn giữ "${mau}" (từ chiTiet.${k}) — vân tay sẽ đổi theo bé`);
      }
    }
    /* Nhưng TÊN NHÃN phải còn lại: mất nó thì chín nhánh ra cùng một vân tay, và
       bảng so ΔC (V8) không phân biệt được nhánh nào dạy tốt hơn. */
    assert.match(khung, new RegExp(`TURN TYPE: ${nhan}`),
      `nhãn ${nhan}: tên nhãn bị lọc mất, ΔC sẽ gom chín nhánh làm một`);
  }
});

test('hai bé khác nhau, cùng nhãn → CÙNG một khung', () => {
  const mk = (nham, beNoi) => dongTheoNhan(NHAN.nhamTu, { nham, beNoi, dich: 'dog' });
  assert.equal(locKhung(mk('duck', 'con noi duck')), locKhung(mk('cat', 'con noi cat')));
});

test('sửa lời dặn đáng kể thì PHIEN_BAN_MAU phải tăng', () => {
  /* Luật 7 · 8 · 8b rời khối chung, 8c mang số 7, hai luật cuối lùi số — khung đổi
     thật, nên bảng so ΔC không được gom lượt mẫu 2 lẫn với mẫu 1. */
  assert.ok(PHIEN_BAN_MAU.luyennoi >= 2,
    'khối luật của loiDan đã đổi mà phiên bản mẫu vẫn là 1');
});

test('khối chung KHÔNG còn luật 7·8·8b, và số luật liền mạch', () => {
  const src = readFileSync(
    new URL('../src/mon/tienganh/lib/phongnoi.js', import.meta.url), 'utf8');
  /* Hai bản của cùng một luật là chỗ sửa một bên rồi hai bên nói khác nhau. */
  assert.ok(!/'8b\./.test(src), 'luật 8b còn ở khối chung — nay nó thuộc nhãn thieuTu/saiThuTu');
  assert.ok(!/'8c\./.test(src), 'luật 8c phải mang số 7, không còn là 8c');
  assert.ok(!/steer back to the words above/.test(src),
    'luật 7 cũ (lạc đề) còn ở khối chung — nay nó thuộc nhãn lacDe');

  const d = loiDan({ von: VON, tenBe: 'Lan', lop: 1 });
  const so = [...d.matchAll(/^(\d+)\. /gm)].map((m) => Number(m[1]));
  assert.deepEqual(so, [1, 2, 3, 4, 5, 6, 7, 8, 9],
    `số luật không liền mạch: ${so.join(',')} — bé không đọc, nhưng người sửa thì đọc`);
  /* Luật KHÔNG được xoá: vốn từ · một câu · JSON · xưng hô · trích đúng chữ. */
  assert.match(d, /Use ONLY these English words/);
  assert.match(d, /exactly ONE short English sentence/);
  assert.match(d, /Vietnamese pronouns are FIXED/);
  assert.match(d, /quote it EXACTLY/);
  assert.match(d, /Reply as JSON only/);
});

test('ba nhãn được ghép vào nhánh kịch bản, sáu nhãn thì không', () => {
  assert.equal(NHAN_TRONG_KICH_BAN.size, 3);
  for (const n of [NHAN.hoiLai, NHAN.tiengViet, NHAN.imLang]) {
    assert.ok(NHAN_TRONG_KICH_BAN.has(n), `${n} phải được ghép: kịch bản không có chỗ nào nói tới nó`);
  }
  for (const n of [NHAN.dung, NHAN.thieuTu, NHAN.saiThuTu, NHAN.nhamTu, NHAN.lacDe, NHAN.moDau]) {
    assert.ok(!NHAN_TRONG_KICH_BAN.has(n),
      `${n} KHÔNG được ghép: dongBuoc đã ra lệnh về câu ấy rồi, hai chỗ cùng ra lệnh là mô hình chọn bừa`);
  }
});

/* ═══════════ 6 · LƯỢT GIỮ VIỆC PHẢI GỠ LUẬT 4 ═══════════ */

/**
 * ĐO THẬT 09-10 với Groq, 27 lượt: bé sai thì KHÔNG LẦN NÀO (0/9) cô nhắc lại đúng
 * câu bé đang tập — cô đổi chữ trong ô. Bé cần nghe lại "It's my brother." thì cô
 * nói "It's my sister."
 *
 * Vì lời dặn tự chọi nhau: luật 4 nằm trong khối HARD RULES và viết thẳng "NEVER
 * say the same English sentence… Vary the word in the slot", còn dòng theo nhãn thì
 * đòi đọc lại NGUYÊN câu ấy. Mô hình chọn bên được gọi là "hard rule" — đúng theo
 * lời ta dặn. Lượt giữ việc phải GỠ luật 4 ra, bằng đúng cách `dongBuoc` đã làm
 * cho bước `sua`.
 *
 * ⚠ Và chỉ gỡ ở ĐÚNG lượt ấy. Gỡ luôn ở lượt thường là dựng lại cái bác bắt đầu
 * tiên: "nó cứ nói đi nói lại".
 */
test('lượt GIỮ VIỆC nói thẳng là nó thắng luật 4; lượt thường thì KHÔNG', () => {
  const lichSu = [luotCo("Hi, I'm Bo."), luotBe({})];
  const giu = loiDan({
    von: VON, tenBe: 'Lan', lop: 1, nhan: NHAN.thieuTu, chiTiet: CTX,
    viec: viecTiepTheo({ von: VON, lichSu, nhan: NHAN.thieuTu }),
  });
  assert.match(giu, /SAY IT AGAIN, unchanged/);
  assert.match(giu, /overrides HARD RULE 4/);
  assert.match(giu, /NEVER say the same English sentence/,
    'luật 4 vẫn phải còn trong khối chung — chỗ này gỡ nó ra, không xoá nó');

  /* Lượt thường: không được có lời gỡ nào. */
  const thuong = loiDan({
    von: VON, tenBe: 'Lan', lop: 1, nhan: NHAN.dung, chiTiet: CTX,
    viec: viecTiepTheo({ von: VON, lichSu, nhan: NHAN.dung }),
  });
  assert.ok(!/overrides HARD RULE 4/.test(thuong),
    'gỡ luật 4 ở lượt thường là dựng lại đúng cái bác bắt đầu tiên: "nó cứ nói đi nói lại"');
});

test('lời gỡ luật 4 nhắc ĐÚNG số luật đang có', () => {
  /* Luật chống lặp vừa đổi số một lần ở V2 (8c thành 7). Trỏ sai số thì lời gỡ
     không gỡ được gì, mà cổng vẫn xanh vì chuỗi "HARD RULE 4" vẫn ở đó. */
  const d = loiDan({ von: VON, tenBe: 'Lan', lop: 1 });
  const dong = d.split('\n').find((x) => /NEVER say the same English sentence/.test(x));
  assert.match(dong, /^4\. /, `luật chống lặp nay mang số khác: ${JSON.stringify(dong)}`);
});

/**
 * ⚠ CHỖ V1 VÀ V2 ĐÁNH NHAU, và nó chỉ lộ ra khi gọi mô hình thật.
 *
 * Đo 09-10: lời dặn đã nói thẳng "SAY IT AGAIN, unchanged" mà cô vẫn không lần nào
 * đọc lại đúng câu bé đang tập. Chỗ hỏng ở MÃ, không ở lời dặn: `soiCau` bác câu
 * trùng lượt trước (`bac: 'lap'`), rồi vòng gọi lại của V1 đọc lý do ấy và nhắc mô
 * hình "Say a DIFFERENT sentence — change the word in the slot" — tức ĐẨY nó đi
 * sai. Ba tầng đều làm đúng phận mình và cộng lại thành hỏng.
 */
test('lượt GIỮ VIỆC: luật chống lặp phải TẮT, nhưng chỉ luật ấy', () => {
  const src = readFileSync(
    new URL('../src/mon/tienganh/lib/goiPhongNoi.js', import.meta.url), 'utf8');
  assert.match(src, /viec\?\.giuViec \? '' : cauTruocThat/,
    'lượt giữ việc vẫn đem câu lượt trước đi so → câu đúng bị gạt vì "lặp"');
  /* Nhánh kịch bản KHÔNG được tắt theo: ở đấy không có `viec`, và luật chống lặp
     vẫn là thứ giữ cho cô đừng đọc mãi một câu. */
  assert.match(src, /cauTruoc: cauTruocThat/,
    'nhánh kịch bản phải giữ nguyên luật chống lặp');
  /* Và TẮT ĐÚNG MỘT LUẬT: vốn từ vẫn phải soi như cũ. */
  const von3 = vonTu({ baiNay: B01 });
  assert.equal(soiCauNgoai('I want chips.', von3), false,
    'tắt luật chống lặp không được kéo theo hàng rào vốn từ');
});

/* Vỏ nhỏ cho phép soi ngoài vốn — gọi `soiCau` với cùng tham số nhánh giữ việc. */
function soiCauNgoai(en, von) {
  return cauHopLe(en, { von, tenBe: 'Lan', cauTruoc: '' });
}

test('lượt giữ việc chỉ có MỘT dòng "THIS TURN:"', () => {
  /* Hai dòng cùng mở đầu `THIS TURN:` là hai lệnh ngang hàng, và mô hình không có
     cách nào biết dòng nào mới là việc của lượt. */
  const lichSu = [luotCo("Hi, I'm Bo."), luotBe({})];
  const d = loiDan({
    von: VON, tenBe: 'Lan', lop: 1, nhan: NHAN.thieuTu, chiTiet: CTX,
    viec: viecTiepTheo({ von: VON, lichSu, nhan: NHAN.thieuTu }),
  });
  const so = d.split('\n').filter((x) => /^THIS TURN:/.test(x.trim())).length;
  assert.equal(so, 1, `có ${so} dòng "THIS TURN:" cùng ra lệnh`);
  assert.match(d, /SAME TASK AS LAST TURN:/);
});
