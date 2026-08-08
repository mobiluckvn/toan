/** Bảng màu MOBILUCK — dùng chung với FigForge để hình và giao diện đồng bộ */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      /**
       * Rút từ icon thương hiệu (icon/icon.jpg): khiên gradient lục lam → xanh
       * dương, chữ M cam vàng.
       *   navy ← xanh sâu của khiên (#1260CC), hạ sáng để chữ trắng đọc được
       *   teal ← lục lam khiên (#23D2B3)
       *   gold ← cam của chữ M (#FFA02C)
       *
       * Màu icon rất tươi nên phần lớn KHÔNG đủ tương phản để làm chữ. Giữ nguyên
       * cấu trúc ba vai (màu chính · biến thể đậm để viết chữ · biến thể nhạt làm
       * nền) và đã đo lại cả 10 cặp thật sự dùng trong app — thấp nhất 4,75.
       *
       * ĐỔI Ở ĐÂY THÌ PHẢI ĐỔI CẢ figforge/core.py rồi vẽ lại 672 hình,
       * nếu không hình và giao diện đá màu nhau.
       */
      colors: {
        navy: { DEFAULT: '#0B4EA8', light: '#1268D6', deep: '#06326E' },
        teal: { DEFAULT: '#1FCBAB', dark: '#04382C', pale: '#E6FAF5' },
        gold: { DEFAULT: '#F9B233', dark: '#5A3A00', pale: '#FFF4DF' },
        alert: { DEFAULT: '#C0392B', pale: '#FDECE9' },
        ink: '#15263A', mute: '#5B6E85', paper: '#EEF4FA', line: '#D4E1EE',
        /* nền hộp nhạt — trước đây ghi thẳng bg-[#EAF1F7] ở 8 nơi nên đổi
           bảng màu là sót; đặt tên để chỉ còn một chỗ phải sửa */
        soft: '#EAF2FB',
      },
      fontFamily: { sans: ['Be Vietnam Pro', 'Segoe UI', 'system-ui', 'sans-serif'] },
      borderRadius: { xl2: '1rem' },
    },
  },
  plugins: [],
};
