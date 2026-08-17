import React, { useEffect, useMemo, useState } from 'react';
import { logout } from '../lib/taiKhoan.js';
import { dsChuongTrinhSapXep, maKy } from '../lib/soQuyen.js';
import HocSinhChiTiet from './HocSinhChiTiet.jsx';

const short = (id) => String(id || '').replace('DL:KSN5Q1.', '');

/**
 * TRÌNH ĐỘ HIỆN TẠI của một dòng — quyển CAO NHẤT em đã có bài đạt.
 *
 * Hàm nền đếm bài đạt theo MÃ SÁCH (`KSN2`, `KSN5Q1`) vì nó chạy trên máy chủ, không
 * có sổ đăng ký. Ở đây dịch ngược bằng chính `maKy()` của sổ — thêm quyển mới thì
 * không phải sửa cả hai đầu.
 *
 * Bảng dựng bằng bản cũ của hàm nền không có `theoSach`; trả về null để dòng ấy để
 * trống, đừng đoán bừa.
 */
function trinhDoCua(r) {
  if (!r?.theoSach) return null;
  const ds = dsChuongTrinhSapXep()
    .filter((c) => c.loai === 'hoc' && r.theoSach[maKy(c.ma)] > 0)
    .sort((a, b) => (b.lop || 0) - (a.lop || 0));
  const cao = ds[0];
  if (!cao) return null;
  return `${cao.ten} · ${r.theoSach[maKy(cao.ma)]} bài đạt`
    + (ds.length > 1 ? ` (+${ds.length - 1} quyển khác)` : '');
}
const when = (ms) => {
  if (!ms) return 'chưa học';
  const d = Math.floor((Date.now() - ms) / 86400000);
  return d <= 0 ? 'hôm nay' : d === 1 ? 'hôm qua' : `${d} ngày trước`;
};

/** Một ô số to ở đầu bảng */
const Stat = ({ label, value, tone = '' }) => (
  <div className="min-w-[86px] flex-1 rounded-xl bg-soft px-3 py-2.5 text-center">
    <b className={`block text-[21px] ${tone || 'text-navy'}`}>{value}</b>
    <span className="text-[10.5px] font-extrabold text-mute">{label}</span>
  </div>
);

/**
 * BẢNG GIÁO VIÊN — đọc MỘT document do Cloud Function dựng mỗi đêm 21h15,
 * không quét hàng chục nghìn dòng nhật ký lúc cô mở app.
 *
 * Bấm vào một em thì mới tải học bạ của riêng em đó (xem `HocSinhChiTiet.jsx`):
 * tiến độ từng bài, kỳ sát hạch từng chương, bậc chủ đề đã vững, và nhật ký từng
 * câu. Tải theo yêu cầu chứ không dựng sẵn cho cả trường — một lớp 40 em thì dựng
 * sẵn là 40 lần quét, mà cô mỗi lần chỉ mở một em.
 */
export default function TeacherBoard({ mon = [], onExit }) {
  /* Mỗi môn có bảng riêng. Hiện mới một môn có nội dung nên lấy môn đầu; khi có môn
     thứ hai thì thêm một thanh chọn môn đúng như bảng xếp hạng và sổ bố mẹ. */
  const monChinh = mon[0];
  const [board, setBoard] = useState(null);
  const [err, setErr] = useState('');
  const [pick, setPick] = useState(null);           // {uid, displayName}
  const [q, setQ] = useState('');
  const [dangMoi, setDangMoi] = useState(false);
  /* Chỉ mục sách và bản đồ dạng bài là của MÔN. Bảng này chỉ nạp trước một lần rồi
     chuyền xuống — nó không biết bên trong có gì. */
  const [sanSang, setSanSang] = useState(false);
  useEffect(() => {
    let song = true;
    Promise.all(mon.map((m) => m.napBanDoDang().catch(() => ({}))))
      .then(() => song && setSanSang(true));
    return () => { song = false; };
  }, [mon]);

  useEffect(() => {
    let alive = true;
    monChinh?.bangCoGiao()
      .then((b) => alive && setBoard(b || { empty: true }))
      .catch((e) => alive && setErr(String(e?.message || e)));
    return () => { alive = false; };
  }, [monChinh]);

  const filtered = useMemo(() => {
    const list = board?.rows || [];
    const k = q.trim().toLowerCase();
    if (!k) return list;
    return list.filter((r) => `${r.displayName} ${r.email}`.toLowerCase().includes(k));
  }, [board, q]);

  if (err) return <Wrap onExit={onExit}><p className="card text-alert">{err}</p></Wrap>;
  if (!board) return <Wrap onExit={onExit}><p className="card text-mute">Đang mở bảng…</p></Wrap>;

  /* ── Học bạ đầy đủ của MỘT em ── */
  if (pick) {
    return (
      <Wrap onExit={() => setPick(null)} title={pick.displayName || 'Học sinh'} back="← Về bảng">
        {!sanSang && <p className="card text-mute">Đang mở chỉ mục sách…</p>}
        {sanSang && <HocSinhChiTiet key={pick.uid} em={pick} mon={mon} />}
      </Wrap>
    );
  }

  /* ── Bảng chung ── */
  if (board.empty || !board.rows) {
    return (
      <Wrap onExit={onExit} title="Bảng theo dõi">
        <div className="card">
          <p className="text-[15px] leading-relaxed">
            Bảng chưa được dựng lần nào. Máy chủ tổng hợp lúc <b>21h15 mỗi đêm</b> — cô quay
            lại sau đó nhé.
          </p>
          {/* Nút dựng phải có Ở ĐÂY, không chỉ ở bảng đã dựng.
              Trước đây nó chỉ nằm trong nhánh bảng-đã-có, còn màn này bảo cô vào
              Firebase Console — đúng cái vòng gà và trứng: cô mới nhận lớp, bảng chưa
              dựng lần nào, tức là đúng lúc cần nút nhất thì không có nút. Mà cô giáo
              thì không có tài khoản Firebase Console. */}
          <button
            className="btn-go mt-3"
            disabled={dangMoi}
            onClick={async () => {
              setDangMoi(true);
              try { await monChinh.lamMoiBangCoGiao(7); setBoard(await monChinh.bangCoGiao() || { empty: true }); }
              catch (e) { setErr(String(e?.message || e)); }
              finally { setDangMoi(false); }
            }}>
            {dangMoi ? 'đang dựng…' : '↻ Dựng bảng ngay'}
          </button>
          <p className="mt-2 text-[13px] text-mute">
            Bảng tổng hợp mỗi đêm; nút trên dựng lại ngay bằng số liệu 7 ngày gần nhất.
          </p>
        </div>
      </Wrap>
    );
  }

  return (
    <Wrap onExit={onExit} title="Bảng theo dõi">
      <div className="card">
        {/* Bảng tự tổng hợp lúc 21:15 mỗi đêm. Con học sáng nay mà cô mở lúc trưa thì
            thấy số liệu của hôm qua — nên nói rõ mốc tổng hợp và cho dựng lại ngay. */}
        <div className="kicker flex flex-wrap items-center gap-2">
          <span>7 NGÀY QUA · TỔNG HỢP {new Date(board.generatedAt).toLocaleString('vi-VN')}</span>
          <button
            className="rounded-full border-[1.5px] border-navy px-2.5 py-0.5 text-[11px] font-bold text-navy disabled:opacity-50"
            disabled={dangMoi}
            onClick={async () => {
              setDangMoi(true);
              try { await monChinh.lamMoiBangCoGiao(7); setBoard(await monChinh.bangCoGiao()); }
              catch (e) { setErr(String(e?.message || e)); }
              finally { setDangMoi(false); }
            }}>
            {dangMoi ? 'đang cập nhật…' : '↻ Cập nhật ngay'}
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          <Stat label="CÓ HỌC" value={`${board.activeLearners}/${board.learners}`} />
          <Stat label="LƯỢT TRẢ LỜI" value={board.answered} />
          <Stat label="TỈ LỆ ĐÚNG" value={`${board.correctRate}%`} />
          <Stat label="BÀI ĐẠT TB" value={board.avgMicrosPassed} />
        </div>
        {/* Quyển 2 để riêng: luyện thi có đồng hồ, cần hỗ trợ khác với học bài */}
        <div className="mt-2 flex flex-wrap gap-2">
          <Stat label="Q2 · LƯỢT" value={board.q2Answered ?? 0} />
          <Stat label="Q2 · ĐÚNG" value={board.q2CorrectRate == null ? '—' : `${board.q2CorrectRate}%`} />
          <Stat label="Q2 · HỌC SINH" value={board.q2Learners ?? 0} />
          <Stat label="Q2 · VÒNG ĐẤU" value={board.q2Vong ?? 0} />
        </div>
      </div>

      {/* ── EM CẦN GIÚP, VÀ YẾU KIỂU GÌ ──
          Đặt TRƯỚC mọi bảng khác vì đây là câu cô hỏi đầu tiên: sáng mai gọi em nào.
          Ba nhãn không phải để phân loại trẻ con, mà để chọn CÁCH GIÚP: em bấm bừa
          cần nhắc đọc kỹ, em bỏ video cần bảo xem hết, em ngồi lâu vẫn sai thì thiếu
          phần giảng — giao thêm bài tập chỉ để em sai thêm một lượt nữa. */}
      {board.canGiup?.length > 0 && (
        <div className="card">
          <div className="kicker">EM CẦN GIÚP TRƯỚC</div>
          {board.canGiup.slice(0, 10).map((e) => {
            const nhan = {
              au: ['BẤM NHANH', 'Nhắc con đọc kỹ đề — con hiểu bài nhưng đang vội.'],
              boQuaGiang: ['BỎ QUA GIẢNG', 'Con bấm vượt video. Bảo con xem hết đã.'],
              hong: ['NGỒI LÂU VẪN SAI', 'Con thiếu phần giảng, không thiếu bài tập.'],
              chuaRo: ['CHƯA ĐỦ SỐ LIỆU', 'Chưa đo được giờ học của con.'],
            }[e.viSao] || ['', ''];
            return (
              <div key={e.uid} className="mt-2 rounded-xl border-[1.5px] border-line px-3 py-2.5">
                <div className="flex items-center gap-2 text-[14px]">
                  <b className="flex-1">{e.displayName || e.uid.slice(0, 6)}</b>
                  <span className="rounded bg-navy px-1.5 py-0.5 text-[11px] font-extrabold text-white">
                    {nhan[0]}
                  </span>
                  <b className="text-alert tabular-nums">{e.correctRate}%</b>
                </div>
                <div className="mt-1 text-[12.5px] text-mute">
                  {e.answered} câu · {e.minutes} phút
                  {e.giayMoiBai != null && ` · ${e.giayMoiBai}s mỗi bài`}
                </div>
                <div className="mt-1 text-[13px]">{nhan[1]}</div>
              </div>
            );
          })}
        </div>
      )}

      {board.topTraps?.length > 0 && (
        <div className="card">
          <div className="kicker">BẪY NHIỀU EM SẬP NHẤT — NÊN DẠY LẠI</div>
          {board.topTraps.map((t) => (
            <div key={t.microId}
                 className="mt-2 flex items-center gap-2.5 rounded-xl border-[1.5px] border-alert bg-alert-pale px-3 py-2.5 text-[14px]">
              <span className="rounded bg-alert px-1.5 py-0.5 font-mono text-[11px] font-extrabold text-white">
                {short(t.microId)}
              </span>
              <span className="flex-1">{t.trapName || t.title || 'câu bẫy'}</span>
              <b className="text-alert">{t.learners} em</b>
            </div>
          ))}
        </div>
      )}

      {board.stuck?.length > 0 && (
        <div className="card">
          <div className="kicker">EM ĐANG TẮC — THỬ NHIỀU LẦN CHƯA QUA</div>
          {board.stuck.slice(0, 10).map((s, i) => {
            const who = board.rows.find((r) => r.uid === s.learnerId);
            return (
              <button key={i} onClick={() => who && setPick(who)}
                className="mt-2 flex w-full items-center gap-2.5 rounded-xl border border-line px-3 py-2.5 text-left text-[14px] hover:bg-[#F0F5F9]">
                <span className="flex-1 font-semibold text-navy">{who?.displayName || s.learnerId}</span>
                <span className="font-mono text-[11.5px] text-mute">{short(s.microId)}</span>
                <span className="text-mute">thử {s.tries} lần</span>
                <span className="text-mute">▶</span>
              </button>
            );
          })}
        </div>
      )}

      <div className="card">
        <div className="kicker">TẤT CẢ HỌC SINH · {board.rows.length}</div>
        <input className="numin mb-2 w-full text-left text-[15px] font-normal"
               placeholder="Tìm theo tên hoặc email…" value={q}
               onChange={(e) => setQ(e.target.value)} />
        {filtered.length === 0 && <p className="py-3 text-center text-[13.5px] text-mute">Không có em nào khớp.</p>}
        {filtered.map((r) => (
          <button key={r.uid} onClick={() => setPick(r)}
            className="flex w-full items-center gap-2.5 border-b border-line py-2.5 text-left last:border-0 hover:bg-[#F0F5F9]">
            <span className="min-w-0 flex-1">
              <b className="block truncate text-[14px] text-navy">{r.displayName || r.email || r.uid}</b>
              <span className="block text-[11.5px] text-mute">
                {r.answered > 0
                  ? `${r.sessions} buổi`
                    /* Số phút do bản mới của hàm nền tính. Bảng dựng bằng bản cũ thì
                       không có trường này — bỏ hẳn dòng, đừng hiện "0 phút". */
                    + (r.minutes != null ? ` · ${r.minutes} phút` : '')
                    + ` · ${r.answered} câu · đúng ${r.correctRate}%`
                  : 'tuần này chưa vào học'}
              </span>
              {/* TRÌNH ĐỘ: quyển cao nhất em đã có bài đạt. "47 bài đạt" một mình
                  không nói lên gì — 47 bài lớp 2 khác hẳn 47 bài lớp 5. */}
              <span className="block text-[11.5px] font-semibold text-navy-light">
                {trinhDoCua(r) || '—'}
              </span>
            </span>
            <span className="text-right">
              <b className="block text-[15px] text-navy">{r.microsPassed}</b>
              <span className="text-[10.5px] text-mute">bài đạt</span>
            </span>
            <span className="w-[70px] text-right text-[11.5px] text-mute">{when(r.lastAt)}</span>
          </button>
        ))}
      </div>

      {board.idleLearners?.length > 0 && (
        <div className="card">
          <div className="kicker">CHƯA VÀO HỌC BUỔI NÀO TUẦN NÀY</div>
          <p className="text-[14px]">
            <b className="text-alert">{board.idleLearners.length} em</b> — cô nhắc phụ huynh giúp nhé.
          </p>
        </div>
      )}
    </Wrap>
  );
}

function Wrap({ children, onExit, title = 'Bảng theo dõi', back = '←' }) {
  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
      <header className="flex items-center gap-2.5 bg-navy px-4 py-3 text-white">
        <button onClick={onExit} className="text-[13px]">{back}</button>
        <h1 className="flex-1 text-[15px] font-bold">{title}</h1>
        <button onClick={() => logout()} className="rounded-full bg-navy-light px-2.5 py-1 text-[11.5px] font-bold">
          Thoát
        </button>
      </header>
      <div className="px-3.5 pt-3.5">{children}</div>
    </div>
  );
}
