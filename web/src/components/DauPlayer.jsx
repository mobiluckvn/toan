import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  BAREM, diemBarem, datChua, keDonOn, tuyenAn, conLai, docGio, chamKep,
} from '../lib/dau.js';
import { checkAnswer, answerFields } from '../lib/flow.js';
import AnswerFields from './AnswerFields.jsx';
import CuonThem from './CuonThem.jsx';
import Figure from './Figure.jsx';

/**
 * VÒNG ĐẤU (Quyển 2) — bốn màn, khác hẳn phòng học Quyển 1.
 *
 *   MÀN 1  làm đề có ĐỒNG HỒ, không xem đáp án
 *   MÀN 2  chữa đề theo barem — con tự chấm bốn mốc từng câu
 *   MÀN 3  phiên tòa bẫy — soi từng bẫy, sập thì kê đơn ôn micro Quyển 1
 *   MÀN 4  nhật ký mùa giải
 *
 * Không cho xem đáp án ở màn 1: sách bắt buộc thế, và cũng là điều phân biệt luyện
 * thi với học bài.
 */

const MAN = ['Làm đề', 'Chữa đề', 'Phiên tòa', 'Nhật ký'];

/** Sơ đồ chiến thuật của màn đang xem — sách chèn chúng đúng chỗ nào thì hiện chỗ ấy */
const SoDo = ({ khoi, man }) => {
  const ds = (khoi.soDo || []).filter((s) => (s.man || 1) === man);
  if (!ds.length) return null;
  return ds.map((s) => <Figure key={s.id} fig={s} />);
};

function DongHo({ batDau, phut, onHet }) {
  const [con, setCon] = useState(() => conLai(batDau, phut));
  const daBao = useRef(false);
  useEffect(() => {
    const id = setInterval(() => {
      const c = conLai(batDau, phut);
      setCon(c);
      if (c === 0 && !daBao.current) { daBao.current = true; onHet?.(); }
    }, 500);
    return () => clearInterval(id);
  }, [batDau, phut, onHet]);
  const gap = con <= 120000;
  return (
    <div className={`fixed right-2.5 top-[52px] z-30 rounded-full px-3 py-1 text-[15px]
                     font-extrabold tabular-nums shadow-md ${
      con === 0 ? 'bg-alert text-white' : gap ? 'bg-gold text-gold-dark' : 'bg-navy text-white'}`}>
      ⏱ {docGio(con)}
    </div>
  );
}

export default function DauPlayer({ khoi, onExit, onXong, onMoMicro }) {
  const [man, setMan] = useState(0);
  const [batDau, setBatDau] = useState(null);         // null = chưa bấm đồng hồ
  const [vals, setVals] = useState({});               // maCau → mảng ô nhập
  const [ketQua, setKetQua] = useState({});           // maCau → {ok, tuChamDung}
  const [barem, setBarem] = useState({});             // maCau → {canCu:…}
  const [dinhDang, setDinhDang] = useState({});       // maCau → {dung}
  const [toa, setToa] = useState({});                 // maBay → 'sap'|'thoat'
  const [i, setI] = useState(0);                      // câu đang làm ở màn 1

  const laTron = khoi.loai === 'detron';
  const cau = khoi.cau;
  const c = cau[i];

  useEffect(() => { window.scrollTo(0, 0); }, [man, i]);

  const nop = () => {
    // chấm những câu MÁY CHẤM được; câu tự luận để con tự chấm ở màn 2
    const kq = { ...ketQua };
    for (const q of cau) {
      if (!q.answerKey) continue;
      const v = vals[q.id];
      const gui = Array.isArray(v) && v.length <= 1 ? v[0] : v;
      kq[q.id] = { ...(kq[q.id] || {}), ok: !!checkAnswer(q, gui ?? '')?.ok, answer: gui ?? '' };
    }
    setKetQua(kq);
    setMan(1);
  };

  const kq = laTron ? chamKep(khoi, ketQua, dinhDang) : datChua(khoi, ketQua);
  const don = keDonOn(khoi, toa);

  /* ══ MÀN 0 · luật vòng đấu, chưa bấm đồng hồ ══ */
  if (man === 0 && !batDau) {
    return (
      <Khung khoi={khoi} man={man} onExit={onExit}>
        <div className="card">
          <div className="kicker">LUẬT VÒNG ĐẤU</div>
          <p className="text-[15.5px] leading-relaxed">{khoi.moTa}</p>
          <div className="mt-3 grid gap-2 text-[14.5px]">
            <Dong nhan="Thời gian" giaTri={`${khoi.phut} phút, có đồng hồ`} />
            <Dong nhan="Thang điểm" giaTri={`${khoi.thang} điểm · đạt từ ${khoi.dat}`} />
            <Dong nhan="Số câu" giaTri={`${cau.length} câu`} />
            {khoi.bay?.length > 0 && <Dong nhan="Bẫy đã gài" giaTri={`${khoi.bay.length} bẫy`} />}
          </div>
          <SoDo khoi={khoi} man={1} />
          <div className="warn-box mt-3 text-[14.5px]">
            Bấm đồng hồ là <b>không xem được đáp án</b> cho tới khi nộp bài. Con chạy
            nghi thức 90 giây trước khi giải câu đầu tiên nhé.
          </div>
        </div>
        <ChanNut>
          <button className="btn-go" onClick={() => setBatDau(Date.now())}>
            Bấm đồng hồ — bắt đầu ▶
          </button>
        </ChanNut>
      </Khung>
    );
  }

  /* ══ MÀN 1 · làm đề ══ */
  if (man === 0) {
    const f = answerFields(c);
    return (
      <Khung khoi={khoi} man={0} onExit={onExit}>
        <DongHo batDau={batDau} phut={khoi.phut} onHet={() => {}} />
        <div className="card">
          <div className="kicker">
            CÂU {c.so}/{cau.length}{c.de ? ` · ĐỀ ${c.de}` : ''} · {'★'.repeat(c.muc || 1)}
          </div>
          <p className="text-[17px] font-semibold leading-snug">{c.text}</p>
          {c.answerKey ? (
            <AnswerFields item={c} vals={vals[c.id] || Array(Math.max(f.length, 1)).fill('')}
                          disabled={false} onChange={(v) => setVals({ ...vals, [c.id]: v })} />
          ) : (
            <div className="mt-3">
              <p className="field-brief"><span aria-hidden>✎</span>
                <span>Câu này con làm ra giấy nháp. Nộp xong sẽ có lời chữa của sách để con tự chấm.</span></p>
              <label className="mt-2 flex items-center gap-2 text-[14.5px]">
                <input type="checkbox" checked={!!ketQua[c.id]?.daLam}
                       onChange={(e) => setKetQua({ ...ketQua, [c.id]: { ...(ketQua[c.id] || {}), daLam: e.target.checked } })} />
                Con đã làm xong câu này ra nháp
              </label>
            </div>
          )}
          {laTron && (
            <div className="mt-3 rounded-xl bg-soft px-3 py-2.5">
              <div className="text-[12.5px] font-bold text-navy">PHIẾU ĐỊNH DẠNG — gọi tên dạng bài</div>
              <input className="numin mt-1.5 w-full text-left text-[15px]"
                     placeholder="vd: tổng - hiệu ẩn · vành khăn · đuổi kịp khác giờ"
                     value={dinhDang[c.id]?.ten || ''}
                     onChange={(e) => setDinhDang({ ...dinhDang, [c.id]: { ...(dinhDang[c.id] || {}), ten: e.target.value } })} />
            </div>
          )}
        </div>
        <ChanNut>
          <button className="btn-ghost" disabled={i === 0} onClick={() => setI(i - 1)}>◀ Câu trước</button>
          {i < cau.length - 1
            ? <button className="btn-go" onClick={() => setI(i + 1)}>Câu sau ▶</button>
            : <button className="btn-gold" onClick={nop}>Nộp bài & chữa đề</button>}
        </ChanNut>
      </Khung>
    );
  }

  /* ══ MÀN 2 · chữa đề theo barem ══ */
  if (man === 1) {
    return (
      <Khung khoi={khoi} man={1} onExit={onExit}>
        <div className="card">
          <div className="kicker">CHỮA ĐỀ KIỂU GIÁM KHẢO</div>
          <p className="text-[14.5px] leading-relaxed text-mute">
            Chấm theo <b>barem</b>, không chấm theo cảm giác “mình hiểu bài mà”.
            Mỗi câu 1 điểm chia bốn mốc.
          </p>
          <SoDo khoi={khoi} man={2} />
        </div>
        {cau.map((q) => (
          <div key={q.id} className="card">
            <div className="kicker">CÂU {q.so}{q.de ? ` · ĐỀ ${q.de}` : ''}</div>
            <p className="text-[15.5px] font-semibold leading-snug">{q.text}</p>
            {q.answerKey && (
              <p className={`mt-1.5 text-[14px] ${ketQua[q.id]?.ok ? 'text-teal-dark' : 'text-alert'}`}>
                Con trả lời: <b>{String(ketQua[q.id]?.answer ?? '(bỏ trống)')}</b>
                {' · '}{ketQua[q.id]?.ok ? 'đúng ✓' : 'chưa đúng'}
              </p>
            )}
            <div className="mt-2 rounded-xl border-[1.5px] border-teal bg-teal-pale px-3.5 py-3 text-[15px]">
              <b>Lời chữa của sách:</b> {q.loiChua}
            </div>
            {!q.answerKey && (
              <label className="mt-2 flex items-center gap-2 text-[14.5px] font-semibold">
                <input type="checkbox" checked={!!ketQua[q.id]?.tuChamDung}
                       onChange={(e) => setKetQua({ ...ketQua, [q.id]: { ...(ketQua[q.id] || {}), tuChamDung: e.target.checked } })} />
                Bài của con ĐÚNG như lời chữa
              </label>
            )}
            <div className="mt-2 grid gap-1.5">
              {BAREM.map((m) => (
                <label key={m.id} className="flex items-start gap-2 text-[13.5px]">
                  <input type="checkbox" className="mt-0.5"
                         checked={!!barem[q.id]?.[m.id]}
                         onChange={(e) => setBarem({ ...barem, [q.id]: { ...(barem[q.id] || {}), [m.id]: e.target.checked } })} />
                  <span><b>{m.diem > 0 ? `${m.diem} đ` : 'không tính điểm'}</b> · {m.ten}
                    <span className="text-mute"> — {m.goi}</span></span>
                </label>
              ))}
            </div>
            <p className="mt-1.5 text-[13px] text-mute">
              Điểm trình bày câu này: <b>{diemBarem(barem[q.id])}</b>/1
            </p>
          </div>
        ))}
        <ChanNut>
          <button className="btn-go" onClick={() => setMan(khoi.bay?.length ? 2 : 3)}>
            {khoi.bay?.length ? 'Sang phiên tòa xử Cáo Đề ▶' : 'Sang nhật ký ▶'}
          </button>
        </ChanNut>
      </Khung>
    );
  }

  /* ══ MÀN 3 · phiên tòa bẫy ══ */
  if (man === 2) {
    return (
      <Khung khoi={khoi} man={2} onExit={onExit}>
        <div className="card">
          <div className="kicker">PHIÊN TÒA XỬ CÁO ĐỀ · {khoi.bay.length} BẪY ĐÃ GÀI</div>
          <p className="text-[14.5px] text-mute">
            Với mỗi bẫy, con soi lại bài mình: <b>SẬP</b> nếu đã dính, <b>THOÁT</b> nếu tránh được.
          </p>
        </div>
        {khoi.bay.map((b) => (
          <div key={b.ma} className="card py-3">
            <div className="flex flex-wrap items-center gap-2">
              <span className="rounded bg-navy px-1.5 py-0.5 text-[11px] font-extrabold text-white">{b.ma}</span>
              <span className="text-[12px] text-mute">câu {(b.cacCau || [b.cau]).join(' & ')}</span>
            </div>
            <p className="mt-1 text-[15px] font-semibold">{b.ten}</p>
            {b.thanChu && <p className="text-[13.5px] italic text-mute">“{b.thanChu}”</p>}
            <div className="mt-2 flex gap-2">
              {[['sap', 'Con SẬP bẫy'], ['thoat', 'Con THOÁT']].map(([v, nhan]) => (
                <button key={v} type="button"
                        onClick={() => setToa({ ...toa, [b.ma]: v })}
                        className={`flex-1 rounded-xl border-[1.5px] px-3 py-2 text-[14px] font-bold ${
                          toa[b.ma] === v
                            ? (v === 'sap' ? 'border-alert bg-alert text-white' : 'border-teal bg-teal text-white')
                            : 'border-line bg-white text-navy'}`}>
                  {nhan}
                </button>
              ))}
            </div>
          </div>
        ))}
        <ChanNut>
          <button className="btn-go" onClick={() => setMan(3)}>Xem nhật ký mùa giải ▶</button>
        </ChanNut>
      </Khung>
    );
  }

  /* ══ MÀN 4 · nhật ký ══ */
  return (
    <Khung khoi={khoi} man={3} onExit={onExit}>
      <div className="card text-center">
        <div className="text-[52px] leading-none">{kq.dat ? '🏅' : '💪'}</div>
        <h2 className="mt-1 text-[20px] font-bold text-navy">
          {laTron
            ? `Toán ${kq.toan}/${kq.tong} · Định dạng ${kq.dinhDang}/${kq.tong}`
            : `${kq.dung}/${kq.tong} câu`}
        </h2>
        <p className="mt-1 text-[14.5px] text-mute">
          {kq.dat ? `ĐẠT — cần ${kq.can}` : `Cần ${kq.can} mới đạt`}
        </p>
      </div>

      <div className="card">
        <SoDo khoi={khoi} man={4} />
        <div className="kicker">ĐIỂM TRÌNH BÀY (BAREM)</div>
        <p className="text-[15px]">
          Tổng: <b>{cau.reduce((s, q) => s + diemBarem(barem[q.id]), 0).toFixed(2)}</b>/{cau.length}
        </p>
        <p className="mt-1 text-[13.5px] text-mute">
          Đây mới là thứ Quyển 2 dạy — điểm đáp số chỉ là số liệu.
        </p>
      </div>

      {khoi.bay?.length > 0 && (
        <div className="card">
          <div className="kicker">TUYÊN ÁN · SẬP {don.soSap}/{don.soBay} BẪY</div>
          <p className="text-[15px] leading-relaxed">{tuyenAn(don.soSap, don.soBay)}</p>
          {don.bay.length > 0 && (
            <>
              <p className="mt-2.5 text-[13px] font-bold text-navy">ÔN NGƯỢC VỀ QUYỂN 1:</p>
              {don.bay.map((b) => (
                <button key={b.ma} onClick={() => onMoMicro?.(b.micro)}
                        className="mt-1.5 flex w-full items-center gap-2 rounded-xl border border-line px-3 py-2 text-left text-[13.5px] hover:bg-soft">
                  <span className="rounded bg-alert px-1.5 py-0.5 text-[11px] font-extrabold text-white">{b.ma}</span>
                  <span className="flex-1">{b.ten}</span>
                  <span className="font-mono text-[11.5px] text-mute">
                    {b.micro.replace('DL:KSN5Q1.', '')} ▶
                  </span>
                </button>
              ))}
            </>
          )}
        </div>
      )}

      <ChanNut>
        <button className="btn-ghost" onClick={onExit}>Về trang chính</button>
        <button className="btn-gold" onClick={() => onXong?.({
          khoiId: khoi.id, dat: kq.dat, ketQua, barem, toa, dinhDang,
          diemBarem: cau.reduce((s, q) => s + diemBarem(barem[q.id]), 0),
          microCanOn: don.micro,
        })}>
          Khép lại vòng đấu 🏅
        </button>
      </ChanNut>
    </Khung>
  );
}

/* ─────────── mảnh dùng chung ─────────── */
const Dong = ({ nhan, giaTri }) => (
  <div className="flex justify-between rounded-lg bg-soft px-3 py-1.5">
    <span className="text-mute">{nhan}</span><b className="text-navy">{giaTri}</b>
  </div>
);

const ChanNut = ({ children }) => (
  <footer className="fixed inset-x-0 bottom-0 border-t border-line bg-white/95 px-3.5 py-2.5 backdrop-blur"
          style={{ paddingBottom: 'calc(.625rem + env(safe-area-inset-bottom))' }}>
    <div className="mx-auto flex max-w-[740px] gap-2.5">{children}</div>
  </footer>
);

function Khung({ khoi, man, onExit, children }) {
  return (
    <div className="flex flex-col min-h-[100dvh]">
      <header className="sticky top-0 z-20 flex items-center gap-2.5 bg-navy px-3.5 py-2 text-white">
        <button onClick={onExit} aria-label="Thoát khỏi vòng đấu"
                className="rounded-full border border-white/40 px-2 py-0.5 text-[11px] font-bold leading-none">
          ⌂ Thoát
        </button>
        <span className="rounded bg-gold px-1.5 py-0.5 text-[11px] font-extrabold text-gold-dark">
          {khoi.id.replace('DR:KSN5Q2.', '')}
        </span>
        <h1 className="flex-1 text-[13px] font-semibold leading-tight line-clamp-2">{khoi.ten}</h1>
      </header>
      <div className="flex justify-center gap-1.5 border-b border-line bg-white px-3 py-1.5">
        {MAN.map((m, k) => (
          <span key={m} className={`rounded-full px-2.5 py-1 text-[10.5px] font-extrabold tracking-wide ${
            k === man ? 'bg-navy text-white' : k < man ? 'bg-teal-pale text-teal-dark' : 'bg-soft text-mute'}`}>
            {m}
          </span>
        ))}
      </div>
      <main className="mx-auto w-full max-w-[740px] flex-1 px-3.5 pb-32 pt-4">{children}</main>
      <CuonThem />
    </div>
  );
}
