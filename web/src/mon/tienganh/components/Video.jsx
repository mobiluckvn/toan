import React, { useRef, useState } from 'react';
import { CONTENT, dongDau } from '../../../chung/lib/soQuyen.js';

/**
 * XEM VIDEO BÀI HỌC — kênh chính để bé nhận nội dung.
 *
 * Bé lớp 1 chưa đọc sõi tiếng Việt, nên mọi lời giảng bằng chữ trên màn hình thực
 * chất là chữ cho người lớn. Video thì bé nhận được: nghe tiếng, nhìn hình.
 *
 * ── BỐN CHỖ TÍNH CHO BÉ 6 TUỔI ──
 *
 * 1. KHÔNG tự chạy. Bé phải bấm — vì tự chạy thì tiếng nổ ra lúc bé chưa sẵn sàng,
 *    và trình duyệt cũng chặn tự chạy có tiếng.
 *
 * 2. Nút XEM LẠI to bằng nút xem. Xem lại là việc học, không phải làm phiền.
 *
 * 3. KHÔNG cho tua. `controlsList="nodownload noplaybackrate"` và không có thanh
 *    tua rời: bé 6 tuổi kéo trúng thanh tua là nhảy mất đoạn, rồi tưởng máy hỏng.
 *    Vẫn giữ `controls` để dừng tạm được.
 *
 * 4. XEM XONG MỚI MỞ nút đi tiếp. Không khoá cứng — bé xem lần hai vẫn qua được
 *    ngay — nhưng lần đầu thì phải xem hết, nếu không video chỉ là thứ trang trí.
 */
export default function Video({ tep, ten, phu, onXongLan1, children }) {
  const [daXong, datDaXong] = useState(false);
  const [dangChay, datDangChay] = useState(false);
  const v = useRef(null);

  if (!tep) return null;
  const duong = dongDau(`${CONTENT}/tienganh/video/${tep}`);

  return (
    <section className="flex flex-col gap-3">
      <div className="overflow-hidden rounded-xl2 border-2 border-navy bg-black">
        <video
          ref={v}
          src={duong}
          className="block aspect-video w-full"
          controls
          controlsList="nodownload noplaybackrate noremoteplayback"
          disablePictureInPicture
          playsInline
          preload="metadata"
          onPlay={() => datDangChay(true)}
          onPause={() => datDangChay(false)}
          onEnded={() => { datDangChay(false); if (!daXong) { datDaXong(true); onXongLan1?.(); } }}
        />
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={() => { const e = v.current; if (!e) return; e.currentTime = 0; e.play(); }}
          className="inline-flex items-center gap-2 rounded-xl2 bg-navy px-6 py-3 text-lg
            font-semibold text-white focus:outline-none focus-visible:ring-4 focus-visible:ring-gold"
        >
          <span aria-hidden="true">{daXong ? '🔁' : '▶️'}</span>
          {daXong ? 'Xem lại' : dangChay ? 'Xem lại từ đầu' : ten || 'Xem bài'}
        </button>
        {phu && <span className="text-sm text-mute">{phu}</span>}
      </div>

      {children}
    </section>
  );
}
