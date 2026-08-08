import React, { useEffect, useMemo, useState } from 'react';
import { buildFlow, PHASES } from '../lib/flow.js';
import { loadLesson, figureSrc, chapterOf } from '../lib/content.js';
import { gradeMicro } from '../lib/flow.js';
import { newSessionId } from '../lib/sync.js';
import StepView from './StepView.jsx';
import CuonThem from './CuonThem.jsx';

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

export default function LessonPlayer({ microId, onFinish, onExit, resumeAt = 0, onMoveStep }) {
  const [lesson, setLesson] = useState(null);
  const [err, setErr] = useState(null);
  const [i, setI] = useState(0);
  const [log, setLog] = useState({ practice: [], assess: [] });
  const [sessionId] = useState(() => newSessionId());
  const [t0] = useState(() => Date.now());
  const [resumed, setResumed] = useState(false);

  useEffect(() => {
    let alive = true;
    setLesson(null); setErr(null); setI(0); setLog({ practice: [], assess: [] }); setResumed(false);
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
  useEffect(() => { if (resumed && flow.length) onMoveStep?.(microId, i, flow.length); },
            [i, resumed, flow.length, microId, onMoveStep]);

  if (err) return <div className="p-6 text-alert">{err}</div>;
  if (!lesson) return <div className="p-6 text-mute">Đang mở bài học…</div>;

  const go = (d = 1) => setI((x) => Math.max(0, Math.min(flow.length - 1, x + d)));
  const record = (kind, entry) =>
    setLog((L) => ({
      ...L,
      [kind]: [...L[kind].filter((e) => e.id !== entry.id),
               { ...entry, phase: kind, itemId: entry.id, ms: Date.now() - t0 }],
    }));
  const jumpTo = (type) => {
    const k = flow.findIndex((s) => s.type === type);
    if (k >= 0) setI(k);
  };

  return (
    <div className="flex flex-col min-h-[100dvh]">
      <header className="sticky top-0 z-20 flex items-center gap-2.5 bg-navy px-3.5 py-2 text-white">
        <button onClick={onExit} aria-label="Về trang chính" className="text-[15px] leading-none">←</button>
        <span className="rounded bg-gold px-1.5 py-0.5 text-[11px] font-extrabold text-gold-dark">
          {microId.replace('DL:KSN5Q1.', '')}
        </span>
        <h1 className="flex-1 text-[13px] font-semibold leading-tight line-clamp-2">
          {lesson.title}
        </h1>
        <span className="text-[11px] tabular-nums opacity-85">{i + 1}/{flow.length}</span>
      </header>

      <div className="h-[5px] bg-navy-deep">
        <i className="block h-full bg-gradient-to-r from-teal to-gold transition-[width] duration-500"
           style={{ width: `${Math.round((i / (flow.length - 1)) * 100)}%` }} />
      </div>

      <PhaseBar current={step.phase} />

      <main className="mx-auto w-full max-w-[740px] flex-1 px-3.5 pb-32 pt-4">
        <StepView
          key={i}
          step={step} lesson={lesson} microId={microId}
          figureSrc={figureSrc} chapter={chapterOf(microId)}
          log={log} onRecord={record} onNext={() => go(1)} onJump={jumpTo}
          onFinish={() => onFinish?.(
            gradeMicro(log.assess, lesson.assessment?.passRule || ''),
            lesson,
            { sessionId, events: [...log.practice, ...log.assess],
              bktUnit: lesson.skills?.bktUnit || null })}
          onRestart={() => { setI(0); setLog({ practice: [], assess: [] }); onMoveStep?.(microId, 0, flow.length); }}
        />
      </main>

      <CuonThem />
    </div>
  );
}
