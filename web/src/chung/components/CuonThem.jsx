import React, { useEffect, useState } from 'react';

/**
 * "CÒN NỮA Ở DƯỚI" — dấu hiệu cho con biết trang chưa hết.
 *
 * Nút đi tiếp dán cứng ở chân màn hình, nên khi nội dung dài hơn màn hình thì phần
 * còn lại bị cắt ngay tại vạch chân — nhìn vào tưởng đã hết bài. Con không cuộn,
 * bỏ qua luôn phần dưới rồi bấm tiếp.
 *
 * Hai lớp gợi ý, đều tự tắt khi con đã cuộn tới cuối:
 *   · một dải mờ ngay trên chân màn hình — chữ "chìm dần" cho thấy còn tiếp
 *   · một viên nhắc "kéo xuống, còn nữa" bấm được để tự cuộn
 */
export default function CuonThem({ chanCao = 76 }) {
  const [con, setCon] = useState(false);

  useEffect(() => {
    const do_ = () => {
      const el = document.documentElement;
      // còn ít nhất một dòng chữ nữa nằm dưới vạch chân màn hình
      setCon(el.scrollHeight - window.scrollY - window.innerHeight > chanCao + 24);
    };
    do_();
    window.addEventListener('scroll', do_, { passive: true });
    window.addEventListener('resize', do_);
    // nội dung mở dần (ví dụ dẫn dắt, gợi ý, lời giải) làm trang cao lên
    const mo = new MutationObserver(do_);
    mo.observe(document.body, { childList: true, subtree: true, characterData: true });
    return () => {
      window.removeEventListener('scroll', do_);
      window.removeEventListener('resize', do_);
      mo.disconnect();
    };
  }, [chanCao]);

  if (!con) return null;

  return (
    <>
      <div aria-hidden className="pointer-events-none fixed inset-x-0 z-10 h-14
                                  bg-gradient-to-t from-white/95 to-transparent"
           style={{ bottom: chanCao }} />
      <button type="button"
              onClick={() => window.scrollBy({ top: window.innerHeight * 0.7, behavior: 'smooth' })}
              className="fixed left-1/2 z-20 -translate-x-1/2 rounded-full border-[1.5px] border-navy
                         bg-white px-3.5 py-1.5 text-[13px] font-bold text-navy shadow-md"
              style={{ bottom: chanCao + 10 }}>
        ▼ kéo xuống, còn nữa
      </button>
    </>
  );
}
