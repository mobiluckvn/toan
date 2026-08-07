import React, { useMemo, useState } from 'react';
import { buildWorkedSteps } from '../lib/flow.js';
import AnswerInput from './AnswerInput.jsx';
import Figure from './Figure.jsx';

/** Ví dụ dẫn dắt: đi từng nhịp, có câu hỏi xen giữa — con làm cùng chứ không ngồi xem */
export default function WorkedExample({ we, figure, onNext }) {
  const seq = useMemo(() => buildWorkedSteps(we), [we]);
  const [k, setK] = useState(0);          // đã mở tới bước con thứ mấy
  const [answered, setAnswered] = useState({});

  const cur = seq[k];
  const done = k >= seq.length;
  const shown = seq.slice(0, k);

  const advance = () => setK((x) => x + 1);

  return (
    <>
      <div className="card">
        <div className="kicker">CÙNG LÀM TỪNG BƯỚC · {(we.title || '').toUpperCase()}</div>
        <div className="rounded-xl bg-[#EAF1F7] px-4 py-3.5 text-[16px] font-semibold leading-relaxed">
          {we.problem}
        </div>
        <Figure fig={figure} />

        {shown.filter((s) => s.kind === 'show').map((s, i) => (
          <div key={i} className="mt-2.5 flex gap-2.5 rounded-xl border-[1.5px] border-teal bg-teal-pale px-3.5 py-3 text-[15px]">
            <span className="font-bold text-teal-dark">▸</span><span>{s.text}</span>
          </div>
        ))}

        {!done && cur?.kind === 'show' && (
          <div className="mt-2.5 flex gap-2.5 rounded-xl border-[1.5px] border-line bg-white px-3.5 py-3 text-[15px] opacity-60">
            <span>▸</span><span>bước tiếp theo…</span>
          </div>
        )}

        {!done && cur?.kind === 'ask' && (
          <div className="mt-4 border-t border-line pt-3.5">
            <p className="text-[16px] font-semibold leading-snug">❓ {cur.item.text}</p>
            <AnswerInput
              item={cur.item}
              onResolve={(r) => setAnswered((a) => ({ ...a, [k]: r }))}
            />
          </div>
        )}
      </div>

      <footer className="fixed inset-x-0 bottom-0 border-t border-line bg-white/95 px-3.5 py-2.5 backdrop-blur"
              style={{ paddingBottom: 'calc(.625rem + env(safe-area-inset-bottom))' }}>
        <div className="mx-auto flex max-w-[740px] gap-2.5">
          {done ? (
            <button className="btn-gold" onClick={onNext}>Vào phòng luyện ▶</button>
          ) : cur.kind === 'show' ? (
            <button className="btn-go" onClick={advance}>Bước tiếp ▶</button>
          ) : (
            <button className="btn-go" disabled={!answered[k]}
                    onClick={advance}>
              {answered[k] ? 'Bước tiếp ▶' : 'Con trả lời rồi mới đi tiếp'}
            </button>
          )}
        </div>
      </footer>
    </>
  );
}
