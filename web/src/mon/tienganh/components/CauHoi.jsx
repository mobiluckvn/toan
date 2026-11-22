import React, { useEffect, useMemo, useRef, useState } from 'react';
import NutNghe from './NutNghe.jsx';
import HinhVe from './HinhVe.jsx';
import { chamTiengAnh } from '../lib/cham.js';
import { duocBoQua, hienGoiY } from '../lib/dandat.js';

/**
 * MỘT CÂU HỎI TIẾNG ANH — bốn bậc, bốn cách trả lời.
 *
 *   bậc 1  nghe rồi bấm HÌNH
 *   bậc 2  từ ↔ nghĩa, bấm chữ
 *   bậc 3  xếp thẻ thành câu · điền chỗ trống (manh mối là HÌNH, không phải tiếng)
 *   bậc 4  gõ lại từ, rồi gõ cả câu
 *
 * Chấm bằng `chamTiengAnh()`, KHÔNG bằng `flow.js` của Toán — bộ chấm Toán bỏ chấm
 * mọi đáp án dài quá 26 ký tự, mà câu dài nhất của lớp 1 là 46.
 *
 * ── HAI QUY TẮC CHO BÉ 6 TUỔI ──
 * 1. Nút phải TO. Ngón tay trẻ con không bấm trúng nút cỡ người lớn, và bấm trượt
 *    thì bé tưởng mình sai chứ không nghĩ là tại nút.
 * 2. Sai KHÔNG mất lượt. Bé được thử lại ngay, và lần thứ hai thì hiện gợi ý. Đây
 *    là lớp 1: nản một lần là nghỉ luôn.
 *
 * ── BỎ QUA ĐƯỢC, NHƯNG PHẢI ĐỂ LẠI DẤU ──
 * Thử quá số lần tối thiểu mà vẫn sai thì hiện đáp án và cho đi tiếp — bắt làm
 * tới khi đúng thì có câu bé không bao giờ ra khỏi được, mà kẹt một câu là nghỉ
 * cả buổi. Nhưng lúc ấy phải báo `boQua: true` lên trên: chỗ gọi gom những câu ấy
 * lại và mời bé làm lại một lượt cuối mức. Bản trước không có cờ này, nên bỏ qua
 * xong là câu ấy MẤT HẲN — bé đi hết mức mà nửa số câu chưa từng làm được, và
 * không con số nào trên màn nói ra điều đó.
 *
 * ── `onLuot` — MỖI LƯỢT TRẢ LỜI MỘT TIẾNG, KHÔNG PHẢI MỖI CÂU MỘT TIẾNG ──
 *
 * `onXong` chỉ kêu khi bé LÀM XONG câu (đúng, hoặc bỏ qua). Nhật ký học thì cần
 * biết cả những lần sai ở giữa: bé sai hai lần rồi mới đúng là ba dòng, và ba
 * dòng ấy mới nói được "bé sai CÁI GÌ trước khi làm được".
 *
 * Mỗi lượt mang theo:
 *   ms         thời gian làm RIÊNG lượt ấy (RT_avg của mục 2.3.1). Đo từ lúc câu
 *              hiện ra, hoặc từ lúc bé bấm "Thử lại" — không phải từ lúc mở bài.
 *   hintsUsed  bé đã THẤY mấy gợi ý (H_req). Bên Tiếng Anh gợi ý hiện TỰ ĐỘNG sau
 *              `hienGoiY()` lần thử chứ không do bé xin, nên đây là "đã thấy",
 *              không phải "đã xin" — nghĩa hơi khác Toán, chỗ nào đọc cũng nên biết.
 *   answer     bé gõ/bấm gì. Trường quý nhất: hai bé sai hai kiểu cần hai cách giúp.
 */
export default function CauHoi({ cau, onXong, onLuot = null }) {
  /* Chỗ gọi PHẢI truyền `key={cau.id}` để component dựng lại mỗi câu — xem chú
     thích ở `BaiHoc.jsx`. `useEffect` dưới đây chỉ là lưới đỡ thứ hai: effect chạy
     SAU lần vẽ đầu, nên nếu chỉ dựa vào nó thì câu xếp thẻ vẽ lần đầu với `dap`
     còn là chuỗi rỗng của câu bấm chọn trước đó, và `dap.map` ném ngay. */
  const [dap, datDap] = useState(cau.the ? [] : '');
  const [kq, datKq] = useState(null);
  const [lan, datLan] = useState(0);

  /* Mốc bấm giờ của LƯỢT hiện tại. `useRef` chứ không `useState`: đổi nó không
     được vẽ lại màn, mà vẽ lại giữa lúc bé đang gõ là mất chữ. */
  const mocLuot = useRef(Date.now());
  useEffect(() => {
    datDap(cau.the ? [] : ''); datKq(null); datLan(0);
    mocLuot.current = Date.now();
    /* ⚠ CHỈ `cau.id`, CÓ CHỦ Ý. ESLint muốn thêm `cau.the` và nó đúng về hình thức,
       nhưng `the` là mảng nằm trong chính `cau` ấy: cùng một `id` thì không bao giờ
       đổi nội dung, chỉ đổi DANH TÍNH khi chỗ gọi dựng lại object. Thêm vào là mỗi
       lần cha vẽ lại, đáp án bé đang gõ bị xoá về rỗng và bấm giờ lượt chạy lại. */
    // eslint-disable-next-line react-hooks/exhaustive-deps -- xem ghi chú trên
  }, [cau.id]);

  const nop = (v) => {
    const r = chamTiengAnh(cau, v);
    /* ⚠ ĐO GIỜ TRƯỚC KHI ĐỔI STATE. Đặt sau `datKq` thì vẫn đúng ở React hiện
       tại, nhưng nó buộc người đọc phải biết state đổi không đồng bộ mới tin
       được — đo ngay tại đây thì không phải tin gì cả. */
    const ms = Math.max(0, Date.now() - mocLuot.current);
    datKq(r);
    datLan((n) => n + 1);
    /* Bé đã THẤY mấy gợi ý tính tới lượt này. Cùng phép tính với chỗ hiện gợi ý ở
       dưới, nên hai chỗ không lệch nhau được. */
    const dsGoi = cau.hints || [];
    const nguongGoi = hienGoiY();
    const daThay = lan >= nguongGoi
      ? Math.min(lan - nguongGoi + 1, dsGoi.length) : 0;
    onLuot?.({
      cau,
      ok: r.ok,
      lan: lan + 1,
      ms,
      hintsUsed: daThay,
      answer: v,
      expected: cau.answerKey,
    });
    if (r.ok) onXong({ dung: true, lan: lan + 1 });
  };

  const thuLai = () => {
    datKq(null); datDap(cau.the ? [] : '');
    /* Bấm "Thử lại" là bắt đầu một lượt MỚI — đặt lại đồng hồ. Không đặt lại thì
       `ms` của lượt hai gồm cả thời gian bé ngồi đọc lời báo sai của lượt một. */
    mocLuot.current = Date.now();
  };

  return (
    <div className="flex flex-col gap-4">
      <De cau={cau} />

      {cau.the ? (
        <XepThe the={cau.the} dap={dap} datDap={datDap} khoa={!!kq?.ok} onNop={nop} />
      ) : cau.choices ? (
        <BamChon cau={cau} khoa={!!kq?.ok} chon={(v) => { datDap(v); nop(v); }} dap={dap} />
      ) : (
        <GoChu dap={dap} datDap={datDap} khoa={!!kq?.ok} onNop={() => nop(dap)} />
      )}

      {kq && (
        <Chua kq={kq} cau={cau} lan={lan} onThuLai={thuLai}
              onTiep={() => onXong({ dung: kq.ok, lan, boQua: !kq.ok })} />
      )}
    </div>
  );
}

/* ─────────── đề bài ─────────── */

function De({ cau }) {
  return (
    <div className="flex items-start gap-3">
      {/* Clip của câu tự phát khi bé vào câu mới: bé chưa đọc được đề, tiếng phải
          tới trước. Bấm lại bao nhiêu lần cũng được. */}
      {cau.am && <NutNghe ma={cau.am} to nhan="Nghe lại" tuDong />}
      <div className="flex-1">
        <p className="text-lg leading-snug text-ink sm:text-xl">{cau.text}</p>
        {/* DÒNG PHỤ TIẾNG VIỆT — bác chốt 19-08-2026: câu hỏi bài đọc hỏi bằng TIẾNG
            ANH, nhưng bé lớp 3 mới tập đọc thì phải có chỗ bám. Để NHỎ và nhạt hơn:
            nó là chỗ dựa, không phải câu hỏi. Bài nào không khai `phu` thì không
            hiện gì — 20 unit kia không đổi. */}
        {cau.phu && <p className="mt-0.5 text-sm text-mute">{cau.phu}</p>}
        {(cau.anh || cau.anhVe) && (
          <div className="mt-2 text-6xl leading-none sm:text-7xl">
            <HinhVe ve={cau.anhVe} hinh={cau.anh} ten="hình gợi ý" />
          </div>
        )}
      </div>
    </div>
  );
}

/* ─────────── bậc 1-2: bấm chọn ─────────── */

function BamChon({ cau, chon, dap, khoa }) {
  const anhNut = cau.hinhNut || {};
  const veNut = cau.veNut || {};
  const laHinh = !!cau.anhChon;
  return (
    <div className={`grid gap-3 ${laHinh ? 'grid-cols-2 sm:grid-cols-4' : 'grid-cols-1 sm:grid-cols-2'}`}>
      {cau.choices.map((x) => {
        const dangChon = dap === x;
        return (
          <button
            key={x}
            type="button"
            disabled={khoa}
            onClick={() => chon(x)}
            className={`rounded-xl2 border-2 p-4 text-left transition disabled:opacity-60
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
              ${dangChon ? 'border-navy bg-soft' : 'border-line bg-white hover:border-navy-light'}`}
          >
            {laHinh ? (
              <span className="mx-auto block text-center text-5xl leading-none sm:text-6xl">
                <HinhVe ve={veNut[x]} hinh={anhNut[x]} ten={x} />
              </span>
            ) : (
              <span className="text-lg text-ink">{x}</span>
            )}
          </button>
        );
      })}
    </div>
  );
}

/* ─────────── bậc 3: xếp thẻ ─────────── */

/**
 * Bé bấm thẻ để đưa lên dòng câu, bấm lại để trả về. KHÔNG dùng kéo-thả: kéo-thả
 * trên màn cảm ứng đòi giữ ngón tay đúng chỗ trong lúc trượt, mà tay bé 6 tuổi
 * chưa làm được đều — bấm thì lần nào cũng trúng.
 */
function XepThe({ the, dap: dapVao, datDap, khoa, onNop }) {
  /* Nhận bừa cũng phải sống: nếu đâu đó còn truyền xuống chuỗi rỗng của câu trước,
     thà hiện một dòng thẻ trống còn hơn cả bài trắng màn hình. */
  const dap = Array.isArray(dapVao) ? dapVao : [];
  /* Thẻ một ký tự = đang ghép CHỮ CÁI, không phải xếp câu. */
  const chuCai = the.every((x) => String(x).length === 1);
  /**
   * Thứ tự thẻ bày ra phải KHÁC thứ tự đúng, nếu không bé chỉ việc bấm từ trái
   * sang phải mà không cần hiểu câu. Đảo bằng phép CỐ ĐỊNH (không random) để chạy
   * hai lần ra một kết quả — bé làm lại bài thấy y như cũ.
   *
   * Chỉ xếp theo độ dài là CHƯA ĐỦ, và đã hỏng thật: "I like milk." có độ dài
   * 1 · 4 · 5 nên xếp theo độ dài ra ĐÚNG THỨ TỰ CÂU, bài thành cho không. Nên
   * sau khi xếp phải kiểm lại: trùng thứ tự gốc thì đảo ngược.
   */
  const bay = useMemo(() => {
    const d = the.map((t, i) => ({ t, i }));
    const x = d.slice().sort((a, b) => (a.t.length - b.t.length) || (b.i - a.i));
    const trungThuTu = x.every((o, k) => o.i === k);
    return trungThuTu && x.length > 1 ? x.slice().reverse() : x;
  }, [the]);
  const daDung = dap.map((x) => x.i);

  return (
    <div className="flex flex-col gap-3">
      <div className="flex min-h-[4rem] flex-wrap items-center gap-2 rounded-xl2 border-2
        border-dashed border-line bg-soft p-3">
        {dap.length === 0 && (
          /* Cùng một khối thẻ dùng cho HAI việc: xếp từ thành câu (bậc 3) và ghép
             chữ cái thành từ (nấc đầu của bậc 4, cho từ dài quá sức gõ). Lời nhắc
             phải nói đúng việc đang làm — bảo bé "xếp thành câu" trong khi trên
             tay là bảy chữ cái rời thì bé không hiểu phải làm gì. */
          <span className="text-mute">
            {chuCai ? 'Bấm từng chữ cái để ghép thành từ…' : 'Bấm các thẻ bên dưới để xếp thành câu…'}
          </span>
        )}
        {dap.map((x, k) => (
          <button
            key={`${x.i}-${k}`}
            type="button"
            disabled={khoa}
            onClick={() => datDap(dap.filter((_, j) => j !== k))}
            className="rounded-lg border-2 border-navy bg-white px-3 py-2 text-lg text-ink
              disabled:opacity-60 focus:outline-none focus-visible:ring-4 focus-visible:ring-gold"
          >
            {x.t}
          </button>
        ))}
      </div>

      <div className="flex flex-wrap gap-2">
        {bay.filter((x) => !daDung.includes(x.i)).map((x) => (
          <button
            key={x.i}
            type="button"
            disabled={khoa}
            onClick={() => datDap([...dap, x])}
            className="rounded-lg border-2 border-line bg-white px-3 py-2 text-lg text-ink
              hover:border-navy-light disabled:opacity-60
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold"
          >
            {x.t}
          </button>
        ))}
      </div>

      <button
        type="button"
        disabled={khoa || dap.length !== the.length}
        onClick={() => onNop(dap.map((x) => x.t))}
        className="self-start rounded-xl2 bg-navy px-6 py-3 font-semibold text-white
          disabled:bg-line disabled:text-mute focus:outline-none focus-visible:ring-4 focus-visible:ring-gold"
      >
        Xong
      </button>
    </div>
  );
}

/* ─────────── bậc 4: gõ ─────────── */

function GoChu({ dap, datDap, khoa, onNop }) {
  return (
    <form
      className="flex flex-wrap items-center gap-3"
      onSubmit={(e) => { e.preventDefault(); if (!khoa && dap.trim()) onNop(); }}
    >
      <input
        value={dap}
        onChange={(e) => datDap(e.target.value)}
        disabled={khoa}
        /* Bàn phím máy tính bảng tự viết hoa và tự sửa chính tả — cả hai đều phá
           đúng cái bài này đang kiểm. Tắt hết; bộ chấm đã tha hoa/thường rồi. */
        autoCapitalize="off"
        autoCorrect="off"
        autoComplete="off"
        spellCheck="false"
        inputMode="text"
        aria-label="Gõ câu trả lời"
        className="min-w-0 flex-1 rounded-xl2 border-2 border-line bg-white px-4 py-3
          text-xl text-ink focus:border-navy focus:outline-none focus-visible:ring-4 focus-visible:ring-gold"
      />
      <button
        type="submit"
        disabled={khoa || !dap.trim()}
        className="rounded-xl2 bg-navy px-6 py-3 font-semibold text-white
          disabled:bg-line disabled:text-mute focus:outline-none focus-visible:ring-4 focus-visible:ring-gold"
      >
        Xong
      </button>
    </form>
  );
}

/* ─────────── lời chữa ─────────── */

function Chua({ kq, cau, lan, onThuLai, onTiep }) {
  if (kq.ok) {
    return (
      <div className="flex flex-wrap items-center gap-3 rounded-xl2 bg-teal-pale p-4">
        <span className="text-2xl" aria-hidden="true">✅</span>
        <p className="flex-1 text-teal-dark">{cau.solutionNarrative || 'Đúng rồi!'}</p>
        <button type="button" onClick={onTiep}
          className="rounded-xl2 bg-teal px-5 py-2 font-semibold text-teal-dark
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Tiếp
        </button>
      </div>
    );
  }
  /* Sai lần đầu: chỉ bảo thử lại. Sai lần hai: mới đưa gợi ý. Đưa gợi ý ngay từ
     lần đầu thì bé không kịp tự nghĩ, mà giấu mãi thì bé nản. */
  const nguongGoi = hienGoiY();
  const goi = lan >= nguongGoi
    ? (cau.hints || [])[Math.min(lan - nguongGoi, (cau.hints || []).length - 1)] : null;
  return (
    <div className="flex flex-col gap-2 rounded-xl2 bg-gold-pale p-4">
      <div className="flex flex-wrap items-center gap-3">
        <span className="text-2xl" aria-hidden="true">🤔</span>
        <p className="flex-1 text-gold-dark">Chưa đúng. Con nghe lại rồi thử lần nữa nhé.</p>
        <button type="button" onClick={onThuLai}
          className="rounded-xl2 bg-gold px-5 py-2 font-semibold text-gold-dark
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Thử lại
        </button>
      </div>
      {goi && <p className="text-sm text-gold-dark">💡 {goi}</p>}
      {duocBoQua(lan) && (
        <div className="flex flex-wrap items-center gap-3 border-t border-gold pt-2">
          <p className="flex-1 text-gold-dark">Đáp án: <b>{kq.expected}</b></p>
          {/* Nhãn nói THẲNG là câu này sẽ quay lại. Ghi trơn "Bỏ qua câu này" thì
              bé hiểu là xong hẳn, rồi cuối mức thấy nó hiện ra lại là hụt hẫng. */}
          <button type="button" onClick={onTiep}
            className="rounded-xl2 border-2 border-gold-dark px-4 py-1.5 text-sm
              font-semibold text-gold-dark focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            Để câu này lại sau →
          </button>
        </div>
      )}
    </div>
  );
}
