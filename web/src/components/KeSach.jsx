import React from 'react';
import { chuongTrinhCua } from '../lib/content.js';
import ChanTrang from './ChanTrang.jsx';
import DongDanhSach from './DongDanhSach.jsx';

/**
 * KỆ SÁCH — màn đầu tiên khi mở app.
 *
 * Trước đây màn này là "Con học lớp mấy?": chọn MỘT lớp, app nhớ, lần sau vào
 * thẳng, muốn sang lớp khác phải bấm "đổi lớp". Với hai chương trình thì tạm ổn;
 * với Toán 12 lớp cộng bốn môn nữa cộng các đề luyện thi thì hỏng hẳn — con không
 * thấy mình đang học dở những gì, và "đổi lớp" nghe như phải bỏ cái này lấy cái kia.
 *
 * Nay kệ sách LÀ trang chính: mở app ra là thấy mình đang học dở đến đâu ở từng
 * quyển, rồi tự chọn học tiếp quyển nào. Không có khái niệm "lớp đang chọn" nữa.
 *
 * Mọi chương trình đọc từ data/chuong_trinh.json — thêm lớp mới hay môn mới thì
 * thêm một mục ở đó, màn này tự hiện, không phải sửa gì ở đây.
 */
const VACH = { navy: 'bg-navy', teal: 'bg-teal', gold: 'bg-gold', tim: 'bg-[#7E57C2]' };

function tienDo(progress, ct) {
  const micros = progress?.micros || {};
  const cua = Object.entries(micros).filter(([id]) => chuongTrinhCua(id) === ct.ma);
  const xong = cua.filter(([, m]) => m.pass).length;
  const dangLam = cua.length;
  const tong = ct.soBai || cua.length || 1;
  const gio = cua.reduce((s, [, m]) => Math.max(s, Date.parse(m.at || 0) || 0), 0);
  return { xong, dangLam, tong, phanTram: Math.round((xong / tong) * 100), gio };
}

export default function KeSach({ dangKy, progress, onMoChuongTrinh, onSoPhuHuynh,
                                account = {} }) {
  const dk = dangKy || {};
  const ds = Object.values(dk.chuongTrinh || {}).map((ct) => ({ ct, td: tienDo(progress, ct) }));
  /* Quyển động vào gần đây nhất lên đầu — mở app ra là bấm học tiếp được ngay,
     không phải đi tìm. Chưa học gì thì không hiện thẻ này. */
  const dangHoc = ds.filter((x) => x.td.dangLam > 0).sort((a, b) => b.td.gio - a.td.gio);
  const ganNhat = dangHoc[0] || null;
  const theoMon = {};
  for (const x of ds) (theoMon[x.ct.mon] ??= []).push(x);

  const monCua = (ma) => (dk.mon || {})[ma] || { ten: ma, bieuTuong: '📘' };

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
      <header className="bg-navy px-4 py-4 text-white">
        <div className="flex items-start gap-2">
          <div className="flex-1">
            <div className="text-[11px] font-extrabold tracking-widest text-gold">
              MOBILUCK · KỸ SƯ NHÍ
            </div>
            <h1 className="mt-1 text-[21px] font-bold leading-snug">Kệ sách của con</h1>
            <p className="mt-0.5 text-[13px] opacity-90">
              Con đang học dở những quyển này — chọn quyển nào học tiếp cũng được.
            </p>
          </div>
          <div className="mt-1 flex shrink-0 flex-col items-end gap-1">
            <button onClick={onSoPhuHuynh}
                    className="rounded-full bg-navy-light px-2.5 py-1 text-[11px] font-bold">
              📖 Sổ bố mẹ
            </button>
            {account.signedIn && (
              <button onClick={account.onSignOut} className="text-[10.5px] opacity-75 underline">
                thoát
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Học tiếp quyển vừa học dở — chỗ bấm to nhất màn hình */}
      {ganNhat && (
        <div className="px-3.5 pt-3.5">
          <div className="rounded-2xl bg-gold-pale px-4 py-3.5">
            <div className="text-[11px] font-extrabold tracking-widest text-gold-dark">
              HỌC TIẾP
            </div>
            <h2 className="mt-1 flex items-center gap-2 text-[18px] font-bold leading-snug text-navy">
              <span className="text-[22px] leading-none">{ganNhat.ct.bieuTuong}</span>
              {ganNhat.ct.ten}
            </h2>
            {/* Mới mở bài mà chưa đạt bài nào thì đừng khoe "xong 0 bài" — nghe như
                con chưa làm gì, trong khi con vừa ngồi học xong. */}
            <p className="mt-0.5 text-[13px] text-mute">
              {ganNhat.td.xong > 0
                ? `Con đã học xong ${ganNhat.td.xong} trên ${ganNhat.td.tong} bài`
                : 'Con đang học dở quyển này'}
            </p>
            <button className="btn-gold mt-2.5" onClick={() => onMoChuongTrinh(ganNhat.ct.ma)}>
              Học tiếp ▶
            </button>
          </div>
        </div>
      )}

      {Object.entries(theoMon).map(([ma, xs]) => {
        const m = monCua(ma);
        return (
          <div key={ma} className="px-3.5 pt-3">
            <section className="card">
              <div className="kicker">{m.bieuTuong} {m.ten.toUpperCase()}</div>
              {xs.map(({ ct, td }) => (
                <button key={ct.ma} onClick={() => onMoChuongTrinh(ct.ma)}
                        className="mt-1.5 flex w-full items-center gap-2.5 rounded-xl border border-line px-3 py-2.5 text-left hover:bg-soft">
                  <span className="text-[22px] leading-none">{ct.bieuTuong}</span>
                  <span className="min-w-0 flex-1">
                    <span className="block text-[15px] font-bold leading-snug text-navy">
                      {ct.ten}
                    </span>
                    <span className="block text-[12px] text-mute">
                      {/* Đơn vị đếm khai ở sổ đăng ký: mùa giải đếm bằng vòng đấu,
                          ghi "26 bài" cho một thứ không có bài nào là sai hẳn. */}
                      {td.xong > 0
                        ? `đã học xong ${td.xong} trên ${td.tong} ${ct.donVi || 'bài'}`
                        : td.dangLam > 0
                          ? `đang học dở · ${td.tong} ${ct.donVi || 'bài'}`
                          : `${td.tong} ${ct.donVi || 'bài'} · ${ct.doTuoi || ''}`}
                    </span>
                    {/* Vạch tiến độ chỉ hiện khi ĐÃ học — vạch 0% chỉ làm con nản */}
                    {td.xong > 0 && (
                      <span className="mt-1 block h-1.5 w-full overflow-hidden rounded-full bg-soft">
                        <i className={`block h-full ${VACH[monCua(ct.mon).mau] || 'bg-teal'}`}
                           style={{ width: `${Math.max(td.phanTram, 3)}%` }} />
                      </span>
                    )}
                  </span>
                  <span className="text-[14px] text-mute">▶</span>
                </button>
              ))}
            </section>
          </div>
        );
      })}

      {/* Sắp có — cho con và bố mẹ thấy đường đi phía trước. Không bấm được,
          và nói THẲNG là chưa có, để không ai bấm mãi rồi tưởng app hỏng. */}
      {(dk.sapCo || []).length > 0 && (
        <div className="px-3.5 pt-3">
          <section className="card">
            <div className="kicker">🌱 SẮP CÓ</div>
            {(dk.sapCo || []).map((s, i) => (
              <DongDanhSach key={i} khoa bieuTuong={monCua(s.mon).bieuTuong}
                            tieuDe={s.nhom} phuDe={s.ten} />
            ))}
          </section>
        </div>
      )}

      {(dk.luyenThi || []).length > 0 && (
        <div className="px-3.5 pt-3">
          <section className="card">
            <div className="kicker">🏁 ÔN THI</div>
            {(dk.luyenThi || []).map((s) => (
              <DongDanhSach key={s.ma} khoa={s.trangThai !== 'dangCo'}
                            bieuTuong={s.bieuTuong} tieuDe={s.ten}
                            phuDe={s.trangThai === 'dangCo' ? s.mo : `${s.mo} · sắp có`} />
            ))}
          </section>
        </div>
      )}

      <ChanTrang />
    </div>
  );
}
