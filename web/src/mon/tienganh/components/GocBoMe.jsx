import React, { useState } from 'react';

/**
 * GÓC BỐ MẸ — chỗ cất mọi lời giải thích dài bằng tiếng Việt.
 *
 * ── VÌ SAO CÓ KHỐI NÀY ──
 * Đếm thật một bài: bé phải nhìn **2 029 ký tự tiếng Việt**. Mà bé lớp 1 chưa đọc
 * sõi tiếng Việt — nghĩa là toàn bộ số chữ ấy, với bé, chỉ là những mảng xám choán
 * chỗ. Chúng không vô dụng: bố mẹ và cô giáo cần chúng để biết bài đang dạy gì.
 * Chỉ là chúng KHÔNG PHẢI thứ bé nhìn vào.
 *
 * Nên chữ chia làm hai loại, và chỉ hai:
 *   · bé nhìn  — chữ TIẾNG ANH (mặt chữ chính là bài học) + nhãn nút ngắn
 *   · bố mẹ đọc — mọi giải thích, mẹo, lời dặn → cất vào đây, GẬP LẠI mặc định
 *
 * ── GẬP LẠI, KHÔNG PHẢI GIẤU ĐI ──
 * Vẫn phải thấy có cái gì ở đó, và mở được bằng một lần bấm. Giấu hẳn thì bố mẹ
 * ngồi cạnh không biết con đang học gì — mà đó mới là người quyết định con có học
 * tiếp hay không.
 */
export default function GocBoMe({ ten = 'Góc bố mẹ', children, moSan = false }) {
  const [mo, datMo] = useState(moSan);
  if (!children) return null;
  return (
    <div className="rounded-xl2 border border-line bg-white/60">
      <button
        type="button"
        onClick={() => datMo(!mo)}
        aria-expanded={mo}
        className="flex w-full items-center gap-2 px-4 py-2.5 text-left text-sm
          font-semibold text-mute hover:text-navy
          focus:outline-none focus-visible:ring-4 focus-visible:ring-gold"
      >
        <span aria-hidden="true">{mo ? '▾' : '▸'}</span>
        <span aria-hidden="true">👨‍👩‍👧</span>
        <span className="flex-1">{ten}</span>
        <span className="text-xs font-normal">{mo ? 'thu lại' : 'mở ra'}</span>
      </button>
      {mo && (
        <div className="flex flex-col gap-3 border-t border-line px-4 py-3 text-sm text-ink">
          {children}
        </div>
      )}
    </div>
  );
}

/** Một mục trong góc bố mẹ — nhãn nhỏ, nội dung thường. */
export function MucBoMe({ nhan, children }) {
  if (!children) return null;
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-wider text-mute">{nhan}</p>
      <div className="mt-0.5">{children}</div>
    </div>
  );
}
