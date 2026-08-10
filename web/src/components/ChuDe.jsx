import React, { useEffect, useState } from 'react';
import { CONTENT, dongDau, chuongTrinhCua } from '../lib/content.js';
import DongDanhSach from './DongDanhSach.jsx';
import ChanTrang from './ChanTrang.jsx';

/**
 * HỌC THEO CHỦ ĐỀ — trục thứ hai của app.
 *
 * Kệ sách đi một chiều: quyển → chương → bài. Muốn luyện "dãy số" thì phải nhớ nó
 * nằm ở bài nào của quyển nào — mà cùng một chủ đề rải khắp bốn quyển, mỗi quyển
 * một tên chương khác nhau. Màn này đi theo chiều kia: chọn chủ đề trước, rồi thấy
 * ngay nó được dạy ở những lớp nào.
 *
 * Ba tầng: 5 mảng kiến thức → 34 chủ đề → 82 dạng bài, rồi tới THANG của một dạng.
 * Tất cả đọc từ `content/chu_de.json` (tools/dung_chu_de.py dựng) — thêm quyển mới
 * thì dựng lại bản đồ, màn này tự có, không phải sửa gì ở đây.
 *
 * THANG là thứ đáng tiền nhất: cùng một dạng bài xếp từ lớp thấp lên cao, nên con
 * (và bố mẹ) nhìn một cái là thấy "chỗ này con hổng từ lớp 3" — điều mà đi theo
 * quyển thì không bao giờ thấy được.
 */

/* Bảng màu thương hiệu chỉ có ba nền nhạt; 5 mảng thì lặp lại, và cố ý lặp theo
   thứ tự để hai mảng cạnh nhau không bao giờ trùng màu. */
const MAU = ['bg-teal-pale text-teal-dark', 'bg-gold-pale text-gold-dark',
             'bg-alert-pale text-alert', 'bg-soft text-navy',
             'bg-teal-pale text-teal-dark'];
const SO_MANG = ['I', 'II', 'III', 'IV', 'V'];

/** Bậc thang đã học xong chưa — mọi bài của bậc đều phải đạt. */
function xongBac(progress, bac) {
  const m = progress?.micros || {};
  return bac.bai.length > 0 && bac.bai.every((i) => m[i]?.pass);
}
function chamBac(progress, bac) {
  const m = progress?.micros || {};
  return bac.bai.some((i) => m[i]);
}

/** Huy hiệu các lớp một dạng bài có bài — "2 · 3 · 4 · 5", tô đậm lớp đã xong. */
function HuyHieuLop({ thang, progress }) {
  if (!thang.length) {
    return <span className="text-[11.5px] text-mute">chưa có bài</span>;
  }
  return (
    <span className="inline-flex gap-1">
      {thang.map((b) => {
        const xong = xongBac(progress, b);
        const cham = !xong && chamBac(progress, b);
        return (
          <span key={b.lop}
                className={`rounded px-1.5 py-0.5 text-[10.5px] font-extrabold ${
                  xong ? 'bg-teal text-white'
                       : cham ? 'bg-gold text-white' : 'bg-soft text-mute'}`}>
            {b.lop}
          </span>
        );
      })}
    </span>
  );
}

export default function ChuDe({ progress, onMoBai, onLuyen, onThoat, viTri = {} }) {
  const [bd, setBd] = useState(null);
  /* Khởi tạo từ `viTri`: con học xong một bài rồi quay về đây thì phải về ĐÚNG cái
     thang vừa đứng, chứ không phải về đầu màn rồi bấm lại ba tầng. Vị trí do App
     giữ trong `view.veLai`, vì state của component này mất khi rời màn. */
  const [maMang, setMaMang] = useState(viTri.maMang || null);
  const [maDang, setMaDang] = useState(viTri.maDang || null);
  const oDau = () => ({ maMang, maDang });

  useEffect(() => {
    fetch(dongDau(`${CONTENT}/chu_de.json`))
      .then((r) => r.json()).then(setBd).catch(() => setBd({ loi: true }));
  }, []);

  if (!bd) return <div className="p-6 text-mute">Đang mở bản đồ chủ đề…</div>;
  if (bd.loi) return <div className="p-6 text-alert">Không nạp được bản đồ chủ đề.</div>;

  const dsMang = SO_MANG.map((s) => bd.mang[`AREA:${s}`]).filter(Boolean);
  /* Trả CẶP [mã, dạng] chứ không riêng dạng: màn dưới cần mã để mở thang, mà dò
     ngược từ giá trị về khoá thì vừa chậm vừa sai khi hai dạng trùng nội dung. */
  const dangCua = (maCd) => (bd.chuDe[maCd]?.dang || [])
    .filter((k) => bd.dang[k]).map((k) => [k, bd.dang[k]]);

  const DauTrang = ({ tieuDe, phuDe, quayLai }) => (
    <header className="bg-navy px-4 py-4 text-white">
      <div className="flex items-start gap-2">
        <button onClick={quayLai} className="mt-0.5 text-[13px] opacity-90">← Quay lại</button>
        <div className="min-w-0 flex-1 text-center">
          <div className="text-[11px] font-extrabold tracking-widest text-gold">
            HỌC THEO CHỦ ĐỀ
          </div>
          <h1 className="mt-1 text-[19px] font-bold leading-snug">{tieuDe}</h1>
          {phuDe && <p className="mt-0.5 text-[12.5px] opacity-90">{phuDe}</p>}
        </div>
        <span className="w-[62px]" />
      </div>
    </header>
  );

  /* ── TẦNG 3 · THANG của một dạng bài ────────────────────────────────────── */
  if (maDang && bd.dang[maDang]) {
    const d = bd.dang[maDang];
    const cd = bd.chuDe[d.chuDe];
    const cb = d.soTruongHop?.CB || 0, nc = d.soTruongHop?.NC || 0;
    return (
      <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
        <DauTrang tieuDe={d.ten} phuDe={cd?.ten} quayLai={() => setMaDang(null)} />

        <div className="px-3.5 pt-3.5">
          <section className="card">
            <div className="kicker">
              THANG HỌC — TỪ LỚP THẤP LÊN CAO
              <span className="ml-2 font-normal normal-case tracking-normal text-mute">
                {cb} trường hợp cơ bản · {nc} nâng cao
              </span>
            </div>

            {d.thang.length === 0 && (
              <p className="mt-2 text-[14px] text-mute">
                Chủ đề này có trong ma trận nhưng chưa quyển nào dạy. Sẽ bổ sung ở
                các quyển sau.
              </p>
            )}

            {d.thang.map((b) => {
              const xong = xongBac(progress, b);
              return (
                <div key={b.lop}
                     className={`mt-2.5 rounded-2xl border-[1.5px] px-3.5 py-3 ${
                       xong ? 'border-teal bg-teal-pale' : 'border-line bg-white'}`}>
                  <div className="flex items-center gap-2">
                    <span className={`rounded-lg px-2 py-1 text-[12px] font-extrabold ${
                      xong ? 'bg-teal text-white' : 'bg-navy text-white'}`}>
                      LỚP {b.lop}
                    </span>
                    {xong && <span className="text-[12.5px] font-bold text-teal-dark">
                      con đã học xong bậc này
                    </span>}
                    {onLuyen && (
                      <button className="ml-auto rounded-lg bg-gold px-2.5 py-1 text-[12px] font-extrabold text-navy"
                              onClick={() => onLuyen(maDang, b.lop)}>
                        Luyện bậc này ▶
                      </button>
                    )}
                  </div>

                  {/* Lời giới thiệu đúng mức của lớp ấy — cùng một chủ đề mà lớp 2
                      học khác lớp 5, nói rõ ra thì bố mẹ chọn bậc mới trúng. */}
                  {d.moTaLop?.[String(b.lop)] && (
                    <p className="mt-2 text-[13.5px] leading-relaxed text-mute">
                      {d.moTaLop[String(b.lop)]}
                    </p>
                  )}

                  {b.bai.map((id, k) => (
                    <DongDanhSach
                      key={id}
                      bieuTuong={progress?.micros?.[id]?.pass ? '✅' : '📘'}
                      tieuDe={b.ten[k] || id}
                      phuDe={chuongTrinhCua(id) === 'lop5' ? 'Toán Tư Duy lớp 5' : null}
                      onClick={() => onMoBai(id, oDau())}
                    />
                  ))}
                </div>
              );
            })}
          </section>
        </div>
        <ChanTrang />
      </div>
    );
  }

  /* ── TẦNG 2 · chủ đề và dạng bài của một mảng ────────────────────────────── */
  if (maMang && bd.mang[maMang]) {
    const m = bd.mang[maMang];
    return (
      <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
        <DauTrang tieuDe={m.ten} quayLai={() => setMaMang(null)} />
        {(m.chuDe || []).map((maCd) => {
          const c = bd.chuDe[maCd];
          if (!c) return null;
          return (
            <div key={maCd} className="px-3.5 pt-3">
              <section className="card">
                <div className="kicker">{c.ten}</div>
                {dangCua(maCd).map(([ma, d]) => (
                    <button key={ma} onClick={() => setMaDang(ma)}
                            className="mt-1.5 flex w-full items-center gap-2.5 rounded-xl border border-line px-3 py-2.5 text-left hover:bg-soft">
                      <span className="min-w-0 flex-1">
                        <span className="block text-[14.5px] font-bold leading-snug text-navy">
                          {d.ten}
                        </span>
                        <span className="mt-1 block">
                          <HuyHieuLop thang={d.thang} progress={progress} />
                        </span>
                      </span>
                      <span className="text-[14px] text-mute">▶</span>
                    </button>
                ))}
              </section>
            </div>
          );
        })}
        <ChanTrang />
      </div>
    );
  }

  /* ── TẦNG 1 · 5 mảng kiến thức ───────────────────────────────────────────── */
  const demBac = (maM) => {
    const m = bd.mang[maM];
    let dang = 0, lui = 0;
    for (const maCd of m.chuDe || []) {
      for (const [, d] of dangCua(maCd)) {
        dang++;
        if ((d.thang || []).length >= 2) lui++;
      }
    }
    return { dang, lui, chuDe: (m.chuDe || []).length };
  };

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
      <header className="bg-navy px-4 py-4 text-white">
        <div className="flex items-start gap-2">
          <button onClick={onThoat} className="mt-0.5 text-[13px] opacity-90">← Kệ sách</button>
          <div className="min-w-0 flex-1 text-center">
            <div className="text-[11px] font-extrabold tracking-widest text-gold">
              MOBILUCK · KỸ SƯ NHÍ
            </div>
            <h1 className="mt-1 text-[21px] font-bold leading-snug">Học theo chủ đề</h1>
            <p className="mt-0.5 text-[12.5px] opacity-90">
              Chọn chủ đề rồi học xuyên các lớp — kém thì lùi xuống lớp dưới cùng chủ đề.
            </p>
          </div>
          <span className="w-[62px]" />
        </div>
      </header>

      <div className="px-3.5 pt-3.5">
        <section className="card">
          <div className="kicker">🗺️ NĂM MẢNG KIẾN THỨC</div>
          {dsMang.map((m, i) => {
            const ma = `AREA:${SO_MANG[i]}`;
            const { dang, lui, chuDe } = demBac(ma);
            return (
              <button key={ma} onClick={() => setMaMang(ma)}
                      className="mt-1.5 flex w-full items-center gap-2.5 rounded-xl border border-line px-3 py-3 text-left hover:bg-soft">
                <span className={`rounded-lg px-2 py-1 text-[12px] font-extrabold ${MAU[i]}`}>
                  {SO_MANG[i]}
                </span>
                <span className="min-w-0 flex-1">
                  <span className="block text-[15px] font-bold leading-snug text-navy">
                    {m.ten}
                  </span>
                  <span className="block text-[12px] text-mute">
                    {chuDe} chủ đề · {dang} dạng bài · {lui} dạng lùi được sang lớp dưới
                  </span>
                </span>
                <span className="text-[14px] text-mute">▶</span>
              </button>
            );
          })}
        </section>
      </div>
      <ChanTrang />
    </div>
  );
}
