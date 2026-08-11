import React, { useState } from 'react';
import { LOP_HOC } from '../lib/soQuyen.js';
import { dsNguoi, tenHien, chuDau } from '../lib/nguoiDung.js';

/**
 * HỒ SƠ CỦA CON — một chỗ duy nhất cho "con là ai" và "sửa lại chỗ khai sai".
 *
 * Trước đây ba việc này nằm rải: đổi biệt danh lọt trong màn Bảng xếp hạng (bố mẹ
 * không ai tìm ra), còn LỚP thì chỉ hỏi đúng một lần ở màn chào — chọn nhầm là chịu,
 * không màn nào sửa được. Mà con số ấy đi thẳng vào bảng xếp hạng và vào bậc xuất
 * phát của vòng luyện chủ đề, nên khai nhầm là sai suốt.
 *
 * Màn này cũng là chỗ trả lời câu "máy đang mở tài khoản của ai" — trước chỉ có mỗi
 * chữ "thoát" bé xíu ở góc, không hề nói tên.
 */
export default function HoSoCon({
  hoSo, email, onLuu, onExit, onDoiNguoi, onSignOut,
}) {
  const [ten, setTen] = useState(hoSo?.displayName || '');
  const [lop, setLop] = useState(Number(hoSo?.grade) || 0);
  const [bietDanh, setBietDanh] = useState(hoSo?.bietDanh || '');
  const [dangLuu, setDangLuu] = useState(false);
  const [xong, setXong] = useState(false);

  const doi = (v) => { setXong(false); return v; };
  const coDoi = (ten.trim() !== (hoSo?.displayName || ''))
    || (lop !== (Number(hoSo?.grade) || 0))
    || (bietDanh.trim() !== (hoSo?.bietDanh || ''));

  const luu = async () => {
    setDangLuu(true);
    try {
      await onLuu({
        displayName: ten.trim(),
        grade: lop,
        bietDanh: bietDanh.trim(),
      });
      setXong(true);
    } finally { setDangLuu(false); }
  };

  const soNguoi = dsNguoi().length;

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[520px] px-3.5 py-4">
      <button onClick={onExit} className="pill bg-soft text-navy">← Về kệ sách</button>

      {/* ĐANG LÀ AI — câu trả lời phải nằm ngay trên cùng, to và rõ */}
      <div className="card mt-3 flex items-center gap-3">
        <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-navy text-[24px] font-extrabold text-white">
          {chuDau({ ten: hoSo?.displayName, email })}
        </span>
        <span className="min-w-0 flex-1">
          <div className="kicker">MÁY ĐANG MỞ TÀI KHOẢN CỦA</div>
          <b className="block truncate text-[17px] text-navy">
            {tenHien({ ten: hoSo?.displayName, email })}
          </b>
          <span className="block truncate text-[12.5px] text-mute">
            {hoSo?.grade ? `Lớp ${hoSo.grade}` : 'chưa chọn lớp'}{email ? ` · ${email}` : ''}
          </span>
        </span>
      </div>

      <div className="card mt-3">
        <div className="kicker">SỬA LẠI CHO ĐÚNG</div>

        <label className="field mt-2 block">
          <span className="field-head">Tên con</span>
          <input className="numin w-full text-[16px]" maxLength={40} placeholder="vd: Minh An"
                 value={ten} onChange={(e) => setTen(doi(e.target.value))} />
        </label>

        <div className="field mt-2.5">
          <span className="field-head">Con đang học lớp</span>
          <div className="grid grid-cols-6 gap-1.5">
            {LOP_HOC.map((g) => (
              <button key={g} type="button" onClick={() => setLop(doi(g))}
                aria-label={`Lớp ${g}`} aria-pressed={lop === g}
                className={`rounded-xl border-[1.5px] py-2 text-[15px] font-bold ${
                  lop === g ? 'border-navy bg-navy text-white' : 'border-line bg-white text-navy'}`}>
                {g}
              </button>
            ))}
          </div>
          {lop > 5 && (
            <p className="mt-2 rounded-xl bg-gold-pale px-3 py-2 text-[12.5px] leading-relaxed text-gold-dark">
              Sách cho lớp {lop} đang được biên soạn — con vẫn học được các quyển đang có.
            </p>
          )}
        </div>

        <label className="field mt-2.5 block">
          <span className="field-head">Biệt danh trên bảng xếp hạng</span>
          <input className="numin w-full text-[16px]" maxLength={24}
                 placeholder={ten.trim() || 'để trống thì lấy tên con'}
                 value={bietDanh} onChange={(e) => setBietDanh(doi(e.target.value))} />
          <span className="mt-1 block text-[12px] text-mute">
            Các bạn khác chỉ nhìn thấy biệt danh, lớp và số sao — không thấy tên thật
            hay email của con.
          </span>
        </label>

        <button className="btn-go mt-3.5 w-full" disabled={dangLuu || !coDoi} onClick={luu}>
          {dangLuu ? 'đang lưu…' : xong ? 'Đã lưu ✓' : 'Lưu lại'}
        </button>
      </div>

      <div className="card mt-3">
        <div className="kicker">TÀI KHOẢN</div>
        {/* Nút này phải hiện KỂ CẢ khi máy mới có một bé — nếu không thì bé đầu tiên
            không có đường nào thêm em mình vào, mà đó chính là lúc cần nó nhất. */}
        <button className="btn-ghost mt-2 w-full" onClick={onDoiNguoi}>
          {soNguoi > 1
            ? `🔄 Đổi sang bé khác (${soNguoi} bé trên máy này)`
            : '＋ Thêm bé nữa vào máy này'}
        </button>
        <button className="btn-ghost mt-2 w-full text-alert" onClick={onSignOut}>
          Thoát khỏi tài khoản này
        </button>
        <p className="mt-2 text-[12px] leading-relaxed text-mute">
          Thoát ra thì bài đã học vẫn còn nguyên trên mạng — đăng nhập lại là thấy lại đủ.
        </p>
      </div>
    </div>
  );
}
