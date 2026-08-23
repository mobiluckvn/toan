/**
 * SỰ KIỆN HỌC CỦA TIẾNG ANH — mỗi lượt trả lời một dòng, bất biến.
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 * Sổ `progressTA/{uid}/micros` chỉ biết "xong bài B04, được 8/10". Nó không biết
 * bé vững TỪ nào, yếu MẪU CÂU nào, làm câu nào lâu, hay mở gợi ý mấy lần. Mà toàn
 * bộ tầng thích ứng — BKT, đường cong học tập, lan truyền chẩn đoán — đều đứng
 * trên những thứ ấy. Nên đây là nhật ký THÔ: một dòng cho một lượt bấm trả lời.
 *
 * ── ⚠ CHÉP TỪ `mon/toan/lib/sync.js`, CỐ Ý KHÔNG IMPORT ──
 * Hình dạng bản ghi giống hệt bên Toán, và giống là CHỦ Ý: hàm nền `onAttempt`,
 * sổ bố mẹ và bảng cô giáo đọc chung một hình dạng. Nhưng KHÔNG được `import` —
 * cổng `ranh_gioi.test.mjs` chặn, và nó chặn vì một lý do đã xảy ra thật: hai môn
 * dính nhau thì sửa cho môn này là gãy môn kia, mà gãy lặng lẽ.
 *
 * Cái giá của việc chép là hai bản có thể trôi xa nhau. Nên cổng
 * `tienganh_sukien.test.mjs` so hình dạng hai bên, và mọi trường ở đây phải có
 * cùng TÊN và cùng NGHĨA với bên Toán.
 *
 * ── ⚠ SÁU TRƯỜNG BẮT BUỘC, THIẾU LÀ MẤT TRẮNG ──
 * `firestore.rules` đòi `['learnerId','microId','itemId','phase','correct','ts']`.
 * Thiếu một trường thì Firestore từ chối — và từ chối TRONG IM LẶNG với lệnh ghi
 * không chờ kết quả: bé học xong, màn hình báo xong, máy chủ không có gì.
 */
import { choDangDung, CHO_DAU } from '../../../chung/lib/nguoiDung.js';

/** Nhật ký của CẢ HAI MÔN chung một collection — xem ghi chú ở `KHO` dưới. */
export const KHO_SU_KIEN = 'attempts';

/**
 * ⚠ HÀNG ĐỢI RIÊNG, dù collection thì chung với Toán.
 *
 * Bản ghi đẩy lên `attempts/` chung được, và chung là ĐÚNG: bảng cô giáo đã đọc
 * collection ấy không lọc theo môn, mã bài hai môn không bao giờ trùng
 * (`DL:TA5.*` với `DL:KSN2.*`), nên hàm nền BKT ăn được ngay mà không phải sửa
 * một dòng nào phía đọc.
 *
 * Nhưng HÀNG ĐỢI TẠI MÁY thì phải tách. Nó nằm ở localStorage, và hai môn cùng
 * đọc-sửa-ghi một khoá là mất bản ghi: môn này đọc hàng đợi, môn kia ghi đè xong,
 * môn này ghi lại bản đã đọc — mất sạch phần môn kia vừa thêm. Không có gì báo,
 * vì mỗi bên đều thấy lệnh ghi của mình thành công.
 */
const QKEY_GOC = 'ttd5.queueTA.v1';
const qkey = () => {
  const cho = choDangDung();
  return cho === CHO_DAU ? QKEY_GOC : `${QKEY_GOC}.${cho}`;
};

/**
 * PHIÊN BẢN BẢN GHI. Nhật ký bất biến nên dòng ghi bằng luật cũ nằm lẫn mãi mãi.
 *   v = 2  cùng luật với Toán: `ms` đo riêng từng câu, `ts` riêng từng lượt.
 * Bắt đầu thẳng từ 2 chứ không từ 1: Tiếng Anh chưa từng ghi dòng nào, nên không
 * có dòng đời cũ để phải phân biệt — và dùng chung số với Toán thì bên đọc chỉ
 * cần một luật.
 */
export const PHIEN_BAN_BAN_GHI = 2;

export const laHocSinhThat = (id) => !!id && id !== 'local';

/** Mã phiên — một lần mở bài là một phiên. */
export const maPhienMoi = (khiNao = Date.now()) =>
  `p${khiNao.toString(36)}${Math.random().toString(36).slice(2, 7)}`;

/**
 * Mã bản ghi — nhúng đủ thứ để dựng lại LẦN NỮA cũng ra đúng mã cũ.
 *
 * Nhờ thế `enqueue` ghi đè theo mã, và đẩy lại bao nhiêu lần cũng không sinh dòng
 * trùng. Đây là cách bên Toán chống mất bản ghi khi mất mạng giữa chừng.
 */
export const maSuKien = (learnerId, maPhien, microId, itemId, seq) =>
  `${learnerId}_${maPhien}_${String(microId).replace(/[^A-Za-z0-9]+/g, '_')}_${itemId}_${seq}`;

export const CHU_TOI_DA = 120;
export function goiDapAn(v) {
  const s = Array.isArray(v) ? v.filter((x) => x !== undefined).join(' | ') : String(v ?? '');
  const g = s.replace(/\s+/g, ' ').trim();
  return g.length > CHU_TOI_DA ? `${g.slice(0, CHU_TOI_DA - 1)}…` : g;
}

/**
 * Dựng bản ghi từ nhật ký một phiên.
 *
 * viec: [{ itemId, maNut, maNutDs, ok, tries, hintsUsed, ms, phase,
 *          answer, expected, mode, khiNao }]
 *
 * ⚠ `bktUnit` LẤY TỪ `maNut` — MỘT nút, không phải cả `maNutDs`. Bản ghi chỉ mang
 * được một `bktUnit`; ghi hai nút cho một lượt là một câu đúng được tính công hai
 * lần, mức thạo phồng lên, và hệ thống hoá ra LẠC QUAN về bé — tức là cho bé đi
 * tiếp khi bé chưa vững. `maNutDs` vẫn ghi kèm để sau này lan truyền chẩn đoán
 * dùng, nhưng KHÔNG chỗ nào được lấy nó ra cộng điểm.
 */
export function dungSuKien({
  learnerId, maPhien, microId, viec, quyen = null, serverTs = null, now = Date.now,
}) {
  if (!learnerId || !maPhien || !microId) {
    throw new Error('thiếu learnerId/maPhien/microId');
  }
  const ts = now();
  return (viec || []).map((e, i) => ({
    id: maSuKien(learnerId, maPhien, microId, e.itemId, i),
    learnerId,
    sessionId: maPhien,
    microId,
    /* Nút của đồ thị tri thức — `v_g5_u1_city` hoặc `sp_g5_u1_1`. Đây là thứ biến
       sổ từ "xong bài" thành "vững từ nào". */
    bktUnit: e.maNut || null,
    maNutDs: Array.isArray(e.maNutDs) && e.maNutDs.length ? e.maNutDs : null,
    /* Quyển nào — để lọc theo môn/quyển mà không phải bóc chuỗi mã bài. */
    quyen,
    mon: 'tienganh',
    itemId: e.itemId,
    phase: e.phase || 'practice',
    correct: !!e.ok,
    tries: e.tries ?? 1,
    /* Số lần bé ĐƯỢC XEM gợi ý (H_req của mục 2.3.1). Bên Tiếng Anh gợi ý hiện TỰ
       ĐỘNG sau vài lần thử chứ không do bé bấm — nên đây là "đã thấy mấy gợi ý",
       không phải "đã xin mấy lần". Cùng tên trường với Toán để màn cô giáo hiện
       được ngay, nhưng nghĩa hơi khác và chỗ nào đọc cũng nên biết điều đó. */
    hintsUsed: e.hintsUsed ?? 0,
    ms: e.ms ?? null,
    answer: e.answer === undefined ? null : goiDapAn(e.answer),
    expected: e.expected === undefined ? null : goiDapAn(e.expected),
    mode: e.mode || null,
    /* ── VÂN TAY LỜI DẶN (mục 2.5.2 · "mã prompt để kiểm toán") ──
       Chỉ có ở lượt do MÔ HÌNH tham gia (bài viết, phòng nói); lượt trắc nghiệm
       thì `null`. Băm KHUNG lời dặn chứ không băm cả prompt — không lưu một chữ
       nào của bé. Nhờ trường này mới so được "mẫu prompt nào giúp bé tiến bộ hơn"
       (ΔC, mục 2.5.3). */
    mauPrompt: e.mauPrompt || null,
    phienBanMau: e.phienBanMau ?? null,
    vanTayPrompt: e.vanTayPrompt || null,
    v: PHIEN_BAN_BAN_GHI,
    /* Mốc RIÊNG từng lượt (màn hình đóng ngay lúc bé bấm). Dùng chung một mốc cho
       cả loạt thì mọi phép đo thời gian ra 0 — lỗi bên Toán đã dính. */
    ts: e.khiNao ?? ts,
    serverTs,
  }));
}

export function docHangDoi(kho = globalThis.localStorage) {
  try { return JSON.parse(kho?.getItem(qkey()) || '[]'); } catch { return []; }
}

export function ghiHangDoi(ds, kho = globalThis.localStorage) {
  try { kho?.setItem(qkey(), JSON.stringify(ds)); } catch { /* chế độ riêng tư */ }
  return ds;
}

/** Xếp vào hàng đợi — trùng mã thì ghi đè, không nhân bản. */
export function xepHang(ds, kho = globalThis.localStorage) {
  const q = docHangDoi(kho);
  const m = new Map(q.map((r) => [r.id, r]));
  for (const r of ds) m.set(r.id, r);
  return ghiHangDoi([...m.values()], kho);
}

/**
 * Đẩy hàng đợi lên máy chủ. Hỏng (mất mạng) thì GIỮ NGUYÊN phần chưa gửi.
 *
 * ⚠ Không bao giờ ném lỗi ra ngoài: bé đang học, mất mạng không phải việc của bé.
 */
export async function dayHangDoi(guiDi, kho = globalThis.localStorage, moLo = 200) {
  const q = docHangDoi(kho);
  if (!q.length) return { daGui: 0, conLai: 0 };
  let daGui = 0;
  try {
    for (let i = 0; i < q.length; i += moLo) {
      const mo = q.slice(i, i + moLo);
      await guiDi(mo);
      daGui += mo.length;
    }
  } catch {
    const con = q.slice(daGui);
    ghiHangDoi(con, kho);
    return { daGui, conLai: con.length, loi: true };
  }
  ghiHangDoi([], kho);
  return { daGui, conLai: 0 };
}

/**
 * Đăng nhập xong thì SANG TÊN hàng đợi cho tài khoản thật.
 *
 * Bé học thử trước khi đăng nhập thì mọi bản ghi mang mã tạm 'local'. Đẩy nguyên
 * lên là luật từ chối (`isMine('local')` sai) — và từ chối trong im lặng, nên công
 * học của bé bay sạch mà không ai thấy. Phải viết lại CẢ `learnerId` LẪN `id`, vì
 * `id` nhúng `learnerId` bên trong.
 */
export function sangTenHangDoi(uid, kho = globalThis.localStorage) {
  if (!laHocSinhThat(uid)) return { doi: 0 };
  const q = docHangDoi(kho);
  let doi = 0;
  const ra = new Map();
  for (const r of q) {
    if (r.learnerId === uid) { ra.set(r.id, r); continue; }
    const seq = String(r.id).split('_').pop();
    const moi = { ...r, learnerId: uid, id: maSuKien(uid, r.sessionId, r.microId, r.itemId, seq) };
    ra.set(moi.id, moi);
    doi += 1;
  }
  ghiHangDoi([...ra.values()], kho);
  return { doi };
}
