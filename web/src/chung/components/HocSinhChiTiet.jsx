import React, { useEffect, useMemo, useState } from 'react';
import Chu from './Chu.jsx';
import { NHAN_MUC_CHUONG, NHAN_TINH_TRANG, NHAN_TRANG_THAI_BAI } from '../lib/nhanHocBa.js';
import { minutesStudied } from '../../../functions/src/report.js';

/**
 * MỘT HỌC SINH, NHÌN TỪ PHÍA CÔ GIÁO.
 *
 * Bảng chung trả lời "em nào đang tắc"; màn này trả lời "em ấy đang ở đâu và hổng
 * chỗ nào". Bản cũ chỉ có đúng MỘT thứ: nhật ký 200 lượt trả lời gần nhất, lọc được
 * theo dạng bài. Hữu ích, nhưng đó là dữ liệu THÔ — cô phải tự đọc 200 dòng rồi tự
 * dựng lại bức tranh trong đầu.
 *
 * Nay bốn tầng, đi từ tổng đến chi tiết:
 *   TỔNG QUAN   trình độ hiện tại · thời gian học · quyển đang học · chỗ cần kèm
 *   THEO LỚP    quyển → chương → bài, trạng thái từng bài
 *   THEO CHỦ ĐỀ mảng → chủ đề → dạng bài, con vững tới bậc lớp mấy
 *   NHẬT KÝ     200 lượt gần nhất, lọc theo dạng bài (giữ nguyên bản cũ)
 *
 * ── ĐỌC TỪ ĐÂU ──
 * `progress/{uid}/micros` cho phần bài, `hocBa/{uid}/muc` cho kỳ sát hạch · bậc chủ
 * đề · vòng đấu. Hai thư mục ấy luật Firestore đã cho giáo viên đọc, nên màn này
 * không cần Cloud Function nào dựng sẵn — bấm vào em nào mới tải của em ấy.
 */

const CHANG = { practice: 'luyện tập', assess: 'sát hạch', check: 'chốt nhanh', worked: 'theo ví dụ' };
const MAU_MUC = {
  master: 'bg-teal text-white', xongBai: 'bg-gold text-gold-dark',
  dangHoc: 'bg-navy-light text-white', chuaHoc: 'bg-soft text-mute',
};
const MAU_TT = {
  vung: 'bg-teal text-white', dangHoc: 'bg-navy-light text-white',
  canCoGang: 'bg-alert text-white', chuaHoc: 'bg-soft text-mute',
};
const CHAM_BAI = {
  dat: 'bg-teal', dangDo: 'bg-gold', chuaDat: 'bg-alert', mo: 'bg-navy-light', khoa: 'bg-line',
};

const O = ({ nhan, gia, mau = 'text-navy' }) => (
  <div className="min-w-[86px] flex-1 rounded-xl bg-soft px-3 py-2.5 text-center">
    <b className={`block text-[20px] ${mau}`}>{gia}</b>
    <span className="text-[10.5px] font-extrabold text-mute">{nhan}</span>
  </div>
);

export default function HocSinhChiTiet({ em, mon = [] }) {
  /* Học bạ của em này, do CHÍNH MÔN dựng theo khuôn chung. Màn này không biết Toán
     chia chương ra sao — nó chỉ vẽ đúng khuôn ấy, nên thêm môn là thêm một tab. */
  const [monMa] = useState(mon[0]?.ma);
  const m = mon.find((x) => x.ma === monMa) || mon[0];
  const [hb, setHb] = useState(null);
  const [rows, setRows] = useState('loading');
  const [tab, setTab] = useState('tong');
  const [moQuyen, setMoQuyen] = useState(null);
  const [moMang, setMoMang] = useState(null);
  const [locDang, setLocDang] = useState('');

  useEffect(() => {
    let song = true;
    setHb(null); setRows('loading'); setLocDang(''); setTab('tong');
    m?.hocBaCuaEm(em.uid).then((x) => song && setHb(x)).catch(() => song && setHb({ quyen: [] }));
    m?.nhatKyCuaEm(em.uid, 200).then((r) => song && setRows(r)).catch(() => song && setRows([]));
    return () => { song = false; };
  }, [em.uid, m]);

  const dsHocBa = hb?.quyen || [];
  const td = hb?.trinhDo;
  const cd = hb?.chuDe;

  /* Thời gian học tính TẠI ĐÂY từ nhật ký, cùng một công thức với sổ phụ huynh
     (ngắt quãng > 5 phút thì không tính). Dùng chung hàm chứ không viết lại. */
  const phut = useMemo(() => {
    if (!Array.isArray(rows)) return null;
    return minutesStudied(rows.map((a) => ({ ...a, ts: a.ts ?? a.serverTs })));
  }, [rows]);
  const buoi = useMemo(
    () => (Array.isArray(rows) ? new Set(rows.map((a) => a.sessionId)).size : 0), [rows]);

  const dangCua = (a) => (a.dangBai?.length ? a.dangBai : (m?.dangCuaBai(a.microId) || []));
  const dsDang = useMemo(() => {
    if (!Array.isArray(rows)) return [];
    const d = new Map();
    for (const a of rows) for (const k of dangCua(a)) d.set(k, (d.get(k) || 0) + 1);
    return [...d.entries()].sort((x, y) => y[1] - x[1]);
  }, [rows, m]);
  const nhatKy = useMemo(() => {
    if (!Array.isArray(rows)) return rows;
    return locDang ? rows.filter((a) => dangCua(a).includes(locDang)) : rows;
  }, [rows, locDang, m]);

  if (!hb) return <p className="card text-mute">Đang mở học bạ của em…</p>;

  const TAB = [['tong', 'Tổng quan'], ['lop', 'Theo lớp'], ['chude', 'Theo chủ đề'], ['nhatky', 'Nhật ký']];

  return (
    <>
      <div className="mb-3 flex flex-wrap gap-1.5">
        {TAB.map(([id, ten]) => (
          <button key={id} onClick={() => setTab(id)}
            className={`rounded-full px-3 py-1.5 text-[12.5px] font-bold ${
              tab === id ? 'bg-navy text-white' : 'bg-soft text-navy'}`}>
            {ten}
          </button>
        ))}
      </div>

      {/* ══════════ TỔNG QUAN ══════════ */}
      {tab === 'tong' && (
        <>
          <div className="card">
            <div className="kicker">TRÌNH ĐỘ HIỆN TẠI</div>
            {td.quyen ? (
              <p className="text-[15px] leading-relaxed">
                Đang học <b>{td.quyen.ten}</b> — đạt <b>{td.quyen.datBai}</b>/{td.quyen.tongBai} bài,
                master <b>{td.quyen.masterChuong}</b>/{td.quyen.tongChuong} chương.
                {td.bacChuDe !== null && (
                  <> Trên {td.soChuDeDoDuoc} chủ đề đã luyện, em vững quanh mức <b>lớp {td.bacChuDe}</b>.</>
                )}
                {td.soQuyenDangHoc > 1 && <> Em học xen kẽ {td.soQuyenDangHoc} quyển.</>}
              </p>
            ) : (
              <p className="text-[15px] text-mute">Em chưa có bài nào được ghi.</p>
            )}
            <div className="mt-3 flex flex-wrap gap-2">
              <O nhan="BÀI ĐÃ ĐẠT" gia={td.tongBaiDat} />
              <O nhan="CHƯƠNG MASTER" gia={td.tongChuongMaster} />
              <O nhan="CHỦ ĐỀ VỮNG" gia={cd?.tong ? `${cd.dem.vung}/${cd.tong}` : '—'} mau="text-teal-dark" />
              <O nhan="CẦN CỐ GẮNG" gia={cd?.dem.canCoGang ?? '—'} mau="text-alert" />
            </div>
            <div className="mt-2 flex flex-wrap gap-2">
              {/* Phút học đo trên 200 lượt gần nhất — nói rõ mẫu số, đừng để cô đọc
                  thành "tổng thời gian em từng học". */}
              <O nhan="PHÚT (200 LƯỢT GẦN NHẤT)" gia={phut === null ? '…' : phut} />
              <O nhan="BUỔI" gia={buoi} />
              <O nhan="LƯỢT TRẢ LỜI" gia={Array.isArray(rows) ? rows.length : '…'} />
            </div>
          </div>

          {/* Chỗ cần kèm — gom từ mọi quyển, nặng nhất lên đầu */}
          {dsHocBa.some((h) => h.canCoGang.length) && (
            <div className="card">
              <div className="kicker">CẦN KÈM NGAY — ĐÃ THỬ MÀ CHƯA QUA</div>
              {dsHocBa.flatMap((h) => h.canCoGang.map((b) => ({ ...b, quyen: h.ten })))
                .sort((x, y) => y.lan - x.lan)
                .slice(0, 8)
                .map((b) => (
                  <div key={b.id}
                       className="mt-1.5 flex items-center gap-2.5 rounded-xl border border-line px-3 py-2 text-[13px]">
                    <span>{b.dangDo ? '⏳' : '🔸'}</span>
                    <span className="min-w-0 flex-1">
                      <b className="block truncate text-navy">Bài {b.so} · {b.ten}</b>
                      <span className="text-[11.5px] text-mute">{b.quyen}</span>
                    </span>
                    <span className="whitespace-nowrap text-[11.5px] text-mute">
                      đúng {b.dung}/{b.tong} · {b.lan} lần
                    </span>
                  </div>
                ))}
            </div>
          )}
        </>
      )}

      {/* ══════════ THEO LỚP · CHƯƠNG · BÀI ══════════ */}
      {tab === 'lop' && dsHocBa.map((h) => {
        const bung = moQuyen === h.ma;
        return (
          <section key={h.ma} className="card">
            <button className="flex w-full items-center gap-2.5 text-left"
                    onClick={() => setMoQuyen(bung ? null : h.ma)}>
              <span className="min-w-0 flex-1">
                <b className="block text-[14.5px] leading-snug text-navy">{h.ten}</b>
                <span className="text-[12px] text-mute">
                  {h.daBatDau
                    ? `${h.datBai}/${h.tongBai} bài · master ${h.masterChuong}/${h.tongChuong} chương · ${h.huyHieu} huy hiệu`
                    : 'chưa mở quyển này'}
                </span>
              </span>
              <span className="h-1.5 w-16 overflow-hidden rounded-full bg-soft">
                <i className="block h-full bg-teal" style={{ width: `${h.phanTram}%` }} />
              </span>
              <span className="text-[13px] text-mute">{bung ? '▾' : '▸'}</span>
            </button>

            {bung && h.chuong.map((c) => (
              <div key={c.so} className="mt-2 rounded-xl border border-line px-3 py-2.5">
                <div className="flex items-center gap-2">
                  <span className="rounded bg-navy px-1.5 py-0.5 text-[11px] font-extrabold text-white">
                    C{c.so}
                  </span>
                  <b className="min-w-0 flex-1 truncate text-[13.5px] text-navy">{c.ten}</b>
                  <span className={`rounded px-1.5 py-0.5 text-[10.5px] font-extrabold ${MAU_MUC[c.muc]}`}>
                    {NHAN_MUC_CHUONG[c.muc]}
                  </span>
                </div>
                <div className="mt-1 text-[11.5px] text-mute">
                  {c.tk.dat}/{c.tk.tong} bài
                  {c.tk.coKy && (c.tk.kyDat ? ' · 🏅 qua kỳ sát hạch'
                    : c.tk.kyDaThi ? ` · ⚔ thi ${c.tk.kyLanTruoc.dung}/${c.tk.kyLanTruoc.tong}, ${c.tk.kyLanTruoc.lan} lần`
                      : ' · ⚔ chưa thi')}
                </div>
                {/* Từng bài một — cô nhìn ra em tắc ở đúng bài nào của chương nào */}
                <div className="mt-1.5 flex flex-wrap gap-1">
                  {(c.bai || []).map((b) => {
                    /* Trạng thái do MÔN chấm sẵn trong học bạ — tầng này chỉ in ra.
                       Trước đây nó gọi thẳng `trangThaiBai` của Toán, một hàm chưa
                       hề được import, nên cả tab này vỡ trắng. */
                    const s = b.trangThai || 'mo';
                    return (
                      <span key={b.id}
                            title={`Bài ${b.so}${b.micro > 1 ? `.${b.micro}` : ''} · ${b.ten} — ${NHAN_TRANG_THAI_BAI[s]}`}
                            className={`flex h-6 min-w-[26px] items-center justify-center rounded px-1 text-[10.5px] font-extrabold text-white ${CHAM_BAI[s]}`}>
                        {b.so}{b.micro > 1 ? `.${b.micro}` : ''}
                      </span>
                    );
                  })}
                </div>
              </div>
            ))}
          </section>
        );
      })}

      {tab === 'lop' && (
        <p className="px-1 pb-2 text-[11.5px] leading-relaxed text-mute">
          Ô xanh = đã đạt · vàng = đang học dở · đỏ = chưa qua câu bẫy · xám nhạt = chưa mở.
        </p>
      )}

      {/* ══════════ THEO CHỦ ĐỀ · DẠNG BÀI ══════════ */}
      {/* Học bạ của môn chỉ nộp `chuDe` khi nạp được bản đồ dạng bài, nên chính `cd`
          đã trả lời câu hỏi "có bản đồ không". Trước đây chỗ này hỏi một biến `banDo`
          chưa hề khai ở đâu — tab vỡ trắng ngay khi cô bấm vào. */}
      {tab === 'chude' && !cd && <p className="card text-mute">Không nạp được bản đồ chủ đề.</p>}
      {tab === 'chude' && cd && (
        <>
          <div className="card">
            <div className="kicker">EM ĐANG ĐỨNG Ở ĐÂU TRÊN {cd.tong} DẠNG BÀI</div>
            <div className="flex flex-wrap gap-2">
              <O nhan="ĐÃ VỮNG" gia={cd.dem.vung} mau="text-teal-dark" />
              <O nhan="ĐANG HỌC" gia={cd.dem.dangHoc} />
              <O nhan="CẦN CỐ GẮNG" gia={cd.dem.canCoGang} mau="text-alert" />
              <O nhan="CHƯA HỌC" gia={cd.dem.chuaHoc} mau="text-mute" />
            </div>
          </div>

          {cd.mang.map((m) => {
            const bung = moMang === m.ma;
            return (
              <section key={m.ma} className="card">
                <button className="flex w-full items-center gap-2.5 text-left"
                        onClick={() => setMoMang(bung ? null : m.ma)}>
                  <span className="min-w-0 flex-1">
                    <b className="block text-[14px] leading-snug text-navy">{m.ten}</b>
                    <span className="text-[11.5px] text-mute">
                      vững {m.dem.vung} · đang học {m.dem.dangHoc} · cần cố gắng {m.dem.canCoGang}
                    </span>
                  </span>
                  <span className="text-[13px] text-mute">{bung ? '▾' : '▸'}</span>
                </button>

                {bung && m.chuDe.map((c) => (
                  <div key={c.ma} className="mt-2 border-t border-line pt-2">
                    <div className="text-[11px] font-extrabold tracking-widest text-mute">{c.ten}</div>
                    {c.dang.map((d) => (
                      <div key={d.ma} className="mt-1.5 rounded-xl border border-line px-3 py-2">
                        <div className="flex items-start gap-2">
                          <span className="min-w-0 flex-1 text-[13px] font-semibold leading-snug text-navy">
                            {d.ten}
                          </span>
                          <span className={`shrink-0 rounded px-1.5 py-0.5 text-[10.5px] font-extrabold ${MAU_TT[d.tinhTrang]}`}>
                            {NHAN_TINH_TRANG[d.tinhTrang]}
                          </span>
                        </div>
                        <div className="mt-1 flex flex-wrap items-center gap-1.5 text-[11.5px] text-mute">
                          {d.thang.map((b) => (
                            <span key={b.lop}
                                  className={`rounded px-1.5 py-0.5 text-[10.5px] font-extrabold ${
                                    d.bacXong.includes(b.lop) ? 'bg-teal text-white'
                                      : d.bacTruot.includes(b.lop) ? 'bg-alert text-white'
                                        : 'bg-soft text-mute'}`}>
                              lớp {b.lop}
                            </span>
                          ))}
                          {d.soBai > 0 && <span>· {d.baiDat}/{d.soBai} bài</span>}
                          {d.vungToi !== null && <span>· vững tới lớp {d.vungToi}</span>}
                        </div>
                      </div>
                    ))}
                  </div>
                ))}
              </section>
            );
          })}
        </>
      )}

      {/* ══════════ NHẬT KÝ TỪNG CÂU ══════════ */}
      {tab === 'nhatky' && (
        <>
          {rows === 'loading' && <p className="card text-mute">Đang mở nhật ký…</p>}
          {Array.isArray(rows) && rows.length === 0 && (
            <p className="card text-mute">Em này chưa có lượt trả lời nào được ghi.</p>
          )}
          {Array.isArray(rows) && rows.length > 0 && (
            <div className="card">
              <div className="kicker">
                NHẬT KÝ TỪNG CÂU · {locDang ? `${nhatKy.length}/${rows.length}` : rows.length} LƯỢT GẦN NHẤT
              </div>

              {/* LỌC THEO DẠNG BÀI — nhìn theo bài, cô thấy "em sai bài 9, 23, 31";
                  nhìn theo dạng, cô thấy cả ba đều là "dấu hiệu chia hết". */}
              {dsDang.length > 1 && (
                <div className="mb-2 flex flex-wrap items-center gap-2">
                  <label className="text-[11.5px] font-extrabold tracking-widest text-mute"
                         htmlFor="loc-dang">DẠNG BÀI</label>
                  <select id="loc-dang" value={locDang} onChange={(e) => setLocDang(e.target.value)}
                          className="min-w-0 flex-1 rounded-xl border-[1.5px] border-line px-2.5 py-1.5 text-[13px]">
                    <option value="">Tất cả ({rows.length} lượt)</option>
                    {dsDang.map(([ma, n]) => (
                      <option key={ma} value={ma}>{m.tenDang(ma)} — {n} lượt</option>
                    ))}
                  </select>
                  {locDang && (
                    <button className="pill bg-soft text-navy" onClick={() => setLocDang('')}>
                      bỏ lọc ✕
                    </button>
                  )}
                </div>
              )}
              {locDang && nhatKy.length === 0 && (
                <p className="py-3 text-center text-[13.5px] text-mute">
                  Không có lượt nào thuộc dạng này.
                </p>
              )}

              <div className="max-h-[70vh] overflow-y-auto">
                {nhatKy.map((a, i) => (
                  <div key={i} className="border-b border-line py-2 text-[13px] last:border-0">
                    <div className="flex items-center gap-2">
                      <span className={`h-2 w-2 flex-none rounded-full ${a.correct ? 'bg-teal' : 'bg-alert'}`} />
                      <span className="w-[76px] flex-none font-mono text-[11.5px] text-mute">
                        {String(a.microId || '').replace('DL:KSN5Q1.', '')}
                      </span>
                      <span className="w-[42px] flex-none font-mono text-[11.5px] text-mute">{a.itemId}</span>
                      <span className="flex-1">
                        {a.correct ? 'đúng' : 'sai'}
                        {a.tries > 1 && <span className="text-mute"> · lần {a.tries}</span>}
                        {a.hintsUsed > 0 && <span className="text-mute"> · xem {a.hintsUsed} gợi ý</span>}
                        {a.ms > 0 && <span className="text-mute"> · {Math.round(a.ms / 1000)}s</span>}
                        {a.phase && <span className="text-mute"> · {CHANG[a.phase] || a.phase}</span>}
                      </span>
                      {a.revealed && <span className="pill flex-none bg-[#F2F6FA] text-mute">đã xem đáp án</span>}
                      {a.mustPass && <span className="pill flex-none bg-alert-pale text-alert">BẪY</span>}
                    </div>
                    {!a.correct && a.answer && (
                      <div className="mt-1 pl-4 text-[12.5px] leading-snug">
                        <span className="text-alert">con trả lời: <b><Chu t={a.answer} /></b></span>
                        {a.expected && <span className="text-mute"> · đáp án: <Chu t={a.expected} /></span>}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </>
  );
}
