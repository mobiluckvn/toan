import React from 'react';
import NutNghe from './NutNghe.jsx';
import HinhVe from './HinhVe.jsx';

/**
 * CÂU NGHE–NHÌN — nghe một từ, nhìn một hình, hình ấy có đúng không.
 *
 * Dạng câu KHÔNG BẮT ĐỌC MỘT CHỮ NÀO. Đó là cả lý do nó tồn tại: bản sát hạch đầu
 * tiên ra câu chữ tiếng Việt (`"ball" nghĩa là "quả bóng"`), nên 80 câu sát hạch
 * của cả quyển đều là câu bé lớp 1 chỉ ĐOÁN — mà đúng/sai thì đoán trúng một nửa,
 * và con số trong sổ bố mẹ thành con số rỗng.
 *
 * Tách ra thành component riêng vì nay có HAI chỗ dùng: sát hạch cuối bài, và kỳ
 * ôn tập chương. Để hai bản chép nhau thì sớm muộn cũng lệch — mà lệch ở đây
 * nghĩa là cùng một câu hỏi, hai chỗ chấm khác nhau.
 *
 * ── HAI DẠNG CÂU, VÀ VÌ SAO CẢ HAI Ở ĐÂY ──
 *   ĐÚNG/SAI      nghe một từ, nhìn một hình, hình ấy có đúng không (408 câu)
 *   NGHE → CHỌN   nghe một từ, chọn nghĩa trong bốn ô (62 câu)
 *
 * Dạng thứ hai là phần BÙ của bộ sinh: câu đúng/sai chỉ dựng được từ từ CÓ HÌNH,
 * mà lớp 3 có 51/204 từ không vẽ được và lớp 5 thì phần lớn từ vựng là cụm việc.
 * Bài nào thiếu thì bù bằng dạng nghe-chọn — vẫn kiểm đúng một việc: bé nối được
 * ÂM với NGHĨA hay không.
 *
 * ⚠ LỖI ĐÃ CHẠY TRÊN BẢN THẬT, sửa 22-08-2026. `SatHach` dựng component này cho
 * MỌI câu, trong khi bản cũ chỉ biết dạng đúng/sai: nó đọc `answerKey.value`, mà
 * câu nghe-chọn thì khoá là `answerKey.choice`. `value` là `undefined`, nên
 * `v === undefined` sai với CẢ HAI nút — bé bấm gì cũng bị chấm sai. 62 câu như
 * thế trên ba quyển, và 9 bài mà CẢ kỳ sát hạch không có lấy một câu trả lời đúng
 * được. Không cổng nào bắt: dữ liệu đủ và đúng, bản dựng xanh, chỉ đường vẽ là
 * hỏng — mà đường vẽ thì phải mở ra nhìn mới thấy.
 *
 * `OnTap.jsx` KHÔNG dính vì nó rẽ nhánh theo `q.nhinNghe` từ đầu. Cùng một dữ
 * liệu, hai màn, một màn đúng một màn sai — đúng dạng lỗi ở CHỖ NỐI mà không tệp
 * nào sở hữu.
 *
 * ── MỘT LƯỢT, KHÔNG THỬ LẠI ──
 * Sửa ở đây chứ không phải cho `SatHach` gọi `CauHoi` như `OnTap` làm: `CauHoi`
 * cho bé thử lại tới khi đúng. Ôn tập thì được, sát hạch thì không — và trộn hai
 * lối trong CÙNG một kỳ 5 câu (3 câu một lượt, 2 câu thử mãi) thì con số cuối
 * cùng không còn nghĩa gì.
 */
export default function CauNgheNhin({ cau, onXong }) {
  const k = cau.answerKey || {};
  /* Câu nghe-chọn: khoá là `choice`, và có `choices` để bày ra. */
  if (cau.choices?.length) {
    const tra = (v) => onXong?.({ dung: v === k.choice });
    return (
      <div className="flex flex-col gap-4">
        <div className="flex flex-col items-center gap-3">
          <NutNghe ma={cau.am} to nhan="Nghe lại" tuDong key={cau.id} />
          <p className="text-lg text-ink">{cau.text}</p>
        </div>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          {cau.choices.map((x) => (
            <button key={x} type="button" onClick={() => tra(x)}
              className="rounded-xl2 border-2 border-line bg-white px-4 py-4 text-left text-lg
                text-ink hover:border-navy
                focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
              {x}
            </button>
          ))}
        </div>
      </div>
    );
  }

  const tra = (v) => onXong?.({ dung: v === k.value });
  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col items-center gap-3">
        {/* Tự phát khi vào câu mới: bé chưa đọc được đề, tiếng phải tới trước.
            `key` buộc dựng lại nút cho mỗi câu, nếu không clip câu trước còn treo. */}
        <NutNghe ma={cau.am} to nhan="Nghe lại" tuDong key={cau.id} />
        <span className="text-7xl leading-none sm:text-8xl">
          <HinhVe ve={cau.anhVe} hinh={cau.anh} ten="hình" />
        </span>
        <p className="text-lg text-mute">Hình này có đúng không?</p>
      </div>
      <div className="flex gap-3">
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
  );
}
