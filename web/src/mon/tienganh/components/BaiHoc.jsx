import React, { useEffect, useMemo, useState } from 'react';
import NutNghe from './NutNghe.jsx';
import CauHoi from './CauHoi.jsx';
import CauNgheNhin from './CauNgheNhin.jsx';
import HinhVe from './HinhVe.jsx';
import NutNoi from './NutNoi.jsx';
import HoiThoai from './HoiThoai.jsx';
import Video from './Video.jsx';
import GocBoMe, { MucBoMe } from './GocBoMe.jsx';
import { napBai, napSoAm, hangXom } from '../lib/noiDung.js';
import { maCua } from './NutNghe.jsx';
import { changCua, NHAN_CHANG, trangThaiChang, THU_TOI_THIEU } from '../lib/dandat.js';

const maCauAm = (c) => maCua(c, 'en');

/**
 * MỘT BÀI TIẾNG ANH — năm chặng, đúng nhịp bốn quyển Toán đang dùng.
 *
 *   TỪ MỚI → MẪU CÂU → LUYỆN TẬP (3 mức sao) → NÓI CHUYỆN → SÁT HẠCH
 *
 * Khác Toán ở chỗ nào thì khác vì lý do cụ thể, không phải vì thích khác:
 *
 *  · MỖI MÀN MỘT Ý và chữ to — bé 6 tuổi là bạn nhỏ nhất trong mọi quyển.
 *  · Chặng nào cũng có NÚT NGHE. Bé chưa đọc được tiếng Việt, nên chữ trên màn
 *    hình là để nhìn cho quen mặt, còn nội dung thì vào bằng tai.
 *  · Không có thanh đếm ngược, không có điểm trừ. Sai thì thử lại.
 *
 * ── ĐI LẦN LƯỢT, VÀ QUAY LẠI ĐƯỢC ──
 * Bản trước giữ đúng MỘT con số: đang ở chặng nào. Nút trên thanh khoá theo
 * `i > tai`. Hai chỗ hỏng vì thế:
 *
 *   · nút "Tiếp" không đòi hỏi gì — bé bấm liền năm cái là ra thẳng sát hạch,
 *     chưa xem một giây video nào;
 *   · quay lại chặng 1 nghe lại từ mới thì chặng 2·3·4 KHOÁ LẠI HẾT, muốn về chỗ
 *     cũ phải làm lại cả bài. Ôn lại là việc tốt, mà app lại phạt.
 *
 * Nên nay có HAI con số: đang đứng ở đâu (`tai`) và đã đi xa nhất tới đâu (`xa`).
 * `xa` chỉ nhích lên khi chặng ấy LÀM XONG THẬT, và không bao giờ tụt xuống. Luật
 * ở `lib/dandat.js` để cổng chạy bằng node soi được.
 */
export default function BaiHoc({ id, tienDo, onXongBai, onThoat, onNoi, onChang, tenBe = 'Bo' }) {
  const [bai, datBai] = useState(null);
  const [loi, datLoi] = useState(null);
  const [tai, datTai] = useState(0);
  const [xa, datXa] = useState(0);

  useEffect(() => {
    let song = true;
    datBai(null); datLoi(null); datTai(0); datXa(0);
    (async () => {
      try {
        await napSoAm();
        const d = await napBai(id);
        if (!song) return;
        datBai(d);
        /* Vào lại đúng chỗ bỏ dở. Kẹp trong khoảng hợp lệ: sổ cũ có thể ghi số
           chặng của bản bài CŨ (bài từng có 6 chặng), mà nhảy ra ngoài mảng thì
           màn trắng. */
        const nho = Math.max(0, Math.min(tienDo?.micros?.[id]?.chang || 0, changCua(d).length - 1));
        datTai(nho); datXa(nho);
      } catch (e) { if (song) datLoi(e.message); }
    })();
    return () => { song = false; };
    /* CỐ Ý không nghe `tienDo`: chỉ đọc chặng đã nhớ MỘT LẦN lúc mở bài. Nghe cả
       `tienDo` thì mỗi lần ghi chặng lại chạy lại effect này, `datBai(null)` xoá
       màn, nạp lại bài — thành vòng lặp không đáy. Đã dính đúng kiểu này một lần
       ở sổ tiến độ, ghi trong docs/tiep_theo_tienganh_lop1.md. */
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  if (loi) {
    return (
      <Khung onThoat={onThoat} ten="Không mở được bài">
        <p className="text-alert">{loi}</p>
      </Khung>
    );
  }
  if (!bai) return <Khung onThoat={onThoat} ten="Đang mở bài…"><p className="text-mute">…</p></Khung>;

  const CHANG = changCua(bai);
  const tenChang = CHANG.map((k) => NHAN_CHANG[k]);

  /* Đi TỚI: chỉ gọi từ trong chặng, khi chặng ấy đã làm xong thật. */
  const xong = () => {
    const n = Math.min(tai + 1, CHANG.length - 1);
    datTai(n);
    if (n > xa) { datXa(n); onChang?.(n); }
  };
  /* Nhảy trên thanh: chỉ tới chặng ĐÃ MỞ, và KHÔNG hạ `xa` xuống. */
  const nhay = (i) => { if (i <= xa) datTai(i); };

  const k = CHANG[tai];
  return (
    <Khung onThoat={onThoat} ten={bai.title}>
      <ThanhChang ten={tenChang} tai={tai} xa={xa} onChon={nhay} />

      {k === 'tu' && <ManTu bai={bai} onTiep={xong} onNoi={onNoi} />}
      {k === 'cau' && <ManCau bai={bai} onTiep={xong} />}
      {k === 'luyen' && <LuyenTap bai={bai} onTiep={xong} />}
      {k === 'noi' && (
        <HoiThoai
          hoiThoai={bai.knowledgeCore.hoiThoai}
          tenBe={tenBe}
          onXong={(kq) => { onNoi?.('hoiThoai', kq); xong(); }}
        />
      )}
      {k === 'sat' && (
        <SatHach bai={bai} onXong={(kq) => onXongBai(kq, hangXom(id).sau)} />
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

/**
 * THANH CHẶNG — vừa là chỗ bé biết mình đang ở đâu, vừa là chỗ QUAY LẠI LÀM LẠI.
 *
 * Chặng đã đi qua thì bấm vào được, và bấm vào KHÔNG mất chặng sau: bé nghe lại
 * từ mới xong bấm thẳng về sát hạch, không phải làm lại cả bài. Chặng chưa tới
 * thì khoá, và khoá có nói vì sao.
 */
function ThanhChang({ ten, tai, xa, onChon }) {
  return (
    <div className="flex flex-col gap-2">
      <ol className="flex flex-wrap gap-1.5">
        {ten.map((x, i) => {
          const tt = trangThaiChang(i, tai, xa);
          return (
            <li key={x}>
              <button
                type="button"
                disabled={tt === 'khoa'}
                onClick={() => onChon(i)}
                title={tt === 'khoa' ? 'Con làm xong phần trước thì phần này mở ra'
                     : tt === 'xong' ? 'Bấm để làm lại phần này' : undefined}
                className={`rounded-full px-3 py-1 text-xs font-semibold transition
                  disabled:cursor-not-allowed disabled:opacity-45
                  focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
                  ${tt === 'dang' ? 'bg-navy text-white'
                    : tt === 'xong' ? 'bg-teal-pale text-teal-dark hover:bg-teal hover:text-white'
                    : 'bg-soft text-mute'}`}
              >
                {tt === 'xong' ? '✓ ' : tt === 'khoa' ? '🔒 ' : `${i + 1}. `}{x}
              </button>
            </li>
          );
        })}
      </ol>
      {/* Bé quay lại ôn rồi thì phải có đường về chỗ đang học, không bắt bấm mò. */}
      {tai < xa && (
        <button type="button" onClick={() => onChon(xa)}
          className="self-start text-sm font-semibold text-navy underline
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          → Về chỗ con đang học ({ten[xa]})
        </button>
      )}
    </div>
  );
}

const NutTiep = ({ onClick, chu = 'Tiếp tục', tat = false, viSao }) => (
  <div className="flex flex-col gap-1">
    <button type="button" onClick={onClick} disabled={tat}
      className="self-start rounded-xl2 bg-navy px-6 py-3 text-lg font-semibold text-white
        disabled:bg-line disabled:text-mute
        focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
      {chu} →
    </button>
    {/* Nút xám mà không nói vì sao thì bé tưởng máy hỏng. Luôn kèm một dòng. */}
    {tat && viSao && <p className="text-sm text-mute">{viSao}</p>}
  </div>
);

/* ─────────── chặng 1 · TỪ MỚI ─────────── */

/**
 * Video từ mới (~30 giây) → thẻ từ có nghe và nói.
 * Không một dòng giải thích nào trên bề mặt: video đã nói hết, và bé không đọc
 * được chữ. Lời giảng nằm trong Góc bố mẹ, gập sẵn.
 *
 * ── MỞ NÚT ĐI TIẾP KHI NÀO ──
 * Xem hết video, HOẶC nghe đủ từng từ một. Hai đường vì chúng là hai cách học
 * thật, không phải một đường chính và một lối lách: video giảng, còn bấm nghe
 * từng từ cũng là nghe đủ chừng ấy từ. Video hỏng thì mở ngay và nói rõ — không
 * để bé kẹt vì tệp không tải được.
 */
function ManTu({ bai, onTiep, onNoi }) {
  const [daXem, datDaXem] = useState(false);
  const [videoHong, datVideoHong] = useState(false);
  const [daNghe, datDaNghe] = useState(() => new Set());
  const K = bai.knowledgeCore.statements || [];
  const dsTu = bai.knowledgeCore.vocabulary || [];
  const ngheDu = dsTu.length > 0 && dsTu.every((v) => daNghe.has(v.tu));
  const moKhoa = daXem || ngheDu || videoHong || !bai.video?.tu;

  return (
    <section className="flex flex-col gap-4">
      <Video
        tep={bai.video?.tu}
        ten="Xem từ mới"
        phu={`${dsTu.length} từ · khoảng nửa phút`}
        onXongLan1={() => datDaXem(true)}
        onLoi={() => datVideoHong(true)}
      />

      <TuVung bai={bai} onNoi={onNoi}
              onNghe={(t) => datDaNghe((s) => (s.has(t) ? s : new Set(s).add(t)))} />

      <GocBoMe ten="Góc bố mẹ · bài này dạy gì">
        <MucBoMe nhan="Mục tiêu">{bai.objective.text}</MucBoMe>
        {K.map((x) => <MucBoMe key={x.id} nhan={x.id}>{x.text}</MucBoMe>)}
        <MucBoMe nhan="Cùng con ở nhà">{bai.parentNote?.homeActivity}</MucBoMe>
        <MucBoMe nhan="Nên và không nên">{bai.parentNote?.watchFor}</MucBoMe>
      </GocBoMe>

      <NutTiep
        onClick={onTiep}
        tat={!moKhoa}
        chu="Sang mẫu câu"
        viSao={`Con xem hết video, hoặc bấm 🔈 nghe đủ ${dsTu.length} từ, rồi đi tiếp nhé.`}
      />
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
function TuVung({ bai, onNoi, onNghe }) {
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
            <NutNghe ma={v.am} nhan={`Nghe từ ${v.tu}`} onPhat={() => onNghe?.(v.tu)} />
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
 *
 * Đi tiếp được khi XEM HẾT MỌI video mẫu câu của bài. Bài có hai mẫu mà chỉ xem
 * một rồi qua thì đúng nửa bài bị bỏ — mà đó là nửa bé sẽ gặp lại ngay ở luyện
 * tập và sát hạch.
 */
function ManCau({ bai, onTiep }) {
  const ds = bai.video?.cau || [];
  const [i, datI] = useState(0);
  const [daXem, datDaXem] = useState(() => new Set());
  const [hong, datHong] = useState(false);
  const mcDs = bai.knowledgeCore.mauCauDs || [];
  const mc = mcDs[i] || bai.knowledgeCore.mauCau;
  const bay = bai.knowledgeCore.misconceptions?.[0];
  const NHAN = { hoi: 'Câu hỏi', dap: 'Câu trả lời', cau: 'Mẫu câu' };
  const conThieu = ds.filter((v) => !daXem.has(v.tep)).length;
  const moKhoa = hong || ds.length === 0 || conThieu === 0;

  return (
    <section className="flex flex-col gap-4">
      {ds.length > 1 && (
        <div className="flex flex-wrap gap-2">
          {ds.map((v, k) => (
            <button key={v.tep} type="button" onClick={() => datI(k)}
              className={`rounded-xl2 px-4 py-2.5 font-semibold transition
                focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
                ${k === i ? 'bg-navy text-white'
                  : daXem.has(v.tep) ? 'bg-teal-pale text-teal-dark hover:bg-line'
                  : 'bg-soft text-navy hover:bg-line'}`}>
              {daXem.has(v.tep) ? '✓ ' : ''}{NHAN[v.vai] || 'Mẫu câu'} · {v.cau}
            </button>
          ))}
        </div>
      )}

      <Video key={ds[i]?.tep} tep={ds[i]?.tep} ten="Xem mẫu câu" phu={ds[i]?.cau}
             onXongLan1={() => datDaXem((s) => new Set(s).add(ds[i]?.tep))}
             onLoi={() => datHong(true)} />

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

      <NutTiep onClick={onTiep} chu="Vào luyện tập" tat={!moKhoa}
               viSao={conThieu === 1
                 ? 'Còn một mẫu câu nữa con chưa xem.'
                 : `Còn ${conThieu} mẫu câu nữa con chưa xem.`} />
    </section>
  );
}

/* ─────────── chặng 3 · luyện tập ─────────── */

const MUC = [
  { khoa: 'warmup', sao: '★', ten: 'Nghe và hiểu' },
  { khoa: 'standard', sao: '★★', ten: 'Ráp câu' },
  { khoa: 'challenge', sao: '★★★', ten: 'Gõ lại' },
];

/**
 * BA MỨC, ĐI LẦN LƯỢT — và mỗi mức làm hết mới sang mức sau.
 *
 * ── CÂU BỎ QUA KHÔNG ĐƯỢC BIẾN MẤT ──
 * Bé sai 2 lần thì được bỏ qua một câu (`duocBoQua` ở lib/dandat.js) — bắt làm
 * tới khi đúng thì có câu bé không bao giờ ra khỏi được. Nhưng bản trước bỏ qua
 * xong là câu ấy mất hẳn: bé đi hết mức mà nửa số câu chưa từng làm được, và
 * không chỗ nào ghi lại.
 *
 * Nay câu bỏ qua được GOM LẠI, và hết mức thì mời bé làm đúng chừng ấy câu một
 * lượt nữa. Chỉ MỘT lượt: hai lượt rồi vẫn tắc thì cái bé cần là người lớn ngồi
 * cạnh, không phải vòng lặp thứ ba.
 */
function LuyenTap({ bai, onTiep }) {
  const [m, datM] = useState(0);
  const [xaM, datXaM] = useState(0);          // mức xa nhất đã mở
  const [i, datI] = useState(0);
  const [dem, datDem] = useState({ dung: 0, tong: 0 });
  const [no, datNo] = useState([]);           // câu bé bỏ qua trong mức này
  const [lamLai, datLamLai] = useState(null); // đang làm lại đúng những câu ấy
  const [moiLamLai, datMoiLamLai] = useState(false);

  const goc = bai.practice.pools[MUC[m].khoa] || [];
  const pool = lamLai || goc;
  const cau = pool[i];

  const sangMuc = (k) => {
    datM(k); datI(0); datNo([]); datLamLai(null); datMoiLamLai(false);
    if (k > xaM) datXaM(k);
  };

  const xong = (kq) => {
    datDem((d) => ({ dung: d.dung + (kq.dung ? 1 : 0), tong: d.tong + 1 }));
    if (kq.boQua) datNo((n) => (n.includes(cau.id) ? n : [...n, cau.id]));

    if (i + 1 < pool.length) { datI(i + 1); return; }
    /* Hết lượt. Còn câu nợ mà chưa làm lại lượt nào thì mời làm lại. */
    if (!lamLai && no.length + (kq.boQua ? 1 : 0) > 0) { datMoiLamLai(true); return; }
    if (m + 1 < MUC.length) { sangMuc(m + 1); return; }
    onTiep();
  };

  if (!cau && !moiLamLai) return <NutTiep onClick={onTiep} chu="Vào sát hạch" />;

  if (moiLamLai) {
    const ds = goc.filter((c) => no.includes(c.id));
    return (
      <section className="flex flex-col items-start gap-4">
        <div className="w-full rounded-xl2 bg-gold-pale p-6">
          <p className="text-4xl" aria-hidden="true">💪</p>
          <p className="mt-2 text-2xl font-bold text-ink">
            Còn {ds.length} câu con chưa làm được
          </p>
          <p className="text-gold-dark">
            Con vừa nghe và xem thêm rồi đấy. Làm lại đúng {ds.length} câu này thôi nhé.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button type="button"
            onClick={() => { datLamLai(ds); datI(0); datMoiLamLai(false); }}
            className="rounded-xl2 bg-navy px-6 py-3 text-lg font-semibold text-white
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            Làm lại {ds.length} câu →
          </button>
          <button type="button"
            onClick={() => { if (m + 1 < MUC.length) sangMuc(m + 1); else onTiep(); }}
            className="rounded-xl2 border-2 border-line px-5 py-3 font-semibold text-mute
              hover:border-navy hover:text-navy
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            Để sau
          </button>
        </div>
      </section>
    );
  }

  return (
    <section className="flex flex-col gap-4">
      {/* Thanh MỨC — cùng luật với thanh chặng: mức đã qua bấm vào làm lại được. */}
      <ol className="flex flex-wrap gap-1.5">
        {MUC.map((x, k) => (
          <li key={x.khoa}>
            <button type="button" disabled={k > xaM} onClick={() => sangMuc(k)}
              title={k > xaM ? 'Con làm xong mức trước thì mức này mở ra'
                   : k < m ? 'Bấm để làm lại mức này' : undefined}
              className={`rounded-full px-3 py-1 text-xs font-semibold transition
                disabled:cursor-not-allowed disabled:opacity-45
                focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
                ${k === m ? 'bg-gold text-gold-dark'
                  : k < m ? 'bg-teal-pale text-teal-dark hover:bg-teal hover:text-white'
                  : 'bg-soft text-mute'}`}>
              {k < m ? '✓ ' : k > xaM ? '🔒 ' : ''}{x.sao} {x.ten}
            </button>
          </li>
        ))}
      </ol>

      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className="text-lg font-bold text-gold-dark">
          <span className="text-gold">{MUC[m].sao}</span> {MUC[m].ten}
          {lamLai && <span className="ml-2 text-sm font-normal text-mute">· làm lại</span>}
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

/* ─────────── chặng cuối · sát hạch ─────────── */

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
            {dat ? 'Con qua bài rồi. Giỏi lắm!'
                 : `Cần ${can} câu đúng. Con nghe lại phần giảng rồi thử lần nữa nhé — `
                   + `làm ${THU_TOI_THIEU} lần thì bài sau cũng mở ra.`}
          </p>
        </div>
        <NutTiep onClick={() => onXong({ pass: dat, dung, tong: ds.length, bac: 4 })}
          chu={dat ? 'Sang bài sau' : 'Về danh sách bài'} />
      </section>
    );
  }

  const q = ds[i];
  const tra = (dung) => {
    if (dung) datDung((n) => n + 1);
    if (i + 1 < ds.length) datI(i + 1); else datHet(true);
  };

  return (
    <section className="flex flex-col gap-4">
      <p className="text-sm text-mute">Câu {i + 1}/{ds.length}</p>
      <div className="rounded-xl2 border-2 border-line bg-white p-5">
        {/* Nghe và nhìn, không phải đọc — xem `CauNgheNhin.jsx`. Kỳ ôn tập chương
            dùng chung đúng component này, để một câu hỏi không có hai cách chấm. */}
        <CauNgheNhin key={q.id} cau={q} onXong={(r) => tra(r.dung)} />
      </div>
    </section>
  );
}
