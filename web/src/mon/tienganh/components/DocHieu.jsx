import React, { useState } from 'react';
import CauHoi from './CauHoi.jsx';
import NutNghe from './NutNghe.jsx';

/**
 * BÀI ĐỌC HIỂU NGẮN — mỗi chương một bài. Bác chốt 18-08-2026.
 *
 * ── VIỆC MỚI, KHÔNG PHẢI MÀN MỚI ──
 * Cả quyển tới giờ dạy NGHE và NÓI: bé nghe một từ rồi bấm hình, nghe một câu rồi
 * nhắc lại. Đọc thì chưa có chỗ nào. Đây là chỗ ấy — và nó khác kỳ ôn tập ở đúng
 * một điểm: câu trả lời KHÔNG nằm trong đầu bé, nó nằm trên màn hình. Bé phải đọc
 * lại đoạn văn để tìm.
 *
 * ── ĐOẠN VĂN Ở LẠI TRÊN MÀN, SUỐT CẢ BÀI ──
 * Đây là điều quan trọng nhất của màn này, và cũng là chỗ dễ làm sai nhất: giấu
 * đoạn văn đi rồi hỏi thì bài hoá ra bài KIỂM TRA TRÍ NHỚ, không phải bài đọc hiểu.
 * Bé lớp 3 đọc tiếng Anh còn chậm, tra đi tra lại là chuyện bình thường và đúng —
 * người lớn đọc hợp đồng cũng làm thế.
 *
 * ── MỖI DÒNG MỘT NÚT NGHE ──
 * Bé mới học đọc thì mặt chữ và tiếng chưa dính vào nhau. Nghe được dòng nào chưa
 * đọc nổi là bé tự nối được hai thứ ấy. Clip đã có sẵn — mọi câu trong đoạn đều là
 * câu SGK của chính bốn bài trong chương (xem `tools/sinh_dochieu_tienganh.py`),
 * nên không phải sinh thêm tiếng cho màn này.
 *
 * ── KHÔNG GHI VÀO HỌC BẠ MÁY CHỦ ──
 * Kết quả ghi ở sổ TẠI MÁY (`ghiDocHieu`). `hocBaTA` chỉ nhận `loai: 'chuong'`, mà
 * thêm một `loai` thì phải sửa `firestore.rules` · bên gửi · bên đọc rồi deploy
 * rules — xem chú ở `progress.js`.
 */
export default function DocHieu({ bai, onXong, onThoat }) {
  const ds = bai?.cau || [];
  const [i, datI] = useState(0);
  const [dung, datDung] = useState(0);
  const [het, datHet] = useState(false);

  if (!ds.length) {
    return (
      <Khung ten={bai?.name} onThoat={onThoat}>
        <p className="text-alert">Bài đọc này chưa có câu hỏi.</p>
      </Khung>
    );
  }

  const can = bai.need || Math.max(2, ds.length - 1);

  if (het) {
    const dat = dung >= can;
    return (
      <Khung ten={bai.name} onThoat={onThoat}>
        <Doan doan={bai.doan} />
        <div className={`rounded-xl2 p-6 ${dat ? 'bg-teal-pale' : 'bg-gold-pale'}`}>
          <p className="text-5xl" aria-hidden="true">{dat ? '📖' : '💪'}</p>
          <p className="mt-2 text-3xl font-bold text-ink">{dung}/{ds.length} câu đúng</p>
          <p className={`mt-1 ${dat ? 'text-teal-dark' : 'text-gold-dark'}`}>
            {dat
              ? 'Con đọc hiểu được cả đoạn rồi!'
              : `Cần ${can} câu đúng. Con đọc lại đoạn ở trên rồi thử lại nhé — `
                + 'làm lại bao nhiêu lần cũng được.'}
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button type="button"
            onClick={() => { datI(0); datDung(0); datHet(false); }}
            className="rounded-xl2 border-2 border-navy px-5 py-3 font-semibold text-navy
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            Đọc lại từ đầu
          </button>
          <button type="button"
            onClick={() => onXong?.({ dat, dung, tong: ds.length })}
            className="rounded-xl2 bg-navy px-6 py-3 text-lg font-semibold text-white
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            Xong →
          </button>
        </div>
      </Khung>
    );
  }

  const q = ds[i];
  const tra = (r) => {
    if (r.dung) datDung((n) => n + 1);
    if (i + 1 < ds.length) datI(i + 1); else datHet(true);
  };

  return (
    <Khung ten={bai.name} onThoat={onThoat}>
      <Doan doan={bai.doan} />

      <div className="flex items-center gap-3">
        <p className="text-sm font-semibold text-mute">Câu {i + 1}/{ds.length}</p>
        <div className="h-2.5 flex-1 overflow-hidden rounded-full bg-line">
          <i className="block h-full bg-gold transition-all"
             style={{ width: `${(i / ds.length) * 100}%` }} />
        </div>
      </div>

      <div className="rounded-xl2 border-2 border-line bg-white p-5">
        {/* `key` buộc dựng lại mỗi câu — không có nó thì đáp án câu trước còn nằm
            trong ô, đúng cái bẫy đã vỡ một lần ở kỳ ôn tập. */}
        <CauHoi key={q.id} cau={q} onXong={tra} />
      </div>
    </Khung>
  );
}

/**
 * ĐOẠN HỘI THOẠI — luôn hiện, kể cả ở màn kết quả.
 *
 * ── VÌ SAO PHẢI HIỆN TÊN NGƯỜI NÓI ── (bác chốt 18-08-2026)
 * Bác đọc thử rồi bảo: "Bài đọc phải là một đoạn văn hoặc đoạn hội thoại có ý
 * nghĩa chứ không phải mấy câu rời rạc chẳng liên quan gì đến nhau."
 *
 * `sinh_dochieu_tienganh.py` nay dựng đoạn thành cuộc trò chuyện giữa HAI bạn, và
 * khai người nói ở `doan[].ai`. Không hiện tên ra thì công ấy mất sạch: trên màn
 * hình vẫn là mấy dòng chữ chồng nhau, bé vẫn không biết ai hỏi ai đáp.
 *
 * ⚠ `key` phải là VỊ TRÍ, không phải câu. Đoạn hội thoại được phép có hai dòng
 * trùng chữ — chính là lúc hai bạn hỏi lại nhau ("What's your name?" hỏi hai
 * lượt). Lấy câu làm khoá thì React thấy khoá trùng và nuốt mất một dòng.
 *
 * Bài cũ chưa có `ai` thì vẫn bày được, chỉ là không có tên — để một bản dựng cũ
 * còn nằm trong cache trình duyệt không làm bé mất hẳn đoạn đọc.
 */
function Doan({ doan = [] }) {
  const coVai = doan.some((d) => d.ai);
  return (
    <section className="rounded-xl2 border-2 border-navy bg-white p-4">
      <h2 className="mb-2 text-sm font-semibold uppercase tracking-wider text-mute">
        {coVai ? 'Hai bạn nói chuyện' : 'Con đọc đoạn này'}
      </h2>
      <ul className="flex flex-col gap-2">
        {doan.map((d, i) => (
          // eslint-disable-next-line react/no-array-index-key
          <li key={i} className="flex items-center gap-3">
            <NutNghe ma={d.am} nhan="Nghe câu này" />
            {d.ai && (
              <span className="w-16 flex-none text-right text-sm font-bold text-navy sm:w-20">
                {d.ai}
              </span>
            )}
            <span className="text-lg text-ink sm:text-xl">{d.cau}</span>
          </li>
        ))}
      </ul>
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
        <h1 className="flex-1 text-lg font-bold text-ink sm:text-xl">📖 {ten}</h1>
      </div>
      {children}
    </div>
  );
}
