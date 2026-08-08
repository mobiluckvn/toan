import React, { useEffect, useState } from 'react';
import { allMicroIds, chapterOf, CONTENT, dongDau } from '../lib/content.js';
import { microState, chapterStats, overallStats, isChapterExamUnlocked, modeOf } from '../lib/progress.js';
import { planSession, keyOf } from '../lib/adaptive.js';
import TodayCard from './TodayCard.jsx';
import ChanTrang from './ChanTrang.jsx';

const CHAPTER_NAMES = {
  1: 'Bản đồ các hàng', 2: 'Lập số & đếm', 3: 'Chia hết & vòng đuôi', 4: 'Tính nhanh & tìm X',
  5: 'So sánh phân số', 6: 'Trung bình cộng', 7: 'Tổng – hiệu & tuổi', 8: 'Tổng – tỉ, hiệu – tỉ',
  9: 'Hai tỉ số', 10: 'Phần trăm & nồng độ', 11: 'Công việc chung & suy luận',
  12: 'Tam giác & hình thang', 13: 'Hình tròn & hình khối', 14: 'Chuyển động',
};
const DOT = { passed: 'bg-teal', tried: 'bg-gold', open: 'bg-navy-light', locked: 'bg-line' };
const WORD = { passed: 'đã đạt', tried: 'chưa qua câu bẫy', open: 'học được ngay', locked: 'chưa mở' };

export default function Home({ onOpenMuaGiai, onDoiChuongTrinh, progress, onOpenMicro, onOpenExam, onOpenReport, onSetMode, account = {}, mastery = {}, cards = [] }) {
  const list = allMicroIds();
  const [index, setIndex] = useState({});
  const [why, setWhy] = useState(null);          // bấm vào bài khoá → nói rõ vì sao

  // tên bài + thời lượng nằm trong chỉ mục; thiếu nó thì màn hình chỉ có mã bài
  useEffect(() => {
    let alive = true;
    fetch(dongDau(`${CONTENT}/index_micro.json`)).then((r) => r.json())
      .then((d) => alive && setIndex(d)).catch(() => {});
    return () => { alive = false; };
  }, []);

  const all = overallStats(progress, list);
  const plan = planSession({ progress, mastery, cards, index, list });
  const next = plan.micro?.microId || null;
  const [open, setOpen] = useState(next ? chapterOf(next) : 1);
  useEffect(() => { if (next) setOpen(chapterOf(next)); }, [next]);

  const started = all.done > 0;
  const cheDo = modeOf(progress);

  return (
    <div className="mx-auto min-h-[100dvh] max-w-[740px] pb-16">
      <header className="bg-navy px-4 py-4 text-white">
        <div className="flex items-start gap-2">
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-extrabold tracking-widest text-gold">MOBILUCK · KỸ SƯ NHÍ</span>
              <button onClick={onDoiChuongTrinh}
                      className="rounded-full bg-white/15 px-2 py-0.5 text-[10.5px] font-bold text-white">
                lớp 5 · đổi
              </button>
            </div>
            <h1 className="mt-1 text-[20px] font-bold">Toán Tư Duy lớp 5 — Quyển 1</h1>
          </div>
          {/* Sổ học là chỗ của bố mẹ — ghi rõ để con không lạc vào rồi bối rối */}
          <div className="mt-1 flex shrink-0 flex-col items-end gap-1">
            <button onClick={onOpenReport}
                    className="rounded-full bg-navy-light px-2.5 py-1 text-[11px] font-bold">
              📖 Sổ bố mẹ
            </button>
            {account.signedIn && (
              <button onClick={account.onSignOut} className="text-[10.5px] opacity-75 underline">
                thoát
              </button>
            )}
          </div>
        </div>

        {/* Ngày đầu chưa có gì để khoe — "0/168" chỉ làm con nản. Hiện khi đã học rồi. */}
        {started ? (
          <>
            <div className="mt-3 flex items-center gap-3">
              <div className="h-2 flex-1 overflow-hidden rounded-full bg-navy-deep">
                <i className="block h-full bg-gradient-to-r from-teal to-gold" style={{ width: `${all.percent}%` }} />
              </div>
              <span className="text-[12px] tabular-nums">{all.done}/{all.total} bài</span>
            </div>
            <div className="mt-1.5 text-[12px] opacity-90">🏅 {all.badges}/14 huy hiệu chương</div>
          </>
        ) : (
          <p className="mt-2.5 text-[13px] leading-relaxed opacity-90">
            Con học từng bài nhỏ khoảng 8 phút. Học xong một bài là mở khoá bài tiếp theo.
          </p>
        )}
      </header>

      {plan.reviews.length > 0 && (
        <div className="mx-3.5 mt-3.5 rounded-2xl border-[1.5px] border-teal bg-teal-pale px-4 py-3">
          <b className="text-[14px] text-teal-dark">🔁 {plan.reviews.length} thẻ ôn đến hạn</b>
          <p className="mt-0.5 text-[12.5px] text-mute">Ôn lại trước khi học bài mới — kiến thức cũ sắp quên quan trọng hơn.</p>
        </div>
      )}

      {plan.exam && (
        <button className="mx-3.5 mt-3.5 w-[calc(100%-1.75rem)] rounded-2xl bg-alert px-4 py-3 text-left text-white"
                onClick={() => onOpenExam(plan.exam)}>
          <b className="text-[14.5px]">⚔ Kỳ sát hạch chương {plan.exam} đang chờ</b>
          <p className="text-[12.5px] opacity-90">Con đã học hết chương — thi lấy huy hiệu nhé!</p>
        </button>
      )}

      {/* Chưa đăng nhập thì phải nói THẲNG là bài đang nằm ở máy này — không thì bố mẹ
          tưởng đã lưu lên mạng, đổi máy là mất hết mà không hiểu vì sao. */}
      {account.available && !account.signedIn && (
        <button onClick={account.onSignIn}
                className="mx-3.5 mt-3.5 flex w-[calc(100%-1.75rem)] items-center gap-2.5 rounded-2xl border-[1.5px] border-gold bg-gold-pale px-4 py-3 text-left">
          <span className="text-[18px]">☁️</span>
          <span className="flex-1">
            <b className="block text-[14px] text-gold-dark">Bài đang lưu ở máy này thôi</b>
            <span className="text-[12.5px] text-mute">
              Đăng nhập để lưu lên mạng — thầy cô theo dõi được, đổi máy vẫn còn.
            </span>
          </span>
          <span className="text-[13px] font-bold text-gold-dark">Đăng nhập ▸</span>
        </button>
      )}

      <TodayCard microId={next} progress={progress} info={index[keyOf(next || '')]}
                 reason={plan.micro?.reason} onOpen={onOpenMicro} />

      {/* Hai lối học. Khoá cứng tuần tự cả 168 bài thì con muốn ôn riêng một chủ đề
          cũng không vào được — nên cho chọn, nhưng TRONG chương vẫn phải lần lượt
          vì các bài trong một chương xây chồng lên nhau. */}
      <div className="mx-3.5 mt-5">
        <h3 className="pb-1.5 text-[11px] font-extrabold tracking-widest text-mute">CON MUỐN HỌC THẾ NÀO?</h3>
        <div className="flex gap-2">
          {[['chuongtrinh', 'Theo chương trình', 'học lần lượt từ đầu — đúng thứ tự cô soạn'],
            ['tuchon', 'Con tự chọn chủ đề', 'thích chương nào vào chương đó']].map(([id, ten, mo]) => (
            <button key={id} onClick={() => onSetMode?.(id)}
              className={`flex-1 rounded-xl border-[1.5px] px-3 py-2.5 text-left ${
                cheDo === id ? 'border-navy bg-navy text-white' : 'border-line bg-white text-navy'}`}>
              <b className="block text-[13.5px]">{ten}</b>
              <span className={`text-[11.5px] ${cheDo === id ? 'opacity-85' : 'text-mute'}`}>{mo}</span>
            </button>
          ))}
        </div>
      </div>

      <h3 className="px-4 pb-1 pt-4 text-[11px] font-extrabold tracking-widest text-mute">
        TẤT CẢ 14 CHƯƠNG
      </h3>

      <div className="px-3.5">
        {Array.from({ length: 14 }, (_, i) => i + 1).map((c) => {
          const st = chapterStats(progress, c, list);
          const micros = list.filter((id) => chapterOf(id) === c);
          const isOpen = open === c;
          const shown = micros.filter((id) => microState(progress, id, list) !== 'locked');
          const lockedCount = micros.length - shown.length;
          return (
            <section key={c} className="mb-2.5 overflow-hidden rounded-2xl bg-white shadow-[0_2px_10px_rgba(12,59,112,.06)]">
              <button className="flex w-full items-center gap-2.5 px-3.5 py-3 text-left"
                      onClick={() => setOpen(isOpen ? 0 : c)}>
                <span className="rounded bg-navy px-1.5 py-0.5 text-[11px] font-extrabold text-white">C{c}</span>
                <span className="flex-1">
                  <b className="block text-[14px] text-navy">{CHAPTER_NAMES[c]}</b>
                  <span className="text-[11.5px] text-mute">{st.done}/{st.total} bài</span>
                </span>
                {st.examPassed && <span className="text-[18px]">🏅</span>}
                <span className="h-1.5 w-14 overflow-hidden rounded-full bg-soft">
                  <i className="block h-full bg-teal" style={{ width: `${st.percent}%` }} />
                </span>
              </button>

              {isOpen && (
                <div className="border-t border-line px-3.5 py-2.5">
                  {shown.map((id) => {
                    const s = microState(progress, id, list);
                    const t = index[keyOf(id)]?.title;
                    return (
                      <button key={id} onClick={() => onOpenMicro(id)}
                        className="flex w-full items-center gap-2.5 rounded-lg px-2 py-2 text-left text-[13.5px] hover:bg-[#F0F5F9]">
                        <i className={`h-2 w-2 flex-none rounded-full ${DOT[s]}`} />
                        <span className="min-w-0 flex-1">
                          <b className="block truncate font-semibold text-navy">{t || id.replace('DL:KSN5Q1.', '')}</b>
                          <span className="text-[11.5px] text-mute">{WORD[s]}</span>
                        </span>
                      </button>
                    );
                  })}

                  {/* Gộp phần chưa mở: ngày đầu con thấy 11 dòng xám + ổ khoá, bấm vào
                      không có gì xảy ra — nhìn như app hỏng chứ không như phần thưởng. */}
                  {lockedCount > 0 && (
                    <button onClick={() => setWhy(c)}
                      className="mt-1.5 flex w-full items-center gap-2 rounded-lg bg-[#F7FAFD] px-2.5 py-2 text-left text-[12.5px] text-mute">
                      <span>🔒</span>
                      <span className="flex-1">Còn {lockedCount} bài nữa — học xong bài trên là mở dần</span>
                      <span className="font-bold text-navy">vì sao?</span>
                    </button>
                  )}

                  <button
                    disabled={!isChapterExamUnlocked(progress, c, list)}
                    onClick={() => onOpenExam(c)}
                    className={`mt-2 w-full rounded-xl px-3 py-2.5 text-[13.5px] font-extrabold ${
                      isChapterExamUnlocked(progress, c, list)
                        ? 'bg-alert text-white' : 'bg-soft text-mute'}`}>
                    ⚔ KỲ SÁT HẠCH CHƯƠNG {c} {st.examPassed ? '· đã đạt 🏅'
                      : isChapterExamUnlocked(progress, c, list) ? '' : '· học hết chương mới mở'}
                  </button>
                </div>
              )}
            </section>
          );
        })}
      </div>

      {/* Cửa vào Quyển 2. Đặt SAU danh sách chương: con học Quyển 1 trước, luyện thi
          sau — nhưng vẫn thấy được để biết còn có phần này. */}
      <div className="px-3.5 pt-2">
        <button onClick={onOpenMuaGiai}
                className="flex w-full items-center gap-3 rounded-2xl border-[1.5px] border-gold bg-gold-pale px-4 py-3.5 text-left">
          <span className="text-[28px] leading-none">🏆</span>
          <span className="flex-1">
            <span className="block text-[11px] font-extrabold tracking-widest text-gold-dark">QUYỂN 2 · LUYỆN THI</span>
            <span className="block text-[16px] font-bold text-navy">Mùa giải Vô địch</span>
            <span className="block text-[12.5px] text-mute">
              14 vòng đấu có đồng hồ · mở dần theo từng chương con học xong
            </span>
          </span>
          <span className="text-[18px] text-gold-dark">▶</span>
        </button>
      </div>

      <ChanTrang />

      {why !== null && (
        <div className="fixed inset-0 z-30 flex items-end justify-center bg-black/40 p-3.5"
             onClick={() => setWhy(null)}>
          <div className="w-full max-w-[740px] rounded-2xl bg-white p-4" onClick={(e) => e.stopPropagation()}>
            <h4 className="text-[16px] font-bold text-navy">Vì sao chưa mở?</h4>
            <p className="mt-2 text-[14.5px] leading-relaxed">
              Mỗi bài dạy một cái bẫy mới, và bài sau dùng lại cái bẫy của bài trước.
              Nên con phải <b>làm đúng câu bẫy</b> của bài này thì bài sau mới mở —
              đúng 2/3 câu mà sai câu bẫy thì vẫn chưa qua.
            </p>
            <p className="mt-2 text-[14.5px] leading-relaxed">
              Học xong bài đang mở là bài kế tiếp hiện ra ngay.
            </p>
            {cheDo === 'chuongtrinh' && (
              <p className="mt-2 rounded-xl bg-gold-pale px-3 py-2.5 text-[14px] text-gold-dark">
                Muốn học chủ đề khác trước? Đổi sang <b>“Con tự chọn chủ đề”</b> ở trang chính —
                khi đó bài đầu của mọi chương đều mở.
              </p>
            )}
            <button className="btn-go mt-3.5" onClick={() => setWhy(null)}>Con hiểu rồi</button>
          </div>
        </div>
      )}
    </div>
  );
}
