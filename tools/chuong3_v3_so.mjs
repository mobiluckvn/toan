/**
 * SỐ LIỆU CHO CHƯƠNG 3 (bản viết lại) → docs/chuong3_v3_so.json
 *
 *     node tools/chuong3_v3_so.mjs
 *
 * Thầy hỏi: "Làm 01 phiên 01 cá nhân cụ thể sẽ như thế nào (một ví dụ minh hoạ)".
 * Tệp này dựng đúng một ví dụ như thế, và dựng bằng CHÍNH MÃ ĐANG CHẠY THẬT:
 *
 *     web/functions/src/bkt.js          cập nhật Bayes có cơ chế quên
 *     web/functions/src/ara.js          điều kiện hợp lệ của một cặp A-R-A
 *     web/functions/src/report.js       mệt mỏi, đường cong học, câu bế tắc
 *     src/mon/tienganh/lib/doThi.js     duyệt ngược / duyệt xuôi trên đồ thị
 *     src/mon/tienganh/lib/lantruyen.js độ ngờ, nút gốc rễ, ma trận trạng thái
 *     src/mon/tienganh/lib/chinhsach.js hàm chính sách π, vectơ S
 *     src/mon/tienganh/lib/zpd.js       xếp câu theo vùng phát triển gần
 *     src/mon/tienganh/lib/phudao.js    dựng bài phụ đạo
 *     src/mon/tienganh/lib/suKien.js    dựng bản ghi lượt trả lời
 *     src/mon/tienganh/lib/cefr.js      quy đổi phủ vốn sang thang năng lực
 *
 * ⚠ Bé trong ví dụ là BÉ GIẢ và chuỗi trả lời do tôi đặt — phải nói thẳng điều
 * ấy trong luận văn. Cái THẬT là: đồ thị, kho câu hỏi, công thức, ngưỡng, lược đồ
 * bản ghi, và mọi con số hệ thống tính ra từ chuỗi ấy. Sai công thức thì số ở đây
 * sai theo, nên đây là bằng chứng chứ không phải lời kể.
 */
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const W = (p) => path.join(GOC, p);

const { applyAttempt, quenDan, DEFAULT_PARAMS, MASTERY_THRESHOLD, NUA_DOI_NGAY } =
  await import(W('web/functions/src/bkt.js'));
const { capHopLe, deltaC, TOI_THIEU_CAP } = await import(W('web/functions/src/ara.js'));
const { metMoi, stuckItems, duongCongHoc, NGUONG_CHAM, TOI_THIEU_MOI_NUA } =
  await import(W('web/functions/src/report.js'));
const { duyetNguoc, baiCuaNut, nhanNut, lopNut, CANH_THAT } =
  await import(W('web/src/mon/tienganh/lib/doThi.js'));
const { nutGocRe, maTranTrangThai, congHuong, ALPHA, BETA, P_MAC_DINH, NGUONG_TRAN } =
  await import(W('web/src/mon/tienganh/lib/lantruyen.js'));
const { viecTiepCuaNut, viecTiepCuaBai, vectorS, SAI_LIEN_TIEP_MAC } =
  await import(W('web/src/mon/tienganh/lib/chinhsach.js'));
const { xepTheoZPD, nhomCua, NGUONG_THAO, NGUONG_YEU } =
  await import(W('web/src/mon/tienganh/lib/zpd.js'));
const { dungPhuDao, SO_CAU_PHU_DAO } = await import(W('web/src/mon/tienganh/lib/phudao.js'));
const { dungSuKien } = await import(W('web/src/mon/tienganh/lib/suKien.js'));
const { ghiDinhDang, xepDinhDang, TOI_THIEU_MAU } =
  await import(W('web/src/mon/tienganh/lib/hoso.js'));
const { bacCefr, cauMoTa, PHU_DAT, TOI_THIEU_NUT } =
  await import(W('web/src/mon/tienganh/lib/cefr.js'));

const DT = JSON.parse(readFileSync(W('web/public/content/tienganh/do_thi.json'), 'utf8'));
const doc = (id) => JSON.parse(readFileSync(
  W(`web/public/content/ta3/${id.replace(/[:.]/g, '_')}.json`), 'utf8'));

const NGAY = 86400000;
const T0 = Date.parse('2026-09-28T08:00:00+07:00');
const MAC = 'sp_g3_u13_2';                       // nút người học mắc
const BAI = 'DL:TA3.B13';
const IDS = ['DL:TA3.B03', 'DL:TA3.B04', 'DL:TA3.B08', 'DL:TA3.B09', 'DL:TA3.B13'];
const B = Object.fromEntries(IDS.map((i) => [i, doc(i)]));
const ra = {};

/* ══ 0 · QUY MÔ ĐỒ THỊ VÀ KHO CÂU HỎI ═══════════════════════════════════════ */
{
  const nut = DT.nut; const canh = DT.canh;
  const HOC = new Set(['vocabulary', 'vocabulary_item', 'grammar', 'pronunciation',
    'letter_sound', 'prior_knowledge', '?']);
  const loai = {}; for (const v of Object.values(nut)) loai[v.t || '?'] = (loai[v.t || '?'] || 0) + 1;
  const eLoai = {}; for (const c of canh) eLoai[c.loai || 'ban_do'] = (eLoai[c.loai || 'ban_do'] || 0) + 1;
  const tq = canh.filter((c) => CANH_THAT.has(c.loai || 'ban_do'));
  ra.doThi = {
    nut: Object.keys(nut).length,
    canh: canh.length,
    loaiNut: loai,
    loaiCanh: eLoai,
    canhTienQuyet: tq.length,
    xuyenLop: canh.filter((c) => c.xuyen_lop).length,
    coNhan: Object.values(nut).filter((v) => v.n).length,
    coBai: Object.values(nut).filter((v) => v.b).length,
    ngoaiLop: Object.values(nut).filter((v) => v.ngoai).length,
    hocDuoc: Object.values(nut).filter((v) => HOC.has(v.t || '?')).length,
    nutCoTienQuyet: new Set(tq.map((c) => c.truoc_khi)).size,
  };

  /* Kho câu hỏi: đếm trên chính tệp học liệu đã phát hành. */
  let tong = 0; const bac = {}; const theoNut = new Map();
  for (const q of ['ta1', 'ta2', 'ta3', 'ta4', 'ta5']) {
    for (const f of readdirSync(W(`web/public/content/${q}`))) {
      if (!/^DL_TA\d_B\d+\.json$/.test(f)) continue;
      const d = JSON.parse(readFileSync(W(`web/public/content/${q}/${f}`), 'utf8'));
      const goi = [];
      for (const [k, v] of Object.entries(d.practice?.pools || {})) {
        bac[k] = (bac[k] || 0) + v.length; goi.push(...v);
      }
      const as = d.assessment?.items || [];
      bac.assessment = (bac.assessment || 0) + as.length;
      goi.push(...as);
      tong += goi.length;
      for (const it of goi) theoNut.set(it.maNut, (theoNut.get(it.maNut) || 0) + 1);
    }
  }
  const phan = {};
  for (const v of theoNut.values()) phan[v] = (phan[v] || 0) + 1;
  ra.khoCau = {
    tong, bac, nutCoCau: theoNut.size, phanBo: phan,
    nutDuoi4Cau: [...theoNut.values()].filter((v) => v < 4).length,
  };
}

/* ══ 1 · TRẠNG THÁI TRƯỚC PHIÊN ═════════════════════════════════════════════ */
const LICH_SU = {            // nút → [chuỗi đúng/sai ở các buổi trước, số ngày trước phiên]
  sp_g3_u3_1: [[1, 1, 1, 1, 1], 24],
  sp_g3_u3_2: [[1, 1, 1], 24],
  sp_g3_u4_1: [[0, 0, 1], 21],
  sp_g3_u8_1: [[1, 1, 1, 1], 14],
  sp_g3_u9_1: [[1, 1, 1, 1, 1], 7],
  sp_g3_u9_2: [[1, 0, 1], 7],
};
const M = {};
for (const [ma, [ch, ng]] of Object.entries(LICH_SU)) {
  ch.forEach((ok, i) => {
    M[ma] = applyAttempt(M[ma], {
      correct: !!ok, ms: 5200 + i * 300, hintsUsed: ok ? 0 : 1, microId: baiCuaNut(DT, ma),
    }, () => T0 - ng * NGAY + i * 60000);
  });
}
ra.truocPhien = Object.entries(M).map(([ma, d]) => ({
  ma, nhan: nhanNut(DT, ma), bai: baiCuaNut(DT, ma),
  n: d.nAttempts, dung: d.nCorrect, p: d.p, thao: d.mastered,
  ngayCach: Math.round((T0 - d.lastSeen) / NGAY),
  pSauQuen: quenDan(d.p, (T0 - d.lastSeen) / NGAY),
}));

/* ══ 2 · MƯỜI MỘT LƯỢT CỦA PHIÊN ════════════════════════════════════════════ */
const LUOT = [
  ['C5', 'v_g3_u13_chair', 1, 6100, 0, 'chon'],
  ['C6', 'v_g3_u13_lamp', 1, 5400, 0, 'chon'],
  ['C7', 'v_g3_u13_table', 1, 4900, 0, 'chon'],
  ['C8', 'v_g3_u13_house', 1, 5200, 0, 'chon'],
  ['C1', 'v_g3_u13_bathroom', 1, 7300, 0, 'chon'],
  ['C2', 'v_g3_u13_bedroom', 1, 6800, 0, 'chon'],
  ['S1', 'sp_g3_u13_1', 1, 8800, 0, 'chon'],
  ['S2', 'sp_g3_u13_1', 1, 7300, 0, 'chon'],
  ['S5', MAC, 0, 12400, 0, 'chon'],
  ['S6', MAC, 0, 9900, 1, 'chon'],
  ['S7', MAC, 0, 15700, 2, 'chon'],
];
let hoSoDang = { chon: { dung: 9, tong: 12 }, go: { dung: 3, tong: 9 }, the: { dung: 5, tong: 8 } };
const dangDauPhien = xepDinhDang(hoSoDang);
let t = T0; const viec = [];
ra.luot = LUOT.map(([item, ma, ok, ms, goi, mode]) => {
  t += ms + 2500;
  const d = applyAttempt(M[ma], {
    correct: !!ok, ms, hintsUsed: goi, microId: BAI,
  }, () => t);
  M[ma] = d;
  hoSoDang = ghiDinhDang(hoSoDang, mode, !!ok);
  const cs = viecTiepCuaNut(d);
  viec.push({
    itemId: item, maNut: ma, maNutDs: [ma], ok: !!ok, tries: 1,
    hintsUsed: goi, ms, phase: 'practice', mode, khiNao: t,
  });
  return {
    item, nut: ma, dung: !!ok, ms, goi,
    pTruoc: d.pTruoc, p: d.p, delta: d.p - d.pTruoc,
    thao: d.mastered, saiLienTiep: d.saiLienTiep,
    viec: cs.viec, viSao: cs.vi_sao,
  };
});
const nhatKy = dungSuKien({
  learnerId: 'u_M3', maPhien: 'pm1x9k2a', microId: BAI, viec, quyen: 'ta3', now: () => t,
});
ra.banGhiMau = nhatKy[nhatKy.length - 1];
ra.maBanGhi = nhatKy.map((r) => r.id);
ra.hoSoNutMau = { ...M[MAC], unit: MAC, learnerId: 'u_M3', mon: 'tienganh', maNutDs: [MAC] };

const nutBai = [...new Set([
  ...['warmup', 'standard', 'challenge'].flatMap((k) => B[BAI].practice.pools[k] || [])
    .map((c) => c.maNut),
  ...B[BAI].assessment.items.map((i) => i.maNut),
])].filter(Boolean);
ra.nutCuaBai = nutBai;
ra.chinhSachBai = viecTiepCuaBai(M, nutBai);
ra.vectorS = vectorS({
  mucThao: M, maNutDs: nutBai,
  dinhDang: { dangManh: dangDauPhien[0]?.ma }, thich: 'ngôi nhà', bayGio: t,
});

/* ══ 3 · CHẨN ĐOÁN ══════════════════════════════════════════════════════════ */
const chon = nutGocRe(DT, M, MAC, { sauToiDa: 4, toiDa: 3 });
const daChon = new Set(chon.map((x) => x.ma));
ra.ungVien = duyetNguoc(DT, MAC, { sauToiDa: 4 }).map(({ ma, buoc }) => {
  const p = M[ma]?.p ?? null;
  const pd = p ?? P_MAC_DINH;
  const bo = pd >= NGUONG_THAO;
  return {
    ma, nhan: nhanNut(DT, ma) || '(không nhãn)', buoc, p,
    doNgo: (ALPHA ** buoc) * (1 - pd),
    bai: baiCuaNut(DT, ma),
    loai: bo ? 'loai' : (chon[0]?.ma === ma ? 'chon' : 'xet'),
    ghi_chu: bo ? 'LOẠI — đã đạt ngưỡng tinh thông'
      : (chon[0]?.ma === ma ? 'đích phụ đạo' : (daChon.has(ma) ? 'trong ba nút trả về' : 'xếp sau')),
  };
}).sort((a, b) => b.doNgo - a.doNgo);
ra.nutGocRe = chon.map((g) => ({ ...g, nhan: nhanNut(DT, g.ma), bai: baiCuaNut(DT, g.ma) }));

ra.manhDoThi = {
  nut: [{ ma: MAC, nhan: nhanNut(DT, MAC), p: M[MAC].p, buoc: 0, bai: baiCuaNut(DT, MAC) },
    ...duyetNguoc(DT, MAC, { sauToiDa: 4 }).map(({ ma, buoc }) => ({
      ma, nhan: nhanNut(DT, ma) || '(không nhãn)', p: M[ma]?.p ?? null, buoc,
      bai: baiCuaNut(DT, ma) || '—',
    }))],
  canh: DT.canh.filter((c) => CANH_THAT.has(c.loai || 'ban_do')),
};
ra.maTran = maTranTrangThai(DT, M, { nguong: 0.5, toiDa: 5 });

/* ══ 4 · GỢI Ý CAN THIỆP ════════════════════════════════════════════════════ */
const pTruocPD = M[chon[0].ma].p;
const pd = await dungPhuDao({
  dt: DT, mucThao: M, maNutMac: MAC, baiDs: IDS.map((i) => B[i]), goiLLM: null,
});
ra.phuDao = {
  nutGoc: pd.nutGoc, nhanGoc: nhanNut(DT, pd.nutGoc), baiGoc: pd.baiGoc,
  nguon: pd.nguon, luiVe: pd.luiVe,
  cau: pd.cau.map((c) => ({
    id: c.id, bac: c.bac ?? null, nut: c.maNut, text: c.text || '',
    dap: JSON.stringify(c.answerKey), format: c.format || null,
  })),
};
const ketQuaPD = [true, false, true, true];
ra.dienBienPhuDao = pd.cau.map((c, i) => {
  t += 9000;
  M[pd.nutGoc] = applyAttempt(M[pd.nutGoc], {
    correct: ketQuaPD[i], ms: 9000, hintsUsed: ketQuaPD[i] ? 0 : 1, microId: pd.baiGoc,
  }, () => t);
  return { item: c.id, dung: ketQuaPD[i], p: M[pd.nutGoc].p };
});
ra.deltaCGoc = { truoc: pTruocPD, sau: M[pd.nutGoc].p, delta: M[pd.nutGoc].p - pTruocPD };

ra.khungARA = {
  microId: BAI, maNutMac: MAC, nutGoc: pd.nutGoc, lam: true,
  viSao: `sai ${SAI_LIEN_TIEP_MAC} lần liên tiếp`,
  soCau: pd.cau.length, dung: ketQuaPD.filter(Boolean).length,
  itemTruoc: ['S5', 'S6', 'S7'], itemPhuDao: pd.cau.map((c) => c.id),
  nguon: pd.nguon, luiVe: pd.luiVe, tsBatDau: T0, tsKetThuc: t,
};
const capTrung = {
  truoc: { p: 0.093, itemIds: ['S5', 'S6', 'S7'] },
  sau: { p: 0.51, itemIds: ['S5', 'S7'] }, mauPrompt: 'phudao', phienBanMau: 1,
};
const capSach = {
  truoc: { p: 0.093, itemIds: ['S5', 'S6', 'S7'] },
  sau: { p: 0.42, itemIds: ['G1', 'G2'] }, mauPrompt: 'phudao', phienBanMau: 1,
};
ra.ara = {
  capTrung: { ...capHopLe(capTrung), deltaC: deltaC(capTrung) },
  capSach: { ...capHopLe(capSach), deltaC: deltaC(capSach) },
  soCauCuaNutMac: ['warmup', 'standard', 'challenge']
    .flatMap((k) => B[BAI].practice.pools[k] || [])
    .concat(B[BAI].assessment.items)
    .filter((c) => c.maNut === MAC || (c.maNutDs || []).includes(MAC)).length,
};

/* ══ 5 · PHIÊN KẾ TIẾP: XẾP LẠI THỨ TỰ CÂU ══════════════════════════════════ */
{
  const pool = B[BAI].practice.pools.warmup.slice(0, 10);
  const xep = xepTheoZPD(pool, M, hoSoDang);
  const ten = { 0: 'đang chông chênh', 1: 'chưa có số liệu', 2: 'yếu hẳn', 3: 'đã tinh thông' };
  ra.xepZPD = {
    goc: pool.map((c) => c.id),
    sau: xep.map((c) => c.id),
    dong: xep.map((c, i) => ({
      thuTu: i + 1, item: c.id, nut: c.maNut,
      p: M[c.maNut]?.p ?? null, nhom: ten[nhomCua(M[c.maNut]?.p)],
    })),
  };
}

/* ══ 6 · NHẬN BIẾT HÀNH VI TRÊN CHÍNH NHẬT KÝ PHIÊN ═════════════════════════ */
ra.hanhVi = {
  metMoi: metMoi(nhatKy),
  beTac: stuckItems(nhatKy),
  duongCong: duongCongHoc(nhatKy, M),
  hoSoDang: xepDinhDang(hoSoDang),
  nguongChamDan: NGUONG_CHAM, toiThieuMoiNua: TOI_THIEU_MOI_NUA, toiThieuMau: TOI_THIEU_MAU,
};

/* ══ 7 · CỘNG HƯỞNG XUÔI VÀ QUY ĐỔI PHỦ VỐN ════════════════════════════════ */
{
  const ch = congHuong(DT, M);
  ra.congHuong = {
    soNutDoi: Object.keys(ch).length,
    nguonThao: Object.entries(M).filter(([, d]) => d.p >= NGUONG_THAO).map(([k]) => k),
    tran: NGUONG_TRAN, beta: BETA,
    viDu: Object.entries(ch).slice(0, 4).map(([k, v]) => ({ ma: k, p: v })),
  };
  const k = bacCefr(DT, M);
  ra.phuVon = {
    banDo: k.banDo.map((b) => ({
      ma: b.ma, moTa: b.moTa, vung: b.vung, tong: b.tong, phu: b.phu,
      dangTin: b.dangTin, dat: b.dat,
    })),
    mucDat: k.mucDat ? k.mucDat.ten : null, cau: cauMoTa(k),
    tongNut: k.tongNut, coSo: k.coSo, phuDat: PHU_DAT, toiThieuNut: TOI_THIEU_NUT,
  };
}

/* ══ 8 · HẰNG SỐ ĐANG DÙNG THẬT ════════════════════════════════════════════ */
ra.hangSo = {
  ...DEFAULT_PARAMS, theta: MASTERY_THRESHOLD, thetaYeu: NGUONG_YEU,
  alpha: ALPHA, beta: BETA, nuaDoiNgay: NUA_DOI_NGAY,
  saiLienTiepMac: SAI_LIEN_TIEP_MAC, soCauPhuDao: SO_CAU_PHU_DAO,
  toiThieuCapARA: TOI_THIEU_CAP,
};
ra.docLuc = new Date().toISOString();

writeFileSync(W('docs/chuong3_v3_so.json'), `${JSON.stringify(ra, null, 1)}\n`, 'utf8');
console.log('→ docs/chuong3_v3_so.json');
console.log(`   đồ thị ${ra.doThi.nut} nút · ${ra.doThi.canh} cạnh · `
  + `${ra.doThi.canhTienQuyet} cạnh tiên quyết`);
console.log(`   kho câu ${ra.khoCau.tong} câu · ${ra.khoCau.nutCoCau} nút có câu`);
console.log(`   phiên ví dụ: ${ra.luot.length} lượt · nút mắc ${MAC} `
  + `p=${ra.luot[ra.luot.length - 1].p.toFixed(3)}`);
console.log(`   nút gốc rễ: ${ra.phuDao.nutGoc} (${ra.phuDao.baiGoc}) · `
  + `${ra.phuDao.cau.length} câu phụ đạo, nguồn ${ra.phuDao.nguon}`);
