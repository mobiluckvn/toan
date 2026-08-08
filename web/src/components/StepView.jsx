import React, { useState } from 'react';
import Figure from './Figure.jsx';
import SampleCard from './SampleCard.jsx';
import WorkedExample from './WorkedExample.jsx';
import AnswerInput from './AnswerInput.jsx';
import PracticeItem from './PracticeItem.jsx';
import AssessItem from './AssessItem.jsx';
import FinaleCard from './FinaleCard.jsx';
import { answerMode } from '../lib/flow.js';

/** Nút chân màn hình lúc con CHƯA trả lời — nhắc đúng việc phải làm cho từng kiểu */
const CHO_TRA_LOI = {
  so:        'Con điền số rồi bấm Kiểm tra',
  bieuthuc:  'Con điền đáp án rồi bấm Kiểm tra',
  dungsai:   'Con chọn ĐÚNG hoặc SAI đã nhé',
  chondapan: 'Con chọn đáp án đã nhé',
  tuluan:    'Con xem lời giải rồi đi tiếp',
};

const Foot = ({ label = 'Tiếp ▶', cls = 'btn-go', onClick, disabled }) => (
  <footer className="fixed inset-x-0 bottom-0 border-t border-line bg-white/95 px-3.5 py-2.5 backdrop-blur"
          style={{ paddingBottom: 'calc(.625rem + env(safe-area-inset-bottom))' }}>
    <div className="mx-auto flex max-w-[740px] gap-2.5">
      <button className={cls} onClick={onClick} disabled={disabled}>{label}</button>
    </div>
  </footer>
);

export default function StepView({ step, lesson, onNext, onJump, onRecord, log, onFinish, onRestart }) {
  const K = lesson.knowledgeCore || {};
  const [checked, setChecked] = useState(null);

  switch (step.type) {
    /* ══ MỞ BÀI ══ */
    case 'intro':
      return (<>
        <div className="card">
          <div className="kicker">MICRO · KHOẢNG {lesson.durationMinutes} PHÚT</div>
          <h2 className="mb-2.5 text-[19px] font-bold leading-snug text-navy">{lesson.title}</h2>
          {/* Con đọc bản ngắn. Bản gốc viết cho người lớn — dài 60 chữ, nhiều ngoặc
              lồng nhau — nên gấp lại phía dưới cho bố mẹ và thầy cô xem khi cần. */}
          <p className="text-[16.5px] leading-relaxed">
            {lesson.objective?.kidText || lesson.objective?.text}
          </p>
          {lesson.objective?.kidText && lesson.objective?.text && (
            <details className="mt-2">
              <summary className="cursor-pointer text-[12.5px] font-semibold text-mute">
                Mục tiêu đầy đủ (dành cho bố mẹ)
              </summary>
              <p className="mt-1.5 text-[14px] leading-relaxed text-mute">{lesson.objective.text}</p>
            </details>
          )}
          <Figure fig={step.figure} />
          <div className="step0-box text-[15px]">
            Đường đi của bài: <b>Giảng nguyên tắc → Xem bài mẫu → Tự luyện → Sát hạch lấy huy hiệu</b>
          </div>
        </div>
        <div className="rounded-2xl bg-gradient-to-br from-gold to-[#fcd88a] px-4 py-5 text-center text-[19px] font-extrabold leading-snug text-gold-dark">
          🔑 {K.mantra}
        </div>
        <Foot label="Bắt đầu ▶" onClick={onNext} />
      </>);

    case 'hook':
      return (<>
        <div className="card">
          <div className="kicker">TÌNH HUỐNG</div>
          <p className="text-[16.5px] leading-relaxed">{step.screen?.narration}</p>
          <Figure fig={step.figure} />
          {step.screen?.display?.caption && (
            <div className="warn-box text-[15px]">
              <b>Câu hỏi:</b> {step.screen.display.caption} — con thử đoán xem bạn ấy sai ở đâu nhé!
            </div>
          )}
        </div>
        <Foot label="Nghe cô giảng ▶" onClick={onNext} />
      </>);

    /* ══ GIẢNG ══ */
    case 'teach':
      return (<>
        <div className="card">
          <div className="kicker">NGUYÊN TẮC</div>
          {step.statements.map((st) => (
            <div key={st.id} className="rule-box text-[15.5px]">
              <span className="mr-2 rounded bg-navy px-1.5 py-0.5 align-[2px] text-[11px] font-extrabold text-white">
                {st.id}
              </span>
              {st.text}
            </div>
          ))}
          <Figure fig={step.figure} />
          {step.screen?.narration && (
            <p className="text-[16px] leading-relaxed">{step.screen.narration}</p>
          )}
          {step.misconception && (
            <div className="warn-box text-[15px]">
              <div><b className="text-alert">SAI:</b> {step.misconception.wrong}</div>
              <div className="mt-1 text-[13.5px] text-mute">Dấu hiệu: {step.misconception.signal}</div>
              <div className="mt-2 rounded-lg bg-teal-pale px-3 py-2">
                <b>GỠ:</b> {step.misconception.fix}
              </div>
              {step.misconception.counterExample && (
                <p className="mt-2 text-[14.5px]">{step.misconception.counterExample}</p>
              )}
            </div>
          )}
        </div>
        <Foot onClick={onNext} />
      </>);

    case 'check':
      return (<>
        <div className="card">
          <div className="kicker">CHỐT NHANH · CON THỬ NHÉ</div>
          <p className="text-[17px] font-semibold leading-snug">{step.item.text}</p>
          <AnswerInput item={step.item} onResolve={setChecked} />
          {checked && !checked.ok && step.item.wrongFeedback && (
            <p className="mt-2 text-[14.5px] text-mute">{step.item.wrongFeedback}</p>
          )}
        </div>
        {/* Nút chân màn hình phải nói ĐÚNG việc con đang phải làm: câu điền số mà
            ghi "Con chọn đáp án nhé" thì con đi tìm nút để bấm, không thấy đâu cả. */}
        <Foot onClick={onNext} disabled={!checked}
              label={checked ? 'Tiếp ▶' : CHO_TRA_LOI[answerMode(step.item)]} />
      </>);

    case 'mantra':
      return (<>
        <div className="card text-center">
          <div className="kicker">THẦN CHÚ CỦA BÀI</div>
          <div className="rounded-2xl bg-gradient-to-br from-gold to-[#fcd88a] px-4 py-5 text-[19px] font-extrabold leading-snug text-gold-dark">
            {step.text}
          </div>
          <p className="mt-3 text-[15px] text-mute">Con đọc to hai lần — gặp đề là nhẩm lại ngay.</p>
          {step.vocabulary?.length > 0 && (
            <div className="mt-3 flex flex-wrap justify-center gap-1.5">
              {step.vocabulary.map((v) => (
                <i key={v} className="pill bg-[#F2F6FA] not-italic text-navy">{v}</i>
              ))}
            </div>
          )}
        </div>
        <Foot label="Xem bài mẫu ▶" cls="btn-gold" onClick={onNext} />
      </>);

    /* ══ BÀI MẪU ══ */
    case 'sample':
      return <SampleCard example={step.example} index={step.index} total={step.total}
                         figure={step.figure} onNext={onNext} />;

    case 'worked':
      return <WorkedExample we={step.we} figure={step.figure} onNext={onNext} />;

    /* ══ LUYỆN TẬP ══ */
    case 'practice':
      return <PracticeItem item={step.item} level={step.level} figure={step.figure}
                           onDone={(e) => onRecord('practice', e)}
                           onJumpTeach={() => onJump('mantra')}
                           onNext={onNext} />;

    /* ══ SÁT HẠCH ══ */
    case 'assess':
      return <AssessItem item={step.item} index={step.index} total={step.total}
                         isLast={step.index === step.total}
                         onDone={(e) => onRecord('assess', e)} onNext={onNext} />;

    case 'finale':
      return <FinaleCard lesson={lesson} log={log}
                         onRetry={onRestart} onJumpTeach={() => onJump('teach')}
                         onFinish={onFinish} />;

    default:
      return (<>
        <div className="card">
          <p className="text-[15px] text-mute">Bước chưa dựng: {step.type}</p>
        </div>
        <Foot onClick={onNext} />
      </>);
  }
}
