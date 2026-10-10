/**
 * BỘ ĐO AN TOÀN NỘI DUNG — kịch bản KB3 của luận văn (mục 3.7.2.c, Bảng 3.29).
 *
 *     node tools/do_an_toan_noi_dung.mjs do            # đo, KHÔNG cần mạng
 *     node tools/do_an_toan_noi_dung.mjs do --vao docs/kb3_dau_ra_tho.json
 *     node tools/do_an_toan_noi_dung.mjs thu           # gọi mô hình thật, cần GROQ_API_KEY
 *
 * ── VÌ SAO PHẢI ĐO Ở HAI VỊ TRÍ ──
 * Bảng 3.29 đòi đo tỷ lệ từ ngoài vốn ở CẢ HAI chỗ: đầu ra THÔ của mô hình, và câu
 * THỰC SỰ đưa cho bé. Chỉ hiệu số giữa hai phép đo mới là đóng góp của tầng hậu
 * kiểm. Đo mỗi một chỗ thì không tách được công của lời nhắc với công của hậu kiểm,
 * và câu "lời nhắc bảo đảm không có từ vượt cấp" thành một lời không kiểm được.
 *
 * ── HAI THỨ TỆP NÀY ĐO, VÀ CHÚNG KHÁC NHAU ──
 *
 *   ① BỘ CHỨNG (không cần mạng). Với mỗi bài, dựng sẵn một tập câu mà ta BIẾT
 *      TRƯỚC đáp án: chứng dương (phải được nhận, mỗi đường công nhận một câu) và
 *      chứng âm (phải bị bác — từ ngoài vốn, ô trống sai loại, câu lặp, câu rỗng).
 *      Đây là phép đo về CHÍNH TẦNG HẬU KIỂM, chạy được ngay, tái lập được, không
 *      phụ thuộc mô hình. Kèm phép thử ĐẢO CHIỀU: tắt từng đường công nhận rồi xem
 *      tỷ lệ bác có tăng đúng ở nhóm câu tương ứng không — đây mới là chứng minh
 *      rằng mỗi đường thật sự có tác dụng, chứ không phải một nhánh mã chết.
 *
 *   ② ĐẦU RA MÔ HÌNH THẬT (cần mạng, lệnh `thu`). Chỉ khi có tệp này thì con số
 *      "OOV thô" mới có nghĩa — nó là tính chất của MÔ HÌNH, không phải của hậu
 *      kiểm, nên không bịa ra được bằng bộ chứng.
 *
 * ⚠ KHÔNG ĐƯỢC ĐỌC KẾT QUẢ CỦA ① THÀNH KẾT QUẢ CỦA ②. Bộ chứng nói "hàng rào đóng
 *   đúng chỗ nó phải đóng"; nó KHÔNG nói "mô hình hay sinh từ lạ tới mức nào". Báo
 *   cáo phải nêu rõ con số nào từ nguồn nào — nên bản in dưới đây tách hẳn hai mục.
 *
 * ⚠ HỒ SƠ NGƯỜI HỌC LÀ GIẢ LẬP: coi như bé đã ĐẠT mọi bài đứng trước. Đó là tình
 *   huống vốn từ RỘNG NHẤT, tức là dễ lọt nhất — chọn có chủ ý, vì đo hàng rào thì
 *   phải đo ở chỗ nó yếu nhất. Con số thu được là CẬN TRÊN của tỷ lệ lọt.
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

import {
  vonCuaBai, vonTu, soiCau, DUONG_CONG_NHAN, LOI_LOP_HOC, loaiOTrong, SO_DEM,
  loiDan, viecTiepTheo,
} from '../web/src/mon/tienganh/lib/phongnoi.js';
import { datDoThi, baiTienQuyet } from '../web/src/mon/tienganh/lib/doThi.js';
import { MO_HINH, NGHI_NGAN, TOKEN_TRA_LOI } from '../web/functions/src/luyennoi.js';

const GOC = join(dirname(fileURLToPath(import.meta.url)), '..');
const NOI_DUNG = join(GOC, 'web/public/content');
const QUYEN = ['ta1', 'ta2', 'ta3', 'ta4', 'ta5'];

/* Tên bé dùng trong mọi phép dựng câu. Cố định để phép đo tái lập được. */
const TEN_BE = 'Bo';

/* ────────────────────────────── nạp dữ liệu ────────────────────────────── */

function napBai() {
  const theoQuyen = new Map();
  const theoId = new Map();
  for (const q of QUYEN) {
    const ds = [];
    for (let i = 0; i <= 40; i += 1) {
      const f = join(NOI_DUNG, q, `DL_${q.toUpperCase()}_B${String(i).padStart(2, '0')}.json`);
      if (!existsSync(f)) continue;
      const b = JSON.parse(readFileSync(f, 'utf8'));
      ds.push(b);
      theoId.set(b.id, b);
    }
    ds.sort((a, b) => (a.so ?? 0) - (b.so ?? 0));
    theoQuyen.set(q, ds);
  }
  return { theoQuyen, theoId };
}

function napDoThiTuDia() {
  const f = join(NOI_DUNG, 'tienganh/do_thi.json');
  const d = JSON.parse(readFileSync(f, 'utf8'));
  datDoThi(d);          // bơm thẳng, khỏi fetch
  return d;
}

/**
 * Chọn bài trải đều năm quyển, PHÂN TẦNG theo số bài của quyển.
 *
 * Không lấy ngẫu nhiên: phép đo phải cho ra cùng kết quả ở hai lần chạy, nếu không
 * thì so hai đợt đo với nhau không có nghĩa. Lấy cách đều theo chỉ số.
 */
function chonBai(theoQuyen, soBai) {
  const tong = QUYEN.reduce((s, q) => s + theoQuyen.get(q).length, 0);
  const ra = [];
  for (const q of QUYEN) {
    const ds = theoQuyen.get(q);
    const lay = Math.max(1, Math.round((ds.length / tong) * soBai));
    for (let i = 0; i < lay && i < ds.length; i += 1) {
      ra.push(ds[Math.floor((i * ds.length) / lay)]);
    }
  }
  return ra;
}

/** Vốn từ của một buổi, với hồ sơ giả lập "đã đạt mọi bài đứng trước". */
function vonCuaBuoi(bai, theoQuyen, theoId, dt) {
  const ds = theoQuyen.get(bai.quyen) || [];
  const i = ds.findIndex((x) => x.id === bai.id);
  const baiCu = i > 0 ? ds.slice(0, i) : [];
  const nut = nutCuaBai(bai);
  const baiTQ = baiTienQuyet(dt, nut, { boQua: bai.id })
    .map((id) => theoId.get(id)).filter(Boolean);
  return vonTu({ baiNay: bai, baiCu, baiTQ, daDat: true, datCu: () => true });
}

function nutCuaBai(bai) {
  const k = bai.knowledgeCore || {};
  const mau = k.mauCauDs?.length ? k.mauCauDs : (k.mauCau ? [k.mauCau] : []);
  return [
    ...(k.vocabulary || []).map((v) => v.ma),
    ...mau.map((m) => m.ma),
  ].filter(Boolean);
}

/* ──────────────────── phép đo TỪ NGOÀI VỐN ở mức TIẾNG ──────────────────── */

const tieng = (s) => String(s || '').toLowerCase().split(/[^a-z']+/).filter(Boolean);

/**
 * Tập tiếng HỢP LỆ của một buổi.
 *
 * ⚠ Đây là phép đo ĐỘC LẬP với `soiCau`, và độc lập là điều kiện để con số có
 * nghĩa: dùng chính `soiCau` để đo đầu ra của `soiCau` thì lúc nào cũng ra 0, và
 * con số 0 ấy không nói lên điều gì.
 *
 * Gồm: mọi tiếng của mục từ vựng (kể cả dạng biến đổi) · mọi tiếng trong mẫu câu
 * và công thức · mọi tiếng trong câu sẵn của sách · mọi tiếng của 14 lời lớp học ·
 * tên riêng · và số đếm KHI bài có ô `[Number]`.
 */
function tiengHopLe(von, tenBe = TEN_BE) {
  const tu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];
  const cau = [...von.loi.cau, ...von.on.flatMap((x) => x.cau)];
  const sach = [...(von.loi.cauSach || []), ...von.on.flatMap((x) => x.cauSach || [])];
  const t = new Set();
  const nap = (s) => tieng(s).forEach((x) => t.add(x));
  for (const v of tu) [v.tu, v.so_nhieu, v.so_it, v.dang_ing, v.dang_qk].forEach(nap);
  for (const c of cau) { nap(c.cau); nap(String(c.congThuc || '').replace(/\[[^\]]+\]/g, ' ')); }
  sach.forEach(nap);
  LOI_LOP_HOC.forEach(nap);
  [tenBe, 'Bill', 'Mai'].forEach(nap);
  if (cau.some((c) => /\[Number\]/i.test(c.congThuc || ''))) SO_DEM.forEach(nap);
  return t;
}

/** Những tiếng của câu KHÔNG nằm trong vốn. Rỗng nghĩa là câu sạch. */
const tiengNgoaiVon = (cauEn, hopLe) => tieng(cauEn).filter((x) => !hopLe.has(x));

/* ─────────────────────────── dựng BỘ CHỨNG ─────────────────────────── */

/* Từ ngoài chương trình tiểu học — đúng dạng "ảo giác từ vựng" mà mục 2.4.2 nêu
   (mô hình dùng `automobile` thay cho `car`). Cố định để phép đo tái lập được. */
const TU_VUOT_CAP = ['automobile', 'vehicle', 'refrigerator', 'astronaut', 'magnificent'];

const dienKhung = (khung, d) =>
  khung.replace(/\s*\+\s*/g, ' ').replace(/\[[^\]]+\]/, d);

/**
 * Bộ chứng của MỘT bài: mỗi câu kèm nhãn `mong` (nhan / bac) và `vi` (vì sao).
 *
 * Chứng dương cố ý nhắm ĐÚNG một đường công nhận mỗi câu, để phép thử đảo chiều
 * sau này quy trách nhiệm được. Chỗ nào một câu lọt qua nhiều đường thì bản in báo
 * ra phần chồng lấn ấy chứ không giấu — chồng lấn không phải lỗi, nhưng người đọc
 * cần biết để không quy hết công cho một đường.
 */
function boChung(bai, von) {
  const tu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];
  const cau = [...von.loi.cau, ...von.on.flatMap((x) => x.cau)];
  const sach = [...(von.loi.cauSach || []), ...von.on.flatMap((x) => x.cauSach || [])];
  const ra = [];
  const them = (nhom, duongNham, en, mong, vi, kem = {}) =>
    ra.push({ baiId: bai.id, quyen: bai.quyen, nhom, duongNham, en, mong, vi, ...kem });

  /* ── chứng DƯƠNG, mỗi đường một câu ── */
  if (tu[0]) them('duong', 'tu', tu[0].tu, 'nhan', 'một mục từ vựng của bài');
  them('duong', 'nghiThuc', LOI_LOP_HOC[0], 'nhan', 'một câu nghi thức lớp học');

  /* ⚠ NỬA THẬT SỰ NÓI ĐƯỢC, không phải mẩu cắt máy móc.
     `nuaCua()` của bộ hậu kiểm tách theo CẢ " - " LẪN "/", nên với
     `"… ? - Yes, I do. / No, I don't."` thì nửa hợp lệ là "No, I don't.", chứ
     chuỗi ghép "Yes, I do. / No, I don't." KHÔNG nằm trong tập ấy. Bản đầu của bộ
     đo cắt máy móc ở " - " rồi báo 5 câu "bị bác oan" — lỗi của phép đo, không phải
     của hàng rào. Lấy mẩu CUỐI của lần tách cuối thì ra đúng câu bé sẽ nói. */
  const nuaNoiDuoc = (s) => {
    const a = String(s || '').split(' - ');
    return a[a.length - 1].split('/').pop().trim();
  };
  const capDoi = cau.find((c) => String(c.cau).includes(' - ') || String(c.cau).includes('/'));
  if (capDoi) {
    them('duong', 'nuaMauCau', nuaNoiDuoc(capDoi.cau), 'nhan', 'nửa ĐÁP của một cặp hỏi–đáp');
  } else if (cau[0]) {
    them('duong', 'nuaMauCau', cau[0].cau, 'nhan', 'một mẫu câu nguyên vẹn');
  }

  /* Ưu tiên câu sách KHÔNG trùng bất kỳ nửa mẫu câu nào — nếu không thì phép thử
     đảo chiều bảo "đường khác đỡ hết", và ta không biết đường `cauSach` có tác
     dụng thật hay chỉ là một nhánh mã chết. */
  const nuaCauDs = new Set(cau.flatMap((c) => {
    const t = String(c.cau || '');
    return [t, ...t.split(' - ').flatMap((x) => x.split('/'))].map((x) => x.trim().toLowerCase());
  }));
  const sachRieng = sach.find((s) => !nuaCauDs.has(String(s).trim().toLowerCase())) || sach[0];
  if (sachRieng) them('duong', 'cauSach', sachRieng, 'nhan', 'một câu có sẵn trong sách');

  /* Công thức MỘT ô trống mới dựng được câu hoàn chỉnh. Công thức hai ô thì phép
     điền chỉ thay ô đầu — dùng làm chứng dương là sai, và chính chỗ ấy là lỗ hổng
     đã tìm ra (xem chứng âm bên dưới). */
  const motO = (s) => (String(s || '').match(/\[[^\]]+\]/g) || []).length === 1;
  const khungMotO = cau.find((c) => c.congThuc && loaiOTrong(c.congThuc) && motO(c.congThuc));
  const khungNhieuO = cau.find((c) => c.congThuc && loaiOTrong(c.congThuc) && !motO(c.congThuc));
  if (khungMotO) {
    const loai = loaiOTrong(khungMotO.congThuc);
    /* Chọn từ KHÔNG xuất hiện trong mẫu câu/câu sách, để câu dựng ra không tình cờ
       trùng một câu đã được đường khác công nhận. */
    const daCo = new Set([...cau.map((c) => c.cau), ...sach].join(' ').toLowerCase().split(/\s+/));
    const chon = tu.find((t) => !daCo.has(String(t.tu).toLowerCase())) || tu[0];
    /* ── ⚠ ĐIỀN ĐÚNG DẠNG MÀ Ô ĐÒI, KHÔNG ĐIỀN DẠNG GỐC ──
       Bản đầu luôn điền `chon.tu`. Với ô `[Verb-ing]` nó dựng ra «I like go for a
       walk» rồi khai đó là chứng DƯƠNG — một câu sai ngữ pháp mà hàng rào PHẢI bác.
       Hai câu như thế hiện lên báo cáo dưới nhãn «hàng rào đóng quá tay», tức bộ đo
       báo lỗi của CHÍNH NÓ thành lỗi của thứ nó đang đo. Người đọc báo cáo sẽ đi
       nới hàng rào — đúng cái bẫy «cổng ép người ta nới mã» mà kho này đã dính bốn
       lần, lần này còn nguy hơn vì hàng rào ấy là thứ chặn từ vượt cấp tới tay bé.

       Thiếu dạng cần thì BỎ HẲN chứng ấy, không lùi về dạng gốc: một chứng dương
       sai còn tệ hơn không có chứng nào. */
    const dangCua = { ing: 'dang_ing', qk: 'dang_qk', nhieu: 'so_nhieu' }[loai];
    const d = loai === 'ten' ? TEN_BE
      : (dangCua ? (chon?.[dangCua] || null) : chon?.tu || null);
    if (d) {
      them('duong', 'congThuc', dienKhung(khungMotO.congThuc, d), 'nhan',
        `công thức MỘT ô đã điền đúng loại (${loai})`);
    }
  }

  /* ── chứng ÂM ── */
  const vuot = TU_VUOT_CAP[bai.id.length % TU_VUOT_CAP.length];
  them('am', null, vuot, 'bac', 'từ ngoài chương trình tiểu học (ảo giác từ vựng)');

  /* Ô TÊN NGƯỜI bị nhét ĐỒ VẬT — đúng lỗi "Bye, bike." đã quan sát được thật với
     Groq. CHỈ dựng cho ô loại `ten`: chiều ngược lại (ô danh từ nhét tên người)
     KHÔNG dùng làm chứng âm được, vì bài nào cũng thường dạy kèm một mẫu
     `This is + [Name].`, nên "This is Bill." là câu ĐÚNG của chính bài — bản đầu
     của bộ đo báo nhầm nó là "hàng rào thủng". */
  const khungTen = cau.find((c) => c.congThuc && loaiOTrong(c.congThuc) === 'ten' && motO(c.congThuc));
  if (khungTen && tu[0]) {
    them('am', null, dienKhung(khungTen.congThuc, tu[0].tu), 'bac',
      'ô [Name] bị điền một ĐỒ VẬT');
  }

  /* CÔNG THỨC HAI Ô CHỈ ĐIỀN Ô ĐẦU — ô sau còn nguyên dấu ngoặc.
     Đây là lỗ hổng tìm ra 26-08: `gonCau` bóc sạch dấu ngoặc trước khi so, nên
     "It's in [Month B]." khớp với chính nó và ĐƯỢC NHẬN. Giữ làm chứng âm cố định
     để lần sau ai nới `soiCau` là cổng đỏ ngay. */
  if (khungNhieuO && tu[0]) {
    const loai = loaiOTrong(khungNhieuO.congThuc);
    them('am', null, dienKhung(khungNhieuO.congThuc, loai === 'ten' ? TEN_BE : tu[0].tu), 'bac',
      'công thức hai ô, ô sau CHƯA ĐIỀN (còn dấu ngoặc)', { bacMong: 'oTrong' });
  }

  if (cau[0]) {
    /* Câu vượt cấp ghép vào khuôn của bài: đúng ngữ pháp, sai vốn từ. */
    const khung = cau[0].congThuc;
    if (khung && loaiOTrong(khung) === 'tu' && motO(khung)) {
      them('am', null, dienKhung(khung, vuot), 'bac', 'khuôn đúng nhưng điền từ vượt cấp');
    }
  }

  them('am', null, '', 'bac', 'câu rỗng', { bacMong: 'rong' });

  if (tu[0]) {
    them('am', null, tu[0].tu, 'bac', 'lặp Y HỆT câu lượt trước',
      { cauTruoc: tu[0].tu, bacMong: 'lap' });
  }
  return ra;
}

/* ─────────────────────────── LỆNH `do` ─────────────────────────── */

function lenhDo({ soBai, tepTho }) {
  const dt = napDoThiTuDia();
  const { theoQuyen, theoId } = napBai();
  const ds = chonBai(theoQuyen, soBai);

  const chung = [];
  const vonTheoBai = new Map();
  for (const bai of ds) {
    const von = vonCuaBuoi(bai, theoQuyen, theoId, dt);
    vonTheoBai.set(bai.id, von);
    chung.push(...boChung(bai, von));
  }

  /* ── ① đo trên bộ chứng ── */
  const theoDuong = Object.fromEntries(DUONG_CONG_NHAN.map((d) => [d, 0]));
  const theoBac = { rong: 0, lap: 0, oTrong: 0, ngoaiVon: 0 };
  let duongDat = 0; let duongTruot = 0; let amDat = 0; let amLot = 0;
  const truot = []; const lot = [];

  for (const c of chung) {
    const von = vonTheoBai.get(c.baiId);
    const kq = soiCau(c.en, { von, tenBe: TEN_BE, cauTruoc: c.cauTruoc || '' });
    c.kq = kq;
    if (kq.ok) theoDuong[kq.duong] += 1; else theoBac[kq.bac] += 1;

    if (c.mong === 'nhan') {
      if (kq.ok) duongDat += 1;
      else { duongTruot += 1; truot.push(c); }
    } else if (!kq.ok) amDat += 1;
    else { amLot += 1; lot.push(c); }
  }

  /* ── OOV mức tiếng trên những câu ĐƯỢC NHẬN ── */
  let oovSau = 0; const oovViDu = [];
  for (const c of chung.filter((x) => x.kq.ok)) {
    const ngoai = tiengNgoaiVon(c.en, tiengHopLe(vonTheoBai.get(c.baiId)));
    if (ngoai.length) { oovSau += 1; oovViDu.push({ ...c, ngoai }); }
  }

  /* ── ② phép thử ĐẢO CHIỀU ── */
  const daoChieu = [];
  for (const d of DUONG_CONG_NHAN) {
    let batDauNhan = 0; let nayBac = 0; let duongKhacDo = 0;
    for (const c of chung) {
      if (!c.kq.ok || c.kq.duong !== d) continue;
      batDauNhan += 1;
      const lai = soiCau(c.en, {
        von: vonTheoBai.get(c.baiId), tenBe: TEN_BE, cauTruoc: c.cauTruoc || '',
        tat: new Set([d]),
      });
      if (lai.ok) duongKhacDo += 1; else nayBac += 1;
    }
    daoChieu.push({ duong: d, batDauNhan, nayBac, duongKhacDo });
  }

  /* ── ③ đầu ra mô hình thật, nếu có ── */
  let tho = null;
  if (tepTho && existsSync(tepTho)) {
    const g = JSON.parse(readFileSync(tepTho, 'utf8'));
    tho = doDauRaTho(g, vonTheoBai, theoQuyen, theoId, dt);
  }

  const kq = {
    chay: { soBai: ds.length, soCauChung: chung.length, tenBe: TEN_BE },
    boChung: {
      chungDuong: { tong: duongDat + duongTruot, dat: duongDat, truot: duongTruot },
      chungAm: { tong: amDat + amLot, bacDung: amDat, lot: amLot },
      theoDuong, theoBac,
      oovSauHauKiem: oovSau,
    },
    daoChieu,
    dauRaTho: tho,
  };
  inRa(kq, { truot, lot, oovViDu });
  const ra = join(GOC, 'docs/kb3_ket_qua.json');
  writeFileSync(ra, JSON.stringify(kq, null, 2));
  console.log(`\n  → đã ghi ${ra}\n`);
  return (duongTruot || amLot || oovSau) ? 1 : 0;
}

/** Đo tệp đầu ra thô do lệnh `thu` sinh ra. */
function doDauRaTho(goi, vonTheoBai, theoQuyen, theoId, dt) {
  let tong = 0; let oovTho = 0; let oovSau = 0; let bac = 0; let lap = 0; let saiKhuon = 0;
  const theoDuong = Object.fromEntries(DUONG_CONG_NHAN.map((d) => [d, 0]));
  for (const r of (goi.ban || [])) {
    tong += 1;
    if (r.saiKhuon) saiKhuon += 1;
    let von = vonTheoBai.get(r.baiId);
    if (!von) {
      const bai = theoId.get(r.baiId);
      if (!bai) continue;
      von = vonCuaBuoi(bai, theoQuyen, theoId, dt);
      vonTheoBai.set(r.baiId, von);
    }
    const hopLe = tiengHopLe(von);
    const truocHauKiem = tiengNgoaiVon(r.en, hopLe).length > 0;
    if (truocHauKiem) oovTho += 1;
    const kq = soiCau(r.en, { von, tenBe: TEN_BE, cauTruoc: r.cauTruoc || '' });
    if (kq.ok) {
      theoDuong[kq.duong] += 1;
      if (tiengNgoaiVon(r.en, hopLe).length) oovSau += 1;
    } else {
      bac += 1;
      if (kq.bac === 'lap') lap += 1;
    }
  }
  return {
    moHinh: goi.moHinh || null, luc: goi.luc || null,
    tong,
    oovTho, tiLeOovTho: tong ? +(oovTho / tong).toFixed(4) : null,
    oovSauHauKiem: oovSau, tiLeOovSau: tong ? +(oovSau / tong).toFixed(4) : null,
    biBacBo: bac, tiLeBacBo: tong ? +(bac / tong).toFixed(4) : null,
    lapCau: lap, saiKhuonTraVe: saiKhuon,
    theoDuong,
  };
}

/* ─────────────────────────── bản in ─────────────────────────── */

const pt = (a, b) => (b ? `${((a / b) * 100).toFixed(1)}%` : '—');

function inRa(k, { truot, lot, oovViDu }) {
  const b = k.boChung;
  console.log(`\n══════ KB3 · ĐO AN TOÀN NỘI DUNG ══════`);
  console.log(`  ${k.chay.soBai} bài · ${k.chay.soCauChung} câu chứng · tên bé "${k.chay.tenBe}"`);

  console.log(`\n── ① BỘ CHỨNG (đo TẦNG HẬU KIỂM, không cần mạng) ──`);
  console.log(`  chứng DƯƠNG được nhận : ${b.chungDuong.dat}/${b.chungDuong.tong}`
    + `  (${pt(b.chungDuong.dat, b.chungDuong.tong)})`);
  console.log(`  chứng ÂM bị bác đúng  : ${b.chungAm.bacDung}/${b.chungAm.tong}`
    + `  (${pt(b.chungAm.bacDung, b.chungAm.tong)})`);
  console.log(`  OOV sau hậu kiểm      : ${b.oovSauHauKiem}   ${b.oovSauHauKiem === 0 ? '✓ đúng thiết kế (phải bằng 0)' : '✗ CÓ TỪ NGOÀI VỐN LỌT QUA'}`);
  console.log(`  câu nhận theo đường   : ${DUONG_CONG_NHAN.map((d) => `${d}=${b.theoDuong[d]}`).join(' · ')}`);
  console.log(`  câu bác theo lý do    : rỗng=${b.theoBac.rong} · lặp=${b.theoBac.lap} · ô trống chưa điền=${b.theoBac.oTrong} · ngoài vốn=${b.theoBac.ngoaiVon}`);

  if (truot.length) {
    console.log(`\n  ✗ CHỨNG DƯƠNG BỊ BÁC OAN (${truot.length}) — hàng rào đóng quá tay:`);
    truot.slice(0, 8).forEach((c) => console.log(`     ${c.baiId} [${c.duongNham}] "${c.en}" — ${c.vi}`));
  }
  if (lot.length) {
    console.log(`\n  ✗ CHỨNG ÂM LỌT QUA (${lot.length}) — hàng rào thủng:`);
    lot.slice(0, 8).forEach((c) => console.log(`     ${c.baiId} "${c.en}" — ${c.vi} (nhận qua đường ${c.kq.duong})`));
  }
  if (oovViDu.length) {
    console.log(`\n  ✗ TỪ NGOÀI VỐN LỌT QUA HẬU KIỂM (${oovViDu.length}):`);
    oovViDu.slice(0, 8).forEach((c) => console.log(`     ${c.baiId} "${c.en}" — tiếng lạ: ${c.ngoai.join(', ')}`));
  }

  console.log(`\n── ② PHÉP THỬ ĐẢO CHIỀU (tắt từng đường công nhận) ──`);
  console.log(`  ${'đường'.padEnd(12)}${'đang nhận'.padStart(10)}${'tắt → bị bác'.padStart(14)}${'đường khác đỡ'.padStart(15)}   kết luận`);
  for (const d of k.daoChieu) {
    const ket = d.batDauNhan === 0 ? 'KHÔNG CÓ CÂU NÀO — bộ chứng chưa phủ tới đường này'
      : (d.nayBac > 0 ? '✓ có tác dụng thật' : '⚠ đường khác đỡ hết — chưa chứng minh được');
    console.log(`  ${d.duong.padEnd(12)}${String(d.batDauNhan).padStart(10)}`
      + `${String(d.nayBac).padStart(14)}${String(d.duongKhacDo).padStart(15)}   ${ket}`);
  }

  console.log(`\n── ③ ĐẦU RA MÔ HÌNH THẬT ──`);
  if (!k.dauRaTho) {
    console.log(`  chưa có. Chạy \`node tools/do_an_toan_noi_dung.mjs thu\` (cần GROQ_API_KEY),`);
    console.log(`  rồi \`... do --vao docs/kb3_dau_ra_tho.json\`.`);
    console.log(`  ⚠ Không có mục này thì KHÔNG được báo cáo con số "OOV thô": bộ chứng đo`);
    console.log(`    hàng rào, không đo mô hình.`);
  } else {
    const t = k.dauRaTho;
    console.log(`  mô hình: ${t.moHinh} · thu lúc ${t.luc} · ${t.tong} lượt`);
    console.log(`  OOV THÔ (trước hậu kiểm) : ${t.oovTho}/${t.tong}  (${pt(t.oovTho, t.tong)})`);
    console.log(`  OOV SAU hậu kiểm         : ${t.oovSauHauKiem}/${t.tong}  (${pt(t.oovSauHauKiem, t.tong)})`
      + `${t.oovSauHauKiem === 0 ? '  ✓ đúng thiết kế' : '  ✗ THỦNG'}`);
    console.log(`  → ĐÓNG GÓP CỦA HẬU KIỂM  : ${(((t.oovTho - t.oovSauHauKiem) / (t.tong || 1)) * 100).toFixed(1)} điểm phần trăm`);
    console.log(`  bị bác bỏ                : ${t.biBacBo}/${t.tong}  (${pt(t.biBacBo, t.tong)})`);
    console.log(`  lặp câu                  : ${t.lapCau}`);
    console.log(`  sai khuôn trả về         : ${t.saiKhuonTraVe}`);
    console.log(`  nhận theo đường          : ${DUONG_CONG_NHAN.map((d) => `${d}=${t.theoDuong[d]}`).join(' · ')}`);
  }
  console.log('');
}

/* ─────────────────────────── LỆNH `thu` ─────────────────────────── */

async function lenhThu({ soBai, soLuot }) {
  const khoa = process.env.GROQ_API_KEY;
  if (!khoa) {
    console.error('✗ thiếu GROQ_API_KEY.\n'
      + '  export GROQ_API_KEY=...   rồi chạy lại.\n'
      + '  ⚠ Khoá này tiêu tiền thật — mỗi lượt là một lời gọi.');
    return 1;
  }
  const dt = napDoThiTuDia();
  const { theoQuyen, theoId } = napBai();
  const ds = chonBai(theoQuyen, soBai);
  console.log(`\n  thu ${ds.length} bài × ${soLuot} lượt = ${ds.length * soLuot} lời gọi tới ${MO_HINH}\n`);

  const ban = [];
  for (const bai of ds) {
    const von = vonCuaBuoi(bai, theoQuyen, theoId, dt);
    const lop = Number(bai.grade) || 1;
    let cauTruoc = '';
    for (let i = 0; i < soLuot; i += 1) {
      const lichSu = cauTruoc
        ? [{ vai: 'may', chu: cauTruoc, en: cauTruoc }, { vai: 'be', chu: cauTruoc }] : [];
      const viec = viecTiepTheo({ von, lichSu, haDoKho: false, hoSo: null });
      const dan = loiDan({ von, tenBe: TEN_BE, lop, viec, hoSo: null, unit: null });
      const r = await goiGroq(khoa, dan, lichSu);
      ban.push({
        baiId: bai.id, quyen: bai.quyen, viTri: 'phongnoi', lanThu: i,
        en: r.en, vi: r.vi, saiKhuon: r.saiKhuon, cauTruoc,
      });
      cauTruoc = r.en || cauTruoc;
      process.stdout.write('.');
    }
    process.stdout.write(` ${bai.id}\n`);
  }
  const goi = { moHinh: MO_HINH, luc: new Date().toISOString(), tenBe: TEN_BE, ban };
  const ra = join(GOC, 'docs/kb3_dau_ra_tho.json');
  writeFileSync(ra, JSON.stringify(goi, null, 2));
  console.log(`\n  → đã ghi ${ban.length} lượt vào ${ra}`);
  console.log(`  giờ chạy: node tools/do_an_toan_noi_dung.mjs do --vao docs/kb3_dau_ra_tho.json\n`);
  return 0;
}

/**
 * Gọi Groq bằng ĐÚNG mô hình và tham số của `functions/src/luyennoi.js`.
 *
 * ⚠ Lệch một tham số là đo một hệ thống khác. Nên nhập hằng từ chính tệp ấy chứ
 * không gõ lại — và ghi tên mô hình vào tệp kết quả, vì nhà cung cấp có thể đổi
 * trọng số giữa hai đợt đo mà không báo (mục 3.5.9).
 */
async function goiGroq(khoa, loiDanChu, lichSu) {
  const messages = [
    { role: 'system', content: loiDanChu },
    ...lichSu.map((x) => ({ role: x.vai === 'may' ? 'assistant' : 'user', content: x.chu })),
  ];
  const r = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${khoa}` },
    body: JSON.stringify({
      model: MO_HINH,
      messages,
      temperature: 0.4,
      max_tokens: TOKEN_TRA_LOI,
      reasoning_effort: NGHI_NGAN,
      response_format: { type: 'json_object' },
    }),
  });
  if (!r.ok) return { en: '', vi: '', saiKhuon: true };
  const j = await r.json();
  const chu = j?.choices?.[0]?.message?.content || '';
  try {
    const o = JSON.parse(chu);
    return { en: String(o.en || '').trim(), vi: String(o.vi || '').trim(), saiKhuon: !o.en };
  } catch { return { en: '', vi: '', saiKhuon: true }; }
}

/* ─────────────────────────── cửa vào ─────────────────────────── */

const cd = process.argv.slice(2);
const lenh = cd.find((x) => !x.startsWith('--')) || 'do';
const so = (ten, mac) => {
  const i = cd.indexOf(ten);
  return i >= 0 ? Number(cd[i + 1]) || mac : mac;
};
const chu = (ten) => {
  const i = cd.indexOf(ten);
  return i >= 0 ? cd[i + 1] : null;
};

let ma = 0;
if (lenh === 'thu') {
  ma = await lenhThu({ soBai: so('--so-bai', 30), soLuot: so('--luot', 20) });
} else if (lenh === 'do') {
  const t = chu('--vao');
  ma = lenhDo({ soBai: so('--so-bai', 30), tepTho: t ? join(GOC, t) : null });
} else {
  console.error(`Lệnh lạ: ${lenh}. Dùng \`do\` hoặc \`thu\`.`);
  ma = 1;
}
process.exit(ma);
