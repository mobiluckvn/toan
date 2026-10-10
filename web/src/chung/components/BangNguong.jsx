import React, { useMemo, useState } from 'react';
import { logout } from '../lib/taiKhoan.js';
import {
  MAC_DINH, KHOANG, boNguong, layNguong, soiNguong,
  nhipTinhThong, NHIP_CHO_PHEP, PHIEN_BAN,
} from '../lib/nguong.js';
import { phatHanhNguong } from '../lib/ghiNguong.js';

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

const TEN = {
  NG01: 'P(L₀) — đã biết từ trước', NG02: 'P(T) — học được sau một lượt',
  NG03: 'P(S) — sơ suất', NG04: 'P(G) — đoán đúng', NG05: 'S/G của câu bẫy',
  NG06: 'h — bán rã trí nhớ (ngày)', NG07: 'θ — ngưỡng tinh thông',
  NG08: 'θ_yếu — ngưỡng yếu', NG09: 'sai liên tiếp để bật phụ đạo',
  NG10: 'd — độ sâu duyệt ngược', NG11: 'm — số nút gốc trả về',
  NG12: 'α — giảm độ ngờ mỗi bước', NG13: 'ngày coi là có nguy cơ quên',
  NG14: 'lần thử thật (lưới an toàn)', NG15: 'nút tối thiểu để bỏ qua bài',
  NG16: 'H3 — coi là bế tắc (giây)', NG17: 'H6 — coi là mệt mỏi',
  NG18: 'H7 — lượt tối thiểu cho dạng câu', NG19: 'cặp ΔC tối thiểu',
  NG20: 'câu hỏi tối thiểu mỗi nút', NG21: 'cỡ mẫu để học một ngưỡng',
};

/** Ngưỡng mang HAI con số thì sửa bằng hai ô. */
const HAI_O = { NG05: ['slip', 'guess'], NG17: ['ti', 'toiThieuMoiNua'] };

export default function BangNguong({ onExit }) {
  const dangHanh = boNguong();
  const [gt, datGt] = useState(() => ({ ...MAC_DINH, ...(dangHanh.macDinh || {}) }));
  const [lyDo, datLyDo] = useState('');
  const [dangGui, datDangGui] = useState(false);
  const [bao, datBao] = useState(null);

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
