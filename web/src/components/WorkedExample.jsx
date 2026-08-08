import React, { useEffect, useMemo, useRef, useState } from 'react';
import { buildWorkedSteps } from '../lib/flow.js';
import AnswerInput from './AnswerInput.jsx';
import Figure from './Figure.jsx';

/** Ví dụ dẫn dắt: đi từng nhịp, có câu hỏi xen giữa — con làm cùng chứ không ngồi xem */
export default function WorkedExample({ we, figure, onNext, onRecord }) {
  const seq = useMemo(() => buildWorkedSteps(we), [we]);
  const [k, setK] = useState(0);          // đã mở tới bước con thứ mấy
  const [answered, setAnswered] = useState({});
  const moiRef = useRef(null);

  const cur = seq[k];
  const done = k >= seq.length;
  const shown = seq.slice(0, k);

  const advance = () => setK((x) => x + 1);

  /**
   * Bước con mở ra thì nó nằm PHÍA DƯỚI chỗ con đang nhìn, mà nút "Bước tiếp" lại
   * dán cứng ở chân màn hình — nên con bấm xong thấy màn hình y như cũ, tưởng hỏng.
   * Kéo đúng phần vừa hiện vào tầm mắt. Bỏ qua bước đầu (k = 0) vì lúc ấy con vẫn
   * đang ở đầu thẻ, kéo là giật màn hình vô cớ.
   */
  useEffect(() => {
    if (k === 0 || !moiRef.current) return;
    moiRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, [k]);

  return (
    <>
      <div className="card">
        <div className="kicker">CÙNG LÀM TỪNG BƯỚC · {(we.title || '').toUpperCase()}</div>
        <div className="rounded-xl bg-[#EAF1F7] px-4 py-3.5 text-[16px] font-semibold leading-relaxed">
          {we.problem}
        </div>
        <Figure fig={figure} />

        {(() => {
          const hien = shown.filter((s) => s.kind === 'show');
          return hien.map((s, i) => (
            <div key={i} ref={i === hien.length - 1 ? moiRef : null}
                 className="mt-2.5 flex gap-2.5 rounded-xl border-[1.5px] border-teal bg-teal-pale px-3.5 py-3 text-[15px]">
              <span className="font-bold text-teal-dark">▸</span><span>{s.text}</span>
            </div>
          ));
        })()}

        {!done && cur?.kind === 'show' && (
          <div className="mt-2.5 flex gap-2.5 rounded-xl border-[1.5px] border-line bg-white px-3.5 py-3 text-[15px] opacity-60">
            <span>▸</span><span>bước tiếp theo…</span>
          </div>
        )}

        {!done && cur?.kind === 'ask' && (
          <div ref={moiRef} className="mt-4 border-t border-line pt-3.5">
            <p className="text-[16px] font-semibold leading-snug">❓ {cur.item.text}</p>
            {/* Câu xen giữa ví dụ cũng là con làm bài thật — 345 câu trên toàn bộ
                168 bài, trước đây không ghi lên máy chủ dòng nào. */}
            <AnswerInput
              item={cur.item}
              onResolve={(r, ct) => {
                setAnswered((a) => ({ ...a, [k]: r }));
                onRecord?.('worked', { id: cur.item.id, ...ct });
              }}
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
