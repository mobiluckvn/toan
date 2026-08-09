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
import { neighborIds, napSoDangKy, soDangKy, nhipDocCham, baiDocCham } from './lib/content.js';
import {
  submitSession, pushAttempts, syncPending, hasFirebase, watchAuth, myRole, myProfile, saveProfile, refreshMyReport,
  myReport, logout,
} from './lib/firebase.js';
import { reassignQueue } from './lib/sync.js';
import KeSach from './components/KeSach.jsx';
import HomeLop2 from './components/HomeLop2.jsx';
import MuaGiai from './components/MuaGiai.jsx';
import TraiHuanLuyen from './components/TraiHuanLuyen.jsx';
import HoSoBay from './components/HoSoBay.jsx';
import TheChienThuat from './components/TheChienThuat.jsx';
import DauLoader from './components/DauLoader.jsx';

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
  /* Quyển con đang mở. KHÔNG nhớ qua các lần mở app: kệ sách là trang chính, mở
     app ra con thấy mình học dở những gì rồi tự chọn — thay vì bị đưa thẳng vào
     một quyển và phải "đổi lớp" mới sang được quyển khác. */
  const [chuongTrinh, setChuongTrinh] = useState(null);
  const veKeSach = useCallback(() => { setChuongTrinh(null); setView({ page: 'home' }); }, []);
  const [skipped, setSkipped] = useState(() => {
    try { return localStorage.getItem(SKIP_KEY) === '1'; } catch { return false; }
  });

  useEffect(() => { saveProgress(progress); }, [progress]);

  /* Sổ đăng ký chương trình — nơi duy nhất khai các lớp và môn.
     Giữ trong state chứ không chỉ gọi rồi thôi: nạp xong phải VẼ LẠI kệ sách, nếu
     không kệ sách chỉ thấy bản mặc định tối thiểu (thiếu biểu tượng, thiếu mục
     "sắp có") mà chẳng có gì báo là đang thiếu. */
  const [dangKy, setDangKy] = useState(() => soDangKy());
  /* Chương trình `loai: 'giai'` không phải chuỗi bài học tuần tự mà là mùa giải —
     mở thẳng vào bảng đấu, không đi qua màn Home của một lớp. */
  const chonChuongTrinh = useCallback((ma) => {
    if (dangKy?.chuongTrinh?.[ma]?.loai === 'giai') {
      setChuongTrinh('lop5'); setView({ page: 'muagiai' });
      return;
    }
    setChuongTrinh(ma); setView({ page: 'home' });
  }, [dangKy]);
  useEffect(() => { napSoDangKy().then(setDangKy); }, []);

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
    if (!next || !grade.pass) { setView({ page: 'home' }); return; }
    // Hai nhịp đọc cùng LessonPlayer nhưng khác tên màn, nên phải hỏi bài thuộc
    // quyển nào — nếu không, học xong bài lớp 2 là nhảy sang bài lớp 5.
    setView(baiDocCham(next)
      ? { page: 'baiDocCham', baiId: next }
      : { page: 'lesson', microId: next });
  }, [learnerId]);

  /**
   * Lưu kết quả một vòng đấu Quyển 2.
   *
   * Ghi vào tiến độ tại máy để mở khoá vòng sau, ĐỒNG THỜI đẩy nhật ký lên máy chủ
   * bằng đúng đường của Quyển 1 — cô giáo xem một bảng thấy cả hai quyển, không
   * phải hai hệ thống rời. Mỗi câu một dòng, kèm con trả lời gì và bẫy nào đã sập.
   */
  const luuVongDau = useCallback((kq) => {
    setProgress((p) => ({
      ...p,
      dau: { ...(p.dau || {}), [kq.khoiId]: {
        dat: !!kq.dat, diemBarem: kq.diemBarem,
        soBaySap: (kq.microCanOn || []).length, at: new Date().toISOString(),
      } },
    }));
    const events = Object.entries(kq.ketQua || {}).map(([itemId, r]) => ({
      phase: 'assess', itemId,
      ok: r.ok ?? r.tuChamDung ?? false,
      answer: r.answer, mode: r.ok === undefined ? 'tuluan' : 'so',
      khiNao: Date.now(),
    }));
    pushAttempts({
      learnerId, sessionId: `dau_${kq.khoiId}`, microId: kq.khoiId,
      bktUnit: null, events,
    }).catch(() => {});
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
        chuongTrinh={chuongTrinh || 'lop5'}
        cloudReport={cloudReport}
        onRefresh={hasFirebase && learnerId !== 'local'
          ? async () => {
              await refreshMyReport(learnerId, 7);
              setCloudReport(await myReport(learnerId));
            }
          : null}
        onExit={() => setView({ page: 'home' })}
        onOpenMicro={(id) => setView(baiDocCham(id)
          ? { page: 'baiDocCham', baiId: id } : { page: 'lesson', microId: id })}
      />
    );

  if (view.page === 'exam')
    return (
      <ExamPlayer
        chapter={view.chapter}
        chuongTrinh={chuongTrinh || 'lop5'}
        onExit={() => setView({ page: 'home' })}
        onOpenMicro={(id) => setView(baiDocCham(id)
          ? { page: 'baiDocCham', baiId: id } : { page: 'lesson', microId: id })}
        onDone={(g) => { setProgress((p) => recordChapter(p, view.chapter, g)); setView({ page: 'home' }); }}
      />
    );

  /* ══ KỆ SÁCH — trang chính ══ */
  if (!chuongTrinh)
    return (
      <KeSach
        dangKy={dangKy}
        progress={progress}
        onMoChuongTrinh={chonChuongTrinh}
        onSoPhuHuynh={() => setView({ page: 'report' })}
        account={{ signedIn: !!auth, onSignOut: signOut }}
      />
    );

  /* ══ QUYỂN ĐỌC CHẬM (lớp 2, lớp 3) ══
     Cùng LessonPlayer với lớp 5 — dữ liệu đã đưa về chung một khuôn, nên bé cũng có
     nhật ký học, nhớ chỗ học dở, sổ phụ huynh và bảng cô giáo.

     Hỏi CỜ trong sổ đăng ký chứ không so tên quyển: thêm lớp 3 mà vẫn so 'lop2' thì
     bé lớp 3 rơi vào phòng học lớp 5 — chữ nhỏ, dồn nhiều khối một màn. */
  if (nhipDocCham(chuongTrinh)) {
    if (view.page === 'baiDocCham')
      return (
        <LessonPlayer
          /* `key` BẮT BUỘC: đổi bài mà không đổi key thì React giữ nguyên component
             cũ, nên số thứ tự màn ở trong nó KHÔNG reset — bấm "Học lại bài lớp 2"
             từ màn kết bài lớp 3 là rơi thẳng vào màn kết bài lớp 2 (24/24, điểm
             0/0), coi như chưa học đã xong. `resumeAt` chỉ là giá trị KHỞI TẠO nên
             không cứu được. */
          key={view.baiId}
          microId={view.baiId}
          resumeAt={view.fromStart ? 0 : (resumeSpot(progress, view.baiId)?.step || 0)}
          onMoveStep={(id, step, total) => setProgress((p) => saveSpot(p, id, step, total))}
          onEvents={(s) => pushAttempts({ learnerId, ...s }).catch(() => {})}
          onExit={() => setView({ page: 'home' })}
          onFinish={(grade, lesson, session) => finishMicro(view.baiId, grade, lesson, session)}
          /* Đường LÙI về quyển dưới: bài lớp 3 mở thẳng bài lớp 2 cùng chủ đề. Đích
             thuộc quyển khác nên phải hỏi lại nhịp đọc của CHÍNH nó — lớp 2 cũng đọc
             chậm nên vẫn cùng phòng học, nhưng đừng ghim cứng điều đó ở đây. */
          onMoBai={(id) => setView(baiDocCham(id)
            /* fromStart: đây là đi LÙI để luyện lại gốc, nên vào từ đầu bài — thả
               con vào giữa chỗ học dở của năm ngoái thì mất hẳn nghĩa "học lại". */
            ? { page: 'baiDocCham', baiId: id, fromStart: true }
            : { page: 'lesson', microId: id })}
        />
      );
    return (
      <HomeLop2
        progress={progress}
        chuongTrinh={chuongTrinh}
        onMoBai={(id) => setView({ page: 'baiDocCham', baiId: id })}
        onMoOnTap={(ch) => setView({ page: 'exam', chapter: ch })}
        onSoPhuHuynh={() => setView({ page: 'report' })}
        onDoiChuongTrinh={veKeSach}
      />
    );
  }

  /* ══ QUYỂN 2 · MÙA GIẢI ══ */
  if (view.page === 'muagiai')
    return (
      <MuaGiai
        progress={progress}
        onMo={(id) => setView({ page: 'dau', khoiId: id })}
        onTrai={() => setView({ page: 'trai' })}
        onHoSo={() => setView({ page: 'hosobay' })}
        onThe={() => setView({ page: 'the' })}
        onExit={() => setView({ page: 'home' })}
      />
    );

  if (view.page === 'trai')
    return <TraiHuanLuyen onExit={() => setView({ page: 'muagiai' })} />;

  if (view.page === 'hosobay')
    return <HoSoBay onExit={() => setView({ page: 'muagiai' })}
                    onMoMicro={(id) => setView({ page: 'lesson', microId: id })} />;

  if (view.page === 'the')
    return <TheChienThuat onExit={() => setView({ page: 'muagiai' })} />;

  if (view.page === 'dau')
    return (
      <DauLoader
        khoiId={view.khoiId}
        onExit={() => setView({ page: 'muagiai' })}
        onMoMicro={(id) => setView({ page: 'lesson', microId: id })}
        onXong={(kq) => { luuVongDau(kq); setView({ page: 'muagiai' }); }}
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
      onOpenMuaGiai={() => setView({ page: 'muagiai' })}
      onDoiChuongTrinh={veKeSach}
    />
  );
}
