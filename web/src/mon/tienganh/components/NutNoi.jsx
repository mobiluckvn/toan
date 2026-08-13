import React, { useCallback, useEffect, useRef, useState } from 'react';
import NutNghe from './NutNghe.jsx';
import { batDauNghe, ngheDuoc, loiDocDuoc, xinMicro } from '../lib/nghenoi.js';
import { chamTu, chamCau, chamTot, loiKhen, datNoi } from '../lib/chamnoi.js';

/**
 * NÓI THEO — bé nghe mẫu, bấm nút, đọc lại; máy chấm trên thang 10.
 *
 * ── BỐN LUẬT CHO BÉ 6 TUỔI ──
 *
 * 1. NGHE TRƯỚC, NÓI SAU. Nút nghe luôn nằm cạnh nút nói, và bé bấm nghe lại bao
 *    nhiêu lần cũng được. Bắt nói khi chưa nghe đủ là bắt đoán.
 *
 * 2. KHÔNG BẮT BẤM HAI LẦN. Trình duyệt tự nhận ra bé nói xong. Bé 6 tuổi không
 *    canh được lúc nào bấm "dừng", và mỗi lần hụt là một lần nản.
 *
 * 3. THỬ LẠI KHÔNG GIỚI HẠN, và điểm giữ là ĐIỂM CAO NHẤT. Nói lại nhiều lần chính
 *    là việc học; phạt vì thử nhiều là phạt đúng cái mình muốn bé làm.
 *
 * 4. MÁY KHÔNG NGHE ĐƯỢC THÌ NÓI RA. Không ẩn nút đi im lặng — bé và bố mẹ phải
 *    biết là do máy, không phải do bé.
 *
 * ── `onHong` — VÌ SAO PHẢI BÁO LÊN TRÊN ──
 * Bản trước nuốt trọn mọi trục trặc micro vào trong ô này: hiện một dòng vàng rồi
 * thôi. Màn hình cha không có cách nào biết, nên khi việc NÓI trở thành điều kiện
 * đi tiếp thì bé có máy không micro sẽ kẹt vĩnh viễn — không ai bảo được rằng lỗi
 * ở máy chứ không ở bé. Nên mọi trục trặc THUỘC VỀ MÁY đều gọi `onHong(mã)`.
 *
 * `no-speech` KHÔNG gọi `onHong`: máy vẫn tốt, bé chỉ chưa nói. Lẫn hai thứ này
 * là bé im lặng ba lần rồi được đi tiếp — mở toang đúng cái cổng vừa dựng.
 */
export default function NutNoi({
  cau, loai = 'tu', maAm, doiThu = [], onXong, onHong, onNghe, noiBat = false,
  nhan = 'Nói theo',
}) {
  const [trangThai, datTrangThai] = useState('cho');   // cho · dangNghe · dangCham
  const [tam, datTam] = useState('');
  const [kq, datKq] = useState(null);
  const [khen, datKhen] = useState(null);
  const [loi, datLoi] = useState(null);
  const [caoNhat, datCaoNhat] = useState(null);
  const [soLan, datSoLan] = useState(0);
  const phien = useRef(null);

  useEffect(() => () => phien.current?.huy(), []);

  const noi = useCallback(async () => {
    if (trangThai === 'dangNghe') { phien.current?.dung(); return; }
    datLoi(null); datKq(null); datKhen(null); datTam('');

    /* Xin micro TRƯỚC. Hộp thoại quyền bật ra giữa lúc bé đang nói là hỏng cả lượt. */
    if (!(await xinMicro())) {
      datLoi(loiDocDuoc('not-allowed'));
      onHong?.('not-allowed');
      return;
    }

    datTrangThai('dangNghe');
    const p = batDauNghe({ onTam: datTam });
    phien.current = p;
    try {
      const { chu, phuongAn } = await p.xong;
      datTrangThai('dangCham');
      const ds = phuongAn?.length ? phuongAn : [chu];
      const k = loai === 'cau'
        ? chamTot(chamCau, cau, ds)
        : chamTot(chamTu, cau, ds, { doiThu });
      const truoc = caoNhat;
      datKq(k);
      datKhen(loiKhen(k, truoc));
      datSoLan((n) => n + 1);
      /* Giữ ĐIỂM CAO NHẤT, không phải điểm lần cuối — xem luật 3. */
      if (truoc == null || k.diem > truoc) datCaoNhat(k.diem);
      /* `daNoi` chỉ tính khi máy NGHE RA CHỮ. Bé bấm nút rồi ngồi im thì `chu`
         rỗng — đó là chưa nói, không phải đã nói. Thiếu chốt này thì bấm ba cái
         trong im lặng là qua được chặng. */
      onXong?.({ ...k, caoNhat: Math.max(truoc ?? 0, k.diem), lan: soLan + 1, coTieng: !!ds.join('').trim() });
    } catch (e) {
      datLoi(e?.message || loiDocDuoc(e?.ma));
      onHong?.(e?.ma || 'khong-ro');
    } finally {
      datTrangThai('cho');
      phien.current = null;
    }
  }, [cau, loai, doiThu, trangThai, caoNhat, soLan, onXong, onHong]);

  /* Trình duyệt không có Web Speech: báo lên NGAY lúc vẽ, đừng đợi bé bấm — nút
     bấm còn không có thì bé chẳng bao giờ chạm tới đường báo lỗi kia. */
  useEffect(() => { if (!ngheDuoc()) onHong?.('khong-ho-tro'); }, [onHong]);

  if (!ngheDuoc()) {
    return (
      <div className="rounded-xl2 border-2 border-line bg-soft p-4 text-mute">
        <p className="font-semibold text-ink">Máy này chưa nghe được</p>
        <p className="mt-1 text-sm">
          Phần nói cần trình duyệt Chrome và có mạng. Con vẫn học các phần khác
          bình thường nhé.
        </p>
      </div>
    );
  }

  const dangNghe = trangThai === 'dangNghe';
  return (
    <div className="flex flex-col gap-3 rounded-xl2 border-2 border-teal bg-teal-pale p-4">
      <div className="flex flex-wrap items-center gap-3">
        <p className="flex-1 text-lg font-semibold text-teal-dark">{nhan}</p>
        {caoNhat != null && (
          <span className="rounded-full bg-white px-3 py-1 text-sm font-bold text-teal-dark">
            Cao nhất {caoNhat}/10
          </span>
        )}
      </div>

      {/* Ở dáng nổi bật thì chữ to đã nằm ngay trên hình rồi — nhắc lại lần nữa
          là thừa, mà chỗ ấy phải dành cho nút nói. */}
      {!noiBat && <p className="font-serif text-2xl text-navy">{cau}</p>}

      <div className={`flex flex-wrap items-center gap-3 ${noiBat ? 'flex-col items-stretch' : ''}`}>
        {/* Nghe mẫu luôn đứng cạnh — luật 1. */}
        {maAm && (
          <NutNghe ma={maAm} to nhan="Nghe cô đọc" onPhat={onNghe}
                   chuBen={noiBat ? 'Nghe cô đọc' : null} />
        )}
        <button
          type="button"
          onClick={noi}
          disabled={trangThai === 'dangCham'}
          className={`inline-flex items-center justify-center gap-2 rounded-xl2
            font-semibold transition disabled:opacity-60
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
            ${noiBat ? 'px-6 py-6 text-2xl' : 'px-6 py-4 text-lg'}
            ${dangNghe ? 'bg-alert text-white' : 'bg-teal text-teal-dark hover:brightness-105'}`}
        >
          <span aria-hidden="true">{dangNghe ? '⏹️' : '🎤'}</span>
          {dangNghe ? 'Đang nghe con…'
            : trangThai === 'dangCham' ? 'Đang chấm…'
              : noiBat ? 'Đến lượt con' : 'Bấm rồi nói'}
        </button>
        {soLan > 0 && !dangNghe && (
          <span className="text-sm text-mute">đã thử {soLan} lần</span>
        )}
      </div>

      {/* Hiện chữ đang nghe dở — để bé thấy máy đang nghe mình thật. */}
      {dangNghe && (
        <p className="min-h-[1.6rem] italic text-teal-dark">
          {tam ? `“${tam}”` : 'Con nói to và rõ nhé…'}
        </p>
      )}

      {loi && (
        <div className="rounded-xl2 bg-gold-pale p-3 text-gold-dark">{loi}</div>
      )}

      {kq && khen && <BangDiem kq={kq} khen={khen} />}
    </div>
  );
}

/* ─────────── bảng điểm ─────────── */

function BangDiem({ kq, khen }) {
  const dat = datNoi(kq.diem);
  return (
    <div className={`flex flex-col gap-2 rounded-xl2 p-4 ${dat ? 'bg-white' : 'bg-gold-pale'}`}>
      <div className="flex items-center gap-4">
        {/* Điểm to, và ba ngôi sao — bé chưa đọc số thạo thì nhìn sao là hiểu. */}
        <span className={`text-4xl font-bold ${dat ? 'text-teal-dark' : 'text-gold-dark'}`}>
          {kq.diem}<span className="text-xl text-mute">/10</span>
        </span>
        <span className="text-2xl" aria-label={`${khen.sao} sao`}>
          {'⭐'.repeat(khen.sao)}{'☆'.repeat(3 - khen.sao)}
        </span>
      </div>
      <p className="text-lg font-semibold text-ink">{khen.chinh}</p>
      <p className="text-mute">{khen.them}</p>
      {/* Cho bé thấy máy nghe ra gì — bé tự đối chiếu, và bố mẹ hiểu vì sao điểm thế. */}
      {kq.nghe && (
        <p className="text-sm text-mute">
          Cô nghe được: <span className="font-mono text-ink">“{kq.nghe}”</span>
        </p>
      )}
    </div>
  );
}
