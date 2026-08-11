/**
 * CỔNG SỔ TIẾN ĐỘ — hai lỗi câm lộ ra khi soát end-to-end ngày 11-08-2026.
 * chạy: node test/so_tien_do.test.mjs
 *
 * Cả hai đều KHÔNG làm màn hình vỡ, nên 1 096 phép kiểm cũ đi qua sạch còn bé thì
 * chịu trận. Chỗ này gác lại đúng hai chỗ ấy.
 *
 * ── Lỗi 1 · vòng lặp không đáy ──
 * Vỏ gộp sổ của môn bằng `{ ...t, [ma]: f(t[ma]) }` — dựng khối MỚI kể cả khi môn
 * báo "chẳng có gì đổi". React thấy sổ đổi thì vẽ lại vỏ; vẽ lại thì hàm `datTienDo`
 * truyền xuống môn cũng mới; mà phòng học có effect canh chính hàm ấy để ghi chỗ
 * học dở — nó chạy lại, lại gọi vào vỏ, lại vẽ. Đo được: 3 180 dòng "Maximum update
 * depth exceeded" trong bốn phút, localStorage bị ghi liên tục, máy quay hết công
 * suất. Màn hình vẫn trông bình thường.
 *
 * ── Lỗi 2 · thẻ HỌC TIẾP chỉ sang quyển cũ ──
 * `saveSpot` nhớ chỗ con đang học dở nhưng KHÔNG đóng dấu thời gian, mà kệ sách lại
 * xếp "quyển động vào gần nhất" theo mốc ấy. Học dở lớp 2 xong quay ra kệ sách thì
 * thẻ vẫn chỉ tay sang lớp 5 — quyển con học xong từ lâu.
 *
 * Nó còn núp dưới một cái bẫy nữa: `Date.parse(m.at || 0) || 0`. Bài chưa có dấu thì
 * `0` bị ép thành chuỗi "0" và đọc ra NĂM 2000 — một con số thật, khác 0, nên `|| 0`
 * phía sau không cứu được. Người viết tưởng đó là đáy; nó không phải.
 */
import { gopTienDoMon } from '../src/chung/lib/soTienDo.js';
import { emptyProgress, recordMicro, saveSpot } from '../src/mon/toan/lib/progress.js';
import { allMicroIds } from '../src/mon/toan/lib/noiDung.js';

let pass = 0, fail = 0;
const t = (n, c) => { c ? pass++ : (fail++, console.log('  ✗', n)); };

/* ── 1 · Gộp sổ: không đổi thì phải trả NGUYÊN khối cũ ── */
const so = { toan: { micros: {} }, tienganh: { micros: {} } };

t('môn trả về đúng sổ cũ → vỏ giữ nguyên khối, không dựng mới',
  gopTienDoMon(so, 'toan', (p) => p) === so);
t('trả thẳng đúng sổ cũ (không qua hàm) cũng giữ nguyên khối',
  gopTienDoMon(so, 'toan', so.toan) === so);

const moi = { micros: { x: {} } };
const sau = gopTienDoMon(so, 'toan', () => moi);
t('có đổi thật thì dựng khối mới', sau !== so);
t('ô của môn được thay đúng', sau.toan === moi);
t('môn KHÁC không bị đụng vào', sau.tienganh === so.tienganh);

/* Vòng lặp thật sự: gọi đi gọi lại như effect của phòng học vẫn phải đứng yên.
   Trước khi sửa, mỗi lượt ở đây là một khối mới → React vẽ lại → effect chạy lại. */
let s = so;
for (let i = 0; i < 50; i++) s = gopTienDoMon(s, 'toan', (p) => saveSpot(p, 'DL:X', 0, 9));
t('ghi đi ghi lại cùng một chỗ dở: sổ đứng yên, không có vòng lặp', s === so);

/* ── 2 · Chỗ đang học dở phải có mốc thời gian ── */
const M0 = allMicroIds()[0];
const dangDo = saveSpot(emptyProgress(), M0, 12, 23);
t('nhớ chỗ dở thì đóng luôn dấu thời gian', !!dangDo.micros[M0].at);
t('dấu ấy đọc ra được ngày giờ thật', Number.isFinite(Date.parse(dangDo.micros[M0].at)));

/* Cái bẫy Date.parse(0) — giữ lại để không ai viết lại kiểu ấy. */
t('Date.parse(0) KHÔNG phải 0 mà là năm 2000 — nên đừng dùng làm đáy',
  Date.parse(0) > 0);

/* ── 3 · Kệ sách: quyển đang học dở phải thắng quyển học xong từ lâu ── */
const mocCua = (m) => (m?.at ? Date.parse(m.at) || 0 : 0);
const gioCua = (p, ids) => ids.reduce((s2, id) => Math.max(s2, mocCua(p.micros[id])), 0);

let P = emptyProgress();
P = recordMicro(P, 'DL:CU.B1.M1', { pass: true, mustOK: true, right: 3, total: 3 });
P.micros['DL:CU.B1.M1'].at = '2020-01-01T00:00:00.000Z';   // quyển cũ, xong từ lâu
P = saveSpot(P, 'DL:MOI.B1.M1', 5, 20);                     // quyển đang học dở HÔM NAY

t('quyển đang học dở hôm nay xếp trên quyển học xong năm 2020',
  gioCua(P, ['DL:MOI.B1.M1']) > gioCua(P, ['DL:CU.B1.M1']));
t('bài chưa từng động vào có mốc đúng bằng 0', mocCua(undefined) === 0);

console.log(`\n${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
