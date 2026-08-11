/**
 * BẢNG XẾP HẠNG — phần tính toán phía màn hình.
 *
 * Máy chủ đã dựng sẵn `rows` kèm ba hạng (tuần · chuỗi · tổng) cho TOÀN TRƯỜNG. Tệp
 * này lo ba việc mà máy chủ không lo được, vì chúng phụ thuộc vào CON ĐANG XEM:
 *
 *   1. lọc theo lớp rồi XẾP HẠNG LẠI — bảng "lớp 3" phải đánh số từ 1, không phải
 *      giữ nguyên hạng toàn trường (bé lớp 3 giỏi nhất mà hiện "hạng 14" thì vô nghĩa);
 *   2. cắt Top N nhưng LUÔN GHIM dòng của con — bé hạng 87 vẫn phải thấy mình, kèm
 *      khoảng cách tới người ngay trên. Đó mới là con số làm bé cố, không phải hạng 1;
 *   3. dựng thanh so kè với BẠN ĐANG ĐUỔI.
 *
 * Thuần hàm, không React — phép kiểm chạy được bằng node (test/xephang.test.mjs).
 */

/** Ba bảng. `khoa` là trường điểm, `nhan` là chữ hiện dưới con số. */
export const BANG = [
  { ma: 'tuan',  ten: '🔥 Tuần này',  khoa: 'saoTuan', nhan: 'sao tuần này',
    mo: 'Sao kiếm được trong 7 ngày. Đặt lại mỗi tuần — ai cũng có cửa.' },
  { ma: 'chuoi', ten: '📅 Chuỗi ngày', khoa: 'chuoi',   nhan: 'ngày liên tiếp',
    mo: 'Số ngày học liên tiếp. Học đều là thắng, không cần học nhiều.' },
  { ma: 'tong',  ten: '👑 Tổng sao',   khoa: 'saoTong', nhan: 'tổng sao',
    mo: 'Cả chặng đường con đã đi. Đây là bảng của người bền bỉ.' },
];

export const bangCua = (ma) => BANG.find((b) => b.ma === ma) || BANG[0];

/** Xếp hạng: cùng điểm thì cùng hạng, hạng sau nhảy đúng số người đứng trên. */
export function xepLai(rows, khoa) {
  const sap = rows.slice().sort((a, b) => (b[khoa] || 0) - (a[khoa] || 0)
    || String(a.ten).localeCompare(String(b.ten), 'vi'));
  let hang = 0, truoc = null;
  return sap.map((r, i) => {
    const d = r[khoa] || 0;
    if (d !== truoc) { hang = i + 1; truoc = d; }
    return { ...r, hang };
  });
}

/**
 * Danh sách để VẼ RA MÀN.
 *
 * Trả về Top N, và nếu con nằm ngoài Top N thì thêm một dấu ngắt rồi tới dòng của
 * con. CỐ Ý không hiện tổng số người đứng dưới, cũng không hiện hạng bét: bé cuối
 * bảng không cần bị dí mũi vào chỗ đó, và bảng xếp hạng không phải chỗ để làm việc ấy.
 */
export function danhSachHien(rows, khoa, maCon, n = 20) {
  const sap = xepLai(rows, khoa);
  const tren = sap.slice(0, n);
  const con = sap.find((r) => r.ma === maCon) || null;
  const trongTop = !!con && tren.some((r) => r.ma === maCon);
  return {
    tren,
    con,
    /* Chỉ chèn dấu ngắt khi con THẬT SỰ ở dưới — con chưa có trong bảng (mới tạo
       tài khoản, chưa kịp dựng lại) thì đừng vẽ một dòng trống lửng lơ. */
    ngoaiTop: !!con && !trongTop,
    tong: sap.length,
  };
}

/**
 * KHOẢNG CÁCH TỚI NGƯỜI NGAY TRÊN — con số làm bé cố gắng.
 *
 * "Còn 12 sao nữa là con vượt Su Kem" nói được nhiều hơn "con hạng 27" gấp nhiều lần:
 * một cái là việc làm được ngay chiều nay, cái kia là một nhãn dán.
 */
export function khoangCachTren(rows, khoa, maCon) {
  const sap = xepLai(rows, khoa);
  const i = sap.findIndex((r) => r.ma === maCon);
  if (i <= 0) return null;                       // chưa có trong bảng, hoặc đang dẫn đầu
  /* Người NGAY TRÊN theo điểm, không phải theo dòng: ba bạn cùng 120 sao thì người
     con cần vượt là bạn 130 sao, chứ không phải bạn cùng 120 đứng trên một dòng. */
  const con = sap[i];
  const tren = sap.slice(0, i).reverse().find((r) => (r[khoa] || 0) > (con[khoa] || 0));
  if (!tren) return null;
  return { ban: tren, thieu: (tren[khoa] || 0) - (con[khoa] || 0) };
}

/**
 * THANH SO KÈ với bạn con đang đuổi.
 *
 * Trả `null` khi chưa chọn ai, khi bạn ấy đã rời bảng, hoặc khi con tự chọn chính
 * mình — ba ngả bìa mà nơi gọi rất dễ quên, và quên thì màn hình vẽ ra một thanh
 * so kè con với chính con.
 */
export function soKe(rows, khoa, maCon, maBan) {
  if (!maBan || maBan === maCon) return null;
  const sap = xepLai(rows, khoa);
  const con = sap.find((r) => r.ma === maCon);
  const ban = sap.find((r) => r.ma === maBan);
  if (!con || !ban) return null;
  const dCon = con[khoa] || 0, dBan = ban[khoa] || 0;
  return {
    con, ban,
    dan: dCon > dBan ? 'con' : dCon < dBan ? 'ban' : 'hoa',
    cach: Math.abs(dCon - dBan),
    /* Phần trăm để vẽ thanh. Cả hai cùng 0 thì chia đôi, đừng chia cho 0. */
    phanTramCon: dCon + dBan > 0 ? Math.round((dCon / (dCon + dBan)) * 100) : 50,
  };
}

/** Lời nhắn dưới thanh so kè — nói bằng VIỆC LÀM ĐƯỢC, không bằng thứ hạng. */
export function loiSoKe(sk, nhan) {
  if (!sk) return '';
  if (sk.dan === 'hoa') return `Con và ${sk.ban.ten} đang hoà nhau — ai học tiếp là người ấy vượt lên!`;
  if (sk.dan === 'con') return `Con đang dẫn ${sk.ban.ten} ${sk.cach} ${nhan}. Giữ vững nhé!`;
  return `Còn ${sk.cach} ${nhan} nữa là con đuổi kịp ${sk.ban.ten}!`;
}

/** Huy chương cho ba hạng đầu; từ hạng 4 trở đi hiện số. */
export const huyChuong = (hang) => ({ 1: '🥇', 2: '🥈', 3: '🥉' }[hang] || null);

/**
 * Bộ lọc lớp — suy TỪ CHÍNH DỮ LIỆU của bảng, không ghim cứng 2·3·4·5.
 *
 * Hai lý do. Một: hồ sơ nay cho khai lớp 2 → 12, nên nếu ghim 2-5 thì anh lớp 8 có
 * mặt trên bảng mà không có ô lọc nào chứa mình. Hai: ghim đủ mười một lớp thì màn
 * hình đầy chip rỗng — trường nào cũng chỉ có vài lớp thật.
 *
 * Chỉ hiện lớp CÓ NGƯỜI, và chỉ hiện bộ lọc khi có từ hai lớp trở lên: một lớp thì
 * cái nút "Cả nhà" chẳng lọc gì, chỉ tổ chiếm chỗ.
 */
export function dsLop(rows = []) {
  const co = [...new Set(rows.map((r) => Number(r.lop)).filter(Number.isFinite))]
    .sort((a, b) => a - b);
  if (co.length < 2) return [];
  return [{ ma: 0, ten: 'Cả nhà' }, ...co.map((l) => ({ ma: l, ten: `Lớp ${l}` }))];
}

export const locLop = (rows, lop) => (lop ? rows.filter((r) => r.lop === lop) : rows);
