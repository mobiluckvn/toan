import React, { useEffect, useState } from 'react';
import { CONTENT, dongDau } from '../lib/content.js';
import CuonThem from './CuonThem.jsx';
import NhietKeHieuBai from './NhietKeHieuBai.jsx';
import Figure from './Figure.jsx';
import AnswerInput from './AnswerInput.jsx';

/**
 * BÀI HỌC LỚP 2 — đi lần lượt 7 mục con đọc, mục "Góc bố mẹ" để riêng cuối bài.
 *
 * Khác phòng học lớp 5: bé 7-8 tuổi đọc chậm, nên mỗi màn CHỈ MỘT MỤC, chữ to,
 * và luôn thấy mình đang ở bước mấy trên mấy. Câu luyện tập cho bé làm ra vở rồi
 * mở lời chữa để tự so — đúng như sách dặn, không ép nhập liệu.
 */
const MUC = [
  ['mucTieu', '🎯', 'Bài này con học gì'],
  ['chuyenMoBai', '📖', 'Chuyện mở bài'],
  ['khamPha', '🔍', 'Cùng khám phá'],
  ['viDuMau', '✏️', 'Bài mẫu'],
  ['suKemNham', '🙃', 'Su Kem nhầm rồi'],
  ['luyenTap', '💪', 'Con luyện tập'],
  ['quiz', '⭐', 'Con hiểu bài chưa'],
];

export default function Lop2Player({ baiId, onExit, onXong }) {
  const [bai, setBai] = useState(null);
  const [loi, setLoi] = useState(null);
  const [i, setI] = useState(0);
  const [mo, setMo] = useState({});          // mã câu → đã mở lời chữa chưa

  useEffect(() => {
    const ten = baiId.replace('DL:', 'DL_').replace(/\./g, '_');
    fetch(dongDau(`${CONTENT}/lop2/${ten}.json`))
      .then((r) => { if (!r.ok) throw new Error('không mở được bài'); return r.json(); })
      .then(setBai).catch((e) => setLoi(String(e?.message || e)));
  }, [baiId]);
  useEffect(() => { window.scrollTo(0, 0); }, [i]);

  if (loi) return <div className="p-6 text-alert">{loi}</div>;
  if (!bai) return <div className="p-6 text-mute">Đang mở bài học…</div>;

  const [ma, bieu, nhan] = MUC[i];
  const m = bai.muc[ma] || { dong: [] };
  const cauCuaMuc = bai.cau.filter((c) => c.phan === ma);
  const cuoi = i === MUC.length - 1;

  return (
    <div className="flex flex-col min-h-[100dvh]">
      <header className="sticky top-0 z-20 flex items-center gap-2.5 bg-navy px-3.5 py-2 text-white">
        <button onClick={onExit}
                className="rounded-full border border-white/40 px-2 py-0.5 text-[11px] font-bold">
          ⌂ Thoát
        </button>
        <span className="rounded bg-gold px-1.5 py-0.5 text-[11px] font-extrabold text-gold-dark">
          Bài {bai.so}
        </span>
        <h1 className="flex-1 text-[13px] font-semibold leading-tight line-clamp-2">{bai.ten}</h1>
      </header>

      {/* Bé cần thấy rõ đang ở bước mấy — đốt to hơn của lớp 5 cho dễ bấm */}
      <div className="border-b border-line bg-white px-3 pb-1.5 pt-2">
        <div className="mb-1 flex items-center gap-2 text-[12px]">
          <button disabled={i === 0} onClick={() => setI(i - 1)}
                  className="rounded-full border-[1.5px] border-navy px-2.5 py-0.5 font-bold text-navy disabled:border-line disabled:text-mute disabled:opacity-45">
            ◀ Quay lại
          </button>
          <span className="flex-1 text-center font-bold text-navy">
            Bước {i + 1} trên {MUC.length}
          </span>
        </div>
        <div className="flex gap-1">
          {MUC.map(([k], j) => (
            <button key={k} disabled={j > i} onClick={() => setI(j)}
                    className={`h-2 flex-1 rounded-full ${
                      j < i ? 'bg-teal' : j === i ? 'bg-teal ring-2 ring-navy' : 'bg-teal-pale'}`} />
          ))}
        </div>
      </div>

      <main className="mx-auto w-full max-w-[740px] flex-1 px-3.5 pb-32 pt-4">
        <div className="card">
          <div className="kicker">{bieu} {nhan}</div>
          {m.dong.map((d, k) => (
            <React.Fragment key={k}>
              <p className={`${k ? 'mt-2.5' : ''} text-[17px] leading-relaxed`}>{d}</p>
              {/* hình đứng ngay sau dòng nó minh hoạ, đúng chỗ sách đặt */}
              {(m.hinh || []).filter((h) => h.sauDong === k).map((h) => (
                <Figure key={h.id} fig={h} />
              ))}
            </React.Fragment>
          ))}
          {m.dong.length === 0 && cauCuaMuc.length === 0 && (
            <p className="text-[15px] text-mute">Mục này không có nội dung.</p>
          )}
        </div>

        {cauCuaMuc.map((c) => (
          <div key={c.id} className="card">
            <div className="kicker">
              CÂU {c.so}{c.muc > 1 ? ` · ${'★'.repeat(c.muc)}` : ''}
            </div>
            <p className="text-[17px] font-semibold leading-snug">{c.text}</p>

            {c.tuLuan === false ? (
              /* Quiz: sách ghi sẵn đáp án Đúng/Sai và A·B·C nên bấm chọn là chấm được ngay.
                 Bé 7 tuổi cần biết đúng/sai LIỀN, đợi tới cuối bài thì quên mất mình chọn gì. */
              <AnswerInput item={c} submitLabel="Con chọn xong rồi" />
            ) : (
              <>
                <p className="mt-2 text-[14px] text-mute">
                  Con làm ra vở nhé. Làm xong rồi hãy mở lời giải để tự chấm.
                </p>
                {mo[c.id] ? (
                  <div className="mt-2 rounded-xl border-[1.5px] border-teal bg-teal-pale px-3.5 py-3 text-[16px]">
                    <b>Lời giải:</b> {c.loiChua || '(sách không ghi lời giải cho câu này)'}
                  </div>
                ) : (
                  <button className="btn-ghost mt-2" onClick={() => setMo({ ...mo, [c.id]: true })}>
                    Con làm xong rồi — xem lời giải
                  </button>
                )}
              </>
            )}
          </div>
        ))}

        {/* Sách in "nhiệt kế" này ở cuối cả 33 bài, ngay sau quiz — xem
            NhietKeHieuBai.jsx về lý do làm giao diện thay vì dựng 33 ảnh */}
        {ma === 'quiz' && <NhietKeHieuBai key={bai.id} />}

        {cuoi && bai.muc.gocBoMe && (
          <details className="card">
            <summary className="cursor-pointer text-[13.5px] font-bold text-mute">
              👨‍👩‍👧 Góc bố mẹ (dành cho người lớn)
            </summary>
            {bai.muc.gocBoMe.dong.map((d, k) => (
              <p key={k} className="mt-2 text-[14.5px] leading-relaxed text-mute">{d}</p>
            ))}
          </details>
        )}
      </main>

      <footer className="fixed inset-x-0 bottom-0 border-t border-line bg-white/95 px-3.5 py-2.5 backdrop-blur"
              style={{ paddingBottom: 'calc(.625rem + env(safe-area-inset-bottom))' }}>
        <div className="mx-auto flex max-w-[740px] gap-2.5">
          {cuoi ? (
            <button className="btn-gold" onClick={() => onXong?.(bai.id)}>Con học xong bài này 🌟</button>
          ) : (
            <button className="btn-go" onClick={() => setI(i + 1)}>Tiếp ▶</button>
          )}
        </div>
      </footer>
      <CuonThem />
    </div>
  );
}
