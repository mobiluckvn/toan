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
import { soiBaiViet, loiDanCham, TOI_DA_CHU_BAI_VIET } from '../functions/src/chamviet.js';

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
  const man = readFileSync(new URL('../src/mon/tienganh/components/VietBai.jsx',
    import.meta.url), 'utf8');
  assert.match(man, /Máy chấm \(AI\)/, 'màn lời chấm phải nói rõ ai chấm');

  const trang = readFileSync(new URL('../src/mon/tienganh/components/ManTiengAnh.jsx',
    import.meta.url), 'utf8');
  assert.match(trang, /điểm \(máy chấm\)/, 'thẻ trên trang chính phải nói rõ ai chấm');

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
      assert.ok((k.vonTu || []).some((v) => /kite|yo-yo|kitten|bear/.test(v.tu)),
        `${k.id}: bảng từ không có vật nào của tranh`);

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
