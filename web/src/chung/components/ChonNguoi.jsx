import React from 'react';
import { dsNguoi, tenHien, chuDau } from '../lib/nguoiDung.js';

const MAU = [
  'bg-navy', 'bg-teal', 'bg-gold-dark', 'bg-alert', 'bg-navy-light',
];

/**
 * AI ĐANG HỌC? — màn đầu tiên khi máy nhớ nhiều hơn một bé.
 *
 * Nhà có anh lớp 5 và em lớp 2 dùng chung máy tính bảng. Trước đây đổi bé nghĩa là
 * thoát ra, gõ email bé kia, mở hộp thư lấy mã — nên thực tế cả nhà dùng chung một
 * tài khoản và hai sổ học trộn vào nhau. Nay mỗi bé giữ phiên riêng, bấm tên là vào.
 *
 * Vòng tròn chữ cái đầu là để bé CHƯA ĐỌC THẠO vẫn nhận ra chỗ của mình — bé lớp 2
 * nhìn chữ "M" của Minh nhanh hơn đọc cả dòng email.
 */
export default function ChonNguoi({ onChon, onThemNguoi, onQuenNguoi }) {
  const ds = dsNguoi();

  return (
    <div className="mx-auto flex min-h-[100dvh] max-w-[520px] flex-col justify-center px-4 py-8">
      <div className="text-center">
        <div className="text-[11px] font-extrabold tracking-widest text-gold-dark">
          MOBILUCK · KỸ SƯ NHÍ
        </div>
        <h1 className="mt-1 text-[22px] font-bold text-navy">Ai đang học nhỉ?</h1>
        <p className="mt-1 text-[13.5px] text-mute">Bấm vào tên con để vào học.</p>
      </div>

      <div className="mt-5 flex flex-col gap-2.5">
        {ds.map((n, i) => (
          <div key={n.cho} className="flex items-center gap-2">
            <button
              onClick={() => onChon(n)}
              className="flex flex-1 items-center gap-3 rounded-2xl border-[1.5px] border-line bg-white px-3.5 py-3 text-left active:scale-[.99]">
              <span className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-full text-[19px] font-extrabold text-white ${MAU[i % MAU.length]}`}>
                {chuDau(n)}
              </span>
              <span className="min-w-0 flex-1">
                <b className="block truncate text-[15.5px] text-navy">{tenHien(n)}</b>
                <span className="text-[12.5px] text-mute">
                  {n.lop ? `Lớp ${n.lop}` : 'chưa chọn lớp'}
                  {n.email ? ` · ${n.email}` : ''}
                </span>
              </span>
              <span className="text-mute">▸</span>
            </button>
            {/* Bỏ khỏi máy — chỉ xoá khỏi danh sách của máy này, tài khoản vẫn nguyên */}
            <button
              onClick={() => onQuenNguoi(n)}
              aria-label={`Bỏ ${tenHien(n)} khỏi máy này`}
              title="Bỏ khỏi máy này (tài khoản vẫn còn)"
              className="shrink-0 rounded-full border border-line px-2 py-1 text-[11px] text-mute">
              ✕
            </button>
          </div>
        ))}
      </div>

      <button onClick={onThemNguoi}
              className="mt-4 rounded-2xl border-[1.5px] border-dashed border-line px-3.5 py-3 text-[14px] font-bold text-navy">
        + Thêm bé khác
      </button>

      <p className="mt-4 text-center text-[12px] leading-relaxed text-mute">
        Mỗi bé một sổ học riêng. Bấm ✕ chỉ bỏ tên khỏi máy này thôi —
        bài của con vẫn còn nguyên trên mạng.
      </p>
    </div>
  );
}
