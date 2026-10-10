import React, { useCallback } from 'react';
import HomeQuyen from './HomeQuyen.jsx';
import LessonPlayer from './LessonPlayer.jsx';
import ExamPlayer from './ExamPlayer.jsx';
import ChuDe from './ChuDe.jsx';
import LuyenChuDe from './LuyenChuDe.jsx';
import MuaGiai from './MuaGiai.jsx';
import TraiHuanLuyen from './TraiHuanLuyen.jsx';
import HoSoBay from './HoSoBay.jsx';
import TheChienThuat from './TheChienThuat.jsx';
import DauLoader from './DauLoader.jsx';
import {
  recordMicro, recordChapter, saveSpot, resumeSpot, setMode, ghiLuyenChuDe, khoaChuong, congGio,
} from '../lib/progress.js';
import { neighborIds, baiDocCham } from '../lib/noiDung.js';
import { submitSession, pushAttempts, luuMucHocBa } from '../lib/duLieu.js';
import { maNgay } from '../lib/dongHo.js';

/**
 * MÀN CỦA MÔN TOÁN — mọi đường đi bên trong môn, gói trọn trong MỘT cửa.
 *
 * Vỏ app (`src/App.jsx`) chỉ dựng component này rồi tránh ra: vỏ không biết Toán có
 * những màn nào, cũng không biết `tienDo` bên trong hình thù ra sao. Nhờ vậy thêm môn
 * thứ hai không phải sửa một dòng nào của vỏ, và sửa Toán không thể chạm sang môn kia.
 *
 * `tienDo`/`datTienDo` do VỎ giữ chứ không giữ ở đây — kệ sách và sổ bố mẹ cũng phải
 * vẽ lại khi con học xong một bài, mà hai màn ấy nằm ngoài môn. Với vỏ thì `tienDo`
 * chỉ là một khối đục: nó chuyền qua chuyền lại chứ không bao giờ soi vào bên trong.
 */
export default function ManToan({
  tienDo: progress, datTienDo: setProgress, quyen: chuongTrinh, learnerId, lopCon,
  account, view, setView, veKeSach, onSoPhuHuynh, onMoXepHang,
}) {
  const finishMicro = useCallback((microId, grade, lesson, session = {}, veLai = null) => {
    /* Ghi kết quả VÀ giờ học trong cùng một lần cập nhật: hai lần `setProgress` liên
       tiếp thì lần sau đọc phải sổ cũ, và số phút của lượt vừa rồi bay mất. */
    setProgress((p) => congGio(recordMicro(p, microId, grade), maNgay(), session.gio));
    submitSession({
      learnerId, sessionId: session.sessionId, microId,
      bktUnit: session.bktUnit, events: session.events || [],
      tomTat: session.tomTat || session.events || [], grade,
      /* Đồng hồ học do `LessonPlayer` chốt lúc nộp — xem `lib/dongHo.js`. Không có
         thì để null, `buildProgressDoc` phân biệt "chưa đo được" với "0 giây". */
      gio: session.gio || null,
    }).catch(() => {});                       // mất mạng: đã nằm trong hàng đợi, lần sau gửi
    /* Có chỗ để quay về thì về đó, ĐỪNG đi tiếp bài kế trong quyển. Con vào bài này
       từ màn chủ đề (hoặc từ vòng luyện chủ đề) nên bài kế của quyển là chuyện khác
       hẳn — đẩy con sang đó là làm mất mạch chủ đề đang theo. */
    if (veLai) { setView(veLai); return; }
    const { next } = neighborIds(microId, lesson);
    if (!next || !grade.pass) { setView({ page: 'home' }); return; }
    // Hai nhịp đọc cùng LessonPlayer nhưng khác tên màn, nên phải hỏi bài thuộc
    // quyển nào — nếu không, học xong bài lớp 2 là nhảy sang bài lớp 5.
    setView(baiDocCham(next)
      ? { page: 'baiDocCham', baiId: next }
      : { page: 'lesson', microId: next });
  }, [learnerId]);

  /* ── GHI HỌC BẠ: vừa vào sổ tại máy, vừa đẩy lên máy chủ ──
     Ba thứ dưới đây (kỳ sát hạch chương · bậc chủ đề · vòng đấu) trước nay chỉ nằm
     ở localStorage. Đổi máy là mất, và cô giáo thì không bao giờ thấy được con vững
     chủ đề nào — chỉ thấy con xong bài nào, một câu hỏi khác hẳn. */
  const ghiChuong = useCallback((ma, chuong, grade) => {
    const sau = recordChapter(progress, ma, chuong, grade);
    setProgress(sau);
    const k = khoaChuong(ma, chuong);
    luuMucHocBa(learnerId, 'chuong', k, { giaTri: sau.chapters[k] }).catch(() => {});
  }, [progress, learnerId]);

  const ghiChuDe = useCallback((maDang, lop, kq) => {
    const sau = ghiLuyenChuDe(progress, maDang, lop, kq);
    setProgress(sau);
    luuMucHocBa(learnerId, 'chuDe', maDang, { giaTri: sau.chuDe[maDang] }).catch(() => {});
  }, [progress, learnerId]);

  /**
   * Lưu kết quả một vòng đấu Quyển 2.
   *
   * Ghi vào tiến độ tại máy để mở khoá vòng sau, ĐỒNG THỜI đẩy nhật ký lên máy chủ
   * bằng đúng đường của Quyển 1 — cô giáo xem một bảng thấy cả hai quyển, không
   * phải hai hệ thống rời. Mỗi câu một dòng, kèm con trả lời gì và bẫy nào đã sập.
   */
  const luuVongDau = useCallback((kq) => {
    const vong = {
      dat: !!kq.dat, diemBarem: kq.diemBarem,
      soBaySap: (kq.microCanOn || []).length, at: new Date().toISOString(),
    };
    setProgress((p) => ({ ...p, dau: { ...(p.dau || {}), [kq.khoiId]: vong } }));
    luuMucHocBa(learnerId, 'dau', kq.khoiId, { giaTri: vong }).catch(() => {});
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

  /* ── Phòng học — MỘT khối cho cả hai nhịp đọc ──
     Trước đây có hai khối gần như trùng nhau: `lesson` (lớp 5) ở đây, `baiDocCham`
     (lớp 2·3·4) nằm bên trong nhánh `nhipDocCham(chuongTrinh)` phía dưới. Nhánh ấy
     đứng SAU `!chuongTrinh`, nên mở một bài lớp 3 từ màn chủ đề — nơi không có
     quyển nào đang mở — là rơi thẳng về kệ sách. Gộp lại thì mở bài từ đâu cũng
     vào đúng phòng học, và sửa khoảng cách một chỗ không còn làm lệch chỗ kia.

     Hai tên màn vẫn giữ: `neighborIds`, `duongLui` và sổ tiến trình đều đã quen
     hỏi `baiDocCham(id)` để biết bài thuộc nhịp nào. */
  if (view.page === 'lesson' || view.page === 'baiDocCham') {
    const baiId = view.microId || view.baiId;
    return (
      <LessonPlayer
        /* `key` BẮT BUỘC: đổi bài mà không đổi key thì React giữ nguyên component
           cũ, nên số thứ tự màn ở trong nó KHÔNG reset — bấm "Học lại bài lớp 2"
           từ màn kết bài lớp 3 là rơi thẳng vào màn kết bài lớp 2 (24/24, điểm
           0/0), coi như chưa học đã xong. `resumeAt` chỉ là giá trị KHỞI TẠO nên
           không cứu được. */
        key={baiId}
        microId={baiId}
        resumeAt={view.fromStart ? 0 : (resumeSpot(progress, baiId)?.step || 0)}
        onMoveStep={(id, step, total) => setProgress((p) => saveSpot(p, id, step, total))}
        /* Gửi dần trong lúc con học — bỏ dở giữa chừng vẫn giữ được bài đã làm */
        onEvents={(s) => pushAttempts({ learnerId, ...s }).catch(() => {})}
        onExit={() => setView(view.veLai || { page: 'home' })}
        onFinish={(grade, lesson, session) => finishMicro(baiId, grade, lesson, session,
                                                         view.veLai)}
        /* Thoát TỪ MÀN KẾT: ghi y như bấm "Micro tiếp theo", nhưng đi về đúng chỗ
           nút Thoát vẫn đưa tới, chứ không đẩy con sang bài kế. */
        onGhiRoiThoat={(grade, lesson, session) => finishMicro(
          baiId, grade, lesson, session, view.veLai || { page: 'home' })}
        /* Đường LÙI về quyển dưới. Đích thuộc quyển khác nên phải hỏi lại nhịp đọc
           của CHÍNH nó, đừng ghim cứng ở đây. `fromStart`: đi lùi là để luyện lại
           gốc, nên vào từ đầu bài — thả con vào giữa chỗ học dở của năm ngoái thì
           mất hẳn nghĩa "học lại". Giữ nguyên `veLai` để chuỗi lùi bao nhiêu nấc
           thì vẫn còn đường về chỗ xuất phát. */
        onMoBai={(id) => setView({
          ...(baiDocCham(id) ? { page: 'baiDocCham', baiId: id }
                             : { page: 'lesson', microId: id }),
          fromStart: true, ...(view.veLai ? { veLai: view.veLai } : {}),
        })}
      />
    );
  }

  if (view.page === 'exam')
    return (
      <ExamPlayer
        chapter={view.chapter}
        chuongTrinh={chuongTrinh || 'lop5'}
        onExit={() => setView({ page: 'home' })}
        onOpenMicro={(id) => setView(baiDocCham(id)
          ? { page: 'baiDocCham', baiId: id } : { page: 'lesson', microId: id })}
        /* Ghi kết quả kèm MÃ QUYỂN. Sổ cũ khoá bằng số chương trần, nên con thi
           chương 3 của lớp 2 là huy hiệu chương 3 của lớp 5 cũng sáng theo. */
        onDone={(g) => { ghiChuong(chuongTrinh || 'lop5', view.chapter, g); setView({ page: 'home' }); }}
      />
    );

  /* ══ HỌC THEO CHỦ ĐỀ — trục thứ hai, cắt ngang mọi quyển ══
     Đặt TRƯỚC nhánh kệ sách vì nó không thuộc quyển nào: chọn chủ đề rồi mở bài
     của bất kỳ lớp nào. Mở bài thì để `chuongTrinh` nguyên như cũ (đúng nếp đường
     lùi ở màn kết), và ghi `veLai` để học xong còn tìm được đường về đây. */
  if (view.page === 'chuDe')
    return (
      <ChuDe
        progress={progress}
        viTri={view.viTri}
        /* Bậc xuất phát lấy theo lớp con khai lúc lập hồ sơ. Chưa khai thì lấy 5 —
           quyển đầy đủ nhất — và vòng luyện tự lùi nếu con chưa với tới. */
        lopCon={lopCon}
        onThoat={() => setView({ page: 'home' })}
        /* Đường về NHÀ, khác với "← Quay lại" (lùi một tầng). Đi sâu ba tầng rồi
           thì không phải bấm ba lần mới ra được kệ sách. */
        onVeNha={veKeSach}
        onMoBai={(id, viTri) => setView({
          ...(baiDocCham(id) ? { page: 'baiDocCham', baiId: id }
                             : { page: 'lesson', microId: id }),
          fromStart: true, veLai: { page: 'chuDe', viTri },
        })}
        /* Không chuyền `view.viTri` sang: lúc này con đã đi sâu bằng state bên
           trong ChuDe nên trường ấy đã cũ. Mã dạng bài là đủ — ChuDe suy ra mảng
           từ chính nó. */
        onLuyen={(maDang, lop) => setView({ page: 'luyenChuDe', maDang, lop })}
        /* Đấu thử ở Mùa giải: khối đấu KHÔNG phải một bậc của thang (tệp `DR_` chạy
           bằng bộ chơi khác), nên đi thẳng sang màn đấu chứ không qua LessonPlayer. */
        onMoDau={(khoiId, viTri) => setView({
          page: 'dau', khoiId, veLai: { page: 'chuDe', viTri },
        })}
      />
    );

  /* ══ LUYỆN MỘT CHỦ ĐỀ — tự lùi khi kém, tự tiến khi đạt ══
     Lùi thì mở BÀI HỌC của bậc dưới (con thiếu phần giảng, không phải thiếu bài
     tập), và `veLai` đưa con thẳng về vòng luyện CỦA BẬC ẤY — học xong là đo lại
     ngay, không phải tự tìm đường quay lại. */
  if (view.page === 'luyenChuDe')
    return (
      <LuyenChuDe
        key={`${view.maDang}@${view.lop}`}
        maDang={view.maDang}
        lop={view.lop}
        progress={progress}
        onXongLuot={ghiChuDe}
        onDoiBac={(lop) => setView({ ...view, lop })}
        onThoat={() => setView({ page: 'chuDe', viTri: { maDang: view.maDang } })}
        onVeNha={veKeSach}
        onMoBai={(id, lopDich) => setView({
          ...(baiDocCham(id) ? { page: 'baiDocCham', baiId: id }
                             : { page: 'lesson', microId: id }),
          fromStart: true,
          veLai: { page: 'luyenChuDe', maDang: view.maDang, lop: lopDich },
        })}
      />
    );

  /* ══ SÂN ĐẤU MÙA GIẢI ══
     Phải đứng TRƯỚC nhánh kệ sách, và đây là chỗ dễ sai nhất của tệp này.

     Vào sân đấu có HAI lối: kệ Mùa giải (lúc ấy `chuongTrinh` là lop5q2), và màn
     chủ đề — "đấu thử ở Mùa giải" — nơi KHÔNG có quyển nào đang mở. Đặt nhánh này
     sau `if (!chuongTrinh)` thì lối thứ hai bị kệ sách chặn ngang: bé bấm vào khối
     đấu và bị ném về trang chính, không một tiếng báo.

     Đúng cái bẫy đã dính một lần với bài lớp 3 mở từ màn chủ đề (khối `baiDocCham`
     nằm sau `!chuongTrinh`). Cùng một hình dạng, cùng một triệu chứng.

     Đường VỀ cũng không cố định là Mùa giải nữa: `veLai` đưa bé trở lại đúng chỗ đã
     bấm, để vào từ chủ đề thì thoát ra vẫn còn mạch chủ đề đang theo. */
  if (view.page === 'dau') {
    const raKhoiDau = view.veLai || { page: 'muagiai' };
    return (
      <DauLoader
        khoiId={view.khoiId}
        onExit={() => setView(raKhoiDau)}
        onMoMicro={(id) => setView({ page: 'lesson', microId: id })}
        onXong={(kq) => { luuVongDau(kq); setView(raKhoiDau); }}
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
        onVeKeSach={veKeSach}
      />
    );

  if (view.page === 'trai')
    return <TraiHuanLuyen onExit={() => setView({ page: 'muagiai' })} />;

  if (view.page === 'hosobay')
    return <HoSoBay onExit={() => setView({ page: 'muagiai' })}
                    onMoMicro={(id) => setView({ page: 'lesson', microId: id })} />;

  if (view.page === 'the')
    return <TheChienThuat onExit={() => setView({ page: 'muagiai' })} />;

  /* ══ TRANG CHÍNH CỦA MỘT QUYỂN — MỘT màn cho cả bốn quyển ══
     Trước đây rẽ đôi ở đây: `nhipDocCham(chuongTrinh)` thì vào HomeLop2, còn lại vào
     Home. Hai tệp, hai trải nghiệm, và mọi việc sửa đều phải làm hai lần (hoặc quên
     một lần). Nay `HomeQuyen` đọc khác biệt từ sổ đăng ký — nhịp đọc CHẬM vẫn giữ,
     nhưng nó là chuyện của PHÒNG HỌC (LessonPlayer), không phải của trang chính. */
  return (
    <HomeQuyen
      progress={progress}
      chuongTrinh={chuongTrinh}
      account={account}
      /* Mở bài thì hỏi lại nhịp đọc của CHÍNH bài ấy, đừng suy từ quyển đang mở —
         hai tên màn phục vụ hai bộ khung khác nhau trong LessonPlayer. */
      onMoBai={(id, opts) => setView({
        ...(baiDocCham(id) ? { page: 'baiDocCham', baiId: id }
                           : { page: 'lesson', microId: id }),
        fromStart: !!opts?.fromStart,
      })}
      onSetMode={(m) => setProgress((p) => setMode(p, m))}
      onMoOnTap={(c) => setView({ page: 'exam', chapter: c })}
      onSoPhuHuynh={onSoPhuHuynh}
      onMoMuaGiai={() => setView({ page: 'muagiai' })}
      onMoXepHang={onMoXepHang}
      onVeKeSach={veKeSach}
    />
  );
}
