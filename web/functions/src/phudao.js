/**
 * SINH CÂU PHỤ ĐẠO — phần máy chủ. Cùng khuôn `chamviet.js`: soi gói, không lưu gì,
 * trả CHỮ TRẦN kèm vân tay.
 *
 * ── VÌ SAO CẦN TỚI MÔ HÌNH Ở ĐÂY ──
 * Phụ đạo lấy câu từ KHO TĨNH (`cauTinhCuaNut`) — câu đã qua bộ sinh và 83 cổng,
 * nên luôn đúng. Nhưng kho tĩnh không đủ cho mọi nút: nút nào bài chỉ dạy một hai
 * câu thì bé mắc ở đó mà không có gì để ôn, và `dungPhuDao` trả về một bài hai câu.
 *
 * ── VÀ VÌ SAO NÓ LÀ ĐƯỜNG CUỐI ──
 * `dungPhuDao` đi hai vòng tĩnh TRƯỚC (nút gốc rễ #1, rồi #2) rồi mới tới đây. Câu
 * ở đây là câu DUY NHẤT trong app không đi qua bộ sinh, nên:
 *   · máy con hậu kiểm từng câu bằng `cauHoiHopLe` (vốn từ của bài);
 *   · câu nào vào bài đều đeo `nguon: 'ai'`;
 *   · và nó phải CHỜ NGƯỜI LỚN DUYỆT mới được vào kho tĩnh (`choDuyetTA`).
 * Ba tầng cho một đường, vì đường ấy là đường duy nhất không có cổng nào canh sẵn.
 */
import { vanTay } from './vantay.js';
import { MO_HINH, NGHI_NGAN, LoiGoi } from './luyennoi.js';
import { goiDoiJson } from './llm.js';
import { layNguong, boNguong } from './nguong.js';

export { MO_HINH, NGHI_NGAN, LoiGoi };

/** Trần gói gửi lên. Rộng cho một nút thật, đủ chặn một gói bất thường. */
export const TOI_DA_TU_VON = 400;
export const TOI_DA_CHU_NHAN = 200;
/* NG27 · trần số câu một gói — ĐỌC LÚC DÙNG (Bảng 4.7, điểm 5). Trước 22-11 gõ cứng
   4, cùng con số với `SO_CAU_PHU_DAO` của máy con nhưng hai nơi hai hằng: chuyên gia
   nâng bài phụ đạo lên 5 câu thì máy con xin 5, máy chủ bác vì "phải từ 1 tới 4".
   Nay cả hai đọc NG27; máy chủ tra theo khối lớp gói khai (máy con xin theo khối lớp
   của phiên), để một giá trị riêng của lớp 3 không bị trần toàn hệ chặn. */
export const soCauToiDa = (bo = boNguong(), nc = {}) => layNguong(bo, 'NG27', nc);
export const SO_CAU_TOI_DA = soCauToiDa();
/* Ngân sách token theo số câu: 700 cho 4 câu như cũ, nới theo khi NG27 lớn hơn. */
export const TOKEN_PHU_DAO = 700;
export const tokenPhuDao = (soCau) => Math.max(TOKEN_PHU_DAO, Math.ceil((TOKEN_PHU_DAO / 4) * soCau));

/**
 * Soi gói máy con gửi lên. Trả gói đã sạch, hoặc ném `LoiGoi`.
 *
 * Tách khỏi phần gọi mạng để chạy được bằng `node` mà không cần khoá — chỗ dễ sai
 * ở đây là mấy con số chốt cửa, mà chúng không cần mạng để thử.
 */
export function soiGoiPhuDao(du, bo = boNguong()) {
  const nhan = String(du?.nhan ?? '').trim();
  const soCau = Number(du?.soCau);
  const vonTu = Array.isArray(du?.vonTu) ? du.vonTu : null;
  const mauCau = Array.isArray(du?.mauCau) ? du.mauCau : [];
  if (!nhan) throw new LoiGoi('thieu-nhan', 'Thiếu tên chỗ cần ôn.');
  if (nhan.length > TOI_DA_CHU_NHAN) {
    throw new LoiGoi('nhan-qua-dai', `Tên chỗ cần ôn dài quá ${TOI_DA_CHU_NHAN} ký tự.`);
  }
  if (!vonTu || !vonTu.length) throw new LoiGoi('thieu-von', 'Thiếu vốn từ của bài.');
  if (vonTu.length > TOI_DA_TU_VON) {
    throw new LoiGoi('von-qua-lon', `Vốn từ nhiều quá ${TOI_DA_TU_VON} mục.`);
  }
  const lop = Number(du?.lop) || 1;
  const tran = soCauToiDa(bo, { mon: 'tienganh', khoiLop: String(lop) });
  if (!Number.isFinite(soCau) || soCau < 1 || soCau > tran) {
    throw new LoiGoi('so-cau-la', `Số câu phải từ 1 tới ${tran}.`);
  }
  return {
    nhan,
    soCau: Math.floor(soCau),
    lop,
    vonTu: vonTu.map((v) => ({ tu: String(v?.tu ?? v ?? ''), nghia: String(v?.nghia || '') }))
      .filter((v) => v.tu),
    mauCau: mauCau.map((x) => String(x || '')).filter(Boolean),
  };
}

/**
 * Lời dặn sinh câu phụ đạo.
 *
 * ⚠ ĐÒI ĐÚNG MỘT HÌNH DẠNG CÂU: bấm chọn, bốn phương án, một đáp án đúng. Thả cho
 * nó tự chọn hình dạng thì nó sinh ra câu điền-vào-ô — mà ô nhập chỉ dành cho SỐ
 * (luật của cả app), và một câu đòi bé GÕ CHỮ tiếng Anh là bắt bé tự nghĩ ra chính
 * tả của một chữ nó đang mắc.
 */
export function loiDanSinhPhuDao({ nhan, vonTu, mauCau, soCau, lop }) {
  const bang = vonTu.map((v) => `${v.tu}${v.nghia ? ` (${v.nghia})` : ''}`).join(' · ');
  return [
    `Bạn là cô giáo tiếng Anh tiểu học, soạn câu ÔN LẠI cho một bé lớp ${lop} người Việt.`,
    '',
    `CHỖ BÉ ĐANG MẮC: ${nhan}`,
    '',
    'VỐN TỪ BÉ ĐÃ HỌC — đây là TOÀN BỘ tiếng Anh bé biết:',
    bang,
    '',
    ...(mauCau.length ? ['MẪU CÂU BÉ ĐÃ HỌC:', ...mauCau.map((x) => `- ${x}`), ''] : []),
    `VIỆC: soạn ĐÚNG ${soCau} câu bấm chọn để gỡ đúng chỗ ấy.`,
    '',
    'LUẬT — theo đủ, không bỏ điều nào:',
    '1. MỌI chữ tiếng Anh trong câu CHỈ ĐƯỢC lấy từ bảng vốn từ ở trên.',
    '   Tuyệt đối không dạy từ mới, dù từ ấy hay hơn.',
    '2. Mỗi câu: lời dẫn TIẾNG VIỆT ngắn, và 4 phương án tiếng Anh, đúng 1 phương',
    '   án đúng. Phương án nhiễu phải là cái SAI TRẺ HAY MẮC ở chỗ này, không phải',
    '   một chữ bừa.',
    '3. Dễ trước, khó sau. Bé đang mắc thì câu đầu phải là câu bé làm được.',
    '4. KHÔNG câu điền vào ô, KHÔNG câu tự luận — chỉ bấm chọn.',
    '5. Không dùng số trong lời dẫn.',
    '',
    'TRẢ LỜI ĐÚNG MỘT KHỐI JSON, không thêm chữ nào ngoài khối:',
    '{"cau":[{"text":"…","choices":["…","…","…","…"],"answer":"…","hint":"…"}]}',
    '- "text", "hint": TIẾNG VIỆT.  - "choices", "answer": TIẾNG ANH.',
    '- "answer" PHẢI là một trong "choices".',
  ].join('\n');
}

/** Khung của lời dặn — dựng bằng CHÍNH hàm trên với phần riêng để rỗng. */
export const khungPhuDao = (lop, soCau, coMauCau) => loiDanSinhPhuDao({
  nhan: '', vonTu: [], mauCau: coMauCau ? ['—'] : [], soCau, lop,
});

export async function sinhPhuDao(du, taoClient, bo = boNguong()) {
  const goi = soiGoiPhuDao(du, bo);
  const token = tokenPhuDao(goi.soCau);
  const client = taoClient();
  const kq = await goiDoiJson(client, {
    model: MO_HINH,
    messages: [{ role: 'system', content: loiDanSinhPhuDao(goi) }],
    temperature: 0.3,
    max_tokens: token,
    reasoning_effort: NGHI_NGAN,
  });
  const chon = kq?.choices?.[0];
  const chu = chon?.message?.content || '';
  if (!chu.trim()) {
    throw new LoiGoi('tra-loi-rong',
      `Máy soạn bài không trả lời được (finish_reason: ${chon?.finish_reason || 'không rõ'}).`);
  }
  /* Trả CHỮ TRẦN: việc bóc JSON và HẬU KIỂM là của máy con (`lib/goiPhuDao.js` +
     `cauHoiHopLe`, có cổng canh) — đúng một chỗ biết hình dạng câu trả lời, và hậu
     kiểm phải nằm cùng phía với vốn từ đầy đủ của bài. */
  return {
    chu,
    moHinh: MO_HINH,
    ...vanTay('phudao', khungPhuDao(goi.lop, goi.soCau, goi.mauCau.length > 0), {
      moHinh: MO_HINH, nhiet: 0.3, token,
    }),
  };
}
