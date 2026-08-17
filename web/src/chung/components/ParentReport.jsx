import React, { useEffect, useMemo, useState } from 'react';
import Chu from './Chu.jsx';
import ThanhTren from './ThanhTren.jsx';
import { NHAN_MUC_CHUONG, NHAN_TINH_TRANG } from '../lib/nhanHocBa.js';

/**
 * SỔ HỌC CỦA CON — dành cho bố mẹ.
 *
 * ── VÌ SAO VIẾT LẠI ──
 * Bản cũ chỉ nhìn được MỘT quyển (quyển con đang mở), và nhìn bằng con số gõ cứng của
 * lớp 5: "14 chương", "b.done/12". Mở sổ từ trang lớp 4 thì bố mẹ thấy 14 ô chương
 * trong đó 3 ô không tồn tại, và mọi ô chia cho 12 trong khi chương lớp 4 có 4 bài.
 * Con số sai mà trông vẫn như số thật — thứ tệ nhất một cái sổ có thể làm.
 *
 * Nay sổ trả lời đúng bốn câu bố mẹ hỏi, trên CẢ BỐN QUYỂN:
 *   1. con đang ở đâu          → thẻ TRÌNH ĐỘ HIỆN TẠI;
 *   2. con MASTER chương nào   → tab THEO LỚP, từng quyển từng chương;
 *   3. con vững CHỦ ĐỀ nào     → tab THEO CHỦ ĐỀ, 5 mảng → chủ đề → dạng bài;
 *   4. cần cố gắng chỗ nào     → danh sách bài chưa qua, bấm vào là mở bài luôn.
 *
 * Hai trục trả lời hai câu khác nhau và KHÔNG thay được cho nhau: trục lớp nói "con
 * học tới bài nào của quyển nào"; trục chủ đề nói "con vững cái gì" — cùng một chủ đề
 * nằm rải bốn quyển dưới bốn tên chương khác nhau, nên nhìn theo quyển thì không bao
 * giờ thấy.
 */

const MAU_MUC = {
  master: 'bg-teal text-white', xongBai: 'bg-gold text-gold-dark',
  dangHoc: 'bg-navy-light text-white', chuaHoc: 'bg-soft text-mute',
};
const MAU_TT = {
  vung: 'bg-teal text-white', dangHoc: 'bg-navy-light text-white',
  canCoGang: 'bg-alert text-white', chuaHoc: 'bg-soft text-mute',
};

const O = ({ nhan, gia, mau = 'text-navy' }) => (
  <div className="min-w-[92px] flex-1 rounded-xl bg-soft px-3 py-2.5 text-center">
    <b className={`block text-[21px] ${mau}`}>{gia}</b>
    <span className="text-[10.5px] font-extrabold text-mute">{nhan}</span>
  </div>
);

export default function ParentReport({ mon = [], tienDo = {}, learnerId, onExit, onVeNha }) {
  /* MỖI MÔN NỘP HỌC BẠ THEO MỘT KHUÔN. Sổ này không biết Toán chia chương thế nào,
     cũng không biết Tiếng Anh rồi sẽ chia ra sao — nó chỉ vẽ đúng khuôn ấy. Thêm môn
     thứ hai là thêm một tab, không phải viết lại màn. */
  const [monMa, setMonMa] = useState(mon[0]?.ma);
  const m = mon.find((x) => x.ma === monMa) || mon[0];
  const [hb, setHb] = useState(null);
  const [cloudReport, setCloudReport] = useState(null);
  const [tab, setTab] = useState('lop');
  const [moQuyen, setMoQuyen] = useState(null);
  const [moMang, setMoMang] = useState(null);
  const [dangMoi, setDangMoi] = useState(false);
  const [loi, setLoi] = useState(null);

  useEffect(() => {
    let song = true;
    setHb(null);
    m?.hocBa(tienDo[m.ma]).then((x) => song && setHb(x)).catch(() => song && setHb({ quyen: [] }));
    m?.soMayChu(learnerId).then((x) => song && setCloudReport(x)).catch(() => {});
    return () => { song = false; };
  }, [m, tienDo, learnerId]);

  const dsHocBa = hb?.quyen || [];
  const td = hb?.trinhDo || { tongBaiDat: 0, tongChuongMaster: 0, quyen: null };
  const cd = hb?.chuDe || { mang: [], dem: { vung: 0, dangHoc: 0, canCoGang: 0, chuaHoc: 0 }, tong: 0 };
  const banDo = !!hb?.chuDe;
  /* Bấm vào một bài để mở lại: đường vào phòng học là của MÔN, không phải của sổ.
     Đợt sau đưa vào giao ước; giờ để trống thay vì gọi liều sang ruột Toán. */
  const onOpenMicro = null;

  const r = cloudReport;
  const weak = r?.weakest || [];

  if (!hb) {
    return (
      <div className="mx-auto min-h-[100dvh] max-w-[740px]">
        <ThanhTren tieuDe="Sổ học của con" onQuayLai={onExit} nhanQuayLai="← Quay lại" onVeNha={onVeNha} />
        <p className="p-6 text-mute">Đang mở sổ…</p>
      </div>
    );
  }

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-10">
      <ThanhTren tieuDe="📖 Sổ học của con" onQuayLai={onExit} nhanQuayLai="← Quay lại" onVeNha={onVeNha}
                 phuDe="Con master chương nào, vững chủ đề nào, cần cố gắng chỗ nào." />

      <div className="px-3.5 pt-3.5">
        {/* Chọn MÔN — chỉ hiện khi có từ hai môn trở lên. */}
        {mon.length > 1 && (
          <div className="mb-3 flex gap-1.5">
            {mon.map((x) => (
              <button key={x.ma} onClick={() => setMonMa(x.ma)}
                className={`flex-1 rounded-xl border-[1.5px] px-2 py-2 text-[13px] font-bold ${
                  x.ma === monMa ? 'border-navy bg-navy text-white' : 'border-line bg-white text-navy'}`}>
                {x.bieuTuong} {x.ten}
              </button>
            ))}
          </div>
        )}

        {/* ══ TRÌNH ĐỘ HIỆN TẠI ══ */}
        <div className="card">
          <div className="kicker">TRÌNH ĐỘ HIỆN TẠI</div>
          {td.quyen ? (
            <p className="text-[15px] leading-relaxed">
              Con đang học <b>{td.quyen.ten}</b> — đã đạt <b>{td.quyen.datBai}</b> trên{' '}
              {td.quyen.tongBai} bài, master <b>{td.quyen.masterChuong}</b> trên{' '}
              {td.quyen.tongChuong} chương.
              {td.bacChuDe !== null && (
                <> Đo trên {td.soChuDeDoDuoc} chủ đề đã luyện, con vững quanh mức <b>lớp {td.bacChuDe}</b>.</>
              )}
            </p>
          ) : (
            <p className="text-[15px] text-mute">Con chưa học bài nào — chưa có gì để tổng kết.</p>
          )}
          <div className="mt-3 flex flex-wrap gap-2.5">
            <O nhan="BÀI ĐÃ ĐẠT" gia={td.tongBaiDat} />
            <O nhan="CHƯƠNG MASTER" gia={td.tongChuongMaster} />
            <O nhan="CHỦ ĐỀ VỮNG" gia={cd.tong ? `${cd.dem.vung}/${cd.tong}` : '—'} />
            {/* Nhãn nói rõ số phút này ĐO ĐƯỢC hay SUY RA. Bản suy ra cộng khoảng
                cách giữa các câu trả lời nên KHÔNG thấy phần con xem giảng — mà phần
                giảng nay là toàn bộ video của bốn quyển. Hai con số khác nhau về bản
                chất; để chung một nhãn là nói dối bố mẹ. */}
            {r && <O nhan={r.nguonGio === 'suyRa' ? 'PHÚT (ƯỚC)' : 'PHÚT (7 NGÀY)'}
                     gia={r.minutes > 0 ? String(r.minutes) : (r.luotThieuGio > 0 ? '—' : '0')} />}
            {r?.nguonGio === 'do' && r.phutXem != null && (
              <O nhan="XEM GIẢNG" gia={`${r.phutXem}′`} />
            )}
            {r && <O nhan="ĐÚNG" gia={`${r.correctRate}%`} />}
          </div>
          {r?.headline && <p className="mt-3 text-[14.5px] leading-relaxed">{r.headline}</p>}
        </div>

        {/* Sổ trên máy chủ chỉ tổng hợp lúc 21:00 mỗi đêm. Con vừa học xong mà bố mẹ
            mở ra thấy trống thì tưởng công học không được lưu. */}
        {m?.lamMoiSoMayChu && learnerId && learnerId !== 'local' && (
          <div className="card flex flex-wrap items-center justify-between gap-2 py-3">
            <span className="text-[13px] text-mute">
              {r?.generatedAt
                ? `Số liệu máy chủ tổng hợp lúc ${new Date(r.generatedAt).toLocaleString('vi-VN')}`
                : 'Chưa có số liệu máy chủ cho tuần này'}
            </span>
            <button
              className="rounded-full border-[1.5px] border-navy px-3 py-1 text-[12.5px] font-bold text-navy disabled:opacity-50"
              disabled={dangMoi}
              onClick={async () => {
                setDangMoi(true); setLoi(null);
                try { await m.lamMoiSoMayChu(learnerId, 7); setCloudReport(await m.soMayChu(learnerId)); } catch (e) { setLoi(String(e?.message || e)); }
                finally { setDangMoi(false); }
              }}>
              {dangMoi ? 'đang cập nhật…' : '↻ Cập nhật ngay'}
            </button>
            {loi && <p className="w-full text-[12.5px] text-alert">{loi}</p>}
          </div>
        )}

        {r?.luotThieuGio > 0 && (
          <p className="mb-2 rounded-xl bg-[#F2F6FA] px-3.5 py-2.5 text-[12.5px] leading-relaxed text-mute">
            Có {r.luotThieuGio} lượt trả lời ghi từ bản cũ nên chưa đo được thời gian —
            phần “phút học” chỉ tính trên các buổi học từ nay về sau.
          </p>
        )}

        {/* ══ HAI TRỤC ══ */}
        <div className="mt-1 flex gap-2">
          {[['lop', 'Xem theo lớp', 'từng quyển · từng chương · từng bài'],
            ['chude', 'Xem theo chủ đề', 'con vững chủ đề nào, hổng chủ đề nào']].map(([id, ten, mt]) => (
            <button key={id} onClick={() => setTab(id)}
              className={`flex-1 rounded-xl border-[1.5px] px-3 py-2.5 text-left ${
                tab === id ? 'border-navy bg-navy text-white' : 'border-line bg-white text-navy'}`}>
              <b className="block text-[13.5px]">{ten}</b>
              <span className={`text-[11.5px] ${tab === id ? 'opacity-85' : 'text-mute'}`}>{mt}</span>
            </button>
          ))}
        </div>

        {/* ══════════ TRỤC 1 · THEO LỚP ══════════ */}
        {tab === 'lop' && dsHocBa.map((h) => {
          const bung = moQuyen === h.ma;
          return (
            <section key={h.ma} className="card mt-3">
              <button className="flex w-full items-center gap-2.5 text-left"
                      onClick={() => setMoQuyen(bung ? null : h.ma)}>
                <span className="min-w-0 flex-1">
                  <b className="block text-[15px] leading-snug text-navy">{h.ten}</b>
                  <span className="text-[12px] text-mute">
                    {h.daBatDau
                      ? `${h.datBai}/${h.tongBai} bài · master ${h.masterChuong}/${h.tongChuong} chương`
                      : 'con chưa mở quyển này'}
                  </span>
                </span>
                <span className="h-1.5 w-16 overflow-hidden rounded-full bg-soft">
                  <i className="block h-full bg-teal" style={{ width: `${h.phanTram}%` }} />
                </span>
                <span className="text-[13px] text-mute">{bung ? '▾' : '▸'}</span>
              </button>

              {bung && (
                <div className="mt-2.5 border-t border-line pt-2.5">
                  {h.chuong.map((c) => (
                    <div key={c.so} className="mt-1.5 rounded-xl border border-line px-3 py-2.5">
                      <div className="flex items-center gap-2">
                        <span className="rounded bg-navy px-1.5 py-0.5 text-[11px] font-extrabold text-white">
                          C{c.so}
                        </span>
                        <b className="min-w-0 flex-1 truncate text-[13.5px] text-navy">{c.ten}</b>
                        <span className={`rounded px-1.5 py-0.5 text-[10.5px] font-extrabold ${MAU_MUC[c.muc]}`}>
                          {NHAN_MUC_CHUONG[c.muc]}
                        </span>
                      </div>
                      <div className="mt-1.5 flex items-center gap-2">
                        <span className="h-1.5 flex-1 overflow-hidden rounded-full bg-soft">
                          <i className="block h-full bg-teal" style={{ width: `${c.tk.phanTram}%` }} />
                        </span>
                        <span className="text-[11.5px] tabular-nums text-mute">
                          {c.tk.dat}/{c.tk.tong} bài
                        </span>
                        {c.tk.coKy && (
                          <span className="text-[11.5px] text-mute">
                            {c.tk.kyDat ? '🏅 qua kỳ'
                              : c.tk.kyDaThi ? `⚔ ${c.tk.kyLanTruoc.dung}/${c.tk.kyLanTruoc.tong}`
                                : '⚔ chưa thi'}
                          </span>
                        )}
                      </div>
                      {/* Bài chưa đạt của CHÍNH chương này — bố mẹ kèm đúng chỗ */}
                      {/* Bài chưa đạt của chính chương này — lấy từ HỌC BẠ môn nộp,
                          sổ không soi vào sổ tiến độ của môn. */}
                      {(h.canCoGang || []).filter((b) => b.chuong === c.so).map((b) => (
                        <div key={b.id}
                             className="mt-1.5 flex items-center gap-2 rounded-lg bg-alert-pale px-2.5 py-1.5 text-[12.5px]">
                          <span>🔸</span>
                          <span className="min-w-0 flex-1 truncate text-navy">
                            Bài {b.so}{b.micro > 1 ? `.${b.micro}` : ''} · {b.ten}
                          </span>
                          <span className="whitespace-nowrap text-mute">
                            đúng {b.dung}/{b.tong} · {b.lan} lần
                          </span>
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              )}

              {/* Ngoài phần gập mở: luôn hiện mấy bài cần cố gắng nhất của quyển */}
              {h.canCoGang.length > 0 && !bung && (
                <p className="mt-2 text-[12.5px] text-mute">
                  Cần cố gắng: {h.canCoGang.slice(0, 3).map((b) => `Bài ${b.so}`).join(' · ')}
                  {h.canCoGang.length > 3 && ` và ${h.canCoGang.length - 3} bài nữa`}
                </p>
              )}
            </section>
          );
        })}

        {/* ══════════ TRỤC 2 · THEO CHỦ ĐỀ ══════════ */}
        {tab === 'chude' && !banDo && (
          <p className="card mt-3 text-mute">Không nạp được bản đồ chủ đề.</p>
        )}
        {tab === 'chude' && banDo && (
          <>
            <div className="card mt-3">
              <div className="kicker">CON ĐANG ĐỨNG Ở ĐÂU TRÊN {cd.tong} DẠNG BÀI</div>
              <div className="flex flex-wrap gap-2.5">
                <O nhan="ĐÃ VỮNG" gia={cd.dem.vung} mau="text-teal-dark" />
                <O nhan="ĐANG HỌC" gia={cd.dem.dangHoc} />
                <O nhan="CẦN CỐ GẮNG" gia={cd.dem.canCoGang} mau="text-alert" />
                <O nhan="CHƯA HỌC" gia={cd.dem.chuaHoc} mau="text-mute" />
              </div>
              {cd.dem.canCoGang > 0 && (
                <p className="mt-3 rounded-xl bg-alert-pale px-3 py-2.5 text-[13.5px] leading-relaxed">
                  <b>Cần cố gắng</b> nghĩa là con đã đụng tới dạng ấy mà chưa qua — đây là chỗ
                  đáng kèm trước, hơn hẳn việc học thêm dạng mới.
                </p>
              )}
            </div>

            {cd.mang.map((m) => {
              const bung = moMang === m.ma;
              return (
                <section key={m.ma} className="card mt-3">
                  <button className="flex w-full items-center gap-2.5 text-left"
                          onClick={() => setMoMang(bung ? null : m.ma)}>
                    <span className="min-w-0 flex-1">
                      <b className="block text-[14.5px] leading-snug text-navy">{m.ten}</b>
                      <span className="text-[12px] text-mute">
                        vững {m.dem.vung} · đang học {m.dem.dangHoc} · cần cố gắng {m.dem.canCoGang}
                        {' · '}chưa học {m.dem.chuaHoc}
                      </span>
                    </span>
                    <span className="text-[13px] text-mute">{bung ? '▾' : '▸'}</span>
                  </button>

                  {bung && m.chuDe.map((c) => (
                    <div key={c.ma} className="mt-2.5 border-t border-line pt-2.5">
                      <div className="text-[11px] font-extrabold tracking-widest text-mute">
                        {c.ten}
                      </div>
                      {c.dang.map((d) => (
                        <div key={d.ma} className="mt-1.5 rounded-xl border border-line px-3 py-2">
                          <div className="flex items-start gap-2">
                            <span className="min-w-0 flex-1 text-[13.5px] font-semibold leading-snug text-navy">
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
                          {/* Bấm thẳng vào bài chưa đạt của dạng này */}
                          {d.tinhTrang === 'canCoGang' && (
                            <p className="mt-1.5 rounded-lg bg-alert-pale px-2.5 py-1.5 text-[12.5px] text-navy">
                              🔸 Con đã đụng tới dạng này mà chưa qua — nên ôn lại trước.
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  ))}
                </section>
              );
            })}
          </>
        )}

        {/* ══ Phần do máy chủ dựng — bẫy hay sập và lời khuyên ══ */}
        {r?.topTraps?.length > 0 && (
          <div className="card">
            <div className="kicker">BẪY HAY SẬP NHẤT TUẦN QUA</div>
            {r.topTraps.map((tp) => (
              <div key={tp.microId}
                   className="mt-2 rounded-xl border-[1.5px] border-alert bg-alert-pale px-3 py-2.5 text-[14px]">
                <b>{tp.trapName || tp.microId}</b>
                <span className="ml-2 text-mute">sập {tp.times} lần</span>
              </div>
            ))}
          </div>
        )}

        {(r?.suggestion || r?.watchFor) && (
          <div className="card">
            <div className="kicker">GỢI Ý CHO BỐ MẸ</div>
            {r.suggestion && <p className="text-[15px]"><b>Chơi cùng con:</b> {r.suggestion}</p>}
            {r.watchFor && <p className="mt-2 text-[15px]"><b>Để ý:</b> <Chu t={r.watchFor} /></p>}
          </div>
        )}

        {weak.length > 0 && (
          <div className="card">
            <div className="kicker">KỸ NĂNG CÒN YẾU</div>
            {weak.map((w) => (
              <div key={w.unit} className="mt-1.5 flex items-center gap-2 text-[13px]">
                <span className="flex-1 truncate font-mono text-[11.5px] text-mute">{w.unit}</span>
                <span className="h-1.5 w-24 overflow-hidden rounded-full bg-soft">
                  <i className="block h-full bg-gold" style={{ width: `${Math.round((w.p || 0) * 100)}%` }} />
                </span>
                <b className="w-9 text-right text-navy">{Math.round((w.p || 0) * 100)}%</b>
              </div>
            ))}
          </div>
        )}

        {!r && (
          <p className="card text-[13px] text-mute">
            Số liệu trên tính tại máy này. Đăng nhập rồi thì sổ có thêm số phút học, tỉ lệ
            đúng và bẫy hay sập — do máy chủ tổng hợp lúc 21 giờ mỗi đêm.
          </p>
        )}
      </div>
    </div>
  );
}
