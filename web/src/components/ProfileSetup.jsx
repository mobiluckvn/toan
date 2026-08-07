import React, { useState } from 'react';

/**
 * LẦN ĐẦU ĐĂNG NHẬP — hỏi đúng hai thứ rồi cho vào học ngay.
 * Không hỏi gì thêm: mỗi ô hỏi thừa là một cơ hội để bố mẹ bỏ dở giữa chừng.
 */
export default function ProfileSetup({ email, onSave, onSkip }) {
  const [name, setName] = useState('');
  const [grade, setGrade] = useState(5);
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
          <div className="flex flex-wrap gap-2">
            {[4, 5, 6].map((g) => (
              <button key={g} type="button" onClick={() => setGrade(g)}
                className={`rounded-full border-[1.5px] px-4 py-1.5 text-[14.5px] font-bold ${
                  grade === g ? 'border-navy bg-navy text-white' : 'border-line bg-white text-navy'}`}>
                Lớp {g}
              </button>
            ))}
          </div>
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
