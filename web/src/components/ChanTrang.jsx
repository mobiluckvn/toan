import React from 'react';

/**
 * CHÂN TRANG — icon thương hiệu và các trang cùng nhà.
 *
 * Đặt ở CUỐI trang chủ chứ không ở đầu: người dùng chính là trẻ lớp 5, thứ đầu
 * tiên con nhìn thấy phải là bài học của con, không phải quảng cáo. Bố mẹ cuộn
 * hết danh sách chương thì gặp — đúng lúc muốn biết "trang này của ai làm".
 *
 * `rel="noopener"` cho mọi liên kết mở tab mới: thiếu nó thì trang vừa mở giành
 * được quyền điều khiển tab cũ qua window.opener.
 */
const TRANG = [
  { ten: 'SpeedUp Education', ghi: 'luyện thi · học liệu', url: 'https://speedup.edu.vn' },
  { ten: 'code247.ai', ghi: 'phần mềm · trí tuệ nhân tạo', url: 'https://code247.ai' },
  { ten: 'MOBILUCK', ghi: 'công ty chủ quản', url: 'https://mobiluck.vn' },
];

export default function ChanTrang() {
  return (
    <footer className="mt-6 border-t border-line bg-white px-3.5 pb-8 pt-5">
      <div className="mx-auto max-w-[740px]">
        <div className="flex items-center gap-2.5">
          <img src="/icon/icon-192.png" alt="" width="34" height="34"
               className="rounded-lg" />
          <div>
            <div className="text-[13.5px] font-bold text-navy">Kỹ Sư Nhí · Toán Tư Duy lớp 5</div>
            <div className="text-[11.5px] text-mute">Quyển 1 · 168 bài · 14 kỳ sát hạch</div>
          </div>
        </div>

        <div className="mt-3.5 flex flex-wrap gap-2">
          {TRANG.map((t) => (
            <a key={t.url} href={t.url} target="_blank" rel="noopener noreferrer"
               className="flex-1 basis-[190px] rounded-xl border border-line px-3 py-2
                          hover:border-navy hover:bg-paper">
              <div className="text-[13px] font-bold text-navy">{t.ten} ↗</div>
              <div className="text-[11.5px] text-mute">{t.ghi}</div>
            </a>
          ))}
        </div>

        <p className="mt-3.5 text-[11.5px] leading-relaxed text-mute">
          © MOBILUCK · nội dung và hình minh hoạ do đội ngũ Kỹ Sư Nhí biên soạn.
        </p>
      </div>
    </footer>
  );
}
