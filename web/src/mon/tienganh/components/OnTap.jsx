import React, { useState } from 'react';
import CauHoi from './CauHoi.jsx';
import CauNgheNhin from './CauNgheNhin.jsx';

/**
 * KỲ ÔN TẬP CHƯƠNG — chỗ CHỐT một chương, và là thứ duy nhất ghi vào học bạ.
 *
 * ── VÌ SAO PHẢI CÓ MÀN NÀY ──
 * `ta1/ontap.json` khai 4 kỳ từ lâu, `luuMucHocBa()` viết xong từ lâu, mà không
 * ai gọi — nên bé học xong bốn unit rồi không có chỗ chốt, huy hiệu chương treo
 * mãi, và `hocBaTA` trên máy chủ rỗng trơn. Bốn unit là một chặng đường dài với
 * bé lớp 1; đi hết mà không có gì đánh dấu thì nó không thành một cái mốc nào cả.
 *
 * ── KHÁC SÁT HẠCH CUỐI BÀI Ở ĐÂU ──
 * Sát hạch hỏi lại đúng bài vừa học, còn kỳ ôn tập trộn câu của CẢ BỐN unit — bé
 * phải nhớ được thứ học từ ba tuần trước, không phải thứ vừa nghe xong năm phút.
 * Nên ở đây KHÔNG có nút bỏ qua và KHÔNG có gợi ý: đây là lúc đo, không phải lúc
 * dạy. Nhưng cũng không phạt — làm lại bao nhiêu lần cũng được, và điểm giữ lại
 * là điểm CAO NHẤT.
 *
 * ── HAI DẠNG CÂU, CẢ HAI ĐỀU KHÔNG BẮT ĐỌC ──
 * nghe → bấm hình đúng · nghe → nhìn hình → đúng/sai. Dùng lại đúng hai component
 * của màn học, không dựng bản riêng: một câu hỏi thì chỉ được có một cách chấm.
 */
export default function OnTap({ ky, onXong, onThoat }) {
  const ds = ky?.cau || [];
  const [i, datI] = useState(0);
  const [dung, datDung] = useState(0);
  const [het, datHet] = useState(false);

  if (!ds.length) {
    return (
      <Khung ten={ky?.name} onThoat={onThoat}>
        <p className="text-alert">Kỳ ôn tập này chưa có câu hỏi.</p>
      </Khung>
    );
  }

  const can = ky.need || Math.ceil(ds.length * 0.8);

  if (het) {
    const dat = dung >= can;
    return (
      <Khung ten={ky.name} onThoat={onThoat}>
        <div className={`rounded-xl2 p-6 ${dat ? 'bg-teal-pale' : 'bg-gold-pale'}`}>
          <p className="text-5xl" aria-hidden="true">{dat ? '🏅' : '💪'}</p>
          <p className="mt-2 text-3xl font-bold text-ink">{dung}/{ds.length} câu đúng</p>
          <p className={`mt-1 ${dat ? 'text-teal-dark' : 'text-gold-dark'}`}>
            {dat
              ? 'Con qua cả chương rồi! Huy hiệu này là của con.'
              : `Cần ${can} câu đúng. Con học lại vài bài trong chương rồi quay lại nhé — `
                + 'làm lại bao nhiêu lần cũng được, con giữ điểm cao nhất.'}
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button type="button"
            onClick={() => { datI(0); datDung(0); datHet(false); }}
            className="rounded-xl2 border-2 border-navy px-5 py-3 font-semibold text-navy
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            Làm lại kỳ này
          </button>
          <button type="button"
            onClick={() => onXong?.({ dat, dung, tong: ds.length })}
            className="rounded-xl2 bg-navy px-6 py-3 text-lg font-semibold text-white
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            Xong →
          </button>
        </div>
      </Khung>
    );
  }

  const q = ds[i];
  const tra = (r) => {
    if (r.dung) datDung((n) => n + 1);
    if (i + 1 < ds.length) datI(i + 1); else datHet(true);
  };

  return (
    <Khung ten={ky.name} onThoat={onThoat}>
      <div className="flex items-center gap-3">
        <p className="text-sm font-semibold text-mute">Câu {i + 1}/{ds.length}</p>
        <div className="h-2.5 flex-1 overflow-hidden rounded-full bg-line">
          <i className="block h-full bg-gold transition-all"
             style={{ width: `${(i / ds.length) * 100}%` }} />
        </div>
      </div>
      <div className="rounded-xl2 border-2 border-line bg-white p-5">
        {/* `key` buộc dựng lại mỗi câu. Không có nó thì component giữ state cũ, và
            chỗ chuyển từ câu BẤM CHỌN sang câu ĐÚNG/SAI là trắng màn hình — đã vỡ
            thật một lần ở đúng kiểu chuyển dạng câu này. */}
        {q.nhinNghe
          ? <CauNgheNhin key={q.id} cau={q} onXong={tra} />
          /* Trong kỳ ôn tập KHÔNG hiện lời chữa: `CauHoi` chỉ báo lên khi bé bấm
             tiếp, nên ở đây bé vẫn thấy đúng/sai của từng câu. Chấp nhận: bé lớp 1
             mà làm 10 câu liền không biết mình thế nào thì rất dễ bỏ giữa chừng. */
          : <CauHoi key={q.id} cau={q} onXong={tra} />}
      </div>
      <p className="text-sm text-mute">Từ bài: {q.tenBai}</p>
    </Khung>
  );
}

function Khung({ ten, children, onThoat }) {
  return (
    <div className="mx-auto flex min-h-screen w-full max-w-3xl flex-col gap-5 p-4 pb-24">
      <div className="flex items-center gap-3">
        <button type="button" onClick={onThoat}
          className="rounded-xl2 border-2 border-line px-3 py-2 text-sm font-semibold text-mute
            hover:border-navy hover:text-navy focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          ← Về
        </button>
        <h1 className="flex-1 text-lg font-bold text-ink sm:text-xl">🏅 {ten}</h1>
      </div>
      {children}
    </div>
  );
}
