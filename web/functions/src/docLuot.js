/**
 * ĐỌC HẾT NHẬT KÝ LƯỢT TỪ MỘT MỐC THỜI GIAN — phân trang bằng CON TRỎ (ts, mã).
 *
 * Tách khỏi `index.js` vì đúng mươi dòng này đã sai ba lần, và cả ba đều là loại
 * sai mà `node --check`, bản dựng và 105 cổng đều không thấy:
 *
 *   1. Dùng `eachDoc` (sắp theo `__name__`) với phép lọc `ts >= …`. Firestore đòi
 *      trường bất đẳng thức đứng ĐẦU thứ tự sắp, nên câu truy vấn ném lúc CHẠY.
 *      Hàm nền chạy hằng tuần, nên lỗi ấy nằm im trong nhật ký máy chủ.
 *   2. Lọc trùng bằng `(bé, nút, ts)`. Một loạt lượt gửi lên cùng lúc mang đúng một
 *      mốc, nên phép lọc ấy NUỐT lượt thật — im lặng, chỉ làm các con số nhỏ đi.
 *   3. Phân trang bằng riêng `ts`, nhích mốc khi cả trang cùng một mốc. Quá một
 *      trang lượt chung một mốc là mất phần dư. Cổng `docluot.test.mjs` bắt được
 *      đúng chỗ này: 700 lượt chung một mốc thì đọc ra 500.
 *
 * Nay phân trang bằng CON TRỎ `(ts, mã tài liệu)` — đúng cặp mà Firestore sắp theo
 * khi `orderBy('ts').orderBy('__name__')`. Cặp ấy là duy nhất với mọi tài liệu, nên
 * không còn mốc trùng, không còn trường hợp riêng, và không cần lọc trùng.
 *
 * `layTrang(sau, soLuong)` là đường nối duy nhất ra ngoài: `sau` là `null` ở trang
 * đầu, rồi là `{ ts, id }` của tài liệu cuối trang trước. Nhờ nó mà cổng dựng lại
 * được đúng các cái bẫy trên bằng một mảng trong bộ nhớ, không cần bộ giả lập.
 */

export const TRANG = 500;

export async function docLuotTuMoc(layTrang, { trang = TRANG, tran = 500000 } = {}) {
  const ra = [];
  let sau = null;

  for (;;) {
    const ds = await layTrang(sau, trang);
    if (!ds || !ds.length) break;

    for (const d of ds) {
      if (!d) continue;
      ra.push(d);
      /* Trần cứng: thà có số liệu của ngần này lượt gần nhất còn hơn hàm nền chạm
         trần 540 giây rồi KHÔNG ghi được dòng nào. */
      if (ra.length >= tran) return ra;
    }

    if (ds.length < trang) break;
    const cuoi = ds[ds.length - 1];
    sau = { ts: cuoi.ts, id: cuoi.id };
  }

  return ra;
}

/**
 * So hai tài liệu theo đúng thứ tự Firestore sắp khi `orderBy('ts').orderBy('__name__')`.
 * Dùng cho kho giả trong cổng; để ở đây để cổng và bản thật nói cùng một thứ tự.
 */
export const soTheoConTro = (a, b) => (a.ts - b.ts) || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0);
