#!/usr/bin/env python3
"""BẢNG ĐỀ XUẤT 42 BÀI TẢ TRANH (lớp 3 · lớp 4) → Excel để bác duyệt.

    tools/tts/.venv/bin/python tools/canh_de_xuat.py

── BA LẦN BÁC BẮT, ĐÂY LÀ BẢN THỨ TƯ ──

1. *"Chủ đề bài là Hello Again thì bạn nên vẽ một bối cảnh có người chào nhau."*
   → Tranh cũ là DÃY KỆ ĐỰNG ĐỒ RỜI nên đoạn văn buộc thành bảng liệt kê. Bác còn
   chỉ ra cái sai sâu hơn: làm mẫu một bài thì tốt, rồi tôi viết bộ nhân bản 20 bài
   còn lại — mà bộ ấy chỉ biết xoay bốn khuôn `This is a … / I can see a …`.

2. *"Bạn quá tham lam khi nhồi nhét quá nhiều thứ… Cần gì số làm gì nữa."*
   → Tôi tự đặt một luật SAI: ép mỗi bức dùng ĐỦ MỌI mẫu câu unit dạy.

3. *"Toàn bộ nội dung sẽ KHÔNG DÙNG HỘI THOẠI. Đều là các đoạn văn mô tả… dùng từ
   lớp 1 tích luỹ đến bài đó. Thêm một cột mô tả về bức tranh sẽ vẽ. Sau khi có mô
   tả thì mới xây dựng câu hỏi dựa vào mô tả đó. Phần nói và viết cũng dựa trên
   phần mô tả. Mô tả phải chi tiết nhất có thể để AI gen được ảnh."*

── THỨ TỰ LÀM, VÀ ĐÂY LÀ CHỖ TRƯỚC ĐÂY TÔI LÀM NGƯỢC ──

    ① MÔ TẢ TRANH (chi tiết, để AI vẽ)
         ↓ mọi thứ dưới đây SUY TỪ mô tả ấy, không suy từ bảng từ vựng
    ② ĐOẠN ĐỌC   — văn mô tả, KHÔNG hội thoại
    ③ CÂU HỎI    — hỏi về thứ CÓ TRONG mô tả
    ④ NÓI · VIẾT — cùng dựa trên mô tả

Trước đây tôi đi từ bảng từ vựng ra tranh, nên tranh là cái kệ đựng từ.

── LUẬT ──
1. KHÔNG HỘI THOẠI. Không có cặp `Hỏi? - Đáp.` trong đoạn đọc. Chỉ câu kể.
   (Mẫu câu hỏi của unit vẫn dùng — nhưng ở CÂU HỎI SAU BÀI và ở phòng nói.)
2. VỐN TÍCH LUỸ TỪ LỚP 1 tới đúng bài ấy, không bó trong từ của riêng unit.
3. MỘT NƠI, MỘT LÚC · nhiều nhất 2–3 người · đồ vật phải thuộc về chỗ ấy.
4. KHÔNG NHÂN BẢN. 42 cảnh viết tay. Bộ sinh chỉ SOI, không quyết nội dung.

⚠ Tệp này CHỈ đẻ ra bảng đề xuất để duyệt. Nó không sửa nội dung đang chạy.
"""
from __future__ import annotations

import json
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs/canh_de_xuat.xlsx"

KIEU = ("Tranh minh hoạ cho trẻ tiểu học: màu phẳng, nét viền đậm, nền sáng, "
        "không đổ bóng cầu kì, KHÔNG có chữ nào trong tranh. ")


def C(noi, mo_ta, doan, hoi, goi_y, ghi=""):
    return {"noi": noi, "mo_ta": KIEU + mo_ta, "doan": doan,
            "hoi": hoi, "goi_y": goi_y, "ghi": ghi}


def tu_viet(doan: str) -> str:
    """Bảng từ gợi ý cho màn VIẾT — suy thẳng từ đoạn, nên không bao giờ thiếu.

    ⚠ Lớp 3 từng đoán chừng bảy chữ nối và thiếu `That's`; bé bấm hết bảng vẫn
    không viết nổi câu trong đoạn.
    """
    ra, thay = [], []
    for w in doan.replace("!", ".").replace("?", ".").split():
        w = w.strip(".,")
        if w and w not in ra:
            ra.append(w)
    return " · ".join(ra)


# ══════════════════════════════ LỚP 3 ══════════════════════════════
L3 = {
0: C("Trong lớp học",
     "Một phòng học nhìn thẳng từ cuối lớp. BÊN TRÁI: cô giáo khoảng ba mươi tuổi, "
     "tóc buộc sau, áo sơ mi xanh, đứng cạnh tấm bảng đen treo tường, tay cầm viên "
     "phấn, mặt tươi. Mặt bảng ĐỂ TRỐNG. GIỮA và TIỀN CẢNH: hai bộ bàn học gỗ vàng "
     "nhạt xếp trước sau, mỗi bàn một ghế; bàn trước có một bạn trai tóc đen ngồi, "
     "bàn sau một bạn gái tóc tết hai bên, cả hai quay mặt về phía cô. Trên mỗi bàn "
     "một quyển vở mở. Dưới chân bàn trước có một chiếc cặp màu đỏ. BÊN PHẢI: một "
     "cửa sổ nhìn ra tán cây xanh.",
     "This is my teacher. That's my friend. There's a desk. "
     "I can see a book. The bag is red.",
     "1. What can you see? → I can see a book.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. What's this? | Hai bạn nhỏ đang ngồi ở cái gì? → It's a desk.  (mồi: It's a pen. · It's a cat. · It's a kite.)",
     "Where are you? · What can you see? · What's this?",
     "Bác chốt: cảnh trong lớp thì CHỈ có lớp. Bỏ thẻ số và con diều của bản trước.\n"
     "⚠ 29-08-2026: mồi câu 2 vốn là `It's a book.` và `It's a bag.` — mà tranh có "
     "CẢ quyển sách LẪN chiếc cặp, nên câu ấy có ba đáp án đúng. Mồi nay là thứ "
     "KHÔNG có trong tranh."),
1: C("Ở cổng trường buổi sáng",
     "Cổng trường xây gạch vàng, cánh cổng sắt mở. GIỮA TRANH: hai bạn nhỏ đứng đối "
     "diện nhau, cùng giơ tay vẫy chào. BÊN TRÁI là bạn trai tóc ngắn, áo sơ mi "
     "trắng, đeo cặp xanh sau lưng. BÊN PHẢI là bạn gái tóc dài buộc nơ, váy hồng, "
     "đeo cặp vàng. Cả hai cười. HẬU CẢNH: một cây bàng lớn bên trái cổng, dãy nhà "
     "học màu vàng nhạt phía sau, bầu trời xanh có mấy đám mây trắng.",
     "This is Ben. This is Lucy. Ben is my friend. Lucy is my friend. "
     "I can see two bikes.",
     "1. What can you see? → I can see two bikes.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. How many bikes can you see? → I can see two.  (mồi: I can see one. · I can see three. · I can see four.)",
     "Where are they? · What can you see? · How many bikes can you see?"),
2: C("Ở bàn học, hai bạn mới làm quen",
     "Cận cảnh một bộ bàn học gỗ nhìn từ phía trước. Hai bạn nhỏ ngồi cạnh nhau, "
     "cùng quay mặt ra ngoài. BÊN TRÁI: bạn gái tóc nâu ngang vai, áo vàng. BÊN "
     "PHẢI: bạn trai tóc đen, áo xanh. Trước mặt mỗi bạn có một tấm bảng tên bằng "
     "bìa gấp đôi đặt đứng trên bàn — bảng bên trái để trống, bảng bên phải để "
     "trống (KHÔNG viết chữ). Trên bàn còn một cây bút chì và một quyển vở mở. "
     "HẬU CẢNH: tường lớp màu kem, một phần bảng đen.",
     "This is Mary. This is Minh. She's eight years old. He's eight years old. "
     "I can see a book.",
     "1. What can you see? → I can see a book.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. How old is Mary? → She's eight years old.  (mồi: She's six years old. · She's seven years old. · She's nine years old.)",
     "What can you see? · How old is Mary? · What's this?",
     "Bác gợi ý đúng kiểu này: hai người có TÊN ở đó, rồi tả họ."),
3: C("Ở sân trường, một bạn giới thiệu cô giáo",
     "Sân trường lát gạch đỏ. BÊN TRÁI: một bạn trai tóc đen áo trắng đứng, tay "
     "phải chỉ sang phải. GIỮA: cô giáo tóc búi, áo dài xanh nhạt, đứng cười, hai "
     "tay chắp trước. BÊN PHẢI: một thầy giáo tóc ngắn, áo sơ mi trắng, quần âu, "
     "đứng hơi lùi phía sau. HẬU CẢNH: một ghế đá màu xám dưới tán cây bàng, dãy "
     "lớp học màu vàng, bầu trời xanh.",
     "This is Ms Hoa. Ms Hoa is my teacher. That's Minh. Minh is my friend. "
     "I can see a garden. I can see a bag.",
     "1. What can you see? → I can see a garden.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. What's this? → It's a bag.  (mồi: It's a book. · It's a pen. · It's a desk.)",
     "What can you see? · What's this?"),
4: C("Trước tấm gương trong lớp",
     "Cận cảnh nửa người một bạn gái khoảng tám tuổi đứng trước tấm gương chữ nhật "
     "treo tường, khung gỗ nâu. Khuôn mặt bạn ấy chiếm phần lớn tranh, nhìn thẳng, "
     "thấy rõ hai mắt, cái mũi, cái miệng đang cười, hai tai và mái tóc đen ngang "
     "vai. Bạn ấy đưa ngón tay trỏ chạm nhẹ vào chóp mũi mình. BÊN PHẢI, hơi lùi "
     "phía sau: cô giáo áo xanh đứng nhìn, tay chỉ về phía khuôn mặt bạn nhỏ. "
     "HẬU CẢNH: tường lớp màu kem.",
     "This is my face. This is my hair. That's my mouth. "
     "I can see an eye. My hair is black.",
     "1. What's this? | Chỗ đang cười trên khuôn mặt là chỗ nào? → It's a mouth.  (mồi: It's a nose. · It's an ear. · It's a bag.)\n"
     "2. What's this? | Hai chấm tròn màu đen trên khuôn mặt là gì? → It's an eye.  (mồi: It's a nose. · It's an ear. · It's a book.)",
     "What's this? · Touch your face! · What can you see?",
     "Bức cũ vẽ mắt-mũi-mồm RỜI trên kệ. Nay là MỘT khuôn mặt để cô chỉ vào.\n"
     "⚠ 29-08-2026, SỬA THEO BỨC TRANH ĐANG CHẠY. Bút `nguoi` vẽ khuôn mặt gồm "
     "TÓC · HAI MẮT · MIỆNG — không vẽ mũi, không vẽ tai. Nên đoạn cũ nói `This "
     "is my nose.` là tả một thứ không có trên tranh, và hai câu hỏi cũ (đáp "
     "`nose` rồi `eye`) lấy mồi toàn bộ phận CÓ THẬT trên mặt → câu nào cũng ba "
     "đáp án đúng. Nay đoạn chỉ nói thứ vẽ ra được, mồi `nose` · `ear` là thứ "
     "tranh KHÔNG vẽ."),
5: C("Ở góc sinh hoạt của lớp",
     "Một góc phòng sinh hoạt, sàn gỗ. BÊN TRÁI: một bạn gái tóc tết, tạp dề đỏ, "
     "đứng trước bộ bếp đồ chơi bằng nhựa, tay cầm cái thìa gỗ khuấy trong nồi. "
     "BÊN PHẢI: một bạn gái tóc ngắn, váy tím, đang nhảy múa, hai tay giơ lên, một "
     "chân nhấc khỏi sàn. GIỮA, phía sau: một cái bàn thấp có đặt cái đài nhỏ. "
     "HẬU CẢNH: tường màu kem, một bức tranh treo tường.",
     "This is my school. She's cooking. She's dancing. "
     "I like cooking. I can see a table.",
     "1. What's she doing? | Bạn đội mũ đầu bếp đang làm gì? → She's cooking.  (mồi: She's singing. · She's running. · She's walking.)\n"
     "2. What's she doing? | Bạn mặc váy tím đang làm gì? → She's dancing.  (mồi: She's swimming. · She's painting. · She's drawing.)",
     "What's she doing? · What's your hobby?",
     "⚠ 29-08-2026: tranh có HAI bạn gái, một nấu một múa — hỏi trống không "
     "`What's she doing?` thì cả `She's cooking.` lẫn `She's dancing.` đều đúng, "
     "mà hai câu hỏi lại lấy nhau làm mồi. Nay chốt bằng dòng phụ (mũ đầu bếp / "
     "váy tím) VÀ mồi đổi sang việc tranh không vẽ — sai cả hai đường."),
6: C("Ở hành lang trường, trước cửa các phòng",
     "Hành lang trường nhìn dọc, sàn gạch xám, lan can bên phải. BÊN TRÁI có ba cánh "
     "cửa gỗ liền nhau, mỗi cửa một tấm biển hình chữ nhật treo trên (biển ĐỂ TRỐNG, "
     "không chữ): cửa gần nhất hé mở nhìn thấy bàn ghế bên trong, cửa thứ hai đóng, "
     "cửa thứ ba mở nhìn thấy giá sách. GIỮA HÀNH LANG: hai bạn nhỏ đứng cạnh nhau, "
     "bạn trai áo trắng chỉ tay vào cánh cửa gần nhất, bạn gái áo hồng nhìn theo. "
     "HẬU CẢNH: cuối hành lang có cửa sổ sáng.",
     "This is our school. That's our classroom. There's a library. "
     "I can see a door. I like my school.",
     "1. What's this? | Bạn trai đang chỉ tay vào phòng nào? → It's our classroom.  (mồi: It's our gym. · It's our playground. · It's our music room.)\n"
     "2. What can you see? → I can see a door.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "What's this? · What can you see?",
     "⚠ 29-08-2026, hai chỗ. (a) Đoạn cũ viết `I can see a gym.` và câu 2 lấy "
     "chính câu ấy làm đáp án — mà trên tranh KHÔNG có phòng thể chất nào, chỉ có "
     "ba cánh cửa với một cửa sổ. Bé nhìn tranh thì không có gì để thấy. Nay đáp "
     "là `a door`, thứ vẽ rõ ba cái. (b) Mồi `It's our library.` của câu 1 lại "
     "ĐÚNG — cửa thứ ba mở ra giá sách, và chính đoạn cũng nói `There's a "
     "library.`"),
7: C("Ở cửa lớp, một bạn đến muộn",
     "Nhìn từ trong lớp ra phía cửa. BÊN PHẢI: cánh cửa gỗ mở, một bạn trai tóc đen "
     "đeo cặp xanh đứng ở ngưỡng cửa, tay phải giơ lên ngang vai xin phép, mặt hơi "
     "ngượng. GIỮA: cô giáo áo xanh đứng quay về phía cửa, một tay đưa ra mời vào. "
     "BÊN TRÁI và TIỀN CẢNH: hai bộ bàn học có hai bạn đang ngồi quay lưng lại phía "
     "người xem, nhìn về phía cửa. HẬU CẢNH: bảng đen để trống.",
     "This is my classroom. This is my teacher. There's a door. "
     "I can see a desk. I like my teacher.",
     "1. What can you see? → I can see a desk.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. What's this? | Bạn trai đến muộn đang đứng ở chỗ nào? → It's a door.  (mồi: It's a book. · It's a pen. · It's a kite.)",
     "What can you see? · What's this?",
     "⚠ 29-08-2026: mồi cũ `It's a desk.` và `It's a bag.` đều CÓ trên tranh — "
     "chính câu 1 đã lấy cái bàn làm đáp án. Ba đáp án đúng trong một câu."),
8: C("Trên mặt bàn học của bạn nhỏ",
     "Nhìn chếch từ trên xuống một mặt bàn học gỗ sáng màu. Trên bàn bày rõ ràng, "
     "tách rời nhau: một cây bút bi xanh nằm ngang phía trên, một cây thước kẻ nhựa "
     "trong nằm chéo bên phải, một cục tẩy trắng-xanh ở giữa, một hộp bút vải màu "
     "xanh dương mở nắp phía dưới bên trái, một quyển vở mở ở góc trên bên phải. "
     "BÊN TRÁI MÉP TRANH: bàn tay một bạn nhỏ đang cầm cây bút giơ lên.",
     "This is my desk. I have a pen. There's a ruler. "
     "I can see an eraser. That's my pencil case.",
     "1. What can you see? → I can see an eraser.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. What's this? | Cái nằm chéo bên phải, có vạch chia, là cái gì? → It's a ruler.  (mồi: It's a bag. · It's a kite. · It's a cat.)",
     "What do you have? · What can you see?",
     "⚠ 29-08-2026: bỏ câu `What do you have? → I have a pen.` Cả BỐN lựa chọn "
     "(pen · ruler · book · eraser) đều nằm rõ trên mặt bàn, mà tranh không có ai "
     "CẦM thứ gì để chốt lại — bé trả lời cái nào cũng đúng với bức tranh."),
9: C("Ở góc mĩ thuật",
     "Một góc lớp mĩ thuật, bàn gỗ dài. TRÊN BÀN bày một mẫu vẽ tĩnh vật: một quả "
     "táo ĐỎ bên trái, một chiếc lá XANH LÁ ở giữa, một cái thùng các-tông NÂU bên "
     "phải. PHÍA SAU BÀN: một bạn gái tóc tết, áo trắng, đứng cười. HẬU CẢNH: tường "
     "treo một bảng màu tròn có các ô màu đỏ, xanh, vàng, xanh lá.",
     "This is an apple. It's red. I can see a leaf. It's green. "
     "There's a box.",
     "1. What colour is the apple? | Quả táo (apple) màu gì? → It's red.  (mồi: It's green. · It's brown. · It's blue.)\n"
     "2. What colour is the leaf? | Chiếc lá (leaf) màu gì? → It's green.  (mồi: It's red. · It's brown. · It's white.)",
     "What colour is the apple? · What colour is the leaf? · What can you see?",
     "⚠ 29-08-2026, DỰNG LẠI CẢ BỨC. Bức cũ bày `ball` · `pen` · `book` rồi hỏi "
     "màu của chúng — nhưng hình thật thì quả bóng NỬA ĐỎ NỬA VÀNG, cây bút 🖊️ "
     "màu ĐEN, quyển sách 📖 màu XANH-TRẮNG. Nghĩa là đáp án `It's blue.` cho cây "
     "bút KHÔNG có lấy một đáp án đúng nào theo tranh, chứ không phải hai.\n"
     "Nay theo đúng luật `MAU_CUA` trong docs/lam_bai_tranh.md: chỉ dùng hình MỘT "
     "MÀU, gọi tên không cãi được — táo 🍎 đỏ, lá 🍃 xanh lá, thùng 📦 nâu. Và chỉ "
     "HAI câu màu, vì cổng chặn quá 2 dòng cùng khuôn `It's + [màu].`"),
10: C("Ở sân trường giờ ra chơi",
     "Sân trường rộng lát gạch đỏ, nhìn từ xa hơi chếch. BÊN TRÁI: hai bạn trai "
     "đang đá một quả bóng đá đen-trắng, một bạn vừa sút, một bạn giơ tay. BÊN "
     "PHẢI: hai bạn gái đứng đối diện nhau, mỗi bạn cầm một cây vợt cầu lông, một "
     "quả cầu trắng bay giữa hai bạn. GIỮA phía sau: một ghế đá xám. HẬU CẢNH: dãy "
     "lớp học màu vàng, hai cây xanh, bầu trời xanh.",
     "This is our playground. I play football at break time. "
     "I can see a football. That's my friend. I like my playground.",
     "1. What do you do at break time? → I play football.  (mồi: I play badminton. · I play chess. · I play basketball.)\n"
     "2. What can you see? → I can see a football.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · What do you do at break time? · What can you see?"),
11: C("Trong phòng khách, cả nhà xem ảnh",
     "Một phòng khách ấm cúng. GIỮA TƯỜNG: một khung ảnh gia đình lớn treo cao, "
     "trong ảnh có bốn người vẽ đơn giản — bố, mẹ, một bạn gái lớn, một bạn trai "
     "nhỏ. TIỀN CẢNH BÊN TRÁI: một bạn trai khoảng tám tuổi đứng, tay chỉ lên khung "
     "ảnh. BÊN PHẢI: mẹ tóc búi, áo hồng, ngồi trên ghế sofa xám nhìn theo tay con. "
     "GIỮA: một cái bàn thấp có lọ hoa. HẬU CẢNH: một cây đèn đứng bên phải.",
     "This is my sister. That's my mother. There's my father. "
     "I can see my brother. I like my sister.",
     "1. Who's this? | Người đang ngồi trên ghế sofa là ai? → It's my mother.  (mồi: It's my sister. · It's my brother. · It's my father.)\n"
     "2. What can you see? → I can see my brother.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Who's this? · What can you see?",
     "⚠ 29-08-2026: `Who's this?` hỏi trống không giữa một bức có ĐỦ bốn người "
     "trong khung ảnh — bố, mẹ, chị, em đều đúng. Nay chốt vào người NGỒI TRÊN "
     "SOFA: chỉ mẹ ngồi đó, ba người kia chỉ có trong ảnh treo tường."),
12: C("Ở ngày hội nghề nghiệp của trường",
     "Một góc sân trường có hai gian nhỏ dựng bằng khung gỗ. GIAN BÊN TRÁI: một cô "
     "mặc áo blouse trắng, ống nghe đeo quanh cổ, đứng cười, tay cầm cái cặp nhiệt "
     "kế. GIAN BÊN PHẢI: một bác nông dân đội nón lá, áo nâu, tay cầm bó lúa vàng. "
     "TIỀN CẢNH: một bạn nhỏ đứng quay lưng lại người xem, nhìn về phía hai gian. "
     "HẬU CẢNH: dãy lớp học màu vàng, bầu trời xanh.",
     "This is a doctor. She's a doctor. That's a farmer. He's a farmer. "
     "I can see a garden.",
     "1. What's her job? → She's a doctor.  (mồi: She's a nurse. · She's a farmer. · She's a teacher.)\n"
     "2. What can you see? → I can see a garden.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "What's her job? · Is he a farmer? · What can you see?"),
13: C("Nhìn vào trong ngôi nhà, thấy các phòng",
     "Mặt cắt một ngôi nhà hai tầng nhìn thẳng, như ngôi nhà búp bê mở ra: bốn ô "
     "phòng vuông vắn. TẦNG TRÊN BÊN TRÁI: phòng ngủ có giường phủ chăn xanh và cửa "
     "sổ. TẦNG TRÊN BÊN PHẢI: phòng tắm có bồn tắm trắng. TẦNG DƯỚI BÊN TRÁI: phòng "
     "khách có ghế sofa và hai cái ghế gỗ. TẦNG DƯỚI BÊN PHẢI: nhà bếp có bếp và "
     "cái nồi. TIỀN CẢNH: một bạn trai đứng ở cửa chính, tay chỉ lên phòng ngủ.",
     "This is my house. That's my bedroom. There's a kitchen. "
     "The chairs are in the living room. I can see a bed.",
     "1. What's this? | Căn phòng ở góc TRÊN BÊN TRÁI là phòng gì? → It's my bedroom.  (mồi: It's my kitchen. · It's my bathroom. · It's my classroom.)\n"
     "2. Where's the bed? → It's in the bedroom.  (mồi: It's in the kitchen. · It's in the bathroom. · It's in the living room.)",
     "What's this? · Where are the chairs?",
     "⚠ 29-08-2026: bức này vẽ BỐN phòng cùng lúc, nên `What's this?` trống "
     "không thì `It's my kitchen.` (phòng dưới bên phải) và `It's my house.` (cả "
     "bức) đều đúng ngang với đáp án. Nay chốt bằng VỊ TRÍ ô phòng — chốt bằng "
     "chỗ đứng chứ không bằng đồ trong phòng, vì `giường → bedroom` là cho sẵn "
     "đáp án."),
14: C("Trong phòng ngủ của bạn nhỏ",
     "Một phòng ngủ trẻ em nhìn thẳng. GIỮA: một cái giường gỗ, chăn màu xanh nhạt "
     "gấp gọn, một cái gối trắng. BÊN TRÁI: một cửa sổ vuông có rèm vàng, nhìn ra "
     "bầu trời xanh. BÊN PHẢI: một bàn học nhỏ, trên bàn có cây đèn bàn màu cam "
     "đang sáng. TIỀN CẢNH BÊN PHẢI: một cánh cửa gỗ lớn màu nâu đang mở. GIỮA "
     "PHÒNG: một bạn gái tóc tết đứng, hai tay dang nhẹ như đang giới thiệu phòng.",
     "This is my bedroom. There's a bed in the room. I can see a window. "
     "That's my lamp. The door is big.",
     "1. What's in the room? → There's a bed in the room.  (mồi: There's a dog in the room. · There's a cat in the room. · There's a chair in the room.)\n"
     "2. Is the door big? → The door is big.  (mồi: The door is small. · The door is red. · The door is blue.)",
     "What's in the room? · Is the door big?",
     "⚠ 29-08-2026, hai chỗ. (a) Mồi `There's a desk in the room.` và `There's a "
     "table in the room.` — phòng ngủ này CÓ một cái bàn, bút `ban` vẽ ra cả "
     "`desk` lẫn `table`. (b) Câu 2 hỏi về CÁNH CỬA mà mồi lại nói về cửa sổ và "
     "cái giường; cả hai đều to thật, nên bé đọc kỹ vẫn phân vân. Nay bốn lựa "
     "chọn cùng nói về cánh cửa, và cửa vẽ màu NÂU nên đỏ · xanh đều sai."),
15: C("Ở bàn ăn, mẹ mời khách",
     "Một bàn ăn gỗ hình chữ nhật nhìn chếch từ trên. TRÊN BÀN: một đĩa bánh mì "
     "vàng ở giữa, một bát cơm trắng bên trái, hai cốc sữa trắng ở hai đầu bàn, một "
     "ấm trà sứ trắng bên phải. PHÍA SAU BÀN: mẹ tóc búi, tạp dề vàng, đang đưa "
     "đĩa bánh mì về phía trước. HAI BÊN BÀN: hai bạn nhỏ ngồi trên ghế gỗ, cùng "
     "nhìn vào đĩa bánh. HẬU CẢNH: tường bếp màu kem, một cái tủ nhỏ.",
     "This is my mother. That's a table. There's some rice. "
     "I want some milk. I can see some bread.",
     "1. What can you see? → I can see some bread.  (mồi: I can see some fish. · I can see some meat. · I can see some water.)\n"
     "2. What's this? | Cái mà cả nhà đang ngồi quanh là cái gì? → It's a table.  (mồi: It's a bag. · It's a pen. · It's a bed.)",
     "What can you see? · Would you like some bread? · What's this?",
     "⚠ 29-08-2026: mồi cũ `some rice` và `some milk` — trên bàn có SẴN bát cơm "
     "và hai cốc sữa, chính đoạn cũng nói `There's some rice. I want some milk.` "
     "Ba đáp án đúng. Mồi mới là món tranh không bày. Câu 2 bỏ mồi `It's a "
     "book.`: góc phải bức có một cái giá sách."),
16: C("Ở góc thú nuôi",
     "Một góc sân nhà lát gạch. BÊN TRÁI: một bạn gái tóc tết ngồi xổm, hai tay ôm "
     "một con mèo vàng. BÊN PHẢI: một bạn trai đứng, tay cầm hai sợi dây dắt hai "
     "con chó nhỏ màu nâu đang ngồi cạnh chân. GIỮA phía sau: một cái lồng chim "
     "treo trên giá, bên trong có một con chim xanh. HẬU CẢNH: hàng rào gỗ thấp, "
     "vài bụi cây xanh.",
     "This is my cat. I have a cat. He has two dogs. I can see a cat. "
     "I can see two dogs.",
     "1. How many dogs can you see? → I can see two.  (mồi: I can see one. · I can see three. · I can see four.)\n"
     "2. What can you see? | Bạn gái đang ôm con gì? → I can see a cat.  (mồi: I can see a duck. · I can see a tiger. · I can see a horse.)",
     "What can you see? · How many dogs can you see?",
     "⚠ 29-08-2026: mồi cũ `I can see a dog.` và `I can see a bird.` — tranh có "
     "HAI con chó và một con chim trong lồng, cả hai mồi đều đúng. Nay mồi là con "
     "vật tranh không có, và dòng phụ chốt vào con bạn gái đang ôm."),
17: C("Ở góc đồ chơi trong lớp",
     "Một góc lớp có thùng đồ chơi gỗ thấp. BÊN TRÁI: một bạn gái tóc ngắn đứng, "
     "hai tay cầm một con diều hình thoi màu xanh-tím có đuôi dài. BÊN PHẢI: một "
     "bạn trai ngồi trên sàn, tay đẩy một chiếc ô tô đồ chơi màu đỏ. GIỮA: thùng đồ "
     "chơi mở nắp, trong có một con quay gỗ và một chiếc tàu thuỷ nhựa. HẬU CẢNH: "
     "tường màu kem, một tấm thảm tròn màu vàng dưới sàn.",
     "This is our room. She has a kite. He has a car. "
     "I can see a top. There's a ship. I can see four.",
     "1. What can you see? → I can see a top.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. How many toys can you see? → I can see four.  (mồi: I can see one. · I can see two. · I can see three.)",
     "What can you see? · How many toys can you see?"),
18: C("Trong phòng sinh hoạt chung",
     "Một phòng sinh hoạt sáng sủa, sàn gỗ. BÊN TRÁI: một bạn gái ngồi trên ghế "
     "bành xanh, hai tay cầm một quyển sách mở, mắt nhìn xuống trang sách. BÊN "
     "PHẢI: một bạn trai ngồi ở bàn gỗ, tay phải cầm bút viết vào quyển vở mở trước "
     "mặt. GIỮA phía sau: một giá sách thấp có mấy quyển sách đứng. HẬU CẢNH: cửa "
     "sổ lớn nhìn ra cây xanh.",
     "This is my room. She's reading. He's writing. "
     "I can see a book. I can see a pen.",
     "1. What's she doing? → She's reading.  (mồi: She's writing. · She's singing. · She's dancing.)\n"
     "2. What's he doing? → He's writing.  (mồi: He's reading. · He's singing. · He's dancing.)",
     "What's she doing? · What's he doing? · What can you see?"),
19: C("Ở sân chơi buổi chiều",
     "Một sân chơi ngoài trời, nền cỏ xanh, nắng chiều vàng nhạt. BÊN TRÁI: một bạn "
     "gái tóc tết đang đạp một chiếc xe đạp màu xanh, người hơi nghiêng về trước. "
     "BÊN PHẢI: một bạn trai đang nhảy dây, sợi dây đỏ vòng qua đầu, hai chân nhấc "
     "khỏi mặt đất. GIỮA phía sau: một ghế đá xám và một cây bàng. HẬU CẢNH: bầu "
     "trời chiều có vài đám mây.",
     "This is our playground. She's cycling. He's skipping. "
     "I can see a bike. There's a garden.",
     "1. What's she doing? → She's cycling.  (mồi: She's skipping. · She's running. · She's walking.)\n"
     "2. What's he doing? → He's skipping.  (mồi: He's cycling. · He's running. · He's walking.)",
     "What's she doing? · What's he doing? · What can you see?"),
20: C("Trong vườn thú, trước chuồng hổ",
     "Trong vườn thú. GIỮA TRANH: một chuồng lớn có song sắt dọc màu xám. TRONG "
     "CHUỒNG BÊN TRÁI: một con hổ vàng vằn đen đứng bốn chân, quay mặt ra ngoài. "
     "TRONG CHUỒNG BÊN PHẢI: một cây cao, một con khỉ nâu đang một tay bám cành đu "
     "người. TIỀN CẢNH: hai bạn nhỏ đứng quay lưng lại người xem, một bạn chỉ tay "
     "vào con hổ; cô giáo áo xanh đứng cạnh. HẬU CẢNH: cây xanh và bầu trời.",
     "This is the zoo. I can see a tiger. There's a monkey. "
     "It's swinging. That's a garden.",
     "1. What can you see? → I can see a tiger.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. What's the monkey doing? → It's swinging.  (mồi: It's running. · It's walking. · It's swimming.)",
     "What can you see? · What's the monkey doing?"),
}

# ══════════════════════ BÀI ÔN TẬP CHƯƠNG — LỚP 3 ══════════════════════
#
# Bác bắt 29-08-2026: *"review bài đọc và bài viết của các bài ôn luyện Unit
# phải đúng chuẩn như bài đọc và viết của các bài nhỏ bên trong nhé. Hiện tại
# là sai hết rồi."*
#
# Đúng, và sai theo đúng một cách: đợt 19→20-08 dựng lại 21 bài UNIT thành bài
# tả tranh, nhưng 5 bài CHƯƠNG thì `sinh_bai_tranh.py` không đụng tới — chúng
# ở lại bản do `sinh_dochieu_tienganh.py` sinh ra từ trước. Nên trong cùng một
# quyển có hai giống bài khác hẳn nhau:
#
#     bài unit    tranh + đoạn văn tả tranh · hỏi bằng TIẾNG ANH · dòng phụ Việt
#     bài chương  không tranh · đoạn HỘI THOẠI ghép · hỏi bằng TIẾNG VIỆT
#                 ("Bài đọc này nói về chuyện gì?" · "Câu nào CÓ trong bài đọc?")
#
# Hai câu hỏi tiếng Việt ấy còn không phải đọc hiểu: câu đầu đáp bằng tên
# chương in ngay trên đầu bài, câu sau là DÒ CHỮ — bé quét mắt tìm chuỗi trùng
# là xong, không cần hiểu câu ấy nói gì. Và đoạn hội thoại ghép thì rời rạc
# thật: bức C3 cũ có Ben nói "I play football at break time." rồi ngay dòng sau
# hỏi "What do you do at break time?"
#
# Nay mỗi chương một BỨC TRANH ÔN — cảnh gom lại thứ cả chương đã học. Dài hơn
# bài unit một nhịp (7 dòng thay vì 5) và 4 câu hỏi thay vì 2, vì đây là bài
# ôn; còn khuôn thì y hệt.
#
# ⚠ CHỈ DÙNG KHUÔN ĐÃ HỌC TỚI HẾT CHƯƠNG ẤY. Chương 1 chưa có "What's this?"
# (unit 4) và chưa có "Who's this?" (unit 11) — nên bài ôn chương 1 hỏi bằng
# "What can you see?" (lớp 2 U4) · "How many … can you see?" (lớp 1 U16) ·
# "Is this …?" (unit 3) · "How old is …?" (unit 2). Cổng soi từng chữ của ĐỀ
# BÀI theo túi từ tích luỹ, nên hỏi vượt là đỏ ngay.
L3C = {
1: C("Ngày đầu năm học, cô Hoa và các bạn",
     "Một lớp học nhìn thẳng từ cuối lớp, tường màu kem. BÊN PHẢI: cô giáo tóc dài "
     "buộc sau, áo xanh, đứng cạnh tấm bảng đen treo tường, một tay chỉ về phía các "
     "bạn nhỏ. Mặt bảng ĐỂ TRỐNG. BÊN TRÁI và GIỮA: hai bộ bàn học gỗ, mỗi bàn một "
     "ghế và một bạn nhỏ ngồi quay mặt về phía cô — bàn trái là bạn trai áo trắng, "
     "bàn giữa là bạn gái tóc tết áo hồng. Trên bàn trái có một quyển vở mở. GIỮA "
     "SÀN, cạnh bàn giữa: một chiếc cặp sách màu đỏ đặt dưới đất. BÊN TRÁI TƯỜNG: "
     "một cửa sổ nhìn ra tán cây xanh.",
     "This is Ms Hoa. Ms Hoa is my teacher. That's Ben. Ben is my friend. "
     "Lucy is eight years old. I can see a book. There's a bag.",
     "1. What can you see? → I can see a book.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. How old is Lucy? | Lucy mấy tuổi? → She's eight years old.  (mồi: She's six years old. · She's seven years old. · She's nine years old.)\n"
     "3. Is this Ms Hoa? | Người đứng cạnh bảng có phải cô Hoa không? → Yes, it is.  (mồi: No, it isn't.)\n"
     "4. How many windows can you see? | Con thấy mấy cái cửa sổ? → I can see two.  (mồi: I can see one. · I can see three. · I can see four.)",
     "What can you see? · How many windows can you see?",
     "Ôn chương 1: chào hỏi, tên, tuổi, bạn bè, cô giáo — và số đếm ở câu hỏi đếm cửa sổ.\n"
     "⚠ Đếm CỬA SỔ chứ không đếm bàn: `desks` mãi tới chương 4 mới có trong túi "
     "từ, còn `windows` thì lớp 1 đã dạy. Hỏi bằng một chữ bé chưa gặp thì câu "
     "đếm hoá ra câu đoán — và cổng soi đề bài theo túi từ nên đỏ ngay."),
2: C("Ở sân trường, giờ hoạt động",
     "Sân trường lát gạch đỏ, nắng sáng. GIỮA TRANH: hai bạn nhỏ đứng cạnh nhau, "
     "bạn gái tóc tết váy tím đang hát, miệng há, hai tay giơ lên; bạn trai áo "
     "trắng đứng cạnh nhìn theo. BÊN TRÁI: một cây bàng lớn tán tròn. BÊN PHẢI: dãy "
     "lớp học hai tầng màu vàng nhạt, cửa sổ xanh nhạt. HẬU CẢNH: bầu trời xanh có "
     "vài đám mây trắng.",
     "This is our school. That's our playground. There's a garden. I like singing. "
     "I can see a friend. My hair is black. I like my school.",
     "1. What can you see? → I can see a garden.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. Is this our library? | Dãy nhà lớn phía sau có phải thư viện không? → No, it isn't.  (mồi: Yes, it is.)\n"
     "3. What's this? | Dãy nhà lớn phía sau là gì? → It's our school.  (mồi: It's our library. · It's our gym. · It's our classroom.)\n"
     "4. What's your hobby? | Sở thích của bạn nhỏ trong bài là gì? → I like singing.  (mồi: I like cooking. · I like walking. · I like painting.)",
     "What can you see? · What's your hobby? · What's this?",
     "Ôn chương 2: nơi chốn trong trường · sở thích · một câu về cơ thể (mái tóc).\n"
     "⚠ KHÔNG viết `tree` và KHÔNG đếm `friends`: cả hai chữ ấy không có trong "
     "túi từ lớp 1–3 (chỉ có `garden`, và `friend` số ít). Cái cây vẫn vẽ — nó "
     "chính là thứ đẻ ra chữ `garden` mà cổng chấp nhận."),
3: C("Ở nhà, hai chị em soạn cặp",
     "Một phòng khách sáng, sàn gỗ. BÊN PHẢI: mẹ tóc búi, áo hồng, ngồi trên ghế "
     "sofa xám. BÊN TRÁI: một bạn gái tóc tết đứng cạnh một cái bàn thấp. TRÊN BÀN: "
     "một cây bút bi và một cái thùng các-tông MÀU NÂU. DƯỚI SÀN, trước bàn: một "
     "quả bóng đá đen-trắng. HẬU CẢNH: tường màu kem, một khung ảnh treo tường.",
     "This is my sister. That's my mother. I have a pen. I can see a box. "
     "It's brown. I play football at break time. I like my sister.",
     "1. What can you see? → I can see a box.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. What colour is the box? | Cái thùng (box) màu gì? → It's brown.  (mồi: It's red. · It's green. · It's blue.)\n"
     "3. Who's this? | Người đang ngồi trên ghế sofa là ai? → It's my mother.  (mồi: It's my sister. · It's my brother. · It's my father.)\n"
     "4. What do you do at break time? | Giờ ra chơi bạn nhỏ làm gì? → I play football.  (mồi: I play badminton. · I play chess. · I play basketball.)",
     "What can you see? · Who's this? · What do you do at break time?",
     "Ôn chương 3: đồ dùng · màu sắc · giờ ra chơi · gia đình.\n"
     "⚠ Câu màu chỉ hỏi về cái THÙNG 📦 — hình một màu, gọi tên không cãi được. "
     "Đừng hỏi màu quả bóng đá: hình ⚽ đen-trắng, hai người nhìn ra hai màu."),
4: C("Trong bếp, mẹ dọn bữa sáng",
     "Một gian bếp sáng sủa nhìn thẳng. GIỮA: một cái bàn ăn gỗ, trên bàn có một "
     "đĩa bánh mì vàng. PHÍA SAU BÀN: mẹ tóc búi, áo blouse trắng của bác sĩ, đứng "
     "cười. BÊN TRÁI: một cái ghế gỗ, và một cây đèn bàn đang sáng đặt trên bàn "
     "nhỏ. BÊN PHẢI: một cánh cửa gỗ LỚN màu nâu đang mở. HẬU CẢNH: tường bếp màu "
     "kem, một cửa sổ vuông nhỏ.",
     "This is my mother. She's a doctor. There's a table in the room. "
     "I can see some bread. That's my lamp. The door is big. I like my house.",
     "1. What can you see? → I can see some bread.  (mồi: I can see some fish. · I can see some meat. · I can see some water.)\n"
     "2. What's her job? | Mẹ bạn nhỏ làm nghề gì? → She's a doctor.  (mồi: She's a nurse. · She's a farmer. · She's a teacher.)\n"
     "3. What's in the room? | Trong phòng có gì? → There's a table in the room.  (mồi: There's a bed in the room. · There's a dog in the room. · There's a cat in the room.)\n"
     "4. Is the door big? | Cánh cửa có to không? → The door is big.  (mồi: The door is small. · The door is red. · The door is blue.)",
     "What can you see? · What's her job? · What's in the room?",
     "Ôn chương 4: nghề nghiệp · phòng trong nhà · đồ đạc · đồ ăn."),
5: C("Cả lớp đi vườn thú",
     "Trong vườn thú, nền cỏ xanh. GIỮA TRANH: một chuồng lớn có song sắt dọc màu "
     "xám. TRONG CHUỒNG BÊN TRÁI: một con voi xám đứng bốn chân. TRONG CHUỒNG BÊN "
     "PHẢI: một con hổ vàng vằn đen. TRÊN NÓC CHUỒNG, phía phải: một con khỉ nâu "
     "ngồi. TIỀN CẢNH BÊN TRÁI: một bạn gái đang đi bộ, tay cầm một con diều hình "
     "thoi màu xanh-tím. BÊN PHẢI: một cây bàng lớn. HẬU CẢNH: bầu trời xanh có mây.",
     "This is the zoo. I can see an elephant. There's a monkey. That's a tiger. "
     "She's walking. She has a kite. I like the zoo.",
     "1. What can you see? → I can see an elephant.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. What's she doing? | Bạn gái ở phía trước đang làm gì? → She's walking.  (mồi: She's running. · She's cycling. · She's skipping.)\n"
     "3. How many toys can you see? | Con thấy mấy món đồ chơi? → I can see one.  (mồi: I can see two. · I can see three. · I can see four.)\n"
     "4. Is this a tiger? | Con vật vàng vằn đen trong chuồng có phải con hổ không? → Yes, it is.  (mồi: No, it isn't.)",
     "What can you see? · What's she doing? · How many toys can you see?",
     "Ôn chương 5: thú nuôi · vườn thú · đồ chơi · việc đang làm."),
}

# ══════════════════════════════ LỚP 4 ══════════════════════════════
# Dài hơn lớp 3 MỘT NHỊP: thêm một câu tả, KHÔNG thêm chuyện thứ hai.
L4 = {
0: C("Ở sân trường ngày tựu trường",
     "Sân trường ngày khai giảng, nắng sáng. GIỮA TRANH: hai bạn nhỏ khoảng chín "
     "tuổi đứng đối diện, bắt tay nhau, cùng cười. BÊN TRÁI là bạn gái tóc dài buộc "
     "nơ đỏ, váy xanh. BÊN PHẢI là bạn trai tóc ngắn, áo sơ mi trắng, quần short "
     "xanh. Cả hai đeo cặp sau lưng. HẬU CẢNH: cổng trường sắt mở, dãy lớp học màu "
     "vàng hai tầng, một cây phượng bên trái, bầu trời xanh có mây trắng.",
     "This is my school. This is Mary. This is Ben. Mary is my friend. "
     "Ben is my friend. I can see two bikes.",
     "1. What can you see? → I can see two bikes.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. How many bikes can you see? → I can see two.  (mồi: I can see one. · I can see three. · I can see four.)",
     "Where are they? · What can you see? · How many bikes can you see?",
     "BỨC BÁC CHÊ. Cũ: 'This is a friend. I can see a girl. That's a ball.' — "
     "không ai chào ai, lại nhét cả bóng, diều, mèo, mũ."),
1: C("Ở trại hè, trước tấm bản đồ thế giới",
     "Một góc phòng sinh hoạt trại hè. HẬU CẢNH: tấm bản đồ thế giới lớn treo "
     "tường, vẽ các châu lục màu xanh lá và nâu nhạt trên nền biển xanh dương, "
     "KHÔNG có chữ. GIỮA TRANH: hai bạn nhỏ đứng trước bản đồ. BÊN TRÁI là bạn gái "
     "tóc đen, áo dài trắng, tay chỉ vào một điểm trên bản đồ. BÊN PHẢI là bạn gái "
     "tóc đen cắt ngắn, áo kimono hồng nhạt. TIỀN CẢNH: một cái bàn gỗ có hai chiếc "
     "ba lô đặt trên.",
     "This is my friend. I'm from Viet Nam. She's from Japan. "
     "I can see a bag. There's a table.",
     "1. Where's she from? → She's from Japan.  (mồi: She's from Britain. · She's from America. · She's from Thailand.)\n"
     "2. What can you see? → I can see a bag.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are you from? · Where's she from? · What can you see?",
     "⚠ Cờ quốc gia emoji VẼ RA RỖNG (phông không có). Cảnh dùng BẢN ĐỒ, không cờ."),
2: C("Trong phòng ngủ buổi sáng",
     "Một phòng ngủ trẻ em buổi sáng sớm, nắng vàng nhạt qua cửa sổ. GIỮA: một bạn "
     "trai vừa ngồi dậy trên giường, chăn xanh còn phủ ngang chân, một tay dụi mắt. "
     "BÊN TRÁI, trên chiếc bàn nhỏ cạnh giường: một chiếc đồng hồ báo thức tròn màu "
     "đỏ, kim chỉ SÁU GIỜ ĐÚNG (kim ngắn ở số 6, kim dài ở số 12). BÊN PHẢI: một "
     "chiếc cặp sách xanh dựng dưới chân bàn học. HẬU CẢNH: cửa sổ có rèm vàng.",
     "This is my bedroom. It's six o'clock. I get up at six o'clock. "
     "I can see a bed. There's a bag.",
     "1. What time is it? → It's six o'clock.  (mồi: It's eight o'clock. · It's six thirty. · It's eight thirty.)\n"
     "2. What can you see? → I can see a bed.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where is he? · What time is it? · What can you see?"),
3: C("Trong lớp, trước tấm lịch tuần treo tường",
     "Một góc lớp học. HẬU CẢNH: tấm lịch tuần lớn treo tường, kẻ bảy ô dọc bằng "
     "nhau, ô đầu tiên được khoanh tròn màu đỏ (các ô ĐỂ TRỐNG, không chữ). BÊN "
     "TRÁI: cô giáo áo xanh đứng cạnh tấm lịch, tay cầm que chỉ vào ô được khoanh. "
     "BÊN PHẢI và TIỀN CẢNH: hai bạn nhỏ ngồi ở bàn học, một bạn giơ tay phát biểu. "
     "Trên bàn có quyển sách mở.",
     "This is my classroom. It's Monday today. I study at school on Mondays. "
     "I can see a teacher. I can see two desks.",
     "1. What day is it today? → It's Monday.  (mồi: It's Sunday. · It's Friday. · It's Tuesday.)\n"
     "2. What do you do on Mondays? → I study at school.  (mồi: I listen to music. · I do housework. · I stay at home.)",
     "What day is it today? · What do you do on Mondays? · What can you see?"),
4: C("Ở bàn tiệc sinh nhật",
     "Một bàn tiệc sinh nhật trong nhà, nhìn chếch từ trên. GIỮA BÀN: một chiếc "
     "bánh kem tròn phủ kem trắng-hồng, cắm mấy cây nến đang cháy. BÊN TRÁI: một "
     "đĩa khoai tây rán vàng. BÊN PHẢI: một chùm nho tím và một lọ mứt dâu nắp "
     "vàng. PHÍA SAU BÀN: một bạn gái đội mũ sinh nhật hình nón đang chụm môi thổi "
     "nến; mẹ tóc búi đứng cạnh, tay đặt lên vai con. HẬU CẢNH: dây cờ giấy nhiều "
     "màu treo ngang tường.",
     "This is my birthday party. My birthday is in May. I can see a cake. "
     "There's some jam. I want some grapes.",
     "1. When's your birthday? → It's in May.  (mồi: It's in April. · It's in March. · It's in February.)\n"
     "2. What can you see? → I can see a cake.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · When's your birthday? · What can you see?"),
5: C("Ở góc tài năng của lớp",
     "Một góc lớp rộng, sàn gỗ. BÊN TRÁI: một bạn trai đang đạp một chiếc xe đạp "
     "màu xanh dương, người hơi nghiêng về trước, mặt vui. BÊN PHẢI: một bạn gái "
     "đứng trước giá vẽ ba chân, tay phải cầm cọ, đang vẽ một bông hoa lên tờ giấy "
     "trắng gắn trên giá. GIỮA phía sau: một cái bàn thấp có hộp màu mở nắp. HẬU "
     "CẢNH: tường màu kem, một tấm bảng ghim treo.",
     "This is my friend. He can ride a bike. She can draw. "
     "I can see a bike. I can see a picture.",
     "1. What can he do? → He can ride a bike.  (mồi: He can ride a horse. · He can play the piano. · He can play the guitar.)\n"
     "2. What can she do? → She can draw.  (mồi: She can swim. · She can cook. · She can sing.)",
     "What can he do? · What can she do? · Can you ride a bike?"),
6: C("Nhìn toàn cảnh sân trường",
     "Toàn cảnh một trường tiểu học nhìn từ trên cao chếch xuống. GIỮA: sân trường "
     "lát gạch đỏ. BÊN TRÁI: một dãy nhà học hai tầng màu vàng. GIỮA phía sau: một "
     "dãy nhà hai tầng màu vàng thứ hai. BÊN PHẢI: một toà nhà thấp có cửa kính "
     "rộng, bên trong thấy giá sách — thư viện. GÓC DƯỚI BÊN PHẢI: một sân chơi có "
     "cầu trượt đỏ và xích đu. TIỀN CẢNH: hai bạn nhỏ đứng quay lưng lại người xem, "
     "một bạn giơ tay chỉ về phía các dãy nhà.",
     "This is my school. My school is in the city. There are three buildings. "
     "I can see a library. I can see a playground.",
     "1. Where's your school? → It's in the city.  (mồi: It's in the town. · It's in the village. · It's in the countryside.)\n"
     "2. How many buildings are there? → There are three.  (mồi: There are two. · There are four. · There are five.)",
     "Where's your school? · How many buildings are there? · What can you see?"),
7: C("Trong lớp, trước thời khoá biểu dán tường",
     "Một góc lớp học. HẬU CẢNH: tấm thời khoá biểu lớn dán tường, kẻ ô vuông thành "
     "lưới, các ô ĐỂ TRỐNG không chữ; hai ô ở cột đầu được tô màu vàng nổi bật. "
     "GIỮA: hai bạn nhỏ đứng trước tấm bảng, bạn trai bên trái giơ tay chỉ vào một "
     "ô vàng, bạn gái bên phải cầm quyển sách áp trước ngực nhìn theo. TIỀN CẢNH: "
     "một cái bàn học có chiếc cặp xanh đặt trên.",
     "This is my classroom. I have English and maths today. "
     "I have maths on Mondays. There's a book on the desk. That's my bag.",
     "1. What subjects do you have today? → I have English and maths.  (mồi: I have art and music. · I have science and art. · I have maths and music.)\n"
     "2. When do you have maths? → I have it on Mondays.  (mồi: I have it on Fridays. · I have it on Tuesdays. · I have it on Sundays.)",
     "What subjects do you have today? · When do you have maths?"),
8: C("Ở góc trưng bày môn Mĩ thuật của lớp",
     "Một góc trưng bày trong lớp. HẬU CẢNH: một tấm bảng ghim treo ba bức tranh "
     "trẻ em vẽ — một bức vẽ ngôi nhà, một bức vẽ cái cây, một bức vẽ mặt trời. "
     "GIỮA: một bạn gái đứng cạnh bảng, một tay chỉ lên bức tranh ngôi nhà, tay kia "
     "cầm bảng màu tròn nhiều màu. BÊN PHẢI: một giá vẽ ba chân có tờ giấy trắng. "
     "TIỀN CẢNH: một cái bàn có hộp màu và mấy cây cọ.",
     "This is my classroom. My favourite subject is art. I want to be a painter. "
     "There's a picture. I can see a table.",
     "1. What's your favourite subject? → It's art.  (mồi: It's maths. · It's music. · It's science.)\n"
     "2. What can you see? → I can see a table.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "What's your favourite subject? · What do you want to be? · What can you see?"),
9: C("Ở ngày hội thể thao trên sân trường",
     "Sân thể thao ngoài trời, đường chạy màu đỏ gạch. GIỮA: ba bạn nhỏ đang chạy "
     "thi trên đường chạy, người nghiêng về trước. BÊN TRÁI: một quả bóng đá "
     "đen-trắng nằm trên cỏ. BÊN PHẢI: cô giáo áo xanh đứng cầm một tấm huy chương "
     "vàng có dải ruy băng đỏ giơ lên. HẬU CẢNH: dây cờ đuôi nheo nhiều màu căng "
     "ngang, khán đài thấp, bầu trời xanh.",
     "This is our sports day. Our sports day is in October. "
     "I can see a ball. There's a teacher. That's my friend.",
     "1. When's your sports day? → It's in October.  (mồi: It's in May. · It's in June. · It's in July.)\n"
     "2. What can you see? → I can see a ball.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · When's your sports day? · What can you see?"),
10: C("Trước bảng ảnh kì nghỉ hè treo ở lớp",
     "Một góc lớp. HẬU CẢNH: một tấm bảng ghim lớn có ba tấm ảnh ghim bằng đinh "
     "mũ màu — ảnh thứ nhất chụp bãi biển có ô dù và sóng, ảnh thứ hai chụp cánh "
     "đồng lúa vùng quê, ảnh thứ ba chụp một thành phố có nhà cao tầng. GIỮA: một "
     "bạn trai đứng, tay chỉ vào tấm ảnh thành phố. BÊN PHẢI: một bạn gái đứng nhìn "
     "theo, hai tay chắp sau lưng. TIỀN CẢNH: một cái bàn học.",
     "This is my picture. I was in Tokyo last summer. I can see a beach. "
     "There's a city. That's the countryside.",
     "1. Where were you last summer? → I was in Tokyo.  (mồi: I was in London. · I was in Sydney. · I was in Bangkok.)\n"
     "2. What can you see? → I can see a beach.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where were you last summer? · What can you see?"),
11: C("Trên con phố trước nhà bạn nhỏ",
     "Một con phố nhỏ trong thành phố, nhìn dọc theo vỉa hè. BÊN TRÁI: một ngôi nhà "
     "hai tầng màu kem, cửa gỗ nâu, có ban công nhỏ. TRÊN GÓC TƯỜNG NHÀ: một tấm "
     "biển tên phố hình chữ nhật màu xanh dương (ĐỂ TRỐNG, không chữ). GIỮA: hai "
     "bạn nhỏ đi bộ trên vỉa hè, bạn trai bên trái giơ tay chỉ lên tấm biển. BÊN "
     "PHẢI: lòng đường có hai chiếc ô tô và một chiếc xe máy đang chạy, vài người "
     "đi bộ — phố đông. HẬU CẢNH: hàng cây và các toà nhà.",
     "This is my street. I live in Tran Hung Dao Street. My street is busy. "
     "I can see two cars. I can see a house.",
     "1. What's the street like? → It's a busy street.  (mồi: It's a quiet street. · It's a noisy street. · It's a big street.)\n"
     "2. What can you see? → I can see two cars.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where do you live? · What's the street like? · What can you see?"),
12: C("Ở bệnh viện, nơi mẹ bạn nhỏ làm việc",
     "Trước cửa một phòng khám trong bệnh viện, tường trắng sạch. GIỮA: một cô "
     "khoảng ba mươi lăm tuổi mặc áo blouse trắng dài, ống nghe đeo quanh cổ, tóc "
     "búi gọn, đứng cười, một tay đặt lên vai con. BÊN PHẢI: một bạn gái khoảng "
     "chín tuổi đứng cạnh mẹ, đeo cặp. BÊN TRÁI: cánh cửa phòng khám mở hé, có tấm "
     "biển chữ thập đỏ treo trên cửa. HẬU CẢNH: hành lang bệnh viện có ghế chờ.",
     "This is my mother. She's a doctor. She works at a hospital. "
     "I can see a hospital. I can see a bag.",
     "1. What does she do? → She's a doctor.  (mồi: She's a nurse. · She's a teacher. · She's a farmer.)\n"
     "2. Where does she work? → She works at a hospital.  (mồi: She works at a school. · She works at a factory. · She works at a nursing home.)",
     "Who is this? · What does she do? · Where does she work?",
     "Bản trước dựng 'ngày hội nghề nghiệp' nhồi năm nghề. Nay MỘT người, MỘT nơi."),
13: C("Trước tấm ảnh lớp treo ở cuối phòng",
     "Một góc lớp học. HẬU CẢNH: một tấm ảnh lớp lớn đóng khung gỗ treo tường, "
     "trong ảnh có bốn bạn nhỏ đứng hàng ngang, vẽ rõ mặt — bạn thứ nhất CAO hơn "
     "hẳn, tóc ngắn; bạn thứ hai tóc DÀI ngang lưng; bạn thứ ba THẤP, tóc xoăn; bạn "
     "thứ tư mặt TRÒN, đeo kính. TIỀN CẢNH: một bạn gái đứng quay lưng lại người "
     "xem, tay chỉ lên bạn cao nhất trong ảnh; cô giáo áo xanh đứng cạnh nhìn theo.",
     "This is my friend. He's tall. She has long hair. He's short. "
     "She has a round face. That's my classroom.",
     "1. What does he look like? | Bạn trai ĐỨNG ĐẦU HÀNG bên trái trong ảnh trông thế nào? → He's tall.  (mồi: He's short. · He's slim. · He's big.)\n"
     "2. What does she look like? | Bạn gái mặc VÁY ĐỎ trong ảnh trông thế nào? → She has long hair.  (mồi: She has short hair. · She's tall. · She's short.)",
     "Who is this? · What does he look like? · What does she look like?",
     "Bức cũ vẽ mắt-mũi-mồm-tay RỜI. Nay là NGƯỜI trong ảnh để tả.\n"
     "⚠ 29-08-2026, HAI câu đều hai đáp án đúng. Trong ảnh có BỐN bạn, và chính "
     "đoạn đọc khẳng định cả `He's tall.` lẫn `He's short.` (hai bạn trai khác "
     "nhau), cả `She has long hair.` lẫn `She has a round face.` (hai bạn gái "
     "khác nhau) — rồi lấy nhau làm mồi. Nay chốt bằng VỊ TRÍ và MÀU VÁY trong ảnh.\n"
     "⚠ Và bỏ hẳn mồi `She has a round face.` · `She has big eyes.`: bút `nguoi` "
     "vẽ MỌI khuôn mặt là một hình tròn với hai chấm mắt to, nên hai câu ấy đúng "
     "với bất kỳ bạn nào trong ảnh — chốt kiểu gì cũng không làm chúng sai được. "
     "Thứ bức này phân biệt được chỉ có TÓC và CHIỀU CAO."),
14: C("Trong nhà buổi sáng",
     "Một phòng khách buổi sáng, nắng qua cửa sổ. GIỮA: một bạn trai khoảng chín "
     "tuổi đang cầm cây lau nhà, đẩy trên sàn gạch sáng bóng; một cái xô nhựa xanh "
     "đặt cạnh chân. BÊN PHẢI: một chiếc ti vi đặt trên kệ gỗ, MÀN HÌNH TỐI (đang "
     "tắt). BÊN TRÁI: một bộ ghế sofa xám và cái bàn thấp. HẬU CẢNH: cửa sổ có rèm "
     "vàng, một chậu cây xanh.",
     "This is my home. I clean the floor in the morning. "
     "I watch TV in the evening. I can see a TV. I can see a chair.",
     "1. What do you do in the morning? → I clean the floor.  (mồi: I wash the dishes. · I wash the clothes. · I cook meals.)\n"
     "2. When do you watch TV? → I watch TV in the evening.  (mồi: I watch TV in the morning. · I watch TV at noon. · I watch TV in the afternoon.)",
     "What is he doing? · What do you do in the morning? · When do you watch TV?"),
15: C("Trước trung tâm thể thao, sáng thứ Bảy",
     "Trước cửa một trung tâm thể thao, nhà mái cong, cửa kính lớn. BÊN TRÁI: một "
     "người bố khoảng bốn mươi tuổi, áo thể thao xanh, đang bước về phía cửa, tay "
     "xách một túi thể thao, tay kia ôm quả bóng quần vợt. BÊN PHẢI: một bạn gái "
     "đứng trên vỉa hè vẫy tay tiễn. TIỀN CẢNH: một chiếc xe đạp dựng cạnh cột "
     "đèn. HẬU CẢNH: bầu trời sáng, vài đám mây.",
     "This is my father. He goes to the sports centre on Saturdays. "
     "He plays tennis on Sundays. I can see a bike. I can see a ball.",
     "1. Where does he go on Saturdays? → He goes to the sports centre.  (mồi: He goes to the cinema. · He goes to the gym. · He goes to the swimming pool.)\n"
     "2. What does he do on Sundays? → He plays tennis.  (mồi: He plays badminton. · He does yoga. · He plays the guitar.)",
     "Who is this? · Where does he go on Saturdays? · What does he do on Sundays?"),
16: C("Bên cửa sổ lớp học, cạnh bảng thời tiết",
     "Một góc lớp học có cửa sổ lớn. BÊN PHẢI: cửa sổ mở, nhìn ra ngoài thấy MẶT "
     "TRỜI vàng chói trên bầu trời xanh không mây, cây cối đứng yên. BÊN TRÁI: một "
     "tấm bảng thời tiết treo tường, chia bốn ô vuông vẽ bốn hình — mặt trời, đám "
     "mây, mây có mưa, mây có gió; ô MẶT TRỜI được khoanh tròn màu đỏ. GIỮA: cô "
     "giáo đứng cạnh bảng, tay vừa gắn hình mặt trời vào ô ấy. TIỀN CẢNH: một bạn "
     "nhỏ ngồi ở bàn nhìn lên.",
     "This is my classroom. It was sunny last weekend. It's sunny today. "
     "I can see the sun. I can see a window.",
     "1. What was the weather like last weekend? → It was sunny.  (mồi: It was rainy. · It was windy. · It was cloudy.)\n"
     "2. What can you see? → I can see the sun.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "What was the weather like? · What can you see?",
     "⚠ Tính từ thời tiết KHÔNG vẽ thành vật rời được. Phải là BẢNG THỜI TIẾT."),
17: C("Ở một ngã tư trong phố",
     "Một ngã tư trong thành phố nhìn chếch. GÓC TRÁI: một cột biển báo cao có tấm "
     "biển BÁT GIÁC MÀU ĐỎ (biển dừng, KHÔNG viết chữ). GIỮA: một bạn nhỏ đeo cặp "
     "đứng trên vỉa hè, ngước nhìn một bác đi đường tóc hoa râm; bác đang giơ tay "
     "trái chỉ về phía bên trái. BÊN PHẢI: một cửa hiệu có tủ kính bày mấy chồng "
     "sách — hiệu sách. HẬU CẢNH: hai chiếc ô tô đang chờ, vạch kẻ đường trắng, các "
     "toà nhà.",
     "This is my city. I can see a road sign. I can see a bookshop. "
     "I can see two cars. The bookshop is on the left.",
     "1. What can you see? → I can see a bookshop.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. How many cars can you see? → I can see two.  (mồi: I can see one. · I can see three. · I can see four.)",
     "Where is he? · What can you see? · How many cars can you see?"),
18: C("Trong trung tâm mua sắm, trước hiệu sách",
     "Bên trong một trung tâm mua sắm, sàn lát đá bóng, trần cao có đèn. GIỮA: hai "
     "gian hàng nằm CẠNH NHAU. Gian bên trái có tủ kính bày các chồng sách nhiều "
     "màu — hiệu sách. Gian bên phải bày những ổ bánh mì và bánh ngọt trong tủ kính "
     "— hiệu bánh. TIỀN CẢNH BÊN TRÁI: hai bạn nhỏ đứng, bạn gái giơ tay chỉ sang "
     "gian hiệu sách. TIỀN CẢNH BÊN PHẢI: một giá treo áo có một chiếc áo thun màu "
     "xanh và một tấm thẻ giá nhỏ (ĐỂ TRỐNG, không chữ).",
     "This is the shopping centre. There's a bookshop. There's a bakery. "
     "The bookshop is near the bakery. I can see a T-shirt.",
     "1. Where's the bookshop? → It's near the bakery.  (mồi: It's opposite the bakery. · It's behind the bakery. · It's near the pet shop.)\n"
     "2. What can you see? → I can see a T-shirt.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · Where's the bookshop? · What can you see?"),
19: C("Trong vườn thú, trước chuồng hươu cao cổ",
     "Trong vườn thú, ngày nắng. GIỮA và BÊN TRÁI: một khu quây rào gỗ thấp, bên "
     "trong có HAI con hươu cao cổ đứng cạnh nhau, cổ vươn cao tới tán một cây "
     "keo. BÊN PHẢI: một con công đang xoè đuôi rộng hình quạt, lông xanh lục "
     "óng. TIỀN CẢNH: cô giáo áo xanh và một bạn nhỏ đứng quay lưng lại người "
     "xem, cô giơ tay chỉ về phía hai con hươu. HẬU CẢNH: cây xanh, bầu trời.",
     "This is the zoo. I can see two giraffes. There's a peacock. "
     "It's dancing. That's a garden.",
     "1. What can you see? → I can see two giraffes.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. How many giraffes can you see? → I can see two.  (mồi: I can see one. · I can see three. · I can see four.)",
     "Where are they? · What can you see? · How many giraffes can you see?"),
20: C("Ở trại hè bên hồ, buổi tối",
     "Một khu trại hè bên hồ lúc chạng vạng, trời tím nhạt. GIỮA: một đống lửa "
     "trại đang cháy, ngọn lửa cam-vàng, mấy thanh củi xếp chụm. BÊN TRÁI: một bạn "
     "trai đang quỳ một chân, tay đặt thêm một thanh củi vào đống lửa. BÊN PHẢI: "
     "hai bạn nhỏ ngồi trên khúc gỗ, một bạn ôm cây đàn ghi ta gảy, cả hai há "
     "miệng hát. HẬU CẢNH: một chiếc lều vải màu cam dựng bên trái, mặt hồ phẳng "
     "phản chiếu ánh lửa, vài cây thông.",
     "This is our campsite. He's building a campfire. "
     "They're singing songs. I can see a tent. There's a lake.",
     "1. What's he doing? → He's building a campfire.  (mồi: He's telling a story. · He's taking a photo. · He's playing card games.)\n"
     "2. What can you see? → I can see a tent.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · What's he doing? · What are they doing?"),
}


# ══════════════════════ BÀI ÔN TẬP CHƯƠNG — LỚP 4 ══════════════════════
# Cùng lý do và cùng khuôn với `L3C` ở trên: bốn bài chương của lớp 4 vẫn ở
# bản hội thoại ghép, hỏi bằng tiếng Việt. Lớp 4 có BỐN chương, mỗi chương 5–6
# unit, nên bức ôn phải gom được nhiều nhánh hơn — 8 dòng, 4 câu hỏi.
L4C = {
1: C("Sáng thứ Hai ở lớp",
     "Một lớp học sáng, nhìn thẳng. TRÊN TƯỜNG GIỮA: một chiếc đồng hồ tròn, kim "
     "chỉ BẢY GIỜ đúng. BÊN PHẢI TƯỜNG: một tấm lịch tuần kẻ ô, ô ĐẦU TIÊN được "
     "khoanh (các ô ĐỂ TRỐNG, không chữ). BÊN TRÁI: một cửa sổ nhìn ra cây xanh. "
     "TIỀN CẢNH BÊN TRÁI: một bạn trai áo trắng ngồi ở bàn học, trên bàn có quyển "
     "vở mở. BÊN PHẢI: một bạn nhỏ áo xanh đứng giơ tay vẫy chào.",
     "This is my classroom. This is Ben. Ben is my friend. He's from Japan. "
     "It's seven o'clock. I go to school at seven o'clock. It's Monday today. "
     "I can see a clock.",
     "1. What can you see? → I can see a clock.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. What time is it? | Đồng hồ trên tường chỉ mấy giờ? → It's seven o'clock.  (mồi: It's six o'clock. · It's eight o'clock. · It's nine o'clock.)\n"
     "3. Where's he from? | Bạn Ben đến từ nước nào? → He's from Japan.  (mồi: He's from Britain. · He's from America. · He's from Thailand.)\n"
     "4. What day is it today? | Hôm nay là thứ mấy? → It's Monday.  (mồi: It's Sunday. · It's Friday. · It's Tuesday.)",
     "What can you see? · What time is it? · What day is it today?",
     "Ôn chương 1: bạn bè và nước bạn ấy · giờ giấc · ngày trong tuần."),
2: C("Trước dãy nhà học của trường",
     "Sân trường lát gạch đỏ, nắng sáng. HẬU CẢNH: HAI dãy nhà học hai tầng màu "
     "vàng nhạt đứng cạnh nhau. BÊN PHẢI: một cây bàng lớn tán tròn. TIỀN CẢNH BÊN "
     "TRÁI: một giá vẽ gỗ dựng trên sân, trên giá là một bức tranh. GIỮA: một bạn "
     "gái tóc tết chỉ tay về phía giá vẽ; bên cạnh là một bạn trai áo xanh đứng "
     "nhìn theo. HẬU CẢNH: bầu trời xanh có mây trắng.",
     "This is my school. My school is in the town. There are two buildings. "
     "I have art today. My favourite subject is art. Our sports day is in October. "
     "I can see a garden. I like my school.",
     "1. What can you see? → I can see a garden.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. How many buildings are there? | Con thấy mấy dãy nhà học? → There are two.  (mồi: There are three. · There are four. · There are five.)\n"
     "3. What's your favourite subject? | Môn bạn nhỏ thích nhất là môn gì? → It's art.  (mồi: It's maths. · It's music. · It's science.)\n"
     "4. When's your sports day? | Ngày hội thể thao vào tháng nào? → It's in October.  (mồi: It's in May. · It's in June. · It's in July.)",
     "What can you see? · What's your favourite subject? · When's your sports day?",
     "Ôn chương 2: trường mình ở đâu · có mấy dãy nhà · môn học · ngày hội."),
3: C("Buổi tối ở nhà mình",
     "Một phòng khách buổi tối, tường màu kem. BÊN TRÁI: một cửa sổ vuông. GIỮA "
     "BÊN TRÁI: mẹ tóc dài, mặc áo blouse TRẮNG của y tá, đứng cười. BÊN PHẢI: bố "
     "tóc ngắn, áo xanh, đứng — bố CAO hơn hẳn mẹ. GIỮA: một cái bàn gỗ và một "
     "chiếc ghế; trên bàn có một cây đèn bàn đang sáng.",
     "This is my home. This is my mother. She's a nurse. She works at a hospital. "
     "My father is tall. I wash the dishes in the evening. I can see a table. "
     "I like my home.",
     "1. What can you see? → I can see a table.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. What does she do? | Mẹ bạn nhỏ làm nghề gì? → She's a nurse.  (mồi: She's a doctor. · She's a teacher. · She's a farmer.)\n"
     "3. Where does she work? | Mẹ làm việc ở đâu? → She works at a hospital.  (mồi: She works at a school. · She works at a factory. · She works at a nursing home.)\n"
     "4. What do you do in the morning? | Buổi TỐI bạn nhỏ làm việc gì? → I wash the dishes.  (mồi: I clean the floor. · I wash the clothes. · I cook meals.)",
     "What can you see? · What does she do? · Where does she work?",
     "Ôn chương 3: nhà mình · nghề của mẹ · trông bố thế nào · việc mỗi ngày.\n"
     "⚠ Câu 4 mượn ĐỀ BÀI của khuôn `What do you do in the morning?` (unit 14) "
     "nhưng dòng phụ chốt vào BUỔI TỐI — đó là chỗ bé phải đọc đoạn mới trả lời "
     "được, chứ đoán theo đề thì ra `in the morning`."),
4: C("Ở trại hè bên hồ",
     "Một khu trại hè bên hồ, chiều muộn. BÊN TRÁI: một chiếc lều vải màu xanh "
     "dựng trên cỏ. GIỮA: một đống lửa trại đang cháy, một bạn trai áo đỏ cúi "
     "người xếp củi. BÊN PHẢI: hai bạn nhỏ đứng cạnh nhau, cùng giơ tay, miệng há "
     "— đang hát. HẬU CẢNH: mặt hồ phẳng và một cây lớn bên phải.",
     "This is our campsite. It was sunny yesterday. I can see the sun. "
     "He's building a campfire. They're singing songs. There's a tent. "
     "I can see a lake. I like our campsite.",
     "1. What can you see? → I can see a lake.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. What's he doing? | Bạn trai áo đỏ đang làm gì? → He's building a campfire.  (mồi: He's telling a story. · He's taking a photo. · He's playing card games.)\n"
     "3. What are they doing? | Hai bạn bên phải đang làm gì? → They're singing songs.  (mồi: They're playing games. · They're putting up a tent. · They're playing tug of war.)\n"
     "4. What was the weather like? | Hôm QUA trời thế nào? → It was sunny.  (mồi: It was rainy. · It was windy. · It was cloudy.)",
     "Where are they? · What's he doing? · What are they doing?",
     "Ôn chương 4: thời tiết · việc ở trại hè · cảnh quanh ta."),
}



# ══════════════════════════════ LỚP 5 ══════════════════════════════
# Vốn từ tích luỹ tới đây đã dày (646–857 chữ), nên đoạn tả được cảnh có
# NGƯỜI ĐANG LÀM VIỆC chứ không chỉ đồ vật đứng yên. Nhưng phần lớn từ MỚI của
# lớp 5 là tính từ, tần suất và cụm việc — không vẽ thành vật được. Nên vật
# trong tranh chủ yếu mượn của bốn quyển trước; đó là điều đúng: bé đã học rồi.
L5 = {
1: C("Trong lớp, một bạn tự giới thiệu",
     "Một phòng học nhìn thẳng. BÊN TRÁI: tấm bảng ghim treo tường, trên ghim một "
     "bức tranh vẽ CON CÁ HEO màu xanh xám đang nhảy trên sóng biển. GIỮA: một bạn "
     "gái khoảng mười tuổi, tóc dài buộc nơ hồng, áo sơ mi trắng, váy xanh, đứng "
     "quay mặt ra lớp, một tay chỉ lên bức tranh cá heo, mặt tươi. TIỀN CẢNH BÊN "
     "PHẢI: hai bộ bàn học gỗ, mỗi bàn một bạn ngồi quay lưng lại người xem, trên "
     "bàn có quyển vở mở. HẬU CẢNH BÊN PHẢI: cửa sổ nhìn ra tán cây xanh.",
     "This is my class. This is Mary. Mary is my friend. "
     "My favourite animal is a dolphin. I can see a dolphin.",
     "1. What's your favourite animal? → It's a dolphin.  (mồi: It's a cat. · It's a dog. · It's a fox.)\n"
     "2. What can you see? → I can see a dolphin.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · What can you see? · What's your favourite animal?"),
2: C("Trên con phố trước nhà",
     "Một con phố nhỏ nhìn dọc theo vỉa hè, trời sáng. BÊN TRÁI: một ngôi nhà MỘT "
     "TẦNG mái đỏ, tường vàng kem, cửa gỗ nâu, có khoảnh sân nhỏ trước cửa. BÊN "
     "PHẢI: một TOÀ NHÀ CAO nhiều tầng, tường xám nhạt, các ô cửa sổ vuông xếp đều. "
     "GIỮA, trên vỉa hè: hai bạn nhỏ đứng cạnh nhau, bạn trai áo trắng giơ tay chỉ "
     "sang toà nhà cao, bạn gái váy tím nhìn theo. LÒNG ĐƯỜNG phía dưới: hai chiếc "
     "ô tô, một đỏ một xanh, đang chạy.",
     "This is my street. That's my house. There's a tall building. "
     "I live in the house. I can see two cars.",
     "1. What can you see? → I can see two cars.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. How many cars can you see? → I can see two.  (mồi: I can see one. · I can see three. · I can see four.)",
     "Where are they? · What can you see? · How many cars can you see?"),
3: C("Trước tấm bản đồ thế giới",
     "Một góc phòng học. HẬU CẢNH: tấm bản đồ thế giới lớn treo tường — các châu "
     "lục màu xanh lá và nâu nhạt trên nền biển xanh dương, KHÔNG có chữ nào. "
     "GIỮA TRANH: hai bạn nhỏ đứng trước bản đồ. BÊN TRÁI là bạn gái tóc nâu, áo "
     "vàng, tay chỉ vào một điểm phía dưới bên phải bản đồ. BÊN PHẢI là bạn trai "
     "tóc đen, áo xanh, đứng nhìn theo. TIỀN CẢNH: một cái bàn gỗ có hai chiếc cặp "
     "sách đặt trên.",
     "This is my class. This is Lucy. She's from Australia. This is Ben. "
     "He's from Japan. Ben is my friend.",
     "1. Where's she from? → She's from Australia.  (mồi: She's from Japan. · She's from America. · She's from Malaysia.)\n"
     "2. Where's he from? → He's from Japan.  (mồi: He's from Australia. · He's from America. · He's from Malaysia.)",
     "Where's she from? · Where's he from? · What can you see?"),
4: C("Trong vườn buổi chiều",
     "Một khu vườn nhỏ, nắng chiều vàng nhạt. BÊN TRÁI: một bạn gái tóc tết hai "
     "bên, áo hồng, đang cầm bình tưới nghiêng vòi tưới xuống một luống hoa — mấy "
     "bông hoa đỏ và vàng nở trên luống. BÊN PHẢI: một bạn trai áo xanh đang bước "
     "đi trên lối sỏi, hai tay đánh nhẹ, mặt vui. GIỮA phía sau: một chiếc xe đạp "
     "màu xanh dựng cạnh hàng rào gỗ thấp. HẬU CẢNH: bụi cây xanh và bầu trời.",
     "This is our garden. She's watering the flowers. He's going for a walk. "
     "I often go for a walk. I can see a bike.",
     "1. What's she doing? → She's watering the flowers.  (mồi: She's playing the violin. · She's surfing the Internet. · She's going for a walk.)\n"
     "2. What do you do at the weekend? → I often go for a walk.  (mồi: I always go for a walk. · I never go for a walk. · I sometimes go for a walk.)",
     "Where are they? · What's she doing? · What do you do at the weekend?"),
5: C("Ở góc nghề nghiệp của lớp",
     "Một góc trưng bày trong lớp. HẬU CẢNH: tấm bảng ghim treo ba bức tranh trẻ em "
     "vẽ — bức thứ nhất vẽ một NGƯỜI LÍNH CỨU HOẢ đội mũ đỏ đứng cạnh vòi nước, bức "
     "thứ hai vẽ một NGƯỜI VIẾT SÁCH ngồi bên bàn có quyển sách mở, bức thứ ba vẽ "
     "một NGƯỜI LÀM VƯỜN đội mũ rộng vành cầm bình tưới. GIỮA: một bạn trai áo vàng "
     "đứng, tay chỉ lên bức tranh lính cứu hoả. TIỀN CẢNH: một cái bàn có quyển vở "
     "mở và cây bút.",
     "This is my class. That's a firefighter. I want to be a firefighter. "
     "That's a writer. I can see a book.",
     "1. What do you want to be? → I want to be a firefighter.  (mồi: I want to be a writer. · I want to be a reporter. · I want to be a gardener.)\n"
     "2. What can you see? → I can see a book.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where is he? · What do you want to be? · What can you see?"),
6: C("Ở hành lang tầng hai",
     "Hành lang một trường học nhìn dọc, sàn gạch xám, lan can bên phải nhìn xuống "
     "sân. BÊN TRÁI có ba cánh cửa gỗ liền nhau, mỗi cửa một tấm biển hình chữ nhật "
     "treo trên — cả ba biển ĐỂ TRỐNG, không chữ. Cửa gần nhất hé mở, nhìn thấy giá "
     "sách bên trong. GIỮA HÀNH LANG: một bạn gái áo trắng đứng, tay chỉ vào cánh "
     "cửa hé mở; một bạn trai áo đỏ đứng cạnh nhìn theo. CUỐI HÀNH LANG: một cầu "
     "thang đi lên, tay vịn gỗ.",
     "This is our school. That's our library. The library is on the first floor. "
     "I like our library. I can see two books.",
     "1. Where's the library? → It's on the first floor.  (mồi: It's on the second floor. · It's on the third floor. · It's on the ground floor.)\n"
     "2. How many books can you see? → I can see two.  (mồi: I can see one. · I can see three. · I can see four.)",
     "Where are they? · Where's the library? · How many books can you see?"),
7: C("Trong lớp, giờ làm bài nhóm",
     "Một lớp học đang giờ hoạt động nhóm. GIỮA: một cái bàn tròn thấp, ba bạn nhỏ "
     "ngồi quanh — bạn bên trái áo vàng đang cầm quyển sách mở đọc, bạn giữa áo "
     "xanh đang viết vào quyển vở, bạn bên phải áo đỏ đang xếp mấy quân cờ trên "
     "bàn. HẬU CẢNH BÊN TRÁI: tấm bảng đen treo tường, mặt bảng ĐỂ TRỐNG. HẬU CẢNH "
     "BÊN PHẢI: cửa sổ nhìn ra tán cây xanh.",
     "This is my class. She's reading books. He likes doing projects. "
     "I like reading books. I can see a book.",
     "1. What school activity does he like? → He likes doing projects.  (mồi: He likes reading books. · He likes playing games. · He likes solving maths problems.)\n"
     "2. What can you see? → I can see a book.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · What's she doing? · What can you see?"),
8: C("Trên bàn học, đồ dùng để đâu",
     "Cận cảnh một góc lớp học nhìn chếch từ trên. GIỮA: một cái bàn học gỗ sáng "
     "màu. TRÊN MẶT BÀN, bày rõ ràng và tách rời nhau: một hộp bút vải xanh mở nắp "
     "nằm bên trái, hai cây SÁP MÀU đỏ và xanh nằm chéo ở giữa, một cái Ê KE nhựa "
     "trong nằm bên phải. DƯỚI GẦM BÀN: một chiếc cặp sách màu đỏ dựng sát chân "
     "bàn. BÊN TRÁI MÉP TRANH: một bạn gái đứng, tay chỉ xuống mấy cây sáp màu.",
     "This is my class. There's a desk. The crayons are on the desk. "
     "I have a set square. I can see a bag.",
     "1. Where are the crayons? → They're on the desk.  (mồi: They're above the desk. · They're beside the desk. · They're under the desk.)\n"
     "2. What do you have? → I have a set square.  (mồi: I have a glue stick. · I have a pencil sharpener. · I have a notebook.)",
     "Where are they? · Where are the crayons? · What do you have?"),
9: C("Ở sân chơi ngoài trời",
     "Một sân chơi ngoài trời, nền cỏ xanh, trời nắng. BÊN TRÁI: hai bạn nhỏ ngồi "
     "đối diện nhau hai bên một cái bàn thấp, trên bàn bày bàn cờ ô vuông đen "
     "trắng, một bạn đang đưa tay đi một quân cờ. BÊN PHẢI: một bạn gái đứng cạnh "
     "một BỂ CÁ hình chữ nhật đặt trên giá, trong bể có mấy con cá vàng bơi; bạn ấy "
     "chống tay lên đầu gối cúi nhìn vào bể. HẬU CẢNH: hàng rào gỗ thấp và mấy bụi "
     "cây xanh.",
     "This is our playground. He's playing chess. She's watching the fish. "
     "I sometimes play chess. I can see a fish.",
     "1. What's he doing? → He's playing chess.  (mồi: He's playing games. · He's reading books. · He's doing projects.)\n"
     "2. What can you see? → I can see a fish.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · What's he doing? · What can you see?"),
10: C("Chuyến đi của lớp, bên hồ",
     "Một bờ hồ rộng, trời trong. HẬU CẢNH: mặt hồ xanh phẳng, xa xa là dãy đồi "
     "thấp màu lam. GIỮA BỜ HỒ: ba bạn nhỏ đang đi bộ thành hàng dọc theo lối đi "
     "lát đá quanh hồ, bạn đi đầu giơ tay chỉ về phía mặt hồ. BÊN TRÁI: một bạn "
     "nhỏ đang quỳ một chân, hai tay đặt một cây con xuống hố đất nhỏ, cạnh đó là "
     "cái xẻng nhỏ. BÊN PHẢI: một ghế đá xám dưới bóng cây.",
     "This is a lake. We walked around the lake. He planted trees. "
     "I like our school. I can see a lake.",
     "1. What did you do? → We walked around the lake.  (mồi: We visited the old buildings. · We planted trees. · We played games.)\n"
     "2. What can you see? → I can see a lake.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · What did you do? · What can you see?"),
11: C("Bên bàn ăn, cả nhà xem ảnh chuyến đi",
     "Một phòng khách ấm cúng buổi tối. GIỮA: một cái bàn thấp, trên bàn đặt một "
     "quyển an-bum ảnh mở, trong an-bum thấy hai tấm ảnh nhỏ — một tấm chụp mặt "
     "biển có chiếc thuyền, một tấm chụp bãi cát có mấy vỏ sò. BÊN TRÁI: mẹ tóc "
     "búi, áo hồng, ngồi trên ghế sofa xám, một tay chỉ vào tấm ảnh chiếc thuyền. "
     "BÊN PHẢI: một bạn nhỏ ngồi trên sofa cạnh mẹ, nghiêng người nhìn vào an-bum. "
     "HẬU CẢNH: một cây đèn đứng toả ánh vàng ấm.",
     "This is my mother. We collected seashells. We walked on the beach. "
     "We took photos. I can see a photo.",
     "1. What did you do? → We collected seashells.  (mồi: We planted trees. · We played games. · We ate seafood.)\n"
     "2. Who's this? → It's my mother.  (mồi: It's my sister. · It's my brother. · It's my father.)",
     "Where are they? · What did your family do? · Who's this?"),
12: C("Chợ hoa ngày Tết",
     "Một góc chợ hoa ngày Tết, trời sáng. BÊN TRÁI: một sạp hoa bày những bó HOA "
     "HỒNG đỏ cắm trong xô nước. GIỮA: một cành ĐÀO nở hoa hồng nhạt cắm trong chậu "
     "gốm nâu, cao ngang đầu người. BÊN PHẢI: hai bạn nhỏ đứng cạnh nhau, bạn gái "
     "áo dài đỏ hai tay ôm một bó hoa hồng, bạn trai áo vàng giơ tay chỉ lên cành "
     "đào. HẬU CẢNH: dãy sạp hàng có mái vải đỏ, vài người lớn đi lại.",
     "This is the flower festival. I'll buy roses. We'll buy roses. "
     "We'll decorate the house. I can see a flower.",
     "1. What will you do for Tet? → We'll decorate the house.  (mồi: We'll make spring rolls. · We'll make banh chung. · We'll do the shopping.)\n"
     "2. What can you see? → I can see a flower.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · What will you do for Tet? · What can you see?"),
13: C("Sân trường ngày hội Trung thu",
     "Sân trường buổi tối ngày hội Trung thu. HẬU CẢNH: bầu trời tím sẫm có MẶT "
     "TRĂNG TRÒN vàng lớn treo cao. GIỮA SÂN: một cái bàn dài phủ khăn đỏ, trên bàn "
     "bày một đĩa BÁNH TRUNG THU hình tròn và mấy cốc nước hoa quả. BÊN TRÁI: hai "
     "bạn nhỏ đứng cạnh bàn, một bạn cầm chiếc đèn lồng ngôi sao đỏ giơ lên. BÊN "
     "PHẢI: một bạn nhỏ đang nhảy múa, hai tay giơ cao. HẬU CẢNH: dây cờ giấy nhiều "
     "màu căng ngang.",
     "This is the Mid-Autumn Festival. We'll have a party. "
     "We'll sing and dance. I can see a cake. I like the Mid-Autumn Festival.",
     "1. What will you do at the Mid-Autumn Festival? → We'll have a party.  (mồi: We'll make banh chung. · We'll watch the fireworks show. · We'll buy roses.)\n"
     "2. What can you see? → I can see a cake.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · What will you do? · What can you see?"),
14: C("Ở công viên buổi sáng sớm",
     "Một công viên buổi sáng sớm, nắng nhạt, cỏ xanh còn ướt sương. BÊN TRÁI: một "
     "bạn trai áo thể thao xanh đang chạy trên lối đi, người hơi ngả về trước. GIỮA: "
     "một bạn gái đứng trên tấm thảm tập, hai tay giơ lên chắp trước ngực, một chân "
     "co lên — dáng tập yoga. BÊN PHẢI: một cái bàn gỗ nhỏ, trên bàn có một cốc "
     "NƯỚC HOA QUẢ màu cam và một đĩa rau xanh. HẬU CẢNH: bụi cây và mấy con chim "
     "đậu trên hàng rào.",
     "This is our park. He does morning exercise every day. She does yoga. "
     "I drink fresh juice. I can see some juice.",
     "1. How does he stay healthy? → He does morning exercise.  (mồi: He does yoga. · He eats healthy food. · He drinks fresh juice.)\n"
     "2. What can you see? → I can see some juice.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · How does he stay healthy? · How often does he do morning exercise?"),
15: C("Ở phòng y tế của trường",
     "Phòng y tế trường học, tường trắng sạch. BÊN TRÁI: một chiếc giường thấp phủ "
     "ga trắng, một bạn nhỏ ngồi trên mép giường, một tay ôm lấy má, mặt nhăn — "
     "dáng đau răng. GIỮA: một cô y tá mặc áo blouse trắng đứng cạnh giường, một "
     "tay cầm cốc nước ấm đưa ra. BÊN PHẢI: một cái bàn nhỏ, trên bàn có hộp thuốc "
     "và cái cốc. HẬU CẢNH: cửa sổ có rèm trắng, một tấm biển chữ thập đỏ treo "
     "tường.",
     "This is our school. He has a toothache. She's a nurse. "
     "He should go to the dentist. I can see a cup.",
     "1. What's the matter? → He has a toothache.  (mồi: He has a headache. · He has a sore throat. · He has a stomach ache.)\n"
     "2. What should he do? → He should go to the dentist.  (mồi: He should go to the doctor. · He should go to the nurse. · He should have a rest.)",
     "Where are they? · What's the matter? · What should he do?"),
16: C("Bên cửa sổ lớp, ngày mùa đông",
     "Một góc lớp học ngày mùa đông. BÊN PHẢI: cửa sổ lớn, nhìn ra ngoài thấy bầu "
     "trời xám nhạt và mấy BÔNG TUYẾT trắng đang rơi, cành cây trơ lá. BÊN TRÁI: "
     "một tấm bảng thời tiết treo tường, chia bốn ô vuông vẽ bốn hình — mặt trời, "
     "đám mây, mây có mưa, bông tuyết; ô BÔNG TUYẾT được khoanh tròn màu đỏ. GIỮA: "
     "một bạn gái mặc ÁO LEN dày màu tím đứng cạnh cửa sổ, hai tay ôm lấy vai vì "
     "lạnh. TIỀN CẢNH: một bộ bàn học có quyển vở mở.",
     "This is my class. It's winter. It's cold today. "
     "I wear a jumper in winter. I like winter.",
     "1. How's the weather in Ha Noi in winter? → It's cold.  (mồi: It's hot. · It's cool. · It's warm.)\n"
     "2. What do you usually wear in winter? → I wear a jumper.  (mồi: I wear a coat. · I wear a blouse. · I wear jeans.)",
     "Where is she? · How's the weather? · What do you usually wear in winter?"),
17: C("Ở góc đọc truyện",
     "Một góc đọc sách trong thư viện trường. HẬU CẢNH: một giá sách gỗ thấp xếp "
     "đầy sách nhiều màu. BÊN TRÁI, trên tường: một bức tranh vẽ CON RÙA và CON THỎ "
     "đang chạy thi trên đường cỏ — con rùa nâu bò chậm phía trước, con thỏ trắng "
     "ngồi ngủ dưới gốc cây. GIỮA: một bạn gái ngồi trên tấm thảm tròn, hai tay cầm "
     "quyển sách mở, mắt nhìn xuống trang sách. BÊN PHẢI: một bạn trai ngồi khoanh "
     "chân, tay chỉ lên bức tranh con rùa.",
     "This is our library. That's a tortoise. That's a hare. "
     "The tortoise ran fast. I can see a book.",
     "1. Who are the main characters in the story? → They're the tortoise and the hare.  (mồi: They're the ant and the grasshopper. · They're the fox and the crow. · They're Snow White and seven dwarfs.)\n"
     "2. What can you see? → I can see a book.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · What can you see? · Who are the main characters?"),
18: C("Ở bến xe buýt trước cổng trường",
     "Một bến xe buýt trên vỉa hè trước cổng trường, trời sáng. BÊN PHẢI: một chiếc "
     "XE BUÝT màu vàng đang đỗ, cửa mở, nhìn thấy mấy hàng ghế bên trong. GIỮA: hai "
     "bạn nhỏ đeo cặp đứng chờ trên vỉa hè, bạn gái áo hồng giơ tay chỉ về phía xe "
     "buýt. BÊN TRÁI: một chiếc XE ĐẠP màu xanh dựng cạnh cột đèn, và một bạn nhỏ "
     "đang dắt xe. HẬU CẢNH: cổng trường sắt và dãy nhà học màu vàng.",
     "This is our school gate. I go to school by bus. She goes to school by bike. "
     "I can see a bus. I can see a bike.",
     "1. How can I get to school? → You can get there by bus.  (mồi: You can get there by train. · You can get there by taxi. · You can get there on foot.)\n"
     "2. What can you see? → I can see a bus.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · How do you go to school? · What can you see?"),
19: C("Trước tấm ảnh cầu Rồng",
     "Một góc lớp học. HẬU CẢNH: tấm bảng ghim lớn treo tường, trên ghim ba tấm ảnh "
     "— ảnh thứ nhất chụp một CÂY CẦU dài bắc qua sông, thành cầu uốn cong; ảnh thứ "
     "hai chụp một mặt HỒ phẳng có hàng cây quanh bờ; ảnh thứ ba chụp một TOÀ NHÀ "
     "cổ mái ngói. GIỮA: một bạn trai áo xanh đứng, tay chỉ vào tấm ảnh cây cầu. "
     "BÊN PHẢI: một bạn gái đứng nhìn theo, hai tay chắp sau lưng. TIỀN CẢNH: một "
     "cái bàn học có quyển vở mở.",
     "This is my class. That's Dragon Bridge. Dragon Bridge is beautiful. "
     "I'd like to visit Dragon Bridge. I can see a lake.",
     "1. What do you think of Dragon Bridge? → I think it's beautiful.  (mồi: I think it's exciting. · I think it's peaceful. · I think it's fantastic.)\n"
     "2. What can you see? → I can see a lake.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · What do you think of Dragon Bridge? · What can you see?"),
20: C("Ở bãi biển mùa hè",
     "Một bãi biển mùa hè, trời trong, nắng chói. HẬU CẢNH: mặt biển xanh có sóng "
     "trắng lăn tăn, chân trời phía xa, MẶT TRỜI vàng treo cao bên phải. GIỮA BÃI "
     "CÁT: một bạn gái đội mũ rộng vành đang cúi nhặt một VỎ SÒ, cạnh chân là mấy "
     "vỏ sò rải rác. BÊN TRÁI: một chiếc LỀU vải màu cam dựng trên cát, cạnh lều có "
     "một chiếc ba lô. BÊN PHẢI: một bạn trai đang bước đi trên mép nước, quần xắn "
     "cao. HẬU CẢNH BÊN TRÁI: một chiếc thuyền nhỏ neo gần bờ.",
     "This is the beach. We went camping last summer. She collected seashells. "
     "He walked on the beach. I can see a tent.",
     "1. What did your family do in Phu Quoc Island? → We went camping.  (mồi: We visited an eco-farm. · We practised swimming. · We ate seafood.)\n"
     "2. What can you see? → I can see a tent.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · What did you do last summer? · What can you see?"),
}


# ══════════════════════ BÀI ÔN TẬP CHƯƠNG — LỚP 5 ══════════════════════
L5C = {
1: C("Trước nhà mình, buổi chiều",
     "Trước một ngôi nhà hai tầng màu kem, sân cỏ xanh. BÊN TRÁI: ngôi nhà, cửa "
     "gỗ nâu. GIỮA: hai bạn nhỏ đứng cạnh nhau — bạn gái tóc dài áo hồng, bạn trai "
     "áo xanh. BÊN PHẢI: một luống hoa và một cây lớn. TIỀN CẢNH BÊN TRÁI: một "
     "chiếc xe đạp dựng cạnh tường.",
     "This is my house. My house is in the city. This is Lucy. "
     "She's from Australia. She's friendly. I often water the flowers. "
     "I want to be a writer. I can see a garden.",
     "1. What can you see? → I can see a garden.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. Where's she from? | Bạn Lucy đến từ nước nào? → She's from Australia.  (mồi: She's from Japan. · She's from America. · She's from Malaysia.)\n"
     "3. What do you want to be? | Lớn lên bạn nhỏ muốn làm nghề gì? → I want to be a writer.  (mồi: I want to be a reporter. · I want to be a gardener. · I want to be a firefighter.)\n"
     "4. What do you do at the weekend? | Cuối tuần bạn nhỏ làm gì? → I often water the flowers.  (mồi: I often go for a walk. · I often play the violin. · I often surf the Internet.)",
     "What can you see? · Where's she from? · What do you want to be?",
     "Ôn chương 1: nhà mình ở đâu · bạn nước ngoài · việc lúc rảnh · nghề muốn làm."),
2: C("Trong lớp, giờ làm dự án",
     "Một lớp học sáng, nhìn chếch xuống mặt bàn dài. TRÊN BÀN, xếp rời nhau: HAI "
     "cây sáp màu đỏ nằm ngang, một quyển sách mở. BÊN PHẢI phía sau: một giá sách "
     "thấp có mấy quyển sách đứng. BÊN TRÁI: một bạn gái tóc tết đứng chỉ tay vào "
     "mặt bàn. BÊN PHẢI: một bạn trai áo xanh ngồi đọc sách. HẬU CẢNH: một cửa sổ "
     "lớn nhìn ra cây xanh.",
     "This is our classroom. There's a desk. The crayons are on the desk. "
     "I like doing projects. It's interesting. He likes reading books. "
     "I can see a book. I like our school.",
     "1. What can you see? → I can see a book.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. Where are the crayons? | Mấy cây sáp màu để ở đâu? → They're on the desk.  (mồi: They're above the desk. · They're beside the desk. · They're under the desk.)\n"
     "3. What school activity does he like? | Bạn trai áo xanh thích hoạt động nào ở trường? → He likes reading books.  (mồi: He likes playing games. · He likes solving maths problems. · He likes playing chess.)\n"
     "4. How many crayons can you see? | Con thấy mấy cây sáp màu? → I can see two.  (mồi: I can see one. · I can see three. · I can see four.)",
     "What can you see? · Where are the crayons? · What school activity does he like?",
     "Ôn chương 2: phòng lớp · đồ dùng để đâu · hoạt động ở trường · đếm."),
3: C("Ở nhà, những ngày giáp Tết",
     "Một phòng khách ấm cúng ngày giáp Tết. BÊN TRÁI: một bạn gái đứng trên tấm "
     "thảm, hai tay chắp trước ngực, một chân co lên — dáng tập yoga. Đó là mẹ. "
     "GIỮA: một cái bàn gỗ thấp, trên bàn có một cốc nước hoa quả màu cam. BÊN "
     "PHẢI: một chiếc ghế sofa xám và một khung ảnh gia đình treo tường.",
     "This is my house. We'll decorate the house. We'll make banh chung. "
     "This is my mother. She does yoga every day. I drink fresh juice. "
     "I can see some juice. I like my house.",
     "1. What can you see? → I can see some juice.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. What will you do for Tet? | Tết này nhà bạn nhỏ sẽ làm gì? → We'll decorate the house.  (mồi: We'll buy roses. · We'll do the shopping. · We'll make spring rolls.)\n"
     "3. How does he stay healthy? | Mẹ bạn nhỏ giữ sức khoẻ bằng cách nào? → She does yoga.  (mồi: She does morning exercise. · She eats healthy food. · She eats vegetables.)\n"
     "4. Who's this? | Người lớn duy nhất trong tranh là ai? → It's my mother.  (mồi: It's my sister. · It's my brother. · It's my father.)",
     "What can you see? · Who's this? · What will you do for Tet?",
     "Ôn chương 3: gia đình · Tết · giữ sức khoẻ.\n"
     "⚠ Dòng phụ KHÔNG chốt bằng \"người đang tập yoga\": bút `nguoi` chỉ có dáng "
     "`gio` (hai tay giơ lên), nhìn ra reo mừng chứ không ra tập yoga — chốt bằng "
     "một thứ bé không đọc được trên tranh thì chốt hoá ra đánh đố.\n"
     "⚠ Mồi câu 2 KHÔNG được là `We'll make banh chung.` — chính đoạn đọc có câu "
     "ấy, nên nó cũng đúng. Đó là lỗi vừa phải vá ở bức U12."),
4: C("Trong thành phố một sáng mùa hè",
     "Một con phố trong thành phố, sáng mùa hè nắng gắt. HẬU CẢNH: hai toà nhà "
     "nhiều tầng màu kem. TRÊN CAO BÊN TRÁI: mặt trời. BÊN PHẢI: một chiếc xe buýt "
     "vàng đang đỗ sát vỉa hè. GIỮA: một bạn trai mặc áo thun ngắn tay đứng trên "
     "vỉa hè. BÊN TRÁI: một chiếc xe đạp dựng cạnh tường.",
     "This is my city. It's summer. It's hot today. "
     "I wear a T-shirt in summer. I go to school by bus. "
     "She goes to school by bicycle. I can see a bus. There's a bike.",
     "1. What can you see? → I can see a bus.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. How's the weather? | Trời hôm nay thế nào? → It's hot.  (mồi: It's cold. · It's cool. · It's warm.)\n"
     "3. How can I get to school? | Bạn nhỏ KỂ CHUYỆN đi học bằng gì? → You can get there by bus.  (mồi: You can get there by taxi. · You can get there on foot. · You can get there by train.)\n"
     "4. What do you usually wear in winter? | Mùa HÈ bạn nhỏ thường mặc gì? → I wear a T-shirt.  (mồi: I wear a coat. · I wear a jumper. · I wear jeans.)",
     "What can you see? · How's the weather? · How can I get to school?",
     "Ôn chương 4: mùa và thời tiết · quần áo theo mùa · đi lại bằng gì.\n"
     "⚠ Câu 3 KHÔNG được để mồi `by bicycle`/`by bike`: tranh vẽ CẢ xe buýt LẪN "
     "xe đạp, và đoạn nói cả hai — đúng lỗi vừa vá ở bức U18."),
}


LUAT = [
    ["BỐN LUẬT — bác chốt 20-08-2026", ""],
    ["", ""],
    ["1 · KHÔNG HỘI THOẠI",
     "Đoạn đọc là VĂN MÔ TẢ, chỉ có câu kể. Không có cặp “Hỏi? - Đáp.” nào. "
     "Mẫu câu HỎI của unit vẫn dùng — nhưng ở CÂU HỎI SAU BÀI và ở phòng nói, "
     "không nhét vào đoạn văn."],
    ["2 · VỐN TÍCH LUỸ TỪ LỚP 1",
     "Chữ và câu lấy từ lớp 1 cộng dồn tới đúng bài ấy, không bó trong từ của "
     "riêng unit. Nhờ vậy đoạn mới đủ chữ để tả một CẢNH."],
    ["3 · MỘT NƠI, MỘT LÚC",
     "Trả lời được “đây là chỗ nào” bằng một câu. Nhiều nhất 2–3 người. Đồ vật "
     "phải THUỘC VỀ chỗ ấy — lớp học thì bàn ghế bảng, không có con diều."],
    ["4 · KHÔNG NHÂN BẢN",
     "42 cảnh viết tay. Bộ sinh chỉ SOI (chữ đã học chưa · vật có hình chưa · "
     "câu hỏi trả lời được bằng đoạn không), KHÔNG quyết nội dung."],
    ["", ""],
    ["THỨ TỰ LÀM — trước đây tôi làm NGƯỢC", ""],
    ["① MÔ TẢ TRANH", "Chi tiết tới mức AI vẽ được: bố cục trái/giữa/phải, "
                      "tiền cảnh/hậu cảnh, tuổi và trang phục từng người, tư thế, "
                      "vị trí từng đồ vật, màu sắc. Ghi rõ chỗ nào ĐỂ TRỐNG."],
    ["② ĐOẠN ĐỌC", "Tả đúng những gì CÓ trong mô tả ấy."],
    ["③ CÂU HỎI", "Hỏi về thứ có trong mô tả. Mồi nhử CÙNG KHUÔN với đáp án."],
    ["④ NÓI · VIẾT", "Cùng dựa trên mô tả. Bảng từ màn VIẾT suy thẳng từ đoạn "
                     "đọc nên không bao giờ thiếu chữ."],
    ["", ""],
    ["⚠ VÌ SAO KHÔNG CÓ CHỮ TRONG TRANH",
     "Biển tên phố, tấm lịch, thời khoá biểu, bảng tên — đều ĐỂ TRỐNG. Bé đang "
     "tập đọc tiếng Anh; chữ in sẵn trên tranh là cho sẵn đáp án, và AI vẽ chữ "
     "thì gần như luôn sai chính tả."],
    ["", ""],
    ["PHÒNG NÓI — BA NHỊP, GIỐNG NHAU Ở MỌI BÀI", ""],
    ["Bé thấy gì", "CHỈ bức tranh. Không thấy đoạn văn."],
    ["Cô (AI) có gì", "Bản mô tả tranh bằng chữ — chính cột “ĐOẠN ĐỌC”."],
    ["Nhịp 1 · MỜI TẢ",
     "Cô: “Con nhìn bức tranh và tả cho cô nghe nhé.” Bé tự nói. Cô KHÔNG đọc đoạn ra."],
    ["Nhịp 2 · GỢI Ý",
     "Bé bí thì cô HỎI — dùng đúng câu ở cột “câu CÔ HỎI khi bé bí”. Bé ĐÁP, không "
     "nhại lại câu hỏi. Đáp sai thì cô nhắc lại CÂU HỎI trước, rồi mới tới chỗ lệch."],
    ["Nhịp 3 · CẢ ĐOẠN",
     "Cô xâu chuỗi mấy câu bé vừa nói, rồi mời bé nói LIỀN cả đoạn. Buổi chỉ xong "
     "khi bé nói được cả đoạn."],
    ["⚠ Chỗ từng hỏng",
     "Phòng nói từng chấm bé theo câu CÔ vừa nói, nên bé nhại lại câu hỏi “What "
     "can you see?” vẫn được 9/10. Nay mỗi lượt của cô mang theo danh sách câu "
     "ĐƯỢC TÍNH LÀ ĐÚNG."],
]


def main() -> int:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill

    wb = Workbook()
    ws = wb.active
    ws.title = "42 bài tả tranh"
    dau = ["Quyển", "Bài", "Chủ đề bài", "Bối cảnh",
           "① MÔ TẢ BỨC TRANH SẼ VẼ (để AI gen ảnh)",
           "② ĐOẠN ĐỌC — văn mô tả, KHÔNG hội thoại",
           "③ CÂU HỎI sau khi đọc",
           "④ NÓI · câu CÔ HỎI khi bé bí",
           "④ VIẾT · bảng từ gợi ý", "Ghi chú", "Bác duyệt"]
    ws.append(dau)
    for i, _ in enumerate(dau, 1):
        o = ws.cell(row=1, column=i)
        o.font = Font(bold=True, color="FFFFFF")
        o.fill = PatternFill("solid", fgColor="0B4EA8")
        o.alignment = Alignment(vertical="center", wrap_text=True)

    for lop, bang in ((3, L3), (4, L4)):
        c = json.loads((GOC / f"data/tienganh/chuan_lop{lop}.json").read_text("utf8"))
        ten = {u["so"]: u["canh"] for u in c["unit"]}
        for so in sorted(bang):
            k = bang[so]
            ws.append([f"lớp {lop}", f"U{so:02d}", ten.get(so, ""), k["noi"],
                       k["mo_ta"], k["doan"], k["hoi"], k["goi_y"],
                       tu_viet(k["doan"]), k["ghi"], ""])

    for cot, w in {"A": 8, "B": 6, "C": 26, "D": 28, "E": 78, "F": 52,
                   "G": 62, "H": 42, "I": 46, "J": 36, "K": 12}.items():
        ws.column_dimensions[cot].width = w
    for r in ws.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)
    ws.freeze_panes = "C2"

    w2 = wb.create_sheet("Luật · Phòng nói")
    for r in LUAT:
        w2.append(r)
    w2.column_dimensions["A"].width = 32
    w2.column_dimensions["B"].width = 94
    for row in w2.iter_rows():
        for o in row:
            o.alignment = Alignment(vertical="top", wrap_text=True)
    for dong in (1, 9, 17):
        w2.cell(row=dong, column=1).font = Font(bold=True, size=13)

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    print(f"→ {RA.relative_to(GOC)}  ({len(L3) + len(L4)} bài)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
