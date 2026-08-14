/**
 * NỘI DUNG MÔN TOÁN — nạp bài, chia chương, bản đồ dạng bài.
 *
 * Tách khỏi `chung/lib/soQuyen.js` (sổ đăng ký) vì đây là phần CHỈ Toán dùng: mã bài
 * `DL:KSN5Q1.B49.M1`, công thức chia chương của lớp 5, ma trận 82 dạng bài. Môn khác
 * có cách tổ chức nội dung riêng và không được thấy những thứ này.
 */
/* Những thứ Toán DÙNG TRỰC TIẾP từ sổ đăng ký — phải `import`, không chỉ tái xuất:
   `export … from` chỉ chuyển tiếp ra ngoài, KHÔNG đưa tên vào phạm vi tệp này. */
import {
  CONTENT, NOI_DUNG_V, chuongTrinh, chuongTrinhCua, dongDau, idToFile, thuMucCua,
} from '../../../chung/lib/soQuyen.js';

/* Tái xuất sổ đăng ký cho các màn của Toán: chúng chỉ cần biết MỘT cửa (`noiDung.js`),
   không phải nhớ thứ nào nằm ở tầng chung, thứ nào của môn. Tầng chung thì ngược lại —
   nó KHÔNG BAO GIỜ được nhìn ngược vào đây, cổng `ranh_gioi.test.mjs` chặn. */
export {
  CONTENT, dongDau, chuongTrinh, chuongTrinhCua, thuMucCua,
  soDangKy, dsChuongTrinh, dsChuongTrinhSapXep, napSoDangKy, datSoDangKy,
  cachDoc, nhipDocCham, baiDocCham, maKy, idToFile, NOI_DUNG_V,
  LOP_HOC, LOP_MAC_DINH, lopHopLe,
} from '../../../chung/lib/soQuyen.js';

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
  const url = dongDau(`${CONTENT}/${thuMucCua(chuongTrinhCua(microId))}/${idToFile(microId)}.json`);
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
      /* ⚠ `so` ĐẾM TỪ VỊ TRÍ, không đọc `b.so`.
         Bản cũ đọc trường `so` đã lưu, mà trường ấy phải khớp với con số nằm trong
         mã bài — nên chèn một bài vào giữa là phải đổi mã của mọi bài phía sau, rồi
         dời tiến độ đã lưu của từng bé cho khớp. Đổi số bài hoá ra là đụng vào dữ
         liệu thật của trẻ con, và sai một nấc thì huy hiệu trỏ nhầm bài mà chẳng có
         gì báo.
         Bác chốt lối C: mã bài chỉ còn là CÁI TÊN. Bài đứng thứ mấy trong mảng thì
         mang số ấy — một sự thật duy nhất, và nó tự đúng. Thứ tự mảng do
         `data/lop<N>/thu_tu.json` khai ra, bộ dựng giữ nguyên khi ghi index.json. */
      bai = (ds || []).map((b, i) => ({
        id: b.id,
        so: i + 1,
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
