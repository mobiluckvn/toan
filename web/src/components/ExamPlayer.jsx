import React, { useEffect, useState } from 'react';
import { CONTENT, dongDau } from '../lib/content.js';
import Figure from './Figure.jsx';

/**
 * Kỳ sát hạch chương: 15 câu tự-soi.
 * Đề trong dữ liệu là câu tự luận có lời giải mẫu → con TỰ CHẤM từng câu
 * (đúng tinh thần "bảng tự soi" của sách), sai câu nào thì mở đúng micro chẩn đoán.
 */
export default function ExamPlayer({ chapter, onDone, onOpenMicro, onExit,
                                    chuongTrinh = 'lop5' }) {
  const [doc, setDoc] = useState(null);
  const [i, setI] = useState(0);
  const [marks, setMarks] = useState({});     // qno → true/false
  const [shown, setShown] = useState(false);

  useEffect(() => {
    /* Hai chương trình cùng một màn sát hạch, chỉ khác tệp nội dung. */
    const ma = chuongTrinh === 'lop2' ? 'KSN2' : 'KSN5Q1';
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
                  {(q.diagnosesMicro || '').replace(/^DL:(KSN5Q1|KSN2)\./, '')} ▶
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

        {shown && (
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
          {!shown ? (
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
