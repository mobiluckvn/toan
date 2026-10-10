import { boNguong } from '../../../chung/lib/nguong.js';
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
 * SỔ "ĐÃ LÊN MÁY CHỦ RỒI" — và vì sao thiếu nó thì MẤT SẠCH TỪ LƯỢT THỨ HAI.
 *
 * ── LỖI ĐÃ XẢY RA THẬT, TÌM RA 23-08-2026 BẰNG KHOÁ QUẢN TRỊ ──
 * Mỗi lượt bé trả lời, màn hình dựng LẠI nhật ký của cả phiên rồi gửi đi — chủ ý
 * là "gửi lại bao nhiêu lần cũng không sinh dòng trùng, vì mã lượt dựng lại ra
 * đúng mã cũ". Chủ ý ấy đúng với `progressTA`, nhưng SAI với `attempts`:
 *
 *     firestore.rules:  allow update, delete: if false;
 *
 * `attempts` là nhật ký BẤT BIẾN. Ghi đè một bản ghi đã có KHÔNG phải là ghi đè
 * vô hại — nó là `update`, và luật cấm. Mà `writeBatch` của Firestore là NGUYÊN
 * KHỐI: một lệnh trong lô bị từ chối thì cả lô rơi.
 *
 * Hệ quả dây chuyền:
 *   lượt 1 → lô [r0]           → 200, r0 lên máy chủ, hàng đợi rỗng
 *   lượt 2 → lô [r0, r1]       → 403 (vì r0 đã có) → cả lô rơi, hàng đợi giữ nguyên
 *   lượt 3 → lô [r0, r1, r2]   → 403 … và mãi mãi như thế
 *
 * Tức MỖI PHIÊN CHỈ CÓ ĐÚNG MỘT LƯỢT lên tới máy chủ, phần còn lại nằm chết
 * trong localStorage. Soi máy chủ thật: cả dự án có 2 bản ghi `attempts` cho hai
 * buổi học, mỗi buổi ~10 lượt. Engine BKT bị bỏ đói mà mọi cổng vẫn xanh, vì
 * không cổng nào gửi ĐẾN LƯỢT THỨ HAI.
 *
 * ⚠ ĐỪNG "SỬA" BẰNG CÁCH NỚI LUẬT cho `attempts` ghi đè được. Tính bất biến của
 *    nhật ký là thứ mục 2.5.2 của luận văn dựa vào, và là thứ bảo vệ điểm của bé
 *    khỏi bị sửa. Chỗ sai nằm ở máy con gửi thừa, không ở luật.
 */
const DA_GUI_GOC = 'ttd5.daGuiTA.v1';
const dgkey = () => {
  const cho = choDangDung();
  return cho === CHO_DAU ? DA_GUI_GOC : `${DA_GUI_GOC}.${cho}`;
};

/** Giữ tối đa bằng này mã. Vượt thì bỏ mã CŨ NHẤT — chúng thuộc phiên đã đóng. */
export const DA_GUI_TOI_DA = 3000;

export function docDaGui(kho = globalThis.localStorage) {
  try { return new Set(JSON.parse(kho?.getItem(dgkey()) || '[]')); } catch { return new Set(); }
}

export function themDaGui(ids, kho = globalThis.localStorage) {
  if (!ids?.length) return docDaGui(kho);
  /* Mảng chứ không Set khi lưu: cần giữ THỨ TỰ để còn biết mã nào cũ nhất. */
  let ds;
  try { ds = JSON.parse(kho?.getItem(dgkey()) || '[]'); } catch { ds = []; }
  const co = new Set(ds);
  for (const id of ids) if (!co.has(id)) { ds.push(id); co.add(id); }
  if (ds.length > DA_GUI_TOI_DA) ds = ds.slice(ds.length - DA_GUI_TOI_DA);
  try { kho?.setItem(dgkey(), JSON.stringify(ds)); } catch { /* chế độ riêng tư */ }
  return new Set(ds);
}

/**
 * PHIÊN BẢN BẢN GHI. Nhật ký bất biến nên dòng ghi bằng luật cũ nằm lẫn mãi mãi.
 *   v = 2  cùng luật với Toán: `ms` đo riêng từng câu, `ts` riêng từng lượt.
 * Bắt đầu thẳng từ 2 chứ không từ 1: Tiếng Anh chưa từng ghi dòng nào, nên không
 * có dòng đời cũ để phải phân biệt — và dùng chung số với Toán thì bên đọc chỉ
 * cần một luật.
 */
/* 3 từ 10-10-2026: bản ghi mang thêm `nguongVer` — phiên bản bộ ngưỡng đã dùng
   (R7, mục 3.8.2). Hai môn phải khai CÙNG một số; cổng `tienganh_sukien` canh. */
export const PHIEN_BAN_BAN_GHI = 3;

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
    /* ── PHIÊN BẢN BỘ NGƯỠNG (R7, mục 3.8.2) ──
       Cùng một lẽ với `phienBanMau` ngay trên: không lưu nội dung, chỉ lưu ĐỦ để
       tính lại. Một ngưỡng đổi mà bản ghi cũ không mang số phiên bản thì không còn
       biết kết quả ấy được tính bằng θ nào — và hai bộ ngưỡng không so được với
       nhau trên cùng một nhật ký. */
    nguongVer: boNguong()?.phienBan ?? null,
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

/**
 * Xếp vào hàng đợi — trùng mã thì ghi đè, không nhân bản.
 *
 * ⚠ VÀ BỎ HẲN mã nào ĐÃ lên máy chủ. `attempts` cấm ghi đè, `writeBatch` là
 * nguyên khối, nên một mã cũ lọt vào lô là cả lô rơi — xem khối chú thích dài ở
 * `DA_GUI_GOC` phía trên. Lọc ở ĐÂY chứ không ở chỗ gửi: chỗ gửi lọc thì mã cũ
 * vẫn nằm lại hàng đợi và phình mãi.
 */
export function xepHang(ds, kho = globalThis.localStorage) {
  const daGui = docDaGui(kho);
  const q = docHangDoi(kho);
  const m = new Map(q.filter((r) => !daGui.has(r.id)).map((r) => [r.id, r]));
  for (const r of ds) if (!daGui.has(r.id)) m.set(r.id, r);
  return ghiHangDoi([...m.values()], kho);
}

/** Mã lỗi Firestore trả khi luật từ chối — phân biệt với mất mạng (`unavailable`). */
const LOI_TU_CHOI = 'permission-denied';

/**
 * Đẩy hàng đợi lên máy chủ. Mất mạng thì GIỮ NGUYÊN phần chưa gửi.
 *
 * ⚠ Không bao giờ ném lỗi ra ngoài: bé đang học, mất mạng không phải việc của bé.
 *
 * ── VÀ PHẢI TỰ GỠ ĐỘC CHO HÀNG ĐỢI CŨ ──
 * Sổ "đã gửi" chặn được việc xếp lại bản ghi đã lên, nhưng CHỈ TỪ NAY. Máy nào
 * đang mang sẵn một hàng đợi nhiễm độc — có bản ghi đã nằm trên máy chủ — thì lô
 * nào cũng chết, mãi mãi, và cả hàng đợi ấy thành mồ chôn. Đo trên máy thật
 * 23-08-2026: hai bé, 12 và 14 bản ghi kẹt cứng như thế.
 *
 * Nên lô hỏng thì THỬ LẠI TỪNG BẢN GHI MỘT:
 *   · gửi lẻ được   → tốt, ghi vào sổ đã gửi;
 *   · lẻ cũng bị TỪ CHỐI (`permission-denied`) → với một kho BẤT BIẾN, nghĩa gần
 *     như chắc chắn là "bản ghi này đã có trên máy chủ rồi". Bỏ nó ra khỏi hàng
 *     đợi để những bản ghi sau còn đường đi;
 *   · lẻ hỏng vì lý do KHÁC (mất mạng) → GIỮ LẠI, lần sau gửi tiếp.
 *
 * ⚠ Phân biệt bằng MÃ LỖI chứ không bằng "cứ hỏng là bỏ". Mất mạng mà bỏ hết thì
 *    mất trắng công học của bé — đúng thứ cả cơ chế hàng đợi này sinh ra để tránh.
 *
 * ⚠ Và ĐẾM số bản ghi bị bỏ, trả về trong `boQua`. Bỏ trong im lặng thì lần sau có
 *    một lỗi khác cũng cho ra `permission-denied` là dữ liệu bay mà không ai biết.
 */
export async function dayHangDoi(guiDi, kho = globalThis.localStorage, moLo = 200) {
  const q = docHangDoi(kho);
  if (!q.length) return { daGui: 0, conLai: 0 };
  let daGui = 0; let boQua = 0;
  /* Mã đã XONG VIỆC — gửi được hoặc xác định là đã có trên máy chủ. Phần còn lại
     của hàng đợi = mọi thứ không nằm trong tập này; tính theo tập thì không phụ
     thuộc vào việc dừng ở đâu, khỏi sai lệch chỉ số. */
  const xong = new Set();
  let matMang = false;

  for (let i = 0; i < q.length && !matMang; i += moLo) {
    const mo = q.slice(i, i + moLo);
    try {
      await guiDi(mo);
      mo.forEach((r) => xong.add(r.id));
      /* Ghi vào sổ "đã gửi" NGAY sau mỗi lô, không đợi hết vòng: lô sau hỏng thì
         lô trước vẫn phải được nhớ là đã lên, kẻo lần đẩy kế tiếp lại kèm nó vào
         và làm rơi cả lô mới. */
      themDaGui(mo.map((r) => r.id), kho);
      daGui += mo.length;
    } catch {
      for (const r of mo) {
        try {
          await guiDi([r]);
          themDaGui([r.id], kho);
          xong.add(r.id);
          daGui += 1;
        } catch (e) {
          if (e?.code === LOI_TU_CHOI) {
            /* Đã có trên máy chủ (kho bất biến) — coi như xong, đừng chặn đường
               những bản ghi phía sau. */
            themDaGui([r.id], kho);
            xong.add(r.id);
            boQua += 1;
          } else {
            matMang = true;
            break;
          }
        }
      }
    }
  }

  const con = matMang ? q.filter((r) => !xong.has(r.id)) : [];
  ghiHangDoi(con, kho);
  return { daGui, boQua, conLai: con.length, ...(matMang ? { loi: true } : {}) };
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
  let boLai = 0;
  for (const r of q) {
    if (r.learnerId === uid) { ra.set(r.id, r); continue; }
    /* ⚠ CHỈ NHẬN BẢN GHI CHƯA CÓ CHỦ. Bản cũ sang tên MỌI bản ghi lạ, kể cả của
       một bé CÓ THẬT khác — ghép với lỗi hàng đợi nghẽn thì bài của bé A chui vào
       học bạ của bé B khi B đăng nhập vào cùng một chỗ. Đo được trên máy chủ
       23-08-2026: 7 phiên, 130/398 bản ghi mang tên sai chủ. Xem chú thích dài ở
       `mon/toan/lib/sync.js` — cùng một lỗi, cùng một ngày. */
    if (laHocSinhThat(r.learnerId)) { boLai += 1; continue; }
    const seq = String(r.id).split('_').pop();
    const moi = { ...r, learnerId: uid, id: maSuKien(uid, r.sessionId, r.microId, r.itemId, seq) };
    ra.set(moi.id, moi);
    doi += 1;
  }
  ghiHangDoi([...ra.values()], kho);
  return { doi, boLai };
}
