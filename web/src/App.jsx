import React, { useCallback, useEffect, useMemo, useState } from 'react';
import LoginScreen from './chung/components/LoginScreen.jsx';
import ProfileSetup from './chung/components/ProfileSetup.jsx';
import TeacherBoard from './chung/components/TeacherBoard.jsx';
import BangNguong from './chung/components/BangNguong.jsx';
import DuyetDeXuat from './chung/components/DuyetDeXuat.jsx';
import KeSach from './chung/components/KeSach.jsx';
import BangXepHang from './chung/components/BangXepHang.jsx';
import ParentReport from './chung/components/ParentReport.jsx';
import { napSoDangKy, soDangKy } from './chung/lib/soQuyen.js';
import { datNguCanh } from './chung/lib/nguong.js';
import { hasFirebase, dungGiaLap, choHienTai } from './chung/lib/nenTang.js';
import ChonNguoi from './chung/components/ChonNguoi.jsx';
import HoSoCon from './chung/components/HoSoCon.jsx';
import {
  dsNguoi, ghiNguoi, xoaNguoi, doiCho, choTrong, dangThemBe,
} from './chung/lib/nguoiDung.js';
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

/**
 * Vừa bấm "Thêm bé khác" hay chưa? Đọc ở TẦNG MODULE, cố ý — `dangThemBe()` đọc xong
 * là xoá dấu, mà `<React.StrictMode>` gọi hàm khởi tạo state HAI LẦN: lần đầu đọc
 * được và xoá, lần hai đọc ra rỗng, thế là app lại hỏi "ai đang học" và nút "Thêm bé
 * khác" quay về đúng màn vừa bấm. Module thì chỉ nạp một lần.
 */
const VUA_THEM_BE = dangThemBe();

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

  /**
   * ── NGỮ CẢNH PHIÊN CHO BỘ NGƯỠNG (R7 · mục 3.8.1) ──
   *
   * θ và ba tham số BKT có thể khác nhau giữa hai môn và giữa các khối lớp. Mọi chỗ
   * gọi `layNguong` đọc ngữ cảnh này, nên nó phải luôn khớp với quyển bé đang mở.
   *
   * ⚠ SUY TỪ TRẠNG THÁI, KHÔNG GÁN TAY Ở CHỖ GỌI. Tôi viết bản đầu đặt ngữ cảnh
   * ngay trong `chonQuyen` — và đó là một trong BỐN đường đổi quyển: `veKeSach` về
   * kệ sách, `moCuaPhu` vào môn mà không qua quyển, nhánh `loai: 'giai'` mở mùa
   * giải. Ba đường kia sẽ để ngữ cảnh của quyển TRƯỚC nằm lại, và hậu quả thì câm:
   * bé lớp 3 làm bài vẫn được chấm bằng θ của lớp 5, không màn nào đổi màu, không
   * cổng nào đỏ — chỉ mức thạo trong học bạ sai. Ngữ cảnh là HÀM của `mon` và
   * `quyen`, nên chỗ đúng để đặt nó là nơi hai thứ ấy đã suy xong.
   *
   * `khoiLop` lấy từ SỔ ĐĂNG KÝ (`ct.lop`), không bóc từ tên quyển: tên quyển là
   * chuỗi hiển thị, sổ đăng ký là nơi duy nhất khai lớp (xem `soQuyen.js`).
   */
  useEffect(() => {
    const ct = quyen ? dangKy?.chuongTrinh?.[quyen] : null;
    datNguCanh({ mon: mon?.ma ?? monMa ?? null, khoiLop: ct?.lop ?? null });
  }, [mon, monMa, quyen, dangKy]);

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
      myProfile(user.uid).then((h) => {
        setProfile(h);
        /* Ghi tên con vào SỔ CỦA MÁY để lần sau mở lên còn biết mà hỏi "ai đang học".
           Ghi cả khi hồ sơ chưa có gì — ít nhất còn cái email để nhận ra nhau. */
        ghiNguoi({
          cho: choHienTai, uid: user.uid, email: user.email,
          ten: h?.displayName || '', bietDanh: h?.bietDanh || '', lop: h?.grade || 0,
        });
      }).catch(() => setProfile(null));
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
    /* Bé thoát hẳn thì bỏ luôn tên khỏi sổ của máy — để nguyên thì màn "Ai đang học"
       vẫn hiện tên ấy, bấm vào lại rơi ra màn nhập mã, trông như hỏng. */
    xoaNguoi(choHienTai);
    try { localStorage.removeItem(SKIP_KEY); } catch { /* chế độ riêng tư */ }
    setSkipped(false);
    setView({ page: 'home' });
  };

  /* ── Nhiều bé chung một máy ──
     `dsNguoi()` là sổ của MÁY (localStorage), không phải state — nên đọc thẳng mỗi
     lần vẽ. Nó chỉ đổi khi đăng nhập/thoát, mà hai việc ấy đều kéo theo vẽ lại. */
  const dsBe = dsNguoi();
  const beKhac = dsBe.filter((n) => n.cho !== choHienTai);
  /* Chưa vào được chỗ này, mà máy còn nhớ bé khác → hỏi "ai đang học" thay vì đẩy
     thẳng ra màn nhập mã. Bé kia vẫn còn phiên nên bấm tên là vào học ngay. */
  const [hoiChonNguoi, setHoiChonNguoi] = useState(!VUA_THEM_BE);
  const themNguoiMoi = () => doiCho(choTrong(), { moi: true });

  const account = {
    signedIn: !!auth,
    name: profile?.displayName || auth?.email || '',
    lop: profile?.grade || 0,
    email: auth?.email || '',
    soNguoi: dsBe.length,
    onSignIn: () => { try { localStorage.removeItem(SKIP_KEY); } catch { /* bỏ qua */ } setSkipped(false); },
    onSignOut: signOut,
    onHoSo: () => setView({ page: 'hoso' }),
    available: hasFirebase && !LOCAL_KHONG_DANG_NHAP,
  };

  /* ── Các màn trước khi vào học ── */
  if (auth === undefined) {
    return <div className="flex min-h-[100dvh] items-center justify-center text-mute">Đang mở…</div>;
  }

  /* AI ĐANG HỌC? — chỗ này chưa có ai vào, nhưng máy còn nhớ bé khác.
     Đặt TRƯỚC màn đăng nhập: nhà có hai bé thì việc thường ngày là "chọn bé", không
     phải "gõ email". Bé nào cũng còn phiên riêng nên bấm tên là vào thẳng. */
  if (hasFirebase && !LOCAL_KHONG_DANG_NHAP && !auth && !skipped
      && beKhac.length > 0 && hoiChonNguoi) {
    return (
      <ChonNguoi
        onChon={(n) => doiCho(n.cho)}
        /* Cấp một chỗ TRỐNG cho bé mới, đừng đăng nhập đè lên chỗ đang mở: chỗ ấy có
           thể là của bé cũ vừa mất phiên, đè lên là bé cũ biến khỏi danh sách. */
        onThemNguoi={themNguoiMoi}
        onQuenNguoi={(n) => { xoaNguoi(n.cho); setHoiChonNguoi(dsNguoi().length > 0); }}
      />
    );
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
  /* ── CHUYÊN GIA CHƯƠNG TRÌNH (R7, mục 3.8.4) ──
     Vai trò thứ tư, tách hẳn khỏi `admin`: người hiểu việc DẠY HỌC quyết định
     ngưỡng. Đặt TRƯỚC nhánh giáo viên vì một tài khoản chỉ mang một vai. */
  if (auth && role === 'chuyengia') {
    /* Hai màn, và chúng trả lời hai câu KHÁC NHAU: màn ngưỡng hỏi «có đổi hệ thống
       bây giờ không» (phát hành một phiên bản), màn đề xuất hỏi «con số máy học ra
       có đáng tin không». Gộp làm một là bấm duyệt xong tưởng đã đổi được gì. */
    if (view.page === 'dexuat') {
      return <DuyetDeXuat onExit={() => setView({ page: 'home' })} />;
    }
    return (
      <BangNguong onExit={signOut} onXemDeXuat={() => setView({ page: 'dexuat' })} />
    );
  }

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
        onSave={async (d) => {
          await saveProfile(auth.uid, d);
          setProfile({ ...profile, ...d, profileComplete: true });
          ghiNguoi({ cho: choHienTai, uid: auth.uid, email: auth.email,
                     ten: d.displayName, lop: d.grade });
        }}
        onSkip={() => setProfile({ ...profile, profileComplete: true })}
      />
    );
  }

  /* ══ ĐỔI BÉ ══ — mở từ hồ sơ, khi đang đăng nhập sẵn */
  if (view.page === 'chonnguoi')
    return (
      <ChonNguoi
        onChon={(n) => (n.cho === choHienTai
          ? setView({ page: 'home' })      // chọn lại chính mình thì chỉ việc quay ra
          : doiCho(n.cho))}
        onThemNguoi={themNguoiMoi}
        onQuenNguoi={(n) => { xoaNguoi(n.cho); setView({ page: 'hoso' }); }}
      />
    );

  /* ══ HỒ SƠ CỦA CON ══ — đang là ai, và sửa lại tên · lớp · biệt danh */
  if (view.page === 'hoso' && auth)
    return (
      <HoSoCon
        hoSo={profile}
        email={auth.email}
        onLuu={async (d) => {
          await saveProfile(auth.uid, d);
          setProfile((h) => ({ ...(h || {}), ...d, profileComplete: true }));
          /* Sổ của máy phải đổi theo, nếu không màn "Ai đang học" còn gọi tên cũ. */
          ghiNguoi({ cho: choHienTai, uid: auth.uid, email: auth.email,
                     ten: d.displayName, bietDanh: d.bietDanh, lop: d.grade });
        }}
        /* KHÔNG logout ở đây: thoát ra là mất phiên của bé này, lần sau bé quay lại
           phải nhập mã. Đổi bé chỉ là mở chỗ khác — phiên của cả hai đều còn nguyên. */
        onDoiNguoi={() => setView({ page: 'chonnguoi' })}
        onSignOut={signOut}
        onExit={() => setView({ page: 'home' })}
      />
    );

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
      /* HỒ SƠ CON — môn cần TÊN THẬT để gọi bé trong bài nói và trong hội thoại.
         Thiếu dòng này thì `hoSo` luôn rỗng, và cái tên dự phòng viết trong màn
         hình hoá ra là tên DUY NHẤT: mọi bé đều bị gọi là "Bo". Đã dính thật —
         bác đổi tên thành "Nguyễn Minh An" mà cô vẫn chào "Bo". */
      hoSo={profile}
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
