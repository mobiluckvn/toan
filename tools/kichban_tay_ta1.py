#!/usr/bin/env python3
"""BA KỊCH BẢN VIẾT TAY — U6 · U9 · U16.

    python3 tools/kichban_tay_ta1.py

── VÌ SAO BA BÀI NÀY PHẢI VIẾT TAY ──
`sinh_kichban_noi.py` bỏ hẳn bước "thay" của ba bài, và bỏ có lý: công thức của
chúng có HAI ô trống —

    U6      It's a + [Colour] + [Noun].
    U9      How many + [Noun-plural]? - [Number].
    U16     How many + [Noun-plural] + can you see? - I can see + [Number].

— mà bài thì không khai ô nào nhận màu, ô nào nhận danh từ, ô nào nhận số. Bản
đầu điền cùng một giá trị vào MỌI ô, đẻ ra "It's a bell bell.". Đoán ở đó là đoán
sai, nên thà bỏ bước còn hơn dạy bé một câu hỏng.

Hậu quả: ba bài chỉ còn đúng một hai câu để luyện, lặp đi lặp lại cả buổi.

── VIẾT TAY, NHƯNG KHÔNG BỊA MỘT CHỮ NÀO ──
Mọi câu tiếng Anh dưới đây lấy nguyên từ `canonicalExamples` của chính bài — sách
đã tự điền sẵn cả hai ô rồi, chỉ là trước nay mình không đọc tới. Phần viết tay
thật sự là LỜI TIẾNG VIỆT: mỗi bài có một chỗ khó riêng, và câu chung chung
"Con nghe rồi nói lại cả câu này nhé" không chỉ ra được chỗ ấy.

    U6   màu đứng TRƯỚC đồ vật — ngược với tiếng Việt ("bút đỏ")
    U9   hỏi bằng "How many", đáp chỉ cần MỘT con số
    U16  thêm "can you see" để hỏi người kia NHÌN THẤY

Ba chỗ ấy chính là `misconceptions` và `hoiThoai` sách đã ghi.

── CHẠY LẠI THÌ SAO ──
Đặt cờ `tay: true`, nên `sinh_kichban_noi.py` chạy lần sau sẽ GIỮ NGUYÊN chứ
không đè lên. Muốn quay về bản sinh tự động thì xoá cờ ấy đi.

Cổng `test/tienganh_phongnoi.test.mjs` soi lại từng câu: mọi câu tiếng Anh phải
nằm trong `vonCuaBai(bai).cauSach` — tức là câu của chính sách, đã lọc theo từ.
Gõ nhầm một chữ là đỏ ngay.
"""
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
RA_PUBLIC = GOC / 'web' / 'public' / 'content' / 'ta1' / 'kichban_noi.json'
RA_DATA = GOC / 'data' / 'tienganh' / 'kichban_noi.json'

CHAO = {'loai': 'chao', 'en': 'Hello!', 'vi': 'Chào con! Hôm nay mình tập nói nhé.'}


def tu_buoc(bai_json, nghia_rieng=None):
    """Bước đọc từng từ — giữ đúng như bản sinh tự động, không việc gì phải khác."""
    ra = []
    for t in bai_json['knowledgeCore'].get('vocabulary', []):
        vi = (nghia_rieng or {}).get(
            t['tu'], f"Con nghe rồi nói lại từ này nhé — nghĩa là {t['nghia']}.")
        ra.append({'loai': 'tu', 'en': t['tu'], 'tu': t['tu'], 'vi': vi})
    return ra


def kich_ban(bai_json, giua):
    return [CHAO, {'loai': 'hoiThich'}] + tu_buoc(bai_json) + giua + [{'loai': 'ket'}]


# ── U6 · Trong lớp học ─────────────────────────────────────────────────────
# Chỗ khó: màu đứng TRƯỚC đồ vật. Tiếng Việt nói "bút đỏ", tiếng Anh nói ngược
# lại — sách ghi thẳng vào `misconceptions`. Nên lời Việt của bước đầu chỉ ra
# đúng chỗ ấy, rồi hai bước sau mới đổi đồ vật để bé thấy MÀU đứng yên một chỗ.
GIUA_B06 = [
    {'loai': 'mau', 'en': "It's a red pen.",
     'vi': 'Nghe kỹ thứ tự nhé: màu đứng TRƯỚC đồ vật. Mình nói "đỏ" rồi mới nói "bút".'},
    {'loai': 'thay', 'khung': "It's a + [Colour] + [Noun].", 'o': 'nhieu',
     'dien': ['red', 'bell'], 'en': "It's a red bell.",
     'vi': 'Vẫn màu đỏ ấy, nay đổi sang cái chuông. Con để ý màu vẫn đứng trước nhé.'},
    {'loai': 'thay', 'khung': "It's a + [Colour] + [Noun].", 'o': 'nhieu',
     'dien': ['red', 'pencil'], 'en': "It's a red pencil.",
     'vi': 'Lần này là cái bút chì. Con nói cả câu nhé.'},
]

# ── U9 · Trong cửa hàng ────────────────────────────────────────────────────
# Chỗ khó: đây là MỘT LƯỢT HỎI và MỘT LƯỢT ĐÁP, không phải một câu dài. Sách
# cũng tách đôi như thế trong `hoiThoai`. Bé phải tập cả hai vai: hỏi thì mở đầu
# bằng "How many", đáp thì chỉ cần đúng một con số — không phải cả câu.
GIUA_B09 = [
    {'loai': 'mau', 'en': 'How many clocks?',
     'vi': 'Muốn hỏi có mấy cái thì mở đầu bằng "How many" nhé.'},
    {'loai': 'mau', 'en': 'Two.',
     'vi': 'Đến lượt con đáp. Đáp thì chỉ cần nói MỘT con số thôi, không phải cả câu.'},
    {'loai': 'thay', 'khung': 'How many + [Noun-plural]?', 'o': 'nhieu',
     'dien': ['locks'], 'en': 'How many locks?',
     'vi': 'Nay con hỏi về ổ khoá nhé — vẫn mở đầu bằng "How many".'},
    {'loai': 'thay', 'khung': '[Number].', 'o': 'nhieu',
     'dien': ['One'], 'en': 'One.',
     'vi': 'Lần này con đếm được một cái thôi. Con đáp đi.'},
    {'loai': 'thay', 'khung': 'How many + [Noun-plural]?', 'o': 'nhieu',
     'dien': ['mops'], 'en': 'How many mops?',
     'vi': 'Con hỏi về cây lau nhà nhé.'},
]

# ── U16 · Ở nhà ────────────────────────────────────────────────────────────
# Chỗ khó: "can you see" — hỏi người KIA nhìn thấy mấy cái, nên đáp cũng phải
# "I can see…" chứ không phải nói trống một con số như Unit 9. Hai bài trông
# giống nhau mà đáp khác nhau, nên lời Việt phải nói rõ chỗ khác ấy.
GIUA_B16 = [
    {'loai': 'mau', 'en': 'How many windows can you see?',
     'vi': 'Thêm "can you see" là hỏi người kia NHÌN THẤY mấy cái nhé.'},
    {'loai': 'mau', 'en': 'I can see six.',
     'vi': 'Bài này đáp phải nói cả "I can see" rồi mới tới con số — khác bài đếm ở cửa hàng.'},
    {'loai': 'thay', 'khung': 'I can see + [Number].', 'o': 'nhieu',
     'dien': ['one'], 'en': 'I can see one.',
     'vi': 'Nay con chỉ nhìn thấy một cái thôi.'},
    {'loai': 'thay', 'khung': 'I can see + [Number].', 'o': 'nhieu',
     'dien': ['two'], 'en': 'I can see two.',
     'vi': 'Hai cái thì con nói thế nào?'},
    {'loai': 'thay', 'khung': 'I can see + [Number].', 'o': 'nhieu',
     'dien': ['three'], 'en': 'I can see three.',
     'vi': 'Ba cái nhé. Con nói cả câu.'},
]

TAY = {
    'DL:TA1.B06': GIUA_B06,
    'DL:TA1.B09': GIUA_B09,
    'DL:TA1.B16': GIUA_B16,
}


def main():
    ds = json.loads(RA_PUBLIC.read_text('utf-8'))
    noi_dung = RA_PUBLIC.parent

    for k in ds:
        if k['bai'] not in TAY:
            continue
        tep = noi_dung / (k['bai'].replace('DL:', 'DL_').replace('.', '_') + '.json')
        bai = json.loads(tep.read_text('utf-8'))
        k['buoc'] = kich_ban(bai, TAY[k['bai']])
        k['tay'] = True
        print(f"{k['bai']} · {len(k['buoc'])} bước · "
              f"{sum(1 for b in k['buoc'] if b['loai'] in ('mau', 'thay'))} câu")

    thieu = [b for b in TAY if b not in {k['bai'] for k in ds}]
    if thieu:
        sys.exit(f'không thấy bài {thieu} trong kịch bản')

    for p in (RA_PUBLIC, RA_DATA):
        p.write_text(json.dumps(ds, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    print('ghi:', RA_PUBLIC.relative_to(GOC), 'và', RA_DATA.relative_to(GOC))


if __name__ == '__main__':
    main()
