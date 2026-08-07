/** Bảng màu MOBILUCK — dùng chung với FigForge để hình và giao diện đồng bộ */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        navy: { DEFAULT: '#0C3B70', light: '#155089', deep: '#082948' },
        teal: { DEFAULT: '#1FC3A6', dark: '#04382c', pale: '#E9F9F4' },
        gold: { DEFAULT: '#F8B942', dark: '#3d2a00', pale: '#FFF6E2' },
        alert: { DEFAULT: '#C0392B', pale: '#FDECE9' },
        ink: '#15263A', mute: '#63758A', paper: '#EEF3F8', line: '#D9E3EC',
      },
      fontFamily: { sans: ['Be Vietnam Pro', 'Segoe UI', 'system-ui', 'sans-serif'] },
      borderRadius: { xl2: '1rem' },
    },
  },
  plugins: [],
};
