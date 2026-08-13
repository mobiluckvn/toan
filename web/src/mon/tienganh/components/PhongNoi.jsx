import React, { useCallback, useEffect, useRef, useState } from 'react';
import HinhVe from './HinhVe.jsx';
import { hinhCuaTu, napBai, maBaiTruoc } from '../lib/noiDung.js';
import {
  vonTu, tuTrongCau, tachTheoTieng, UNIT_CU_TOI_DA,
  tinhBuoi, loiKet, cauHoiSoThich, PHUT_TOI_DA,
} from '../lib/phongnoi.js';
import { hoiCoGiao, luuBuoi } from '../lib/goiPhongNoi.js';
import { auth } from '../../../chung/lib/nenTang.js';
import { doc as docLen, docDoan, docDuoc, coGiong, thoiDoc } from '../lib/doclen.js';
import { batDauNghe, ngheDuoc, loiDocDuoc, xinMicroChiTiet, MICRO, TIENG } from '../lib/nghenoi.js';
import { chamTot, chamCau, datNoi, loiKhen } from '../lib/chamnoi.js';

/**
 * PHÒNG LUYỆN NÓI — bé nói chuyện với cô giáo máy, trong đúng vốn từ của unit.
 *
 * ── KHÁC CHẶNG "NÓI CHUYỆN" Ở CHỖ NÀO ──
 * Chặng ấy đi theo kịch bản viết sẵn: bé biết trước phải nói gì, và hết kịch bản là
 * hết. Ở đây câu do máy sinh, nên bé hỏi lại được, nói sai thì cô nói theo cách
 * khác, và không bao giờ hết câu. Đó mới là chỗ tập DÙNG tiếng Anh.
 *
 * ── BA THỨ BÉ LỚP 1 CẦN, VÀ CẢ BA ĐỀU KHÔNG PHẢI CHỮ ──
 *  1. NGHE ĐƯỢC. Câu tiếng Anh đọc giọng en-GB, lời tiếng Việt giọng vi-VN, và đọc
 *     TỰ ĐỘNG ngay khi cô trả lời — bé chưa đọc chữ thì chờ bé bấm là chờ mãi.
 *  2. NHÌN THẤY NGHĨA. Cô nói tới từ nào thì hiện hình từ ấy (bác dặn 13-08). Không
 *     có hình thì phòng này quay về thành một khối chữ.
 *  3. MỘT NÚT DUY NHẤT để nói. Không menu, không lựa chọn.
 *
 * ── KHÔNG ĐỂ BÉ KẸT ──
 * Máy không nghe được, không đọc được, hoặc mạng hỏng — cả ba đều nói THẲNG ra và
 * vẫn cho bé ở lại phòng nghe cô nói. Đây là chỗ luyện thêm, không phải cửa ải.
 */
export default function PhongNoi({ bai, tienDo, tenBe = 'con', lop = 1 }) {
  const daDat = !!tienDo?.micros?.[bai?.id]?.pass;
  const [baiCu, datBaiCu] = useState([]);

  /* Nạp các unit trước CHỈ khi bé đã đạt unit này — chưa đạt thì vốn từ bó trong
     unit ấy, nạp thêm là tải mấy tệp chẳng dùng tới. */
  useEffect(() => {
    let song = true;
    if (!daDat || !bai?.id) { datBaiCu([]); return () => { song = false; }; }
    (async () => {
      const ds = maBaiTruoc(bai.id, UNIT_CU_TOI_DA);
      const d = await Promise.all(ds.map((x) => napBai(x).catch(() => null)));
      if (song) datBaiCu(d.filter(Boolean));
    })();
    return () => { song = false; };
  }, [bai?.id, daDat]);

  const datCu = useCallback((id) => !!tienDo?.micros?.[id]?.pass, [tienDo]);
  const von = React.useMemo(
    () => vonTu({ baiNay: bai, baiCu, daDat, datCu }),
    [bai, baiCu, daDat, datCu],
  );

  /* Mỗi lần mở phòng của một unit là MỘT buổi. Mã buổi dựng một lần rồi giữ nguyên,
     để mọi lượt của buổi ấy ghi đè lên cùng một tài liệu chứ không rải ra. */
  const maBuoi = useRef(null);
  if (!maBuoi.current && bai?.id) {
    maBuoi.current = `${String(bai.id).replace(/[:.]/g, '_')}__${Date.now()}`;
  }
  const [lichSu, datLichSu] = useState([]);
  const [dangHoi, datDangHoi] = useState(false);
  const [dangNghe, datDangNghe] = useState(false);
  const [tam, datTam] = useState('');
  const [loi, datLoi] = useState(null);
  const [micHong, datMicHong] = useState(false);
  const [thich, datThich] = useState(null);
  const batDau = useRef(Date.now());
  /* `nhip` KHÔNG mang giá trị nào — nó chỉ để bắt màn hình vẽ lại mỗi 30 giây, để
     đồng hồ 20 phút tự tới nơi. Bản đầu viết `Date.now() + nhip * 0`: chạy đúng,
     nhưng nhân 0 thì ai đọc cũng tưởng lỗi rồi xoá đi, và xoá là đồng hồ chết. */
  const [, datNhip] = useState(0);
  const dauDs = useRef(null);
  const phien = useRef(null);
  const daChao = useRef(false);

  const cauCoVuaNoi = [...lichSu].reverse().find((x) => x.vai === 'may')?.en || '';
  const buoi = tinhBuoi({ lichSu, batDau: batDau.current, bayGio: Date.now() });
  const ket = loiKet(buoi);
  const hoiThich = cauHoiSoThich(von);

  useEffect(() => () => { phien.current?.huy(); thoiDoc(); }, []);
  /* Nhịp 30 giây chỉ để VẼ LẠI, không đụng gì tới dữ liệu — hết 20 phút mà màn
     hình không tự biết thì bé cứ nói tiếp, rồi đúng lượt sau mới bị cắt ngang. */
  useEffect(() => { const id = setInterval(() => datNhip((n) => n + 1), 30000); return () => clearInterval(id); }, []);
  /* Có lượt mới thì đưa ĐẦU danh sách vào tầm mắt — tin mới nằm trên cùng. Bản
     trước cuộn xuống đáy, nay làm thế là chạy ngược hướng và bé mất dấu câu vừa
     nói. */
  useEffect(() => { dauDs.current?.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }, [lichSu, dangHoi]);

  /* Gửi một lượt lên cô giáo. `themVaoLichSu` nhận lịch sử ĐÃ có lượt của bé —
     đọc state ngay tại đây thì lượt vừa thêm chưa kịp vào, và cô trả lời câu cũ. */
  const guiLuot = useCallback(async (ds) => {
    datLoi(null); datDangHoi(true);
    try {
      const tra = await hoiCoGiao({ von, lichSu: ds, tenBe, lop,
        haDoKho: buoi.haDoKho, hoSo: { thich } });
      const luot = { vai: 'may', chu: tra.en || tra.vi, en: tra.en, vi: tra.vi };
      const sau = [...ds, luot];
      datLichSu(sau);
      /* Client giữ ngữ cảnh và tự đẩy lên máy chủ — bác chốt như thế; server không
         lưu gì. KHÔNG chờ: mất mạng thì bé vẫn nói chuyện bình thường. */
      luuBuoi(auth?.currentUser?.uid, {
        maBuoi: maBuoi.current, quyen: 'ta1', baiId: bai?.id, tenBai: bai?.title, lichSu: sau,
      });
      /* Câu tiếng Anh đọc nguyên khối giọng en-GB; lời giải thích thì TÁCH theo
         thứ tiếng — trong đó thường có lẫn chính từ bé đang học. */
      (async () => {
        thoiDoc();
        if (tra.en) await docLen(tra.en, 'en-GB', { nhanh: 0.9 });
        await docDoan(tachTheoTieng(tra.vi, von));
      })();
    } catch (e) {
      /* Nói đúng chỗ hỏng. "Có lỗi xảy ra" là câu vô dụng nhất — bố mẹ không biết
         phải sửa gì, mà mấy lỗi ở đây thì mỗi lỗi một cách chữa hẳn. */
      datLoi(e?.code === 'functions/permission-denied'
        ? 'Khoá của cô giáo máy chưa dùng được — người lớn kiểm tra giúp con nhé.'
        : e?.code === 'functions/unauthenticated'
          ? 'Con đăng nhập rồi mới vào phòng này được nhé.'
          : 'Cô giáo máy chưa trả lời được. Con thử lại nhé.');
    } finally { datDangHoi(false); }
  }, [von, tenBe, lop, bai, buoi.haDoKho, thich]);

  /* Cô chào trước. Bé 6 tuổi mở ra thấy màn trắng thì không biết làm gì cả. */
  useEffect(() => {
    if (daChao.current || !bai) return;
    daChao.current = true;
    guiLuot([{ vai: 'be', chu: 'Chào cô, con muốn tập nói.' }]);
  }, [bai, guiLuot]);

  const noi = useCallback(async () => {
    if (dangNghe) { phien.current?.dung(); return; }
    datLoi(null); datTam('');
    const cho = await xinMicroChiTiet();
    if (cho !== MICRO.duoc) { datMicHong(true); datLoi(loiDocDuoc(cho)); return; }
    thoiDoc();                       // đang đọc mà bật micro thì máy nghe lại chính nó
    datDangNghe(true);
    const p = batDauNghe({ onTam: datTam, tieng: TIENG });
    phien.current = p;
    try {
      const { chu, phuongAn } = await p.xong;
      const noiGi = (chu || '').trim();
      if (!noiGi) { datLoi('Cô chưa nghe thấy gì. Con nói to hơn một chút nhé.'); return; }
      /* Chấm khi bé đang NHẠI LẠI câu cô vừa nói. Bé nói câu khác thì không chấm —
         chấm một câu bé tự nghĩ ra theo mẫu của câu khác là chấm sai. */
      const kq = cauCoVuaNoi ? chamTot(chamCau, cauCoVuaNoi, phuongAn?.length ? phuongAn : [noiGi]) : null;
      const sau = [...lichSu, { vai: 'be', chu: noiGi, diem: kq?.diem ?? null }];
      datLichSu(sau);
      /* Lượt này vừa KẾT THÚC buổi thì đừng hỏi cô nữa: bé đã xong, mà gọi thêm
         một lượt là hoặc cô nói chen vào sau lời khen, hoặc mạng trục trặc và bé
         thấy dòng lỗi đỏ ngay dưới câu "con giỏi lắm". Đã thấy thật lúc đi thử. */
      const sauKhiNoi = tinhBuoi({ lichSu: sau, batDau: batDau.current, bayGio: Date.now() });
      if (sauKhiNoi.trangThai !== 'dang') { datLoi(null); return; }
      guiLuot(sau);
    } catch (e) {
      datMicHong(true);
      datLoi(e?.message || loiDocDuoc(e?.ma));
    } finally { datDangNghe(false); phien.current = null; }
  }, [dangNghe, lichSu, cauCoVuaNoi, guiLuot]);

  const dsTu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];

  return (
    <section className="flex flex-col gap-3">
      {/* VỐN TỪ HÔM NAY — bé nhìn vào là biết phòng này nói về những gì. Bấm vào
          một hình là nghe từ ấy, để bé bắt chuyện được mà không cần ai gợi. */}
      <div className="rounded-xl2 border-2 border-line bg-white p-3">
        <div className="flex flex-wrap items-baseline gap-x-3">
          <h3 className="text-sm font-bold uppercase tracking-wide text-navy">Con nói về</h3>
          {/* Còn bao lâu — cho bố mẹ, và để hết giờ không cắt ngang đột ngột. Chỉ
              hiện khi sắp hết: đếm ngược suốt buổi chỉ làm bé nhìn đồng hồ thay vì
              nhìn bài. */}
          {buoi.trangThai === 'dang' && buoi.phutConLai <= 5 && (
            <span className="rounded-full bg-gold-pale px-2 py-0.5 text-xs font-bold text-gold-dark">
              còn {Math.ceil(buoi.phutConLai)} phút
            </span>
          )}
          <p className="text-sm text-mute">
            {von.moRong
              ? `${dsTu.length} từ — có cả từ mấy bài trước con đã học`
              : `${dsTu.length} từ của bài này`}
          </p>
        </div>
        <ul className="mt-2 flex flex-wrap gap-2">
          {dsTu.map((t) => (
            <li key={t.tu}>
              <button type="button" onClick={() => docLen(t.tu, 'en-GB', { nhanh: 0.9 })}
                aria-label={`Nghe từ ${t.tu} — ${t.nghia}`}
                className="flex w-[4.5rem] flex-col items-center gap-0.5 rounded-xl2 border-2
                  border-line bg-soft p-2 transition hover:brightness-95
                  focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
                <span className="text-3xl leading-none"><HinhVe ten={t.tu} {...hinhCuaTu(bai, t.tu)} /></span>
                <span className="text-[0.7rem] font-semibold leading-tight text-ink">{t.tu}</span>
              </button>
            </li>
          ))}
        </ul>
      </div>

      {!docDuoc() && (
        <p className="rounded-xl2 bg-gold-pale p-3 text-sm text-gold-dark">
          Máy này chưa đọc thành tiếng được. Con vẫn nói chuyện được, nhưng phải nhờ
          bố mẹ đọc hộ câu tiếng Anh.
        </p>
      )}
      {docDuoc() && !coGiong('en-GB') && (
        <p className="rounded-xl2 bg-gold-pale p-3 text-sm text-gold-dark">
          Máy chưa có giọng tiếng Anh — câu tiếng Anh sẽ đọc bằng giọng máy sẵn có,
          nghe hơi lạ. Người lớn cài thêm giọng tiếng Anh giúp con nhé.
        </p>
      )}

      {/* HỎI BÉ THÍCH GÌ — hỏi MỘT LẦN, bằng hình, trước khi vào nói chuyện.
          Bé bấm vào hình chứ không gõ và không nói tự do: bé 6 tuổi không gõ được,
          mà nói tự do thì bộ nhận dạng nghe ra gì cũng được. Câu trả lời rơi đúng
          vào vốn từ của bài nên không có từ lạ nào lọt vào phòng, và KHÔNG có
          thông tin riêng tư nào mới rời khỏi máy — chỉ là một từ trong sách. */}
      {!thich && hoiThich && buoi.trangThai === 'dang' && (
        <div className="rounded-xl2 border-2 border-gold bg-gold-pale p-4">
          <p className="text-lg font-bold text-navy">{hoiThich.hoi}</p>
          <p className="text-sm text-gold-dark">Con chọn một cái, rồi mình sẽ tập nói về nó.</p>
          <ul className="mt-2 flex flex-wrap gap-2">
            {hoiThich.chon.map((t) => (
              <li key={t.tu}>
                <button type="button" onClick={() => datThich(t.tu)}
                  aria-label={`Con thích ${t.nghia} (${t.tu})`}
                  className="flex w-[5rem] flex-col items-center gap-0.5 rounded-xl2 border-2
                    border-line bg-white p-2 transition hover:brightness-95
                    focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
                  <span className="text-4xl leading-none"><HinhVe ten={t.tu} {...hinhCuaTu(bai, t.tu)} /></span>
                  <span className="text-[0.7rem] font-semibold text-ink">{t.nghia}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* MÀN KẾT — bé phải thấy vạch đích. Một việc không có chỗ kết thì bé không
          bao giờ thấy mình LÀM ĐƯỢC, mà đó mới là thứ giữ bé quay lại. */}
      {ket && (
        <div className={`rounded-xl2 p-5 ${buoi.trangThai === 'xongGioi' ? 'bg-teal-pale' : 'bg-gold-pale'}`}>
          <p className="text-4xl" aria-hidden="true">{ket.bieuTuong}</p>
          <p className="mt-1 text-2xl font-bold text-ink">{ket.tieuDe}</p>
          <p className="mt-0.5 text-ink">{ket.chu}</p>
        </div>
      )}

      {buoi.haDoKho && buoi.trangThai === 'dang' && (
        <p className="rounded-xl2 bg-gold-pale p-3 text-sm text-gold-dark">
          Mình tập lại từng từ một cho dễ nhé — xong rồi mới ghép thành câu.
        </p>
      )}

      {loi && <p className="rounded-xl2 bg-gold-pale p-3 text-gold-dark">{loi}</p>}

      {/* MỘT NÚT DUY NHẤT, và nay nó đứng TRÊN cuộc trò chuyện.
          Bác đổi 13-08: tin mới nhất lên trên, tin cũ xuống dưới. Nếu để nút ở
          cuối như bản trước thì mỗi lượt nói xong danh sách lại dài thêm, và bé
          phải cuộn qua cả buổi học mới tìm lại được cái nút. Nay nút đứng yên một
          chỗ, câu cô vừa nói nằm ngay bên dưới — bé thấy cả hai cùng lúc, không
          phải cuộn lần nào. */}
      {buoi.trangThai !== 'dang' ? null : ngheDuoc() && !micHong ? (
        <button type="button" onClick={noi} disabled={dangHoi}
          className={`flex items-center justify-center gap-3 rounded-xl2 px-6 py-6 text-2xl
            font-semibold transition disabled:opacity-60
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
            ${dangNghe ? 'bg-alert text-white' : 'bg-teal text-teal-dark hover:brightness-105'}`}>
          <span aria-hidden="true">{dangNghe ? '⏹️' : '🎤'}</span>
          {dangNghe ? 'Đang nghe con…' : 'Đến lượt con'}
        </button>
      ) : (
        <p className="rounded-xl2 border-2 border-line bg-soft p-4 text-mute">
          <b className="block text-ink">Máy này chưa nghe được</b>
          Phần nói cần trình duyệt Chrome và có mạng. Con cứ bấm vào hình để nghe cô
          đọc từng từ, rồi đọc theo nhé.
        </p>
      )}
      {dangNghe && (
        <p className="min-h-[1.6rem] text-center italic text-teal-dark">
          {tam ? `“${tam}”` : 'Con nói to và rõ nhé…'}
        </p>
      )}

      {/* CUỘC TRÒ CHUYỆN — MỚI NHẤT LÊN TRÊN.
          Lượt đầu tiên là câu chào mình tự gửi hộ bé để cô mở lời, không phải bé
          nói; lọc đi trước rồi mới đảo, chứ đảo trước thì nó rơi xuống cuối và
          `i === 0` không còn trỏ đúng nó nữa. */}
      <ol className="flex flex-col gap-3">
        <li ref={dauDs} />
        {dangHoi && (
          <li className="text-sm text-mute">Cô đang nghĩ…</li>
        )}
        {lichSu
          .filter((x, i) => !(i === 0 && x.vai === 'be'))
          .map((x, i) => ({ x, i }))
          .reverse()
          .map(({ x, i }) => (
            <li key={i}>
              {x.vai === 'may'
                ? <LuotCo luot={x} bai={bai} von={von} />
                : <LuotBe luot={x} />}
            </li>
          ))}
      </ol>
    </section>
  );
}

/* ─────────── một lượt của cô ─────────── */

function LuotCo({ luot, bai, von }) {
  const hinh = tuTrongCau(luot.en, von);
  return (
    <div className="flex flex-col gap-2 rounded-xl2 border-2 border-navy bg-white p-4">
      <div className="flex flex-wrap items-center gap-3">
        <span className="text-2xl" aria-hidden="true">🗣️</span>
        <p className="flex-1 font-serif text-2xl text-navy">{luot.en}</p>
        <button type="button" onClick={() => docLen(luot.en, 'en-GB', { nhanh: 0.9 })}
          aria-label={`Nghe lại: ${luot.en}`}
          className="h-12 w-12 flex-none rounded-full border-2 border-teal bg-teal-pale text-2xl
            text-teal-dark hover:bg-teal hover:text-white
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          <span aria-hidden="true">🔈</span>
        </button>
      </div>

      {/* Hình của các từ cô vừa nói tới — chỗ bé hiểu nghĩa mà không cần đọc chữ. */}
      {hinh.length > 0 && (
        <ul className="flex flex-wrap gap-2">
          {hinh.map((t) => (
            <li key={t.tu} className="flex w-[4rem] flex-col items-center rounded-xl2 bg-soft p-1.5">
              <span className="text-3xl leading-none"><HinhVe ten={t.tu} {...hinhCuaTu(bai, t.tu)} /></span>
              <span className="text-[0.65rem] text-mute">{t.nghia}</span>
            </li>
          ))}
        </ul>
      )}

      {luot.vi && (
        <div className="flex items-center gap-2">
          <p className="flex-1 text-ink">{luot.vi}</p>
          <button type="button" onClick={() => docDoan(tachTheoTieng(luot.vi, von))}
            aria-label={`Nghe lại lời tiếng Việt: ${luot.vi}`}
            className="h-9 w-9 flex-none rounded-full border-2 border-line text-sm text-mute
              hover:border-navy hover:text-navy
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            <span aria-hidden="true">🔈</span>
          </button>
        </div>
      )}
    </div>
  );
}

/* ─────────── một lượt của bé ─────────── */

function LuotBe({ luot }) {
  const dat = luot.diem != null && datNoi(luot.diem);
  return (
    <div className={`ml-8 flex flex-wrap items-center gap-3 rounded-xl2 p-3
      ${luot.diem == null ? 'bg-soft' : dat ? 'bg-teal-pale' : 'bg-gold-pale'}`}>
      <span className="text-xl" aria-hidden="true">🧒</span>
      <p className="flex-1 font-mono text-ink">“{luot.chu}”</p>
      {luot.diem != null && (
        <span className="text-lg" aria-label={`${loiKhen({ diem: luot.diem }).sao} sao`}>
          {'⭐'.repeat(loiKhen({ diem: luot.diem }).sao)}
        </span>
      )}
    </div>
  );
}
