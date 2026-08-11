import React, { useEffect, useMemo, useState } from 'react';
import { napChiMuc, chuongTrinh as tra } from '../lib/content.js';
import { modeOf, resumeSpot, ketQuaChuong } from '../lib/progress.js';
import { hocBaQuyen, trangThaiBai, NHAN_TRANG_THAI, NHAN_MUC_CHUONG } from '../lib/hocba.js';
import ThanhTren from './ThanhTren.jsx';
import ChanTrang from './ChanTrang.jsx';
import DongDanhSach from './DongDanhSach.jsx';
import BangSuuTapSao from './BangSuuTapSao.jsx';

/**
 * TRANG CHÍNH CỦA MỘT QUYỂN — MỘT màn cho cả bốn quyển.
 *
 * ── VÌ SAO GỘP ──
 * Trước đây có hai tệp: `Home.jsx` (lớp 5) và `HomeLop2.jsx` (lớp 2·3·4). Ghi chú cũ
 * trong `DongDanhSach.jsx` nói cố ý tách, vì hai quyển khác nhau "mười điểm chính
 * sách". Đúng lúc chỉ có hai quyển. Với bốn quyển thì cái giá lộ ra: cùng là "trang
 * chính của một quyển sách" mà bé gặp hai app khác nhau — một bên có thẻ việc hôm
 * nay, chương gập mở được, giải thích vì sao khoá; bên kia chỉ có một danh sách
 * phẳng và đúng một thẻ "bài tiếp theo" cho cả 44 bài. Mở chương 6 của lớp 4 ra thì
 * không có gì chỉ cho bé biết bắt đầu từ đâu.
 *
 * Nay một màn, và MƯỜI ĐIỂM KHÁC BIỆT ẤY ĐỌC TỪ DỮ LIỆU chứ không từ tên quyển:
 *   · `ct.khoaBai`  — khoá bài tuần tự (chỉ lớp 5)
 *   · `ct.quyen2`   — có cửa sang quyển luyện thi không (chỉ lớp 5)
 *   · `chiMuc.ai`   — ba cửa ải cuối sách (chỉ lớp 2·3)
 *   · `chuong[].onTap` — kỳ ôn tập của chương (cả bốn quyển, đã dựng cho lớp 5)
 * Thêm quyển thứ năm thì khai mấy cờ ấy trong `data/chuong_trinh.json`, không sửa
 * tệp này.
 *
 * ── BA CÂU MÀN NÀY PHẢI TRẢ LỜI ──
 *   1. con đang học cái gì   → thẻ VIỆC CỦA CON, và vạch tiến độ ở đầu trang;
 *   2. nên học tiếp cái gì   → mỗi chương có DÒNG ĐỀ XUẤT riêng, không chỉ cả quyển
 *                              một dòng: chưa học chương nào thì đó là bài ĐẦU chương,
 *                              đang học dở thì đó là chỗ dở, học rồi thì là bài kế;
 *   3. về nhà bằng đường nào → ⌂ Kệ sách ở đúng một chỗ trên mọi màn (ThanhTren).
 */

const CHAM = {
  dat: 'bg-teal', dangDo: 'bg-gold', chuaDat: 'bg-alert', mo: 'bg-navy-light', khoa: 'bg-line',
};
const BIEU_TUONG = { dat: '🌟', dangDo: '⏳', chuaDat: '🔸', mo: '⭕', khoa: '🔒' };
const MAU_MUC = {
  master: 'bg-teal text-white', xongBai: 'bg-gold text-gold-dark',
  dangHoc: 'bg-navy-light text-white', chuaHoc: 'bg-soft text-mute',
};

const VI_SAO = {
  dangDo: 'Con đang học dở bài này',
  chuaDat: 'Bài này con chưa qua câu bẫy — làm lại nhé',
  moi: 'Việc của con bây giờ',
};

/**
 * Dòng mô tả một kỳ ôn tập.
 *
 * `need` CÓ THỂ VẮNG — ba cửa ải của lớp 3 không đặt ngưỡng, sách chỉ bảo "làm hết
 * 10 câu". Bản cũ ghép chuỗi thẳng nên bé đọc được đúng chữ **“làm đúng null câu là
 * qua”** trên màn hình. Hợp lệ về dữ liệu, cổng vẫn xanh, chỉ có bé là chịu.
 */
const loiKy = (o, lanTruoc) =>
  `${o.soCau} câu · ${o.need ? `làm đúng ${o.need} câu là qua` : 'làm hết là qua'}`
  + (lanTruoc?.tong ? ` · lần trước ${lanTruoc.dung}/${lanTruoc.tong}` : '');

export default function HomeQuyen({
  progress, chuongTrinh, onMoBai, onMoOnTap, onSoPhuHuynh, onVeKeSach,
  onMoMuaGiai, onMoXepHang, onSetMode, account = {},
}) {
  const ct = tra(chuongTrinh);
  const [chiMuc, setChiMuc] = useState(null);
  const [loi, setLoi] = useState(null);
  const [mo, setMo] = useState(null);          // chương đang bung
  const [viSaoKhoa, setViSaoKhoa] = useState(null);

  useEffect(() => {
    let song = true;
    setChiMuc(null); setLoi(null);
    napChiMuc(chuongTrinh)
      .then((d) => { if (song) setChiMuc(d); })
      .catch((e) => song && setLoi(String(e?.message || e)));
    return () => { song = false; };
  }, [chuongTrinh]);

  const hb = useMemo(
    () => (chiMuc ? hocBaQuyen(chiMuc, progress, { khoaBai: !!ct.khoaBai }) : null),
    [chiMuc, progress, ct.khoaBai]);

  /* Bung sẵn chương có việc — mở app ra là thấy ngay chỗ cần làm, không phải bấm dò.
     Chỉ đặt khi CHƯA chọn tay, nếu không thì bé bấm gập chương lại là nó tự bung ra. */
  useEffect(() => {
    if (mo === null && hb?.deXuat?.chuong) setMo(hb.deXuat.chuong.so);
  }, [hb, mo]);

  if (loi) return <div className="p-6 text-alert">Không mở được {ct.ten}: {loi}</div>;
  if (!hb) return <div className="p-6 text-mute">Đang mở bài học…</div>;

  const list = chiMuc.bai.map((b) => b.id);
  const dx = hb.deXuat;
  const cheDo = modeOf(progress);

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
      <ThanhTren
        nhan="MOBILUCK · KỸ SƯ NHÍ"
        tieuDe={`${ct.bieuTuong || '📘'} ${ct.ten}`}
        phuDe={ct.phuDe}
        onVeNha={onVeKeSach}
        phai={(
          <>
            {onMoXepHang && (
              <button onClick={onMoXepHang}
                      className="rounded-full bg-gold px-2.5 py-1 text-[11px] font-bold text-navy">
                🏆 Xếp hạng
              </button>
            )}
            <button onClick={onSoPhuHuynh}
                    className="rounded-full bg-navy-light px-2.5 py-1 text-[11px] font-bold">
              📖 Sổ bố mẹ
            </button>
            {account.signedIn && (
              <button onClick={account.onSignOut} className="text-[10.5px] opacity-75 underline">
                thoát
              </button>
            )}
          </>
        )}
      >
        {/* Ngày đầu chưa có gì để khoe — "0/168" chỉ làm con nản. */}
        {hb.daBatDau ? (
          <>
            <div className="mt-3 flex items-center gap-3">
              <div className="h-2 flex-1 overflow-hidden rounded-full bg-navy-deep">
                <i className="block h-full bg-gradient-to-r from-teal to-gold"
                   style={{ width: `${hb.phanTram}%` }} />
              </div>
              <span className="text-[12px] tabular-nums">{hb.datBai}/{hb.tongBai} bài</span>
            </div>
            <div className="mt-1.5 text-[12px] opacity-90">
              🏅 {hb.huyHieu}/{hb.tongChuong} huy hiệu chương
              {hb.masterChuong > 0 && ` · ⭐ ${hb.masterChuong} chương đã master`}
            </div>
          </>
        ) : (
          <p className="mt-2.5 text-[13px] leading-relaxed opacity-90">
            Con học từng bài nhỏ. Học xong một bài là bài tiếp theo hiện ra ngay.
          </p>
        )}
      </ThanhTren>

      {/* ══ VIỆC CỦA CON BÂY GIỜ ══ */}
      {dx && (
        <div className="px-3.5 pt-3.5">
          <section className="overflow-hidden rounded-2xl bg-white shadow-[0_3px_16px_rgba(12,59,112,.10)]">
            <div className="bg-gold px-4 py-2 text-[12px] font-extrabold tracking-wide text-gold-dark">
              {hb.daBatDau ? VI_SAO[dx.viSao] : 'Bắt đầu từ đây nhé!'}
            </div>
            <div className="px-4 pt-3.5">
              <h2 className="text-[17px] font-bold leading-snug text-navy">
                Bài {dx.bai.so}{dx.bai.micro > 1 ? `.${dx.bai.micro}` : ''} · {dx.bai.ten}
              </h2>
              <p className="mt-1 text-[12.5px] text-mute">
                Chương {dx.chuong.so} · {dx.chuong.ten}
                {dx.bai.durationMinutes ? ` · khoảng ${dx.bai.durationMinutes} phút` : ''}
              </p>
              {(() => {
                const spot = resumeSpot(progress, dx.bai.id);
                return spot ? (
                  <p className="mt-2.5 rounded-xl bg-teal-pale px-3 py-2 text-[13px] font-semibold text-teal-dark">
                    Con làm đến bước {spot.step + 1} rồi — mở lại là vào đúng chỗ cũ.
                  </p>
                ) : null;
              })()}
            </div>
            <div className="flex gap-2.5 px-4 pb-4 pt-3">
              <button className="btn-gold flex-1" onClick={() => onMoBai(dx.bai.id)}>
                {resumeSpot(progress, dx.bai.id) ? 'Học tiếp ▶' : 'Bắt đầu học ▶'}
              </button>
              {resumeSpot(progress, dx.bai.id) && (
                <button className="btn-ghost w-auto whitespace-nowrap px-3.5"
                        onClick={() => onMoBai(dx.bai.id, { fromStart: true })}>
                  Từ đầu
                </button>
              )}
            </div>
          </section>
        </div>
      )}

      {hb.xongQuyen && (
        <div className="px-3.5 pt-3.5">
          <div className="rounded-2xl border-[1.5px] border-teal bg-teal-pale px-4 py-3.5">
            <b className="text-[15px] text-teal-dark">🎉 Con đã học xong cả quyển!</b>
            <p className="mt-0.5 text-[13px] text-mute">
              Còn kỳ sát hạch nào chưa qua thì thi nốt để lấy đủ huy hiệu nhé.
            </p>
          </div>
        </div>
      )}

      {/* Kỳ sát hạch đang chờ — học xong chương mà không chốt thì huy hiệu treo mãi */}
      {hb.kyChoNo && (
        <button className="mx-3.5 mt-3.5 w-[calc(100%-1.75rem)] rounded-2xl bg-alert px-4 py-3 text-left text-white"
                onClick={() => onMoOnTap(hb.kyChoNo.onTap[0].chapter)}>
          <b className="text-[14.5px]">⚔ Kỳ sát hạch chương {hb.kyChoNo.so} đang chờ</b>
          <p className="text-[12.5px] opacity-90">Con đã học hết chương — thi lấy huy hiệu nhé!</p>
        </button>
      )}

      {/* Chưa đăng nhập thì phải nói THẲNG là bài đang nằm ở máy này */}
      {account.available && !account.signedIn && account.onSignIn && (
        <button onClick={account.onSignIn}
                className="mx-3.5 mt-3.5 flex w-[calc(100%-1.75rem)] items-center gap-2.5 rounded-2xl border-[1.5px] border-gold bg-gold-pale px-4 py-3 text-left">
          <span className="text-[18px]">☁️</span>
          <span className="flex-1">
            <b className="block text-[14px] text-gold-dark">Bài đang lưu ở máy này thôi</b>
            <span className="text-[12.5px] text-mute">
              Đăng nhập để lưu lên mạng — thầy cô theo dõi được, đổi máy vẫn còn.
            </span>
          </span>
          <span className="text-[13px] font-bold text-gold-dark">Đăng nhập ▸</span>
        </button>
      )}

      {/* Hai lối học — chỉ có nghĩa ở quyển KHOÁ BÀI. Quyển không khoá thì chương nào
          cũng vào được sẵn, hỏi bé chọn chế độ là hỏi một câu không có hệ quả. */}
      {ct.khoaBai && onSetMode && (
        <div className="mx-3.5 mt-5">
          <h3 className="pb-1.5 text-[11px] font-extrabold tracking-widest text-mute">
            CON MUỐN HỌC THẾ NÀO?
          </h3>
          <div className="flex gap-2">
            {[['chuongtrinh', 'Theo chương trình', 'học lần lượt từ đầu — đúng thứ tự cô soạn'],
              ['tuchon', 'Con tự chọn chủ đề', 'thích chương nào vào chương đó']].map(([id, ten, mt]) => (
              <button key={id} onClick={() => onSetMode(id)}
                className={`flex-1 rounded-xl border-[1.5px] px-3 py-2.5 text-left ${
                  cheDo === id ? 'border-navy bg-navy text-white' : 'border-line bg-white text-navy'}`}>
                <b className="block text-[13.5px]">{ten}</b>
                <span className={`text-[11.5px] ${cheDo === id ? 'opacity-85' : 'text-mute'}`}>{mt}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="px-3.5 pt-3">
        <BangSuuTapSao idx={chiMuc.bai} xong={progress?.micros || {}} />
      </div>

      <h3 className="px-4 pb-1 pt-3 text-[11px] font-extrabold tracking-widest text-mute">
        TẤT CẢ {hb.tongChuong} CHƯƠNG
      </h3>

      <div className="px-3.5">
        {hb.chuong.map((c) => {
          const bung = mo === c.so;
          const hien = c.bai.filter((b) => trangThaiBai(progress, b.id, { list, khoaBai: ct.khoaBai }) !== 'khoa');
          const soKhoa = c.bai.length - hien.length;
          return (
            <section key={c.so}
                     className="mb-2.5 overflow-hidden rounded-2xl bg-white shadow-[0_2px_10px_rgba(12,59,112,.06)]">
              <button className="flex w-full items-center gap-2.5 px-3.5 py-3 text-left"
                      onClick={() => setMo(bung ? 0 : c.so)}>
                <span className="rounded bg-navy px-1.5 py-0.5 text-[11px] font-extrabold text-white">
                  C{c.so}
                </span>
                <span className="min-w-0 flex-1">
                  <b className="block text-[14px] leading-snug text-navy">{c.ten}</b>
                  <span className="text-[11.5px] text-mute">
                    {c.tk.dat}/{c.tk.tong} bài · {NHAN_MUC_CHUONG[c.muc]}
                  </span>
                </span>
                {c.tk.master && <span className="text-[18px]">⭐</span>}
                {!c.tk.master && c.tk.kyDat && <span className="text-[18px]">🏅</span>}
                <span className="h-1.5 w-14 overflow-hidden rounded-full bg-soft">
                  <i className="block h-full bg-teal" style={{ width: `${c.tk.phanTram}%` }} />
                </span>
              </button>

              {bung && (
                <div className="border-t border-line px-3.5 py-2.5">
                  {/* DÒNG ĐỀ XUẤT CỦA CHƯƠNG — thứ lớp 2·3·4 chưa từng có. Chưa học
                      chương này thì nó chỉ vào bài ĐẦU chương, đúng như lớp 5. */}
                  {c.deXuat && (
                    <button onClick={() => onMoBai(c.deXuat.bai.id)}
                      className="mb-2 flex w-full items-center gap-2.5 rounded-xl border-[1.5px] border-gold bg-gold-pale px-3 py-2.5 text-left">
                      <span className="text-[18px] leading-none">
                        {c.deXuat.viSao === 'dangDo' ? '⏳' : '▶'}
                      </span>
                      <span className="min-w-0 flex-1">
                        <span className="block text-[11px] font-extrabold tracking-widest text-gold-dark">
                          {c.deXuat.viSao === 'dangDo' ? 'ĐANG HỌC DỞ'
                            : c.deXuat.viSao === 'chuaDat' ? 'LÀM LẠI BÀI NÀY'
                              : c.tk.cham === 0 ? 'BẮT ĐẦU CHƯƠNG NÀY' : 'HỌC TIẾP CHƯƠNG NÀY'}
                        </span>
                        <span className="block truncate text-[14px] font-bold text-navy">
                          Bài {c.deXuat.bai.so}{c.deXuat.bai.micro > 1 ? `.${c.deXuat.bai.micro}` : ''} · {c.deXuat.bai.ten}
                        </span>
                      </span>
                      <span className="text-[14px] text-gold-dark">▶</span>
                    </button>
                  )}
                  {!c.deXuat && c.tk.tong > 0 && (
                    <p className="mb-2 rounded-xl bg-teal-pale px-3 py-2 text-[13px] font-semibold text-teal-dark">
                      ✅ Con đã học xong mọi bài của chương này.
                    </p>
                  )}

                  {hien.map((b) => {
                    const s = trangThaiBai(progress, b.id, { list, khoaBai: ct.khoaBai });
                    return (
                      <button key={b.id} onClick={() => onMoBai(b.id)}
                        className="flex w-full items-center gap-2.5 rounded-lg px-2 py-2 text-left text-[13.5px] hover:bg-[#F0F5F9]">
                        <span className="text-[15px] leading-none">{BIEU_TUONG[s]}</span>
                        <i className={`h-2 w-2 flex-none rounded-full ${CHAM[s]}`} />
                        <span className="min-w-0 flex-1">
                          <b className="block truncate font-semibold text-navy">
                            Bài {b.so}{b.micro > 1 ? `.${b.micro}` : ''} · {b.ten}
                          </b>
                          <span className="text-[11.5px] text-mute">
                            {NHAN_TRANG_THAI[s]}
                            {b.soCau ? ` · ${b.soCau} câu luyện tập` : ''}
                            {b.soQuiz ? ` · ${b.soQuiz} câu tự kiểm` : ''}
                          </span>
                        </span>
                      </button>
                    );
                  })}

                  {/* Gộp phần chưa mở: ngày đầu con thấy 11 dòng xám + ổ khoá, bấm vào
                      không có gì xảy ra — nhìn như app hỏng chứ không như phần thưởng. */}
                  {soKhoa > 0 && (
                    <button onClick={() => setViSaoKhoa(c.so)}
                      className="mt-1.5 flex w-full items-center gap-2 rounded-lg bg-[#F7FAFD] px-2.5 py-2 text-left text-[12.5px] text-mute">
                      <span>🔒</span>
                      <span className="flex-1">Còn {soKhoa} bài nữa — học xong bài trên là mở dần</span>
                      <span className="font-bold text-navy">vì sao?</span>
                    </button>
                  )}

                  {/* Kỳ ôn tập của chương đứng NGAY SAU các bài của chương ấy — học xong
                      chương là thấy ngay cửa ải, không phải đi tìm ở đâu khác. */}
                  {(c.onTap || []).map((o) => (
                    <DongDanhSach
                      key={o.id} kieu="nhan" mauChu="text-gold-dark"
                      khoa={ct.khoaBai && !c.tk.xongBai}
                      bieuTuong={c.tk.kyDat ? '🏅' : '⚔'}
                      tieuDe={o.name}
                      phuDe={c.tk.kyDat ? 'con đã đạt' : loiKy(o, c.tk.kyLanTruoc)}
                      onClick={() => onMoOnTap(o.chapter)}
                    />
                  ))}
                </div>
              )}
            </section>
          );
        })}
      </div>

      {/* Ba ải cuối sách — trộn đủ mọi chương. Chỉ lớp 2·3 có. */}
      {hb.ai.length > 0 && (
        <div className="px-3.5">
          <section className="card">
            <div className="kicker">🏰 {hb.ai.length} CỬA ẢI CUỐI SÁCH</div>
            <p className="text-[13.5px] text-mute">
              Trộn đủ cả {hb.tongChuong} chương. Làm lần lượt từ Ải 1.
            </p>
            {hb.ai.map((o) => {
              const kq = ketQuaChuong(progress, hb.ma, o.chapter);
              return (
                <DongDanhSach
                  key={o.id}
                  bieuTuong={kq?.pass ? '⭐' : '🚪'}
                  tieuDe={o.name}
                  phuDe={loiKy(o, kq && { dung: kq.best, tong: kq.total })}
                  onClick={() => onMoOnTap(o.chapter)}
                />
              );
            })}
          </section>
        </div>
      )}

      {/* Cửa vào quyển luyện thi. Đặt SAU danh sách chương: con học quyển này trước,
          luyện thi sau — nhưng vẫn thấy được để biết còn có phần ấy. */}
      {ct.quyen2 && onMoMuaGiai && (
        <div className="px-3.5 pt-2">
          <button onClick={onMoMuaGiai}
                  className="flex w-full items-center gap-3 rounded-2xl border-[1.5px] border-gold bg-gold-pale px-4 py-3.5 text-left">
            <span className="text-[28px] leading-none">{tra(ct.quyen2).bieuTuong || '🏆'}</span>
            <span className="flex-1">
              <span className="block text-[11px] font-extrabold tracking-widest text-gold-dark">
                QUYỂN 2 · LUYỆN THI
              </span>
              <span className="block text-[16px] font-bold text-navy">
                {tra(ct.quyen2).ten}
              </span>
              <span className="block text-[12.5px] text-mute">
                vòng đấu có đồng hồ · mở dần theo từng chương con học xong
              </span>
            </span>
            <span className="text-[18px] text-gold-dark">▶</span>
          </button>
        </div>
      )}

      <ChanTrang />

      {viSaoKhoa !== null && (
        <div className="fixed inset-0 z-30 flex items-end justify-center bg-black/40 p-3.5"
             onClick={() => setViSaoKhoa(null)}>
          <div className="w-full max-w-[740px] rounded-2xl bg-white p-4" onClick={(e) => e.stopPropagation()}>
            <h4 className="text-[16px] font-bold text-navy">Vì sao chưa mở?</h4>
            <p className="mt-2 text-[14.5px] leading-relaxed">
              Mỗi bài dạy một cái bẫy mới, và bài sau dùng lại cái bẫy của bài trước.
              Nên con phải <b>làm đúng câu bẫy</b> của bài này thì bài sau mới mở —
              đúng 2/3 câu mà sai câu bẫy thì vẫn chưa qua.
            </p>
            <p className="mt-2 text-[14.5px] leading-relaxed">
              Học xong bài đang mở là bài kế tiếp hiện ra ngay.
            </p>
            {cheDo === 'chuongtrinh' && (
              <p className="mt-2 rounded-xl bg-gold-pale px-3 py-2.5 text-[14px] text-gold-dark">
                Muốn học chủ đề khác trước? Đổi sang <b>“Con tự chọn chủ đề”</b> ở trang chính —
                khi đó bài đầu của mọi chương đều mở.
              </p>
            )}
            <button className="btn-go mt-3.5" onClick={() => setViSaoKhoa(null)}>Con hiểu rồi</button>
          </div>
        </div>
      )}
    </div>
  );
}
