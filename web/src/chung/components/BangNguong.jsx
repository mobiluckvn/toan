import React, { useEffect, useMemo, useState } from 'react';
import { logout } from '../lib/taiKhoan.js';
import {
  MAC_DINH, KHOANG, boNguong, layNguong, soiNguong,
  nhipTinhThong, NHIP_CHO_PHEP, PHIEN_BAN,
} from '../lib/nguong.js';
import { phatHanhNguong } from '../lib/ghiNguong.js';
import { TEN_NGUONG as TEN } from '../lib/tenNguong.js';
import { docThongKeNguong, gomTheoPhamVi, docHieu } from '../lib/docThongKe.js';

/**
 * MÀN HÌNH QUẢN LÝ NGƯỠNG — R7, mục 3.8.4.
 *
 * ── MÀN NÀY TỒN TẠI ĐỂ BỎ MỘT CÂU "PHẢI NHỜ NGƯỜI VIẾT MÃ" ──
 * Trước R7, muốn đổi θ thì phải sửa mã rồi deploy. Người hiểu việc dạy học không tự
 * làm được. Màn này là chỗ họ làm được.
 *
 * ── BA ĐIỀU BÀY RA, VÀ VÌ SAO ──
 *
 * 1 · KHOẢNG HỢP LỆ hiện ngay cạnh ô nhập, không giấu trong lời báo lỗi. Giới hạn mà
 *     chỉ thấy sau khi gõ sai thì người ta gõ sai rồi mới biết.
 *
 * 2 · NHỊP TINH THÔNG (Bảng 3.21) hiện LIỀN mỗi lần sửa. Đây là phần quan trọng nhất
 *     của màn: nhìn con số θ thì không thấy được rằng đổi 0,85 → 0,90 chẳng đổi gì
 *     trong cách hệ thống đối xử với trẻ (cả hai đều cần bốn câu đúng liên tiếp), còn
 *     hạ xuống 0,80 thì chỉ còn ba. Chuyên gia phải sửa theo SỐ CÂU, không theo xác suất.
 *
 * 3 · LÝ DO là bắt buộc. Luật Firestore cũng đòi (`lyDo.size() > 0`), và đòi vì sáu
 *     tháng sau không ai nhớ vì sao θ thành 0,88 — bảng `nguong_lich_su` chỉ đáng giá
 *     khi mỗi dòng trả lời được câu "vì sao".
 *
 * ⚠ MÀN NÀY KHÔNG ĐỔI PHIÊN ĐANG CHẠY. Mục 3.8.4: "Phiên bản mới chỉ có hiệu lực từ
 *   phiên tiếp theo." Nên sau khi phát hành, màn nói thẳng điều ấy thay vì để chuyên
 *   gia tưởng mình vừa đổi cái gì đó ngay lập tức.
 */

const NHOM = [
  ['moHinh', 'Tham số mô hình người học và trí nhớ', ['NG01', 'NG02', 'NG03', 'NG04', 'NG05', 'NG06']],
  ['quyetDinh', 'Ngưỡng quyết định tinh thông và can thiệp', ['NG07', 'NG08', 'NG09']],
  ['chanDoan', 'Tham số chẩn đoán nguyên nhân', ['NG10', 'NG11', 'NG12', 'NG13']],
  ['danDat', 'Lưới an toàn và dẫn dắt', ['NG14', 'NG15']],
  ['hanhViVaDo', 'Ngưỡng hành vi và đo lường', ['NG16', 'NG17', 'NG18', 'NG19', 'NG20', 'NG21']],
];


/** Ngưỡng mang HAI con số thì sửa bằng hai ô. */
const HAI_O = { NG05: ['slip', 'guess'], NG17: ['ti', 'toiThieuMoiNua'] };

export default function BangNguong({ onExit, onXemDeXuat = null }) {
  const dangHanh = boNguong();
  const [gt, datGt] = useState(() => ({ ...MAC_DINH, ...(dangHanh.macDinh || {}) }));
  const [lyDo, datLyDo] = useState('');
  const [dangGui, datDangGui] = useState(false);
  const [bao, datBao] = useState(null);
  /* Chỉ số theo dõi (Bảng 3.22). `null` = đang nạp, `[]` = đã nạp và chưa có gì —
     hai trạng thái phải phân biệt được, vì chúng nói hai chuyện khác nhau. */
  const [tk, datTk] = useState(null);
  const [loiTk, datLoiTk] = useState(null);

  useEffect(() => {
    let song = true;
    docThongKeNguong().then(({ dong, loi }) => {
      if (!song) return;
      datTk(gomTheoPhamVi(dong));
      datLoiTk(loi);
    });
    return () => { song = false; };
  }, []);

  const bo = useMemo(() => ({ phienBan: dangHanh.phienBan, macDinh: gt, theoPhamVi: {} }), [gt, dangHanh]);
  const loi = useMemo(() => soiNguong(bo), [bo]);
  const nhip = useMemo(() => nhipTinhThong(bo), [bo]);
  const doi = useMemo(
    () => Object.keys(MAC_DINH).filter((m) => JSON.stringify(gt[m]) !== JSON.stringify(dangHanh.macDinh?.[m] ?? MAC_DINH[m])),
    [gt, dangHanh],
  );

  const dat = (ma, truong, chu) => {
    const so = Number(chu);
    datBao(null);
    datGt((c) => ({ ...c, [ma]: truong ? { ...c[ma], [truong]: so } : so }));
  };

  const phatHanh = async () => {
    datDangGui(true); datBao(null);
    try {
      const pb = await phatHanhNguong({ giaTri: gt, doi, lyDo });
      datBao({ ok: true, chu: `Đã phát hành phiên bản ${pb}. `
        + 'Phiên đang chạy giữ nguyên bộ cũ — bản mới có hiệu lực từ phiên sau.' });
    } catch (e) {
      datBao({ ok: false, chu: e?.message || 'Không ghi được. Người lớn kiểm tra giúp.' });
    } finally { datDangGui(false); }
  };

  const [itNhat, nhieuNhat] = NHIP_CHO_PHEP;
  const nhipXau = nhip.soCau === null || nhip.soCau < itNhat || nhip.soCau > nhieuNhat;

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-4 p-4">
      <header className="flex items-center gap-3">
        <h1 className="flex-1 text-xl font-bold text-ink sm:text-2xl">
          Bảng ngưỡng · phiên bản {dangHanh.phienBan ?? PHIEN_BAN}
        </h1>
        <button type="button" onClick={() => logout().then(onExit)}
          className="rounded-xl2 border border-line px-3 py-1.5 text-sm text-mute hover:text-navy">
          Thoát
        </button>
      </header>

      {/* NHỊP TINH THÔNG — phần quan trọng nhất của màn, nên đặt TRÊN danh sách. */}
      {onXemDeXuat && (
        <button type="button" onClick={onXemDeXuat}
          className="rounded-xl2 border-2 border-line p-3 text-left text-sm">
          <b className="text-ink">Đề xuất máy học được →</b>
          <span className="block text-mute">
            Máy học từ nhật ký mỗi sáng thứ Hai. Nó chỉ ĐỀ XUẤT — duyệt ở đó rồi vẫn phải
            quay về đây phát hành thì giá trị mới có hiệu lực.
          </span>
        </button>
      )}

      <section className={`rounded-xl2 p-4 ${nhipXau ? 'bg-gold-pale' : 'bg-teal-pale'}`}>
        <h2 className="font-bold text-ink">Với bộ này, con cần nói đúng mấy câu liền?</h2>
        <p className="mt-1 text-2xl font-bold text-navy">
          {nhip.soCau === null ? 'Không bao giờ đạt' : `${nhip.soCau} câu đúng liên tiếp`}
        </p>
        <p className="text-sm text-ink">
          Khi vừa đạt: <b>{nhip.mucKhiDat.toFixed(3)}</b> · sau đó sai một câu còn{' '}
          <b>{nhip.sauKhiSai.toFixed(3)}</b>
        </p>
        <p className="mt-2 text-xs leading-relaxed text-mute">
          Nên sửa ngưỡng theo con số này, đừng sửa theo giá trị xác suất: với bộ tham số
          hiện tại, đổi θ từ 0,85 lên 0,90 không đổi gì trong cách hệ thống đối xử với
          trẻ — cả hai đều cần bốn câu. Phát hành được khi nhịp nằm trong {itNhat}–{nhieuNhat} câu.
        </p>
      </section>

      {!!loi.length && (
        <ul className="flex flex-col gap-1 rounded-xl2 bg-gold-pale p-3 text-sm text-gold-dark">
          {loi.map((x, i) => <li key={`${x.ma}-${i}`}><b>{x.ma}</b> — {x.vi}</li>)}
        </ul>
      )}

      {/* ── CHỈ SỐ THEO DÕI (Bảng 3.22, mục 3.8.5) ──
          Đặt TRƯỚC danh sách ngưỡng, cùng một lẽ với bảng nhịp tinh thông ở trên:
          chuyên gia nên sửa theo số liệu, không theo cảm tính. Để nó dưới 21 ô nhập
          thì người ta sửa xong mới nhìn thấy căn cứ. */}
      <section className="rounded-xl2 border border-line p-3">
        <h2 className="mb-2 font-bold text-ink">Dữ liệu tuần này nói gì về các ngưỡng</h2>
        {loiTk && (
          <p className="text-sm text-gold-dark">
            Chưa đọc được thống kê ({loiTk}). Đây KHÁC với &ldquo;chưa có số liệu&rdquo; — người lớn
            kiểm tra giúp, đừng sửa ngưỡng theo một bảng trống.
          </p>
        )}
        {!loiTk && tk === null && <p className="text-sm text-mute">Đang đọc…</p>}
        {!loiTk && tk !== null && !tk.length && (
          <p className="text-sm text-mute">
            Chưa có số liệu. Hàm nền tính mỗi sáng thứ Hai, và chỉ có số khi đã đủ lượt học thật —
            tới lúc ấy thì cứ giữ giá trị mặc định, đừng đoán.
          </p>
        )}
        {!loiTk && !!tk?.length && (
          <ul className="flex flex-col gap-3">
            {tk.map((pv) => {
              const moi = pv.tuan[0];
              const cach = docHieu(moi);
              return (
                <li key={`${pv.phamVi}:${pv.khoa}`} className="rounded-xl2 bg-paper p-3">
                  <p className="text-sm font-bold text-ink">
                    {pv.phamVi === 'toanHe' ? 'Toàn hệ thống' : `${pv.phamVi} · ${pv.khoa}`}
                    <span className="ml-2 font-normal text-mute">
                      {moi.mocTuan} · {moi.coMau} lượt · {moi.soChuoi} chuỗi
                      {moi.duMauDeHoc ? '' : ' · chưa đủ mẫu để học ngưỡng'}
                    </span>
                  </p>
                  {!cach.length && (
                    <p className="mt-1 text-sm text-mute">Chưa đủ mẫu để nói gì chắc chắn.</p>
                  )}
                  <ul className="mt-1 flex flex-col gap-1">
                    {cach.map((c) => (
                      <li key={c.ma} className={`text-sm ${c.muc === 'canXem' ? 'text-gold-dark' : 'text-mute'}`}>
                        <b className="text-ink">{c.ma}</b> · {c.chu}
                      </li>
                    ))}
                  </ul>
                </li>
              );
            })}
          </ul>
        )}
      </section>

      {NHOM.map(([khoa, ten, ds]) => (
        <section key={khoa} className="rounded-xl2 border border-line p-3">
          <h2 className="mb-2 text-sm font-bold uppercase tracking-wide text-mute">{ten}</h2>
          <ul className="flex flex-col gap-2">
            {ds.map((ma) => {
              const [d, t] = KHOANG[ma];
              const truongs = HAI_O[ma];
              const xau = loi.some((x) => x.ma === ma);
              return (
                <li key={ma} className="flex flex-wrap items-center gap-2 text-sm">
                  <span className="w-16 shrink-0 font-mono text-xs text-mute">{ma}</span>
                  <span className="min-w-[13rem] flex-1 text-ink">{TEN[ma]}</span>
                  {(truongs || [null]).map((tr) => (
                    <input key={tr || 'x'} type="number" step="any"
                      aria-label={`${TEN[ma]}${tr ? ` — ${tr}` : ''}`}
                      value={tr ? (gt[ma]?.[tr] ?? '') : (gt[ma] ?? '')}
                      onChange={(e) => dat(ma, tr, e.target.value)}
                      className={`numin w-24 text-[16px] ${xau ? 'border-gold' : ''}`} />
                  ))}
                  <span className="w-28 shrink-0 text-right text-xs text-mute">[{d} – {t}]</span>
                </li>
              );
            })}
          </ul>
        </section>
      ))}

      <section className="flex flex-col gap-2 rounded-xl2 border border-line p-3">
        <label className="text-sm font-semibold text-ink" htmlFor="lydo">
          Vì sao đổi? {doi.length ? `(${doi.length} ngưỡng đã sửa: ${doi.join(', ')})` : '(chưa sửa gì)'}
        </label>
        <input id="lydo" className="numin w-full text-[16px]" value={lyDo}
               placeholder="ví dụ: tỷ lệ công nhận sớm tuần này 18%, nâng θ"
               onChange={(e) => { datLyDo(e.target.value); datBao(null); }} />
        <div className="flex items-center gap-3">
          <button type="button" disabled={!!loi.length || !doi.length || !lyDo.trim() || dangGui}
            onClick={phatHanh}
            className="rounded-xl2 bg-navy px-4 py-2 text-sm font-semibold text-white
                       disabled:opacity-40 focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            {dangGui ? 'Đang phát hành…' : 'Phát hành phiên bản mới'}
          </button>
          {!!doi.length && (
            <button type="button" onClick={() => { datGt({ ...MAC_DINH, ...(dangHanh.macDinh || {}) }); datBao(null); }}
              className="text-sm text-mute underline">bỏ các thay đổi</button>
          )}
        </div>
        {bao && (
          <p className={`text-sm ${bao.ok ? 'text-teal-dark' : 'text-gold-dark'}`}>{bao.chu}</p>
        )}
      </section>
    </div>
  );
}
