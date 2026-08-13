import React from 'react';

/**
 * DÃY CHẤM — tiến độ cho chặng có NHIỀU CÂU (luyện tập, sát hạch, kỳ ôn tập).
 *
 * ── VÌ SAO KHÔNG DÙNG Ô CÓ HÌNH NHƯ THANH VIỆC ──
 * Thanh VIỆC CỦA CON vẽ mỗi việc một ô có hình, hợp khi có 4–5 việc. Mức luyện
 * tập có 9–16 câu: 16 ô hình thì tràn màn, và bản thân câu hỏi cũng không có
 * "hình đại diện" nào cho ra hồn. Nên ở đây mỗi câu chỉ còn một CHẤM.
 *
 * ── VÌ SAO KHÔNG DÙNG MỘT THANH LẤP ĐẦY ──
 * Thanh lấp đầy nói được "còn bao nhiêu", nhưng không nói được câu nào bé ĐỂ LẠI
 * SAU — mà đúng mấy câu ấy là món nợ cuối mức sẽ đòi lại. Dãy chấm nói được cả
 * hai, vẫn gọn.
 *
 * ── VÌ SAO KHÔNG DÙNG DÒNG "Câu 4/9" ──
 * Đó là CHỮ và SỐ. Bé lớp 1 chưa đọc thạo, và đó đúng là cái lỗi vừa phải sửa ở
 * chặng Từ mới. Dòng chữ vẫn còn, nhưng để cho bố mẹ — bé đọc dãy chấm.
 *
 * Bốn dáng chấm, và cả bốn KHÁC NHAU VỀ HÌNH chứ không chỉ khác màu:
 *   ● đúng rồi     ◍ để lại sau (vòng có lõi)   ○ chưa tới (nét đứt)   ◉ đang ở đây
 */
export default function ThanhCau({ tong = 0, tt = [], tai = -1, nhan = 'Các câu trong phần này' }) {
  /* Một chấm đơn độc không nói được gì — "còn 1 việc" thì bản thân màn hình đã là
     câu trả lời. Vẽ ra chỉ tổ chiếm chỗ và làm bé phải đoán xem nó nghĩa là gì.
     Có thật ở Unit 5: hội thoại chỉ có MỘT lượt của bé. */
  if (tong < 2) return null;
  const xong = tt.filter((x) => x === 'dung').length;
  const no = tt.filter((x) => x === 'no').length;

  return (
    <div className="flex flex-col gap-1">
      <ol aria-label={nhan} className="flex flex-wrap items-center gap-1.5">
        {Array.from({ length: tong }, (_, k) => (
          <ChamCau key={k} so={k + 1} tt={tt[k]} tai={k === tai} />
        ))}
      </ol>
      {/* Cho bố mẹ và cho máy đọc màn hình. Bé đọc dãy chấm ở trên. */}
      <p className="text-xs text-mute">
        {`Đúng ${xong}/${tong}`}
        {no > 0 && ` · ${no} câu để lại sau`}
      </p>
    </div>
  );
}

const DANG = {
  dung: 'border-teal bg-teal',
  no: 'border-gold bg-gold-pale',
  sai: 'border-gold bg-gold-pale',
};

function ChamCau({ so, tt, tai }) {
  const chu = tt === 'dung' ? `Câu ${so}: đúng rồi`
    : tt === 'no' ? `Câu ${so}: để lại sau`
      : tai ? `Câu ${so}: con đang ở đây` : `Câu ${so}: chưa tới`;
  return (
    <li
      title={chu}
      aria-label={chu}
      aria-current={tai ? 'true' : undefined}
      className={`h-4 w-4 rounded-full border-2 transition
        ${DANG[tt] || 'border-dashed border-line bg-white'}
        ${tai ? 'ring-4 ring-navy/30 scale-125' : ''}`}
    >
      {/* Lõi của chấm "để lại sau" — để nó khác HÌNH với chấm đúng, không chỉ
          khác màu; bé không phân biệt được xanh với vàng vẫn đọc được dãy này. */}
      {tt === 'no' && (
        <span aria-hidden="true" className="block h-full w-full scale-50 rounded-full bg-gold" />
      )}
    </li>
  );
}
