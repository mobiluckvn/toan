import React from 'react';
import { bamDuocDot } from '../lib/flow.js';

/**
 * THANH TIẾN TRÌNH — con nhìn là biết bài có mấy phần, đang ở đâu, còn bao nhiêu.
 *
 * Thanh cũ là một vạch gradient chạy dần: con thấy "được khoảng một nửa" nhưng
 * không biết một nửa của MẤY phần, và cũng không bấm vào đâu được. Nay mỗi bước
 * một đốt:
 *   · đã học   → xanh đậm, BẤM ĐƯỢC để quay lại xem hoặc làm lại
 *   · đang học → đốt cao hơn, viền đậm, cho biết con đứng chỗ nào
 *   · chưa học → xanh mờ, không bấm được (bấm vượt lên là bỏ qua bài giảng)
 *
 * Chỉ cho quay lại chỗ ĐÃ ĐI QUA (daDi), không cho nhảy cóc về trước — cổng
 * mustPass và mạch giảng bài sẽ vô nghĩa nếu con bấm thẳng tới phần sát hạch.
 */
export default function TienTrinh({ tong, hienTai, daDi, nhan = [], onChon, onLui }) {
  if (!tong) return null;
  const conLai = tong - hienTai - 1;

  return (
    <div className="border-b border-line bg-white px-3 pb-1.5 pt-2">
      <div className="mb-1 flex items-center gap-2 text-[11.5px]">
        {/* Bài vốn chỉ đi MỘT CHIỀU: lỡ tay bấm Tiếp là mất luôn phần vừa đọc,
            muốn xem lại hay làm lại cũng chịu. Nút này luôn ở một chỗ cố định. */}
        <button
          type="button" disabled={hienTai === 0} onClick={() => onLui?.()}
          className="rounded-full border-[1.5px] border-navy px-2.5 py-0.5 font-bold text-navy
                     disabled:border-line disabled:text-mute disabled:opacity-45">
          ◀ Quay lại
        </button>
        <span className="flex-1 text-center font-bold text-navy">
          Phần {hienTai + 1} trên {tong}
        </span>
        <span className="text-right text-mute">
          {conLai > 0 ? `còn ${conLai}` : 'phần cuối!'}
        </span>
      </div>

      <div className="flex items-end gap-[2px]" role="list">
        {Array.from({ length: tong }, (_, k) => {
          const dangHoc = k === hienTai;
          const daHoc = k < hienTai;
          const bamDuoc = bamDuocDot(k, hienTai, daDi);
          const ten = nhan[k] ? `${nhan[k]} — phần ${k + 1}` : `phần ${k + 1}`;
          return (
            <button
              key={k} type="button" role="listitem"
              aria-label={ten + (daHoc ? ' (đã học)' : dangHoc ? ' (đang học)' : ' (chưa học)')}
              aria-current={dangHoc ? 'step' : undefined}
              title={ten}
              disabled={!bamDuoc}
              onClick={() => bamDuoc && onChon?.(k)}
              className={`flex-1 rounded-full transition-all ${
                dangHoc ? 'h-[9px] bg-teal ring-2 ring-navy'
                  : daHoc ? 'h-[6px] bg-teal hover:h-[9px]'
                  : k <= daDi ? 'h-[6px] bg-teal/40'
                  : 'h-[6px] bg-teal-pale'
              } ${bamDuoc ? 'cursor-pointer' : 'cursor-default'}`}
            />
          );
        })}
      </div>
    </div>
  );
}
