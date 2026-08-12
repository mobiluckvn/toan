import React, { useCallback, useEffect, useState } from 'react';
import BaiHoc from './BaiHoc.jsx';
import OnTap from './OnTap.jsx';
import NutNghe from './NutNghe.jsx';
import { napBai, napSoAm, napOnTap, chuongCua, quyenDau, timQuyen } from '../lib/noiDung.js';
import { ghiBai, ghiChang, ghiChuong, khoaChuong } from '../lib/progress.js';
import { luuBai, luuMucHocBa } from '../lib/duLieu.js';
import {
  trangThaiBai, baiNenHoc, moBai, moKyOnTap, conThieuChoOnTap,
} from '../lib/dandat.js';

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
  const [kyOn, datKyOn] = useState([]);

  /* Nạp CHỈ MỤC 16 bài để vẽ trang chính. Mỗi tệp bài ~25 KB, 16 tệp là 400 KB —
     chấp nhận được cho một quyển, và đổi lại trang chính hiện đúng tên chương,
     số từ, số câu mà không cần một tệp chỉ mục riêng phải giữ đồng bộ tay. */
  useEffect(() => {
    let song = true;
    (async () => {
      await napSoAm(ct?.ma);
      const [ds, on] = await Promise.all([
        Promise.all((ct?.bai || []).map((id) => napBai(id).catch(() => null))),
        napOnTap(ct?.ma).catch(() => []),
      ]);
      if (!song) return;
      datBais(ds.filter(Boolean));
      datKyOn(on || []);
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

  /* Bé đang học tới chặng nào thì nhớ, để lần sau vào lại đúng chỗ. Chỉ ghi tại
     máy, không đẩy máy chủ — xem `ghiChang` trong progress.js. */
  const nhoChang = useCallback((id, chang) => {
    datTienDo((p) => ghiChang(p, id, chang));
  }, [datTienDo]);

  /**
   * XONG MỘT KỲ ÔN TẬP — chỗ DUY NHẤT ghi vào học bạ Tiếng Anh.
   *
   * Ghi hai nơi vì hai nơi trả lời hai câu khác nhau: sổ tại máy để huy hiệu hiện
   * lên ngay kể cả đang mất mạng, còn `hocBaTA` trên máy chủ là bằng chứng lâu dài
   * mà sổ bố mẹ và bảng cô giáo cùng đọc. Ghi máy chủ KHÔNG chờ: mất mạng thì bé
   * vẫn thấy huy hiệu, và `LOI_GHI` trong duLieu.js đếm chứ không nuốt im.
   */
  const xongOnTap = useCallback((ky, kq) => {
    datTienDo((p) => ghiChuong(p, ct.ma, ky.chapter, { dat: kq.dat, dung: kq.dung, tong: kq.tong }));
    luuMucHocBa(learnerId, 'ontap', khoaChuong(ct.ma, ky.chapter), {
      quyen: ct.ma, chuong: ky.chapter, ten: ky.name,
      dat: kq.dat, dung: kq.dung, tong: kq.tong, can: ky.need,
    });
    setView({ page: 'home' });
  }, [datTienDo, setView, learnerId, ct.ma]);

  if (view.page === 'ontap' && view.kyId) {
    const ky = kyOn.find((k) => k.id === view.kyId);
    return (
      <OnTap ky={ky} onThoat={() => setView({ page: 'home' })}
             onXong={(kq) => xongOnTap(ky, kq)} />
    );
  }

  if (view.page === 'bai' && view.baiId) {
    return (
      <BaiHoc
        id={view.baiId}
        tienDo={tienDo}
        onThoat={() => setView({ page: 'home' })}
        onXongBai={(kq, sau) => xongBai(view.baiId, kq, sau)}
        onChang={(c) => nhoChang(view.baiId, c)}
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
      kyOn={kyOn}
      tienDo={tienDo}
      onMoBai={(id) => setView({ page: 'bai', baiId: id })}
      onMoOnTap={(id) => setView({ page: 'ontap', kyId: id })}
      onVeKeSach={veKeSach}
    />
  );
}

/* ─────────── trang chính của quyển ─────────── */

function NhaQuyen({ ct, bais, kyOn = [], tienDo, onMoBai, onMoOnTap, onVeKeSach }) {
  if (!bais) {
    return <div className="p-6 text-mute">Đang mở quyển…</div>;
  }
  const chuong = chuongCua(bais);
  const xong = bais.filter((b) => tienDo?.micros?.[b.id]?.pass).length;

  /* Thứ tự học lấy từ SỔ ĐĂNG KÝ (`ct.bai`), không phải từ thứ tự tệp nạp về:
     `Promise.all` giữ đúng thứ tự, nhưng bài nào nạp hỏng thì bị lọc mất và cả
     dãy dồn lên một nấc — khoá bài sẽ tính theo hàng xóm SAI. */
  const thuTu = ct?.bai || [];
  const khoaBai = !!ct?.khoaBai;
  const opt = { khoaBai };
  const nen = baiNenHoc(tienDo, thuTu, opt);
  const baiNen = bais.find((b) => b.id === nen);

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

      {/* MỘT VIỆC PHẢI LÀM, to và đứng trên cùng. Bé chưa đọc được 16 tên bài để
          tự chọn; danh sách bên dưới là để bố mẹ nhìn và để bé quay lại bài cũ,
          còn đường đi thì app phải chỉ. */}
      {baiNen && (
        <button type="button" onClick={() => onMoBai(baiNen.id)}
          className="flex items-center gap-4 rounded-xl2 bg-navy p-5 text-left text-white
            hover:brightness-110 focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          <span className="text-4xl" aria-hidden="true">▶️</span>
          <span className="min-w-0 flex-1">
            <span className="block text-sm font-semibold uppercase tracking-wider text-white/70">
              {trangThaiBai(tienDo, baiNen.id, thuTu, opt) === 'mo' ? 'Bài tiếp theo' : 'Con đang học dở'}
            </span>
            <span className="block truncate text-xl font-bold">{baiNen.title}</span>
          </span>
          <span className="flex-none rounded-xl2 bg-white px-4 py-2 font-bold text-navy">Học</span>
        </button>
      )}

      {chuong.map((c) => (
        <section key={c.so} className="flex flex-col gap-2">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-mute">
            Chương {c.so} · {c.ten}
          </h2>
          <ul className="flex flex-col gap-2">
            {c.bai.map((b) => (
              <DongBai key={b.id} bai={b} m={tienDo?.micros?.[b.id]} onMo={onMoBai}
                       tt={trangThaiBai(tienDo, b.id, thuTu, opt)}
                       moSau={khoaBai ? moBai(tienDo, b.id, thuTu) : true} />
            ))}
          </ul>
          {/* Kỳ ôn tập đứng NGAY SAU bốn bài của chính chương nó, không gom hết
              xuống cuối quyển: bé vừa học xong chương thì cái mốc phải nằm ngay
              đó, chứ không phải ở một chỗ khác mà bé chẳng bao giờ cuộn tới. */}
          {kyOn.filter((k) => k.chapter === c.so).map((k) => (
            <TheOnTap key={k.id} ky={k} onMo={onMoOnTap}
                      mo={moKyOnTap(tienDo, c.bai.map((b) => b.id))}
                      conThieu={conThieuChoOnTap(tienDo, c.bai.map((b) => b.id))}
                      xong={tienDo?.chapters?.[`${ct.ma}:C${c.so}`]} />
          ))}
        </section>
      ))}
    </div>
  );
}

/* Nhãn ngắn cho bé và bố mẹ cùng đọc. Bài đi vòng qua (thử 2 lần chưa đạt) KHÔNG
   được nói tránh thành "xong" — nó là món còn nợ, và phải nhìn ra ngay là còn nợ. */
const NHAN_DONG = {
  dat: null,
  dangDo: { chu: 'đang học dở', mau: 'bg-gold-pale text-gold-dark' },
  chuaDat: { chu: 'làm lại nhé', mau: 'bg-gold-pale text-gold-dark' },
  mo: null,
  khoa: null,
};

function DongBai({ bai, m, onMo, tt, moSau }) {
  const chu = (bai.dangGoc || '').split(' ')[0];
  const tu = bai.knowledgeCore?.vocabulary || [];
  const khoa = tt === 'khoa' || !moSau;
  const nhan = NHAN_DONG[tt];
  return (
    <li>
      <button type="button" onClick={() => onMo(bai.id)} disabled={khoa}
        /* Khoá thì phải NÓI VÌ SAO. Nút xám không giải thích gì thì bé tưởng máy
           hỏng, còn bố mẹ tưởng app thiếu bài. */
        title={khoa ? 'Con học xong bài phía trên thì bài này mở ra' : undefined}
        className={`flex w-full items-center gap-3 rounded-xl2 border-2 p-3 text-left
          focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
          ${khoa ? 'cursor-not-allowed border-line bg-soft opacity-60'
                 : 'border-line bg-white hover:border-navy-light'}`}>
        <span className={`flex h-12 w-12 flex-none items-center justify-center rounded-xl2
          text-lg font-bold ${khoa ? 'bg-line text-mute' : 'bg-navy text-white'}`}>
          {khoa ? '🔒' : chu}
        </span>
        <span className="min-w-0 flex-1">
          <span className="block font-semibold text-ink">{bai.title}</span>
          <span className="block truncate text-sm text-mute">
            {khoa ? 'Chưa tới lượt bài này' : tu.map((v) => v.tu).join(' · ')}
          </span>
        </span>
        {nhan && (
          <span className={`flex-none rounded-full px-2.5 py-1 text-xs font-semibold ${nhan.mau}`}>
            {nhan.chu}
          </span>
        )}
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

/**
 * THẺ KỲ ÔN TẬP — cái mốc cuối mỗi chương.
 *
 * Khoá thì phải nói CÒN MẤY BÀI NỮA, không phải chỉ "chưa mở". Con số ấy là thứ
 * biến một cái cửa đóng thành một cái đích: bé biết còn hai bài nữa là tới.
 */
function TheOnTap({ ky, mo, conThieu, xong, onMo }) {
  const dat = !!xong?.dat;
  return (
    <button type="button" disabled={!mo && !dat} onClick={() => onMo(ky.id)}
      className={`flex items-center gap-3 rounded-xl2 border-2 border-dashed p-4 text-left
        focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
        ${dat ? 'border-teal bg-teal-pale'
          : mo ? 'border-gold bg-gold-pale hover:brightness-105'
          : 'cursor-not-allowed border-line bg-soft opacity-60'}`}>
      <span className="text-3xl" aria-hidden="true">{dat ? '🏅' : mo ? '🎯' : '🔒'}</span>
      <span className="min-w-0 flex-1">
        <span className="block font-bold text-ink">{ky.name}</span>
        <span className="block text-sm text-mute">
          {dat ? `Con đã qua · ${xong.best}/${xong.tong} câu đúng`
            : mo ? `${ky.soCau} câu · cần ${ky.need} câu đúng để lấy huy hiệu`
            : conThieu === 1 ? 'Còn 1 bài nữa trong chương này là mở'
            : `Còn ${conThieu} bài nữa trong chương này là mở`}
        </span>
      </span>
      {(mo || dat) && (
        <span className="flex-none rounded-xl2 bg-white px-3 py-1.5 text-sm font-bold text-navy">
          {dat ? 'Làm lại' : 'Thi thử'}
        </span>
      )}
    </button>
  );
}
