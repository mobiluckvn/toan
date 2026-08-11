import React from 'react';
import Chu from '../../../chung/components/Chu.jsx';
import { answerFields, answerBrief } from '../lib/flow.js';

/**
 * Một ô trả lời dạng BẤM CHỌN — dùng cho Đúng/Sai, trắc nghiệm, và các ô mà đề đã
 * nói rõ bộ đáp án ("Điền TĂNG hoặc GIẢM").
 *
 * Đáp án dài (câu giải thích, dãy số) mà xếp thành viên tròn nằm ngang thì bị bóp
 * lại, con phải căng mắt đọc. Dài quá thì xếp DỌC, mỗi phương án một dòng đủ rộng.
 */
export function PickRow({ options, value, disabled, onPick }) {
  const dai = options.some((o) => String(o).length > 24);
  return (
    <div className={dai ? 'flex flex-col gap-2' : 'flex flex-wrap items-center gap-2'}>
      {options.map((o) => (
        <button key={o} type="button" disabled={disabled} onClick={() => onPick(o)}
          aria-pressed={value === o}
          className={dai
            ? `rounded-xl border-[1.5px] px-3.5 py-2.5 text-left text-[15px] leading-snug ${
                value === o ? 'border-navy bg-navy font-bold text-white' : 'border-line bg-white text-navy'}`
            : `rounded-full border-[1.5px] px-3.5 py-1.5 text-[14.5px] font-bold ${
                value === o ? 'border-navy bg-navy text-white' : 'border-line bg-white text-navy'}`}>
          <Chu t={o} />
        </button>
      ))}
    </div>
  );
}

/**
 * Khối ô trả lời dùng chung cho luyện tập · sát hạch · chốt nhanh.
 *
 * Ba thứ con cần thấy TRƯỚC khi gõ, và phải còn thấy TRONG LÚC gõ:
 *   1. bài này cần điền mấy ô          → dòng tóm tắt
 *   2. ô này hỏi cái gì                → nhãn nằm NGOÀI ô, không phải chữ mờ
 *   3. điền dạng gì, đơn vị nào        → chip đơn vị + chữ mờ mô tả dạng
 */
export default function AnswerFields({ item, vals, disabled, onChange, onEnter }) {
  const fields = answerFields(item);
  if (fields.length === 0) return null;
  const brief = answerBrief(item);
  const set = (i, v) => onChange(vals.map((x, k) => (k === i ? v : x)));

  return (
    <div className="mt-3">
      {brief && <p className="field-brief"><span aria-hidden>✎</span><span>{brief}</span></p>}
      <div className="flex flex-col gap-2.5">
        {fields.map((f) => (
          <div key={f.index} className="field">
            <div className="field-head">
              {f.letter && <span className="field-letter">{f.letter}</span>}
              <label htmlFor={`ans-${f.index}`}><Chu t={f.label} /></label>
              {f.unit && <span className="field-unit">đơn vị: {f.unit}</span>}
            </div>
            {f.kind === 'pick' ? (
              <PickRow options={f.options} value={vals[f.index]} disabled={disabled}
                       onPick={(o) => set(f.index, o)} />
            ) : f.kind === 'essay' ? (
              /* Câu tự luận: ô nhiều dòng để con viết lập luận, xong mới so lời giải mẫu.
                 Enter ở đây là XUỐNG DÒNG, không phải nộp bài. */
              <textarea id={`ans-${f.index}`} rows={4}
                        className="numin w-full text-left text-[15px] font-normal leading-relaxed"
                        placeholder={f.placeholder} value={vals[f.index] ?? ''} disabled={disabled}
                        onChange={(e) => set(f.index, e.target.value)} />
            ) : (
              <input id={`ans-${f.index}`} className="numin w-full"
                     inputMode={f.kind === 'number' ? 'decimal' : 'text'} autoComplete="off"
                     placeholder={f.placeholder} value={vals[f.index] ?? ''} disabled={disabled}
                     onChange={(e) => set(f.index, e.target.value)}
                     onKeyDown={(e) => e.key === 'Enter' && !disabled && onEnter?.()} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
