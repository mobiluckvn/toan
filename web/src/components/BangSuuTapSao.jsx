import React from 'react';

/**
 * BẢNG SƯU TẬP SAO — mỗi chương học xong là một ngôi sao sáng lên.
 *
 * Cuối sách in bảng này (image7.png) để bé DÁN STICKER sau mỗi chặng. Trong app
 * thì tiến trình đã biết bé học tới đâu, nên sao tự sáng — không cần bé tự đánh dấu.
 *
 * Sách đếm chặng là "8 chương · 3 ải cuối". Ở đây mới có 8 chương: 3 ải chưa
 * trích vào app nên KHÔNG vẽ sẵn ô trống cho chúng — hứa rồi không có thì bé đợi.
 */
export default function BangSuuTapSao({ idx, xong }) {
  if (!idx?.length) return null;

  const chuong = new Map();
  for (const b of idx) {
    const c = chuong.get(b.chuong) || { ten: b.tenChuong, tong: 0, xong: 0 };
    c.tong += 1;
    if (xong[b.id]?.pass) c.xong += 1;
    chuong.set(b.chuong, c);
  }
  const ds = [...chuong.entries()].sort((a, b) => a[0] - b[0]);
  const duoc = ds.filter(([, c]) => c.xong === c.tong).length;

  return (
    <section className="card">
      <div className="kicker">⭐ BẢNG SƯU TẬP SAO CỦA CON</div>
      <p className="text-[14px] leading-snug text-mute">
        Học hết một chương là con được một ngôi sao.
      </p>

      <div className="mt-3 flex flex-wrap justify-center gap-2">
        {ds.map(([so, c]) => {
          const day = c.xong === c.tong;
          return (
            <div key={so} className="flex w-[62px] flex-col items-center" title={c.ten}>
              <span className={`text-[30px] leading-none ${day ? '' : 'opacity-25 grayscale'}`}>
                ⭐
              </span>
              <span className="mt-0.5 text-[11px] font-bold text-navy">Ch. {so}</span>
              <span className="text-[10.5px] text-mute">{c.xong}/{c.tong}</span>
            </div>
          );
        })}
      </div>

      <p className="mt-2.5 text-center text-[13.5px] font-bold text-teal-dark">
        {duoc === ds.length
          ? 'Đủ 8 sao — con là nhà vô địch Vương quốc Số! 🏆'
          : `Con đã có ${duoc} trên ${ds.length} ngôi sao`}
      </p>
    </section>
  );
}
