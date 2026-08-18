import React from 'react';
import KHO from '../lib/hinh_ve.json';

/**
 * BẢY HÌNH VẼ TAY — chỗ emoji không diễn đạt nổi.
 *
 * 53/60 từ của lớp 1 dùng emoji: nhận ra ngay, không tốn dung lượng, nét ở mọi cỡ.
 * Bảy từ còn lại thì emoji chỉ GẦN đúng, và gần đúng với bé đang học từ mới là sai:
 *
 *     gate 🚧 biển công trường     head 👤 bóng người      hair 💇 đang cắt tóc
 *     top  🪀 yo-yo                lake 🏞️ phong cảnh chung
 *     run  🏃 · wash 🧼            động từ — emoji chỉ gợi một phần
 *
 * ── VÌ SAO NÉT VẼ NẰM Ở TỆP JSON, KHÔNG VIẾT THẲNG VÀO ĐÂY ──
 * Bản đầu vẽ bằng JSX nội tuyến. Đẹp, gọn, và có đúng một chỗ hỏng: VIDEO không
 * vẽ được. Pillow không dựng SVG, nên 7 từ này trong video hiện một thẻ chữ thay
 * cho hình — đúng cái mà cả bộ hình vẽ tay sinh ra để tránh.
 *
 * Cách chữa dễ nhất là vẽ lại 7 hình ấy bằng Pillow cho video. Cũng là cách sai
 * nhất: thành HAI bản vẽ của cùng một vật, và hai bản thì sớm muộn cũng lệch —
 * sửa cái cổng trên màn hình mà quên cái cổng trong video, không cổng nào bắt
 * được, chỉ có bé là thấy hai cái cổng khác nhau.
 *
 * Nên nét vẽ dọn sang `lib/hinh_ve.json`, và cả hai bên cùng đọc một tệp ấy:
 * màn hình đọc ở đây, video đọc bằng `tools/video/hinh_ve.py` rồi rasterize bằng
 * cairosvg. Sửa một chỗ là cả hai đổi theo.
 *
 * ── VỀ `dangerouslySetInnerHTML` ──
 * Nội dung đến từ tệp JSON của chính kho này, biên dịch vào bundle lúc dựng — nó
 * KHÔNG phải thứ người dùng nhập, cũng không tải về lúc chạy. Đây là chỗ dùng
 * đúng của nó: chèn một đoạn SVG mình tự viết.
 */
const BO = KHO.hinh || {};

export default function HinhVe({ ve, hinh, ten = '' }) {
  const v = ve && BO[ve];
  if (v) {
    return (
      <svg
        viewBox={KHO._khungNhin}
        role="img"
        aria-label={v.ten || ten}
        className="h-[1em] w-[1em]"
        style={{ display: 'block' }}
        dangerouslySetInnerHTML={{ __html: v.than }}
      />
    );
  }
  if (hinh) return <span role="img" aria-label={ten}>{hinh}</span>;
  /**
   * KHÔNG CÓ HÌNH THÌ HIỆN CHÍNH CHỮ ẤY, đừng vẽ ❔.
   *
   * Lớp 1·2 từ nào cũng có hình nên nhánh này gần như không chạy. Lớp 3 thì 51/204
   * từ không vẽ được (`hello` · `fine` · `my` · `this`), và Unit 1 thì KHÔNG TỪ NÀO
   * có hình — cả màn thành một rừng dấu hỏi giống hệt nhau: thanh việc mất công
   * dụng, thẻ từ hiện một ô trống to bằng bàn tay, và bé ngồi đợi tranh hiện ra.
   *
   * Cỡ chữ tính bằng `em` nên nó co theo chỗ gọi: ô nhỏ trên thanh việc thì chữ
   * nhỏ, thẻ từ `text-7xl` thì chữ to. Một nhánh, mọi chỗ gọi cùng đúng.
   */
  return (
    <span aria-label={ten}
      className="block max-w-[3.2em] truncate text-[0.32em] font-bold leading-tight text-navy">
      {ten || '❔'}
    </span>
  );
}

export const COI_HINH = Object.keys(BO);
