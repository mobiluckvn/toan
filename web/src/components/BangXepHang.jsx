import React, { useEffect, useMemo, useState } from 'react';
import ThanhTren from './ThanhTren.jsx';
import ChanTrang from './ChanTrang.jsx';
import { bangXepHang, lamMoiBangXepHang, luuBietDanh, luuDuoiKip } from '../lib/firebase.js';
import {
  BANG, bangCua, dsLop, locLop, danhSachHien, khoangCachTren, soKe, loiSoKe, huyChuong,
} from '../lib/xephang.js';

/**
 * BẢNG XẾP HẠNG — chỗ các con nhìn thấy nhau.
 *
 * ── BA BẢNG CHỨ KHÔNG MỘT ──
 * Xếp theo "tổng bài đã đạt" thì bé lớp 2 (33 bài) nằm đáy vĩnh viễn trước bé lớp 5
 * (168 bài), và bé vào sau không bao giờ đuổi kịp bé vào trước — nhìn một lần rồi
 * thôi. Nên: 🔥 tuần này (đặt lại mỗi tuần) · 📅 chuỗi ngày (chăm là thắng) ·
 * 👑 tổng sao (đường dài). Ai cũng có một bảng để mà thắng.
 *
 * ── THỨ THÚC BÉ KHÔNG PHẢI HẠNG 1 ──
 * Là câu "còn 12 sao nữa là con vượt Su Kem". Nên màn này luôn GHIM dòng của con
 * (kể cả hạng 87), luôn hiện khoảng cách tới người ngay trên, và cho con CHỌN MỘT
 * BẠN ĐỂ ĐUỔI — thanh so kè hai người, cập nhật mỗi lần bảng dựng lại.
 *
 * ── CỐ Ý KHÔNG LÀM ──
 * Không hiện hạng bét, không hiện "con đứng trên bao nhiêu bạn". Bé cuối bảng không
 * cần bị dí mũi vào chỗ đó — bảng này để thúc, không phải để xếp loại.
 */


const O_TIN = ({ nhan, gia }) => (
  <div className="min-w-[84px] flex-1 rounded-xl bg-white/15 px-2.5 py-2 text-center">
    <b className="block text-[19px] leading-tight">{gia}</b>
    <span className="text-[10px] font-extrabold uppercase tracking-wide opacity-80">{nhan}</span>
  </div>
);

function Dong({ r, khoa, nhan, laCon, onDuoi, dangDuoi }) {
  const hc = huyChuong(r.hang);
  return (
    <div className={`mt-1.5 flex items-center gap-2.5 rounded-xl border-[1.5px] px-3 py-2.5 ${
      laCon ? 'border-gold bg-gold-pale' : dangDuoi ? 'border-teal bg-teal-pale' : 'border-line bg-white'}`}>
      <span className={`flex h-8 w-8 flex-none items-center justify-center rounded-full text-[15px] font-extrabold ${
        hc ? '' : 'bg-soft text-mute'}`}>
        {hc || r.hang}
      </span>
      <span className="min-w-0 flex-1">
        <b className="block truncate text-[14.5px] text-navy">
          {r.ten}{laCon && <span className="ml-1.5 text-[11px] font-extrabold text-gold-dark">← con đây</span>}
        </b>
        <span className="text-[11.5px] text-mute">
          Lớp {r.lop}
          {khoa !== 'chuoi' && r.chuoi > 0 && ` · 🔥 chuỗi ${r.chuoi} ngày`}
        </span>
      </span>
      <span className="text-right">
        <b className="block text-[16px] tabular-nums text-navy">{r[khoa] || 0}</b>
        <span className="text-[10px] text-mute">{nhan}</span>
      </span>
      {/* Đuổi ai đó — nút nhỏ, chỉ hiện ở dòng của bạn khác */}
      {!laCon && onDuoi && (
        <button onClick={() => onDuoi(dangDuoi ? null : r.ma)}
                className={`flex-none rounded-full px-2 py-1 text-[11px] font-bold ${
                  dangDuoi ? 'bg-teal text-white' : 'bg-soft text-navy'}`}>
          {dangDuoi ? 'đang đuổi ✓' : 'đuổi 🎯'}
        </button>
      )}
    </div>
  );
}

export default function BangXepHang({ maCon, hoSo, onExit, onVeNha, onLuuHoSo }) {
  const [bang, setBang] = useState(undefined);      // undefined = đang mở
  const [tab, setTab] = useState('tuan');
  const [lop, setLop] = useState(0);
  const [dangMoi, setDangMoi] = useState(false);
  const [suaTen, setSuaTen] = useState(false);
  const [tenMoi, setTenMoi] = useState('');
  const [duoi, setDuoi] = useState(hoSo?.duoiKip || null);
  const [loi, setLoi] = useState(null);

  useEffect(() => {
    let song = true;
    bangXepHang().then((b) => song && setBang(b)).catch(() => song && setBang(null));
    return () => { song = false; };
  }, []);

  const b = bangCua(tab);
  const rows = useMemo(() => locLop(bang?.rows || [], lop), [bang, lop]);
  const ds = useMemo(() => danhSachHien(rows, b.khoa, maCon), [rows, b.khoa, maCon]);
  const cach = useMemo(() => khoangCachTren(rows, b.khoa, maCon), [rows, b.khoa, maCon]);
  /* Thanh so kè luôn tính trên TOÀN TRƯỜNG, không theo bộ lọc lớp đang xem: con đuổi
     một bạn lớp khác thì lọc về "Lớp 3" không được làm bạn ấy biến mất. */
  const sk = useMemo(() => soKe(bang?.rows || [], b.khoa, maCon, duoi), [bang, b.khoa, maCon, duoi]);

  const chonDuoi = async (ma) => {
    setDuoi(ma);
    try { await luuDuoiKip(maCon, ma); onLuuHoSo?.({ duoiKip: ma }); } catch { /* mất mạng: lần sau ghi lại */ }
  };

  const luuTen = async () => {
    const t = tenMoi.trim();
    if (!t) return;
    try {
      await luuBietDanh(maCon, t);
      onLuuHoSo?.({ bietDanh: t });
      setSuaTen(false);
      /* Tên chỉ đổi trên bảng sau lần dựng kế tiếp — nói thẳng, đừng để con bấm lưu
         rồi nhìn bảng vẫn tên cũ và tưởng hỏng. */
      setLoi('Đã lưu biệt danh. Tên trên bảng đổi sau lần cập nhật tới nhé.');
    } catch (e) { setLoi(String(e?.message || e)); }
  };

  const lamMoi = async () => {
    setDangMoi(true); setLoi(null);
    try {
      const kq = await lamMoiBangXepHang();
      setBang(await bangXepHang());
      if (kq?.boQua) setLoi('Bảng vừa được cập nhật xong — con xem bản mới nhất rồi.');
    } catch (e) { setLoi(String(e?.message || e)); }
    finally { setDangMoi(false); }
  };

  const dau = (
    <ThanhTren nhan="MOBILUCK · KỸ SƯ NHÍ" tieuDe="🏆 Bảng xếp hạng"
               phuDe="Xem các bạn đang học tới đâu — và còn bao xa nữa thì con đuổi kịp."
               onQuayLai={onExit} nhanQuayLai="← Quay lại" onVeNha={onVeNha} />
  );

  if (bang === undefined) {
    return <div className="mx-auto min-h-[100dvh] max-w-[740px]">{dau}
      <p className="p-6 text-mute">Đang mở bảng…</p></div>;
  }

  /* Chưa đăng nhập, hoặc bảng chưa dựng lần nào. Hai chuyện khác nhau, nói khác nhau. */
  if (!bang || !bang.rows?.length) {
    return (
      <div className="mx-auto min-h-[100dvh] max-w-[740px]">{dau}
        <div className="px-3.5 pt-3.5">
          <div className="card">
            {maCon && maCon !== 'local' ? (
              <>
                <p className="text-[15px] leading-relaxed">
                  Bảng chưa được dựng lần nào. Máy chủ tổng hợp lúc <b>21h15 mỗi đêm</b> —
                  con quay lại sau đó nhé, hoặc bấm nút dưới đây để dựng ngay.
                </p>
                <button className="btn-go mt-3" disabled={dangMoi} onClick={lamMoi}>
                  {dangMoi ? 'đang dựng…' : '↻ Dựng bảng ngay'}
                </button>
              </>
            ) : (
              <p className="text-[15px] leading-relaxed">
                Con cần <b>đăng nhập</b> thì mới lên bảng xếp hạng được — bảng cần biết
                con là ai để xếp con vào đúng chỗ, và để các bạn nhìn thấy con.
              </p>
            )}
            {loi && <p className="mt-2 text-[13px] text-alert">{loi}</p>}
          </div>
        </div>
      </div>
    );
  }

  const con = ds.con;

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
      {dau}

      {/* ══ THẺ CỦA CON — thứ đầu tiên con tìm khi mở bảng ══ */}
      <div className="bg-navy px-3.5 pb-4 text-white">
        {con ? (
          <>
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-[11px] font-extrabold tracking-widest text-gold">CON ĐANG Ở ĐÂY</span>
              <button onClick={() => { setTenMoi(con.ten); setSuaTen(!suaTen); }}
                      className="rounded-full bg-white/15 px-2 py-0.5 text-[10.5px] font-bold">
                ✎ đổi biệt danh
              </button>
            </div>
            {suaTen && (
              <div className="mt-2 flex gap-2">
                <input className="numin min-w-0 flex-1 text-left text-[15px] font-normal"
                       maxLength={24} value={tenMoi} placeholder="vd: Trí Long"
                       onChange={(e) => setTenMoi(e.target.value)} />
                <button className="rounded-xl bg-gold px-3 text-[13px] font-bold text-navy" onClick={luuTen}>
                  Lưu
                </button>
              </div>
            )}
            <div className="mt-2 flex flex-wrap gap-2">
              <O_TIN nhan={`hạng ${b.ten.replace(/^\S+\s/, '')}`} gia={`#${con.hang}`} />
              <O_TIN nhan={b.nhan} gia={con[b.khoa] || 0} />
              <O_TIN nhan="chuỗi ngày" gia={`🔥 ${con.chuoi}`} />
              <O_TIN nhan="bài đã đạt" gia={con.baiDat} />
            </div>
            {cach && (
              <p className="mt-2.5 rounded-xl bg-gold px-3 py-2 text-[14px] font-bold leading-snug text-navy">
                Còn <b>{cach.thieu}</b> {b.nhan} nữa là con vượt <b>{cach.ban.ten}</b>!
              </p>
            )}
            {!cach && con.hang === 1 && (
              <p className="mt-2.5 rounded-xl bg-gold px-3 py-2 text-[14px] font-bold text-navy">
                🎉 Con đang DẪN ĐẦU bảng này. Giữ vững nhé!
              </p>
            )}
          </>
        ) : (
          <p className="text-[13.5px] leading-relaxed opacity-90">
            Con chưa có trên bảng — học một bài là con xuất hiện ở lần cập nhật tới.
          </p>
        )}
      </div>

      {/* ══ THANH SO KÈ VỚI BẠN ĐANG ĐUỔI ══ */}
      {sk && (
        <div className="px-3.5 pt-3.5">
          <div className="rounded-2xl border-[1.5px] border-teal bg-teal-pale px-4 py-3">
            <div className="flex items-center justify-between text-[12px] font-extrabold text-teal-dark">
              <span>🎯 CON ĐANG ĐUỔI</span>
              <button onClick={() => chonDuoi(null)} className="text-[11px] font-bold underline opacity-75">
                bỏ đuổi
              </button>
            </div>
            <div className="mt-1.5 flex items-center justify-between text-[13.5px] font-bold text-navy">
              <span>Con · {sk.con[b.khoa] || 0}</span>
              <span>{sk.ban.ten} · {sk.ban[b.khoa] || 0}</span>
            </div>
            <div className="mt-1 flex h-2.5 overflow-hidden rounded-full bg-white">
              <i className="block h-full bg-gold" style={{ width: `${sk.phanTramCon}%` }} />
              <i className="block h-full flex-1 bg-teal" />
            </div>
            <p className="mt-1.5 text-[13.5px] font-semibold leading-snug text-teal-dark">
              {loiSoKe(sk, b.nhan)}
            </p>
          </div>
        </div>
      )}

      {/* ══ CHỌN BẢNG ══ */}
      <div className="px-3.5 pt-3.5">
        <div className="flex gap-1.5">
          {BANG.map((x) => (
            <button key={x.ma} onClick={() => setTab(x.ma)}
              className={`flex-1 rounded-xl border-[1.5px] px-2 py-2 text-center text-[12.5px] font-bold ${
                tab === x.ma ? 'border-navy bg-navy text-white' : 'border-line bg-white text-navy'}`}>
              {x.ten}
            </button>
          ))}
        </div>
        <p className="mt-1.5 text-[12.5px] leading-snug text-mute">{b.mo}</p>

        {/* Lọc theo lớp. "Cả nhà" đứng đầu và là mặc định — cả điểm của bảng này là
            để bé lớp 2 nhìn thấy bé lớp 3, không phải để nhốt mỗi bé trong lớp mình. */}
        <div className="mt-2 flex flex-wrap gap-1.5">
          {dsLop(bang.rows).map((l) => (
            <button key={l.ma} onClick={() => setLop(l.ma)}
              className={`rounded-full px-2.5 py-1 text-[12px] font-bold ${
                lop === l.ma ? 'bg-navy text-white' : 'bg-soft text-navy'}`}>
              {l.ten}
            </button>
          ))}
        </div>
      </div>

      {/* ══ BẢNG ══ */}
      <div className="px-3.5 pt-3">
        {ds.tren.length === 0 && (
          <p className="card text-[14px] text-mute">Chưa bạn nào có sao ở bảng này.</p>
        )}
        {ds.tren.map((r) => (
          <Dong key={r.ma} r={r} khoa={b.khoa} nhan={b.nhan} laCon={r.ma === maCon}
                onDuoi={maCon ? chonDuoi : null} dangDuoi={r.ma === duoi} />
        ))}

        {ds.ngoaiTop && (
          <>
            <div className="py-1 text-center text-[16px] leading-none text-mute">⋯</div>
            <Dong r={ds.con} khoa={b.khoa} nhan={b.nhan} laCon />
          </>
        )}
      </div>

      {/* ══ SAO TÍNH THẾ NÀO — in ra để bé thấy công bằng ══ */}
      <div className="px-3.5 pt-3">
        <section className="card">
          <div className="kicker">⭐ SAO TÍNH THẾ NÀO?</div>
          <div className="grid gap-1.5 text-[13.5px]">
            {[['mỗi câu trả lời đúng', bang.cong?.cauDung ?? 1],
              ['mỗi bài học đạt', bang.cong?.baiDat ?? 10],
              ['mỗi huy hiệu chương', bang.cong?.huyHieu ?? 30],
              ['mỗi vòng đấu Mùa giải đạt', bang.cong?.vongDau ?? 50]].map(([ten, so]) => (
              <div key={ten} className="flex items-center justify-between rounded-lg bg-soft px-3 py-1.5">
                <span className="text-mute">{ten}</span>
                <b className="text-navy">+{so} ⭐</b>
              </div>
            ))}
          </div>
          <p className="mt-2 text-[12.5px] leading-relaxed text-mute">
            Mỗi ngày, sao từ câu trả lời đúng tính tối đa {bang.cong?.tranNgay ?? 60} sao — để
            bạn nào ngồi bấm lại một bài thật nhiều lần cũng không leo lên đầu bảng được.
            Bảng <b>Tổng sao</b> chỉ cộng bài · huy hiệu · vòng đấu.
          </p>
        </section>

        <div className="card flex flex-wrap items-center justify-between gap-2 py-3">
          <span className="text-[12.5px] text-mute">
            Cập nhật lúc {new Date(bang.generatedAt).toLocaleString('vi-VN')}
            {' · '}{bang.soEmCoHoc}/{bang.soEm} bạn có học tuần này
          </span>
          <button className="rounded-full border-[1.5px] border-navy px-3 py-1 text-[12.5px] font-bold text-navy disabled:opacity-50"
                  disabled={dangMoi} onClick={lamMoi}>
            {dangMoi ? 'đang cập nhật…' : '↻ Cập nhật ngay'}
          </button>
          {loi && <p className="w-full text-[12.5px] text-teal-dark">{loi}</p>}
        </div>
      </div>

      <ChanTrang />
    </div>
  );
}
