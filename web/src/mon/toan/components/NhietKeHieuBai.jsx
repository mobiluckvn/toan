import React from 'react';

/**
 * NHIỆT KẾ HIỂU BÀI — con đạt mấy sao ở phần sát hạch cuối bài.
 *
 * Trong sách đây là một HÌNH lặp nguyên si ở mọi bài (lớp 2: `image13.png` 33 lần;
 * lớp 4: `image1.png` 44 lần), và bé "tô màu" ô sao mình đạt bằng bút chì. Dựng
 * thành PNG là dựng mấy chục lần một tấm ảnh chết mà bé không tô được — nên làm
 * giao diện, đúng ý sách hơn.
 *
 * ── VÌ SAO NAY KHÔNG BẮT BÉ TỰ BẤM NỮA ──
 *
 * Bản đầu (đợt lớp 2) cho bé tự bấm số sao của mình, vì hồi ấy phần quiz chưa chấm
 * máy được. Nay cả 220 câu quiz của lớp 4 đều có đáp án nên MÁY BIẾT bé được mấy
 * sao — hỏi lại là vừa thừa một thao tác, vừa cho bé cơ hội tự chấm khác với kết
 * quả thật. Thành phần nhận thẳng `dat`/`tong` và tô đúng nấc.
 *
 * Nhận `tong` chứ không ghim 5 sao, nên quyển nào cũng dùng được.
 */

/* Ba mốc lời khuyên của sách. Bảng màu thương hiệu chỉ có ba nền nhạt — gom 5 ô về
   ĐÚNG BA MỨC ấy để màu và lời khuyên nói cùng một điều, thay vì hai thang song song. */
const MUC = [
  { den: 0.4, nen: 'bg-alert-pale', vien: 'border-alert', chu: 'text-alert',
    nhan: 'Ôn lại cùng bố mẹ nhé' },
  { den: 0.7, nen: 'bg-gold-pale', vien: 'border-gold', chu: 'text-gold-dark',
    nhan: 'Khá lắm, xem lại câu sai' },
  { den: 1.0, nen: 'bg-teal-pale', vien: 'border-teal', chu: 'text-teal-dark',
    nhan: 'Tuyệt vời! Sang bài mới' },
];

const mucCua = (dat, tong) => MUC.find((m) => dat <= Math.round(m.den * tong)) || MUC[2];

export default function NhietKeHieuBai({ dat = 0, tong = 5 }) {
  const muc = mucCua(dat, tong);
  return (
    <div className="mt-4">
      <h4 className="mb-2 text-[11.5px] font-extrabold tracking-widest text-mute">
        🌡️ NHIỆT KẾ HIỂU BÀI
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
