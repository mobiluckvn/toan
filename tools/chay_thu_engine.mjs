/**
 * CHẠY THỬ ENGINE — bằng CHÍNH MÃ ĐANG CHẠY THẬT, không viết lại công thức.
 *
 *     node tools/chay_thu_engine.mjs            # in ra màn hình
 *     node tools/chay_thu_engine.mjs --json     # xuất JSON cho bộ dựng Excel
 *
 * Bác hỏi 23-08-2026: "Show cho mình Engine đang hoạt động thế nào?"
 *
 * ── VÌ SAO KHÔNG VẼ SƠ ĐỒ ──
 * Sơ đồ nói cái người vẽ TIN là đang xảy ra. Tệp này `import` thẳng
 * `functions/src/bkt.js`, `lib/zpd.js`, `lib/chinhsach.js`, `lib/lantruyen.js`,
 * `lib/onlai.js` — đúng những tệp máy chủ và máy con đang chạy — rồi cho một bé
 * giả đi qua một chuỗi lượt và IN SỐ RA. Sai công thức thì số ở đây sai theo, nên
 * nó là bằng chứng chứ không phải lời kể.
 *
 * ⚠ Bé ở đây là BÉ GIẢ, chuỗi lượt do tôi đặt. Cái THẬT là công thức và ngưỡng.
 */
import { bktUpdate, applyAttempt, quenDan, isMastered, DEFAULT_PARAMS, MASTERY_THRESHOLD, NUA_DOI_NGAY }
  from '../web/functions/src/bkt.js';
import { xepTheoZPD, nhomCua, NHOM, NGUONG_THAO, NGUONG_YEU }
  from '../web/src/mon/tienganh/lib/zpd.js';

import { viecTiepCuaNut, duocVuotAi, vectorS, VIEC, SAI_LIEN_TIEP_MAC }
  from '../web/src/mon/tienganh/lib/chinhsach.js';
import { nutGocRe, congHuong, ALPHA, BETA } from '../web/src/mon/tienganh/lib/lantruyen.js';
import { daySauKhiOn, BOX_NGAY } from '../web/src/mon/tienganh/lib/onlai.js';

/* Tên đọc được của bốn nhóm ZPD. `NHOM` là CHỈ SỐ ƯU TIÊN XẾP, không phải thang
   nặng–nhẹ: chông chênh đứng TRƯỚC vì đó đúng là VÙNG PHÁT TRIỂN GẦN — chỗ bé
   gần làm được. Nút bé đã thạo xếp cuối, nút bé chưa biết gì xếp giữa. */
const TEN_NHOM = Object.fromEntries(Object.entries(NHOM).map(([k, v]) => [v, k]));

const ra = { canh: [] };
const canh = (ten, dong) => { ra.canh.push({ ten, dong }); };
const so = (x) => (x == null ? '—' : (typeof x === 'number' ? x.toFixed(3) : String(x)));

/* ══ CẢNH 1 · MỘT NÚT, MƯỜI LƯỢT — P(L) đi thế nào ══════════════════════════ */
{
  const chuoi = [false, false, true, true, true, false, true, true, true, true];
  let doc; const dong = [];
  chuoi.forEach((dung, i) => {
    doc = applyAttempt(doc, { correct: dung, ms: 4200 + i * 130, hintsUsed: dung ? 0 : 1 },
      () => 1_700_000_000_000 + i * 60_000);
    dong.push({
      luot: i + 1,
      traLoi: dung ? 'đúng' : 'SAI',
      pTruoc: so(doc.pTruoc),
      p: so(doc.p),
      delta: so(doc.p - doc.pTruoc),
      thao: doc.mastered ? 'ĐÃ THẠO' : '',
      saiLienTiep: doc.saiLienTiep,
      rtTrungBinh: doc.msTrungBinh,
      goiTrungBinh: doc.goiTrungBinh,
    });
  });
  canh('1 · MỘT NÚT, MƯỜI LƯỢT — P(L) đổi ra sao', dong);
}

/* ══ CẢNH 2 · ĐƯỜNG CONG QUÊN — không học thì tụt về đâu ════════════════════ */
{
  const p0 = 0.92;
  const dong = [0, 3, 7, 14, 21, 30, 60].map((ngay) => ({
    ngayKhongDung: ngay,
    p: so(quenDan(p0, ngay)),
    conThao: isMastered(quenDan(p0, ngay)) ? 'còn thạo' : 'RỚT NGƯỠNG',
  }));
  canh(`2 · QUÊN DẦN (nửa đời ${NUA_DOI_NGAY} ngày, xuất phát P(L)=0,92)`, dong);
}

/* ══ CẢNH 3 · ZPD — xếp lại thứ tự câu theo mức thạo ════════════════════════ */
{
  const mucThao = {
    v_g5_u1_city: { p: 0.05 },        // chưa biết
    v_g5_u1_class: { p: 0.35 },       // yếu
    v_g5_u1_dolphin: { p: 0.62 },     // chông chênh
    v_g5_u1_pink: { p: 0.97 },        // đã thạo
  };
  const cauDs = [
    { id: 'C1', maNut: 'v_g5_u1_pink', format: 'chon' },
    { id: 'C2', maNut: 'v_g5_u1_city', format: 'chon' },
    { id: 'C3', maNut: 'v_g5_u1_dolphin', format: 'go' },
    { id: 'C4', maNut: 'v_g5_u1_class', format: 'chon' },
  ];
  const xep = xepTheoZPD(cauDs, mucThao, null);
  canh('3 · ZPD — thứ tự câu bé gặp', xep.map((c, i) => ({
    thuTu: i + 1,
    cau: c.id,
    nut: c.maNut,
    p: so(mucThao[c.maNut].p),
    nhom: TEN_NHOM[nhomCua(mucThao[c.maNut].p)],
  })));
}

/* ══ CẢNH 4 · CHÍNH SÁCH — cùng một nút, ba tình huống, ba việc khác nhau ═══ */
{
  const th = [
    ['mới gặp, chưa vững', { p: 0.30, saiLienTiep: 0 }],
    ['đã vững', { p: 0.96, saiLienTiep: 0 }],
    ['còn rất yếu', { p: 0.12, saiLienTiep: 0 }],
    [`sai ${SAI_LIEN_TIEP_MAC} lần liên tiếp`, { p: 0.28, saiLienTiep: SAI_LIEN_TIEP_MAC }],
    ['vững NHƯNG vừa sai 3 lần', { p: 0.96, saiLienTiep: SAI_LIEN_TIEP_MAC }],
  ];
  canh('4 · CHÍNH SÁCH π — hệ thống quyết định làm gì tiếp', th.map(([ten, m]) => {
    const v = viecTiepCuaNut(m);
    return {
      tinhHuong: ten, p: so(m.p), saiLienTiep: m.saiLienTiep,
      viecTiep: v.viec, viSao: v.vi_sao,
    };
  }));

  /* ⚠ VƯỢT ẢI XÉT Ở MỨC BÀI, KHÔNG PHẢI MỨC NÚT — và đòi ĐỦ BA ĐIỀU. Bản đầu
     của tệp này gọi `duocVuotAi(m)` với một tham số nên lúc nào cũng `false`;
     lỗi của bộ mô phỏng, không phải của engine. */
  const thao = { a: { p: 0.97 }, b: { p: 0.95 }, c: { p: 0.99 } };
  const chuaThao = { a: { p: 0.97 }, b: { p: 0.40 }, c: { p: 0.99 } };
  canh('4b · VƯỢT ẢI — xét ở mức BÀI, đòi đủ ba điều', [
    { dieuKien: 'đã đạt bài + đủ 3 nút + MỌI nút đều vững',
      ketQua: duocVuotAi(thao, ['a', 'b', 'c'], true) ? 'ĐƯỢC vượt ải' : 'không' },
    { dieuKien: 'đã đạt bài + đủ 3 nút nhưng MỘT nút còn yếu (b=0,40)',
      ketQua: duocVuotAi(chuaThao, ['a', 'b', 'c'], true) ? 'được' : 'KHÔNG — còn nút yếu' },
    { dieuKien: 'mọi nút đều vững nhưng CHƯA đạt bài',
      ketQua: duocVuotAi(thao, ['a', 'b', 'c'], false) ? 'được' : 'KHÔNG — chưa đạt bài' },
    { dieuKien: 'mọi nút vững nhưng bài chỉ có 2 nút (dưới mức tối thiểu 3)',
      ketQua: duocVuotAi(thao, ['a', 'b'], true) ? 'được' : 'KHÔNG — quá ít nút để tin' },
  ]);
}

/* ══ CẢNH 5 · LAN TRUYỀN CHẨN ĐOÁN — bé sai ở ngọn, gốc nằm đâu ═════════════ */
{
  const dt = {
    nut: {
      v_g1_u3_can: { n: 'can — cái lon' },
      v_g3_u10_football: { n: 'football — quả bóng đá' },
      sp_g3_u10_1: { n: 'I play football at break time.' },
      sp_g5_u7_1: { n: 'What school activity does he like?' },
    },
    canh: [
      { can: 'v_g3_u10_football', truoc_khi: 'sp_g3_u10_1', loai: 'ban_do' },
      { can: 'sp_g3_u10_1', truoc_khi: 'sp_g5_u7_1', loai: 'noi_bai' },
    ],
  };
  const mucThao = {
    sp_g5_u7_1: { p: 0.22 },          // bé đang sai ở ĐÂY
    sp_g3_u10_1: { p: 0.41 },
    v_g3_u10_football: { p: 0.12 },   // gốc thật sự yếu
  };
  const goc = nutGocRe(dt, mucThao, 'sp_g5_u7_1', { toiDa: 3 });
  canh('5 · LAN TRUYỀN NGƯỢC — bé mắc ở "sp_g5_u7_1" (p=0,22), gốc ở đâu',
    goc.map((g) => ({
      nutGoc: g.ma,
      nhan: dt.nut[g.ma]?.n || '',
      cachMayBuoc: g.buoc,
      p: so(g.p),
      diemNghiNgo: so(g.diem ?? g.p),
    })));
  canh(`5b · HAI HỆ SỐ (α=${ALPHA} lan ngược · β=${BETA} cộng hưởng xuôi)`, [
    { y: 'α — mỗi bước lùi về gốc, độ nghi ngờ nhân với α', giaTri: ALPHA },
    { y: 'β — bé thạo nút trên thì nút dưới được cộng thêm', giaTri: BETA },
    { y: 'cộng hưởng cho nút p=0,55 khi nút trên đã thạo', giaTri: so(congHuong(0.55, 1)) },
  ]);
}

/* ══ CẢNH 6 · LỊCH ÔN — hộp Leitner, đúng thì giãn, sai thì về đầu ══════════ */
{
  let the = { bac: 0, lan: 0 };
  const dong = [];
  [true, true, true, false, true].forEach((dung, i) => {
    the = daySauKhiOn(the, dung, () => 1_700_000_000_000 + i * 86_400_000);
    dong.push({
      luotOn: i + 1,
      ketQua: dung ? 'đúng' : 'SAI',
      bacMoi: the.bac,
      henLaiSau: `${BOX_NGAY[the.bac] ?? '?'} ngày`,
    });
  });
  canh(`6 · LỊCH ÔN NGẮT QUÃNG — các bậc ${BOX_NGAY.join(' / ')} ngày`, dong);
}

/* ══ CẢNH 7 · SIÊU VECTOR S = [C, T, P, M] ═════════════════════════════════ */
{
  const s = vectorS({
    mucThao: { v_g5_u1_dolphin: { p: 0.62, saiLienTiep: 1, lastSeen: 1_700_000_000_000 } },
    hoSoDang: { chon: { dung: 7, tong: 10 }, go: { dung: 2, tong: 9 } },
    soThich: 'dolphin',
    bayGio: 1_700_000_000_000 + 5 * 86_400_000,
  });
  canh('7 · SIÊU VECTOR S — bốn chiều luận văn đòi', [
    { chieu: 'C · Nhận thức', giaTri: JSON.stringify(s.C) },
    { chieu: 'T · Thời gian', giaTri: JSON.stringify(s.T) },
    { chieu: 'P · Sư phạm', giaTri: JSON.stringify(s.P) },
    { chieu: 'M · Động lực', giaTri: JSON.stringify(s.M) },
  ]);
}

/* ══ HẰNG SỐ ĐANG DÙNG THẬT ════════════════════════════════════════════════ */
canh('0 · HẰNG SỐ ENGINE (đọc thẳng từ mã đang chạy)', [
  { ten: 'P(L₀) — mức thạo ban đầu', giaTri: DEFAULT_PARAMS.L0 },
  { ten: 'P(T) — xác suất học được sau một lượt', giaTri: DEFAULT_PARAMS.T },
  { ten: 'P(S) — xác suất biết mà vẫn sai (slip)', giaTri: DEFAULT_PARAMS.slip },
  { ten: 'P(G) — xác suất không biết mà đoán trúng (guess)', giaTri: DEFAULT_PARAMS.guess },
  { ten: 'θ — ngưỡng coi là ĐÃ THẠO', giaTri: MASTERY_THRESHOLD },
  { ten: 'ngưỡng ZPD "đã thạo" / "yếu"', giaTri: `${NGUONG_THAO} / ${NGUONG_YEU}` },
  { ten: 'sai liên tiếp bao nhiêu thì gọi phụ đạo', giaTri: SAI_LIEN_TIEP_MAC },
  { ten: 'nửa đời của đường cong quên (ngày)', giaTri: NUA_DOI_NGAY },
  { ten: 'các bậc hộp ôn (ngày)', giaTri: BOX_NGAY.join(' / ') },
  { ten: 'ba việc chính sách', giaTri: Object.values(VIEC).join(' · ') },
]);

if (process.argv.includes('--json')) {
  console.log(JSON.stringify(ra));
} else {
  for (const c of ra.canh) {
    console.log(`\n══ ${c.ten}`);
    console.table(c.dong);
  }
}
