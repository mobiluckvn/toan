import React, { useEffect, useMemo, useState } from 'react';
import { CONTENT, dongDau, ghiNhoChuong, chuongTrinh as tra } from '../lib/content.js';
import ChanTrang from './ChanTrang.jsx';
import BangSuuTapSao from './BangSuuTapSao.jsx';
import DongDanhSach from './DongDanhSach.jsx';

/**
 * TRANG CHÍNH CỦA QUYỂN ĐỌC CHẬM — lớp 2 (33 bài) và lớp 3 (34 bài), 8 chương.
 *
 * Bé chưa đọc nhanh, nên KHÔNG khoá bài: khoá rồi giải thích vì sao là thêm chữ để
 * đọc, mà bé chưa có nhu cầu "mở khoá". Thay vào đó đánh dấu bài đã học bằng ngôi
 * sao, và luôn chỉ rõ "bài tiếp theo của con".
 *
 * MỌI THỨ RIÊNG CỦA TỪNG QUYỂN đọc từ sổ đăng ký: thư mục nội dung, tên quyển, phụ
 * đề. Bản đầu gõ cứng `content/lop2/` và tên "Toán Tư Duy lớp 2" ngay trong JSX, nên
 * mở lớp 3 ra là thấy đúng 33 bài của lớp 2 dưới cái tên lớp 2 — sai mà vẫn chạy êm.
 */
export default function HomeLop2({ progress, onMoBai, onDoiChuongTrinh, onSoPhuHuynh,
                                   onMoOnTap, chuongTrinh = 'lop2' }) {
  const [idx, setIdx] = useState(null);
  const [onTap, setOnTap] = useState([]);
  const [loi, setLoi] = useState(null);

  const ct = tra(chuongTrinh);
  const thuMuc = ct.thuMuc || 'lop2';

  useEffect(() => {
    fetch(dongDau(`${CONTENT}/${thuMuc}/index.json`))
      .then((r) => r.json())
      /* Chương của bài lớp 2 nằm trong dữ liệu chứ không suy ra bằng công thức như
         lớp 5 — ghi nhớ ngay khi nạp để chapterOf/allMicroIds dùng chung được. */
      .then((ds) => { ghiNhoChuong(ds); setIdx(ds); })
      .catch((e) => setLoi(String(e?.message || e)));
    // 8 bài ôn tập + 3 ải — dùng chung màn sát hạch với lớp 5
    fetch(dongDau(`${CONTENT}/${thuMuc}/ontap.json`))
      .then((r) => r.json()).then(setOnTap).catch(() => setOnTap([]));
  }, [thuMuc]);

  /* Dùng CHUNG sổ tiến độ với lớp 5 (progress.micros) thay vì sổ riêng
     progress.lop2 — một nguồn sự thật thì sổ phụ huynh và bảng cô giáo mới thấy
     được bài lớp 2. */
  const micros = progress?.micros || {};
  const xong = micros;
  const tiep = useMemo(() => idx?.find((b) => !micros[b.id]?.pass) || null, [idx, micros]);

  if (loi) return <div className="p-6 text-alert">Không mở được {ct.ten || 'chương trình'}: {loi}</div>;
  if (!idx) return <div className="p-6 text-mute">Đang mở bài học…</div>;

  const theoChuong = {};
  for (const b of idx) (theoChuong[b.chuong] ??= []).push(b);
  const soXong = idx.filter((b) => micros[b.id]?.pass).length;

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
      <header className="bg-gradient-to-br from-teal to-[#7fe3d0] px-4 py-4">
        <div className="flex items-start gap-2">
          <div className="flex-1">
            <div className="text-[11px] font-extrabold tracking-widest text-teal-dark">
              MOBILUCK · KỸ SƯ NHÍ
            </div>
            <h1 className="mt-1 text-[21px] font-extrabold leading-snug text-teal-dark">
              {ct.ten}
            </h1>
            <p className="mt-0.5 text-[13.5px] font-bold text-teal-dark opacity-85">
              {ct.phuDe}
            </p>
          </div>
          <div className="flex shrink-0 flex-col gap-1">
            <button onClick={onDoiChuongTrinh}
                    className="rounded-full bg-white/70 px-2.5 py-1 text-[11.5px] font-bold text-teal-dark">
              ← kệ sách
            </button>
            {/* Quyển đọc chậm dùng chung sổ học với lớp 5 — bố mẹ xem được con làm tới đâu */}
            <button onClick={onSoPhuHuynh}
                    className="rounded-full bg-white/70 px-2.5 py-1 text-[11.5px] font-bold text-teal-dark">
              sổ của con
            </button>
          </div>
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
        <BangSuuTapSao idx={idx} xong={xong} />

        {Object.entries(theoChuong).map(([ch, ds]) => (
          <section key={ch} className="card">
            <div className="kicker">CHƯƠNG {ch} · {ds[0].tenChuong}</div>
            {ds.map((b) => (
              <DongDanhSach
                key={b.id}
                bieuTuong={micros[b.id]?.pass ? '🌟' : micros[b.id]?.done ? '🔸' : '⭕'}
                tieuDe={`Bài ${b.so} · ${b.ten}`}
                phuDe={`${b.soCau} câu luyện tập${b.soQuiz ? ` · ${b.soQuiz} câu tự kiểm` : ''}`}
                onClick={() => onMoBai(b.id)}
              />
            ))}

            {/* Ôn tập của chương đứng NGAY SAU các bài của chương ấy — bé học xong
                chương là thấy ngay cửa ải, không phải đi tìm ở đâu khác. */}
            {onTap.filter((o) => o.loai === 'ontap' && o.so === Number(ch)).map((o) => {
              const kq = progress?.chapters?.[o.chapter];
              return (
                <DongDanhSach
                  key={o.id} kieu="nhan" mauChu="text-gold-dark"
                  bieuTuong={kq?.pass ? '🏅' : '🎯'}
                  tieuDe={o.name}
                  phuDe={`${o.soCau} câu · làm đúng ${o.need} câu là qua`
                         + (kq ? ` · lần trước ${kq.right}/${kq.total}` : '')}
                  onClick={() => onMoOnTap(o.chapter)}
                />
              );
            })}
          </section>
        ))}

        {/* Ba ải cuối sách — trộn đủ 8 chương */}
        {onTap.some((o) => o.loai === 'ai') && (
          <section className="card">
            <div className="kicker">🏰 BA CỬA ẢI CUỐI SÁCH</div>
            <p className="text-[13.5px] text-mute">Trộn đủ cả 8 chương. Làm lần lượt từ Ải 1.</p>
            {onTap.filter((o) => o.loai === 'ai').sort((a, b) => a.so - b.so).map((o) => {
              const kq = progress?.chapters?.[o.chapter];
              return (
                <DongDanhSach
                  key={o.id} 
                  bieuTuong={kq?.pass ? '⭐' : '🚪'}
                  tieuDe={o.name}
                  phuDe={`${o.soCau} câu · làm đúng ${o.need} câu là qua`
                         + (kq ? ` · lần trước ${kq.right}/${kq.total}` : '')}
                  onClick={() => onMoOnTap(o.chapter)}
                />
              );
            })}
          </section>
        )}
      </div>

      <ChanTrang />
    </div>
  );
}
