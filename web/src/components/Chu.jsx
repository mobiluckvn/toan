import React from 'react';
import { tachToan, docToan, docKhoi, docNhanManh } from '../lib/chuviet.js';

/**
 * CHỮ — vẽ một chuỗi markdown + LaTeX. Dùng ở MỌI chỗ có lời văn của bài.
 *
 * Trước đây mọi màn đều in thẳng `{item.text}`, nên "1/(1×2) + 1/(2×3)" hiện
 * đúng như thế: một dòng ký tự chen chúc, phân số nằm ngang, dấu × lẫn với chữ
 * x. Bài toán trông không ra bài toán.
 *
 * `<Chu t="…" />`      một đoạn (không xuống dòng)
 * `<Chu t="…" khoi />` nhiều đoạn, có gạch đầu dòng và danh sách đánh số
 */

/* ── một biểu thức LaTeX ── */
function Toan({ bt }) {
  return (
    <span className="font-mono text-[0.96em] tabular-nums">{renderPhang(docToan(bt))}</span>
  );
}

/** Vẽ một cây đã đọc sẵn (dùng cho tử/mẫu, vốn đã là mảng). */
function renderPhang(ds) {
  return ds.map((o, i) => {
    if (o.k === 'phanso') {
      return (
        <span key={i} className="mx-0.5 inline-flex flex-col items-center align-middle leading-none">
          <span className="px-1 pb-0.5">{renderPhang(o.tu)}</span>
          <span className="w-full border-t-[1.5px] border-current" />
          <span className="px-1 pt-0.5">{renderPhang(o.mau)}</span>
        </span>
      );
    }
    if (o.k === 'mu') return <sup key={i} className="text-[0.75em]">{o.t}</sup>;
    if (o.k === 'chiso') return <sub key={i} className="text-[0.75em]">{o.t}</sub>;
    return <span key={i}>{o.t}</span>;
  });
}

/** Một dòng: xen kẽ lời văn (có **đậm**) và biểu thức. */
function Dong({ t }) {
  return (
    <>
      {tachToan(t).map((m, i) => (m.loai === 'toan'
        ? <Toan key={i} bt={m.t} />
        : (
          <React.Fragment key={i}>
            {docNhanManh(m.t).map((x, j) => {
              if (x.k === 'dam') return <b key={j} className="font-bold text-navy">{x.t}</b>;
              if (x.k === 'nghieng') return <i key={j}>{x.t}</i>;
              if (x.k === 'ma') {
                return <code key={j} className="rounded bg-soft px-1 font-mono text-[0.92em]">{x.t}</code>;
              }
              return <React.Fragment key={j}>{x.t}</React.Fragment>;
            })}
          </React.Fragment>
        )))}
    </>
  );
}

export default function Chu({ t, khoi = false, className = '' }) {
  if (t === null || t === undefined || t === '') return null;
  if (!khoi) return <span className={className}><Dong t={String(t)} /></span>;

  return (
    <div className={className}>
      {docKhoi(t).map((b, i) => {
        if (b.k === 'de') {
          return (
            <h4 key={i} className="mb-1 mt-3 text-[11.5px] font-extrabold tracking-widest text-mute first:mt-0">
              <Dong t={b.t} />
            </h4>
          );
        }
        if (b.k === 'ds') {
          const The = b.kieu === 'so' ? 'ol' : 'ul';
          return (
            <The key={i} className={`mt-1.5 space-y-1 ${b.kieu === 'so' ? 'list-decimal' : 'list-disc'} pl-5`}>
              {b.muc.map((m, j) => <li key={j}><Dong t={m} /></li>)}
            </The>
          );
        }
        return <p key={i} className="mt-1.5 leading-relaxed first:mt-0"><Dong t={b.t} /></p>;
      })}
    </div>
  );
}
