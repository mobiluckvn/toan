import React, { useMemo, useState } from 'react';
import GocBoMe, { MucBoMe } from './GocBoMe.jsx';
import { Tranh } from './DocHieu.jsx';
import { duocGui, DIEM_TOI_DA } from '../lib/chamviet.js';
import { diemHienThi } from '../lib/hocba.js';
import { nhoCham } from '../lib/goiChamViet.js';

/**
 * BÀI VIẾT NGẮN — bé viết 2–3 câu, MÁY chấm. Bác chốt 18-08-2026.
 *
 * ── VIỆC THỨ TƯ CỦA MÔN ──
 * Nghe · nói · đọc đã có chỗ. Viết thì chưa: bậc 4 của mỗi bài chỉ là GÕ LẠI một
 * từ hoặc một câu đã cho. Gõ lại không phải viết — viết là tự chọn nói gì.
 *
 * ── BỐN ĐIỀU BÁC CHỐT, VÀ CHÚNG NẰM Ở ĐÂU TRÊN MÀN NÀY ──
 *
 *   1. sửa lỗi và khen CỤ THỂ  → khối "Cô khen" và bảng lỗi từng câu, có câu sửa
 *   2. có điểm, NÓI RÕ AI CHẤM → số điểm to, và ngay dưới nó là dòng "máy chấm"
 *   3. gợi ý chỉ bằng từ đã học → bảng từ bấm được ở trên, và lời chấm đã bị SOI
 *                                 (`soiLoiCham`) trước khi tới đây
 *   4. bố mẹ đọc được          → Góc bố mẹ mở ra là thấy nguyên bài viết và lời chấm
 *
 * ── VÌ SAO BẢNG TỪ BẤM ĐƯỢC ──
 * Bé lớp 3 gõ tiếng Anh còn chậm và nhớ mặt chữ chưa chắc. Bấm một từ là nó rơi
 * vào ô viết. Đây KHÔNG phải cho sẵn đáp án: bé vẫn phải chọn từ nào, xếp theo thứ
 * tự nào, và tự thêm dấu chấm câu. Cái được là bé không bỏ cuộc vì gõ sai chính tả
 * một từ mình biết rõ.
 *
 * ── ĐIỂM KHÔNG KHOÁ ĐƯỜNG ĐI ──
 * Không có nút "đi tiếp" nào ở đây, và điểm thấp cũng không chặn gì. Viết là việc
 * khó nhất; gắn cửa vào nó là bé né luôn cả bài.
 */
/* ── NGƯỠNG "ĐẠT" CỦA MỘT BÀI VIẾT ──
   Bài viết KHÔNG có đúng/sai sạch sẽ như câu trắc nghiệm, mà engine BKT thì chỉ
   nhận `ok` là true/false. Nên phải chọn một ngưỡng, và chọn ở ĐÂY, một chỗ, có
   tên — chứ đừng rải số 7 vào giữa dòng gọi.

   7/10 vì `chamViet` chấm trên thang 10 và coi 1–2 lỗi nhỏ là bài khá; lấy 9 thì
   gần như bài nào cũng thành "chưa đạt" và mức thạo tụt oan, lấy 5 thì bài sai
   nửa cũng tính công. Đây là con số CHỌN, không phải đo ra — đổi thì đổi ở đây. */
export const DIEM_DAT = 7;

export default function VietBai({ bai, onXong, onThoat, onLuot = null }) {
  const [viet, datViet] = useState('');
  const [dangCham, datDangCham] = useState(false);
  const [kq, datKq] = useState(null);
  const [loi, datLoi] = useState('');

  const vonTu = bai?.vonTu || [];
  const mauCau = bai?.mauCau || [];
  const goiY = bai?.goiY || [];
  const toiThieu = bai?.toiThieu || 2;
  const duoc = useMemo(() => duocGui(viet, toiThieu), [viet, toiThieu]);

  if (!bai) {
    return (
      <Khung ten="Bài viết" onThoat={onThoat}>
        <p className="text-alert">Chưa có đề bài viết cho chương này.</p>
      </Khung>
    );
  }

  const themTu = (t) => datViet((s) => (s.trim() ? `${s.replace(/\s+$/, '')} ${t}` : t));

  const cham = async () => {
    datLoi('');
    datDangCham(true);
    try {
      const r = await nhoCham({ de: bai.de, viet, vonTu, mauCau, lop: 3 });
      datKq(r);
      /* Ghi NGAY khi có kết quả, không đợi bé bấm gì thêm: bé tám tuổi đọc xong lời
         chấm là đóng máy, và lúc ấy công viết cả bài mất trắng. Cùng cái bẫy "thoát
         ở màn kết phải ghi" đã sập một lần. */
      onXong?.({ viet, cham: r.cham });
      /* ── ĐƯA BÀI VIẾT VÀO ENGINE ──
         Bác chốt 23-08: phần viết phải vào engine, không chỉ nằm trong học bạ cho
         bố mẹ đọc. Một bài viết = MỘT lượt, trên nút của chính bài ấy (`maNut` do
         `tools/nut_tri_thuc.py` gán).
         ⚠ `ms` KHÔNG đo được thật ở đây: bé gõ bài trong bao lâu thì màn này không
         biết, và lấy giờ gọi máy chấm làm thời gian phản hồi là bịa một con số cho
         chiều Thời gian. Để `null` — thiếu thì thấy được, bịa thì không. */
      onLuot?.({
        cau: { id: bai.id, maNut: bai.maNut, maNutDs: bai.maNutDs, format: 'viet' },
        ok: Number(r?.cham?.diem ?? 0) >= DIEM_DAT,
        lan: 1,
        ms: null,
        hintsUsed: 0,
        answer: viet,
        expected: null,
        phase: 'worked',
        /* Vân tay của lời dặn đã chấm bài này — đi cùng lượt để sau còn so
           "mẫu prompt nào giúp bé tiến bộ hơn" (ΔC, mục 2.5.3). */
        mauPrompt: r?.mauPrompt || null,
        phienBanMau: r?.phienBanMau ?? null,
        vanTayPrompt: r?.vanTayPrompt || null,
        maPhien: `viet-${bai.id}-${Date.now()}`,
        microId: bai.id,
      });
    } catch (e) {
      /* Nói ĐÚNG chỗ hỏng. "Thử lại nhé" cho mọi thứ thì bé bấm mãi trong khi lỗi
         nằm ở chỗ chẳng ai xem — cùng lý do với phòng luyện nói. */
      const ma = String(e?.code || '');
      datLoi(ma.includes('unauthenticated') ? 'Con đăng nhập rồi cô chấm cho nhé.'
        : ma.includes('permission-denied') ? 'Máy chấm chưa dùng được. Nhờ người lớn xem giúp nhé.'
        : ma.includes('invalid-argument') ? (e.message || 'Bài viết chưa gửi được.')
        : 'Chưa gọi được cô giáo máy. Con thử lại nhé.');
    } finally {
      datDangCham(false);
    }
  };

  return (
    <Khung ten={bai.name} onThoat={onThoat}>
      {/* ⚠ CÓ TRANH THÌ KHÔNG BÀY "Mẫu câu con đã học" — với bài tả tranh, mấy mẫu
          ấy CHÍNH LÀ bản mô tả bức tranh. Bày ra là cho sẵn đáp án, và bài viết
          hoá ra bài chép lại. Bác chốt: bài viết thì bé "chỉ được nhìn tranh". */}
      <Tranh src={bai.tranh} ten={bai.tranhTen} />
      <section className="rounded-xl2 border-2 border-navy bg-white p-4">
        <h2 className="mb-1 text-sm font-semibold uppercase tracking-wider text-mute">
          Đề bài
        </h2>
        <p className="text-lg text-ink">{bai.de}</p>
        {!bai.tranh && !!mauCau.length && (
          <details className="mt-3">
            <summary className="cursor-pointer text-sm font-semibold text-navy">
              Mẫu câu con đã học ({mauCau.length})
            </summary>
            <ul className="mt-2 flex flex-col gap-1 text-ink">
              {mauCau.map((m) => <li key={m} className="text-sm">· {m}</li>)}
            </ul>
          </details>
        )}
      </section>

      <label className="flex flex-col gap-2">
        <span className="text-sm font-semibold uppercase tracking-wider text-mute">
          Con viết ở đây
        </span>
        <textarea
          value={viet}
          onChange={(e) => datViet(e.target.value)}
          rows={5}
          maxLength={600}
          spellCheck={false}
          placeholder={bai.tranh ? 'I can see ...' : "Hello. I'm ..."}
          className="w-full rounded-xl2 border-2 border-line bg-white p-3 text-lg text-ink
            focus:border-navy focus:outline-none focus-visible:ring-4 focus-visible:ring-gold"
        />
      </label>

      {/* ══ GỢI Ý — CỤM GHÉP ĐƯỢC, XẾP THEO CHỖ TRONG ĐOẠN ══

          Bác chốt 18-08-2026: "phần gợi ý nên bổ sung thêm nhiều từ hơn cho con
          chọn và ghi là gợi ý. Con có thể typing thêm theo ý của con. Lưu ý là các
          từ gợi ý ấy phải ghép lại thành được đoạn văn có ý nghĩa chứ như giờ bạn
          cho linh tinh."

          Bản cũ bày đúng một bảng: 53 ô chữ rời, dồn từ chương 1 tới đây, xếp theo
          thứ tự sách — `one · two · … · the alphabet (A–Z) · hello · … · your`.
          Bấm bừa vài cái ra "ten hello your old": không phải câu, càng không phải
          đoạn. Nay mỗi nhóm là một CHỖ trong đoạn (mở đầu → nội dung → chào tạm
          biệt), và mỗi mục là một câu trọn vẹn của sách. Bấm mỗi nhóm một cái là
          ra một đoạn có đầu có cuối. Bảng từ vẫn còn, nhưng lùi xuống làm việc của
          nó: thay vào chỗ trống. */}
      {!!goiY.length && (
        <section>
          <h2 className="text-sm font-semibold uppercase tracking-wider text-mute">
            Gợi ý — bấm để thêm vào bài
          </h2>
          <p className="mb-2 text-sm text-mute">
            Đây chỉ là gợi ý thôi. Con tự gõ thêm câu của riêng con cũng được nhé.
          </p>
          <div className="flex flex-col gap-3">
            {goiY.map((g) => (
              <div key={g.nhan}>
                <p className="text-sm font-semibold text-navy">{g.nhan}</p>
                <div className="mt-1 flex flex-wrap gap-2">
                  {g.cum.map((c) => (
                    <button key={c} type="button" onClick={() => themTu(c)}
                      className="rounded-xl2 border-2 border-line bg-white px-3 py-1.5 text-ink
                        hover:border-navy focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
                      {c}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      <section>
        <h2 className="mb-2 text-sm font-semibold uppercase tracking-wider text-mute">
          {bai.tranh
            ? 'Từ trong tranh — bấm để thêm vào bài'
            : (goiY.length ? 'Từ để thay vào chỗ trống' : 'Từ con đã học — bấm để thêm vào bài')}
        </h2>
        {/* ⚠ NGHĨA TIẾNG VIỆT PHẢI HIỆN RA, KHÔNG ĐƯỢC NẰM TRONG `title`.
            Bản cũ bày nghĩa bằng `title={v.nghia}` — tức TOOLTIP, chỉ hiện khi rê
            chuột. Bé học trên máy tính bảng và điện thoại thì không bao giờ thấy,
            nên 2167 ô ĐÃ CÓ nghĩa cũng vô hình y hệt ô không có. Suốt thời gian
            ấy dữ liệu vẫn đầy đủ và không cổng nào đỏ: chỗ hỏng nằm giữa dữ liệu
            và mắt đứa trẻ, không tệp nào sở hữu chỗ ấy.
            Bày theo đúng khuôn màn Nói: chữ trên, nghĩa nhỏ bên dưới. */}
        <div className="flex flex-wrap gap-2">
          {vonTu.map((v) => (
            <button key={v.tu} type="button" onClick={() => themTu(v.tu)}
              aria-label={v.nghia ? `${v.tu} — ${v.nghia}` : v.tu}
              className="flex flex-col items-start rounded-xl2 border-2 border-line bg-white
                px-3 py-1.5 text-left text-ink
                hover:border-navy focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
              <span>{v.tu}</span>
              {v.nghia && (
                <span className="text-[0.7rem] leading-tight text-mute">{v.nghia}</span>
              )}
            </button>
          ))}
        </div>
      </section>

      <div className="flex flex-wrap items-center gap-3">
        <button type="button" onClick={cham} disabled={!duoc.ok || dangCham}
          className="rounded-xl2 bg-navy px-6 py-3 text-lg font-semibold text-white
            disabled:opacity-50 focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          {dangCham ? 'Cô đang đọc bài…' : 'Nhờ cô chấm'}
        </button>
        {!duoc.ok && <p className="text-sm text-mute">{duoc.vi}</p>}
      </div>
      {!!loi && <p className="rounded-xl2 bg-gold-pale px-4 py-2.5 text-gold-dark">{loi}</p>}

      {kq?.cham && <LoiCham kq={kq} viet={viet} />}
    </Khung>
  );
}

/** Lời chấm — điểm, khen, sửa từng lỗi, gợi ý. Và NÓI RÕ là máy chấm. */
function LoiCham({ kq, viet, muc = null }) {
  const { cham, boQua } = kq;
  /* MỘT nguồn cho con số và cái nhãn đi kèm — xem `diemHienThi` (việc V5). `muc` là
     bản đã nằm trong sổ; chưa có (vừa chấm xong, chưa kịp ghi) thì dựng tạm từ
     chính lời chấm, và nó sẽ ra nhãn "chờ bố mẹ" — đúng trạng thái lúc ấy. */
  const hien = diemHienThi(muc || { diem: cham?.diem ?? null });
  return (
    <section className="flex flex-col gap-4 rounded-xl2 border-2 border-teal bg-teal-pale p-4">
      <div className="flex items-baseline gap-3">
        <p className="text-4xl font-bold text-teal-dark">
          {hien.diem ?? '—'}<span className="text-2xl">/{DIEM_TOI_DA}</span>
        </p>
        {/* ⚠ DÒNG NÀY KHÔNG ĐƯỢC BỎ. Bác chốt: có điểm thì phải nói rõ ai chấm.
            Con số không nhãn sẽ được đọc thành điểm của cô giáo, và đó là hiểu nhầm
            bố mẹ không có cách nào tự phát hiện.
            Từ V5 nhãn do `diemHienThi` sinh — ba chỗ con số này lộ ra từng mỗi chỗ
            tự viết một dòng chữ khác nhau. */}
        <p className="text-sm text-teal-dark">
          {`${hien.nhanDay}, không phải điểm của cô giáo`}
        </p>
      </div>

      {!!cham.khen && (
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wider text-mute">Cô khen</h3>
          <p className="text-ink">{cham.khen}</p>
        </div>
      )}

      {!!cham.loi.length && (
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wider text-mute">
            Chỗ cần sửa
          </h3>
          <ul className="flex flex-col gap-2">
            {cham.loi.map((x) => (
              <li key={`${x.cau}|${x.sua}`} className="rounded-xl2 bg-white p-3">
                <p className="text-ink line-through decoration-alert">{x.cau}</p>
                <p className="font-semibold text-teal-dark">{x.sua}</p>
                {!!x.viSao && <p className="mt-1 text-sm text-mute">{x.viSao}</p>}
              </li>
            ))}
          </ul>
        </div>
      )}

      {!cham.loi.length && (
        <p className="text-teal-dark">Cô không tìm thấy lỗi nào trong bài của con.</p>
      )}

      {!!cham.goiY && (
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wider text-mute">
            Lần sau con thử
          </h3>
          <p className="text-ink">{cham.goiY}</p>
        </div>
      )}

      {/* Bỏ bớt thì PHẢI NÓI. Giấu đi thì lời chấm trông đầy đủ trong khi nó vừa
          mất một mục, và lần sau chẳng ai biết lời dặn đang không ăn. */}
      {!!boQua.length && (
        <p className="text-sm text-mute">
          Cô có {boQua.length} câu gợi ý dùng từ con chưa học, nên cô giấu đi rồi.
        </p>
      )}

      <GocBoMe ten="Góc bố mẹ · bài viết và lời chấm">
        <MucBoMe nhan="Con viết">{viet}</MucBoMe>
        <MucBoMe nhan="Điểm">
          {`${hien.diem ?? '—'}/${DIEM_TOI_DA} · ${hien.nhanDay} · ${cham.loi.length} lỗi`}
        </MucBoMe>
        {!!cham.choBoMe && <MucBoMe nhan="Lời cho bố mẹ">{cham.choBoMe}</MucBoMe>}
        <MucBoMe nhan="Ai chấm">
          {`Điểm và lời chấm do mô hình ${kq.moHinh || 'AI'} sinh ra. Đây là gợi ý `
           + 'cho con tự sửa, không phải điểm của giáo viên.'}
        </MucBoMe>
      </GocBoMe>
    </section>
  );
}

function Khung({ ten, children, onThoat }) {
  return (
    <div className="mx-auto flex min-h-screen w-full max-w-3xl flex-col gap-5 p-4 pb-24">
      <div className="flex items-center gap-3">
        <button type="button" onClick={onThoat}
          className="rounded-xl2 border-2 border-line px-3 py-2 text-sm font-semibold text-mute
            hover:border-navy hover:text-navy focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          ← Về
        </button>
        <h1 className="flex-1 text-lg font-bold text-ink sm:text-xl">✍️ {ten}</h1>
      </div>
      {children}
    </div>
  );
}
