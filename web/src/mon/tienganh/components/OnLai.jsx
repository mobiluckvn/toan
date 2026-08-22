import React, { useEffect, useMemo, useState } from 'react';
import CauHoi from './CauHoi.jsx';
import { napBai } from '../lib/noiDung.js';
import { chonCauOn, theQua, SO_CAU_MOI_THE } from '../lib/onlai.js';

/**
 * ÔN LẠI — buổi ôn ngắn cho những thẻ đã tới hạn.
 *
 * ── VÌ SAO MÀN NÀY RA ĐỜI MUỘN ──
 * Hàm nền sinh thẻ ôn theo lịch +1 / +3 / +7 ngày từ lâu, luật Firestore cũng đã
 * cho máy con đọc `reviewQueue`. Nhưng không màn nào ĐỌC thư mục ấy — kể cả môn
 * Toán. Nghĩa là suốt thời gian qua hệ thống vẫn ghi lịch ôn đều đặn, mà bé thì
 * không bao giờ được mời ôn. Có lịch, không có buổi.
 *
 * ── BA LUẬT CHO BUỔI ÔN ──
 * 1. NGẮN. Nhiều nhất 3 thẻ, mỗi thẻ 3 câu. Ôn tập mà dài bằng một bài học thì bé
 *    coi nó là bài học, và bài học thì để dành mai làm.
 * 2. KHÔNG CÂU MỚI. Câu lấy từ chính bài của thẻ. Ôn mà hỏi câu bé chưa từng gặp
 *    là bài mới đội lốt.
 * 3. ĐÚNG HẾT MỚI QUA. Nghiêm hơn bài học thường (ở đó sai vẫn đi tiếp) là cố ý —
 *    cả điểm của lặp lại ngắt quãng nằm ở chỗ thẻ chưa chắc thì quay lại SỚM.
 *
 * ── KHÔNG ĐỂ BÉ KẸT ──
 * Bài của thẻ không tải về được (mất mạng, hoặc bài đã bị bỏ khỏi quyển) thì BỎ
 * QUA thẻ ấy và đi tiếp, không bắt bé ngồi nhìn màn trắng. Thẻ hỏng sẽ tới hạn
 * lại vào lần sau; thà ôn hụt một thẻ còn hơn chặn cả buổi.
 */
export default function OnLai({ the: dsThe = [], onXongThe, onThoat, onLuot }) {
  const [iThe, datIThe] = useState(0);
  const [bai, datBai] = useState(null);
  const [loi, datLoi] = useState(false);
  const [iCau, datICau] = useState(0);
  const [ketQua, datKetQua] = useState([]);
  const [xongHet, datXongHet] = useState(false);

  const the = dsThe[iThe] || null;

  /* Nạp bài của thẻ đang tới. Đổi thẻ thì dọn sạch trạng thái câu, nếu không câu
     của thẻ trước còn dính sang thẻ sau. */
  useEffect(() => {
    let song = true;
    datBai(null); datLoi(false); datICau(0); datKetQua([]);
    if (!the?.microId) return () => { song = false; };
    napBai(the.microId)
      .then((d) => { if (song) datBai(d); })
      .catch(() => { if (song) datLoi(true); });
    return () => { song = false; };
  }, [the?.microId, the?.id]);

  const cauDs = useMemo(
    () => (bai ? chonCauOn(bai, the, { batDau: Number(the?.soLanOn) || 0 }) : []),
    [bai, the],
  );

  /* Thẻ hỏng hoặc bài không có câu nào → nhảy sang thẻ sau. Đặt trong effect chứ
     không tính lúc vẽ: gọi `datIThe` giữa lần vẽ là vòng lặp không đáy. */
  useEffect(() => {
    if (!the) return;
    if (loi || (bai && cauDs.length === 0)) sangTheSau(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loi, bai, cauDs.length]);

  function sangTheSau(qua) {
    if (the) onXongThe?.(the, qua);
    if (iThe + 1 < dsThe.length) datIThe(iThe + 1);
    else datXongHet(true);
  }

  if (xongHet || !the) {
    const soQua = 0;
    return (
      <Khung onThoat={onThoat}>
        <div className="rounded-xl2 bg-teal-pale p-6">
          <p className="text-4xl" aria-hidden="true">🌟</p>
          <p className="mt-2 text-2xl font-bold text-ink">Con ôn xong rồi!</p>
          <p className="text-teal-dark">
            Ôn lại như thế này giúp con nhớ lâu hơn nhiều so với học một lần rồi thôi.
          </p>
        </div>
        <button type="button" onClick={onThoat}
          className="mt-4 rounded-xl2 bg-navy px-6 py-3 text-lg font-bold text-white
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Về trang chính
        </button>
        <span className="sr-only">{soQua}</span>
      </Khung>
    );
  }

  if (loi || !bai) {
    return (
      <Khung onThoat={onThoat}>
        <p className="text-mute">{loi ? 'Bỏ qua một thẻ, đang sang thẻ sau…' : 'Đang mở bài ôn…'}</p>
      </Khung>
    );
  }

  const cau = cauDs[iCau];
  if (!cau) return <Khung onThoat={onThoat}><p className="text-mute">…</p></Khung>;

  const xongCau = (kq) => {
    const sau = [...ketQua, !!kq.dung && !kq.boQua];
    datKetQua(sau);
    if (iCau + 1 < cauDs.length) { datICau(iCau + 1); return; }
    sangTheSau(theQua(sau));
  };

  return (
    <Khung onThoat={onThoat}>
      <div className="flex items-center gap-2">
        <span className="text-sm font-bold text-mute">
          Thẻ {iThe + 1}/{dsThe.length} · câu {iCau + 1}/{cauDs.length}
        </span>
        <div className="flex flex-1 gap-1">
          {cauDs.map((c, i) => (
            <span key={c.id}
              className={`h-1.5 flex-1 rounded-full ${
                i < ketQua.length ? (ketQua[i] ? 'bg-teal' : 'bg-gold') : 'bg-line'}`} />
          ))}
        </div>
      </div>
      <p className="text-sm text-mute">Ôn lại: {bai.title}</p>
      <div className="rounded-xl2 border-2 border-line bg-white p-5">
        <CauHoi
          key={`${the.id}_${cau.id}`}
          cau={cau}
          onXong={xongCau}
          /* Lượt ôn CŨNG vào nhật ký, và cũng chạy qua BKT — đó là cả lý do có
             phép quên: gặp lại thì mức thạo phải được kéo lên. Gắn `laOnTap` để
             sau này tách được "ôn" khỏi "học lần đầu" nếu cần. */
          onLuot={(e) => onLuot?.({ ...e, laOnTap: true, microId: the.microId })}
        />
      </div>
    </Khung>
  );
}

function Khung({ children, onThoat }) {
  return (
    <div className="mx-auto flex min-h-screen w-full max-w-3xl flex-col gap-4 p-4 pb-24">
      <div className="flex items-center gap-3">
        <button type="button" onClick={onThoat}
          className="rounded-xl2 border-2 border-line px-3 py-2 text-sm font-semibold text-mute
            hover:border-navy hover:text-navy focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          ← Về
        </button>
        <h1 className="flex-1 text-xl font-bold text-ink sm:text-2xl">Ôn lại</h1>
      </div>
      {children}
    </div>
  );
}

export { SO_CAU_MOI_THE };
