/**
 * BẢNG TRẠNG THÁI — MỘT nguồn sự thật về bé cho mọi mô-đun (mẫu Blackboard).
 *
 * ── VÌ SAO CẦN ──
 * Trạng thái của một bé nằm rải ở SÁU chỗ, và mỗi màn tự đi gom lấy phần nó cần:
 *
 *   `vectorS`      mức nắm bài · hay quên · dạng mạnh · dễ mệt   → PhongNoi.jsx
 *   `xepTheoZPD`   câu nào trong vùng phát triển gần             → BaiHoc.jsx
 *   `nutGocRe`     nút gốc rễ của chỗ bé mắc                     → PhuDao.jsx
 *   `theDenHan`    thẻ ôn tới hạn                                → ManTiengAnh.jsx
 *   `hoSoAI`       trí nhớ qua nhiều buổi (V3)                   → PhongNoi.jsx
 *   `buoiThu`      buổi thứ mấy                                  → PhongNoi.jsx
 *
 * Mỗi màn gom một kiểu thì không màn nào thấy đủ, và hai màn có thể nói hai điều
 * khác nhau về cùng một bé. Kế hoạch buổi (V7) thì cần CẢ SÁU trong một lượt —
 * không có chỗ nào đưa cả sáu cho nó được.
 *
 * ── THUẦN, VÀ BẤT BIẾN ──
 * Tệp này KHÔNG fetch gì: màn hình nạp dữ liệu rồi truyền vào. Nhờ thế cổng chạy
 * được bằng `node`, và cái bảng thì tái dựng được y hệt từ cùng đầu vào.
 *
 * Mọi hàm GHI (`ghiLuot`, và sau này `datKeHoach` của V7) trả BẢN MỚI, không sửa
 * tại chỗ. Lý do thực tế: bảng đi vào `useMemo`/`useEffect` của React, mà sửa tại
 * chỗ thì React không thấy nó đổi — màn vẽ lại bằng dữ liệu cũ, và chỗ hỏng ấy
 * không bao giờ hiện thành một lỗi, chỉ thành "sao cô không biết con vừa nói gì".
 */
import { vectorS } from './chinhsach.js';
import { xepTheoZPD } from './zpd.js';
import { nutGocRe } from './lantruyen.js';
import { theDenHan } from './onlai.js';
import { dongHoSoAI } from './hosoai.js';

/** Trần kích thước cả bảng. Vượt là có ai đang nhét dữ liệu thô vào. */
export const TRAN_BANG_KY_TU = 4000;

/** Trần ký tự phần tóm tắt đi vào lời dặn. Lời dặn còn phải chừa chỗ cho bảng vốn. */
export const TRAN_TOM_TAT = 900;

/** Dấu bọc khối riêng — giao ước với `locKhung` ở `functions/src/vantay.js`. */
export const DAU_KHOI_RIENG = '<<RIENG';
export const CUOI_KHOI_RIENG = 'RIENG>>';

/** Mọi mã nút xuất hiện trong kho câu của một bài. */
export const nutCuaBai = (bai) => [...new Set(
  (bai?.practice?.pools ? Object.values(bai.practice.pools).flat() : [])
    .map((c) => c?.maNut).filter(Boolean),
)];

/**
 * DỰNG BẢNG. Mọi đầu vào đều KHÔNG bắt buộc — màn nào có gì thì truyền, thiếu thì
 * trường ấy là `null`/`[]`.
 *
 * ⚠ Thiếu thì để RỖNG, đừng đoán. Một màn chỉ nạp `mucThao` mà bảng tự bịa ra
 * `theDenHan: []` nghe như "không có thẻ nào đến hạn" — trong khi thật ra là "màn
 * này không biết". Hai điều ấy khác nhau, nên `theDenHan` để `null` khi không có
 * `cards`, và chỗ đọc phải phân biệt được.
 */
export function dungBang({
  tienDo = null, mucThao = null, doThi = null, cards = null, hoSoAI = null,
  bai = null, cauDs = null, maNutMac = null, quyen = null, dinhDang = null,
  thich = null, bayGio = Date.now(),
  /* ⚠ ĐƯỜNG TƯƠNG THÍCH. Mấy chỗ gọi cũ (`loiDan({hoSo})`, và cả cổng) truyền một
     `hoSo` ĐÃ TÍNH SẴN — họ không có `mucThao` để `vectorS` tính lại. Nhận nó vào
     và ĐẮP LÊN kết quả tính: thiếu đường này thì `mucNam` · `dangManh` · `hayQuen`
     · `deMet` của mọi chỗ gọi cũ lặng lẽ về `null`, và lời dặn mất mấy dòng mà
     không cổng nào kêu (chúng chỉ soi `loiDan` với `hoSo`, và `hoSo` thì vẫn ở đó). */
  hoSo = null,
} = {}) {
  const maNutDs = nutCuaBai(bai);
  const ai = hoSoAI || hoSo?.ai || tienDo?.hoSoAI || null;
  return {
    mucThao: mucThao || null,
    /* Thứ tự câu theo vùng phát triển gần. Không có kho câu thì `null` — xem ghi
       chú trên: `[]` nghe như "không câu nào", khác hẳn "màn này không biết". */
    nhomZPD: cauDs ? xepTheoZPD(cauDs, mucThao, dinhDang) : null,
    nutGocRe: (doThi && maNutMac)
      ? (nutGocRe(doThi, mucThao, maNutMac, { toiDa: 1 })[0]?.ma || maNutMac) : null,
    theDenHan: cards ? theDenHan(cards, { quyen, bayGio, mucThao }) : null,
    hoSo: {
      ...vectorS({ mucThao, maNutDs, dinhDang, thich: thich || hoSo?.thich, bayGio }),
      /* Bản đã tính sẵn đắp lên — xem ghi chú ở tham số `hoSo`. Chỉ đắp trường CÓ
         giá trị, để một `hoSo` thiếu trường không xoá mất phần `vectorS` vừa tính. */
      ...Object.fromEntries(Object.entries(hoSo || {})
        .filter(([k, v]) => k !== 'ai' && v !== null && v !== undefined)),
      /* `ai` nằm TRONG `hoSo` chứ không đứng riêng: `dongHoSo` và `hoiCoGiao` xưa
         nay nhận một đối tượng `hoSo`, nên giữ hình dạng ấy thì không chỗ gọi nào
         phải sửa. V3 đã dùng `hoSo.ai`. */
      ai,
    },
    /* Lượt gần nhất và nhãn của nó — `ghiLuot` điền. `null` lúc dựng là ĐÚNG: đầu
       buổi thì chưa có lượt nào, và cổng canh đúng điều ấy. */
    luotGanNhat: null,
    nhanGanNhat: null,
    /* Kế hoạch buổi — V7 điền. Khai sẵn để hình dạng bảng khỏi đổi lần nữa. */
    keHoach: null,
    buoiThu: ai?.buoiThu || 0,
    bai: bai?.id || null,
    quyen: quyen || null,
  };
}

/**
 * Ghi lượt vừa rồi vào bảng — TRẢ BẢN MỚI.
 *
 * ⚠ Chỉ giữ ĐÚNG lượt gần nhất, không giữ cả lịch sử: lịch sử là của màn hình
 * (`lichSu` trong `PhongNoi.jsx`), và nhân đôi nó vào đây thì hai bản sớm muộn
 * lệch nhau — mà bảng thì đi vào lời dặn.
 */
export function ghiLuot(bang, luot = null, nhan = null) {
  return { ...(bang || dungBang()), luotGanNhat: luot || null, nhanGanNhat: nhan || null };
}

/**
 * Đặt (hoặc cập nhật) KẾ HOẠCH BUỔI vào bảng — TRẢ BẢN MỚI (việc V7).
 *
 * Bảng khai sẵn trường `keHoach` từ V6 đúng để chỗ này không phải đổi hình dạng
 * bảng. Và cùng một lý do bất biến như `ghiLuot`: bảng đi vào `useMemo` của React.
 */
export function datKeHoach(bang, keHoach = null) {
  return { ...(bang || dungBang()), keHoach: keHoach || null };
}

/* ─────────── tóm tắt cho lời dặn ─────────── */

/**
 * HAI THỨ TỰ KHÁC NHAU, và trộn chúng làm một là lỗi tôi vừa phải sửa.
 *
 * `UU_TIEN_GIU` — vượt trần thì bỏ từ CUỐI lên. Thứ tự lấy từ §7 việc V6: nhãn gần
 * nhất giữ chặt nhất, sở thích bỏ trước nhất.
 *
 * `THU_TU_IN` — thứ tự ĐỌC. Dùng luôn thứ tự giữ để in thì khối ra như thế này
 * (đo thật 09-10): khối trí nhớ "ABOUT THIS CHILD" đứng TRƯỚC, rồi một dòng sở
 * thích lủng lẳng phía sau nó. Mô hình đọc xuôi từ trên xuống, nên dòng rời rạc ở
 * cuối là dòng dễ bị hiểu thành một lệnh mới.
 */
const UU_TIEN_GIU = ['ten', 'nhan', 'muc', 'zpd', 'baiHoc', 'soThich'];
const THU_TU_IN = ['ten', 'nhan', 'muc', 'soThich', 'zpd', 'baiHoc'];

/**
 * KHỐI "ABOUT THE CHILD" CHO LỜI DẶN — một chỗ duy nhất dựng nó.
 *
 * Trước V6 khối này do `dongHoSo` trong `phongnoi.js` dựng, và phần trí nhớ do
 * `dongHoSoAI` dựng riêng — hai hàm, hai tệp, cùng một khối. Nay một hàm.
 *
 * Ba quy ước, cả ba đều có từ trước và KHÔNG được phá:
 *   · KHÔNG SỐ. Mô hình rất dễ nhại nguyên văn, và "Con được 42%" thì không phải
 *     câu đọc to lên được trước mặt bé. Cắt chữ số ở ĐÚNG MỘT CHỖ, cuối hàm.
 *   · Câu nào cũng phải KHÔNG SAO nếu lỡ bị đọc to.
 *   · Nói bằng câu người đọc được, đừng đổ dữ liệu thô vào.
 *
 * Và cả khối nằm giữa `<<RIENG … RIENG>>` để `locKhung` bỏ sạch khỏi vân tay.
 */
export function tomTatChoLoiDan(bang, tenBe = '') {
  const b = bang || dungBang();
  const h = b.hoSo || {};
  const phan = { ten: [], nhan: [], muc: [], zpd: [], baiHoc: [], soThich: [] };

  if (tenBe) phan.ten.push(`The child's name is ${tenBe} — use it in [Name] slots.`);

  /* ⚠ ĐỪNG NÓI SỞ THÍCH HAI LẦN. `h.thich` (chọn trong buổi này) và
     `h.ai.soThich` (nhớ từ buổi trước) rất hay là CÙNG MỘT TỪ — V3 và V6 mỗi bên
     dựng một dòng, và khối ra hai câu gần như y nhau:
       "Lan has told you she likes: fish."
       "The child told you they like \"fish\"."
     Hai câu cùng nghĩa trong một lời dặn vừa tốn chỗ vừa nghe như hai lệnh. Nhớ
     được rồi thì để phần trí nhớ nói, vì nó nói gọn hơn. */
  const aiDaNoi = (h.ai?.soThich || []).includes(h.thich);
  if (h.thich && !aiDaNoi) {
    phan.soThich.push(`The child told you they like "${h.thich}".`
      + ' Prefer that word when a pattern needs a thing — it makes the sentence about them.');
  }
  /* ⚠ NÓI BẰNG CÂU, ĐỪNG ĐỔ SỐ VÀO. "p=0.42" thì mô hình không biết làm gì với nó,
     mà chỗ nào cũng có thể hiểu khác đi. "She is still shaky" thì rõ một nghĩa. */
  if (h.mucNam === 'yeu') {
    phan.muc.push('She is still shaky on this unit — keep sentences short, stay with'
      + ' words she has met many times, and praise small correct bits.');
  } else if (h.mucNam === 'vung') {
    phan.muc.push('She is solid on this unit — you may ask slightly longer questions'
      + ' and let her lead more of the turns.');
  }
  if (h.dangManh) phan.muc.push(`She answers best in "${h.dangManh}" style tasks.`);
  if (h.hayQuen) {
    phan.muc.push('She has not touched some of this for a while — bring back one or'
      + ' two older words on purpose.');
  }
  if (h.deMet) phan.muc.push('She slows down towards the end of a session — keep this one brisk.');

  /* Thẻ ôn tới hạn: nói CÓ hay KHÔNG, không nói MẤY CÁI (luật không-số). */
  if (b.theDenHan && b.theDenHan.length) {
    phan.zpd.push('Some older words are due for review today — weave them in when'
      + ' a pattern lets you.');
  }

  /* Trí nhớ qua nhiều buổi (V3). `dongHoSoAI` tự lui về chuỗi rỗng ở buổi đầu. */
  const nho = dongHoSoAI(h.ai, tenBe);
  if (nho) phan.baiHoc.push(nho);

  /* ── CẮT THEO ƯU TIÊN ── Bỏ từ nhóm ưu tiên THẤP nhất, cho tới khi vừa trần. */
  const dung = (bo) => THU_TU_IN.filter((k) => !bo.has(k)).flatMap((k) => phan[k]).join('\n');
  const bo = new Set();
  let than = dung(bo);
  for (const k of [...UU_TIEN_GIU].reverse()) {
    if (than.length <= TRAN_TOM_TAT) break;
    bo.add(k);
    than = dung(bo);
  }
  if (!than) return '';

  /* Cắt chữ số ở ĐÚNG MỘT CHỖ. Lọc ở từng dòng thì thêm một dòng mới mà quên lọc
     là con số lọt vào lời dặn — mà phần trí nhớ do mô hình viết là đường dễ lọt
     nhất, và câu sẵn của sách cũng có số ("It's 45 Ba Trieu Street."). */
  const khongSo = (s) => s.replace(/\d+([.,]\d+)?%?/g, 'some');
  return `${DAU_KHOI_RIENG}\n${khongSo(than).slice(0, TRAN_TOM_TAT)}\n${CUOI_KHOI_RIENG}`;
}
