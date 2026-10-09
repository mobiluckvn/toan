/**
 * BẢNG ΔC — MẪU LỜI DẶN NÀO ĐANG DẠY HIỆU QUẢ HƠN (mục 2.5.3 luận văn, việc V8).
 *
 *   cd web && node tools/doc_delta_c.mjs                     # in bảng
 *   cd web && node tools/doc_delta_c.mjs --de-xuat           # + đề xuất sửa lời dặn
 *   cd web && node tools/doc_delta_c.mjs --tep <x.json>      # đọc từ tệp, không cần mạng
 *
 * ── CHẠY TAY, KHÔNG PHẢI HÀM NỀN ──
 * Nó đọc dữ liệu của MỌI bé bằng khoá quản trị. Một việc như thế không được chạy tự
 * động: nó phải là một lần có người gõ lệnh và đọc kết quả.
 *
 * ── VÀ NÓ KHÔNG BAO GIỜ TỰ SỬA LỜI DẶN ──
 * Cờ `--de-xuat` gọi mô hình MỘT lần để xin một đề xuất, rồi IN RA. Sửa lời dặn là
 * việc của người: lời dặn là thứ quyết định cô giáo máy nói gì với trẻ con, và một
 * vòng "mô hình tự sửa lời dặn của chính nó" thì không ai còn kiểm được điều gì.
 * Sửa xong phải TỰ TAY tăng `PHIEN_BAN_MAU.luyennoi` — `vantay_prompt.test.mjs` canh
 * chỗ ấy, nhưng nó chỉ canh được khi số đã tăng.
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { gomTheoMau, mauTotNhat, capHopLe, TOI_THIEU_CAP } from '../functions/src/ara.js';

const args = process.argv.slice(2);
const co = (t) => args.includes(t);
const giaTri = (t, mac = null) => {
  const i = args.indexOf(t);
  return i >= 0 && args[i + 1] ? args[i + 1] : mac;
};

/* ─────────── nguồn dữ liệu ─────────── */

/**
 * Dựng CẶP A-R-A từ nhật ký.
 *
 * Một cặp = hai lần đo mức nắm cùng một nút, cách nhau một lần can thiệp, và KHÔNG
 * dùng lại câu nào (`capHopLe` bác nếu trùng — đo trí nhớ ngắn hạn thì ΔC đẹp lên
 * một cách vô nghĩa).
 *
 * ⚠ ĐỌC `attempts`, KHÔNG đọc `phongNoiTA`. §7 ghi `phongNoiTA`, nhưng chỗ ấy chỉ
 * lưu lời nói của buổi (`vai` · `chu` · `en` · `vi` · `nhan`) — nó KHÔNG có `itemId`
 * lẫn mức nắm, tức không dựng được một cặp nào. `attempts` thì có cả `maPhien`,
 * `mauPrompt`, `phienBanMau` (phòng nói đã ghi từ Đợt 1) và `itemId` — đúng ba thứ
 * `capHopLe` đòi. Nói thẳng ra đây để đừng ai đi sửa theo bản rà.
 */
function dungCap(attempts, mastery) {
  const theoNut = new Map();
  for (const a of attempts) {
    const nut = a.maNut || a.cau?.maNut || null;
    if (!nut || !a.maPhien) continue;
    const k = `${a.learnerId}|${nut}`;
    if (!theoNut.has(k)) theoNut.set(k, new Map());
    const phien = theoNut.get(k);
    if (!phien.has(a.maPhien)) {
      phien.set(a.maPhien, { itemIds: [], mauPrompt: a.mauPrompt || null,
        phienBanMau: a.phienBanMau ?? null, ts: a.ts || '' });
    }
    phien.get(a.maPhien).itemIds.push(a.itemId);
  }
  const ds = [];
  for (const [k, phien] of theoNut) {
    const [learnerId, nut] = k.split('|');
    const sx = [...phien.values()].sort((a, b) => String(a.ts).localeCompare(String(b.ts)));
    for (let i = 1; i < sx.length; i += 1) {
      const p = mastery[`${learnerId}|${nut}`];
      /* Mức nắm TRƯỚC và SAU phải là hai con số khác nhau của CÙNG nút. `mastery`
         chỉ giữ bản mới nhất, nên lịch sử p lấy từ `pTruoc`/`pSau` nếu hàm nền có
         ghi; không có thì cặp bị `capHopLe` bác vì thiếu mức nắm — và bị bác là
         ĐÚNG, chứ không được đoán một con số. */
      ds.push({
        truoc: { p: sx[i - 1].pSau ?? p?.lichSu?.[i - 1] ?? null, itemIds: sx[i - 1].itemIds },
        sau: { p: sx[i].pSau ?? p?.lichSu?.[i] ?? p?.p ?? null, itemIds: sx[i].itemIds },
        mauPrompt: sx[i].mauPrompt, phienBanMau: sx[i].phienBanMau, nut, learnerId,
      });
    }
  }
  return ds;
}

async function docTuMay() {
  const project = giaTri('--project')
    || (fs.existsSync('.firebaserc') && JSON.parse(fs.readFileSync('.firebaserc', 'utf8')).projects?.default);
  if (!project) throw new Error('Không biết dự án nào. Thêm --project <mã>.');
  const cfg = path.join(os.homedir(), '.config', 'configstore', 'firebase-tools.json');
  const tok = fs.existsSync(cfg)
    ? (JSON.parse(fs.readFileSync(cfg, 'utf8')).tokens || {}).access_token : null;
  if (!tok) throw new Error('Chưa đăng nhập. Chạy: firebase login');
  const FS = `https://firestore.googleapis.com/v1/projects/${project}/databases/(default)/documents`;
  const lay = async (duong) => {
    const r = await fetch(`${FS}/${duong}?pageSize=1000`,
      { headers: { Authorization: `Bearer ${tok}` } });
    if (!r.ok) throw new Error(`${r.status} ${(await r.text()).slice(0, 200)}`);
    return (await r.json()).documents || [];
  };
  const tho = (d) => Object.fromEntries(Object.entries(d.fields || {})
    .map(([k, v]) => [k, v.stringValue ?? (v.integerValue != null ? Number(v.integerValue)
      : (v.doubleValue ?? v.booleanValue ?? null))]));
  const attempts = (await lay('attempts')).map(tho).filter((a) => a.format === 'phongNoi' || a.mauPrompt);
  return { attempts, mastery: {} };
}

/* ─────────── chạy ─────────── */

let nguon;
const tep = giaTri('--tep');
if (tep) {
  nguon = JSON.parse(fs.readFileSync(tep, 'utf8'));
} else {
  try { nguon = await docTuMay(); } catch (e) {
    console.error(`Không đọc được máy chủ: ${e.message}`);
    console.error('Chạy thử không cần mạng:  node tools/doc_delta_c.mjs --tep <tệp.json>');
    console.error('Tệp ấy hình dạng: { "attempts": [...], "mastery": {} }');
    process.exit(1);
  }
}

const dsCap = Array.isArray(nguon.capSan) ? nguon.capSan
  : dungCap(nguon.attempts || [], nguon.mastery || {});

const bang = gomTheoMau(dsCap);
console.log(`\n══════ BẢNG ΔC · ${dsCap.length} cặp A-R-A dựng được ══════`);
if (!bang.length) {
  console.log('Chưa có cặp nào. Cần ít nhất hai lần đo cùng một nút, KHÁC câu.');
} else {
  console.log('mẫu'.padEnd(14), 'phiên bản'.padEnd(10), 'số cặp'.padEnd(8),
    'bỏ qua'.padEnd(8), 'ΔC trung bình');
  for (const r of bang) {
    console.log(String(r.mau).padEnd(14), String(r.phienBan).padEnd(10),
      String(r.soCap).padEnd(8), String(r.boQua).padEnd(8),
      r.duMau ? r.deltaTB : `— (cần ${TOI_THIEU_CAP} cặp)`);
  }
}
/* Nói ra LÝ DO bị bỏ: "bỏ qua 40" mà không biết vì sao thì không sửa được gì. */
const ly = new Map();
for (const c of dsCap) {
  const k = capHopLe(c);
  if (!k.ok) ly.set(k.vi, (ly.get(k.vi) || 0) + 1);
}
if (ly.size) {
  console.log('\nLý do cặp bị bỏ:');
  for (const [v, n] of [...ly].sort((a, b) => b[1] - a[1])) console.log(`  ${String(n).padStart(5)}  ${v}`);
}

const so = mauTotNhat(dsCap);
if (!so) {
  console.log('\nChƯA so được hai mẫu: cần ÍT NHẤT HAI mẫu đủ cỡ mẫu.');
  console.log('Một mẫu đủ dữ liệu thì nó vừa tốt nhất vừa tệ nhất — câu ấy vô nghĩa.');
} else {
  console.log(`\nTốt nhất : ${so.tot.mau}@${so.tot.phienBan}  ΔC ${so.tot.deltaTB}`);
  console.log(`Kém nhất : ${so.kem.mau}@${so.kem.phienBan}  ΔC ${so.kem.deltaTB}`);
}

if (!co('--de-xuat')) {
  console.log('\n(thêm --de-xuat để xin MỘT đề xuất sửa lời dặn — chỉ in ra, không tự sửa)');
  process.exit(0);
}

/* ─────────── đề xuất, và CHỈ IN RA ─────────── */

if (!so) { console.log('\nKhông đề xuất gì khi chưa so được hai mẫu.'); process.exit(0); }
const khoa = (() => {
  const f = 'functions/.secret.local';
  if (!fs.existsSync(f)) return null;
  return fs.readFileSync(f, 'utf8').split('\n')
    .map((l) => l.match(/^GROQ_API_KEY=(.+)$/)).filter(Boolean)
    .map((m) => m[1].trim().replace(/^["']|["']$/g, '')).find((x) => x.length > 10) || null;
})();
if (!khoa) { console.error('\nKhông thấy GROQ_API_KEY trong functions/.secret.local'); process.exit(1); }

const { MO_HINH, NGHI_NGAN } = await import('../functions/src/luyennoi.js');
const { Groq } = await import('../functions/node_modules/groq-sdk/index.mjs');
const kq = await new Groq({ apiKey: khoa }).chat.completions.create({
  model: MO_HINH,
  messages: [{ role: 'system', content: [
    'Bạn đang giúp một người sửa LỜI DẶN cho cô giáo tiếng Anh tự động của trẻ tiểu học.',
    `Mẫu lời dặn "${so.kem.mau}" phiên bản ${so.kem.phienBan} đang cho kết quả học KÉM NHẤT`,
    `(ΔC trung bình ${so.kem.deltaTB} trên ${so.kem.soCap} cặp đo), còn`,
    `"${so.tot.mau}" phiên bản ${so.tot.phienBan} tốt nhất (ΔC ${so.tot.deltaTB}).`,
    '',
    'Viết tiếng Việt, nhiều nhất 5 gạch đầu dòng, mỗi dòng một thay đổi CỤ THỂ nên thử',
    'ở mẫu kém. KHÔNG viết lại cả lời dặn. KHÔNG đề nghị nới vốn từ của bé.',
  ].join('\n') }],
  temperature: 0.4,
  max_tokens: 500,
  reasoning_effort: NGHI_NGAN,
});
console.log('\n══════ ĐỀ XUẤT (CHỈ IN RA — không tệp nào bị sửa) ══════');
console.log(kq?.choices?.[0]?.message?.content || '(mô hình không trả lời)');
console.log('\n⚠ Sửa lời dặn xong thì TỰ TAY tăng PHIEN_BAN_MAU.luyennoi ở');
console.log('  functions/src/vantay.js — không tăng thì bảng này gom lẫn mẫu mới với mẫu cũ.');
