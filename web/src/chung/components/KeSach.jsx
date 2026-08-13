import React from 'react';
import { dsChuongTrinhSapXep, gomNhomKeSach } from '../lib/soQuyen.js';
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

/**
 * Tiến độ một quyển — HỎI MÔN, không tự đếm.
 *
 * Kệ sách không biết mã bài của môn nào trông ra sao, và nếu nó biết thì thêm môn thứ
 * hai là phải viết thêm một nhánh `if` ngay tại đây. Mỗi môn nộp `tienDoQuyen` theo
 * giao ước ở `src/soMon.js`; kệ sách chỉ vẽ.
 */
const rong = { xong: 0, dangLam: 0, tong: 0, phanTram: 0, gio: 0 };

export default function KeSach({ dangKy, mon = [], tienDo = {}, onMoQuyen, onMoCuaPhu,
                                onMoXepHang, onSoPhuHuynh, account = {} }) {
  /* Tra môn theo mã, để hỏi đúng môn về tiến độ của quyển nó sở hữu. */
  const hoSoMon = (ma) => mon.find((m) => m.ma === ma);
  const doTien = (ct) => {
    const m = hoSoMon(ct.mon);
    return m ? { ...rong, ...m.tienDoQuyen(tienDo[m.ma], ct) } : rong;
  };
  const dk = dangKy || {};
  /* XẾP THEO `thuTu`, không theo thứ tự khai trong tệp. Sổ vốn khai theo thứ tự làm
     xong quyển (lop2, lop5, lop5q2, lop3, lop4), nên kệ sách hiện lớp 5 và Mùa giải
     chen vào giữa lớp 2 và lớp 3 — bố mẹ nhìn vào không đọc ra được đường đi.
     Đúng thứ tự trải nghiệm: lớp 2 → 3 → 4 → 5 → tổng ôn lớp 5. */
  const dsCt = dk.chuongTrinh
    ? Object.values(dk.chuongTrinh).slice()
        .sort((a, b) => (a.thuTu ?? 99) - (b.thuTu ?? 99)
                        || String(a.ma).localeCompare(String(b.ma)))
    : dsChuongTrinhSapXep();
  const ds = dsCt.map((ct) => ({ ct, td: doTien(ct) }));
  /* Quyển động vào gần đây nhất lên đầu — mở app ra là bấm học tiếp được ngay,
     không phải đi tìm. Chưa học gì thì không hiện thẻ này. */
  const monCua = (ma) => (dk.mon || {})[ma] || { ten: ma, bieuTuong: '📘' };

  /* Luật gom nhóm nằm ở `soQuyen.js` để cổng chạy được bằng node — đọc phần đầu
     hàm ấy là đủ hiểu ba việc nó lo. Ở đây chỉ vẽ. */
  const dsNhom = gomNhomKeSach(ds, mon, (ma) => monCua(ma).ten, (ma) => monCua(ma).bieuTuong);

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
          </div>
        </div>

        {/* ĐANG LÀ AI — trước đây chỗ này chỉ có mỗi chữ "thoát" bé xíu, không hề nói
            tên. Máy tính bảng dùng chung cả nhà thì câu hỏi đầu tiên của bố mẹ là
            "đang mở tài khoản của đứa nào" — phải trả lời ngay trên đầu màn hình.
            Bấm vào là mở hồ sơ: đổi tên, đổi lớp, đổi biệt danh, đổi bé. */}
        {account.signedIn && (
          <button onClick={account.onHoSo}
                  className="mt-3 flex w-full items-center gap-2.5 rounded-xl bg-navy-light px-3 py-2 text-left">
            <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-white text-[13px] font-extrabold text-navy">
              {(account.name || '?').trim().charAt(0).toUpperCase() || '?'}
            </span>
            <span className="min-w-0 flex-1">
              <b className="block truncate text-[13px] leading-tight">{account.name}</b>
              <span className="block text-[11px] leading-tight opacity-80">
                {account.lop ? `Lớp ${account.lop}` : 'chưa chọn lớp'}
                {account.soNguoi > 1 ? ` · ${account.soNguoi} bé trên máy này` : ''}
              </span>
            </span>
            <span className="shrink-0 text-[11px] opacity-80">hồ sơ ▸</span>
          </button>
        )}

        {/* CHƯA ĐĂNG NHẬP — phải có đường quay lại, ngay trên trang chính.
            Trước đây nút đăng nhập CHỈ nằm trong trang của một quyển. Bé bấm "Để sau
            — cho con học thử trước" là rơi thẳng vào kệ sách, và từ đó không còn cửa
            nào để đăng nhập: phải mở đại một quyển ra mới thấy. Bố mẹ ngồi tìm không
            ra, tưởng app hỏng — mà bài con học thì vẫn nằm nguyên ở máy, không lên
            mạng, đổi máy là mất. */}
        {account.available && !account.signedIn && account.onSignIn && (
          <button onClick={account.onSignIn}
                  className="mt-3 flex w-full items-center gap-2.5 rounded-xl bg-gold-pale px-3 py-2 text-left">
            <span className="text-[16px]">☁️</span>
            <span className="min-w-0 flex-1">
              <b className="block text-[12.5px] leading-tight text-gold-dark">
                Bài đang lưu ở máy này thôi
              </b>
              <span className="block text-[11px] leading-tight text-gold-dark opacity-80">
                Đăng nhập để lưu lên mạng — đổi máy vẫn còn, thầy cô theo dõi được.
              </span>
            </span>
            <span className="shrink-0 text-[11.5px] font-bold text-gold-dark">Đăng nhập ▸</span>
          </button>
        )}
      </header>

      {/* BẢNG XẾP HẠNG — chỗ các con nhìn thấy nhau.
          Đứng TRÊN kệ sách: đây là thứ thúc bé mở app, giấu dưới đáy trang thì bé
          không bao giờ cuộn tới. Nó cắt ngang MỌI môn nên không thuộc nhóm nào. */}
      {onMoXepHang && (
        <div className="px-3.5 pt-3">
          <button onClick={onMoXepHang}
                  className="flex w-full items-center gap-3 rounded-2xl border-[1.5px] border-gold bg-gold-pale px-4 py-3.5 text-left">
            <span className="text-[24px] leading-none">🏆</span>
            <span className="min-w-0 flex-1">
              <span className="block text-[16px] font-bold leading-snug text-navy">
                Bảng xếp hạng
              </span>
              <span className="block text-[12.5px] text-mute">
                Xem các bạn học tới đâu — và còn bao xa nữa thì con đuổi kịp
              </span>
            </span>
            <span className="text-[14px] text-mute">▶</span>
          </button>
        </div>
      )}

      {dsNhom.map((nh) => (
          <div key={nh.ten} className="px-3.5 pt-3">
            <section className="card">
              <div className="kicker">{nh.bieuTuong} {nh.ten.toUpperCase()}</div>

              {/* Chỗ bấm to nhất của nhóm — đứng ngay dưới tên nhóm. */}
              {nh.tiep && (
                <div className="mt-1.5 rounded-xl bg-gold-pale px-3.5 py-3">
                  <div className="text-[11px] font-extrabold tracking-widest text-gold-dark">
                    HỌC TIẾP
                  </div>
                  <h2 className="mt-0.5 flex items-center gap-2 text-[17px] font-bold leading-snug text-navy">
                    <span className="text-[22px] leading-none">{nh.tiep.ct.bieuTuong}</span>
                    {nh.tiep.ct.ten}
                  </h2>
                  {/* Mới mở bài mà chưa đạt bài nào thì đừng khoe "xong 0 bài" — nghe
                      như con chưa làm gì, trong khi con vừa ngồi học xong. */}
                  <p className="mt-0.5 text-[13px] text-mute">
                    {nh.tiep.td.xong > 0
                      ? `Con đã học xong ${nh.tiep.td.xong} trên ${nh.tiep.td.tong} ${nh.tiep.ct.donVi || 'bài'}`
                      : 'Con đang học dở quyển này'}
                  </p>
                  <button className="btn-gold mt-2.5" onClick={() => onMoQuyen(nh.tiep.ct.ma)}>
                    Học tiếp ▶
                  </button>
                </div>
              )}

              {nh.sach.map(({ ct, td }) => (
                <button key={ct.ma} onClick={() => onMoQuyen(ct.ma)}
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

              {/* Lối học khác của CHÍNH mấy quyển ở trên. Đứng sau danh sách sách —
                  kệ sách thì sách phải đứng trước — nhưng giữ viền xanh riêng để
                  không bị đọc nhầm thành quyển thứ năm. */}
              {nh.cua.map(({ m, c }) => (
                <button key={`${m.ma}:${c.trang}`} onClick={() => onMoCuaPhu?.(m.ma, c.trang)}
                        className="mt-1.5 flex w-full items-center gap-2.5 rounded-xl border-[1.5px] border-teal bg-teal-pale px-3 py-2.5 text-left hover:brightness-95">
                  <span className="text-[22px] leading-none">{c.bieuTuong}</span>
                  <span className="min-w-0 flex-1">
                    <span className="block text-[15px] font-bold leading-snug text-navy">{c.ten}</span>
                    <span className="block text-[12px] text-mute">{c.mo}</span>
                  </span>
                  <span className="text-[14px] text-mute">▶</span>
                </button>
              ))}
            </section>
          </div>
      ))}

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
