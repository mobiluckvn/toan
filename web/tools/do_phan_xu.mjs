/**
 * ĐO PHẦN BỎ PHIẾU LƯỢT NÓI MƠ HỒ (việc V10 · phần B).
 *
 * ── HAI PHÉP ĐO, VÀ VÌ SAO PHẢI LÀ HAI ──
 *
 * 1 · TẦN SỐ (chạy được không cần mạng, `--tinh`)
 *     Vùng mơ hồ có xảy ra thật trên vốn từ năm quyển không? Nếu không thì cả phần
 *     bỏ phiếu là mã chết, và không con số nào về độ chính xác của nó có nghĩa.
 *
 * 2 · TÍNH NHẤT QUÁN KHI ĐẢO VAI (cần khoá Groq)
 *     Cùng một chuỗi máy nghe được, cùng hai chữ — nhưng đổi chữ nào là "từ đích".
 *     Mô hình phải gọi ra CÙNG một chữ. Lệch là bằng chứng nó đang đoán theo VỊ TRÍ
 *     chứ không theo âm, và lúc ấy "hai phiếu nhất trí" chỉ là tiếng vang của thứ
 *     tự mình xếp ra.
 *
 * ── ⚠ VÌ SAO KHÔNG ĐO "ĐÚNG / SAI" ──
 * Bản đầu của bộ đo này gán nhãn đúng-sai theo CHỮ NÀO BỊ BỘ MÉO LÀM MÉO: méo
 * `brother` ra `blothel` thì nhãn đúng là `brother`. Nó cho ra "sai 23%", và con số
 * ấy VÔ NGHĨA — bộ méo của mình không phải bộ nhận dạng giọng nói, và chữ nó méo ra
 * không phải chữ bé đã đọc. Ca rõ nhất: méo `it` thành `at`, rồi bắt mô hình phải
 * trả lời `it`; nhưng `at` nghe giống `that` hơn `it`, và mô hình nói thế là nó
 * đúng, nhãn của mình sai.
 *
 * Muốn con số đúng-sai thật thì phải có NGƯỜI nghe 50 lượt nói thật rồi chấm tay —
 * đó là "Định nghĩa XONG" của §7, và nó KHÔNG phải việc code. Chưa có bộ ấy thì bộ
 * đo này chỉ nói hai điều nó đo được thật.
 *
 * ── CHẠY ──
 *     node tools/do_phan_xu.mjs --tinh     # chỉ phép đo 1, không cần mạng
 *     node tools/do_phan_xu.mjs            # cả hai (đọc khoá ở functions/.secret.local)
 */
import { readFileSync, readdirSync } from 'node:fs';
import { chamTu, moHoCanBoPhieu, apDungPhieu, VUNG_MO_HO, GAN_NHAU }
  from '../src/mon/tienganh/lib/chamnoi.js';

const G = new URL('../public/content/', import.meta.url);
const QUYEN = ['ta1', 'ta2', 'ta3', 'ta4', 'ta5'];
const chiTinh = process.argv.includes('--tinh');

/**
 * BỘ MÉO — mô phỏng mấy kiểu bộ nhận dạng ghi sai hay gặp với giọng trẻ Việt.
 *
 * ⚠ ĐÂY LÀ MÔ PHỎNG THÔ, KHÔNG PHẢI DỮ LIỆU THẬT. Sáu luật máy móc; lời STT thật
 * lạ hơn thế nhiều. Nên con số tần số dưới đây là một CỠ, không phải một phép đo —
 * nó trả lời "có xảy ra không", không trả lời "xảy ra bao nhiêu".
 */
const BO_MEO = [
  (w) => w.replace(/s$/, ''),          // mất âm cuối /s/
  (w) => w.replace(/[aeiou]/, 'a'),    // nguyên âm bẹt về /a/
  (w) => w.replace(/.$/, ''),          // mất âm cuối
  (w) => w.replace(/^th/, 't'),        // th → t
  (w) => w.replace(/r/g, 'l'),         // r → l, kiểu lẫn kinh điển
  (w) => `${w}a`,                      // thêm nguyên âm cuối
];

function docVon() {
  const ra = [];
  for (const q of QUYEN) {
    const thuMuc = new URL(`${q}/`, G);
    for (const t of readdirSync(thuMuc).filter((x) => /^DL_.*\.json$/.test(x))) {
      const bai = JSON.parse(readFileSync(new URL(t, thuMuc), 'utf8'));
      const von = (bai?.knowledgeCore?.vocabulary || [])
        .map((v) => String(v?.tu || '').toLowerCase())
        .filter((x) => /^[a-z' ]+$/.test(x));
      if (von.length > 1) ra.push({ quyen: q, bai: t, von });
    }
  }
  return ra;
}

/* ───────────────────── 1 · TẦN SỐ ───────────────────── */

function domoHo(dsBai) {
  let tong = 0, nham = 0, coGan = 0, moHo = 0;
  const cap = new Map();
  for (const { quyen, von } of dsBai) {
    for (const w of von) {
      const doiThu = von.filter((x) => x !== w);
      for (const meo of BO_MEO) {
        const nghe = meo(w);
        if (!nghe || nghe === w) continue;
        tong += 1;
        const k = chamTu(w, nghe, { doiThu });
        if (k.lyDo === 'nhamTu') { nham += 1; continue; }
        if (k.doiThuGan) coGan += 1;
        if (!moHoCanBoPhieu(k)) continue;
        moHo += 1;
        /* Gom theo CẶP ĐỘC NHẤT: cùng chuỗi nghe + cùng bộ hai chữ là một câu hỏi,
           dù nó xuất hiện ở hai lượt khác nhau. */
        const khoa = `${nghe}|${[w, k.doiThuGan.tu].sort().join('~')}`;
        if (!cap.has(khoa)) {
          cap.set(khoa, { quyen, nghe, a: w, b: k.doiThuGan.tu, diem: k.diem,
            gA: k.doGiong, gB: k.doiThuGan.doGiong });
        }
      }
    }
  }
  return { tong, nham, coGan, moHo, cap: [...cap.values()] };
}

/* ───────────────────── 2 · NHẤT QUÁN ───────────────────── */

async function doNhatQuan(cap) {
  const { phanXu } = await import('../functions/src/phanxu.js');
  /* ⚠ `groq-sdk` nằm ở `functions/node_modules`, KHÔNG ở `web/node_modules` — hai
     gói phụ thuộc riêng, và `web/` cố ý không kéo SDK của máy chủ về. Nên trỏ thẳng
     đường dẫn, đừng để Node tự tìm (nó tìm từ tệp này lên và không thấy). */
  const { Groq } = await import(
    new URL('../functions/node_modules/groq-sdk/index.mjs', import.meta.url).href);
  const tep = new URL('../functions/.secret.local', import.meta.url);
  const khoa = readFileSync(tep, 'utf8').match(/GROQ_API_KEY\s*=\s*"?([^"\n]+)/)?.[1]?.trim();
  if (!khoa) throw new Error('Không thấy GROQ_API_KEY trong functions/.secret.local');
  const tao = () => new Groq({ apiKey: khoa });

  let nhatQuan = 0, lech = 0, motChieu = 0, giuCa = 0;
  for (const x of cap) {
    /* Hỏi CẢ HAI chiều vai, song song. */
    const [p, q] = await Promise.all([
      phanXu({ nghe: x.nghe, dich: x.a, canhTranh: x.b }, tao),
      phanXu({ nghe: x.nghe, dich: x.b, canhTranh: x.a }, tao),
    ]);
    const chu = (r, dich, canh) => (r.dieuChinh === 0 ? null : (r.gan === 'dich' ? dich : canh));
    const c1 = chu(p, x.a, x.b);
    const c2 = chu(q, x.b, x.a);
    let ket;
    if (c1 && c2) {
      if (c1 === c2) { nhatQuan += 1; ket = `NHẤT QUÁN → ${c1}`; }
      else { lech += 1; ket = `⚠ LỆCH: ${c1} / ${c2}`; }
    } else if (c1 || c2) { motChieu += 1; ket = `chỉ một chiều ngã → ${c1 || c2}`; }
    else { giuCa += 1; ket = 'cả hai chiều giữ điểm'; }
    const sau = apDungPhieu(x.diem, p.dieuChinh);
    console.log(`  "${x.nghe}"  ${x.a} / ${x.b}  (${x.gA.toFixed(2)}/${x.gB.toFixed(2)})`
      + `  ${x.diem}→${sau}đ  ${ket}`);
    await new Promise((s) => setTimeout(s, 120));
  }
  return { nhatQuan, lech, motChieu, giuCa };
}

/* ───────────────────── CHẠY ───────────────────── */

const dsBai = docVon();
const d = domoHo(dsBai);

console.log(`\n── 1 · TẦN SỐ (${dsBai.length} bài, ${QUYEN.length} quyển) ──\n`);
console.log(`  lượt mô phỏng         ${d.tong}`);
console.log(`  bắt được nhầm từ      ${d.nham}  (${(d.nham / d.tong * 100).toFixed(1)}%)`
  + '  ← trần 3 điểm, không cần phiếu');
console.log(`  có đối thủ ở gần      ${d.coGan}  (${(d.coGan / d.tong * 100).toFixed(1)}%)`);
console.log(`  CẦN BỎ PHIẾU          ${d.moHo}  (${(d.moHo / d.tong * 100).toFixed(1)}%)`);
console.log(`  cặp câu hỏi độc nhất  ${d.cap.length}`);
console.log(`\n  vùng mơ hồ [${VUNG_MO_HO.join(', ')}] · gần nhau ≤ ${GAN_NHAU}`);

if (chiTinh) {
  console.log('\n  (--tinh: bỏ phép đo nhất quán)\n');
} else {
  console.log('\n── 2 · NHẤT QUÁN KHI ĐẢO VAI (mô hình THẬT) ──\n');
  const n = await doNhatQuan(d.cap);
  console.log(`\n  nhất quán hai chiều  ${n.nhatQuan}`);
  console.log(`  LỆCH hai chiều       ${n.lech}   ← lỗi THẬT của phép đảo vai`);
  console.log(`  chỉ một chiều ngã    ${n.motChieu}`);
  console.log(`  cả hai chiều giữ     ${n.giuCa}`);
  console.log('\n  ⚠ Bộ đo này KHÔNG nói đúng/sai — xem khối chú thích đầu tệp.\n');
}
