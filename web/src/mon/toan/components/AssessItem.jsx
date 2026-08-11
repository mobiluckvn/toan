import React, { useState } from 'react';
import Chu from '../../../chung/components/Chu.jsx';
import AnswerInput from './AnswerInput.jsx';

/** Sát hạch: không gợi ý, không làm lại — trả lời một lần rồi đi tiếp */
export default function AssessItem({ item, index, total, onDone, onNext, isLast }) {
  const [res, setRes] = useState(null);

  /* Sát hạch chỉ trả lời một lần, nhưng vẫn ghi đủ chi tiết: con bấm gì, mất bao lâu.
     Câu BẮT BUỘC ĐÚNG mà con chọn nhầm phương án nào — đó là chỗ cô cần nhìn nhất. */
  const resolve = (r, ct) => {
    setRes(r);
    onDone?.({ id: item.id, ok: r.ok, mustPass: !!item.mustPass, ...ct });
  };

  return (
    <>
      <div className="card">
        <div className="kicker">SÁT HẠCH · CÂU {index}/{total}</div>
        {item.mustPass && <span className="pill bg-alert text-white">CÂU BẮT BUỘC ĐÚNG</span>}
        <p className="mt-2 text-[17px] font-semibold leading-snug"><Chu t={item.text} /></p>
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
