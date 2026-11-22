/**
 * ĐỌC TƯƠI VÀ PHÁT HÀNH MỘT PHIÊN BẢN NGƯỠNG — chỗ DUY NHẤT của máy con ghi vào bảng
 * `nguong`.
 *
 * ── MỖI NGƯỠNG ĐỔI LÀ HAI DÒNG, VÀ CHÚNG PHẢI ĐI CÙNG NHAU ──
 * Giá trị mới ở `nguong`, và một dòng `nguong_lich_su` kèm LÝ DO. Ghi được cái trước
 * mà hụt cái sau thì sáu tháng nữa có một con số mà không ai biết vì sao — mà "không
 * biết vì sao" chính là một trong ba hạn chế mà R7 sinh ra để bỏ (mục 3.8).
 *
 * ── SỐ PHIÊN BẢN LẤY TỪ BẢNG, TRONG MỘT GIAO DỊCH (Bảng 4.7, điểm 3) ──
 * Trước 22-11 số phiên bản mới = phiên bản của BỘ ĐÃ NẠP lúc mở app + 1, và giá trị
 * cũ ghi vào lịch sử cũng lấy từ bộ ấy. Hai chuyên gia mở màn cùng buổi sáng là hai
 * lần phát hành cùng mang số 5; một chuyên gia để màn mở từ hôm qua là lịch sử ghi
 * "giá trị cũ" là con số của hôm qua chứ không phải con số đang chạy.
 *
 * Nay:
 *   · mở màn và lúc bấm phát hành đều ĐỌC TƯƠI bảng `nguong` (`docBangNguong`);
 *   · số mới = max(bộ đếm, phiên bản cao nhất trong bảng) + 1, tính TRONG một giao
 *     dịch Firestore có đọc tài liệu đếm `nguong_phien_ban/hienHanh`. Hai lần phát
 *     hành chạy song song thì giao dịch sau thấy bộ đếm đã đổi, chạy lại, và lấy số
 *     kế tiếp — không bao giờ trùng. Luật Firestore canh thêm một lớp: bộ đếm chỉ
 *     được tăng đúng 1, và mọi dòng `nguong`/`nguong_lich_su` phải mang đúng số ấy;
 *   · giá trị cũ đọc TRONG giao dịch từ chính tài liệu sắp bị ghi đè. Phạm vi hẹp
 *     chưa từng khai thì "giá trị cũ" là giá trị THỪA HƯỞNG từ bảng (ghi kèm
 *     `nguonCu: 'thuaHuong'` để người đọc lịch sử không tưởng đã có một dòng trước).
 *
 * ⚠ MÁY CON KHÔNG ĐƯỢC TIN. Luật Firestore mới là chốt thật: chỉ vai trò `chuyengia`
 *   ghi được, giá trị phải nằm trong `[canDuoi, canTren]`. Phép soi ở đây là để
 *   chuyên gia thấy sai TRƯỚC khi bấm, và để ràng buộc GIỮA các ngưỡng (luật không so
 *   được) có một chỗ canh.
 *
 * ⚠ KHÔNG ĐỔI BỘ ĐANG HÀNH. Mục 3.8.4: "Phiên bản mới chỉ có hiệu lực từ phiên tiếp
 *   theo; phiên đang chạy giữ nguyên bộ ngưỡng đã tải."
 */
import {
  KHOANG, PHIEN_BAN, boTuBang, chuanHoaBo, apDungThayDoi, soiPhamVi,
  layNguongThuan, nguCanhCuaPhamVi,
} from './nguong.js';
import { phamViHopLe } from './phamViNguong.js';

/** Tài liệu đếm phiên bản. Một tài liệu, một trường `so`. */
export const DEM_PHIEN_BAN = 'nguong_phien_ban/hienHanh';

/** Mã tài liệu của một ngưỡng: `NG07` ở toàn hệ, `NG07__khoiLop__3` ở phạm vi hẹp. */
export const maTaiLieu = (ma, phamVi = null) => {
  const nc = nguCanhCuaPhamVi(phamVi);
  const [loai] = Object.keys(nc);
  return loai ? `${ma}__${loai}__${nc[loai]}` : ma;
};

/** Phiên bản cao nhất đang có trong các dòng của bảng. */
export const phienBanCaoNhat = (dong) => (dong || []).reduce(
  (m, x) => (Number.isFinite(x?.phienBan) ? Math.max(m, x.phienBan) : m), PHIEN_BAN);

/**
 * NỀN THẬT — Firestore. Tách ra để cổng tiêm một kho giả có giao dịch thật (đọc
 * trước, ghi sau, xung đột thì chạy lại), thay vì chỉ đọc mã bằng regex.
 *
 * ⚠ IMPORT ĐỘNG, cùng lẽ với `napNguong.js`: tệp phải nạp được bằng `node`.
 */
async function nenThat() {
  const nt = await import('./nenTang.js');
  if (!nt.hasFirebase || !nt.db) throw new Error('Máy chưa nối được lên mạng.');
  const fs = await import('firebase/firestore');
  const { db } = nt;
  const ref = (duong) => fs.doc(db, duong);
  return {
    nguoi: nt.auth?.currentUser?.uid || null,
    docBang: async () => (await fs.getDocs(fs.collection(db, 'nguong'))).docs.map((d) => d.data()),
    moiLichSu: () => `nguong_lich_su/${fs.doc(fs.collection(db, 'nguong_lich_su')).id}`,
    dauGio: () => fs.serverTimestamp(),
    giaoDich: (viec) => fs.runTransaction(db, (tx) => viec({
      get: async (duong) => {
        const s = await tx.get(ref(duong));
        return { exists: s.exists(), data: () => s.data() };
      },
      set: (duong, du) => { tx.set(ref(duong), du); },
    })),
  };
}

/**
 * ĐỌC TƯƠI bảng `nguong` → `{ bo, dong }`. `bo` đã chuẩn hoá (đủ 30 mã), nhưng KHÔNG
 * đặt làm bộ của phiên. Bảng rỗng → bộ mặc định với phiên bản `PHIEN_BAN`.
 */
export async function docBangNguong(nen = null) {
  const n = nen || await nenThat();
  const dong = await n.docBang();
  return { dong, bo: chuanHoaBo(boTuBang(dong)) };
}

/**
 * Phát hành. Trả về số phiên bản mới.
 *
 * @param giaTri  bộ giá trị HIỆU LỰC của phạm vi đang sửa, dạng { NGxx: số | object }
 * @param doi     danh sách mã THỰC SỰ đổi — chỉ ghi ngần ấy dòng
 * @param lyDo    bắt buộc; luật Firestore cũng đòi
 * @param phamVi  `{ loai, khoa }`; bỏ trống = toàn hệ
 * @param nen     chỉ cổng truyền; chỗ gọi thật để trống
 */
export async function phatHanhNguong({ giaTri, doi, lyDo, phamVi = null }, nen = null) {
  const vi = String(lyDo || '').trim();
  if (!vi) throw new Error('Phải ghi lý do — đó là thứ làm bảng lịch sử có giá trị.');
  if (!doi?.length) throw new Error('Chưa có ngưỡng nào đổi.');
  const saiPv = phamViHopLe(phamVi);
  if (saiPv) throw new Error(`Phạm vi chưa hợp lệ: ${saiPv}.`);
  for (const ma of doi) if (!KHOANG[ma]) throw new Error(`Không có ngưỡng ${ma}.`);

  const n = nen || await nenThat();
  if (!n.nguoi) throw new Error('Phải đăng nhập bằng tài khoản chuyên gia.');

  /* ĐỌC TƯƠI ngay lúc bấm — không tin bộ màn hình đã đọc lúc mở. Rồi soi bộ ỨNG VIÊN
     ở đúng phạm vi sắp ghi, kèm mọi chỗ nó giao với phạm vi khác đã khai. */
  const dong = await n.docBang();
  const boBang = chuanHoaBo(boTuBang(dong));
  const ungVien = apDungThayDoi(boBang, phamVi, giaTri, doi);
  const loi = soiPhamVi(ungVien, phamVi);
  if (loi.length) {
    throw new Error(`Còn ${loi.length} chỗ chưa hợp lệ: ${[...new Set(loi.map((x) => x.ma))].join(', ')}`);
  }

  const nc = nguCanhCuaPhamVi(phamVi);
  const [loai] = Object.keys(nc);
  const pv = loai ? { loai, khoa: nc[loai] } : { loai: 'toanHe' };
  const caoNhatBang = phienBanCaoNhat(dong);

  /* ── HAI LỚP CHỐNG TRÙNG SỐ, VÀ VÌ SAO PHẢI TỰ CHẠY LẠI ──
     Giao dịch của Firestore tự chạy lại khi tài liệu đã đọc bị đổi trước lúc cam kết.
     Nhưng LUẬT được xét TRƯỚC phép so ấy: giao dịch đến sau ghi `so = 9` lên một bộ
     đếm đã là 9, luật thấy "không tăng đúng một" và trả `permission-denied` — không
     phải lỗi xung đột, nên SDK không chạy lại (đo thật trên bộ giả lập 22-11). Luật
     làm đúng việc của nó: số không bao giờ trùng. Còn việc lấy số KẾ TIẾP thì ở đây:
     bị từ chối mà bộ đếm ĐÃ ĐỔI so với lần đọc trước → có người vừa phát hành, chạy
     lại; bộ đếm KHÔNG đổi → từ chối thật (sai vai trò, sai khoảng), ném ngay. */
  let soDaDoc = null;
  let soLanTruoc = null;
  for (let lan = 0; ; lan += 1) {
    try {
      return await n.giaoDich(viecGiaoDich);
    } catch (e) {
      const xungDot = /permission-denied|aborted|failed-precondition/.test(String(e?.code || ''));
      if (!xungDot || lan >= 4 || soDaDoc === soLanTruoc) throw e;
      soLanTruoc = soDaDoc;
    }
  }

  async function viecGiaoDich(tx) {
    /* ⚠ ĐỌC HẾT RỒI MỚI GHI — giao dịch Firestore đòi thế. */
    const dem = await tx.get(DEM_PHIEN_BAN);
    const soCu = dem.exists ? (Number(dem.data()?.so) || 0) : 0;
    soDaDoc = soCu;
    const phienBan = Math.max(soCu, caoNhatBang) + 1;
    const cu = {};
    for (const ma of doi) {
      const d = await tx.get(`nguong/${maTaiLieu(ma, phamVi)}`);
      cu[ma] = d.exists
        ? { giaTri: d.data()?.giaTri ?? null, nguon: 'bang' }
        : { giaTri: layNguongThuan(boBang, ma, nc), nguon: 'thuaHuong' };
    }

    const luc = new Date().toISOString();
    /* Bộ đếm trước: luật đọc `getAfter` của nó để soi số phiên bản trên mọi dòng. */
    tx.set(DEM_PHIEN_BAN, { so: phienBan, nguoiSua: n.nguoi, thoiDiem: luc });
    for (const ma of doi) {
      const [canDuoi, canTren] = KHOANG[ma];
      tx.set(`nguong/${maTaiLieu(ma, phamVi)}`, {
        ma, giaTri: giaTri[ma], canDuoi, canTren,
        phamVi: pv,
        nguon: 'chuyenGia', phienBan, hieuLucTu: luc, serverTs: n.dauGio(),
      });
      tx.set(n.moiLichSu(), {
        ma, phamVi: pv,
        giaTriCu: cu[ma].giaTri, nguonCu: cu[ma].nguon,
        giaTriMoi: giaTri[ma],
        phienBan, nguoiSua: n.nguoi, thoiDiem: luc, lyDo: vi,
        maDeXuat: null, serverTs: n.dauGio(),
      });
    }
    return phienBan;
  }
}
