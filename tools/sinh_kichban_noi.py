#!/usr/bin/env python3
"""SINH KỊCH BẢN PHÒNG LUYỆN NÓI — mỗi unit một kịch bản dạy NÓI CẢ CÂU.

    python3 tools/sinh_kichban_noi.py --lop 3

Đọc `web/public/content/taN/DL_TAN_B*.json` rồi đẻ ra `taN/kichban_noi.json`.

── VÌ SAO PHẢI CÓ TỆP NÀY ──
Bác chốt 13-08: "viết sẵn kịch bản theo từng bài học để AI theo bài nào thì dùng
kịch bản đó sẽ đảm bảo hơn."

Đúng, và có bằng chứng. Trong một buổi đi thử, mô hình đã hai lần KHÔNG theo lời
dặn dù lời dặn viết rất rõ:

  · sinh ra "Bye, bike." — nhét đồ vật vào ô dành cho TÊN NGƯỜI;
  · nói y một câu hai lượt liền, ngay sau khi được dặn "đừng lặp".

Dặn dò là thứ mô hình CÓ THỂ theo. Kịch bản viết sẵn là thứ nó KHÔNG CẦN theo —
câu tiếng Anh đã nằm sẵn trong tệp, nó chỉ còn việc diễn đạt lời tiếng Việt và
phản ứng với cái bé vừa nói. Rút đúng cái quyền hay hỏng ra khỏi tay nó.

══════════════════════════════════════════════════════════════════════════════
BẢN 18-08-2026 — DẠY NÓI, KHÔNG PHẢI ĐỌC TỪ RỜI
══════════════════════════════════════════════════════════════════════════════

Bác xem phòng nói rồi bảo: "AI đóng vai trò là Cô giáo dạy học sinh nói được các
câu giao tiếp hoàn chỉnh chứ không như máy như giờ chẳng có hiệu quả gì. Cần dạy
học sinh nói rồi hướng dẫn học sinh sửa."

Bản cũ hỏng ở đâu, kể thẳng ra:

  1. PHẦN LỚN LƯỢT LÀ TỪ RỜI. Unit 5 lớp 3 có 15 bước thì 8 bước là một chữ trần
     ("cooking", "dancing"). Bé nhại xong tám chữ ấy vẫn không nói nổi một câu.
     Mà buổi kết thúc ở ba lần nói đúng — nên bé giỏi thì XONG BUỔI trước khi
     gặp câu đầu tiên.

  2. LỜI VIỆT LÀ MỘT KHUÔN DUY NHẤT. Cả tám bước từ đều đúng một dòng
     "Con nghe rồi nói lại từ này nhé — nghĩa là …". Đấy là chỗ chữ "như máy"
     của bác chỉ vào.

  3. KHÔNG CÓ LƯỢT SỬA. Bé nói trượt 3 điểm thì bước sau vẫn là bước kế tiếp
     trong danh sách; cái câu bé chưa nói được nằm lại đó. Nay `buocTiepTheo`
     dựng bước `sua` ngay tại chỗ — xem `phongnoi.js`.

  4. KHÔNG CÓ ĐỐI THOẠI. Bước `mau` đưa bé CẢ CẶP hỏi–đáp để nhại
     ("What's your hobby? - It's cooking.") — bé đọc thuộc cả hai vai, không bao
     giờ phải tự đáp ai. Nay tách đôi: cô hỏi thì bé đáp, rồi đổi vai.

── CÁC LOẠI BƯỚC, VÀ VIỆC CỦA BÉ Ở TỪNG LOẠI ──

    chao      Hello!                     bé chào lại
    hoiThich  (không có câu)             bé bấm hình chọn thứ mình thích
    mau       cả mẫu câu của sách        bé NGHE cô làm mẫu một lần
    noiCa     một câu trọn của sách      bé nói lại CẢ CÂU (không phải mỗi từ)
    hoiBe     nửa HỎI của mẫu            cô hỏi thật — bé TỰ ĐÁP
    doiVai    nửa HỎI của mẫu            đổi vai: BÉ hỏi, cô đáp
    thay      nửa ĐÁP đã điền            bé nói câu ấy VỀ CHÍNH MÌNH
    tu        một từ trần                CHỈ dùng khi bé đuối — xem `haDoKho`
    ket       (không có câu)             lời chia tay

Bước `sua` KHÔNG nằm trong tệp này: nó dựng lúc chạy từ chính câu bé vừa trượt.

── MỌI CÂU TIẾNG ANH ĐỀU LÀ CÂU CỦA SÁCH ──
`noiCa` lấy từ `canonicalExamples` — những câu chính bộ sinh bài đã dựng và đã
qua cổng. Không ghép câu mới ở đây. Luật "không bịa câu tiếng Anh" của cả môn.

Cặp hỏi–đáp tách ở dấu `" - "`, đúng cách `cauSachCuaBai` trong `phongnoi.js`
đang tách. Lớp 1 không có cặp nào (21 mẫu, 0 cặp) nên lớp 1 không có `hoiBe`
và `doiVai` — ở đó `thay` chính là chỗ bé nói về mình.

── VÌ SAO SINH CHỨ KHÔNG GÕ TAY 53 TỆP ──
Từ mới và mẫu câu đã nằm trong bài học rồi. Gõ tay lần nữa là chép, mà chép thì
sớm muộn lệch — sửa từ trong bài mà quên sửa trong kịch bản, không cổng nào bắt
được. Sinh ra từ chính bài học thì hai bên không thể lệch.

Sinh xong VẪN SỬA TAY ĐƯỢC: tệp là JSON thường, unit nào cần kịch bản riêng thì
sửa thẳng rồi thêm cờ `tay: true` để lần sinh sau không đè lên.

── BA CHỖ THAY LÚC CHẠY ──
    {ten}     tên bé
    {thich}   thứ bé vừa chọn ở màn "Con thích cái nào nhất?"
Chỗ nào không thay được thì máy con điền mặc định đã ghi sẵn ở `mac_dinh`.
"""
import json
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent

# Quyển nào — `--lop N`, mặc định 1 để lệnh cũ trong sổ vẫn chạy.
# ⚠ `RA_DATA` phải MANG SỐ LỚP. Bản đầu ghi thẳng `kichban_noi.json` cho mọi quyển,
# nên chạy lớp 2 là đè mất kịch bản lớp 1 — mà lớp 1 có ba bài viết tay không sinh
# lại được bằng máy (tools/kichban_tay_ta1.py mới dựng lại được).
LOP = 1
for _i, _a in enumerate(sys.argv):
    if _a == '--lop' and _i + 1 < len(sys.argv):
        LOP = int(sys.argv[_i + 1])
NOI_DUNG = GOC / 'web' / 'public' / 'content' / f'ta{LOP}'
RA_PUBLIC = NOI_DUNG / 'kichban_noi.json'
RA_DATA = GOC / 'data' / 'tienganh' / (
    'kichban_noi.json' if LOP == 1 else f'kichban_noi_lop{LOP}.json')
TIEN_TO_BAI = f'DL_TA{LOP}_B*.json'

# Nhiều nhất bao nhiêu câu `noiCa` một mẫu. `canonicalExamples` của lớp 3 có bài
# tới 12 câu cùng khuôn; nhét hết vào thì phần luyện toàn một khuôn, mà bé chỉ đi
# hết được vài bước trong một buổi. Bốn câu là đủ để bé thấy ô trống thay được.
NOI_CA_TOI_DA = 4

# Câu bị bỏ vì nguồn hỏng — in ra cuối mỗi lần chạy. Nuốt im thì cái thiếu ở bản đồ
# nằm nguyên đó, mà kịch bản trông vẫn đầy đủ.
BO_QUA: list[str] = []


def so_o_trong(cong_thuc):
    return len(re.findall(r'\[[^\]]+\]', cong_thuc or ''))


def o_trong(cong_thuc):
    """Ô trống của công thức nhận LOẠI gì.

    `Bye, + [Name].` mà điền từ vựng vào là ra "Bye, book." — vô nghĩa, và với bé
    đang tập nhại thì đó là dạy sai. Đã sinh ra thật khi thả cho mô hình tự điền.

    ⚠ HAI LOẠI LÀ KHÔNG ĐỦ — vá 09-10-2026. Bản cũ gộp mọi ô không-phải-tên thành
    "ô nhận từ bất kỳ", nên bước THAY nhét từ vựng đầu bài vào ô kiểu khác. BỐN câu
    đã lên dữ liệu phát hành như thế, và bé nghe chúng suốt buổi:

        ta1/B11  "She's bus."   "He's bus."         ô `[Number]` (tuổi) nhận danh từ
        ta2/B12  "The grape are on the table."       ô `[Noun-plural]` nhận dạng gốc
        ta2/B14  "He's/She's brother."                ô `[Number]` nhận từ gia đình

    Phải khớp từng chữ với `loaiOTrong` ở `web/src/mon/tienganh/lib/phongnoi.js`.
    Không có cổng so hai bản mã (một bên Python, một bên JS), nhưng CÓ cổng so KẾT
    QUẢ — `tienganh_phongnoi.test.mjs` soi mọi câu của mọi kịch bản bằng luật JS, nên
    lệch nhau một chữ là nó đỏ. Soi kết quả thì chắc hơn soi hai bản mã.
    """
    m = re.search(r'\[([^\]]+)\]', cong_thuc or '')
    if not m:
        return None
    o = m.group(1).lower()
    if re.search(r'name|tên', o):
        return 'ten'
    if re.search(r'plural|số nhiều', o):
        return 'nhieu'
    if re.search(r'-ing|^v-?ing|\bing\b', o):
        return 'ing'
    if re.search(r'past|\bqk\b|\bv2\b', o):
        return 'qk'
    if re.search(r'number|age|tuổi|\bsố\b', o):
        return 'so'
    return 'tu'


def la_tu_so(t):
    """Mục từ này là một CON SỐ — suy từ lời chú của sách ("mười một (11)")."""
    return bool(re.search(r'\(\s*\d+\s*\)|^\s*\d+\s*$', t.get('nghia') or ''))


def dien_duoc_vao_o(loai, tu):
    """Những giá trị điền được vào một ô, theo ĐÚNG loại của nó.

    Khớp với `dienDuocVaoO` bên JS. Mục từ có thể ĐÃ ở dạng ấy sẵn và trường dẫn
    xuất để `null` — lớp 4 unit 20 dạy hẳn `putting up a tent` với `dang_ing: null`.
    """
    if loai == 'ing':
        return [t.get('dang_ing') or (t['tu'] if re.search(
            r'ing$', t['tu'].split()[0], re.I) else None) for t in tu]
    if loai == 'qk':
        return [t.get('dang_qk') or t['tu'] for t in tu]
    if loai == 'nhieu':
        return [t.get('so_nhieu') or t['tu'] for t in tu]
    if loai == 'so':
        return [t['tu'] for t in tu if la_tu_so(t)]
    # Ô thường thì TRỪ con số ra — đó là chỗ "this sixteen" lọt qua bên JS.
    return [t['tu'] for t in tu if not la_tu_so(t)]


def ten_trong_vi_du(cong_thuc, cau):
    """Giá trị mà chính SÁCH điền vào ô trống — `Hi, I'm + [Name].` + `Hi, I'm Bill.`
    thì ra "Bill".

    Dùng làm giá trị dự phòng khi bé chưa khai tên. Bịa sẵn một cái tên ("Bo") thì
    bé nào không khai tên cũng bị gọi bằng tên người khác; lấy tên trong sách thì
    ít nhất bé đang nhại đúng nhân vật của bài.
    """
    khung = re.sub(r'\s*\+\s*', ' ', cong_thuc or '')
    mau = re.escape(khung).replace(r'\[', '[').replace(r'\]', ']')
    mau = re.sub(r'\[[^\]]+\]', '(.+?)', mau)
    m = re.fullmatch(mau, cau or '')
    return m.group(1) if m else None


def khop_khung(cong_thuc, cau):
    """Câu này có phải là một cách điền của công thức kia không?

    ⚠ ĐỪNG LỌC THEO NỬA HỎI. Bản đầu gom câu cùng khuôn bằng cách so nửa HỎI, mà
    lớp 3 unit 5 có hai mẫu dùng CHUNG một câu hỏi:

        What's your hobby? - It's cooking.
        What's your hobby? - I like singing.

    Nên mẫu "I like …" nhận về đúng bốn câu "It's …" của mẫu kia, và lời Việt thì
    lại giảng chữ "singing" — cô giảng một chữ không có trong câu cô vừa nói. Cổng
    không bắt được: câu nào cũng là câu của sách, và nó có mặt thật trong bài.

    So theo KHUNG ĐÁP thì hai mẫu tách hẳn ra, vì khung mới là thứ khác nhau.
    """
    if not cong_thuc:
        return False
    khung = re.sub(r'\s*\+\s*', ' ', cong_thuc)
    mau = re.escape(khung).replace(r'\[', '[').replace(r'\]', ']')
    mau = re.sub(r'\[[^\]]+\]', '(.+?)', mau)
    return re.fullmatch(mau, str(cau or '').strip()) is not None


def dien(cong_thuc, gia_tri):
    """Điền một giá trị vào ô trống, bỏ dấu `+` nối của công thức."""
    return re.sub(r'\[[^\]]+\]', gia_tri, re.sub(r'\s*\+\s*', ' ', cong_thuc))


def tach_doi(s):
    """`"What's your hobby? - It's cooking."` → `("What's your hobby?", "It's cooking.")`.

    Không phải cặp thì trả `(None, cả câu)` — chỗ gọi chỉ cần hỏi "có nửa hỏi không".
    Cắt ở `" - "` đúng như `cauSachCuaBai` bên `phongnoi.js`; hai bên mà cắt khác
    nhau thì câu ở kịch bản không nằm trong túi câu hợp lệ, và không gì kêu.
    """
    phan = [x.strip() for x in str(s or '').split(' - ')]
    if len(phan) == 2 and all(phan):
        return phan[0], phan[1]
    return None, str(s or '').strip()


def tach_lua_chon(s):
    """`"Yes, it is. / No, it isn't."` → `["Yes, it is.", "No, it isn't."]`.

    ── VÌ SAO PHẢI TÁCH ──
    45 câu của lớp 2·3 là mẫu YES/NO, và sách viết cả hai lối đáp trong MỘT chuỗi
    ngăn bằng dấu gạch chéo. Đưa nguyên chuỗi ấy cho bé nhại thì bé đọc cả hai câu
    trái ngược nhau liền một hơi — "vâng đúng rồi không phải đâu". Mà đó lại đúng
    là chỗ đáng dạy nhất của bài: biết đáp CÓ hay KHÔNG.

    Tách ra thì mỗi vế là một câu trọn vẹn, và cả hai đều là câu của sách. Chỗ soi
    câu bên `phongnoi.js` (`cauSachCuaBai`) cũng tách đúng như thế — hai bên lệch
    nhau thì câu ở kịch bản rơi ra ngoài vốn câu hợp lệ mà không gì kêu.
    """
    if '/' not in str(s or ''):
        return [str(s or '').strip()]
    ra = [x.strip() for x in re.split(r'\s*/\s*', str(s))]
    # Chỉ nhận khi MỌI vế đều là một câu trọn. `a/an` trong công thức chưa điền cũng
    # có dấu gạch chéo, mà nó không phải hai lựa chọn câu.
    if all(re.match(r'^[A-Z].*[.?!]$', x) for x in ra if x):
        return [x for x in ra if x]
    return [str(s).strip()]


def cau_lanh_lan(s):
    """Câu này có sạch để đưa cho bé đọc không.

    ⚠ Bản đồ lớp 2 khai `"... - Yes,[Pronoun] is./No,[Pronoun] isn't."` — THIẾU DẤU
    CÁCH sau dấu phẩy (data/ban_do_tieng_anh.json dòng 58013). Điền vào thì ra
    "Yes,he is." Máy đọc lên nghe thành một chữ, và `cauHopLe` cũng gạt vì `gonCau`
    bỏ dấu phẩy mà không chèn khoảng trắng: "yeshe is".

    Ở đây chỉ BỎ QUA và đếm, KHÔNG tự chèn dấu cách. Sửa hộ ở tầng kịch bản thì câu
    trong phòng nói khác câu trên màn bài học, mà chỗ sai thật thì vẫn nằm nguyên
    trong bản đồ. Bộ sinh in ra để còn người sửa tận gốc.
    """
    return bool(s) and not re.search(r'[,;](?=\S)', s)


SO_DEM = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']


def chu_biet(bai):
    """Túi CHỮ bé được coi là đã biết ở bài này.

    ⚠ ĐÂY LÀ BẢN SAO CỦA `cauSachCuaBai` BÊN `phongnoi.js`. Chép luật sang hai thứ
    tiếng là chuyện đáng ngại, nhưng cổng `tienganh_phongnoi` soi từng câu kịch bản
    bằng chính `cauHopLe` của bên kia — nên hai bên lệch một nấc là cổng đỏ ngay,
    chứ không âm thầm. Đã bắt được thật hai lần trong buổi 18-08.

    ── VÌ SAO PHẢI LỌC ──
    `canonicalExamples` KHÔNG phải chỗ nào cũng sạch. Lớp 2 unit 5 khai:

        "What's She doing? - She is doing a quiz."     ← "She" viết hoa giữa câu
        "What's He doing? - He is doing a question."   ← "doing a question" vô nghĩa

    Sách sinh ra chúng bằng cách điền máy vào công thức nhiều ô, không ai soi nghĩa.
    Đem cho bé nhại thì bé học một câu tiếng Anh không ai nói. Lọc theo túi chữ thì
    cả hai rơi ra — vì "she" không nằm trong vốn của bài ấy.
    """
    k = bai['knowledgeCore']
    mau = k.get('mauCauDs') or ([k['mauCau']] if k.get('mauCau') else [])
    biet = set()
    for v in k.get('vocabulary') or []:
        biet.update(chu_trong(v['tu']))
        # ⚠ DẠNG BIẾN ĐỔI CŨNG LÀ CHỮ BÉ ĐỌC. Lớp 5 dạy thì quá khứ, và
        # "bought" · "collected" không suy ra được từ "buy" · "collect" — túi chỉ
        # có dạng gốc thì phòng nói gọi câu đúng là "chữ lạ" rồi BỎ câu ấy đi.
        for d in ('so_nhieu', 'dang_ing', 'dang_qk', 'so_it'):
            biet.update(chu_trong(v.get(d)))
    # Nhóm `them` của bản chuẩn — tên phố, tên lớp, chỗ để đồ. Không nạp thì
    # "Class 5A" thành chữ lạ "a", và "beside the table" mất chữ "table".
    try:
        cn = json.loads((GOC / f"data/tienganh/chuan_lop{LOP}.json").read_text('utf8'))
        for ten, goi in (cn.get('them') or {}).items():
            # ⚠ TRỪ NHÓM ĐẠI TỪ. Các nhóm `them` khác là DANH TỪ phụ trợ nằm sẵn
            # trong câu sách ("Class 5A" · "the table"); đại từ thì khác hẳn — nó
            # là thứ điền vào ô `[Pronoun]`, mà bên `phongnoi.js` ô ấy chỉ điền
            # được bằng vốn của CHÍNH BÀI. Coi cả danh sách đại từ chung là "bé đã
            # biết" thì bộ sinh đẻ ra câu mà app từ chối ngay sau đó.
            #
            # Đo trên cả 5 quyển: bỏ nhóm này chỉ rụng 4 nửa câu, và cả 4 đều bẩn —
            # "She is doing a quiz." (chính chú thích trên đã nêu là câu phải lọc)
            # và "Yes,he is./No,he isn't." (thiếu cả dấu cách). Không rụng câu lành
            # nào, vì đại từ bài NÀO CÓ DẠY thì đã vào túi qua `vocabulary` và
            # `mau_cau` rồi.
            if ten == 'dai_tu' or not isinstance(goi, dict):
                continue
            for m in goi.get('muc') or []:
                biet.update(chu_trong(m if isinstance(m, str) else m.get('word')))
    except Exception:
        pass
    for m in mau:
        biet.update(chu_trong(m.get('cau')))
        biet.update(chu_trong(m.get('congThuc')))
    if any(re.search(r'\[Number\]', m.get('congThuc') or '', re.I) for m in mau):
        biet.update(SO_DEM)
    return biet


def chu_trong(s):
    return re.findall(r"[a-z']+", str(s or '').lower())


def _cho_thay(m):
    """Phần THAY ĐƯỢC của mẫu câu, kèm lời sách giải thích nó làm gì.

    `phan[].thay` là chỗ sách đánh dấu ô trống — dùng nó thay vì tự đoán từ công
    thức, vì lời `lam_gi` ("SỞ THÍCH, có đuôi -ing") là thứ đáng dạy nhất mà công
    thức không mang theo.
    """
    for p in (m.get('phan') or []):
        if p.get('thay'):
            return p.get('chu') or '', p.get('lam_gi') or ''
    return '', ''


def _bay_cua_mau(bai, m):
    """Lời cảnh báo của SÁCH cho đúng mẫu câu này — `misconceptions[].why`.

    ⚠ CHỈ NHẬN KHI `right` TRÙNG ĐÚNG CÂU MẪU. Có bài khai `right` sai hẳn: lớp 2
    unit 3 ghi `"right": "Let is look at the sea!"` cho mẫu "Let's look at the
    sea!" — một khuôn giải thích chung ("thiếu is") dán nhầm vào câu có `'s` là
    dạng rút của `us`. Đem câu ấy đi dạy thì cô giáo máy dạy bé một câu sai.
    Không trùng thì BỎ, chứ không sửa hộ: sửa hộ là đoán ý người soạn.
    """
    for x in (bai['knowledgeCore'].get('misconceptions') or []):
        if str(x.get('right') or '').strip() == str(m.get('cau') or '').strip():
            return str(x.get('why') or '').strip() or None
    return None


def _muc_tieu(bai):
    """Năng lực của unit, thành một dòng — chỗ mô hình biết buổi này dạy CÁI GÌ."""
    o = bai.get('objective') or {}
    t = str(o.get('text') or '').strip()
    return t or str(bai.get('title') or '')


def kich_ban_cua(bai):
    k = bai['knowledgeCore']
    tu = k.get('vocabulary', [])
    mau = k.get('mauCauDs') or []
    if not mau and k.get('mauCau'):
        mau = [k['mauCau']]
    vi_du = [str(x) for x in (k.get('canonicalExamples') or [])]
    biet = chu_biet(bai)

    buoc = [{'loai': 'chao', 'en': 'Hello!',
             'vi': 'Chào con! Hôm nay cô con mình tập nói thành câu nhé.'}]

    # Hỏi sở thích khi có từ hai cái trở lên — chọn giữa một cái không phải là chọn.
    if len(tu) >= 2:
        buoc.append({'loai': 'hoiThich'})

    # ── ĐƯỜNG LUI: từng TỪ một ──
    # Không nằm trong vòng luyện thường nữa (xem `BUOC_LUYEN` bên `phongnoi.js`),
    # chỉ dùng khi `haDoKho` bật — bé nói trượt mấy lượt liền thì lùi về chỗ dễ
    # nhất rồi đi lên lại. Bỏ hẳn chúng đi thì bé đuối không còn gì để bám.
    for t in tu:
        # Nghĩa để TRONG NGOẶC. Sách chú `you` là "bạn, các bạn"; để trần thì phép
        # soi lời Việt đọc chữ "bạn" ấy là cô đang gọi bé bằng "bạn" và gạt cả câu.
        # Trong ngoặc là trích lời sách — xem `loiVietHopLe`.
        buoc.append({'loai': 'tu', 'en': t['tu'], 'tu': t['tu'],
                     'vi': f"Chỉ một chữ thôi: “{t['tu']}” — nghĩa là “{t['nghia']}”."})

    # ── VÒNG LUYỆN: CÂU ──
    for i, m in enumerate(mau):
        hoi, dap = tach_doi(m.get('cau'))
        cho, lam_gi = _cho_thay(m)
        bay = _bay_cua_mau(bai, m)

        # 1 · CÔ LÀM MẪU. Lượt duy nhất bé chỉ phải nghe.
        # ⚠ `dungDe` và `tinhHuong` KHÔNG ghép thẳng vào `vi`.
        #
        # Cổng bắt được ngay: `tinhHuong` của lớp 1 unit 1 là "Ngày đầu tới lớp, con
        # đứng cạnh một bạn chưa quen bao giờ." — chữ "bạn" ở đây là DANH TỪ, hoàn
        # toàn đúng tiếng Việt, nhưng `loiVietHopLe` cấm "bạn" vì cô không được gọi
        # bé là "bạn". Ghép vào là lời viết sẵn TỰ NÓ trượt phép soi, và `loiVietSach`
        # sẽ vứt nó đi đúng lúc cần nhất.
        #
        # Nên hai thứ ấy đi đường KHÁC: chúng là ngữ cảnh cho MÔ HÌNH (`dongBuoc` gửi
        # kèm lời dặn), để cô kể lại bằng lời của cô với đúng đại từ. Còn `vi` giữ
        # ngắn và luôn qua được phép soi — nó là đường lui, không phải bài giảng.
        buoc.append({
            'loai': 'mau', 'en': m['cau'], 'mauCau': m['cau'],
            'vi': 'Cô làm mẫu cả câu hỏi lẫn câu đáp. Con nghe, rồi nói theo cô cũng được.',
            **({'dungDe': m['dungDe']} if m.get('dungDe') else {}),
            **({'tinhHuong': m['tinhHuong']} if m.get('tinhHuong') else {}),
            # Cái bẫy của sách đi kèm mẫu câu, chứ không rải đều mọi bước: nói một
            # lần đúng lúc thì bé nhớ, nói lượt nào cũng nói thì thành tiếng ồn.
            **({'bay': bay} if bay else {}),
        })

        # 2 · BÉ NÓI LẠI CẢ CÂU — mỗi câu của sách một bước.
        # Chỉ lấy nửa ĐÁP: nửa hỏi là việc của cô, và bắt bé nhại cả cặp thì bé học
        # thuộc hai vai chứ không học đối đáp.
        khung_dap = tach_doi(m.get('congThuc') or '')[1]
        cau_noi, da_co = [], set()
        for x in tach_lua_chon(dap):
            if x and x not in da_co and cau_lanh_lan(x):
                da_co.add(x)
                cau_noi.append(x)
            elif x and not cau_lanh_lan(x):
                BO_QUA.append(f"{bai['id']}: “{x}”")
        # ⚠ Ô TÊN NGƯỜI THÌ KHÔNG GOM THÊM CÂU CỦA SÁCH.
        #
        # `canonicalExamples` của lớp 1 unit 1 có "Hi, I'm Nam.", "Hi, I'm Linh." —
        # câu đúng của sách, nhưng đem cho bé nhại thì bé đang tự giới thiệu bằng
        # TÊN NGƯỜI KHÁC. Cổng bắt được: `cauHopLe` chỉ nhận tên bé, "Bill" và "Mai"
        # vào ô `[Name]`, nên "Hi, I'm Nam." rơi ra ngoài vốn câu hợp lệ.
        # Ô tên thì đúng một câu mẫu của sách là đủ, phần "nói về mình" đã có bước
        # `thay` lo — nó điền tên THẬT của bé.
        if o_trong(khung_dap) != 'ten':
            for x in vi_du:
                _, nua = tach_doi(x)
                if not nua or not khop_khung(khung_dap, nua):
                    continue
                for y in tach_lua_chon(nua):
                    if not y or y in da_co:
                        continue
                    if not cau_lanh_lan(y):
                        BO_QUA.append(f"{bai['id']}: “{y}” (thiếu dấu cách)")
                        continue
                    # Câu ví dụ dùng chữ NGOÀI vốn của bài thì bỏ — xem `chu_biet`.
                    la = [w for w in chu_trong(y) if w not in biet]
                    if la:
                        BO_QUA.append(f"{bai['id']}: “{y}” (chữ lạ: {', '.join(la)})")
                        continue
                    # ⚠ CÔNG THỨC HAI Ô: chỉ nhận ĐÚNG câu mẫu của sách.
                    #
                    # `cauHopLe` bên `phongnoi.js` công nhận một câu bằng cách DỰNG
                    # LẠI công thức đã điền, mà nó chỉ điền được MỘT ô. Công thức
                    # hai ô thì không cách nào dựng lại → app từ chối, dù phép lọc
                    # theo chữ ở trên đã cho qua.
                    #
                    # Và chỗ ấy app đúng: lớp 2 unit 11 dạy "They + are +
                    # [Verb-ing] + [Noun]." với vốn từ chỉ có slide · ride · drive.
                    # Sách điền máy cả hai ô rồi đẻ ra "They are sliding cars." ·
                    # "They are riding cars." · "They are driving bikes." — ba câu
                    # tiếng Anh KHÔNG AI NÓI. Phép lọc theo chữ không bắt được, vì
                    # từng chữ một đều là chữ bé đã gặp.
                    if len(re.findall(r'\[[^\]]+\]', khung_dap)) > 1:
                        BO_QUA.append(f"{bai['id']}: “{y}” (công thức hai ô, "
                                      f"app không dựng lại được)")
                        continue
                    da_co.add(y)
                    cau_noi.append(y)
        for j, c in enumerate(cau_noi[:NOI_CA_TOI_DA]):
            # Lời Việt ĐỔI THEO TỪNG BƯỚC. Một khuôn dùng lại cho tám bước chính là
            # chỗ bác gọi là "như máy".
            # ⚠ `lam_gi` cũng KHÔNG ghép thẳng vào `vi`, cùng lý do với `tinhHuong`.
            # Sách viết `lam_gi` của lớp 1 unit 11 là "VIỆC đang làm, có đuôi -ing".
            # Trong ngoặc kép của lời Việt thì "-ing" bị đọc là một mẩu TIẾNG ANH, và
            # "ing" không phải chữ nào trong bài — `loiVietHopLe` gạt cả câu. Cổng
            # bắt được thật. Chỉ đặt trong ngoặc thứ CHẮC CHẮN là chữ của sách.
            if j == 0 and cho:
                loi = f'Con nói lại CẢ CÂU nhé, đừng nói mỗi chữ “{cho}”.'
            elif j == 0:
                loi = 'Con nói lại cả câu nhé, đừng nói mỗi một chữ.'
            else:
                loi = ('Vẫn khuôn ấy, đổi chỗ thay được thôi. '
                       'Con nói cả câu cho tròn nhé.')
            buoc.append({
                'loai': 'noiCa', 'en': c, 'mauCau': m['cau'], 'vi': loi,
                # Chỗ thay được và VAI của nó — ngữ cảnh cho mô hình, không phải lời
                # đọc cho bé. Đây mới là thứ đáng dạy ở bước này.
                **({'cho': cho} if cho else {}),
                **({'vaiCho': lam_gi} if lam_gi else {}),
            })

        # 3 · CÔ HỎI THẬT, BÉ TỰ ĐÁP. Chỗ này mới là nói chuyện.
        if hoi and dap:
            buoc.append({
                'loai': 'hoiBe', 'en': hoi, 'mauCau': m['cau'], 'dapMau': dap,
                'vi': ('Cô hỏi thật đấy, con tự đáp nhé. Con đáp theo khuôn: '
                       f'{khung_dap or dap}'),
            })

        # 4 · ĐỔI VAI — bé làm người hỏi.
        if hoi and dap:
            buoc.append({
                'loai': 'doiVai', 'en': hoi, 'mauCau': m['cau'], 'dapMau': dap,
                'vi': (f'Đổi vai nào — lần này CON hỏi cô. Con nói câu hỏi này: '
                       f'“{hoi}” rồi nghe cô đáp nhé.'),
            })

        # 5 · NÓI VỀ CHÍNH MÌNH.
        if not khung_dap or so_o_trong(khung_dap) != 1:
            # ── CHỈ THAY KHI CÔNG THỨC CÓ ĐÚNG MỘT Ô TRỐNG ──
            # Ba bài có công thức HAI ô: `It's a + [Colour] + [Noun].` (U6) và
            # `How many + [Noun-plural]? - [Number].` (U9 · U16). Bản đầu điền cùng
            # một giá trị vào MỌI ô, đẻ ra "It's a bell bell." — cổng bắt được ngay.
            # Điền cho đúng hai ô thì phải biết ô nào nhận màu, ô nào nhận danh từ —
            # mà bài không khai. Đoán ở đây là đoán sai, nên bỏ bước THAY cho mấy
            # bài ấy: `mau` và `noiCa` vẫn còn, bé vẫn được nói cả câu.
            continue
        loai_o = o_trong(khung_dap)
        if loai_o == 'ten':
            buoc.append({'loai': 'thay', 'khung': khung_dap, 'o': 'ten',
                         'en': dien(khung_dap, '{ten}'), 'mauCau': m['cau'],
                         'mac_dinh': ten_trong_vi_du(khung_dap, dap) or 'Bill',
                         'vi': 'Cùng khuôn ấy, nhưng nay là con nói về CHÍNH CON.'})
        elif tu:
            # Giá trị mặc định phải ĐÚNG LOẠI Ô, không phải "từ đầu bài". Không có
            # giá trị nào đúng loại thì BỎ bước THAY — y như cách đã làm với công
            # thức hai ô ở trên: `mau` và `noiCa` vẫn còn, bé vẫn được nói cả câu.
            dien_duoc = [x for x in dien_duoc_vao_o(loai_o, tu) if x]
            if not dien_duoc:
                BO_QUA.append(f"{bai['id']} · ô [{loai_o}] của “{khung_dap}” "
                              'không có từ nào của bài điền được — bỏ bước THAY')
                continue
            buoc.append({'loai': 'thay', 'khung': khung_dap, 'o': 'tu',
                         'en': dien(khung_dap, '{thich}'), 'mauCau': m['cau'],
                         'mac_dinh': dien_duoc[0],
                         'vi': 'Nay con nói về thứ CON thích, không phải của cô nữa.'})

    buoc.append({'loai': 'ket'})
    return {
        'bai': bai['id'],
        'ten': bai.get('title', ''),
        # Bối cảnh của unit — ghép vào lời dặn để cô giáo máy biết buổi này dạy gì.
        # Bác dặn "kịch bản/prompt theo từng Unit mới đảm bảo sát nội dung": câu thì
        # đã sát rồi (lấy của sách), còn cái KHUNG buổi học thì nằm ở đây.
        'muc_tieu': _muc_tieu(bai),
        'tinh_huong': next((m.get('tinhHuong') for m in mau if m.get('tinhHuong')), ''),
        'tu': [t['tu'] for t in tu],
        'buoc': buoc,
    }


def main():
    tep = sorted(NOI_DUNG.glob(TIEN_TO_BAI))
    if not tep:
        sys.exit(f'không thấy bài học nào ở {NOI_DUNG}')

    cu = {}
    if RA_PUBLIC.exists():
        cu = {k['bai']: k for k in json.loads(RA_PUBLIC.read_text('utf-8'))}

    ra, giu_tay = [], []
    for f in tep:
        bai = json.loads(f.read_text('utf-8'))
        # Kịch bản đã sửa tay thì GIỮ NGUYÊN — sinh lại mà đè lên là mất công người sửa.
        if cu.get(bai['id'], {}).get('tay'):
            ra.append(cu[bai['id']])
            giu_tay.append(bai['id'])
        else:
            ra.append(kich_ban_cua(bai))

    for p in (RA_PUBLIC, RA_DATA):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(ra, ensure_ascii=False, indent=1) + '\n', 'utf-8')

    dem = {}
    for k in ra:
        for b in k['buoc']:
            dem[b['loai']] = dem.get(b['loai'], 0) + 1
    tong = sum(len(k['buoc']) for k in ra)
    print(f'{len(ra)} kịch bản · {tong} bước · trung bình {tong / len(ra):.1f} bước một bài')
    print('  ' + ' · '.join(f'{k} {v}' for k, v in sorted(dem.items())))
    cau = sum(dem.get(x, 0) for x in ('mau', 'noiCa', 'hoiBe', 'doiVai', 'thay'))
    print(f'  bước dạy CÂU: {cau} · bước từ rời (chỉ dùng khi bé đuối): {dem.get("tu", 0)}')
    if BO_QUA:
        print(f'  ⚠ bỏ {len(BO_QUA)} câu ví dụ vì NGUỒN hỏng — sửa tận gốc thì cả '
              'bài học được nhờ, không riêng phòng nói:')
        for x in dict.fromkeys(BO_QUA):
            print('     ', x)
    if giu_tay:
        print('giữ nguyên bản sửa tay:', ', '.join(giu_tay))
    print('ghi:', RA_PUBLIC.relative_to(GOC), 'và', RA_DATA.relative_to(GOC))


if __name__ == '__main__':
    main()
