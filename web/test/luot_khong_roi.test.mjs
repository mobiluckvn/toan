/**
 * CỔNG: từ lượt thứ hai trở đi vẫn phải lên được máy chủ.
 *
 * ── LỖI NÀY ĐÃ ĂN MẤT ~90% DỮ LIỆU HỌC, VÀ MỌI CỔNG ĐỀU XANH ──
 * Tìm ra 23-08-2026 khi soi Firestore bằng khoá quản trị: cả dự án có ĐÚNG 2 bản
 * ghi `attempts` cho hai buổi học, mỗi buổi khoảng mười lượt.
 *
 * Dây chuyền hỏng:
 *   · mỗi lượt, màn hình dựng LẠI nhật ký cả phiên rồi gửi đi (chủ ý: gửi lại
 *     nhiều lần cũng không sinh dòng trùng, vì mã lượt dựng lại ra đúng mã cũ);
 *   · nhưng `firestore.rules` cho `attempts` là `allow update, delete: if false`
 *     — nhật ký BẤT BIẾN, ghi đè bản ghi đã có là `update`, và bị cấm;
 *   · `writeBatch` NGUYÊN KHỐI: một lệnh trong lô bị từ chối thì CẢ LÔ rơi.
 *   ⇒ lượt 1 lên được, lô của lượt 2 kèm theo lượt 1 nên rơi, và mãi mãi như thế.
 *
 * ── VÌ SAO CỔNG CŨ KHÔNG BẮT ĐƯỢC ──
 * `luat_firestore` có thử `attempts`, nhưng chỉ thử GHI MỘT BẢN GHI. Không phép
 * nào gửi tới lượt thứ hai, nên không phép nào chạm vào chỗ hỏng. Cùng họ với
 * mọi lỗi "chỗ nối" khác trong kho này: từng mảnh đều đúng.
 *
 * Nên cổng này KHÔNG đọc mã và KHÔNG thử luật. Nó dựng một máy chủ giả có đúng
 * MỘT tính chất của máy chủ thật — cấm ghi đè, và rơi cả lô — rồi chạy đúng dòng
 * đời thật: bé trả lời 5 lượt liên tiếp, mỗi lượt gọi `luuSuKien` một lần.
 */

import {
  dungSuKien, xepHang, dayHangDoi, docHangDoi, docDaGui, themDaGui,
} from '../src/mon/tienganh/lib/suKien.js';

let pass = 0; let fail = 0;
const ok = (dieu, ten, them = '') => {
  if (dieu) { pass += 1; } else { fail += 1; console.log(`  ✗ ${ten}${them ? ` — ${them}` : ''}`); }
};

/** localStorage giả — đủ dùng cho `getItem`/`setItem`. */
const khoMoi = () => {
  const m = new Map();
  return { getItem: (k) => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, String(v)) };
};

/**
 * MÁY CHỦ GIẢ mang đúng hai tính chất đã đo được trên bộ giả lập hôm nay:
 *   ① mã đã có thì lệnh ghi bị TỪ CHỐI (không phải ghi đè êm);
 *   ② một lệnh hỏng thì CẢ LÔ rơi, không bản ghi nào trong lô được lưu.
 */
const mayChuGia = () => {
  const kho = new Map();
  const nhan = async (lo) => {
    if (lo.some((r) => kho.has(r.id))) {
      /* ⚠ MANG ĐÚNG MÃ LỖI CỦA FIRESTORE THẬT. Bản đầu của máy chủ giả ném một
         `Error` trần, và vì thế nó không phân biệt được "luật từ chối" với "mất
         mạng" — hai chuyện phải xử lý ngược nhau. Máy chủ giả mà không giống chỗ
         quan trọng nhất thì cổng chỉ thử chính nó. Đo trên bộ giả lập thật hôm
         nay: SDK ném `FirebaseError` với `code === 'permission-denied'`. */
      const e = new Error('PERMISSION_DENIED: attempts cấm ghi đè');
      e.code = 'permission-denied';
      throw e;
    }
    lo.forEach((r) => kho.set(r.id, r));
  };
  return { nhan, kho };
};

/** Một lượt bé trả lời, đúng như `ghiLuot` + `luuSuKien` làm. */
const motLuot = async (nhatKy, may, kho, e) => {
  nhatKy.push(e);
  const ds = dungSuKien({
    learnerId: 'be1', maPhien: 'p1', microId: 'DL:TA3.B00', viec: nhatKy, quyen: 'ta3',
  });
  xepHang(ds, kho);
  return dayHangDoi(may.nhan, kho);
};

/* ── 1. Năm lượt liên tiếp thì phải có đủ NĂM bản ghi trên máy chủ ────────── */
{
  const kho = khoMoi(); const may = mayChuGia(); const nhatKy = [];
  for (let i = 0; i < 5; i += 1) {
    await motLuot(nhatKy, may, kho, {
      itemId: `C${i + 1}`, maNut: 'v_g3_ustarter_one', ok: i % 2 === 0,
      tries: 1, hintsUsed: 0, ms: 1000 + i, phase: 'practice', khiNao: 100 + i,
    });
  }
  ok(may.kho.size === 5, 'bé làm 5 lượt thì máy chủ nhận đủ 5 bản ghi',
    `chỉ nhận ${may.kho.size} — từ lượt thứ ${may.kho.size + 1} là RƠI SẠCH`);
  ok(docHangDoi(kho).length === 0, 'gửi xong thì hàng đợi tại máy rỗng',
    `còn ${docHangDoi(kho).length} bản ghi kẹt lại`);
  ok(docDaGui(kho).size === 5, 'sổ "đã gửi" nhớ đủ 5 mã');
}

/* ── 2. Trả lời LẠI cùng một câu cũng phải ghi thành lượt riêng ───────────── */
{
  const kho = khoMoi(); const may = mayChuGia(); const nhatKy = [];
  for (let lan = 1; lan <= 3; lan += 1) {
    await motLuot(nhatKy, may, kho, {
      itemId: 'C1', maNut: 'v_g3_ustarter_one', ok: lan === 3, tries: lan,
      hintsUsed: 0, ms: 900, phase: 'practice', khiNao: 200 + lan,
    });
  }
  ok(may.kho.size === 3, 'sai · sai · đúng trên CÙNG một câu ra 3 bản ghi',
    `ra ${may.kho.size} — mất chính chuỗi mà BKT cần để hạ rồi nâng P(L)`);
  const seq = [...may.kho.keys()].map((k) => k.split('_').pop());
  ok(new Set(seq).size === 3, 'ba bản ghi mang ba số thứ tự KHÁC nhau', `seq = ${seq}`);
}

/* ── 3. Mất mạng giữa chừng thì GIỮ, nối mạng lại thì gửi nốt ─────────────── */
{
  const kho = khoMoi(); const may = mayChuGia(); const nhatKy = [];
  await motLuot(nhatKy, may, kho, {
    itemId: 'C1', maNut: 'n1', ok: true, tries: 1, hintsUsed: 0, ms: 1, phase: 'practice', khiNao: 1,
  });
  /* Lượt 2 và 3 gặp mạng hỏng — máy chủ ném vì lý do KHÁC (không phải trùng mã). */
  const hong = async () => { throw new Error('mạng hỏng'); };
  for (const it of ['C2', 'C3']) {
    nhatKy.push({ itemId: it, maNut: 'n1', ok: true, tries: 1, hintsUsed: 0, ms: 1, phase: 'practice', khiNao: 1 });
    const ds = dungSuKien({ learnerId: 'be1', maPhien: 'p1', microId: 'DL:TA3.B00', viec: nhatKy, quyen: 'ta3' });
    xepHang(ds, kho);
    await dayHangDoi(hong, kho);
  }
  ok(docHangDoi(kho).length === 2, 'mất mạng thì 2 lượt chưa gửi NẰM LẠI hàng đợi',
    `hàng đợi có ${docHangDoi(kho).length}`);
  ok(may.kho.size === 1, 'và máy chủ vẫn chỉ có lượt đầu');
  const r = await dayHangDoi(may.nhan, kho);
  ok(may.kho.size === 3, 'nối mạng lại thì đẩy nốt, đủ 3 bản ghi',
    `máy chủ có ${may.kho.size}; daGui=${r.daGui}`);
  ok(docHangDoi(kho).length === 0, 'và hàng đợi sạch');
}

/* ── 4. MÁY CHỦ GIẢ CÓ TÁI DỰNG ĐƯỢC LỖI GỐC KHÔNG ───────────────────────────
 *
 * Một cổng dựng trên máy chủ giả chỉ đáng tin nếu máy chủ giả ấy tái dựng được
 * ĐÚNG cái lỗi đã xảy ra thật. Nên phép này chạy lại BẢN CŨ của hàm đẩy — chép
 * nguyên vào đây, không gọi mã hiện tại — và đòi nó cho ra đúng triệu chứng đã
 * đo trên máy chủ thật: mỗi phiên còn ĐÚNG MỘT bản ghi.
 *
 * ⚠ Phép này đỏ thì đừng vội sửa mã sản phẩm: nhiều khả năng máy chủ giả đã trôi
 *    xa máy chủ thật, và khi ấy MỌI phép khác trong tệp này đều mất giá trị.
 */
{
  const kho = khoMoi(); const may = mayChuGia(); const nhatKy = [];
  /* BẢN CŨ: xếp hàng không lọc, đẩy cả lô, hỏng thì giữ nguyên — không thử lẻ. */
  const dayCu = async () => {
    const q = docHangDoi(kho);
    if (!q.length) return;
    try { await may.nhan(q); kho.setItem('ttd5.queueTA.v1', '[]'); } catch { /* giữ nguyên */ }
  };
  for (let i = 0; i < 4; i += 1) {
    nhatKy.push({ itemId: `C${i + 1}`, maNut: 'n1', ok: true, tries: 1, hintsUsed: 0, ms: 1, phase: 'practice', khiNao: i });
    const ds = dungSuKien({ learnerId: 'be1', maPhien: 'p1', microId: 'DL:TA3.B00', viec: nhatKy, quyen: 'ta3' });
    const q = docHangDoi(kho);
    const m = new Map(q.map((r) => [r.id, r]));
    for (const r of ds) m.set(r.id, r);
    kho.setItem('ttd5.queueTA.v1', JSON.stringify([...m.values()]));
    await dayCu();
  }
  ok(may.kho.size === 1,
    'máy chủ giả tái dựng đúng lỗi gốc: bản cũ chỉ đưa lên được 1 lượt',
    `ra ${may.kho.size} — máy chủ giả đã trôi khỏi máy chủ thật, mọi phép trên mất giá trị`);
}

/* ── 4b. HÀNG ĐỢI ĐANG NHIỄM ĐỘC PHẢI TỰ GỠ ĐƯỢC ──────────────────────────────
 *
 * Sổ "đã gửi" chỉ chặn từ nay. Máy nào đã mang sẵn hàng đợi có bản ghi nằm trên
 * máy chủ thì lô nào cũng chết, mãi mãi. Đo trên máy thật 23-08-2026: hai bé, 12
 * và 14 bản ghi kẹt cứng — và bản vá đầu tiên KHÔNG gỡ được, buổi đi thử sau khi
 * deploy ra ĐÚNG 0 bản ghi mới. Phép này khoá chỗ đó.
 */
{
  const kho = khoMoi(); const may = mayChuGia();
  /* Máy chủ đã có r0 từ phiên trước; hàng đợi tại máy vẫn ôm cả r0 lẫn r1, r2. */
  const nhatKy = [
    { itemId: 'C1', maNut: 'n1', ok: false, tries: 1, hintsUsed: 0, ms: 1, phase: 'practice', khiNao: 1 },
    { itemId: 'C2', maNut: 'n1', ok: true, tries: 1, hintsUsed: 0, ms: 1, phase: 'practice', khiNao: 2 },
    { itemId: 'C3', maNut: 'n1', ok: true, tries: 1, hintsUsed: 0, ms: 1, phase: 'practice', khiNao: 3 },
  ];
  const ds = dungSuKien({ learnerId: 'be1', maPhien: 'p9', microId: 'DL:TA3.B00', viec: nhatKy, quyen: 'ta3' });
  await may.nhan([ds[0]]);                       // r0 đã lên máy chủ từ trước
  kho.setItem('ttd5.queueTA.v1', JSON.stringify(ds));  // hàng đợi cũ, chưa có sổ "đã gửi"
  ok(may.kho.size === 1, 'tiền đề: máy chủ có sẵn 1 bản ghi');
  ok(docHangDoi(kho).length === 3, 'tiền đề: hàng đợi ôm cả 3, kể cả bản đã lên');

  const r = await dayHangDoi(may.nhan, kho);
  ok(may.kho.size === 3, 'GỠ ĐỘC: hai bản ghi còn lại lên được máy chủ',
    `máy chủ có ${may.kho.size} — hàng đợi vẫn kẹt`);
  ok(r.boQua === 1, 'và đếm đúng 1 bản ghi bị bỏ vì đã có sẵn', `boQua=${r.boQua}`);
  ok(docHangDoi(kho).length === 0, 'hàng đợi sạch sau khi gỡ');
}

/* ── 4c. MẤT MẠNG THÌ KHÔNG ĐƯỢC BỎ BẢN GHI NÀO ──────────────────────────────
 *
 * Phép gỡ độc ở trên bỏ bản ghi khi máy chủ TỪ CHỐI. Nếu nó cũng bỏ khi MẤT MẠNG
 * thì công học của bé bay sạch — đúng thứ cả cơ chế hàng đợi sinh ra để tránh.
 * Phân biệt bằng MÃ LỖI, và phép này canh đúng chỗ phân biệt ấy.
 */
{
  const kho = khoMoi();
  const nhatKy = [
    { itemId: 'C1', maNut: 'n1', ok: true, tries: 1, hintsUsed: 0, ms: 1, phase: 'practice', khiNao: 1 },
    { itemId: 'C2', maNut: 'n1', ok: true, tries: 1, hintsUsed: 0, ms: 1, phase: 'practice', khiNao: 2 },
  ];
  const ds = dungSuKien({ learnerId: 'be1', maPhien: 'p8', microId: 'DL:TA3.B00', viec: nhatKy, quyen: 'ta3' });
  kho.setItem('ttd5.queueTA.v1', JSON.stringify(ds));
  const rot = async () => { const e = new Error('mất mạng'); e.code = 'unavailable'; throw e; };
  const r = await dayHangDoi(rot, kho);
  ok(docHangDoi(kho).length === 2, 'mất mạng: GIỮ NGUYÊN cả 2 bản ghi',
    `còn ${docHangDoi(kho).length} — bỏ mất ${2 - docHangDoi(kho).length}`);
  ok((r.boQua || 0) === 0, 'và KHÔNG bỏ qua bản ghi nào', `boQua=${r.boQua}`);
  ok(docDaGui(kho).size === 0, 'không đánh dấu nhầm là đã gửi');
}

/* ── 5. MÔN TOÁN cũng phải chịu đúng phép ấy ──────────────────────────────────
 *
 * Toán hiện chưa mất bản ghi nào (43/43 phiên còn đủ, soi máy chủ 23-08). Nhưng
 * mọi bản ghi của một phiên mang ĐÚNG MỘT dấu `serverTs` — cả phiên lên bằng một
 * lô, tức những lần đẩy giữa chừng đều đã hỏng sẵn. Nó sống nhờ MAY: chưa lô nào
 * lọt sớm. Phép này khoá cái may ấy lại thành cái chắc.
 */
{
  const { buildAttempts, enqueue, flushQueue, readQueue, readSent } =
    await import('../src/mon/toan/lib/sync.js');
  const kho = khoMoi(); const may = mayChuGia(); const nhatKy = [];
  for (let i = 0; i < 5; i += 1) {
    nhatKy.push({ itemId: `A${i + 1}`, phase: 'practice', ok: true, khiNao: 10 + i });
    const recs = buildAttempts({
      learnerId: 'be1', sessionId: 's1', microId: 'DL:KSN2.B02', bktUnit: 'u1',
      dangBai: null, events: nhatKy,
    });
    enqueue(recs, kho);
    await flushQueue(may.nhan, kho);
  }
  ok(may.kho.size === 5, 'TOÁN: 5 lượt thì máy chủ nhận đủ 5 bản ghi',
    `chỉ nhận ${may.kho.size}`);
  ok(readQueue(kho).length === 0, 'TOÁN: hàng đợi rỗng sau khi gửi xong');
  ok(readSent(kho).size === 5, 'TOÁN: sổ "đã gửi" nhớ đủ 5 mã');

  /* Và gỡ độc: hàng đợi cũ ôm bản ghi đã lên thì phải tự tách ra được. */
  const kho2 = khoMoi(); const may2 = mayChuGia();
  const ev = [0, 1, 2].map((i) => ({ itemId: `A${i}`, phase: 'practice', ok: true, khiNao: i }));
  const recs = buildAttempts({
    learnerId: 'be1', sessionId: 's2', microId: 'DL:KSN2.B02', bktUnit: 'u1',
    dangBai: null, events: ev,
  });
  await may2.nhan([recs[0]]);
  kho2.setItem('ttd5.queue.v1', JSON.stringify(recs));
  const r2 = await flushQueue(may2.nhan, kho2);
  ok(may2.kho.size === 3, 'TOÁN gỡ độc: 2 bản ghi còn lại lên được',
    `máy chủ có ${may2.kho.size}`);
  ok(r2.skipped === 1, 'TOÁN: đếm đúng 1 bản ghi bỏ vì đã có', `skipped=${r2.skipped}`);
  ok(readQueue(kho2).length === 0, 'TOÁN: hàng đợi sạch');
}

console.log(`${pass} PASS · ${fail} FAIL`);
process.exit(fail ? 1 : 0);
