import js from '@eslint/js';
import globals from 'globals';
import reactHooks from 'eslint-plugin-react-hooks';
import react from 'eslint-plugin-react';

/**
 * ESLINT — và bộ luật ở đây CỐ Ý HẸP.
 *
 * ── ⚠ VÌ SAO KHÔNG BẬT CẢ BỘ KHUYẾN NGHỊ ──
 * Kho này có 116 cổng và một lối viết riêng đã dùng suốt: chú thích dài, biến tiếng
 * Việt, hàm thuần. Bật cả `recommended` cho ra hàng nghìn lời than về lối viết, và
 * khi một bộ kiểm kêu quá nhiều thì người ta tắt nó đi — hoặc tệ hơn, sửa mã cho
 * vừa lòng nó. Cả hai đều tệ hơn không có.
 *
 * Nên chỉ bật những luật trả lời được câu: «luật này có bắt được một lỗi ĐÃ XẢY RA
 * THẬT ở kho này không?» Bốn nhóm dưới đây đều trả lời được.
 *
 * ── BỐN NHÓM, VÀ LỖI THẬT ĐỨNG SAU TỪNG NHÓM ──
 *
 *   1 · `no-undef` — BỐN lần một `ReferenceError` lọt qua `npm run build` và cả
 *       116 cổng, hai lần lên tới bản thật và cho ra MÀN TRẮNG HOÀN TOÀN. Đây là
 *       luật đắt giá nhất trong cả tệp: nó bắt được đúng lớp lỗi ấy, ở ngay lúc gõ.
 *
 *   2 · `react-hooks/rules-of-hooks` — hook đặt sau một `return` sớm (React 310),
 *       đã lên bản thật một lần. Cổng `man_dung_duoc` dựng màn ở MÁY CHỦ nên KHÔNG
 *       bắt được lớp này (nó đòi lượt vẽ thứ hai); ESLint bắt được ở dạng tĩnh.
 *
 *   3 · `no-unused-vars` — kho đã có «cổng xanh mà không ai gọi»: bốn thuật toán
 *       chỉ có cổng và công cụ gọi, nằm chết suốt hơn một tháng.
 *
 *   4 · mấy luật bắt lỗi im lặng: `no-dupe-keys` (khoá trùng trong object literal
 *       — lặng lẽ ghi đè), `no-fallthrough`, `no-cond-assign`, `eqeqeq` chỉ cho
 *       `null`.
 *
 * ── ⚠ CHẠY RIÊNG, KHÔNG GẮN VÀO `npm test` ──
 * `npm test` là 116 cổng nói về HÀNH VI; ESLint nói về HÌNH DẠNG MÃ. Gộp vào một
 * lệnh thì một lời than về biến thừa chặn mất một phép canh về việc dạy trẻ. Chạy
 * `npm run soi`.
 */
export default [
  {
    ignores: ['dist/**', 'node_modules/**', 'public/**', 'functions/node_modules/**'],
  },
  {
    files: ['src/**/*.{js,jsx}', 'functions/**/*.js', 'test/**/*.mjs'],
    languageOptions: {
      ecmaVersion: 2023,
      sourceType: 'module',
      parserOptions: { ecmaFeatures: { jsx: true } },
      globals: {
        ...globals.browser,
        ...globals.node,
        /* Hằng do Vite thay lúc dựng (`define`) — có thật lúc chạy, không khai ở
           đâu trong mã nguồn. */
        __NOI_DUNG_V__: 'readonly',
      },
    },
    plugins: { 'react-hooks': reactHooks, react },
    rules: {
      /* ── 1 · lớp lỗi đã BỐN lần cho ra màn trắng ── */
      'no-undef': 'error',

      /* ── 2 · hook sai chỗ ── */
      'react-hooks/rules-of-hooks': 'error',
      /* `exhaustive-deps` để CẢNH BÁO, không chặn: nó đúng phần lớn nhưng có chỗ
         kho này cố ý bỏ phụ thuộc, và mỗi chỗ ấy đã có chú thích giải thích. */
      'react-hooks/exhaustive-deps': 'warn',

      /* ── ⚠ HAI LUẬT CHỈ ĐỂ ESLINT HIỂU JSX ──
         Không có chúng thì mọi component dùng trong JSX bị kể là «khai mà không
         dùng»: đo lần đầu ra 257 lời than, trong đó 56 là chính `React`. Một bộ
         kiểm kêu 257 lần về thứ không sai thì người ta tắt nó đi — và tắt đi là mất
         luôn 7 lỗi `no-undef` thật mà nó vừa tìm ra. */
      'react/jsx-uses-react': 'error',
      'react/jsx-uses-vars': 'error',

      /* ── 3 · mã chết ── */
      'no-unused-vars': ['error', {
        /* Tham số thừa trước một tham số có dùng thì không bỏ được — đó là hình
           dạng của JavaScript, không phải lỗi của người viết. */
        args: 'after-used',
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
        caughtErrors: 'none',
        /* `const { step, steps, ...rest } = m` — trải để BỎ khoá, một lối viết cố
           ý và không có cách nào gọn hơn. Không bật cái này thì nó bị kêu, và người
           ta sẽ viết lại thành `delete` — vừa dài vừa sửa tại chỗ đối tượng gốc. */
        ignoreRestSiblings: true,
      }],

      /* ── 4 · lỗi im lặng ── */
      'no-dupe-keys': 'error',
      'no-dupe-args': 'error',
      'no-dupe-class-members': 'error',
      'no-fallthrough': 'error',
      /* ⚠ `except-parens`, KHÔNG phải `always`. Lối `while ((m = r.exec(s)))` là
         cách chuẩn để duyệt mọi lần khớp của một biểu thức chính quy, và kho này
         dùng nó có chủ ý — dấu ngoặc thừa chính là lời khai «tôi cố ý gán ở đây».
         Đặt `always` thì sáu chỗ đúng bị kêu, và người ta sẽ viết lại chúng thành
         thứ dài hơn mà không an toàn hơn. */
      'no-cond-assign': ['error', 'except-parens'],
      'no-self-compare': 'error',
      'no-unsafe-negation': 'error',
      'no-unreachable': 'error',
      'use-isnan': 'error',
      'valid-typeof': 'error',
      eqeqeq: ['error', 'always', { null: 'ignore' }],
    },
  },
  {
    /* Cổng được phép gọi hàm chưa khai trước (chúng nhập động), và hay có biến chỉ
       dùng để khẳng định sự tồn tại. */
    files: ['test/**/*.mjs'],
    rules: { 'no-unused-vars': 'warn' },
  },
  js.configs.recommended.rules ? {} : {},
].filter((x) => Object.keys(x).length);
