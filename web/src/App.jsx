import React, { useCallback, useEffect, useState } from 'react';
import Home from './components/Home.jsx';
import LessonPlayer from './components/LessonPlayer.jsx';
import ExamPlayer from './components/ExamPlayer.jsx';
import ParentReport from './components/ParentReport.jsx';
import LoginScreen from './components/LoginScreen.jsx';
import ProfileSetup from './components/ProfileSetup.jsx';
import TeacherBoard from './components/TeacherBoard.jsx';
import {
  loadProgress, saveProgress, recordMicro, recordChapter, saveSpot, resumeSpot, setMode,
} from './lib/progress.js';
import { neighborIds } from './lib/content.js';
import {
  submitSession, pushAttempts, syncPending, hasFirebase, watchAuth, myRole, myProfile, saveProfile, refreshMyReport,
  myReport, logout,
} from './lib/firebase.js';
import { reassignQueue } from './lib/sync.js';

const SKIP_KEY = 'ttd5.skipLogin.v1';

/**
 * CHẠY LOCAL THÌ KHÔNG HỎI ĐĂNG NHẬP.
 *
 * import.meta.env.DEV do Vite đặt: true khi `npm run dev`, false khi `npm run build`.
 * Nghĩa là cờ này KHÔNG THỂ lọt sang bản đưa lên mạng — không phải nhớ tắt bằng tay,
 * cũng không phụ thuộc vào một biến môi trường ai đó có thể quên xoá.
 */
const LOCAL_KHONG_DANG_NHAP = !!import.meta.env?.DEV;

export default function App() {
  const [progress, setProgress] = useState(() => loadProgress());
  const [view, setView] = useState({ page: 'home' });

  /* ── Đăng nhập ──
     auth: undefined = đang hỏi máy chủ · null = chưa đăng nhập · object = đã vào */
  const [auth, setAuth] = useState(hasFirebase && !LOCAL_KHONG_DANG_NHAP ? undefined : null);
  const [role, setRole] = useState(null);
  const [profile, setProfile] = useState(null);
  const [cloudReport, setCloudReport] = useState(null);
  const [skipped, setSkipped] = useState(() => {
    try { return localStorage.getItem(SKIP_KEY) === '1'; } catch { return false; }
  });

  useEffect(() => { saveProgress(progress); }, [progress]);

  useEffect(() => {
    if (!hasFirebase || LOCAL_KHONG_DANG_NHAP) return undefined;
    return watchAuth(async (user) => {
      setAuth(user || null);
      if (!user) { setRole(null); setProfile(null); setCloudReport(null); return; }
      const r = await myRole(user).catch(() => 'learner');
      setRole(r);
      if (r === 'learner') {
        // Bài học lúc chưa đăng nhập mang mã tạm 'local' — sang tên rồi mới đẩy được,
        // nếu không luật bảo mật từ chối trong im lặng và công học của con bay sạch.
        reassignQueue(user.uid);
        setProgress((p) => ({ ...p, learnerId: user.uid }));
        syncPending().catch(() => {});
        myProfile(user.uid).then(setProfile).catch(() => setProfile(null));
        myReport(user.uid).then(setCloudReport).catch(() => {});
      }
    });
  }, []);

  // học không đăng nhập: vẫn xếp hàng đợi, gửi khi có tài khoản
  useEffect(() => { if (!hasFirebase) syncPending().catch(() => {}); }, []);

  const learnerId = progress.learnerId || 'local';

  const finishMicro = useCallback((microId, grade, lesson, session = {}) => {
    setProgress((p) => recordMicro(p, microId, grade));
    submitSession({
      learnerId, sessionId: session.sessionId, microId,
      bktUnit: session.bktUnit, events: session.events || [],
      tomTat: session.tomTat || session.events || [], grade,
    }).catch(() => {});                       // mất mạng: đã nằm trong hàng đợi, lần sau gửi
    const { next } = neighborIds(microId, lesson);
    setView(next && grade.pass ? { page: 'lesson', microId: next } : { page: 'home' });
  }, [learnerId]);

  const signOut = async () => {
    await logout().catch(() => {});
    try { localStorage.removeItem(SKIP_KEY); } catch { /* chế độ riêng tư */ }
    setSkipped(false);
    setView({ page: 'home' });
  };

  /* ── Các màn trước khi vào học ── */
  if (auth === undefined) {
    return <div className="flex min-h-[100dvh] items-center justify-center text-mute">Đang mở…</div>;
  }

  if (hasFirebase && !LOCAL_KHONG_DANG_NHAP && !auth && !skipped) {
    return (
      <LoginScreen
        onDone={() => { /* watchAuth lo phần còn lại */ }}
        onSkip={() => {
          try { localStorage.setItem(SKIP_KEY, '1'); } catch { /* bỏ qua */ }
          setSkipped(true);
        }}
      />
    );
  }

  // Giáo viên và quản trị không vào phòng học — họ chỉ xem kết quả
  if (auth && (role === 'teacher' || role === 'admin')) {
    return <TeacherBoard onExit={signOut} />;
  }

  // Lần đầu đăng nhập: hỏi tên con rồi cho vào ngay.
  // Dựa vào cờ profileComplete chứ KHÔNG dựa vào displayName — máy chủ luôn điền sẵn
  // tên tạm (phần trước @), nên xét theo tên thì màn này không bao giờ hiện.
  if (auth && role === 'learner' && profile && !profile.profileComplete) {
    return (
      <ProfileSetup
        email={auth.email}
        onSave={async (d) => { await saveProfile(auth.uid, d); setProfile({ ...profile, ...d, profileComplete: true }); }}
        onSkip={() => setProfile({ ...profile, profileComplete: true })}
      />
    );
  }

  /* ── Phòng học ── */
  if (view.page === 'lesson')
    return (
      <LessonPlayer
        microId={view.microId}
        resumeAt={view.fromStart ? 0 : (resumeSpot(progress, view.microId)?.step || 0)}
        onMoveStep={(id, step, total) => setProgress((p) => saveSpot(p, id, step, total))}
        /* Gửi dần trong lúc con học — bỏ dở giữa chừng vẫn giữ được bài đã làm */
        onEvents={(s) => pushAttempts({ learnerId, ...s }).catch(() => {})}
        onExit={() => setView({ page: 'home' })}
        onFinish={(grade, lesson, session) => finishMicro(view.microId, grade, lesson, session)}
      />
    );

  if (view.page === 'report')
    return (
      <ParentReport
        progress={progress}
        cloudReport={cloudReport}
        onRefresh={hasFirebase && learnerId !== 'local'
          ? async () => {
              await refreshMyReport(learnerId, 7);
              setCloudReport(await myReport(learnerId));
            }
          : null}
        onExit={() => setView({ page: 'home' })}
        onOpenMicro={(id) => setView({ page: 'lesson', microId: id })}
      />
    );

  if (view.page === 'exam')
    return (
      <ExamPlayer
        chapter={view.chapter}
        onExit={() => setView({ page: 'home' })}
        onOpenMicro={(id) => setView({ page: 'lesson', microId: id })}
        onDone={(g) => { setProgress((p) => recordChapter(p, view.chapter, g)); setView({ page: 'home' }); }}
      />
    );

  return (
    <Home
      progress={progress}
      account={{
        signedIn: !!auth,
        name: profile?.displayName || auth?.email || '',
        onSignIn: () => { try { localStorage.removeItem(SKIP_KEY); } catch { /* bỏ qua */ } setSkipped(false); },
        onSignOut: signOut,
        available: hasFirebase && !LOCAL_KHONG_DANG_NHAP,
      }}
      onOpenMicro={(id, opts) => setView({ page: 'lesson', microId: id, fromStart: !!opts?.fromStart })}
      onSetMode={(m) => setProgress((p) => setMode(p, m))}
      onOpenExam={(c) => setView({ page: 'exam', chapter: c })}
      onOpenReport={() => setView({ page: 'report' })}
    />
  );
}
