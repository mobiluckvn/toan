/**
 * HỌC SINH MÔ PHỎNG cho phần thực nghiệm của luận văn.
 *
 *     cd web
 *     node tools/mo_phong/hoc_sinh_ao.mjs sinh           # chỉ sinh ra tệp, KHÔNG đụng máy chủ
 *     node tools/mo_phong/hoc_sinh_ao.mjs day --that     # đẩy lên dự án (cần `firebase login`)
 *     node tools/mo_phong/hoc_sinh_ao.mjs xoa --that     # gỡ SẠCH mọi thứ mang cờ moPhong
 *     node tools/mo_phong/hoc_sinh_ao.mjs xoa --that --giu-tai-khoan
 *                                    # gỡ dữ liệu học nhưng GIỮ tài khoản đăng nhập — dùng
 *                                    # trước khi đẩy lại, để phiên đang mở trên Chrome và
 *                                    # email đăng nhập (`EMAIL_DANG_NHAP`) không mất
 *
 * ── ĐÂY LÀ DỮ LIỆU MÔ PHỎNG, VÀ PHẢI ĐƯỢC GỌI ĐÚNG TÊN ──
 * 30 em là học sinh ẢO, lớp 1–5 (mỗi lớp 6 em) — đúng phạm vi nội dung app có. Mọi tài liệu mang `moPhong: true`, email đuôi `.test`
 * (không bao giờ nhận thư), tên hiển thị bắt đầu bằng "HS mô phỏng". Luận văn và
 * slide phải ghi "thực nghiệm trên dữ liệu mô phỏng", không ghi "học sinh thật".
 * Máy chủ loại các em khỏi bảng cô giáo, bảng xếp hạng và phép học ngưỡng —
 * xem `functions/src/moPhong.js`.
 *
 * ── MÔ HÌNH NGƯỜI HỌC (cái được mô phỏng) ──
 * Mỗi em có `gioi` (năng lực nền), `tiepThu` (tốc độ học vào) và một mốc xong
 * chương trình riêng quanh 13 tuần. Học hằng ngày 19h–22h, có ngày hai buổi; bộ
 * điều nhịp chia số bài còn lại cho số ngày còn lại tới mốc.
 * Với mỗi nút kiến thức em mang một độ vững ẩn `s`. Nút MỚI không bắt đầu từ số 0
 * như nhau mãi: em đã làm càng nhiều câu thì nền càng chắc, nên `s` khởi đầu của
 * nút mới nhích lên dần (học bài trước đỡ cho bài sau):
 *     P(đúng) = đoán + (1 − đoán − trượt) · s
 *     sau mỗi lượt: s ← s + tốc_độ · (1 − s)       (học)
 *     giữa hai lần gặp: s giảm dần theo số ngày     (quên)
 * Đây là mô hình SINH dữ liệu; mức thạo mà app báo ra vẫn do đúng hàm BKT của
 * máy chủ (`functions/src/bkt.js`) tính, chạy trên đồng hồ mô phỏng. Tức là con số
 * "tiến bộ" là thứ hệ thống ĐO được từ nhật ký, không phải thứ script tự khai.
 *
 * Bộ sinh ngẫu nhiên TIỀN ĐỊNH (`--hat`): chạy lại ra đúng dữ liệu ấy.
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { applyAttempt } from '../../functions/src/bkt.js';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const NOI_DUNG = path.join(GOC, 'public/content');
const RA = path.join(GOC, 'tools/mo_phong/ra');

const lenh = process.argv[2];
const co = (ten) => process.argv.includes(`--${ten}`);
const so = (ten, mac) => {
  const i = process.argv.indexOf(`--${ten}`);
  return i > 0 && process.argv[i + 1] ? Number(process.argv[i + 1]) : mac;
};

const SO_EM = so('em', 30);
const HAT = so('hat', 20260701);
const PHIEN_BAN = 1;
const DU_AN = 'ky-su-nhi';
const VN = 7 * 3600000;                                 // giờ Việt Nam
/* Hết 21-11-2026. Em chậm xong chương trình trong tháng 11 (trước 15-11); em đã xong
   thì vẫn quay lại ôn THƯA tới tận tuần này — người dùng thật học xong không biến
   mất, và sổ bố mẹ "tuần này" của các em vì thế có số liệu. */
const KET_THUC = Date.UTC(2026, 10, 21, 23, 59) - VN;
const BAT_DAU = Date.UTC(2026, 6, 1) - VN;              // mọi em vào học trong tháng 7
const HAN_VAO = Date.UTC(2026, 7, 1) - VN;
/* Tỉ trọng lớp 1–5 — KHÔNG đều nhau, như người dùng tự tìm tới. Lớp 2–3 đông
   nhất (bố mẹ quan tâm nhất), lớp 1 ít vì mới có Tiếng Anh. Số em mỗi lớp làm
   tròn từ tỉ trọng (30 em → 4·8·7·6·5), rồi XÁO thứ tự để lớp nào vào lúc nào
   cũng ngẫu nhiên. Rút ngẫu nhiên từng em thì với 30 em dễ ra lớp 13 em, lớp 2. */
const TI_TRONG_LOP = [0.12, 0.27, 0.25, 0.2, 0.16];

let hat = HAT;
const ran = () => { hat = (hat * 1103515245 + 12345) % 2147483648; return hat / 2147483648; };
const trongKhoang = (a, b) => a + (b - a) * ran();
const nguyen = (a, b) => Math.floor(trongKhoang(a, b + 1));
const chon = (ds) => ds[Math.floor(ran() * ds.length)];

/* ─────────── NỘI DUNG — đọc đúng các bài app đang phát ─────────── */

const THU_MUC = { toan: { 2: 'lop2', 3: 'lop3', 4: 'lop4', 5: 'lessons' }, tienganh: (l) => `ta${l}` };
const tuNhien = (a, b) => a.localeCompare(b, 'en', { numeric: true });

function napBai(mon, lop) {
  const tm = mon === 'toan' ? THU_MUC.toan[lop] : THU_MUC.tienganh(lop);
  const tep = fs.readdirSync(path.join(NOI_DUNG, tm)).filter((t) => /^DL_.*\.json$/.test(t)).sort(tuNhien);
  return tep.map((t) => {
    const d = JSON.parse(fs.readFileSync(path.join(NOI_DUNG, tm, t), 'utf8'));
    const nutBai = d.skills?.bktUnit;
    const cau = (x) => ({
      id: x.id,
      nut: (mon === 'tienganh' && x.maNut) || nutBai,
      maNutDs: x.maNutDs || null,
      bac: x.bac ?? null,
      mode: x.format || (x.choices ? 'chondapan' : 'so'),
      soLuaChon: (x.choices || x.answerKey?.parts?.[0]?.options || []).length,
    });
    const pools = d.practice?.pools || {};
    let luyen = [...(pools.warmup || []), ...(pools.standard || []), ...(pools.challenge || [])].map(cau);
    /* Tiếng Anh có kho luyện rất dày (tới 50 câu) — app rút một phần mỗi lượt. */
    if (luyen.length > 10) luyen = luyen.filter((_, i) => i % Math.ceil(luyen.length / 9) === 0);
    const kt = (d.assessment?.items || []).map(cau);
    const m = String(d.assessment?.passRule || '').match(/(\d+)\s*(?:\/|trên)\s*(\d+)/);
    return {
      id: d.id, mon, lop, tieuDe: d.title, nut: nutBai, luyen, kt,
      /* Chương: Toán lớp 5 đánh bằng công thức (4 bài × 3 micro), đúng `chapterOf`
         của app; các quyển khác khai sẵn trong bài. */
      chuong: mon === 'toan' && lop === 5
        ? Math.ceil(Number(String(d.id).split('.B')[1]?.split('.M')[0]) / 4)
        : Number(d.chuong) || 1,
      cacNut: [...new Set([...luyen, ...kt].map((c) => c.nut))],
      nguongDat: m ? Number(m[1]) / Number(m[2]) : 0.8,
      phut: Number(d.durationMinutes) || 10,
    };
  }).filter((b) => b.id && b.nut && b.kt.length);
}

/* ─────────── SINH ─────────── */

const iso = (ms) => new Date(ms).toISOString();
const ngayVN = (ms) => new Date(ms + VN).toISOString().slice(0, 10);
const NGAY = 86400000;

/* ── TÊN GỌI ──
   Tên tự nhiên, không nhãn trên giao diện (bác chốt 22-11-2026: mọi tài khoản của
   dự án đều do tác giả tạo). Dấu vết mô phỏng nằm ở DỮ LIỆU: cờ `moPhong`, email đuôi
   `.test` (tên miền dành riêng, không bao giờ là của ai), `moPhongMeta` trên hồ sơ.
   Ảnh đưa vào luận văn phải chú thích "dữ liệu mô phỏng". Năm sinh trong email suy
   từ lớp (lớp 1 ↔ 2019). */
const TEN = ['Minh An', 'Bảo Ngọc', 'Gia Huy', 'Khánh Linh', 'Đức Anh', 'Thảo Vy', 'Hoàng Nam',
  'Phương Anh', 'Tuấn Kiệt', 'Ngọc Hân', 'Quang Minh', 'Hà My', 'Nhật Long', 'Thu Trang',
  'Bảo Châu', 'Minh Khang', 'Diệu Linh', 'Trung Kiên', 'An Nhiên', 'Hải Đăng', 'Mai Anh',
  'Đăng Khoa', 'Tường Vi', 'Phúc Lâm', 'Yến Nhi', 'Thành Đạt', 'Lan Chi', 'Gia Bảo',
  'Kim Ngân', 'Việt Hoàng'];
/* Bốn em dùng để ĐĂNG NHẬP chụp ảnh minh chứng: email là bí danh `+` của hộp thư
   tác giả (Google Workspace chuyển mọi `congvt+…` về `congvt`), nên mã OTP về đúng
   người. Các em còn lại giữ đuôi `.test`. Khoá là mã em (thứ tự vào học). */
const EMAIL_DANG_NHAP = {
  '01': 'congvt+minhan.lop1@mobiluck.vn',
  '17': 'congvt+dieulinh.lop2@mobiluck.vn',
  '10': 'congvt+ngochan.lop3@mobiluck.vn',
  '24': 'congvt+phuclam.lop5@mobiluck.vn',
};
const boDau = (x) => x.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D');

/* Phân bố gần chuẩn quanh `tb` (trung bình ba số đều) — để phần đông em ở giữa,
   ít em quá giỏi hay quá yếu, thay vì rải đều như kẻ thước. */
const gan = (tb, rong) => tb + rong * ((ran() + ran() + ran()) / 1.5 - 1);
const kep = (x, a, b) => Math.min(b, Math.max(a, x));

function taoEm(i, lop, mocVao) {
  const ma = String(i + 1).padStart(2, '0');
  /* ── MỖI EM MỘT NHỊP HỌC RIÊNG ──
     gioi      năng lực nền → xác suất đúng lúc mới gặp
     tiepThu   em này học vào nhanh hay chậm (nhân vào tốc độ học)
     tuanMucTieu  mốc xong chương trình của em (tuần)
     diHoc     tỉ lệ ngày có mở app · haiBuoi  tỉ lệ ngày học hai buổi */
  const gioi = +kep(gan(0.6, 0.32), 0.22, 0.95).toFixed(3);
  /* Mốc xong chương trình riêng của em, quanh 13 tuần: ~20% nhanh, ~65% đúng nhịp,
     ~15% chậm. Em chậm còn trượt sát hạch nhiều hơn nên thường về muộn hơn cả mốc. */
  const u = ran();
  const heSo = u < 0.2 ? trongKhoang(0.7, 0.85) : u < 0.85 ? trongKhoang(0.9, 1.02) : trongKhoang(1.05, 1.2);
  return {
    uid: `moPhong${ma}${String(HAT).slice(-4)}`,
    ma, lop,
    gioi: u < 0.2 ? Math.max(gioi, 0.7) : u >= 0.85 ? Math.min(gioi, 0.5) : gioi,
    tiepThu: +kep(gan(1, 0.4) * (u < 0.2 ? 1.2 : u >= 0.85 ? 0.8 : 1), 0.45, 1.7).toFixed(3),
    tuanMucTieu: +(13 * heSo).toFixed(1),
    diHoc: +trongKhoang(0.85, 0.95).toFixed(3),      // tỉ lệ ngày có mở app
    haiBuoi: +trongKhoang(0.15, 0.35).toFixed(3),    // tỉ lệ ngày học hai buổi
    /* Lớp 1 chưa có Toán (chương trình ghi "Sắp có") — em lớp 1 chỉ học Tiếng Anh.
       Mọi em lớp 2–5 học CẢ HAI môn. */
    hocToan: lop >= 2,
    hocTiengAnh: true,
    mocVao,
    email: EMAIL_DANG_NHAP[ma] || `${boDau(TEN[i % TEN.length]).toLowerCase().replace(/\s+/g, '')}.${2020 - lop}@mophong.test`,
    displayName: TEN[i % TEN.length],
    bietDanh: TEN[i % TEN.length].split(' ').pop(),
  };
}

function moPhongMotEm(em, baiTheoMon) {
  const luot = [], tienDo = {}, gio = {}, mastery = {};
  const vung = {};                    // độ vững ẩn s theo nút
  const lanCuoi = {};                 // ngày gặp nút gần nhất (mô hình quên)
  const viTri = { toan: 0, tienganh: 0 };
  const tocDo = (0.04 + 0.09 * em.gioi) * em.tiepThu;
  let soPhien = 0;

  let soCau = 0;
  const goc = 0.1 + 0.3 * em.gioi;
  const s0 = () => goc + (0.8 - goc) * 0.55 * (1 - Math.exp(-soCau / 450));
  const layS = (nut, t) => {
    let s = vung[nut] ?? s0();
    if (lanCuoi[nut] != null) s = Math.max(s0() * 0.8, s - 0.012 * ((t - lanCuoi[nut]) / NGAY));
    return s;
  };

  const monHoc = [...(em.hocToan ? ['toan'] : []), ...(em.hocTiengAnh ? ['tienganh'] : [])];
  const tongBai = monHoc.reduce((s, m) => s + baiTheoMon[m].length, 0);
  const conLai = () => monHoc.reduce((s, m) => s + baiTheoMon[m].length - viTri[m], 0);
  /* Lịch ôn của bài đã đạt: +1 · +3 · +7 ngày — đúng lịch `buildReviewCards` của app. */
  const LICH_ON = [1, 3, 7];
  const hanMuc = em.mocVao + em.tuanMucTieu * 7 * NGAY;

  /* Làm MỘT bài trong một buổi. `on` = buổi ôn: chỉ luyện vài câu, không sát hạch. */
  function lamBai(bai, mon, ctx, k, on) {
    const xem = on ? 0 : Math.round(bai.phut * 60 * trongKhoang(0.25, 0.45) * (tienDo[bai.id] ? 0.4 : 1));
    ctx.giayXem += xem; ctx.t += xem * 1000;
    let seq = 0;
    const lam = (c, pha) => {
      const s = layS(c.nut, ctx.t);
      const doan = c.soLuaChon ? 1 / c.soLuaChon : (c.mode === 'tf' || c.mode === 'dungsai' ? 0.5 : 0.05);
      const pDung = doan + (1 - doan - 0.08) * s;
      const toiDa = pha === 'assess' ? 1 : 2;
      let goi = 0, dung = false;
      for (let lan = 1; lan <= toiDa; lan++) {
        dung = ran() < pDung + (lan - 1) * 0.15;
        const nhanh = 1 - 0.3 * (1 - Math.exp(-soCau / 600));     // quen tay dần
        const ms = Math.round((12000 + 40000 * (1.15 - s)) * nhanh * trongKhoang(0.6, 1.4) * (c.mode === 'tf' ? 0.6 : 1));
        ctx.t += ms + nguyen(1500, 4000);
        ctx.giayLam += Math.round(ms / 1000);
        const a = {
          id: `${em.uid}_${ctx.phien}_${k}_${bai.id.replace(/^DL:/, '').replace(/[:.]/g, '_')}_${c.id}_${seq}`,
          learnerId: em.uid, sessionId: ctx.phien, microId: bai.id,
          bktUnit: c.nut, dangBai: null, itemId: c.id, phase: pha,
          correct: dung, tries: lan, hintsUsed: goi, mustPass: false, ms,
          answer: null, expected: null, mode: c.mode, revealed: false,
          nguongVer: 1, mon, khoiLop: String(em.lop), nhomThuNghiem: null, v: 7,
          ts: Math.round(ctx.t), serverTs: Math.round(ctx.t) + nguyen(150, 900),
          moPhong: true,
        };
        if (mon === 'tienganh') Object.assign(a, { maNutDs: c.maNutDs, bac: c.bac, quyen: `ta${em.lop}` });
        seq += 1;
        soCau += 1;
        luot.push(a);
        mastery[c.nut] = applyAttempt(mastery[c.nut], a, () => a.ts);
        mastery[c.nut]._mon = mon;
        /* Học: đúng thì vững thêm, sai mà được gợi ý cũng vững thêm chút. */
        vung[c.nut] = Math.min(0.98, s + tocDo * (dung ? 1 : 0.6) * (1 - s));
        lanCuoi[c.nut] = ctx.t;
        /* Tiếng Anh khai nút theo TỪNG CÂU (từ, mẫu câu), nên một nút ít khi gặp
           lại. Nhưng luyện một từ của unit thì cả unit vững thêm — các nút cùng bài
           được một phần ba lượng học ấy. */
        if (mon === 'tienganh') {
          for (const n of bai.cacNut) {
            if (n === c.nut) continue;
            const sn = layS(n, ctx.t);
            vung[n] = Math.min(0.98, sn + tocDo * 0.33 * (1 - sn));
            lanCuoi[n] = ctx.t;
          }
        }
        if (dung) break;
        if (ran() < 0.6) goi += 1;
      }
      return dung;
    };

    ctx.cuoi = bai.id;
    ctx.mon = mon;
    if (on) {
      for (const c of [...bai.luyen].sort(() => ran() - 0.5).slice(0, em.lop === 1 ? 8 : 4)) lam(c, 'practice');
      return;
    }
    for (const c of bai.luyen) lam(c, 'practice');
    const dungKt = bai.kt.filter((c) => lam(c, 'assess')).length;
    const dat = dungKt / bai.kt.length >= bai.nguongDat - 1e-9;
    const cu = tienDo[bai.id];
    tienDo[bai.id] = {
      microId: bai.id, mon, pass: dat || !!cu?.pass,
      score: Math.max(dungKt, cu?.score ?? 0), total: bai.kt.length,
      attempts: (cu?.attempts ?? 0) + 1, at: Math.round(ctx.t),
      state: dat || cu?.pass ? 'passed' : 'tried', sessionId: ctx.phien,
      datLuc: cu?.datLuc ?? (dat ? Math.round(ctx.t) : null), daOn: cu?.daOn ?? 0,
    };
    if (dat) { viTri[mon] += 1; xetXongChuong(bai, mon); }   // chưa đạt thì buổi sau làm lại
  }

  /* Môn của bài mới kế tiếp: chọn theo TỈ LỆ BÀI CÒN LẠI, để hai môn cùng về đích. */
  const monKeTiep = () => {
    const con = monHoc.map((m) => [m, baiTheoMon[m].length - viTri[m]]).filter(([, n]) => n > 0);
    const tong = con.reduce((s, [, n]) => s + n, 0);
    let u = ran() * tong;
    for (const [m, n] of con) { u -= n; if (u <= 0) return m; }
    return con[con.length - 1]?.[0];
  };

  /* ── KỲ ÔN TẬP CHƯƠNG ──
     Xong hết bài của một chương thì chương ấy chờ kỳ ôn (10 câu, cần 8 — đúng
     `need` trong `ontap.json`). Em làm kỳ ôn ở một buổi sau; trượt thì buổi sau thi
     lại. Điểm rút từ độ vững trung bình của các nút trong chương — em vững thật thì
     mới qua. Không sinh dòng `attempts` cho kỳ ôn: app ghi kỳ ôn vào học bạ, không
     vào nhật ký từng câu. */
  const kyChuong = {};          // khoá → { mon, khoa, chuong, ma, dat, best, lan, at }
  const choKy = [];             // khoá chương đang chờ thi
  const maQuyen = (mon) => (mon === 'toan' ? `lop${em.lop}` : `ta${em.lop}`);
  const khoaKy = (mon, ch) => (mon === 'toan' ? `${maQuyen(mon)}.${ch}` : `${maQuyen(mon)}:C${ch}`);
  const xetXongChuong = (bai, mon) => {
    const ds = baiTheoMon[mon].filter((b) => b.chuong === bai.chuong);
    if (!ds.every((b) => tienDo[b.id]?.pass)) return;
    const k = khoaKy(mon, bai.chuong);
    if (!kyChuong[k] && !choKy.includes(k)) choKy.push(k);
  };
  function thiChuong(k, ctx) {
    const mon = k.startsWith('lop') ? 'toan' : 'tienganh';
    const ch = Number(k.split(/[.:]C?/).pop());
    const nut = [...new Set(baiTheoMon[mon].filter((b) => b.chuong === ch).flatMap((b) => b.cacNut))];
    const sTB = nut.reduce((x, n) => x + layS(n, ctx.t), 0) / Math.max(1, nut.length);
    /* Trượt rồi thì em ôn lại trước khi thi tiếp — mỗi lần thi lại khá lên một nấc. */
    const pCau = Math.min(0.97, 0.12 + 0.86 * sTB + 0.07 * (kyChuong[k]?.lan ?? 0));
    let dung = 0;
    for (let i = 0; i < 10; i++) if (ran() < pCau) dung += 1;
    const giay = nguyen(360, 660);
    ctx.t += giay * 1000; ctx.giayLam += giay;
    const cu = kyChuong[k];
    const dat = dung >= 8;
    kyChuong[k] = {
      mon, khoa: k, chuong: ch, ma: maQuyen(mon),
      dat: dat || !!cu?.dat, best: Math.max(dung, cu?.best ?? 0),
      lan: (cu?.lan ?? 0) + 1, at: Math.round(ctx.t),
    };
    if (dat) choKy.splice(choKy.indexOf(k), 1);
    ctx.mon = ctx.mon || mon;
  }

  let quy = 0;                  // phần bài lẻ cộng dồn của bộ điều nhịp
  let xongLuc = null, ngungLuc = null;

  for (let ngay = em.mocVao; ngay < KET_THUC; ngay += NGAY) {
    const xong = conLai() === 0 && !choKy.length;
    if (xong && xongLuc == null) {
      xongLuc = ngay;
      ngungLuc = ngay + nguyen(5, 20) * NGAY;      // học xong còn ôn thêm vài tuần rồi thưa dần
    }
    /* Xong rồi: vài tuần đầu ôn khá đều (35% số ngày), sau đó thưa dần (~2 buổi/tuần). */
    const pOn = !xong ? em.diHoc : ngay <= ngungLuc ? 0.35 : 0.28;
    if (ran() > pOn) continue;

    /* ── BỘ ĐIỀU NHỊP ──
       Bài còn lại ÷ số ngày học còn lại tới mốc của em. Quá mốc mà chưa xong thì
       tăng tốc vừa phải (×1,4) — nhưng trần 4 bài một ngày, vì một đứa trẻ thật
       không ngồi được hơn thế sau giờ học ở trường. */
    let soMoi = 0;
    if (!xong) {
      const ngayCon = (hanMuc - ngay) / NGAY;
      const can = ngayCon > 0.5 ? conLai() / (ngayCon * em.diHoc) : 1.4 * Math.max(1, conLai() / 7);
      quy += Math.min(4, can) * trongKhoang(0.7, 1.3);
      soMoi = Math.floor(quy);
      quy -= soMoi;
    }

    const haiBuoi = ran() < em.haiBuoi && (soMoi >= 2 || ran() < 0.3);
    const soBuoi = haiBuoi ? 2 : 1;
    /* Giờ mở app rải khắp 19:00–21:45 (giờ VN); ngày hai buổi thì buổi đầu sớm hơn. */
    let batDau = ngay + (haiBuoi ? trongKhoang(19, 20.2) : trongKhoang(19, 21.75)) * 3600000;

    for (let b = 0; b < soBuoi; b++) {
      if (b === 1) {
        batDau = Math.max(batDau, ngay + 19 * 3600000);
        if (batDau > ngay + 21.75 * 3600000) break;        // không mở buổi hai sau 21:45
      }
      const ctx = { t: batDau, phien: `mophong-${em.ma}-${++soPhien}`, giayLam: 0, giayXem: 0, cuoi: null, mon: null };
      let k = 0;

      /* Ôn bài đến hạn trước (tối đa 2), như thẻ "Ôn lại" của app. */
      const denHan = Object.values(tienDo)
        .filter((p) => p.pass && p.datLuc && p.daOn < LICH_ON.length && ngay >= p.datLuc + LICH_ON[p.daOn] * NGAY - NGAY / 2)
        .slice(0, b === 0 ? 2 : 1);
      /* Lớp 1 chỉ có 16 unit — một bài mới mỗi vài ngày. Buổi không có bài mới thì
         bé luyện lại hai, ba unit cũ cho đủ một buổi 10–15 phút. */
      if (em.lop === 1 && !soMoi) {
        const daDat = Object.values(tienDo).filter((p) => p.pass && !denHan.includes(p));
        for (let x = 0; x < 2 && daDat.length; x++) denHan.push({ ...chon(daDat), _them: true });
      }
      for (const p of denHan) {
        const bai = baiTheoMon[p.mon].find((x) => x.id === p.microId);
        lamBai(bai, p.mon, ctx, k++, true);
        if (!p._them) p.daOn += 1;
      }

      /* Chương vừa xong thì phần đông em thi kỳ ôn ngay buổi sau (85%). */
      if (choKy.length && ran() < 0.85) { thiChuong(choKy[0], ctx); k++; }

      const phanBuoi = b === 0 ? Math.ceil(soMoi / soBuoi) : soMoi - Math.ceil(soMoi / soBuoi);
      for (let j = 0; j < phanBuoi; j++) {
        const mon = monKeTiep();
        if (!mon) break;
        lamBai(baiTheoMon[mon][viTri[mon]], mon, ctx, k++, false);
        if (ctx.t > ngay + 22.25 * 3600000) break;          // quá 22:15 thì nghỉ, mai học tiếp
      }
      /* Không có bài mới cũng không có bài đến hạn: ôn một bài bất kỳ đã đạt. */
      if (!k) {
        const daDat = Object.values(tienDo).filter((p) => p.pass);
        if (!daDat.length) {
          const mon = monKeTiep();
          if (mon) lamBai(baiTheoMon[mon][viTri[mon]], mon, ctx, k++, false);
        } else {
          const p = chon(daDat);
          lamBai(baiTheoMon[p.mon].find((x) => x.id === p.microId), p.mon, ctx, k++, true);
        }
      }
      if (!k) { soPhien -= 1; continue; }

      const n = ngayVN(ctx.t);
      const g = gio[`${ctx.mon}|${n}`] || { mon: ctx.mon, ngay: n, giayLam: 0, giayXem: 0, soLuot: 0, baiCuoi: null, at: 0 };
      g.giayLam += ctx.giayLam; g.giayXem += ctx.giayXem; g.soLuot += 1; g.baiCuoi = ctx.cuoi; g.at = Math.round(ctx.t);
      gio[`${ctx.mon}|${n}`] = g;
      batDau = ctx.t + trongKhoang(45, 75) * 60000;       // buổi hai cách ít nhất 45 phút
    }
  }
  return { luot, tienDo, gio, mastery, soPhien, xongLuc, tongBaiCT: tongBai, kyChuong };
}

function sinh() {
  const em = [];
  /* ── TỰ TÌM TỚI, KHÔNG THEO ĐỢT ──
     Ngày vào rải liên tục từ 01-07 tới 25-10, hơi dày dần về sau (truyền miệng).
     Lớp rút theo `TI_TRONG_LOP`. Mã em đánh theo THỨ TỰ VÀO HỌC. Chỉ lớp 1–5 —
     đúng phạm vi nội dung đang có; lớp 6 trở lên chưa có bài. */
  const soTheoLop = TI_TRONG_LOP.map((w) => Math.round(w * SO_EM));
  soTheoLop[1] += SO_EM - soTheoLop.reduce((a, b) => a + b, 0);   // bù lệch làm tròn vào lớp 2
  const dsLop = soTheoLop.flatMap((n, k) => Array(n).fill(k + 1));
  for (let k = dsLop.length - 1; k > 0; k--) { const j = Math.floor(ran() * (k + 1)); [dsLop[k], dsLop[j]] = [dsLop[j], dsLop[k]]; }
  const rutLop = (i) => dsLop[i];
  /* Rải CÓ NHIỄU: chia khoảng vào học thành SO_EM ô, mỗi em một ngày ngẫu nhiên
     trong ô của mình. Rút tự do 30 ngày thì dễ ra 16 em tháng 7, 2 em tháng 9 —
     ngẫu nhiên đấy nhưng nhìn vào lại thấy giả. Mũ 1,2 dồn nhẹ về đầu: em vào sớm
     mới có lịch sử đủ dài để thấy tiến bộ. */
  const vao = Array.from({ length: SO_EM }, (_, i) => BAT_DAU + (HAN_VAO - BAT_DAU) * Math.pow((i + ran()) / SO_EM, 1.2))
    .map((t) => Math.floor((t + VN) / NGAY) * NGAY - VN)
    .sort((a, b) => a - b);
  vao.forEach((t, i) => em.push(taoEm(i, rutLop(i), t)));
  const bai = {};
  for (const l of [1, 2, 3, 4, 5]) bai[l] = { toan: l >= 2 ? napBai('toan', l) : [], tienganh: napBai('tienganh', l) };

  return em.map((e) => ({
    ...e, ...moPhongMotEm(e, bai[e.lop]),
    tongBai: { toan: bai[e.lop].toan.length, tienganh: bai[e.lop].tienganh.length },
  }));
}

/* ─────────── TÓM TẮT — số liệu cho Chương 4 ─────────── */

/**
 * TỐC ĐỘ ĐI HẾT CHƯƠNG TRÌNH — mỗi môn: đã đạt bao nhiêu bài trên tổng, bao nhiêu
 * bài một tuần (tính trên số tuần em CÒN HỌC, tức tới lượt cuối), và nếu đã đạt
 * hết thì mất mấy tuần kể từ ngày vào.
 * ⚠ Đây là con số MÔ HÌNH DỰ ĐOÁN dưới các giả định ở đầu tệp, không phải bằng
 * chứng phương pháp làm trẻ học nhanh hơn.
 */
function tocDoHoc(e) {
  const ra = {};
  for (const [mon, k] of [['toan', 'toan'], ['tienganh', 'ta']]) {
    const tong = e.tongBai?.[mon] ?? 0;
    if (!tong) { Object.assign(ra, { [`${k}_dat`]: null, [`${k}_tong`]: 0, [`${k}_baiMoiTuan`]: null, [`${k}_tuanXong`]: null }); continue; }
    const dat = Object.values(e.tienDo).filter((p) => p.mon === mon && p.pass);
    const luotMon = e.luot.filter((a) => a.mon === mon);
    const cuoi = luotMon.length ? luotMon[luotMon.length - 1].ts : e.mocVao;
    const tuanHoc = Math.max(1, (cuoi - e.mocVao) / (7 * NGAY));
    const xong = dat.length >= tong ? Math.max(...dat.map((p) => p.datLuc)) : null;
    Object.assign(ra, {
      [`${k}_dat`]: dat.length, [`${k}_tong`]: tong,
      [`${k}_baiMoiTuan`]: +(dat.length / tuanHoc).toFixed(1),
      [`${k}_tuanXong`]: xong ? +((xong - e.mocVao) / (7 * NGAY)).toFixed(1) : null,
    });
  }
  return ra;
}

function tomTat(ds) {
  const thang = (ms) => new Date(ms + VN).toISOString().slice(0, 7);
  const theoThang = {};
  for (const e of ds) {
    for (const a of e.luot) {
      const k = thang(a.ts);
      const x = theoThang[k] ||= { luot: 0, dung: 0, msTong: 0, em: new Set(), dungLanDau: 0, lanDau: 0 };
      x.luot += 1; x.dung += a.correct ? 1 : 0; x.msTong += a.ms; x.em.add(e.uid);
      if (a.tries === 1) { x.lanDau += 1; x.dungLanDau += a.correct ? 1 : 0; }
    }
  }
  const bang = Object.entries(theoThang).sort().map(([k, x]) => ({
    thang: k, soEmHoc: x.em.size, soLuot: x.luot,
    tiLeDungLanDau: +(x.dungLanDau / x.lanDau).toFixed(3),
    giayTrungBinh: +(x.msTong / x.luot / 1000).toFixed(1),
  }));
  const tungEm = ds.map((e) => {
    const nut = Object.values(e.mastery);
    const lanDau = e.luot.filter((a) => a.tries === 1);
    const nuaDau = lanDau.slice(0, Math.floor(lanDau.length / 2));
    const nuaSau = lanDau.slice(Math.floor(lanDau.length / 2));
    const ti = (x) => (x.length ? +(x.filter((a) => a.correct).length / x.length).toFixed(3) : null);
    return {
      ma: e.ma, lop: e.lop, gioi: e.gioi, vao: ngayVN(e.mocVao), soPhien: e.soPhien,
      soLuot: e.luot.length, baiDat: Object.values(e.tienDo).filter((p) => p.pass).length,
      nutThao: nut.filter((m) => m.mastered).length, tongNut: nut.length,
      dungNuaDau: ti(nuaDau), dungNuaSau: ti(nuaSau),
      phut: Math.round(Object.values(e.gio).reduce((s, g) => s + g.giayLam + g.giayXem, 0) / 60),
      chuongDat: Object.values(e.kyChuong).filter((c) => c.dat).length,
      lanThiChuong: Object.values(e.kyChuong).reduce((x, c) => x + c.lan, 0),
      ...tocDoHoc(e),
    };
  });
  /* Theo lớp: số em, và số tuần trung vị để xong cả chương trình (chỉ tính em đã xong). */
  const trungVi = (x) => { const a = x.filter((v) => v != null).sort((p, q) => p - q); return a.length ? a[Math.floor(a.length / 2)] : null; };
  const theoLop = [1, 2, 3, 4, 5].map((l) => {
    const ds2 = tungEm.filter((e) => e.lop === l);
    return {
      lop: l, soEm: ds2.length,
      toan_xongCT: ds2.filter((e) => e.toan_tuanXong != null).length,
      toan_tuanTrungVi: trungVi(ds2.map((e) => e.toan_tuanXong)),
      toan_baiMoiTuanTV: trungVi(ds2.map((e) => e.toan_baiMoiTuan)),
      ta_xongCT: ds2.filter((e) => e.ta_tuanXong != null).length,
      ta_tuanTrungVi: trungVi(ds2.map((e) => e.ta_tuanXong)),
      ta_baiMoiTuanTV: trungVi(ds2.map((e) => e.ta_baiMoiTuan)),
    };
  });
  /* ĐƯỜNG HỌC — hai cách nhìn không bị lẫn bởi việc em mới vào giữa chừng:
       theo tuần kể từ ngày CHÍNH EM vào học;
       theo lần gặp thứ k của CÙNG một nút (đường học kinh điển của BKT). */
  const tuan = {}, lanGap = {};
  for (const e of ds) {
    const dem = {};
    for (const a of e.luot) {
      if (a.tries !== 1) continue;
      const w = Math.floor((a.ts - e.mocVao) / (7 * NGAY)) + 1;
      const x = tuan[w] ||= { n: 0, dung: 0, ms: 0, em: new Set() };
      x.n += 1; x.dung += a.correct ? 1 : 0; x.ms += a.ms; x.em.add(e.uid);
      const k = Math.min(10, (dem[a.bktUnit] = (dem[a.bktUnit] || 0) + 1));
      const y = lanGap[k] ||= { n: 0, dung: 0 };
      y.n += 1; y.dung += a.correct ? 1 : 0;
    }
  }
  const theoTuanHoc = Object.entries(tuan).map(([w, x]) => ({
    tuan: +w, soEm: x.em.size, soLuot: x.n,
    tiLeDung: +(x.dung / x.n).toFixed(3), giayTB: +(x.ms / x.n / 1000).toFixed(1),
  })).filter((r) => r.soEm >= 5).sort((a, b) => a.tuan - b.tuan);
  const theoLanGap = Object.entries(lanGap).map(([k, y]) => ({
    lanGap: +k === 10 ? '10+' : +k, soLuot: y.n, tiLeDung: +(y.dung / y.n).toFixed(3),
  }));
  return { theoThang: bang, theoTuanHoc, theoLanGap, theoLop, tungEm };
}

function ghiRa(ds) {
  fs.mkdirSync(RA, { recursive: true });
  const tt = tomTat(ds);
  fs.writeFileSync(path.join(RA, 'tom_tat.json'), JSON.stringify({
    ghiChu: 'DỮ LIỆU MÔ PHỎNG — 30 học sinh ảo, không phải người thật.',
    hat: HAT, phienBan: PHIEN_BAN, soEm: ds.length, ...tt,
  }, null, 2));
  const cot = ['learnerId', 'sessionId', 'microId', 'bktUnit', 'itemId', 'phase', 'mon', 'khoiLop',
    'correct', 'tries', 'hintsUsed', 'ms', 'ts'];
  const dong = [cot.join(',') + ',tsISO'];
  for (const e of ds) for (const a of e.luot) dong.push(cot.map((c) => a[c]).join(',') + ',' + iso(a.ts));
  fs.writeFileSync(path.join(RA, 'nhat_ky_mo_phong.csv'), dong.join('\n'));
  return tt;
}

/* ─────────── MÁY CHỦ — REST bằng token của `firebase login` ─────────── */

function token() {
  const cfg = path.join(os.homedir(), '.config/configstore/firebase-tools.json');
  const t = JSON.parse(fs.readFileSync(cfg, 'utf8')).tokens;
  if (!t?.access_token || (t.expires_at && t.expires_at < Date.now() + 120000)) {
    throw new Error('Token hết hạn — chạy `firebase projects:list` một lần rồi chạy lại.');
  }
  return t.access_token;
}
const H = () => ({ Authorization: `Bearer ${token()}`, 'Content-Type': 'application/json' });
const GOC_FS = `projects/${DU_AN}/databases/(default)/documents`;
const API_FS = `https://firestore.googleapis.com/v1/${GOC_FS}`;

const giaTri = (v) => {
  if (v === null || v === undefined) return { nullValue: null };
  if (v instanceof Date) return { timestampValue: v.toISOString() };
  if (typeof v === 'boolean') return { booleanValue: v };
  if (typeof v === 'number') return Number.isInteger(v) ? { integerValue: String(v) } : { doubleValue: v };
  if (typeof v === 'string') return { stringValue: v };
  if (Array.isArray(v)) return { arrayValue: { values: v.map(giaTri) } };
  return { mapValue: { fields: truong(v) } };
};
const truong = (o) => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, giaTri(v)]));

async function goi(url, body, method = 'POST') {
  for (let lan = 0; ; lan++) {
    const r = await fetch(url, { method, headers: H(), body: body ? JSON.stringify(body) : undefined });
    if (r.ok) return r.json();
    if (lan < 4 && [429, 500, 503].includes(r.status)) { await new Promise((x) => setTimeout(x, 1500 * (lan + 1))); continue; }
    throw new Error(`${method} ${url.split('?')[0]} → ${r.status} ${(await r.text()).slice(0, 300)}`);
  }
}

async function ghiLo(ghi) {
  for (let i = 0; i < ghi.length; i += 450) {
    const lo = ghi.slice(i, i + 450);
    const kq = await goi(`${API_FS}:batchWrite`, { writes: lo });
    const hong = (kq.status || []).filter((s) => s.code);
    if (hong.length) throw new Error(`batchWrite hỏng ${hong.length}: ${JSON.stringify(hong[0])}`);
    process.stdout.write('.');
  }
}
const datDoc = (duong, du) => ({ update: { name: `${GOC_FS}/${duong}`, fields: truong(du) } });
const xoaDoc = (ten) => ({ delete: ten });

async function taoTaiKhoan(e) {
  const ID = `https://identitytoolkit.googleapis.com/v1/projects/${DU_AN}`;
  const co = await goi(`${ID}/accounts:lookup`, { localId: [e.uid] });
  if (!co.users?.length) {
    await goi(`${ID}/accounts`, { localId: e.uid, email: e.email, emailVerified: true, displayName: e.displayName });
  }
  await goi(`${ID}/accounts:update`, { localId: e.uid, customAttributes: JSON.stringify({ role: 'learner' }) });
}

const maTep = (id) => String(id).replace(/[:.]/g, '_');

async function day(ds) {
  const bayGio = Date.now();
  for (const e of ds) {
    await taoTaiKhoan(e);
    const lanCuoi = e.luot.length ? e.luot[e.luot.length - 1].serverTs : null;
    const ghi = [datDoc(`users/${e.uid}`, {
      uid: e.uid, email: e.email, role: 'learner', displayName: e.displayName,
      bietDanh: e.bietDanh, grade: e.lop, profileComplete: true,
      createdAt: e.mocVao, lastStudiedAt: lanCuoi ? new Date(lanCuoi) : null,
      moPhong: true,
      moPhongMeta: {
        ghiChu: 'Học sinh MÔ PHỎNG cho thực nghiệm luận văn — không phải người thật.',
        hat: HAT, phienBan: PHIEN_BAN, gioi: e.gioi, tiepThu: e.tiepThu, tuanMucTieu: e.tuanMucTieu, taoLuc: bayGio,
      },
    })];
    for (const a of e.luot) ghi.push(datDoc(`attempts/${a.id}`, { ...a, serverTs: new Date(a.serverTs) }));
    for (const [nut, m] of Object.entries(e.mastery)) {
      const { _mon, ...con } = m;
      ghi.push(datDoc(`mastery/${e.uid}/units/${encodeURIComponent(nut)}`, {
        ...con, unit: nut, learnerId: e.uid, nguongVer: 1, mon: _mon, maNutDs: null, moPhong: true,
      }));
    }
    for (const p of Object.values(e.tienDo)) {
      const kho = p.mon === 'toan' ? 'progress' : 'progressTA';
      const { mon, datLuc, ...con } = p;
      ghi.push(datDoc(`${kho}/${e.uid}/micros/${maTep(p.microId)}`, {
        ...con, serverTs: new Date(p.at), moPhong: true,
      }));
    }
    for (const c of Object.values(e.kyChuong)) {
      const at = new Date(c.at).toISOString();
      if (c.mon === 'toan') {
        ghi.push(datDoc(`hocBa/${e.uid}/muc/chuong_${c.khoa.replace(/[^A-Za-z0-9]+/g, '_')}`, {
          loai: 'chuong', khoa: c.khoa, serverTs: new Date(c.at), moPhong: true,
          giaTri: { total: 10, best: c.best, pass: c.dat, chuong: c.chuong, chuongTrinh: c.ma,
                    done: true, attempts: c.lan, at },
        }));
      } else {
        ghi.push(datDoc(`hocBaTA/${e.uid}/muc/chuong__${c.khoa.replace(/[^A-Za-z0-9]+/g, '_')}`, {
          loai: 'chuong', khoa: c.khoa, at, serverTs: new Date(c.at), moPhong: true,
          giaTri: { tong: 10, best: c.best, dat: c.dat, at },
        }));
      }
    }
    for (const g of Object.values(e.gio)) {
      const kho = g.mon === 'toan' ? 'hocBa' : 'hocBaTA';
      ghi.push(datDoc(`${kho}/${e.uid}/muc/gio_${g.ngay.replace(/-/g, '_')}`, {
        loai: 'gio', ngay: g.ngay, giayLam: g.giayLam, giayXem: g.giayXem,
        giay: g.giayLam + g.giayXem, soLuot: g.soLuot, baiCuoi: g.baiCuoi, at: g.at,
        serverTs: new Date(g.at), moPhong: true,
      }));
    }
    process.stdout.write(`\n${e.displayName} (lớp ${e.lop}): ${ghi.length} tài liệu `);
    await ghiLo(ghi);
  }
  console.log('\nxong.');
}

async function liet(cha, col, loc) {
  const ra = [];
  let sau = null;
  for (;;) {
    const sq = {
      from: [{ collectionId: col }], orderBy: [{ field: { fieldPath: '__name__' } }], limit: 500,
      ...(loc ? { where: loc } : {}),
      ...(sau ? { startAt: { values: [{ referenceValue: sau }], before: false } } : {}),
    };
    const kq = await goi(`${API_FS}${cha}:runQuery`, { structuredQuery: sq });
    const docs = kq.filter((x) => x.document).map((x) => x.document.name);
    ra.push(...docs);
    if (docs.length < 500) return ra;
    sau = docs[docs.length - 1];
  }
}

async function xoa({ giuTaiKhoan = false } = {}) {
  const loc = (f, v) => ({ fieldFilter: { field: { fieldPath: f }, op: 'EQUAL', value: v } });
  const users = await liet('', 'users', loc('moPhong', { booleanValue: true }));
  const uids = users.map((n) => n.split('/').pop());
  console.log(`${uids.length} học sinh mô phỏng`);
  for (const uid of uids) {
    const ten = [];
    ten.push(...await liet('', 'attempts', loc('learnerId', { stringValue: uid })));
    for (const [cha, col] of [['mastery', 'units'], ['progress', 'micros'], ['progressTA', 'micros'],
      ['hocBa', 'muc'], ['hocBaTA', 'muc'], ['reviewQueue', 'cards']]) {
      ten.push(...await liet(`/${cha}/${uid}`, col));
    }
    ten.push(`${GOC_FS}/report/${uid}`);
    if (!giuTaiKhoan) ten.push(`${GOC_FS}/users/${uid}`);
    process.stdout.write(`\n${uid}: xoá ${ten.length} `);
    await ghiLo(ten.map(xoaDoc));
    if (giuTaiKhoan) continue;
    await goi(`https://identitytoolkit.googleapis.com/v1/projects/${DU_AN}/accounts:delete`, { localId: uid })
      .catch((e) => console.warn(' (tài khoản Auth:', e.message.slice(0, 80), ')'));
  }
  console.log('\nđã gỡ sạch.');
}

/* ─────────── CHẠY ─────────── */

if (lenh === 'xoa') {
  if (!co('that')) { console.error('Thêm --that để xoá thật trên dự án', DU_AN); process.exit(1); }
  await xoa({ giuTaiKhoan: co('giu-tai-khoan') });
} else if (lenh === 'sinh' || lenh === 'day') {
  const ds = sinh();
  const tt = ghiRa(ds);
  console.table(tt.theoThang);
  console.table(tt.theoTuanHoc);
  console.table(tt.theoLanGap);
  console.table(tt.theoLop);
  if (co('chi-tiet')) console.table(tt.tungEm);
  console.log(`tổng: ${ds.reduce((s, e) => s + e.luot.length, 0)} lượt · tệp ở ${path.relative(GOC, RA)}/`);
  if (lenh === 'day') {
    if (!co('that')) { console.error('Thêm --that để ghi thật lên dự án', DU_AN); process.exit(1); }
    await day(ds);
  }
} else {
  console.error('Dùng: node tools/mo_phong/hoc_sinh_ao.mjs <sinh|day|xoa> [--that] [--hat N] [--em N]');
  process.exit(1);
}
