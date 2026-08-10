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

export default function StepView({ step, lesson, onNext, onJump, onRecord, log, onFinish, onRestart, onMoBai }) {
  const K = lesson.knowledgeCore || {};
  const [checked, setChecked] = useState(null);

  switch (step.type) {
    /* ══ MỞ BÀI — MỘT MÀN, VÀ VIỆC CỦA NÓ LÀ NÊU VẤN ĐỀ ══
       Trước đây đây là HAI màn, và cả hai đều nói trước cách làm:
         · màn 1 in `knowledgeCore.mantra` bằng chữ to — toàn bộ cách làm;
         · rồi in `objective.kidText`, mà với lớp 5 dòng ấy cũng là một câu luật:
           "Số dư luôn bé hơn số chia, nên dư lớn nhất bằng số chia trừ 1."
         · màn 2 mới hỏi: "Số dư lớn nhất khi chia cho 5 là bao nhiêu?"
       Bé đọc đáp trước khi đọc đề, và phải bấm hai lần mới tới được bài toán.

       Nay: nêu vấn đề ở đây, giải quyết ở phần giảng. Mục tiêu giáo án chỉ hiện
       khi nó THẬT SỰ là lời mời viết tay (`objective.laLoiChao`) — quyển chưa có
       lời chào thì dòng ấy là câu trả lời, để ở đây là lộ bài. */
    case 'intro': {
      const de = step.screen?.narration;
      const loiChao = lesson.objective?.laLoiChao ? lesson.objective.kidText : null;
      return (<>
        <div className="card">
          <div className="kicker">MICRO · KHOẢNG {lesson.durationMinutes} PHÚT</div>
          <h2 className="mb-2.5 text-[19px] font-bold leading-snug text-navy">{lesson.title}</h2>
          {loiChao && <p className="text-[16.5px] leading-relaxed">{loiChao}</p>}

          {/* ĐỀ BÀI — thứ đáng đọc nhất màn này, nên cho nó một khung riêng. */}
          {de && (
            <div className={`rounded-2xl border-[1.5px] border-line bg-soft px-4 py-3.5 ${loiChao ? 'mt-3' : ''}`}>
              <div className="kicker mb-1">BÀI TOÁN</div>
              <p className="text-[16.5px] font-semibold leading-relaxed text-navy">{de}</p>
            </div>
          )}
          <Figure fig={step.figure} />

          {/* Bản đầy đủ của mục tiêu gấp lại cho bố mẹ — con không phải đọc. */}
          {lesson.objective?.text && (
            <details className="mt-2.5">
              <summary className="cursor-pointer text-[12.5px] font-semibold text-mute">
                Bài này học gì (dành cho bố mẹ)
              </summary>
              <p className="mt-1.5 text-[14px] leading-relaxed text-mute">{lesson.objective.text}</p>
            </details>
          )}
        </div>
        <div className="rounded-2xl bg-gradient-to-br from-gold to-[#fcd88a] px-4 py-4 text-center text-[17px] font-extrabold leading-snug text-gold-dark">
          {de ? 'Con thử nghĩ trước xem làm thế nào, rồi mình cùng gỡ nhé.'
              : 'Mình bắt đầu nhé — con thử nghĩ trước, rồi mình cùng tìm cách làm.'}
        </div>
        <Foot label={de ? 'Nghe cô giảng ▶' : 'Xem bài toán ▶'} onClick={onNext} />
      </>);
    }

    /* Màn ĐỀ BÀI riêng — chỉ có ở quyển đã viết lời chào, để lời chào được một
       nhịp mời vào rồi mới tới đề. */
    case 'hook':
      return (<>
        <div className="card">
          <div className="kicker">BÀI TOÁN</div>
          <p className="text-[16.5px] leading-relaxed">{step.screen?.narration}</p>
          <Figure fig={step.figure} />
        </div>
        <Foot label="Nghe cô giảng ▶" onClick={onNext} />
      </>);

    /* ══ GIẢNG ══ */
    case 'teach':
      return (<>
        <div className="card">
          {/* Màn giảng KHÔNG mang nguyên tắc nào thì đừng gọi nó là "NGUYÊN TẮC":
              sách lớp 4 có hai màn kiểu ấy mỗi bài (nhịp DỊCH dựng mô hình, nhịp
              LẮP - SOI lắp kết quả về đời thật). Quyển nào không khai `nhan` thì
              giữ nguyên nhãn cũ, nên lớp 2 · lớp 3 · lớp 5 không đổi một chữ. */}
          <div className="kicker">
            {step.screen?.nhan
              || (step.statements.length ? 'NGUYÊN TẮC'
                : step.screen?.kind === 'trap' ? 'CHỖ HAY NHẦM' : 'CÙNG XEM')}
          </div>
          {step.statements.map((st) => (
            <div key={st.id} className="rule-box text-[15.5px]">
              <span className="mr-2 rounded bg-navy px-1.5 py-0.5 align-[2px] text-[11px] font-extrabold text-white">
                {st.id}
              </span>
              {st.text}
            </div>
          ))}
          <Figure fig={step.figure} />
          {/* `whitespace-pre-line` để mục ③ và ⑤ của lớp 4 giữ được từng dòng có
              nhãn (CHO GÌ · HỎI GÌ · …). Quyển khác không có ký tự xuống dòng trong
              lời giảng nên hiện y như cũ. */}
          {/* Màn BẪY có lời dẫn TRÙNG NGUYÊN VĂN với ô "SAI" ngay dưới — cùng lấy từ
              câu nói sai của nhân vật. In hai lần thì bé đọc lại y hệt một đoạn, mà
              đoạn ấy lại là câu SAI: nhắc hai lần thứ mình muốn bé quên. Bỏ bản trên,
              giữ ô SAI vì nó có kèm dấu hiệu và lời gỡ. */}
          {step.screen?.narration
            && step.screen.narration !== step.misconception?.wrong && (
            <p className="whitespace-pre-line text-[16px] leading-relaxed">
              {step.screen.narration}
            </p>
          )}
          {step.misconception && (
            <div className="warn-box text-[15px]">
              {/* Hình của chỗ hay nhầm — thường là bong bóng lời thoại một bạn nói
                  chắc nịch một câu SAI. Đặt ở ĐÂY, ngay trên dòng "SAI:", thì bé
                  đọc xong biết ngay đó là bẫy. Trước kia nó nằm ở màn mở bài, tức
                  hiện trước khi bé học gì và không có gì đính chính. */}
              <Figure fig={step.figureBay} />
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
          {/* Chốt nhanh CŨNG là con làm bài — trước đây không ghi lên máy chủ, mất
              trắng 168 câu (một câu mỗi bài). */}
          <AnswerInput item={step.item}
                       onResolve={(r, ct) => { setChecked(r); onRecord?.('check', { id: step.item.id, ...ct }); }} />
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
      return <WorkedExample we={step.we} figure={step.figure} onNext={onNext} onRecord={onRecord} />;

    /* ══ LUYỆN TẬP ══ */
    case 'practice':
      return <PracticeItem item={step.item} level={step.level} figure={step.figure}
                           figureGiai={step.figureGiai}
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
                         onFinish={onFinish} onMoBai={onMoBai} />;

    default:
      return (<>
        <div className="card">
          <p className="text-[15px] text-mute">Bước chưa dựng: {step.type}</p>
        </div>
        <Foot onClick={onNext} />
      </>);
  }
}
