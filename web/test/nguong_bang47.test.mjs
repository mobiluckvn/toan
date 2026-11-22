/**
 * CỔNG · BẢNG 4.7 — sáu điểm phần quản lý ngưỡng chưa khớp thiết kế ở mục 3.8.
 *
 * Mỗi khối dưới đây canh MỘT điểm, và canh bằng HÀNH VI chứ không chỉ bằng chữ trong
 * mã: đổi bộ ngưỡng → quyết định phải đổi theo. Một cổng chỉ soi regex thì xanh cả
 * khi lời gọi nằm trong một nhánh không bao giờ chạy.
 *
 *   1 · máy con đọc BẢNG `nguong` (có bản nhớ, tệp tĩnh, mặc định; không treo)
 *   2 · màn chuyên gia ghi được cho PHẠM VI HẸP, soi trên bộ hiệu lực của phạm vi
 *   3 · số phiên bản và "giá trị cũ" lấy từ BẢNG, trong giao dịch, không trùng số
 *   4 · ngưỡng đọc LÚC DÙNG, kèm ngữ cảnh — cả máy con lẫn sổ bố mẹ, ΔC ở máy chủ
 *   5 · hằng số gõ cứng nay là NG22–NG30, mặc định đúng bằng con số cũ
 *   (điểm 6 — NG20 — ở `nguong_ng20.test.mjs`, vì nó soi cả kho nội dung thật)
 *
 * ⚠ BỘ ĐANG HÀNH LÀ MỘT Ô NHỚ DÙNG CHUNG cho cả tiến trình. Mọi phép thử đổi nó đều
 *   trả lại `BO_MAC_DINH` (và ngữ cảnh rỗng) trong `finally`, để cổng sau không chạy
 *   trên bộ của cổng trước.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

import * as con from '../src/chung/lib/nguong.js';
import * as may from '../functions/src/nguong.js';
import { napNguong, quenNguong, LOI_NAP, KHOA_NHO } from '../src/chung/lib/napNguong.js';
import { layBoNguong, quenNguong as quenMayChu } from '../functions/src/napNguong.js';
import { phatHanhNguong, docBangNguong, maTaiLieu, DEM_PHIEN_BAN } from '../src/chung/lib/ghiNguong.js';
import { PHAM_VI_CHON, phamViHopLe } from '../src/chung/lib/phamViNguong.js';
import { TEN_NGUONG } from '../src/chung/lib/tenNguong.js';
import { TEN_DINH_DANG, tiLeDung } from '../src/mon/tienganh/lib/hoso.js';
import { viecTiepCuaNut, viecTiepCuaBai, duocVuotAi, vectorS, VIEC } from '../src/mon/tienganh/lib/chinhsach.js';
import { daThuDu, duocBoQua } from '../src/mon/tienganh/lib/dandat.js';
import { nhomCua, NHOM } from '../src/mon/tienganh/lib/zpd.js';
import { nutGocRe, congHuong, nguongTran } from '../src/mon/tienganh/lib/lantruyen.js';
import { bacCefr } from '../src/mon/tienganh/lib/cefr.js';
import { dungPhuDao, cauTinhCuaNut } from '../src/mon/tienganh/lib/phudao.js';
import { pickMicro } from '../src/mon/toan/lib/adaptive.js';
import { buildParentReport, stuckItems, metMoi } from '../functions/src/report.js';
import { gomTheoMau } from '../functions/src/ara.js';
import { quenDan } from '../functions/src/bkt.js';
import { soiGoiPhuDao } from '../functions/src/phudao.js';
import { lichOnMacDinh, buildReviewCards } from '../functions/src/schedule.js';

const doc = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');

/** Chạy `viec` với một bộ ngưỡng của PHIÊN (máy con), rồi trả lại bộ mặc định. */
async function voiBo(bo, viec, nguCanh = {}) {
  con.datBoNguong(bo);
  con.datNguCanh(nguCanh);
  try { return await viec(); } finally { con.datBoNguong(con.BO_MAC_DINH); con.datNguCanh({}); }
}
const bo = (macDinh = {}, theoPhamVi = {}) => ({ phienBan: 9, macDinh: { ...con.MAC_DINH, ...macDinh }, theoPhamVi });

/* ════════════════════ 1 · MÁY CON ĐỌC BẢNG `nguong` ════════════════════ */

/** Kho nhớ giả, kiểu `localStorage`. `hong` = mọi lời gọi đều ném (chế độ riêng tư). */
const khoGia = (dau = {}, hong = false) => {
  const m = new Map(Object.entries(dau));
  const chan = () => { if (hong) throw new Error('SecurityError'); };
  return {
    m,
    getItem: (k) => { chan(); return m.has(k) ? m.get(k) : null; },
    setItem: (k, v) => { chan(); m.set(k, String(v)); },
    removeItem: (k) => { chan(); m.delete(k); },
  };
};
const DONG = [
  { ma: 'NG07', giaTri: 0.92, phienBan: 6, phamVi: { loai: 'toanHe' } },
  { ma: 'NG09', giaTri: 5, phienBan: 6, phamVi: { loai: 'khoiLop', khoa: '3' } },
  { ma: 'NG04', giaTri: 0.05, phienBan: 5, phamVi: { loai: 'dangCau', khoa: 'go' } },
];
const tepTinh = async () => ({ phienBan: 1, macDinh: { ...con.MAC_DINH, NG07: 0.81 }, theoPhamVi: {} });

async function nap(opt) {
  quenNguong();
  try { return await napNguong(opt); } finally { quenNguong(); }
}

test('1 · đọc BẢNG `nguong`: cùng hình dạng với máy chủ, và ghi bản nhớ', async () => {
  const kho = khoGia();
  try {
    const b = await nap({ docBang: async () => DONG, kho, taiTep: tepTinh });
    assert.equal(LOI_NAP.nguon, 'bang');
    assert.equal(con.layNguong(b, 'NG07'), 0.92);
    assert.equal(con.layNguong(b, 'NG09', { khoiLop: '3' }), 5);
    assert.equal(con.layNguong(b, 'NG09', { khoiLop: '1' }), 3, 'khối khác giữ mặc định');
    assert.equal(con.layNguong(b, 'NG04', { dangCau: 'go' }), 0.05);
    assert.equal(b.phienBan, 6);
    assert.ok(kho.m.has(KHOA_NHO), 'đọc được bảng thì phải nhớ lại cho lần mất mạng');

    /* Máy chủ đọc CÙNG các dòng ấy phải ra CÙNG bộ — một luật đổi duy nhất. */
    quenMayChu();
    const giaDb = { collection: () => ({ get: async () => ({ forEach: (f) => DONG.forEach((x) => f({ data: () => x })) }) }) };
    const bm = await layBoNguong(giaDb);
    assert.deepEqual(bm.theoPhamVi, b.theoPhamVi);
    assert.deepEqual(bm.macDinh, b.macDinh);
    assert.equal(bm.phienBan, b.phienBan);
  } finally { quenMayChu(); may.datBoNguong(may.BO_MAC_DINH); con.datBoNguong(con.BO_MAC_DINH); }
});

test('1 · mất mạng thì dùng BẢN NHỚ của lần trước, không tụt về mặc định', async () => {
  const kho = khoGia({ [KHOA_NHO]: JSON.stringify({ luc: 1, bo: { phienBan: 4, macDinh: { NG07: 0.9 }, theoPhamVi: {} } }) });
  try {
    const b = await nap({ docBang: async () => { throw new Error('unavailable'); }, kho, taiTep: tepTinh });
    assert.equal(LOI_NAP.nguon, 'nhoTam');
    assert.equal(con.layNguong(b, 'NG07'), 0.9);
    assert.equal(b.phienBan, 4);
  } finally { con.datBoNguong(con.BO_MAC_DINH); }
});

test('1 · bảng TREO thì không treo theo: hết hạn chót là lùi, trong vòng vài trăm mili-giây', async () => {
  const kho = khoGia();
  const t0 = Date.now();
  try {
    const b = await nap({ docBang: () => new Promise(() => {}), kho, taiTep: tepTinh, choToiDa: 60 });
    const lau = Date.now() - t0;
    assert.ok(lau < 1500, `chờ ${lau} ms — màn trắng trước mặt bé`);
    assert.equal(LOI_NAP.nguon, 'tep', 'không có bản nhớ thì lùi về tệp tĩnh');
    assert.equal(con.layNguong(b, 'NG07'), 0.81);
  } finally { con.datBoNguong(con.BO_MAC_DINH); }
});

test('1 · cả bảng lẫn tệp đều hỏng → bộ mặc định, và ĐẾM lần lùi', async () => {
  const truoc = LOI_NAP.lui;
  try {
    const b = await nap({
      docBang: async () => { throw new Error('x'); }, kho: khoGia(),
      taiTep: async () => { throw new Error('offline'); },
    });
    assert.equal(LOI_NAP.nguon, 'macDinh');
    assert.equal(LOI_NAP.lui, truoc + 1);
    assert.deepEqual(b.macDinh, con.MAC_DINH);
  } finally { con.datBoNguong(con.BO_MAC_DINH); }
});

test('1 · chưa đăng nhập (đọc bảng trả null) → bản nhớ; kho nhớ hỏng cũng không làm vỡ', async () => {
  try {
    const b = await nap({ docBang: async () => null, kho: khoGia({}, true), taiTep: tepTinh });
    assert.equal(LOI_NAP.nguon, 'tep');
    assert.equal(con.layNguong(b, 'NG07'), 0.81);
    const b2 = await nap({ docBang: async () => DONG, kho: khoGia({}, true), taiTep: tepTinh });
    assert.equal(LOI_NAP.nguon, 'bang', 'không ghi được bản nhớ thì vẫn dùng bảng');
    assert.equal(con.layNguong(b2, 'NG07'), 0.92);
  } finally { con.datBoNguong(con.BO_MAC_DINH); }
});

test('1 · bảng đọc được mà RỖNG → bỏ bản nhớ cũ (đã lỗi thời), dùng tệp tĩnh', async () => {
  const kho = khoGia({ [KHOA_NHO]: JSON.stringify({ bo: { phienBan: 4, macDinh: { NG07: 0.9 } } }) });
  try {
    const b = await nap({ docBang: async () => [], kho, taiTep: tepTinh });
    assert.equal(LOI_NAP.nguon, 'tep');
    assert.equal(con.layNguong(b, 'NG07'), 0.81);
    assert.equal(kho.m.has(KHOA_NHO), false);
  } finally { con.datBoNguong(con.BO_MAC_DINH); }
});

test('1 · MỘT LẦN MỖI PHIÊN: gọi lại không đọc bảng lần nữa', async () => {
  let lan = 0;
  quenNguong();
  try {
    const opt = { docBang: async () => { lan += 1; return DONG; }, kho: khoGia(), taiTep: tepTinh };
    const [a, b] = await Promise.all([napNguong(opt), napNguong(opt)]);
    await napNguong(opt);
    assert.equal(lan, 1, 'phiên đang chạy phải giữ bộ đã tải (mục 3.8.4)');
    assert.equal(a, b);
  } finally { quenNguong(); con.datBoNguong(con.BO_MAC_DINH); }
});

test('1 · đường thật: đọc Firestore, chờ phiên đăng nhập, có hạn chót; main.jsx vẫn chờ trước App', () => {
  const s = doc('../src/chung/lib/napNguong.js');
  assert.match(s, /getDocs\(collection\(nt\.db, 'nguong'\)\)/, 'máy con phải đọc bảng `nguong`');
  assert.match(s, /authStateReady/, 'luật chỉ cho tài khoản đã đăng nhập đọc — phải chờ phiên');
  assert.match(s, /localStorage/);
  assert.match(s, /CHO_TOI_DA_MS = 3000/);
  const m = doc('../src/main.jsx');
  assert.ok(m.indexOf('await napNguong()') < m.indexOf("import('./App.jsx')"));
});

/* ════════════════════ 2 · PHẠM VI HẸP TRÊN MÀN CHUYÊN GIA ════════════════════ */

test('2 · màn chọn được ít nhất khối lớp 1–5, hai môn, dạng câu, loại nút', () => {
  const khoa = (loai) => (PHAM_VI_CHON.find((x) => x.loai === loai)?.khoa || []).map(([k]) => k);
  assert.deepEqual(khoa('khoiLop'), ['1', '2', '3', '4', '5']);
  assert.deepEqual(khoa('mon'), ['toan', 'tienganh']);
  for (const d of Object.keys(TEN_DINH_DANG)) {
    assert.ok(khoa('dangCau').includes(d), `dạng câu Tiếng Anh '${d}' không chọn được`);
  }
  for (const t of ['vocabulary', 'grammar', 'pronunciation']) assert.ok(khoa('loaiNut').includes(t));
  /* Danh sách khoá phải là nấc THẬT của thang, không thì ghi ra một dòng không ai đọc. */
  for (const x of PHAM_VI_CHON) assert.ok(con.THANG_PHAM_VI.includes(x.loai), x.loai);
  assert.equal(phamViHopLe({ loai: 'khoiLop', khoa: '3' }), '');
  assert.notEqual(phamViHopLe({ loai: 'khoiLop', khoa: '9' }), '');
  assert.notEqual(phamViHopLe({ loai: 'nut', khoa: '' }), '', 'khoá rỗng sẽ bị coi là toàn hệ');
  assert.notEqual(phamViHopLe({ loai: 'nut', khoa: 'a/b' }), '');
});

/**
 * KHO FIRESTORE GIẢ — có GIAO DỊCH THẬT: đọc ghi lại phiên bản tài liệu, lúc cam kết
 * mà một tài liệu đã đọc bị người khác đổi thì CHẠY LẠI cả việc (đúng cách Firestore
 * làm). Nhờ vậy cổng thử được chuyện hai chuyên gia bấm cùng lúc, không chỉ đọc mã.
 */
function khoFirestoreGia(dau = {}, { kieuLuat = false, tuChoi = false } = {}) {
  const tl = new Map(Object.entries(dau).map(([k, v]) => [k, { du: v, ban: 1 }]));
  let id = 0;
  const thong = { chayLai: 0, camKet: 0 };
  const cho = () => new Promise((r) => { setTimeout(r, 3); });
  const nen = {
    nguoi: 'cg1',
    tl, thong,
    docBang: async () => [...tl].filter(([k]) => /^nguong\/[^/]+$/.test(k)).map(([, v]) => v.du),
    moiLichSu: () => `nguong_lich_su/ls${++id}`,
    dauGio: () => 'TS',
    giaoDich: async (viec) => {
      for (let lan = 0; lan < 10; lan += 1) {
        const doc = new Map();
        const ghi = [];
        const kq = await viec({
          get: async (d) => { await cho(); const x = tl.get(d); doc.set(d, x?.ban ?? 0); return { exists: !!x, data: () => x?.du }; },
          set: (d, du) => { ghi.push([d, du]); },
        });
        if (tuChoi) { const e = new Error('Missing or insufficient permissions.'); e.code = 'permission-denied'; throw e; }
        if ([...doc].some(([d, ban]) => (tl.get(d)?.ban ?? 0) !== ban)) {
          thong.chayLai += 1;
          /* `kieuLuat`: đúng cách bộ giả lập thật cư xử — LUẬT xét trước phép so phiên
             bản tài liệu, nên giao dịch đến sau nhận `permission-denied` chứ SDK không
             tự chạy lại. */
          if (kieuLuat) { const e = new Error('PERMISSION_DENIED'); e.code = 'permission-denied'; throw e; }
          continue;
        }
        for (const [d, du] of ghi) tl.set(d, { du, ban: (tl.get(d)?.ban ?? 0) + 1 });
        thong.camKet += 1;
        return kq;
      }
      throw new Error('giao dịch chạy lại quá nhiều lần');
    },
  };
  return nen;
}
const lichSu = (nen) => [...nen.tl].filter(([k]) => k.startsWith('nguong_lich_su/')).map(([, v]) => v.du);

test('2 · phát hành cho MỘT khối lớp: ghi `phamVi`, và máy chủ đọc ra đúng phạm vi ấy', async () => {
  const nen = khoFirestoreGia();
  const pv = { loai: 'khoiLop', khoa: '3' };
  const giaTri = { ...con.MAC_DINH, NG07: 0.80 };
  const pb = await phatHanhNguong({ giaTri, doi: ['NG07'], lyDo: 'lớp 3 đạt sớm hơn', phamVi: pv }, nen);
  const dong = nen.tl.get(`nguong/${maTaiLieu('NG07', pv)}`)?.du;
  assert.ok(dong, 'phải ghi tài liệu NG07__khoiLop__3');
  assert.equal(maTaiLieu('NG07', pv), 'NG07__khoiLop__3');
  assert.deepEqual(dong.phamVi, { loai: 'khoiLop', khoa: '3' });
  assert.equal(dong.phienBan, pb);
  assert.equal(nen.tl.has('nguong/NG07'), false, 'phạm vi hẹp KHÔNG được đè giá trị toàn hệ');

  quenMayChu();
  try {
    const giaDb = { collection: () => ({ get: async () => {
      const ds = await nen.docBang();
      return { forEach: (f) => ds.forEach((x) => f({ data: () => x })) };
    } }) };
    const bm = await layBoNguong(giaDb);
    assert.equal(may.layNguong(bm, 'NG07', { khoiLop: '3' }), 0.80);
    assert.equal(may.layNguong(bm, 'NG07', { khoiLop: '4' }), 0.85);
  } finally { quenMayChu(); may.datBoNguong(may.BO_MAC_DINH); }
});

test('2 · phép soi chạy trên BỘ HIỆU LỰC của phạm vi, kể cả chỗ nó giao với phạm vi khác', async () => {
  /* Môn Tiếng Anh đã khai θ_yếu = 0,60. Đặt θ = 0,75 cho khối lớp 3: riêng khối lớp 3
     thì sạch (θ_yếu toàn hệ 0,30), nhưng bé lớp 3 học Tiếng Anh nhận θ_yếu 0,60 >
     0,75 − 0,20. Đó đúng là chỗ một đứa trẻ thật đứng. */
  const nen = khoFirestoreGia({
    'nguong/NG08__mon__tienganh': { ma: 'NG08', giaTri: 0.60, phienBan: 3, phamVi: { loai: 'mon', khoa: 'tienganh' } },
  });
  const pv = { loai: 'khoiLop', khoa: '3' };
  const ungVien = con.apDungThayDoi((await docBangNguong(nen)).bo, pv, { NG07: 0.75 }, ['NG07']);
  assert.deepEqual(con.soiNguong(ungVien, { khoiLop: '3' }), [], 'riêng khối lớp 3 thì sạch');
  const loi = con.soiPhamVi(ungVien, pv);
  assert.ok(loi.some((x) => x.ma === 'NG08' && x.nguCanh?.mon === 'tienganh'),
    'phải bắt được chỗ giao khối lớp 3 × Tiếng Anh');
  await assert.rejects(
    phatHanhNguong({ giaTri: { ...con.MAC_DINH, NG07: 0.75 }, doi: ['NG07'], lyDo: 'x', phamVi: pv }, nen),
    /NG08/);
  assert.equal(lichSu(nen).length, 0, 'bị bác thì không ghi gì');

  /* Và nhịp tinh thông cũng tính trên bộ hiệu lực: θ 0,70 cho khối lớp 1 GHÉP với
     P(T) 0,40 đã khai cho lớp 1 ra nhịp 2 câu — dù toàn hệ vẫn 4 câu. */
  const b2 = con.apDungThayDoi(bo({}, { khoiLop: { 1: { NG02: 0.40 } } }), { loai: 'khoiLop', khoa: '1' }, { NG07: 0.70 }, ['NG07']);
  assert.equal(con.nhipTinhThong(b2).soCau, 4);
  assert.ok(con.soiPhamVi(b2, { loai: 'khoiLop', khoa: '1' }).some((x) => /nhịp tinh thông/.test(x.vi)));
});

test('2 · màn chuyên gia có ô chọn phạm vi và truyền phạm vi xuống hàm phát hành', () => {
  const s = doc('../src/chung/components/BangNguong.jsx');
  assert.match(s, /PHAM_VI_CHON\.map/);
  assert.match(s, /soiPhamVi\(ungVien, phamVi\)/, 'phải soi bộ hiệu lực của phạm vi');
  assert.match(s, /nhipTinhThong\(ungVien, nguCanhCuaPhamVi\(phamVi\)\)/);
  assert.match(s, /phatHanhNguong\(\{ giaTri: gt, doi, lyDo, phamVi \}\)/);
});

/* ════════════════════ 3 · PHIÊN BẢN VÀ GIÁ TRỊ CŨ LẤY TỪ BẢNG ════════════════════ */

test('3 · số mới = max(phiên bản trong bảng) + 1 — không phải bộ đã nạp + 1', async () => {
  /* Bộ của phiên vẫn là mặc định (phiên bản 1). Bảng thì đã tới 7. */
  const nen = khoFirestoreGia({
    'nguong/NG07': { ma: 'NG07', giaTri: 0.9, phienBan: 7, phamVi: { loai: 'toanHe' } },
  });
  const pb = await phatHanhNguong({ giaTri: { ...con.MAC_DINH, NG07: 0.88 }, doi: ['NG07'], lyDo: 'x' }, nen);
  assert.equal(pb, 8);
  assert.equal(nen.tl.get(DEM_PHIEN_BAN).du.so, 8, 'bộ đếm phải đi cùng');
  const [ls] = lichSu(nen);
  assert.equal(ls.phienBan, 8);
  assert.equal(ls.giaTriCu, 0.9, 'giá trị cũ phải là con số ĐANG Ở BẢNG, không phải 0,85 của bộ đã nạp');
  assert.equal(ls.nguonCu, 'bang');
  /* Bộ đếm đi trước bảng (một lần phát hành chỉ đổi phạm vi khác) thì theo bộ đếm. */
  nen.tl.set(DEM_PHIEN_BAN, { du: { so: 12 }, ban: 5 });
  assert.equal(await phatHanhNguong({ giaTri: { ...con.MAC_DINH, NG09: 4 }, doi: ['NG09'], lyDo: 'y' }, nen), 13);
});

test('3 · phạm vi hẹp chưa từng khai: giá trị cũ là giá trị THỪA HƯỞNG từ bảng', async () => {
  const nen = khoFirestoreGia({
    'nguong/NG07': { ma: 'NG07', giaTri: 0.9, phienBan: 2, phamVi: { loai: 'toanHe' } },
  });
  await phatHanhNguong({ giaTri: { ...con.MAC_DINH, NG07: 0.8 }, doi: ['NG07'], lyDo: 'x', phamVi: { loai: 'mon', khoa: 'toan' } }, nen);
  const [ls] = lichSu(nen);
  assert.equal(ls.giaTriCu, 0.9);
  assert.equal(ls.nguonCu, 'thuaHuong');
  assert.deepEqual(ls.phamVi, { loai: 'mon', khoa: 'toan' });
});

test('3 · hai chuyên gia bấm CÙNG LÚC: hai số khác nhau, không bao giờ trùng', async () => {
  const nen = khoFirestoreGia({
    'nguong/NG07': { ma: 'NG07', giaTri: 0.85, phienBan: 4, phamVi: { loai: 'toanHe' } },
  });
  const [a, b] = await Promise.all([
    phatHanhNguong({ giaTri: { ...con.MAC_DINH, NG09: 4 }, doi: ['NG09'], lyDo: 'a' }, nen),
    phatHanhNguong({ giaTri: { ...con.MAC_DINH, NG14: 3 }, doi: ['NG14'], lyDo: 'b' }, nen),
  ]);
  assert.notEqual(a, b, `trùng số phiên bản ${a}`);
  assert.deepEqual([a, b].sort(), [5, 6]);
  assert.ok(nen.thong.chayLai >= 1, 'phép thử phải thật sự gây xung đột — không thì nó không thử gì');
  assert.deepEqual(lichSu(nen).map((x) => x.phienBan).sort(), [5, 6]);
});

test('3 · xung đột bị LUẬT chặn (permission-denied) thì tự chạy lại; từ chối thật thì ném', async () => {
  const nen = khoFirestoreGia({}, { kieuLuat: true });
  const [a, b] = await Promise.all([
    phatHanhNguong({ giaTri: { ...con.MAC_DINH, NG09: 4 }, doi: ['NG09'], lyDo: 'a' }, nen),
    phatHanhNguong({ giaTri: { ...con.MAC_DINH, NG14: 3 }, doi: ['NG14'], lyDo: 'b' }, nen),
  ]);
  assert.deepEqual([a, b].sort(), [2, 3]);
  assert.ok(nen.thong.chayLai >= 1);

  const cam = khoFirestoreGia({}, { tuChoi: true });
  let lan = 0;
  const goc = cam.giaoDich;
  cam.giaoDich = (v) => { lan += 1; return goc(v); };
  await assert.rejects(phatHanhNguong({ giaTri: { ...con.MAC_DINH, NG09: 4 }, doi: ['NG09'], lyDo: 'a' }, cam),
    (e) => e.code === 'permission-denied');
  assert.ok(lan <= 2, `từ chối thật mà chạy lại ${lan} lần`);
});

test('3 · bộ của PHIÊN không đổi sau khi phát hành (mục 3.8.4)', async () => {
  const truoc = con.boNguong();
  await phatHanhNguong({ giaTri: { ...con.MAC_DINH, NG09: 4 }, doi: ['NG09'], lyDo: 'a' }, khoFirestoreGia());
  assert.equal(con.boNguong(), truoc);
});

test('3 · màn và hàm phát hành đọc TƯƠI, giao dịch đọc bộ đếm; luật canh bộ đếm', () => {
  const s = doc('../src/chung/components/BangNguong.jsx');
  assert.match(s, /docBangNguong\(\)/, 'mở màn phải đọc tươi bảng');
  assert.match(s, /phiên bản \{boBang \? boBang\.phienBan/, 'số phiên bản trên màn phải lấy từ bảng');
  assert.doesNotMatch(s, /dangHanh\.phienBan/);
  const g = doc('../src/chung/lib/ghiNguong.js');
  assert.match(g, /runTransaction/);
  assert.doesNotMatch(g, /boNguong\(\)/, 'hàm phát hành không được dựa vào bộ đã nạp');
  const r = doc('../firestore.rules');
  assert.match(r, /match \/nguong_phien_ban\//);
  assert.match(r, /request\.resource\.data\.so == resource\.data\.so \+ 1/);
  assert.match(r, /phienBanVuaTang\(\)/);
});

/* ════════════════════ 4 · ĐỌC LÚC DÙNG, KÈM NGỮ CẢNH ════════════════════ */

test('4 · NG09 (phụ đạo) đọc lúc dùng, và theo khối lớp của phiên', async () => {
  const ho = { p: 0.5, saiLienTiep: 3 };
  assert.equal(viecTiepCuaNut(ho).viec, VIEC.phuDao, 'mặc định 3 lần sai là phụ đạo');
  await voiBo(bo({ NG09: 5 }), () => assert.equal(viecTiepCuaNut(ho).viec, VIEC.tiep));
  await voiBo(bo({}, { khoiLop: { 3: { NG09: 5 } } }),
    () => assert.equal(viecTiepCuaNut(ho).viec, VIEC.tiep, 'khối lớp 3 khai riêng NG09'), { khoiLop: 3 });
  await voiBo(bo({}, { nut: { n1: { NG09: 5 } } }), () => {
    const r = viecTiepCuaBai({ n1: ho, n2: { p: 0.5, saiLienTiep: 0 } }, ['n1', 'n2']);
    assert.equal(r.viec, VIEC.tiep, 'nấc nút phải tới được hàm chính sách của bài');
  });
});

test('4 · NG13, NG14, NG15, NG18, NG07 — đọc lúc dùng', async () => {
  const bayGio = 10 * 86400000;
  const s = (b) => vectorS({ mucThao: { a: { p: 0.5, lastSeen: bayGio - 5 * 86400000 } }, maNutDs: ['a'], bayGio, ...b });
  assert.equal(s().hayQuen, false);
  await voiBo(bo({ NG13: 3 }), () => assert.equal(s().hayQuen, true));

  assert.equal(daThuDu({ attempts: 2 }), true);
  await voiBo(bo({ NG14: 3 }), () => {
    assert.equal(daThuDu({ attempts: 2 }), false);
    assert.equal(duocBoQua(3), false);
  });

  const vung = { a: { p: 0.95 }, b: { p: 0.95 } };
  assert.equal(duocVuotAi(vung, ['a', 'b'], true), false, 'mặc định cần 3 nút');
  await voiBo(bo({ NG15: 2 }), () => assert.equal(duocVuotAi(vung, ['a', 'b'], true), true));

  const hs = { go: { dung: 4, tong: 5 } };
  assert.equal(tiLeDung(hs, 'go'), null);
  await voiBo(bo({}, { dangCau: { go: { NG18: 5 } } }), () => assert.equal(tiLeDung(hs, 'go'), 0.8));

  assert.equal(nhomCua(0.8), NHOM.chongChenh);
  await voiBo(bo({}, { nut: { n1: { NG07: 0.75 } } }), () => {
    assert.equal(nhomCua(0.8, { nut: 'n1' }), NHOM.daThao);
    assert.equal(nhomCua(0.8, { nut: 'n2' }), NHOM.chongChenh);
  });

  const toan = { progress: { micros: { m1: { pass: true } } }, mastery: { u1: { p: 0.8 } },
                 index: { m1: { bktUnit: 'u1' } }, list: ['m1'] };
  assert.equal(pickMicro(toan)?.reason, 'đã quên bớt');
  await voiBo(bo({ NG07: 0.75 }), () => assert.equal(pickMicro(toan), null));
});

const DT = {
  nut: { a: { t: 'vocabulary' }, b: { t: 'grammar' }, c: { t: 'grammar' }, d: { t: 'grammar' } },
  canh: [
    { can: 'a', truoc_khi: 'b' }, { can: 'b', truoc_khi: 'c' }, { can: 'c', truoc_khi: 'd' },
  ],
};

test('4 · NG10/NG11/NG12 của chẩn đoán gốc rễ đọc lúc dùng', async () => {
  const mt = { a: { p: 0.2 }, b: { p: 0.2 }, c: { p: 0.2 } };
  assert.equal(nutGocRe(DT, mt, 'd').length, 3);
  await voiBo(bo({ NG11: 1 }), () => assert.equal(nutGocRe(DT, mt, 'd').length, 1));
  await voiBo(bo({ NG10: 1 }), () => assert.deepEqual(nutGocRe(DT, mt, 'd').map((x) => x.ma), ['c']));
  const doNgo = nutGocRe(DT, mt, 'd')[0].doNgo;
  await voiBo(bo({ NG12: 0.9 }), () => assert.ok(nutGocRe(DT, mt, 'd')[0].doNgo > doNgo));
});

test('4 · máy chủ: sổ bố mẹ và ΔC dùng BỘ TRUYỀN VÀO, không dùng BO_MAC_DINH', () => {
  const luot = (ms, extra = {}) => ({ v: 7, sessionId: 's', microId: 'm', itemId: 'i', ts: 1, serverTs: 1, ms, correct: false, ...extra });
  assert.equal(stuckItems([luot(40000)]).length, 0, 'mặc định H3 = 45 giây');
  const b30 = { ...may.BO_MAC_DINH, macDinh: { ...may.MAC_DINH, NG16: 30 } };
  assert.equal(stuckItems([luot(40000)], null, 3, b30).length, 1);
  const bTheoDang = { ...may.BO_MAC_DINH, theoPhamVi: { dangCau: { go: { NG16: 30 } } } };
  assert.equal(stuckItems([luot(40000, { mode: 'go' })], null, 3, bTheoDang).length, 1, 'NG16 theo dạng câu của lượt');
  assert.equal(stuckItems([luot(40000, { mode: 'chon' })], null, 3, bTheoDang).length, 0);

  const now = 1000 * 86400000;
  const rep = (b) => buildParentReport({ learnerId: 'b', attempts: [], mastery: { u: { p: 0.8, unit: 'u' } }, now, bo: b });
  assert.equal(rep(may.BO_MAC_DINH).unitsMastered, 0);
  assert.equal(rep({ ...may.BO_MAC_DINH, macDinh: { ...may.MAC_DINH, NG07: 0.75 } }).unitsMastered, 1);

  const phien = [];
  for (let i = 0; i < 8; i += 1) phien.push({ sessionId: 'p', mode: 'chon', ms: i < 4 ? 1000 : 1200, ts: i });
  assert.equal(metMoi(phien).metMoi, false, 'chậm 20% < ngưỡng 25%');
  assert.equal(metMoi(phien, { bo: { ...may.BO_MAC_DINH, macDinh: { ...may.MAC_DINH, NG17: { ti: 0.15, toiThieuMoiNua: 3 } } } }).metMoi, true);

  const cap = (i) => ({ mauPrompt: 'm', phienBanMau: 1, truoc: { p: 0.2, itemIds: [`a${i}`] }, sau: { p: 0.5, itemIds: [`b${i}`] } });
  assert.equal(gomTheoMau([cap(1), cap(2)])[0].duMau, false, 'mặc định cần 5 cặp');
  assert.equal(gomTheoMau([cap(1), cap(2)], { bo: { ...may.BO_MAC_DINH, macDinh: { ...may.MAC_DINH, NG19: 2 } } })[0].duMau, true);

  for (const p of ['../functions/src/report.js', '../functions/src/ara.js']) {
    assert.doesNotMatch(doc(p), /BO_MAC_DINH/, `${p}: còn đọc bộ mặc định`);
  }
  const idx = doc('../functions/index.js');
  const than = idx.slice(idx.indexOf('async function dungSoHoc'), idx.indexOf('export const nightlyReport'));
  assert.match(than, /await layBoNguong\(db\)/, 'sổ học phải nạp bộ đã phát hành');
  assert.match(than, /buildParentReport\(\{[^}]*\bbo\b/, 'và truyền bộ ấy vào');
});

test('4 · máy con: hằng viết hoa không còn ra quyết định ở đâu cả', () => {
  /* Mỗi hằng chỉ được xuất hiện ĐÚNG MỘT LẦN trong mã (chỗ khai) ở tệp của nó — mọi
     quyết định phải gọi hàm đọc lúc dùng. Bỏ chú thích trước khi đếm. */
  const boChu = (s) => s.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
  const CANH = {
    '../src/mon/tienganh/lib/chinhsach.js': ['SAI_LIEN_TIEP_MAC', 'NUT_TOI_THIEU_VUOT_AI', 'NGAY_COI_LA_QUEN'],
    '../src/mon/tienganh/lib/lantruyen.js': ['ALPHA', 'BETA', 'SAU_TOI_DA', 'NUT_GOC_TOI_DA', 'P_MAC_DINH', 'NGUONG_TRAN'],
    '../src/mon/tienganh/lib/dandat.js': ['THU_TOI_THIEU'],
    '../src/mon/tienganh/lib/hoso.js': ['TOI_THIEU_MAU'],
    '../src/mon/tienganh/lib/zpd.js': ['NGUONG_THAO', 'NGUONG_YEU'],
    '../src/mon/tienganh/lib/cefr.js': ['PHU_DAT', 'TOI_THIEU_NUT'],
    '../src/mon/tienganh/lib/phudao.js': ['SO_CAU_PHU_DAO'],
    '../src/mon/toan/lib/adaptive.js': ['MASTERY_THRESHOLD'],
  };
  for (const [p, ds] of Object.entries(CANH)) {
    const s = boChu(doc(p));
    for (const h of ds) {
      const n = (s.match(new RegExp(`\\b${h}\\b`, 'g')) || []).length;
      assert.equal(n, 1, `${p}: ${h} còn được dùng ${n - 1} chỗ ngoài chỗ khai`);
    }
  }
  /* Và các màn dùng chúng cũng đã chuyển sang hàm. */
  assert.doesNotMatch(doc('../src/mon/tienganh/components/CauHoi.jsx'), /HIEN_GOI_Y/);
  assert.doesNotMatch(doc('../src/mon/tienganh/components/PhuDao.jsx'), /SO_CAU_PHU_DAO/);
});

/* ════════════════════ 5 · NG22–NG30: HẰNG SỐ GÕ CỨNG ĐƯA RA BẢNG ════════════════════ */

const CU = { NG22: 0.08, NG23: 0.05, NG24: 2, NG25: 0.5, NG26: 0.1, NG27: 4,
             NG28: { m1: 1, m2: 3, m3: 7 }, NG29: 0.6, NG30: 30 };

test('5 · mặc định của NG22–NG30 ĐÚNG BẰNG con số đã gõ cứng — không đổi hành vi', () => {
  for (const [ma, v] of Object.entries(CU)) {
    assert.deepEqual(con.MAC_DINH[ma], v, `${ma} lệch con số cũ`);
    assert.ok(con.KHOANG[ma], `${ma} thiếu khoảng hợp lệ`);
    assert.ok(TEN_NGUONG[ma], `${ma} thiếu tên đọc được`);
  }
  assert.deepEqual(con.soiNguong(con.BO_MAC_DINH), [], 'bộ mặc định phải sạch với cả ngưỡng mới');
  /* Mọi ngưỡng đều nằm trong MỘT nhóm của màn chuyên gia. */
  const s = doc('../src/chung/components/BangNguong.jsx');
  const nhom = s.slice(s.indexOf('export const NHOM'), s.indexOf('];', s.indexOf('export const NHOM')));
  for (const ma of Object.keys(con.KHOANG)) assert.match(nhom, new RegExp(`'${ma}'`), `${ma} không có trên màn`);
  assert.match(doc('../../tools/xuat_nguong.py'), /"NG28": \["m1", "m2", "m3"\]/, 'lệnh xuất phải soi được NG28');
});

test('5 · ràng buộc mới: lịch ôn tăng dần, điểm tựa hàm quên ≤ θ − 0,20', () => {
  assert.ok(con.soiNguong(bo({ NG28: { m1: 3, m2: 3, m3: 7 } })).some((x) => x.ma === 'NG28'));
  assert.ok(con.soiNguong(bo({ NG28: { m1: 1, m2: 3, m3: 99 } })).some((x) => x.ma === 'NG28'), 'ngoài khoảng');
  assert.ok(con.soiNguong(bo({ NG25: 0.6, NG07: 0.75 })).some((x) => x.ma === 'NG25'));
  assert.deepEqual(con.soiNguong(bo({ NG07: 0.70 })).filter((x) => x.ma === 'NG25'), [],
    'θ = 0,70 hợp lệ thì điểm tựa 0,5 cũng phải hợp lệ (bẫy số thực 0,70 − 0,20)');
});

test('5 · NG22/NG23/NG24/NG26 điều khiển lan truyền', async () => {
  const mt = { a: { p: 0.95 }, b: { p: 0.30 }, c: { p: 0.20 }, d: { p: 0.20 } };
  const goc = congHuong(DT, mt);
  assert.equal(goc.d, undefined, 'mặc định độ sâu xuôi 2: d (3 bước) không nhích');
  await voiBo(bo({ NG24: 3 }), () => assert.ok(congHuong(DT, mt).d > 0.20));
  await voiBo(bo({ NG22: 0.16 }), () => assert.ok(congHuong(DT, mt).b > goc.b));
  await voiBo(bo({ NG23: 0.30 }), () => {
    assert.ok(Math.abs(nguongTran() - 0.55) < 1e-9);
    assert.ok(congHuong(DT, { a: { p: 0.99 }, b: { p: 0.54 } }).b <= 0.55 + 1e-9);
  });
  const pTruoc = nutGocRe(DT, { a: { p: 0.2 } }, 'c').find((x) => x.ma === 'b').p;
  assert.equal(pTruoc, 0.1);
  await voiBo(bo({ NG26: 0.3 }), () => assert.equal(nutGocRe(DT, { a: { p: 0.2 } }, 'c').find((x) => x.ma === 'b').p, 0.3));
});

test('5 · NG25 điều khiển hàm quên ở máy chủ', () => {
  assert.ok(Math.abs(quenDan(0.9, 14) - 0.7) < 1e-9, 'mặc định: kéo về 0,5 — nửa đời 14 ngày');
  may.datBoNguong({ macDinh: { ...may.MAC_DINH, NG25: 0.3 } });
  try { assert.ok(Math.abs(quenDan(0.9, 14) - 0.6) < 1e-9); } finally { may.datBoNguong(may.BO_MAC_DINH); }
});

test('5 · NG27: độ dài bài phụ đạo ở máy con, và trần gói ở máy chủ, cùng một mã', async () => {
  const bai = { practice: { pools: { warmup: Array.from({ length: 8 }, (_, i) => ({ id: `c${i}`, maNut: 'n' })) } } };
  assert.equal(cauTinhCuaNut([bai], 'n').length, 4);
  await voiBo(bo({ NG27: 6 }), () => assert.equal(cauTinhCuaNut([bai], 'n').length, 6));
  const goi = { nhan: 'x', soCau: 5, vonTu: [{ tu: 'cat' }], lop: 3 };
  assert.throws(() => soiGoiPhuDao(goi), /từ 1 tới 4/);
  assert.equal(soiGoiPhuDao(goi, { ...may.BO_MAC_DINH, macDinh: { ...may.MAC_DINH, NG27: 6 } }).soCau, 5);
  assert.equal(soiGoiPhuDao(goi, { ...may.BO_MAC_DINH, theoPhamVi: { khoiLop: { 3: { NG27: 5 } } } }).soCau, 5,
    'máy chủ tra theo khối lớp của gói, cùng phạm vi máy con xin');
  const idx = doc('../functions/index.js');
  assert.match(idx, /sinhPhuDao\(du, taoClient, await layBoNguong\(db\)\)/);
});

test('5 · NG28: lịch ôn mặc định của hàm nền', () => {
  assert.deepEqual(lichOnMacDinh(), ['+1 ngày: flashcard', '+3 ngày: câu luyện', '+7 ngày: câu thử thách'],
    'mặc định phải ra ĐÚNG ba chuỗi đã gõ cứng trước 22-11');
  const b = { ...may.BO_MAC_DINH, macDinh: { ...may.MAC_DINH, NG28: { m1: 2, m2: 5, m3: 10 } } };
  const the = buildReviewCards({ learnerId: 'b', microId: 'm', lesson: { spacedReview: { schedule: lichOnMacDinh(b) } }, at: 0 });
  assert.deepEqual(the.map((x) => x.dueAt / 86400000), [2, 5, 10]);
  const idx = doc('../functions/index.js');
  assert.doesNotMatch(idx, /'\+1 ngày: flashcard'/, 'lịch còn gõ cứng ở hàm nền');
  assert.match(idx, /lichOnMacDinh\(await layBoNguong\(db\)/);
});

test('5 · NG29/NG30: quy đổi CEFR', async () => {
  const nut = {};
  const mt = {};
  for (let i = 0; i < 20; i += 1) { nut[`a${i}`] = { t: 'vocabulary', g: 3 }; if (i < 13) mt[`a${i}`] = { p: 0.95 }; }
  assert.equal(bacCefr({ nut }, mt).mucDat, null, '20 nút < 30 — khối chưa đáng tin');
  await voiBo(bo({ NG30: 20 }), () => assert.equal(bacCefr({ nut }, mt).mucDat?.ma, 'A1'));
  await voiBo(bo({ NG30: 20, NG29: 0.7 }), () => assert.equal(bacCefr({ nut }, mt).mucDat, null, '13/20 = 65% < 70%'));
});

test('5 · hằng số cũ không còn gõ cứng ở chỗ cũ', () => {
  assert.doesNotMatch(doc('../src/mon/tienganh/lib/lantruyen.js'), /= 0\.08;|- 0\.05;|sauToiDa = 2|P_MAC_DINH = 0\.1/);
  assert.doesNotMatch(doc('../functions/src/bkt.js'), /0\.5 \+ \(p - 0\.5\)/);
  assert.doesNotMatch(doc('../functions/src/hocNguong.js'), /0\.5 \+ \(m\.p - 0\.5\)/);
  assert.doesNotMatch(doc('../src/mon/tienganh/lib/cefr.js'), /TOI_THIEU_NUT = 30|PHU_DAT = 0\.6/);
  assert.doesNotMatch(doc('../src/mon/tienganh/lib/phudao.js'), /SO_CAU_PHU_DAO = 4/);
  assert.doesNotMatch(doc('../functions/src/phudao.js'), /SO_CAU_TOI_DA = 4/);
});

test('5 · dungPhuDao vẫn ra đúng 4 câu với bộ mặc định', async () => {
  const bai = { id: 'b1', practice: { pools: { warmup: Array.from({ length: 6 }, (_, i) => ({ id: `c${i}`, maNut: 'a', format: 'chon' })) } } };
  const r = await dungPhuDao({ dt: { nut: { a: { t: 'vocabulary' } }, canh: [] }, mucThao: {}, maNutMac: 'a', baiDs: [bai] });
  assert.ok(r.cau.length <= 4);
});
