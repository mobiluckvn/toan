/**
 * MÔ PHỎNG 50 BUỔI LUYỆN NÓI — không mạng, không khoá, chạy bằng `node`.
 *
 *     cd web && node tools/mo_phong_buoi.mjs
 *
 * ── VÌ SAO CẦN ──
 * Cổng đơn vị soi từng hàm; phép đo thật qua Groq thì đắt và mỗi lần một kết quả.
 * Giữa hai thứ ấy thiếu một phép đo: cả buổi đi từ đầu tới cuối thì có XONG không,
 * và cô giáo phải lui về câu máy dựng bao nhiêu lần.
 *
 * ── MÔ HÌNH GIẢ, VÀ NÓ GIẢ CÓ CHỦ ĐÍCH ──
 * `LAP` 40% · `NGOAI_VON` 10% — hai tỉ lệ ấy lấy từ chính chỗ hỏng bác bắt ("nó cứ
 * nói đi nói lại") và từ phép đo thật 09-10 (câu đầu bị bác 20,4%). Mô hình giả
 * KHÔNG nghe lời nhắc sửa: nó lặp lại với đúng tỉ lệ ấy ở mọi vòng. Nên con số dưới
 * đây là CẬN DƯỚI — mô hình thật chịu nghe nhắc thì còn tốt hơn.
 *
 * ── BÉ GIẢ ──
 * Mỗi bé một mức khá (`gioi`), quyết định xác suất nói đúng. 50 bé rải từ 0,35 tới
 * 0,95 để không đo đúng một kiểu bé.
 *
 * Bộ sinh ngẫu nhiên TIỀN ĐỊNH (`--hat`): chạy hai lần ra một kết quả, nếu không thì
 * con số nào cũng không ai kiểm lại được.
 */
import { readFileSync } from 'node:fs';
import {
  vonTu, tinhBuoi, luotLuyen, soiCau, cauThayThe, viecTiepTheo, dienBuoc,
} from '../src/mon/tienganh/lib/phongnoi.js';
import { nhanLuot } from '../src/mon/tienganh/lib/nhanluot.js';
import { dungBang, datKeHoach } from '../src/mon/tienganh/lib/bangtrangthai.js';
import { lapKeHoach, capNhatSauLuot, buocHienTai, xongKeHoach } from '../src/mon/tienganh/lib/kehoach.js';
import { chamCau, chamTot, DAT } from '../src/mon/tienganh/lib/chamnoi.js';

const doSo = (ten, mac) => {
  const i = process.argv.indexOf(ten);
  return i > 0 && process.argv[i + 1] ? Number(process.argv[i + 1]) : mac;
};
const SO_BE = doSo('--be', 50);
const LAP = doSo('--lap', 0.4);
const NGOAI_VON = doSo('--ngoai', 0.1);
let hat = doSo('--hat', 20261009);
const ran = () => { hat = (hat * 1103515245 + 12345) % 2147483648; return hat / 2147483648; };

const BAI = ['ta1/DL_TA1_B05', 'ta1/DL_TA1_B09', 'ta3/DL_TA3_B11', 'ta5/DL_TA5_B11']
  .map((p) => JSON.parse(readFileSync(new URL(`../public/content/${p}.json`, import.meta.url), 'utf8')));

/** Cô giáo máy GIẢ: lặp 40%, ngoài vốn 10%, còn lại nói đúng câu của việc. */
function coGiaoGia(viec, tenBe, cauTruoc) {
  if (ran() < LAP && cauTruoc) return cauTruoc;
  if (ran() < NGOAI_VON) return 'I want some delicious chips.';
  const t = cauThayThe(viec, tenBe, '');
  return t?.en || viec?.tu?.tu || 'Hello!';
}

/** Bé GIẢ: `gioi` là xác suất nói trọn câu; không trọn thì bỏ bớt chữ. */
function beGia(dich, gioi) {
  const w = String(dich || '').split(/\s+/).filter(Boolean);
  if (!w.length) return '';
  if (ran() < gioi) return dich;
  if (ran() < 0.15) return '';                       // im lặng
  if (ran() < 0.12) return 'cô ơi con chưa hiểu';    // nói tiếng Việt
  return w.length > 2 ? w.slice(1).join(' ') : w.slice(0, -1).join(' ');
}

const dem = { xongKH: 0, xongDat: 0, hetGio: 0, dang: 0, luot: 0, daThay: 0,
  nhan: {}, buocXong: [], replan: 0 };

for (let n = 0; n < SO_BE; n += 1) {
  const bai = BAI[n % BAI.length];
  const gioi = 0.35 + (0.6 * (n % 10)) / 9;
  const von = vonTu({ baiNay: bai });
  let bang = dungBang({ bai, thich: von.loi.tu[0]?.tu || null, quyen: 'ta1' });
  let kh = lapKeHoach(bang, { von });
  bang = datKeHoach(bang, kh);
  const lichSu = [];
  const batDau = 0;
  let phut = 0;

  for (let i = 0; i < 40; i += 1) {
    const buoi = tinhBuoi({ lichSu, batDau, bayGio: phut * 60000,
      xongKeHoach: xongKeHoach(kh), keHoachConViec: !xongKeHoach(kh) });
    if (buoi.trangThai !== 'dang') {
      /* ⚠ TÁCH HAI LÝ DO KẾT. Gộp chúng thì con số "100% buổi xong" che mất chuyện
         phần lớn buổi kết TRƯỚC khi bé làm hết việc — và §7 đòi đúng con số bị che. */
      if (buoi.trangThai !== 'xongGioi') dem.hetGio += 1;
      else if (xongKeHoach(kh)) dem.xongKH += 1;
      else dem.xongDat += 1;
      break;
    }

    const luotBe = [...lichSu].reverse().find((x) => x.vai === 'be' && x.diem != null) || null;
    const { nhan } = nhanLuot(luotBe, { von });
    dem.nhan[nhan] = (dem.nhan[nhan] || 0) + 1;

    const b = buocHienTai(kh);
    const viec = viecTiepTheo({ von, lichSu, haDoKho: buoi.haDoKho, nhan, buocKH: b });
    const cauTruoc = [...lichSu].reverse().find((x) => x.vai === 'may')?.en || '';
    let en = coGiaoGia(viec, 'Lan', cauTruoc);
    /* Vòng xin lại của V1, rồi mới tới đường lui — đúng thứ tự `hoiCoGiao`. */
    const soi = () => soiCau(en, { von, tenBe: 'Lan', cauTruoc: viec?.giuViec ? '' : cauTruoc });
    for (let v = 0; v < 2 && !soi().ok; v += 1) en = coGiaoGia(viec, 'Lan', cauTruoc);
    if (!soi().ok) { en = cauThayThe(viec, 'Lan', cauTruoc)?.en || en; dem.daThay += 1; }
    dem.luot += 1;
    lichSu.push({ vai: 'may', chu: en, en, vi: 'x', buoc: 'mau', nhan });

    const noi = beGia(en, gioi);
    const kq = en ? { ...chamTot(chamCau, en, [noi]), mau: en } : null;
    lichSu.push({ vai: 'be', chu: noi, diem: kq?.diem ?? null, mau: kq?.mau || null,
      thieu: kq?.thieu || [], thieuChucNang: kq?.thieuChucNang || [] });
    kh = capNhatSauLuot(kh, { nhan, diem: kq?.diem ?? null, bang });
    bang = datKeHoach(bang, kh);
    phut += 1.2;
  }
  if (!xongKeHoach(kh) && dem.xong + dem.hetGio === n) dem.dang += 1;
  dem.buocXong.push(kh.buoc.filter((x) => x.trangThai === 'xong').length / kh.buoc.length);
  dem.replan += kh.soReplan || 0;
}

const pc = (x) => `${(100 * x).toFixed(1)}%`;
console.log(`══════ ${SO_BE} buổi · mô hình giả: lặp ${pc(LAP)} · ngoài vốn ${pc(NGOAI_VON)} ══════`);
console.log(`buổi XONG KẾ HOẠCH                : ${dem.xongKH}  (${pc(dem.xongKH / SO_BE)})`);
console.log(`buổi xong vì ba lượt đạt liền     : ${dem.xongDat}  (${pc(dem.xongDat / SO_BE)})`);
console.log(`buổi hết giờ                      : ${dem.hetGio}  (${pc(dem.hetGio / SO_BE)})`);
console.log(`buổi còn dở (quá 40 lượt)         : ${dem.dang}`);
console.log(`lượt của cô                       : ${dem.luot}`);
console.log(`phải lui về câu máy dựng          : ${dem.daThay}  (${pc(dem.daThay / dem.luot)})`);
console.log(`bước kế hoạch làm xong, trung bình: ${pc(dem.buocXong.reduce((a, b) => a + b, 0) / SO_BE)}`);
console.log(`tổng số lần replan                : ${dem.replan}`);
console.log('phân phối nhãn:', Object.fromEntries(
  Object.entries(dem.nhan).sort((a, b) => b[1] - a[1])));
