/**
 * DỮ LIỆU HỌC CỦA MÔN TIẾNG ANH — tiến độ và học bạ trên máy chủ.
 *
 * Mọi collection ở đây là CỦA RIÊNG TIẾNG ANH. Chỉ dùng chung với môn khác đúng hai
 * thứ: thể hiện Firebase (`chung/lib/nenTang.js`) và tài khoản (`chung/lib/taiKhoan.js`).
 *
 * ── VÌ SAO KHÔNG DÙNG CHUNG `progress/{uid}/micros` VỚI TOÁN ──
 * Không phải vì sợ trùng mã bài (`DL:TA1.B04` khác `DL:KSN2.B04` sẵn rồi). Lý do thật:
 * Cloud Function nền chạy trên MỌI tài liệu của thư mục ấy và xử theo luật của Toán —
 * tính mức thạo BKT theo ma trận Toán, dựng sổ học theo dạng bài Toán. Đổ bài tiếng
 * Anh vào đó là hàm nền âm thầm tính sai cho cả hai môn, mà không có gì báo.
 *
 * ── ⚠ PHẢI DEPLOY LUẬT TRƯỚC KHI GHI ──
 * `firestore.rules` kết bằng `match /{document=**} { allow read, write: if false; }`.
 * Nghĩa là collection MỚI bị từ chối — và Firestore từ chối **trong im lặng** với
 * lệnh ghi không chờ kết quả: bé học xong, máy báo xong, mà máy chủ không có gì.
 * Đây là lỗi đã dính thật một lần khi làm học bạ (xem sổ ghi nhớ).
 *
 * Nên: luật cho `progressTA` và `hocBaTA` đã viết sẵn trong `firestore.rules`, nhưng
 * **phải `firebase deploy --only firestore:rules`** thì mới có tác dụng. Trước khi
 * deploy thì `LOI_GHI` dưới đây đếm số lần bị từ chối để còn biết mà lần ra.
 */
import {
  doc, getDoc, setDoc, collection, getDocs, serverTimestamp, writeBatch,
} from 'firebase/firestore';
import { db, hasFirebase } from '../../../chung/lib/nenTang.js';
import {
  KHO_SU_KIEN, dungSuKien, xepHang, dayHangDoi, laHocSinhThat,
} from './suKien.js';

/** Tên collection — gõ MỘT chỗ. Hậu tố TA để không bao giờ lẫn với Toán. */
export const KHO = {
  tienDo: (uid) => `progressTA/${uid}/micros`,
  hocBa: (uid) => `hocBaTA/${uid}/muc`,
  /* ⚠ THẺ ÔN DÙNG CHUNG THƯ MỤC VỚI TOÁN, khác hẳn hai khoá trên.
     Hai khoá trên phải tách vì hàm nền xử theo luật của Toán. Còn `reviewQueue`
     thì hàm nền chỉ GHI vào, không đọc ra để tính gì — và mã thẻ nhúng `microId`
     mà mã bài hai môn không bao giờ trùng (`DL:TA5.*` với `DL:KSN2.*`). Bên đọc
     lọc theo tiền tố quyển (`theDenHan`), nên hai môn không thấy thẻ của nhau. */
  theOn: (uid) => `reviewQueue/${uid}/cards`,
};

/* Mã bài có dấu ':' và '.', mà tên tài liệu Firestore thì không chứa '/' và nên
   tránh dấu lạ — quy về gạch dưới, và quy NGƯỢC lại được để đọc ra. */
const maTep = (id) => String(id).replace(/[:.]/g, '_');

/**
 * Đếm số lần máy chủ từ chối. Không ném lỗi ra màn hình — bé đang học thì không
 * việc gì phải thấy — nhưng cũng KHÔNG nuốt im: có số thì người sửa lần ra được.
 */
export const LOI_GHI = { tuChoi: 0, ganNhat: null };

const nuot = (e) => {
  LOI_GHI.tuChoi += 1;
  LOI_GHI.ganNhat = String(e?.code || e?.message || e);
  if (import.meta.env?.DEV) {
    // eslint-disable-next-line no-console
    console.warn('[tienganh] máy chủ từ chối ghi:', LOI_GHI.ganNhat,
      '— đã deploy firestore.rules cho progressTA/hocBaTA chưa?');
  }
};

const dungDuoc = (uid) => !!(hasFirebase && db && uid);

/* ─────────── NHẬT KÝ TỪNG LƯỢT TRẢ LỜI ─────────── */

/**
 * ĐẨY NHẬT KÝ — gọi sau MỖI lượt bé trả lời, không đợi hết bài.
 *
 * Đợi màn kết bài mới gửi thì bé làm 8/10 câu rồi mẹ gọi ăn cơm là mất trắng —
 * bên Toán đã tính ra tối đa 1141 câu trên toàn chương trình. Và cô giáo cũng
 * phải đợi bé học xong mới thấy gì.
 *
 * ⚠ VÀO `attempts/` CHUNG VỚI TOÁN, và đó là chủ ý — khác hẳn `progressTA` phải
 * tách. Lý do tách `progressTA` là hàm nền chạy trên mọi tài liệu của thư mục ấy
 * rồi tính theo ma trận Toán. Còn `onAttempt` thì chỉ làm đúng một việc TRUNG
 * TÍNH: đọc `bktUnit` rồi cập nhật mức thạo. Bảng cô giáo cũng đã đọc `attempts`
 * không lọc theo môn. Nên đổ vào đây là hàm nền BKT ăn được ngay, không phải sửa
 * một dòng nào phía đọc.
 *
 * Không ném lỗi ra ngoài: mất mạng thì bản ghi nằm lại hàng đợi, bé vẫn học tiếp.
 */
async function guiSuKien(ds) {
  if (!db) throw new Error('chưa cấu hình Firebase');
  const lo = writeBatch(db);
  for (const r of ds) {
    /* Đóng dấu máy chủ ĐÚNG LÚC GỬI. Bản ghi nằm chờ trong hàng đợi mấy ngày vì
       mất mạng thì `ts` (giờ máy bé) vẫn giữ nguyên lúc bé làm bài — hai mốc phục
       vụ hai việc khác nhau, và luật Firestore đòi `serverTs == request.time`. */
    lo.set(doc(db, KHO_SU_KIEN, r.id), { ...r, serverTs: serverTimestamp() }, { merge: true });
  }
  await lo.commit();
}

export async function luuSuKien({ uid, maPhien, microId, quyen, viec }) {
  if (!viec?.length) return { daGui: 0, conLai: 0 };
  let ds;
  try {
    ds = dungSuKien({ learnerId: uid || 'local', maPhien, microId, quyen, viec });
  } catch (e) { nuot(e); return { daGui: 0, conLai: 0, loi: true }; }
  xepHang(ds);
  /* Chưa đăng nhập thì CHỈ xếp hàng — đẩy lên với mã 'local' là luật từ chối, và
     từ chối trong im lặng. Đăng nhập xong `sangTenHangDoi` sẽ sang tên rồi gửi. */
  if (!laHocSinhThat(uid) || !hasFirebase || !db) {
    return { daGui: 0, conLai: ds.length, chiTaiMay: true };
  }
  try { return await dayHangDoi(guiSuKien); }
  catch (e) { nuot(e); return { daGui: 0, conLai: ds.length, loi: true }; }
}

/* ─────────── MỨC THẠO TỪNG NÚT (BKT) ─────────── */

/**
 * Đọc mức thạo của bé, khoá theo MÃ NÚT đồ thị.
 *
 * `mastery/{uid}/units` do HÀM NỀN ghi (luật: `allow write: if false`), máy con
 * chỉ đọc. Hỏng thì trả `{}` — bộ chọn câu sẽ giữ nguyên thứ tự cũ và bé học y
 * như trước, không có gì lạ xảy ra.
 *
 * ⚠ Thư mục này dùng CHUNG với Toán, và không lọc theo môn ở đây: mã nút Tiếng
 * Anh (`v_g5_*` · `sp_g5_*`) không bao giờ trùng mã micro của Toán, nên bên dùng
 * cứ tra theo mã nút của chính câu mình đang xếp là đủ.
 */
export async function docMucThao(uid) {
  if (!dungDuoc(uid)) return {};
  try {
    const snap = await getDocs(collection(db, `mastery/${uid}/units`));
    const ra = {};
    snap.forEach((d) => { ra[d.id] = d.data(); });
    return ra;
  } catch (e) { nuot(e); return {}; }
}

/* ─────────── THẺ ÔN NGẮT QUÃNG ─────────── */

/**
 * Đọc thẻ ôn của bé.
 *
 * Hỏng thì trả MẢNG RỖNG chứ không ném: trang chính chỉ mất thẻ mời ôn tập, bé
 * vẫn học bình thường. Mất mạng không phải việc của bé.
 */
export async function docTheOn(uid) {
  if (!dungDuoc(uid)) return [];
  try {
    const snap = await getDocs(collection(db, KHO.theOn(uid)));
    const ra = [];
    snap.forEach((d) => ra.push({ id: d.id, ...d.data() }));
    return ra;
  } catch (e) { nuot(e); return []; }
}

/**
 * Ghi lại một thẻ sau khi bé ôn xong — hộp Leitner mới và ngày hẹn mới.
 *
 * ⚠ `merge: true`. Thẻ do HÀM NỀN tạo và giữ các trường máy con không biết
 * (`kind` · `what` · `createdAt`); ghi đè cả tài liệu là xoá mất chúng, và lần
 * sinh thẻ sau sẽ dựng lại từ đầu như thể bé chưa ôn lần nào.
 */
export async function luuTheOn(uid, the) {
  if (!dungDuoc(uid) || !the?.id) return false;
  try {
    await setDoc(doc(db, KHO.theOn(uid), the.id), {
      box: Number(the.box) || 0,
      dueAt: Number(the.dueAt) || Date.now(),
      lastResult: !!the.lastResult,
      reviewedAt: Number(the.reviewedAt) || Date.now(),
      soLanOn: Number(the.soLanOn) || 0,
    }, { merge: true });
    return true;
  } catch (e) { nuot(e); return false; }
}

/* ─────────── GHI ─────────── */

/**
 * Lưu kết quả một bài lên máy chủ.
 *
 * `merge: true` chứ không ghi đè: bé làm lại bài trên máy khác thì hai lần ghi
 * không xoá nhau, và `gopTienDo` ở tầng trên chọn bản mới hơn.
 */
export async function luuBai(uid, id, m) {
  if (!dungDuoc(uid)) return false;
  try {
    await setDoc(doc(db, KHO.tienDo(uid), maTep(id)), {
      microId: id,
      pass: !!m.pass,
      /* `score` và `pass` là hai trường luật Firestore ĐÒI phải có và đúng kiểu.
         Thiếu một trong hai là bị từ chối — và từ chối im lặng. */
      score: Number(m.best || 0),
      total: Number(m.total || 0),
      bac: Number(m.bac || 0),
      attempts: Number(m.attempts || 1),
      at: m.at || new Date().toISOString(),
      serverTs: serverTimestamp(),
    }, { merge: true });
    return true;
  } catch (e) { nuot(e); return false; }
}

/** Lưu một mục học bạ (kỳ ôn tập chương). */
export async function luuMucHocBa(uid, loai, khoa, du) {
  if (!dungDuoc(uid)) return false;
  try {
    await setDoc(doc(db, KHO.hocBa(uid), `${loai}__${maTep(khoa)}`), {
      loai, khoa, ...du, at: new Date().toISOString(), serverTs: serverTimestamp(),
    }, { merge: true });
    return true;
  } catch (e) { nuot(e); return false; }
}

/* ─────────── ĐỌC ─────────── */

async function docTienDo(uid) {
  const snap = await getDocs(collection(db, KHO.tienDo(uid)));
  const micros = {};
  snap.forEach((d) => {
    const v = d.data();
    if (v.microId) {
      micros[v.microId] = {
        done: true, pass: !!v.pass, best: v.score || 0, total: v.total || 0,
        bac: v.bac || 0, attempts: v.attempts || 1, at: v.at || null,
      };
    }
  });
  return micros;
}

async function docHocBa(uid) {
  const snap = await getDocs(collection(db, KHO.hocBa(uid)));
  const chapters = {}, baiViet = {}, soThich = {};
  let dinhDang = {};
  snap.forEach((d) => {
    const v = d.data();
    /* `|| {}` chứ KHÔNG `|| v`. Bản cũ đỡ lấy cả tài liệu khi thiếu `giaTri`, và
       cái đỡ ấy chính là thứ che mất chuyện bên ghi đang gửi sai hình dạng: đọc ra
       vẫn có gì đó, chỉ là thiếu `best` — thẻ huy hiệu hiện "undefined/undefined".
       Nay chỉ nhận đúng một hình dạng, giống hệt Toán (`toan/lib/duLieu.js`). */
    if (v.loai === 'chuong' && v.khoa) chapters[v.khoa] = v.giaTri || {};
    /* `viet` — bài viết ngắn, điểm do AI chấm. Đọc ở đây chứ không bỏ mặc: luật
       Firestore CHO ghi loại nào thì bên đọc phải nhặt đúng chừng ấy loại, nếu
       không thì ghi lên rồi bỏ đó — cổng `hocba_khop_luat.test.mjs` canh chuyện
       này, và nó canh vì đã xảy ra thật với chính `hocBaTA`. */
    else if (v.loai === 'viet' && v.khoa) baiViet[v.khoa] = v.giaTri || {};
    /* `soThich` — từ bé thích nhất trong quyển, cô giáo máy lấy làm ngữ cảnh. Cùng
       một luật với hai loại trên: luật CHO ghi loại nào thì bên đọc phải nhặt đúng
       chừng ấy, không thừa không thiếu. */
    else if (v.loai === 'soThich' && v.khoa) soThich[v.khoa] = v.giaTri || {};
    /* `hoSo` chỉ có MỘT mục cho cả môn — không khoá theo quyển: bé gõ chữ kém thì
       kém ở mọi quyển, chia nhỏ ra chỉ làm mẫu bé đi và chẳng dạng nào đủ mẫu. */
    else if (v.loai === 'hoSo') dinhDang = (v.giaTri || {}).dinhDang || {};
  });
  return { chapters, baiViet, soThich, dinhDang };
}

/**
 * Sổ tiến độ đầy đủ từ máy chủ. Hỏng chỗ nào thì trả rỗng chỗ ấy — bé vẫn học
 * được bằng sổ tại máy, đó mới là nguồn chính.
 */
export async function tienDoTuMay(uid) {
  if (!dungDuoc(uid)) return { micros: {}, chapters: {}, baiViet: {}, soThich: {}, dinhDang: {} };
  const [micros, hb] = await Promise.all([
    docTienDo(uid).catch((e) => { nuot(e); return {}; }),
    docHocBa(uid).catch((e) => {
      nuot(e); return { chapters: {}, baiViet: {}, soThich: {}, dinhDang: {} };
    }),
  ]);
  return {
    micros,
    chapters: hb.chapters || {},
    baiViet: hb.baiViet || {},
    soThich: hb.soThich || {},
    dinhDang: hb.dinhDang || {},
  };
}

/**
 * BẢNG XẾP HẠNG — đọc chung một tài liệu với Toán, và đó là CỐ Ý.
 *
 * `bangXepHang/global` là tài liệu DUY NHẤT một bé đọc được về bé khác, nên nó là
 * chỗ cẩn thận nhất của cả bộ luật: Cloud Function dựng nó và chỉ đặt vào biệt danh ·
 * lớp · sao. Dựng thêm một bảng thứ hai cho tiếng Anh nghĩa là mở thêm một lối rò dữ
 * liệu nữa — đắt hơn nhiều so với cái lợi.
 *
 * Nhưng hàm nền hiện CHỈ đếm sao của Toán. Nên ở đây trả `null` cho tới khi hàm ấy
 * biết tính cả tiếng Anh — trả một bảng chỉ có điểm Toán mà gắn nhãn "Tiếng Anh" thì
 * còn tệ hơn không có bảng.
 */
export async function bangXepHang() {
  if (!dungDuoc('x')) return null;
  try {
    const snap = await getDoc(doc(db, 'bangXepHang/global'));
    const d = snap.exists() ? snap.data() : null;
    return d && d.coTiengAnh ? d : null;
  } catch { return null; }
}
