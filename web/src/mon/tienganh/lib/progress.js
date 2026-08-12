/**
 * SỔ TIẾN ĐỘ TIẾNG ANH — lưu tại máy.
 *
 * Khoá RIÊNG, không dùng chung với Toán. Hai môn chung một khoá thì `micros` lẫn
 * vào nhau: mã bài `DL:TA1.B04` và `DL:KSN2.B04` khác nhau nên chưa trùng ngay,
 * nhưng mọi phép đếm "xong bao nhiêu bài" đều phải lọc theo tiền tố — và chỗ nào
 * quên lọc thì con số sai mà không ai biết. Tách khoá thì không có gì để quên.
 *
 * Và PHẢI TÁCH THEO CHỖ như bên Toán: máy tính bảng dùng chung cả nhà, mỗi bé một
 * "chỗ". Không tách thì em vừa đăng nhập đã thấy bài của anh.
 */
import { choDangDung, CHO_DAU } from '../../../chung/lib/nguoiDung.js';

const KEY_GOC = 'ttd5.tienganh.v1';
const khoa = () => {
  const cho = choDangDung();
  return cho === CHO_DAU ? KEY_GOC : `${KEY_GOC}.${cho}`;
};

export const soRong = () => ({ micros: {}, chapters: {}, updatedAt: null });

export function napTienDo(kho = globalThis.localStorage) {
  try {
    const raw = kho?.getItem(khoa());
    return raw ? { ...soRong(), ...JSON.parse(raw) } : soRong();
  } catch { return soRong(); }
}

export function luuTienDo(p, kho = globalThis.localStorage) {
  try { kho?.setItem(khoa(), JSON.stringify({ ...p, updatedAt: new Date().toISOString() })); }
  catch { /* chế độ riêng tư — bỏ qua, học vẫn chạy */ }
  return p;
}

/**
 * Ghi kết quả một bài.
 *
 * `best` giữ số câu đúng CAO NHẤT từ trước tới nay, không phải lần gần nhất: bé làm
 * lại bài đã đạt mà hôm ấy mệt, làm kém hơn, thì không được tụt sao đã có.
 */
export function ghiBai(p, id, kq) {
  const cu = p.micros[id] || {};
  return {
    ...p,
    micros: {
      ...p.micros,
      [id]: {
        done: true,
        pass: !!kq.pass || !!cu.pass,
        best: Math.max(cu.best || 0, kq.dung || 0),
        total: kq.tong || 0,
        /* Bậc cao nhất bé đã qua trong bài này — cái này mới là thứ đáng khoe với
           bố mẹ. "Xong bài" thì bé nào cũng xong; "gõ lại được cả câu" thì không. */
        bac: Math.max(cu.bac || 0, kq.bac || 0),
        attempts: (cu.attempts || 0) + 1,
        at: new Date().toISOString(),
      },
    },
  };
}

/** Khoá chương PHẢI kèm mã quyển — khoá số trần làm huy hiệu lây giữa các quyển. */
export const khoaChuong = (ma, chuong) => `${ma}:C${chuong}`;

export function ghiChuong(p, ma, chuong, kq) {
  const k = khoaChuong(ma, chuong);
  const cu = p.chapters[k] || {};
  return {
    ...p,
    chapters: {
      ...p.chapters,
      [k]: {
        dat: !!kq.dat || !!cu.dat,
        best: Math.max(cu.best || 0, kq.dung || 0),
        tong: kq.tong || 0,
        at: new Date().toISOString(),
      },
    },
  };
}

/** Gộp sổ tại máy với sổ trên máy chủ — bản nào MỚI HƠN thì thắng, từng bài một. */
export function gopTienDo(a, b) {
  if (!b) return a;
  const micros = { ...a.micros };
  for (const [k, v] of Object.entries(b.micros || {})) {
    const cu = micros[k];
    if (!cu || String(v.at || '') > String(cu.at || '')) micros[k] = v;
    else micros[k] = { ...v, ...cu, best: Math.max(cu.best || 0, v.best || 0),
                       bac: Math.max(cu.bac || 0, v.bac || 0) };
  }
  const chapters = { ...a.chapters };
  for (const [k, v] of Object.entries(b.chapters || {})) {
    const cu = chapters[k];
    if (!cu || String(v.at || '') > String(cu.at || '')) chapters[k] = v;
  }
  return { ...a, micros, chapters };
}
