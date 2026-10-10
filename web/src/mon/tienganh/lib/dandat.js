import { layNguong, BO_MAC_DINH } from '../../../chung/lib/nguong.js';
/**
 * DẪN DẮT — luật "đi lần lượt", để riêng khỏi giao diện.
 *
 * ── VÌ SAO CÓ TỆP NÀY ──
 * Quyển này mở ra là thấy cả 16 bài, bài nào bấm cũng vào. Bé 6 tuổi bấm bài 16
 * trước bài 1 không phải vì nghịch — nó chưa đọc được tên bài, thấy ô nào cũng
 * như nhau. Mà 16 unit này dựng chồng lên nhau: chưa có `a`/`the` của unit 1 thì
 * unit 16 chỉ là những chữ lạ. Bỏ qua bài không phải đi nhanh, là đi hụt.
 *
 * Toán lớp 5 đã có cờ `khoaBai` và luật "bài trước ĐẠT thì bài sau mở". Môn này
 * đi theo, nhưng KHÔNG import sang `mon/toan/` — hai môn không được với vào ruột
 * nhau (cổng `ranh_gioi` gác). Chép luật thì rẻ hơn là mở một lối đi giữa hai môn
 * mà sau này không ai dám đóng lại.
 *
 * ── MỘT LUẬT DUY NHẤT, DÙNG CHO CẢ BA TẦNG ──
 *
 *     ĐI TIẾP ĐƯỢC KHI: đã ĐẠT — hoặc đã THỬ THẬT ít nhất 2 lần.
 *
 * Vế sau mới là vế quan trọng. Khoá cứng theo "phải đạt" thì bé nào tắc ở unit 7
 * là tắc vĩnh viễn: không qua được thì không có bài nào khác để học, và cái bé
 * học được ở lớp 1 không phải tiếng Anh mà là "mình học dốt". Cho qua ngay lần
 * đầu thì lại thành không khoá gì cả.
 *
 * Hai lần là chỗ đứng giữa: đủ để chắc bé đã THỬ chứ không phải bấm cho xong, mà
 * không đủ để thành hình phạt. Và bài đi vòng ấy KHÔNG được ghi là đạt — nó nằm
 * lại trong danh sách "còn nợ", có nhãn riêng, bấm vào làm lại lúc nào cũng được.
 *
 * Con số này dùng lại nguyên vẹn ở ba chỗ: mở bài sau · mở chặng sau · bỏ qua một
 * câu. Ba chỗ cùng một luật thì bé học được luật ấy một lần rồi áp dụng ở mọi
 * chỗ, thay vì mỗi màn một kiểu.
 */
import { NHAN_TRANG_THAI_BAI } from '../../../chung/lib/nhanHocBa.js';

export { NHAN_TRANG_THAI_BAI as NHAN_TRANG_THAI };

/** Số lần THỬ THẬT tối thiểu trước khi được đi vòng qua. Xem đầu tệp. */
export const THU_TOI_THIEU = layNguong(BO_MAC_DINH, 'NG14');

/** Đã thử đủ số lần để được đi tiếp dù chưa đạt chưa? */
export const daThuDu = (m) => (m?.attempts || 0) >= THU_TOI_THIEU;

/* ═══════════ TẦNG 1 · MỘT BÀI TRONG QUYỂN ═══════════ */

/**
 * Bài này đã mở chưa?
 *
 * `ds` là danh sách mã bài THEO ĐÚNG THỨ TỰ HỌC (`ct.bai`). Truyền danh sách rỗng
 * thì mọi bài đều đóng — chủ ý: thà không vào được bài nào và thấy ngay là hỏng,
 * còn hơn mở toang cả quyển vì nạp chỉ mục lỗi.
 */
export function moBai(tienDo, id, ds = []) {
  const i = ds.indexOf(id);
  if (i < 0) return false;
  if (i === 0) return true;                      // bài đầu luôn mở
  const truoc = tienDo?.micros?.[ds[i - 1]];
  return !!truoc?.pass || daThuDu(truoc);
}

/**
 * Trạng thái hiện lên màn của một bài. Dùng ĐÚNG năm tên mà `chung/nhanHocBa.js`
 * đã đặt, để sổ bố mẹ và bảng cô giáo in ra cùng một thứ tiếng với màn học.
 *
 *   dat     đã qua sát hạch
 *   dangDo  đang học dở, còn chặng đánh dấu
 *   chuaDat đã làm hết mà chưa đủ điểm  → đây là chỗ bé cần quay lại
 *   mo      học được ngay
 *   khoa    chưa tới lượt
 */
export function trangThaiBai(tienDo, id, ds = [], { khoaBai = true } = {}) {
  const m = tienDo?.micros?.[id];
  if (m?.pass) return 'dat';
  if (m?.done) return 'chuaDat';
  if (m?.chang > 0) return 'dangDo';
  if (khoaBai && !moBai(tienDo, id, ds)) return 'khoa';
  return 'mo';
}

/**
 * Bài bé NÊN học tiếp — thứ mà trang chính chỉ mũi tên vào.
 *
 * Thứ tự ưu tiên, và thứ tự này có lý do:
 *   1. bài đang học DỞ   → về đúng chỗ cũ, không bắt làm lại từ đầu
 *   2. bài đầu tiên CHƯA ĐẠT mà đã mở  → gồm cả bài đi vòng còn nợ
 *   3. hết  → quyển đã xong
 *
 * Điểm 2 gộp "chưa từng học" với "học rồi mà chưa qua" vào một chỗ, và đó là chủ
 * ý: với bé thì cả hai đều là "bài mình chưa làm được", không cần phân biệt.
 */
export function baiNenHoc(tienDo, ds = [], opt = {}) {
  const tt = (id) => trangThaiBai(tienDo, id, ds, opt);
  return ds.find((id) => tt(id) === 'dangDo')
      ?? ds.find((id) => tt(id) === 'chuaDat' || tt(id) === 'mo')
      ?? null;
}

/** Bài đã mở mà chưa đạt — danh sách "còn nợ" hiện cho bé và bố mẹ. */
export const baiConNo = (tienDo, ds = [], opt = {}) =>
  ds.filter((id) => ['chuaDat', 'dangDo'].includes(trangThaiBai(tienDo, id, ds, opt)));

/* ═══════════ TẦNG 2 · CÁC CHẶNG TRONG MỘT BÀI ═══════════ */

/**
 * Chuỗi chặng của một bài. Bài nào có kịch bản hội thoại thì có thêm chặng NÓI
 * CHUYỆN; hỏi chính dữ liệu bài chứ không đếm số cứng, vì không phải bài nào cũng
 * có, và cắm số 5 vào đây là lúc thêm bài không có hội thoại thì lệch hết.
 */
export const NHAN_CHANG = {
  tu: 'Từ mới', cau: 'Mẫu câu', luyen: 'Luyện tập',
  noi: 'Nói chuyện', sat: 'Sát hạch', phong: 'Phòng luyện nói',
};

/**
 * PHÒNG LUYỆN NÓI đứng CUỐI và KHÔNG khoá.
 *
 * Nó không phải cửa ải phải qua — nó là chỗ bé quay lại tập nói bao nhiêu lần cũng
 * được, và vốn từ tự rộng ra khi bé đạt unit. Bắt bé qua sát hạch mới được vào thì
 * đúng những bé cần tập nói nhất lại là những bé không vào được.
 */
export const CHANG_KHONG_KHOA = new Set(['phong']);

export function changCua(bai) {
  const coNoi = !!bai?.knowledgeCore?.hoiThoai?.luot?.length;
  return ['tu', 'cau', 'luyen', ...(coNoi ? ['noi'] : []), 'sat', 'phong'];
}

/**
 * Trạng thái một chặng trên thanh điều hướng.
 *
 *   xong  đã làm qua  → bấm vào LÀM LẠI được, và làm lại không mất chặng sau
 *   dang  đang ở đây
 *   khoa  chưa tới
 *
 * Chỗ này từng sai theo kiểu khó thấy: bản cũ chỉ giữ MỘT con số `tai`, và nút
 * trên thanh khoá theo `i > tai`. Nghĩa là bé đang ở chặng 4, quay lại chặng 1
 * nghe lại từ mới, thì chặng 2·3·4 khoá lại hết — muốn về chỗ cũ phải làm lại cả
 * bài. Quay lại ôn là việc TỐT, mà app lại phạt. Nên phải có HAI con số: đang
 * đứng ở đâu (`tai`), và đã đi xa nhất tới đâu (`xa`).
 */
export function trangThaiChang(i, tai, xa, ds = []) {
  if (i === tai) return 'dang';
  if (i <= xa) return 'xong';
  /* Chặng khai KHÔNG KHOÁ thì mở sẵn, dù bé chưa đi tới. Không phải cửa ải. */
  return CHANG_KHONG_KHOA.has(ds[i]) ? 'mo' : 'khoa';
}

/* ═══════════ TẦNG 2b · VIỆC PHẢI LÀM TRONG CHẶNG TỪ MỚI ═══════════ */

/**
 * VIỆC CỦA CON — danh sách việc của chặng Từ mới, để vẽ thành thanh trạng thái.
 *
 * ── VÌ SAO CÓ PHẦN NÀY ──
 * Bản trước mở nút đi tiếp đúng luật, nhưng nói điều kiện ấy bằng MỘT DÒNG CHỮ:
 * "Con xem hết video, hoặc bấm 🔈 nghe đủ 3 từ, rồi đi tiếp nhé." Bé lớp 1 chưa
 * đọc được dòng ấy. Nên thực tế bé thấy một nút xám không rõ vì sao, và cách duy
 * nhất để biết là bấm thử khắp nơi. Cả quyển dựng trên nguyên tắc "không bắt bé
 * đọc chữ" mà đúng chỗ chỉ đường lại quay về chữ.
 *
 * Nên: mỗi việc là MỘT Ô CÓ HÌNH. Bé liếc một cái là thấy ô nào còn trắng.
 *
 * ── BA TRẠNG THÁI, VÀ VÌ SAO KHÔNG PHẢI HAI ──
 *   chua  chưa đụng tới       ○
 *   dang  làm được một nửa    ◔   (mới nghe, hoặc mới nói)
 *   xong  nghe rồi, nói rồi   ◕
 *
 * Hai trạng thái (xong/chưa) thì bé nghe xong một từ mà ô vẫn trắng — công vừa bỏ
 * ra không để lại dấu gì, và đó đúng là lúc bé bỏ cuộc. Ô phải nhúc nhích ngay
 * lần bấm đầu.
 *
 * ── VÌ SAO VIỆC NÓI KHOÁ ĐƯỜNG ĐI, MÀ MICRO HỎNG THÌ MỞ ──
 * Nghe rồi đi tiếp thì phần nói thành thứ trang trí — bé không bao giờ mở miệng,
 * mà nói mới là chỗ khó nhất của học tiếng. Nên nói PHẢI làm.
 *
 * Nhưng micro là thứ hỏng được vì lý do chẳng liên quan gì tới bé: máy không có
 * micro, trình duyệt chưa được cho phép, hoặc mất mạng (Web Speech cần mạng). Bé
 * mà kẹt vì mấy thứ ấy thì đúng vào cái bẫy `THU_TOI_THIEU` sinh ra để tránh —
 * xem đầu tệp. Nên `micHong` mở đường NGAY, và màn hình phải nói rõ là do máy.
 *
 * ⚠ Đường "tự mở" này là loại đã nuốt sáu lỗi câm của đợt trước: nó chỉ chạy khi
 * có sự cố, nên đi thử tay gần như không bao giờ chạm tới. Phải có phép kiểm.
 */
export const TT_VIEC = { chua: 'chua', dang: 'dang', xong: 'xong' };

/**
 * NÓI ĐƯỢC MỘT TỪ CHƯA — lại đúng một luật ấy, lần thứ tư.
 *
 *     ĐÃ NÓI ĐƯỢC KHI: đã ĐẠT — hoặc đã THỬ THẬT ít nhất 2 lần.
 *
 *   dat   đạt ngưỡng phát âm            → ⭐
 *   thu   thử thật đủ số lần, chưa đạt  → ✓   (vẫn đi tiếp được)
 *   chua  chưa đủ                       → ○
 *
 * ── VÌ SAO KHÔNG ĐÒI PHẢI ĐẠT ──
 * Bé ngọng, bé nói giọng miền, micro rẻ tiền — cả ba đều có thể không bao giờ
 * chạm ngưỡng. Khoá cứng theo "phải đạt" thì bé tắc là tắc vĩnh viễn, và cái nó
 * học được không phải tiếng Anh. Xem đầu tệp.
 *
 * ── VÌ SAO KHÔNG NHẬN "CÓ MỞ MIỆNG LÀ XONG" ──
 * Bé nhìn 🍟 mà đọc "chicken" cũng được tính thì dấu ✓ trên thanh không còn nghĩa
 * là "con nói được từ này" — nó chỉ còn nghĩa là "con có phát ra tiếng". Nên
 * `lan` chỉ đếm những lần MÁY NGHE RA CHỮ; im lặng không cộng (xem `coTieng` ở
 * `NutNoi`). Hai chốt ấy phải đi cùng nhau, gỡ một cái là cái kia thành vô nghĩa.
 */
export function noiDuoc({ caoNhat = null, lan = 0 } = {}, dat = 6) {
  if (caoNhat != null && caoNhat >= dat) return 'dat';
  return lan >= THU_TOI_THIEU ? 'thu' : 'chua';
}

/**
 * @param  {object} t  đã làm được những gì
 * @param  {object} t.soNoi  sổ nói: `{ [từ]: { caoNhat, lan } }` — xem `noiDuoc`
 * @return {{viec: Array, mo: boolean, conThieu: number, vuongMicro: boolean}}
 *
 * `viec` mở đầu bằng MỘT Ô CHO MỖI VIDEO từ mới; sau đó mỗi từ một ô.
 *
 * ── VÌ SAO KHÔNG CÒN MỘT Ô VIDEO ──
 * Lớp 3 có unit 15 từ, và video từ mới tách theo NHÓM NGHĨA thành ba tệp (xem
 * `dsVideoTu`). Một ô chung cho ba tệp thì ô ấy sáng lên ngay khi bé xem xong tệp
 * đầu, và hai tệp kia thành thứ không ai biết là có — đúng cái mà thanh VIỆC CỦA
 * CON sinh ra để tránh.
 */
export function viecChangTu({
  dsTu = [], dsVideo = [], daXem = [], videoHong = false,
  daNghe = [], soNoi = {}, micHong = false, datNoi = 6,
} = {}) {
  const nghe = new Set(daNghe);
  const xem = new Set(daXem);
  const mucNoi = (tu) => noiDuoc(soNoi[tu], datNoi);
  const noi = new Set(dsTu.map((v) => v.tu).filter((tu) => mucNoi(tu) !== 'chua'));
  const viec = [];

  for (const [i, g] of dsVideo.entries()) {
    viec.push({
      ma: `__video:${g.tep}`, loai: 'video', tep: g.tep, bieuTuong: '🎬',
      /* Số thứ tự để thanh việc đánh số lên ô: bốn ô 🎬 giống hệt nhau thì bé
         không biết mình còn thiếu cái nào. */
      thuTu: i + 1, tong: dsVideo.length,
      /* Bài một nhóm thì nhãn y như cũ; nhiều nhóm thì nhãn phải NÓI RA nhóm nào,
         không thì ba ô giống hệt nhau và bé không biết mình còn thiếu cái nào. */
      nhan: dsVideo.length === 1 ? 'Xem từ mới' : g.ten,
      /* Video hỏng KHÔNG phải là "xong" — bé chưa xem gì cả. Nhưng cũng không
         được để "chưa", vì thế là bắt bé làm một việc bất khả. Ô riêng: `hong`. */
      tt: videoHong ? 'hong' : (xem.has(g.tep) ? TT_VIEC.xong : TT_VIEC.chua),
      viecCon: [],
    });
  }

  for (const v of dsTu) {
    const n = nghe.has(v.tu);
    const mn = mucNoi(v.tu);
    const o = mn !== 'chua' || micHong;
    viec.push({
      ma: v.tu, loai: 'tu', nhan: v.tu, nghia: v.nghia, ve: v.ve, hinh: v.hinh,
      daNghe: n, daNoi: mn !== 'chua', mucNoi: mn,
      boQuaNoi: micHong && mn === 'chua',
      tt: (n && o) ? TT_VIEC.xong : ((n || o) ? TT_VIEC.dang : TT_VIEC.chua),
      viecCon: [
        { ma: 'nghe', chu: '🔈', ten: 'nghe', xong: n },
        { ma: 'noi', chu: '🎤', ten: 'nói', xong: mn !== 'chua', sao: mn === 'dat',
          boQua: micHong && mn === 'chua' },
      ],
    });
  }

  /* Xem hết video HOẶC nghe đủ từng từ — hai đường, cả hai đều là nghe đủ chừng
     ấy từ. Bài không có video thì vế ấy tự đúng, không phải chờ gì. */
  const ngheDu = dsTu.length > 0 && dsTu.every((v) => nghe.has(v.tu));
  /* XEM HẾT nghĩa là hết MỌI video của bài. Bài ba nhóm mà xem một tệp đã kể là
     xong thì hai nhóm từ kia không ai giảng — cùng cái bẫy đã sửa ở chặng mẫu câu. */
  const xemXong = dsVideo.length === 0 || videoHong
    || dsVideo.every((g) => xem.has(g.tep));
  const noiDu = dsTu.length === 0 || dsTu.every((v) => mucNoi(v.tu) !== 'chua');

  return {
    viec,
    mo: (xemXong || ngheDu) && (noiDu || micHong),
    conThieu: viec.filter((x) => x.tt !== TT_VIEC.xong && x.tt !== 'hong').length,
    vuongMicro: micHong && !noiDu,
  };
}

/**
 * VIỆC CỦA CON trong chặng MẪU CÂU — cùng khuôn với chặng Từ mới.
 *
 * Mỗi mẫu câu MỘT ô, hai việc trong ô: xem video 🎬 và nói cả câu 🎤. Bài hỏi–đáp
 * có hai mẫu rời (câu hỏi trước, câu trả lời sau) nên thành hai ô.
 *
 * ── VÌ SAO NÓI CŨNG KHOÁ Ở ĐÂY ──
 * Nói được từng TỪ rời không phải là nói được tiếng Anh. Cả câu mới là chỗ bé
 * phải ghép nhịp, và đó là việc khó nhất của chặng này. Bản trước chỉ đòi xem hết
 * video, nên `NutNoi` ở đây thành thứ trang trí y hệt chuyện đã xảy ra ở chặng
 * Từ mới. Cùng một cái bẫy, đừng để lại lần thứ hai.
 *
 * Vẫn giữ đủ hai đường lui: video hỏng thì ô ấy thành `hong` và không chặn, micro
 * hỏng thì tha việc nói (nhưng KHÔNG tha việc xem).
 */
export function viecChangCau({
  dsCau = [], daXem = [], videoHong = false, soNoi = {}, micHong = false, datNoi = 6,
} = {}) {
  const xem = new Set(daXem);
  const mucNoi = (cau) => noiDuoc(soNoi[cau], datNoi);

  const viec = dsCau.map((c) => {
    const x = videoHong || xem.has(c.tep);
    const mn = mucNoi(c.cau);
    const o = mn !== 'chua' || micHong;
    return {
      ma: c.tep || c.cau, loai: 'cau', nhan: c.cau, nghia: c.nhanVai, bieuTuong: '💬',
      daXem: x, daNoi: mn !== 'chua', mucNoi: mn,
      boQuaNoi: micHong && mn === 'chua',
      tt: (x && o) ? TT_VIEC.xong : ((x || o) ? TT_VIEC.dang : TT_VIEC.chua),
      viecCon: [
        { ma: 'xem', chu: '🎬', ten: 'xem', xong: x, boQua: videoHong && !xem.has(c.tep) },
        { ma: 'noi', chu: '🎤', ten: 'nói', xong: mn !== 'chua', sao: mn === 'dat',
          boQua: micHong && mn === 'chua' },
      ],
    };
  });

  const xemDu = dsCau.length === 0 || videoHong || dsCau.every((c) => xem.has(c.tep));
  const noiDu = dsCau.length === 0 || dsCau.every((c) => mucNoi(c.cau) !== 'chua');

  return {
    viec,
    mo: xemDu && (noiDu || micHong),
    conThieu: viec.filter((x) => x.tt !== TT_VIEC.xong).length,
    vuongMicro: micHong && !noiDu,
  };
}

/* ═══════════ TẦNG 3 · MỘT CÂU ═══════════ */

/**
 * Được bỏ qua câu này chưa? `lan` là số lần bé ĐÃ NỘP và sai.
 *
 * Thang ba nấc, và ba nấc là cố ý:
 *
 *   sai lần 1        → chỉ bảo thử lại. Bé chưa kịp nghĩ.
 *   sai lần 2        → hiện GỢI Ý. Đây là nấc `THU_TOI_THIEU`: đã thử thật.
 *   sai lần 3 trở đi → hiện đáp án, và cho để lại sau.
 *
 * Nếu mở nút bỏ qua ngay ở nấc 2 thì gợi ý và đáp án hiện CÙNG LÚC — không bé nào
 * đọc gợi ý khi đáp án nằm ngay bên cạnh, và cái nấc gợi ý coi như không tồn tại.
 * Nên phải để bé có đúng một lượt được thử VỚI gợi ý trong tay.
 *
 * Vẫn đúng lời "ít nhất 2 lần": đây là 3, mà 3 thì nhiều hơn 2.
 *
 * Câu bỏ qua bị ĐẾM lại — xem `conNoTrongMuc` — để cuối mức bé được mời làm lại
 * đúng những câu ấy.
 */
export const HIEN_GOI_Y = THU_TOI_THIEU;
export const duocBoQua = (lan) => lan > THU_TOI_THIEU;

/** Trong một mức luyện tập: những câu bé bỏ qua, để mời làm lại. */
export const conNoTrongMuc = (ketQua = []) => ketQua.filter((k) => k?.boQua).map((k) => k.id);

/* ═══════════ KỲ ÔN TẬP CHƯƠNG ═══════════ */

/**
 * Kỳ ôn tập chương đã mở chưa?
 *
 * Ở đây KHÔNG có cửa "thử 2 lần" như khi mở bài. Cố ý: mở bài là để bé còn có
 * đường đi tiếp khi tắc; còn kỳ ôn tập là chỗ CHỐT một chương và ghi vào học bạ.
 * Cho vào khi còn bốn bài chưa đạt thì huy hiệu ấy không nói lên điều gì, mà đó
 * lại đúng là thứ bố mẹ nhìn vào để tin.
 *
 * Bé đi vòng qua vài bài vẫn học tiếp được bình thường — chỉ là muốn lấy huy hiệu
 * thì phải quay lại làm cho xong những bài còn nợ. Đó là chỗ món nợ được đòi.
 */
export const moKyOnTap = (tienDo, dsBai = []) =>
  dsBai.length > 0 && dsBai.every((id) => tienDo?.micros?.[id]?.pass);

/** Còn mấy bài nữa thì mở được kỳ ôn tập — để nói cho bé biết còn bao xa. */
export const conThieuChoOnTap = (tienDo, dsBai = []) =>
  dsBai.filter((id) => !tienDo?.micros?.[id]?.pass).length;
