import React from 'react';

/**
 * BẢY HÌNH VẼ TAY — chỗ emoji không diễn đạt nổi.
 *
 * 53/60 từ của lớp 1 dùng emoji: nhận ra ngay, không tốn dung lượng, nét ở mọi cỡ.
 * Bảy từ còn lại thì emoji chỉ GẦN đúng, và gần đúng với bé đang học từ mới là sai:
 *
 *     gate 🚧 biển công trường     head 👤 bóng người      hair 💇 đang cắt tóc
 *     top  🪀 yo-yo                lake 🏞️ phong cảnh chung
 *     run  🏃 · wash 🧼            động từ — emoji chỉ gợi một phần
 *
 * Vẽ ở đây bằng SVG nội tuyến chứ KHÔNG dựng tệp PNG như `figforge`, và đó là chủ ý:
 *
 *   · giữ đúng tính chất của lớp emoji — hình đi LIỀN với từ, không có tệp rời nào
 *     phải đồng bộ giữa `data/` · `public/` · `dist/` (cái bẫy quen của kho này);
 *   · nét vector nên sắc ở mọi cỡ, từ ô 40px trên danh sách tới ô 96px trong bài;
 *   · `figforge` chỉ dựng sơ đồ toán bằng matplotlib, không vẽ được vật.
 *
 * ── VẼ CHO BÉ 6 TUỔI ──
 * Nét dày, ít chi tiết, màu phẳng. Mỗi hình chỉ giữ đúng cái làm nó khác mọi thứ
 * còn lại trong unit ấy — cổng thì phải thấy song sắt và bản lề, con quay thì phải
 * thấy chóp nhọn và trục xoay. Thêm chi tiết là bé nhìn lâu hơn chứ không hiểu hơn.
 */

/* Màu lấy từ bảng MOBILUCK (tailwind.config.js) cộng vài màu tự nhiên — con dê phải
   ra màu dê, cái hồ phải ra màu nước, không ép vào màu thương hiệu. */
const M = {
  go: '#A9714B', goDam: '#7A4F33', nuoc: '#3FA9E0', nuocDam: '#1E7BAA',
  da: '#F2C79A', toc: '#3A2A20', ao: '#0B4EA8', vang: '#F9B233',
  do: '#C0392B', la: '#4CAF50', net: '#15263A', trang: '#FFFFFF',
};

const Khung = ({ children, ten }) => (
  <svg viewBox="0 0 64 64" role="img" aria-label={ten}
       className="h-[1em] w-[1em]" style={{ display: 'block' }}>
    {children}
  </svg>
);

const net = { stroke: M.net, strokeWidth: 2.4, strokeLinecap: 'round', strokeLinejoin: 'round', fill: 'none' };

/* ─────────── cái cổng ─────────── */
const Gate = () => (
  <Khung ten="cái cổng">
    <rect x="6" y="14" width="5" height="42" rx="2" fill={M.goDam} />
    <rect x="53" y="14" width="5" height="42" rx="2" fill={M.goDam} />
    <rect x="13" y="22" width="38" height="30" rx="2" fill={M.go} />
    <g {...net}>
      <rect x="13" y="22" width="38" height="30" rx="2" />
      <path d="M13 32h38M13 42h38M32 22v30M13 52l19-30M51 52L32 22" />
      <path d="M6 14h5M53 14h5" />
    </g>
    <circle cx="32" cy="37" r="2.6" fill={M.vang} stroke={M.net} strokeWidth="1.6" />
  </Khung>
);

/* ─────────── cái đầu ─────────── */
const Head = () => (
  <Khung ten="cái đầu">
    <path d="M32 8c11 0 18 8 18 18 0 12-8 20-18 20s-18-8-18-20c0-10 7-18 18-18z" fill={M.da} />
    <path d="M14 24c0-11 8-17 18-17s18 6 18 17c-4-6-10-8-18-8s-14 2-18 8z" fill={M.toc} />
    <ellipse cx="12" cy="30" rx="4" ry="5" fill={M.da} />
    <ellipse cx="52" cy="30" rx="4" ry="5" fill={M.da} />
    <g {...net}>
      <path d="M32 8c11 0 18 8 18 18 0 12-8 20-18 20s-18-8-18-20c0-10 7-18 18-18z" />
      <ellipse cx="12" cy="30" rx="4" ry="5" />
      <ellipse cx="52" cy="30" rx="4" ry="5" />
      <path d="M26 36q6 5 12 0" />
    </g>
    <circle cx="25" cy="27" r="2.2" fill={M.net} />
    <circle cx="39" cy="27" r="2.2" fill={M.net} />
    {/* cổ và vai: để bé thấy đây là CÁI ĐẦU trên người, không phải quả bóng */}
    <path d="M24 46h16v6H24z" fill={M.da} />
    <path d="M14 62c2-7 8-11 18-11s16 4 18 11z" fill={M.ao} />
    <g {...net}><path d="M14 62c2-7 8-11 18-11s16 4 18 11" /></g>
  </Khung>
);

/* ─────────── mái tóc ─────────── */
const Hair = () => (
  <Khung ten="mái tóc">
    <path d="M32 12c10 0 16 7 16 16 0 10-7 17-16 17s-16-7-16-17c0-9 6-16 16-16z" fill={M.da} />
    {/* Tóc là nhân vật chính: dài, xoã hai bên, chiếm phần lớn hình. */}
    <path d="M16 30c-1-14 7-22 16-22s17 8 16 22c2 10 1 18-2 26-1-10-3-16-5-20-4 3-9 4-9 4s-5-1-9-4c-2 4-4 10-5 20-3-8-4-16-2-26z"
          fill={M.toc} />
    <g {...net}>
      <path d="M16 30c-1-14 7-22 16-22s17 8 16 22c2 10 1 18-2 26-1-10-3-16-5-20-4 3-9 4-9 4s-5-1-9-4c-2 4-4 10-5 20-3-8-4-16-2-26z" />
      <path d="M24 36q8 6 16 0" />
    </g>
    <circle cx="26" cy="30" r="1.9" fill={M.net} />
    <circle cx="38" cy="30" r="1.9" fill={M.net} />
  </Khung>
);

/* ─────────── con quay ─────────── */
const Top = () => (
  <Khung ten="con quay">
    <path d="M32 8v10" {...net} />
    <ellipse cx="32" cy="24" rx="22" ry="8" fill={M.do} />
    <path d="M10 24c0 12 12 22 22 30 10-8 22-18 22-30z" fill={M.vang} />
    <path d="M32 54c-6-5-12-11-16-18 5 3 10 4 16 4s11-1 16-4c-4 7-10 13-16 18z" fill={M.do} />
    <g {...net}>
      <ellipse cx="32" cy="24" rx="22" ry="8" />
      <path d="M10 24c0 12 12 22 22 30 10-8 22-18 22-30" />
    </g>
    {/* trục xoay — dấu hiệu duy nhất phân biệt con quay với cái nón */}
    <path d="M32 54v4" {...net} />
    <circle cx="32" cy="18" r="3" fill={M.trang} stroke={M.net} strokeWidth="2" />
  </Khung>
);

/* ─────────── cái hồ ─────────── */
const Lake = () => (
  <Khung ten="cái hồ">
    <path d="M2 46c6-3 10-8 14-14 4-6 10-10 16-10s12 4 16 10c4 6 8 11 14 14v14H2z" fill={M.la} />
    {/* Mặt nước là hình bầu dục KHÉP KÍN — đó là chỗ khác biệt với biển hay sông. */}
    <ellipse cx="32" cy="44" rx="24" ry="13" fill={M.nuoc} />
    <ellipse cx="32" cy="44" rx="24" ry="13" fill="none" stroke={M.nuocDam} strokeWidth="2.4" />
    <g stroke={M.trang} strokeWidth="2" strokeLinecap="round" fill="none" opacity="0.85">
      <path d="M18 42q4-2 8 0M34 47q4-2 8 0M26 51q4-2 8 0" />
    </g>
    <g {...net}>
      <path d="M2 46c6-3 10-8 14-14 4-6 10-10 16-10s12 4 16 10c4 6 8 11 14 14" />
    </g>
  </Khung>
);

/* ─────────── chạy ─────────── */
const Run = () => (
  <Khung ten="chạy">
    <circle cx="40" cy="13" r="7" fill={M.da} stroke={M.net} strokeWidth="2.4" />
    <g {...net} strokeWidth="5">
      {/* Thân nghiêng về trước + hai chân mở rộng = đang CHẠY, không phải đang đứng. */}
      <path d="M38 22l-6 14" />
      <path d="M32 36l-9 16M32 36l12 10" />
      <path d="M36 26l-14 2M36 26l13 8" />
    </g>
    <g stroke={M.teal || '#1FCBAB'} strokeWidth="2.6" strokeLinecap="round" fill="none" opacity="0.9">
      <path d="M8 20h9M5 28h7M9 36h6" />
    </g>
  </Khung>
);

/* ─────────── rửa ─────────── */
const Wash = () => (
  <Khung ten="rửa">
    <path d="M8 8h6v16h22" fill="none" stroke={M.net} strokeWidth="4" strokeLinecap="round" />
    <rect x="34" y="20" width="8" height="8" rx="2" fill={M.net} />
    <g stroke={M.nuoc} strokeWidth="3" strokeLinecap="round" fill="none">
      <path d="M38 30v8M34 32v5M42 32v5" />
    </g>
    {/* Hai bàn tay hứng nước — việc RỬA nằm ở đôi tay, không ở bánh xà phòng. */}
    <path d="M20 46c0-5 5-8 12-8s12 3 12 8c0 4-5 7-12 7s-12-3-12-7z" fill={M.da} />
    <g {...net}>
      <path d="M20 46c0-5 5-8 12-8s12 3 12 8c0 4-5 7-12 7s-12-3-12-7z" />
      <path d="M26 44v6M32 43v7M38 44v6" strokeWidth="1.8" />
    </g>
    <g fill="none" stroke={M.trang} strokeWidth="2">
      <circle cx="22" cy="38" r="3" /><circle cx="44" cy="40" r="2.4" /><circle cx="30" cy="34" r="2" />
    </g>
  </Khung>
);

const BO = { gate: Gate, head: Head, hair: Hair, top: Top, lake: Lake, run: Run, wash: Wash };

/**
 * Vẽ hình của một từ. `hinh` là emoji (chuỗi), `ve` là khoá của bộ hình vẽ tay.
 * Có `ve` thì ưu tiên hình vẽ; không thì dùng emoji; không có gì thì dấu hỏi.
 */
export default function HinhVe({ ve, hinh, ten = '' }) {
  const V = ve && BO[ve];
  if (V) return <V />;
  return <span role="img" aria-label={ten}>{hinh || '❔'}</span>;
}

export const COI_HINH = Object.keys(BO);
