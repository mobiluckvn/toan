import React, { useCallback, useEffect, useRef, useState } from 'react';
import HinhVe from './HinhVe.jsx';
import { Tranh } from './DocHieu.jsx';
import { hinhCuaTu, napBai, maBaiTruoc, napKichBanNoi, kichBanCua } from '../lib/noiDung.js';
import {
  vonTu, tuTrongCau, tachTheoTieng, UNIT_CU_TOI_DA,
  tinhBuoi, loiKet, cauHoiSoThich, PHUT_TOI_DA,
} from '../lib/phongnoi.js';
import { hoiCoGiao, luuBuoi } from '../lib/goiPhongNoi.js';
import { auth } from '../../../chung/lib/nenTang.js';
import { doc as docLen, docDoan, docDuoc, coGiong, thoiDoc } from '../lib/doclen.js';
import { batDauNghe, ngheDuoc, loiDocDuoc, xinMicroChiTiet, MICRO, TIENG } from '../lib/nghenoi.js';
import { chamTot, chamCau, datNoi, loiKhen } from '../lib/chamnoi.js';

/**
 * PHÒNG LUYỆN NÓI — bé nói chuyện với cô giáo máy, trong đúng vốn từ của unit.
 *
 * ── KHÁC CHẶNG "NÓI CHUYỆN" Ở CHỖ NÀO ──
 * Chặng ấy đi theo kịch bản viết sẵn: bé biết trước phải nói gì, và hết kịch bản là
 * hết. Ở đây câu do máy sinh, nên bé hỏi lại được, nói sai thì cô nói theo cách
 * khác, và không bao giờ hết câu. Đó mới là chỗ tập DÙNG tiếng Anh.
 *
 * ── BA THỨ BÉ LỚP 1 CẦN, VÀ CẢ BA ĐỀU KHÔNG PHẢI CHỮ ──
 *  1. NGHE ĐƯỢC. Câu tiếng Anh đọc giọng en-GB, lời tiếng Việt giọng vi-VN, và đọc
 *     TỰ ĐỘNG ngay khi cô trả lời — bé chưa đọc chữ thì chờ bé bấm là chờ mãi.
 *  2. NHÌN THẤY NGHĨA. Cô nói tới từ nào thì hiện hình từ ấy (bác dặn 13-08). Không
 *     có hình thì phòng này quay về thành một khối chữ.
 *  3. MỘT NÚT DUY NHẤT để nói. Không menu, không lựa chọn.
 *
 * ── KHÔNG ĐỂ BÉ KẸT ──
 * Máy không nghe được, không đọc được, hoặc mạng hỏng — cả ba đều nói THẲNG ra và
 * vẫn cho bé ở lại phòng nghe cô nói. Đây là chỗ luyện thêm, không phải cửa ải.
 */
export default function PhongNoi({ bai, tienDo, tenBe = 'con',
                                   soThich = null, onSoThich = null }) {
  /**
   * QUYỂN VÀ LỚP SUY TỪ CHÍNH BÀI, không nhận từ ngoài.
   *
   * ⚠ Ba chỗ trước đây ghim cứng lớp 1, và không chỗ nào kêu:
   *   · `napKichBanNoi()` gọi không tham số → lớp 2·3 tải kịch bản của LỚP 1,
   *     `kichBanCua` không thấy bài nào, cả tầng kịch bản tắt lặng lẽ;
   *   · `lop = 1` mặc định mà `BaiHoc.jsx` không truyền → lời dặn gọi bé lớp 3 là
   *     "a six-year-old";
   *   · `luuBuoi({ quyen: 'ta1' })` → sổ trên máy chủ ghi mọi buổi vào quyển 1,
   *     bố mẹ mở ra thấy con học lớp 3 mà buổi nào cũng đề "ta1".
   * Bài học đã mang sẵn `quyen` và `grade`; hỏi nó thì không có gì để mà quên.
   */
  const ma = bai?.quyen || 'ta1';
  const lop = bai?.grade || 1;
  const daDat = !!tienDo?.micros?.[bai?.id]?.pass;
  const [baiCu, datBaiCu] = useState([]);

  /* Nạp các unit trước CHỈ khi bé đã đạt unit này — chưa đạt thì vốn từ bó trong
     unit ấy, nạp thêm là tải mấy tệp chẳng dùng tới. */
  useEffect(() => {
    let song = true;
    if (!daDat || !bai?.id) { datBaiCu([]); return () => { song = false; }; }
    (async () => {
      const ds = maBaiTruoc(bai.id, UNIT_CU_TOI_DA);
      const d = await Promise.all(ds.map((x) => napBai(x).catch(() => null)));
      if (song) datBaiCu(d.filter(Boolean));
    })();
    return () => { song = false; };
  }, [bai?.id, daDat]);

  /* Kịch bản của CHÍNH bài này. Không nạp được thì phòng vẫn chạy bằng cách cũ —
     bé không được đứng chờ chỉ vì một tệp không tải về. */
  useEffect(() => {
    let song = true;
    datKbXong(false);
    napKichBanNoi(ma)
      .then((ds) => { if (song) datKichBan(kichBanCua(ds, bai?.id)); })
      .catch(() => {})
      .finally(() => { if (song) datKbXong(true); });
    return () => { song = false; };
  }, [bai?.id, ma]);

  const datCu = useCallback((id) => !!tienDo?.micros?.[id]?.pass, [tienDo]);
  const von = React.useMemo(
    () => vonTu({ baiNay: bai, baiCu, daDat, datCu }),
    [bai, baiCu, daDat, datCu],
  );

  /* Mỗi lần mở phòng của một unit là MỘT buổi. Mã buổi dựng một lần rồi giữ nguyên,
     để mọi lượt của buổi ấy ghi đè lên cùng một tài liệu chứ không rải ra. */
  const maBuoi = useRef(null);
  if (!maBuoi.current && bai?.id) {
    maBuoi.current = `${String(bai.id).replace(/[:.]/g, '_')}__${Date.now()}`;
  }
  const [lichSu, datLichSu] = useState([]);
  const [dangHoi, datDangHoi] = useState(false);
  const [dangNghe, datDangNghe] = useState(false);
  const [tam, datTam] = useState('');
  const [loi, datLoi] = useState(null);
  const [micHong, datMicHong] = useState(false);
  const [thich, datThich] = useState(null);
  const [kichBan, datKichBan] = useState(null);
  const [kbXong, datKbXong] = useState(false);   // đã nạp xong HOẶC đã bỏ cuộc

  const laTranh = kichBan?.dang === 'tranh';

  /**
   * MỐC TIẾNG ANH CỦA CHÍNH BUỔI NÀY — để lời cô không bị đọc nhầm sang giọng Việt.
   *
   * Bác bắt 19-08-2026: lời hướng dẫn có lẫn tiếng Anh mà máy đọc hết bằng giọng
   * Việt. `tachTheoTieng` vốn chỉ nhận ra tiếng Anh nằm trong VỐN TỪ CỦA UNIT —
   * đúng cho bài thường, hỏng ở bài tả tranh vì câu cô trích là câu của kho tích
   * luỹ. Nên đưa thêm: bản mô tả tranh, mọi câu trong kịch bản, và mọi câu cô ĐÃ
   * NÓI trong buổi. Ba nguồn ấy chắc hơn vốn từ, vì chúng là chữ có thật trên màn.
   */
  const mocEn = React.useMemo(() => [
    ...(kichBan?.moTaTranh || []),
    ...((kichBan?.buoc || []).map((b) => b.en).filter(Boolean)),
    ...lichSu.filter((x) => x.vai === 'may' && x.en).map((x) => x.en),
  ], [kichBan, lichSu]);
  const batDau = useRef(Date.now());
  /* `nhip` KHÔNG mang giá trị nào — nó chỉ để bắt màn hình vẽ lại mỗi 30 giây, để
     đồng hồ 20 phút tự tới nơi. Bản đầu viết `Date.now() + nhip * 0`: chạy đúng,
     nhưng nhân 0 thì ai đọc cũng tưởng lỗi rồi xoá đi, và xoá là đồng hồ chết. */
  const [, datNhip] = useState(0);
  /* Bé đang nói lại ô nào — để đúng nút ấy đổi mặt, chứ không phải cả danh sách. */
  const [laiO, datLaiO] = useState(null);
  /* Đếm số buổi trong một lần mở phòng. Chỉ để bắt effect chào chạy lại sau khi bé
     bấm "nói lại từ đầu" — xem `noiLaiTuDau`. */
  const [lanBuoi, datLanBuoi] = useState(0);
  const cuoiDs = useRef(null);
  const phien = useRef(null);
  const daChao = useRef(false);
  const daDocKet = useRef(false);

  /* `findLast` chứ không `[...lichSu].reverse().find(...)`: cùng kết quả, nhưng
     không phải chép cả mảng, và quan trọng hơn — nói thẳng ý "câu CUỐI của cô".
     Bản cũ có chữ `.reverse()` nằm ngay cạnh chỗ bày danh sách, mà chiều bày thì
     vừa đổi hai lần; để lẫn vào đấy là sớm muộn có người sửa nhầm. */
  const luotCoCuoi = lichSu.findLast((x) => x.vai === 'may');
  /**
   * CÂU BÉ CẦN NÓI — không phải câu cô vừa nói.
   *
   * ⚠ Bác bắt 19-08-2026: "Phần nói là AI đóng vai trò giáo viên hướng dẫn học sinh
   * tả tranh chứ không phải là bắt học sinh nói theo mấy câu kiểu What can you see."
   *
   * Cả phòng này dựng trên giả định BÉ NHẠI LẠI CÂU CÔ VỪA NÓI, và phép chấm cũng
   * thế. Với bài tả tranh thì sai hẳn: cô HỎI, bé phải ĐÁP. Trải một buổi ra giấy
   * thấy bé nói "what can you see?" và được 9/10 — hệ thống khen bé vì nhại đúng
   * câu hỏi. Không có gì đỏ, điểm còn cao.
   *
   * Nay lượt của cô mang theo `can` (những câu được tính là đúng). Bài thường thì
   * `can` chính là câu cô nói, nên 20 kịch bản kia không đổi hành vi.
   */
  const canNoiGi = luotCoCuoi?.can?.length ? luotCoCuoi.can
    : (luotCoCuoi?.en ? [luotCoCuoi.en] : []);
  const buoi = tinhBuoi({ lichSu, batDau: batDau.current, bayGio: Date.now(),
                         dichCaDoan: kichBan?.dang === 'tranh' });
  const ket = loiKet(buoi);
  const hoiThich = cauHoiSoThich(von);

  /**
   * SỞ THÍCH NHỚ TỪ BUỔI TRƯỚC — nhưng CHỈ DÙNG NẾU TỪ ẤY CÒN TRONG VỐN.
   *
   * `dongHoSo()` nhét từ này thẳng vào lời dặn LLM ("The child told you they like
   * …"). Vốn từ là hàng rào duy nhất giữ cô giáo máy không nói ra chữ bé chưa học
   * — nên một từ đi vòng qua hàng rào ấy là tự mình chọc thủng tầng chống ảo giác,
   * mà chọc từ phía trong thì `cauHopLe()` phía sau cũng không cứu được: nó bác câu
   * có chữ lạ, thế là cô giáo cứ nói rồi cứ bị bác, buổi học đứng im.
   *
   * Sổ sống lâu hơn nội dung — bé đổi quyển, sách dồn unit, hay sổ cũ còn nằm trên
   * máy sau một lần dựng lại — nên KHÔNG tin từ nhớ được. Soi lại, mỗi lần mở màn.
   */
  const thichNho = React.useMemo(() => {
    const t = String(soThich?.tu || '');
    if (!t) return null;
    const co = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)].some((x) => x.tu === t);
    return co ? t : null;
  }, [soThich, von]);
  const thichDung = thich || thichNho;

  useEffect(() => () => { phien.current?.huy(); thoiDoc(); }, []);
  /* Nhịp 30 giây chỉ để VẼ LẠI, không đụng gì tới dữ liệu — hết 20 phút mà màn
     hình không tự biết thì bé cứ nói tiếp, rồi đúng lượt sau mới bị cắt ngang. */
  useEffect(() => { const id = setInterval(() => datNhip((n) => n + 1), 30000); return () => clearInterval(id); }, []);
  /**
   * CÓ LƯỢT MỚI THÌ TỰ CUỘN XUỐNG — bác chốt 14-08.
   *
   * Đã đi qua hai chiều và chiều nào cũng có chỗ hỏng, nên ghi lại cả hai kẻo mai
   * kia lại lật:
   *
   *   · MỚI Ở DƯỚI (bản đầu) — đúng lối trò chuyện ai cũng quen, nhưng KHÔNG tự
   *     cuộn: bé nói xong, cô trả lời ở dưới màn hình, bé ngồi nhìn câu cũ.
   *   · MỚI Ở TRÊN (bản 13-08) — chữa được chuyện phải cuộn, nhưng đọc ngược đời:
   *     bé muốn xem lại buổi học thì phải đọc từ dưới lên.
   *
   * Nay giữ chiều tự nhiên VÀ tự cuộn — cái thiếu của bản đầu chỉ là mấy dòng này,
   * chứ không phải chiều bày. Neo đặt sau NÚT MICRO chứ không sau danh sách: cuộn
   * tới đó là bé thấy cùng lúc câu cô vừa nói và cái nút phải bấm tiếp.
   *
   * ⚠ Xoá dòng này thì không có gì đỏ cả — chỉ là bé không bao giờ thấy cô trả
   * lời. Có cổng canh, đừng dọn đi.
   */
  useEffect(() => {
    cuoiDs.current?.scrollIntoView({ block: 'end', behavior: 'smooth' });
  }, [lichSu, dangHoi, buoi.trangThai]);

  /**
   * ĐỌC LUÔN CÂU KẾT — bác dặn 14-08: "câu kết thúc cũng nên chuyển sang Voice".
   *
   * Cả buổi mọi thứ đều có tiếng, tới lúc chia tay thì màn hình im bặt. Với bé chưa
   * đọc chữ thì đó là phòng học tắt tiếng giữa chừng.
   *
   * Chốt bằng `ref` chứ không bằng deps: `ket` là object dựng lại mỗi lần vẽ, mà
   * nhịp 30 giây thì cứ 30 giây vẽ một lần — để nó vào deps là cứ nửa phút cô lại
   * chào tạm biệt một lần.
   */
  useEffect(() => {
    if (!ket || daDocKet.current) return;
    daDocKet.current = true;
    (async () => {
      thoiDoc();
      if (ket.en) await docLen(ket.en, 'en-GB', { nhanh: 0.9 });
      await docDoan(tachTheoTieng(ket.chu, von, mocEn));
    })();
  }, [ket, von]);

  /* Gửi một lượt lên cô giáo. `themVaoLichSu` nhận lịch sử ĐÃ có lượt của bé —
     đọc state ngay tại đây thì lượt vừa thêm chưa kịp vào, và cô trả lời câu cũ. */
  const guiLuot = useCallback(async (ds) => {
    datLoi(null); datDangHoi(true);
    try {
      const tra = await hoiCoGiao({ von, lichSu: ds, tenBe, lop,
        haDoKho: buoi.haDoKho, hoSo: { thich: thichDung }, kichBan });
      /* `buoc` — bước nào sinh ra lượt này. Không bày ra màn hình, nhưng
         `luotLuyen` cần: lượt bé đáp lời chào KHÔNG được tính là một lần luyện. */
      const luot = { vai: 'may', chu: tra.en || tra.vi, en: tra.en, vi: tra.vi,
                     buoc: tra.buoc, can: tra.can };
      const sau = [...ds, luot];
      datLichSu(sau);
      /* Client giữ ngữ cảnh và tự đẩy lên máy chủ — bác chốt như thế; server không
         lưu gì. KHÔNG chờ: mất mạng thì bé vẫn nói chuyện bình thường. */
      luuBuoi(auth?.currentUser?.uid, {
        maBuoi: maBuoi.current, quyen: ma, baiId: bai?.id, tenBai: bai?.title, lichSu: sau,
      });
      /* Câu tiếng Anh đọc nguyên khối giọng en-GB; lời giải thích thì TÁCH theo
         thứ tiếng — trong đó thường có lẫn chính từ bé đang học. */
      (async () => {
        thoiDoc();
        if (tra.en) await docLen(tra.en, 'en-GB', { nhanh: 0.9 });
        await docDoan(tachTheoTieng(tra.vi, von, mocEn));
      })();
    } catch (e) {
      /* Nói đúng chỗ hỏng. "Có lỗi xảy ra" là câu vô dụng nhất — bố mẹ không biết
         phải sửa gì, mà mấy lỗi ở đây thì mỗi lỗi một cách chữa hẳn. */
      datLoi(e?.code === 'functions/permission-denied'
        ? 'Khoá của cô giáo máy chưa dùng được — người lớn kiểm tra giúp con nhé.'
        : e?.code === 'functions/unauthenticated'
          ? 'Con đăng nhập rồi mới vào phòng này được nhé.'
          : 'Cô giáo máy chưa trả lời được. Con thử lại nhé.');
    } finally { datDangHoi(false); }
  }, [von, tenBe, lop, bai, buoi.haDoKho, thichDung, kichBan, ma, mocEn]);

  /* Cô chào trước. Bé 6 tuổi mở ra thấy màn trắng thì không biết làm gì cả. */
  useEffect(() => {
    /* ĐỢI KỊCH BẢN rồi mới chào. Bản đầu chào ngay, mà kịch bản nạp không đồng bộ
       nên lượt ĐẦU TIÊN — lượt định ra cả buổi — rơi về lối cũ: cô nói thẳng
       "ball" thay vì "Hello!". Nhìn màn hình mới thấy. Nạp hỏng cũng đặt cờ này,
       để bé không phải đứng chờ một tệp không bao giờ về. */
    if (daChao.current || !bai || !kbXong) return;
    daChao.current = true;
    guiLuot([{ vai: 'be', chu: 'Chào cô, con muốn tập nói.' }]);
  }, [bai, kbXong, guiLuot, lanBuoi]);

  /**
   * GHI ÂM MỘT LẦN — chỉ lo cái micro, không biết gì về cuộc trò chuyện.
   *
   * Tách ra vì nay có HAI chỗ cần nghe bé nói: lượt mới (`noi`) và nói lại một câu
   * cũ (`noiLai`). Chép đôi cái đoạn xin quyền · bật máy · bắt lỗi này là sớm muộn
   * hai bản lệch nhau, mà lệch ở đây thì hoặc bé kẹt, hoặc máy nghe lại chính nó.
   *
   * Trả `null` khi không nghe được, và ĐÃ báo lỗi ra màn hình rồi — bên gọi chỉ cần
   * dừng lại, không phải đoán vì sao.
   */
  const ghiAm = useCallback(async () => {
    if (dangNghe) { phien.current?.dung(); return null; }
    datLoi(null); datTam('');
    const cho = await xinMicroChiTiet();
    if (cho !== MICRO.duoc) { datMicHong(true); datLoi(loiDocDuoc(cho)); return null; }
    thoiDoc();                       // đang đọc mà bật micro thì máy nghe lại chính nó
    datDangNghe(true);
    const p = batDauNghe({ onTam: datTam, tieng: TIENG });
    phien.current = p;
    try {
      const { chu, phuongAn } = await p.xong;
      const noiGi = (chu || '').trim();
      if (!noiGi) { datLoi('Cô chưa nghe thấy gì. Con nói to hơn một chút nhé.'); return null; }
      return { noiGi, phuongAn };
    } catch (e) {
      datMicHong(true);
      datLoi(e?.message || loiDocDuoc(e?.ma));
      return null;
    } finally { datDangNghe(false); phien.current = null; }
  }, [dangNghe]);

  const noi = useCallback(async () => {
    const r = await ghiAm();
    if (!r) return;
    /* Chấm khi bé đang NHẠI LẠI câu cô vừa nói. Bé nói câu khác thì không chấm —
       chấm một câu bé tự nghĩ ra theo mẫu của câu khác là chấm sai. */
    /* Chấm với TỪNG câu được chấp nhận rồi lấy điểm cao nhất: ở bước `taTranh` bé
       tả câu nào trong tranh cũng đúng, nên bắt khớp đúng một câu là chấm sai. */
    const nghe = r.phuongAn?.length ? r.phuongAn : [r.noiGi];
    const kq = canNoiGi.length
      ? canNoiGi.map((c) => ({ ...chamTot(chamCau, c, nghe), mau: c }))
        .reduce((a, b) => (b.diem > a.diem ? b : a))
      : null;
    /* GIỮ LẠI CÂU MẪU ngay trong lượt của bé. Không giữ thì nút "nói lại" sau này
       chẳng biết đang chấm theo câu nào — lúc bé bấm thì cô đã nói sang câu khác
       rồi, và chấm theo câu mới là chấm sai một câu bé không hề định nói. */
    /* ── GIỮ CẢ CHỖ BÉ BỎ SÓT, không chỉ điểm ── (bác chốt 18-08)
       `chamCau` đã tính sẵn `thieu` (chữ có nghĩa bé không nói) và `thieuChucNang`
       (chữ chức năng: is, a, the…) từ lâu, nhưng cả hai bị vứt ngay tại dòng này —
       chỉ `diem` được giữ. Nên cô giáo máy không có cách nào biết bé sót chữ nào,
       và lời sửa đành chung chung ("con nói lại nhé"). Đúng chỗ bác gọi là máy.
       Nay đi kèm lượt của bé, rồi `dongBuoc` gửi lên cùng lời dặn. */
    const sau = [...lichSu, {
      vai: 'be',
      chu: r.noiGi,
      diem: kq?.diem ?? null,
      mau: kq?.mau || luotCoCuoi?.en || null,
      thieu: kq?.thieu || [],
      thieuChucNang: kq?.thieuChucNang || [],
    }];
    datLichSu(sau);
    /* Lượt này vừa KẾT THÚC buổi thì đừng hỏi cô nữa: bé đã xong, mà gọi thêm
       một lượt là hoặc cô nói chen vào sau lời khen, hoặc mạng trục trặc và bé
       thấy dòng lỗi đỏ ngay dưới câu "con giỏi lắm". Đã thấy thật lúc đi thử. */
    const sauKhiNoi = tinhBuoi({ lichSu: sau, batDau: batDau.current, bayGio: Date.now() });
    if (sauKhiNoi.trangThai !== 'dang') { datLoi(null); return; }
    guiLuot(sau);
  }, [ghiAm, lichSu, canNoiGi, luotCoCuoi, guiLuot]);

  /**
   * NÓI LẠI MỘT CÂU — bác dặn 14-08.
   *
   * Trước nay bé nói một lần rồi thôi: được 4 điểm thì cô cứ thế nói sang câu khác,
   * và cái câu bé chưa nói được nằm lại đó vĩnh viễn. Nhưng phát âm thì không ai
   * sửa được trong một lần — nghe lại, thử lại, nghe lại mới là cách học nói.
   *
   * ── VÌ SAO SỬA TẠI CHỖ, KHÔNG THÊM LƯỢT MỚI ──
   * Thêm lượt thì cuộc trò chuyện phình ra toàn câu hỏng của chính bé, và cô sẽ
   * trả lời từng lần thử — bé chỉ muốn đọc lại cho tròn tiếng chứ không muốn nói
   * chuyện. Nên nói lại KHÔNG gọi cô: chỉ chấm lại đúng ô ấy.
   *
   * ── GIỮ LẦN TỐT NHẤT, VÀ GIỮ CẢ CÂU CỦA LẦN ẤY ──
   * Giữ điểm cao mà hiện chữ của lần mới nhất thì thẻ nói dối: "con nói X, 9 điểm"
   * trong khi 9 điểm là của lần trước. Hai thứ phải đi cùng nhau.
   */
  const noiLai = useCallback(async (chiSo) => {
    const cu = lichSu[chiSo];
    if (!cu?.mau) return;
    datLaiO(chiSo);
    const r = await ghiAm();
    datLaiO(null);
    if (!r) return;
    const kq = chamTot(chamCau, cu.mau, r.phuongAn?.length ? r.phuongAn : [r.noiGi]);
    const hon = (kq?.diem ?? 0) > (cu.diem ?? -1);
    const sau = lichSu.map((x, i) => (i !== chiSo ? x : {
      ...x,
      chu: hon ? r.noiGi : x.chu,
      diem: hon ? kq.diem : x.diem,
      /* Chỗ sót đi CÙNG lần thử được giữ lại. Giữ điểm của lần này mà giữ chỗ sót
         của lần kia thì cô sửa một chữ bé đã nói được rồi. */
      thieu: hon ? (kq.thieu || []) : x.thieu,
      thieuChucNang: hon ? (kq.thieuChucNang || []) : x.thieuChucNang,
      soLan: (x.soLan || 1) + 1,
    }));
    datLichSu(sau);
    luuBuoi(auth?.currentUser?.uid, {
      maBuoi: maBuoi.current, quyen: ma, baiId: bai?.id, tenBai: bai?.title, lichSu: sau,
    });
  }, [ghiAm, lichSu, bai]);

  /**
   * NÓI CHUYỆN LẠI TỪ ĐẦU — vì màn kết là ngõ cụt.
   *
   * Xong buổi thì nút micro biến mất (đúng), nhưng bé lớp 1 thích thì muốn chơi
   * lại ngay chứ không đợi mai. Không có nút này thì bé phải thoát ra rồi vào lại
   * — mà bé 6 tuổi không nghĩ ra chuyện đó.
   *
   * Mã buổi dựng LẠI, để buổi mới không ghi đè lên buổi vừa xong trên máy chủ.
   */
  const noiLaiTuDau = useCallback(() => {
    thoiDoc();
    phien.current?.huy();
    datLichSu([]); datLoi(null); datTam(''); datMicHong(false);
    batDau.current = Date.now();
    maBuoi.current = `${String(bai?.id).replace(/[:.]/g, '_')}__${Date.now()}`;
    daChao.current = false;
    daDocKet.current = false;
    /* Cờ `daChao` là ref nên đổi nó KHÔNG làm effect chào chạy lại. Phải có một
       con số trong deps thì React mới ngó tới — thiếu dòng này là bấm nút xong
       màn hình trắng trơn, không ai chào cả. */
    datLanBuoi((n) => n + 1);
  }, [bai?.id]);

  const dsTu = [...von.loi.tu, ...von.on.flatMap((x) => x.tu)];

  return (
    <section className="flex flex-col gap-3">      {/* ⚠ BỎ KHỐI "CON NÓI VỀ" Ở BÀI TẢ TRANH — bác chốt 19-08-2026.
          Nó liệt kê sẵn từng vật kèm HÌNH: kite · yo-yo · kitten · teddy bear. Với
          bài tả tranh thì đó chính là ĐÁP ÁN bày ra trước mặt — bé chỉ việc đọc
          bảng chứ không phải nhìn tranh mà tìm chữ. Bài thường thì bảng ấy vẫn
          đúng việc của nó (vốn từ của unit), nên giữ.
          Đồng hồ "còn mấy phút" tách ra đứng riêng, vì nó cần cho cả hai loại. */}
      {buoi.trangThai === 'dang' && buoi.phutConLai <= 5 && (
        <p className="text-right">
          <span className="rounded-full bg-gold-pale px-2 py-0.5 text-xs font-bold text-gold-dark">
            còn {Math.ceil(buoi.phutConLai)} phút
          </span>
        </p>
      )}
      {laTranh ? null : (
      <div className="rounded-xl2 border-2 border-line bg-white p-3">
        <div className="flex flex-wrap items-baseline gap-x-3">
          <h3 className="text-sm font-bold uppercase tracking-wide text-navy">Con nói về</h3>
          <p className="text-sm text-mute">
            {von.moRong
              ? `${dsTu.length} từ — có cả từ mấy bài trước con đã học`
              : `${dsTu.length} từ của bài này`}
          </p>
        </div>
        <ul className="mt-2 flex flex-wrap gap-2">
          {dsTu.map((t) => (
            <li key={t.tu}>
              <button type="button" onClick={() => docLen(t.tu, 'en-GB', { nhanh: 0.9 })}
                aria-label={`Nghe từ ${t.tu} — ${t.nghia}`}
                className="flex w-[4.5rem] flex-col items-center gap-0.5 rounded-xl2 border-2
                  border-line bg-soft p-2 transition hover:brightness-95
                  focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
                <span className="text-3xl leading-none"><HinhVe ten={t.tu} {...hinhCuaTu(bai, t.tu)} /></span>
                <span className="text-[0.7rem] font-semibold leading-tight text-ink">{t.tu}</span>
              </button>
            </li>
          ))}
        </ul>
      </div>
      )}

      {/* ══ BỨC TRANH — bé CHỈ ĐƯỢC NHÌN TRANH ══ (bác chốt 19-08-2026)
          "Bài nói sẽ cho một bức tranh và cùng mô tả về bức tranh đó (AI sẽ có phần
          mô tả bức tranh bằng chữ còn học sinh thì chỉ được nhìn tranh thôi)."
          Nên trên màn KHÔNG bày `moTaTranh` ra ở đâu cả — nó chỉ đi lên lời dặn cho
          mô hình. Bày ra là bé đọc chứ không phải tả. */}
      <Tranh src={kichBan?.tranh} ten={kichBan?.ten} />

      {!docDuoc() && (
        <p className="rounded-xl2 bg-gold-pale p-3 text-sm text-gold-dark">
          Máy này chưa đọc thành tiếng được. Con vẫn nói chuyện được, nhưng phải nhờ
          bố mẹ đọc hộ câu tiếng Anh.
        </p>
      )}
      {docDuoc() && !coGiong('en-GB') && (
        <p className="rounded-xl2 bg-gold-pale p-3 text-sm text-gold-dark">
          Máy chưa có giọng tiếng Anh — câu tiếng Anh sẽ đọc bằng giọng máy sẵn có,
          nghe hơi lạ. Người lớn cài thêm giọng tiếng Anh giúp con nhé.
        </p>
      )}

      {/* HỎI BÉ THÍCH GÌ — hỏi MỘT LẦN, bằng hình, trước khi vào nói chuyện.
          Bé bấm vào hình chứ không gõ và không nói tự do: bé 6 tuổi không gõ được,
          mà nói tự do thì bộ nhận dạng nghe ra gì cũng được. Câu trả lời rơi đúng
          vào vốn từ của bài nên không có từ lạ nào lọt vào phòng, và KHÔNG có
          thông tin riêng tư nào mới rời khỏi máy — chỉ là một từ trong sách. */}
      {/* ⚠ BỎ THẺ "CON THÍCH CÁI NÀO NHẤT" Ở BÀI TẢ TRANH — bác chốt 19-08-2026.
          Thẻ ấy sinh ra cho bài thường: bé chọn một thứ rồi cô lấy nó điền vào ô
          trống của mẫu câu. Bài tả tranh không có ô trống nào, và cũng không hỏi
          bé thích gì — nó hỏi bé NHÌN THẤY gì. Để lại là chen một việc lạ vào giữa,
          lại còn bày sẵn tên mấy vật trong tranh kèm hình. */}
      {/* `thichDung` chứ không `thich`: nhớ được từ buổi trước thì ĐỪNG HỎI LẠI —
          hỏi lại chính là cái làm phần nhớ thành vô nghĩa. */}
      {!laTranh && !thichDung && hoiThich && buoi.trangThai === 'dang' && (
        <div className="rounded-xl2 border-2 border-gold bg-gold-pale p-4">
          <p className="text-lg font-bold text-navy">{hoiThich.hoi}</p>
          <p className="text-sm text-gold-dark">Con chọn một cái, rồi mình sẽ tập nói về nó.</p>
          <ul className="mt-2 flex flex-wrap gap-2">
            {hoiThich.chon.map((t) => (
              <li key={t.tu}>
                <button type="button"
                  onClick={() => { datThich(t.tu); onSoThich?.(t.tu, bai?.unit ?? null); }}
                  aria-label={`Con thích ${t.nghia} (${t.tu})`}
                  className="flex w-[5rem] flex-col items-center gap-0.5 rounded-xl2 border-2
                    border-line bg-white p-2 transition hover:brightness-95
                    focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
                  <span className="text-4xl leading-none"><HinhVe ten={t.tu} {...hinhCuaTu(bai, t.tu)} /></span>
                  <span className="text-[0.7rem] font-semibold text-ink">{t.nghia}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {buoi.haDoKho && buoi.trangThai === 'dang' && (
        <p className="rounded-xl2 bg-gold-pale p-3 text-sm text-gold-dark">
          Mình tập lại từng từ một cho dễ nhé — xong rồi mới ghép thành câu.
        </p>
      )}

      {/* CUỘC TRÒ CHUYỆN — CŨ Ở TRÊN, MỚI Ở DƯỚI.
          Đánh số theo chỉ số THẬT trong `lichSu` rồi mới lọc, chứ không lọc trước:
          nút "nói lại" sửa đúng một ô trong mảng gốc, mà lọc trước thì số thứ tự
          xê dịch một nấc và bé bấm ô này lại sửa ô khác.
          Lượt đầu là câu chào mình tự gửi hộ bé để cô mở lời — không phải bé nói,
          nên không bày ra. */}
      <ol className="flex flex-col gap-3">
        {lichSu
          .map((x, i) => ({ x, i }))
          .filter(({ x, i }) => !(i === 0 && x.vai === 'be'))
          .map(({ x, i }) => (
            <li key={i}>
              {x.vai === 'may'
                ? <LuotCo luot={x} bai={bai} von={von} />
                : (
                  <LuotBe luot={x} dangNghe={laiO === i && dangNghe}
                    onNoiLai={x.mau && buoi.trangThai === 'dang' && ngheDuoc() && !micHong
                      ? () => noiLai(i) : null} />
                )}
            </li>
          ))}
        {dangHoi && <li className="text-sm text-mute">Cô đang nghĩ…</li>}
      </ol>

      {/* MÀN KẾT — bé phải thấy vạch đích. Một việc không có chỗ kết thì bé không
          bao giờ thấy mình LÀM ĐƯỢC, mà đó mới là thứ giữ bé quay lại.
          Nay nằm CUỐI cuộc trò chuyện vì nó là thứ mới nhất, và có tiếng: câu
          tiếng Anh đọc giọng en-GB, lời tiếng Việt giọng vi-VN. */}
      {ket && (
        <div className={`rounded-xl2 p-5 ${buoi.trangThai === 'xongGioi' ? 'bg-teal-pale' : 'bg-gold-pale'}`}>
          <p className="text-4xl" aria-hidden="true">{ket.bieuTuong}</p>
          <p className="mt-1 text-2xl font-bold text-ink">{ket.tieuDe}</p>
          {ket.en && (
            <div className="mt-2 flex flex-wrap items-center gap-3">
              <p className="flex-1 font-serif text-2xl text-navy">{ket.en}</p>
              <button type="button" onClick={() => docLen(ket.en, 'en-GB', { nhanh: 0.9 })}
                aria-label={`Nghe lại: ${ket.en}`}
                className="h-12 w-12 flex-none rounded-full border-2 border-teal bg-white text-2xl
                  text-teal-dark hover:bg-teal hover:text-white
                  focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
                <span aria-hidden="true">🔈</span>
              </button>
            </div>
          )}
          <div className="mt-1 flex items-center gap-2">
            <p className="flex-1 text-ink">{ket.chu}</p>
            <button type="button" onClick={() => docDoan(tachTheoTieng(ket.chu, von, mocEn))}
              aria-label={`Nghe lại lời tiếng Việt: ${ket.chu}`}
              className="h-9 w-9 flex-none rounded-full border-2 border-line text-sm text-mute
                hover:border-navy hover:text-navy
                focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
              <span aria-hidden="true">🔈</span>
            </button>
          </div>
          {/* Xong buổi thì nút micro biến mất — không có đường này thì bé phải
              thoát ra vào lại mới nói tiếp được, mà bé 6 tuổi không nghĩ ra. */}
          <button type="button" onClick={noiLaiTuDau}
            className="mt-3 rounded-xl2 border-2 border-navy bg-white px-5 py-3 text-lg
              font-semibold text-navy transition hover:brightness-95
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            <span aria-hidden="true">🔁</span> Mình nói chuyện lại nhé
          </button>
        </div>
      )}

      {loi && <p className="rounded-xl2 bg-gold-pale p-3 text-gold-dark">{loi}</p>}

      {/* MỘT NÚT DUY NHẤT, đứng DƯỚI cuộc trò chuyện — đúng chỗ bé vừa đọc tới.
          Bản 13-08 đưa nút lên trên vì danh sách bày ngược; nay danh sách xuôi
          chiều và màn hình tự cuộn nên nút về lại chỗ tự nhiên của nó. Nó nằm sau
          câu cô vừa nói, nên cuộn tới neo là bé thấy CẢ HAI cùng lúc. */}
      {buoi.trangThai !== 'dang' ? null : ngheDuoc() && !micHong ? (
        <button type="button" onClick={noi} disabled={dangHoi || laiO != null}
          className={`flex items-center justify-center gap-3 rounded-xl2 px-6 py-6 text-2xl
            font-semibold transition disabled:opacity-60
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
            ${dangNghe && laiO == null ? 'bg-alert text-white' : 'bg-teal text-teal-dark hover:brightness-105'}`}>
          <span aria-hidden="true">{dangNghe && laiO == null ? '⏹️' : '🎤'}</span>
          {dangNghe && laiO == null ? 'Đang nghe con…' : 'Đến lượt con'}
        </button>
      ) : (
        <p className="rounded-xl2 border-2 border-line bg-soft p-4 text-mute">
          <b className="block text-ink">Máy này chưa nghe được</b>
          Phần nói cần trình duyệt Chrome và có mạng. Con cứ bấm vào hình để nghe cô
          đọc từng từ, rồi đọc theo nhé.
        </p>
      )}
      {dangNghe && (
        <p className="min-h-[1.6rem] text-center italic text-teal-dark">
          {tam ? `“${tam}”` : 'Con nói to và rõ nhé…'}
        </p>
      )}

      {/* NEO CUỘN — đặt SAU nút micro, không phải sau danh sách. Cuộn tới đây là
          câu cô vừa nói và cái nút phải bấm cùng nằm trong tầm mắt. */}
      <div ref={cuoiDs} aria-hidden="true" />
    </section>
  );
}

/* ─────────── một lượt của cô ─────────── */

function LuotCo({ luot, bai, von }) {
  const hinh = tuTrongCau(luot.en, von);
  return (
    <div className="flex flex-col gap-2 rounded-xl2 border-2 border-navy bg-white p-4">
      <div className="flex flex-wrap items-center gap-3">
        <span className="text-2xl" aria-hidden="true">🗣️</span>
        <p className="flex-1 font-serif text-2xl text-navy">{luot.en}</p>
        <button type="button" onClick={() => docLen(luot.en, 'en-GB', { nhanh: 0.9 })}
          aria-label={`Nghe lại: ${luot.en}`}
          className="h-12 w-12 flex-none rounded-full border-2 border-teal bg-teal-pale text-2xl
            text-teal-dark hover:bg-teal hover:text-white
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          <span aria-hidden="true">🔈</span>
        </button>
      </div>

      {/* Hình của các từ cô vừa nói tới — chỗ bé hiểu nghĩa mà không cần đọc chữ. */}
      {hinh.length > 0 && (
        <ul className="flex flex-wrap gap-2">
          {hinh.map((t) => (
            <li key={t.tu} className="flex w-[4rem] flex-col items-center rounded-xl2 bg-soft p-1.5">
              <span className="text-3xl leading-none"><HinhVe ten={t.tu} {...hinhCuaTu(bai, t.tu)} /></span>
              <span className="text-[0.65rem] text-mute">{t.nghia}</span>
            </li>
          ))}
        </ul>
      )}

      {luot.vi && (
        <div className="flex items-center gap-2">
          <p className="flex-1 text-ink">{luot.vi}</p>
          <button type="button" onClick={() => docDoan(tachTheoTieng(luot.vi, von, mocEn))}
            aria-label={`Nghe lại lời tiếng Việt: ${luot.vi}`}
            className="h-9 w-9 flex-none rounded-full border-2 border-line text-sm text-mute
              hover:border-navy hover:text-navy
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            <span aria-hidden="true">🔈</span>
          </button>
        </div>
      )}
    </div>
  );
}

/* ─────────── một lượt của bé ─────────── */

function LuotBe({ luot, onNoiLai = null, dangNghe = false }) {
  const dat = luot.diem != null && datNoi(luot.diem);
  return (
    <div className={`ml-8 flex flex-wrap items-center gap-3 rounded-xl2 p-3
      ${luot.diem == null ? 'bg-soft' : dat ? 'bg-teal-pale' : 'bg-gold-pale'}`}>
      <span className="text-xl" aria-hidden="true">🧒</span>
      <p className="flex-1 font-mono text-ink">“{luot.chu}”</p>
      {/* Đã thử mấy lần — bé thấy công mình bỏ ra, và bố mẹ thấy con có chịu sửa
          không. Chỉ hiện từ lần thứ hai: "1 lần" thì chẳng nói lên điều gì. */}
      {luot.soLan > 1 && (
        <span className="text-xs text-mute">{luot.soLan} lần</span>
      )}
      {luot.diem != null && (
        <span className="text-lg" aria-label={`${loiKhen({ diem: luot.diem }).sao} sao`}>
          {'⭐'.repeat(loiKhen({ diem: luot.diem }).sao)}
        </span>
      )}
      {/* NÓI LẠI CÂU NÀY. Hiện cả khi bé đã đạt: đạt 6 điểm rồi vẫn có quyền muốn
          nói cho tròn tiếng hơn, và đó chính là lúc bé đang tự học. */}
      {onNoiLai && (
        <button type="button" onClick={onNoiLai} disabled={dangNghe}
          aria-label={`Nói lại câu: ${luot.mau}`}
          className={`flex-none rounded-full border-2 px-3 py-1.5 text-sm font-semibold
            transition disabled:opacity-70
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold
            ${dangNghe ? 'border-alert bg-alert text-white' : 'border-navy bg-white text-navy hover:bg-navy hover:text-white'}`}>
          <span aria-hidden="true">{dangNghe ? '⏹️' : '🔁'}</span> {dangNghe ? 'Đang nghe…' : 'Nói lại'}
        </button>
      )}
    </div>
  );
}
