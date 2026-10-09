/**
 * CỔNG · ĐIỂM MÁY CHẤM LÀ ĐIỂM TẠM CHO TỚI KHI NGƯỜI LỚN XEM (việc V5, HITL).
 *
 * ── VIỆC NÀY LÀM GÌ ──
 * Điểm bài viết do mô hình chấm. Màn hình đã nói "máy chấm (AI), không phải điểm của
 * cô giáo" từ lâu — nhưng đó chỉ là một dòng chữ; con số thì vẫn nằm trong sổ học bạ
 * y như mọi điểm khác, và sổ học bạ là thứ bố mẹ đọc để biết con đang ở đâu.
 *
 * ── CÁI DỄ HỎNG ──
 * Ba chỗ con số ấy lộ ra (thẻ bài · màn lời chấm · Góc bố mẹ) từng mỗi chỗ tự viết
 * một dòng chữ khác nhau. Nên tệp này canh: MỌI chỗ hiện điểm viết phải đi qua
 * `diemHienThi`, và nhãn chỉ có ĐÚNG BA giá trị.
 *
 * Và canh hai điều không được phá: không có nút nào cho BÉ tự xác nhận điểm của
 * mình; BKT vẫn đọc `diem` chứ không chờ bố mẹ (quyết định, không phải sơ sót).
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  TRANG_THAI_DIEM, xacNhanDiem, diemHienThi, baiChoXacNhan,
} from '../src/mon/tienganh/lib/hocba.js';
import { soRong, ghiBaiViet, khoaBaiViet } from '../src/mon/tienganh/lib/progress.js';

/* ═══════════ ĐIỂM MÁY CHẤM Ở TRẠNG THÁI "TẠM" (việc V5) ═══════════ */

test('xacNhanDiem: đồng ý · sửa · và KHÔNG sửa tại chỗ', () => {
  const muc = { viet: 'My school is big.', diem: 8, khen: 'ok', nguon: 'ai' };

  /* Đồng ý với điểm máy — `diemNguoi` để `null`. */
  const dongY = xacNhanDiem(muc, { luc: 0 });
  assert.equal(dongY.trangThai, TRANG_THAI_DIEM.xacNhan);
  assert.equal(dongY.diemNguoi, null);
  assert.equal(diemHienThi(dongY).diem, 8);
  assert.match(diemHienThi(dongY).nhan, /bố mẹ đã xác nhận/);

  /* Sửa điểm. */
  const sua = xacNhanDiem(muc, { diemNguoi: 7, luc: 0 });
  assert.equal(diemHienThi(sua).diem, 7);
  assert.match(diemHienThi(sua).nhan, /bố mẹ sửa/);
  /* ⚠ ĐIỂM MÁY CHẤM VẪN CÒN. Đè lên thì mất bằng chứng máy chấm bao nhiêu, và câu
     "máy chấm có hay sai không" hết đường trả lời. */
  assert.equal(sua.diem, 8);
  assert.equal(diemHienThi(sua).diemMay, 8);

  /* ⚠ KHÔNG SỬA TẠI CHỖ — mục này nằm trong sổ, mà sổ đi vào `useMemo` của React.
     Sửa tại chỗ thì màn hình không thấy nó đổi, và bố mẹ bấm nút mà không thấy gì. */
  assert.equal(muc.trangThai, undefined);
  assert.equal(muc.diemNguoi, undefined);
});

/**
 * ⚠ `Number(null)` LÀ 0, VÀ `Number.isFinite(0)` LÀ TRUE.
 * Bản đầu của `diemHienThi` viết `Number.isFinite(Number(muc.diemNguoi))`, nên
 * `diemNguoi: null` (nghĩa là "bố mẹ ĐỒNG Ý") hoá thành số 0 — nhãn ra "bố mẹ sửa:
 * 0", tức bấm Đồng ý là điểm bé tụt về 0. Phép thử khói bắt được, nhưng nó là loại
 * lỗi đi qua mọi phép kiểm kiểu `typeof` hay `!= undefined`.
 */
test('bấm ĐỒNG Ý không được làm điểm tụt về 0', () => {
  const x = diemHienThi(xacNhanDiem({ diem: 8 }, { diemNguoi: null, luc: 0 }));
  assert.equal(x.diem, 8);
  assert.ok(!/sửa/.test(x.nhan), `nhãn sai: ${x.nhan}`);
  /* Nhưng sửa THÀNH 0 thì vẫn phải là 0 — bé viết sai hết thì điểm 0 là điểm thật. */
  const khong = diemHienThi(xacNhanDiem({ diem: 8 }, { diemNguoi: 0, luc: 0 }));
  assert.equal(khong.diem, 0);
  assert.match(khong.nhan, /bố mẹ sửa: 0/);
});

test('sửa THÀNH ĐÚNG điểm máy thì vẫn là "đã xác nhận", không phải "đã sửa"', () => {
  const x = diemHienThi(xacNhanDiem({ diem: 8 }, { diemNguoi: 8, luc: 0 }));
  assert.match(x.nhan, /đã xác nhận/);
});

test('diemHienThi LUÔN có nhãn nguồn — ba nhãn, không có nhãn thứ tư', () => {
  /* Con số không nhãn sẽ được đọc thành điểm của cô giáo, và đó là hiểu nhầm bố mẹ
     KHÔNG có cách nào tự phát hiện. */
  const ca = [
    { diem: 8 },
    { diem: 8, trangThai: 'tam' },
    xacNhanDiem({ diem: 8 }, { luc: 0 }),
    xacNhanDiem({ diem: 8 }, { diemNguoi: 6, luc: 0 }),
  ];
  const BA = ['máy chấm – chờ bố mẹ', 'bố mẹ đã xác nhận', /^bố mẹ sửa: \d+$/];
  for (const m of ca) {
    const { nhan } = diemHienThi(m);
    assert.ok(nhan, `mục này ra điểm KHÔNG nhãn: ${JSON.stringify(m)}`);
    assert.ok(BA.some((x) => (x instanceof RegExp ? x.test(nhan) : x === nhan)),
      `nhãn lạ: ${JSON.stringify(nhan)}`);
  }
  /* Mục cũ trong sổ không có `trangThai` → coi là `tam`. Sổ sống lâu hơn mã, và
     hỏng về phía "chờ bố mẹ" chỉ hơi sai, còn hỏng về phía "đã xác nhận" thì sai
     hẳn về phía nguy hiểm. */
  assert.equal(diemHienThi({ diem: 8 }).choXacNhan, true);
  /* Và nhãn ĐẦY ĐỦ (thứ màn hình dùng) phải LUÔN nói điểm do máy chấm — xem ghi
     chú ở `diemHienThi`. "bố mẹ đã xác nhận" một mình thì vẫn đọc được thành điểm
     của cô giáo. */
  for (const m of ca) {
    assert.match(diemHienThi(m).nhanDay, /Máy chấm \(AI\)/,
      `nhãn đầy đủ không nói nguồn: ${JSON.stringify(diemHienThi(m).nhanDay)}`);
  }
  /* Không có mục thì không có nhãn, và không được vỡ. */
  assert.deepEqual(diemHienThi(null),
    { diem: null, nhan: '', nhanDay: '', choXacNhan: false });
});

test('baiChoXacNhan chỉ nhặt bài CÓ ĐIỂM và CHƯA ai xem', () => {
  const tienDo = { baiViet: {
    cho: { diem: 8 },
    roi: xacNhanDiem({ diem: 7 }, { luc: 0 }),
    chuaCham: { viet: 'x', diem: null },
  } };
  assert.deepEqual(baiChoXacNhan(tienDo).map((x) => x.khoa), ['cho']);
  assert.deepEqual(baiChoXacNhan({}), []);
  assert.deepEqual(baiChoXacNhan(null), []);
});

test('ghiBaiViet đặt trangThai TẠM, và bé viết lại thì về TẠM', () => {
  let p = ghiBaiViet(soRong(), 'ta3', 1, { viet: 'a', cham: { diem: 8, loi: [] } }, 'unit');
  const k = khoaBaiViet('ta3', 1, 'unit');
  assert.equal(p.baiViet[k].trangThai, TRANG_THAI_DIEM.tam);
  assert.equal(p.baiViet[k].diemNguoi, null);

  /* Bố mẹ xác nhận, rồi bé viết LẠI → phải về `tam`: lời chấm mới thì lần xác nhận
     cũ không còn nói về bài này. */
  p = { ...p, baiViet: { ...p.baiViet, [k]: xacNhanDiem(p.baiViet[k], { diemNguoi: 6, luc: 0 }) } };
  assert.equal(p.baiViet[k].trangThai, TRANG_THAI_DIEM.xacNhan);
  const lai = ghiBaiViet(p, 'ta3', 1, { viet: 'b', cham: { diem: 9, loi: [] } }, 'unit');
  assert.equal(lai.baiViet[k].trangThai, TRANG_THAI_DIEM.tam);
  assert.equal(lai.baiViet[k].diemNguoi, null);
  assert.equal(lai.baiViet[k].xacNhanLuc, null);
});

test('MỌI chỗ hiện điểm viết đều đi qua diemHienThi', () => {
  /* "Định nghĩa XONG" của §7: mọi điểm viết trên màn có 1 trong 3 nhãn. Ba chỗ con
     số ấy lộ ra từng mỗi chỗ tự viết một dòng chữ khác nhau. */
  const bo = (x) => x.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');
  for (const [p, ten] of [
    ['../src/mon/tienganh/components/VietBai.jsx', 'màn lời chấm'],
    ['../src/mon/tienganh/components/ManTiengAnh.jsx', 'thẻ bài viết'],
  ]) {
    const ma = bo(readFileSync(new URL(p, import.meta.url), 'utf8'));
    assert.match(ma, /diemHienThi\(/, `${ten} không đi qua diemHienThi`);
    /* Và KHÔNG còn chỗ nào lôi `cham.diem` hay `xong.diem` ra hiển thị trực tiếp. */
    assert.ok(!/\{cham\.diem/.test(ma), `${ten} còn hiện cham.diem trực tiếp`);
    assert.ok(!/\$\{xong\.diem\}/.test(ma), `${ten} còn hiện xong.diem trực tiếp`);
  }
});

test('KHÔNG có nút xác nhận nào ngoài Góc bố mẹ', () => {
  /* Xác nhận điểm của chính mình thì không còn là xác nhận. */
  const bo = (x) => x.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^[ \t]*\/\/.*$/gm, ' ');
  const vb = bo(readFileSync(new URL('../src/mon/tienganh/components/VietBai.jsx', import.meta.url), 'utf8'));
  assert.ok(!/xacNhanDiem/.test(vb), 'màn bé làm bài có đường gọi xacNhanDiem');
  const man = bo(readFileSync(new URL('../src/mon/tienganh/components/ManTiengAnh.jsx', import.meta.url), 'utf8'));
  const i = man.indexOf('function ChoXacNhan');
  assert.notEqual(i, -1, 'không thấy khối xác nhận trong Góc bố mẹ');
  assert.match(man.slice(i, i + 3000), /MucBoMe/,
    'khối xác nhận không nằm trong Góc bố mẹ — bé sẽ thấy nó');
});

test('BKT đọc `diem`, KHÔNG chờ xác nhận — và đó là quyết định', () => {
  /* Bắt `onAttempt` chờ bố mẹ thì engine đứng lại ở mọi bài viết của mọi bé chưa có
     người lớn ngồi cạnh, tức phần thích ứng tắt hẳn vì một việc của người lớn. */
  const hb = readFileSync(new URL('../src/mon/tienganh/lib/hocba.js', import.meta.url), 'utf8');
  assert.match(hb, /BKT ĐỌC `diem`, KHÔNG ĐỌC HÀM NÀY/,
    'quyết định này phải ghi rõ trong chú thích — không thì lần sau có người "sửa" nó');
  const vb = readFileSync(new URL('../src/mon/tienganh/components/VietBai.jsx', import.meta.url), 'utf8');
  assert.match(vb, /ok: Number\(r\?\.cham\?\.diem/,
    'đường vào engine đã đổi — kiểm lại quyết định ở `diemHienThi`');
});
