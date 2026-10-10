import { capNhatBKT, layNguong } from './nguong.js';

/**
 * NGƯỜI HỌC MÔ PHỎNG — kịch bản KB1 của Bảng 3.24.
 *
 * KB1: «hiệu chỉnh tham số θ, α, h và tạo bộ ngưỡng đề xuất đầu tiên — 1.000 người
 * học mô phỏng, quét lưới». Mức sẵn sàng luận văn ghi là «cao», và nó đúng: hàm
 * học ngưỡng đã chạy được trên dữ liệu thật, chỉ thiếu đủ CỠ MẪU ở những ngưỡng mà
 * nhật ký hiện có nói được quá ít (NG06 và NG07 mới có 46 lượt, cần 200).
 *
 * ── ⚠ DỮ LIỆU MÔ PHỎNG KHÔNG ĐƯỢC LẪN VÀO DỮ LIỆU THẬT ──
 * Đây là chốt lớn nhất của cả tệp. Lượt mô phỏng mà trôi vào `attempts` thì:
 *   · mọi chỉ số của Bảng 3.22 nói về một đám trẻ không tồn tại;
 *   · hàm học ngưỡng đề xuất theo chúng, và chuyên gia duyệt một con số học từ
 *     một mô hình học từ chính nó;
 *   · không có đường lùi, vì nhật ký là BẤT BIẾN.
 * Nên tệp này KHÔNG ghi Firestore và không nhận `db`. Nó trả về một MẢNG trong bộ
 * nhớ; bên gọi (`tools/kb1_quet_luoi.mjs`) truyền thẳng vào `hocMoiPhamVi`.
 * Mọi lượt còn mang `moPhong: true` để nếu một ngày nào đó có ai ghi chúng xuống
 * thì ít nhất lọc ra được.
 *
 * ── ⚠ MÔ PHỎNG CHỈ TRẢ LỜI ĐƯỢC CÂU «VỚI MÔ HÌNH NÀY THÌ NGƯỠNG NÀO HỢP» ──
 * Nó KHÔNG trả lời được «ngưỡng nào dạy trẻ tốt hơn». Trẻ mô phỏng học đúng theo
 * BKT vì ta bảo nó thế; chạy quét lưới trên đó rồi kết luận về việc dạy học là lấy
 * giả thiết làm kết luận. Giá trị thật của KB1 nằm ở chỗ khác: nó cho biết một bộ
 * ngưỡng dẫn tới NHỊP DẠY nào — mấy câu tới khi công nhận, bao nhiêu lần công nhận
 * sớm — và nhịp ấy thì chuyên gia đọc được và bác được.
 */

/** Sinh số giả tất định — chạy hai lần phải ra hai tập y hệt. */
export function taoNgauNhien(seed = 1) {
  let s = (seed >>> 0) || 1;
  return () => {
    s = (Math.imul(s, 1103515245) + 12345) >>> 0;
    return s / 4294967296;
  };
}

export const MAC_DINH = {
  soBe: 1000,
  soNutMoiBe: 6,
  soLuotMoiNut: 14,
  moiBuoi: 4,          // mấy lượt một buổi
  cachNgay: 2,         // hai buổi cách nhau mấy ngày
  /* ── ⚠ THẾ GIỚI MÔ PHỎNG PHẢI CÓ CHU KỲ BÁN RÃ RIÊNG ──
     Bản đầu của tệp này không cho trẻ mô phỏng QUÊN — BKT chuẩn không có đường về
     từ «đã thạo» sang «chưa thạo». Chạy KB1 trên nó thì NG06 ra đúng 60 và NG07 ra
     đúng 0,70: cả hai đụng BIÊN của khoảng hợp lệ. Hợp lẽ thôi — trong một thế giới
     không ai quên thì bán rã càng dài càng khớp, và θ càng thấp càng lợi vì công
     nhận sớm không bao giờ phải trả giá.

     Hai con số đụng biên ấy KHÔNG phải kết quả hiệu chỉnh; chúng là lời khai rằng
     mô phỏng không nói được gì về hai ngưỡng kia.

     ⚠ VÀ `nuaDoiThat` PHẢI ĐỘC LẬP VỚI NG06. Lấy chính NG06 làm chu kỳ của thế giới
     rồi đi tìm lại NG06 là vòng tròn: ta sẽ luôn «tìm thấy» đúng thứ đã giả thiết.
     Mặc định 10 ngày, khác hẳn NG06 = 14, nên phép quét lưới có chỗ để sai. */
  nuaDoiThat: 10,
  /* Bé không giống nhau: mỗi bé một hệ số học, rải quanh 1. Không có nó thì mọi
     chuỗi na ná nhau và quét lưới thấy một thế giới đều tăm tắp — trong khi chỗ
     ngưỡng thật sự phải phân xử là chỗ bé nhanh và bé chậm cùng tồn tại. */
  taiNangLech: 0.5,
  dangCau: ['chon', 'go', 'the', 'tf'],
  bac: [1, 2, 3, 4],
  /* Thời gian trả lời theo DẠNG CÂU — gõ chữ lâu hơn bấm chọn. Bản đầu dùng một
     con số chung, nên NG16 ra y hệt nhau cho cả bốn dạng, trong khi dữ liệu THẬT
     chênh nhau gấp chín lần. Một mô phỏng không tái tạo nổi tính chất ấy thì không
     dùng để hiệu chỉnh ngưỡng của chính tính chất ấy được. */
  giayTheoDang: { chon: 5, tf: 4, the: 11, go: 16, chondapan: 7, so: 13, bieuthuc: 22 },
};

/**
 * Sinh nhật ký lượt cho `soBe` người học mô phỏng.
 *
 * Trẻ mô phỏng đi đúng theo BKT: trạng thái ẩn «đã thạo / chưa thạo», chuyển một
 * chiều với xác suất T, quan sát nhiễu bởi slip và guess. Tham số lấy từ CHÍNH bộ
 * ngưỡng truyền vào, nên đổi bộ là đổi cả thế giới mô phỏng — đúng ý: ta muốn hỏi
 * «nếu thế giới đúng như bộ tham số ta tin, thì ngưỡng nào hợp».
 *
 * ⚠ `guess` lấy theo DẠNG CÂU. Câu bốn lựa chọn đoán trúng khác hẳn câu gõ chữ, và
 * nhập chúng làm một thì quét lưới cho NG16/NG04 ra một con số không mô tả dạng nào.
 */
export function sinhNhatKy(bo, {
  soBe = MAC_DINH.soBe, soNutMoiBe = MAC_DINH.soNutMoiBe,
  soLuotMoiNut = MAC_DINH.soLuotMoiNut, moiBuoi = MAC_DINH.moiBuoi,
  cachNgay = MAC_DINH.cachNgay, taiNangLech = MAC_DINH.taiNangLech,
  dangCau = MAC_DINH.dangCau, bac = MAC_DINH.bac,
  nuaDoiThat = MAC_DINH.nuaDoiThat, giayTheoDang = MAC_DINH.giayTheoDang,
  mocDau = Date.UTC(2026, 0, 1), seed = 20261010,
} = {}) {
  const rnd = taoNgauNhien(seed);
  const NGAY = 86400000;
  const luots = [];

  for (let b = 0; b < soBe; b += 1) {
    /* Hệ số học của bé này — nhân vào T. Kẹp để không ai học tức thì hay không bao
       giờ học được: cả hai đầu đều là những đứa trẻ không có thật. */
    const tai = Math.min(2.5, Math.max(0.25, 1 + (rnd() - 0.5) * 2 * taiNangLech));
    for (let n = 0; n < soNutMoiBe; n += 1) {
      const dang = dangCau[Math.floor(rnd() * dangCau.length)];
      const bacNay = bac[Math.floor(rnd() * bac.length)];
      const nc = { dangCau: dang, bac: String(bacNay) };
      const L0 = layNguong(bo, 'NG01', nc);
      const T = layNguong(bo, 'NG02', nc);
      const slip = layNguong(bo, 'NG03', nc);
      const guess = layNguong(bo, 'NG04', nc);

      let thao = rnd() < L0;
      let buoiTruoc = -1;
      for (let t = 0; t < soLuotMoiNut; t += 1) {
        const buoi = Math.floor(t / moiBuoi);
        /* ── QUÊN GIỮA HAI BUỔI ──
           Xác suất còn giữ được = 2^(−Δt / nuaDoiThat). Đây là thứ làm cho việc
           công nhận quá sớm có GIÁ: nút được công nhận khi bé chưa thật vững thì
           vài ngày sau bé làm sai, và chỉ số «công nhận sớm» mới có ý nghĩa. */
        if (thao && buoiTruoc >= 0 && buoi > buoiTruoc) {
          const cach = (buoi - buoiTruoc) * cachNgay;
          if (rnd() > 2 ** (-cach / nuaDoiThat)) thao = false;
        }
        buoiTruoc = buoi;
        const dung = thao ? rnd() > slip : rnd() < guess;
        luots.push({
          learnerId: `mp_${b}`,
          bktUnit: `mp_nut_${n}`,
          correct: dung,
          ts: mocDau + buoi * cachNgay * NGAY + (t % moiBuoi) * 60000 + b * 1000,
          mon: 'tienganh',
          khoiLop: String(1 + (b % 5)),
          mode: dang,
          bac: bacNay,
          /* Thời gian trả lời: theo DẠNG CÂU, và chậm hơn khi chưa thạo. */
          ms: Math.round((giayTheoDang[dang] ?? 8) * 1000
            * (thao ? 1 : 2.2) * (0.6 + rnd() * 0.8)),
          sauPhuDao: false,
          moPhong: true,
        });
        if (!thao && rnd() < Math.min(0.95, T * tai)) thao = true;
      }
    }
  }
  return luots;
}

/**
 * NHỊP DẠY mà một bộ ngưỡng dẫn tới — thứ chuyên gia đọc được và bác được.
 *
 * Trả về cho mỗi θ: mấy câu tới khi công nhận, tỉ lệ công nhận sớm, và tỉ lệ nút
 * được công nhận. Ba con số ấy nói về việc DẠY, còn bản thân θ thì không.
 */
export function nhipDay(luots, bo, theta) {
  const nhom = new Map();
  for (const a of luots) {
    const k = `${a.learnerId}::${a.bktUnit}`;
    if (!nhom.has(k)) nhom.set(k, []);
    nhom.get(k).push(a);
  }
  const NGAY = 86400000;
  let toiThao = 0;
  let soThao = 0;
  let soXet = 0;
  let somSai = 0;
  let soSom = 0;

  for (const ds of nhom.values()) {
    ds.sort((x, y) => x.ts - y.ts);
    soXet += 1;
    const nc = { dangCau: ds[0].mode, bac: String(ds[0].bac) };
    const ts = {
      L0: layNguong(bo, 'NG01', nc), T: layNguong(bo, 'NG02', nc),
      slip: layNguong(bo, 'NG03', nc), guess: layNguong(bo, 'NG04', nc),
    };
    let p = ts.L0;
    for (let i = 0; i < ds.length; i += 1) {
      p = capNhatBKT(p, !!ds[i].correct, ts);
      if (p < theta) continue;
      soThao += 1;
      toiThao += i + 1;
      const sau = ds.slice(i + 1).find((x) => x.ts - ds[i].ts >= NGAY);
      if (sau) { soSom += 1; if (!sau.correct) somSai += 1; }
      break;
    }
  }

  return {
    theta,
    soCauToiThao: soThao ? +(toiThao / soThao).toFixed(2) : null,
    tiLeDuocCongNhan: soXet ? +(soThao / soXet).toFixed(4) : null,
    tiLeCongNhanSom: soSom ? +(somSai / soSom).toFixed(4) : null,
    coMauSom: soSom,
    coMauThao: soThao,
  };
}
