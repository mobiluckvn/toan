import React, { useEffect, useMemo, useRef, useState } from 'react';
import NutNghe, { maCua } from './NutNghe.jsx';
import NutNoi from './NutNoi.jsx';
import ThanhCau from './ThanhCau.jsx';
import { datNoi } from '../lib/chamnoi.js';
import { ngheDuoc } from '../lib/nghenoi.js';

/**
 * HỘI THOẠI THEO KỊCH BẢN — việc cuối của chuỗi nghe → hiểu → ráp câu → gõ → nói.
 *
 * Nói TỪ và nói CÂU là tập phát âm: bé đã biết trước phải nói gì. Đối đáp thì khác —
 * bé phải NGHE người kia nói gì rồi mới biết mình đáp gì. Đó mới là dùng tiếng Anh.
 *
 * ── HAI KIỂU LƯỢT ──
 *   máy nói TIẾNG ANH  → bé đáp tiếng Anh   (bài có sẵn cặp hỏi–đáp: U1 · U9 · U16)
 *   máy gợi TIẾNG VIỆT → bé nói tiếng Anh   (mọi bài còn lại)
 *
 * Kiểu thứ hai không phải giải pháp tạm. Bé lớp 1 chưa đủ vốn để hỏi lại bằng tiếng
 * Anh, nhưng ĐÃ đủ để nói ra thứ mình thấy — gợi bằng tiếng Việt là đúng tầm.
 *
 * ── BA CHỖ KHÁC HẲN PHẦN NÓI TỪNG CÂU ──
 * 1. Đi TỪNG LƯỢT, không mở hết một lúc. Bé thấy đúng một việc phải làm.
 * 2. Lượt của bé có nút NGHE MẪU — nhưng để BÊN CẠNH, không tự phát: đây là lúc
 *    kiểm xem bé tự nhớ được không, nghe mẫu là quyền của bé chứ không phải mặc định.
 * 3. Điểm cả đoạn là TRUNG BÌNH các lượt bé nói. Một lượt hụt không xoá cả đoạn.
 *
 * ── LUÔN PHẢI CÓ ĐƯỜNG ĐI TIẾP ──
 * Bản đầu chỉ mở nút "đi tiếp" SAU khi chấm xong một lượt. Nghĩa là máy không có
 * micro, hoặc bé đang ngồi trong lớp không tiện nói, thì kẹt cứng ở chặng này và
 * KHÔNG BAO GIỜ tới được phần sát hạch. Đi thử end-to-end mới lộ ra.
 *
 * Nói là phần đáng giá nhất, nhưng không được là cửa ải chặn đường. Nên mỗi lượt
 * đều có "Để sau", và máy không nghe được thì cả chặng bỏ qua được bằng một nút.
 */
export default function HoiThoai({ hoiThoai, tenBe = 'Bo', onXong }) {
  const luot = useMemo(
    () => (hoiThoai?.luot || []).map((l, i) => ({
      ...l, i, chu: String(l.chu).replace(/\{ten\}/g, tenBe),
    })),
    [hoiThoai, tenBe],
  );
  const [tai, datTai] = useState(0);
  const [diem, datDiem] = useState({});          // chỉ số lượt → điểm cao nhất
  const cuon = useRef(null);

  useEffect(() => { cuon.current?.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }, [tai]);

  if (!luot.length) return null;

  /* Máy không nghe được thì đừng bắt bé đứng nhìn: nói rõ vì sao, rồi cho đi tiếp. */
  if (!ngheDuoc()) {
    return (
      <section className="flex flex-col items-start gap-4">
        <div className="rounded-xl2 border-2 border-line bg-soft p-5">
          <p className="text-lg font-semibold text-ink">Máy này chưa nghe được</p>
          <p className="mt-1 text-mute">
            Phần nói chuyện cần trình duyệt Chrome và có mạng. Con học tiếp phần sau
            bình thường nhé — lúc nào mở bằng Chrome thì quay lại làm phần này.
          </p>
        </div>
        <button type="button" onClick={() => onXong?.({ diem: 0, boQua: true })}
          className="rounded-xl2 bg-navy px-6 py-3 text-lg font-semibold text-white
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Đi tiếp →
        </button>
      </section>
    );
  }

  const luotBe = luot.filter((l) => l.ai === 'be');
  const daCham = luotBe.filter((l) => diem[l.i] != null);
  const xongHet = tai >= luot.length;
  const trungBinh = daCham.length
    ? Math.round(daCham.reduce((a, l) => a + diem[l.i], 0) / daCham.length) : 0;

  return (
    <section className="flex flex-col gap-4">
      <div className="rounded-xl2 border-2 border-navy bg-white p-5">
        <p className="text-sm font-semibold uppercase tracking-wider text-mute">Cùng nói chuyện</p>
        <p className="mt-1 text-2xl font-bold text-navy">{hoiThoai.ten}</p>
        <p className="mt-2 rounded-xl2 bg-soft p-3 text-ink">🖼️ {hoiThoai.canh}</p>
      </div>

      {/* Bé phải biết còn mấy LƯỢT của mình nữa. Không có chỗ nào nói thì mỗi lượt
          đều có thể là lượt cuối, và một đoạn hội thoại 8 lượt hoá ra dài vô tận
          với bé 6 tuổi. Chỉ đếm lượt CỦA BÉ — lượt của máy bé không phải làm gì. */}
      {luotBe.length > 1 && (
        <div className="rounded-xl2 border-2 border-line bg-white p-3">
          <ThanhCau
            tong={luotBe.length}
            tt={luotBe.map((l) => (diem[l.i] == null ? undefined : (datNoi(diem[l.i]) ? 'dung' : 'no')))}
            tai={luotBe.findIndex((l) => l.i === tai)}
            nhan="Những lượt con phải nói"
          />
        </div>
      )}

      <ol className="flex flex-col gap-3">
        {luot.slice(0, tai + 1).map((l) => (
          <li key={l.i} ref={l.i === tai ? cuon : null}>
            {l.ai === 'may'
              ? <LuotMay l={l} onTiep={() => datTai(l.i + 1)} xong={l.i < tai} />
              : (
                <LuotBe
                  l={l}
                  diem={diem[l.i]}
                  onXong={(k) => {
                    datDiem((d) => ({ ...d, [l.i]: Math.max(d[l.i] ?? 0, k.diem) }));
                  }}
                  onTiep={() => datTai(l.i + 1)}
                  dangLam={l.i === tai}
                />
              )}
          </li>
        ))}
      </ol>

      {!xongHet && (
        <button type="button" onClick={() => onXong?.({ diem: trungBinh, boQua: true })}
          className="self-start text-sm font-semibold text-mute underline
            hover:text-navy focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Để sau, con làm phần tiếp theo trước
        </button>
      )}

      {xongHet && (
        <KetDoan diem={trungBinh} so={daCham.length} tong={luotBe.length}
                 onLai={() => { datTai(0); }} onXong={() => onXong?.({ diem: trungBinh })} />
      )}
    </section>
  );
}

/* ─────────── lượt của máy ─────────── */

function LuotMay({ l, onTiep, xong }) {
  const vi = l.tieng === 'vi';
  const ma = vi ? maCua(l.chu, 'vi') : maCua(l.chu, 'en');
  return (
    <div className={`flex items-start gap-3 rounded-xl2 p-4 ${vi ? 'bg-soft' : 'bg-navy'}`}>
      <span className="text-2xl" aria-hidden="true">{vi ? '💬' : '🗣️'}</span>
      <div className="min-w-0 flex-1">
        <p className={`${vi ? 'text-ink' : 'font-serif text-2xl text-white'}`}>{l.chu}</p>
        <div className="mt-2 flex items-center gap-3">
          {/* Lượt máy TỰ PHÁT: bé chưa đọc được, phải nghe mới biết người kia nói gì. */}
          <NutNghe ma={ma} nhan="Nghe lại" tuDong={!xong} />
          {!xong && (
            <button type="button" onClick={onTiep}
              className={`rounded-xl2 px-4 py-2 text-sm font-semibold
                focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
                ${vi ? 'bg-navy text-white' : 'bg-white text-navy'}`}>
              Đến lượt con →
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

/* ─────────── lượt của bé ─────────── */

function LuotBe({ l, diem, onXong, onTiep, dangLam }) {
  if (!dangLam && diem != null) {
    return (
      <div className="flex items-center gap-3 rounded-xl2 border-2 border-teal bg-teal-pale p-3">
        <span className="text-xl" aria-hidden="true">🙋</span>
        <p className="flex-1 font-serif text-lg text-teal-dark">{l.chu}</p>
        <span className="font-bold text-teal-dark">{diem}/10</span>
      </div>
    );
  }
  return (
    <div className="flex flex-col gap-2">
      <p className="flex items-center gap-2 text-mute">
        <span aria-hidden="true">🙋</span> {l.goi}
      </p>
      {/* `maAm` để bé bấm NGHE MẪU nếu cần — nhưng không tự phát, xem luật 2 ở đầu tệp. */}
      <NutNoi cau={l.chu} loai="cau" maAm={maCua(l.chu, 'en')}
              nhan="Đến lượt con nói" onXong={onXong} />
      {/* "Để sau" LUÔN có, kể cả khi chưa chấm được lượt này — xem đầu tệp. */}
      <div className="flex flex-wrap items-center gap-3">
      {diem == null && (
        <button type="button" onClick={onTiep}
          className="rounded-xl2 border-2 border-line px-4 py-2 text-sm font-semibold
            text-mute hover:border-navy hover:text-navy
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Để sau, bỏ qua lượt này →
        </button>
      )}
      {diem != null && (
        <button type="button" onClick={onTiep}
          className="self-start rounded-xl2 bg-navy px-5 py-2.5 font-semibold text-white
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          {datNoi(diem) ? 'Tốt rồi, đi tiếp →' : 'Đi tiếp (làm lại sau cũng được) →'}
        </button>
      )}
      </div>
    </div>
  );
}

/* ─────────── kết đoạn ─────────── */

function KetDoan({ diem, so, tong, onLai, onXong }) {
  const dat = datNoi(diem);
  return (
    <div className={`flex flex-col items-start gap-3 rounded-xl2 p-6
      ${dat ? 'bg-teal-pale' : 'bg-gold-pale'}`}>
      <p className="text-4xl" aria-hidden="true">{dat ? '🎉' : '💪'}</p>
      <p className="text-2xl font-bold text-ink">
        Cả đoạn: {diem}/10 <span className="text-base font-normal text-mute">
          ({so}/{tong} lượt con đã nói)</span>
      </p>
      <p className={dat ? 'text-teal-dark' : 'text-gold-dark'}>
        {dat
          ? 'Con nói chuyện được bằng tiếng Anh rồi đấy. Giỏi lắm!'
          : 'Con đã nói được cả đoạn. Nghe lại rồi làm thêm một lượt là ngon ngay.'}
      </p>
      <div className="flex flex-wrap gap-3">
        <button type="button" onClick={onLai}
          className="rounded-xl2 border-2 border-navy px-5 py-2.5 font-semibold text-navy
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Nói lại cả đoạn
        </button>
        <button type="button" onClick={onXong}
          className="rounded-xl2 bg-navy px-6 py-2.5 font-semibold text-white
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Xong →
        </button>
      </div>
    </div>
  );
}
