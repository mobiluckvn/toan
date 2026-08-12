import React, { useEffect, useMemo, useState } from 'react';
import NutNghe, { NutNgheDoan } from './NutNghe.jsx';
import CauHoi from './CauHoi.jsx';
import HinhVe from './HinhVe.jsx';
import NutNoi from './NutNoi.jsx';
import HoiThoai from './HoiThoai.jsx';
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

  /* NÓI CHUYỆN đứng SAU luyện tập và TRƯỚC sát hạch, và đó là chủ ý: bé phải ráp
     được câu bằng tay (bậc 3) và gõ được (bậc 4) rồi mới nói ra miệng được. Đặt
     trước luyện tập là bắt bé nói thứ nó chưa ráp nổi. */
  const coHoiThoai = !!bai.knowledgeCore?.hoiThoai;
  const CHANG = ['Mở bài', 'Giảng', 'Bài mẫu', 'Luyện tập',
    ...(coHoiThoai ? ['Nói chuyện'] : []), 'Sát hạch'];
  const buoc = (n) => datChang(Math.max(0, Math.min(CHANG.length - 1, n)));

  return (
    <Khung onThoat={onThoat} ten={bai.title}>
      <ThanhChang ten={CHANG} tai={chang} onChon={buoc} />

      {chang === 0 && <MoBai bai={bai} onTiep={() => buoc(1)} />}
      {chang === 1 && <Giang bai={bai} onTiep={() => buoc(2)} onNoi={onNoi} />}
      {chang === 2 && <BaiMau bai={bai} onTiep={() => buoc(3)} />}
      {chang === 3 && <LuyenTap bai={bai} onTiep={() => buoc(4)} />}
      {coHoiThoai && chang === 4 && (
        <HoiThoai
          hoiThoai={bai.knowledgeCore.hoiThoai}
          tenBe={tenBe}
          onXong={(k) => { onNoi?.('hoiThoai', k); buoc(5); }}
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

/* ─────────── chặng 1 · mở bài ─────────── */

function MoBai({ bai, onTiep }) {
  const man = bai.lecture.screens.find((m) => m.kind === 'hook');
  return (
    <section className="flex flex-col gap-4">
      <div className="rounded-xl2 bg-soft p-5">
        <p className="text-xl text-ink">{man?.narration}</p>
        {man?.doanAm && <div className="mt-3"><NutNgheDoan doan={man.doanAm} nhan="Nghe" /></div>}
      </div>
      <div className="rounded-xl2 border-2 border-line p-5">
        <p className="text-sm font-semibold uppercase tracking-wider text-mute">Xong bài này con sẽ</p>
        <p className="mt-1 text-lg text-ink">{bai.objective.kidText}</p>
      </div>
      <NutTiep onClick={onTiep} />
    </section>
  );
}

/* ─────────── chặng 2 · giảng ─────────── */

function Giang({ bai, onTiep, onNoi }) {
  const K = Object.fromEntries(bai.knowledgeCore.statements.map((s) => [s.id, s]));
  const man = bai.lecture.screens.filter((m) => m.kind === 'explain');
  const bay = bai.knowledgeCore.misconceptions?.[0];
  const traps = bai.lecture.screens.find((m) => m.kind === 'trap');
  const [i, datI] = useState(0);
  const het = i >= man.length;

  if (het) {
    return (
      <section className="flex flex-col gap-4">
        <TuVung bai={bai} onNoi={onNoi} />
        <MauCau mc={bai.knowledgeCore.mauCau} />
        {bay && <ChoDeNham bay={bay} man={traps} />}
        <NutTiep onClick={onTiep} />
      </section>
    );
  }

  const k = K[(man[i].teaches || [])[0]];
  return (
    <section className="flex flex-col gap-4">
      <div className="min-h-[9rem] rounded-xl2 bg-soft p-5">
        <p className="text-xl leading-relaxed text-ink">{k?.text}</p>
        {k?.doanAm && <div className="mt-3"><NutNgheDoan doan={k.doanAm} nhan="Nghe" /></div>}
      </div>
      <div className="flex items-center gap-3">
        <NutTiep onClick={() => datI(i + 1)} chu={i === man.length - 1 ? 'Xem lại từ mới' : 'Tiếp'} />
        <span className="text-sm text-mute">{i + 1}/{man.length}</span>
      </div>
    </section>
  );
}

function TuVung({ bai, onNoi }) {
  /* Các từ KHÁC của bài — để bộ chấm bắt được việc bé đọc "dog" thành "duck".
     Hai từ ấy cùng một unit, nhầm sang nhau mà vẫn điểm cao thì bài nói vô nghĩa. */
  const cungBai = bai.knowledgeCore.vocabulary.map((x) => x.tu);
  const [noiTu, datNoiTu] = useState(null);
  return (
    <div className="flex flex-col gap-3">
    <div className="grid gap-3 sm:grid-cols-2">
      {bai.knowledgeCore.vocabulary.map((v) => (
        <div key={v.tu} className="flex items-center gap-3 rounded-xl2 border-2 border-line bg-white p-3">
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

/**
 * MẪU CÂU — dạy VIỆC trước, dạy CÂU sau.
 *
 * Bác chỉ ra chỗ yếu nhất của bản đầu: bài dạy bé đọc “Bye, Mai.” mà không nói câu
 * ấy dùng lúc nào, nên với bé nó chỉ là một chuỗi âm phải nhớ. Bé 6 tuổi học ngoại
 * ngữ thì thứ cần biết TRƯỚC TIÊN là “nói câu này để làm gì”.
 *
 * Nên khối này trả lời ba câu, theo đúng thứ tự bé cần:
 *   1. dùng để làm gì — kèm MỘT cảnh cụ thể bé hình dung ra ngay
 *   2. từng mẩu trong câu làm việc gì — và mẩu nào là mẩu THAY ĐƯỢC
 *   3. khác mẫu câu nào đã học — chỗ này mới là chỗ bé hay lẫn
 *      ("This is" với "That's", "Touch" với "Point to")
 */
function MauCau({ mc }) {
  if (!mc?.dungDe) return null;
  return (
    <div className="rounded-xl2 border-2 border-navy bg-white p-5">
      <p className="text-sm font-semibold uppercase tracking-wider text-mute">
        Câu hôm nay dùng để làm gì
      </p>
      <p className="mt-1 text-xl font-semibold text-navy">{mc.dungDe}</p>
      {mc.tinhHuong && (
        <p className="mt-2 rounded-xl2 bg-soft p-3 text-ink">🖼️ {mc.tinhHuong}</p>
      )}

      {/* Tách câu ra: mỗi mẩu một dòng, mẩu THAY ĐƯỢC tô khác hẳn để bé thấy ngay
          chỗ nào là chỗ mình đổi. Đây là thứ công thức "Hi, I'm + [Name]." không
          nói được — bé lớp 1 chưa đọc nổi ký hiệu ngoặc vuông. */}
      <div className="mt-4 flex flex-col gap-1.5">
        {(mc.phan || []).map((x, i) => (
          <div key={i} className="flex items-baseline gap-3">
            <span className={`min-w-[6.5rem] flex-none rounded-lg px-2.5 py-1 text-center
              font-semibold ${x.thay
                ? 'bg-gold text-gold-dark ring-2 ring-gold-dark'
                : 'bg-soft text-navy'}`}>
              {x.chu}
            </span>
            <span className="text-ink">{x.lam_gi}</span>
          </div>
        ))}
      </div>
      {(mc.phan || []).some((x) => x.thay) && (
        <p className="mt-2 text-sm text-mute">
          Ô <span className="rounded bg-gold px-1.5 font-semibold text-gold-dark">vàng</span> là
          chỗ con thay được — đổi chữ ở đó là ra câu mới.
        </p>
      )}

      {/* Nói cả câu — bậc cao hơn nói từ, nên đặt SAU phần tách mẩu: bé phải thấy
          câu gồm những gì rồi mới nói được nó. */}
      <div className="mt-4">
        <NutNoi cau={mc.cau} loai="cau" maAm={maCauAm(mc.cau)}
                nhan={`Nói cả câu “${mc.cau}”`} />
      </div>

      {mc.khacVoi && (
        <div className="mt-4 rounded-xl2 border-l-4 border-teal bg-teal-pale p-3">
          <p className="text-sm font-semibold uppercase tracking-wider text-teal-dark">
            Đừng lẫn
          </p>
          <p className="mt-1 text-teal-dark">{mc.khacVoi}</p>
        </div>
      )}
    </div>
  );
}

/**
 * CHỖ DỄ NHẦM — khuôn "nghe câu sai rồi tự nhận ra".
 * Không nhân vật nào nói câu sai: quyển này dựng cho mọi học sinh, không đòi bé
 * phải biết trước thế giới của bốn quyển Toán. Câu sai đứng một mình.
 */
function ChoDeNham({ bay, man }) {
  const [mo, datMo] = useState(false);
  return (
    <div className="rounded-xl2 border-2 border-gold bg-gold-pale p-5">
      <p className="text-sm font-semibold uppercase tracking-wider text-gold-dark">Chỗ dễ nhầm</p>
      <p className="mt-2 text-xl text-ink">
        <span className="line-through decoration-alert decoration-2">{bay.wrong}</span>
      </p>
      {man?.doanAm && <div className="mt-3"><NutNgheDoan doan={man.doanAm} nhan="Nghe cả hai câu" /></div>}
      {mo ? (
        <div className="mt-3">
          <p className="text-xl font-semibold text-teal-dark">{bay.right}</p>
          <p className="mt-1 text-gold-dark">{bay.why}</p>
        </div>
      ) : (
        <button type="button" onClick={() => datMo(true)}
          className="mt-3 rounded-xl2 border-2 border-gold-dark px-4 py-2 text-sm font-semibold
            text-gold-dark focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Câu đúng là gì?
        </button>
      )}
    </div>
  );
}

/* ─────────── chặng 3 · bài mẫu ─────────── */

function BaiMau({ bai, onTiep }) {
  const we = bai.workedExample || {};
  const [n, datN] = useState(1);
  const buoc = we.steps || [];
  return (
    <section className="flex flex-col gap-4">
      <div className="rounded-xl2 border-2 border-navy bg-white p-5">
        <p className="text-sm font-semibold uppercase tracking-wider text-mute">{we.title}</p>
        <p className="mt-1 text-2xl font-bold text-navy">{we.problem}</p>
      </div>
      <ol className="flex flex-col gap-2">
        {buoc.slice(0, n).map((s, i) => (
          <li key={i} className="rounded-xl2 bg-soft p-4 text-lg text-ink">{s.show}</li>
        ))}
      </ol>
      {n < buoc.length
        ? <NutTiep onClick={() => datN(n + 1)} chu="Bước tiếp" />
        : <NutTiep onClick={onTiep} chu="Vào luyện tập" />}
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
        <p className="text-xl text-ink">{q.text}</p>
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
