/**
 * SỔ NGƯỜI DÙNG CỦA MÁY NÀY — nhà có mấy bé thì máy nhớ mấy bé.
 *
 * ── VÌ SAO CẦN ──
 * Một máy tính bảng thường là của cả nhà: anh học lớp 5, em học lớp 2. Firebase Auth
 * chỉ giữ được MỘT phiên cho mỗi "app", nên nếu cả nhà dùng chung một app thì mỗi lần
 * đổi bé là một lần mở hộp thư lấy mã — không ai chịu nổi, và rốt cuộc hai bé dùng
 * chung một tài khoản, sổ học trộn vào nhau.
 *
 * ── CÁCH LÀM: MỖI BÉ MỘT CHỖ ──
 * Firebase cho phép dựng nhiều thể hiện app, mỗi cái một TÊN, và phiên đăng nhập lưu
 * theo tên ấy (`firebase:authUser:{apiKey}:{tênApp}`). Nên mỗi bé được cấp một "chỗ" —
 * `c1`, `c2`, … — và phiên của bé nằm nguyên trong chỗ của mình, không đụng bé khác.
 *
 * Máy nhớ chỗ nào đang mở trong `ttd5.choDangDung.v1`. Đổi bé = ghi chỗ khác rồi TẢI
 * LẠI TRANG. Tải lại nghe thô, nhưng nó giữ cho `nenTang.js` chỉ phải dựng đúng MỘT
 * thể hiện lúc khởi động — nếu không, `db`/`auth`/`fns` phải đổi được giữa chừng và
 * mọi tệp đang `import` chúng đều phải viết lại. Đổi bé là việc vài giây một lần trong
 * ngày; đánh đổi ấy quá rẻ.
 *
 * ── SỔ NÀY KHÔNG PHẢI GIẤY THÔNG HÀNH ──
 * Ở đây chỉ ghi tên · lớp · email để VẼ ra danh sách chọn. Vào được hay không vẫn do
 * phiên Firebase trong chỗ ấy quyết định: xoá phiên đi thì bấm vào tên chỉ ra màn nhập
 * mã. Sổ này mất cũng không mất tài khoản nào.
 */

const KHOA_SO = 'ttd5.nguoiDung.v1';
const KHOA_CHO = 'ttd5.choDangDung.v1';

/** Chỗ mặc định — tên app rỗng nghĩa là thể hiện `[DEFAULT]` của Firebase. */
export const CHO_DAU = 'c1';

const doc = (kho) => {
  try { return JSON.parse(kho.getItem(KHOA_SO) || '[]'); } catch { return []; }
};
const ghi = (ds, kho) => {
  try { kho.setItem(KHOA_SO, JSON.stringify(ds)); } catch { /* chế độ riêng tư */ }
};

/** Danh sách bé đã đăng nhập trên máy này, bé động vào gần nhất lên đầu. */
export function dsNguoi(kho = globalThis.localStorage) {
  return doc(kho)
    .filter((n) => n && n.cho)
    .sort((a, b) => (b.lanCuoi || 0) - (a.lanCuoi || 0));
}

/** Chỗ đang mở. Chưa có thì là chỗ đầu. */
export function choDangDung(kho = globalThis.localStorage) {
  try { return kho.getItem(KHOA_CHO) || CHO_DAU; } catch { return CHO_DAU; }
}

/**
 * Ghi nhận một bé vừa đăng nhập (hoặc vừa đổi tên/lớp) vào chỗ đang mở.
 * Khoá theo CHỖ chứ không theo uid: một chỗ chỉ giữ được một phiên, nên bé mới đăng
 * nhập vào chỗ ấy là thay hẳn bé cũ — ghi đè đúng là điều mình muốn.
 */
export function ghiNguoi(tin, kho = globalThis.localStorage) {
  const cho = tin.cho || choDangDung(kho);
  const ds = doc(kho).filter((n) => n && n.cho && n.cho !== cho);
  ds.push({ ...tin, cho, lanCuoi: tin.lanCuoi ?? Date.now() });
  ghi(ds, kho);
  return ds;
}

/** Bỏ một bé khỏi sổ (bé thôi học ở máy này). Không đụng tới phiên Firebase. */
export function xoaNguoi(cho, kho = globalThis.localStorage) {
  ghi(doc(kho).filter((n) => n && n.cho !== cho), kho);
}

/**
 * Chỗ trống tiếp theo để thêm bé mới.
 * Đếm từ `c1` lên, lấy số nhỏ nhất chưa ai dùng — bé rời đi thì chỗ ấy dùng lại được,
 * không để số cứ tăng mãi.
 */
export function choTrong(kho = globalThis.localStorage) {
  const dung = new Set(doc(kho).map((n) => n?.cho));
  for (let i = 1; i <= 20; i++) if (!dung.has(`c${i}`)) return `c${i}`;
  return `c${Date.now().toString(36)}`;      // hai chục bé một máy thì chịu, cứ cấp bừa
}

const KHOA_THEM = 'ttd5.dangThemBe.v1';

/**
 * Đổi sang chỗ khác rồi TẢI LẠI trang.
 * Tải lại là cố ý — xem lời giải thích ở đầu tệp.
 *
 * `moi: true` khi chỗ ấy còn trống và mình vừa cấp nó để THÊM một bé. Không có dấu
 * này thì sau khi tải lại, app thấy "chỗ này chưa ai đăng nhập, mà máy còn nhớ bé
 * khác" và lại hỏi "ai đang học" — bấm "Thêm bé khác" quay về đúng màn vừa bấm, một
 * vòng luẩn quẩn không có lối ra.
 */
export function doiCho(cho, { kho = globalThis.localStorage, taiLai, moi = false } = {}) {
  try {
    kho.setItem(KHOA_CHO, cho);
    if (moi) kho.setItem(KHOA_THEM, '1'); else kho.removeItem(KHOA_THEM);
  } catch { /* chế độ riêng tư */ }
  const nap = taiLai || (() => globalThis.location?.reload());
  nap();
}

/**
 * Có phải vừa mở một chỗ trống để thêm bé không? Đọc XONG LÀ XOÁ — chỉ đúng cho
 * đúng một lần vẽ ngay sau khi tải lại; bé bỏ dở giữa chừng rồi mở app lần sau thì
 * vẫn được hỏi "ai đang học" như thường.
 */
export function dangThemBe(kho = globalThis.localStorage) {
  try {
    const co = kho.getItem(KHOA_THEM) === '1';
    if (co) kho.removeItem(KHOA_THEM);
    return co;
  } catch { return false; }
}

/** Tên hiện lên nút chọn: ưu tiên tên con, không có thì lấy phần trước @ của email. */
export const tenHien = (n) =>
  n?.ten || n?.bietDanh || String(n?.email || '').split('@')[0] || 'Bạn nhỏ';

/** Chữ cái đầu cho vòng tròn avatar — bé chưa biết đọc vẫn nhận ra chỗ của mình. */
export const chuDau = (n) => tenHien(n).trim().charAt(0).toUpperCase() || '?';
