#!/usr/bin/env python3
"""BẢNG ĐỀ XUẤT BỐI CẢNH cho 42 bài tả tranh (lớp 3 · lớp 4) → Excel để bác duyệt.

    tools/tts/.venv/bin/python tools/canh_de_xuat.py

── HAI LẦN BÁC BẮT, ĐÂY LÀ BẢN THỨ BA ──

Lần 1: *"This is a friend. I can see a girl. That's a ball. […] Chủ đề bài là
Hello Again thì bạn nên vẽ một bối cảnh có người chào nhau."*
→ Tranh cũ là một DÃY KỆ ĐỰNG ĐỒ RỜI nên đoạn văn buộc phải thành bảng liệt kê.
Bác còn chỉ ra cái sai sâu hơn: làm mẫu một bài thì tốt, rồi tôi viết bộ
`soan_tranh_lopN.py` để NHÂN BẢN 20 bài còn lại — mà bộ ấy chỉ biết xoay bốn khuôn.

Lần 2: *"Bạn quá tham lam khi nhồi nhét quá nhiều thứ. Ví dụ U00 nếu bối cảnh
trong lớp thì tập trung vào bối cảnh trong lớp thôi. Có cô giáo, có bàn, có ghế,
có bảng. Và mô tả cái lớp đó. Cần gì số làm gì nữa."*
→ Bản hai vẫn tham: tôi ép mỗi bức phải dùng ĐỦ MỌI MẪU CÂU unit dạy, nên bức
"Khởi động" có cả thẻ số, cả con diều, cả cặp sách — ba chuyện trong một cảnh.

── LUẬT CỦA BẢN NÀY ──
1. MỘT NƠI, MỘT LÚC. Bức nào cũng trả lời được "đây là chỗ nào" bằng một câu.
2. NHIỀU NHẤT 2–3 NGƯỜI, mỗi người một việc.
3. ĐỒ VẬT chỉ lấy thứ VỐN CÓ Ở CHỖ ẤY — lớp học thì bàn ghế bảng, không có con diều.
4. ĐOẠN mở bằng "đây là chỗ nào / ai", rồi 2 lượt hỏi–đáp của chính unit.
   KHÔNG ép dùng hết mẫu câu; mẫu nào không hợp cảnh thì để cho phần luyện tập.
5. KHÔNG NHÂN BẢN. 42 cảnh viết tay, có trần.

⚠ Tệp này CHỈ đẻ ra bảng đề xuất để duyệt. Nó không sửa nội dung đang chạy.
"""
from __future__ import annotations

import json
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs/canh_de_xuat.xlsx"


def C(noi, ai, do_vat, doan, hoi, goi_y, ghi=""):
    return {"noi": noi, "ai": ai, "do_vat": do_vat, "doan": doan,
            "hoi": hoi, "goi_y": goi_y, "ghi": ghi}


# ══════════════════════════════ LỚP 3 ══════════════════════════════
L3 = {
0: C("Trong lớp học",
     "Cô giáo đứng cạnh bảng; hai bạn ngồi ở bàn",
     "bảng · hai cái bàn · ghế · cặp sách",
     "This is my classroom. This is my teacher. I can see two desks. "
     "I can see a board.",
     "1. What can you see? → I can see two desks.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. How many desks can you see? → I can see two.  (mồi: I can see one. · I can see three. · I can see four.)",
     "Where are you? · What can you see? · How many desks can you see?",
     "Bác chốt: cảnh trong lớp thì CHỈ có lớp — cô, bàn, ghế, bảng. Bỏ hẳn thẻ số "
     "và con diều của bản trước. Số đếm vẫn dùng được TỰ NHIÊN khi đếm bàn."),
1: C("Ở cổng trường buổi sáng",
     "Ben và Lucy gặp nhau, vẫy tay chào",
     "cổng trường · hai cặp sách · cái cây",
     "This is Ben. This is Lucy. Hello, Ben. Hello, Lucy. "
     "How are you? - Fine, thank you.",
     "1. Who is this? → This is Ben.  (mồi: This is Lucy. · This is Mai. · This is Minh.)\n"
     "2. How are you? → Fine, thank you.  (mồi: Hello, Ben. · Hello, Lucy. · Goodbye.)",
     "Who is this? · What does Ben say? · How are you?"),
2: C("Ở bàn học, hai bạn mới làm quen",
     "Mary và Minh ngồi cạnh nhau, trước mặt có bảng tên",
     "hai bảng tên · bàn học · hai cái ghế",
     "This is Mary. This is Minh. What's your name? - My name's Mary. "
     "How old are you? - I'm eight years old.",
     "1. What's your name? → My name's Mary.  (mồi: My name's Lucy. · My name's Minh. · My name's Ben.)\n"
     "2. How old are you? → I'm eight years old.  (mồi: I'm six years old. · I'm seven years old. · I'm nine years old.)",
     "Who is this? · What's your name? · How old are you?",
     "Bác gợi ý đúng kiểu này: hai người có TÊN ở đó, rồi tả họ."),
3: C("Ở sân trường, một bạn giới thiệu cô giáo",
     "Minh chỉ về phía cô Hoa; thầy Long đứng bên",
     "sân trường · ghế đá · cái cây",
     "This is Ms Hoa. This is Mr Long. Hello, Ms Hoa. "
     "Is this Mr Long? - Yes, it is.",
     "1. Who is this? → This is Ms Hoa.  (mồi: This is Mr Long. · This is Minh. · This is Mai.)\n"
     "2. Is this Mr Long? → Yes, it is.  (mồi: No, it isn't.)",
     "Who is this? · Is this Mr Long?"),
4: C("Trước tấm gương trong lớp",
     "Một bạn đứng soi gương; cô chỉ vào mũi bạn ấy",
     "tấm gương · khuôn mặt bạn nhỏ",
     "This is my face. What's this? - It's a nose. What's this? - It's an eye. "
     "Touch your face!",
     "1. What's this? → It's a nose.  (mồi: It's an eye. · It's a hand. · It's an ear.)\n"
     "2. What's this? → It's an eye.  (mồi: It's a nose. · It's a mouth. · It's a face.)",
     "What's this? · Touch your face!",
     "Bức cũ vẽ mắt-mũi-mồm RỜI trên kệ. Nay là MỘT khuôn mặt để cô chỉ vào."),
5: C("Ở góc sinh hoạt của lớp",
     "Một bạn đang nấu ăn giả; một bạn đang nhảy múa",
     "bếp đồ chơi · cái bàn",
     "What's your hobby? - It's cooking. She's dancing. I like singing.",
     "1. What's your hobby? → It's cooking.  (mồi: It's singing. · It's dancing. · It's running.)\n"
     "2. What's she doing? → She's dancing.  (mồi: She's cooking. · She's singing. · She's running.)",
     "What's your hobby? · What's she doing?"),
6: C("Ở hành lang trường, trước cửa các phòng",
     "Hai bạn đứng trước cửa lớp, một bạn chỉ tay",
     "cửa lớp học · cửa thư viện · hành lang",
     "This is our school. Is this our classroom? - Yes, it is. "
     "Let's go to the library. - OK, let's go.",
     "1. Is this our classroom? → Yes, it is.  (mồi: No, it isn't.)\n"
     "2. Where do they go? → Let's go to the library.  (mồi: Let's go to the gym. · Let's go to the playground. · Let's go to the classroom.)",
     "Is this our classroom? · Where do they go?"),
7: C("Ở cửa lớp, một bạn đến muộn",
     "Bạn đứng ở cửa xin phép; cô giáo gật đầu",
     "cửa lớp · bàn học · bảng",
     "This is my classroom. May I come in? - Yes, you can. Sit down, please!",
     "1. May I come in? → Yes, you can.  (mồi: No, you can't.)\n"
     "2. What does the teacher say? → Sit down, please!  (mồi: Come in, please! · Stand up, please! · Open your books, please!)",
     "May I come in? · What does the teacher say?"),
8: C("Trên mặt bàn học của bạn nhỏ",
     "Một bạn giơ cây bút; bạn bên cạnh hỏi mượn thước",
     "bút · thước · cục tẩy · hộp bút",
     "This is my desk. I have a pen. Do you have a ruler? - Yes, I do.",
     "1. What do you have? → I have a pen.  (mồi: I have a ruler. · I have a book. · I have an eraser.)\n"
     "2. Do you have a ruler? → Yes, I do.  (mồi: No, I don't.)",
     "What do you have? · Do you have a ruler?"),
9: C("Ở góc mĩ thuật",
     "Một bạn giơ quả bóng đỏ lên; cô hỏi màu",
     "quả bóng đỏ · cây bút xanh · hộp màu",
     "This is my ball. What colour is it? - It's red. "
     "This is my pen. What colour is it? - It's blue.",
     "1. What colour is it? → It's red.  (mồi: It's blue. · It's green. · It's yellow.)\n"
     "2. What colour is it? → It's blue.  (mồi: It's red. · It's black. · It's white.)",
     "What colour is it? · What can you see?"),
10: C("Ở sân trường giờ ra chơi",
     "Một nhóm đá bóng; hai bạn đánh cầu lông",
     "quả bóng đá · vợt cầu lông · sân trường",
     "This is our playground. I play football at break time. "
     "What do you do at break time? - I play badminton.",
     "1. What do you do at break time? → I play badminton.  (mồi: I play football. · I play chess. · I play basketball.)\n"
     "2. What can you see? → I can see a ball.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)",
     "Where are they? · What do you do at break time?"),
11: C("Trong phòng khách, cả nhà xem ảnh",
     "Bạn nhỏ chỉ vào ảnh chị gái; mẹ ngồi cạnh",
     "khung ảnh gia đình · ghế · cái bàn",
     "This is my family. Who's this? - It's my sister. "
     "Who's this? - It's my mother.",
     "1. Who's this? → It's my sister.  (mồi: It's my brother. · It's my mother. · It's my father.)\n"
     "2. Who's this? → It's my mother.  (mồi: It's my sister. · It's my brother. · It's my father.)",
     "Who's this? · How many people can you see?"),
12: C("Ở ngày hội nghề nghiệp của trường",
     "Một bác sĩ và một nông dân đứng ở gian của mình",
     "áo blouse · ống nghe · mũ nông dân",
     "What's her job? - She's a doctor. What's his job? - He's a farmer. "
     "Is he a nurse? - No, he isn't.",
     "1. What's her job? → She's a doctor.  (mồi: She's a nurse. · She's a farmer. · She's a teacher.)\n"
     "2. Is he a nurse? → No, he isn't.  (mồi: Yes, he is.)",
     "What's her job? · What's his job? · Is he a nurse?"),
13: C("Nhìn vào trong ngôi nhà, thấy các phòng",
     "Một bạn đứng ở cửa chỉ lên phòng ngủ",
     "phòng ngủ · nhà bếp · phòng tắm",
     "This is my house. Where's your bedroom? - It's here. "
     "Where are the chairs? - They're in the living room.",
     "1. Where's your bedroom? → It's here.  (mồi: It's there.)\n"
     "2. Where are the chairs? → They're in the living room.  (mồi: They're in the bedroom. · They're in the kitchen. · They're in the bathroom.)",
     "Where's your bedroom? · Where are the chairs?"),
14: C("Trong phòng ngủ của bạn nhỏ",
     "Bạn đứng giữa phòng, giới thiệu phòng mình",
     "giường · cửa sổ · cái chăn · cái đèn",
     "This is my bedroom. There's a bed in the room. "
     "There's a window in the room. The door is big.",
     "1. What's in the room? → There's a bed in the room.  (mồi: There's a desk in the room. · There's a chair in the room. · There's a lamp in the room.)\n"
     "2. Is the door big? → The door is big.  (mồi: The door is small.)",
     "What's in the room? · Is the door big?"),
15: C("Ở bàn ăn, mẹ mời khách",
     "Mẹ đưa đĩa bánh mì; hai bạn nhỏ ngồi ở bàn",
     "bàn ăn · bánh mì · cốc sữa",
     "This is my family. Would you like some bread? - Yes, please. "
     "Would you like some milk? - No, thanks.",
     "1. Would you like some bread? → Yes, please.  (mồi: No, thanks.)\n"
     "2. What would you like to eat? → I'd like some rice, please.  (mồi: I'd like some bread, please. · I'd like some fish, please. · I'd like some meat, please.)",
     "Would you like some bread? · What would you like to eat?"),
16: C("Ở góc thú nuôi",
     "Một bạn ôm con mèo; bạn kia dắt hai con chó",
     "con mèo · hai con chó · lồng chim",
     "This is my cat. Do you have any dogs? - Yes, I do. "
     "How many dogs do you have? - I have two.",
     "1. Do you have any dogs? → Yes, I do.  (mồi: No, I don't.)\n"
     "2. How many dogs do you have? → I have two.  (mồi: I have one. · I have three. · I have four.)",
     "Do you have any dogs? · How many dogs do you have?"),
17: C("Ở góc đồ chơi trong lớp",
     "Một bạn gái cầm con diều; một bạn trai cầm ô tô",
     "con diều · ô tô · con quay",
     "This is our toy box. She has a kite. He has a car. They have toys.",
     "1. What does she have? → She has a kite.  (mồi: She has a car. · She has a ship. · She has a plane.)\n"
     "2. What does he have? → He has a car.  (mồi: He has a kite. · He has a ship. · He has a top.)",
     "What does she have? · What does he have?"),
18: C("Trong phòng sinh hoạt chung",
     "Một bạn đang đọc sách; một bạn đang viết",
     "quyển sách · cây bút · cái bàn",
     "This is my room. I'm reading. What are you doing? - I'm writing.",
     "1. What are you doing? → I'm writing.  (mồi: I'm reading. · I'm singing. · I'm dancing.)\n"
     "2. What's he doing? → He's reading.  (mồi: He's writing. · He's singing. · He's dancing.)",
     "What are you doing? · What's he doing?"),
19: C("Ở sân chơi buổi chiều",
     "Một bạn đạp xe; một bạn nhảy dây",
     "xe đạp · dây nhảy · ghế đá",
     "This is our playground. She's cycling. "
     "What's she doing? - She's skipping.",
     "1. What's she doing? → She's skipping.  (mồi: She's cycling. · She's running. · She's walking.)\n"
     "2. What's she doing? → She's cycling.  (mồi: She's skipping. · She's running. · She's walking.)",
     "Where are they? · What's she doing?"),
20: C("Trong vườn thú, trước chuồng hổ",
     "Cô chỉ vào con hổ; một con khỉ đang đu cành",
     "chuồng thú · con hổ · con khỉ",
     "This is the zoo. What can you see? - I can see a tiger. "
     "What's the tiger doing? - It's swinging.",
     "1. What can you see? → I can see a tiger.  (mồi: I can see a dog. · I can see a cat. · I can see a duck.)\n"
     "2. What's the tiger doing? → It's swinging.  (mồi: It's running. · It's walking. · It's swimming.)",
     "What can you see? · What's the tiger doing?"),
}

# ══════════════════════════════ LỚP 4 ══════════════════════════════
# Dài hơn lớp 3 MỘT NHỊP — thêm một câu mở cảnh, KHÔNG thêm chuyện thứ hai.
L4 = {
0: C("Ở sân trường ngày tựu trường",
     "Hai bạn gặp lại nhau, bắt tay chào",
     "cổng trường · cặp sách · cái cây",
     "This is my school. This is Mary. This is Ben. "
     "Hello. How are you? - I'm fine, thank you.",
     "1. Who is this? → This is Mary.  (mồi: This is Ben. · This is Lucy. · This is Minh.)\n"
     "2. How are you? → I'm fine, thank you.  (mồi: I'm from Viet Nam. · I'm eight years old. · I'm a pupil.)",
     "Where are they? · Who is this? · How are you?",
     "BỨC BÁC CHÊ. Cũ: 'This is a friend. I can see a girl. That's a ball.' — không "
     "ai chào ai, lại nhét cả bóng, diều, mèo, mũ. Nay CHỈ CÒN CẢNH CHÀO."),
1: C("Ở trại hè, trước tấm bản đồ thế giới",
     "Một bạn hỏi bạn nước ngoài đến từ đâu",
     "bản đồ thế giới · ba lô · cái bàn",
     "This is my friend. Where are you from? - I'm from Viet Nam. "
     "Where's she from? - She's from Japan.",
     "1. Where are you from? → I'm from Viet Nam.  (mồi: I'm from Japan. · I'm from Britain. · I'm from Australia.)\n"
     "2. Where's she from? → She's from Japan.  (mồi: She's from Viet Nam. · She's from America. · She's from Thailand.)",
     "Where are you from? · Where's she from?",
     "⚠ Cờ quốc gia emoji VẼ RA RỖNG (phông không có). Cảnh dùng BẢN ĐỒ, không cờ."),
2: C("Trong phòng ngủ buổi sáng",
     "Bạn nhỏ vừa thức dậy, nhìn đồng hồ báo thức",
     "đồng hồ · giường · cặp sách",
     "This is my bedroom. What time is it? - It's six o'clock. "
     "What time do you get up? - I get up at six o'clock.",
     "1. What time is it? → It's six o'clock.  (mồi: It's eight o'clock. · It's six thirty. · It's eight thirty.)\n"
     "2. What time do you get up? → I get up at six o'clock.  (mồi: I get up at eight o'clock. · I get up at six thirty. · I get up at eight thirty.)",
     "Where is he? · What time is it? · What time do you get up?"),
3: C("Trong lớp, trước tấm lịch tuần treo tường",
     "Cô chỉ vào thứ Hai trên lịch; một bạn giơ tay đáp",
     "tấm lịch tuần · bảng · bàn học",
     "This is my classroom. What day is it today? - It's Monday. "
     "What do you do on Mondays? - I study at school.",
     "1. What day is it today? → It's Monday.  (mồi: It's Sunday. · It's Friday. · It's Tuesday.)\n"
     "2. What do you do on Mondays? → I study at school.  (mồi: I listen to music. · I do housework. · I watch TV.)",
     "What day is it today? · What do you do on Mondays?"),
4: C("Ở bàn tiệc sinh nhật",
     "Bạn nhỏ thổi nến; mẹ hỏi khách muốn ăn gì",
     "bánh sinh nhật · chùm nho · cốc nước ép",
     "This is my birthday party. When's your birthday? - It's in May. "
     "What do you want to eat? - I want some jam.",
     "1. When's your birthday? → It's in May.  (mồi: It's in June. · It's in April. · It's in March.)\n"
     "2. What do you want to eat? → I want some jam.  (mồi: I want some chips. · I want some grapes. · I want some bread.)",
     "Where are they? · When's your birthday? · What do you want to eat?"),
5: C("Ở góc tài năng của lớp",
     "Một bạn đạp xe; một bạn đang vẽ",
     "xe đạp · giá vẽ · hộp màu",
     "This is my friend. Can you ride a bike? - Yes, I can. "
     "Can she swim? - No, she can't, but she can draw.",
     "1. Can you ride a bike? → Yes, I can.  (mồi: No, I can't.)\n"
     "2. Can she swim? → No, she can't, but she can draw.  (mồi: Yes, she can.)",
     "Can you ride a bike? · Can she swim? · What can she do?"),
6: C("Nhìn toàn cảnh sân trường",
     "Một bạn dẫn bạn mới đi một vòng, chỉ từng khu",
     "dãy nhà học · thư viện · sân chơi",
     "This is my school. Where's your school? - It's in the city. "
     "How many buildings are there at your school? - There are three.",
     "1. Where's your school? → It's in the city.  (mồi: It's in the town. · It's in the village. · It's in the countryside.)\n"
     "2. How many buildings are there at your school? → There are three.  (mồi: There are two. · There are four. · There are five.)",
     "Where's your school? · How many buildings are there?"),
7: C("Trong lớp, trước thời khoá biểu dán tường",
     "Hai bạn cùng dò thời khoá biểu; một bạn chỉ vào tiết Toán",
     "thời khoá biểu · sách Toán · cặp sách",
     "This is my classroom. What subjects do you have today? - "
     "I have English and maths. When do you have maths? - I have it on Mondays.",
     "1. What subjects do you have today? → I have English and maths.  (mồi: I have art and music. · I have science and art. · I have maths and music.)\n"
     "2. When do you have maths? → I have it on Mondays.  (mồi: I have it on Fridays. · I have it on Tuesdays. · I have it on Sundays.)",
     "What subjects do you have today? · When do you have maths?"),
8: C("Ở góc trưng bày môn Mĩ thuật của lớp",
     "Một bạn đứng cạnh bức tranh mình vẽ, kể vì sao thích môn ấy",
     "bảng màu · bức tranh · giá vẽ",
     "This is my classroom. What's your favourite subject? - It's art. "
     "Why do you like art? - Because I want to be a painter.",
     "1. What's your favourite subject? → It's art.  (mồi: It's maths. · It's music. · It's science.)\n"
     "2. Why do you like art? → Because I want to be a painter.  (mồi: Because I want to be a singer. · Because I want to be a teacher. · Because I want to be a doctor.)",
     "What's your favourite subject? · Why do you like art?"),
9: C("Ở ngày hội thể thao trên sân trường",
     "Các bạn chạy thi; cô cầm tấm huy chương",
     "huy chương · quả bóng đá · băng rôn",
     "This is our sports day. When's your sports day? - It's in October. "
     "Is your sports day in May? - No, it isn't.",
     "1. When's your sports day? → It's in October.  (mồi: It's in May. · It's in June. · It's in July.)\n"
     "2. Is your sports day in May? → No, it isn't.  (mồi: Yes, it is.)",
     "Where are they? · When's your sports day? · Is your sports day in May?"),
10: C("Trước bảng ảnh kì nghỉ hè treo ở lớp",
     "Một bạn chỉ vào ảnh của mình, kể hè vừa rồi ở đâu",
     "ảnh bãi biển · ảnh vùng quê · bảng ghim",
     "This is my photo. Where were you last summer? - I was in Tokyo. "
     "Were you at the beach? - Yes, I was.",
     "1. Where were you last summer? → I was in Tokyo.  (mồi: I was in London. · I was in Sydney. · I was in Bangkok.)\n"
     "2. Were you at the beach? → Yes, I was.  (mồi: No, I wasn't.)",
     "Where were you last summer? · Were you at the beach?"),
11: C("Trên con phố trước nhà bạn nhỏ",
     "Bạn dẫn bạn khác về nhà, chỉ vào biển tên phố",
     "biển tên phố · ngôi nhà · cái cây",
     "This is my street. Where do you live? - I live in Tran Hung Dao Street. "
     "What's the street like? - It's a busy street.",
     "1. Where do you live? → I live in Tran Hung Dao Street.  (mồi: cùng khuôn, đổi tên phố)\n"
     "2. What's the street like? → It's a busy street.  (mồi: It's a quiet street. · It's a noisy street. · It's a big street.)",
     "Where do you live? · What's the street like?"),
12: C("Ở bệnh viện, nơi mẹ bạn nhỏ làm việc",
     "Mẹ mặc áo blouse đứng ở cửa phòng khám; bạn nhỏ đứng cạnh",
     "áo blouse · ống nghe · biển bệnh viện",
     "This is my mother. What does she do? - She's a doctor. "
     "Where does she work? - She works at a hospital.",
     "1. What does she do? → She's a doctor.  (mồi: She's a nurse. · She's a teacher. · She's a farmer.)\n"
     "2. Where does she work? → She works at a hospital.  (mồi: She works at a school. · She works at a factory. · She works at a nursing home.)",
     "Who is this? · What does she do? · Where does she work?",
     "Bản trước dựng 'ngày hội nghề nghiệp' nhồi năm nghề vào một bức. "
     "Nay MỘT người, MỘT nơi làm việc."),
13: C("Trước tấm ảnh lớp treo ở cuối phòng",
     "Một bạn chỉ vào ảnh, tả bạn trong ảnh cho cô nghe",
     "tấm ảnh lớp · khung ảnh",
     "This is my friend. What does he look like? - He's tall. "
     "What does she look like? - She has long hair.",
     "1. What does he look like? → He's tall.  (mồi: He's short. · He's slim. · He's big.)\n"
     "2. What does she look like? → She has long hair.  (mồi: She has short hair. · She has a round face. · She has big eyes.)",
     "Who is this? · What does he look like? · What does she look like?",
     "Bức cũ vẽ mắt-mũi-mồm-tay RỜI. Nay là NGƯỜI trong ảnh để tả."),
14: C("Trong nhà buổi sáng",
     "Bạn nhỏ đang lau sàn; ti vi tắt ở góc phòng",
     "cây lau nhà · ti vi · ghế",
     "This is my home. What do you do in the morning? - I clean the floor. "
     "When do you watch TV? - I watch TV in the evening.",
     "1. What do you do in the morning? → I clean the floor.  (mồi: I wash the dishes. · I wash the clothes. · I cook meals.)\n"
     "2. When do you watch TV? → I watch TV in the evening.  (mồi: I watch TV in the morning. · I watch TV at noon. · I watch TV in the afternoon.)",
     "What is he doing? · What do you do in the morning? · When do you watch TV?"),
15: C("Trước trung tâm thể thao, sáng thứ Bảy",
     "Bố đi vào trung tâm thể thao; bạn nhỏ đứng ngoài",
     "biển trung tâm thể thao · quả bóng · xe đạp",
     "This is my father. Where does he go on Saturdays? - "
     "He goes to the sports centre. What does he do on Sundays? - He plays tennis.",
     "1. Where does he go on Saturdays? → He goes to the sports centre.  (mồi: He goes to the cinema. · He goes to the gym. · He goes to the swimming pool.)\n"
     "2. What does he do on Sundays? → He plays tennis.  (mồi: He does yoga. · He watches films. · He cooks meals.)",
     "Who is this? · Where does he go on Saturdays? · What does he do on Sundays?"),
16: C("Bên cửa sổ lớp học, cạnh bảng thời tiết",
     "Cô gắn hình mặt trời lên bảng thời tiết; ngoài cửa sổ trời nắng",
     "bảng thời tiết · hình mặt trời · cửa sổ",
     "This is my classroom. What was the weather like last weekend? - It was sunny. "
     "Do you want to go to the water park? - Great! Let's go.",
     "1. What was the weather like last weekend? → It was sunny.  (mồi: It was rainy. · It was windy. · It was cloudy.)\n"
     "2. Do you want to go to the water park? → Great! Let's go.  (mồi: Sorry, I can't.)",
     "What was the weather like? · Do you want to go to the water park?",
     "⚠ Tính từ thời tiết KHÔNG vẽ thành vật rời được. Phải là BẢNG THỜI TIẾT."),
17: C("Ở một ngã tư trong phố",
     "Một bạn hỏi đường; bác đi đường chỉ tay rẽ trái",
     "biển STOP · hiệu sách · ô tô",
     "This is my city. What does it say? - It says stop. "
     "How can I get to the bookshop? - Go straight and turn left.",
     "1. What does it say? → It says stop.  (mồi: It says go straight. · It says turn left. · It says turn right.)\n"
     "2. How can I get to the bookshop? → Go straight and turn left.  (mồi: Go straight and turn right.)",
     "Where is he? · What does it say? · How can I get to the bookshop?"),
18: C("Trong trung tâm mua sắm, trước hiệu sách",
     "Một bạn hỏi hiệu sách ở đâu; bạn kia chỉ sang cạnh hiệu bánh",
     "hiệu sách · hiệu bánh mì · áo thun",
     "This is the shopping centre. Where's the bookshop? - It's near the bakery. "
     "How much is the T-shirt? - It's sixty thousand dong.",
     "1. Where's the bookshop? → It's near the bakery.  (mồi: It's opposite the bakery. · It's behind the bakery. · It's between the bakery.)\n"
     "2. How much is the T-shirt? → It's sixty thousand dong.  (mồi: cùng khuôn, đổi số)",
     "Where are they? · Where's the bookshop? · How much is the T-shirt?"),
19: C("Trong vườn thú, trước chuồng hươu cao cổ",
     "Cô chỉ vào đàn hươu cao cổ; một con công đang múa bên cạnh",
     "chuồng thú · hươu cao cổ · con công",
     "This is the zoo. What are these animals? - They're giraffes. "
     "Why do you like peacocks? - Because they dance beautifully.",
     "1. What are these animals? → They're giraffes.  (mồi: They're lions. · They're hippos. · They're peacocks.)\n"
     "2. Why do you like peacocks? → Because they dance beautifully.  (mồi: Because they roar loudly. · Because they run quickly. · Because they sing merrily.)",
     "Where are they? · What are these animals? · Why do you like peacocks?"),
20: C("Ở trại hè bên hồ, buổi tối",
     "Một bạn nhóm lửa trại; nhóm bạn ngồi hát quanh đống lửa",
     "lều · đống lửa · cây đàn ghi ta",
     "This is our summer camp. What's he doing? - He's building a campfire. "
     "What are they doing? - They're singing songs.",
     "1. What's he doing? → He's building a campfire.  (mồi: He's putting up a tent. · He's taking a photo. · He's telling a story.)\n"
     "2. What are they doing? → They're singing songs.  (mồi: They're playing card games. · They're playing tug of war. · They're dancing.)",
     "Where are they? · What's he doing? · What are they doing?"),
}


LUAT = [
    ["LUẬT DỰNG CẢNH — bác chốt 20-08-2026", ""],
    ["", ""],
    ["1 · MỘT NƠI, MỘT LÚC",
     "Bức nào cũng trả lời được “đây là chỗ nào” bằng một câu. Bác: “nếu bối cảnh "
     "trong lớp thì tập trung vào bối cảnh trong lớp thôi.”"],
    ["2 · NHIỀU NHẤT 2–3 NGƯỜI", "Mỗi người một việc. Không dựng đám đông."],
    ["3 · ĐỒ VẬT PHẢI THUỘC VỀ CHỖ ẤY",
     "Lớp học thì bàn · ghế · bảng. KHÔNG có con diều, quả bóng, con mèo chỉ vì "
     "chúng có trong bảng từ vựng."],
    ["4 · KHÔNG ÉP DÙNG HẾT MẪU CÂU",
     "Đoạn mở bằng “đây là chỗ nào / ai”, rồi 2 lượt hỏi–đáp của unit. Mẫu nào "
     "không hợp cảnh thì để dành cho phần luyện tập. Bác: “Cần gì số làm gì nữa.”"],
    ["5 · KHÔNG NHÂN BẢN",
     "42 cảnh viết tay. Bộ sinh chỉ SOI (chữ đã học chưa · khuôn đúng sách chưa · "
     "vật có hình chưa), KHÔNG quyết nội dung."],
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
    ["KHÔNG có gì khác",
     "Không bước chào, không bước từ mới, không mẫu câu, không thẻ “con thích cái "
     "nào nhất”, không bảng “con nói về”."],
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
    ws.title = "Bối cảnh đề xuất"
    dau = ["Quyển", "Bài", "Chủ đề bài", "SÁCH dạy mẫu câu gì",
           "BỐI CẢNH · một nơi một lúc", "Ai · đang làm gì",
           "Đồ vật (chỉ thứ vốn có ở đó)", "ĐOẠN ĐỌC đề xuất",
           "CÂU HỎI sau khi đọc", "NÓI · câu CÔ HỎI khi bé bí", "Ghi chú", "Bác duyệt"]
    ws.append(dau)
    for i, _ in enumerate(dau, 1):
        o = ws.cell(row=1, column=i)
        o.font = Font(bold=True, color="FFFFFF")
        o.fill = PatternFill("solid", fgColor="0B4EA8")
        o.alignment = Alignment(vertical="center", wrap_text=True)

    for lop, bang in ((3, L3), (4, L4)):
        c = json.loads((GOC / f"data/tienganh/chuan_lop{lop}.json").read_text("utf8"))
        ten = {u["so"]: u["canh"] for u in c["unit"]}
        mau = {u["so"]: " | ".join(m.get("vi_du") or m.get("cong_thuc") or ""
                                   for m in u["mau_cau"]) for u in c["unit"]}
        for so in sorted(bang):
            k = bang[so]
            ws.append([f"lớp {lop}", f"U{so:02d}", ten.get(so, ""), mau.get(so, ""),
                       k["noi"], k["ai"], k["do_vat"], k["doan"],
                       k["hoi"], k["goi_y"], k["ghi"], ""])

    for cot, w in {"A": 8, "B": 6, "C": 26, "D": 40, "E": 34, "F": 38, "G": 30,
                   "H": 54, "I": 66, "J": 44, "K": 40, "L": 12}.items():
        ws.column_dimensions[cot].width = w
    for r in ws.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)
    ws.freeze_panes = "A2"

    w2 = wb.create_sheet("Luật · Phòng nói")
    for r in LUAT:
        w2.append(r)
    w2.column_dimensions["A"].width = 34
    w2.column_dimensions["B"].width = 92
    for row in w2.iter_rows():
        for o in row:
            o.alignment = Alignment(vertical="top", wrap_text=True)
    w2["A1"].font = Font(bold=True, size=13)
    w2["A9"].font = Font(bold=True, size=13)

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    print(f"→ {RA.relative_to(GOC)}  ({len(L3) + len(L4)} bài)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
