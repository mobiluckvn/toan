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
 */
export default function CauNgheNhin({ cau, onXong }) {
  const tra = (v) => onXong?.({ dung: v === cau.answerKey.value });
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
