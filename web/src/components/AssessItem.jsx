import React, { useState } from 'react';
import AnswerInput from './AnswerInput.jsx';

/** Sát hạch: không gợi ý, không làm lại — trả lời một lần rồi đi tiếp */
export default function AssessItem({ item, index, total, onDone, onNext, isLast }) {
  const [res, setRes] = useState(null);

  const resolve = (r) => {
    setRes(r);
    onDone?.({ id: item.id, ok: r.ok, mustPass: !!item.mustPass });
  };

  return (
    <>
      <div className="card">
        <div className="kicker">SÁT HẠCH · CÂU {index}/{total}</div>
        {item.mustPass && <span className="pill bg-alert text-white">CÂU BẮT BUỘC ĐÚNG</span>}
        <p className="mt-2 text-[17px] font-semibold leading-snug">{item.text}</p>
        <AnswerInput item={item} onResolve={resolve} submitLabel="Nộp câu này" />
      </div>

      <footer className="fixed inset-x-0 bottom-0 border-t border-line bg-white/95 px-3.5 py-2.5 backdrop-blur"
              style={{ paddingBottom: 'calc(.625rem + env(safe-area-inset-bottom))' }}>
        <div className="mx-auto flex max-w-[740px] gap-2.5">
          <button className="btn-go" disabled={!res} onClick={onNext}>
            {!res ? 'Con trả lời rồi mới nộp' : isLast ? 'Xem kết quả 🏅' : 'Câu tiếp ▶'}
          </button>
        </div>
      </footer>
    </>
  );
}
