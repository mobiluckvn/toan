import React, { useEffect, useMemo, useState } from 'react';
import { collection, doc, getDocs, orderBy, query, updateDoc } from 'firebase/firestore';
import { db, hasFirebase, auth } from '../lib/nenTang.js';
import { TEN_NGUONG } from '../lib/tenNguong.js';

/**
 * MÀN DUYỆT ĐỀ XUẤT NGƯỠNG — mục 3.8.4.
 *
 * ── ⚠ MÀN NÀY KHÔNG PHẢI MỘT DANH SÁCH CÓ NÚT ĐỒNG Ý ──
 * Mục 3.8.3 đòi mỗi đề xuất lưu kèm cỡ mẫu, khoảng tin cậy, phương pháp, VÀ chỉ số
 * tính trên nhật ký với giá trị cũ và giá trị mới. Lý do nằm ở đây: nếu màn chỉ hiện
 * «NG07: 0,85 → 0,80  [Duyệt] [Từ chối]» thì «duyệt» chỉ là bấm nút, và cái vòng
 * người-trong-vòng-lặp mà R2 dựng ra để mô hình không tự quyết trở thành một thủ tục.
 *
 * Nên mỗi dòng ở đây bày ra ĐỦ để chuyên gia bác được: cỡ mẫu, phương pháp, chỉ số
 * trước và sau, và lời giải thích vì sao máy nghiêng về con số ấy.
 *
 * ── ⚠ HIỆN CẢ NHỮNG ĐỀ XUẤT BỊ CHÍNH MÁY TỪ CHỐI ──
 * Ba loại dòng không có giá trị đề xuất, và cả ba đều đáng đọc:
 *   · thiếu mẫu      — dữ liệu đang nghiêng về đâu, và còn thiếu bao nhiêu
 *   · ngoài khoảng   — máy tính ra một con số mà Bảng 3.19 cấm; đó là một DẤU HIỆU
 *   · không hơn      — bộ đang hành vẫn tốt hơn trên dữ liệu giữ lại
 * Giấu chúng đi thì màn chỉ còn những chỗ máy muốn đổi, và chuyên gia mất hẳn phần
 * «máy đã thử và không tìm được gì tốt hơn» — phần đáng tin nhất của cả quy trình.
 *
 * ── ⚠ DUYỆT KHÔNG PHẢI PHÁT HÀNH ──
 * Luật Firestore chỉ cho đổi `trangThai`, `nguoiDuyet`, `duyetLuc` — không cho sửa
 * con số máy học ra. Và duyệt xong thì giá trị vẫn chưa có hiệu lực: phải sang màn
 * ngưỡng phát hành một phiên bản mới. Hai bước là chủ ý, vì chúng trả lời hai câu
 * khác nhau: «con số này có đáng tin không» và «có đổi hệ thống bây giờ không».
 */

const TRANG_THAI = {
  cho: { chu: 'đang chờ', mau: 'text-ink' },
  daDuyet: { chu: 'đã duyệt', mau: 'text-teal-dark' },
  tuChoi: { chu: 'đã từ chối', mau: 'text-mute' },
};

const so = (x) => (typeof x === 'number' ? (Number.isInteger(x) ? String(x) : x.toFixed(4).replace(/0+$/, '')) : JSON.stringify(x));

export default function DuyetDeXuat({ onExit }) {
  const [ds, datDs] = useState(null);
  const [loi, datLoi] = useState(null);
  const [dangGui, datDangGui] = useState(null);
  const [hienHet, datHienHet] = useState(false);

  useEffect(() => {
    let song = true;
    (async () => {
      if (!hasFirebase || !db) { datDs([]); return; }
      try {
        const snap = await getDocs(query(collection(db, 'nguong_de_xuat'), orderBy('ma')));
        if (song) datDs(snap.docs.map((d) => ({ id: d.id, ...d.data() })));
      } catch (e) {
        if (song) { datDs([]); datLoi(e?.message || 'không đọc được đề xuất'); }
      }
    })();
    return () => { song = false; };
  }, []);

  const quyetDinh = async (d, trangThai) => {
    datDangGui(d.id);
    try {
      await updateDoc(doc(db, 'nguong_de_xuat', d.id), {
        trangThai,
        nguoiDuyet: auth?.currentUser?.uid || null,
        duyetLuc: new Date().toISOString(),
      });
      datDs((cu) => cu.map((x) => (x.id === d.id ? { ...x, trangThai } : x)));
    } catch (e) {
      datLoi(e?.message || 'không ghi được quyết định');
    } finally { datDangGui(null); }
  };

  const { coGiaTri, khongCo } = useMemo(() => ({
    coGiaTri: (ds || []).filter((d) => d.giaTriDeXuat !== null && d.giaTriDeXuat !== undefined),
    khongCo: (ds || []).filter((d) => d.giaTriDeXuat === null || d.giaTriDeXuat === undefined),
  }), [ds]);

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-4 p-4">
      <header className="flex items-center gap-3">
        {onExit && (
          <button type="button" onClick={onExit}
            className="rounded-xl2 border-2 border-line px-3 py-1 text-sm">← Về</button>
        )}
        <h1 className="flex-1 text-xl font-bold text-ink sm:text-2xl">Đề xuất ngưỡng máy học được</h1>
      </header>

      <p className="rounded-xl2 bg-paper p-3 text-sm text-mute">
        Máy học để <b>đề xuất</b>, không tự áp dụng. Duyệt ở đây chưa đổi gì —
        giá trị chỉ có hiệu lực sau khi phát hành một phiên bản ngưỡng mới ở màn Ngưỡng.
      </p>

      {loi && <p className="text-sm text-gold-dark">Không đọc được: {loi}</p>}
      {ds === null && <p className="text-sm text-mute">Đang đọc…</p>}
      {ds !== null && !ds.length && !loi && (
        <p className="text-sm text-mute">
          Chưa có đề xuất nào. Hàm nền học mỗi sáng thứ Hai, và chỉ sinh đề xuất khi đủ cỡ mẫu.
        </p>
      )}

      {coGiaTri.map((d) => <Dong key={d.id} d={d} onQuyet={quyetDinh} dangGui={dangGui === d.id} />)}

      {!!khongCo.length && (
        <section className="rounded-xl2 border border-line p-3">
          <button type="button" onClick={() => datHienHet((x) => !x)}
            className="text-sm font-semibold text-ink">
            {hienHet ? '▾' : '▸'} {khongCo.length} ngưỡng máy ĐÃ XÉT mà không đề xuất đổi
          </button>
          <p className="mt-1 text-xs text-mute">
            Phần này đáng đọc ngang phần trên: nó cho biết máy đã thử và không tìm được gì tốt hơn,
            hoặc còn thiếu bao nhiêu dữ liệu nữa.
          </p>
          {hienHet && (
            <ul className="mt-2 flex flex-col gap-2">
              {khongCo.map((d) => (
                <li key={d.id} className="rounded-xl2 bg-paper p-2 text-sm">
                  <b className="text-ink">{d.ma}</b>
                  <span className="text-mute"> · {d.phamVi}{d.khoa ? `=${d.khoa}` : ''} · đang là {so(d.giaTriHienTai)}</span>
                  <p className="text-xs text-mute">{d.canCu}</p>
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </div>
  );
}

function Dong({ d, onQuyet, dangGui }) {
  const tt = TRANG_THAI[d.trangThai] || TRANG_THAI.cho;
  const cho = d.trangThai === 'cho';
  return (
    <section className="flex flex-col gap-2 rounded-xl2 border border-line p-3">
      <div className="flex flex-wrap items-baseline gap-2">
        <b className="text-ink">{d.ma}</b>
        <span className="text-sm text-mute">{TEN_NGUONG[d.ma] || ''}</span>
        <span className="text-xs text-mute">· {d.phamVi}{d.khoa ? `=${d.khoa}` : ''}</span>
        <span className={`ml-auto text-xs font-semibold ${tt.mau}`}>{tt.chu}</span>
      </div>

      <p className="text-lg">
        <span className="text-mute">{so(d.giaTriHienTai)}</span>
        <span className="mx-2 text-mute">→</span>
        <b className="text-ink">{so(d.giaTriDeXuat)}</b>
      </p>

      <dl className="grid grid-cols-[auto_1fr] gap-x-3 gap-y-1 text-sm">
        <dt className="text-mute">Cỡ mẫu</dt>
        <dd className="text-ink">
          {d.coMau?.toLocaleString('vi-VN')} lượt
          {d.khoangTinCay && ` · khoảng tin cậy 95% [${d.khoangTinCay.map((x) => x.toFixed(3)).join(' – ')}]`}
        </dd>
        <dt className="text-mute">Cách học</dt>
        <dd className="text-ink">{d.phuongPhap}</dd>
        {d.chiSoTruoc && (
          <>
            <dt className="text-mute">Trước</dt>
            <dd className="text-ink">{JSON.stringify(d.chiSoTruoc)}</dd>
          </>
        )}
        {d.chiSoSau && (
          <>
            <dt className="text-mute">Sau</dt>
            <dd className="text-ink">{JSON.stringify(d.chiSoSau)}</dd>
          </>
        )}
        <dt className="text-mute">Căn cứ</dt>
        <dd className="text-ink">{d.canCu}</dd>
      </dl>

      {cho && (
        <div className="flex items-center gap-3">
          <button type="button" disabled={dangGui} onClick={() => onQuyet(d, 'daDuyet')}
            className="rounded-xl2 bg-navy px-4 py-2 text-sm font-semibold text-white disabled:opacity-40">
            Duyệt con số này
          </button>
          <button type="button" disabled={dangGui} onClick={() => onQuyet(d, 'tuChoi')}
            className="text-sm text-mute underline disabled:opacity-40">từ chối</button>
        </div>
      )}
    </section>
  );
}
