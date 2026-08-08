import React from 'react';

/**
 * MỘT DÒNG TRONG DANH SÁCH — dùng chung cho cả lớp 2 và lớp 5.
 *
 * Bốn chỗ đang dựng đúng một hình dạng này: bài học lớp 5, bài học lớp 2, kỳ sát
 * hạch cuối chương, và ba ải. Bốn bản sao thì sửa khoảng cách một chỗ là ba chỗ
 * kia lệch đi mà không ai nhận ra.
 *
 * CỐ Ý không gộp cả hai trang chính thành một component: lớp 2 và lớp 5 khác nhau
 * mười điểm CHÍNH SÁCH (khoá bài · chế độ học · thẻ hôm nay · bảng sao · chương
 * gập mở · luật mở kỳ thi · ba ải · Mùa giải · màu đầu trang). Một component với
 * mười cờ điều kiện khó đọc hơn hẳn hai tệp mỗi tệp làm một việc rõ ràng. Chỗ
 * đáng gom là hình dạng lặp lại — chính là dòng này.
 */
const KIEU = {
  thuong: 'border border-line bg-white hover:bg-soft',
  nhan:   'border-2 border-gold bg-gold-pale',      // kỳ sát hạch: phải nổi hơn bài học
  mo:     'border border-line bg-white opacity-55', // chưa mở
};

export default function DongDanhSach({
  bieuTuong, tieuDe, phuDe, kieu = 'thuong', khoa = false, onClick, mauChu = 'text-navy',
}) {
  return (
    <button
      type="button"
      disabled={khoa}
      onClick={onClick}
      className={`mt-1.5 flex w-full items-center gap-2.5 rounded-xl px-3 py-2.5 text-left
                  ${KIEU[khoa ? 'mo' : kieu]} disabled:cursor-default`}
    >
      <span className="text-[18px] leading-none">{bieuTuong}</span>
      <span className="min-w-0 flex-1">
        <span className={`block text-[15px] font-bold leading-snug ${mauChu}`}>{tieuDe}</span>
        {phuDe && <span className="block text-[12px] text-mute">{phuDe}</span>}
      </span>
      <span className="text-[14px] text-mute">{khoa ? '🔒' : '▶'}</span>
    </button>
  );
}
