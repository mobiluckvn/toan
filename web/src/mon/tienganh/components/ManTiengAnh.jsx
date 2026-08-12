import React, { useCallback, useEffect, useState } from 'react';
import BaiHoc from './BaiHoc.jsx';
import NutNghe from './NutNghe.jsx';
import { napBai, napSoAm, chuongCua, quyenDau, timQuyen } from '../lib/noiDung.js';
import { ghiBai } from '../lib/progress.js';
import { luuBai } from '../lib/duLieu.js';

/**
 * MÀN CỦA MÔN TIẾNG ANH — mọi đường đi bên trong môn, gói trong MỘT cửa.
 *
 * Vỏ app dựng component này rồi tránh ra; nó không biết môn này có những màn nào,
 * cũng không soi vào `tienDo`. Giống hệt cách `ManToan` nhận việc — và đó là lý do
 * thêm môn thứ hai không phải sửa một dòng nào của vỏ.
 */
export default function ManTiengAnh({
  tienDo, datTienDo, quyen, learnerId, hoSo, view, setView, veKeSach,
}) {
  /* `quyen` vỏ truyền xuống là MÃ CHUỖI ('ta1'), không phải mục chương trình —
     `App.jsx` gọi `setQuyen(ma)`. Dùng thẳng thì `ct.bai` là undefined, danh sách
     bài rỗng, và trang chính hiện "Xong 0/0 bài · NaN%" trong khi quyển có 16 bài.
     Không cổng nào bắt được: dữ liệu đủ, bản dựng xanh, chỉ màn hình là trống.
     Đã ghi lại vào giao ước ở `src/soMon.js`. */
  const ct = (typeof quyen === 'string' ? timQuyen(quyen) : quyen) || quyenDau();
  const [bais, datBais] = useState(null);

  /* Nạp CHỈ MỤC 16 bài để vẽ trang chính. Mỗi tệp bài ~25 KB, 16 tệp là 400 KB —
     chấp nhận được cho một quyển, và đổi lại trang chính hiện đúng tên chương,
     số từ, số câu mà không cần một tệp chỉ mục riêng phải giữ đồng bộ tay. */
  useEffect(() => {
    let song = true;
    (async () => {
      await napSoAm(ct?.ma);
      const ds = await Promise.all((ct?.bai || []).map((id) => napBai(id).catch(() => null)));
      if (song) datBais(ds.filter(Boolean));
    })();
    return () => { song = false; };
  }, [ct?.ma]);

  const xongBai = useCallback((id, kq, sau) => {
    datTienDo((p) => {
      const sau2 = ghiBai(p, id, kq);
      /* Đẩy lên máy chủ NGAY, nhưng không chờ: mất mạng thì bé vẫn học tiếp bình
         thường, sổ tại máy giữ đủ, và lần đăng nhập sau `napTuMay` + `gopTienDo`
         hoà lại. Ghi hỏng thì `LOI_GHI` trong duLieu.js đếm chứ không nuốt im. */
      luuBai(learnerId, id, sau2.micros[id]);
      return sau2;
    });
    /* Đạt thì sang bài sau; chưa đạt thì về danh sách để bé chọn lại — KHÔNG đẩy
       bé đi tiếp khi chưa vững, vì bài sau dựng trên bài này. */
    setView(kq.pass && sau ? { page: 'bai', baiId: sau } : { page: 'home' });
  }, [datTienDo, setView, learnerId]);

  if (view.page === 'bai' && view.baiId) {
    return (
      <BaiHoc
        id={view.baiId}
        tienDo={tienDo}
        onThoat={() => setView({ page: 'home' })}
        onXongBai={(kq, sau) => xongBai(view.baiId, kq, sau)}
        /* Biệt danh của chính bé đi vào đoạn hội thoại — bé nghe tên mình trong
           một câu tiếng Anh. Đó là chỗ bài này khác mọi bài luyện phát âm khác. */
        tenBe={(hoSo?.displayName || '').trim().split(/\s+/).pop() || 'Bo'}
      />
    );
  }

  return (
    <NhaQuyen
      ct={ct}
      bais={bais}
      tienDo={tienDo}
      onMoBai={(id) => setView({ page: 'bai', baiId: id })}
      onVeKeSach={veKeSach}
    />
  );
}

/* ─────────── trang chính của quyển ─────────── */

function NhaQuyen({ ct, bais, tienDo, onMoBai, onVeKeSach }) {
  if (!bais) {
    return <div className="p-6 text-mute">Đang mở quyển…</div>;
  }
  const chuong = chuongCua(bais);
  const xong = bais.filter((b) => tienDo?.micros?.[b.id]?.pass).length;

  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col gap-5 p-4 pb-24">
      <div className="flex items-center gap-3">
        <button type="button" onClick={onVeKeSach}
          className="rounded-xl2 border-2 border-line px-3 py-2 text-sm font-semibold text-mute
            hover:border-navy hover:text-navy focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          ← Kệ sách
        </button>
        <div className="flex-1">
          <h1 className="text-xl font-bold text-ink sm:text-2xl">{ct?.ten}</h1>
          <p className="text-sm text-mute">{ct?.phuDe}</p>
        </div>
      </div>

      <div className="rounded-xl2 bg-soft p-4">
        <div className="flex items-baseline justify-between">
          <p className="font-semibold text-ink">Xong {xong}/{bais.length} bài</p>
          <p className="text-sm text-mute">{Math.round((xong / bais.length) * 100)}%</p>
        </div>
        <div className="mt-2 h-2.5 overflow-hidden rounded-full bg-line">
          <i className="block h-full bg-teal transition-all"
             style={{ width: `${(xong / bais.length) * 100}%` }} />
        </div>
      </div>

      {chuong.map((c) => (
        <section key={c.so} className="flex flex-col gap-2">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-mute">
            Chương {c.so} · {c.ten}
          </h2>
          <ul className="flex flex-col gap-2">
            {c.bai.map((b) => <DongBai key={b.id} bai={b} m={tienDo?.micros?.[b.id]} onMo={onMoBai} />)}
          </ul>
        </section>
      ))}
    </div>
  );
}

function DongBai({ bai, m, onMo }) {
  const chu = (bai.dangGoc || '').split(' ')[0];
  const tu = bai.knowledgeCore?.vocabulary || [];
  return (
    <li>
      <button type="button" onClick={() => onMo(bai.id)}
        className="flex w-full items-center gap-3 rounded-xl2 border-2 border-line bg-white p-3
          text-left hover:border-navy-light focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
        <span className="flex h-12 w-12 flex-none items-center justify-center rounded-xl2
          bg-navy text-lg font-bold text-white">{chu}</span>
        <span className="min-w-0 flex-1">
          <span className="block font-semibold text-ink">{bai.title}</span>
          <span className="block truncate text-sm text-mute">
            {tu.map((v) => v.tu).join(' · ')}
          </span>
        </span>
        {/* Hiện BẬC CAO NHẤT đã qua, không phải "xong / chưa xong": bé nào cũng
            xong được bài, nhưng gõ lại được cả câu thì không. */}
        {m?.pass && (
          <span className="flex-none text-sm font-semibold text-teal-dark" title={`Bậc ${m.bac || 1}`}>
            {'★'.repeat(Math.max(1, Math.min(3, m.bac ? m.bac - 1 : 1)))}
          </span>
        )}
      </button>
    </li>
  );
}
