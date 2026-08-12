import React, { useEffect, useMemo, useState } from 'react';
import NutNghe, { NutNgheDoan } from './NutNghe.jsx';
import CauHoi from './CauHoi.jsx';
import HinhVe from './HinhVe.jsx';
import NutNoi from './NutNoi.jsx';
import HoiThoai from './HoiThoai.jsx';
import Video from './Video.jsx';
import GocBoMe, { MucBoMe } from './GocBoMe.jsx';
import { napBai, napSoAm, hangXom } from '../lib/noiDung.js';
import { maCua } from './NutNghe.jsx';

const maCauAm = (c) => maCua(c, 'en');

/**
 * MỘT BÀI TIẾNG ANH — năm chặng, đúng nhịp bốn quyển Toán đang dùng.
 *
 *   MỞ BÀI → GIẢNG → BÀI MẪU → LUYỆN TẬP (3 mức sao) → SÁT HẠCH
 *
 * Khác Toán ở chỗ nào thì khác vì lý do cụ thể, không phải vì thích khác:
 *
 *  · MỖI MÀN MỘT Ý và chữ to — bé 6 tuổi là bạn nhỏ nhất trong mọi quyển.
 *  · Chặng nào cũng có NÚT NGHE. Bé chưa đọc được tiếng Việt, nên chữ trên màn
 *    hình là để nhìn cho quen mặt, còn nội dung thì vào bằng tai.
 *  · Không có thanh đếm ngược, không có điểm trừ. Sai thì thử lại.
 */
export default function BaiHoc({ id, tienDo, onXongBai, onThoat, onNoi, tenBe = 'Bo' }) {
  const [bai, datBai] = useState(null);
  const [loi, datLoi] = useState(null);
  const [chang, datChang] = useState(0);

  useEffect(() => {
    let song = true;
    datBai(null); datLoi(null); datChang(0);
    (async () => {
      try {
        await napSoAm();
        const d = await napBai(id);
        if (song) datBai(d);
      } catch (e) { if (song) datLoi(e.message); }
    })();
    return () => { song = false; };
  }, [id]);

  if (loi) {
    return (
      <Khung onThoat={onThoat} ten="Không mở được bài">
        <p className="text-alert">{loi}</p>
      </Khung>
    );
  }
  if (!bai) return <Khung onThoat={onThoat} ten="Đang mở bài…"><p className="text-mute">…</p></Khung>;

  /* ── NĂM CHẶNG, VIDEO DẪN ĐƯỜNG ──
     Bản trước có sáu chặng, trong đó Mở bài · Giảng · Bài mẫu đều là CHỮ — mà đếm
     thật thì một bài bắt bé nhìn 2 029 ký tự tiếng Việt. Bé lớp 1 chưa đọc sõi
     tiếng Việt, nên với bé đó chỉ là những mảng xám choán chỗ.
     Nay ba chặng ấy gộp lại thành hai màn XEM: video đã làm đúng việc của chúng —
     nghe tiếng, nhìn hình. Chữ giải thích lui vào Góc bố mẹ, gập lại sẵn.

     NÓI CHUYỆN vẫn đứng SAU luyện tập: bé phải ráp được câu bằng tay và gõ được
     rồi mới nói ra miệng được. */
  const coHoiThoai = !!bai.knowledgeCore?.hoiThoai;
  const CHANG = ['Từ mới', 'Mẫu câu', 'Luyện tập',
    ...(coHoiThoai ? ['Nói chuyện'] : []), 'Sát hạch'];
  const buoc = (n) => datChang(Math.max(0, Math.min(CHANG.length - 1, n)));

  return (
    <Khung onThoat={onThoat} ten={bai.title}>
      <ThanhChang ten={CHANG} tai={chang} onChon={buoc} />

      {chang === 0 && <ManTu bai={bai} onTiep={() => buoc(1)} onNoi={onNoi} />}
      {chang === 1 && <ManCau bai={bai} onTiep={() => buoc(2)} />}
      {chang === 2 && <LuyenTap bai={bai} onTiep={() => buoc(3)} />}
      {coHoiThoai && chang === 3 && (
        <HoiThoai
          hoiThoai={bai.knowledgeCore.hoiThoai}
          tenBe={tenBe}
          onXong={(k) => { onNoi?.('hoiThoai', k); buoc(4); }}
        />
      )}
      {chang === CHANG.length - 1 && (
        <SatHach
          bai={bai}
          onXong={(kq) => onXongBai(kq, hangXom(id).sau)}
        />
      )}
    </Khung>
  );
}

/* ─────────── khung chung ─────────── */

function Khung({ ten, children, onThoat }) {
  return (
    <div className="mx-auto flex min-h-screen w-full max-w-3xl flex-col gap-5 p-4 pb-24">
      <div className="flex items-center gap-3">
        <button type="button" onClick={onThoat}
          className="rounded-xl2 border-2 border-line px-3 py-2 text-sm font-semibold text-mute
            hover:border-navy hover:text-navy focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          ← Về
        </button>
        <h1 className="flex-1 text-xl font-bold text-ink sm:text-2xl">{ten}</h1>
      </div>
      {children}
    </div>
  );
}

function ThanhChang({ ten, tai, onChon }) {
  return (
    <ol className="flex flex-wrap gap-1.5">
      {ten.map((x, i) => (
        <li key={x}>
          <button
            type="button"
            /* Đi LÙI được, đi TỚI thì không: bé quay lại nghe giảng lần nữa là
               chuyện tốt, còn nhảy thẳng tới sát hạch thì bỏ mất bài. */
            disabled={i > tai}
            onClick={() => onChon(i)}
            className={`rounded-full px-3 py-1 text-xs font-semibold transition
              disabled:cursor-not-allowed disabled:opacity-45
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
              ${i === tai ? 'bg-navy text-white' : 'bg-soft text-mute hover:bg-line'}`}
          >
            {i + 1}. {x}
          </button>
        </li>
      ))}
    </ol>
  );
}

const NutTiep = ({ onClick, chu = 'Tiếp tục' }) => (
  <button type="button" onClick={onClick}
    className="self-start rounded-xl2 bg-navy px-6 py-3 text-lg font-semibold text-white
      focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
    {chu} →
  </button>
);

/* ─────────── chặng 1 · TỪ MỚI ─────────── */

/**
 * Video từ mới (~30 giây) → thẻ từ có nghe và nói.
 * Không một dòng giải thích nào trên bề mặt: video đã nói hết, và bé không đọc
 * được chữ. Lời giảng nằm trong Góc bố mẹ, gập sẵn.
 */
function ManTu({ bai, onTiep, onNoi }) {
  const [daXem, datDaXem] = useState(false);
  const K = bai.knowledgeCore.statements || [];
  return (
    <section className="flex flex-col gap-4">
      <Video
        tep={bai.video?.tu}
        ten="Xem từ mới"
        phu={`${bai.knowledgeCore.vocabulary.length} từ · khoảng nửa phút`}
        onXongLan1={() => datDaXem(true)}
      />

      <TuVung bai={bai} onNoi={onNoi} />

      <GocBoMe ten="Góc bố mẹ · bài này dạy gì">
        <MucBoMe nhan="Mục tiêu">{bai.objective.text}</MucBoMe>
        {K.map((k) => <MucBoMe key={k.id} nhan={k.id}>{k.text}</MucBoMe>)}
        <MucBoMe nhan="Cùng con ở nhà">{bai.parentNote?.homeActivity}</MucBoMe>
        <MucBoMe nhan="Nên và không nên">{bai.parentNote?.watchFor}</MucBoMe>
      </GocBoMe>

      <NutTiep onClick={onTiep} chu={daXem ? 'Sang mẫu câu' : 'Xem xong rồi, đi tiếp'} />
    </section>
  );
}


/**
 * THẺ TỪ — bé nhìn hình, nghe từ, rồi tự nói lại.
 *
 * Ba việc trên một thẻ và chỉ ba việc: HÌNH để biết nghĩa, 🔈 để nghe mẫu, 🎤 để
 * tự nói. Không có ô giải thích nào — nghĩa tiếng Việt đã nằm ngay dưới từ, còn
 * lời giảng thì video vừa nói xong.
 */
function TuVung({ bai, onNoi }) {
  /* Các từ KHÁC của bài — để bộ chấm bắt được việc bé đọc "dog" thành "duck".
     Hai từ ấy cùng một unit, nhầm sang nhau mà vẫn điểm cao thì bài nói vô nghĩa. */
  const cungBai = bai.knowledgeCore.vocabulary.map((x) => x.tu);
  const [noiTu, datNoiTu] = useState(null);
  return (
    <div className="flex flex-col gap-3">
      <div className="grid gap-3 sm:grid-cols-2">
        {bai.knowledgeCore.vocabulary.map((v) => (
          <div key={v.tu}
               className="flex items-center gap-3 rounded-xl2 border-2 border-line bg-white p-3">
            <span className="text-4xl leading-none">
              <HinhVe ten={v.tu} {...((bai.hinhTu || []).find((h) => h.tu === v.tu) || {})} />
            </span>
            <div className="min-w-0 flex-1">
              <p className="text-lg font-bold text-navy">{v.tu}</p>
              <p className="font-mono text-xs text-mute">{v.ipa}</p>
              <p className="text-ink">{v.nghia}</p>
            </div>
            <NutNghe ma={v.am} nhan={`Nghe từ ${v.tu}`} />
            <button type="button" onClick={() => datNoiTu(noiTu === v.tu ? null : v.tu)}
              aria-label={`Nói từ ${v.tu}`}
              className={`h-11 w-11 flex-none rounded-full border-2 text-xl transition
                focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
                ${noiTu === v.tu ? 'border-teal bg-teal text-white'
                  : 'border-teal bg-white text-teal-dark hover:bg-teal-pale'}`}>
              <span aria-hidden="true">🎤</span>
            </button>
          </div>
        ))}
      </div>
      {/* Mỗi lúc chỉ MỘT ô nói mở ra: hai micro cùng bật thì máy nghe lẫn, và bé
          cũng không biết đang được hỏi từ nào. */}
      {noiTu && (
        <NutNoi
          key={noiTu}
          cau={noiTu}
          loai="tu"
          maAm={bai.knowledgeCore.vocabulary.find((x) => x.tu === noiTu)?.am}
          doiThu={cungBai}
          nhan={`Nói từ “${noiTu}”`}
          onXong={(k) => onNoi?.(noiTu, k)}
        />
      )}
    </div>
  );
}

/* ─────────── chặng 2 · MẪU CÂU ─────────── */

/**
 * Mỗi mẫu câu MỘT video, và bài hỏi–đáp thì hai video rời (câu hỏi trước, câu trả
 * lời sau). Bé chọn xem cái nào — nhưng mặc định mở cái đầu, để bé không phải chọn.
 */
function ManCau({ bai, onTiep }) {
  const ds = bai.video?.cau || [];
  const [i, datI] = useState(0);
  const mcDs = bai.knowledgeCore.mauCauDs || [];
  const mc = mcDs[i] || bai.knowledgeCore.mauCau;
  const bay = bai.knowledgeCore.misconceptions?.[0];
  const NHAN = { hoi: 'Câu hỏi', dap: 'Câu trả lời', cau: 'Mẫu câu' };

  return (
    <section className="flex flex-col gap-4">
      {ds.length > 1 && (
        <div className="flex flex-wrap gap-2">
          {ds.map((v, k) => (
            <button key={v.tep} type="button" onClick={() => datI(k)}
              className={`rounded-xl2 px-4 py-2.5 font-semibold transition
                focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
                ${k === i ? 'bg-navy text-white' : 'bg-soft text-navy hover:bg-line'}`}>
              {NHAN[v.vai] || 'Mẫu câu'} · {v.cau}
            </button>
          ))}
        </div>
      )}

      <Video key={ds[i]?.tep} tep={ds[i]?.tep} ten="Xem mẫu câu"
             phu={ds[i]?.cau} />

      {mc && <NutNoi cau={mc.cau} loai="cau" maAm={maCauAm(mc.cau)}
                     nhan={`Nói cả câu “${mc.cau}”`} />}

      <GocBoMe ten="Góc bố mẹ · mẫu câu này dùng để làm gì">
        {mc && <MucBoMe nhan="Dùng để">{mc.dungDe}</MucBoMe>}
        {mc?.tinhHuong && <MucBoMe nhan="Tình huống">{mc.tinhHuong}</MucBoMe>}
        {mc?.phan?.length > 0 && (
          <MucBoMe nhan="Câu gồm những mẩu nào">
            <ul className="mt-1 flex flex-col gap-0.5">
              {mc.phan.map((x, k) => (
                <li key={k}>
                  <b className={x.thay ? 'text-gold-dark' : 'text-navy'}>{x.chu}</b>
                  {' — '}{x.lam_gi}
                </li>
              ))}
            </ul>
          </MucBoMe>
        )}
        {mc?.khacVoi && <MucBoMe nhan="Đừng lẫn">{mc.khacVoi}</MucBoMe>}
        {bay && (
          <MucBoMe nhan="Chỗ dễ nhầm">
            <span className="line-through decoration-alert">{bay.wrong}</span>
            {' → '}<b className="text-teal-dark">{bay.right}</b>
            <p className="mt-0.5">{bay.why}</p>
          </MucBoMe>
        )}
      </GocBoMe>

      <NutTiep onClick={onTiep} chu="Vào luyện tập" />
    </section>
  );
}

/* ─────────── chặng 4 · luyện tập ─────────── */

const MUC = [
  { khoa: 'warmup', sao: '★', ten: 'Nghe và hiểu' },
  { khoa: 'standard', sao: '★★', ten: 'Ráp câu' },
  { khoa: 'challenge', sao: '★★★', ten: 'Gõ lại' },
];

function LuyenTap({ bai, onTiep }) {
  const [m, datM] = useState(0);
  const [i, datI] = useState(0);
  const [dem, datDem] = useState({ dung: 0, tong: 0 });
  const pool = bai.practice.pools[MUC[m].khoa] || [];
  const cau = pool[i];

  const xong = (kq) => {
    datDem((d) => ({ dung: d.dung + (kq.dung ? 1 : 0), tong: d.tong + 1 }));
    if (i + 1 < pool.length) { datI(i + 1); return; }
    if (m + 1 < MUC.length) { datM(m + 1); datI(0); return; }
    onTiep();
  };

  if (!cau) return <NutTiep onClick={onTiep} chu="Vào sát hạch" />;

  return (
    <section className="flex flex-col gap-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className="text-lg font-bold text-gold-dark">
          <span className="text-gold">{MUC[m].sao}</span> {MUC[m].ten}
        </p>
        <p className="text-sm text-mute">Câu {i + 1}/{pool.length} · đúng {dem.dung}/{dem.tong}</p>
      </div>
      <div className="rounded-xl2 border-2 border-line bg-white p-5">
        {/* `key` là BẮT BUỘC, không phải để React bớt cảnh báo. Không có nó thì
            component giữ nguyên state khi đổi câu, và lúc chuyển từ câu BẤM CHỌN
            (đáp án là chuỗi) sang câu XẾP THẺ (đáp án là mảng), lần vẽ đầu tiên
            gọi `''.map()` — cả bài trắng màn hình ngay giữa chừng. Đã vỡ thật ở
            đúng chỗ nối ★ sang ★★. */}
        <CauHoi key={cau.id} cau={cau} onXong={xong} />
      </div>
    </section>
  );
}

/* ─────────── chặng 5 · sát hạch ─────────── */

function SatHach({ bai, onXong }) {
  const ds = bai.assessment.items;
  const [i, datI] = useState(0);
  const [dung, datDung] = useState(0);
  const [het, datHet] = useState(false);
  const can = useMemo(() => Math.ceil(ds.length * 0.8), [ds.length]);

  if (het) {
    const dat = dung >= can;
    return (
      <section className="flex flex-col items-start gap-4">
        <div className={`w-full rounded-xl2 p-6 ${dat ? 'bg-teal-pale' : 'bg-gold-pale'}`}>
          <p className="text-4xl" aria-hidden="true">{dat ? '🎉' : '💪'}</p>
          <p className="mt-2 text-2xl font-bold text-ink">
            {dung}/{ds.length} câu đúng
          </p>
          <p className={dat ? 'text-teal-dark' : 'text-gold-dark'}>
            {dat ? 'Con qua bài rồi. Giỏi lắm!' : `Cần ${can} câu đúng. Con nghe lại phần giảng rồi thử lần nữa nhé.`}
          </p>
        </div>
        <NutTiep onClick={() => onXong({ pass: dat, dung, tong: ds.length, bac: 4 })}
          chu={dat ? 'Sang bài sau' : 'Về danh sách bài'} />
      </section>
    );
  }

  const q = ds[i];
  const tra = (v) => {
    if (v === q.answerKey.value) datDung((n) => n + 1);
    if (i + 1 < ds.length) datI(i + 1); else datHet(true);
  };

  return (
    <section className="flex flex-col gap-4">
      <p className="text-sm text-mute">Câu {i + 1}/{ds.length}</p>
      <div className="rounded-xl2 border-2 border-line bg-white p-5">
        {/* NGHE và NHÌN, không phải đọc. Câu hỏi là: nghe từ tiếng Anh, nhìn hình,
            hình ấy có đúng là từ vừa nghe không. Bản trước ra câu chữ tiếng Việt
            nên 80 câu sát hạch của cả quyển đều là câu bé KHÔNG làm được — nó chỉ
            đoán, mà đúng/sai thì đoán trúng một nửa. */}
        {q.nhinNghe ? (
          <div className="flex flex-col items-center gap-3">
            <NutNghe ma={q.am} to nhan="Nghe lại" tuDong key={q.id} />
            <span className="text-7xl leading-none sm:text-8xl">
              <HinhVe ve={q.anhVe} hinh={q.anh} ten="hình" />
            </span>
            <p className="text-lg text-mute">Hình này có đúng không?</p>
          </div>
        ) : (
          <p className="text-xl text-ink">{q.text}</p>
        )}
        <div className="mt-4 flex gap-3">
          {[true, false].map((v) => (
            <button key={String(v)} type="button" onClick={() => tra(v)}
              className="flex-1 rounded-xl2 border-2 border-line bg-white px-4 py-4 text-lg
                font-semibold text-ink hover:border-navy
                focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
              {v ? '✓ ĐÚNG' : '✗ SAI'}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
