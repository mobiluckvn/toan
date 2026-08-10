import React from 'react';

/**
 * NHIỆT KẾ HIỂU BÀI — con tự soi mình đạt mấy sao ở phần sát hạch.
 *
 * Sách lớp 4 in hình này ở CUỐI MỖI BÀI, và in tới 44 lần bằng đúng một tệp ảnh.
 * Làm thành phần giao diện thay vì ảnh tĩnh vì ba lẽ:
 *
 *   · một ảnh dùng 44 chỗ thì sửa một chữ là phải vẽ lại rồi cập nhật 44 mã băm;
 *   · ảnh raster không tô được ô con VỪA ĐẠT — mà cả ý nghĩa của nhiệt kế nằm ở chỗ
 *     con nhìn ra mình đang đứng ở nấc nào;
 *   · chữ trên ảnh không đọc được bằng trình đọc màn hình.
 *
 * Lớp 3 còn nợ đúng việc này với `image3.png` (dùng 34 lần) — thành phần ở đây nhận
 * `tong` nên dùng lại được cho mọi quyển, không ghim cứng 5 sao.
 */

/* Năm nấc, lời nhắn lấy nguyên văn từ sách. Ba mốc màu theo bảng màu thương hiệu —
   đỏ nhạt · vàng nhạt · xanh nhạt — không bắt chước màu sách. */
const LOI = [
  { den: 0.4, nen: 'bg-alert-pale', vien: 'border-alert', chu: 'text-alert',
    nhan: 'Ôn lại cùng bố mẹ nhé' },
  { den: 0.7, nen: 'bg-gold-pale', vien: 'border-gold', chu: 'text-gold-dark',
    nhan: 'Khá lắm, xem lại câu sai' },
  { den: 1.0, nen: 'bg-teal-pale', vien: 'border-teal', chu: 'text-teal-dark',
    nhan: 'Tuyệt vời! Sang bài mới' },
];

const mucCua = (dat, tong) => LOI.find((m) => dat <= Math.round(m.den * tong)) || LOI[2];

export default function NhietKe({ dat = 0, tong = 5 }) {
  const muc = mucCua(dat, tong);
  return (
    <div className="mt-4">
      <h4 className="mb-2 text-[11.5px] font-extrabold tracking-widest text-mute">
        NHIỆT KẾ HIỂU BÀI
      </h4>
      <div className="flex justify-center gap-1.5" role="img"
           aria-label={`Con đạt ${dat} trên ${tong} sao. ${muc.nhan}.`}>
        {Array.from({ length: tong }, (_, i) => i + 1).map((n) => {
          const m = mucCua(n, tong);
          const sang = n <= dat;
          return (
            <div key={n}
                 className={`flex-1 rounded-xl border-[1.5px] py-2 text-center transition
                   ${sang ? `${m.nen} ${m.vien}` : 'border-line bg-white'}`}>
              <b className={`text-[15px] ${sang ? m.chu : 'text-line'}`}>{n} ★</b>
            </div>
          );
        })}
      </div>
      <p className={`mt-1.5 text-center text-[13.5px] font-bold ${muc.chu}`}>{muc.nhan}</p>
    </div>
  );
}
