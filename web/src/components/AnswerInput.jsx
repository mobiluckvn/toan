import React, { useState } from 'react';
import { checkAnswer, inputCount, answerBrief } from '../lib/flow.js';
import AnswerFields, { PickRow } from './AnswerFields.jsx';

export { PickRow };

/**
 * Ô trả lời dùng chung cho: chốt nhanh · câu hỏi xen giữa ví dụ dẫn dắt · sát hạch.
 * Tự chọn kiểu nhập theo format và answerKey — không cần cấu hình thêm.
 */
export default function AnswerInput({ item, onResolve, submitLabel = 'Kiểm tra', autoAdvance }) {
  const n = inputCount(item);
  const isChoice = item.format === 'tf' || item.format === 'mcq';
  const choices = item.format === 'tf' ? ['ĐÚNG', 'SAI'] : (item.choices || []);
  const [vals, setVals] = useState(Array(Math.max(n, 1)).fill(''));
  const [res, setRes] = useState(null);
  const [picked, setPicked] = useState(null);

  const settle = (r) => { setRes(r); onResolve?.(r); };

  const pick = (c, idx) => {
    if (res) return;
    setPicked(idx);
    const input = item.format === 'tf' ? idx === 0 : c;
    settle(checkAnswer(item, input));
  };

  const submit = () => {
    if (res && res.mode !== 'selfcheck') return;
    settle(checkAnswer(item, n <= 1 ? vals[0] : vals));
  };

  /* câu chỉ để tự đối chiếu — không có ô nhập */
  if (n === 0 && !isChoice) {
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
      {isChoice ? (
        <>
          <p className="field-brief"><span aria-hidden>✎</span><span>{answerBrief(item)}</span></p>
          <div className="flex flex-col gap-2.5">
            {choices.map((c, idx) => {
              const isKey = item.format === 'tf'
                ? (idx === 0) === item.answerKey?.value
                : c === item.answerKey?.choice;
              const cls = !res ? '' : isKey ? 'opt-right' : (picked === idx ? 'opt-wrong' : '');
              return (
                <button key={idx} className={`opt ${cls}`} disabled={!!res} onClick={() => pick(c, idx)}>
                  {c}
                </button>
              );
            })}
          </div>
        </>
      ) : (
        <>
          <AnswerFields item={item} vals={vals} disabled={!!res && res.ok}
                        onChange={setVals} onEnter={submit} />
          {!res?.ok && <button className="btn-go mt-3" onClick={submit}>{submitLabel}</button>}
        </>
      )}

      {res && (
        <div className={`mt-3 rounded-xl border-[1.5px] px-3.5 py-3 text-[15px] ${
          res.mode === 'selfcheck' ? 'border-teal bg-teal-pale'
            : res.ok ? 'border-teal bg-teal-pale text-teal-dark' : 'border-alert bg-alert-pale text-alert'}`}>
          {res.mode === 'selfcheck' ? <><b>Lời giải mẫu:</b> {res.expected}</>
            : res.ok ? <>🎉 Đúng rồi! {item.solutionNarrative || ''}</>
            : <>Chưa đúng — con thử lại nhé.</>}
        </div>
      )}
    </div>
  );
}
