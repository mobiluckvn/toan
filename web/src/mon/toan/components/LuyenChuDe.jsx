import React, { useEffect, useState } from 'react';
import Chu from '../../../chung/components/Chu.jsx';
import { CONTENT, dongDau } from '../../../chung/lib/soQuyen.js';
import { loadLesson } from '../lib/noiDung.js';
import { buocSau, nguongDat } from '../lib/progress.js';
import AnswerInput from './AnswerInput.jsx';

/**
 * LUYỆN MỘT CHỦ ĐỀ TẠI MỘT BẬC — và tự lùi / tự tiến theo kết quả.
 *
 * Đây là chỗ trả lời câu hỏi của bác: "luyện chủ đề lớp 5 mà kém thì tự chuyển về
 * lớp 4 cho con luyện rồi tiến lên; kém nữa thì về lớp 3".
 *
 * ── KÉM THÌ MỞ BÀI HỌC, KHÔNG PHẢI CHO LÀM THÊM BÀI TẬP ──
 *
 * Con sai ở bậc trên nghĩa là hổng gốc. Đưa thêm một xấp bài tập cùng kiểu ở lớp
 * dưới chỉ để con sai thêm một lượt nữa — thứ con thiếu là phần GIẢNG. Nên lùi một
 * bậc là mở BÀI HỌC của bậc ấy; học xong bài thì `veLai` đưa con về đúng vòng luyện
 * của bậc ấy, đạt rồi mới tiến lên. Đó là lý do màn này chỉ lo phần đo, còn phần
 * dạy thì trả về cho LessonPlayer đã có sẵn.
 *
 * ── CHẤM MỘT LẦN ──
 *
 * `chotMotLan` như kỳ sát hạch: vòng này quyết định con LÙI hay TIẾN, mà sai rồi
 * sửa lại được thì con số đo ra chẳng còn nghĩa gì. Khác hẳn phần luyện tập trong
 * bài, nơi sai rồi thử lại chính là việc cần làm.
 */

const SO_CAU = 6;

/** Câu MÁY CHẤM ĐƯỢC của một bài — thứ tự dễ → khó theo tên hồ chứa. */
const HO = ['warmup', 'standard', 'challenge'];
function cauCua(bai) {
  const pools = bai?.practice?.pools || {};
  return HO.flatMap((h, muc) => (pools[h] || [])
    .filter((c) => c.answerKey)
    .map((c) => ({ ...c, id: `${bai.id}#${c.id}`, muc, tuBai: bai.id, tenBai: bai.title })));
}

export default function LuyenChuDe({ maDang, lop, progress: _progress, onXongLuot, onMoBai,
                                    onThoat, onDoiBac, onVeNha }) {
  const [bd, setBd] = useState(null);
  const [cau, setCau] = useState(null);
  const [i, setI] = useState(0);
  const [dung, setDung] = useState(0);
  const [res, setRes] = useState(null);
  const [daGhi, setDaGhi] = useState(false);

  useEffect(() => {
    fetch(dongDau(`${CONTENT}/chu_de.json`))
      .then((r) => r.json()).then(setBd).catch(() => setBd({ loi: true }));
  }, []);

  const d = bd && !bd.loi ? bd.dang?.[maDang] : null;
  const bac = d ? (d.thang || []).find((b) => b.lop === lop) : null;

  /* Nạp bài của bậc rồi rút câu. `loadLesson` có sẵn bộ nhớ đệm nên lùi lên lùi
     xuống trong cùng một chủ đề không phải tải lại. */
  useEffect(() => {
    if (!bac) return;
    let bo = false;
    setCau(null); setI(0); setDung(0); setRes(null); setDaGhi(false);
    Promise.all(bac.bai.map((id) => loadLesson(id).catch(() => null)))
      .then((bais) => {
        if (bo) return;
        const ds = bais.filter(Boolean).flatMap(cauCua);
        ds.sort((a, b) => a.muc - b.muc);
        setCau(ds.slice(0, SO_CAU));
      });
    return () => { bo = true; };
  }, [maDang, lop, bac?.bai?.join()]);

  /* Ghi sổ ĐÚNG MỘT LẦN khi hết câu. Phải là hiệu ứng chứ không phải làm ngay trong
     lúc vẽ: gọi setState của màn cha giữa chừng một lượt vẽ thì React vẽ lại, và
     lượt luyện bị ghi hai lần — con số của bố mẹ cộng đôi mà không có gì báo. */
  const hetCau = !!cau && i >= cau.length;
  useEffect(() => {
    if (!hetCau || daGhi) return;
    setDaGhi(true);
    onXongLuot?.(maDang, lop, { dat: dung, tong: cau.length });
  }, [hetCau, daGhi]);

  if (!bd) return <div className="p-6 text-mute">Đang mở bản đồ chủ đề…</div>;
  if (bd.loi || !d) return <div className="p-6 text-alert">Không nạp được chủ đề này.</div>;
  if (!bac) return <div className="p-6 text-alert">Chủ đề này không có bậc lớp {lop}.</div>;
  if (!cau) return <div className="p-6 text-mute">Đang lấy bài luyện…</div>;

  const DauTrang = (
    <header className="mb-3 flex items-center gap-2.5">
      <button className="text-[13px] text-mute" onClick={onThoat}>← Thoát</button>
      {/* Cửa về NHÀ cũng phải có ở đây: vòng luyện vào được từ màn chủ đề, mà màn chủ
          đề không thuộc quyển nào — thoát ra chỉ lùi được một tầng. */}
      {onVeNha && (
        <button className="text-[13px] text-mute" onClick={onVeNha}>⌂</button>
      )}
      <b className="flex-1 text-center text-[13.5px] leading-snug text-navy">
        {d.ten}
        <span className="ml-1.5 rounded bg-navy px-1.5 py-0.5 text-[11px] text-white">
          LỚP {lop}
        </span>
      </b>
      <span className="w-[52px] text-right text-[12px] tabular-nums text-mute">
        {Math.min(i + 1, cau.length)}/{cau.length}
      </span>
    </header>
  );

  /* Bậc không đủ câu máy chấm được thì nói thẳng và mời học bài, đừng dựng một vòng
     luyện hai câu rồi phán con vững hay không vững. */
  if (cau.length < 3) {
    return (
      <div className="mx-auto max-w-[740px] px-3.5 pb-28 pt-4">
        {DauTrang}
        <div className="card">
          <p className="text-[15px] leading-relaxed">
            Bậc lớp {lop} của chủ đề này chưa có đủ câu chấm máy để luyện riêng.
            Con học thẳng bài nhé:
          </p>
          {bac.bai.map((id, k) => (
            <button key={id} className="btn-go mt-2.5" onClick={() => onMoBai(id, lop)}>
              {bac.ten[k] || id} ▶
            </button>
          ))}
        </div>
      </div>
    );
  }

  /* ── XONG LƯỢT ─────────────────────────────────────────────────────────── */
  if (i >= cau.length) {
    const can = nguongDat(cau.length);
    const dat = dung >= can;
    const b = buocSau(d.thang, lop, dung, cau.length);
    const bacDuoi = b.hanh === 'xuong' ? d.thang.find((x) => x.lop === b.lop) : null;

    return (
      <div className="mx-auto max-w-[740px] px-3.5 pb-28 pt-4">
        {DauTrang}
        <div className="card text-center">
          <div className="text-[54px] leading-none">{dat ? '🏅' : '💪'}</div>
          <h2 className="mt-1 text-[21px] font-bold text-navy">
            {dung}/{cau.length} câu · {dat ? 'vững rồi!' : `cần ${can} câu mới qua`}
          </h2>

          {b.hanh === 'xong' && (
            <p className="mt-2 text-[15px] leading-relaxed text-teal-dark">
              Con đã vững chủ đề này tới bậc cao nhất hiện có. Chọn chủ đề khác nhé.
            </p>
          )}

          {b.hanh === 'len' && (
            <p className="mt-2 text-[15px] leading-relaxed">
              Bậc lớp {lop} xong rồi. Mình lên bậc lớp {b.lop} của cùng chủ đề này.
            </p>
          )}

          {b.hanh === 'xuong' && (
            <>
              <p className="mt-2 text-[15px] leading-relaxed">
                Chưa qua bậc lớp {lop} thì thường là hổng ở gốc. Mình lùi về{' '}
                <b>bài lớp {b.lop}</b> cùng chủ đề, học lại cho chắc rồi quay lên.
              </p>
              {/* Mở BÀI HỌC chứ không phải vòng luyện: con thiếu phần giảng, cho
                  làm thêm bài tập cùng kiểu chỉ sai thêm một lượt nữa. */}
              <div className="mt-3 flex flex-col gap-2">
                {bacDuoi?.bai.map((id, k) => (
                  <button key={id} className="btn-go" onClick={() => onMoBai(id, b.lop)}>
                    Học bài lớp {b.lop} · {bacDuoi.ten[k] || id} ▶
                  </button>
                ))}
              </div>
            </>
          )}

          {b.hanh === 'san' && (
            <div className="mt-3 rounded-2xl border-[1.5px] border-gold bg-gold-pale px-4 py-3.5 text-left text-[14.5px] leading-relaxed">
              <b className="text-navy">Chủ đề này chưa có bậc nào thấp hơn.</b>
              <p className="mt-1 text-mute">
                Con và bố mẹ cùng xem lại bài lớp {lop} một lượt nhé — đây là gốc
                của chủ đề, không lùi thêm được nữa.
              </p>
              <div className="mt-2 flex flex-col gap-2">
                {bac.bai.map((id, k) => (
                  <button key={id} className="btn-ghost text-left"
                          onClick={() => onMoBai(id, lop)}>
                    ◀ {bac.ten[k] || id}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <footer className="fixed inset-x-0 bottom-0 border-t border-line bg-white/95 px-3.5 py-2.5"
                style={{ paddingBottom: 'calc(.625rem + env(safe-area-inset-bottom))' }}>
          <div className="mx-auto flex max-w-[740px] gap-2.5">
            <button className="btn-ghost" onClick={onThoat}>Về bản đồ chủ đề</button>
            {b.hanh === 'len' && (
              <button className="btn-gold" onClick={() => onDoiBac(b.lop)}>
                Lên bậc lớp {b.lop} ▶
              </button>
            )}
            {(b.hanh === 'xuong' || b.hanh === 'san') && (
              <button className="btn-go" onClick={() => onDoiBac(lop)}>Luyện lại bậc này</button>
            )}
          </div>
        </footer>
      </div>
    );
  }

  /* ── ĐANG LÀM ──────────────────────────────────────────────────────────── */
  const q = cau[i];
  return (
    <div className="mx-auto max-w-[740px] px-3.5 pb-28 pt-4">
      {DauTrang}
      <div className="card">
        <div className="kicker">
          CÂU {i + 1} {'★'.repeat(q.muc + 1)}
          <span className="ml-2 font-normal normal-case tracking-normal text-mute">
            {q.tenBai}
          </span>
        </div>
        <p className="text-[16.5px] font-semibold leading-relaxed"><Chu t={q.text} /></p>

        <AnswerInput key={q.id} item={q} submitLabel="Kiểm tra" chotMotLan
                     onResolve={(r) => {
                       setRes(r);
                       if (r.ok) setDung((n) => n + 1);
                     }} />

        {res && (
          <div className={`mt-3 rounded-xl border-[1.5px] px-3.5 py-3 text-[15px] ${
            res.ok ? 'border-teal bg-teal-pale text-teal-dark'
                   : 'border-alert bg-alert-pale text-alert'}`}>
            {res.ok
              ? <><b>🎉 Đúng rồi!</b> <Chu t={q.solutionNarrative || ''} /></>
              : <><b>Chưa đúng.</b> Lời giải: <Chu t={q.solutionNarrative || res.expected} /></>}
          </div>
        )}
      </div>

      <footer className="fixed inset-x-0 bottom-0 border-t border-line bg-white/95 px-3.5 py-2.5"
              style={{ paddingBottom: 'calc(.625rem + env(safe-area-inset-bottom))' }}>
        <div className="mx-auto flex max-w-[740px] gap-2.5">
          <button className="btn-go" disabled={!res}
                  onClick={() => { setRes(null); setI(i + 1); }}>
            {res ? (i + 1 < cau.length ? 'Câu tiếp ▶' : 'Xem kết quả ▶')
                 : 'Con trả lời rồi bấm Kiểm tra'}
          </button>
        </div>
      </footer>
    </div>
  );
}
