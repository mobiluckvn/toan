/**
 * PHÂN XỬ LƯỢT NÓI MƠ HỒ — hai phiếu song song (việc V10, mẫu #3 Parallelization).
 *
 * ── CHỖ HỎNG NÓ ĐI CHỮA ──
 * `chamTu` chấm bằng độ giống chuỗi. Khi từ đích và một từ CÙNG UNIT đều gần với
 * cái máy nghe được — `nine` 0.62 với `name` 0.50 — thì bộ chấm vẫn chọn một trong
 * hai, bằng một con số lẻ sau dấu phẩy. Chọn đúng hay sai ở đó là chuyện may, mà nó
 * lại rơi quanh ngưỡng đạt 6: cùng một lượt nói có thể thành "đạt" hay "chưa" tuỳ
 * phép đo chuỗi lệch nhau 0.04.
 *
 * Phép đo chuỗi không biết gì về PHÁT ÂM. Mô hình thì biết — nó đã đọc hàng triệu
 * lần người ta gõ sai chính tả theo âm. Nên ở đúng vùng mơ hồ ấy, hỏi nó một câu
 * rất hẹp: "máy nghe ra thế này, bé đang nói chữ nào trong hai chữ?"
 *
 * ── HAI PHIẾU, VÀ VÌ SAO PHẢI KHÁC NHAU HAI ĐƯỜNG ──
 * Hỏi cùng một mô hình hai lần cùng một cách thì hai câu trả lời không độc lập — nó
 * sai thì sai y như nhau, và "hai phiếu nhất trí" trở thành một con dấu vô nghĩa
 * đóng lên đúng cái sai ấy. Nên hai phiếu khác nhau ở HAI chỗ:
 *
 *   1. NHIỆT khác nhau (0.2 / 0.5) — §7 của bản thiết kế chốt thế.
 *   2. THỨ TỰ HAI CHỮ đảo ngược. Phiếu một thấy "A = từ đích", phiếu hai thấy
 *      "A = từ cạnh tranh". Đây là phần tôi thêm, vì nhiệt không chữa được thiên
 *      lệch theo VỊ TRÍ, mà thiên lệch vị trí là thứ có thật ở mọi mô hình.
 *
 * ── VÀ LỜI DẶN KHÔNG NÓI CHỮ NÀO LÀ CHỮ ĐANG HỎI ──
 * Nói ra là mời nó lấy lòng: "bé được yêu cầu đọc `nine`" thì câu trả lời dễ đoán
 * trước khi gọi. Nên hai chữ vào lời dặn dưới tên A và B, và CHỈ mã này biết chữ
 * nào là chữ nào.
 *
 * ── KHÔNG LƯU GÌ, VÀ KHÔNG VIẾT LỜI CHO BÉ ──
 * Mô hình chỉ được trả về MỘT NHÃN: A, B, hay "khac". Lời cô nói với bé vẫn do
 * `chamnoi.loiKhen` dựng, từ điểm đã chỉnh. Cho mô hình viết lời khen ở đây là mở
 * một cửa nữa cho chữ ngoài vốn đi vào, mà cửa ấy chẳng đổi lấy gì.
 */
import { vanTay } from './vantay.js';
import { MO_HINH, NGHI_NGAN, LoiGoi } from './luyennoi.js';

export { MO_HINH, NGHI_NGAN, LoiGoi };

/** Trần gói gửi lên. Ba chuỗi rất ngắn — gói to hơn thế là gói bất thường. */
export const TOI_DA_CHU = 120;

/**
 * Trần token. Câu trả lời đúng một nhãn, nhưng mô hình này vẫn nghĩ trước khi đáp,
 * nên đừng bóp tới sát — bóp quá thì nó trả rỗng và phiếu mất trắng.
 */
export const TOKEN_PHAN_XU = 200;

/** Hai phiếu, hai nhiệt. Số lượng phiếu là HẰNG, không phải con số rải trong vòng lặp. */
export const SO_PHIEU = 2;
export const NHIET_PHIEU = [0.2, 0.5];

/** Đếm để còn lần ra trên bản thật. Máy chủ KHÔNG ghi gì xuống Firestore. */
export const LOI_PHAN_XU = { goi: 0, hong: 0, nhatTri: 0, lech: 0, ganNhat: null };

/**
 * Soi gói máy con gửi lên. Trả gói đã sạch, hoặc ném `LoiGoi`.
 *
 * Tách khỏi phần gọi mạng để chạy được bằng `node` mà không cần khoá — cùng khuôn
 * `soiGoiPhuDao`.
 */
export function soiGoiPhanXu(du) {
  const chu = (x) => String(x ?? '').trim();
  const nghe = chu(du?.nghe);
  const dich = chu(du?.dich);
  const canhTranh = chu(du?.canhTranh);
  if (!nghe) throw new LoiGoi('thieu-nghe', 'Thiếu lời máy nghe được.');
  if (!dich) throw new LoiGoi('thieu-dich', 'Thiếu từ cần đọc.');
  if (!canhTranh) throw new LoiGoi('thieu-canh-tranh', 'Thiếu từ cạnh tranh.');
  for (const [ten, x] of [['nghe', nghe], ['dich', dich], ['canhTranh', canhTranh]]) {
    if (x.length > TOI_DA_CHU) {
      throw new LoiGoi('qua-dai', `Trường "${ten}" dài quá ${TOI_DA_CHU} ký tự.`);
    }
  }
  /* Hai chữ TRÙNG nhau thì chẳng có gì để phân xử, mà vẫn tốn hai lượt gọi. Bác ở
     đây chứ không để mô hình tự phát hiện: nó sẽ trả về một nhãn nào đó, và nhãn
     ấy nhất trí 2/2 rồi điểm bị chỉnh vì một câu hỏi vô nghĩa. */
  if (dich.toLowerCase() === canhTranh.toLowerCase()) {
    throw new LoiGoi('hai-chu-trung', 'Từ cần đọc và từ cạnh tranh trùng nhau.');
  }
  /* KHÔNG nhận `lop`: lời dặn không dùng tới nó. Chuyền một trường qua ba tầng
     rồi không ai đọc là thứ sẽ mục — và mỗi trường thừa đi lên máy chủ lại là một
     mẩu nữa về bé rời khỏi máy, dù mẩu ấy chẳng để làm gì. */
  return { nghe, dich, canhTranh };
}

/**
 * Lời dặn phân xử.
 *
 * @param daoChieu  `false` → A là từ đích; `true` → A là từ cạnh tranh. Hai phiếu
 *                  gọi với hai giá trị khác nhau, xem khối chú thích đầu tệp.
 */
export function loiDanPhanXu({ nghe, dich, canhTranh, daoChieu = false }) {
  const A = daoChieu ? canhTranh : dich;
  const B = daoChieu ? dich : canhTranh;
  return [
    'Một bé người Việt đang học tiếng Anh đọc to một từ vào micro. Bộ nhận dạng',
    'giọng nói của trình duyệt ghi lại được chuỗi dưới đây — nó thường ghi sai, vì',
    'nó đoán theo cách người bản ngữ nói.',
    '',
    `MÁY NGHE ĐƯỢC: "${nghe}"`,
    '',
    'HAI TỪ CÓ THỂ BÉ ĐANG ĐỌC:',
    `A. ${A}`,
    `B. ${B}`,
    '',
    'VIỆC CỦA BẠN: xét theo CÁCH PHÁT ÂM, chuỗi máy nghe được giống lời đọc của từ',
    'nào hơn? Nghĩ theo âm, không theo cách viết: bé có thể đọc đúng mà máy ghi lại',
    'bằng một cách viết khác hẳn.',
    '',
    'CHỈ trả về một trong ba nhãn:',
    '- "A" nếu nghiêng về từ A;',
    '- "B" nếu nghiêng về từ B;',
    '- "khac" nếu không nghiêng về bên nào, hoặc chuỗi ấy rõ ràng là một từ thứ ba.',
    'Không chắc thì trả "khac" — đoán bừa còn tệ hơn không trả lời.',
    '',
    'TRẢ LỜI ĐÚNG MỘT KHỐI JSON, không thêm chữ nào ngoài khối:',
    '{"gan": "A"}',
  ].join('\n');
}

/**
 * Khung của lời dặn — dựng bằng CHÍNH hàm trên với phần riêng để rỗng.
 *
 * ⚠ Dựng CẢ HAI chiều rồi ghép: hai phiếu là hai lời dặn khác nhau, nên mẫu của
 * lượt này là cả cặp. Dựng một chiều thôi thì sửa chiều kia bao nhiêu cũng không
 * làm vân tay đổi — đúng cái bẫy `khungCham` đã dính ở V4.
 */
export const khungPhanXu = () => [
  loiDanPhanXu({ nghe: '', dich: '', canhTranh: '', daoChieu: false }),
  loiDanPhanXu({ nghe: '', dich: '', canhTranh: '', daoChieu: true }),
].join('\n');

/** Nhãn A/B của một phiếu → chữ nào, kể theo vai (`dich` | `canhTranh` | `khac`). */
export function doiNhan(gan, daoChieu) {
  const g = String(gan ?? '').trim().toUpperCase();
  if (g === 'A') return daoChieu ? 'canhTranh' : 'dich';
  if (g === 'B') return daoChieu ? 'dich' : 'canhTranh';
  return 'khac';
}

/* Bóc JSON — cùng lý do như `chamviet.js`: mô hình được dặn trả đúng một khối,
   nhưng không được TIN là nó luôn làm đúng. */
function bocJSON(chu) {
  const m = String(chu || '').match(/\{[\s\S]*\}/);
  if (!m) return null;
  try { return JSON.parse(m[0]); } catch { return null; }
}

/**
 * Gộp phiếu thành mức điều chỉnh.
 *
 * ⚠ CHỈ NHẤT TRÍ TUYỆT ĐỐI MỚI ĐƯỢC ĐỔI ĐIỂM. Hai phiếu thì "đa số" chỉ có thể là
 * 2/2; 1–1 là mô hình tự nó không chắc, mà chỗ nó không chắc thì phép đo chuỗi của
 * mình vẫn là thứ đáng tin hơn — nó ít nhất còn đo được, và đo cùng một cách cho
 * mọi bé. Một phiếu "khac" cũng đủ làm cả cặp mất hiệu lực.
 *
 * Thuần, không mạng — nên cổng canh được cả bốn tổ hợp.
 */
export function gopPhieu(phieu) {
  const ds = (phieu || []).filter((x) => x === 'dich' || x === 'canhTranh' || x === 'khac');
  if (ds.length < SO_PHIEU) return { gan: 'khac', dieuChinh: 0, nhatTri: false };
  const dau = ds[0];
  if (!ds.every((x) => x === dau)) return { gan: 'khac', dieuChinh: 0, nhatTri: false };
  if (dau === 'dich') return { gan: 'dich', dieuChinh: 1, nhatTri: true };
  if (dau === 'canhTranh') return { gan: 'canhTranh', dieuChinh: -1, nhatTri: true };
  /* Cả hai phiếu đều "khac": nhất trí rằng ĐÓ KHÔNG PHẢI từ nào trong hai — nhưng
     điều đó không nói bé đọc từ đích đúng hay sai, nên không chỉnh gì. */
  return { gan: 'khac', dieuChinh: 0, nhatTri: true };
}

/* Một phiếu. Hỏng thì trả `null` chứ không ném: một phiếu mất là cặp mất nhất trí,
   mà cặp mất nhất trí nghĩa là GIỮ ĐIỂM — đúng điều §7 đòi khi mất mạng. */
async function motPhieu(client, goi, { nhiet, daoChieu }) {
  try {
    const kq = await client.chat.completions.create({
      model: MO_HINH,
      messages: [{ role: 'system', content: loiDanPhanXu({ ...goi, daoChieu }) }],
      temperature: nhiet,
      max_tokens: TOKEN_PHAN_XU,
      reasoning_effort: NGHI_NGAN,
      response_format: { type: 'json_object' },
    });
    const chu = kq?.choices?.[0]?.message?.content || '';
    const b = bocJSON(chu);
    if (!b || b.gan == null) return null;
    return doiNhan(b.gan, daoChieu);
  } catch {
    return null;
  }
}

/**
 * PHÂN XỬ — hai phiếu SONG SONG.
 *
 * Song song không phải để nhanh cho vui: lượt này nằm giữa lúc bé vừa nói xong và
 * lúc thấy điểm. Hai lượt nối tiếp là nhân đôi quãng chờ ấy, mà quãng chờ là chỗ bé
 * sáu tuổi bỏ đi. Chạy song song thì thêm một phiếu gần như không thêm giây nào.
 *
 * Trả về MỨC ĐIỀU CHỈNH, không trả về điểm: phép kẹp trong [5, 7] nằm ở
 * `chamnoi.apDungPhieu` của máy con, cùng chỗ với `VUNG_MO_HO` và có cổng canh.
 * Máy chủ quyết điểm là hai nơi cùng biết một luật.
 */
export async function phanXu(du, taoClient) {
  const goi = soiGoiPhanXu(du);
  const client = taoClient();
  LOI_PHAN_XU.goi += 1;

  const phieu = await Promise.all(
    NHIET_PHIEU.slice(0, SO_PHIEU).map((nhiet, i) => motPhieu(client, goi, {
      nhiet,
      /* Phiếu chẵn xem từ đích là A, phiếu lẻ xem từ cạnh tranh là A. */
      daoChieu: i % 2 === 1,
    })),
  );

  const hong = phieu.filter((x) => x == null).length;
  if (hong) LOI_PHAN_XU.hong += hong;
  const ket = gopPhieu(phieu.filter((x) => x != null));
  if (ket.nhatTri) LOI_PHAN_XU.nhatTri += 1; else LOI_PHAN_XU.lech += 1;
  LOI_PHAN_XU.ganNhat = `${phieu.join('|')} → ${ket.dieuChinh}`;

  return {
    ...ket,
    phieu,
    soPhieuHong: hong,
    moHinh: MO_HINH,
    ...vanTay('phanxu', khungPhanXu(), {
      moHinh: MO_HINH, nhiet: NHIET_PHIEU.join('/'), token: TOKEN_PHAN_XU,
    }),
  };
}
