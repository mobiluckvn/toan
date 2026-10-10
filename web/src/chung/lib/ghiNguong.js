/**
 * PHÁT HÀNH MỘT PHIÊN BẢN NGƯỠNG — chỗ DUY NHẤT của máy con ghi vào bảng `nguong`.
 *
 * ── HAI LỆNH GHI, VÀ CHÚNG PHẢI ĐI CÙNG NHAU ──
 * Mỗi ngưỡng đổi sinh ra hai dòng: giá trị mới ở `nguong`, và một dòng
 * `nguong_lich_su` kèm LÝ DO. Ghi được cái trước mà hụt cái sau thì sáu tháng nữa có
 * một con số mà không ai biết vì sao — mà "không biết vì sao" chính là một trong ba
 * hạn chế mà R7 sinh ra để bỏ (mục 3.8).
 *
 * Nên dùng `writeBatch`: cả hai cùng vào hoặc cùng không.
 *
 * ⚠ MÁY CON KHÔNG ĐƯỢC TIN. Luật Firestore mới là chốt thật: chỉ vai trò
 *   `chuyengia` ghi được, và giá trị phải nằm trong `[canDuoi, canTren]`. Phép soi ở
 *   đây (`soiNguong`) là để chuyên gia thấy sai TRƯỚC khi bấm, không phải để thay luật.
 *
 * ⚠ KHÔNG ĐỔI BỘ ĐANG HÀNH. Mục 3.8.4: "Phiên bản mới chỉ có hiệu lực từ phiên tiếp
 *   theo; phiên đang chạy giữ nguyên bộ ngưỡng đã tải." Đổi giữa chừng thì nửa đầu
 *   buổi và nửa sau chấm theo hai luật, mà bản ghi chỉ mang được một `nguongVer`.
 */
import {
  collection, doc, serverTimestamp, writeBatch,
} from 'firebase/firestore';
import { db, hasFirebase, auth } from './nenTang.js';
import { KHOANG, boNguong, soiNguong } from './nguong.js';

/** Mã tài liệu của một ngưỡng ở phạm vi toàn hệ. Đợt sau thêm phạm vi thì thêm hậu tố. */
export const maTaiLieu = (ma, phamVi = null) =>
  (phamVi?.loai && phamVi?.khoa ? `${ma}__${phamVi.loai}__${phamVi.khoa}` : ma);

/**
 * Phát hành. Trả về số phiên bản mới.
 *
 * @param giaTri  bộ giá trị chuyên gia vừa sửa, dạng { NGxx: số | object }
 * @param doi     danh sách mã THỰC SỰ đổi — chỉ ghi ngần ấy dòng, không ghi cả 21
 * @param lyDo    bắt buộc; luật Firestore cũng đòi
 */
export async function phatHanhNguong({ giaTri, doi, lyDo }) {
  if (!hasFirebase || !db) throw new Error('Máy chưa nối được lên mạng.');
  const nguoi = auth?.currentUser?.uid;
  if (!nguoi) throw new Error('Phải đăng nhập bằng tài khoản chuyên gia.');
  const vi = String(lyDo || '').trim();
  if (!vi) throw new Error('Phải ghi lý do — đó là thứ làm bảng lịch sử có giá trị.');
  if (!doi?.length) throw new Error('Chưa có ngưỡng nào đổi.');

  const cu = boNguong();
  const bo = { phienBan: cu.phienBan, macDinh: giaTri, theoPhamVi: cu.theoPhamVi || {} };
  const loi = soiNguong(bo);
  if (loi.length) {
    throw new Error(`Còn ${loi.length} chỗ chưa hợp lệ: ${loi.map((x) => x.ma).join(', ')}`);
  }

  const phienBan = (Number(cu.phienBan) || 0) + 1;
  const lo = writeBatch(db);
  const luc = new Date().toISOString();
  for (const ma of doi) {
    const [canDuoi, canTren] = KHOANG[ma];
    lo.set(doc(db, 'nguong', maTaiLieu(ma)), {
      ma, giaTri: giaTri[ma], canDuoi, canTren,
      phamVi: { loai: 'toanHe' },
      nguon: 'chuyenGia', phienBan, hieuLucTu: luc, serverTs: serverTimestamp(),
    });
    lo.set(doc(collection(db, 'nguong_lich_su')), {
      ma, phamVi: { loai: 'toanHe' },
      giaTriCu: cu.macDinh?.[ma] ?? null,
      giaTriMoi: giaTri[ma],
      phienBan, nguoiSua: nguoi, thoiDiem: luc, lyDo: vi,
      maDeXuat: null, serverTs: serverTimestamp(),
    });
  }
  await lo.commit();
  return phienBan;
}
