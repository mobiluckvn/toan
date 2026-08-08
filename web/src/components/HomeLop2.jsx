import React, { useEffect, useMemo, useState } from 'react';
import { CONTENT, dongDau } from '../lib/content.js';
import ChanTrang from './ChanTrang.jsx';

/**
 * TRANG CHÍNH LỚP 2 — danh sách 33 bài theo 8 chương.
 *
 * Bé lớp 2 chưa đọc nhanh, nên KHÔNG khoá bài: khoá rồi giải thích vì sao là thêm
 * chữ để đọc, mà bé chưa có nhu cầu "mở khoá". Thay vào đó đánh dấu bài đã học
 * bằng ngôi sao, và luôn chỉ rõ "bài tiếp theo của con".
 */
export default function HomeLop2({ progress, onMoBai, onDoiChuongTrinh }) {
  const [idx, setIdx] = useState(null);
  const [loi, setLoi] = useState(null);

  useEffect(() => {
    fetch(dongDau(`${CONTENT}/lop2/index.json`))
      .then((r) => r.json()).then(setIdx)
      .catch((e) => setLoi(String(e?.message || e)));
  }, []);

  const xong = progress?.lop2 || {};
  const tiep = useMemo(() => idx?.find((b) => !xong[b.id]) || null, [idx, xong]);

  if (loi) return <div className="p-6 text-alert">Không mở được chương trình lớp 2: {loi}</div>;
  if (!idx) return <div className="p-6 text-mute">Đang mở bài học…</div>;

  const theoChuong = {};
  for (const b of idx) (theoChuong[b.chuong] ??= []).push(b);
  const soXong = idx.filter((b) => xong[b.id]).length;

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
      <header className="bg-gradient-to-br from-teal to-[#7fe3d0] px-4 py-4">
        <div className="flex items-start gap-2">
          <div className="flex-1">
            <div className="text-[11px] font-extrabold tracking-widest text-teal-dark">
              MOBILUCK · KỸ SƯ NHÍ
            </div>
            <h1 className="mt-1 text-[21px] font-extrabold leading-snug text-teal-dark">
              Toán Tư Duy lớp 2
            </h1>
            <p className="mt-0.5 text-[13.5px] font-bold text-teal-dark opacity-85">
              Cùng Trí Long khám phá Vương quốc Số
            </p>
          </div>
          <button onClick={onDoiChuongTrinh}
                  className="shrink-0 rounded-full bg-white/70 px-2.5 py-1 text-[11.5px] font-bold text-teal-dark">
            đổi lớp
          </button>
        </div>
        <div className="mt-2.5 rounded-xl bg-white/70 px-3 py-2 text-[13.5px] font-bold text-teal-dark">
          Con đã học xong {soXong} trên {idx.length} bài 🌟
        </div>
      </header>

      {tiep && (
        <div className="px-3.5 pt-3.5">
          <div className="rounded-2xl bg-gold-pale px-4 py-3.5">
            <div className="text-[11px] font-extrabold tracking-widest text-gold-dark">
              BÀI TIẾP THEO CỦA CON
            </div>
            <h2 className="mt-1 text-[18px] font-bold leading-snug text-navy">
              Bài {tiep.so} · {tiep.ten}
            </h2>
            <button className="btn-gold mt-2.5" onClick={() => onMoBai(tiep.id)}>
              Bắt đầu học ▶
            </button>
          </div>
        </div>
      )}

      <div className="px-3.5 pt-3">
        {Object.entries(theoChuong).map(([ch, ds]) => (
          <section key={ch} className="card">
            <div className="kicker">CHƯƠNG {ch} · {ds[0].tenChuong}</div>
            {ds.map((b) => (
              <button key={b.id} onClick={() => onMoBai(b.id)}
                      className="mt-1.5 flex w-full items-center gap-2.5 rounded-xl border border-line px-3 py-2.5 text-left hover:bg-soft">
                <span className="text-[18px] leading-none">{xong[b.id] ? '🌟' : '⭕'}</span>
                <span className="flex-1">
                  <span className="block text-[15px] font-bold leading-snug text-navy">
                    Bài {b.so} · {b.ten}
                  </span>
                  <span className="block text-[12px] text-mute">{b.soCau} câu luyện tập</span>
                </span>
                <span className="text-[14px] text-mute">▶</span>
              </button>
            ))}
          </section>
        ))}
      </div>

      <ChanTrang />
    </div>
  );
}
