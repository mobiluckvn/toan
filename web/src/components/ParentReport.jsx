import React, { useMemo, useState } from 'react';
import { overallStats } from '../lib/progress.js';
import { allMicroIds, chapterOf } from '../lib/content.js';
import { weakestUnits } from '../lib/adaptive.js';

/**
 * SỔ HỌC — bản tính tại máy từ tiến độ cục bộ (chạy được cả khi chưa có Firebase).
 * Khi đã nối Firebase, màn này đọc thẳng parentReport/{learnerId} do Function ghi mỗi đêm.
 */
export default function ParentReport({ progress, cloudReport, onExit, onOpenMicro, onRefresh }) {
  const list = allMicroIds();
  const all = overallStats(progress, list);

  const local = useMemo(() => {
    const ms = Object.entries(progress.micros || {});
    const tried = ms.filter(([, m]) => m.done && !m.pass);
    const attempts = ms.reduce((s, [, m]) => s + (m.attempts || 0), 0);
    const byChapter = {};
    ms.forEach(([id, m]) => {
      const c = chapterOf(id);
      byChapter[c] = byChapter[c] || { done: 0, tried: 0 };
      m.pass ? byChapter[c].done++ : byChapter[c].tried++;
    });
    return { tried, attempts, byChapter };
  }, [progress]);

  const r = cloudReport;
  const weak = r?.weakest || weakestUnits(progress.mastery || {}, 3);
  const [dangMoi, setDangMoi] = useState(false);
  const [loi, setLoi] = useState(null);

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
      <header className="flex items-center gap-2.5 bg-navy px-4 py-3 text-white">
        <button onClick={onExit} className="text-[15px]">←</button>
        <h1 className="flex-1 text-[15px] font-bold">Sổ học của con</h1>
      </header>

      <div className="px-3.5 pt-3.5">
        {/* Sổ trên máy chủ chỉ tổng hợp lúc 21:00 mỗi đêm. Con vừa học xong mà bố mẹ
            mở ra thấy trống thì tưởng công học không được lưu — nên nói rõ mốc tổng
            hợp và cho dựng lại ngay. */}
        {onRefresh && (
          <div className="card flex flex-wrap items-center justify-between gap-2 py-3">
            <span className="text-[13px] text-mute">
              {r?.generatedAt
                ? `Số liệu máy chủ tổng hợp lúc ${new Date(r.generatedAt).toLocaleString('vi-VN')}`
                : 'Chưa có số liệu máy chủ cho tuần này'}
            </span>
            <button
              className="rounded-full border-[1.5px] border-navy px-3 py-1 text-[12.5px] font-bold text-navy disabled:opacity-50"
              disabled={dangMoi}
              onClick={async () => {
                setDangMoi(true); setLoi(null);
                try { await onRefresh(); } catch (e) { setLoi(String(e?.message || e)); }
                finally { setDangMoi(false); }
              }}>
              {dangMoi ? 'đang cập nhật…' : '↻ Cập nhật ngay'}
            </button>
            {loi && <p className="w-full text-[12.5px] text-alert">{loi}</p>}
          </div>
        )}

        {r?.luotThieuGio > 0 && (
          <p className="mb-2 rounded-xl bg-[#F2F6FA] px-3.5 py-2.5 text-[12.5px] leading-relaxed text-mute">
            Có {r.luotThieuGio} lượt trả lời ghi từ bản cũ nên chưa đo được thời gian —
            phần “phút học” và “câu con làm lâu” chỉ tính trên các buổi học từ nay về sau.
          </p>
        )}

        <div className="card">
          <div className="kicker">TỔNG QUAN</div>
          <div className="flex flex-wrap gap-2.5">
            {[['MICRO ĐÃ ĐẠT', `${all.done}/${all.total}`], ['HUY HIỆU', `${all.badges}/14`],
              ['LƯỢT HỌC', String(local.attempts)],
              /* Buổi học ghi bằng luật cũ không có dữ liệu giờ giấc dùng được. Hiện
                 "0 phút" thì bố mẹ tưởng con không học — nói thẳng là chưa đo được. */
              ...(r ? [['PHÚT (7 NGÀY)', r.minutes > 0 ? String(r.minutes) : (r.luotThieuGio > 0 ? '—' : '0')],
                       ['ĐÚNG', `${r.correctRate}%`]] : [])
            ].map(([k, v]) => (
              <div key={k} className="min-w-[92px] flex-1 rounded-xl bg-[#EAF1F7] px-3 py-2.5 text-center">
                <b className="block text-[21px] text-navy">{v}</b>
                <span className="text-[10.5px] font-extrabold text-mute">{k}</span>
              </div>
            ))}
          </div>
          {r && <p className="mt-3 text-[14.5px] leading-relaxed">{r.headline}</p>}
          {!r && (
            <p className="mt-3 text-[13px] text-mute">
              Số liệu tính tại máy. Khi nối Firebase, mục này hiện thêm số phút học, tỉ lệ đúng và bẫy hay sập —
              do máy chủ tổng hợp lúc 21 giờ mỗi đêm.
            </p>
          )}
        </div>

        {local.tried.length > 0 && (
          <div className="card">
            <div className="kicker">CHƯA QUA CÂU BẪY — NÊN ÔN LẠI</div>
            {local.tried.slice(0, 6).map(([id, m]) => (
              <button key={id} onClick={() => onOpenMicro(id)}
                className="mt-2 flex w-full items-center gap-2.5 rounded-xl border border-line px-3 py-2.5 text-left text-[14px] hover:bg-[#F0F5F9]">
                <span className="rounded bg-gold px-1.5 py-0.5 text-[11px] font-extrabold text-gold-dark">
                  {id.replace('DL:KSN5Q1.', '')}
                </span>
                <span className="flex-1">đúng {m.best}/{m.total} · đã thử {m.attempts} lần</span>
                <span className="text-mute">▶</span>
              </button>
            ))}
          </div>
        )}

        {r?.topTraps?.length > 0 && (
          <div className="card">
            <div className="kicker">BẪY HAY SẬP NHẤT TUẦN QUA</div>
            {r.topTraps.map((tp) => (
              <div key={tp.microId} className="mt-2 rounded-xl border-[1.5px] border-alert bg-alert-pale px-3 py-2.5 text-[14px]">
                <b>{tp.trapName || tp.microId.replace('DL:KSN5Q1.', '')}</b>
                <span className="ml-2 text-mute">sập {tp.times} lần</span>
              </div>
            ))}
          </div>
        )}

        {(r?.suggestion || r?.watchFor) && (
          <div className="card">
            <div className="kicker">GỢI Ý CHO BỐ MẸ</div>
            {r.suggestion && <p className="text-[15px]"><b>Chơi cùng con:</b> {r.suggestion}</p>}
            {r.watchFor && <p className="mt-2 text-[15px]"><b>Để ý:</b> {r.watchFor}</p>}
          </div>
        )}

        <div className="card">
          <div className="kicker">TIẾN ĐỘ TỪNG CHƯƠNG</div>
          <div className="flex flex-wrap gap-1.5">
            {Array.from({ length: 14 }, (_, i) => i + 1).map((c) => {
              const b = local.byChapter[c] || { done: 0 };
              const pct = Math.round((b.done / 12) * 100);
              return (
                <div key={c} className="w-[68px] rounded-lg bg-[#F2F6FA] px-2 py-1.5 text-center">
                  <div className="text-[11px] font-extrabold text-navy">C{c}</div>
                  <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-white">
                    <i className="block h-full bg-teal" style={{ width: `${pct}%` }} />
                  </div>
                  <div className="mt-1 text-[10.5px] text-mute">{b.done}/12</div>
                </div>
              );
            })}
          </div>
        </div>

        {weak.length > 0 && (
          <div className="card">
            <div className="kicker">KỸ NĂNG CÒN YẾU</div>
            {weak.map((w) => (
              <div key={w.unit} className="mt-1.5 flex items-center gap-2 text-[13px]">
                <span className="flex-1 truncate font-mono text-[11.5px] text-mute">{w.unit}</span>
                <span className="h-1.5 w-24 overflow-hidden rounded-full bg-[#EAF1F7]">
                  <i className="block h-full bg-gold" style={{ width: `${Math.round((w.p || 0) * 100)}%` }} />
                </span>
                <b className="w-9 text-right text-navy">{Math.round((w.p || 0) * 100)}%</b>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
