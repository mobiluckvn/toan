import React, { useEffect, useState } from 'react';
import Chu from './Chu.jsx';
import { CONTENT, dongDau } from '../lib/content.js';

/**
 * KHỐI 1 · TRẠI HUẤN LUYỆN — 5 bài kỹ năng phòng thi (T1–T5).
 *
 * Sách bắt học Khối 1 TRƯỚC khi đấu vòng 1: đây là kỹ năng nền (đọc đề, trình bày
 * ăn điểm, quản trị thời gian, săn bẫy, tâm lý). Không dạy toán mới, dạy cách BIẾN
 * nội công thành điểm.
 *
 * Không có câu hỏi đánh số nên không chấm — con đọc và tập theo. Vì thế màn này để
 * đọc, gấp mở từng mục, chứ không dựng thành bài kiểm tra giả tạo.
 */
export default function TraiHuanLuyen({ onExit }) {
  const [bai, setBai] = useState(null);
  const [loi, setLoi] = useState(null);
  const [chon, setChon] = useState(0);
  const [mo, setMo] = useState({});

  useEffect(() => {
    fetch(dongDau(`${CONTENT}/quyen2/bai_ky_nang.json`))
      .then((r) => r.json()).then(setBai)
      .catch((e) => setLoi(String(e?.message || e)));
  }, []);
  useEffect(() => { window.scrollTo(0, 0); setMo({}); }, [chon]);

  if (loi) return <div className="p-6 text-alert">Không mở được trại huấn luyện: {loi}</div>;
  if (!bai) return <div className="p-6 text-mute">Đang mở trại huấn luyện…</div>;

  const b = bai[chon];

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-16">
      <header className="sticky top-0 z-20 bg-navy px-3.5 py-2.5 text-white">
        <div className="flex items-center gap-2.5">
          <button onClick={onExit}
                  className="rounded-full border border-white/40 px-2 py-0.5 text-[11px] font-bold">
            ← Mùa giải
          </button>
          <span className="text-[11px] font-extrabold tracking-widest text-gold">
            KHỐI 1 · TRẠI HUẤN LUYỆN
          </span>
        </div>
        <div className="mt-2 flex gap-1.5 overflow-x-auto">
          {bai.map((x, k) => (
            <button key={x.ma} onClick={() => setChon(k)}
                    className={`shrink-0 rounded-full px-2.5 py-1 text-[11.5px] font-extrabold ${
                      k === chon ? 'bg-gold text-gold-dark' : 'bg-white/15 text-white'}`}>
              {x.ma}
            </button>
          ))}
        </div>
      </header>

      <div className="px-3.5 pt-3.5">
        <div className="card">
          <div className="kicker">BÀI KỸ NĂNG {b.ma}</div>
          <h2 className="text-[19px] font-bold leading-snug text-navy"><Chu t={b.ten} /></h2>
          {b.phuDe && <p className="mt-1 text-[14px] text-mute">{b.phuDe}</p>}
        </div>

        {b.muc.map((m, k) => {
          const dangMo = mo[k] ?? k < 2;      // hai mục đầu mở sẵn, còn lại gấp cho đỡ ngợp
          return (
            <section key={k} className="card">
              <button className="flex w-full items-start gap-2 text-left"
                      onClick={() => setMo({ ...mo, [k]: !dangMo })}>
                {m.so && <span className="text-[17px] leading-none text-gold-dark">{m.so}</span>}
                <span className="flex-1 text-[15.5px] font-bold leading-snug text-navy">
                  {m.ten || 'Mở đầu'}
                </span>
                <span className="text-[13px] text-mute">{dangMo ? '▲' : '▼'}</span>
              </button>
              {dangMo && m.dong.map((d, i) => (
                <p key={i} className="mt-2 text-[15px] leading-relaxed">{d}</p>
              ))}
            </section>
          );
        })}

        <div className="card bg-gold-pale">
          <p className="text-[14.5px] leading-relaxed text-gold-dark">
            Học hết cả năm bài {bai.map((x) => x.ma).join(' · ')} rồi hãy vào vòng đấu —
            sách xếp Khối 1 trước là có lý do: bốn quy trình này dùng ở <b>mọi</b> vòng.
          </p>
        </div>
      </div>
    </div>
  );
}
