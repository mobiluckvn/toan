import React, { useState } from 'react';
import { LOP_HOC, LOP_MAC_DINH } from '../lib/content.js';

/**
 * LẦN ĐẦU ĐĂNG NHẬP — hỏi đúng hai thứ rồi cho vào học ngay.
 * Không hỏi gì thêm: mỗi ô hỏi thừa là một cơ hội để bố mẹ bỏ dở giữa chừng.
 *
 * Danh sách lớp lấy từ `LOP_HOC` (lớp 2 → 12), KHÔNG phải từ danh sách sách đang có.
 * Bản đầu chỉ cho chọn 4·5·6 — anh chị lớp 8 phải khai sai ngay ở màn đầu tiên, mà
 * con số ấy đi thẳng vào bảng xếp hạng lẫn vào bậc xuất phát của vòng luyện chủ đề.
 */
export default function ProfileSetup({ email, onSave, onSkip }) {
  const [name, setName] = useState('');
  const [grade, setGrade] = useState(LOP_MAC_DINH);
  const [busy, setBusy] = useState(false);

  const save = async () => {
    setBusy(true);
    try { await onSave({ displayName: name.trim(), grade }); }
    finally { setBusy(false); }
  };

  return (
    <div className="mx-auto flex min-h-[100dvh] max-w-[440px] flex-col justify-center px-4 py-8">
      <div className="card">
        <div className="kicker">CHÀO BẠN MỚI</div>
        <h1 className="text-[19px] font-bold leading-snug text-navy">Con tên là gì nhỉ?</h1>
        <p className="mt-1 text-[14px] leading-relaxed text-mute">
          Tên này hiện trong sổ học và trong bảng của thầy cô. Đổi lúc nào cũng được.
        </p>

        <label className="field mt-3.5 block">
          <span className="field-head">Tên con</span>
          <input className="numin w-full text-[16px]" autoFocus maxLength={40}
                 placeholder="vd: Minh An" value={name}
                 onChange={(e) => setName(e.target.value)}
                 onKeyDown={(e) => e.key === 'Enter' && name.trim() && !busy && save()} />
        </label>

        <div className="field mt-2.5">
          <span className="field-head">Con đang học lớp</span>
          {/* Lưới đều thay vì hàng cuộn: mười một nút xếp hai hàng cân nhau, bấm được
              bằng ngón tay, và nhìn một cái là thấy hết — không có nút nào nấp ngoài
              mép màn hình. Nhãn "Lớp" đã nằm ở dòng trên nên nút chỉ cần con số. */}
          <div className="grid grid-cols-6 gap-1.5">
            {LOP_HOC.map((g) => (
              <button key={g} type="button" onClick={() => setGrade(g)}
                aria-label={`Lớp ${g}`} aria-pressed={grade === g}
                className={`rounded-xl border-[1.5px] py-2 text-[15px] font-bold ${
                  grade === g ? 'border-navy bg-navy text-white' : 'border-line bg-white text-navy'}`}>
                {g}
              </button>
            ))}
          </div>
          {/* Nói thẳng là chưa có sách cho lớp trên — khai đúng lớp vẫn có ích (bảng
              xếp hạng và bậc luyện chủ đề dùng tới), nhưng đừng để anh chị lớp 8 chọn
              xong rồi đi tìm sách lớp 8 mà không thấy. */}
          {grade > 5 && (
            <p className="mt-2 rounded-xl bg-gold-pale px-3 py-2 text-[12.5px] leading-relaxed text-gold-dark">
              Sách cho lớp {grade} đang được biên soạn. Trong lúc chờ, con học được cả
              bốn quyển Toán Tư Duy lớp 2 – 5 và luyện theo chủ đề để chắc lại nền.
            </p>
          )}
        </div>

        <button className="btn-go mt-4" disabled={!name.trim() || busy} onClick={save}>
          {busy ? 'Đang lưu…' : 'Bắt đầu học ▶'}
        </button>

        <p className="mt-3 text-center text-[12px] text-mute">
          Đăng nhập bằng <b className="text-navy">{email}</b>
        </p>
      </div>

      <button className="mt-2 text-center text-[13px] text-mute underline" onClick={onSkip}>
        Để sau
      </button>
    </div>
  );
}
