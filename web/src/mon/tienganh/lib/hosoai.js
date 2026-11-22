/**
 * TRÍ NHỚ CỦA CÔ GIÁO MÁY VỀ MỘT BÉ — giữ qua nhiều buổi.
 *
 * ── VÌ SAO CẦN ──
 * Trước bản này cô giáo máy không có trí nhớ nào giữa hai buổi. Bé hôm qua sót
 * chữ "a" ba lần thì hôm nay cô vẫn hỏi như chưa gặp bao giờ, và cái bé thích thì
 * chỉ còn đúng MỘT chữ (`hoSo.thich`) sống sót sang buổi sau. Một cô giáo thật thì
 * mở sổ ra là nhớ.
 *
 * ── BỐN LUẬT, VÀ CẢ BỐN ĐỀU LÀ GIỚI HẠN ──
 * Đây là trí nhớ về MỘT ĐỨA TRẺ, nên nó phải nhỏ, phải quên, và phải xoá được.
 *
 *  1. CHỈ DỮ LIỆU HỌC. Không một chữ nào bé tự nói ra được lưu ở đây. `cauDungGanNhat`
 *     giữ CÂU ĐÍCH của sách (`luotBe.mau`) chứ không giữ `luotBe.chu` — hai thứ ấy
 *     khác nhau hẳn: một cái là câu bài dạy, một cái là tiếng bé vừa phát ra.
 *  2. KHÔNG NHẬN XÉT VỀ BÉ. Không "bé lười", không "bé hay quên", không điểm, không
 *     phần trăm. Giữ đúng quy ước của `dongHoSo`: câu nào ở đây cũng phải là câu
 *     KHÔNG SAO nếu lỡ bị đọc to lên trước mặt bé.
 *  3. MỌI MỤC CÓ HẠN hoặc có điều kiện tự xoá. Bài học hết `HAN_BUOI` buổi thì đi;
 *     lỗi lặp ở một nút bé đã thạo thì đi. Trí nhớ không có hạn là một cái hồ sơ.
 *  4. TRẦN CỨNG `TRAN_KY_TU`. Nó đi vào lời dặn mỗi lượt, nên phình ra là vừa tốn
 *     chỗ của lịch sử nói chuyện vừa làm mô hình loãng.
 *
 * Và bố mẹ xoá được sạch bất cứ lúc nào — `xoaHoSoAI`.
 *
 * ⚠ KHÔNG GỌI MÔ HÌNH Ở ĐÂY. Mọi thứ trong tệp này suy từ con số `chamCau` đã
 * tính, nên chạy được bằng `node` và cổng soi được. Phần bài học do mô hình viết
 * (Reflexion) đi vào bằng `themBaiHoc`, và nó phải qua phép soi của chính việc ấy.
 */
import { nguongThao, mucThaoCua } from './zpd.js';

/** Trần ký tự cả hồ sơ. Đi vào lời dặn mỗi lượt, nên phải nhỏ. */
export const TRAN_KY_TU = 1200;

/** Bài học sống được bao nhiêu buổi rồi tự đi. */
export const HAN_BUOI = 5;

/**
 * Trần SỐ PHẦN TỬ từng mảng. Khai một chỗ để cổng đếm được, và để `donHoSo` không
 * phải nhớ sáu con số rải rác.
 */
export const TRAN_PHAN_TU = {
  soThich: 5, nguoiVat: 5, loiLap: 5, tuNham: 5, cauDungGanNhat: 3, baiHoc: 5,
};

/** Lỗi phải LẶP mấy lần trong một buổi mới đáng nhớ. Một lần là chuyện tình cờ. */
export const LAP_DE_NHO = 2;

/**
 * Hình dạng CỐ ĐỊNH. Mọi trường đều có, kể cả khi rỗng — thiếu trường thì chỗ đọc
 * phải đoán, và đoán thì mỗi chỗ đoán một kiểu.
 */
export const hoSoRong = () => ({
  soThich: [],
  /* Người và vật bé kể về mình. CỐ Ý ĐỂ RỖNG ở bản này: rút nó ra đòi đọc hiểu lời
     bé nói, tức phải gọi mô hình, mà việc ấy là của Reflexion (`themBaiHoc`) và
     phải qua phép soi của nó. Giữ trường để hình dạng khỏi đổi lần nữa. */
  nguoiVat: [],
  loiLap: [],
  tuNham: [],
  cauDungGanNhat: [],
  baiHoc: [],
  buoiThu: 0,
  capNhatLuc: 0,
});

const gon = (ds) => [...new Set(ds.filter(Boolean))];
const catMang = (ds, n) => gon(ds).slice(-n);

/**
 * CẬP NHẬT HỒ SƠ TỪ MỘT BUỔI — thuần code, từ chính con số `chamCau` đã tính.
 *
 * @param lichSu  cả buổi nói chuyện, đúng hình dạng `PhongNoi.jsx` giữ
 * @param hoSo    hồ sơ cũ (`hoSo.thich` — thứ bé đã chọn)
 * @param bayGio  mốc thời gian, tiêm vào để cổng chạy tiền định
 */
export function capNhatTuBuoi(hs, { lichSu = [], hoSo = null, bayGio = Date.now() } = {}) {
  const cu = { ...hoSoRong(), ...(hs || {}) };
  const be = lichSu.filter((x) => x?.vai === 'be' && x.diem != null);

  /* ── LỖI LẶP ── Chữ CHỨC NĂNG bé bỏ sót từ `LAP_DE_NHO` lần trở lên trong buổi.
     Một lần sót là chuyện tình cờ (nói nhanh, máy nghe không rõ); lặp lại mới là
     chỗ bé chưa nắm. Và chỉ chữ chức năng (`a` · `is` · `the`): chữ có nghĩa thì
     đã có cả một tầng BKT đo riêng, nhắc thêm ở đây là nhắc hai lần. */
  const dem = new Map();
  for (const l of be) {
    for (const c of gon(l.thieuChucNang || [])) dem.set(c, (dem.get(c) || 0) + 1);
  }
  const lapMoi = [...dem.entries()].filter(([, n]) => n >= LAP_DE_NHO).map(([c]) => c);

  /* ── CHỮ BÉ NHẦM SANG CHỮ KHÁC CỦA BÀI ── `chamnoi.chamTu` tính sẵn `nhamThanh`.
     ⚠ Đường này hiện chưa có nguồn trên bản chạy: phòng nói chấm bằng `chamCau`, mà
     chỉ `chamTu` tính `nhamThanh` (xem ghi chú ở `nhanluot.js`). Vẫn đọc, để ngày
     nối nguồn thì không phải sửa thêm chỗ nào. */
  const nhamMoi = be.map((l) => l.nhamThanh).filter(Boolean);

  /* ── CÂU BÉ ĐÃ NÓI ĐƯỢC ── Lấy CÂU ĐÍCH của sách (`mau`), KHÔNG lấy `chu`.
     `chu` là tiếng bé vừa phát ra, và luật 1 ở đầu tệp cấm lưu nó. `mau` thì là
     câu của chính bài học, lưu nó không lộ gì về bé ngoài việc bé nói được. */
  const dungMoi = be.filter((l) => l.diem >= 6).map((l) => l.mau).filter(Boolean);

  return {
    ...cu,
    soThich: catMang([...cu.soThich, hoSo?.thich], TRAN_PHAN_TU.soThich),
    loiLap: catMang([...cu.loiLap, ...lapMoi], TRAN_PHAN_TU.loiLap),
    tuNham: catMang([...cu.tuNham, ...nhamMoi], TRAN_PHAN_TU.tuNham),
    /* Câu MỚI đứng cuối, và `catMang` cắt từ đuôi — nên buổi sau đẩy buổi trước ra.
       Giữ câu cũ nhất thì sang buổi thứ năm cô vẫn khen một câu bé đã quên. */
    cauDungGanNhat: catMang([...cu.cauDungGanNhat, ...dungMoi], TRAN_PHAN_TU.cauDungGanNhat),
    buoiThu: (cu.buoiThu || 0) + 1,
    capNhatLuc: bayGio,
  };
}

/** Trần ký tự MỘT bài học. Dài hơn thế thì nó không còn là một lời nhắc. */
export const BAI_HOC_TOI_DA_CHU = 160;

/**
 * Thêm một bài học cuối buổi (mẫu Reflexion).
 *
 * ⚠ Hàm này KHÔNG soi nội dung — phép soi (`soiBaiHoc`: chặn từ cấm về tính cách,
 * chặn chữ Anh ngoài vốn, chặn số) là của chính việc sinh ra bài học, vì chỉ ở đấy
 * mới biết vốn từ của buổi. Ở đây chỉ chặn hình dạng: cắt ngắn, và gắn HẠN.
 */
export function themBaiHoc(hs, { chu, nut = null, buoi = 0 } = {}) {
  const cu = { ...hoSoRong(), ...(hs || {}) };
  const s = String(chu || '').replace(/\s+/g, ' ').trim();
  if (!s) return cu;
  const moi = {
    chu: s.length > BAI_HOC_TOI_DA_CHU ? `${s.slice(0, BAI_HOC_TOI_DA_CHU - 3)}...` : s,
    nut,
    /* Hạn tính theo SỐ BUỔI, không theo ngày: bé học thưa thì một bài học vẫn còn
       đúng sau hai tuần, còn bé học dồn thì năm buổi là nó cũ thật. */
    hetHanBuoi: (buoi || cu.buoiThu || 0) + HAN_BUOI,
  };
  return { ...cu, baiHoc: [...cu.baiHoc.filter((x) => x.chu !== moi.chu), moi]
    .slice(-TRAN_PHAN_TU.baiHoc) };
}

/**
 * DỌN HỒ SƠ — phần làm cho trí nhớ này KHÁC một cái hồ sơ.
 *
 * Ba phép dọn, và cả ba đều tự chạy:
 *   · bài học hết hạn thì đi;
 *   · lỗi lặp / chữ nhầm ở nút bé ĐÃ THẠO thì đi — nhắc lại chỗ bé đã qua là vừa
 *     tốn chỗ vừa nói sai về bé;
 *   · cắt về `TRAN_KY_TU`, bỏ từ mục CŨ nhất.
 */
export function donHoSo(hs, { mucThao = null, buoiHienTai = 0 } = {}) {
  let ra = { ...hoSoRong(), ...(hs || {}) };
  const nay = buoiHienTai || ra.buoiThu || 0;

  ra.baiHoc = ra.baiHoc.filter((x) => (x?.hetHanBuoi ?? 0) > nay)
    .slice(-TRAN_PHAN_TU.baiHoc);

  const daThao = (nut) => nut && (mucThaoCua(mucThao, nut) ?? 0) >= nguongThao({ nut });
  ra.baiHoc = ra.baiHoc.filter((x) => !daThao(x?.nut));
  /* `loiLap` và `tuNham` là chuỗi chữ trần, không mang nút. Khi chỗ gọi biết nút
     thì nó truyền dạng `{chu, nut}` — nhận cả hai hình dạng, vì bản đầu chỉ có
     chuỗi và sổ của bé đang chạy thì không được vỡ. */
  const bo = (ds) => ds.filter((x) => !(x && typeof x === 'object' && daThao(x.nut)));
  ra.loiLap = bo(ra.loiLap);
  ra.tuNham = bo(ra.tuNham);

  for (const [k, n] of Object.entries(TRAN_PHAN_TU)) ra[k] = (ra[k] || []).slice(-n);

  /* ── CẮT VỀ TRẦN KÝ TỰ ── Bỏ từ mục CŨ nhất của mảng DÀI nhất, lặp tới khi vừa.
     Cắt đều mọi mảng thì mất cả những mục chỉ có một cái; cắt mảng dài nhất thì
     thứ bị mất luôn là thứ đang chiếm chỗ nhiều nhất. */
  const CO = ['cauDungGanNhat', 'baiHoc', 'soThich', 'nguoiVat', 'loiLap', 'tuNham'];
  for (let i = 0; i < 40 && JSON.stringify(ra).length > TRAN_KY_TU; i += 1) {
    const dai = CO.map((k) => [k, JSON.stringify(ra[k] || []).length])
      .sort((a, b) => b[1] - a[1])[0];
    if (!dai || !(ra[dai[0]] || []).length) break;
    ra = { ...ra, [dai[0]]: ra[dai[0]].slice(1) };
  }
  return ra;
}

/** Bố mẹ bấm xoá thì hồ sơ về RỖNG HẲN, không phải "ẩn đi". */
export const xoaHoSoAI = () => hoSoRong();

const chuCua = (x) => (typeof x === 'string' ? x : x?.chu || '');

/**
 * KHỐI LỜI DẶN — tiếng Anh, ≤ 8 dòng, KHÔNG một chữ số nào.
 *
 * Ba quy ước, cả ba đều là quy ước của `dongHoSo` và không được phá:
 *   · không số, không phần trăm, không điểm;
 *   · câu nào cũng phải KHÔNG SAO nếu lỡ bị đọc to trước mặt bé;
 *   · nói bằng câu người đọc được, đừng đổ dữ liệu thô vào.
 */
export function dongHoSoAI(hs, tenBe = '') {
  const h = { ...hoSoRong(), ...(hs || {}) };
  if ((h.buoiThu || 0) < 1) return '';
  const d = [];
  const ten = tenBe || 'she';

  if (h.soThich.length) {
    d.push(`${ten} has told you she likes: ${h.soThich.join(', ')}.`
      + ' Use those words when a pattern needs a thing.');
  }
  if (h.cauDungGanNhat.length) {
    d.push(`She has already said these sentences well: ${h.cauDungGanNhat.map((x) => `"${x}"`).join(' ')}.`
      + ' You may build on them; do not drill them again from scratch.');
  }
  if (h.loiLap.length) {
    d.push(`She keeps leaving out these small words: ${h.loiLap.map(chuCua).join(', ')}.`
      + ' When one of them belongs in the sentence, make it the thing you point at.');
  }
  if (h.tuNham.length) {
    d.push(`She mixes up these words: ${h.tuNham.map(chuCua).join(', ')}.`
      + ' Say their meanings apart before asking for either.');
  }
  for (const b of h.baiHoc) {
    const s = chuCua(b);
    if (s) d.push(`Note from an earlier session: ${s}`);
  }
  if (!d.length) return '';

  /* ⚠ CẮT CHỮ SỐ Ở ĐÚNG MỘT CHỖ — ngay trước khi ra khỏi hàm. Lọc ở từng dòng thì
     thêm một dòng mới mà quên lọc là con số lọt vào lời dặn, và mô hình rất dễ nhại
     nguyên văn. Bài học do mô hình viết (`themBaiHoc`) là đường dễ lọt nhất. */
  const khongSo = (s) => s.replace(/\d+([.,]\d+)?%?/g, 'some');
  /* Trần 8 dòng: giữ mấy dòng ĐẦU, vì chúng xếp từ thứ chắc nhất (sở thích, câu đã
     nói được) tới thứ do mô hình viết. */
  return ['ABOUT THIS CHILD (from earlier sessions):',
    ...d.slice(0, 7)].map(khongSo).join('\n');
}
