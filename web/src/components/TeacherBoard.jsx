import React, { useEffect, useMemo, useState } from 'react';
import { teacherBoard, learnerAttempts, logout } from '../lib/firebase.js';

const short = (id) => String(id || '').replace('DL:KSN5Q1.', '');
const when = (ms) => {
  if (!ms) return 'chưa học';
  const d = Math.floor((Date.now() - ms) / 86400000);
  return d <= 0 ? 'hôm nay' : d === 1 ? 'hôm qua' : `${d} ngày trước`;
};

/** Một ô số to ở đầu bảng */
const Stat = ({ label, value, tone = '' }) => (
  <div className="min-w-[86px] flex-1 rounded-xl bg-[#EAF1F7] px-3 py-2.5 text-center">
    <b className={`block text-[21px] ${tone || 'text-navy'}`}>{value}</b>
    <span className="text-[10.5px] font-extrabold text-mute">{label}</span>
  </div>
);

/**
 * BẢNG GIÁO VIÊN — đọc MỘT document do Cloud Function dựng mỗi đêm 21h15,
 * không quét hàng chục nghìn dòng nhật ký lúc cô mở app.
 * Bấm vào một em thì mới tải nhật ký từng câu của riêng em đó.
 */
export default function TeacherBoard({ onExit }) {
  const [board, setBoard] = useState(null);
  const [err, setErr] = useState('');
  const [pick, setPick] = useState(null);           // {uid, displayName}
  const [rows, setRows] = useState(null);
  const [q, setQ] = useState('');

  useEffect(() => {
    let alive = true;
    teacherBoard()
      .then((b) => alive && setBoard(b || { empty: true }))
      .catch((e) => alive && setErr(String(e?.message || e)));
    return () => { alive = false; };
  }, []);

  useEffect(() => {
    if (!pick) { setRows(null); return undefined; }
    let alive = true;
    setRows('loading');
    learnerAttempts(pick.uid, 200)
      .then((r) => alive && setRows(r))
      .catch(() => alive && setRows([]));
    return () => { alive = false; };
  }, [pick]);

  const filtered = useMemo(() => {
    const list = board?.rows || [];
    const k = q.trim().toLowerCase();
    if (!k) return list;
    return list.filter((r) => `${r.displayName} ${r.email}`.toLowerCase().includes(k));
  }, [board, q]);

  if (err) return <Wrap onExit={onExit}><p className="card text-alert">{err}</p></Wrap>;
  if (!board) return <Wrap onExit={onExit}><p className="card text-mute">Đang mở bảng…</p></Wrap>;

  /* ── Nhật ký từng câu của MỘT em ── */
  if (pick) {
    return (
      <Wrap onExit={() => setPick(null)} title={pick.displayName || 'Học sinh'} back="← Về bảng">
        {rows === 'loading' && <p className="card text-mute">Đang mở nhật ký…</p>}
        {Array.isArray(rows) && rows.length === 0 && (
          <p className="card text-mute">Em này chưa có lượt trả lời nào được ghi.</p>
        )}
        {Array.isArray(rows) && rows.length > 0 && (
          <div className="card">
            <div className="kicker">NHẬT KÝ TỪNG CÂU · {rows.length} LƯỢT GẦN NHẤT</div>
            <div className="max-h-[70vh] overflow-y-auto">
              {rows.map((a, i) => (
                <div key={i} className="flex items-center gap-2 border-b border-line py-2 text-[13px] last:border-0">
                  <span className={`h-2 w-2 flex-none rounded-full ${a.correct ? 'bg-teal' : 'bg-alert'}`} />
                  <span className="w-[76px] flex-none font-mono text-[11.5px] text-mute">{short(a.microId)}</span>
                  <span className="w-[42px] flex-none font-mono text-[11.5px] text-mute">{a.itemId}</span>
                  <span className="flex-1">
                    {a.correct ? 'đúng' : 'sai'}
                    {a.tries > 1 && <span className="text-mute"> · thử {a.tries} lần</span>}
                    {a.hintsUsed > 0 && <span className="text-mute"> · xem {a.hintsUsed} gợi ý</span>}
                  </span>
                  {a.mustPass && (
                    <span className="pill flex-none bg-alert-pale text-alert">BẪY</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
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
          <p className="mt-2 text-[13px] text-mute">
            Muốn có ngay thì chạy tay hàm <code>nightlyTeacherBoard</code> trong Firebase Console.
          </p>
        </div>
      </Wrap>
    );
  }

  return (
    <Wrap onExit={onExit} title="Bảng theo dõi">
      <div className="card">
        <div className="kicker">
          7 NGÀY QUA · TỔNG HỢP {new Date(board.generatedAt).toLocaleString('vi-VN')}
        </div>
        <div className="flex flex-wrap gap-2">
          <Stat label="CÓ HỌC" value={`${board.activeLearners}/${board.learners}`} />
          <Stat label="LƯỢT TRẢ LỜI" value={board.answered} />
          <Stat label="TỈ LỆ ĐÚNG" value={`${board.correctRate}%`} />
          <Stat label="BÀI ĐẠT TB" value={board.avgMicrosPassed} />
        </div>
      </div>

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
              <span className="text-[11.5px] text-mute">
                {r.answered > 0
                  ? `${r.sessions} buổi · ${r.answered} câu · đúng ${r.correctRate}%`
                  : 'tuần này chưa vào học'}
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
