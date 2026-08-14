import React, { useRef, useState } from 'react';
import { CONTENT, dongDau } from '../lib/soQuyen.js';

/**
 * XEM VIDEO BÀI HỌC — kênh chính để bé nhận nội dung. DÙNG CHUNG hai môn.
 *
 * Chuyển từ `mon/tienganh/` sang vùng chung 14-08 khi bác chốt mở bài và bài
 * giảng lớp 4 cũng phải thành video. Chép bản thứ hai cho Toán thì hai bản sớm
 * muộn lệch — mà chỗ lệch ở đây là mấy luật đã tính riêng cho bé (không tự chạy,
 * không cho tua, xem xong mới mở nút đi tiếp).
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
 * 4. XEM XONG MỚI MỞ nút đi tiếp. Chặng gọi tới quyết định điều đó; ở đây chỉ
 *    báo ra `onXongLan1`. Không khoá cứng — bé xem lần hai vẫn qua được ngay.
 *
 * 5. TỆP HỎNG THÌ PHẢI KÊU LÊN. `onLoi` bắn ra ngoài để chặng mở khoá nút đi
 *    tiếp: mạng rớt hay tệp thiếu là lỗi của máy, mà bé thì ngồi chịu trận trước
 *    một ô đen và một nút xám không giải thích gì.
 */
export default function Video({ tep, thuMuc = 'tienganh', ten, phu, onXongLan1, onLoi, children }) {
  const [daXong, datDaXong] = useState(false);
  const [dangChay, datDangChay] = useState(false);
  const [hong, datHong] = useState(false);
  const v = useRef(null);

  if (!tep) return null;
  /* `thuMuc` chứ không ghim 'tienganh': component này nay ở vùng CHUNG và hai
     môn cùng dùng. Ghim cứng thì môn Toán trỏ vào thư mục của Tiếng Anh, video
     404, và bé chỉ thấy một ô đen — `onLoi` có kêu, nhưng chẳng ai hiểu vì sao. */
  const duong = dongDau(`${CONTENT}/${thuMuc}/video/${tep}`);

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
          onError={() => { if (!hong) { datHong(true); onLoi?.(); } }}
        />
      </div>

      {hong && (
        <p className="rounded-xl2 bg-gold-pale p-3 text-gold-dark">
          Video chưa tải được — chắc mạng đang yếu. Con cứ bấm 🔈 nghe từng từ,
          rồi học tiếp bình thường nhé.
        </p>
      )}

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
