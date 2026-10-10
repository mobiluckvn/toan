import React from 'react';

/**
 * LƯỚI ĐỠ KHI MÀN HÌNH VỠ — thay màn trắng bằng một câu bé đọc được.
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 * Hai lần một `ReferenceError` lên tới bản thật và làm màn trắng hoàn toàn: một lần
 * hook đặt sau `return` sớm (React lỗi 310), một lần biến dùng trước khi khai (TDZ)
 * ở Phòng luyện nói. Cả hai lần, 103 cổng và bản dựng đều XANH — kho này không có
 * cổng nào dựng một màn React, và không có ESLint.
 *
 * Lưới đỡ không sửa được lỗi. Nó sửa HẬU QUẢ: thay vì một trang trắng không nói gì,
 * bé thấy một câu và một nút bấm được, còn người lớn thấy đủ chữ để đi tìm.
 *
 * ── ⚠ KHÔNG NUỐT LỖI ──
 * Vẫn `console.error` nguyên vẹn. Lưới đỡ mà im lặng thì nó che mất chính thứ nó
 * đang đỡ: màn vẫn hỏng, chỉ là hỏng đẹp hơn, và không ai biết để đi sửa.
 *
 * ── ⚠ KHÔNG HIỆN CHI TIẾT LỖI CHO BÉ ──
 * Vết gọi hàm là chữ của người lớn, và có thể lộ đường dẫn nội bộ. Bé thấy một câu
 * tiếng Việt và hai nút; chi tiết nằm trong console, nơi người lớn mở được.
 *
 * ── ⚠ CÓ NÚT "HỌC TIẾP", KHÔNG CHỈ CÓ "TẢI LẠI" ──
 * Tải lại trang mà lỗi nằm ở màn đầu thì bé quay về đúng chỗ vỡ, lặp vô tận. Nút thứ
 * hai dựng lại cây giao diện từ đầu (`khoa` đổi) và đưa về kệ sách — một đường ra
 * mà bé tự đi được.
 */
export default class LuoiDoLoi extends React.Component {
  constructor(props) {
    super(props);
    this.state = { vo: false, khoa: 0 };
  }

  static getDerivedStateFromError() {
    return { vo: true };
  }

  componentDidCatch(loi, chiTiet) {
    /* Nguyên văn, không rút gọn — đây là thứ duy nhất còn lại để lần ra. */
    console.error('[màn vỡ]', loi, chiTiet?.componentStack);
  }

  render() {
    /* `key` đổi là React VỨT cả cây cũ và dựng lại từ đầu. Không có nó thì mấy
       component con giữ nguyên state hỏng, và màn vỡ lại ngay lần vẽ kế tiếp. */
    if (!this.state.vo) {
      return <React.Fragment key={this.state.khoa}>{this.props.children}</React.Fragment>;
    }

    const veDau = () => {
      /* Dọn chỗ đứng trước khi dựng lại: một `view` trỏ vào màn vừa vỡ thì dựng lại
         bao nhiêu lần cũng vỡ lại bấy nhiêu. ⚠ CHỈ xoá chỗ đứng, KHÔNG đụng tới bài
         bé đã học — sổ tại máy là thứ duy nhất giữ công học khi chưa đăng nhập. */
      try { sessionStorage.clear(); } catch { /* chế độ riêng tư */ }
      this.setState((c) => ({ vo: false, khoa: c.khoa + 1 }));
      if (typeof this.props.veDau === 'function') this.props.veDau();
    };

    return (
      <div className="mx-auto flex max-w-lg flex-col gap-4 p-6 text-center">
        <p className="text-5xl" aria-hidden="true">🧰</p>
        <h1 className="text-xl font-bold text-ink">Màn này đang hỏng mất rồi</h1>
        <p className="text-mute">
          Không phải lỗi của con đâu. Bài con đã học vẫn còn nguyên — con bấm nút dưới
          để về kệ sách và học tiếp nhé.
        </p>
        <div className="flex flex-col gap-2">
          <button type="button" onClick={veDau}
            className="rounded-xl2 bg-navy px-4 py-3 font-semibold text-white
                       focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            Về kệ sách, học tiếp
          </button>
          <button type="button" onClick={() => window.location.reload()}
            className="text-sm text-mute underline">tải lại trang</button>
        </div>
        <p className="text-xs text-mute">
          Người lớn giúp con: mở Console của trình duyệt sẽ thấy dòng <b>[màn vỡ]</b> kèm
          chỗ hỏng.
        </p>
      </div>
    );
  }
}
