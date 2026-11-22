import React, { useEffect, useMemo, useState } from 'react';
import { httpsCallable } from 'firebase/functions';
import { fns } from '../lib/nenTang.js';

/**
 * BIỂU ĐỒ MỘT EM — tab "Biểu đồ" trong màn chi tiết học sinh của cô giáo.
 *
 * Số liệu do hàm nền `bieuDoHocSinh` dựng từ TOÀN BỘ nhật ký của em (xem
 * `functions/src/bieuDo.js`); màn này chỉ vẽ. Hai phần:
 *
 *   A · EM HỌC THẾ NÀO — đếm thẳng từ nhật ký
 *     1. tỉ lệ đúng ngay lần đầu theo tuần        3. phút học mỗi tuần
 *     2. số bài đã học cộng dồn                    4. giờ bắt đầu buổi học
 *
 *   B · MÔ HÌNH NGƯỜI HỌC — đúng các hình của luận văn, chạy lại BKT trên lượt của em
 *     5. đường cong học tập (mục 2.5)             8. hồ sơ trước/sau khi tính quên (Hình 3.13)
 *     6. số nút đạt θ theo tuần                    9. diễn biến P(L) và số lần sai liên
 *     7. sáu tình trạng của nút (Bảng 3.9, Hình 3.10)  tiếp tại một nút (Hình 3.14, 3.16)
 *
 * ── MỖI BIỂU ĐỒ PHẢI TỰ NÓI ĐƯỢC NÓ LÀ GÌ ──
 * Tên trục ngang, tên trục dọc (kèm đơn vị) và một dòng "Cách đọc". Cô giáo không có
 * luận văn trong tay; một biểu đồ phải nhìn vào là hiểu, không cần ai giải thích.
 *
 * ── MÀU ──
 * Hai môn, hai màu cố định theo MÔN: Toán xanh khiên, Tiếng Anh cam. Hai đường "đã
 * lưu / sau khi tính quên" dùng cặp lục–tím, KHÔNG mượn màu môn để không đọc nhầm
 * thành môn. Cả hai cặp đã qua bộ kiểm màu (mù màu ΔE ≥ 17; tương phản ≥ 3:1). Màu
 * chỉ để nhận chuỗi — chuỗi luôn có chú giải bằng chữ đi kèm.
 */
const MAU_MON = { toan: '#0B4EA8', tienganh: '#D97A0B' };
const TEN_MON = { toan: 'Toán', tienganh: 'Tiếng Anh' };
const MAU_LUU = '#0E8A74';
const MAU_QUEN = '#7B4FC9';
const MAU_COT = '#1268D6';
const LUOI = '#D4E1EE';
const CHU_PHU = '#5B6E85';
const CHU = '#15263A';

const W = 640;
const H = 240;
const LE = { trai: 58, phai: 14, tren: 14, duoi: 46 };

const ngayNgan = (iso) => { const [, m, d] = iso.split('-'); return `${+d}/${+m}`; };
const so = (v, chu = 0) => (v == null ? '—' : Number(v).toLocaleString('vi-VN',
  { minimumFractionDigits: chu, maximumFractionDigits: chu }));

/**
 * Khung chung: lưới ngang mờ, nhãn hai trục, TÊN hai trục, và đường tham chiếu.
 * `dai` = thang dải (mỗi điểm một ô, cho biểu đồ cột); không có thì thang điểm.
 */
function Khung({ xs, yMax, yNhan, xTen, yTen, children, onDi, onRoi, chuThich,
  dai = false, thamChieu = [], dinhDangY = (v) => so(v) }) {
  const rong = W - LE.trai - LE.phai;
  const cao = H - LE.tren - LE.duoi;
  const buoc = Math.max(1, Math.ceil(xs.length / 8));
  const Y = (v) => LE.tren + cao - (v / yMax) * cao;
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="block h-auto w-full" role="img"
         aria-label={`${chuThich}. Trục ngang: ${xTen}. Trục dọc: ${yTen}.`}
         onMouseMove={onDi} onMouseLeave={onRoi}>
      {yNhan.map((v) => (
        <g key={v}>
          <line x1={LE.trai} x2={W - LE.phai} y1={Y(v)} y2={Y(v)} stroke={LUOI} strokeWidth="1" />
          <text x={LE.trai - 6} y={Y(v) + 4} textAnchor="end" fontSize="11" fill={CHU_PHU}>{dinhDangY(v)}</text>
        </g>
      ))}
      {/* Nhãn cuối luôn hiện, nhưng chỉ khi nó không dính vào nhãn thưa ngay trước. */}
      {xs.map((x, i) => (i % buoc === 0
        || (i === xs.length - 1 && (xs.length - 1) % buoc >= Math.max(2, buoc / 2))) && (
        <text key={i} x={dai ? LE.trai + (rong / xs.length) * (i + 0.5)
                         : LE.trai + (xs.length === 1 ? rong / 2 : (i * rong) / (xs.length - 1))}
              y={LE.tren + cao + 17} textAnchor="middle" fontSize="11" fill={CHU_PHU}>{x}</text>
      ))}
      {/* TÊN TRỤC — ngang ở dưới, dọc xoay dọc bên trái */}
      <text x={LE.trai + rong / 2} y={H - 6} textAnchor="middle" fontSize="11.5" fontWeight="700" fill={CHU}>
        {xTen}
      </text>
      <text x={13} y={LE.tren + cao / 2} textAnchor="middle" fontSize="11.5" fontWeight="700" fill={CHU}
            transform={`rotate(-90 13 ${LE.tren + cao / 2})`}>
        {yTen}
      </text>
      {children({ rong, cao, Y })}
      {/* Đường tham chiếu (ngưỡng θ, θ_yếu…) vẽ SAU dữ liệu để luôn nhìn thấy. */}
      {thamChieu.map((t) => (
        <g key={t.nhan}>
          <line x1={LE.trai} x2={W - LE.phai} y1={Y(t.v)} y2={Y(t.v)}
                stroke={CHU_PHU} strokeWidth="1.2" strokeDasharray="5 4" />
          <text x={W - LE.phai - 2} y={Y(t.v) - 4} textAnchor="end" fontSize="10.5" fontWeight="700" fill={CHU_PHU}>
            {t.nhan}
          </text>
        </g>
      ))}
    </svg>
  );
}

/** Đổi vị trí chuột thành chỉ số điểm gần nhất. */
const chiSoTu = (e, n, dai = false) => {
  const r = e.currentTarget.getBoundingClientRect();
  const x = ((e.clientX - r.left) / r.width) * W;
  const t = (x - LE.trai) / (W - LE.trai - LE.phai);
  const k = dai ? Math.floor(t * n) : Math.round(t * (n - 1));
  return Math.max(0, Math.min(n - 1, k));
};

/** Chú giải bằng chữ — kể cả khi chỉ một chuỗi, vì "đường cam" không tự nói nó là gì. */
function ChuGiai({ chuoi }) {
  if (!chuoi.length) return null;
  return (
    <div className="mb-1 flex flex-wrap gap-3 text-[12px] text-ink">
      {chuoi.map((c) => (
        <span key={c.ma} className="flex items-center gap-1.5">
          <i className="inline-block h-[3px] w-4 rounded" style={{ background: c.mau }} />
          {c.ten}
        </span>
      ))}
    </div>
  );
}

function Nhac({ dong }) {
  if (!dong) return null;
  return (
    <div className="mt-1 rounded-lg bg-soft px-2.5 py-1.5 text-[12px] text-ink tabular-nums">{dong}</div>
  );
}

/**
 * Nhiều đường trên một trục. `chuoi` = [{ma, ten, mau, gia: (k) => số | null}].
 * Điểm null thì NGẮT đường (tuần không có lượt), không nối tắt qua.
 */
function Duong({ xs, chuoi, yMax, yNhan, xTen, yTen, chuThich, nhacCua, nhanCuoi,
  thamChieu, dinhDangY, cham }) {
  const [i, setI] = useState(null);
  return (
    <>
      <ChuGiai chuoi={chuoi} />
      <Khung xs={xs} yMax={yMax} yNhan={yNhan} xTen={xTen} yTen={yTen} chuThich={chuThich}
             thamChieu={thamChieu} dinhDangY={dinhDangY}
             onDi={(e) => setI(chiSoTu(e, xs.length))} onRoi={() => setI(null)}>
        {({ rong, Y }) => {
          const X = (k) => LE.trai + (xs.length === 1 ? rong / 2 : (k * rong) / (xs.length - 1));
          return (
            <>
              {i !== null && <line x1={X(i)} x2={X(i)} y1={LE.tren} y2={Y(0)}
                                   stroke={CHU_PHU} strokeWidth="1" strokeDasharray="3 3" />}
              {chuoi.map((c) => {
                const doan = [];
                let cur = [];
                xs.forEach((_, k) => {
                  const v = c.gia(k);
                  if (v == null) { if (cur.length) doan.push(cur); cur = []; } else cur.push([X(k), Y(v)]);
                });
                if (cur.length) doan.push(cur);
                let cuoi = null;
                for (let k = xs.length - 1; k >= 0; k--) {
                  if (c.gia(k) != null) { cuoi = [k, c.gia(k)]; break; }
                }
                return (
                  <g key={c.ma}>
                    {doan.map((d, j) => (d.length > 1
                      ? <polyline key={j} points={d.map((p) => p.join(',')).join(' ')} fill="none"
                                  stroke={c.mau} strokeWidth="2" strokeLinejoin="round" strokeLinecap="round" />
                      : <circle key={j} cx={d[0][0]} cy={d[0][1]} r="3" fill={c.mau} />))}
                    {/* Chấm từng điểm (khi được yêu cầu): đặc = đúng, rỗng = sai. Phân biệt
                        bằng HÌNH chứ không bằng màu, để người mù màu vẫn đọc được. */}
                    {cham && xs.map((_, k) => c.gia(k) != null && (
                      <circle key={k} cx={X(k)} cy={Y(c.gia(k))} r="4"
                              fill={cham(k) ? c.mau : '#fff'} stroke={c.mau} strokeWidth="2" />
                    ))}
                    {i !== null && c.gia(i) != null && (
                      <circle cx={X(i)} cy={Y(c.gia(i))} r="5" fill={c.mau} stroke="#fff" strokeWidth="2" />
                    )}
                    {cuoi && nhanCuoi && (
                      <text x={Math.min(X(cuoi[0]), W - LE.phai) - 2} y={Y(cuoi[1]) - 8}
                            textAnchor="end" fontSize="11" fontWeight="700" fill={CHU}>
                        {nhanCuoi(c, cuoi[1])}
                      </text>
                    )}
                  </g>
                );
              })}
            </>
          );
        }}
      </Khung>
      <Nhac dong={i !== null ? nhacCua(i) : null} />
    </>
  );
}

/** Đường dẫn một cột: đầu bo 4px, chân vuông, đứng trên đường đáy. */
const duongCot = (x, y, be, h) => {
  if (h <= 0) return '';
  const r = Math.min(4, be / 2, h);
  return `M${x},${y + h} V${y + r} Q${x},${y} ${x + r},${y} H${x + be - r} Q${x + be},${y} ${x + be},${y + r} V${y + h} Z`;
};

/**
 * Cột — một hoặc nhiều chuỗi, các chuỗi đứng cạnh nhau trong mỗi ô (cách nhau 2px).
 * `chuoi` = [{ma, ten, mau, gia: number[]}].
 */
function Cot({ xs, chuoi, yMax, yNhan, xTen, yTen, chuThich, nhacCua, thamChieu, nhanTren = false }) {
  const [i, setI] = useState(null);
  return (
    <>
      {chuoi.length > 1 && <ChuGiai chuoi={chuoi} />}
      <Khung xs={xs} yMax={yMax} yNhan={yNhan} xTen={xTen} yTen={yTen} chuThich={chuThich} dai
             thamChieu={thamChieu}
             onDi={(e) => setI(chiSoTu(e, xs.length, true))} onRoi={() => setI(null)}>
        {({ rong, cao, Y }) => {
          const o = rong / Math.max(1, xs.length);
          const nhom = Math.max(3, Math.min(28 * chuoi.length + 2 * (chuoi.length - 1), o - 4));
          const be = (nhom - 2 * (chuoi.length - 1)) / chuoi.length;
          return xs.map((_, k) => (
            <g key={k}>
              <rect x={LE.trai + o * k} y={LE.tren} width={o} height={cao} fill="transparent" />
              {chuoi.map((c, j) => {
                const v = c.gia[k] || 0;
                const x = LE.trai + o * (k + 0.5) - nhom / 2 + j * (be + 2);
                const h = (v / yMax) * cao;
                return (
                  <g key={c.ma} opacity={i === null || i === k ? 1 : 0.45}>
                    <path d={duongCot(x, Y(v), be, h)} fill={c.mau} />
                    {/* Cột 0 vẫn in số 0 — không có số thì cô tưởng thiếu dữ liệu. */}
                    {nhanTren && (
                      <text x={x + be / 2} y={Y(v) - 4} textAnchor="middle" fontSize="11"
                            fontWeight="700" fill={CHU}>{so(v)}</text>
                    )}
                  </g>
                );
              })}
            </g>
          ));
        }}
      </Khung>
      <Nhac dong={i !== null ? nhacCua(i) : null} />
    </>
  );
}

/** Trục dọc "đẹp": bốn nấc, mỗi nấc 1 · 2 · 2,5 · 5 × 10ⁿ — không ra 23, 68. */
function trucY(v) {
  const tho = Math.max(1, v) / 4;
  const mu = 10 ** Math.floor(Math.log10(tho));
  const buoc = [1, 2, 2.5, 5, 10].map((x) => x * mu).find((x) => x >= tho);
  const nac = Math.max(1, Math.round(buoc));
  return { max: nac * 4, nhan: [0, 1, 2, 3, 4].map((k) => k * nac) };
}
const TRUC_PHAN_TRAM = { max: 100, nhan: [0, 25, 50, 75, 100] };
const TRUC_XAC_SUAT = { max: 1, nhan: [0, 0.25, 0.5, 0.75, 1] };

/** Khung một biểu đồ: câu hỏi, chỗ trong luận văn, biểu đồ, và cách đọc. */
function The({ tieuDe, luanVan, children, cachDoc }) {
  return (
    <section className="card">
      <div className="kicker">{tieuDe}</div>
      {luanVan && <p className="-mt-1 mb-1.5 text-[11.5px] font-semibold text-navy-light">Theo luận văn: {luanVan}</p>}
      {children}
      <p className="mt-1.5 text-[12px] leading-snug text-mute"><b className="text-ink">Cách đọc:</b> {cachDoc}</p>
    </section>
  );
}

/** Bảng số liệu — cho người không đọc được biểu đồ, và để cô chép số. */
function BangSo({ bd }) {
  const nv = new Map((bd.moHinh?.nutVung || []).map((x) => [x.tuan, x]));
  return (
    <div className="max-h-[50vh] overflow-auto">
      <table className="w-full text-[12px] tabular-nums">
        <thead className="text-left text-mute">
          <tr>
            <th className="py-1 pr-2">Tuần từ</th>
            {bd.mon.map((m) => <th key={m} className="pr-2">Đúng lần đầu · {TEN_MON[m]}</th>)}
            {bd.mon.map((m) => <th key={`b${m}`} className="pr-2">Bài đã học · {TEN_MON[m]}</th>)}
            <th className="pr-2">Phút</th><th className="pr-2">Buổi</th><th className="pr-2">Giây/câu</th>
            <th className="pr-2">Nút đạt θ (đã lưu)</th><th>Nút đạt θ (tính quên)</th>
          </tr>
        </thead>
        <tbody>
          {bd.tuan.map((t) => (
            <tr key={t.tuan} className="border-t border-line">
              <td className="py-1 pr-2">{ngayNgan(t.tuan)}</td>
              {bd.mon.map((m) => <td key={m} className="pr-2">{t.mon[m]?.dungLanDau ?? '—'}{t.mon[m]?.dungLanDau != null && '%'}</td>)}
              {bd.mon.map((m) => <td key={`b${m}`} className="pr-2">{t.mon[m]?.baiDaHoc ?? 0}</td>)}
              <td className="pr-2">{t.phut}</td><td className="pr-2">{t.buoi}</td><td className="pr-2">{so(t.giayMoiCau, 1)}</td>
              <td className="pr-2">{nv.get(t.tuan)?.vungLuu ?? '—'}</td><td>{nv.get(t.tuan)?.vungQuen ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/** Hình 3.14 / 3.16 — P(L) và số lần sai liên tiếp qua từng lượt tại MỘT nút. */
function DienBienNut({ dienBien, nguong }) {
  const [chon, setChon] = useState(0);
  const d = dienBien[Math.min(chon, dienBien.length - 1)];
  if (!d) return null;
  const xs = d.luot.map((_, k) => `${d.soLuot - d.luot.length + k + 1}`);
  const mau = MAU_MON[d.mon] || MAU_COT;
  const maxSai = trucY(Math.max(nguong.nguongMac + 1, ...d.luot.map((x) => x.sai)));
  const ngay = (ts) => new Date(ts).toLocaleDateString('vi-VN');
  return (
    <>
      <div className="mb-2 flex flex-wrap items-center gap-2">
        <label htmlFor="chon-nut" className="text-[11.5px] font-extrabold tracking-widest text-mute">NÚT</label>
        <select id="chon-nut" value={chon} onChange={(e) => setChon(Number(e.target.value))}
                className="min-w-0 flex-1 rounded-xl border-[1.5px] border-line px-2.5 py-1.5 text-[13px]">
          {dienBien.map((x, k) => (
            <option key={x.nut} value={k}>
              {x.nut} · {TEN_MON[x.mon]} · {x.soLuot} lượt{x.tungMac ? ' · từng "đang mắc"' : ''}
            </option>
          ))}
        </select>
      </div>
      <Duong xs={xs} chuoi={[{ ma: 'p', ten: `Mức nắm vững P(L) sau mỗi lượt · nút ${d.nut}`, mau,
        gia: (k) => d.luot[k].p }]}
             yMax={1} yNhan={TRUC_XAC_SUAT.nhan} dinhDangY={(v) => so(v, 2)}
             xTen="Lượt trả lời thứ mấy tại nút này" yTen="P(L) — mức nắm vững (0–1)"
             chuThich="Diễn biến mức nắm vững tại một nút"
             thamChieu={[{ v: nguong.theta, nhan: `θ = ${so(nguong.theta, 2)} (đã nắm vững)` },
               { v: nguong.thetaYeu, nhan: `θ_yếu = ${so(nguong.thetaYeu, 2)}` }]}
             cham={(k) => d.luot[k].dung}
             nhacCua={(k) => `Lượt ${xs[k]} (${ngay(d.luot[k].ts)}): ${d.luot[k].dung ? 'đúng' : 'sai'} · P(L) trước lượt ${so(d.luot[k].pTruoc, 3)} (đã tính quên) → sau lượt ${so(d.luot[k].p, 3)} · sai liên tiếp ${d.luot[k].sai}`} />
      <div className="mt-3" />
      <Cot xs={xs} chuoi={[{ ma: 's', ten: 'Số lần sai liên tiếp', mau: MAU_COT, gia: d.luot.map((x) => x.sai) }]}
           yMax={maxSai.max} yNhan={maxSai.nhan}
           xTen="Lượt trả lời thứ mấy tại nút này" yTen="Số lần sai liên tiếp (S_c)"
           chuThich="Số lần sai liên tiếp tại một nút"
           thamChieu={[{ v: nguong.nguongMac, nhan: `NG09 = ${nguong.nguongMac} → "đang mắc", bật phụ đạo` }]}
           nhacCua={(k) => `Lượt ${xs[k]}: sai liên tiếp ${d.luot[k].sai}`} />
      {d.soLuot > d.luot.length && (
        <p className="mt-1 text-[11.5px] text-mute">Hiện {d.luot.length} lượt gần nhất trên tổng {d.soLuot} lượt của nút.</p>
      )}
    </>
  );
}

export default function BieuDoHocSinh({ uid }) {
  const [bd, setBd] = useState(null);
  const [loi, setLoi] = useState('');
  const [xemBang, setXemBang] = useState(false);

  useEffect(() => {
    let song = true;
    setBd(null); setLoi('');
    if (!fns) { setLoi('Chưa cấu hình máy chủ.'); return undefined; }
    httpsCallable(fns, 'bieuDoHocSinh')({ uid })
      .then(({ data }) => song && setBd(data))
      .catch((e) => song && setLoi(String(e?.message || e)));
    return () => { song = false; };
  }, [uid]);

  const xs = useMemo(() => (bd?.tuan || []).map((t) => ngayNgan(t.tuan)), [bd]);

  if (loi) return <p className="card text-alert">Không mở được biểu đồ: {loi}</p>;
  if (!bd) return <p className="card text-mute">Đang dựng biểu đồ từ toàn bộ nhật ký của em…</p>;
  if (!bd.soLuot) return <p className="card text-mute">Em chưa có lượt trả lời nào để vẽ.</p>;

  const tuan = bd.tuan;
  const chuoiMon = (gia) => bd.mon.map((m) => ({ ma: m, ten: TEN_MON[m] || m, mau: MAU_MON[m], gia: (k) => gia(m, k) }));
  const yPhut = trucY(Math.max(...tuan.map((t) => t.phut)));
  const yBai = trucY(Math.max(...bd.mon.map((m) => tuan[tuan.length - 1].mon[m]?.baiDaHoc || 0)));
  const yBuoi = trucY(Math.max(...bd.gioHoc.map((g) => g.buoi)));
  const tu = new Date(bd.tuLuc).toLocaleDateString('vi-VN');
  const den = new Date(bd.denLuc).toLocaleDateString('vi-VN');
  const XT = 'Tuần học (ngày thứ Hai đầu tuần)';

  const mh = bd.moHinh || {};
  const ng = { theta: 0.85, thetaYeu: 0.3, nguongMac: 3, ngayQuen: 14, nuaDoi: 14, tua: 0.5, ...mh.nguong };
  const monCong = Object.keys(mh.duongCong || {}).filter((m) => mh.duongCong[m].some((o) => o.tiLeLoi != null)).sort();
  const lanCong = Array.from({ length: Math.max(0, ...monCong.map((m) => mh.duongCong[m].length)) }, (_, k) => `${k + 1}`);
  const nv = mh.nutVung || [];
  const yNut = trucY(Math.max(...nv.map((x) => x.vungLuu), 1));
  const tt = mh.tinhTrang;
  const TEN_TT = ['Đang mắc', 'Yếu hẳn', 'Vùng PT gần', 'Đã nắm vững', 'Nguy cơ quên*'];
  const TEN_TT_DU = ['Đang mắc', 'Yếu hẳn', 'Vùng phát triển gần', 'Đã nắm vững', 'Có nguy cơ quên (cờ)'];
  const giaTT = tt ? [tt.dangMac, tt.yeu, tt.vungGan, tt.daVung, tt.nguyCoQuen] : [];
  const yTT = trucY(Math.max(...giaTT, 1));
  const hq = mh.hoSoQuen;
  const DAI = [`< ${so(ng.thetaYeu, 2)} (yếu hẳn)`, `${so(ng.thetaYeu, 2)}–${so(ng.theta, 2)} (đang học)`, `≥ ${so(ng.theta, 2)} (đã vững)`];
  const yHq = hq ? trucY(Math.max(...hq.truoc, ...hq.sau, 1)) : null;

  return (
    <>
      <div className="card">
        <div className="kicker">TỪ {tu} ĐẾN {den} · {bd.soLuot.toLocaleString('vi-VN')} LƯỢT · {tuan.length} TUẦN</div>
        <p className="text-[13px] leading-relaxed text-mute">
          Dựng từ toàn bộ nhật ký của em, không chỉ 7 ngày gần nhất. Rê chuột lên biểu đồ để xem số từng điểm.
          Phần B chạy lại đúng thuật toán BKT có tính quên của hệ thống trên từng lượt của em, với bộ ngưỡng
          đang dùng (θ = {so(ng.theta, 2)}, θ_yếu = {so(ng.thetaYeu, 2)}, đang mắc khi sai {ng.nguongMac} lần liền,
          nguy cơ quên sau {ng.ngayQuen} ngày).
        </p>
        <button className="mt-2 rounded-full border-[1.5px] border-navy px-2.5 py-0.5 text-[11.5px] font-bold text-navy"
                onClick={() => setXemBang(!xemBang)}>
          {xemBang ? 'Ẩn bảng số' : 'Xem dạng bảng số'}
        </button>
        {xemBang && <div className="mt-2"><BangSo bd={bd} /></div>}
      </div>

      <h2 className="mb-2 mt-4 px-1 text-[13px] font-extrabold tracking-wide text-navy">A · EM HỌC THẾ NÀO</h2>

      <The tieuDe="1 · EM CÓ TIẾN BỘ KHÔNG — TỈ LỆ ĐÚNG NGAY LẦN ĐẦU THEO TUẦN"
           cachDoc="Mỗi điểm là một tuần. Đường đi lên là em làm đúng ngay từ lần đầu nhiều hơn. Chỉ tính lần thử đầu của mỗi câu — câu làm lại sau gợi ý không được tính, để con số không bị đẩy lên. Đường đứt quãng là tuần em không học môn đó.">
        <Duong xs={xs} chuoi={chuoiMon((m, k) => tuan[k].mon[m]?.dungLanDau ?? null)}
               yMax={100} yNhan={TRUC_PHAN_TRAM.nhan} xTen={XT} yTen="% câu đúng ngay lần đầu"
               chuThich="Tỉ lệ đúng lần đầu theo tuần" nhanCuoi={(c, v) => `${v}%`}
               nhacCua={(k) => `Tuần từ ${ngayNgan(tuan[k].tuan)}: ${bd.mon.map((m) =>
                 `${TEN_MON[m]} ${tuan[k].mon[m]?.dungLanDau ?? '—'}${tuan[k].mon[m]?.dungLanDau != null ? '%' : ''} (${tuan[k].mon[m]?.luot || 0} lượt)`).join(' · ')}`} />
      </The>

      <The tieuDe="2 · EM ĐI ĐƯỢC BAO XA — SỐ BÀI ĐÃ HỌC, CỘNG DỒN"
           cachDoc="Mỗi điểm là tổng số bài em đã mở và làm ít nhất một câu tính tới hết tuần đó. Đường dốc là tuần em học nhiều bài mới; đường nằm ngang là em đã đi hết bài và chỉ còn ôn. “Đã học” chưa chắc đã đạt — số bài đạt xem ở tab Tổng quan.">
        <Duong xs={xs} chuoi={chuoiMon((m, k) => tuan[k].mon[m]?.baiDaHoc ?? null)}
               yMax={yBai.max} yNhan={yBai.nhan} xTen={XT} yTen="Số bài đã học (cộng dồn)"
               chuThich="Số bài đã học cộng dồn theo tuần" nhanCuoi={(c, v) => `${v} bài`}
               nhacCua={(k) => `Đến hết tuần ${ngayNgan(tuan[k].tuan)}: ${bd.mon.map((m) =>
                 `${TEN_MON[m]} ${tuan[k].mon[m]?.baiDaHoc || 0} bài`).join(' · ')}`} />
      </The>

      <The tieuDe="3 · EM HỌC CÓ ĐỀU KHÔNG — PHÚT HỌC MỖI TUẦN"
           cachDoc="Mỗi cột là một tuần, chiều cao là số phút em thực sự làm bài trong tuần đó. Cột đều nhau là em học đều; cột thấp hẳn là tuần em nghỉ hoặc chỉ ôn. Tính từ khoảng cách giữa các câu trả lời, nghỉ quá 5 phút thì không cộng — nên chưa gồm thời gian xem giảng.">
        <Cot xs={xs} chuoi={[{ ma: 'phut', ten: 'Phút học', mau: MAU_COT, gia: tuan.map((t) => t.phut) }]}
             yMax={yPhut.max} yNhan={yPhut.nhan} xTen={XT} yTen="Số phút học trong tuần"
             chuThich="Phút học mỗi tuần"
             nhacCua={(k) => `Tuần từ ${ngayNgan(tuan[k].tuan)}: ${tuan[k].phut} phút · ${tuan[k].buoi} buổi · ${so(tuan[k].giayMoiCau, 1)} giây mỗi câu`} />
      </The>

      {bd.gioHoc.length > 0 && (
        <The tieuDe="4 · EM HAY HỌC LÚC MẤY GIỜ — SỐ BUỔI THEO GIỜ BẮT ĐẦU"
             cachDoc="Mỗi cột là một khung nửa tiếng (giờ Việt Nam), chiều cao là số buổi học em bắt đầu trong khung đó, tính theo câu trả lời đầu tiên của buổi.">
          <Cot xs={bd.gioHoc.map((g) => g.khung)} chuoi={[{ ma: 'buoi', ten: 'Số buổi', mau: MAU_COT, gia: bd.gioHoc.map((g) => g.buoi) }]}
               yMax={yBuoi.max} yNhan={yBuoi.nhan} xTen="Giờ bắt đầu buổi học (khung 30 phút)" yTen="Số buổi học"
               chuThich="Số buổi theo giờ bắt đầu"
               nhacCua={(k) => `Bắt đầu từ ${bd.gioHoc[k].khung}: ${bd.gioHoc[k].buoi} buổi`} />
        </The>
      )}

      <h2 className="mb-2 mt-4 px-1 text-[13px] font-extrabold tracking-wide text-navy">B · MÔ HÌNH NGƯỜI HỌC (CÁC HÌNH CỦA LUẬN VĂN)</h2>

      {monCong.length > 0 && (
        <The tieuDe="5 · ĐƯỜNG CONG HỌC TẬP — TỈ LỆ LỖI THEO LẦN LUYỆN"
             luanVan="mục 2.5 (đường cong học tập) và mục 3.9 (bốn nhóm độ đo)"
             cachDoc={`Trục ngang là lần thứ mấy em gặp lại cùng một nút kiến thức (Tiếng Anh: một từ hoặc một mẫu câu; Toán: một bài). Trục dọc là tỉ lệ câu em làm sai ở lần đó. Đường đi xuống dần là em đang thật sự học được; đường đi ngang hoặc lên xuống thất thường là dấu hiệu học thuộc mà không hiểu, cô nên xem lại. Điểm có ít hơn 10 lượt bị bỏ, không vẽ.`}>
          <Duong xs={lanCong} chuoi={monCong.map((m) => ({ ma: m, ten: TEN_MON[m], mau: MAU_MON[m],
            gia: (k) => mh.duongCong[m][k]?.tiLeLoi ?? null }))}
                 yMax={100} yNhan={TRUC_PHAN_TRAM.nhan} xTen="Lần luyện thứ k tại cùng một nút" yTen="% câu sai (tỉ lệ lỗi)"
                 chuThich="Đường cong học tập" nhanCuoi={(c, v) => `${v}%`}
                 nhacCua={(k) => `Lần luyện thứ ${k + 1}: ${monCong.map((m) => {
                   const o = mh.duongCong[m][k];
                   return `${TEN_MON[m]} ${o?.tiLeLoi ?? '—'}${o?.tiLeLoi != null ? '%' : ''} sai (${o?.tong || 0} lượt)`;
                 }).join(' · ')}`} />
        </The>
      )}

      {nv.length > 0 && (
        <The tieuDe="6 · SỐ NÚT KIẾN THỨC ĐẠT NGƯỠNG NẮM VỮNG θ THEO TUẦN"
             luanVan="mục 2.3.3 (ngưỡng θ), Hình 3.9 (hàm quên) và Hình 3.13 (trước và sau khi tính quên)"
             cachDoc={`Mỗi điểm là cuối một tuần. Đường lục đếm số nút có P(L) ≥ ${so(ng.theta, 2)} theo giá trị lưu ở lần gặp gần nhất. Đường tím đếm lại sau khi tính quên tới cuối tuần đó (chu kỳ bán rã ${so(ng.nuaDoi)} ngày): khoảng cách giữa hai đường là phần em đã nắm nhưng có thể đã quên — đó là lý do hệ thống đưa nút vào lịch ôn.`}>
          <Duong xs={nv.map((x) => ngayNgan(x.tuan))}
                 chuoi={[{ ma: 'luu', ten: 'Đạt θ theo P(L) đã lưu', mau: MAU_LUU, gia: (k) => nv[k].vungLuu },
                   { ma: 'quen', ten: 'Còn đạt θ sau khi tính quên', mau: MAU_QUEN, gia: (k) => nv[k].vungQuen }]}
                 yMax={yNut.max} yNhan={yNut.nhan} xTen={XT} yTen="Số nút đạt θ"
                 chuThich="Số nút đạt ngưỡng nắm vững theo tuần" nhanCuoi={(c, v) => `${v} nút`}
                 nhacCua={(k) => `Cuối tuần ${ngayNgan(nv[k].tuan)}: đã gặp ${nv[k].daGap} nút · đạt θ (đã lưu) ${nv[k].vungLuu} · còn đạt sau khi tính quên ${nv[k].vungQuen}`} />
        </The>
      )}

      {tt && (
        <The tieuDe={`7 · SÁU TÌNH TRẠNG CỦA NÚT — HIỆN TẠI, TRÊN ${tt.tong} NÚT EM ĐÃ GẶP`}
             luanVan="Bảng 3.9 và Hình 3.10 (sáu tình trạng của một nút)"
             cachDoc={`Mỗi cột đếm số nút ở một tình trạng. Đang mắc: sai từ ${ng.nguongMac} lần liền (xét trước) — hệ thống bật phụ đạo. Yếu hẳn: P(L) < ${so(ng.thetaYeu, 2)} — bật phụ đạo. Vùng phát triển gần (Vùng PT gần): đang học, câu của nút được xếp lên đầu. Đã nắm vững: P(L) ≥ ${so(ng.theta, 2)}. Nguy cơ quên (*) là CỜ (chưa gặp lại từ ${ng.ngayQuen} ngày), đi kèm một trong bốn tình trạng kia nên đếm riêng. “Chưa có số liệu” (nút chưa gặp) không vẽ.`}>
          <Cot xs={TEN_TT} chuoi={[{ ma: 'tt', ten: 'Số nút', mau: MAU_COT, gia: giaTT }]} nhanTren
               yMax={yTT.max} yNhan={yTT.nhan} xTen="Tình trạng của nút (luật nhận dạng ở Bảng 3.9)" yTen="Số nút"
               chuThich="Số nút theo tình trạng"
               nhacCua={(k) => `${TEN_TT_DU[k]}: ${giaTT[k]} nút`} />
        </The>
      )}

      {hq && (
        <The tieuDe="8 · HỒ SƠ NÚT TRƯỚC VÀ SAU KHI TÍNH QUÊN — TỚI HÔM NAY"
             luanVan="Hình 3.13 (hồ sơ nút của người học trước phiên: trước và sau khi tính quên)"
             cachDoc={`Mỗi nhóm cột là một dải P(L). Cột lục: số nút theo P(L) đã lưu ở lần gặp gần nhất. Cột tím: cùng các nút ấy nếu em mở bài hôm nay — P(L) bị kéo dần về ${so(ng.tua, 1)} theo số ngày chưa gặp lại. Cột “đã vững” tụt mạnh nghĩa là nhiều nút cần ôn lại.`}>
          <Cot xs={DAI} chuoi={[{ ma: 'truoc', ten: 'P(L) đã lưu', mau: MAU_LUU, gia: hq.truoc },
            { ma: 'sau', ten: 'Sau khi tính quên tới hôm nay', mau: MAU_QUEN, gia: hq.sau }]} nhanTren
               yMax={yHq.max} yNhan={yHq.nhan} xTen="Dải mức nắm vững P(L)" yTen="Số nút"
               chuThich="Hồ sơ nút trước và sau khi tính quên"
               nhacCua={(k) => `${DAI[k]}: đã lưu ${hq.truoc[k]} nút → sau khi tính quên ${hq.sau[k]} nút`} />
        </The>
      )}

      {mh.dienBien?.length > 0 && (
        <The tieuDe="9 · DIỄN BIẾN TẠI MỘT NÚT — MỨC NẮM VỮNG VÀ SỐ LẦN SAI LIÊN TIẾP"
             luanVan="Hình 3.14 (diễn biến qua mười một lượt) và Hình 3.16 (mức nắm vững tại nút nguyên nhân qua bài phụ đạo)"
             cachDoc={`Chọn một nút ở ô trên (ưu tiên nút từng “đang mắc”). Biểu đồ trên: P(L) của nút sau từng lượt; chấm đặc là trả lời đúng, chấm rỗng là sai; vạch đứt là hai ngưỡng θ và θ_yếu. Biểu đồ dưới: số lần sai liên tiếp sau từng lượt; chạm vạch ${ng.nguongMac} là nút thành “đang mắc” và hệ thống bật phụ đạo. Hai đại lượng khác đơn vị nên vẽ thành hai biểu đồ, cùng trục ngang.`}>
          <DienBienNut dienBien={mh.dienBien} nguong={ng} />
        </The>
      )}
    </>
  );
}
