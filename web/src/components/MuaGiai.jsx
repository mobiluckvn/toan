import React, { useEffect, useMemo, useState } from 'react';
import { CONTENT, dongDau, chapterOf } from '../lib/content.js';
import { moKhoa, chuongDaXong } from '../lib/dau.js';
import Chu from './Chu.jsx';
import ChanTrang from './ChanTrang.jsx';
import ThanhTren from './ThanhTren.jsx';

/**
 * MÙA GIẢI (Quyển 2) — trang chọn vòng đấu.
 *
 * Vòng n mở khi con học xong CHƯƠNG n của Quyển 1. Con học xen kẽ được: xong
 * chương 1 là vào luyện thi vòng 1 ngay, không phải đợi hết 168 micro.
 *
 * Khoá thì nói rõ VÌ SAO và còn thiếu mấy bài — ở Quyển 1 chúng tôi từng để danh
 * sách khoá im lặng, bố mẹ tưởng hỏng.
 */
const NHAN = { vong: 'VÒNG ĐẤU', detron: 'ĐỀ TRỘN', thithu: 'KỲ THI THỬ' };

export default function MuaGiai({ progress, onMo, onExit, onTrai, onHoSo, onThe, onVeKeSach }) {
  const [idx, setIdx] = useState(null);
  const [loi, setLoi] = useState(null);

  useEffect(() => {
    fetch(dongDau(`${CONTENT}/quyen2/index.json`))
      .then((r) => r.json()).then(setIdx)
      .catch((e) => setLoi(String(e?.message || e)));
  }, []);

  const xong = useMemo(
    () => chuongDaXong(progress?.micros || {}, chapterOf),
    [progress]);

  if (loi) return <div className="p-6 text-alert">Không mở được Mùa giải: {loi}</div>;
  if (!idx) return <div className="p-6 text-mute">Đang mở Mùa giải…</div>;

  /* Chỉ đếm bài QUYỂN 1. Sổ `micros` là sổ chung của bốn quyển, mà `chapterOf` là
     hàm chia chương của Quyển 1 — thả mã bài lớp 2·3·4 vào là chúng dồn hết về
     chương 1, và dòng "còn N bài nữa" báo sai số. Cùng một cái bẫy với
     `chuongDaXong`, chỉ khác chỗ ngồi. */
  const conThieu = (ch) => {
    const ms = Object.keys(progress?.micros || {}).filter((id) => id.startsWith('DL:KSN5Q1.'));
    const cua = 12 - ms.filter((id) => chapterOf(id) === ch && progress.micros[id]?.pass).length;
    return Math.max(0, cua);
  };

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
      {/* Hai lối ra khác nhau, và trước đây chỉ có một: "⌂ Về trang chính" đưa bé về
          trang lớp 5 chứ không về kệ sách, nên vào Mùa giải thẳng từ kệ sách là mắc kẹt
          một tầng. Nay tách rõ: ← Lớp 5 (quyển mẹ) và ⌂ Kệ sách (nhà). */}
      <ThanhTren
        nhan="QUYỂN 2 · LUYỆN THI"
        tieuDe="Mùa giải Vô địch"
        phuDe="14 vòng đấu · 4 đề trộn · 3 kỳ thi thử. Mỗi vòng có đồng hồ, chấm theo barem và một phiên tòa xử 12 cái bẫy của Cáo Đề."
        onQuayLai={onExit} nhanQuayLai="← Toán lớp 5"
        onVeNha={onVeKeSach}
      />

      <div className="px-3.5 pt-3.5">
        <div className="rounded-xl bg-gold-pale px-3.5 py-2.5 text-[13.5px] leading-relaxed text-gold-dark">
          <b>Vòng đấu mở dần theo Quyển 1:</b> học xong chương nào thì vòng đấu của
          chương ấy mở ra. Con không phải đợi hết cả quyển.
        </div>

        {/* Ba cửa phụ. Sách bắt học Khối 1 TRƯỚC khi đấu vòng 1, nên để ngay trên
            danh sách vòng chứ không giấu dưới đáy. */}
        <div className="mt-3 grid grid-cols-3 gap-2">
          {[['🎯', 'Trại huấn luyện', '5 bài kỹ năng', onTrai],
            ['🦊', 'Hồ sơ Cáo Đề', '168 bẫy', onHoSo],
            ['🗂', 'Thẻ chiến thuật', '14 thẻ', onThe]].map(([bt, ten, mo2, fn]) => (
            <button key={ten} onClick={fn}
                    className="rounded-2xl border-[1.5px] border-line bg-white px-2 py-2.5 text-center hover:border-navy">
              <div className="text-[20px] leading-none">{bt}</div>
              <div className="mt-1 text-[12.5px] font-bold leading-tight text-navy">{ten}</div>
              <div className="text-[11px] text-mute">{mo2}</div>
            </button>
          ))}
        </div>

        {idx.map((k) => {
          const mo = moKhoa(k, xong);
          return (
            <section key={k.id} className="card mt-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className={`rounded px-1.5 py-0.5 text-[11px] font-extrabold ${
                  k.loai === 'vong' ? 'bg-navy text-white'
                    : k.loai === 'detron' ? 'bg-gold text-gold-dark' : 'bg-alert text-white'}`}>
                  {NHAN[k.loai]} {k.so}
                </span>
                <span className="text-[11.5px] text-mute">
                  {k.soCau} câu · {k.phut} phút · đạt {k.dat}/{k.thang}
                </span>
              </div>
              <h3 className="mt-1 text-[16.5px] font-bold leading-snug text-navy"><Chu t={k.ten} /></h3>

              {mo ? (
                <button className="btn-go mt-2.5" onClick={() => onMo(k.id)}>
                  Vào thi đấu ▶
                </button>
              ) : (
                <div className="mt-2.5 rounded-xl bg-soft px-3 py-2.5 text-[13.5px] text-mute">
                  🔒 Mở khi con học xong <b>chương {k.chuongQ1}</b> của Quyển 1
                  {conThieu(k.chuongQ1) > 0 && <> — còn <b>{conThieu(k.chuongQ1)}</b> bài nữa</>}
                </div>
              )}
            </section>
          );
        })}
      </div>

      <ChanTrang />
    </div>
  );
}
