import React, { useEffect, useState } from 'react';
import { CONTENT, dongDau, maKy } from '../lib/content.js';
import Figure from './Figure.jsx';
import AnswerInput from './AnswerInput.jsx';

/**
 * Kỳ sát hạch chương — MÁY CHẤM khi câu có `answerKey`, tự chấm khi không có.
 *
 * Trước đây màn này chấm tay 100%: mỗi câu chỉ có một nút "Con làm xong — xem lời
 * giải" rồi hỏi bé "Mình làm đúng / Mình làm sai". Nghĩa là chỗ QUAN TRỌNG NHẤT của
 * quyển — nơi quyết định bé có qua chương hay không — lại là chỗ không đo được gì:
 * sổ phụ huynh và bảng cô giáo nhận đúng con số bé tự chấm cho mình. Nếp ấy đến từ
 * lớp 5, nơi câu sát hạch là tự luận dài nên tự chấm là hợp lý; sách lớp 4 thì 236
 * câu đều có đáp số xác định.
 *
 * Nay: câu nào có `answerKey` thì `AnswerInput` lo cả việc nhập lẫn việc chấm, và
 * kết quả tự ghi vào `marks`. Câu nào KHÔNG có (đọc số thành chữ — mỗi bé đọc một
 * cách) thì vẫn giữ hai nút tự chấm. Bảng tự soi ở cuối không đổi.
 */
export default function ExamPlayer({ chapter, onDone, onOpenMicro, onExit,
                                    chuongTrinh = 'lop5' }) {
  const [doc, setDoc] = useState(null);
  const [i, setI] = useState(0);
  const [marks, setMarks] = useState({});     // qno → true/false
  const [shown, setShown] = useState(false);   // chỉ dùng cho câu KHÔNG có answerKey
  const [res, setRes] = useState(null);        // kết quả máy chấm câu đang làm

  useEffect(() => {
    /* Mọi chương trình cùng một màn sát hạch, chỉ khác tệp nội dung. Tiền tố tệp
       suy TỪ SỔ ĐĂNG KÝ, không gõ tay: bảng `lop2 ? KSN2 : KSN5Q1` chỉ đúng khi có
       hai quyển, thêm lớp 3 là mọi kỳ sát hạch của nó nạp nhầm tệp của lớp 5. */
    const ma = maKy(chuongTrinh);
    fetch(dongDau(`${CONTENT}/reviews/DCR_${ma}_C${chapter}.json`))
      .then((r) => r.json()).then(setDoc).catch(() => setDoc({ error: true }));
  }, [chapter, chuongTrinh]);

  if (!doc) return <div className="p-6 text-mute">Đang mở kỳ sát hạch…</div>;
  if (doc.error) return <div className="p-6 text-alert">Không nạp được kỳ sát hạch chương {chapter}.</div>;

  const qs = doc.examA || [];
  const done = i >= qs.length;
  const right = Object.values(marks).filter(Boolean).length;
  /* Ngưỡng đạt lấy TỪ DỮ LIỆU: sách lớp 2 mỗi chương một ngưỡng (8/12, 8/10,
     6/8 vụ án). Ghim cứng 12 là chấm sai cho cả 11 kỳ của lớp 2. */
  const need = doc.need || 12;

  if (done) {
    const pass = right >= need;
    const wrong = qs.filter((q) => marks[q.qno] === false);
    return (
      <div className="mx-auto max-w-[740px] px-3.5 pb-28 pt-4">
        <div className="card text-center">
          <div className="text-[58px] leading-none">{pass ? '🏅' : '💪'}</div>
          <h2 className="mt-1 text-[21px] font-bold text-navy">
            {right}/{qs.length} câu · {pass ? 'ĐẠT!' : `cần ${need} câu mới đạt`}
          </h2>
          <p className="mt-1 text-[14.5px] text-mute">{doc.passRule}</p>
        </div>

        {wrong.length > 0 && (
          <div className="card">
            <div className="kicker">BẢNG TỰ SOI — SAI CÂU NÀO, ÔN BÀI ĐÓ</div>
            {wrong.map((q) => (
              <button key={q.qno} onClick={() => onOpenMicro(q.diagnosesMicro)}
                className="mt-2 flex w-full items-center gap-2.5 rounded-xl border border-line px-3 py-2.5 text-left text-[14px] hover:bg-[#F0F5F9]">
                <span className="rounded bg-alert px-1.5 py-0.5 text-[11px] font-extrabold text-white">câu {q.qno}</span>
                <span className="flex-1">{q.trapName || 'ôn lại bài này'}</span>
                <span className="font-mono text-[11.5px] text-mute">
                  {(q.diagnosesMicro || '').replace(/^DL:[A-Z0-9]+\./, '')} ▶
                </span>
              </button>
            ))}
          </div>
        )}

        <footer className="fixed inset-x-0 bottom-0 border-t border-line bg-white/95 px-3.5 py-2.5"
                style={{ paddingBottom: 'calc(.625rem + env(safe-area-inset-bottom))' }}>
          <div className="mx-auto flex max-w-[740px] gap-2.5">
            <button className="btn-ghost" onClick={() => { setI(0); setMarks({}); setShown(false); }}>Làm lại</button>
            <button className="btn-gold" onClick={() => onDone({ pass, right, total: qs.length })}>
              Về trang chính
            </button>
          </div>
        </footer>
      </div>
    );
  }

  const q = qs[i];
  return (
    <div className="mx-auto max-w-[740px] px-3.5 pb-28 pt-4">
      <header className="mb-3 flex items-center gap-2.5">
        <button className="text-[13px] text-mute" onClick={onExit}>← Thoát</button>
        <b className="flex-1 text-center text-[14px] text-navy">{doc.name}</b>
        <span className="text-[12px] tabular-nums text-mute">{i + 1}/{qs.length}</span>
      </header>

      {/* Hình dùng CHUNG cho cả kỳ (tranh công viên, cuộn mật thư, bốn trạm…):
          nhiều câu hỏi cùng nhìn vào nó, nên phải thấy được ở MỌI câu. */}
      {(doc.hinh || []).map((h) => <Figure key={h.id} fig={h} />)}

      <div className="card">
        <div className="kicker">
          CÂU {q.qno} {q.star ? '· ' + '★'.repeat(q.star) : ''}
          {q.hasTrap && <span className="pill ml-2 bg-alert text-white">CÓ BẪY</span>}
        </div>
        <p className="text-[16.5px] font-semibold leading-relaxed">{q.text}</p>

        {/* Có khoá đáp án thì máy chấm — bé điền số hoặc bấm chọn, không phải tự
            phán mình đúng hay sai. `key` theo mã câu để sang câu mới thì ô nhập
            reset; thiếu nó là câu sau thừa hưởng đáp án câu trước. */}
        {q.answerKey && (
          <AnswerInput key={q.id} item={q} submitLabel="Kiểm tra"
                       onResolve={(r) => {
                         setRes(r);
                         setMarks((m) => ({ ...m, [q.qno]: !!r.ok }));
                       }} />
        )}

        {q.answerKey && res && (
          <div className={`mt-3 rounded-xl border-[1.5px] px-3.5 py-3 text-[15px] ${
            res.ok ? 'border-teal bg-teal-pale text-teal-dark'
                   : 'border-alert bg-alert-pale text-alert'}`}>
            {res.ok ? <>🎉 Chuẩn!</> : <><b>Chưa đúng.</b> Lời giải: {q.answer}</>}
          </div>
        )}

        {!q.answerKey && shown && (
          <div className="mt-3 rounded-xl border-[1.5px] border-teal bg-teal-pale px-3.5 py-3 text-[15px]">
            <b>Lời giải:</b> {q.answer}
            {q.hasTrap && q.trapName && (
              <div className="mt-2 text-[13.5px] text-alert"><b>Bẫy:</b> {q.trapName}</div>
            )}
          </div>
        )}
      </div>

      <footer className="fixed inset-x-0 bottom-0 border-t border-line bg-white/95 px-3.5 py-2.5"
              style={{ paddingBottom: 'calc(.625rem + env(safe-area-inset-bottom))' }}>
        <div className="mx-auto flex max-w-[740px] gap-2.5">
          {q.answerKey ? (
            /* Máy đã chấm rồi thì không hỏi lại bé đúng hay sai — chỉ đi tiếp.
               Chưa trả lời thì nút nhắc đúng việc đang phải làm. */
            <button className="btn-go" disabled={!res}
                    onClick={() => { setRes(null); setI(i + 1); }}>
              {res ? 'Câu tiếp ▶' : 'Con trả lời rồi bấm Kiểm tra'}
            </button>
          ) : !shown ? (
            <button className="btn-go" onClick={() => setShown(true)}>Con làm xong — xem lời giải</button>
          ) : (
            <>
              <button className="btn-ghost"
                onClick={() => { setMarks((m) => ({ ...m, [q.qno]: false })); setShown(false); setI(i + 1); }}>
                Mình làm sai
              </button>
              <button className="btn-go"
                onClick={() => { setMarks((m) => ({ ...m, [q.qno]: true })); setShown(false); setI(i + 1); }}>
                Mình làm đúng ✓
              </button>
            </>
          )}
        </div>
      </footer>
    </div>
  );
}
