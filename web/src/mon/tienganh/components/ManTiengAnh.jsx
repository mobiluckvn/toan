import React, { useCallback, useEffect, useRef, useState } from 'react';
import BaiHoc from './BaiHoc.jsx';
import OnTap from './OnTap.jsx';
import DocHieu from './DocHieu.jsx';
import VietBai from './VietBai.jsx';
import OnLai from './OnLai.jsx';
import NutNghe from './NutNghe.jsx';
import {
  napBai, napSoAm, napOnTap, napDocHieu, napVietBai, chuongCua, quyenDau, timQuyen,
} from '../lib/noiDung.js';
import {
  ghiBai, ghiChang, ghiMoc, ghiChuong, khoaChuong, ghiDocHieu, khoaDocHieu,
  ghiBaiViet, khoaBaiViet, ghiSoThich, khoaSoThich, ghiDangCau,
} from '../lib/progress.js';
import {
  luuBai, luuMucHocBa, luuSuKien, docTheOn, luuTheOn, docMucThao,
} from '../lib/duLieu.js';
import { theDenHan, demDenHan, daySauKhiOn } from '../lib/onlai.js';
import { manhNhat, yeuNhat } from '../lib/hoso.js';
import { napDoThi } from '../lib/doThi.js';
import { maTranTrangThai } from '../lib/lantruyen.js';
import GocBoMe, { MucBoMe } from './GocBoMe.jsx';
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
  const [docs, datDocs] = useState([]);
  const [viets, datViets] = useState([]);
  /* Thẻ ôn tới hạn. Nạp một lần khi mở quyển; hỏng thì mảng rỗng và trang chính
     đơn giản là không mọc thẻ mời — bé vẫn học bình thường. */
  const [theOn, datTheOn] = useState([]);
  /* Mức thạo từng nút, do hàm nền BKT ghi. Dùng để xếp câu theo ZPD — không có
     thì bộ chọn giữ nguyên thứ tự cũ, bé học y như trước. */
  const [mucThao, datMucThao] = useState({});

  /* Nạp CHỈ MỤC 16 bài để vẽ trang chính. Mỗi tệp bài ~25 KB, 16 tệp là 400 KB —
     chấp nhận được cho một quyển, và đổi lại trang chính hiện đúng tên chương,
     số từ, số câu mà không cần một tệp chỉ mục riêng phải giữ đồng bộ tay. */
  useEffect(() => {
    let song = true;
    (async () => {
      await napSoAm(ct?.ma);
      const [ds, on, dh, vb] = await Promise.all([
        Promise.all((ct?.bai || []).map((id) => napBai(id).catch(() => null))),
        napOnTap(ct?.ma).catch(() => []),
        /* Quyển chưa có bài đọc hiểu thì trả mảng rỗng và trang chính không mọc
           thẻ nào — KHÔNG phải lỗi. Lớp 1·2 chưa có, lớp 3 có. */
        napDocHieu(ct?.ma).catch(() => []),
        napVietBai(ct?.ma).catch(() => []),
      ]);
      if (!song) return;
      datBais(ds.filter(Boolean));
      datKyOn(on || []);
      datDocs(dh || []);
      datViets(vb || []);
    })();
    return () => { song = false; };
  }, [ct?.ma]);

  useEffect(() => {
    let song = true;
    docTheOn(learnerId).then((ds) => { if (song) datTheOn(ds); });
    docMucThao(learnerId).then((m) => { if (song) datMucThao(m); });
    return () => { song = false; };
  }, [learnerId]);

  const xongBai = useCallback((id, kq, sau) => {
    datTienDo((p) => {
      const sau2 = ghiBai(p, id, kq);
      /* Đẩy lên máy chủ NGAY, nhưng không chờ: mất mạng thì bé vẫn học tiếp bình
         thường, sổ tại máy giữ đủ, và lần đăng nhập sau `napTuMay` + `gopTienDo`
         hoà lại. Ghi hỏng thì `LOI_GHI` trong duLieu.js đếm chứ không nuốt im. */
      luuBai(learnerId, id, sau2.micros[id]);
      /* Đẩy hồ sơ bé lên CÙNG LÚC với kết quả bài — không đẩy sau mỗi câu: bảng
         định dạng đổi từng lượt nhưng chẳng ai đọc nó giữa buổi, mà ghi mỗi câu
         một lần là thêm một nhịp mạng cho việc không ai cần. */
      luuMucHocBa(learnerId, 'hoSo', `${ct.ma}:HS`, {
        giaTri: { dinhDang: sau2.dinhDang || {} },
      });
      return sau2;
    });
    /* Đạt thì sang bài sau; chưa đạt thì về danh sách để bé chọn lại — KHÔNG đẩy
       bé đi tiếp khi chưa vững, vì bài sau dựng trên bài này. */
    setView(kq.pass && sau ? { page: 'bai', baiId: sau } : { page: 'home' });
  }, [datTienDo, setView, learnerId, ct.ma]);

  /* Bé đang học tới chặng nào thì nhớ, để lần sau vào lại đúng chỗ. Chỉ ghi tại
     máy, không đẩy máy chủ — xem `ghiChang` trong progress.js. */
  const nhoChang = useCallback((id, chang) => {
    datTienDo((p) => ghiChang(p, id, chang));
  }, [datTienDo]);

  /* Và nhớ luôn chỗ dở BÊN TRONG chặng — mức nào, câu thứ mấy. Cũng chỉ tại máy.
     `ghiMoc` trả nguyên khối cũ khi không có gì đổi, nên hàm này gọi được sau MỖI
     câu mà không làm vỏ vẽ lại. Bỏ điều ấy đi là vòng lặp không đáy. */
  const nhoMoc = useCallback((id, chang, moc) => {
    datTienDo((p) => ghiMoc(p, id, chang, moc));
  }, [datTienDo]);

  /**
   * XONG MỘT KỲ ÔN TẬP — chỗ DUY NHẤT ghi vào học bạ Tiếng Anh.
   *
   * Ghi hai nơi vì hai nơi trả lời hai câu khác nhau: sổ tại máy để huy hiệu hiện
   * lên ngay kể cả đang mất mạng, còn `hocBaTA` trên máy chủ là bằng chứng lâu dài
   * mà sổ bố mẹ và bảng cô giáo cùng đọc. Ghi máy chủ KHÔNG chờ: mất mạng thì bé
   * vẫn thấy huy hiệu, và `LOI_GHI` trong duLieu.js đếm chứ không nuốt im.
   */
  /**
   * ⚠ BA CHỖ PHẢI KHỚP NHAU, VÀ TỪNG LỆCH CẢ BA.
   *
   * Bản đầu ghi `loai: 'ontap'` với các trường trải thẳng ra ngoài. Nhìn riêng thì
   * hợp lý — đây đúng là kỳ ôn tập. Nhưng:
   *
   *   · `firestore.rules` chỉ cho `loai in ['chuong']` → máy chủ TỪ CHỐI;
   *   · từ chối là IM LẶNG, vì lệnh ghi không chờ kết quả (`LOI_GHI` đếm, không kêu);
   *   · `docHocBa` cũng chỉ nhặt `loai === 'chuong'`, nên dù có lọt cũng không ai đọc;
   *   · và nó đọc `v.giaTri`, trong khi bên này trải phẳng — hình dạng thứ ba.
   *
   * Hậu quả trên bản thật: bé làm xong kỳ ôn tập, huy hiệu hiện lên ngay (sổ tại
   * máy), nhưng máy chủ trống trơn. Đổi máy là mất, và sổ bố mẹ không bao giờ thấy.
   *
   * Cổng cũ không bắt được vì nó TỰ DỰNG gói `{loai:'chuong'}` rồi mang đi thử —
   * thử đúng cái luật cho phép, chứ không phải cái màn hình gửi đi. Nay
   * `test/hocba_khop_luat.test.mjs` đọc chính dòng dưới đây và đối chiếu với
   * `firestore.rules`.
   *
   * Ghi ĐÚNG cái sổ tại máy đang giữ (`giaTri`), không dựng hình dạng thứ hai: thẻ
   * huy hiệu đọc `xong.best`, mà bản cũ gửi `dung` — hoà sổ về là mất điểm cao nhất.
   */
  const xongOnTap = useCallback((ky, kq) => {
    const sau = ghiChuong(tienDo, ct.ma, ky.chapter,
      { dat: kq.dat, dung: kq.dung, tong: kq.tong });
    datTienDo(sau);
    const k = khoaChuong(ct.ma, ky.chapter);
    luuMucHocBa(learnerId, 'chuong', k, { giaTri: sau.chapters[k] });
    setView({ page: 'home' });
  }, [tienDo, datTienDo, setView, learnerId, ct.ma]);

  /**
   * XONG MỘT BÀI ĐỌC HIỂU — ghi HAI NƠI, đúng khuôn bài viết.
   *
   * ⚠ ĐỔI CHỦ Ý, 23-08-2026. Trước đây bài đọc chỉ ghi sổ TẠI MÁY, vì "bác chốt
   * bài đọc hiểu không cần vào sổ". Nay bác chốt ngược lại: phần đọc và phần viết
   * đều phải lên máy chủ và vào engine. Nên `hocBaTA` có thêm loại `doc`.
   *
   * ⚠ THÊM MỘT LOẠI LÀ SỬA BỐN CHỖ (xem chú thích trong `firestore.rules`): luật ·
   * `duLieu.js` bên đọc · chỗ gọi này · và phải `deploy --only firestore:rules`
   * TRƯỚC khi bản mới lên. Thiếu bước deploy thì Firestore từ chối TRONG IM LẶNG.
   */
  const xongDocHieu = useCallback((bai, kq) => {
    const unit = bai.phamVi === 'unit';
    const so = unit ? bai.unit : bai.chapter;
    const sau = ghiDocHieu(tienDo, ct.ma, so, kq, unit ? 'unit' : 'chuong');
    datTienDo(sau);
    const k = khoaDocHieu(ct.ma, so, unit ? 'unit' : 'chuong');
    luuMucHocBa(learnerId, 'doc', k, { giaTri: sau.docHieu?.[k] ?? null });
    setView({ page: 'home' });
  }, [tienDo, datTienDo, setView, learnerId, ct.ma]);

  /**
   * XONG MỘT BÀI VIẾT — ghi hai nơi, đúng khuôn kỳ ôn tập.
   *
   * Sổ tại máy để bé mở lại thấy ngay; `hocBaTA` (loai `viet`) để BỐ MẸ đọc được
   * bài viết và lời chấm — bác chốt điều ấy, và nó chỉ thành thật khi bài lên tới
   * máy chủ. Gói bọc trong `giaTri` y như `chuong`: bên đọc chỉ nhận một hình dạng.
   */
  const xongVietBai = useCallback((bai, kq) => {
    const unit = bai.phamVi === 'unit';
    const so = unit ? bai.unit : bai.chapter;
    const sau = ghiBaiViet(tienDo, ct.ma, so, kq, unit ? 'unit' : 'chuong');
    datTienDo(sau);
    const k = khoaBaiViet(ct.ma, so, unit ? 'unit' : 'chuong');
    luuMucHocBa(learnerId, 'viet', k, { giaTri: sau.baiViet[k] });
  }, [tienDo, datTienDo, learnerId, ct.ma]);

  /**
   * BÉ CHỌN TỪ MÌNH THÍCH NHẤT — ghi hai nơi, đúng khuôn bài viết ở trên.
   *
   * Phòng nói xưa nay hỏi rồi dùng ngay trong phiên, nhưng không nhớ. Ghi lại thì
   * cô giáo máy còn nhớ bé thích gì ở buổi sau — đó là cả điểm khác nhau giữa "có
   * hỏi" và "có biết về bé".
   *
   * ⚠ GHI Ở ĐÂY chứ không ghi thẳng trong `PhongNoi.jsx`, và không phải chuyện gu
   * kiến trúc: cổng `hocba_khop_luat.test.mjs` chỉ soi `luuMucHocBa` trong CHÍNH
   * tệp này. Gọi ở chỗ khác thì hình dạng gói không ai canh, mà sai hình dạng gói
   * thì máy chủ từ chối trong im lặng.
   */
  /**
   * NHẬT KÝ TỪNG LƯỢT TRẢ LỜI — gom cả phiên rồi dựng lại, không đẩy từng lượt.
   *
   * ⚠ VÌ SAO PHẢI GIỮ CẢ PHIÊN chứ không gửi mỗi lượt một lần: mã bản ghi nhúng
   * SỐ THỨ TỰ của lượt trong phiên. Đẩy từng lượt một thì số thứ tự lúc nào cũng
   * là 0, mọi lượt của cùng một câu đè lên nhau, và bé sai hai lần rồi mới đúng
   * chỉ còn lại MỘT dòng — đúng thứ mà nhật ký thô sinh ra để giữ. Dựng lại từ cả
   * phiên thì mã lượt cũ ra đúng mã cũ, `xepHang` ghi đè theo mã, nên gửi bao
   * nhiêu lần cũng không sinh dòng trùng. Đây là lối bên Toán đã dùng.
   */
  const nhatKy = useRef({ maPhien: null, ds: [] });
  const ghiLuot = useCallback((e) => {
    if (!e?.maPhien || !e?.microId || !e?.cau?.id) return;
    if (nhatKy.current.maPhien !== e.maPhien) {
      nhatKy.current = { maPhien: e.maPhien, ds: [] };
    }
    nhatKy.current.ds.push({
      itemId: e.cau.id,
      maNut: e.cau.maNut || null,
      maNutDs: e.cau.maNutDs || null,
      ok: e.ok,
      tries: e.lan,
      hintsUsed: e.hintsUsed,
      ms: e.ms,
      phase: e.phase || 'practice',
      answer: e.answer,
      expected: e.expected,
      mode: e.cau.format || null,
      khiNao: Date.now(),
    });
    /* Chiều Sư phạm: cộng lượt này vào bảng "bé làm tốt dạng nào". Chỉ đếm lượt
       ĐẦU của mỗi câu (`lan === 1`) — đếm cả lượt thử lại thì dạng nào cho phép
       thử nhiều lần tự nhiên có tỉ lệ đúng thấp hơn, mà đó là tính chất của dạng
       câu chứ không phải của bé. */
    if (e.lan === 1 && e.cau?.format) {
      datTienDo((p) => ghiDangCau(p, e.cau.format, e.ok));
    }
    /* Không `await`: bé đang học, không đợi mạng. Hỏng thì bản ghi nằm lại hàng
       đợi tại máy và `LOI_GHI` đếm — không nuốt im. */
    luuSuKien({
      uid: learnerId,
      maPhien: e.maPhien,
      microId: e.microId,
      quyen: ct.ma,
      viec: nhatKy.current.ds,
    });
  }, [learnerId, ct.ma, datTienDo]);

  /**
   * XONG MỘT THẺ ÔN — đẩy hộp Leitner rồi hẹn ngày mới.
   *
   * Luật hộp ở `lib/onlai.js` (`daySauKhiOn`) — bản chép của
   * `functions/src/schedule.js`, vì `functions/` là mã máy chủ và kéo nó vào gói
   * trình duyệt là mang theo cả `firebase-admin`. Cổng `tienganh_onlai` so hai
   * bên để chúng không trôi xa nhau.
   */
  const xongTheOn = useCallback((the, qua) => {
    const sau = daySauKhiOn(the, qua);
    datTheOn((ds) => ds.map((x) => (x.id === the.id ? sau : x)));
    luuTheOn(learnerId, sau);
  }, [learnerId]);

  const xongSoThich = useCallback((tu, unit = null) => {
    if (!tu) return;
    const sau = ghiSoThich(tienDo, ct.ma, tu, unit);
    datTienDo(sau);
    const k = khoaSoThich(ct.ma);
    luuMucHocBa(learnerId, 'soThich', k, { giaTri: sau.soThich[k] });
  }, [tienDo, datTienDo, learnerId, ct.ma]);

  if (view.page === 'onlai') {
    return (
      <OnLai
        the={theDenHan(theOn, { quyen: ct.ma })}
        onXongThe={xongTheOn}
        onLuot={ghiLuot}
        onThoat={() => setView({ page: 'home' })}
      />
    );
  }

  if (view.page === 'vietbai' && view.vietId) {
    const b = viets.find((x) => x.id === view.vietId);
    return (
      <VietBai bai={b} onLuot={ghiLuot} onThoat={() => setView({ page: 'home' })}
               onXong={(kq) => xongVietBai(b, kq)} />
    );
  }

  if (view.page === 'dochieu' && view.docId) {
    const b = docs.find((x) => x.id === view.docId);
    return (
      <DocHieu bai={b} onLuot={ghiLuot} onThoat={() => setView({ page: 'home' })}
               onXong={(kq) => xongDocHieu(b, kq)} />
    );
  }

  if (view.page === 'ontap' && view.kyId) {
    const ky = kyOn.find((k) => k.id === view.kyId);
    return (
      <OnTap ky={ky} onLuot={ghiLuot} onThoat={() => setView({ page: 'home' })}
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
        onMoc={(chang, m) => nhoMoc(view.baiId, chang, m)}
        /* ⚠ CHỖ NÀY TRỐNG SUỐT TỪ ĐỢT 1 TỚI 23-08-2026.
           `BaiHoc` có sẵn `onLuot` và nối sẵn cho cả chặng Luyện tập lẫn Sát hạch,
           4226 câu cũng đã được gắn `maNut` từ Đợt 1 — nhưng chỗ DỰNG nó ở đây
           không truyền hàm xuống, nên `onLuot` luôn là null và KHÔNG MỘT LƯỢT NÀO
           của bài học đi tới `attempts`. Cả đường BKT dựng ở Đợt 1 nằm im.
           Màn duy nhất từng nuôi engine là `OnLai`, mà thẻ ôn chỉ sinh ra SAU khi
           xong bài — nên gần như không bao giờ tới lượt.
           Không cổng nào bắt được: mỗi tệp một mình đều đúng, chỗ hỏng nằm ở CHỖ
           NỐI. Nay `tienganh_vao_engine.test.mjs` soi đúng chỗ nối này. */
        onLuot={ghiLuot}
        /* Biệt danh của chính bé đi vào đoạn hội thoại — bé nghe tên mình trong
           một câu tiếng Anh. Đó là chỗ bài này khác mọi bài luyện phát âm khác. */
        tenBe={(hoSo?.displayName || '').trim().split(/\s+/).pop() || 'Bo'}
        soThich={(tienDo.soThich || {})[khoaSoThich(ct.ma)] || null}
        onSoThich={xongSoThich}
        mucThao={mucThao}
        hoSoDang={tienDo.dinhDang || null}
      />
    );
  }

  return (
    <NhaQuyen
      ct={ct}
      bais={bais}
      kyOn={kyOn}
      docs={docs}
      viets={viets}
      tienDo={tienDo}
      onMoBai={(id) => setView({ page: 'bai', baiId: id })}
      onMoOnTap={(id) => setView({ page: 'ontap', kyId: id })}
      onMoDocHieu={(id) => setView({ page: 'dochieu', docId: id })}
      onMoVietBai={(id) => setView({ page: 'vietbai', vietId: id })}
      mucThao={mucThao}
      soTheOn={demDenHan(theOn, { quyen: ct.ma })}
      onMoOnLai={() => setView({ page: 'onlai' })}
      onVeKeSach={veKeSach}
    />
  );
}

/**
 * HỒ SƠ BÉ — hai câu cho bố mẹ, giấu trong "Góc bố mẹ".
 *
 * Chiều Sư phạm (mục 2.1.2-P) và CEFR mức bé (mục 2.3.1). Đây là chỗ DUY NHẤT
 * trên màn hình nói ra rằng hệ thống có biết gì về cách bé học.
 *
 * ── ⚠ IM LẶNG KHI CHƯA ĐỦ MẪU, ĐỪNG ĐOÁN ──
 * `manhNhat`/`yeuNhat` trả `null` cho tới khi một định dạng đủ 8 lượt. Không có
 * gì để nói thì không hiện dòng nào — thà trống còn hơn dán cho bé một cái nhãn
 * dựng trên hai câu, vì nhãn ấy đi vào cách bố mẹ nhìn con.
 *
 * Và hiện CẢ CỠ MẪU. Bố mẹ đọc "làm tốt nhất dạng chọn đáp án" mà không biết nó
 * dựng trên 9 câu hay 900 câu thì tin nó như nhau, mà hai con số ấy khác hẳn.
 */
function HoSoBe({ tienDo, ct }) {
  const hs = tienDo?.dinhDang || {};
  const manh = manhNhat(hs);
  const yeu = yeuNhat(hs);
  const cefr = ct?.cefr;
  if (!manh && !cefr) return null;
  const pc = (x) => `${Math.round(x.ti * 100)}%`;
  return (
    <GocBoMe ten="Góc bố mẹ · hệ thống biết gì về cách con học">
      <div className="flex flex-col gap-2 text-sm">
        {cefr && (
          <MucBoMe nhan="Trình độ quyển này">
            <p className="text-ink">{cefr} — khung tham chiếu châu Âu (CEFR)</p>
          </MucBoMe>
        )}
        {manh && (
          <MucBoMe nhan="Dạng câu con làm tốt nhất">
            <p className="text-ink">
              {manh.ten} — đúng {pc(manh)} <span className="text-mute">({manh.tong} câu)</span>
            </p>
          </MucBoMe>
        )}
        {yeu && (
          <MucBoMe nhan="Dạng con còn chật vật">
            <p className="text-ink">
              {yeu.ten} — đúng {pc(yeu)} <span className="text-mute">({yeu.tong} câu)</span>
            </p>
          </MucBoMe>
        )}
        <p className="text-xs leading-relaxed text-mute">
          Chỉ tính lượt trả lời ĐẦU của mỗi câu, và chỉ nói về dạng câu con đã làm
          đủ nhiều. Dạng nào con mới gặp vài lần thì chưa đủ để kết luận gì.
        </p>
      </div>
    </GocBoMe>
  );
}

/**
 * MA TRẬN TRẠNG THÁI — bé đang mắc ở đâu, và GỐC của chỗ mắc ấy là gì.
 *
 * Đợt 3 tính được `maTranTrangThai()` nhưng không màn nào bày ra — tính mà không
 * ai xem thì cũng như chưa có, đúng cùng dạng với `reviewQueue` trước Đợt 2.
 *
 * ── ⚠ BÀY Ở ĐÂY CHỨ KHÔNG PHẢI Ở MÀN CÔ GIÁO, VÀ ĐÓ LÀ RÀNG BUỘC KIẾN TRÚC ──
 * Màn cô giáo nằm ở `chung/`, mà `chung` KHÔNG được import `mon/` — cổng
 * `ranh_gioi` chặn, và nó chặn vì hai môn dính nhau thì sửa môn này gãy môn kia.
 * Phép tính ma trận thì nằm ở `mon/tienganh/lib/lantruyen.js`. Muốn đưa lên màn
 * cô giáo thì phải nới giao ước ở `src/soMon.js` — việc riêng, không nhét vào đây.
 *
 * ── GIÁ TRỊ THẬT NẰM Ở CỘT "GỐC" ──
 * "Con yếu mẫu câu unit 12" thì sổ nào cũng nói được. "Gốc là số đếm unit 2" mới
 * là thứ đổi được cách dạy — và đó chính là chỗ lan truyền ngược của mục 2.3.3
 * kiếm cơm.
 */
function MaTran({ mucThao }) {
  const [dt, datDt] = useState(null);
  useEffect(() => { let s = true; napDoThi().then((d) => s && datDt(d)); return () => { s = false; }; }, []);
  const ds = React.useMemo(
    () => (dt && mucThao ? maTranTrangThai(dt, mucThao, { toiDa: 5 }) : []),
    [dt, mucThao],
  );
  if (!ds.length) return null;
  return (
    <GocBoMe ten="Góc bố mẹ · con đang mắc ở đâu">
      <ul className="flex flex-col gap-2 text-sm">
        {ds.map((x) => (
          <li key={x.ma} className="rounded-xl2 bg-soft px-3 py-2">
            <p className="font-semibold text-ink">
              {x.nhan || x.ma}
              {' '}<span className="font-normal text-mute">— nắm {Math.round(x.p * 100)}%</span>
            </p>
            {x.goc && x.goc.ma !== x.ma && (
              <p className="text-gold-dark">
                Gốc đáng ngờ: <b>{x.goc.nhan || x.goc.ma}</b>
                {' '}<span className="text-mute">(cách {x.goc.buoc} bước, nắm {Math.round(x.goc.p * 100)}%)</span>
              </p>
            )}
          </li>
        ))}
      </ul>
      <p className="mt-2 text-xs leading-relaxed text-mute">
        Cột “gốc” là phần kiến thức mà phần trên DỰNG TRÊN. Con sai ở trên mà gốc
        chưa vững thì luyện thêm phần trên không gỡ được — nên xem gốc trước.
      </p>
    </GocBoMe>
  );
}

/* ─────────── trang chính của quyển ─────────── */

function NhaQuyen({
  ct, bais, kyOn = [], docs = [], viets = [], tienDo,
  onMoBai, onMoOnTap, onMoDocHieu, onMoVietBai, onVeKeSach,
  soTheOn = 0, onMoOnLai, mucThao = null,
}) {
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
  /* ── ĐỌC HIỂU · BÀI VIẾT · ÔN TẬP MỞ THEO CÙNG MỘT CỜ VỚI BÀI HỌC ──
   *
   * Ba loại thẻ ấy trước đây đòi XONG CẢ BỐN BÀI của chương mới mở, trong khi bài học
   * thì mở sẵn (`khoaBai: false` cho cả ba quyển Tiếng Anh). Hai luật ngược nhau trên
   * cùng một trang: bé bấm vào unit nào cũng học được, nhưng bài đọc của chính unit ấy
   * lại khoá.
   *
   * Nay hỏi ĐÚNG MỘT CỜ. Quyển nào khoá bài tuần tự thì ba thẻ này cũng khoá theo (và
   * vẫn hiện "còn mấy bài nữa"); quyển mở thì mở hết — người lớn xem trước được, bé
   * muốn đọc lại chương cũ cũng không phải làm lại bài. */
  const moThem = (dsBai) => (khoaBai ? moKyOnTap(tienDo, dsBai) : true);
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

      <HoSoBe tienDo={tienDo} ct={ct} />
      <MaTran mucThao={mucThao} />

      {/* ── THẺ MỜI ÔN LẠI ──
          Đứng TRÊN thẻ "bài tiếp theo", và đó là chủ ý: ôn cái sắp quên có giá
          hơn học thêm cái mới, mà bé thì luôn chọn cái nào đứng trước.

          ⚠ CHỈ HIỆN KHI CÓ THẺ TỚI HẠN. Hiện thường trực với con số 0 thì nó
          thành một nút chết trên trang chính, và bé học được cách bỏ qua nó —
          rồi bỏ qua luôn cả những hôm nó có số thật. */}
      {soTheOn > 0 && (
        <button type="button" onClick={onMoOnLai}
          className="flex items-center gap-4 rounded-xl2 bg-gold-pale p-5 text-left
            ring-2 ring-gold hover:brightness-105
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          <span className="text-4xl" aria-hidden="true">🔁</span>
          <span className="min-w-0 flex-1">
            <span className="block text-sm font-semibold uppercase tracking-wider text-gold-dark">
              Đến giờ ôn lại
            </span>
            <span className="block text-xl font-bold text-ink">
              {soTheOn} phần con học hôm trước
            </span>
            <span className="block text-sm text-gold-dark">
              Ôn nhanh vài câu để nhớ lâu hơn.
            </span>
          </span>
          <span className="flex-none rounded-xl2 bg-gold px-4 py-2 font-bold text-gold-dark">Ôn</span>
        </button>
      )}

      {/* MỘT VIỆC ĐƯỢC GỢI Ý, to và đứng trên cùng — nhưng KHÔNG còn là việc duy
          nhất. Bé chưa đọc được 16 tên bài để tự chọn, nên app vẫn phải chỉ đường;
          còn bố mẹ muốn nhắm thẳng vào unit đang học trên lớp thì bấm dưới danh
          sách. Hai lối, và lối gợi ý đứng trước vì bé mở app ra là bấm được ngay. */}
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

      {/* Quyển KHÔNG khoá bài thì phải nói ra, nếu không cái thẻ xanh to ở trên
          trông y hệt "chỉ được học bài này". Dòng cho bố mẹ đọc — bé thì thấy 16
          unit không cái nào đeo ổ khoá, đó mới là tín hiệu bé hiểu được. */}
      {!khoaBai && (
        <p className="rounded-xl2 bg-teal-pale px-4 py-2.5 text-sm text-teal-dark">
          Con bấm vào unit nào cũng học được — không phải theo thứ tự. Muốn theo
          đúng chương trình thì cứ bấm thẻ xanh ở trên.
        </p>
      )}

      {chuong.map((c) => (
        <section key={c.so} className="flex flex-col gap-2">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-mute">
            Chương {c.so} · {c.ten}
          </h2>
          <ul className="flex flex-col gap-2">
            {c.bai.map((b) => (
              <React.Fragment key={b.id}>
                <DongBai bai={b} m={tienDo?.micros?.[b.id]} onMo={onMoBai}
                         tt={trangThaiBai(tienDo, b.id, thuTu, opt)}
                         moSau={khoaBai ? moBai(tienDo, b.id, thuTu) : true} />
                {/* Hai ô luyện của CHÍNH unit ấy, nằm ngay dưới bài — bác chốt
                    18-08: học xong một unit thì đọc và viết ngay của unit ấy, không
                    phải chờ hết chương. Bài theo chương vẫn còn, ở cuối chương, và
                    là chỗ ÔN LẠI cả bốn unit. */}
                <OLuyenUnit
                  doc={docs.find((d) => d.phamVi === 'unit' && d.unit === b.so)}
                  viet={viets.find((v) => v.phamVi === 'unit' && v.unit === b.so)}
                  xongDoc={tienDo?.docHieu?.[khoaDocHieu(ct.ma, b.so, 'unit')]}
                  xongViet={tienDo?.baiViet?.[khoaBaiViet(ct.ma, b.so, 'unit')]}
                  mo={khoaBai ? moBai(tienDo, b.id, thuTu) : true}
                  onDoc={onMoDocHieu} onViet={onMoVietBai} />
              </React.Fragment>
            ))}
          </ul>
          {/* Kỳ ôn tập đứng NGAY SAU bốn bài của chính chương nó, không gom hết
              xuống cuối quyển: bé vừa học xong chương thì cái mốc phải nằm ngay
              đó, chứ không phải ở một chỗ khác mà bé chẳng bao giờ cuộn tới. */}
          {/* Bài đọc hiểu đứng TRƯỚC kỳ ôn tập: đọc là việc học tiếp, còn kỳ ôn
              tập là chỗ CHỐT chương. Chốt xong rồi mới đọc thì cái chốt hết nghĩa. */}
          {docs.filter((d) => d.chapter === c.so && d.phamVi !== 'unit').map((d) => (
            <TheDocHieu key={d.id} bai={d} onMo={onMoDocHieu}
                        mo={moThem(c.bai.map((b) => b.id))}
                        conThieu={conThieuChoOnTap(tienDo, c.bai.map((b) => b.id))}
                        xong={tienDo?.docHieu?.[khoaDocHieu(ct.ma, c.so)]} />
          ))}
          {viets.filter((v) => v.chapter === c.so && v.phamVi !== 'unit').map((v) => (
            <TheVietBai key={v.id} bai={v} onMo={onMoVietBai}
                        mo={moThem(c.bai.map((b) => b.id))}
                        conThieu={conThieuChoOnTap(tienDo, c.bai.map((b) => b.id))}
                        xong={tienDo?.baiViet?.[khoaBaiViet(ct.ma, c.so)]} />
          ))}
          {kyOn.filter((k) => k.chapter === c.so).map((k) => (
            <TheOnTap key={k.id} ky={k} onMo={onMoOnTap}
                      mo={moThem(c.bai.map((b) => b.id))}
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
/**
 * HAI Ô LUYỆN CỦA MỘT UNIT — đọc hiểu và bài viết của chính bài vừa học.
 *
 * Dáng NHỎ và nằm thụt vào so với dòng bài: chúng là phần luyện thêm của bài ấy,
 * không phải một bài ngang hàng. Ba thẻ to (đọc hiểu · bài viết · ôn tập) của chương
 * vẫn giữ nguyên ở cuối chương.
 *
 * Unit nào không dựng được bài (vốn câu quá mỏng, xem `sinh_dochieu_tienganh.py`)
 * thì ô ấy không hiện — chứ không hiện một nút bấm vào chẳng có gì.
 */
function OLuyenUnit({ doc, viet, xongDoc, xongViet, mo, onDoc, onViet }) {
  if (!doc && !viet) return null;
  const o = (bai, xong, onMo, chu, bieuTuong) => (bai ? (
    <button type="button" disabled={!mo} onClick={() => onMo(bai.id)}
      className={`flex items-center gap-1.5 rounded-xl2 border-2 px-3 py-1.5 text-sm
        font-semibold focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
        ${xong ? 'border-teal bg-teal-pale text-teal-dark'
          : mo ? 'border-line bg-white text-navy hover:border-navy'
          : 'cursor-not-allowed border-line bg-soft text-mute opacity-60'}`}>
      <span aria-hidden="true">{bieuTuong}</span>{chu}{xong ? ' ✓' : ''}
    </button>
  ) : null);
  return (
    <li className="-mt-1 flex flex-wrap gap-2 pl-4">
      {o(doc, xongDoc?.dat, onDoc, 'Đọc hiểu', '📖')}
      {o(viet, Number.isFinite(xongViet?.diem), onViet, 'Viết', '✍️')}
    </li>
  );
}

/* Cùng dáng với thẻ kỳ ôn tập, khác BIỂU TƯỢNG và khác lời: 📖 chứ không 🏅, và
   "Đọc" chứ không "Thi thử". Hai việc khác nhau thì phải nhìn ra là khác nhau. */
function TheDocHieu({ bai, mo, conThieu, xong, onMo }) {
  const dat = !!xong?.dat;
  return (
    <button type="button" disabled={!mo && !dat} onClick={() => onMo(bai.id)}
      className={`flex items-center gap-3 rounded-xl2 border-2 border-dashed p-4 text-left
        focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
        ${dat ? 'border-teal bg-teal-pale'
          : mo ? 'border-navy bg-soft hover:brightness-105'
          : 'cursor-not-allowed border-line bg-soft opacity-60'}`}>
      <span className="text-3xl" aria-hidden="true">{dat ? '📖' : mo ? '📖' : '🔒'}</span>
      <span className="min-w-0 flex-1">
        <span className="block font-bold text-ink">{bai.name}</span>
        <span className="block text-sm text-mute">
          {dat ? `Con đã đọc xong · ${xong.best}/${xong.tong} câu đúng`
            : mo ? `Đoạn ${bai.doan?.length || 0} câu · ${bai.soCau} câu hỏi`
            : conThieu === 1 ? 'Còn 1 bài nữa trong chương này là mở'
            : `Còn ${conThieu} bài nữa trong chương này là mở`}
        </span>
      </span>
      {(mo || dat) && (
        <span className="flex-none rounded-xl2 bg-white px-3 py-1.5 text-sm font-bold text-navy">
          {dat ? 'Đọc lại' : 'Đọc'}
        </span>
      )}
    </button>
  );
}

/* Thẻ bài viết. Điểm hiện trên thẻ thì PHẢI kèm chữ "máy chấm" — cùng một luật với
   màn lời chấm, và đây là chỗ thứ hai con số ấy lộ ra. */
function TheVietBai({ bai, mo, conThieu, xong, onMo }) {
  const daViet = Number.isFinite(xong?.diem);
  return (
    <button type="button" disabled={!mo && !daViet} onClick={() => onMo(bai.id)}
      className={`flex items-center gap-3 rounded-xl2 border-2 border-dashed p-4 text-left
        focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
        ${daViet ? 'border-teal bg-teal-pale'
          : mo ? 'border-navy bg-soft hover:brightness-105'
          : 'cursor-not-allowed border-line bg-soft opacity-60'}`}>
      <span className="text-3xl" aria-hidden="true">{mo || daViet ? '✍️' : '🔒'}</span>
      <span className="min-w-0 flex-1">
        <span className="block font-bold text-ink">{bai.name}</span>
        <span className="block text-sm text-mute">
          {daViet ? `Con đã viết · ${xong.diem}/10 điểm (máy chấm)`
            : mo ? `Viết ${bai.toiThieu}–3 câu, cô giáo máy chấm cho con`
            : conThieu === 1 ? 'Còn 1 bài nữa trong chương này là mở'
            : `Còn ${conThieu} bài nữa trong chương này là mở`}
        </span>
      </span>
      {(mo || daViet) && (
        <span className="flex-none rounded-xl2 bg-white px-3 py-1.5 text-sm font-bold text-navy">
          {daViet ? 'Viết lại' : 'Viết'}
        </span>
      )}
    </button>
  );
}

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
