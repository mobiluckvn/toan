import React from 'react';
import { gradeMicro } from '../lib/flow.js';

/** Trang kết: huy hiệu · điểm · thẻ ôn · sổ phụ huynh */
export default function FinaleCard({ lesson, log, onRetry, onJumpTeach, onFinish }) {
  const rule = lesson.assessment?.passRule || '';
  const g = gradeMicro(log.assess, rule);
  const firstTry = log.practice.filter((p) => p.tries === 1).length;
  const pn = lesson.parentNote || {};
  const flash = lesson.spacedReview?.flashcards?.[0];
  const award = lesson.assessment?.onPass?.award || '';

  const fill = (s) => String(s || '')
    .replace('{score}', g.right)
    .replace('{trapResult}', g.mustOK ? 'đúng' : 'chưa đúng');

  return (
    <>
      <div className="card text-center">
        <div className="text-[58px] leading-none">{g.pass ? '🏅' : '💪'}</div>
        <h2 className="mt-1 text-[22px] font-bold text-navy">
          {g.pass ? 'Đạt rồi!' : 'Gần được rồi con ơi!'}
        </h2>
        <p className="mt-1 text-[15px] text-mute">
          {g.pass
            ? (award ? `Con nhận ${award.replace(/_/g, ' ')}.` : 'Con mở khoá micro tiếp theo.')
            : 'Mình xem lại phần nguyên tắc rồi thử lại nhé.'}
        </p>

        <div className="mt-4 flex flex-wrap justify-center gap-2.5">
          {[['SÁT HẠCH', `${g.right}/${g.total}`], ['ĐÚNG NGAY', `${firstTry}/${log.practice.length}`],
            ['CÂU BẪY', g.mustOK ? '✓' : '✗']].map(([k, v]) => (
            <div key={k} className="min-w-[86px] rounded-xl bg-soft px-3.5 py-2.5">
              <b className="block text-[23px] text-navy">{v}</b>
              <span className="text-[10.5px] font-extrabold text-mute">{k}</span>
            </div>
          ))}
        </div>

        {flash && (
          <div className="mt-4 rounded-2xl bg-navy px-4 py-3.5 text-left text-[14.5px] leading-relaxed text-white">
            <b className="text-gold">Thẻ ôn (hiện lại sau 1 ngày):</b>
            <div className="mt-1">{flash.back}</div>
          </div>
        )}

        <div className="mt-3 rounded-2xl border-[1.5px] border-dashed border-line bg-[#F7FAFD] p-3.5 text-left text-[14.5px]">
          <h4 className="mb-1.5 text-[11.5px] font-extrabold tracking-widest text-mute">GỬI BỐ MẸ</h4>
          <p>{fill(pn.onComplete)}</p>
          {pn.homeActivity && <p className="mt-1.5"><b>Chơi cùng con:</b> {pn.homeActivity}</p>}
          {pn.watchFor && <p className="mt-1.5"><b>Để ý:</b> {pn.watchFor}</p>}
        </div>
      </div>

      <footer className="fixed inset-x-0 bottom-0 border-t border-line bg-white/95 px-3.5 py-2.5 backdrop-blur"
              style={{ paddingBottom: 'calc(.625rem + env(safe-area-inset-bottom))' }}>
        <div className="mx-auto flex max-w-[740px] gap-2.5">
          {g.pass ? (
            <>
              <button className="btn-ghost" onClick={onRetry}>Học lại</button>
              <button className="btn-gold" onClick={onFinish}>Micro tiếp theo ▶</button>
            </>
          ) : (
            <>
              <button className="btn-ghost" onClick={onRetry}>Học lại từ đầu</button>
              <button className="btn-go" onClick={onJumpTeach}>Ôn lại nguyên tắc</button>
            </>
          )}
        </div>
      </footer>
    </>
  );
}
