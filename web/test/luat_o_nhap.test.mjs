/**
 * LUẬT Ô NHẬP — áp cho MỌI QUYỂN, tự đọc sổ đăng ký.
 * chạy: node test/luat_o_nhap.test.mjs
 *
 * Vì sao tệp này tồn tại: mọi luật dưới đây đều rút ra từ một lỗi ĐÃ XẢY RA THẬT
 * khi đưa lớp 3 vào app. Viết lại thành phép kiểm CHUNG, đọc danh sách quyển từ
 * `content/chuong_trinh.json`, nên **quyển lớp 4 vừa khai vào sổ là bị soi ngay** —
 * không ai phải nhớ chép lại luật, và không ai chép thiếu.
 *
 * ── LUẬT ──
 *
 * 1. QUYỂN ĐỌC CHẬM KHÔNG ĐƯỢC CÓ Ô GÕ CHỮ.
 *    Bé 7-9 tuổi gõ chậm; sai chính tả một chữ, hay thừa một dấu cách trong biểu
 *    thức, là mất điểm oan — mà bài đang kiểm TOÁN chứ không kiểm kỹ năng gõ. Đáp
 *    án không phải một con số thì PHẢI cho bấm nút (`options`).
 *    Luật này chỉ áp cho quyển khai `doc.moiManMotMuc` trong sổ (lớp 2, lớp 3).
 *    Lớp 5 là bạn 10-11 tuổi, gõ biểu thức được — nên KHÔNG áp, và đó là chủ ý
 *    chứ không phải nợ bỏ quên.
 *
 * 2. MỒI NHỬ PHẢI THẬT SỰ SAI — nhưng chỉ soi được ở câu hỏi GIÁ TRỊ.
 *    Một mồi vô tình cũng đúng thì bé chọn nó bị chấm sai oan, tệ hơn cả việc không
 *    có trắc nghiệm. Nhưng chỉ áp khi đáp án là MỘT CON SỐ TRẦN.
 *
 *    Vì sao phải hẹp lại: có câu hỏi về DẠNG VIẾT chứ không hỏi giá trị. Lớp 5 hỏi
 *    "viết 2,73 thành tổng giá trị các hàng", đáp "2 + 0,7 + 0,03", mồi "2 + 0,73"
 *    — cộng lại cũng ra 2,73 nhưng KHÔNG phải tách theo hàng, tức là đúng cái lỗi
 *    bài ấy muốn bẫy. Mồi TỐT. Bản đầu của phép kiểm này so bằng giá trị nên báo
 *    hỏng chính chỗ làm đúng nhất.
 *
 * 3. ĐÁP ÁN BẤM CHỌN PHẢI NẰM TRONG DANH SÁCH NÚT.
 *    Lệch một chữ là bé bấm đúng mà máy báo sai — và bé thì tin máy chứ không tin
 *    mình.
 *
 * 4. Ô NÀO CŨNG CÓ NHÃN, VÀ NHÃN KHÔNG ĐƯA SẴN ĐÁP ÁN.
 *    Nhiều ô mà không nhãn thì bé không biết ô nào hỏi gì; nhãn dựng từ lời giải
 *    thì cho không bé đáp số.
 *
 * 5. ĐO ĐƯỢC VIỆC HỌC.
 *    Quyển đọc chậm phải chấm máy ≥ 85% câu luyện tập. Dưới ngưỡng ấy thì bé làm
 *    xong không ai biết đúng sai — sổ phụ huynh và bảng cô giáo trống.
 *
 * ══ LUẬT ÁP THEO MÔN — đọc kỹ trước khi sửa ══
 *
 * Năm luật trên rút ra từ môn TOÁN và đúng cho môn Toán. Môn Tiếng Anh vào sổ thì
 * hai luật quay ra chống lại chính việc đang dạy:
 *
 *   · luật 1 cấm ô gõ chữ — mà GÕ LẠI ĐƯỢC TỪ chính là bậc 4 của bài tiếng Anh;
 *   · luật 2 so mồi nhử bằng GIÁ TRỊ SỐ — tiếng Anh không có giá trị số để so.
 *
 * Nên tệp này hỏi `ct.mon` trước, rồi mới chọn luật. Cách sai — và rất dễ mắc khi
 * vội — là TẮT luật cho tất cả: làm thế thì mất luôn hàng rào đã cứu lớp 3 và lớp 4
 * bên Toán. Mỗi luật bị thay đều phải có luật KHÁC thay chỗ, không được để trống:
 *
 *   luật 1 → 1A: ô gõ của tiếng Anh phải gõ được bằng bàn phím thường (chữ Latin
 *                không dấu) và không dài quá câu dài nhất của quyển;
 *   luật 2 → 2A: mồi nhử không được TRÙNG đáp án sau khi chuẩn hoá (hoa/thường,
 *                dấu nháy cong, dấu chấm cuối) — đúng ba chỗ bé không phân biệt nổi.
 *
 * Luật 3, 4, 5 áp cho MỌI môn, không đổi.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { normText, splitAside, answerCore } from '../src/mon/toan/lib/flow.js';
import { chuanTA } from '../src/mon/tienganh/lib/cham.js';

const G = new URL('../public/content/', import.meta.url).pathname;
let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };
const in5 = (xs) => xs.slice(0, 5).forEach((x) => console.log('     ', x));

const dk = JSON.parse(readFileSync(join(G, 'chuong_trinh.json'), 'utf8')).chuongTrinh || {};

/** Chỉ NHẬN ô là số thuần. Biểu thức cũng phải bấm chọn ở quyển đọc chậm. */
const laSo = (v) => /^[\d\s.,]+$/.test(String(v).trim());

/**
 * Tính giá trị một biểu thức số, hoặc null nếu KHÔNG CHẮC đó là biểu thức.
 *
 * Gạch NGANG NGẮN "–" (U+2013) trong dữ liệu là dấu KHOẢNG, không phải phép trừ:
 * nhãn "mắt 3–4" nghĩa là từ 3 đến 4. Bản đầu của phép kiểm này quy nó về phép trừ
 * nên "3–4" và "5–6" cùng ra −1, và nó báo hai mồi nhử "vô tình cũng đúng" — báo
 * nhầm chính chỗ dữ liệu không có lỗi nào.
 *
 * Nên chỉ tính khi có dấu phép tính KHÔNG NHẬP NHẰNG: + × * : / ( ) hoặc dấu trừ
 * toán học "−" (U+2212). Không chắc thì trả null và bỏ qua — thà bỏ sót một phép
 * kiểm còn hơn đỏ oan, vì phép kiểm đỏ oan thì lần sau người ta tắt nó đi.
 */
function tinh(s) {
  const g = String(s);
  if (!/[+×*:/()\u2212]/.test(g)) return null;
  const t2 = g.replace(/×/g, '*').replace(/\u2212/g, '-').replace(/:/g, '/').replace(/\s/g, '');
  if (!/^[\d+\-*/().,]+$/.test(t2) || !/\d/.test(t2)) return null;
  try { return Function(`"use strict";return(${t2.replace(/,/g, '.')})`)(); } catch { return null; }
}

/**
 * Chữ trên nút có khớp đáp án không — theo ĐÚNG luật của bộ chấm (`matchPick`).
 *
 * Lớp 5 cố ý để lý do trong ngoặc / sau gạch ngang ở `value` ("cặp vàng (1,25 × 8)")
 * còn nút chỉ in phần cốt lõi ("cặp vàng"); bộ chấm tha chỗ ấy. Phép kiểm mà so
 * chuỗi thô thì đỏ oan 5 câu của lớp 5 — chặt hơn bộ chấm là sai, không phải nghiêm.
 */
function nutKhop(options, value) {
  const { core } = splitAside(value);
  const dang = [value, core, answerCore(value)].map((x) => normText(x));
  return options.some((o) => dang.includes(normText(o)));
}

/* 'DL:KSN3.' → 'KSN3' — cùng luật với `maKy` của content.js, suy TỪ SỔ ĐĂNG KÝ
   chứ không gõ tay tên tệp. */
const maKyCua = (ct) => (ct.tienTo || 'DL:KSN5Q1.').replace(/^[A-Z]+:/, '').replace(/\.$/, '');

let soQuyen = 0;
for (const [ma, ct] of Object.entries(dk)) {
  const thuMuc = join(G, ct.thuMuc || '');
  if (!ct.thuMuc || !existsSync(thuMuc)) continue;
  const teps = readdirSync(thuMuc).filter((f) => /^D[LR]_.*\.json$/.test(f));
  if (!teps.length) continue;
  soQuyen += 1;

  const bais = teps.map((f) => JSON.parse(readFileSync(join(thuMuc, f), 'utf8')));
  /* Năm luật phải áp cho CẢ KỲ SÁT HẠCH, không chỉ phần luyện tập.
     Trước đây chỉ soi `practice.pools`, nên 236 câu ôn tập của lớp 4 — chỗ quyết
     định bé qua chương hay không — nằm ngoài tầm mọi phép kiểm, và ExamPlayer thì
     hỏi bé "Mình làm đúng / Mình làm sai". Ô nhập của kỳ sát hạch cũng là ô nhập. */
  const thuMucKy = join(G, 'reviews');
  const ky = existsSync(thuMucKy)
    ? readdirSync(thuMucKy).filter((f) => f.startsWith(`DCR_${maKyCua(ct)}_`))
        .map((f) => JSON.parse(readFileSync(join(thuMucKy, f), 'utf8')))
    : [];
  const cauLuyen = bais.flatMap((b) => Object.values(b.practice?.pools || {}).flat());
  const cauKy = ky.flatMap((k) => [...(k.examA || []), ...(k.deB || [])]);
  /* KHỐI QUIZ CỦA TỪNG BÀI — chỗ mù thứ hai của tệp này.
     "Kỳ sát hạch" ở trên chỉ là các đề chung trong `reviews/DCR_*`. Còn mỗi bài
     lại có khối `assessment` riêng, và nó KHÔNG hề nằm trong tầm soi của bất cứ
     luật nào: 1 148 câu của bốn quyển Toán cộng 80 câu của Tiếng Anh.
     Đếm riêng chứ không gộp vào `cauKy`: hai thứ khác nhau, và gộp thì ngưỡng 85%
     của luật 5 nói dối — nợ đã biết của lớp 5 (210 câu đề chung chưa có ô nhập)
     sẽ bị pha loãng, hoặc ngược lại kéo tụt quyển vừa làm tốt phần quiz. */
  const cauQuiz = bais.flatMap((b) => b.assessment?.items || []);
  /* Bốn luật CHẤT LƯỢNG (nhãn, mồi nhử, đáp án trong nút, cấm ô gõ chữ) soi CẢ HAI
     phần — ô nhập của kỳ sát hạch cũng là ô nhập. Còn luật 5 (ngưỡng phủ) thì tách
     riêng, xem cuối tệp. */
  const cau = [...cauLuyen, ...cauKy, ...cauQuiz];
  const cham = cau.filter((x) => x.answerKey);
  const chamLuyen = cauLuyen.filter((x) => x.answerKey);
  const chamKy = cauKy.filter((x) => x.answerKey);
  const chamQuiz = cauQuiz.filter((x) => x.answerKey);
  /* Cờ nhịp đọc chậm nằm trong sổ, không đoán theo tên quyển — thêm lớp 4 chỉ cần
     khai cờ, khỏi sửa tệp này. */
  const docCham = !!(ct.doc || {}).moiManMotMuc;
  /* MÔN cũng lấy TỪ SỔ. Xem khối "LUẬT ÁP THEO MÔN" ở đầu tệp trước khi đổi. */
  const mon = ct.mon || 'toan';

  /**
   * Các Ô của một câu, quy về MỘT hình dạng `{label, value, options}`.
   *
   * Dữ liệu khai nút bằng HAI cách khác nhau, và bản đầu của tệp này chỉ biết một:
   *
   *   · nhiều ô  → `answerKey.parts[].options`      ← chỉ cách này được soi
   *   · một ô    → `choices` + `answerKey.choice`   ← 244 câu, KHÔNG được soi
   *
   * Nghĩa là luật 2 (mồi nhử) và luật 3 (đáp án phải nằm trong nút) chưa từng chạy
   * cho 244 câu ấy — gồm cả câu trắc nghiệm của bốn quyển Toán. Cổng vẫn xanh suốt,
   * vì nó đếm 0 ô cần soi rồi kết luận "không có lỗi nào".
   *
   * Đây đúng là kiểu hỏng tệ nhất của một cổng: không báo sai, chỉ lặng lẽ không
   * kiểm gì.
   */
  const o = (x) => {
    if (x.answerKey.parts) return x.answerKey.parts;
    if (Array.isArray(x.choices) && x.choices.length) {
      return [{ label: '', value: x.answerKey.choice, options: x.choices }];
    }
    /* Câu ĐÚNG/SAI là HAI NÚT, không phải ô gõ. Không khai ra thì luật 1 thấy
       `value: true` → chuỗi "true" → "không phải số" → báo là ô gõ chữ, và cả ba
       quyển đọc chậm đỏ oan ngay khi khối quiz được đưa vào tầm soi. */
    if (x.format === 'tf' && typeof x.answerKey.value === 'boolean') {
      return [{ label: '', value: x.answerKey.value ? 'ĐÚNG' : 'SAI', options: ['ĐÚNG', 'SAI'] }];
    }
    return [{ value: x.answerKey.value, label: '' }];
  };

  /* ── luật 3 ── */
  const ngoaiNut = [];
  for (const x of cham) {
    for (const p of o(x)) {
      if (!p.options) continue;
      if (!nutKhop(p.options.map(String), String(p.value))) {
        ngoaiNut.push(`${x.id} [${p.label}]: đáp "${p.value}" không có trong nút`);
      }
    }
  }
  t(`${ma} · đáp án bấm chọn nằm trong danh sách nút`, ngoaiNut.length === 0);
  in5(ngoaiNut);

  /* ── luật 2 (Toán) · luật 2A (Tiếng Anh) ── */
  const moiHong = [];
  for (const x of cham) {
    for (const p of o(x)) {
      if (!p.options) continue;

      if (mon === 'tienganh') {
        /* Dạng "mồi vô tình cũng đúng" của tiếng Anh KHÔNG phải chuyện giá trị số,
           mà là hai nút chỉ khác nhau ở ba chỗ bé không phân biệt nổi: chữ hoa,
           dấu nháy cong ’ ↔ thẳng ', và dấu chấm cuối. Bé bấm nút nào cũng phải
           được điểm, mà bộ chấm chỉ nhận đúng một — nên bé bấm ĐÚNG mà máy báo SAI. */
        const dung = chuanTA(p.value);
        for (const c of p.options) {
          if (String(c) === String(p.value)) continue;
          if (chuanTA(c) === dung) {
            moiHong.push(`${x.id} [${p.label}]: mồi "${c}" trùng đáp án "${p.value}"`);
          }
        }
        continue;
      }

      /* Chỉ soi khi đáp án là MỘT CON SỐ TRẦN. Đáp án là biểu thức thì câu hỏi
         đang hỏi DẠNG VIẾT, mà dạng thì không so bằng giá trị được. */
      if (!laSo(p.value)) continue;
      const dung = tinh(p.value) ?? Number(String(p.value).replace(/\s/g, '').replace(',', '.'));
      if (!Number.isFinite(dung)) continue;
      for (const c of p.options) {
        if (String(c) === String(p.value)) continue;
        if (tinh(c) === dung) moiHong.push(`${x.id} [${p.label}]: mồi "${c}" cũng ra ${dung}`);
      }
    }
  }
  t(`${ma} · không mồi nhử nào vô tình cũng đúng`, moiHong.length === 0);
  in5(moiHong);

  /* ── luật 4 ── */
  const nhanHong = [];
  for (const x of cham) {
    const ps = x.answerKey.parts || [];
    for (const p of ps) {
      const nhan = String(p.label ?? '').trim();
      if (ps.length > 1 && !nhan) { nhanHong.push(`${x.id}: có ${ps.length} ô mà thiếu nhãn`); continue; }
      const v = String(p.value ?? '').trim().replace(/\s/g, '');
      const l = nhan.replace(/\s/g, '');
      if (v && (l === v || l.endsWith(`=${v}`))) {
        nhanHong.push(`${x.id}: nhãn "${p.label}" đưa sẵn đáp án`);
      }
    }
  }
  t(`${ma} · ô nào cũng có nhãn và nhãn không đưa sẵn đáp án`, nhanHong.length === 0);
  in5(nhanHong);

  if (mon === 'tienganh') {
    /* ── luật 1A · Ô GÕ CỦA TIẾNG ANH ──
       Luật 1 gốc cấm ô gõ chữ. Ở đây gõ chữ CHÍNH LÀ bài, nên không cấm được — mà
       bỏ trống thì mất hàng rào. Thay bằng hai điều kiện, mỗi điều kiện chặn một
       lỗi đã thấy trước khi nó xảy ra:

         (a) chỉ chữ Latin KHÔNG DẤU và dấu câu tiếng Anh. Chặn việc lỡ đưa đáp án
             tiếng Việt có dấu vào ô gõ ("quả bóng") — bé 6 tuổi không gõ nổi, và
             đó cũng không phải thứ bài này kiểm;
         (b) không dài quá câu dài nhất của quyển. Bé 6 tuổi gõ ~10 ký tự/phút; một
             ô 60 ký tự là bỏ cuộc chứ không phải làm sai. */
    const DAI_NHAT = 46;   // "How many windows can you see? - I can see six."
    const goHong = [];
    for (const x of cham) {
      for (const p of o(x)) {
        const v = String(p.value ?? '').trim();
        if (!v || p.options) continue;
        if (!/^[A-Za-z0-9 '\-.,?!]+$/.test(v)) {
          goHong.push(`${x.id} [${p.label || ''}] → "${v}" có ký tự gõ không được`);
        } else if (v.length > DAI_NHAT) {
          goHong.push(`${x.id} [${p.label || ''}] → dài ${v.length} ký tự (quá ${DAI_NHAT})`);
        }
      }
    }
    t(`${ma} · ô gõ tiếng Anh gõ được bằng bàn phím thường và không quá dài`,
      goHong.length === 0);
    in5(goHong);
  } else if (!docCham) {
    console.log(`   ${ma}: ${bais.length} bài · luyện ${chamLuyen.length}/${cauLuyen.length}`
    + ` · sát hạch ${chamKy.length}/${cauKy.length} chấm máy`
      + ' · nhịp đọc nhanh nên KHÔNG áp luật "cấm ô gõ chữ"');
    continue;
  } else {
    /* ── luật 1 · chỉ quyển ĐỌC CHẬM của môn TOÁN ── */
    const goChu = [];
    for (const x of cham) {
      if (x.answerKey.values) continue;
      for (const p of o(x)) {
        const v = String(p.value ?? '').trim();
        if (!v || p.options) continue;
        if (!laSo(v)) goChu.push(`${x.id} [${p.label || ''}] → ${v}`);
      }
    }
    t(`${ma} · mọi ô là điền SỐ hoặc BẤM CHỌN (quyển đọc chậm)`, goChu.length === 0);
    in5(goChu);
  }

  /* ── luật 5 · ngưỡng phủ, đo RIÊNG hai phần ──
     Gộp chung thì con số nói dối theo cả hai chiều: quyển làm tốt phần luyện tập mà
     bỏ trống kỳ sát hạch vẫn qua ngưỡng, còn quyển vừa thêm kỳ sát hạch lại bị kéo
     tụt. Lớp 2 và lớp 3 hiện CHƯA có ô nhập cho kỳ sát hạch — đó là việc còn nợ
     thật, ghi trong docs/tiep_theo_lop4.md, nên phép kiểm nói ra chứ không đỏ oan
     hai quyển đang chạy. Quyển nào ĐÃ khai ô nhập cho kỳ sát hạch thì bị soi ngay. */
  t(`${ma} · chấm máy ≥ 85% câu luyện tập (${chamLuyen.length}/${cauLuyen.length})`,
    cauLuyen.length === 0 || chamLuyen.length >= cauLuyen.length * 0.85);
  if (cauQuiz.length) {
    t(`${ma} · chấm máy ≥ 85% câu quiz cuối bài (${chamQuiz.length}/${cauQuiz.length})`,
      chamQuiz.length >= cauQuiz.length * 0.85);
  }
  if (chamKy.length) {
    t(`${ma} · chấm máy ≥ 85% câu kỳ sát hạch (${chamKy.length}/${cauKy.length})`,
      chamKy.length >= cauKy.length * 0.85);
  } else if (cauKy.length) {
    console.log(`   ${ma}: ⏸ ${cauKy.length} câu kỳ sát hạch CHƯA có ô nhập — `
      + 'bé tự đánh dấu đúng/sai, không đo được');
  }

  const soO = cham.reduce((a, x) => a + (x.answerKey.parts?.length || 1), 0);
  const nut = cham.reduce((a, x) => a + o(x).filter((p) => p.options).length, 0);
  console.log(`   ${ma}: ${bais.length} bài · luyện ${chamLuyen.length}/${cauLuyen.length}`
    + ` · sát hạch ${chamKy.length}/${cauKy.length} · quiz ${chamQuiz.length}/${cauQuiz.length} chấm máy`
    + ` · ${soO} ô (${nut} bấm chọn) · ${mon}${docCham ? ' · đọc chậm' : ''}`);
}

t(`soi được ít nhất hai quyển (${soQuyen})`, soQuyen >= 2);

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
