/**
 * CỔNG · BÀI VIẾT NGẮN CHẤM BẰNG AI.
 * chạy: node test/tienganh_chamviet.test.mjs
 *
 * Bác chốt 18-08-2026 bốn điều, và cả bốn đều là thứ cổng soi được:
 *
 *   1. sửa lỗi và khen CỤ THỂ      → lời dặn phải ĐÒI `khen` và `loi[]` có câu sửa
 *   2. có điểm, nói rõ AI chấm     → điểm kẹp trong thang, và mọi chỗ hiện điểm
 *                                    phải kèm chữ "máy chấm"
 *   3. chỉ gợi ý bằng vốn đã học   → `soiLoiCham` phải BỎ câu có chữ lạ
 *   4. bố mẹ đọc được              → bài viết được giữ lại, không chỉ con số
 *
 * ── VÌ SAO SOI ĐIỀU 3 KỸ NHẤT ──
 * Ba điều kia hỏng thì nhìn ra ngay. Điều 3 hỏng thì lời chấm vẫn đẹp, vẫn đúng
 * ngữ pháp, chỉ là dạy bé một từ bé không có cách nào hiểu — và bé tám tuổi đọc
 * lời chấm là tin. Cùng dòng họ với `"Bye, bike."`: mô hình đã được dặn rất rõ và
 * vẫn làm sai, nên chỗ nào chặn được bằng luật thì phải chặn bằng luật.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import {
  docLoiCham, soiLoiCham, chuLa, demCau, duocGui, DIEM_TOI_DA,
} from '../src/mon/tienganh/lib/chamviet.js';
import { readFileSync as _rf } from 'node:fs';
const tranhKhai = (() => { try { return JSON.parse(_rf(new URL('../../data/tienganh/canh_lop3.json', import.meta.url), 'utf8')); } catch { return []; } })();
import {
  soiBaiViet, loiDanCham, TOI_DA_CHU_BAI_VIET,
  loiDanTimLoi, loiDanSua, loiDanBoMe, chamBaiViet, khungCham,
  SUA_LAI_TOI_DA, TOKEN_TIM_LOI, TOKEN_SUA, TOKEN_BO_ME, LOI_SUA_LAI,
} from '../functions/src/chamviet.js';
import { PHIEN_BAN_MAU, locKhung } from '../functions/src/vantay.js';
import { diemHienThi } from '../src/mon/tienganh/lib/hocba.js';

const VON = [
  { tu: 'hello', nghia: 'xin chào' },
  { tu: 'I', nghia: 'tôi' },
  { tu: 'thank you', nghia: 'cảm ơn' },
  { tu: 'Ben', nghia: 'bạn Ben' },
];
const MAU = ["Hello. I'm Ben."];

/* ═══════════ MÁY CHỦ · CHỐT CỬA ═══════════ */

test('bài rỗng bị chặn ngay tại cửa, không tốn một lượt gọi Groq', () => {
  assert.throws(() => soiBaiViet({ viet: '   ', de: 'x', vonTu: VON }), /Con chưa viết gì/);
});

test('bài quá dài bị chặn — khoá Groq là khoá của mình', () => {
  const dai = 'a'.repeat(TOI_DA_CHU_BAI_VIET + 1);
  assert.throws(() => soiBaiViet({ viet: dai, de: 'x', vonTu: VON }), /dài quá/);
});

test('thiếu bảng vốn từ thì TỪ CHỐI, không chấm bừa', () => {
  /* Chấm mà không có bảng vốn thì máy tự do gợi ý bất cứ từ nào — hỏng đúng điều
     bác chốt, và hỏng im lặng vì lời chấm vẫn trông tử tế. */
  assert.throws(() => soiBaiViet({ viet: 'Hello.', de: 'x', vonTu: [] }), /vốn từ/);
});

test('gói hợp lệ thì trả về bản đã sạch, giữ đủ bốn phần', () => {
  const g = soiBaiViet({ viet: ' Hello. ', de: 'Viết đi', vonTu: VON, mauCau: MAU });
  assert.equal(g.viet, 'Hello.');
  assert.equal(g.de, 'Viết đi');
  assert.equal(g.vonTu.length, 4);
  assert.deepEqual(g.mauCau, MAU);
});

test('lời dặn ĐÒI đủ bốn điều bác chốt', () => {
  const d = loiDanCham({ de: 'Viết đi', viet: 'Hello.', vonTu: VON, mauCau: MAU, lop: 3 });
  assert.match(d, /CỤ THỂ/, 'phải đòi khen cụ thể');
  assert.match(d, /câu sửa lại cho đúng/i, 'phải đòi câu sửa');
  assert.match(d, /CHỈ ĐƯỢC dùng từ trong bảng vốn từ/, 'phải cấm từ mới');
  assert.match(d, /Điểm từ 0 tới 10/, 'phải đòi điểm');
  assert.match(d, /bố mẹ/i, 'phải đòi lời cho bố mẹ');
  /* Bảng vốn từ phải nằm TRONG lời dặn, không phải chỉ được nhắc tới. */
  for (const v of VON) assert.ok(d.includes(v.tu), `thiếu từ "${v.tu}" trong lời dặn`);
});

/* ═══════════ MÁY CON · BÓC VÀ SOI ═══════════ */

const THO = JSON.stringify({
  diem: 8,
  khen: 'Con chào đúng và viết đúng tên mình.',
  loi: [{ cau: 'I Ben.', sua: "I'm Ben.", viSao: 'Thiếu chữ “am”.' }],
  goiY: 'Con thử viết thêm câu cảm ơn: Thank you.',
  choBoMe: 'Con viết được câu chào và câu giới thiệu tên.',
});

test('bóc được lời chấm từ JSON', () => {
  const c = docLoiCham(THO);
  assert.equal(c.diem, 8);
  assert.equal(c.loi.length, 1);
  assert.equal(c.loi[0].sua, "I'm Ben.");
});

test('bóc được cả khi mô hình kèm chữ thừa quanh khối JSON', () => {
  /* Mô hình được dặn trả JSON thuần, nhưng KHÔNG được tin là nó luôn làm đúng —
     cùng lối với `docTraLoi` của phòng luyện nói. */
  assert.equal(docLoiCham(`Đây là kết quả:\n${THO}\nHết.`).diem, 8);
});

test('không bóc ra được thì trả null, KHÔNG dựng lời chấm rỗng', () => {
  /* Lời chấm rỗng thì bé thấy "0/10" và một ô trắng — tệ hơn hẳn một câu báo lỗi. */
  assert.equal(docLoiCham('cô chưa chấm được'), null);
  assert.equal(docLoiCham(''), null);
});

test('điểm ngoài thang thì KẸP về thang, không vứt cả lời chấm', () => {
  assert.equal(docLoiCham(JSON.stringify({ diem: 95, khen: 'x' })).diem, DIEM_TOI_DA);
  assert.equal(docLoiCham(JSON.stringify({ diem: -3, khen: 'x' })).diem, 0);
  assert.equal(docLoiCham(JSON.stringify({ diem: 'giỏi', khen: 'x' })).diem, null);
});

test('chữ lạ nhận ra được, kể cả khi vốn từ là CỤM nhiều chữ', () => {
  /* `thank you` là một mục trong bảng từ. So nguyên cụm thì cả `thank` lẫn `you`
     đều thành chữ lạ, và lời chấm đúng lại bị bỏ. */
  assert.deepEqual(chuLa('Thank you.', { vonTu: VON }), []);
  assert.deepEqual(chuLa('I have a dog.', { vonTu: VON, mauCau: MAU }), ['have', 'a', 'dog']);
});

test('chữ trong MẪU CÂU cũng tính là đã học', () => {
  /* `I'm` không phải "từ mới" của unit nào, nhưng nó nằm trong công thức bé học
     mỗi ngày. Không cộng vào là lời chấm đúng nhất cũng bị bỏ. */
  assert.deepEqual(chuLa("I'm Ben.", { vonTu: VON, mauCau: MAU }), []);
});

test('câu sửa chứa từ CHƯA HỌC thì bị BỎ, và bỏ có báo', () => {
  const tho = docLoiCham(JSON.stringify({
    diem: 7, khen: 'Tốt lắm.',
    loi: [{ cau: 'I Ben.', sua: 'I am a student.', viSao: '…' }],
    goiY: 'Con viết thêm: I like football.',
  }));
  const { cham, boQua } = soiLoiCham(tho, { vonTu: VON, mauCau: MAU });
  assert.equal(cham.loi.length, 0, 'câu sửa có từ lạ thì bỏ CẢ mục lỗi');
  assert.equal(cham.goiY, '', 'gợi ý có từ lạ thì bỏ');
  assert.equal(boQua.length, 2, 'bỏ thì phải đếm được, để màn hình nói ra');
  assert.equal(cham.diem, 7, 'điểm và lời khen vẫn giữ — bỏ đúng phần hỏng thôi');
  assert.equal(cham.khen, 'Tốt lắm.');
});

test('lời gợi ý TIẾNG VIỆT có lẫn tiếng Anh KHÔNG bị bỏ oan', () => {
  /* "Con thử viết thêm câu cảm ơn: Thank you." — đem cả câu đi so với vốn từ tiếng
     Anh thì mọi chữ Việt đều "lạ", và lời gợi ý đúng bị bỏ. Đã sập ngay lượt thử
     đầu tiên, nên phải có phép kiểm riêng. */
  const tho = docLoiCham(JSON.stringify({
    diem: 9, khen: 'Tốt.', loi: [],
    goiY: 'Con thử viết thêm câu cảm ơn: Thank you.',
  }));
  const { cham, boQua } = soiLoiCham(tho, { vonTu: VON, mauCau: MAU });
  assert.equal(boQua.length, 0);
  assert.match(cham.goiY, /Thank you/);
});

test('gợi ý có câu tiếng Anh chứa từ CHƯA HỌC thì vẫn bị bỏ', () => {
  /* Chiều ngược lại của phép trên — nới cho lời Việt đi qua mà thả lọt câu Anh lạ
     thì phép kiểm mất sạch ý nghĩa. */
  const tho = docLoiCham(JSON.stringify({
    diem: 9, khen: 'Tốt.', loi: [],
    goiY: 'Con thử viết thêm: I like football.',
  }));
  const { cham, boQua } = soiLoiCham(tho, { vonTu: VON, mauCau: MAU });
  assert.equal(cham.goiY, '');
  assert.equal(boQua.length, 1);
});

test('lời chấm sạch thì đi qua nguyên vẹn', () => {
  const { cham, boQua } = soiLoiCham(docLoiCham(THO), { vonTu: VON, mauCau: MAU });
  assert.equal(boQua.length, 0);
  assert.equal(cham.loi.length, 1);
  assert.ok(cham.goiY);
});

/* ═══════════ CHẶN TẠI CHỖ, TRƯỚC KHI GỌI MẠNG ═══════════ */

test('đếm câu: câu cuối quên dấu chấm vẫn tính', () => {
  assert.equal(demCau('Hello. I am Ben'), 2);
  assert.equal(demCau('Hello.'), 1);
  assert.equal(demCau('   '), 0);
});

test('chưa đủ số câu thì chặn ngay, và NÓI RÕ vì sao', () => {
  assert.equal(duocGui('Hello.', 2).ok, false);
  assert.match(duocGui('Hello.', 2).vi, /ít nhất 2 câu/);
  assert.equal(duocGui('Hello. I am Ben.', 2).ok, true);
});

/* ═══════════ ĐIỂM PHẢI ĐEO NHÃN ═══════════ */

test('mọi chỗ hiện điểm đều nói rõ MÁY CHẤM', () => {
  /* Bác chốt: "có điểm để vào sổ — và phải nói rõ là AI chấm". Con số không nhãn
     trong sổ học bạ sẽ được đọc thành điểm của cô giáo, và bố mẹ không có cách nào
     tự phát hiện. Ba chỗ con số ấy lộ ra: màn lời chấm, thẻ trên trang chính, và
     gói ghi vào sổ. */
  /* ⚠ SOI TÍNH CHẤT, ĐỪNG GHIM CHUỖI. Bản đầu đòi đúng chữ `Máy chấm (AI)` ở
     `VietBai.jsx` và `điểm (máy chấm)` ở `ManTiengAnh.jsx`. Tới việc V5 cả hai nhãn
     do `diemHienThi` sinh (vì có thêm trạng thái "bố mẹ đã xác nhận"), nên cổng đỏ.
     Và nó đỏ CÓ ÍCH: nó chỉ ra rằng nhãn mới của ca "đã xác nhận" không còn một chữ
     nào nói con số do MÁY chấm — tức mất đúng thứ phép canh này sinh ra để giữ. Vá
     bằng `nhanDay`, và nay soi TÍNH CHẤT ở hai tầng:
       1. mọi nhãn `diemHienThi` sinh ra đều nói điểm từ đâu;
       2. hai màn đều dùng nhãn ấy, không tự viết chữ. */
  for (const m of [{ diem: 8 }, { diem: 8, trangThai: 'xacNhan' },
                   { diem: 8, trangThai: 'xacNhan', diemNguoi: 6 }]) {
    const { nhanDay } = diemHienThi(m);
    assert.match(nhanDay, /Máy chấm \(AI\)/,
      `nhãn không nói điểm do MÁY chấm: ${JSON.stringify(nhanDay)}`);
  }
  for (const [p, ten] of [['../src/mon/tienganh/components/VietBai.jsx', 'màn lời chấm'],
                          ['../src/mon/tienganh/components/ManTiengAnh.jsx', 'thẻ trang chính']]) {
    const ma = readFileSync(new URL(p, import.meta.url), 'utf8');
    assert.match(ma, /hien\.nhanDay/, `${ten} không dùng nhãn đầy đủ của diemHienThi`);
  }

  const so = readFileSync(new URL('../src/mon/tienganh/lib/progress.js',
    import.meta.url), 'utf8');
  assert.match(so, /nguon: 'ai'/, 'gói ghi vào sổ phải đeo nhãn nguồn');
  assert.match(so, /viet: String\(viet/, 'sổ phải giữ CẢ BÀI VIẾT, không chỉ điểm');
});

test('luật Firestore CHO ghi loại `viet` — không thì máy chủ từ chối trong im lặng', () => {
  const luat = readFileSync(new URL('../firestore.rules', import.meta.url), 'utf8');
  const khoi = luat.slice(luat.indexOf('match /hocBaTA/'));
  const m = khoi.match(/data\.loai in \[([^\]]+)\]/);
  assert.ok(m, 'khối hocBaTA không chốt danh sách loai');
  assert.match(m[1], /'viet'/, "thiếu 'viet' — bài viết ghi lên sẽ bị từ chối, im lặng");
});

test('đề bài viết đã dựng và đủ hình dạng', () => {
  const p = new URL('../public/content/ta3/vietbai.json', import.meta.url);
  if (!existsSync(p)) return;                 // quyển chưa dựng thì bỏ qua
  const ds = JSON.parse(readFileSync(p, 'utf8'));
  assert.ok(ds.length >= 4, `phải có đề cho mỗi chương, đang ${ds.length}`);
  assert.ok(ds.filter((d) => d.phamVi === 'unit').length >= 15,
    'phải có đề cho từng unit nữa — bác chốt 18-08');
  for (const d of ds) {
    assert.ok(d.de && /[àáảãạăâêôơư]/i.test(d.de), `${d.id}: đề phải bằng TIẾNG VIỆT`);
    /* ⚠ Ngưỡng hạ từ `> 10` xuống `>= 10` ngày 18-08, và hạ vì một lý do CỤ THỂ:
       bảng từ nay lọc bỏ những mục bé không gõ được — sách khai "the alphabet
       (A–Z)" như một từ vựng, bấm vào là bài của bé có một chuỗi không ai viết bao
       giờ. Unit 0 vì thế còn đúng 10 từ, mà vốn THẬT thì không mất gì.
       Đây không phải nới cổng cho dễ thở: phần "nhiều hơn" bác đòi nay nằm ở
       `goiY` — những CỤM ghép được, có cổng riêng ngay dưới. */
    assert.ok(d.vonTu.length >= 10, `${d.id}: vốn từ quá ít (${d.vonTu.length})`);
    /* Bài TẢ TRANH cố ý không có mẫu câu — chỗ dựa của bé là BỨC TRANH, không phải
       một danh sách câu để chép. Xem phép soi riêng ở khối dưới. */
    if (d.dang !== 'tranh') {
      assert.ok(d.mauCau.length > 0, `${d.id}: không có mẫu câu nào để bé dựa vào`);
    }
    assert.ok(d.toiThieu >= 2, `${d.id}: số câu tối thiểu vô lý`);
  }
  /* Vốn từ DỒN, và dồn RIÊNG TỪNG PHẠM VI: đề unit 5 chứa trọn vốn của unit 4, đề
     chương 2 chứa trọn vốn của chương 1. So lẫn hai phạm vi thì đề chương 1 (44 từ)
     đứng ngay sau đề unit 20 (204 từ) và cổng báo mất 160 từ — báo oan. */
  for (const pv of ['unit', 'chuong']) {
    /* ⚠ BÀI TẢ TRANH ĐỨNG NGOÀI PHÉP DỒN DẦN. Bảng từ của nó là VẬT CÓ TRONG BỨC
       TRANH ấy (kite · yo-yo · kitten…), không phải vốn tích luỹ của quyển — nên
       unit sau không có nghĩa vụ chứa chúng. Không loại ra thì cổng báo "unit 1 mất
       từ kite", một lỗi không có thật. */
    const nhom = ds.filter((d) => (d.phamVi || 'chuong') === pv && d.dang !== 'tranh');
    for (let i = 1; i < nhom.length; i += 1) {
      const truoc = new Set(nhom[i - 1].vonTu.map((v) => v.tu));
      const nay = new Set(nhom[i].vonTu.map((v) => v.tu));
      for (const t of truoc) {
        assert.ok(nay.has(t), `${nhom[i].id}: mất từ "${t}" của ${pv} trước`);
      }
    }
  }
});

/* ═══════════ GỢI Ý PHẢI GHÉP ĐƯỢC THÀNH MỘT ĐOẠN ═══════════ */

test('gợi ý là CỤM ghép được, xếp theo chỗ trong đoạn', async () => {
  /* Bác chốt 18-08-2026: "phần gợi ý nên bổ sung thêm nhiều từ hơn cho con chọn và
     ghi là gợi ý. Con có thể typing thêm theo ý của con. Lưu ý là các từ gợi ý ấy
     phải ghép lại thành được đoạn văn có ý nghĩa chứ như giờ bạn cho linh tinh."

     Bản cũ bày đúng một bảng: 53 ô CHỮ RỜI, dồn từ chương 1 tới đây, xếp theo thứ
     tự sách — `one · two · … · the alphabet (A–Z) · hello · … · your`. Bấm bừa vài
     cái ra "ten hello your old": không phải câu, càng không phải đoạn.

     Không cổng nào bắt được, vì mọi thứ đo được đều đúng: từ nào cũng đã học, số
     lượng thì dư dả. Chỉ MỞ RA BẤM THỬ mới thấy. Nên phép kiểm phải hỏi đúng câu
     ấy: bấm mỗi nhóm một cái thì có ra một đoạn không. */
  const { readFileSync, existsSync } = await import('node:fs');
  const url = new URL('../public/content/ta3/vietbai.json', import.meta.url);
  if (!existsSync(url)) return;
  const ds = JSON.parse(readFileSync(url, 'utf8'));
  assert.ok(ds.length > 0, 'không có đề nào thì mọi vòng lặp chạy 0 lần');

  for (const k of ds) {
    /* ⚠ BÀI TẢ TRANH KHÔNG CÓ GỢI Ý CÂU, và đó là chủ ý. Bác chốt 19-08: "Về phần
       viết cũng vậy" — bày mẫu câu ra thì bé chép lại, mà mẫu câu của bài tả tranh
       CHÍNH LÀ đoạn mô tả, tức là cho sẵn đáp án. Bảng TỪ thì vẫn còn (bấm một từ
       không phải được cho một câu), và cổng dưới vẫn soi nó. */
    if (k.dang === 'tranh') {
      assert.ok(k.tranh, `${k.id}: khai dạng tranh mà không có ảnh`);
      assert.ok(!k.goiY?.length && !k.mauCau?.length,
        `${k.id}: bài tả tranh mà vẫn bày mẫu câu — thành bài chép lại`);
      assert.ok(k.yTrongTranh?.length, `${k.id}: thiếu bản mô tả để máy chấm đối chiếu`);
      /* ⚠ Soi ĐỘNG, đừng ghim tên vật. Bản đầu viết /kite|yo-yo|kitten|bear/ — đúng
         cho bức tranh unit 0 và sai cho hai mươi bức còn lại. Bảng từ phải chứa MỌI
         vật của chính bức tranh ấy, và bản khai tranh nói sẵn vật nào. */
      /* ⚠ NGUỒN ĐỔI 20-08-2026: bản khai CẢNH thay bản khai KỆ. Vật của cảnh nằm
         ở `vat[].tu` — những mục khai `ve` là đồ vẽ tay (bàn · ghế · cửa sổ), không
         phải từ vựng nên không đòi có trong bảng từ. */
      const khaiT = tranhKhai.find((x) => x.unit === k.unit);
      for (const n of (khaiT?.vat || []).filter((x) => x.tu)) {
        assert.ok((k.vonTu || []).some((v) => v.tu === n.tu),
          `${k.id}: bảng từ thiếu vật “${n.tu}” của tranh`);
      }

      /* ══ BẢNG TỪ PHẢI ĐỦ ĐỂ VIẾT LẠI CẢ ĐOẠN MÔ TẢ ══ (bác chốt 19-08-2026)
         "Phần từ trong tranh cần đầy đủ hơn như nội dung của phần đọc (ít nhất là
          thế)."

         Bản trước gom tên VẬT rồi thêm tay mấy chữ nối ĐOÁN CHỪNG — và đoán thiếu:
         "That's" của câu "That's a yo-yo." không có trong bảng, nên bé bấm hết bảng
         vẫn không viết nổi đoạn mà chính bài đọc vừa cho đọc. Không lỗi đỏ ở đâu:
         bảng vẫn đầy chữ, chỉ là thiếu đúng một chữ bé cần.

         Phép đo: xoá mọi từ trong bảng khỏi từng câu của đoạn; còn sót chữ nào thì
         chữ ấy bé không có cách nào gõ ra. */
      const bang = (k.vonTu || []).map((v) => v.tu).filter(Boolean);
      for (const cau of k.yTrongTranh || []) {
        let con = cau;
        for (const t of bang) {
          con = con.replace(new RegExp(`\\b${t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi'), ' ');
        }
        const sot = con.match(/[A-Za-z][A-Za-z']*/g) || [];
        assert.equal(sot.length, 0,
          `${k.id}: bảng từ thiếu ${JSON.stringify(sot)} — bé không viết nổi “${cau}”`);
      }
      continue;
    }
    assert.ok(k.goiY?.length, `${k.id}: không có gợi ý theo nhóm nào`);
    for (const g of k.goiY) {
      assert.ok(g.nhan && g.cum?.length, `${k.id}: nhóm “${g.nhan}” rỗng`);
      for (const c of g.cum) {
        /* Mỗi mục là một CÂU TRỌN: mở đầu chữ hoa (hoặc chỗ trống), đóng bằng dấu
           câu. Một từ trần thì bấm vào không ghép được với gì cả — đúng chỗ hỏng cũ. */
        assert.match(c, /^([A-Z]|___)/, `${k.id}: “${c}” không mở đầu chữ hoa`);
        assert.match(c, /[.!?]$/, `${k.id}: “${c}” không phải một câu trọn`);
        /* Dấu vết của một phép cắt hỏng, và của nguồn thiếu dấu cách. */
        assert.ok(!/ - |\/|\[/.test(c), `${k.id}: “${c}” còn dấu ghép câu`);
        assert.ok(!/[,;]\S/.test(c), `${k.id}: “${c}” thiếu dấu cách sau dấu phẩy`);
      }
      assert.equal(new Set(g.cum).size, g.cum.length, `${k.id}: nhóm “${g.nhan}” có mục trùng`);
    }
    /* ⚠ KHÔNG ĐƯỢC BÀY TÊN NGƯỜI KHÁC. Bé tên Mai mà bấm "Hello. I'm Ben." thì bài
       của bé viết sai về CHÍNH BÉ, và máy chấm vẫn cho đúng ngữ pháp. Bốn ví dụ của
       unit 1 chỉ khác nhau ở cái tên, nên bày cả bốn là bày bốn tên người lạ. */
    const ten = new Set(['Ben', 'Lucy', 'Mai', 'Minh', 'Bill', 'Linh', 'Mary', 'Nam']);
    for (const g of k.goiY) {
      for (const c of g.cum) {
        for (const w of c.split(/[^A-Za-z']+/)) {
          assert.ok(!ten.has(w), `${k.id}: gợi ý “${c}” bắt bé xưng tên người khác`);
        }
      }
    }
    /* Bảng từ chỉ nhận thứ bé GÕ ĐƯỢC. Sách khai "the alphabet (A–Z)" như một từ
       vựng; bấm vào là bài của bé có một chuỗi không ai viết bao giờ. */
    for (const v of k.vonTu || []) {
      assert.ok(!/[()–]/.test(v.tu), `${k.id}: bảng từ còn mục không gõ được “${v.tu}”`);
    }
  }
});

test('màn bài viết NÓI RÕ đó là gợi ý, và bé được tự gõ thêm', async () => {
  /* Bác dặn "ghi là gợi ý" và "con có thể typing thêm theo ý của con". Ô nhập vốn
     đã cho gõ tự do từ đầu — nhưng không nói ra thì bé tám tuổi tưởng chỉ được bấm
     mấy cái nút, và cả phần tự viết coi như không có. */
  const { readFileSync } = await import('node:fs');
  const s = readFileSync(new URL('../src/mon/tienganh/components/VietBai.jsx', import.meta.url), 'utf8')
    .replace(/\{\/\*[\s\S]*?\*\/\}/g, '');
  assert.match(s, /Gợi ý — bấm để thêm vào bài/);
  assert.match(s, /tự gõ thêm câu của riêng con/);
  assert.match(s, /bai\?\.goiY/, 'màn phải đọc gợi ý theo nhóm từ đề bài');
});

/* ═══════════ CHUỖI BA MẮT XÍCH (việc V4) ═══════════ */

const GOI = {
  de: 'Viết 3 câu về trường của em.',
  viet: 'My school is big. I like my school.',
  vonTu: [{ tu: 'school', nghia: 'trường' }, { tu: 'big', nghia: 'to' },
          { tu: 'like', nghia: 'thích' }, { tu: 'my', nghia: 'của tôi' },
          { tu: 'is', nghia: 'là' }, { tu: 'i', nghia: 'tôi' }],
  mauCau: ['My school is + [Adjective].'],
  lop: 3,
};

/** Client giả trả lần lượt theo danh sách, và CHỤP LẠI từng lời dặn gửi lên. */
function mayGia(ds) {
  const daGoi = [];
  const f = () => ({ chat: { completions: { create: async (o) => {
    daGoi.push(o);
    const x = ds[Math.min(daGoi.length - 1, ds.length - 1)];
    return { choices: [{ message: { content: typeof x === 'string' ? x : JSON.stringify(x) } }] };
  } } } });
  f.daGoi = daGoi;
  return f;
}

const CHAM_SACH = { diem: 8, khen: 'Con dùng đúng từ "school".',
  loi: [{ cau: 'x', sua: 'My school is big.', viSao: 'thiếu is' }], goiY: 'Viết thêm nhé' };
const CHAM_LA = { ...CHAM_SACH,
  loi: [{ cau: 'x', sua: 'My school is delicious.', viSao: 'thiếu is' }] };

/**
 * ⚠ CHỮ "KHÔNG SỬA" LÀ CHỐT CỦA MẮT XÍCH 1.
 * Cho nó sửa luôn thì nó sửa bằng từ hay nhất nó biết, và từ hay nhất thường là từ
 * bé chưa học — đúng chỗ hỏng mà cả việc V4 sinh ra để chữa.
 */
test('mắt xích 1 CẤM sửa, cấm khen, cấm gợi ý', () => {
  const d = loiDanTimLoi(GOI);
  assert.match(d, /KHÔNG SỬA/);
  assert.match(d, /KHÔNG KHEN/);
  assert.match(d, /CHỈ LIỆT KÊ LỖI/);
  assert.match(d, /NGUYÊN VĂN/, 'phải đòi trích đúng câu bé viết');
  /* Và khung JSON của nó KHÔNG được có trường `sua` — có là mời nó sửa. */
  assert.ok(!/"sua"/.test(d), 'khung JSON mắt xích 1 vẫn có trường `sua`');
  assert.match(d, /chinhTa \| thieuTu \| thuTu \| mauCau \| khac/, 'thiếu danh sách loại lỗi');
});

test('mắt xích 2 nhận danh sách lỗi, và dòng CẤM chỉ mọc khi có chữ lạ', () => {
  const co = loiDanSua(GOI, [{ cau: 'My school big.', loai: 'thieuTu', ghiChu: 'thiếu is' }]);
  assert.match(co, /DANH SÁCH LỖI ĐÃ TÌM ĐƯỢC/);
  assert.match(co, /My school big\./);
  assert.match(co, /đừng thêm lỗi mới/, 'không chốt thì nó tự tìm thêm lỗi, lệch với mắt xích 1');
  assert.ok(!/LẦN TRƯỚC/.test(co), 'dòng cấm mọc ra khi chưa có chữ lạ nào');

  const cam = loiDanSua(GOI, [], ['delicious', 'wonderful']);
  assert.match(cam, /LẦN TRƯỚC/);
  assert.match(cam, /delicious, wonderful/, 'phải GỌI TÊN chữ cấm, không nhắc chung chung');
  /* ⚠ Và phải CHO PHÉP bỏ trống câu sửa: ép nó sửa bằng mọi giá là ép nó bịa thêm
     một chữ khác. `soiLoiCham` của máy con vẫn còn đó. */
  assert.match(cam, /"sua": ""/, 'không cho bỏ trống thì nó bịa chữ khác');

  /* Không có lỗi nào thì phải NÓI RA, đừng để danh sách rỗng im lặng. */
  assert.match(loiDanSua(GOI, []), /KHÔNG CÓ LỖI NÀO/);
});

test('mắt xích 3 KHÔNG mang bài viết của bé', () => {
  /* Bố mẹ cần hai câu suy từ LỜI CHẤM. Đưa thêm một bản bài viết là thêm một chỗ
     chữ của bé đi qua, mà chẳng để làm gì. */
  const d = loiDanBoMe(GOI, CHAM_SACH);
  assert.ok(!d.includes(GOI.viet), 'bài viết của bé lọt vào mắt xích 3');
  assert.ok(!d.includes(GOI.de), 'đề bài lọt vào mắt xích 3');
  assert.match(d, /ĐÚNG HAI câu/);
  assert.match(d, /không nhắc điểm số/);
});

test('chạy đủ chuỗi: 1 → 2 → 3, mỗi mắt xích một trần token', async () => {
  const gia = mayGia([{ loi: [{ cau: 'x', loai: 'thieuTu', ghiChu: 'thiếu is' }] },
                      CHAM_SACH, { choBoMe: 'Con làm tốt.' }]);
  const r = await chamBaiViet(GOI, gia);
  assert.equal(gia.daGoi.length, 3, 'không chạy đủ ba mắt xích');
  assert.deepEqual(gia.daGoi.map((x) => x.max_tokens), [TOKEN_TIM_LOI, TOKEN_SUA, TOKEN_BO_ME]);
  assert.ok(TOKEN_TIM_LOI + TOKEN_SUA + TOKEN_BO_ME <= 1300, 'tổng token vượt trần §7');
  /* Nhiệt độ TĂNG dần: tìm lỗi là việc máy móc nhất, lời cho bố mẹ cần chữ mềm hơn. */
  assert.deepEqual(gia.daGoi.map((x) => x.temperature), [0.1, 0.2, 0.3]);
  assert.equal(r.lanSuaLai, 0);
  const c = JSON.parse(r.chu);
  /* Lời chấm phải đủ NĂM trường — "Định nghĩa XONG" của §7. */
  for (const k of ['diem', 'khen', 'loi', 'goiY', 'choBoMe']) {
    assert.ok(k in c, `lời chấm thiếu trường "${k}"`);
  }
  /* Danh sách lỗi của mắt xích 1 phải THẬT SỰ tới mắt xích 2. */
  assert.match(gia.daGoi[1].messages[0].content, /thiếu is/);
});

test('chữ lạ → xin lại mắt xích 2, kèm đúng chữ cấm', async () => {
  const truoc = { ...LOI_SUA_LAI };
  const gia = mayGia([{ loi: [] }, CHAM_LA, CHAM_SACH, { choBoMe: 'ổn' }]);
  const r = await chamBaiViet(GOI, gia);
  assert.equal(r.lanSuaLai, 1);
  assert.deepEqual(r.chuLaConLai, [], 'xin lại ăn thì không còn chữ lạ nào');
  assert.equal(JSON.parse(r.chu).loi[0].sua, 'My school is big.');
  /* Lượt xin lại phải mang dòng cấm, và gọi tên đúng chữ vừa dùng. */
  assert.match(gia.daGoi[2].messages[0].content, /LẦN TRƯỚC/);
  assert.match(gia.daGoi[2].messages[0].content, /delicious/);
  assert.equal(LOI_SUA_LAI.so - truoc.so, 1);
  assert.equal(LOI_SUA_LAI.thanh - truoc.thanh, 1);
});

test('trượt đủ vòng → trả về kèm chữ lạ, máy con boQua như cũ', async () => {
  const gia = mayGia([{ loi: [] }, CHAM_LA]);   // lần nào cũng "delicious"
  const r = await chamBaiViet(GOI, gia);
  /* 1 (tìm lỗi) + 1 (sửa) + SUA_LAI_TOI_DA (xin lại) = 4; mắt xích 3 vẫn chạy. */
  assert.equal(r.lanSuaLai, SUA_LAI_TOI_DA);
  assert.ok(r.chuLaConLai.includes('delicious'),
    'hết vòng mà vẫn trượt thì phải NÓI RA chữ nào còn sót');
  /* ⚠ VÀ VẪN TRẢ LỜI CHẤM. `soiLoiCham` ở máy con là hàng rào CUỐI — nó bỏ đúng
     mục hỏng và giữ lại điểm với lời khen. Vứt cả lời chấm là bé mất phần nó xứng
     đáng được nghe. */
  assert.ok(JSON.parse(r.chu).diem, 'vứt cả lời chấm vì một chữ');
  assert.ok(JSON.parse(r.chu).khen);
});

test('chữ CẤM dồn qua các vòng, không quên vòng trước', async () => {
  /* Bỏ chữ A rồi dùng chữ B, vòng sau quay về A — đã thấy ở vòng gọi lại phòng nói. */
  const la2 = { ...CHAM_SACH, loi: [{ cau: 'x', sua: 'My school is wonderful.', viSao: 'x' }] };
  const gia = mayGia([{ loi: [] }, CHAM_LA, la2, CHAM_SACH, { choBoMe: 'ổn' }]);
  await chamBaiViet(GOI, gia);
  const dan3 = gia.daGoi[3].messages[0].content;
  assert.match(dan3, /delicious/, 'quên chữ cấm của vòng trước');
  assert.match(dan3, /wonderful/);
});

test('mắt xích 1 hỏng thì vẫn chấm được, chỉ kém hơn', async () => {
  /* Dừng cả lời chấm vì mắt xích tìm lỗi trượt là bé mất hết. Mắt xích 2 tự tìm
     lỗi được như bản trước V4. */
  let n = 0;
  const gia = () => ({ chat: { completions: { create: async () => {
    n += 1;
    if (n === 1) return { choices: [{ finish_reason: 'length', message: { content: '' } }] };
    return { choices: [{ message: { content: JSON.stringify(n === 2 ? CHAM_SACH : { choBoMe: 'ổn' }) } }] };
  } } } });
  const r = await chamBaiViet(GOI, gia);
  assert.ok(JSON.parse(r.chu).diem, 'mắt xích 1 trượt là mất cả lời chấm');
});

test('mắt xích 3 hỏng thì KHÔNG làm hỏng lời chấm', async () => {
  let n = 0;
  const gia = () => ({ chat: { completions: { create: async () => {
    n += 1;
    if (n === 3) throw Object.assign(new Error('400'), { status: 400 });
    return { choices: [{ message: { content: JSON.stringify(n === 1 ? { loi: [] } : CHAM_SACH) } }] };
  } } } });
  const r = await chamBaiViet(GOI, gia);
  const c = JSON.parse(r.chu);
  assert.ok(c.diem && c.khen, 'mất cả lời chấm vì hai câu tiếng Việt cho người lớn');
  assert.ok(!c.choBoMe, 'phần phụ mất thì để trống, đừng bịa');
});

test('khung vân tay = BA khung ghép lại, và phiên bản mẫu đã tăng', () => {
  /* Dựng khung từ một mắt xích thôi thì hai mắt xích kia sửa bao nhiêu cũng không
     làm vân tay đổi — bảng so ΔC gom lẫn hai mẫu khác nhau mà không ai thấy. */
  const k = khungCham(3, true);
  assert.match(k, /CHỈ LIỆT KÊ LỖI/, 'khung thiếu mắt xích 1');
  assert.match(k, /LUẬT CHẤM/, 'khung thiếu mắt xích 2');
  assert.match(k, /cho BỐ MẸ/, 'khung thiếu mắt xích 3');
  /* Và khung KHÔNG chứa một chữ nào của bé. */
  for (const x of [GOI.de, GOI.viet, 'school', 'trường']) {
    assert.ok(!k.includes(x), `khung lọt dữ liệu của bé: ${x}`);
  }
  assert.ok(PHIEN_BAN_MAU.chamviet >= 2, 'lời dặn tách thành ba mà phiên bản vẫn là 1');
  /* Lớp khác thì khung khác — câu đầu ghi rõ lớp. */
  assert.notEqual(khungCham(3, true), khungCham(5, true));
});

test('máy chủ vẫn KHÔNG lưu gì, kể cả sau khi thêm chuỗi', () => {
  const bo = (x) => x.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
  const src = bo(readFileSync(new URL('../functions/src/chamviet.js', import.meta.url), 'utf8'));
  assert.ok(!/firestore|getFirestore|db\./i.test(src), 'máy chủ đụng tới Firestore');
  assert.ok(!/console\.(log|info|warn)/.test(src), 'máy chủ ghi nội dung ra log');
});

test('máy con đọc lanSuaLai, và GIỮ soiLoiCham làm hàng rào cuối', () => {
  const g = readFileSync(new URL('../src/mon/tienganh/lib/goiChamViet.js', import.meta.url), 'utf8');
  assert.match(g, /lanSuaLai: data\?\.lanSuaLai/, 'máy con không đọc lanSuaLai');
  assert.match(g, /soiLoiCham\(/,
    'bỏ soiLoiCham vì máy chủ đã soi — mất hàng rào cuối, mà hai tầng là CỐ Ý');
});
