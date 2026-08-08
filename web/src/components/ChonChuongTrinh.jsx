import React from 'react';
import ChanTrang from './ChanTrang.jsx';

/**
 * CHỌN CHƯƠNG TRÌNH — màn đầu tiên khi mở app.
 *
 * Trước đây app chỉ có lớp 5 nên vào thẳng phòng học. Nay có hai chương trình, mà
 * người bấm là TRẺ CON: không thể để bé lớp 2 lạc vào bài lớp 5 rồi nản.
 *
 * Nên màn này to, rõ, mỗi lựa chọn một màu và một dòng nói thẳng "dành cho ai".
 * Chọn xong app NHỚ, lần sau vào thẳng — nhưng luôn có nút đổi ở trang chính.
 */
const CT = [
  {
    ma: 'lop2', bieu: '🏰', ten: 'Lớp 2',
    phu: 'Cùng Trí Long khám phá Vương quốc Số',
    mo: '33 bài · 8 chương · bé đọc và làm cùng',
    ai: 'Dành cho bé lớp 1 – lớp 2',
    nen: 'from-teal to-[#7fe3d0]', chu: 'text-teal-dark',
  },
  {
    ma: 'lop5', bieu: '🎓', ten: 'Lớp 5',
    phu: 'Toán Tư Duy — Quyển 1 & Mùa giải Vô địch',
    mo: '168 bài · 14 chương · có cả phần luyện thi',
    ai: 'Dành cho bạn lớp 4 – lớp 5',
    nen: 'from-gold to-[#fcd88a]', chu: 'text-gold-dark',
  },
];

export default function ChonChuongTrinh({ onChon }) {
  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
      <header className="bg-navy px-4 py-5 text-white">
        <div className="text-[11px] font-extrabold tracking-widest text-gold">MOBILUCK · KỸ SƯ NHÍ</div>
        <h1 className="mt-1 text-[22px] font-bold leading-snug">Con học lớp mấy?</h1>
        <p className="mt-1 text-[14px] leading-relaxed opacity-90">
          Chọn đúng chương trình để bài học vừa sức con nhé. Chọn nhầm cũng không sao —
          đổi lại được bất cứ lúc nào.
        </p>
      </header>

      <div className="px-3.5 pt-4">
        {CT.map((c) => (
          <button key={c.ma} onClick={() => onChon(c.ma)}
                  className={`mb-3 flex w-full items-center gap-3.5 rounded-2xl bg-gradient-to-br ${c.nen} px-4 py-5 text-left`}>
            <span className="text-[44px] leading-none">{c.bieu}</span>
            <span className="flex-1">
              <span className={`block text-[24px] font-extrabold leading-none ${c.chu}`}>{c.ten}</span>
              <span className={`mt-1 block text-[14.5px] font-bold ${c.chu}`}>{c.phu}</span>
              <span className={`mt-1 block text-[13px] opacity-80 ${c.chu}`}>{c.mo}</span>
              <span className={`mt-1.5 block text-[12.5px] font-bold ${c.chu}`}>{c.ai}</span>
            </span>
            <span className={`text-[22px] ${c.chu}`}>▶</span>
          </button>
        ))}
      </div>

      <ChanTrang />
    </div>
  );
}
