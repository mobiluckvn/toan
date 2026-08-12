import React, { useCallback, useEffect, useRef, useState } from 'react';
import { duongAm } from '../lib/noiDung.js';

/**
 * NÚT NGHE — thứ mà bốn quyển Toán chưa từng cần.
 *
 * Bé lớp 1 CHƯA ĐỌC ĐƯỢC. Với quyển này, tiếng không phải trang trí thêm vào cho
 * vui: nó là cách bé nhận nội dung. Nên nút nghe phải to, bấm được bằng ngón tay
 * trẻ con, và bấm lại được bao nhiêu lần tuỳ thích — nghe lại là việc học, không
 * phải gian lận.
 *
 * ── BA CHỖ ĐÃ TÍNH TRƯỚC ──
 * 1. `preload="none"`: một bài có tới ~30 clip. Tải hết ngay là bé ngồi chờ màn
 *    trắng trên mạng nhà.
 * 2. Chỉ MỘT clip kêu tại một thời điểm. Không dừng clip cũ thì bé bấm nhanh hai
 *    nút là hai giọng chồng lên nhau, nghe không ra chữ nào.
 * 3. Thiếu tệp thì nút TỰ ẨN, không hiện nút hỏng. Bài vẫn học được bằng chữ và
 *    hình — mất một nửa, nhưng thà thế còn hơn bé bấm mãi không ra tiếng rồi
 *    tưởng máy hỏng.
 */

/* Clip đang kêu — để trong module chứ không trong state: hai nút khác nhau phải
   biết về nhau, mà chúng không có cha chung nào gần. */
let dangKeu = null;

/* `onPhat` báo ra ngoài mỗi lần clip chạy. Chặng TỪ MỚI dùng nó để biết bé đã
   nghe đủ các từ chưa — đó là đường đi tiếp thứ hai khi video không tải được. */
export default function NutNghe({ ma, nhan = 'Nghe', to = false, tuDong = false, onPhat }) {
  const [keu, datKeu] = useState(false);
  const tk = useRef(null);
  const duong = duongAm(ma);

  /* `onPhat` giữ trong REF chứ không đưa vào deps của `phat`. Chỗ gọi truyền hàm
     mũi tên viết thẳng, nên mỗi lần vẽ lại là một hàm MỚI — đưa vào deps thì
     `phat` đổi danh tính, `useEffect` bên dưới chạy lại, và phần dọn dẹp của nó
     `pause()` ngay clip đang kêu. Mà `onPhat` lại đổi state ở cha → vẽ lại →
     tắt tiếng. Bấm nghe ra đúng một tiếng "tách" rồi im. */
  const bao = useRef(onPhat);
  bao.current = onPhat;

  const phat = useCallback(() => {
    if (!duong) return;
    if (dangKeu && dangKeu !== tk.current) { dangKeu.pause(); dangKeu.currentTime = 0; }
    if (!tk.current) {
      tk.current = new Audio(duong);
      tk.current.preload = 'none';
      tk.current.addEventListener('ended', () => datKeu(false));
      tk.current.addEventListener('error', () => datKeu(false));
    }
    dangKeu = tk.current;
    tk.current.currentTime = 0;
    datKeu(true);
    bao.current?.();
    /* Trình duyệt có thể CHẶN phát tự động khi bé chưa chạm màn hình lần nào.
       Nuốt lỗi ấy: nút vẫn còn đó để bé tự bấm. */
    tk.current.play().catch(() => datKeu(false));
  }, [duong]);

  useEffect(() => {
    if (tuDong) phat();
    return () => { if (tk.current) { tk.current.pause(); if (dangKeu === tk.current) dangKeu = null; } };
  }, [tuDong, phat]);

  if (!duong) return null;

  const co = to ? 'h-16 w-16 text-3xl' : 'h-11 w-11 text-xl';
  return (
    <button
      type="button"
      onClick={phat}
      aria-label={nhan}
      className={`${co} inline-flex flex-none items-center justify-center rounded-full
        border-2 transition focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
        ${keu ? 'border-teal bg-teal text-white' : 'border-teal bg-teal-pale text-teal-dark hover:bg-teal hover:text-white'}`}
    >
      <span aria-hidden="true">{keu ? '🔊' : '🔈'}</span>
    </button>
  );
}

/**
 * Đọc liền một CHUỖI ĐOẠN, mỗi đoạn một thứ tiếng.
 *
 * Lời giảng hay lẫn Việt và Anh trong một ý ("Nghe câu này." → "This is a dog.").
 * Hai model khác nhau nên KHÔNG thể sinh thành một clip: mỗi đoạn một tệp, ở đây
 * nối lại lúc phát. Xem `tools/tts/README.md` mục 1.
 */
export function NutNgheDoan({ doan = [], nhan = 'Nghe cả đoạn' }) {
  const [i, datI] = useState(-1);
  const ds = doan.map(([chu, tieng]) => ({ chu, tieng, ma: maCua(chu, tieng) }))
    .filter((x) => duongAm(x.ma));
  const tk = useRef(null);

  useEffect(() => () => { if (tk.current) tk.current.pause(); }, []);

  if (!ds.length) return null;

  const chay = (k) => {
    if (k >= ds.length) { datI(-1); return; }
    datI(k);
    if (dangKeu) { dangKeu.pause(); }
    const a = new Audio(duongAm(ds[k].ma));
    tk.current = a; dangKeu = a;
    a.addEventListener('ended', () => chay(k + 1));
    a.addEventListener('error', () => chay(k + 1));
    a.play().catch(() => datI(-1));
  };

  return (
    <button
      type="button"
      onClick={() => chay(0)}
      className="inline-flex items-center gap-2 rounded-full border-2 border-teal
        bg-teal-pale px-4 py-2 text-teal-dark hover:bg-teal hover:text-white
        focus:outline-none focus-visible:ring-4 focus-visible:ring-gold"
    >
      <span aria-hidden="true">{i >= 0 ? '🔊' : '🔈'}</span>
      <span className="text-sm font-semibold">{nhan}</span>
    </button>
  );
}

/**
 * Cùng luật đặt mã với `am_id` của `tools/tts/sinh_am.py`.
 *
 * Bên Python là `c.isalnum()`, và trong Python thì "ó" LÀ alnum — nên "con chó"
 * ra `nghia_con_chó`, giữ nguyên dấu. Bản đầu của hàm này dùng `[^a-z0-9]` nên
 * "chó" thành "ch_", tra không ra clip, và TOÀN BỘ tiếng Việt câm — mà màn hình
 * vẫn vẽ đủ, chỉ là bấm nút không ra tiếng.
 *
 * Nên phải dùng lớp ký tự UNICODE. Cổng `tienganh_am.test.mjs` đối chiếu hai bên.
 */
export const maCua = (chu, tieng) => {
  /* MỖI ký tự lạ thành MỘT gạch — không gộp. Bên Python là
     `"".join(c if c.isalnum() else "_" for c in ...)`, nên ": " (hai ký tự) ra
     HAI gạch. Bản đầu ở đây dùng `+` để gộp chuỗi gạch liền nhau, thành ra
     "Cảnh hôm nay: Trong phòng ngủ." ra mã lệch đúng một ký tự — tra không thấy
     clip, và MỌI nút nghe của lời giảng biến mất. Màn hình vẫn đủ chữ, chỉ là câm. */
  const sach = [...String(chu).toLowerCase()]
    .map((c) => (/[\p{L}\p{N}]/u.test(c) ? c : '_'))
    .join('')
    .replace(/^_+|_+$/g, '');
  return `${tieng === 'vi' ? 'loi' : 'cau'}_${sach}`.slice(0, 60);
};
