/**
 * BẢNG XẾP HẠNG — tổng hợp thành tích của TOÀN BỘ học sinh thành MỘT document.
 *
 * ── ĐÂY LÀ TÀI LIỆU DUY NHẤT MỘT BÉ ĐỌC ĐƯỢC VỀ BÉ KHÁC ──
 * Cả app đóng theo luật "mỗi bé chỉ đọc dữ liệu của mình". Bảng này phá luật ấy có
 * chủ ý, nên nó phải là chỗ CẨN THẬN NHẤT của cả kho:
 *
 *   · KHÔNG email, KHÔNG số bài sai, KHÔNG "em đang tắc ở bài nào".
 *   · Tên hiện là BIỆT DANH con tự chọn. Chưa khai tên thì hiện "Bạn nhỏ lớp 3" —
 *     tuyệt đối không lấy tên tạm, vì tên tạm chính là phần trước @ của email bố mẹ
 *     (xem buildUserDoc). Đưa nó lên bảng là lộ email người lớn cho cả trường đọc.
 *
 * ── VÌ SAO KHÔNG XẾP THEO SỐ BÀI ĐÃ ĐẠT ──
 * Lớp 5 có 168 bài, lớp 2 có 33. Xếp chung một cột thì bé lớp 2 nằm đáy vĩnh viễn,
 * và bé vào sau không bao giờ đuổi kịp bé vào trước — nhìn một lần rồi thôi. Bảng
 * cộng dồn mãi mãi chỉ thưởng NGƯỜI ĐẾN SỚM, không thưởng NGƯỜI ĐANG CỐ.
 *
 * Nên có BA bảng, và điểm tính bằng SAO — thưởng cả nỗ lực lẫn thành tích:
 *
 *   🔥 tuần này   sao kiếm trong 7 ngày, ĐẶT LẠI mỗi tuần → ai cũng có cửa
 *   📅 chuỗi ngày số ngày học liên tiếp → bé chăm thắng được bé giỏi
 *   👑 tổng sao   cả chặng đường → bé đi đường dài
 *
 * Thuần hàm, không đụng Firestore — chạy test bằng node (test/xephang.test.mjs).
 */

/** Công thức sao. IN NGUYÊN VĂN LÊN MÀN HÌNH — bé thấy được mới tin là công bằng. */
export const SAO = {
  cauDung: 1,        // mỗi câu trả lời đúng
  baiDat: 10,        // mỗi bài học đạt
  huyHieu: 30,       // mỗi kỳ sát hạch chương qua được
  vongDau: 50,       // mỗi vòng đấu Mùa giải đạt
};

/**
 * Trần sao KIẾM TỪ CÂU TRẢ LỜI trong một ngày.
 *
 * Ba nguồn kia đều một-lần-một-mã (bài, chương, vòng đấu) nên không cày được. Riêng
 * câu trả lời đúng thì bé ngồi làm lại một bài luyện tập 50 lượt là leo lên đỉnh
 * bảng mà chẳng học thêm gì — và bé khác nhìn vào thì thấy bảng vô nghĩa.
 */
export const TRAN_SAO_NGAY = 60;

/** Múi giờ Việt Nam. Ranh giới NGÀY phải theo giờ con ngồi học, không theo UTC:
 *  bé học lúc 21h30 tối là 14h30 UTC — tính theo UTC thì hai buổi tối liền nhau
 *  rơi vào cùng một ngày, và chuỗi ngày đứng im dù bé học đều. */
const LECH_VN = 7 * 3600000;
export const ngayVN = (ts) => Math.floor((Number(ts) + LECH_VN) / 86400000);

/**
 * SAO KIẾM TRONG MỘT KHOẢNG.
 *
 * @param attempts  nhật ký đã lọc theo khoảng, mỗi lượt {correct, ts}
 * @param moc       [{at}] các mốc đạt được: bài · chương · vòng đấu
 */
export function saoTrongKhoang({ attempts = [], baiDat = [], huyHieu = [], vongDau = [] }) {
  /* Câu đúng: cộng theo NGÀY rồi mới chặn trần, không chặn trên tổng — bé học đều
     ba ngày, mỗi ngày 40 câu, thì phải được 120 chứ không phải 60. */
  const theoNgay = new Map();
  for (const a of attempts) {
    if (!a?.correct) continue;
    const d = ngayVN(a.ts);
    theoNgay.set(d, (theoNgay.get(d) || 0) + 1);
  }
  let sao = 0;
  for (const n of theoNgay.values()) sao += Math.min(n, TRAN_SAO_NGAY) * SAO.cauDung;

  sao += baiDat.length * SAO.baiDat;
  sao += huyHieu.length * SAO.huyHieu;
  sao += vongDau.length * SAO.vongDau;
  return sao;
}

/**
 * CHUỖI NGÀY HỌC LIÊN TIẾP.
 *
 * Đếm lùi từ HÔM NAY. Học hôm nay hoặc hôm qua thì chuỗi còn sống — cho phép lệch
 * một ngày, vì tính chặt theo "hôm nay" nghĩa là bé mở app lúc 8 giờ sáng đã thấy
 * chuỗi về 0 dù tối qua vừa học.
 */
export function chuoiNgay(attempts = [], now = Date.now()) {
  const ngay = new Set(attempts.map((a) => ngayVN(a.ts)).filter(Number.isFinite));
  if (!ngay.size) return 0;
  const homNay = ngayVN(now);
  let d = ngay.has(homNay) ? homNay : (ngay.has(homNay - 1) ? homNay - 1 : null);
  if (d === null) return 0;
  let n = 0;
  while (ngay.has(d)) { n++; d--; }
  return n;
}

/**
 * TÊN HIỆN TRÊN BẢNG.
 *
 * Thứ tự: biệt danh con tự chọn → tên con đã khai → "Bạn nhỏ lớp N".
 * KHÔNG bao giờ lùi về `displayName` khi `profileComplete` còn false: lúc ấy trường
 * đó là tên tạm máy chủ tự điền = phần trước @ của email.
 */
export function tenHien(u = {}) {
  const bd = String(u.bietDanh || '').trim();
  if (bd) return bd.slice(0, 24);
  const ten = String(u.displayName || '').trim();
  if (u.profileComplete && ten) return ten.slice(0, 24);
  return `Bạn nhỏ lớp ${u.grade || 5}`;
}

/** Xếp hạng: cùng điểm thì cùng hạng, hạng sau nhảy đúng số người đứng trên. */
export function xepHang(ds, diemCua) {
  const sap = ds.slice().sort((a, b) => diemCua(b) - diemCua(a)
    || String(a.ten).localeCompare(String(b.ten), 'vi'));
  let hang = 0, truoc = null;
  return sap.map((r, i) => {
    const d = diemCua(r);
    if (d !== truoc) { hang = i + 1; truoc = d; }
    return { ...r, hang };
  });
}

/**
 * Dựng bảng xếp hạng.
 *
 * @param roster   [{uid, displayName, bietDanh, grade, profileComplete}]
 * @param attempts nhật ký TRONG KHOẢNG, đã quy `ts` về mốc máy chủ
 * @param progress { uid: { microId: {pass, at} } }
 * @param hocBa    { uid: [{loai, giaTri:{pass|dat, at}}] }
 */
export function buildBangXepHang({
  roster = [], attempts = [], progress = {}, hocBa = {}, now = Date.now(), days = 7,
}) {
  const from = now - days * 86400000;
  const trongTuan = (t) => Number.isFinite(t) && t >= from && t <= now;
  const mocCua = (o) => Date.parse(o?.at || 0) || (typeof o?.at === 'number' ? o.at : 0);

  const theoEm = new Map(roster.map((r) => [r.uid, []]));
  for (const a of attempts) {
    const ds = theoEm.get(a.learnerId);
    if (ds) ds.push(a);                       // tài khoản đã xoá — không dựng dòng ma
  }

  const rows = roster.map((u) => {
    const nhat = theoEm.get(u.uid) || [];
    const bai = Object.values(progress[u.uid] || {}).filter((m) => m?.pass);
    const hb = hocBa[u.uid] || [];
    const chuong = hb.filter((x) => x.loai === 'chuong' && x.giaTri?.pass);
    const dau = hb.filter((x) => x.loai === 'dau' && x.giaTri?.dat);

    const trongKhoang = {
      attempts: nhat.filter((a) => trongTuan(a.ts)),
      baiDat: bai.filter((m) => trongTuan(mocCua(m))),
      huyHieu: chuong.filter((x) => trongTuan(mocCua(x.giaTri))),
      vongDau: dau.filter((x) => trongTuan(mocCua(x.giaTri))),
    };

    return {
      ma: u.uid,
      ten: tenHien(u),
      lop: u.grade || 5,
      saoTuan: saoTrongKhoang(trongKhoang),
      /* TỔNG SAO chỉ đếm THÀNH TÍCH TÍCH LUỸ, không cộng câu trả lời đúng: nhật ký
         chỉ giữ theo cửa sổ ngày nên cộng vào là con số tụt dần theo thời gian —
         một bảng "tổng" mà đi lùi thì bé không hiểu nổi. */
      saoTong: bai.length * SAO.baiDat + chuong.length * SAO.huyHieu + dau.length * SAO.vongDau,
      chuoi: chuoiNgay(nhat, now),
      baiTuan: trongKhoang.baiDat.length,
      cauTuan: trongKhoang.attempts.filter((a) => a.correct).length,
      baiDat: bai.length,
      huyHieu: chuong.length,
      vongDau: dau.length,
    };
  });

  const gan = (ds, khoa, diemCua) => {
    const h = new Map(xepHang(ds, diemCua).map((r) => [r.ma, r.hang]));
    for (const r of ds) r[khoa] = h.get(r.ma);
  };
  gan(rows, 'hangTuan', (r) => r.saoTuan);
  gan(rows, 'hangChuoi', (r) => r.chuoi);
  gan(rows, 'hangTong', (r) => r.saoTong);

  return {
    generatedAt: now,
    periodDays: days,
    soEm: rows.length,
    soEmCoHoc: rows.filter((r) => r.saoTuan > 0).length,
    cong: { ...SAO, tranNgay: TRAN_SAO_NGAY },
    rows,
  };
}
