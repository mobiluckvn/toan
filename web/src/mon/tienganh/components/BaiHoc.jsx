import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import ThanhViec from './ThanhViec.jsx';
import ThanhCau from './ThanhCau.jsx';
import PhongNoi from './PhongNoi.jsx';
import CauHoi from './CauHoi.jsx';
import CauNgheNhin from './CauNgheNhin.jsx';
import HinhVe from './HinhVe.jsx';
import NutNoi from './NutNoi.jsx';
import HoiThoai from './HoiThoai.jsx';
import Video from '../../../chung/components/Video.jsx';
import GocBoMe, { MucBoMe } from './GocBoMe.jsx';
import { napBai, napSoAm, hangXom, hinhCuaTu, dsVideoTu } from '../lib/noiDung.js';
import { maCua } from './NutNghe.jsx';
import {
  changCua, NHAN_CHANG, trangThaiChang, THU_TOI_THIEU, viecChangTu, viecChangCau,
  noiDuoc, CHANG_KHONG_KHOA,
} from '../lib/dandat.js';
import { DAT as DAT_NOI } from '../lib/chamnoi.js';
import { maPhienMoi } from '../lib/suKien.js';
import { xepTheoZPD } from '../lib/zpd.js';

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
export default function BaiHoc({ id, tienDo, onXongBai, onThoat, onNoi, onChang,
                                 onMoc, tenBe = 'Bo', soThich = null,
                                 onSoThich = null, onLuot = null, mucThao = null,
                                 hoSoDang = null }) {
  /* MỘT LẦN MỞ BÀI LÀ MỘT PHIÊN. Mã phiên đi vào mã từng bản ghi nhật ký, nên nó
     phải ĐỔI khi đổi bài và GIỮ NGUYÊN trong suốt bài — `useMemo` theo `id` cho
     đúng cả hai. Component này KHÔNG dựng lại khi đổi bài (chỗ gọi không đặt
     `key`), nên để mã phiên trong `useRef` trần là hai bài dính chung một phiên. */
  const maPhien = useMemo(() => maPhienMoi(), [id]);
  const ghiLuot = useCallback((e, phase = 'practice') => {
    onLuot?.({ ...e, phase, maPhien, microId: id });
  }, [onLuot, maPhien, id]);
  const [bai, datBai] = useState(null);
  const [loi, datLoi] = useState(null);
  const [tai, datTai] = useState(0);
  const [xa, datXa] = useState(0);
  /* Mốc trong chặng, đọc MỘT LẦN lúc mở bài — cùng lý do với `chang` ở dưới:
     nghe cả `tienDo` thì mỗi lần ghi mốc lại nạp lại bài, thành vòng lặp. */
  const [mocDau, datMocDau] = useState(null);

  useEffect(() => {
    let song = true;
    datBai(null); datLoi(null); datTai(0); datXa(0); datMocDau(null);
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
        datMocDau(tienDo?.micros?.[id]?.moc || null);
      } catch (e) { if (song) datLoi(e.message); }
    })();
    return () => { song = false; };
    /* CỐ Ý không nghe `tienDo`: chỉ đọc chặng đã nhớ MỘT LẦN lúc mở bài. Nghe cả
       `tienDo` thì mỗi lần ghi chặng lại chạy lại effect này, `datBai(null)` xoá
       màn, nạp lại bài — thành vòng lặp không đáy. Đã dính đúng kiểu này một lần
       ở sổ tiến độ, ghi trong docs/tiep_theo_tienganh_lop1.md. */
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  /* ⚠ BA HOOK NÀY PHẢI ĐỨNG TRƯỚC MỌI LỆNH `return` SỚM.
     Đặt xuống dưới thì lần vẽ đầu (`bai` còn null, hàm thoát ở nhánh "Đang mở
     bài…") gọi ít hook hơn lần vẽ sau — React đếm hook theo THỨ TỰ GỌI, lệch một
     cái là ném lỗi 310 và cả màn hình trắng. Đã vỡ đúng thế: 66 cổng xanh, `npm run
     build` xanh, mở bài ra thì trắng bốc.
     Chúng cần `useCallback` vì ba màn con canh chính hàm này trong effect ghi mốc;
     tạo mới mỗi lần vẽ thì effect chạy lại sau từng lần vẽ. */
  const mocTu = useCallback((m) => onMoc?.('tu', m), [onMoc]);
  const mocCau = useCallback((m) => onMoc?.('cau', m), [onMoc]);
  const mocLuyen = useCallback((m) => onMoc?.('luyen', m), [onMoc]);

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
  /* Chặng KHÔNG KHOÁ nhảy tới lúc nào cũng được — xem CHANG_KHONG_KHOA. */
  const nhay = (i) => { if (i <= xa || CHANG_KHONG_KHOA.has(CHANG[i])) datTai(i); };

  const k = CHANG[tai];
  return (
    <Khung onThoat={onThoat} ten={bai.title}>
      <ThanhChang ten={tenChang} ds={CHANG} tai={tai} xa={xa} onChon={nhay} />

      {/* `key` gắn mã bài: đổi bài thì ba màn dưới đây phải dựng lại từ đầu, không
          thì mốc của bài cũ dính sang bài mới. */}
      {k === 'tu' && (
        <ManTu key={id} bai={bai} onTiep={xong} onNoi={onNoi}
               moc={mocDau?.tu} onMoc={mocTu} />
      )}
      {k === 'cau' && (
        <ManCau key={id} bai={bai} onTiep={xong}
                moc={mocDau?.cau} onMoc={mocCau} />
      )}
      {k === 'luyen' && (
        <LuyenTap key={id} bai={bai} onTiep={xong}
                  moc={mocDau?.luyen} onMoc={mocLuyen} onLuot={ghiLuot}
                  mucThao={mucThao} hoSoDang={hoSoDang} />
      )}
      {k === 'noi' && (
        <HoiThoai
          hoiThoai={bai.knowledgeCore.hoiThoai}
          tenBe={tenBe}
          onXong={(kq) => { onNoi?.('hoiThoai', kq); xong(); }}
        />
      )}
      {k === 'sat' && (
        <SatHach bai={bai} onXong={(kq) => onXongBai(kq, hangXom(id).sau)}
                 onLuot={(e) => ghiLuot(e, 'assess')} />
      )}
      {k === 'phong' && (
        <PhongNoi bai={bai} tienDo={tienDo} tenBe={tenBe}
                  soThich={soThich} onSoThich={onSoThich} />
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
function ThanhChang({ ten, ds = [], tai, xa, onChon }) {
  return (
    <div className="flex flex-col gap-2">
      <ol className="flex flex-wrap gap-1.5">
        {ten.map((x, i) => {
          const tt = trangThaiChang(i, tai, xa, ds);
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
                {tt === 'xong' ? '✓ ' : tt === 'khoa' ? '🔒 ' : tt === 'mo' ? '' : `${i + 1}. `}{x}
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
function ManTu({ bai, onTiep, onNoi, moc, onMoc }) {
  const dsVideo = useMemo(() => dsVideoTu(bai), [bai]);
  /* Nghe bốn từ rồi bị gọi đi ăn cơm — vào lại mà thanh VIỆC CỦA CON trắng trơn
     thì công vừa bỏ ra không để lại dấu, và đó đúng là lúc bé bỏ cuộc.

     Mốc CŨ ghi `daXem: true` (hồi mỗi bài chỉ có một video). Bé đang học dở lớp 1
     mà bản mới lên là mốc ấy vẫn nằm trong máy — đọc nó thành `new Set(true)` thì
     ra Set rỗng, và bé vừa xem xong lại thấy ô video trắng. Nên dịch thẳng: đã xem
     hết ngày ấy nghĩa là đã xem hết bây giờ. */
  const [daXem, datDaXem] = useState(() => new Set(
    moc?.daXem === true ? dsVideo.map((g) => g.tep) : (moc?.daXem || []),
  ));
  const [videoHong, datVideoHong] = useState(false);
  const [daNghe, datDaNghe] = useState(() => new Set(moc?.daNghe || []));
  const [soNoi, datSoNoi] = useState(() => ({ ...(moc?.soNoi || {}) }));
  const [micHong, datMicHong] = useState(false);
  const [iTu, datITu] = useState(() => Math.max(0, Number(moc?.iTu) || 0));
  const [iVideo, datIVideo] = useState(0);
  const K = bai.knowledgeCore.statements || [];
  const dsTu = bai.knowledgeCore.vocabulary || [];
  const oVideo = useRef(null);

  /* Ghi mốc — `daNghe` là Set nên phải rải thành mảng, không thì JSON ra `{}` và
     phép so "có đổi không" bên `ghiMoc` luôn thấy giống nhau, mốc đứng im. */
  useEffect(() => {
    onMoc?.({ daXem: [...daXem], daNghe: [...daNghe], soNoi, iTu });
  }, [daXem, daNghe, soNoi, iTu, onMoc]);

  /* Gắn hình vào từ TRƯỚC khi đưa cho thanh việc — cùng nguồn với thẻ từ. */
  const dsTuCoHinh = useMemo(
    () => dsTu.map((v) => ({ ...v, ...hinhCuaTu(bai, v.tu) })),
    [bai, dsTu],
  );

  const { viec, mo, conThieu, vuongMicro } = viecChangTu({
    dsTu: dsTuCoHinh, dsVideo, daXem: [...daXem], videoHong,
    daNghe: [...daNghe], soNoi, micHong, datNoi: DAT_NOI,
  });

  /* Bấm một ô trên thanh: ô TỪ thì chuyển hẳn sang từ ấy (màn chỉ hiện một từ
     một lúc), ô VIDEO thì MỞ ĐÚNG video ấy rồi cuộn lên. Biết mình thiếu gì mà
     không tới được chỗ ấy thì thanh mới đi nửa đường. */
  const toiViec = useCallback((x) => {
    if (x.loai === 'video') {
      const k = dsVideo.findIndex((g) => g.tep === x.tep);
      if (k >= 0) datIVideo(k);
      const dich = oVideo.current;
      if (!dich) return;
      dich.scrollIntoView({ behavior: 'smooth', block: 'center' });
      dich.classList.add('ring-4', 'ring-gold');
      setTimeout(() => dich.classList.remove('ring-4', 'ring-gold'), 1400);
      return;
    }
    const i = dsTuCoHinh.findIndex((v) => v.tu === x.ma);
    if (i >= 0) datITu(i);
  }, [dsTuCoHinh, dsVideo]);

  /* `lan` chỉ cộng khi máy NGHE RA CHỮ. Bé bấm nút rồi ngồi im thì không tính —
     nếu tính thì bấm hai cái trong im lặng là "đã thử thật 2 lần" và qua luôn. */
  const ghiNoi = useCallback((tu, kq) => {
    if (kq?.coTieng) {
      datSoNoi((s) => {
        const cu = s[tu] || { caoNhat: null, lan: 0 };
        return {
          ...s,
          [tu]: {
            caoNhat: Math.max(cu.caoNhat ?? 0, kq.diem ?? 0),
            lan: cu.lan + 1,
          },
        };
      });
    }
    onNoi?.(tu, kq);
  }, [onNoi]);

  return (
    <section className="flex flex-col gap-4">
      <ThanhViec viec={viec} conThieu={conThieu} mo={mo} dangO={dsTuCoHinh[iTu]?.tu}
                 vuongMicro={vuongMicro} onChon={toiViec} />

      {/* MỘT video một lúc, đúng khuôn chặng Mẫu câu. Bày cả ba tệp cùng lúc thì
          màn dài ra và bé không biết xem cái nào trước; thanh việc ở trên đã lo
          phần nhìn bao quát, bấm ô nào là nhảy tới video ấy.
          `key` là tên tệp: không có nó thì React giữ nguyên thẻ <video> cũ, đổi ô
          mà tranh vẫn đứng im ở khung cuối của video trước. */}
      <div ref={oVideo} className="rounded-xl2 transition">
        {dsVideo.length > 1 && (
          <p className="mb-2 text-sm font-semibold uppercase tracking-wide text-mute">
            Nhóm từ {iVideo + 1} / {dsVideo.length} · {dsVideo[iVideo]?.ten}
          </p>
        )}
        <Video
          key={dsVideo[iVideo]?.tep}
          tep={dsVideo[iVideo]?.tep}
          ten={dsVideo.length > 1 ? dsVideo[iVideo]?.ten : 'Xem từ mới'}
          phu={`${(dsVideo[iVideo]?.tu || dsTu).length} từ · khoảng nửa phút`}
          onXongLan1={() => {
            const t = dsVideo[iVideo]?.tep;
            datDaXem((s) => (s.has(t) ? s : new Set(s).add(t)));
            /* Xem xong thì tự sang nhóm CHƯA XEM kế tiếp — bé không phải đi tìm.
               Không tự chạy, chỉ đổi tệp: luật "không tự chạy" nằm ở `Video`. */
            const k = dsVideo.findIndex((g, j) => j > iVideo && !daXem.has(g.tep));
            if (k >= 0) datIVideo(k);
          }}
          onLoi={() => datVideoHong(true)}
        />
      </div>

      <LuyenTu
        bai={bai} ds={dsTuCoHinh} i={iTu} onDoi={datITu}
        soNoi={soNoi} micHong={micHong}
        onNoi={ghiNoi} onMicHong={() => datMicHong(true)}
        onNghe={(t) => datDaNghe((s) => (s.has(t) ? s : new Set(s).add(t)))}
      />

      <GocBoMe ten="Góc bố mẹ · bài này dạy gì">
        <MucBoMe nhan="Mục tiêu">{bai.objective.text}</MucBoMe>
        {K.map((x) => <MucBoMe key={x.id} nhan={x.id}>{x.text}</MucBoMe>)}
        <MucBoMe nhan="Cùng con ở nhà">{bai.parentNote?.homeActivity}</MucBoMe>
        <MucBoMe nhan="Nên và không nên">{bai.parentNote?.watchFor}</MucBoMe>
      </GocBoMe>

      <NutTiep
        onClick={onTiep}
        tat={!mo}
        chu="Sang mẫu câu"
        viSao="Con làm nốt mấy ô còn trắng ở trên rồi đi tiếp nhé."
      />
    </section>
  );
}

/* `hinhCuaTu` nay ở `lib/noiDung.js` — phòng luyện nói cũng vẽ hình từ, và ba chỗ
   vẽ cùng một vật thì phải hỏi cùng một nguồn. Đọc phần chú ở hàm ấy. */


/**
 * LUYỆN TỪNG TỪ — MỘT từ một lượt, và việc chính là NÓI.
 *
 * ── VÌ SAO BỎ LƯỚI BỐN THẺ ──
 * Bản trước bày cả bốn từ cùng lúc, mỗi thẻ hai nút tròn 🔈 và 🎤 to bằng nhau.
 * Ba điều hỏng cùng lúc:
 *
 *   · hai nút bằng nhau thì trông như hai việc ngang hàng, trong khi video vừa
 *     dạy âm xong rồi — tới đây NÓI mới là đích, nghe chỉ là để lấy mẫu;
 *   · bấm 🎤 thì ô chấm điểm bung ra ở DƯỚI CẢ LƯỚI, cách xa cái thẻ bé vừa bấm.
 *     Bé 6 tuổi không nối được hai thứ ấy với nhau;
 *   · muốn nói một từ phải bấm ba lần: 🎤 → tìm ô ở dưới → "Bấm rồi nói".
 *
 * Nay màn chỉ còn MỘT từ: hình to, và nút nói là thứ to nhất màn. Bé không phải
 * chọn gì, không lạc đi đâu, chấm điểm hiện ngay tại chỗ. Phần nhìn bao quát đã
 * có thanh VIỆC CỦA CON ở trên lo — bấm ô nào trên thanh là nhảy tới từ ấy.
 *
 * ── VẪN GIỮ: MỖI LÚC CHỈ MỘT MICRO ──
 * Hai micro cùng bật thì máy nghe lẫn, và bé cũng không biết đang được hỏi từ
 * nào. Màn một từ một lượt làm điều ấy thành hiển nhiên, không phải canh nữa.
 */
function LuyenTu({ bai, ds, i, onDoi, soNoi, micHong, onNoi, onNghe, onMicHong }) {
  /* Các từ KHÁC của bài — để bộ chấm bắt được việc bé đọc "dog" thành "duck".
     Hai từ ấy cùng một unit, nhầm sang nhau mà vẫn điểm cao thì bài nói vô nghĩa. */
  const cungBai = useMemo(() => ds.map((x) => x.tu), [ds]);
  const v = ds[i];
  if (!v) return null;

  const muc = noiDuoc(soNoi[v.tu], DAT_NOI);
  const conTu = ds.findIndex((x, k) => k > i && noiDuoc(soNoi[x.tu], DAT_NOI) === 'chua');
  const tuSau = conTu >= 0 ? conTu : (i + 1 < ds.length ? i + 1 : -1);

  return (
    <div className="flex flex-col gap-3 rounded-xl2 border-2 border-line bg-white p-4">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold uppercase tracking-wide text-mute">
          Từ {i + 1} / {ds.length}
        </p>
        {muc !== 'chua' && (
          <span className={`rounded-full px-3 py-1 text-sm font-bold
            ${muc === 'dat' ? 'bg-teal-pale text-teal-dark' : 'bg-gold-pale text-gold-dark'}`}>
            {muc === 'dat' ? '⭐ Con nói được rồi' : '✓ Con đã thử thật'}
          </span>
        )}
      </div>

      {/* Hình to hẳn: đây là thứ bé nhìn vào để nhớ nghĩa lúc đang cố nói.
          ⚠ KHÔNG CÓ HÌNH thì đừng vẽ gì Ở ĐÂY — 51 từ của lớp 3 không vẽ được, và
          chữ thì ngay bên dưới đã có, to và rõ. (`HinhVe` lui về hiện chữ, nhưng ở
          chỗ này lui như thế là hiện hai lần cùng một chữ.) */}
      <div className="flex flex-col items-center gap-1 py-2">
        {(() => {
          const h = hinhCuaTu(bai, v.tu);
          return (h.hinh || h.ve)
            ? <span className="text-7xl leading-none"><HinhVe ten={v.tu} {...h} /></span>
            : null;
        })()}
        <p className="text-3xl font-bold text-navy">{v.tu}</p>
        <p className="font-mono text-sm text-mute">{v.ipa}</p>
        <p className="text-lg text-ink">{v.nghia}</p>
      </div>

      {/* `key` theo từ: đổi từ thì ô nói dựng lại từ đầu, không mang điểm của từ
          trước sang từ sau. */}
      <NutNoi
        key={v.tu}
        cau={v.tu}
        loai="tu"
        maAm={v.am}
        doiThu={cungBai}
        noiBat
        nhan="Nghe cô đọc, rồi con nói lại"
        onNghe={() => onNghe?.(v.tu)}
        onXong={(k) => onNoi?.(v.tu, k)}
        onHong={onMicHong}
      />

      {/* Đi lại giữa các từ. Nút "từ sau" nhảy tới từ CHƯA NÓI gần nhất, để bé
          không phải tự dò xem còn thiếu từ nào. */}
      <div className="flex items-center justify-between gap-2">
        <button type="button" onClick={() => onDoi(i - 1)} disabled={i === 0}
          className="rounded-xl2 px-4 py-2 font-semibold text-navy disabled:text-line
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          ← Từ trước
        </button>
        <button type="button" onClick={() => onDoi(tuSau)} disabled={tuSau < 0}
          className="rounded-xl2 bg-navy px-5 py-2 font-semibold text-white
            disabled:bg-line disabled:text-mute
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Từ sau →
        </button>
      </div>

      {micHong && (
        <p className="rounded-xl2 bg-gold-pale p-2 text-sm text-gold-dark">
          Máy chưa nghe được nên phần nói để lúc khác — con cứ bấm 🔈 nghe rồi
          đọc theo, xong bấm “Từ sau” nhé.
        </p>
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
function ManCau({ bai, onTiep, moc, onMoc }) {
  const ds = bai.video?.cau || [];
  const [i, datI] = useState(() => Math.max(0, Number(moc?.i) || 0));
  const [daXem, datDaXem] = useState(() => new Set(moc?.daXem || []));
  const [hong, datHong] = useState(false);
  const [soNoi, datSoNoi] = useState(() => ({ ...(moc?.soNoi || {}) }));
  const [micHong, datMicHong] = useState(false);
  const mcDs = bai.knowledgeCore.mauCauDs || [];
  const mc = mcDs[i] || bai.knowledgeCore.mauCau;
  const bay = bai.knowledgeCore.misconceptions?.[0];
  const NHAN = { hoi: 'Câu hỏi', dap: 'Câu trả lời', cau: 'Mẫu câu' };

  const dsCau = useMemo(
    () => ds.map((v) => ({ ...v, nhanVai: NHAN[v.vai] || 'Mẫu câu' })),
    [ds],
  );

  useEffect(() => {
    onMoc?.({ i, daXem: [...daXem], soNoi });
  }, [i, daXem, soNoi, onMoc]);
  const { viec, mo, conThieu, vuongMicro } = viecChangCau({
    dsCau, daXem: [...daXem], videoHong: hong, soNoi, micHong, datNoi: DAT_NOI,
  });

  const ghiNoi = useCallback((cau, kq) => {
    if (!kq?.coTieng) return;
    datSoNoi((s) => {
      const cu = s[cau] || { caoNhat: null, lan: 0 };
      return { ...s, [cau]: { caoNhat: Math.max(cu.caoNhat ?? 0, kq.diem ?? 0), lan: cu.lan + 1 } };
    });
  }, []);

  const cauNay = ds[i]?.cau;
  const chuaXong = ds.findIndex((v, k) => k > i
    && !(daXem.has(v.tep) && noiDuoc(soNoi[v.cau], DAT_NOI) !== 'chua'));
  const mauSau = chuaXong >= 0 ? chuaXong : (i + 1 < ds.length ? i + 1 : -1);

  return (
    <section className="flex flex-col gap-4">
      <ThanhViec viec={viec} conThieu={conThieu} mo={mo} dangO={ds[i]?.tep}
                 vuongMicro={vuongMicro}
                 onChon={(x) => { const k = ds.findIndex((v) => v.tep === x.ma); if (k >= 0) datI(k); }} />

      {ds.length > 1 && (
        <p className="text-sm font-semibold uppercase tracking-wide text-mute">
          {NHAN[ds[i]?.vai] || 'Mẫu câu'} {i + 1} / {ds.length}
        </p>
      )}

      <Video key={ds[i]?.tep} tep={ds[i]?.tep} ten="Xem mẫu câu" phu={ds[i]?.cau}
             onXongLan1={() => datDaXem((s) => new Set(s).add(ds[i]?.tep))}
             onLoi={() => datHong(true)} />

      {/* Nói CẢ CÂU là việc khó nhất chặng này, nên nút nói dùng dáng nổi bật y
          như chặng Từ mới — `key` theo câu để đổi mẫu là ô nói dựng lại từ đầu. */}
      {cauNay && (
        <NutNoi
          key={cauNay}
          cau={cauNay}
          loai="cau"
          maAm={maCauAm(cauNay)}
          noiBat
          nhan="Nghe cô đọc, rồi con nói cả câu"
          onXong={(k) => ghiNoi(cauNay, k)}
          onHong={() => datMicHong(true)}
        />
      )}

      {ds.length > 1 && (
        <div className="flex items-center justify-between gap-2">
          <button type="button" onClick={() => datI(i - 1)} disabled={i === 0}
            className="rounded-xl2 px-4 py-2 font-semibold text-navy disabled:text-line
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            ← Mẫu trước
          </button>
          <button type="button" onClick={() => datI(mauSau)} disabled={mauSau < 0}
            className="rounded-xl2 bg-navy px-5 py-2 font-semibold text-white
              disabled:bg-line disabled:text-mute
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            Mẫu sau →
          </button>
        </div>
      )}

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

      <NutTiep onClick={onTiep} chu="Vào luyện tập" tat={!mo}
               viSao="Con làm nốt mấy ô còn trắng ở trên rồi đi tiếp nhé." />
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
function LuyenTap({ bai, onTiep, moc, onMoc, onLuot = null, mucThao = null,
                    hoSoDang = null }) {
  /* ── VÀO LẠI ĐÚNG CHỖ BỎ DỞ ──
     `moc` là thứ đã ghi lần trước. KHÔNG tin nó mù quáng: sổ có thể là của bản bài
     cũ, mà chỉ số mức hay chỉ số câu nhảy ra ngoài mảng là màn trắng ngay. Nên kẹp
     lại trong khoảng hợp lệ, và lọc `no` theo những câu CÓ THẬT trong bài này. */
  const dau = useMemo(() => {
    const d = { m: 0, xaM: 0, i: 0, dem: { dung: 0, tong: 0 }, no: [], tt: [],
                moiLamLai: false };
    if (!moc) return d;
    const m0 = Math.max(0, Math.min(Number(moc.m) || 0, MUC.length - 1));
    const pool = bai.practice.pools[MUC[m0].khoa] || [];
    const idCo = new Set(pool.map((c) => c.id));
    return {
      m: m0,
      xaM: Math.max(m0, Math.min(Number(moc.xaM) || 0, MUC.length - 1)),
      i: Math.max(0, Math.min(Number(moc.i) || 0, Math.max(pool.length - 1, 0))),
      dem: { dung: Number(moc.dem?.dung) || 0, tong: Number(moc.dem?.tong) || 0 },
      no: (moc.no || []).filter((x) => idCo.has(x)),
      tt: Array.isArray(moc.tt) ? moc.tt.slice(0, pool.length) : [],
      moiLamLai: !!moc.moiLamLai,
    };
  }, [moc, bai]);

  const [m, datM] = useState(dau.m);
  const [xaM, datXaM] = useState(dau.xaM);    // mức xa nhất đã mở
  const [i, datI] = useState(dau.i);
  /* ⚠ `dem` HIỆN KHÔNG AI ĐỌC. Thanh "Đúng x/y" đếm thẳng từ `ttCau`, còn `dem` chỉ
     được ghi vào chứ chưa hiện ở đâu. Vẫn giữ trong mốc vì nó là một trong năm thứ
     mà Lỗi B làm mất, và ngày nào đó hiện nó ra thì con số đã đúng sẵn — chứ không
     phải sửa lại chỗ lưu lần nữa. */
  const [dem, datDem] = useState(dau.dem);
  const [no, datNo] = useState(dau.no);       // câu bé bỏ qua trong mức này
  const [lamLai, datLamLai] = useState(null); // đang làm lại đúng những câu ấy
  const [moiLamLai, datMoiLamLai] = useState(dau.moiLamLai);

  const [ttCau, datTtCau] = useState(dau.tt); // trạng thái từng chấm của mức này

  /* Ghi mốc sau MỖI lần đổi chỗ. Gọi dày thế này chỉ an toàn vì `ghiMoc` trả nguyên
     khối cũ khi không có gì đổi — xem chú thích dài ở `lib/progress.js`.

     KHÔNG ghi `lamLai`: lúc ấy `i` đánh số theo danh sách câu nợ chứ không theo mức,
     lưu vào rồi khôi phục là bé rơi vào câu khác hẳn. Thay vào đó ghi `moiLamLai`,
     nên vào lại thì lời mời làm lại hiện ra nguyên vẹn — mất mấy giây, không mất
     câu nào. */
  useEffect(() => {
    if (lamLai) return;
    onMoc?.({ m, xaM, i, dem, no, tt: ttCau, moiLamLai });
  }, [m, xaM, i, dem, no, ttCau, moiLamLai, lamLai, onMoc]);

  /* ── XẾP CÂU THEO ZPD ──
     Chỗ bé đang chông chênh lên trước, chỗ đã thạo xuống cuối. KHÔNG bỏ câu nào
     — chỉ đổi thứ tự, vì thanh đếm câu và phép chấm đều dựa trên số câu.
     Xếp trong MỘT mức thôi: ba mức là thang độ khó do người soạn dựng.
     `useMemo` để thứ tự KHÔNG đổi giữa chừng khi màn vẽ lại — đổi giữa buổi thì
     `i` đang trỏ câu này bỗng trỏ câu khác, bé mất câu đang làm dở. */
  const goc = React.useMemo(
    () => xepTheoZPD(bai.practice.pools[MUC[m].khoa] || [], mucThao, hoSoDang),
    [bai, m, mucThao, hoSoDang],
  );
  const pool = lamLai || goc;
  const cau = pool[i];

  const sangMuc = (k) => {
    datM(k); datI(0); datNo([]); datLamLai(null); datMoiLamLai(false); datTtCau([]);
    if (k > xaM) datXaM(k);
  };

  const xong = (kq) => {
    datDem((d) => ({ dung: d.dung + (kq.dung ? 1 : 0), tong: d.tong + 1 }));
    datTtCau((t) => { const s = [...t]; s[i] = kq.boQua ? 'no' : (kq.dung ? 'dung' : 'sai'); return s; });
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
            onClick={() => { datLamLai(ds); datI(0); datMoiLamLai(false); datTtCau([]); }}
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
      {/* VIỆC CỦA CON của chặng luyện tập: ba ô MỨC to ở trên, rồi dãy chấm cho
          từng câu của mức đang làm. Cùng ý với thanh ở chặng Từ mới — bé liếc một
          cái là biết đang ở đâu và còn bao nhiêu, không phải đọc "Câu 4/9". */}
      <section aria-label="Việc của con trong phần này"
        className="flex flex-col gap-2 rounded-xl2 border-2 border-line bg-white p-3">
        <div className="flex flex-wrap items-baseline gap-x-3">
          <h3 className="text-sm font-bold uppercase tracking-wide text-navy">Việc của con</h3>
          {lamLai && <p className="text-sm text-gold-dark">Đang làm lại mấy câu còn nợ.</p>}
        </div>

        <ol className="flex flex-wrap gap-2">
          {MUC.map((x, k) => {
            const khoa = k > xaM;
            return (
              <li key={x.khoa}>
                <button type="button" disabled={khoa} onClick={() => sangMuc(k)}
                  aria-current={k === m ? 'true' : undefined}
                  aria-label={`${x.ten} — ${khoa ? 'chưa tới lượt' : k < m ? 'đã làm qua, bấm để làm lại' : 'con đang ở đây'}`}
                  className={`flex w-[5.5rem] flex-col items-center gap-0.5 rounded-xl2 border-2 p-2
                    transition disabled:cursor-not-allowed
                    focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
                    ${k === m ? 'border-gold bg-gold-pale ring-4 ring-navy'
                      : k < m ? 'border-teal bg-teal-pale hover:brightness-95'
                        : 'border-dashed border-line bg-soft'}`}>
                  <span aria-hidden="true" className={`text-xl leading-none ${khoa ? 'opacity-50' : ''}`}>
                    {khoa ? '🔒' : k < m ? '✅' : x.sao}
                  </span>
                  <span className={`text-[0.7rem] font-semibold leading-tight
                    ${khoa ? 'text-mute' : 'text-ink'}`}>{x.ten}</span>
                </button>
              </li>
            );
          })}
        </ol>

        <ThanhCau tong={pool.length} tt={ttCau} tai={i}
                  nhan={`Các câu của mức ${MUC[m].ten}`} />
      </section>
      <div className="rounded-xl2 border-2 border-line bg-white p-5">
        {/* `key` là BẮT BUỘC, không phải để React bớt cảnh báo. Không có nó thì
            component giữ nguyên state khi đổi câu, và lúc chuyển từ câu BẤM CHỌN
            (đáp án là chuỗi) sang câu XẾP THẺ (đáp án là mảng), lần vẽ đầu tiên
            gọi `''.map()` — cả bài trắng màn hình ngay giữa chừng. Đã vỡ thật ở
            đúng chỗ nối ★ sang ★★. */}
        <CauHoi key={cau.id} cau={cau} onXong={xong} onLuot={onLuot} />
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
  const [ttCau, datTtCau] = useState([]);
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
  const tra = (kqDung) => {
    if (kqDung) datDung((n) => n + 1);
    datTtCau((t) => { const s = [...t]; s[i] = kqDung ? 'dung' : 'sai'; return s; });
    if (i + 1 < ds.length) datI(i + 1); else datHet(true);
  };

  return (
    <section className="flex flex-col gap-4">
      {/* Dãy chấm thay cho dòng "Câu 1/5". Bé sát hạch mà không biết còn mấy câu
          thì mỗi câu đều có thể là câu cuối — dài vô tận với bé 6 tuổi. */}
      {ds.length > 1 && (
        <div className="rounded-xl2 border-2 border-line bg-white p-3">
          <ThanhCau tong={ds.length} tt={ttCau} tai={i} nhan="Các câu của bài sát hạch" />
        </div>
      )}
      <div className="rounded-xl2 border-2 border-line bg-white p-5">
        {/* Nghe và nhìn, không phải đọc — xem `CauNgheNhin.jsx`. Kỳ ôn tập chương
            dùng chung đúng component này, để một câu hỏi không có hai cách chấm. */}
        <CauNgheNhin key={q.id} cau={q} onXong={(r) => tra(r.dung)} />
      </div>
    </section>
  );
}
