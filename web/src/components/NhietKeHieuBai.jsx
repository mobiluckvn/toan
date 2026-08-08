import React, { useState } from 'react';

/**
 * NHIỆT KẾ HIỂU BÀI — bé tự chấm mình được mấy sao ở phần quiz cuối bài.
 *
 * Trong sách đây là một HÌNH (image13.png) lặp nguyên si ở cả 33 bài, và bé "tô
 * màu" ô sao mình đạt bằng bút chì. Dựng thành PNG là dựng 33 lần một tấm ảnh
 * chết mà bé không tô được — nên làm giao diện bấm chọn, đúng ý sách hơn.
 *
 * Sách tô 5 ô thành 5 sắc chuyển dần, nhưng bảng màu thương hiệu chỉ có ba nền
 * nhạt. Không chế thêm mã màu thô: gom 5 ô về ĐÚNG BA MỨC LỜI KHUYÊN của sách,
 * nhờ vậy màu và lời khuyên nói cùng một điều thay vì hai thang song song.
 *
 * KHÔNG ghi vào tiến trình: sách để bé tự chấm cho mình, không phải để chấm điểm.
 */
const MUC = [
  { den: 2, nen: 'bg-alert-pale', vien: 'border-alert/45', chu: 'Ôn lại cùng bố mẹ nhé',   mau: 'text-alert' },
  { den: 3, nen: 'bg-gold-pale',  vien: 'border-gold/60',  chu: 'Khá lắm, xem lại câu sai', mau: 'text-gold-dark' },
  { den: 5, nen: 'bg-teal-pale',  vien: 'border-teal/60',  chu: 'Tuyệt vời! Sang bài mới',  mau: 'text-teal-dark' },
];

const mucCua = (sao) => MUC.find((m) => sao <= m.den);

export default function NhietKeHieuBai() {
  const [chon, setChon] = useState(null);
  const m = chon == null ? null : mucCua(chon);

  return (
    <div className="card">
      <div className="kicker">🌡️ NHIỆT KẾ HIỂU BÀI</div>
      <p className="text-[15px] leading-snug text-ink">
        Con được mấy sao ở phần quiz? Bấm vào ô của con nhé.
      </p>

      <div className="mt-3 flex gap-1.5" role="group" aria-label="Con được mấy sao">
        {[1, 2, 3, 4, 5].map((sao) => {
          const o = mucCua(sao);
          const dang = chon === sao;
          return (
            <button
              key={sao}
              type="button"
              aria-pressed={dang}
              onClick={() => setChon(dang ? null : sao)}
              className={`flex-1 rounded-xl border-2 py-3 text-[17px] font-extrabold text-navy
                          ${o.nen} ${dang ? 'border-navy ring-2 ring-navy/30' : o.vien}`}
            >
              {sao} ★
            </button>
          );
        })}
      </div>

      {m && <p className={`mt-2.5 text-center text-[15px] font-bold ${m.mau}`}>{m.chu}</p>}
    </div>
  );
}
