import React, { useState } from 'react';
import { checkAnswer, inputCount, answerBrief, answerFields } from '../lib/flow.js';
import AnswerFields, { PickRow } from './AnswerFields.jsx';

export { PickRow };

/**
 * Ô trả lời dùng chung cho: chốt nhanh · câu hỏi xen giữa ví dụ dẫn dắt · sát hạch.
 * Tự chọn kiểu nhập theo format và answerKey — không cần cấu hình thêm.
 */
export default function AnswerInput({ item, onResolve, submitLabel = 'Kiểm tra', autoAdvance }) {
  const n = inputCount(item);
  const [vals, setVals] = useState(Array(Math.max(n, 1)).fill(''));
  const [res, setRes] = useState(null);

  const settle = (r) => { setRes(r); onResolve?.(r); };

  /* Đúng/Sai và trắc nghiệm nay cũng là một ô trong AnswerFields, nên không còn
     nhánh riêng ở đây — một khối ô trả lời dùng chung cho mọi màn hình. */
  const submit = () => {
    if (res?.ok) return;                   // đúng rồi thì thôi, còn sai thì thử lại thoải mái
    settle(checkAnswer(item, n <= 1 ? vals[0] : vals));
  };

  /* câu tự luận — làm ra nháp rồi tự so, không có ô nhập */
  if (answerFields(item).length === 0) {
    return (
      <div className="mt-3">
        {!res ? (
          <>
            <p className="field-brief"><span aria-hidden>✎</span><span>{answerBrief(item)}</span></p>
            <button className="btn-ghost" onClick={() => settle(checkAnswer(item, ''))}>
              Con nghĩ xong rồi — xem lời giải
            </button>
          </>
        ) : (
          <div className="rounded-xl border-[1.5px] border-teal bg-teal-pale px-3.5 py-3 text-[15px]">
            <b>Lời giải mẫu:</b> {res.expected || item.solutionNarrative}
            {autoAdvance && <p className="mt-1.5 text-[13px] text-mute">Con so với cách làm của mình nhé.</p>}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="mt-3">
      <AnswerFields item={item} vals={vals} disabled={!!res?.ok}
                    onChange={setVals} onEnter={submit} />
      {!res?.ok && <button className="btn-go mt-3" onClick={submit}>{submitLabel}</button>}

      {res && (
        <div className={`mt-3 rounded-xl border-[1.5px] px-3.5 py-3 text-[15px] ${
          res.mode === 'selfcheck' ? 'border-teal bg-teal-pale'
            : res.ok ? 'border-teal bg-teal-pale text-teal-dark' : 'border-alert bg-alert-pale text-alert'}`}>
          {res.mode === 'selfcheck' ? <><b>Lời giải mẫu:</b> {res.expected}</>
            : res.ok ? <>🎉 Đúng rồi! {item.solutionNarrative || ''}</>
            : <>Chưa đúng — con chọn/sửa lại rồi bấm {submitLabel} lần nữa nhé.</>}
        </div>
      )}
    </div>
  );
}
