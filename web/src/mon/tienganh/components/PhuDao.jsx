/**
 * MÀN PHỤ ĐẠO — nhánh thứ ba của Hàm chính sách π (mục 2.5.1 · 3.4.7 · 3.5.3).
 *
 * ── VÌ SAO TỆP NÀY TỒN TẠI ──
 * `lib/phudao.js` (Thuật toán 3.10) viết xong từ Đợt 4 và có cổng kiểm đầy đủ,
 * nhưng tới 26-08-2026 KHÔNG MÀN NÀO GỌI — nó chỉ chạy trong `web/test/`. Nghĩa là
 * nhánh mà mục 2.5.1 gọi là "cốt lõi của tính thích ứng" chưa từng chạm tới một
 * đứa trẻ nào. Tệp này là chỗ nối.
 *
 * ── ⚠ MỜI, KHÔNG CẮT NGANG ──
 * Bé vừa sai ba câu liền. Quăng thẳng một bài mới vào giữa mạch học là lấy mất
 * quyền quyết định của bé đúng lúc bé đang chông chênh nhất — và ràng buộc R2 nói
 * rõ: không ai được kẹt, mọi cửa đều phải có đường vòng. Nên đây là một LỜI MỜI,
 * có nút "Để sau", đúng lối `moiLamLai` mà chặng luyện tập đã dùng.
 *
 * ── ⚠ NẠP MUỘN, VÀ ĐÓ LÀ CHỦ Ý ──
 * Thành phần này chỉ được dựng KHI đã có bé mắc thật. Bé học trôi chảy thì không
 * tải thêm tệp bài nào, không nạp đồ thị, không tốn một lượt mạng nào. Đặt phần
 * nạp ở `BaiHoc.jsx` thì mọi bé đều trả giá cho một nhánh phần lớn không dùng tới.
 *
 * ── ⚠ HỎNG THÌ IM VÀ TRẢ BÉ VỀ CHỖ CŨ ──
 * Không nạp được đồ thị, không tải được bài của nút gốc rễ, kho tĩnh không có câu
 * nào hợp lệ — cả ba đều KHÔNG được biến thành màn trắng. Bé đang học dở và màn
 * hình vừa hứa sẽ giúp; mất mạch học lúc ấy nặng hơn là không có phụ đạo.
 */
import React, { useEffect, useRef, useState } from 'react';
import CauHoi from './CauHoi.jsx';
import { napDoThi, baiCuaNut, baiTienQuyet, nhanNut } from '../lib/doThi.js';
import { napBai, maBaiTruoc } from '../lib/noiDung.js';
import { dungBang } from '../lib/bangtrangthai.js';
import { dungPhuDao, cauHoiHopLe, soiCauAI, soCauPhuDao } from '../lib/phudao.js';
import { nhoSinh } from '../lib/goiPhuDao.js';
import { luuCauChoDuyet } from '../lib/duLieu.js';
import { auth } from '../../../chung/lib/nenTang.js';
import { vonTu, UNIT_CU_TOI_DA, tachTheoTieng } from '../lib/phongnoi.js';
import { docDoan, thoiDoc } from '../lib/doclen.js';

/**
 * Dựng bài phụ đạo cho một nút bé đang mắc.
 *
 * Trả `{ trangThai, bai, loi }` — `trangThai` là 'dangDung' | 'xong' | 'khongCo'.
 */
function useBaiPhuDao({ baiNay, maNutMac, mucThao, tienDo, tenBe, nhan = null, lop = 1 }) {
  const [kq, datKq] = useState({ trangThai: 'dangDung', bai: null });

  useEffect(() => {
    let song = true;
    (async () => {
      try {
        const dt = await napDoThi();

        /* Tính nút gốc rễ TRƯỚC, để biết phải tải bài nào. `dungPhuDao` sẽ tính
           lại đúng con số ấy (hàm thuần, cùng đầu vào cho cùng đầu ra) — chấp nhận
           tính hai lần, đổi lấy việc không phải sửa chữ ký của Thuật toán 3.10. */
        /* Qua BẢNG TRẠNG THÁI (việc V6) — một nguồn sự thật về bé cho cả bốn
           màn, thay vì mỗi màn tự gọi một hàm riêng. */
        const goc = dungBang({ doThi: dt, mucThao, maNutMac }).nutGocRe;
        const maBaiGoc = baiCuaNut(dt, goc);

        /* ⚠ VỐN TỪ PHẢI GỒM CẢ BÀI CỦA NÚT GỐC RỄ.
           Nút gốc rễ thường nằm ở một bài CŨ, có khi ở quyển khác. Nếu vốn từ chỉ
           dựng từ bài hiện tại và cửa sổ ba bài liền trước thì chính những câu phụ
           đạo của nút ấy sẽ bị hậu kiểm bác vì "ngoài vốn" — bác đúng luật nhưng
           sai ý: bé ĐÃ HỌC bài ấy rồi, đó là cả lý do ta lùi về đây. */
        const datCu = (id) => !!tienDo?.micros?.[id]?.pass;
        const daDat = datCu(baiNay?.id);
        const dsCu = daDat ? maBaiTruoc(baiNay.id, UNIT_CU_TOI_DA) : [];
        const nutBai = [...new Set(
          (baiNay?.practice?.pools ? Object.values(baiNay.practice.pools).flat() : [])
            .map((c) => c?.maNut).filter(Boolean),
        )];
        const dsTQ = daDat ? baiTienQuyet(dt, nutBai, { boQua: baiNay.id }).filter(datCu) : [];
        const canTai = [...new Set([maBaiGoc, ...dsCu, ...dsTQ])]
          .filter((x) => x && x !== baiNay?.id);

        const daTai = (await Promise.all(canTai.map((x) => napBai(x).catch(() => null))))
          .filter(Boolean);
        if (!song) return;

        const baiGoc = daTai.find((b) => b.id === maBaiGoc) || null;
        const von = vonTu({
          baiNay,
          baiCu: daTai.filter((b) => dsCu.includes(b.id)),
          /* Bài của nút gốc rễ đi vào phần ôn kể cả khi đồ thị không khai nó là
             tiên quyết của bài hiện tại — nó là tiên quyết của chính NÚT đang mắc. */
          baiTQ: daTai.filter((b) => b.id !== baiNay?.id
            && (b.id === maBaiGoc || dsTQ.includes(b.id))),
          daDat,
          datCu,
        });

        const r = await dungPhuDao({
          dt,
          mucThao,
          maNutMac,
          /* Bài của nút gốc rễ đứng TRƯỚC: `cauTinhCuaNut` duyệt theo thứ tự, và
             câu của chính nút gốc rễ mới là thứ ta đi tìm. */
          baiDs: [baiGoc, baiNay].filter(Boolean),
          von,
          nhan,
          /* ── ĐƯỜNG CUỐI: NHỜ MÔ HÌNH SOẠN CÂU (việc V9) ──
             `dungPhuDao` chỉ gọi tới đây khi HAI vòng kho tĩnh không đủ câu, và nó
             bắt mọi lỗi — mất mạng, chưa có khoá, mô hình trả rác thì phụ đạo vẫn
             ra bài bằng phần tĩnh đã có. Xem khối chú thích ở cuối tệp. */
          goiLLM: ({ maNut, von: v, soCau }) => nhoSinh({ maNut, nhan: nhanNut(dt, maNut),
            von: v, soCau, lop }),
          /* HAI tầng hậu kiểm, và chúng soi hai thứ khác nhau:
             `cauHoiHopLe` — câu có dùng chữ bé đã học không (vốn từ);
             `soiCauAI`    — câu có phải là một CÂU HỎI dùng được không (hai đáp án
                             đúng, đáp án ngoài danh sách, gợi ý lộ đáp án…).
             Thiếu tầng thứ hai thì câu "hai đáp án đúng" đi lọt — đúng chỗ khối chú
             thích cuối tệp đã cảnh báo trước khi cắm mô hình. */
          soiCau: (c) => cauHoiHopLe(c, { von, tenBe })
            && (c.nguon !== 'ai' || soiCauAI(c).ok),
          /* NG27 đọc LÚC GỌI (Bảng 4.7, điểm 5) — ngữ cảnh phiên mang sẵn môn, khối lớp. */
          soCau: soCauPhuDao({ nut: maNutMac || undefined }),
        });
        if (!song) return;

        /* Câu do mô hình soạn đi vào HÀNG ĐỢI DUYỆT — người lớn xem rồi mới được
           ghép vào kho tĩnh. Không chờ: bé đang đợi bài, và mất mạng thì chỉ là câu
           ấy không lên được hàng đợi. */
        for (const c of (r.choDuyet || [])) {
          luuCauChoDuyet(auth?.currentUser?.uid, r.nutGoc, c);
        }

        datKq(r.cau.length
          /* `von` đi kèm để `tachTheoTieng` tách được mẩu tiếng Anh trong câu chẩn
             đoán lúc đọc to — nhãn nút từ vựng là `mango, quả xoài`, và đọc cả câu
             bằng giọng Việt thì chữ Anh ra một thứ tiếng không phải tiếng nào. */
          ? { trangThai: 'xong', bai: { ...r, von, nhanGoc: nhanNut(dt, r.nutGoc) } }
          : { trangThai: 'khongCo', bai: null });
      } catch {
        /* Hỏng thì coi như không có bài — bé được mời đi tiếp, không thấy lỗi nào. */
        if (song) datKq({ trangThai: 'khongCo', bai: null });
      }
    })();
    return () => { song = false; };
    /* ⚠ CHỈ DỰNG LẠI KHI ĐỔI BÀI HOẶC ĐỔI NÚT MẮC.
       `mucThao` và `tienDo` là đối tượng do màn cha giữ; đưa chúng vào dãy phụ
       thuộc thì mỗi lần cha vẽ lại là dựng lại cả bài phụ đạo — bé đang làm dở câu
       thứ hai thì màn nhảy về đầu. Ở đây ta CỐ Ý dùng bản chụp tại lúc kích hoạt:
       chuỗi sai liên tiếp đã xảy ra rồi, trạng thái mới hơn không đổi được chẩn
       đoán của lần can thiệp này. */
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [baiNay?.id, maNutMac]);

  return kq;
}

/**
 * @param onXong  ({lam, soCau, dung, nutGoc, itemIds}) => void — gọi ĐÚNG MỘT LẦN,
 *                kể cả khi bé bấm "Để sau" hay khi không dựng được bài. Bên gọi
 *                dựa vào đó để trả bé về mạch học, nên nuốt một đường ra là bé kẹt.
 */
export default function PhuDao({
  baiNay, maNutMac, mucThao, tienDo, tenBe = 'Bo', onLuot = null, onXong,
  nhan = null, lop = 1,
}) {
  const { trangThai, bai } = useBaiPhuDao({
    baiNay, maNutMac, mucThao, tienDo, tenBe, nhan, lop,
  });
  const [i, datI] = useState(0);
  const [dung, datDung] = useState(0);
  const [batDau, datBatDau] = useState(false);

  /**
   * ĐỌC CÂU CHẨN ĐOÁN — một lần, lúc màn mời hiện ra (việc V9).
   *
   * Bé sáu tuổi chưa đọc được chữ, nên một dòng chữ một mình chưa đủ. Đọc bằng
   * `tachTheoTieng`: câu chẩn đoán có thể mang một mẩu tiếng Anh (nhãn nút từ vựng
   * là `mango, quả xoài`), và đọc cả câu bằng giọng Việt thì chữ Anh ra một thứ
   * tiếng không phải tiếng nào — đúng luật "mỗi dòng một thứ tiếng" bác bắt 13-08.
   */
  const daDocChanDoan = useRef(false);
  useEffect(() => {
    if (daDocChanDoan.current || batDau || !bai?.chanDoan) return;
    daDocChanDoan.current = true;
    (async () => {
      thoiDoc();
      const von = bai.von || { loi: { tu: [], cau: [], cauSach: [] }, on: [] };
      await docDoan(tachTheoTieng(bai.chanDoan, von));
    })().catch(() => {});
  }, [bai, batDau]);

  /* Không dựng được bài thì đi tiếp NGAY, đừng bắt bé bấm một nút chỉ để nghe báo
     là không có gì. Gọi trong effect chứ không giữa lúc vẽ.
     ⚠ `daBao` chặn gọi hai lần: `onXong` do màn cha dựng lại mỗi lần vẽ, nên dãy
     phụ thuộc của effect đổi theo — mà `onXong` thì ghi một mục học bạ, gọi hai
     lần là hai bản ghi cho cùng một lần can thiệp, và phép đếm A-R-A lệch. */
  const daBao = useRef(false);
  useEffect(() => {
    if (trangThai !== 'khongCo' || daBao.current) return;
    daBao.current = true;
    onXong({ lam: false, viSao: 'khongDungDuocBai' });
  }, [trangThai, onXong]);

  if (trangThai === 'dangDung') {
    return (
      <section className="rounded-xl2 border-2 border-line bg-white p-6">
        <p className="text-lg font-semibold text-ink">Đợi cô một chút nhé…</p>
        <p className="text-mute">Cô đang tìm chỗ con vướng.</p>
      </section>
    );
  }
  if (trangThai !== 'xong' || !bai) return null;

  const ds = bai.cau;

  if (!batDau) {
    return (
      <section className="flex flex-col items-start gap-4">
        <div className="w-full rounded-xl2 bg-gold-pale p-6">
          <p className="text-4xl" aria-hidden="true">🔎</p>
          <p className="mt-2 text-2xl font-bold text-ink">Mình gỡ chỗ này cùng nhau nhé</p>
          {/* Nhãn ĐỌC ĐƯỢC, không bao giờ là mã máy. Bày `v_g3_u10_break_time` ra
              cho bé (hay cho bố mẹ ngồi cạnh) là đúng lỗi đã xảy ra ngày 22-08. */}
          {/* ── CÂU CHẨN ĐOÁN (việc V9) ──
              Hệ thống BIẾT vì sao nó lùi về đây: nó vừa tính ra nút nào bé mắc và
              nút nào là gốc. Không nói ra thì cả tầng lan truyền ngược — thứ đắt
              nhất của môn này — nhìn từ phía bé chỉ là một bài tập ngẫu nhiên. */}
          {!!bai.chanDoan && (
            <p className="mt-1 font-semibold text-gold-dark">{bai.chanDoan}</p>
          )}
          <p className="text-gold-dark">
            {bai.nhanGoc
              ? <>Cô thấy con chưa chắc phần <b>{bai.nhanGoc}</b>. Làm {ds.length} câu
                  ngắn về phần ấy rồi mình quay lại nhé.</>
              : <>Cô có {ds.length} câu ngắn giúp con dễ hơn. Làm xong mình quay lại bài nhé.</>}
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button type="button" onClick={() => datBatDau(true)}
            className="rounded-xl2 bg-navy px-6 py-3 text-lg font-semibold text-white
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            Làm {ds.length} câu →
          </button>
          {/* ĐƯỜNG VÒNG BẮT BUỘC — ràng buộc R2. Bé không muốn thì thôi, và không
              mất gì cả: bài phụ đạo không phải cửa ải. */}
          <button type="button"
            onClick={() => onXong({ lam: false, viSao: 'deSau', nutGoc: bai.nutGoc })}
            className="rounded-xl2 border-2 border-line px-5 py-3 font-semibold text-mute
              hover:border-navy hover:text-navy
              focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
            Để sau
          </button>
        </div>
      </section>
    );
  }

  const cau = ds[i];
  if (!cau) {
    return (
      <section className="flex flex-col items-start gap-4">
        <div className="w-full rounded-xl2 bg-teal-pale p-6">
          <p className="text-4xl" aria-hidden="true">👍</p>
          <p className="mt-2 text-2xl font-bold text-ink">Xong rồi, mình quay lại bài nhé</p>
          <p className="text-teal-dark">Con làm đúng {dung}/{ds.length} câu.</p>
        </div>
        <button type="button"
          onClick={() => onXong({
            lam: true, soCau: ds.length, dung, nutGoc: bai.nutGoc,
            itemIds: ds.map((c) => c.id), nguon: bai.nguon, luiVe: bai.luiVe,
          })}
          className="rounded-xl2 bg-navy px-6 py-3 text-lg font-semibold text-white
            focus:outline-none focus-visible:ring-4 focus-visible:ring-gold">
          Quay lại bài →
        </button>
      </section>
    );
  }

  return (
    <section className="flex flex-col gap-4">
      <div className="rounded-xl2 bg-gold-pale px-4 py-2">
        <p className="text-sm font-semibold text-gold-dark">
          Phần gỡ rối · câu {i + 1}/{ds.length}
          {bai.nhanGoc ? <> · {bai.nhanGoc}</> : null}
        </p>
      </div>
      <div className="rounded-xl2 border-2 border-line bg-white p-5">
        {/* `key` bắt buộc — cùng lý do với chặng luyện tập: đổi câu mà giữ state cũ
            thì lúc chuyển giữa hai dạng đáp án là trắng màn. */}
        <CauHoi key={cau.id} cau={cau}
          onXong={(kq) => {
            if (kq.dung) datDung((n) => n + 1);
            datI((n) => n + 1);
          }}
          /* ⚠ Lượt phụ đạo VẪN vào mô hình, và vẫn mang pha `practice`: bé TỰ trả
             lời, nên đúng phạm vi mà mục 3.4.3 cho phép cập nhật mức tinh thông.
             Bỏ ra ngoài thì chính bài gỡ rối không được ghi công, và đường cong học
             tập thủng đúng chỗ đáng xem nhất. */
          onLuot={onLuot} />
      </div>
    </section>
  );
}

/* ── ĐƯỜNG MÔ HÌNH: ĐÃ CẮM 09-10-2026 (việc V9) ────────────────────────────────
 *
 * Khối dưới đây là bản chú thích CŨ, giữ lại vì lập luận của nó vẫn đúng và chính
 * nó định ra điều kiện để được cắm. Nay điều kiện ấy đã làm xong:
 *
 *   · `soiCauAI` (ở `lib/phudao.js`) soi SÁU luật của một câu hỏi mà vốn từ không
 *     nói được: hai phương án trùng nhau (→ hai đáp án đúng), đáp án ngoài danh
 *     sách, gợi ý lộ đáp án, một phương án, lời dẫn rỗng, lời dẫn có số;
 *   · luật thứ bảy — "phương án nhiễu có thật là cái sai trẻ hay mắc hay chỉ là
 *     một chữ bừa" — KHÔNG kiểm được bằng code, nên câu phải qua HÀNG ĐỢI DUYỆT
 *     (`choDuyetTA`): bé ghi được, chỉ người lớn đọc và duyệt được;
 *   · và đường tĩnh vẫn đi TRƯỚC, hai vòng (nút gốc rễ #1, rồi #2). Mô hình chỉ
 *     được gọi khi cả hai vòng không đủ câu, đúng một lời gọi mỗi lần phụ đạo.
 *
 * ⚠ Con số "tỷ lệ dùng phương án dự phòng" (Bảng 3.29) từ nay MỚI có nghĩa: trước
 * 09-10 nó luôn bằng 0 vì không có lời gọi nào để mà lùi. `LOI_SINH` ở
 * `lib/goiPhuDao.js` đếm.
 *
 * ── Bản chú thích cũ, để lại nguyên văn ──
 *
 * Bảng 3.23 khai bài phụ đạo là MỘT TRONG BA vị trí được gọi mô hình lúc chạy.
 * Chỗ nối ấy để sẵn ở đây (`goiLLM`), nhưng chưa cắm, và đây là lý do:
 *
 * Ba vị trí kia (phòng luyện nói · chấm bài viết) chỉ cần mô hình sinh MỘT CÂU
 * tiếng Anh hoặc một đoạn nhận xét — hậu kiểm soi được trọn vẹn bằng `soiCau`. Một
 * CÂU HỎI thì khác: nó có phương án nhiễu, có đáp án đúng duy nhất, có gợi ý đi từ
 * xa tới gần, có mã nút đánh giá — bảy luật ở mục 3.5.2. Sinh thiếu một luật là ra
 * một câu hỏi hai đáp án đúng, hoặc một gợi ý lộ luôn đáp án; hậu kiểm theo vốn từ
 * KHÔNG bắt được những lỗi ấy.
 *
 * Nên thứ tự đúng là: nối luồng trước (đang làm ở đây), rồi mới thêm mô hình cùng
 * với tầng hậu kiểm riêng cho bảy luật kia. Trong lúc chờ, kho 4.226 câu tĩnh phủ
 * phần lớn trường hợp — `cauTinhCuaNut` tìm câu quanh nút gốc rễ ở cả ba bậc độ
 * khó, và chỉ khi nó về rỗng thì bé mới không có bài gỡ.
 *
 * ⚠ Khi cắm mô hình vào, phải cập nhật LẠI Bảng 3.23 và mục 3.5.3 của luận văn —
 * và tới lúc ấy con số "tỷ lệ dùng phương án dự phòng" (Bảng 3.29) mới có nghĩa,
 * vì hiện giờ nó luôn bằng 0 do không có lời gọi nào để mà lùi.
 */
