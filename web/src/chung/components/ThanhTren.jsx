import React from 'react';

/**
 * THANH TRÊN — đầu trang dùng chung cho MỌI màn không phải phòng học.
 *
 * VÌ SAO GOM: trước đây mỗi màn tự vẽ đầu trang lấy, và mỗi cái cho một đường ra
 * khác nhau. Trang lớp 5 có nút "← kệ sách"; trang lớp 2·3·4 cũng có nhưng màu khác,
 * chữ khác, đặt chỗ khác; màn chủ đề tầng 2 và tầng 3 chỉ có "← Quay lại" đi LÊN MỘT
 * TẦNG, nên bé lỡ đi sâu ba tầng thì phải bấm ba lần mới ra được; vòng luyện chỉ có
 * "← Thoát"; sổ bố mẹ chỉ có một mũi tên trần.
 *
 * Kết quả: đứng ở màn nào bé cũng phải học lại một lần "đường về nằm ở đâu". Nay MỌI
 * màn có đúng hai lối, luôn ở đúng một chỗ:
 *   · trái  — lùi MỘT bước (về nơi vừa đi ra);
 *   · phải  — ⌂ về KỆ SÁCH, trang chính của cả app, dù đang ở sâu bao nhiêu tầng.
 *
 * Không có `onVeNha` thì nút nhà không hiện — dùng cho chính kệ sách, nơi đã là nhà.
 */
export default function ThanhTren({
  nhan, tieuDe, phuDe, onQuayLai, nhanQuayLai = '← Quay lại', onVeNha,
  nhanVeNha = '⌂ Kệ sách', giua = false, children, phai,
}) {
  return (
    <header className="bg-navy px-4 py-3.5 text-white">
      <div className="flex items-start gap-2">
        <div className="flex min-w-0 flex-1 flex-wrap items-center gap-1.5">
          {onQuayLai && (
            <button onClick={onQuayLai}
                    className="rounded-full bg-white/15 px-2.5 py-1 text-[11.5px] font-bold text-white">
              {nhanQuayLai}
            </button>
          )}
          {onVeNha && (
            <button onClick={onVeNha}
                    className="rounded-full bg-white/15 px-2.5 py-1 text-[11.5px] font-bold text-white">
              {nhanVeNha}
            </button>
          )}
        </div>
        {phai && <div className="flex shrink-0 flex-col items-end gap-1">{phai}</div>}
      </div>

      <div className={`mt-2 ${giua ? 'text-center' : ''}`}>
        {nhan && (
          <div className="text-[11px] font-extrabold tracking-widest text-gold">{nhan}</div>
        )}
        {tieuDe && <h1 className="mt-0.5 text-[20px] font-bold leading-snug">{tieuDe}</h1>}
        {phuDe && <p className="mt-0.5 text-[12.5px] leading-relaxed opacity-90">{phuDe}</p>}
      </div>

      {children}
    </header>
  );
}
