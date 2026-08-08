import React, { useEffect, useState } from 'react';
import { CONTENT, dongDau } from '../lib/content.js';

/**
 * SỔ TAY CHIẾN THUẬT — 14 thẻ, mỗi chương một thẻ.
 *
 * Sách dặn: in ra, cắt rời, đọc 3 phút TRƯỚC mỗi vòng đấu. Trên máy thì không cắt
 * được, nên làm thành thẻ lật — chọn chương nào đọc thẻ ấy, gọn trong một màn.
 */
export default function TheChienThuat({ onExit }) {
  const [the, setThe] = useState(null);
  const [loi, setLoi] = useState(null);
  const [chon, setChon] = useState(0);

  useEffect(() => {
    fetch(dongDau(`${CONTENT}/quyen2/the_chien_thuat.json`))
      .then((r) => r.json()).then(setThe)
      .catch((e) => setLoi(String(e?.message || e)));
  }, []);
  useEffect(() => { window.scrollTo(0, 0); }, [chon]);

  if (loi) return <div className="p-6 text-alert">Không mở được sổ tay: {loi}</div>;
  if (!the) return <div className="p-6 text-mute">Đang mở sổ tay chiến thuật…</div>;

  const t = the[chon];
  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-16">
      <header className="sticky top-0 z-20 bg-navy px-3.5 py-2.5 text-white">
        <div className="flex items-center gap-2.5">
          <button onClick={onExit}
                  className="rounded-full border border-white/40 px-2 py-0.5 text-[11px] font-bold">
            ← Mùa giải
          </button>
          <span className="flex-1 text-[13px] font-bold">Sổ tay chiến thuật · 14 thẻ</span>
        </div>
        <div className="mt-2 flex gap-1.5 overflow-x-auto">
          {the.map((x, k) => (
            <button key={x.so} onClick={() => setChon(k)}
                    className={`shrink-0 rounded-full px-2.5 py-1 text-[11.5px] font-extrabold ${
                      k === chon ? 'bg-gold text-gold-dark' : 'bg-white/15 text-white'}`}>
              C{x.chuong}
            </button>
          ))}
        </div>
      </header>

      <div className="px-3.5 pt-3.5">
        <div className="card">
          <div className="kicker">THẺ {t.so} · CHƯƠNG {t.chuong}</div>
          <h2 className="text-[18px] font-bold leading-snug text-navy">{t.ten}</h2>
        </div>
        <div className="card">
          {t.dong.map((d, i) => (
            <p key={i} className={`${i ? 'mt-2' : ''} text-[14.5px] leading-relaxed ${
              /^(Bài|CA )/.test(d) ? 'font-bold text-navy' : ''}`}>{d}</p>
          ))}
        </div>
        <p className="px-1 text-[12.5px] leading-relaxed text-mute">
          Sách dặn đọc thẻ này <b>3 phút trước mỗi vòng đấu</b> — không học dạng mới,
          chỉ nhắc lại những gì đã thuộc.
        </p>
      </div>
    </div>
  );
}
