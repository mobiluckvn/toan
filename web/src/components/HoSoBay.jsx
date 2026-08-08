import React, { useEffect, useMemo, useState } from 'react';
import { CONTENT, dongDau } from '../lib/content.js';

/**
 * HỒ SƠ CÁO ĐỀ — tra 168 cái bẫy.
 *
 * Trước đây hồ sơ chỉ hiện khi con SẬP bẫy trong một vòng đấu. Nhưng sách dùng nó
 * theo ba cách khác nữa: soi 30 giây cuối mỗi câu, chữa đề sau mỗi vòng, và ôn
 * nước rút tuần cuối. Muốn thế thì phải TRA ĐƯỢC — nên có màn riêng, tìm theo chữ,
 * lọc theo chương và theo tầng.
 *
 * Mỗi bẫy nối thẳng về micro Quyển 1 dạy đúng cái bẫy ấy (trục CĐ-x.y ↔ Bx.My).
 */
const TANG = { 1: '⚠ sơ cấp', 2: '⚠⚠ trung cấp', 3: '⚠⚠⚠ cao cấp' };
const MAU_TANG = {
  1: 'bg-teal-pale text-teal-dark',
  2: 'bg-gold-pale text-gold-dark',
  3: 'bg-alert-pale text-alert',
};

export default function HoSoBay({ onExit, onMoMicro }) {
  const [hs, setHs] = useState(null);
  const [loi, setLoi] = useState(null);
  const [tim, setTim] = useState('');
  const [chuong, setChuong] = useState(0);
  const [tang, setTang] = useState(0);

  useEffect(() => {
    fetch(dongDau(`${CONTENT}/quyen2/ho_so_bay.json`))
      .then((r) => r.json()).then(setHs)
      .catch((e) => setLoi(String(e?.message || e)));
  }, []);

  const loc = useMemo(() => {
    if (!hs) return [];
    const q = tim.trim().toLowerCase();
    return hs.filter((h) =>
      (!chuong || h.chuong === chuong)
      && (!tang || h.tang === tang)
      && (!q || `${h.ma} ${h.ten} ${h.dauHieu} ${h.donGo} ${h.thanChu}`.toLowerCase().includes(q)));
  }, [hs, tim, chuong, tang]);

  if (loi) return <div className="p-6 text-alert">Không mở được hồ sơ: {loi}</div>;
  if (!hs) return <div className="p-6 text-mute">Đang mở hồ sơ Cáo Đề…</div>;

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-16">
      <header className="sticky top-0 z-20 bg-navy px-3.5 py-2.5 text-white">
        <div className="flex items-center gap-2.5">
          <button onClick={onExit}
                  className="rounded-full border border-white/40 px-2 py-0.5 text-[11px] font-bold">
            ← Mùa giải
          </button>
          <span className="flex-1 text-[13px] font-bold">Hồ sơ Cáo Đề · 168 bẫy</span>
        </div>
        <input className="mt-2 w-full rounded-xl px-3 py-1.5 text-[14.5px] text-ink"
               placeholder="tìm theo mã, tên bẫy hay thần chú…"
               value={tim} onChange={(e) => setTim(e.target.value)} />
      </header>

      <div className="sticky top-[84px] z-10 border-b border-line bg-white px-2.5 py-1.5">
        <div className="flex gap-1.5 overflow-x-auto">
          {[[0, 'mọi tầng'], [1, '⚠'], [2, '⚠⚠'], [3, '⚠⚠⚠']].map(([v, nh]) => (
            <button key={v} onClick={() => setTang(v)}
                    className={`shrink-0 rounded-full px-2.5 py-1 text-[11.5px] font-bold ${
                      tang === v ? 'bg-navy text-white' : 'bg-soft text-mute'}`}>{nh}</button>
          ))}
          <span className="w-2" />
          {[0, ...Array.from({ length: 14 }, (_, i) => i + 1)].map((c) => (
            <button key={c} onClick={() => setChuong(c)}
                    className={`shrink-0 rounded-full px-2.5 py-1 text-[11.5px] font-bold ${
                      chuong === c ? 'bg-teal text-white' : 'bg-soft text-mute'}`}>
              {c ? `C${c}` : 'mọi chương'}
            </button>
          ))}
        </div>
      </div>

      <div className="px-3.5 pt-3">
        <p className="mb-2 text-[12.5px] text-mute">{loc.length} bẫy</p>
        {loc.map((h) => (
          <article key={h.ma} className="card">
            <div className="flex flex-wrap items-center gap-2">
              <span className="rounded bg-navy px-1.5 py-0.5 text-[11px] font-extrabold text-white">{h.ma}</span>
              <span className={`rounded-full px-2 py-0.5 text-[10.5px] font-bold ${MAU_TANG[h.tang]}`}>
                {TANG[h.tang]}
              </span>
              <span className="text-[11.5px] text-mute">chương {h.chuong} · bài {h.bai}</span>
            </div>
            <h3 className="mt-1 text-[16px] font-bold leading-snug text-navy">{h.ten}</h3>
            <p className="mt-1.5 text-[14.5px] leading-relaxed">
              <b className="text-alert">Dấu hiệu:</b> {h.dauHieu}
            </p>
            <p className="mt-1.5 text-[14.5px] leading-relaxed">
              <b className="text-teal-dark">Đòn gỡ:</b> {h.donGo}
            </p>
            {h.thanChu && (
              <p className="mt-2 rounded-xl bg-gold-pale px-3 py-2 text-[14.5px] font-bold text-gold-dark">
                🔑 “{h.thanChu}”
              </p>
            )}
            <button onClick={() => onMoMicro?.(h.micro)}
                    className="mt-2 text-[13px] font-bold text-navy underline">
              Ôn micro {h.micro.replace('DL:KSN5Q1.', '')} của Quyển 1 ▶
            </button>
          </article>
        ))}
        {loc.length === 0 && (
          <p className="py-8 text-center text-[14.5px] text-mute">
            Không có bẫy nào khớp. Thử bỏ bớt bộ lọc nhé.
          </p>
        )}
      </div>
    </div>
  );
}
