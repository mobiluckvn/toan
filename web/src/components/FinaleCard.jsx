import React from 'react';
import { gradeMicro } from '../lib/flow.js';
import NhietKe from './NhietKe.jsx';

/** Trang kết: huy hiệu · điểm · thẻ ôn · sổ phụ huynh · đường lùi về quyển dưới */
export default function FinaleCard({ lesson, log, onRetry, onJumpTeach, onFinish, onMoBai }) {
  const rule = lesson.assessment?.passRule || '';
  const g = gradeMicro(log.assess, rule);
  const firstTry = log.practice.filter((p) => p.tries === 1).length;
  const pn = lesson.parentNote || {};
  const flash = lesson.spacedReview?.flashcards?.[0];
  const award = lesson.assessment?.onPass?.award || '';
  /* Đường LÙI về quyển dưới: bài lớp 3 trỏ về bài lớp 2 cùng chủ đề. Chỉ có ở quyển
     nối tiếp, và bộ dựng CHỈ ghi trường này khi thật sự có đích — nên ở đây không
     phải biết luật nào, cứ có thì hiện. */
  const lui = onMoBai ? lesson.duongLui : null;

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

        {/* Nhiệt kế tự đánh giá — sách lớp 4 in ở cuối mỗi bài. Là THÀNH PHẦN chứ
            không phải ảnh: nó tô đúng nấc con vừa đạt, việc mà ảnh tĩnh không làm
            được. Quyển nào cũng dùng được vì nó nhận số câu sát hạch thật. */}
        {g.total > 0 && <NhietKe dat={g.right} tong={g.total} />}

        {flash && (
          <div className="mt-4 rounded-2xl bg-navy px-4 py-3.5 text-left text-[14.5px] leading-relaxed text-white">
            <b className="text-gold">Thẻ ôn (hiện lại sau 1 ngày):</b>
            <div className="mt-1">{flash.back}</div>
          </div>
        )}

        {/* HẠT MẦM NĂM NGOÁI — sách viết sẵn ở đầu mỗi bài lớp 3, nối bài hôm nay
            với thứ con đã học năm ngoái. Đặt ở màn kết để con vừa làm xong thì thấy
            ngay mình đã đi được bao xa từ quyển trước. */}
        {lesson.hatMam && (
          <div className="mt-4 rounded-2xl bg-teal-pale px-4 py-3.5 text-left text-[14.5px] leading-relaxed">
            <b className="text-teal-dark">🌱 Hạt mầm năm ngoái</b>
            <p className="mt-1 text-navy">{lesson.hatMam}</p>
          </div>
        )}

        {/* Chưa đạt thì đây là lối ra đỡ hụt hẫng nhất: về luyện lại đúng bài gốc của
            năm ngoái, chứ không phải làm lại bài khó thêm một lượt nữa. */}
        {lui && (
          <div className={`mt-3 rounded-2xl px-4 py-3.5 text-left text-[14.5px] ${
            g.pass ? 'bg-soft' : 'border-[1.5px] border-gold bg-gold-pale'}`}>
            <b className="text-navy">{lui.nhan}</b>
            <p className="mt-1 text-mute">
              {g.pass ? 'Muốn ôn lại gốc của bài này thì mở:' : 'Bài này dựng trên một bài năm ngoái — luyện lại gốc rồi quay lên nhé:'}
            </p>
            <div className="mt-2 flex flex-col gap-1.5">
              {lui.ve.map((id, k) => (
                <button key={id} className="btn-ghost text-left"
                        onClick={() => onMoBai(id)}>
                  ◀ {lui.ten[k] || id}
                </button>
              ))}
            </div>
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
