/**
 * Nạp nội dung bài học từ thư mục tĩnh (Hosting/CDN) — không cần API.
 * Cấu trúc thư mục public/:
 *    content/lessons/DL_KSN5Q1_B49_M1.json
 *    content/figures/KSN5Q1_B49_M1_F1.png
 */
const BASE = import.meta?.env?.BASE_URL || '/';
export const CONTENT = BASE.replace(/\/$/, '') + '/content';

/**
 * Dấu phiên bản nội dung — vite.config.js băm public/content rồi dán vào đây.
 * Nội dung để `immutable` 7 ngày mà tên tệp không đổi, nên không có dấu này thì
 * sửa bài xong đẩy lên, máy đã từng mở trang vẫn học bản cũ suốt một tuần.
 * Chạy bằng node (bộ kiểm) thì không có biến, lùi về 'dev' — vô hại.
 */
export const NOI_DUNG_V =
  typeof __NOI_DUNG_V__ === 'string' ? __NOI_DUNG_V__ : 'dev';

/** Gắn dấu phiên bản vào một đường dẫn nội dung */
export const dongDau = (url, v = NOI_DUNG_V) =>
  (v && v !== 'dev' ? `${url}?v=${v}` : url);

/** DL:KSN5Q1.B49.M1 → DL_KSN5Q1_B49_M1 */
export const idToFile = (microId) => microId.replace('DL:', 'DL_').replace(/\./g, '_');

/* ─────────── HAI CHƯƠNG TRÌNH, MỘT BỘ MÃ ───────────
 * Lớp 2 và lớp 5 dùng chung mọi màn hình; khác nhau chỉ ở NỘI DUNG và ở nhịp đọc.
 * Chỗ khai khác biệt duy nhất là data/chuong_trinh.json — đừng rải điều kiện
 * "nếu là lớp 2 thì…" ra khắp các component, vì thêm lớp thứ ba là phải đi sửa lại
 * từng chỗ một.
 */
/* Sổ đăng ký chương trình. Đọc từ content/chuong_trinh.json khi app khởi động; có
   sẵn bản tối thiểu để bộ kiểm chạy bằng node (không có mạng) vẫn dùng được.
   THÊM LỚP/MÔN MỚI thì thêm mục trong data/chuong_trinh.json, KHÔNG sửa tệp này. */
let SO_DK = {
  mon: { toan: { ten: 'Toán', bieuTuong: '🔢' } },
  chuongTrinh: {
    lop2: { ma: 'lop2', mon: 'toan', lop: 2, thuMuc: 'lop2', tienTo: 'DL:KSN2.',
            ten: 'Toán Tư Duy lớp 2', soBai: 33, doc: { chuTo: true } },
    lop5: { ma: 'lop5', mon: 'toan', lop: 5, thuMuc: 'lessons', tienTo: 'DL:KSN5Q1.',
            ten: 'Toán Tư Duy lớp 5', soBai: 168, doc: { chuTo: false } },
  },
  sapCo: [], luyenThi: [],
};

export const soDangKy = () => SO_DK;
export const dsChuongTrinh = () => Object.values(SO_DK.chuongTrinh || {});

/**
 * Các quyển theo ĐÚNG THỨ TỰ HIỆN LÊN KỆ SÁCH: lớp 2 → 3 → 4 → 5 → tổng ôn lớp 5.
 *
 * Thứ tự khai trong tệp KHÔNG dùng được: sổ vốn khai theo thứ tự làm xong quyển
 * (lop2, lop5, lop5q2, lop3, lop4), nên kệ sách hiện lớp 5 nằm giữa lớp 2 và lớp 3.
 * Chèn quyển mới vào giữa thì chỉ sửa `thuTu`, không phải chép lại cả sổ.
 *
 * Quyển chưa khai `thuTu` xuống cuối chứ không lên đầu — quyển mới thêm mà quên khai
 * thì nó nằm sau các quyển đã xếp, không đội lên trên đầu kệ.
 */
export const dsChuongTrinhSapXep = () => dsChuongTrinh()
  .slice()
  .sort((a, b) => (a.thuTu ?? 99) - (b.thuTu ?? 99)
                  || String(a.ma).localeCompare(String(b.ma)));
export const chuongTrinh = (ma) => (SO_DK.chuongTrinh || {})[ma] || SO_DK.chuongTrinh.lop5;
export const cachDoc = (id) => chuongTrinh(chuongTrinhCua(id)).doc || {};

/**
 * Đặt sổ đăng ký từ một đối tượng đã có sẵn.
 *
 * Bộ kiểm chạy bằng node thì không fetch được, mà bản mặc định ở trên chỉ có lớp 2 và
 * lớp 5 — nên `chuongTrinhCua('DL:KSN3.B01')` lùi về 'lop5' và mọi phép đếm theo quyển
 * lệch trong im lặng. Có cửa này thì phép kiểm nạp thẳng tệp thật, đo đúng cái đang chạy.
 */
export function datSoDangKy(json) {
  if (json?.chuongTrinh) SO_DK = { ...SO_DK, ...json };
  return SO_DK;
}

export async function napSoDangKy() {
  try {
    const r = await fetch(dongDau(`${CONTENT}/chuong_trinh.json`));
    if (r.ok) datSoDangKy(await r.json());
  } catch { /* mất mạng: dùng bản mặc định, không chặn bé học */ }
  return SO_DK;
}

/** Bài thuộc chương trình nào — tra TIỀN TỐ mã bài trong sổ đăng ký.
 *  Trước đây so cứng 'DL:KSN2.' trong mã; thêm lớp thứ ba là phải sửa hàm này. */
export const chuongTrinhCua = (id) => {
  const s = String(id || '');
  for (const ct of dsChuongTrinh()) if (ct.tienTo && s.startsWith(ct.tienTo)) return ct.ma;
  return 'lop5';
};

const THU_MUC_CUA = (ma) => chuongTrinh(ma).thuMuc || 'lessons';
export const thuMucCua = THU_MUC_CUA;

/** Quyển này có đi theo NHỊP ĐỌC CHẬM không (chữ to, mỗi màn một mục)?
 *
 *  Trước đây App.jsx hỏi thẳng `chuongTrinh === 'lop2'`. Đúng chừng nào chỉ có một
 *  quyển đọc chậm — thêm lớp 3 là bốn chỗ phải sửa, và quên một chỗ thì bé lớp 3 rơi
 *  vào phòng học của lớp 5: chữ nhỏ, dồn nhiều khối một màn. Sổ đăng ký đã khai sẵn
 *  cờ này, hỏi cờ thì thêm quyển thứ ba, thứ tư cũng không phải sửa gì.
 */
export const nhipDocCham = (ma) => !!(chuongTrinh(ma).doc || {}).moiManMotMuc;
export const baiDocCham = (id) => nhipDocCham(chuongTrinhCua(id));

/** Tiền tố tệp kỳ sát hạch: 'DL:KSN3.' → 'KSN3' (tệp reviews/DCR_KSN3_C1.json). */
export const maKy = (ma) => (chuongTrinh(ma).tienTo || 'DL:KSN5Q1.')
  .replace(/^[A-Z]+:/, '').replace(/\.$/, '');

/* Chương của từng bài lớp 2 nằm trong dữ liệu (8 chương, số bài mỗi chương khác
   nhau) chứ không suy ra được bằng công thức như lớp 5. Nạp chỉ mục là ghi nhớ. */
const chuongCua = new Map();
const baiCua = new Map();          // mã chương trình → danh sách bài đúng thứ tự học
export function ghiNhoChuong(danhSach) {
  const ids = [];
  for (const b of danhSach || []) {
    if (!b?.id) continue;
    ids.push(b.id);
    if (b.chuong) chuongCua.set(b.id, b.chuong);
  }
  if (ids.length) baiCua.set(chuongTrinhCua(ids[0]), ids);
}

/** B49.M1 (dạng gọn người dùng gõ) → DL:KSN5Q1.B49.M1 */
export const shortToId = (s) => (s.startsWith('DL:') ? s : `DL:KSN5Q1.${s}`);

const cache = new Map();

export async function loadLesson(microId) {
  if (cache.has(microId)) return cache.get(microId);
  const url = dongDau(`${CONTENT}/${THU_MUC_CUA(chuongTrinhCua(microId))}/${idToFile(microId)}.json`);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Không nạp được bài ${microId} (${res.status})`);
  const data = await res.json();
  cache.set(microId, data);
  return data;
}

/* ─────────── BÀI NÀY THUỘC DẠNG BÀI NÀO ───────────
 *
 * `chu_de.json` mang sẵn bảng tra ngược `baiDang` (tools/dung_chu_de.py dựng), nên
 * ở đây chỉ nạp một lần rồi tra bằng khoá.
 *
 * Dùng để đóng dấu `dangBai` lên từng lượt trả lời gửi về máy chủ: cô giáo lọc sổ
 * theo DẠNG BÀI của ma trận, chứ không chỉ theo từng bài rời. `bktUnit` đã có sẵn
 * trả lời câu "con mắc ở micro nào"; `dangBai` trả lời câu khác hẳn — "cả lớp đang
 * yếu MẢNG kiến thức nào", câu mà nhìn theo bài thì không bao giờ thấy.
 *
 * Nạp HỎNG thì trả về mảng rỗng chứ không ném lỗi: thiếu một nhãn phân loại không
 * đáng để mất trắng nhật ký học của con.
 */
let BAN_DO_DANG = null;
let TEN_DANG = null;
let dangDoi = null;

export async function napBanDoDang() {
  if (BAN_DO_DANG) return BAN_DO_DANG;
  if (!dangDoi) {
    dangDoi = fetch(dongDau(`${CONTENT}/chu_de.json`))
      .then((r) => (r.ok ? r.json() : null))
      .then((b) => {
        BAN_DO_DANG = (b && b.baiDang) || {};
        TEN_DANG = Object.fromEntries(
          Object.entries((b && b.dang) || {}).map(([k, v]) => [k, v.ten]));
        return BAN_DO_DANG;
      })
      .catch(() => { BAN_DO_DANG = {}; TEN_DANG = {}; return BAN_DO_DANG; });
  }
  return dangDoi;
}

/** Mã dạng bài của một micro — mảng rỗng khi bản đồ chưa nạp hoặc bài chưa vào thang. */
export const dangCuaBai = (microId) => (BAN_DO_DANG || {})[microId] || [];

/** Tên đọc được của một mã dạng bài; chưa nạp bản đồ thì trả lại chính cái mã. */
export const tenDang = (ma) => (TEN_DANG || {})[ma] || ma;

/**
 * figureSpec lưu "figures/KSN5Q1_B49_M1_F1.png" → URL đầy đủ.
 * Mỗi hình đã có mã kiểm riêng, dùng luôn làm dấu phiên bản: vẽ lại MỘT hình thì
 * chỉ hình ấy được tải lại, 671 hình còn lại vẫn nằm yên trong bộ nhớ đệm.
 */
export const figureSrc = (fig) =>
  (fig?.file ? dongDau(`${CONTENT}/${fig.file}`, fig.sha256_16 || NOI_DUNG_V) : null);

/** Danh sách 168 micro theo đúng thứ tự học */
export function allMicroIds(ct = 'lop5') {
  if (ct !== 'lop5') return baiCua.get(ct) || [];
  const out = [];
  for (let b = 1; b <= 56; b++) for (const k of [1, 2, 3]) out.push(`DL:KSN5Q1.B${b}.M${k}`);
  return out;
}

/** Micro kế tiếp / trước đó — ưu tiên series.next trong dữ liệu, không có thì theo thứ tự */
export function neighborIds(microId, lesson) {
  const list = allMicroIds();
  const i = list.indexOf(microId);
  const next = lesson?.series?.next && lesson.series.next.startsWith('DL:')
    ? lesson.series.next : (i >= 0 && i < list.length - 1 ? list[i + 1] : null);
  const prev = lesson?.series?.prev && lesson.series.prev.startsWith('DL:')
    ? lesson.series.prev : (i > 0 ? list[i - 1] : null);
  return { prev, next };
}

/** Chương của một bài. Lớp 5 suy ra bằng công thức, quyển khác tra bảng đã ghi nhớ. */
export const chapterOf = (microId) => {
  if (chuongCua.has(microId)) return chuongCua.get(microId);
  /* Chưa nạp chỉ mục của quyển ấy. Hỏi CỜ nhịp đọc chứ không so 'lop2': bản cũ so
     tên nên bài lớp 3·4 rơi vào công thức của lớp 5 và nhận chương 9, 10, 11 — số
     chương không tồn tại, chương trống trơn mà chẳng có gì báo. */
  if (chuongTrinhCua(microId) !== 'lop5') return 1;
  const b = Number(String(microId).split('.B')[1]?.split('.M')[0]);
  return Number.isFinite(b) ? Math.ceil(b / 4) : 1;
};

/* ═════════════ CHỈ MỤC CHUẨN HOÁ CỦA MỘT QUYỂN ═════════════
 *
 * Bốn quyển vốn khai chỉ mục theo hai hình dạng khác nhau:
 *   · lớp 2·3·4  `<thuMuc>/index.json` — MẢNG, mỗi bài một mục, có sẵn `chuong`,
 *                `tenChuong`, `soCau`;
 *   · lớp 5      `index_micro.json` — ĐỐI TƯỢNG khoá theo mã bài, không có chương,
 *                không có tên chương (tên chương gõ cứng trong JSX).
 *
 * Nên trang chính của lớp 5 và của lớp 2 là hai tệp khác hẳn nhau, và bốn quyển cho
 * bốn trải nghiệm khác nhau. Hàm này đưa cả bốn về MỘT hình dạng, để một màn hình
 * dùng chung được — khác biệt còn lại (khoá bài, Mùa giải, ba ải) đọc từ sổ đăng ký.
 *
 * Trả về: { ma, bai: [...], chuong: [{so, ten, bai:[...]}], onTap: [...], ai: [...] }
 */
const chiMucCache = new Map();

const soBaiCua = (id) => {
  const m = String(id).match(/\.B(\d+)/);
  return m ? Number(m[1]) : 0;
};

async function napJson(url, mac) {
  try {
    const r = await fetch(dongDau(url));
    return r.ok ? await r.json() : mac;
  } catch { return mac; }
}

export async function napChiMuc(ma) {
  if (chiMucCache.has(ma)) return chiMucCache.get(ma);
  const doi = (async () => {
    const ct = chuongTrinh(ma);
    const thuMuc = ct.thuMuc || 'lessons';
    let bai = [];

    if (ma === 'lop5') {
      /* Lớp 5 đánh chương bằng công thức (4 bài × 3 micro = 1 chương), tên chương
         khai trong sổ đăng ký. Thứ tự học lấy từ `allMicroIds` chứ không từ thứ tự
         khoá của tệp — tệp JSON không hứa giữ thứ tự nào cả. */
      const idx = await napJson(`${CONTENT}/index_micro.json`, {});
      const tenCh = Object.fromEntries((ct.chuong || []).map((c) => [c.so, c.ten]));
      bai = allMicroIds('lop5').map((id) => {
        const m = idx[id.replace(/[:.]/g, '_')] || {};
        const ch = chapterOf(id);
        return {
          id,
          so: soBaiCua(id),
          micro: Number(String(id).split('.M')[1]) || 1,
          ten: m.title || id.replace('DL:KSN5Q1.', ''),
          title: m.title || id,
          chuong: ch,
          tenChuong: tenCh[ch] || `Chương ${ch}`,
          durationMinutes: m.durationMinutes || null,
          bktUnit: m.bktUnit || null,
          objective: m.objective || '',
        };
      });
    } else {
      const ds = await napJson(`${CONTENT}/${thuMuc}/index.json`, []);
      ghiNhoChuong(ds);
      bai = (ds || []).map((b) => ({
        id: b.id,
        so: b.so,
        micro: 1,
        ten: b.ten || b.title || b.id,
        title: b.title || b.ten || b.id,
        chuong: b.chuong,
        tenChuong: b.tenChuong || `Chương ${b.chuong}`,
        durationMinutes: b.durationMinutes || null,
        bktUnit: b.bktUnit || null,
        objective: b.objective || '',
        soCau: b.soCau,
        soQuiz: b.soQuiz,
      }));
    }

    /* Danh mục kỳ ôn tập. Quy ước `<thuMuc>/ontap.json`, nhưng lớp 5 khai riêng qua
       `tepOnTap`: thuMuc của nó là `lessons`, mà thư mục ấy chỉ được chứa BÀI HỌC —
       bốn phép kiểm quét nó bằng `*.json` rồi đọc thẳng `j.id`. */
    const onTapAll = await napJson(
      `${CONTENT}/${ct.tepOnTap || `${thuMuc}/ontap.json`}`, []);

    /* Chương dựng TỪ BÀI THẬT, không từ `soChuong` khai trong sổ: khai lệch một số
       thì màn hình vẽ ra một chương rỗng, bấm vào không có gì — mà cổng vẫn xanh. */
    const theoChuong = new Map();
    for (const b of bai) {
      if (!theoChuong.has(b.chuong)) {
        theoChuong.set(b.chuong, { so: b.chuong, ten: b.tenChuong, bai: [] });
      }
      theoChuong.get(b.chuong).bai.push(b);
    }
    const chuong = [...theoChuong.values()].sort((x, y) => x.so - y.so);
    for (const c of chuong) {
      c.onTap = (onTapAll || []).filter((o) => o.loai !== 'ai' && o.chapter === c.so);
    }

    const kq = {
      ma,
      ten: ct.ten,
      /* Mang theo CỜ CHÍNH SÁCH của quyển, để nơi dùng không phải so tên: `ma === 'lop5'`
         rải khắp các màn là thêm quyển thứ năm phải đi sửa từng chỗ, mà quên một chỗ
         thì hỏng câm — đúng cái bẫy sổ tay đã ghi. */
      khoaBai: !!ct.khoaBai,
      bai,
      chuong,
      onTap: (onTapAll || []).filter((o) => o.loai !== 'ai'),
      /* Ba cửa ải cuối sách chỉ lớp 2·3 có — trộn đủ 8 chương, đánh số chương 9·10·11
         nên KHÔNG được lẫn vào danh sách chương thật. */
      ai: (onTapAll || []).filter((o) => o.loai === 'ai').sort((x, y) => x.so - y.so),
    };
    chiMucCache.set(ma, kq);
    return kq;
  })();
  chiMucCache.set(ma, doi);
  return doi;
}
