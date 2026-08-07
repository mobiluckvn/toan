import React from 'react';
import { chapterOf } from '../lib/content.js';
import { resumeSpot } from '../lib/progress.js';

const CHAPTER_NAMES = {
  1: 'Bản đồ các hàng', 2: 'Lập số & đếm', 3: 'Chia hết & vòng đuôi', 4: 'Tính nhanh & tìm X',
  5: 'So sánh phân số', 6: 'Trung bình cộng', 7: 'Tổng – hiệu & tuổi', 8: 'Tổng – tỉ, hiệu – tỉ',
  9: 'Hai tỉ số', 10: 'Phần trăm & nồng độ', 11: 'Công việc chung & suy luận',
  12: 'Tam giác & hình thang', 13: 'Hình tròn & hình khối', 14: 'Chuyển động',
};

const STEPS = [
  ['1', 'Cô giảng nguyên tắc'],
  ['2', 'Xem bài mẫu'],
  ['3', 'Con tự luyện'],
  ['4', 'Thi lấy huy hiệu'],
];

/**
 * Thẻ VIỆC CỦA CON — thứ đầu tiên con nhìn thấy khi mở app.
 *
 * Trước đây nút to nhất trang ghi "Học tiếp: B1.M1" — mã nội bộ, con không biết
 * sắp học gì, mất bao lâu, và lần đầu vào vẫn bị bảo "học TIẾP" dù chưa học gì.
 * Thẻ này trả lời đúng ba câu: học gì · mất bao lâu · bấm vào đâu.
 */
export default function TodayCard({ microId, progress, info, reason, onOpen }) {
  if (!microId) return null;
  const spot = resumeSpot(progress, microId);
  const learnedAny = Object.values(progress.micros || {}).some((m) => m.pass);
  const ch = chapterOf(microId);
  const title = info?.title || microId.replace('DL:KSN5Q1.', 'Bài ');
  const mins = info?.durationMinutes;

  const heading = spot ? 'Con đang học dở bài này'
    : reason === 'đã quên bớt' ? 'Ôn lại cho nhớ'
    : learnedAny ? 'Việc của con bây giờ'
    : 'Bắt đầu từ đây nhé!';

  const cta = spot ? `Học tiếp — bước ${spot.step + 1}${spot.steps ? `/${spot.steps}` : ''} ▶`
                   : 'Bắt đầu học ▶';

  return (
    <section className="mx-3.5 mt-3.5 overflow-hidden rounded-2xl bg-white shadow-[0_3px_16px_rgba(12,59,112,.10)]">
      <div className="bg-gold px-4 py-2 text-[12px] font-extrabold tracking-wide text-gold-dark">
        {heading}
      </div>

      <div className="px-4 pt-3.5">
        <h2 className="text-[17px] font-bold leading-snug text-navy">{title}</h2>
        <p className="mt-1 text-[12.5px] text-mute">
          Chương {ch} · {CHAPTER_NAMES[ch]}
          {mins ? ` · khoảng ${mins} phút` : ''}
        </p>

        {/* Lần đầu con chưa biết một bài diễn ra thế nào — kể trước cho đỡ bỡ ngỡ */}
        {!learnedAny && !spot && (
          <ol className="mt-3 grid grid-cols-2 gap-1.5">
            {STEPS.map(([n, label]) => (
              <li key={n} className="flex items-center gap-2 rounded-xl bg-[#F2F6FA] px-2.5 py-2 text-[12.5px] font-semibold text-navy">
                <span className="flex h-[19px] w-[19px] flex-none items-center justify-center rounded-full bg-navy text-[11px] font-extrabold text-white">{n}</span>
                {label}
              </li>
            ))}
          </ol>
        )}

        {spot && (
          <p className="mt-2.5 rounded-xl bg-teal-pale px-3 py-2 text-[13px] font-semibold text-teal-dark">
            Con làm đến bước {spot.step + 1} rồi — mở lại là vào đúng chỗ cũ.
          </p>
        )}
      </div>

      <div className="flex gap-2.5 px-4 pb-4 pt-3">
        <button className="btn-gold flex-1" onClick={() => onOpen(microId)}>{cta}</button>
        {spot && (
          <button className="btn-ghost w-auto whitespace-nowrap px-3.5"
                  onClick={() => onOpen(microId, { fromStart: true })}>
            Từ đầu
          </button>
        )}
      </div>
    </section>
  );
}
