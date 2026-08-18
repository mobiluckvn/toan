/**
 * CỔNG · HÌNH PHẢI ĐÚNG VỚI TỪ.
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 * Bác bắt 14-08: "hình là ghế nhưng từ lại là Desk". Đúng, và rà ra thì không chỉ
 * một chỗ. Đây là loại lỗi TỆ NHẤT của một quyển dạy từ vựng: bé sáu tuổi chưa
 * đọc được chữ, nên với bé thì HÌNH CHÍNH LÀ NGHĨA. Hình sai không phải là thiếu
 * sót — nó là dạy sai, và bé học thuộc cái sai ấy.
 *
 * Không cổng nào bắt được suốt từ đầu, vì mọi cổng cũ đều hỏi "có hình không",
 * "hình có nằm trong bộ vẽ tay không" — không cổng nào hỏi "hình này VẼ CÁI GÌ".
 * Máy không tự nhìn được tranh, nên phần ấy phải người soát. Nhưng có bốn thứ máy
 * soát được, và cả bốn đều đã hỏng thật:
 *
 *   1. mỗi từ phải CÓ hình;
 *   2. hai từ khác nhau KHÔNG được dùng chung một hình;
 *   3. câu bảo "nhìn hình" thì phải CÓ hình;
 *   4. đáp án phải là từ bé ĐÃ ĐƯỢC DẠY.
 *
 * ── PHẦN MÁY KHÔNG SOÁT ĐƯỢC ──
 * "🪑 có phải cái bàn học không" thì máy chịu. Chỗ ấy chốt bằng `docs/hinh_da_soat.md`
 * — bảng người đã nhìn tận mắt từng hình. Cổng dưới đây đòi mọi từ phải có tên
 * trong bảng ấy, nên thêm từ mới mà chưa ai nhìn là đỏ ngay.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, existsSync } from 'node:fs';

/* ⚠ SOI CẢ BA QUYỂN, và đây là chỗ cổng này từng hỏng NẶNG NHẤT.
 *
 * Bản đầu mở đúng thư mục `ta1` rồi chốt `assert.equal(tep.length, 16)`. Con số 16
 * trông như một phép chống-glob-rỗng nghiêm túc, nên không ai đọc lại nó khi thêm
 * quyển — và suốt hai quyển sau, tám phép dưới đây KHÔNG CHẠY LẤY MỘT LẦN.
 *
 * Giá phải trả, đếm được ngày 18-08 khi rà lớp 3: 60 câu "bấm vào HÌNH đúng" mà
 * bốn nút đều không có hình · 15 câu sát hạch "nhìn hình rồi đúng/sai" mà không có
 * hình · `desk` và `table` lại là 🪑 CHAIR — đúng cái lỗi bác bắt ở lớp 1, quay về
 * nguyên văn ở quyển thứ ba. Tất cả đều là thứ phép 1·2·3 bắt được ngay.
 *
 * Nay danh sách quyển suy từ ĐĨA, và chốt "có tệp để mà soi" chứ không chốt một con
 * số — thêm quyển thứ tư là nó tự soi theo. Mỗi quyển một sổ soát riêng.
 */
const QUYEN = ['ta1', 'ta2', 'ta3']
  .map((q) => ({ q, url: new URL(`../public/content/${q}/`, import.meta.url) }))
  .map(({ q, url }) => ({
    q,
    url,
    tep: existsSync(url) ? readdirSync(url).filter((f) => /^DL_.*\.json$/.test(f)).sort() : [],
  }))
  .filter((x) => x.tep.length);

assert.ok(QUYEN.length >= 2, `phải soi từ hai quyển trở lên, đang thấy ${QUYEN.length}`);
const BAI = QUYEN.flatMap(
  ({ q, url, tep }) => tep.map((f) => ({
    ...JSON.parse(readFileSync(new URL(f, url), 'utf8')), _quyen: q,
  })));
assert.ok(BAI.length > 40, `phải soi hơn 40 bài, đang thấy ${BAI.length}`);

const mucHoi = (b) => [
  ...b.assessment.items.map((x) => ({ ...x, _o: 'sát hạch' })),
  ...b.practice.pools.standard.map((x) => ({ ...x, _o: 'luyện tập' })),
];
const coHinh = (x) => !!(x.anh || x.anhVe);

test('1 · mỗi từ mới đều CÓ hình, trừ từ CỐ Ý không vẽ', () => {
  /* Lớp 1·2 từ nào cũng vẽ được. Lớp 3 thì 59/204 từ là `hello` · `fine` · `my` ·
     `this` — không vẽ được, và CỐ TÌM một emoji cho chúng chính là cách đẻ ra
     `desk` → 🪑. Chúng khai `hinh._khong_ve` KÈM LÝ DO ở phần bù, nên ở đây chỉ
     hỏi: từ nào không có hình mà cũng không khai lý do? */
  /* Hai kiểu được phép không có hình, và cả hai đều khai ở BẢN CHUẨN:
       `khong_ve`  — từ trừu tượng, có ghi lý do ở phần bù
       `ten_rieng` — `Ben` · `Ms Hoa`: vẽ một cái tên thì vẽ ra ai? */
  const mienHinh = new Map(QUYEN.map(({ q }) => {
    const c = JSON.parse(readFileSync(
      new URL(`../../data/tienganh/chuan_lop${q.slice(2)}.json`, import.meta.url), 'utf8'));
    return [q, new Set(c.unit.flatMap((u) => u.tu
      .filter((t) => t.khong_ve || t.ten_rieng).map((t) => t.tu)))];
  }));
  const xau = [];
  for (const b of BAI) {
    const co = new Set((b.hinhTu || []).filter((h) => h.hinh || h.ve).map((h) => h.tu));
    for (const t of b.knowledgeCore.vocabulary || []) {
      if (!co.has(t.tu) && !mienHinh.get(b._quyen)?.has(t.tu)) {
        xau.push(`${b.id}: từ "${t.tu}" không có hình mà cũng không khai khong_ve/ten_rieng`);
      }
    }
  }
  assert.deepEqual(xau, [], `${xau.length} từ không hình mà không ai giải thích`);
});

test('2 · hai từ KHÁC NHAU không được dùng chung một hình', () => {
  /* Đã hỏng thật: `ball` (Unit 1) và `football` (Unit 15) cùng dùng ⚽. Bé học
     Unit 1 thì ⚽ nghĩa là "ball"; tới Unit 15 vẫn cái hình ấy lại là "football".
     Với bé chưa đọc chữ thì đó là hai bài dạy ngược nhau về cùng một bức tranh.
     Soi CẢ QUYỂN chứ không từng bài — hai bài cách nhau 14 unit vẫn là một quyển. */
  /* So TRONG TỪNG QUYỂN: bé học một quyển một lúc, và `table` của lớp 2 với
     `table` của lớp 3 dùng chung nét vẽ là ĐÚNG — một vật thì một hình.

     Ba cặp được tha, khai đích danh: danh từ và hoạt động dùng chính vật ấy
     (`kite` / `flying a kite`). Khai đích danh chứ không nới luật, để cặp thứ tư
     mọc ra thì vẫn đỏ. */
  const THA = new Set(['badminton|playing badminton', 'basketball|playing basketball',
    'flying a kite|kite']);
  const xau = [];
  for (const { q } of QUYEN) {
    const cua = new Map();
    for (const b of BAI.filter((x) => x._quyen === q)) {
      for (const h of b.hinhTu || []) {
        const khoa = h.ve ? `ve:${h.ve}` : `hinh:${h.hinh}`;
        if (!h.ve && !h.hinh) continue;
        const cu = cua.get(khoa);
        if (cu && cu.tu !== h.tu && !THA.has([cu.tu, h.tu].sort().join('|'))) {
          xau.push(`${q} · hình ${khoa} dùng cho CẢ "${cu.tu}" (${cu.bai}) lẫn "${h.tu}" (${b.id})`);
        }
        cua.set(khoa, { tu: h.tu, bai: b.id });
      }
    }
  }
  assert.deepEqual(xau, [], `${xau.length} hình bị hai từ khác nhau dùng chung`);
});

test('3 · câu bảo "nhìn hình" thì phải CÓ hình', () => {
  /* 15 câu từng bảo bé nhìn hình mà không có hình nào. Bốn câu của Unit 16 là
     nặng nhất: "How many windows can you see? - I can see ___" với đáp án
     six/one/two/three và KHÔNG có hình — bé không thể nào làm đúng trừ khi đoán
     may, mà bốn câu ấy còn giống hệt nhau từng chữ. */
  const xau = [];
  for (const b of BAI) {
    for (const x of mucHoi(b)) {
      const bao = /hìn hình/i.test(x.text || '') || x.nhinNghe;
      if (bao && !coHinh(x)) xau.push(`${b.id} · ${x._o} ${x.id}: "${(x.text || '').slice(0, 55)}"`);
    }
  }
  assert.deepEqual(xau, [], `${xau.length} câu bảo nhìn hình mà không có hình`);
});

test('4 · câu bảo "điền chỗ trống" thì phải CÓ chỗ trống', () => {
  /* Máy sinh xoá từ khỏi câu bằng `replace` phân biệt hoa/thường, nên "two" không
     khớp "Two." và chỗ trống không bao giờ được tạo — đề in nguyên đáp án ra rồi
     hỏi lại chính nó. */
  const xau = [];
  for (const b of BAI) {
    for (const x of mucHoi(b)) {
      if (/chỗ trống/.test(x.text || '') && !(x.text || '').includes('___')) {
        xau.push(`${b.id} · ${x._o} ${x.id}: "${x.text}" → đáp án ${JSON.stringify(x.answerKey)}`);
      }
    }
  }
  assert.deepEqual(xau, [], `${xau.length} câu điền chỗ trống mà không có chỗ trống`);
});

test('5 · đáp án phải là từ bé ĐÃ ĐƯỢC DẠY', () => {
  /* Unit 6 từng có câu đáp án là "blue", trong khi CẢ QUYỂN không bài nào dạy
     "blue" — dò đủ 16 bài. Từ phụ (số đếm, màu) sinh ra để ĐIỀN VÀO KHUNG cho có
     câu mà luyện, không phải để làm đáp án bé phải nhớ.
     Nới ra cả quyển chứ không bó trong một bài: bé Unit 15 nhớ từ Unit 8 là chuyện
     thường, mà "blue" thì vẫn không ở đâu cả. */
  /* Vốn từ dựng theo TỪNG QUYỂN, và lấy thẳng từ BẢN CHUẨN chứ không đoán:
       `tu` · `so_it` · `so_nhieu` · `dang_ing`  — mọi DẠNG sách dùng
       `nghia`                                   — đáp án của câu "nghe → chọn nghĩa"
     Đoán dạng biến đổi bằng tiền tố (`d.startsWith(goc)`) thì `drive` → `driving`
     trượt (mất chữ e), và cổng báo oan bốn câu đúng của lớp 2. */
  const von = new Map(QUYEN.map(({ q }) => {
    const c = JSON.parse(readFileSync(
      new URL(`../../data/tienganh/chuan_lop${q.slice(2)}.json`, import.meta.url), 'utf8'));
    const bo = new Set();
    for (const u of c.unit) {
      for (const t of u.tu) {
        for (const x of [t.tu, t.so_it, t.so_nhieu, t.dang_ing, t.nghia]) if (x) bo.add(x);
      }
    }
    for (const nhom of Object.values(c.them || {})) {
      for (const m of nhom.muc || []) bo.add(typeof m === 'string' ? m : m.word);
    }
    return [q, bo];
  }));
  const tenRieng = /^[A-Z]/;                 // Bill · Mai — tên người, không phải từ vựng
  const xau = [];
  for (const b of BAI) {
    /* Câu của CHÍNH bài này — để nhận ra dạng biến đổi. */
    const cauBai = [
      ...(b.knowledgeCore.mauCauDs || []).map((c) => c.cau),
      ...(b.knowledgeCore.canonicalExamples || []),
    ].join(' ').toLowerCase();
    const bo = von.get(b._quyen);
    const daDay = [...bo];
    for (const x of mucHoi(b)) {
      const d = x.answerKey?.choice;
      if (!d || tenRieng.test(d)) continue;
      if (bo.has(d)) continue;
      /* DẠNG BIẾN ĐỔI của một từ có dạy vẫn hợp lệ: `run` → "running",
         `window` → "windows". Đó đúng là dạng câu của sách dùng, và cũng là dạng
         bé phải nói ra. Đòi trùng khít từ điển thì chặn nhầm cả hai — cổng bắt
         được thật lúc đang sửa chính đợt này.
         Vẫn phải có GỐC được dạy VÀ dạng ấy có mặt trong câu của bài, nên "blue"
         (không gốc nào, dù có trong một câu ví dụ) thì không lọt. */
      const goc = daDay.find((t) => d.length > t.length && d.startsWith(t));
      if (goc && cauBai.includes(d.toLowerCase())) continue;
      xau.push(`${b.id} · ${x._o} ${x.id}: đáp án "${d}" — cả quyển không dạy`);
    }
  }
  assert.deepEqual(xau, [], `${xau.length} câu có đáp án là từ chưa dạy`);
});

test('6 · câu ĐÚNG/SAI: đúng thì hình phải khớp, sai thì hình phải lệch', () => {
  /* Khuôn của phần sát hạch: Q1/Q3/Q5 ghép ĐÚNG (đáp án true), Q2/Q4 ghép LỆCH có
     chủ ý (đáp án false). Lệch có chủ ý là bài tập tốt — nhưng nếu một câu `true`
     mà hình lại không phải của từ ấy thì bé được dạy rằng cái sai là đúng. Đó
     chính là hình dạng của lỗi `desk` + 🪑. */
  const xau = [];
  for (const b of BAI) {
    const nguoc = new Map();
    for (const h of b.hinhTu || []) {
      nguoc.set(h.ve ? `ve:${h.ve}` : `hinh:${h.hinh}`, h.tu);
    }
    for (const x of mucHoi(b)) {
      if (x.format !== 'tf' || !coHinh(x)) continue;
      const m = /^tu_(.+)$/.exec(x.am || '');
      if (!m) continue;
      /* Mã clip biến MỌI ký tự không phải chữ-số thành `_`, nên `yo-yo` → `yo_yo`.
         So thẳng chuỗi thì "yo yo" ≠ "yo-yo" và cổng báo oan. Chuẩn hoá cả hai bên. */
      const chuan_ = (t) => String(t || '').toLowerCase().replace(/[^a-z0-9]+/g, '');
      const tu = m[1];
      const dangVe = nguoc.get(x.anhVe ? `ve:${x.anhVe}` : `hinh:${x.anh}`);
      const khop = chuan_(dangVe) === chuan_(tu);
      if (x.answerKey?.value === true && !khop) {
        xau.push(`${b.id} ${x.id}: nghe "${tu}", hiện hình của "${dangVe}", mà đáp án là ĐÚNG`);
      }
      if (x.answerKey?.value === false && khop) {
        xau.push(`${b.id} ${x.id}: nghe "${tu}", hiện đúng hình của nó, mà đáp án là SAI`);
      }
      /* Câu SAI phải gọi đúng tên vật đang hiện — "SAI, đó là dog" mà hình lại là
         cái cửa thì bé càng rối hơn trước khi làm bài. */
      if (x.answerKey?.value === false && dangVe && !(x.solutionNarrative || '').includes(dangVe)) {
        xau.push(`${b.id} ${x.id}: lời giải không gọi tên "${dangVe}" đang hiện`);
      }
    }
  }
  assert.deepEqual(xau, [], `${xau.length} câu đúng/sai ghép hình lệch luật`);
});

test('7 · ĐỀ ÔN TẬP dùng đúng hình của bài, không giữ bản cũ', () => {
  /* ⚠ Đã lọt thật trong chính đợt soát này. `ontap.json` là tệp SINH RA từ 16 bài,
     nhưng nó không tự dựng lại khi bài đổi. Sửa xong bốn hình, chạy lại bộ sinh
     bài, mở app thấy đúng — mà đề ôn tập vẫn giữ ⚽ cho `ball` và 🪑 cho `desk`.
     Bé học "cái bàn" rồi đi thi lại gặp cái ghế: tệ hơn cả lúc chưa sửa, vì nay
     hai chỗ trong cùng một quyển dạy hai nghĩa khác nhau.
     Cổng cũ không bắt được vì nó chỉ soi `DL_TA1_B*.json`. */
  const xau = [];
  for (const { q, url } of QUYEN) {
  const on = existsSync(new URL('ontap.json', url))
    ? JSON.parse(readFileSync(new URL('ontap.json', url), 'utf8')) : [];
  const chuan = new Map();
  for (const b of BAI.filter((x) => x._quyen === q)) {
    for (const h of b.hinhTu || []) chuan.set(h.tu, { hinh: h.hinh || null, ve: h.ve || null });
  }
  const so = (tu, hinh, ve, o) => {
    const c = chuan.get(tu);
    if (!c) return;
    if ((hinh || null) !== c.hinh || (ve || null) !== c.ve) {
      xau.push(`${q} · ${o} · "${tu}": đề dùng ${ve || hinh}, bài dùng ${c.ve || c.hinh}`);
    }
  };
  for (const k of on) {
    for (const c of k.cau || []) {
      for (const tu of Object.keys(c.hinhNut || {})) {
        so(tu, c.hinhNut[tu], (c.veNut || {})[tu], `kỳ ${k.so} · ${c.id}`);
      }
      /* Câu đúng/sai: chỉ soi câu ĐÁP ÚNG (ghép đúng). Câu ghép lệch là cố ý. */
      const m = /^tu_(.+)$/.exec(c.am || '');
      if (m && c.answerKey?.value === true) {
        so(m[1].replace(/_/g, ' '), c.anh, c.anhVe, `kỳ ${k.so} · ${c.id}`);
      }
    }
  }
  }
  assert.deepEqual(xau, [], `${xau.length} chỗ đề ôn tập lệch hình với bài học`);
});

test('8 · MỌI từ phải có trong bảng NGƯỜI ĐÃ SOÁT tận mắt', () => {
  /* Bốn phép trên đều là phép hình thức: chúng chứng minh được "có hình", "không
     trùng hình", nhưng KHÔNG chứng minh được "🪑 có phải cái bàn học không". Máy
     không nhìn tranh. Chỗ ấy chỉ người soát được, nên phải có một bảng ghi lại ai
     đã nhìn cái gì — và cổng đòi bảng ấy phủ hết mọi từ.
     Thêm từ mới mà quên nhìn hình của nó thì đỏ ngay tại đây. */
  /* MỖI QUYỂN MỘT SỔ. Dùng chung một sổ thì từ trùng tên giữa hai quyển (`cat` ·
     `table` · `eleven`) tự "đã soát" ở quyển sau, trong khi hình của nó có thể
     khác hẳn — lớp 1 dùng 🐱 MẶT MÈO, lớp 3 dùng 🐈 CẢ CON. */
  const SO = { ta1: 'hinh_da_soat.md', ta2: 'hinh_da_soat_lop2.md', ta3: 'hinh_da_soat_lop3.md' };
  const daSoat = Object.fromEntries(QUYEN.map(({ q }) => {
    const bang = readFileSync(new URL(`../../docs/${SO[q]}`, import.meta.url), 'utf8');
    return [q, new Set([...bang.matchAll(/^\|\s*`([^`]+)`\s*\|/gm)].map((m) => m[1]))];
  }));
  const xau = [];
  for (const b of BAI) {
    for (const t of b.knowledgeCore.vocabulary || []) {
      if (!daSoat[b._quyen].has(t.tu)) {
        xau.push(`${b.id} · "${t.tu}" chưa có trong ${SO[b._quyen]}`);
      }
    }
  }
  assert.deepEqual(xau, [], `${xau.length} từ chưa ai nhìn hình tận mắt`);
});
