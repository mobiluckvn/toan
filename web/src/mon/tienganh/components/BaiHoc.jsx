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
import { napBai, napSoAm, hangXom, hinhCuaTu, dsVideoTu, quyenCua } from '../lib/noiDung.js';
import { maCua } from './NutNghe.jsx';
import {
  changCua, NHAN_CHANG, trangThaiChang, thuToiThieu, viecChangTu, viecChangCau,
  noiDuoc, CHANG_KHONG_KHOA,
} from '../lib/dandat.js';
import { DAT as DAT_NOI } from '../lib/chamnoi.js';
import { maPhienMoi } from '../lib/suKien.js';
import { dungBang } from '../lib/bangtrangthai.js';
import PhuDao from './PhuDao.jsx';
import { viecTiepCuaNut, VIEC } from '../lib/chinhsach.js';
import { mucThaoCua } from '../lib/zpd.js';

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
                                 onHoSoAI = null,
                                 hoSoDang = null, onRoiMan = null, onPhuDao = null }) {
  /* ── SỰ KIỆN RỜI MÀN GIỮA CHỪNG (mục 2.1.2 · chiều Thời gian) ──
     Luận văn đòi đo "mệt mỏi nhận thức", nhưng muốn suy ra trạng thái mệt thì
     phải biết bé BỎ DỞ ở đâu — mà xưa nay bé mở bài rồi thoát KHÔNG để lại dấu
     vết nào. Từ `attempts` chỉ thấy những câu bé CÓ trả lời; bé mở bài, xem nửa
     video rồi tắt thì không ai biết.

     ⚠ CHỈ BẮT ĐƯỢC LÚC RỜI MÀN TỬ TẾ (bấm "Về", hoặc chuyển bài). Đóng thẳng tab
     hay sập máy thì React không kịp chạy hàm dọn — nên con số này là CẬN DƯỚI của
     số lần bỏ dở thật, và chỗ nào đọc nó cũng phải biết điều đó. */
  const moLuc = useRef(Date.now());
  const daXong = useRef(false);
  const soLuot = useRef(0);
  /* Chặng bé đang đứng lúc bỏ đi. Ô nhớ khai Ở ĐÂY còn GIÁ TRỊ gán mãi dưới kia
     (sau khi `bai` đã về) — khai hook ở dưới là lỗi 310, xem khối cảnh báo dưới. */
  const changCuoi = useRef(null);
  useEffect(() => {
    moLuc.current = Date.now();
    daXong.current = false;
    soLuot.current = 0;
  }, [id]);
  /* Rời màn mà chưa xong bài → ghi một bản ghi PHIÊN. */
  useEffect(() => () => {
    if (daXong.current) return;
    onRoiMan?.({
      maPhien,
      microId: id,
      chang: changCuoi.current,
      soLuot: soLuot.current,
      giay: Math.round((Date.now() - moLuc.current) / 1000),
    });
    /* `maPhien` cố ý không có trong dãy phụ thuộc: nó suy từ `id` (useMemo ngay
       dưới), thêm vào chỉ làm dãy dài ra chứ không đổi lúc nào effect chạy. */
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id, onRoiMan]);
  /* MỘT LẦN MỞ BÀI LÀ MỘT PHIÊN. Mã phiên đi vào mã từng bản ghi nhật ký, nên nó
     phải ĐỔI khi đổi bài và GIỮ NGUYÊN trong suốt bài — `useMemo` theo `id` cho
     đúng cả hai. Component này KHÔNG dựng lại khi đổi bài (chỗ gọi không đặt
     `key`), nên để mã phiên trong `useRef` trần là hai bài dính chung một phiên. */
  /* ⚠ `id` là phụ thuộc THỪA về mặt hình thức (thân hàm không đọc nó), và ESLint
     kêu đúng — nhưng nó chính là THỨ KÍCH HOẠT: mã phiên phải đổi khi đổi bài, và
     `useMemo` là cách duy nhất ở đây để nói điều đó. Bỏ `id` đi là mọi bài dùng
     chung một mã phiên, đúng cái chú thích trên vừa cảnh báo. */
  // eslint-disable-next-line react-hooks/exhaustive-deps -- `id` là thứ kích hoạt, không phải thứ đọc
  const maPhien = useMemo(() => maPhienMoi(), [id]);
  const ghiLuot = useCallback((e, phase = 'practice') => {
    soLuot.current += 1;
    /* ⚠ `sauPhuDao` KHÔNG đặt ở đây, dù đây trông như chỗ hợp lý nhất. Cờ ấy do
       `LuyenTap` đặt, vì chỉ nó biết nút nào vừa đi qua một lượt phụ đạo — và
       `LuyenTap` là một component KHÁC trong cùng tệp này. Bản đầu tôi viết ở đây
       và đọc `daPhuDao.current`: bản dựng xanh, 109 cổng xanh, và bé thấy MÀN
       TRẮNG, vì biến ấy không tồn tại trong phạm vi của `BaiHoc`. Đúng lớp lỗi đã
       hai lần lên tới bản thật. */
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
        /* ⚠ PHẢI TRUYỀN QUYỂN. Gọi trần thì mặc định `ta1`, và nó chạy song song
           với lời gọi của `ManTiengAnh` — lời nào xong sau thì thắng, nên bé học
           lớp 3·4·5 có thể nhận sổ âm của lớp 1 và MẤT HẾT nút nghe. Xem ghi chú
           dài ở `napSoAm`. */
        await napSoAm(quyenCua(id));
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

  /* Gán TRẦN, không phải hook — chạy mỗi lần vẽ nên `changCuoi` luôn giữ đúng chặng
     bé đang đứng. Ô nhớ đã khai tít trên đầu hàm cùng `moLuc`/`daXong`/`soLuot`. */
  changCuoi.current = k;

  return (
    <Khung onThoat={onThoat} ten={bai.title}>
      <ThanhChang ten={tenChang} ds={CHANG} tai={tai} xa={xa} onChon={nhay} />

      {/* `key` gắn mã bài: đổi bài thì ba màn dưới đây phải dựng lại từ đầu, không
          thì mốc của bài cũ dính sang bài mới. */}
      {k === 'tu' && (
        <ManTu key={id} bai={bai} onTiep={xong} onNoi={onNoi}
               moc={mocDau?.tu} onMoc={mocTu} onLuot={ghiLuot} />
      )}
      {k === 'cau' && (
        <ManCau key={id} bai={bai} onTiep={xong}
                moc={mocDau?.cau} onMoc={mocCau} onLuot={ghiLuot} />
      )}
      {k === 'luyen' && (
        <LuyenTap key={id} bai={bai} onTiep={xong}
                  moc={mocDau?.luyen} onMoc={mocLuyen} onLuot={ghiLuot}
                  mucThao={mucThao} hoSoDang={hoSoDang}
                  tienDo={tienDo} tenBe={tenBe} onPhuDao={onPhuDao} />
      )}
      {k === 'noi' && (
        <HoiThoai
          hoiThoai={bai.knowledgeCore.hoiThoai}
          tenBe={tenBe}
          onXong={(kq) => { onNoi?.('hoiThoai', kq); xong(); }}
        />
      )}
      {k === 'sat' && (
        <SatHach bai={bai}
                 onXong={(kq) => { daXong.current = true; onXongBai(kq, hangXom(id).sau); }}
                 onLuot={(e) => ghiLuot(e, 'assess')} />
      )}
      {k === 'phong' && (
        <PhongNoi bai={bai} tienDo={tienDo} tenBe={tenBe}
                  soThich={soThich} onSoThich={onSoThich} mucThao={mucThao}
                  onLuot={ghiLuot} onHoSoAI={onHoSoAI} />
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
function ManTu({ bai, onTiep, onNoi, moc, onMoc, onLuot = null }) {
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
  const dsTu = useMemo(() => bai.knowledgeCore.vocabulary || [], [bai]);
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
  /* ── LƯỢT NÓI VÀO ENGINE (bác chốt 23-08-2026) ──
     Trước bản này, phần NÓI là kỹ năng duy nhất nằm ngoài BKT: có chấm điểm từng
     lượt, nhưng điểm ấy chỉ nằm trong `moc.soNoi` tại máy và `luuBai` cố ý không
     đẩy `moc` lên. Nên "con phát âm thế nào" không có bằng chứng nào trên máy chủ.

     ⚠ CHỈ GHI KHI MÁY NGHE RA CHỮ (`coTieng`). Bé bấm nút rồi ngồi im thì đó là
     CHƯA NÓI, không phải nói sai — ghi thành một lượt sai là mức thạo tụt vì một
     việc bé chưa từng làm. Cùng chốt mà `ghiNoi` đã dùng cho `soNoi`.

     ⚠ `phase: 'practice'` chứ không đặt pha mới: luật Firestore chỉ nhận bốn pha,
     thêm pha thứ năm là phải sửa luật rồi deploy trước. Phân biệt "nói" với các
     dạng khác bằng `mode` — đó đúng là việc của trường ấy, và bảng cô giáo lọc
     theo `mode` được ngay. */
  const ghiNoi = useCallback((tu, kq) => {
    if (kq?.coTieng) {
      const nut = (bai.knowledgeCore.vocabulary || []).find((x) => x.tu === tu);
      onLuot?.({
        cau: { id: `noi:${tu}`, maNut: nut?.ma || null, format: 'noiTu' },
        ok: (kq.diem ?? 0) >= DAT_NOI,
        lan: kq.lan ?? 1,
        ms: null,
        hintsUsed: 0,
        answer: kq.nghe ?? null,
        expected: tu,
        phase: 'practice',
      });
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
    /* ── ⚠ PHẢI PHỤ THUỘC VÀO `bai`, không chỉ `onNoi` ──
       `BaiHoc` KHÔNG dựng lại khi đổi bài (chỗ gọi không đặt `key` — xem chú thích
       ở `maPhien`), nên `bai` đổi mà component vẫn sống. Với mảng phụ thuộc cũ
       `[onNoi]`, bao đóng giữ vốn từ của bài TRƯỚC: bé nói một từ của bài mới thì
       `find` không thấy, `maNut` thành `null`, và lượt ấy rơi ra ngoài BKT trong im
       lặng. Cùng lớp lỗi với `ghiNoi` của chặng Mẫu câu bên dưới. */
  }, [bai.knowledgeCore.vocabulary, onLuot, onNoi]);

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
        daNgheTu={daNghe.has(dsTuCoHinh[iTu]?.tu)}
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
function LuyenTu({ bai, ds, i, onDoi, soNoi, micHong, daNgheTu = false,
                   onNoi, onNghe, onMicHong }) {
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

      {/* ── ĐƯỜNG LUI TỰ KHAI, KHÔNG PHẢI CHỜ HỎNG ──
          `micHong` xưa nay CHỈ bật khi micro hỏng THẬT — tức bé phải bấm nói rồi
          thất bại mới được đi tiếp. Nhưng bé KHÔNG CÓ micro, bé không được phép
          dùng micro, bé đang ở chỗ đông người, hay bé ngọng chưa dám nói, thì
          không có cái hỏng nào để mà bắt: chặng Từ mới khoá luôn, và ba chặng sau
          khoá theo. Đi thử bản chạy 23-08 đứng đúng ở đây — không tới được Luyện
          tập nên không sinh nổi một bản ghi BKT nào (lỗ thủng P2).

          Nên mở một lối TỰ KHAI. Chỉ hiện SAU KHI bé đã bấm nghe: phần nghe mới là
          thứ chặng này thật sự dạy, bỏ cả nghe thì không còn gì để bỏ. */}
      {daNgheTu && !micHong && (
        <button type="button" onClick={onMicHong}
          className="self-start rounded-xl2 px-2 py-1 text-sm text-mute underline
            hover:text-navy focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Con chưa nói được — cho con đi tiếp nhé
        </button>
      )}

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
function ManCau({ bai, onTiep, moc, onMoc, onLuot = null }) {
  /* `useMemo` để DANH TÍNH ổn định: không có nó thì mảng mới mỗi lần vẽ, và mọi
     mảng phụ thuộc chứa nó đều đổi mỗi lần vẽ — tức mất tác dụng, mà vẫn trông như
     có. */
  const ds = useMemo(() => bai.video?.cau || [], [bai]);
  const [i, datI] = useState(() => Math.max(0, Number(moc?.i) || 0));
  const [daXem, datDaXem] = useState(() => new Set(moc?.daXem || []));
  const [hong, datHong] = useState(false);
  const [soNoi, datSoNoi] = useState(() => ({ ...(moc?.soNoi || {}) }));
  const [micHong, datMicHong] = useState(false);
  /* Câu nào bé đã bấm NGHE. Chỉ dùng để mở đường lui tự khai — xem chú ở dưới. */
  const [daNgheCau, datDaNgheCau] = useState(() => new Set());
  const mcDs = useMemo(() => bai.knowledgeCore.mauCauDs || [], [bai]);
  const mc = mcDs[i] || bai.knowledgeCore.mauCau;
  const bay = bai.knowledgeCore.misconceptions?.[0];

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
    /* Cùng luật với chặng 1 — xem chú thích ở `LuyenTu`. Nút ở đây là MẪU CÂU
       (`sp_*`): bé nói cả câu thì cái được kiểm là cấu trúc, không phải một từ. */
    if (!kq?.coTieng) return;
    onLuot?.({
      cau: { id: `noi:${cau}`, maNut: (ds[i] && mcDs[i]?.ma) || null, format: 'noiCau' },
      ok: (kq.diem ?? 0) >= DAT_NOI,
      lan: kq.lan ?? 1,
      ms: null,
      hintsUsed: 0,
      answer: kq.nghe ?? null,
      expected: cau,
      phase: 'practice',
    });
    datSoNoi((s) => {
      const cu = s[cau] || { caoNhat: null, lan: 0 };
      return { ...s, [cau]: { caoNhat: Math.max(cu.caoNhat ?? 0, kq.diem ?? 0), lan: cu.lan + 1 } };
    });
    /* ── ⚠ MẢNG PHỤ THUỘC NÀY TỪNG RỖNG, VÀ ĐÓ LÀ MỘT LỖI THẬT ──
       Thân hàm đọc `ds[i]` và `mcDs[i]`, mà `i` là state đổi mỗi lần bé chọn câu
       khác (`datI` ở thanh chọn câu). Với `[]`, bao đóng giữ NGUYÊN `i` của lần vẽ
       đầu — nên bé nói câu thứ ba thì lượt được ghi vào `maNut` của câu thứ NHẤT.
       Sai ở đúng chỗ tệ nhất: `bktUnit` của bản ghi lượt, tức BKT cộng công cho
       nhầm nút, rồi mức thạo · phụ đạo · cả thang phạm vi đều dựng trên số sai.
       Không màn nào đổi màu, không cổng nào đỏ. ESLint `exhaustive-deps` tìm ra
       10-10-2026. */
  }, [ds, i, mcDs, onLuot]);

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
          onNghe={() => datDaNgheCau((s) => new Set(s).add(cauNay))}
          onXong={(k) => ghiNoi(cauNay, k)}
          onHong={() => datMicHong(true)}
        />
      )}

      {/* ── ĐƯỜNG LUI TỰ KHAI — Y HỆT CHẶNG TỪ MỚI, VÀ ĐÓ LÀ ĐIỂM CHÍNH ──
          Bản vá 23-08 chỉ mở lối này ở chặng Từ mới, nên đi thử bản chạy lại đứng
          đúng ở ĐÂY: qua được chặng 1 rồi tắc chặng 2, mà bốn chặng sau khoá theo
          chặng 2. Vá một nửa một hàng rào thì hàng rào vẫn kín.

          Nên hễ chặng nào ĐÒI NÓI thì chặng ấy phải có lối tự khai. Cổng
          `tienganh_vao_engine` nay đếm số chặng đòi nói và đòi đủ chừng ấy lối. */}
      {daNgheCau.has(cauNay) && !micHong && (
        <button type="button" onClick={() => datMicHong(true)}
          className="self-start rounded-xl2 px-2 py-1 text-sm text-mute underline
            hover:text-navy focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Con chưa nói được — cho con đi tiếp nhé
        </button>
      )}

      {micHong && (
        <p className="rounded-xl2 bg-gold-pale p-2 text-sm text-gold-dark">
          Máy chưa nghe được nên phần nói để lúc khác — con cứ bấm 🔈 nghe rồi
          đọc theo, xong bấm “Mẫu sau” nhé.
        </p>
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

/**
 * MỘT LẦN PHỤ ĐẠO CHO MỖI LẦN MỞ BÀI — và con số 1 là có căn cứ.
 *
 * `viecTiepCuaNut` trả PHỤ ĐẠO ở HAI điều kiện: sai ba lần liên tiếp, HOẶC mức
 * tinh thông tụt dưới ngưỡng yếu (Thuật toán 3.9 dòng 1 và dòng 4). Điều kiện thứ
 * hai đúng ngay từ câu sai ĐẦU TIÊN ở một nút bé còn yếu — nên một bài mười nút có
 * thể mời tới mười lần nếu không chặn. Với bé đang chật vật thì mười lời mời "mình
 * gỡ chỗ này nhé" không phải mười lần giúp, mà là mười lần bị nhắc rằng mình sai.
 *
 * Chọn 1 chứ không phải 2: bài phụ đạo là chỗ gỡ GIỮA mạch học, và mạch học của bé
 * sáu tuổi không chịu được hai lần rẽ ngang trong một bài. Bé mắc ở nhiều nút thì
 * lần mở bài sau sẽ gỡ nút tiếp theo — `daMoi` đặt lại theo từng lần mở bài, vì
 * `LuyenTap` mang `key={id}` nên đổi bài là dựng lại từ đầu.
 */
const PHU_DAO_MOI_BAI = 1;

/* Nhãn vai của mẫu câu — HẰNG, nên để ngoài component: dựng lại mỗi lần vẽ thì
   mọi `useMemo` phụ thuộc vào nó đều mất tác dụng. */
const NHAN = { hoi: 'Câu hỏi', dap: 'Câu trả lời', cau: 'Mẫu câu' };

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
                    hoSoDang = null, tienDo = null, tenBe = 'Bo', onPhuDao = null }) {
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

  /* ══════════ NHÁNH PHỤ ĐẠO CỦA HÀM CHÍNH SÁCH (mục 2.5.1 · 3.4.7) ══════════
   *
   * ── VÌ SAO ĐẾM TẠI MÁY CHỨ KHÔNG ĐỌC `mastery.saiLienTiep` ──
   * `mastery` do hàm nền ghi, mà hàm nền chạy SAU khi bản ghi lên tới máy chủ —
   * mục 3.1.3 nói thẳng là giữa bước 3 và bước 4 có độ trễ. Đọc con số ấy thì lúc
   * bé sai câu thứ ba, hệ thống còn đang thấy số 0 hoặc 1. Nên chuỗi sai liên tiếp
   * — thứ mục 3.4.7 gọi là "tín hiệu tức thời" — phải đếm ngay tại đây.
   *
   * ── ĐẾM THEO LƯỢT, KHÔNG THEO CÂU ──
   * Bảng 3.12 định nghĩa `S_c` là số lần sai LIÊN TIẾP, và `applyAttempt` đặt lại
   * về 0 ngay khi có một lượt đúng. Đếm theo câu thì một câu bé sai bốn lần rồi
   * đúng chỉ tính là một — mất đúng tín hiệu cần đo.
   */
  const demSai = useRef(new Map());        // maNut → số lần sai liên tiếp
  const cauDaLam = useRef(new Map());      // maNut → [mã câu đã trả lời]
  const choPhuDao = useRef(null);          // nút đang chờ mời, xét lúc xong câu
  /* Nút nào đã ĐI QUA một lượt phụ đạo trong phiên này. Mọi lượt sau đó tại nút ấy
     là lượt SAU CAN THIỆP, và chỉ số NG09 phải tách chúng ra — xem `thongke.js`.
     Giữ theo NÚT chứ không theo cả phiên: bé phụ đạo nút A rồi làm câu của nút B
     thì lượt ở B vẫn là lượt tự gỡ. */
  const daPhuDao = useRef(new Set());
  const daMoi = useRef(new Set());         // nút đã mời rồi trong bài này
  const [moiPhuDao, datMoiPhuDao] = useState(null);
  const mocPhuDao = useRef(0);

  /**
   * ⚠ MỖI NÚT CHỈ MỜI MỘT LẦN TRONG MỘT BÀI.
   *
   * Không có chốt này thì bé sai ba câu, làm phụ đạo, quay lại sai tiếp ba câu, và
   * bị mời lần nữa — thành một vòng không lối ra đúng lúc bé đang nản nhất. Ràng
   * buộc R2 cấm chính hình dạng ấy. Sai tiếp sau khi đã gỡ một lần thì thứ bé cần
   * là người lớn ngồi cạnh, không phải vòng phụ đạo thứ hai.
   */
  const ghiLuotLuyen = useCallback((e) => {
    const nut = e?.cau?.maNut;
    /* ── `sauPhuDao` — ĐẶT Ở ĐÂY, và chỉ ở đây ──
       Lượt này có nằm sau một can thiệp tại CHÍNH nút ấy không. Phải khai lúc ghi:
       khung phụ đạo nằm ở học bạ, kho KHÁC với nhật ký lượt, nên không ai suy
       ngược ra được. Chỉ `LuyenTap` biết điều này — `BaiHoc` ở ngoài không thấy
       `daPhuDao`, và viết ở đó là màn trắng (xem chú thích tại `ghiLuot`). */
    onLuot?.({ ...e, sauPhuDao: !!(nut && daPhuDao.current.has(nut)) });
    if (!nut) return;
    const ds = cauDaLam.current.get(nut) || [];
    if (e?.cau?.id && !ds.includes(e.cau.id)) cauDaLam.current.set(nut, [...ds, e.cau.id]);
    if (e.ok) { demSai.current.set(nut, 0); return; }
    const n = (demSai.current.get(nut) || 0) + 1;
    demSai.current.set(nut, n);

    /* ⚠ HỎI CHÍNH HÀM CHÍNH SÁCH, đừng so tay với hằng số.
       `viecTiepCuaNut` là Thuật toán 3.9 — nó xét chuỗi sai liên tiếp TRƯỚC mức
       tinh thông, và còn bắt cả nhánh "p tụt dưới ngưỡng yếu" mà một phép so
       `n >= 3` gõ tay ở đây sẽ bỏ sót. Gõ lại luật ở màn hình là dựng một bản thứ
       hai của cùng một chính sách, rồi hai bản trôi xa nhau mà không gì báo. */
    /* Truyền mã NÚT — nấc hẹp nhất của thang phạm vi (mục 3.8.1). Môn và khối lớp
       đã nằm trong ngữ cảnh phiên, đặt lúc bé mở quyển. */
    const viec = viecTiepCuaNut({ p: mucThaoCua(mucThao, nut), saiLienTiep: n }, { nut });
    if (viec.viec === VIEC.phuDao && !daMoi.current.has(nut) && !choPhuDao.current
        && daMoi.current.size < PHU_DAO_MOI_BAI) {
      choPhuDao.current = nut;
    }
  }, [onLuot, mucThao]);

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
    /* Qua BẢNG TRẠNG THÁI (việc V6), không gọi `xepTheoZPD` trực tiếp: một nguồn
       sự thật về bé cho cả bốn màn. `dungBang` thuần và rẻ, nên gọi nó để lấy
       đúng một trường là chuyện không tốn gì. */
    () => dungBang({
      cauDs: bai.practice.pools[MUC[m].khoa] || [], mucThao, dinhDang: hoSoDang,
    }).nhomZPD || [],
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

    /* ⚠ MỜI PHỤ ĐẠO KHI CÂU HIỆN TẠI ĐÃ XONG, không phải ngay lúc chạm ngưỡng.
       Chạm ngưỡng là lúc bé vừa sai lần thứ ba và màn hình đang bày đáp án cùng nút
       "để lại sau". Đổi màn ngay lúc ấy là giật mất câu đang dở khỏi tay bé. */
    const cho = choPhuDao.current;
    choPhuDao.current = null;
    if (cho) {
      daMoi.current.add(cho);
      mocPhuDao.current = Date.now();
      /* Từ đây mọi lượt tại nút ấy là lượt SAU CAN THIỆP. Đánh dấu ở chỗ MỜI chứ
         không ở chỗ bé bấm "làm" — bé từ chối lời mời thì vẫn đã được chỉ ra chỗ
         mắc và bày đáp án, tức can thiệp đã xảy ra một phần. Thà đánh dấu rộng
         hơn thực tế còn hơn để lượt sau can thiệp lẫn vào lượt tự gỡ: lẫn vào thì
         chuyên gia đọc chỉ số NG09 sai theo hướng không ai nhận ra. */
      daPhuDao.current.add(cho);
    }

    if (i + 1 < pool.length) { datI(i + 1); if (cho) datMoiPhuDao(cho); return; }
    /* Hết lượt. Còn câu nợ mà chưa làm lại lượt nào thì mời làm lại. */
    if (!lamLai && no.length + (kq.boQua ? 1 : 0) > 0) {
      datMoiLamLai(true); if (cho) datMoiPhuDao(cho); return;
    }
    if (m + 1 < MUC.length) { sangMuc(m + 1); if (cho) datMoiPhuDao(cho); return; }
    /* Hết cả chặng thì đi tiếp — KHÔNG giữ bé lại để phụ đạo. Phụ đạo là chỗ gỡ
       giữa mạch học, không phải một cửa ải cắm ở lối ra. */
    onTiep();
  };

  /**
   * XONG MỘT LƯỢT PHỤ ĐẠO — trả bé về đúng chỗ cũ, và ghi lại KHUNG A-R-A.
   *
   * ⚠ KHÔNG ghi mức tinh thông trước/sau vào đây. Máy con chỉ có bản `mucThao` nạp
   * lúc mở bài, mà hàm nền thì cập nhật sau một quãng trễ (mục 3.1.3) — con số đọc
   * được lúc này là con số CŨ, ghi vào là ΔC sai theo hướng không ai lần ra.
   *
   * Thay vào đó ghi KHUNG: nút mắc · nút gốc rễ · các câu đã hỏi TRƯỚC · các câu
   * của bài phụ đạo · hai mốc thời gian. Mức tinh thông ở hai lần đo thì dựng lại
   * được từ chính nhật ký `attempts` bằng phép chạy lại của
   * `tools/danh_gia_mo_hinh.mjs`. Đó là cả lý do kho lưu vết là bất biến: thứ gì
   * suy được từ nhật ký thì đừng chép thêm một bản (mục 3.2.4).
   */
  const xongPhuDao = (r) => {
    onPhuDao?.({
      microId: bai.id,
      maNutMac: moiPhuDao,
      nutGoc: r?.nutGoc || null,
      lam: !!r?.lam,
      viSao: r?.viSao || null,
      soCau: r?.soCau ?? 0,
      dung: r?.dung ?? 0,
      itemTruoc: cauDaLam.current.get(moiPhuDao) || [],
      itemPhuDao: r?.itemIds || [],
      nguon: r?.nguon || null,
      luiVe: !!r?.luiVe,
      tsBatDau: mocPhuDao.current || null,
      tsKetThuc: Date.now(),
    });
    /* Đặt lại bộ đếm của nút ấy: bé vừa được gỡ, chuỗi sai cũ không còn là tín hiệu
       về trạng thái HIỆN TẠI nữa — đúng lý do `applyAttempt` đặt lại về 0 khi có
       một lượt đúng. */
    demSai.current.set(moiPhuDao, 0);
    datMoiPhuDao(null);
  };

  /* ⚠ PHỤ ĐẠO XÉT TRƯỚC MỌI NHÁNH KHÁC — cùng thứ tự với Thuật toán 3.9 dòng 9,
     nơi nhánh phụ đạo thắng nhánh vượt ải. Bé đang mắc thì việc cần làm là gỡ, chứ
     không phải mời làm lại mấy câu nợ hay đẩy sang mức sau. */
  if (moiPhuDao) {
    return (
      <PhuDao baiNay={bai} maNutMac={moiPhuDao} mucThao={mucThao} tienDo={tienDo}
              tenBe={tenBe} onLuot={onLuot} onXong={xongPhuDao} />
    );
  }

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
        <CauHoi key={cau.id} cau={cau} onXong={xong} onLuot={ghiLuotLuyen} />
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
                   + `làm ${thuToiThieu()} lần thì bài sau cũng mở ra.`}
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
