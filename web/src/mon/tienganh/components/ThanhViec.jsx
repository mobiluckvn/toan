import React from 'react';
import HinhVe from './HinhVe.jsx';
import { TT_VIEC } from '../lib/dandat.js';

/**
 * THANH VIỆC CỦA CON — bé nhìn vào là biết đã làm gì, còn phải làm gì.
 *
 * ── VÌ SAO KHÔNG PHẢI MỘT DÒNG CHỮ ──
 * Điều kiện đi tiếp trước đây nằm ở dòng "Con xem hết video, hoặc bấm 🔈 nghe đủ
 * 3 từ, rồi đi tiếp nhé." Bé lớp 1 chưa đọc được — mà cả quyển này dựng đúng trên
 * nguyên tắc không bắt bé đọc chữ. Nên chỗ chỉ đường phải là HÌNH.
 *
 * ── MỘT Ô LÀ MỘT VIỆC, VÀ Ô ẤY PHẢI BẤM ĐƯỢC ──
 * Biết mình thiếu gì mà không tới được chỗ ấy thì mới đi nửa đường. Bấm vào ô là
 * cuộn thẳng tới thẻ từ đó và làm nó sáng lên một nhịp — bé 6 tuổi lần theo được
 * mà không cần ai đọc hộ.
 *
 * ── VÌ SAO MỖI Ô CÓ HAI CHẤM NHỎ 🔈 🎤 ──
 * Một ô "chưa xong" chưa đủ: bé không biết còn thiếu NGHE hay thiếu NÓI. Tách
 * thành hai ô riêng thì bài 4 từ thành 9 ô, màn nhỏ phải cuộn ngang. Nên: một ô
 * cho một từ, và hai chấm nhỏ trong ô nói rõ còn thiếu việc nào.
 *
 * ── MÀU KHÔNG ĐƯỢC LÀ THỨ DUY NHẤT MANG TIN ──
 * Xong thì có thêm dấu ✓, chưa xong thì viền nét đứt. Bé không phân biệt được
 * xanh với xám vẫn đọc được thanh này, và ảnh chụp đen trắng cũng vậy.
 */
export default function ThanhViec({
  viec = [], conThieu = 0, mo = false, vuongMicro = false, dangO = null, onChon,
  /* Hai chỗ đổi được tiêu đề và dòng mô tả — thêm cho việc V7 (thanh KẾ HOẠCH
     BUỔI ở phòng luyện nói). Cùng một thanh, cùng một cách đọc: một ô một việc,
     xong thì ✓, chưa xong thì nét đứt. Dựng một thanh thứ hai gần giống thì bé
     phải học hai cách đọc cho cùng một ý. */
  ten = 'Việc của con', loiRieng = null,
}) {
  if (!viec.length) return null;

  /* Ba câu cho ba tình huống, và cái ở giữa mới là cái phải cẩn thận: bé nghe đủ
     mọi từ nhưng chưa xem video thì nút ĐÃ MỞ trong khi vẫn còn một ô trắng. Nói
     "Còn 1 việc nữa" lúc ấy là thanh cãi nhau với cái nút ngay bên dưới — bé 6
     tuổi gặp hai tín hiệu ngược nhau thì tin cái nào cũng sai. */
  const loi = loiRieng || (conThieu === 0 ? 'Xong hết rồi — giỏi lắm!'
    : mo ? 'Con đi tiếp được rồi. Ô nào còn trắng thì làm thêm cũng hay.'
      : `Còn ${conThieu} việc nữa.`);

  return (
    <section
      aria-label={`${ten} trong phần này`}
      className="flex flex-col gap-2 rounded-xl2 border-2 border-line bg-white p-3"
    >
      <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
        <h3 className="text-sm font-bold uppercase tracking-wide text-navy">{ten}</h3>
        {/* Dòng này cho bố mẹ và cho máy đọc màn hình. Bé đọc thanh ô bên dưới. */}
        <p className="text-sm text-mute">{loi}</p>
      </div>

      <ol className="flex flex-wrap gap-2">
        {viec.map((x) => (
          <ONhiemVu key={x.ma} viec={x} dangO={x.ma === dangO} onChon={onChon} />
        ))}
      </ol>

      {vuongMicro && (
        <p className="rounded-xl2 bg-gold-pale p-2 text-sm text-gold-dark">
          Máy chưa nghe được nên phần nói để lúc khác — con cứ học tiếp bình thường nhé.
        </p>
      )}
    </section>
  );
}

/* Bốn dáng của một ô. Gom thành bảng để không rải `className` dài khắp nơi. */
const DANG = {
  [TT_VIEC.chua]: 'border-dashed border-line bg-soft',
  [TT_VIEC.dang]: 'border-gold bg-gold-pale',
  [TT_VIEC.xong]: 'border-teal bg-teal-pale',
  hong: 'border-dashed border-gold bg-white',
};

function ONhiemVu({ viec: x, dangO, onChon }) {
  const xong = x.tt === TT_VIEC.xong;
  const dat = x.mucNoi === 'dat';
  const viecCon = x.viecCon || [];

  /* Nhãn cho máy đọc màn hình: đọc ĐỦ từng việc con, vì bé dùng máy đọc thì
     không thấy được mấy chấm nhỏ. Sinh từ chính `viecCon` nên thêm một việc mới
     là nhãn tự có, không phải nhớ sửa ở hai nơi. */
  const keViec = viecCon
    .map((c) => (c.sao ? `${c.ten} được rồi`
      : c.xong ? `đã ${c.ten}`
        : c.boQua ? `phần ${c.ten} để lúc khác` : `chưa ${c.ten}`))
    .join(', ');
  const nhanDayDu = x.tt === 'hong'
    ? `${x.nhan} — không tải được, bỏ qua`
    : `${x.nhan}${x.nghia ? ` (${x.nghia})` : ''}`
      + `${keViec ? ` — ${keViec}` : ` — ${xong ? 'xong' : 'chưa xong'}`}`
      + `${dangO ? ' — con đang ở đây' : ''}`;

  return (
    <li>
      <button
        type="button"
        onClick={() => onChon?.(x)}
        aria-label={nhanDayDu}
        aria-current={dangO ? 'true' : undefined}
        className={`flex w-[4.5rem] flex-col items-center gap-1 rounded-xl2 border-2 p-2
          transition hover:brightness-95
          focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
          ${dangO ? 'ring-4 ring-navy' : ''}
          ${DANG[x.tt] || DANG[TT_VIEC.chua]}`}
      >
        <span className={`relative text-3xl leading-none ${xong ? '' : 'opacity-70'}`}>
          {x.bieuTuong
            ? (
              <span aria-hidden="true">
                {x.bieuTuong}
                {/* Bài lớp 3 có tới BỐN video từ mới, và bốn ô 🎬 giống hệt nhau thì
                    bé không biết mình còn thiếu cái nào — đúng cái mà thanh việc
                    sinh ra để tránh. Đánh số ngay trên biểu tượng. */}
                {x.tong > 1 && (
                  <span className="absolute -left-1 -top-1 rounded-full bg-navy px-1.5
                    text-xs font-bold text-white">{x.thuTu}</span>
                )}
              </span>
            )
            /* Từ không có hình thì `HinhVe` hiện CHÍNH CHỮ ấy chứ không vẽ ❔ — sửa
               ở đó, một chỗ cho cả ba màn cùng vẽ hình từ. */
            : <HinhVe ten={x.nhan} ve={x.ve} hinh={x.hinh} />}
          {(xong || dat) && (
            <span aria-hidden="true"
              className={`absolute -right-2 -top-1 rounded-full px-1 text-xs font-bold
                ${dat ? 'bg-gold text-gold-dark' : 'bg-teal text-white'}`}>
              {dat ? '⭐' : '✓'}
            </span>
          )}
        </span>

        {viecCon.length > 0 && (
          <span aria-hidden="true" className="flex gap-1 text-[0.65rem] leading-none">
            {viecCon.map((c) => <Cham key={c.ma} {...c} />)}
          </span>
        )}
      </button>
    </li>
  );
}

const Cham = ({ xong, boQua, chu }) => (
  <span className={`rounded-full px-1 py-[0.1rem]
    ${xong ? 'bg-teal text-white' : boQua ? 'bg-line text-mute line-through' : 'bg-white text-mute opacity-60'}`}>
    {chu}
  </span>
);
