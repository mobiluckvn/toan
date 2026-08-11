import React, { useEffect, useMemo, useState } from 'react';
import Chu from './Chu.jsx';
import { buildFlow, PHASES } from '../lib/flow.js';
import { loadLesson, figureSrc, chapterOf, cachDoc } from '../lib/content.js';
import { gradeMicro } from '../lib/flow.js';
import { newSessionId } from '../lib/sync.js';
import StepView from './StepView.jsx';
import CuonThem from './CuonThem.jsx';
import TienTrinh from './TienTrinh.jsx';

/** Thanh chặng: MỞ BÀI · GIẢNG · BÀI MẪU · LUYỆN TẬP · SÁT HẠCH */
function PhaseBar({ current }) {
  return (
    <div className="sticky top-[47px] z-10 flex justify-center gap-1.5 bg-white border-b border-line px-3 py-1.5">
      {PHASES.map((p) => (
        <span key={p.id}
          className={`text-[10.5px] font-extrabold tracking-wide rounded-full px-2.5 py-1 ${
            p.id === current ? 'bg-navy text-white' : 'bg-[#F2F6FA] text-mute'}`}>
          {p.label}
        </span>
      ))}
    </div>
  );
}

export default function LessonPlayer({ microId, onFinish, onExit, resumeAt = 0, onMoveStep, onEvents, onMoBai }) {
  const [lesson, setLesson] = useState(null);
  const [err, setErr] = useState(null);
  const [i, setI] = useState(0);
  const [log, setLog] = useState({ practice: [], assess: [], raw: [] });
  const [sessionId] = useState(() => newSessionId());
  const [t0] = useState(() => Date.now());
  const [resumed, setResumed] = useState(false);
  /* Bước XA NHẤT con từng tới. Quay lại xem bài cũ thì không được kéo mốc này lùi,
     nếu không con lùi một bước là mất quyền đi tiếp tới chỗ vừa nãy. */
  const [xaNhat, setXaNhat] = useState(0);

  useEffect(() => {
    let alive = true;
    setLesson(null); setErr(null); setI(0); setLog({ practice: [], assess: [], raw: [] });
    setResumed(false); setXaNhat(0);
    loadLesson(microId).then((d) => alive && setLesson(d)).catch((e) => alive && setErr(e.message));
    return () => { alive = false; };
  }, [microId]);

  const flow = useMemo(() => (lesson ? buildFlow(lesson) : []), [lesson]);

  // Về đúng chỗ con bỏ dở. Chỉ nhảy MỘT lần, ngay khi bài vừa nạp xong — nhảy lại
  // giữa chừng thì con đang đọc dở lại bị đá đi chỗ khác.
  useEffect(() => {
    if (!flow.length || resumed) return;
    setResumed(true);
    if (resumeAt > 0) setI(Math.min(resumeAt, flow.length - 1));
  }, [flow.length, resumeAt, resumed]);

  const step = flow[i];

  useEffect(() => { window.scrollTo(0, 0); }, [i]);
  useEffect(() => { setXaNhat((x) => Math.max(x, i)); }, [i]);

  /**
   * Đẩy nhật ký lên máy chủ NGAY sau mỗi lượt trả lời, không đợi con học hết bài.
   * Bỏ dở giữa chừng là chuyện thường ngày (mẹ gọi ăn cơm, hết pin) — đợi tới màn
   * kết bài mới gửi thì công học của con bay mất, mà cô giáo cũng không thấy gì
   * cho đến khi con làm xong.
   */
  const soLuot = log.raw.length;
  useEffect(() => {
    if (!soLuot || !lesson) return;
    onEvents?.({ sessionId, microId, bktUnit: lesson.skills?.bktUnit || null, events: log.raw });
    // chỉ theo SỐ LƯỢT: log.raw là mảng mới mỗi lần dựng lại, để nguyên sẽ chạy vô hạn
  }, [soLuot]);   // eslint-disable-line react-hooks/exhaustive-deps
  /**
   * Ghi chỗ để lần sau mở lại: dùng bước XA NHẤT, không dùng bước đang đứng.
   * Con lùi về xem lại phần 2 rồi tắt máy — nhớ theo chỗ đang đứng thì lần sau
   * phải bấm lại từ đầu quãng đã học. Muốn xem lại thì lùi tiếp, dễ hơn nhiều.
   */
  useEffect(() => { if (resumed && flow.length) onMoveStep?.(microId, xaNhat, flow.length); },
            [xaNhat, resumed, flow.length, microId, onMoveStep]);

  if (err) return <div className="p-6 text-alert">{err}</div>;
  if (!lesson) return <div className="p-6 text-mute">Đang mở bài học…</div>;

  const go = (d = 1) => setI((x) => Math.max(0, Math.min(flow.length - 1, x + d)));
  /**
   * Ghi một lượt bấm "Kiểm tra".
   *
   * Hai sổ khác nhau, đừng gộp:
   *   · L[kind]  — sổ TÓM TẮT, mỗi câu một dòng (dòng sau đè dòng trước). Chấm bài
   *                dựa vào sổ này, nên nó phải giữ nguyên hình dạng cũ.
   *   · L.raw    — sổ THÔ, ghi nối đuôi MỌI lượt bấm. Đây là thứ đẩy lên máy chủ:
   *                con sai hai lần rồi mới đúng thì cô thấy đủ ba lượt.
   *
   * Trước đây chỉ ghi 'practice' và 'assess', bỏ trắng 'check' (chốt nhanh) và
   * 'worked' (câu xen giữa ví dụ) — mất 513/1654 câu, tức 31% số câu con thực làm.
   */
  const record = (kind, entry) =>
    setLog((L) => {
      const day = { ...entry, phase: kind, itemId: entry.id };
      const tomTat = L[kind] ? { ...L, [kind]: [...L[kind].filter((e) => e.id !== entry.id), day] } : L;
      return { ...tomTat, raw: [...(L.raw || []), { ...day, khiNao: Date.now(), at: Date.now() - t0 }] };
    });
  const jumpTo = (type) => {
    const k = flow.findIndex((s) => s.type === type);
    if (k >= 0) setI(k);
  };

  return (
    <div className={`flex flex-col min-h-[100dvh]${cachDoc(microId).chuTo ? ' doc-to' : ''}`}>
      <header className="sticky top-0 z-20 flex items-center gap-2.5 bg-navy px-3.5 py-2 text-white">
        {/* Nói rõ đây là THOÁT khỏi bài. Trước chỉ có mũi tên ← nên con bấm vào
            tưởng lùi một bước, hoá ra ra thẳng trang chủ. */}
        <button onClick={onExit} aria-label="Thoát khỏi bài học"
                className="rounded-full border border-white/40 px-2 py-0.5 text-[11px] font-bold leading-none">
          ⌂ Thoát
        </button>
        <span className="rounded bg-gold px-1.5 py-0.5 text-[11px] font-extrabold text-gold-dark">
          {microId.replace(/^DL:(KSN5Q1|KSN2)\./, '')}
        </span>
        <h1 className="flex-1 text-[13px] font-semibold leading-tight line-clamp-2">
          <Chu t={lesson.title} />
        </h1>
        <span className="text-[11px] tabular-nums opacity-85">{i + 1}/{flow.length}</span>
      </header>

      {/* Mỗi bước một đốt, bấm được để quay lại — thay cho vạch gradient cũ vốn
          chỉ cho biết "được khoảng một nửa" mà không nói nửa của mấy phần. */}
      <TienTrinh
        tong={flow.length} hienTai={i} daDi={xaNhat}
        nhan={flow.map((s2) => PHASES.find((p) => p.id === s2.phase)?.label || '')}
        onChon={(k) => setI(k)} onLui={() => go(-1)}
      />

      <PhaseBar current={step.phase} />

      <main className="mx-auto w-full max-w-[740px] flex-1 px-3.5 pb-32 pt-4">
        <StepView
          key={i}
          step={step} lesson={lesson} microId={microId}
          figureSrc={figureSrc} chapter={chapterOf(microId)}
          log={log} onRecord={record} onNext={() => go(1)} onJump={jumpTo}
          onMoBai={onMoBai}
          onFinish={() => onFinish?.(
            gradeMicro(log.assess, lesson.assessment?.passRule || ''),
            lesson,
            /* attempts đi từ sổ THÔ (mọi lượt bấm, đủ bốn chặng); tóm tắt tiến độ
               vẫn đi từ sổ tóm tắt để con số "làm đúng ngay lần đầu" không đổi nghĩa. */
            { sessionId, events: log.raw, tomTat: [...log.practice, ...log.assess],
              bktUnit: lesson.skills?.bktUnit || null })}
          onRestart={() => { setI(0); setLog({ practice: [], assess: [], raw: [] }); onMoveStep?.(microId, 0, flow.length); }}
        />
      </main>

      <CuonThem />
    </div>
  );
}
