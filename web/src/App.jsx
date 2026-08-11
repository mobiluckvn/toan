import React, { useCallback, useEffect, useMemo, useState } from 'react';
import LoginScreen from './chung/components/LoginScreen.jsx';
import ProfileSetup from './chung/components/ProfileSetup.jsx';
import TeacherBoard from './chung/components/TeacherBoard.jsx';
import KeSach from './chung/components/KeSach.jsx';
import BangXepHang from './chung/components/BangXepHang.jsx';
import ParentReport from './chung/components/ParentReport.jsx';
import { napSoDangKy, soDangKy } from './chung/lib/soQuyen.js';
import { hasFirebase, dungGiaLap } from './chung/lib/nenTang.js';
import { gopTienDoMon } from './chung/lib/soTienDo.js';
import { watchAuth, myRole, myProfile, saveProfile, logout } from './chung/lib/taiKhoan.js';
import { MON, monCua } from './soMon.js';

const SKIP_KEY = 'ttd5.skipLogin.v1';

/**
 * VỎ APP — đăng nhập, hồ sơ, kệ sách, và bốn màn nhìn nhiều môn một lượt.
 *
 * ── VỎ KHÔNG BIẾT GÌ VỀ RUỘT TỪNG MÔN ──
 * Tệp này không import một dòng nào từ `mon/toan/**` hay `mon/tienganh/**`; nó chỉ
 * biết `src/soMon.js` và giao ước ghi ở đó. Mỗi môn nộp một component `Man` rồi tự lo
 * mọi đường đi bên trong.
 *
 * Nhờ vậy: thêm môn thứ hai không sửa một dòng nào ở đây, và sửa môn này không thể
 * làm sai môn kia. Cổng `ranh_gioi.test.mjs` biến điều đó thành hàng rào máy gác chứ
 * không phải một lời hứa.
 *
 * `tienDo` của mỗi môn thì vỏ GIỮ (để kệ sách và sổ bố mẹ cùng vẽ lại khi con học
 * xong một bài) nhưng KHÔNG BAO GIỜ soi vào bên trong — với vỏ nó là một khối đục.
 */

/**
 * CHẠY LOCAL THÌ KHÔNG HỎI ĐĂNG NHẬP.
 *
 * import.meta.env.DEV do Vite đặt: true khi `npm run dev`, false khi `npm run build`.
 * Nghĩa là cờ này KHÔNG THỂ lọt sang bản đưa lên mạng — không phải nhớ tắt bằng tay,
 * cũng không phụ thuộc vào một biến môi trường ai đó có thể quên xoá.
 *
 * NGOẠI TRỪ khi chạy trên bộ giả lập. Cờ này tiện, nhưng nó tiện đến mức che mất
 * hẳn màn đăng nhập: chạy `npm run dev` thì KHÔNG CÁCH NÀO đi thử được đăng nhập ·
 * hồ sơ lần đầu · bảng xếp hạng · bảng cô giáo — bốn màn ấy chưa từng được soi bằng
 * mắt, chỉ vì cửa vào chúng không bao giờ mở ra ở local.
 *
 * Bật giả lập là nói rõ "tôi đang đi thử phần tài khoản", nên trả màn đăng nhập lại.
 * Dữ liệu vẫn nằm trọn trong máy — xem `chung/lib/nenTang.js`.
 */
const LOCAL_KHONG_DANG_NHAP = !!import.meta.env?.DEV && !dungGiaLap;

export default function App() {
  const [view, setView] = useState({ page: 'home' });

  /* ── Đăng nhập ──
     auth: undefined = đang hỏi máy chủ · null = chưa đăng nhập · object = đã vào */
  const [auth, setAuth] = useState(hasFirebase && !LOCAL_KHONG_DANG_NHAP ? undefined : null);
  const [role, setRole] = useState(null);
  const [profile, setProfile] = useState(null);
  const [skipped, setSkipped] = useState(() => {
    try { return localStorage.getItem(SKIP_KEY) === '1'; } catch { return false; }
  });

  /* Sổ tiến độ của TỪNG MÔN, khoá theo mã môn. Vỏ giữ để mọi màn cùng vẽ lại; hình
     dạng bên trong là chuyện riêng của môn. */
  const [tienDo, setTienDo] = useState(
    () => Object.fromEntries(MON.map((m) => [m.ma, m.napTienDo()])));
  /* `gopTienDoMon` giữ nguyên khối cũ khi môn báo "không có gì đổi" — đọc lời giải
     thích ở `chung/lib/soTienDo.js` trước khi định viết gọn lại thành một dòng. */
  const datTienDoCua = useCallback(
    (ma) => (f) => setTienDo((t) => gopTienDoMon(t, ma, f)), []);
  useEffect(() => { for (const m of MON) m.luuTienDo(tienDo[m.ma]); }, [tienDo]);

  /* Quyển con đang mở. KHÔNG nhớ qua các lần mở app: kệ sách là trang chính, mở
     app ra con thấy mình học dở những gì rồi tự chọn — thay vì bị đưa thẳng vào
     một quyển và phải "đổi lớp" mới sang được quyển khác. */
  const [quyen, setQuyen] = useState(null);
  /* Môn đang mở. Thường suy ra từ quyển, nhưng CỬA PHỤ (vd "Học theo chủ đề") vào
     được môn mà không qua quyển nào — nên phải giữ riêng. */
  const [monMa, setMonMa] = useState(null);
  const veKeSach = useCallback(() => {
    setQuyen(null); setMonMa(null); setView({ page: 'home' });
  }, []);

  /* Sổ đăng ký quyển — nơi duy nhất khai các lớp và môn. Giữ trong state chứ không
     chỉ gọi rồi thôi: nạp xong phải VẼ LẠI kệ sách, nếu không kệ sách chỉ thấy bản
     mặc định tối thiểu mà chẳng có gì báo là đang thiếu. */
  const [dangKy, setDangKy] = useState(() => soDangKy());
  useEffect(() => { napSoDangKy().then(setDangKy); }, []);

  /** Môn đang mở — suy từ sổ đăng ký, không đoán theo tên quyển. */
  const mon = useMemo(() => {
    if (monMa) return monCua(monMa);
    return quyen ? monCua(dangKy?.chuongTrinh?.[quyen]?.mon) : null;
  }, [monMa, quyen, dangKy]);

  const chonQuyen = useCallback((ma) => {
    /* Chương trình `loai: 'giai'` không phải chuỗi bài học tuần tự mà là mùa giải —
       mở thẳng vào bảng đấu, không đi qua trang chính của một quyển. */
    const ct = dangKy?.chuongTrinh?.[ma];
    if (ct?.loai === 'giai') { setQuyen(ct.choQuyen || ma); setView({ page: 'muagiai' }); return; }
    setQuyen(ma); setMonMa(ct?.mon || null); setView({ page: 'home' });
  }, [dangKy]);

  /** Cửa phụ: vào thẳng một màn của môn, không qua quyển nào. */
  const moCuaPhu = useCallback((ma, trang) => {
    setMonMa(ma); setQuyen(null); setView({ page: trang });
  }, []);

  useEffect(() => {
    if (!hasFirebase || LOCAL_KHONG_DANG_NHAP) return undefined;
    return watchAuth(async (user) => {
      setAuth(user || null);
      if (!user) { setRole(null); setProfile(null); return; }
      const r = await myRole(user).catch(() => 'learner');
      setRole(r);
      if (r !== 'learner') return;
      myProfile(user.uid).then(setProfile).catch(() => setProfile(null));
      /* KÉO SỔ VỀ cho TỪNG MÔN. Con học ở máy tính bảng rồi mở máy của bố mẹ mà thấy
         trắng tinh thì tưởng mất bài — dữ liệu vẫn còn nguyên, chỉ là màn hình không
         hỏi. Gộp chứ không đè: hai máy có thể đang học dở hai bài khác nhau. */
      for (const m of MON) {
        /* SANG TÊN trước, kéo sổ sau — và phải xong trước khi con kịp học câu tiếp.
           Bài con làm lúc chưa đăng nhập mang mã tạm; để nguyên là luật bảo mật từ
           chối cả lô ghi, im lặng, vĩnh viễn. Xem `dangNhapXong` ở cửa của môn. */
        try { m.dangNhapXong?.(user.uid); } catch { /* môn không cần dọn thì thôi */ }
        m.napTuMay(user.uid)
          .then((may) => datTienDoCua(m.ma)((p) => m.gopTienDo({ ...p, learnerId: user.uid }, may)))
          .catch(() => datTienDoCua(m.ma)((p) => ({ ...p, learnerId: user.uid })));
      }
    });
  }, [datTienDoCua]);

  const learnerId = tienDo[MON[0].ma]?.learnerId || 'local';

  const signOut = async () => {
    await logout().catch(() => {});
    try { localStorage.removeItem(SKIP_KEY); } catch { /* chế độ riêng tư */ }
    setSkipped(false);
    setView({ page: 'home' });
  };

  const account = {
    signedIn: !!auth,
    name: profile?.displayName || auth?.email || '',
    onSignIn: () => { try { localStorage.removeItem(SKIP_KEY); } catch { /* bỏ qua */ } setSkipped(false); },
    onSignOut: signOut,
    available: hasFirebase && !LOCAL_KHONG_DANG_NHAP,
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
    return <TeacherBoard mon={MON} onExit={signOut} />;
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

  /* ══ SỔ BỐ MẸ ══ — nhìn MỌI môn một lượt, mỗi môn một tab */
  if (view.page === 'report')
    return (
      <ParentReport
        mon={MON}
        tienDo={tienDo}
        learnerId={learnerId}
        onExit={() => setView(view.veLai || { page: 'home' })}
        onVeNha={veKeSach}
      />
    );

  /* ══ BẢNG XẾP HẠNG ══
     Đặt TRƯỚC nhánh kệ sách: bảng không thuộc quyển nào mà vào được từ CẢ HAI nơi
     (kệ sách và trang quyển). Đứng sau `!quyen` là bấm từ kệ sách sẽ bị nuốt mất —
     đúng cái bẫy đã dính hai lần. */
  if (view.page === 'xephang')
    return (
      <BangXepHang
        mon={MON}
        maCon={learnerId}
        hoSo={profile}
        onExit={() => setView(view.veLai || { page: 'home' })}
        onVeNha={veKeSach}
        /* Con đổi biệt danh hay đổi bạn đang đuổi thì hồ sơ trong bộ nhớ phải đổi
           theo — không thì thoát ra vào lại là thấy giá trị cũ, tưởng không lưu được. */
        onLuuHoSo={(v) => setProfile((h) => ({ ...(h || {}), ...v }))}
      />
    );

  /* ══ KỆ SÁCH — trang chính ══ */
  if (!mon?.Man || (!quyen && view.page === 'home'))
    return (
      <KeSach
        dangKy={dangKy}
        mon={MON}
        tienDo={tienDo}
        onMoQuyen={chonQuyen}
        onMoCuaPhu={moCuaPhu}
        onMoXepHang={() => setView({ page: 'xephang' })}
        onSoPhuHuynh={() => setView({ page: 'report' })}
        account={account}
      />
    );

  /* ══ GIAO CHO MÔN ══
     Từ đây trở đi vỏ không biết gì nữa: môn tự dựng mọi màn của mình. */
  const Man = mon.Man;
  return (
    <Man
      tienDo={tienDo[mon.ma]}
      datTienDo={datTienDoCua(mon.ma)}
      quyen={quyen}
      learnerId={learnerId}
      /* Bậc xuất phát lấy theo lớp con khai lúc lập hồ sơ. Chưa khai thì lấy 5 —
         quyển đầy đủ nhất — và vòng luyện tự lùi nếu con chưa với tới. */
      lopCon={profile?.grade || 5}
      account={account}
      view={view}
      setView={setView}
      veKeSach={veKeSach}
      onSoPhuHuynh={() => setView({ page: 'report', veLai: { page: 'home' } })}
      onMoXepHang={() => setView({ page: 'xephang', veLai: { page: 'home' } })}
    />
  );
}
