import React, { useState } from 'react';
import Chu from '../../../chung/components/Chu.jsx';
import {
  checkAnswer, inputCount, hintState, canGenerate, makeVariant, answerBrief, answerFields, answerMode,
} from '../lib/flow.js';
import Figure from './Figure.jsx';
import AnswerFields from './AnswerFields.jsx';

const LEVEL = { warmup: 'KHỞI ĐỘNG', standard: 'CƠ BẢN', challenge: 'THỬ THÁCH' };

/** Luyện tập: gợi ý 2 tầng · sai 3 lần mở đáp án · luôn có lối quay lại nguyên tắc */
export default function PracticeItem({ item: base, level, figure, figureGiai, onDone, onJumpTeach, onNext }) {
  const [item, setItem] = useState(base);
  const [vals, setVals] = useState(() => Array(Math.max(inputCount(base), 1)).fill(''));
  const [tries, setTries] = useState(0);
  const [res, setRes] = useState(null);
  const [tCau, setTCau] = useState(() => Date.now());   // mốc để đo thời gian RIÊNG câu này

  const n = inputCount(item);
  const hs = hintState(item, tries);
  /**
   * Khoá ô CHỈ khi con đã đúng. Trước đây có một biến `finished = res?.ok ||
   * hs.reveal` và màn khoá theo nó — mà nó còn bật khi lộ đáp án sau 3 lần sai:
   * màn hình bảo "con thử lại nhé" trong khi mọi ô đã tắt, con sửa cũng không
   * được. Sai bao nhiêu lần cũng phải được thử lại.
   * Biến ấy nằm lại không ai dùng cho tới 10-10-2026, ESLint tìm ra thì gỡ.
   */
  const khoaO = !!res?.ok;
  const variantable = !!canGenerate(item);

  /**
   * Ghi MỌI lượt bấm "Kiểm tra", kể cả lượt sai ở giữa.
   *
   * Trước đây chỉ báo khi con ĐÚNG, hoặc khi đã sai đủ 3 lần — nên con sai lần một
   * rồi tự sửa đúng lần hai thì máy chủ chỉ thấy "đúng ngay", mất sạch dấu vết con
   * vấp ở đâu. Chính chỗ vấp ấy mới là thứ cô giáo cần để giúp con.
   */
  const submit = () => {
    const dap = n <= 1 ? vals[0] : vals;
    const r = checkAnswer(item, dap);
    setRes(r);
    const t = tries + 1;
    const xong = r.ok || r.mode === 'selfcheck';
    if (!xong) setTries(t);
    onDone?.({
      id: item.id, ok: xong, tries: t,
      ms: Date.now() - tCau, answer: dap, expected: r.expected,
      mode: answerMode(item), hintsUsed: hs.show.length,
      revealed: !xong && t >= 3, mustPass: !!item.mustPass,
    });
  };

  const another = () => {
    const v = makeVariant(item);
    if (!v) return;
    setItem(v); setVals(Array(Math.max(inputCount(v), 1)).fill('')); setTries(0); setRes(null);
    setTCau(Date.now());
  };

  return (
    <>
      <div className="card">
        <div className="kicker">PHÒNG LUYỆN · {LEVEL[level] || level}</div>
        <p className="text-[17px] font-semibold leading-snug"><Chu t={item.text} /></p>
        {item._variant && <span className="pill mt-2 bg-teal-pale text-teal-dark">đề mới cùng dạng</span>}
        <Figure fig={figure} />

        {n === 0 ? (
          <div className="mt-3">
            <p className="field-brief"><span aria-hidden>✎</span><span>{answerBrief(item)}</span></p>
            <button className="btn-ghost" onClick={submit} disabled={!!res}>
              Con làm xong rồi — xem lời giải
            </button>
          </div>
        ) : (
          <>
            <AnswerFields item={item} vals={vals} disabled={khoaO}
                          onChange={setVals} onEnter={submit} />
            {/* chỉ nhắc chuyện đơn vị khi ô ĐANG chờ một con số — câu trả lời bằng
                chữ mà bảo "điền số là đủ" thì con lại tưởng mình hiểu sai đề */}
            {answerFields(item).every((f) => f.kind === 'number') && (
              <p className="mt-1.5 text-[12.5px] text-mute">
                Con điền số là đủ — ghi kèm đơn vị cũng được.
              </p>
            )}
          </>
        )}

        {res && (
          <div className={`mt-3 rounded-xl border-[1.5px] px-3.5 py-3 text-[15px] ${
            res.ok || res.mode === 'selfcheck'
              ? 'border-teal bg-teal-pale text-teal-dark' : 'border-alert bg-alert-pale text-alert'}`}>
            {res.mode === 'selfcheck' ? <><b>Lời giải mẫu:</b> <Chu t={res.expected} /></>
              : res.ok ? <>🎉 Chuẩn! <Chu t={item.solutionNarrative || ''} /></>
              : <>Chưa đúng — con sửa lại rồi bấm Kiểm tra lần nữa nhé. Thử bao nhiêu lần cũng được.</>}
          </div>
        )}

        {hs.show.map((h, i) => (
          <div key={i} className="step0-box text-[14.5px]">💡 <Chu t={h} /></div>
        ))}

        {hs.reveal && !res?.ok && (
          <div className="mt-2 rounded-xl border-[1.5px] border-teal bg-teal-pale px-3.5 py-3 text-[15px]">
            <b>Đáp án:</b> <Chu t={res?.expected} />
            {item.solutionNarrative && <div className="mt-1"><Chu t={item.solutionNarrative} /></div>}
            <Figure fig={figureGiai} />
          </div>
        )}
      </div>

      <footer className="fixed inset-x-0 bottom-0 border-t border-line bg-white/95 px-3.5 py-2.5 backdrop-blur"
              style={{ paddingBottom: 'calc(.625rem + env(safe-area-inset-bottom))' }}>
        <div className="mx-auto flex max-w-[740px] gap-2.5">
          {res?.ok ? (
            <>
              {variantable && <button className="btn-ghost" onClick={another}>Đề khác</button>}
              <button className="btn-go" onClick={onNext}>Câu tiếp ▶</button>
            </>
          ) : hs.reveal ? (
            /* Đã lộ đáp án sau 3 lần sai — con vẫn được thử lại cho tới khi tự làm
               đúng, hoặc bấm đi tiếp. Không cụt đường như trước. */
            <>
              <button className="btn-ghost" onClick={submit}>Thử lại</button>
              <button className="btn-go" onClick={onNext}>Câu tiếp ▶</button>
            </>
          ) : (
            <>
              <button className="btn-ghost" onClick={onJumpTeach}>Xem lại nguyên tắc</button>
              <button className="btn-go" onClick={submit}>Kiểm tra</button>
            </>
          )}
        </div>
      </footer>
    </>
  );
}
