import React, { useEffect, useMemo, useRef, useState } from 'react';
import Chu from '../../../chung/components/Chu.jsx';
import { buildWorkedSteps } from '../lib/flow.js';
import AnswerInput from './AnswerInput.jsx';
import Figure from './Figure.jsx';

/** Ví dụ dẫn dắt: đi từng nhịp, có câu hỏi xen giữa — con làm cùng chứ không ngồi xem */
/* Năm phần của một bài trình bày chuẩn. Màu đi theo VAI TRÒ: tóm tắt và phân
   tích là chỗ NGHĨ (nền xám nhạt), bài giải là chỗ VIẾT (nền xanh), đáp số là
   chỗ CHỐT (nền vàng) — bé liếc màu là biết đang ở khúc nào. */
const TEN = {
  tomtat: 'TÓM TẮT', phantich: 'PHÂN TÍCH', giai: 'BÀI GIẢI',
  thulai: 'THỬ LẠI', dapso: 'ĐÁP SỐ', ghichu: 'NÓI THÊM',
};
const KIEU = {
  tomtat:   { hop: 'border-line bg-soft', nhan: 'text-mute' },
  phantich: { hop: 'border-line bg-soft', nhan: 'text-mute' },
  giai:     { hop: 'border-teal bg-teal-pale', nhan: 'text-teal-dark' },
  thulai:   { hop: 'border-line bg-white', nhan: 'text-mute' },
  dapso:    { hop: 'border-gold bg-gold-pale', nhan: 'text-gold-dark' },
  ghichu:   { hop: 'border-line bg-white', nhan: 'text-mute' },
};

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
        <div className="rounded-xl bg-soft px-4 py-3.5 text-[16px] font-semibold leading-relaxed">
          <Chu t={we.problem} />
        </div>
        <Figure fig={figure} />

        {/* Gom theo PHẦN rồi in tiêu đề — đúng thứ tự cô giáo dạy trình bày vào
            vở: tóm tắt → phân tích → bài giải → thử lại → đáp số. Trước đây 1634
            dòng bước chạy thành một cột chữ dài, bé không phân biệt được đâu là
            suy nghĩ, đâu là bài làm. Tiêu đề chỉ hiện khi phần ấy ĐÃ có dòng nào
            lộ ra, nếu không thì nó tiết lộ trước là sắp có phần "Đáp số". */}
        {(() => {
          const hien = shown.filter((s) => s.kind === 'show');
          const cuoi = hien[hien.length - 1];
          const nhom = [];
          for (const s of hien) {
            const p = s.phan || 'giai';
            if (!nhom.length || nhom[nhom.length - 1].phan !== p) nhom.push({ phan: p, ds: [] });
            nhom[nhom.length - 1].ds.push(s);
          }
          return nhom.map((g, gi) => (
            <div key={gi} className="mt-3.5 first:mt-2.5">
              <div className={`kicker ${KIEU[g.phan]?.nhan || 'text-mute'}`}>
                {TEN[g.phan] || 'BÀI GIẢI'}
              </div>
              {g.ds.map((s, i) => (
                <div key={i} ref={s === cuoi ? moiRef : null}
                     className={`mt-1.5 flex gap-2.5 rounded-xl border-[1.5px] px-3.5 py-3 text-[15px] ${
                       KIEU[g.phan]?.hop || KIEU.giai.hop}`}>
                  <span className={`font-bold ${KIEU[g.phan]?.nhan || 'text-teal-dark'}`}>▸</span>
                  <span><Chu t={s.text} /></span>
                </div>
              ))}
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
            <p className="text-[16px] font-semibold leading-snug">❓ <Chu t={cur.item.text} /></p>
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
