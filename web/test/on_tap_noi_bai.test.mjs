/* ═══════════ KỲ SÁT HẠCH TRỎ VỀ ĐÚNG BÀI ═══════════
 *
 * Bé làm sai một câu ôn tập thì màn hình chìa ra một nút "ôn lại bài này". Nút ấy
 * dẫn đi đâu là do mối nối `veBai` của câu quyết định — và mối nối ấy đã từng sai
 * suốt mà không ai biết.
 *
 * ── LỖI ĐÃ XẢY RA THẬT, HAI LẦN, CÙNG MỘT DÒNG HỌ ──
 *
 * 1. `ontap_lop4.py` suy mã bài từ SỐ BÀI CỦA SÁCH. Hồi sách còn đúng 44 bài thì
 *    hai thứ trùng nhau. Từ lúc tách bài làm video thì không còn trùng: chạy lại
 *    bộ dựng ấy đổi mối nối của 102 CÂU Ở CHÍN CHƯƠNG, câu hỏi quãng đường dẫn bé
 *    sang bài phân số. Không có gì kêu, vì hai đầu đều là mã hợp lệ.
 *
 * 2. Chương 10 tách bài 45 cũ thành bốn bài. Câu hỏi bán kính đường kính vẫn trỏ
 *    về mã B45, mà mã ấy nay là bài BỐN LOẠI GÓC. Bé sai câu hình tròn, bấm ôn
 *    lại, và được dẫn tới bài dạy góc nhọn góc tù.
 *
 * ── VÌ SAO PHÉP ĐẾM DƯỚI ĐÂY BẮT ĐƯỢC ──
 *
 * Không máy nào đọc hiểu được "câu này có hỏi đúng bài kia không". Nhưng khi một
 * câu trỏ nhầm sang bài khác thì luôn có MỘT BÀI BỊ BỎ TRỐNG — cả chương có ngần
 * ấy bài và ngần ấy câu, trỏ dồn vào một chỗ thì chỗ khác hụt. Phép ④ đếm đúng cái
 * hụt ấy, và nó chính là cách lỗi số 2 lộ ra.
 *
 * NGƯỠNG ĐẶT Ở ĐÚNG CHỖ DỮ LIỆU ĐANG ĐỨNG: cả 11 chương lớp 4 nay phủ 100%. Nên
 * đòi 100%, và từ nay chỉ được siết thêm chứ không được nới.
 */
import { test } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';

const GOC = path.resolve(import.meta.dirname, '..', '..');
const doc = (p) => JSON.parse(fs.readFileSync(path.join(GOC, p), 'utf8'));

/* Hai quyển khai mối nối bằng HAI TRƯỜNG KHÁC NHAU — lớp 4 dùng `veBai` (mảng, một
   câu trỏ được nhiều bài), lớp 2 dùng `diagnosesMicro` (một mã). Đọc cả hai rồi
   quy về một mảng, để phép soi bên dưới không phải biết quyển nào là quyển nào. */
const moiNoi = (q) => (q.veBai || []).map((x) => x.id)
  .concat(q.diagnosesMicro && !(q.veBai || []).length ? [q.diagnosesMicro] : []);

const QUYEN = [
  { ma: 'lop4', tienTo: 'DCR_KSN4_C', soKy: 11 },
  { ma: 'lop2', tienTo: 'DCR_KSN2_C', soKy: 11 },
];

for (const Q of QUYEN) {
const thuTu = doc(`data/${Q.ma}/thu_tu.json`).thuTu;
const chuongCua = new Map();
const tenCua = new Map();
for (const ma of thuTu) {
  const b = doc(`web/public/content/${Q.ma}/${ma.replace('DL:', 'DL_').replace(/\./g, '_')}.json`);
  chuongCua.set(ma, b.chuong);
  tenCua.set(ma, b.title);
}

const ky = fs
  .readdirSync(path.join(GOC, 'web/public/content/reviews'))
  .filter((f) => new RegExp(`^${Q.tienTo}\\d+\\.json$`).test(f))
  .map((f) => doc(`web/public/content/reviews/${f}`))
  /* Lớp 2 có thêm mấy "ải" xếp sau tám chương — chúng không thuộc chương nào nên
     phép ④ không áp được. Chỉ soi kỳ của chương thật. */
  .filter((d) => chuongCua.size && [...chuongCua.values()].includes(d.chapter))
  .sort((a, b) => a.chapter - b.chapter);

test(`${Q.ma} · có kỳ sát hạch chương`, () => {
  assert.ok(ky.length > 0, 'không thấy kỳ nào');
});

for (const k of ky) {
  const nhan = `${Q.ma} ch${k.chapter}`;
  const baiCuaChuong = thuTu.filter((m) => chuongCua.get(m) === k.chapter);

  /* ① Câu nào cũng phải có đường về. Không có thì nút "ôn lại bài này" chết câm. */
  test(`${nhan} · mọi câu đều có mối nối về bài`, () => {
    const trong = k.examA.filter((q) => !moiNoi(q).length).map((q) => q.qno);
    assert.deepEqual(trong, [], 'câu không có veBai');
  });

  /* ② Mã trỏ về phải là bài CÓ THẬT trong sổ thứ tự — đây là chỗ lỗi số 1 lọt qua,
     vì bộ dựng cũ tự soi bằng số bài của sách, tức là soi bằng chính cái đang sai. */
  test(`${nhan} · mọi mã trỏ về đều có trong thu_tu.json`, () => {
    const ma = k.examA.flatMap(moiNoi);
    const la = [...new Set(ma.filter((x) => !chuongCua.has(x)))];
    assert.deepEqual(la, [], 'trỏ về bài không có trong sổ');
  });

  /* ③ Và phải là bài CÙNG CHƯƠNG. Kỳ sát hạch chương 10 mà dẫn bé về chương 9 thì
     bé ôn xong vẫn không sửa được chỗ vừa sai. */
  test(`${nhan} · mọi mã trỏ về đều thuộc đúng chương này`, () => {
    const lac = [
      ...new Set(
        k.examA.flatMap(moiNoi).filter((x) => chuongCua.get(x) !== k.chapter),
      ),
    ];
    assert.deepEqual(lac, [], `trỏ ra ngoài chương ${k.chapter}`);
  });

  /* ④ PHÉP ĐÁNG GIÁ NHẤT: bài nào của chương cũng phải có ít nhất một câu hỏi tới.
     Bài không ai hỏi tới là bài bé học xong rồi không bao giờ được kiểm — mà thường
     nó trống vì có câu khác đã trỏ nhầm vào chỗ của nó. */
  test(`${nhan} · mọi bài của chương đều được ít nhất một câu hỏi tới`, () => {
    const tro = new Set(k.examA.flatMap(moiNoi));
    const thieu = baiCuaChuong.filter((m) => !tro.has(m))
      .map((m) => `${m} (${tenCua.get(m)})`);
    assert.deepEqual(thieu, [], 'bài không câu nào hỏi tới');
  });

  /* ⑤ Tên bài hiện trên nút phải đúng tên bài mình đang dẫn tới. Hai thứ này do hai
     nơi ghi, nên chúng lệch được — và bé đọc tên chứ không đọc mã. */
  test(`${nhan} · tên bài trên nút khớp với bài được trỏ về`, () => {
    const lech = k.examA
      .filter((q) => q.diagnosesMicro && q.trapName !== tenCua.get(q.diagnosesMicro))
      .map((q) => `câu ${q.qno}: "${q.trapName}" ≠ "${tenCua.get(q.diagnosesMicro)}"`);
    assert.deepEqual(lech, [], 'tên trên nút lệch tên bài');
  });
}
}
