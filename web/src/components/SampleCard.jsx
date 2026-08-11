import React, { useState } from 'react';
import Chu from './Chu.jsx';
import { sampleParts } from '../lib/flow.js';
import Figure from './Figure.jsx';

/** Ca mẫu: hiện đề → con NGHĨ TRƯỚC → bấm mới mở lời giải (không cho xem ngay) */
export default function SampleCard({ example, index, total, figure, onNext }) {
  const ex = sampleParts(example);
  const [open, setOpen] = useState(false);

  return (
    <>
      <div className="card">
        <div className="kicker">BÀI MẪU {index}/{total} · {ex.kind.toUpperCase() || 'CA CHUẨN'}</div>
        <div className="rounded-xl bg-soft px-4 py-3.5 text-[16px] font-semibold leading-relaxed">
          <Chu t={ex.problem} />
        </div>
        <Figure fig={figure} />
        {!open ? (
          <p className="mt-2 text-[14.5px] text-mute">
            💭 Con thử nhẩm trong đầu xem làm thế nào, rồi bấm nút để so với lời giải nhé.
          </p>
        ) : (
          <div className="mt-3 rounded-xl border-[1.5px] border-teal bg-teal-pale px-3.5 py-3 text-[15.5px]">
            <b>Lời giải:</b> <Chu t={ex.solution} />
            {ex.why && <span className="mt-1.5 block text-[13px] text-mute">📌 <Chu t={ex.why} /></span>}
          </div>
        )}
      </div>

      <footer className="fixed inset-x-0 bottom-0 border-t border-line bg-white/95 px-3.5 py-2.5 backdrop-blur"
              style={{ paddingBottom: 'calc(.625rem + env(safe-area-inset-bottom))' }}>
        <div className="mx-auto flex max-w-[740px] gap-2.5">
          {!open
            ? <button className="btn-go" onClick={() => setOpen(true)}>Xem lời giải</button>
            : <button className="btn-go" onClick={onNext}>
                {index === total ? 'Cùng làm từng bước ▶' : 'Bài mẫu tiếp ▶'}
              </button>}
        </div>
      </footer>
    </>
  );
}
