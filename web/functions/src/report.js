import { layNguong, boNguong } from './nguong.js';
import { nguCanhLuot } from './bkt.js';
/**
 * SỔ PHỤ HUYNH — tổng hợp từ nhật ký thô thành MỘT document.
 * Bố mẹ mở app đọc 1 lần, thay vì quét hàng nghìn attempts.
 * Thuần hàm, có test (test/report.test.mjs).
 */

/** Gom các lượt trả lời trong khoảng thời gian */
export const inRange = (attempts, from, to) => attempts.filter((a) => a.ts >= from && a.ts <= to);

/**
 * Dòng ghi đủ tin cậy để tính THỜI GIAN.
 * Bản ghi cũ (v < 2) có `ms` tính từ lúc mở bài và cả loạt chung một mốc `ts` —
 * đem tính số phút học hay "câu làm lâu" là ra số sai. Nhật ký bất biến nên
 * không sửa được; chỉ có thể loại chúng ra khỏi thống kê thời gian.
 */
export const DU_TIN_CAY = (a) => (a?.v ?? 1) >= 2;

/**
 * SỐ PHÚT SUY RA — cộng khoảng cách giữa các lượt trả lời, nghỉ > 5 phút thì bỏ.
 *
 * ⚠ ĐÂY LÀ PHÉP CŨ, GIỮ LẠI CHO DỮ LIỆU CŨ. Nó đếm hụt nặng kể từ khi cả bốn quyển
 * chuyển sang video: phần giảng là 405 video, cộng lại 390,7 phút, mà xem video thì
 * con không bấm gì nên không một giây nào được đếm. Con xem trọn video sáu mươi lăm
 * giây rồi trả lời đúng ngay câu chốt thì phép này ra 0 phút. Nó còn bỏ luôn quãng
 * làm câu ĐẦU TIÊN (không có lượt nào đứng trước) và quãng sau câu cuối.
 *
 * Số ĐO THẬT nay do máy con ghi (`src/mon/toan/lib/dongHo.js`) rồi cộng dồn theo
 * ngày ở `hocBa/{uid}/muc` `loai='gio'`. Dùng `phutHoc()` bên dưới, nó tự chọn.
 */
export function minutesStudied(attempts, gapMs = 5 * 60 * 1000) {
  const ts = attempts.filter(DU_TIN_CAY).map((a) => a.ts).sort((x, y) => x - y);
  let total = 0;
  for (let i = 1; i < ts.length; i++) {
    const d = ts[i] - ts[i - 1];
    if (d > 0 && d <= gapMs) total += d;
  }
  return Math.round(total / 60000);
}

/**
 * Số phút học của một khoảng — LẤY SỐ ĐO THẬT khi có, không thì suy ra như cũ.
 *
 * Trả về cả `nguon` để màn hình nói thật với bố mẹ: `'do'` là máy con bấm giờ từng
 * bước (có tính cả lúc xem giảng), `'suyRa'` là ước lượng từ khoảng cách giữa các
 * câu trả lời và **chắc chắn thiếu phần xem giảng**. Hai con số khác nhau về bản
 * chất; trộn làm một rồi hiện chung một nhãn là nói dối bố mẹ.
 *
 * `soGio` là các tài liệu `loai='gio'` trong khoảng: [{ngay, giay, giayXem, giayLam}].
 */
export function phutHoc(attempts, soGio = [], { from = null, to = null } = {}) {
  const trong = soGio.filter((g) => {
    if (!g || typeof g.giay !== 'number') return false;
    const m = Date.parse(`${g.ngay}T00:00:00+07:00`);
    if (Number.isNaN(m)) return false;
    /* So theo NGÀY: một tài liệu là trọn một ngày, nên chỉ cần ngày ấy chạm khoảng. */
    return (from === null || m + 86399999 >= from) && (to === null || m <= to);
  });
  if (trong.length) {
    const giay = trong.reduce((s, g) => s + (g.giay || 0), 0);
    return {
      phut: Math.round(giay / 60),
      phutXem: Math.round(trong.reduce((s, g) => s + (g.giayXem || 0), 0) / 60),
      phutLam: Math.round(trong.reduce((s, g) => s + (g.giayLam || 0), 0) / 60),
      nguon: 'do',
      soNgayCoHoc: trong.filter((g) => (g.giay || 0) > 0).length,
    };
  }
  return {
    phut: minutesStudied(attempts),
    phutXem: null, phutLam: null,
    nguon: 'suyRa',
    soNgayCoHoc: new Set(attempts.filter(DU_TIN_CAY)
      .map((a) => new Date(a.ts).toISOString().slice(0, 10))).size,
  };
}

/** Bẫy hay sập nhất — thứ bố mẹ và cô giáo cần nhất */
export function topTraps(attempts, index = {}, n = 3) {
  const miss = {};
  for (const a of attempts) {
    if (!a.mustPass || a.correct) continue;
    const k = a.microId;
    miss[k] = (miss[k] || 0) + 1;
  }
  return Object.entries(miss)
    .sort((x, y) => y[1] - x[1])
    .slice(0, n)
    .map(([microId, times]) => ({
      microId, times,
      trapName: index[microId.replace(/[:.]/g, '_')]?.trapName || '',
    }));
}

/** Câu làm lâu mà vẫn sai — dấu hiệu con đang bế tắc chứ không phải ẩu */
/** NG16 · H3 — làm lâu hơn ngần này mà vẫn sai thì coi là bế tắc (mili-giây). */
/* ⚠ Danh mục ghi NG16 bằng GIÂY (Bảng 3.19), mã ở đây đo bằng MILI-GIÂY. Đổi
   đơn vị ngay tại chỗ đọc, đừng để hai đơn vị cùng tên trôi nổi hai nơi. */
/* ⚠ ĐỌC LÚC DÙNG, TỪ BỘ ĐÃ PHÁT HÀNH (Bảng 4.7, điểm 4). Trước 22-11 hằng này chụp
   bộ MẶC ĐỊNH lúc nạp module — chuyên gia đặt H3 = 60 giây cho câu gõ chữ thì BKT ăn, sổ bố mẹ
   vẫn báo "bế tắc" ở 45 giây. Nay `dungSoHoc` nạp bộ bằng `layBoNguong(db)` rồi
   truyền vào; và NG16 tra theo ngữ cảnh CỦA TỪNG LƯỢT (dạng câu, bậc) — đúng phạm vi
   Bảng 3.19 khai cho nó. Hằng dưới còn lại cho cổng: bộ của tiến trình, ở toàn hệ. */
export const msBeTac = (bo = boNguong(), nc = {}) => layNguong(bo, 'NG16', nc) * 1000;
export const MS_BE_TAC = msBeTac();

export function stuckItems(attempts, msThreshold = null, n = 3, bo = boNguong()) {
  /* `msThreshold` truyền tay thì dùng đúng số ấy cho mọi lượt (cổng, quét lưới);
     bỏ trống thì mỗi lượt lấy NG16 của chính nó. */
  const nguong = (a) => (Number.isFinite(msThreshold) ? msThreshold : msBeTac(bo, nguCanhLuot(a)));
  return attempts
    .filter((a) => DU_TIN_CAY(a) && !a.correct && (a.ms ?? 0) >= nguong(a))
    .sort((x, y) => (y.ms ?? 0) - (x.ms ?? 0))
    .slice(0, n)
    .map((a) => ({ microId: a.microId, itemId: a.itemId, seconds: Math.round((a.ms ?? 0) / 1000) }));
}

/**
 * Dựng sổ phụ huynh cho một khoảng (mặc định 7 ngày).
 * lessonsIndex: { DL_KSN5Q1_B49_M1: {microId, homeActivity, watchFor, title} }
 */
export function buildParentReport({ learnerId, attempts, progress = {}, mastery = {},
                                    soGio = [], index = {}, now = Date.now(), days = 7,
                                    bo = boNguong() }) {
  const from = now - days * 86400000;
  const win = inRange(attempts, from, now);
  const micros = [...new Set(win.map((a) => a.microId))];
  const passed = Object.values(progress).filter((m) => m.pass).length;
  const units = Object.values(mastery);
  /* θ của CHÍNH nút ấy (môn của nó, mã nút của nó) — trước 22-11 gõ cứng 0,85. */
  const mastered = units.filter((u) => (u.p ?? 0) >= layNguong(bo, 'NG07',
    nguCanhLuot({ mon: u.mon, bktUnit: u.unit }))).length;

  const gio = phutHoc(win, soGio, { from, to: now });
  const traps = topTraps(win, index);
  const focus = traps[0]?.microId;
  const tip = focus ? index[focus.replace(/[:.]/g, '_')] : null;

  return {
    learnerId,
    periodDays: days,
    generatedAt: now,
    minutes: gio.phut,
    /* Số phút này ĐO ĐƯỢC hay SUY RA — màn hình phải nói thật, vì bản suy ra không
       thấy phần xem giảng, mà phần giảng nay là toàn bộ video của bốn quyển. */
    nguonGio: gio.nguon,
    phutXem: gio.phutXem,
    phutLam: gio.phutLam,
    soNgayCoHoc: gio.soNgayCoHoc,
    /* Bao nhiêu lượt trong kỳ này KHÔNG dùng được cho thống kê thời gian. > 0 thì
       màn hình phải nói rõ, đừng để bố mẹ tưởng con học 0 phút. */
    luotThieuGio: win.filter((a) => !DU_TIN_CAY(a)).length,
    sessions: new Set(win.map((a) => a.sessionId)).size,
    answered: win.length,
    correctRate: win.length ? Math.round((win.filter((a) => a.correct).length / win.length) * 100) : 0,
    microsTouched: micros.length,
    microsPassed: passed,
    unitsMastered: mastered,
    unitsTotal: units.length,
    topTraps: traps,
    stuck: stuckItems(win, null, 3, bo),
    suggestion: tip?.homeActivity || '',
    watchFor: tip?.watchFor || '',
    focusMicro: focus || null,
    /* Đường cong học tập — xem `duongCongHoc` cho hai cái bẫy đã tránh. */
    duongCong: duongCongHoc(win, mastery),
    /* Mệt mỏi nhận thức — xem `metMoi` cho cái bẫy "phiên nào cũng ra mệt". */
    metMoi: metMoi(win, { bo }),
  };
}

/**
 * ĐƯỜNG CONG HỌC TẬP — tỉ lệ sai theo SỐ LẦN ĐÃ LUYỆN (mục 2.5.3 luận văn).
 *
 * Bố mẹ nhìn ra tiến bộ ở đây rõ hơn mọi con số phần trăm: lần đầu chạm một từ
 * thì sai nhiều, tới lần thứ tư thì gần như không sai nữa. Một con số "đúng 78%"
 * không nói được điều đó, vì nó trộn lần đầu với lần thứ mười vào cùng một rổ.
 *
 * ── ⚠ CÁI BẪY: "LẦN THỨ MẤY" TÍNH TỪ ĐÂU ──
 * Sổ học chỉ lấy nhật ký 7 ngày gần nhất. Đánh số thứ tự trong chừng ấy thì lượt
 * thứ 12 của một từ bé học từ tháng trước bị ghi thành "lần thứ 1" — và đường
 * cong dựng trên đó nói dối theo hướng đẹp lên: lần 1 trông có tỉ lệ sai thấp
 * bất thường, vì lẫn vào đó toàn những từ bé đã thạo từ lâu.
 *
 * Lối thoát KHÔNG phải là kéo dài cửa sổ (tốn, và bao nhiêu ngày cũng vẫn hụt).
 * Hồ sơ nút đã giữ `nAttempts` — TỔNG SỐ lượt từ trước tới nay. Nút nào có số ấy
 * ĐÚNG BẰNG số lượt đếm được trong cửa sổ thì cả lịch sử của nó nằm trọn ở đây,
 * và chỉ những nút ấy mới được vào đường cong.
 *
 * Nghĩa là đường cong này nói về "những nút bé BẮT ĐẦU học trong kỳ" — hẹp hơn,
 * nhưng đúng. Trả kèm `soNutDaLoc` để màn hình nói được điều đó thay vì giấu.
 *
 * ── ⚠ ĐIỂM CÓ ÍT MẪU THÌ ĐỪNG VẼ ──
 * Đuôi đường cong luôn thưa: ít nút nào bị luyện tới lần thứ tám. Một điểm dựng
 * trên 2 mẫu nhảy 0% hay 100% tuỳ một câu, mà mắt người nhìn biểu đồ thì tin
 * ngay. Nên mỗi điểm mang theo `soMau`, và điểm dưới ngưỡng bị BỎ HẲN chứ không
 * trả về kèm cờ — trả về là sớm muộn có chỗ vẽ nó lên.
 */
export function duongCongHoc(attempts, mastery = {}, {
  toiThieuMau = 3, toiDaLan = 8,
} = {}) {
  /* Gom theo nút, giữ đúng thứ tự thời gian. `bktUnit` rỗng thì bỏ — lượt ấy
     không gắn với nút nào nên không có "lần thứ mấy". */
  const theoNut = new Map();
  for (const a of attempts) {
    if (!a?.bktUnit) continue;
    if (!theoNut.has(a.bktUnit)) theoNut.set(a.bktUnit, []);
    theoNut.get(a.bktUnit).push(a);
  }

  const tra = (u) => mastery[u] ?? mastery[encodeURIComponent(u)];
  let daLoc = 0;
  const diem = new Map();          // lần thứ n → { tong, sai }
  for (const [nut, ds] of theoNut) {
    const ho = tra(nut);
    /* Không có hồ sơ nút thì KHÔNG đoán là đủ lịch sử — bỏ. Thiếu hồ sơ nghĩa là
       hàm nền chưa chạy xong hoặc nút vừa mới có, cả hai đều chưa tin được. */
    if (!ho || ho.nAttempts !== ds.length) { daLoc += 1; continue; }
    ds.sort((x, y) => (x.ts ?? 0) - (y.ts ?? 0));
    ds.forEach((a, i) => {
      const lan = i + 1;
      if (lan > toiDaLan) return;
      const d = diem.get(lan) || { tong: 0, sai: 0 };
      d.tong += 1;
      if (!a.correct) d.sai += 1;
      diem.set(lan, d);
    });
  }

  const duong = [...diem.entries()]
    .sort((a, b) => a[0] - b[0])
    .filter(([, d]) => d.tong >= toiThieuMau)
    .map(([lan, d]) => ({
      lan,
      soMau: d.tong,
      tiLeSai: Math.round((d.sai / d.tong) * 100),
    }));

  return { duong, soNut: theoNut.size - daLoc, soNutDaLoc: daLoc, toiThieuMau };
}

/**
 * MỆT MỎI NHẬN THỨC — bé có chậm dần trong một buổi học không (mục 2.1.2-T).
 *
 * Tín hiệu là thời gian trả lời dài dần. Có nó thì nói được với bố mẹ một câu
 * thật sự dùng được: "con học chừng 20 phút thì bắt đầu chậm lại, nên cho nghỉ
 * giữa chừng" — cụ thể hơn mọi lời khuyên chung chung về thời lượng.
 *
 * ── ⚠ CÁI BẪY LÀM PHIÊN NÀO CŨNG RA "MỆT" ──
 * Cách hiển nhiên là so nửa đầu phiên với nửa sau. Cách ấy SAI, và sai một chiều:
 * bài học đi theo thang độ khó (khởi động → ráp câu → thử thách), nên câu cuối
 * phiên VỐN ĐÃ khó hơn câu đầu. So thẳng thì mọi buổi học đều "có dấu hiệu mệt",
 * và bố mẹ đọc thành "con tôi chóng mệt" trong khi thật ra app đang tăng độ khó
 * đúng như thiết kế.
 *
 * Nên chỉ so TRONG CÙNG MỘT ĐỊNH DẠNG: câu chọn-đáp-án đầu phiên với câu
 * chọn-đáp-án cuối phiên. Cùng loại việc, cùng cỡ khó — chênh lệch còn lại mới
 * là của bé.
 *
 * ── ⚠ VÀ CHỈ NÓI KHI ĐỦ MẪU ──
 * Một định dạng phải có ít nhất `TOI_THIEU_MOI_NUA` lượt ở MỖI nửa thì mới so.
 * Dưới đó, chênh lệch chỉ là một câu bé mải nhìn ra ngoài cửa sổ.
 */
/* NG17 — đọc LÚC DÙNG từ bộ truyền vào (Bảng 4.7, điểm 4); hai hằng dưới chỉ còn cho
   cổng. `toiThieuMoiNua` tra theo dạng câu của từng nhóm; `ti` so trên cả phiên. */
export const TOI_THIEU_MOI_NUA = layNguong(boNguong(), 'NG17').toiThieuMoiNua;

/** Chậm hơn bao nhiêu phần trăm thì đáng nói. Dưới ngưỡng là dao động thường. */
export const NGUONG_CHAM = layNguong(boNguong(), 'NG17').ti;

export function metMoi(attempts, { toiThieu = null, bo = boNguong() } = {}) {
  /* Chỉ dùng lượt ĐO ĐƯỢC thời gian và có đủ định danh phiên. */
  const dung = (attempts || []).filter(
    (a) => a?.sessionId && Number.isFinite(a.ms) && a.ms > 0 && Number.isFinite(a.ts),
  );

  const theoPhien = new Map();
  for (const a of dung) {
    if (!theoPhien.has(a.sessionId)) theoPhien.set(a.sessionId, []);
    theoPhien.get(a.sessionId).push(a);
  }

  let dauTong = 0; let dauDem = 0;
  let cuoiTong = 0; let cuoiDem = 0;
  let soPhien = 0;

  for (const ds of theoPhien.values()) {
    ds.sort((x, y) => x.ts - y.ts);
    /* Gom theo ĐỊNH DẠNG trong chính phiên ấy — đây là chỗ chặn cái bẫy trên. */
    const theoDang = new Map();
    for (const a of ds) {
      const k = a.mode || a.format || '?';
      if (!theoDang.has(k)) theoDang.set(k, []);
      theoDang.get(k).push(a);
    }
    let phienCoDung = false;
    for (const [dang, nhom] of theoDang.entries()) {
      const tt = toiThieu ?? layNguong(bo, 'NG17', dang === '?' ? {} : { dangCau: String(dang) }).toiThieuMoiNua;
      if (nhom.length < tt * 2) continue;
      const nua = Math.floor(nhom.length / 2);
      for (const a of nhom.slice(0, nua)) { dauTong += a.ms; dauDem += 1; }
      /* Lấy từ CUỐI ngược lại đúng `nua` lượt — số lẻ thì bỏ lượt GIỮA, không dồn
         nó vào một bên. Dồn vào nửa sau là tự tay nghiêng kết quả về phía "mệt". */
      for (const a of nhom.slice(nhom.length - nua)) { cuoiTong += a.ms; cuoiDem += 1; }
      phienCoDung = true;
    }
    if (phienCoDung) soPhien += 1;
  }

  if (!dauDem || !cuoiDem) {
    return { duLieu: false, soPhien, msDau: null, msCuoi: null, chamHon: null, metMoi: false };
  }
  const msDau = Math.round(dauTong / dauDem);
  const msCuoi = Math.round(cuoiTong / cuoiDem);
  const chamHon = (msCuoi - msDau) / msDau;
  return {
    duLieu: true,
    soPhien,
    soMau: dauDem + cuoiDem,
    msDau,
    msCuoi,
    chamHon: Math.round(chamHon * 100) / 100,
    metMoi: chamHon >= layNguong(bo, 'NG17').ti,
  };
}

/** Câu văn ngắn cho bố mẹ đọc lướt */
export function reportHeadline(r) {
  if (!r.answered) return 'Tuần này con chưa vào học buổi nào.';
  const t = r.topTraps[0];
  return `Con học ${r.minutes} phút trong ${r.sessions} buổi, trả lời ${r.answered} câu, đúng ${r.correctRate}%.`
    + (t ? ` Bẫy hay sập nhất: ${t.trapName || t.microId} (${t.times} lần).` : '');
}
