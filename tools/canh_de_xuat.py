#!/usr/bin/env python3
"""BẢNG ĐỀ XUẤT BỐI CẢNH cho 42 bài tả tranh (lớp 3 · lớp 4) → Excel để bác duyệt.

    tools/tts/.venv/bin/python tools/canh_de_xuat.py

── VÌ SAO CÓ TỆP NÀY ──
Bác bắt đúng chỗ hỏng nặng nhất, 20-08-2026:

    "This is a friend. I can see a girl. That's a ball. […] Nội dung này không hề
     phù hợp là một bài đọc. Một bức tranh rất vớ vẩn. Chủ đề bài là Hello Again
     thì bạn nên vẽ một bối cảnh có người chào nhau."

Và bác chỉ ra cái sai sâu hơn: làm mẫu MỘT bài thì tốt, nhưng rồi tôi viết bộ
`soan_tranh_lopN.py` để NHÂN BẢN 20 bài còn lại — mà bộ ấy chỉ biết lấy danh sách
từ vựng xoay bốn khuôn `This is a … / I can see a …`. Bức mẫu là một CẢNH; hai
mươi bức nhân ra là hai mươi BẢNG LIỆT KÊ.

Thông tin để dựng một cảnh KHÔNG nằm trong danh sách từ vựng. Nên phần "cảnh này
vẽ gì, đoạn này nói gì" phải viết TAY cho từng bài — 42 bài, có trần, không nhân
bản. Máy giữ đúng phần máy làm được: soi chữ đã học chưa, khuôn đúng sách chưa,
vật có hình chưa.

⚠ Tệp này CHỈ đẻ ra bảng đề xuất để duyệt. Nó không sửa nội dung đang chạy.
"""
from __future__ import annotations

import json
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
RA = GOC / "docs/canh_de_xuat.xlsx"


def C(boi_canh, ai, do_vat, doan, ghi="", hoi="", goi_y="", dich=""):
    """`hoi`  — câu hỏi sau khi ĐỌC (đáp án · mồi nhử).
    `goi_y`  — câu CÔ HỎI ở phòng nói khi bé bí. Không phải câu bắt bé nhại.
    `dich`   — đoạn bé phải nói được ở nhịp cuối. Trống thì lấy chính `doan`."""
    return {"boi_canh": boi_canh, "ai": ai, "do_vat": do_vat, "doan": doan,
            "ghi": ghi, "hoi": hoi, "goi_y": goi_y, "dich": dich or doan}


# ══════════════════════════ LỚP 3 ══════════════════════════
L3 = {
0: C("Lớp học buổi đầu năm, trên bảng treo mấy tấm thẻ SỐ",
     "Cô giáo chỉ vào một tấm thẻ; một bạn giơ tay đáp",
     "thẻ số 1–5 · bảng · bàn học · cặp sách",
     "This is my classroom. What number is it? - It's five. "
     "What number is it? - It's two. I can see five kites.",
     "Unit chỉ dạy đọc số, nên cảnh phải có CHỖ để đọc số — tấm thẻ trên bảng."),
1: C("Cổng trường buổi sáng, hai bạn gặp nhau",
     "Ben vẫy tay chào Lucy; phía sau có bạn khác đang chào tạm biệt mẹ",
     "cổng trường · cặp sách · cây · con mèo",
     "Hello. I'm Ben. Hello, Ben. I'm Lucy. How are you? - Fine, thank you. Goodbye.",
     "Đây đúng cảnh unit dạy: gặp · chào · hỏi thăm · tạm biệt."),
2: C("Góc lớp, hai bạn mới làm quen, có bảng tên trên bàn",
     "Mary hỏi tên bạn ngồi cạnh; bạn kia chỉ vào bảng tên của mình",
     "bảng tên · bàn học · bút · quyển vở",
     "What's your name? - My name's Mary. How old are you? - I'm eight years old.",
     ""),
3: C("Sân trường giờ ra chơi, một bạn giới thiệu cô giáo với bạn mới",
     "Minh chỉ tay về phía cô Hoa đang đứng; thầy Long đi ngang qua",
     "sân trường · ghế đá · cây · quả bóng",
     "This is Ms Hoa. Is this Mr Long? - Yes, it is. Hello, Ms Hoa.",
     ""),
4: C("Trước tấm gương trong lớp, cô dạy các bộ phận trên mặt",
     "Cô chỉ vào mũi mình; hai bạn sờ lên mặt làm theo",
     "gương · khuôn mặt bạn nhỏ · bàn · ghế",
     "What's this? - It's a nose. What's this? - It's an eye. Touch your face!",
     "Bức cũ vẽ mắt-mũi-mồm rời trên kệ. Phải là NGƯỜI có mặt, cô chỉ vào."),
5: C("Góc sở thích của lớp, mỗi bạn đang làm một việc mình thích",
     "Một bạn đang nấu ăn giả, một bạn đang hát, một bạn đang nhảy múa",
     "bếp đồ chơi · micro · bàn · quyển sách",
     "What's your hobby? - It's cooking. What's your hobby? - I like singing. "
     "She's dancing.",
     ""),
6: C("Hành lang trường, hai bạn đứng trước cửa các phòng",
     "Một bạn chỉ vào cửa lớp và hỏi; bạn kia rủ sang thư viện",
     "cửa lớp học · thư viện · phòng máy tính · nhà thể chất",
     "Is this our classroom? - Yes, it is. Let's go to the library. - OK, let's go.",
     ""),
7: C("Cửa lớp, một bạn đến muộn xin phép vào",
     "Bạn đứng ở cửa giơ tay xin phép; cô giáo gật đầu; cả lớp đang ngồi",
     "cửa lớp · bàn học · bảng · cặp sách",
     "May I come in? - Yes, you can. Come in, please! Sit down, please!",
     ""),
8: C("Mặt bàn học bày đồ dùng, hai bạn đổi đồ cho nhau",
     "Một bạn giơ cây bút lên khoe; bạn kia hỏi mượn thước",
     "bút · thước · cục tẩy · quyển vở · hộp bút · cặp sách",
     "I have a pen. Do you have a ruler? - Yes, I do. This is my pencil case.",
     ""),
9: C("Góc mĩ thuật, các bạn cầm đồ vật nhiều màu",
     "Một bạn giơ quả bóng đỏ; cô hỏi màu; bạn khác cầm bút xanh",
     "quả bóng đỏ · bút xanh · quyển vở vàng · hộp màu",
     "What colour is it? - It's red. What colour is it? - It's blue. "
     "What colour are they? - They're green.",
     "Bức cũ xếp bốn vật đủ màu lên kệ mà không ai hỏi ai."),
10: C("Sân trường giờ ra chơi, mỗi nhóm chơi một trò",
     "Nhóm đá bóng, hai bạn đánh cầu lông, hai bạn ngồi chơi cờ",
     "quả bóng đá · vợt cầu lông · bàn cờ · ghế đá",
     "I play football at break time. What do you do at break time? - I play chess. "
     "She plays badminton.",
     ""),
11: C("Phòng khách nhà bạn nhỏ, cả nhà xem ảnh chung",
     "Bạn chỉ vào ảnh chị gái; bố mẹ ngồi cạnh; em trai đứng bên",
     "khung ảnh gia đình · ghế · bàn · đèn",
     "Who's this? - It's my sister. Who's this? - It's my father. "
     "How old is he? - He's twenty years old.",
     ""),
12: C("Ngày hội nghề nghiệp ở trường, mỗi người mặc đồng phục nghề mình",
     "Bác sĩ, y tá, nông dân, công nhân đứng thành hàng; một bạn hỏi cô",
     "áo blouse · ống nghe · mũ bảo hộ · bảng tên nghề",
     "What's her job? - She's a doctor. Is he a doctor? - No, he isn't. "
     "He's a farmer.",
     ""),
13: C("Mặt cắt ngôi nhà nhìn từ ngoài vào, thấy các phòng",
     "Một bạn đứng ở cửa chỉ lên phòng ngủ; mẹ ở bếp",
     "phòng ngủ · nhà bếp · phòng tắm · ghế · đèn",
     "Where's your bedroom? - It's here. Where are the chairs? - "
     "They're in the living room.",
     ""),
14: C("Trong phòng ngủ của bạn nhỏ",
     "Bạn đứng giữa phòng giới thiệu đồ đạc của mình",
     "giường · cửa sổ · bàn học · cái chăn · đèn",
     "There's a bed in the room. The door is big. There's a window in the room.",
     ""),
15: C("Bàn ăn gia đình, mẹ mời bạn của con ở lại ăn",
     "Mẹ đưa đĩa bánh mì mời; hai bạn nhỏ ngồi ở bàn",
     "bàn ăn · bánh mì · bát cơm · cốc nước · ấm trà",
     "Would you like some bread? - Yes, please. "
     "What would you like to eat? - I'd like some rice, please.",
     ""),
16: C("Góc thú nuôi, hai bạn khoe con vật nhà mình",
     "Một bạn ôm con mèo; bạn kia dắt con chó; lồng chim treo bên",
     "con mèo · con chó · lồng chim · bể cá vàng",
     "Do you have any dogs? - Yes, I do. How many dogs do you have? - I have some. "
     "I have a cat.",
     ""),
17: C("Góc đồ chơi trong lớp, các bạn chia nhau đồ chơi",
     "Một bạn gái cầm con diều; nhóm bạn bày đồ chơi ra bàn",
     "con diều · ô tô · tàu thuỷ · con quay · máy bay",
     "She has a kite. They have toys. He has a car.",
     ""),
18: C("Trong phòng sinh hoạt chung, mỗi bạn đang làm một việc",
     "Một bạn đang đọc sách, một bạn đang hát, một bạn đang viết",
     "quyển sách · cây bút · quả bóng · bàn",
     "I'm reading. What are you doing? - I'm singing. He's writing.",
     ""),
19: C("Công viên buổi chiều, các bạn chơi ngoài trời",
     "Một bạn đạp xe, một bạn nhảy dây, một bạn chạy, một bạn đi bộ",
     "xe đạp · dây nhảy · ghế đá · cây",
     "She's cycling. What's she doing? - She's skipping. He's running.",
     ""),
20: C("Trong vườn thú, cả lớp đứng trước chuồng thú",
     "Cô chỉ vào con hổ; một con khỉ đang đu cành; các bạn nhìn theo",
     "chuồng thú · con hổ · con voi · con khỉ · con ngựa",
     "What can you see? - I can see a tiger. "
     "What's the tiger doing? - It's swinging. I can see an elephant.",
     ""),
}

# ══════════════════════════ LỚP 4 ══════════════════════════
L4 = {
0: C("Sân trường ngày tựu trường, các bạn gặp lại nhau sau hè",
     "Hai bạn bắt tay chào hỏi; một bạn dẫn bạn mới đến giới thiệu; "
     "phía xa vài bạn đang bơi ở bể bơi trường",
     "cổng trường · xe đạp dựng bên · con mèo · cái mũ · quả bóng",
     "Hello. How are you? - I'm fine, thank you. This is Mary. Nice to see you. "
     "What are they doing? - They're swimming.",
     "BỨC BÁC CHÊ. Cũ: 'This is a friend. I can see a girl. That's a ball.' — "
     "không ai chào ai. Đồ vật vẫn còn nhưng là CHI TIẾT của cảnh."),
1: C("Trại hè quốc tế, các bạn cầm cờ nước mình đứng cạnh bản đồ thế giới",
     "Một bạn hỏi bạn nước ngoài đến từ đâu; bạn kia chỉ lên bản đồ",
     "bản đồ thế giới · cờ các nước · ba lô · bàn",
     "Where are you from? - I'm from Viet Nam. Where's she from? - "
     "She's from Japan. This is my friend.",
     "⚠ Cờ emoji VẼ RA RỖNG (phông không có). Cờ ở đây phải VẼ TAY hoặc bỏ."),
2: C("Phòng ngủ buổi sáng, đồng hồ báo thức reo",
     "Bạn nhỏ vừa thức dậy nhìn đồng hồ; mẹ gọi ăn sáng ở phòng bên",
     "đồng hồ · giường · cặp sách · bàn ăn sáng · cốc sữa",
     "What time is it? - It's six o'clock. What time do you get up? - "
     "I get up at six o'clock. What time do you have breakfast? - "
     "I have breakfast at six thirty.",
     ""),
3: C("Trước tấm lịch tuần treo tường ở lớp",
     "Cô chỉ vào thứ Hai trên lịch; các bạn kể việc mình làm hôm ấy",
     "tấm lịch tuần · bảng · bàn học · quyển sách",
     "What day is it today? - It's Monday. What do you do on Mondays? - "
     "I study at school. What do you do on Sundays? - I listen to music.",
     ""),
4: C("Tiệc sinh nhật ở nhà, bàn bày bánh và đồ ăn",
     "Bạn nhỏ thổi nến; mẹ hỏi khách muốn ăn gì; các bạn ngồi quanh bàn",
     "bánh sinh nhật · khoai tây rán · chùm nho · lọ mứt · cốc nước ép",
     "When's your birthday? - It's in May. What do you want to eat? - "
     "I want some jam. Happy birthday!",
     ""),
5: C("Ngày hội tài năng của lớp, mỗi bạn trổ một tài",
     "Một bạn đạp xe, một bạn đánh đàn ghi ta, một bạn vẽ, một bạn bơi",
     "xe đạp · đàn ghi ta · giá vẽ · bể bơi",
     "Can you ride a bike? - Yes, I can. Can she swim? - No, she can't, "
     "but she can draw. He can play the guitar.",
     ""),
6: C("Toàn cảnh sân trường nhìn từ trên, thấy các khu",
     "Một bạn dẫn bạn mới đi một vòng, chỉ từng khu",
     "dãy nhà học · thư viện · sân chơi · nhà thể chất · vườn trường",
     "Where's your school? - It's in the city. "
     "How many buildings are there at your school? - There are three. "
     "This is our library.",
     ""),
7: C("Trước thời khoá biểu dán trên tường lớp",
     "Hai bạn cùng dò thời khoá biểu, một bạn chỉ vào tiết Toán",
     "thời khoá biểu · sách Toán · sách Tiếng Anh · cặp · bút",
     "What subjects do you have today? - I have English and maths. "
     "When do you have maths? - I have it on Mondays.",
     ""),
8: C("Góc trưng bày của lớp, mỗi môn một bàn nhỏ",
     "Các bạn đứng cạnh bàn môn mình thích và nói lý do",
     "bảng màu · nốt nhạc · kính hiển vi · quả bóng · máy tính",
     "What's your favourite subject? - It's art. Why do you like art? - "
     "Because I want to be a painter.",
     ""),
9: C("Ngày hội thể thao trên sân trường, cờ và băng rôn",
     "Các bạn thi chạy, đá bóng, ném bóng rổ; cô cầm tấm lịch báo tháng",
     "quả bóng đá · bóng rổ · bóng chuyền · huy chương · tấm lịch",
     "When's your sports day? - It's in October. "
     "Is your sports day in May? - No, it isn't. It's in October.",
     ""),
10: C("Bảng ảnh kì nghỉ hè treo ở lớp, mỗi ảnh một nơi",
     "Các bạn chỉ vào ảnh của mình và kể hè vừa rồi ở đâu",
     "ảnh bãi biển · ảnh vùng quê · ảnh trại hè · lều · ba lô",
     "Where were you last summer? - I was in Tokyo. "
     "Were you in the countryside last weekend? - Yes, I was.",
     ""),
11: C("Con phố trước nhà bạn nhỏ, có biển tên đường",
     "Bạn dẫn bạn khác về nhà, chỉ vào biển tên phố",
     "biển tên phố · ngôi nhà · cây · xe đạp · con đường",
     "Where do you live? - I live in Tran Hung Dao Street. "
     "What's the street like? - It's a busy street.",
     ""),
12: C("Ngày hội nghề nghiệp, mỗi người đứng ở gian của nghề mình",
     "Bác sĩ ở gian bệnh viện, nông dân ở gian trang trại, "
     "người làm vườn ở gian vườn trường",
     "áo blouse · ống nghe · mũ vành · bình tưới · mũ bảo hộ",
     "What does she do? - She's a doctor. Where does she work? - "
     "She works at a hospital. What does he do? - He's a gardener.",
     ""),
13: C("Bảng ảnh cả lớp, các bạn tả nhau",
     "Một bạn chỉ vào ảnh và tả bạn trong ảnh cho cô nghe",
     "khung ảnh · khuôn mặt các bạn · bảng · bàn",
     "What does he look like? - He's tall. What does she look like? - "
     "She has long hair. She has a round face.",
     "Bức cũ vẽ mắt-mũi-mồm-tay rời. Phải là NGƯỜI để tả."),
14: C("Mặt cắt ngôi nhà một ngày, bốn góc là bốn buổi",
     "Sáng bạn lau nhà, trưa mẹ nấu ăn, chiều bạn rửa bát, tối cả nhà xem ti vi",
     "cây lau nhà · nồi · chậu bát · ti vi · ghế",
     "What do you do in the morning? - I clean the floor. "
     "When do you watch TV? - I watch TV in the evening.",
     ""),
15: C("Cuối tuần, các thành viên trong nhà mỗi người một nơi",
     "Bố đi trung tâm thể thao, mẹ ở nhà tập yoga, anh đi rạp phim",
     "trung tâm thể thao · rạp chiếu phim · bể bơi · thảm tập",
     "Where does he go on Saturdays? - He goes to the sports centre. "
     "What does she do on Sundays? - She does yoga.",
     ""),
16: C("Cửa sổ lớp học nhìn ra ngoài, bảng thời tiết treo bên",
     "Cô gắn hình mặt trời lên bảng thời tiết; ngoài cửa sổ trời nắng; "
     "một bạn rủ bạn khác đi công viên nước",
     "bảng thời tiết · hình mặt trời · mây · con diều · cửa sổ",
     "What was the weather like last weekend? - It was sunny. "
     "Do you want to go to the water park? - Great! Let's go.",
     "⚠ Tính từ thời tiết KHÔNG vẽ thành vật rời được. Phải là BẢNG THỜI TIẾT "
     "và cảnh ngoài cửa sổ."),
17: C("Ngã tư trong phố, có biển báo và người hỏi đường",
     "Một bạn hỏi đường bác đi đường; bác chỉ tay rẽ trái; biển STOP ở góc",
     "biển STOP · biển chỉ đường · hiệu sách · siêu thị · ô tô",
     "What does it say? - It says stop. How can I get to the bookshop? - "
     "Go straight and turn left.",
     ""),
18: C("Trong trung tâm mua sắm, các cửa hàng nằm cạnh nhau",
     "Một bạn hỏi hiệu sách ở đâu; bạn kia chỉ sang bên cạnh hiệu bánh; "
     "một bạn cầm áo hỏi giá",
     "hiệu sách · hiệu bánh mì · cửa hàng quần áo · áo thun · biển giá tiền",
     "Where's the bookshop? - It's near the bakery. "
     "How much is the T-shirt? - It's sixty thousand dong.",
     ""),
19: C("Trong vườn thú, mấy chuồng thú cạnh nhau",
     "Cô chỉ vào đàn hươu cao cổ; một con công đang múa; sư tử gầm",
     "chuồng thú · hươu cao cổ · công · sư tử · hà mã · cá sấu",
     "What are these animals? - They're giraffes. Why do you like peacocks? - "
     "Because they dance beautifully.",
     ""),
20: C("Trại hè bên hồ, buổi tối quanh đống lửa",
     "Một bạn dựng lều, một bạn nhóm lửa, nhóm bạn chơi kéo co, "
     "vài bạn ngồi hát quanh lửa",
     "lều · đống lửa · dây kéo co · hồ nước · máy ảnh",
     "What's he doing? - He's building a campfire. "
     "What are they doing? - They're playing tug of war.",
     ""),
}


# (unit) → (câu hỏi sau khi đọc, câu CÔ HỎI gợi ý ở phòng nói)
H3 = {
0: ("1. What number is it? → It's five.  (mồi: It's two. · It's four. · It's three.)\n"
    "2. What can you see? → I can see five kites.  (mồi: I can see a dog. · a cat. · a duck.)",
    "What number is it? · How many kites can you see? · What can you see?"),
1: ("1. What's his name? → I'm Ben.  (mồi: I'm Minh. · I'm Nam. · I'm Bill.)\n"
    "2. How are you? → Fine, thank you.  (mồi: I'm Ben. · Goodbye. · Hello.)",
    "Who says hello? · What does Ben say? · How are you?"),
2: ("1. What's your name? → My name's Mary.  (mồi: My name's Lucy. · Minh. · Ben.)\n"
    "2. How old are you? → I'm eight years old.  (mồi: I'm six · seven · nine years old.)",
    "What's her name? · How old is she?"),
3: ("1. Who's this? → This is Ms Hoa.  (mồi: This is Mr Long. · Ms Mai. · Mr Nam.)\n"
    "2. Is this Mr Long? → Yes, it is.  (mồi: No, it isn't.)",
    "Who's this? · Is this Mr Long?"),
4: ("1. What's this? → It's a nose.  (mồi: It's an eye. · a hand. · an ear.)\n"
    "2. What's this? → It's an eye.  (mồi: It's a nose. · a mouth. · a face.)",
    "What's this? · Touch your face! · What can you see?"),
5: ("1. What's your hobby? → It's cooking.  (mồi: It's singing. · dancing. · running.)\n"
    "2. What's she doing? → She's dancing.  (mồi: She's cooking. · singing. · running.)",
    "What's your hobby? · What's she doing? · Do you like singing?"),
6: ("1. Is this our classroom? → Yes, it is.  (mồi: No, it isn't.)\n"
    "2. Where do they go? → Let's go to the library.  (mồi: to the gym · playground · classroom)",
    "Is this our classroom? · Where's the library?"),
7: ("1. May I come in? → Yes, you can.  (mồi: No, you can't.)\n"
    "2. What does the teacher say? → Sit down, please!  (mồi: Come in, please! · Stand up, please! · Open your books, please!)",
    "May I come in? · What does the teacher say?"),
8: ("1. What do you have? → I have a pen.  (mồi: I have a ruler. · a book. · an eraser.)\n"
    "2. Do you have a ruler? → Yes, I do.  (mồi: No, I don't.)",
    "What do you have? · Do you have a ruler?"),
9: ("1. What colour is it? → It's red.  (mồi: It's blue. · green. · yellow.)\n"
    "2. What colour are they? → They're green.  (mồi: They're red. · blue. · black.)",
    "What colour is it? · What colour are they?"),
10: ("1. What do you do at break time? → I play chess.  (mồi: I play football. · badminton. · basketball.)\n"
     "2. What does she do at break time? → She plays badminton.  (mồi: She plays football. · chess. · basketball.)",
     "What do you do at break time? · What does she play?"),
11: ("1. Who's this? → It's my sister.  (mồi: It's my brother. · mother. · father.)\n"
     "2. How old is he? → He's twenty years old.  (mồi: He's ten · twelve · eleven years old.)",
     "Who's this? · How old is he?"),
12: ("1. What's her job? → She's a doctor.  (mồi: She's a nurse. · a farmer. · a teacher.)\n"
     "2. Is he a doctor? → No, he isn't.  (mồi: Yes, he is.)",
     "What's her job? · Is he a doctor? · What's his job?"),
13: ("1. Where's your bedroom? → It's here.  (mồi: It's there.)\n"
     "2. Where are the chairs? → They're in the living room.  (mồi: in the bedroom · kitchen · bathroom)",
     "Where's your bedroom? · Where are the chairs?"),
14: ("1. What's in the room? → There's a bed in the room.  (mồi: There's a desk · a chair · a lamp in the room.)\n"
     "2. Is the door big? → The door is big.  (mồi: The door is small.)",
     "What's in the room? · Is the door big?"),
15: ("1. Would you like some bread? → Yes, please.  (mồi: No, thanks.)\n"
     "2. What would you like to eat? → I'd like some rice, please.  (mồi: some bread · some fish · some meat, please)",
     "Would you like some bread? · What would you like to eat?"),
16: ("1. Do you have any dogs? → Yes, I do.  (mồi: No, I don't.)\n"
     "2. How many dogs do you have? → I have some.  (mồi: I have one. · two. · three.)",
     "Do you have any dogs? · How many dogs do you have? · What can you see?"),
17: ("1. What does she have? → She has a kite.  (mồi: She has a car. · a ship. · a plane.)\n"
     "2. What do they have? → They have toys.  (mồi: They have books. · balls. · kites.)",
     "What does she have? · What do they have?"),
18: ("1. What are you doing? → I'm singing.  (mồi: I'm reading. · writing. · dancing.)\n"
     "2. What's he doing? → He's writing.  (mồi: He's reading. · singing. · dancing.)",
     "What are you doing? · What's he doing?"),
19: ("1. What's she doing? → She's skipping.  (mồi: She's cycling. · running. · walking.)\n"
     "2. What's he doing? → He's running.  (mồi: He's cycling. · skipping. · walking.)",
     "What's she doing? · What's he doing?"),
20: ("1. What can you see? → I can see a tiger.  (mồi: I can see a dog. · a cat. · a duck.)\n"
     "2. What's the tiger doing? → It's swinging.  (mồi: It's running. · walking. · swimming.)",
     "What can you see? · What's the tiger doing?"),
}

H4 = {
0: ("1. Who is this? → This is Mary.  (mồi: Ben. · Lucy. · Minh.)\n"
    "2. What are they doing? → They're swimming.  (mồi: running. · dancing. · reading.)",
    "How are you? · Who is this? · What are they doing?"),
1: ("1. Where are you from? → I'm from Viet Nam.  (mồi: I'm from Japan. · Britain. · Australia.)\n"
    "2. Where's she from? → She's from Japan.  (mồi: She's from Viet Nam. · America. · Thailand.)",
    "Where are you from? · Where's she from?"),
2: ("1. What time is it? → It's six o'clock.  (mồi: It's eight o'clock. · six thirty. · eight thirty.)\n"
    "2. What time do you get up? → I get up at six o'clock.  (mồi: at eight o'clock · at six thirty · at eight thirty)",
    "What time is it? · What time do you get up? · What time do you have breakfast?"),
3: ("1. What day is it today? → It's Monday.  (mồi: It's Sunday. · Friday. · Tuesday.)\n"
    "2. What do you do on Mondays? → I study at school.  (mồi: I listen to music. · do housework. · watch TV.)",
    "What day is it today? · What do you do on Mondays?"),
4: ("1. When's your birthday? → It's in May.  (mồi: It's in June. · April. · March.)\n"
    "2. What do you want to eat? → I want some jam.  (mồi: some chips · some grapes · some bread)",
    "When's your birthday? · What do you want to eat?"),
5: ("1. Can you ride a bike? → Yes, I can.  (mồi: No, I can't.)\n"
    "2. Can she swim? → No, she can't, but she can draw.  (mồi: Yes, she can.)",
    "Can you ride a bike? · Can she swim? · What can he do?"),
6: ("1. Where's your school? → It's in the city.  (mồi: It's in the town. · village. · countryside.)\n"
    "2. How many buildings are there at your school? → There are three.  (mồi: There are two. · four. · five.)",
    "Where's your school? · How many buildings are there?"),
7: ("1. What subjects do you have today? → I have English and maths.  (mồi: art and music · science and art · maths and music)\n"
    "2. When do you have maths? → I have it on Mondays.  (mồi: on Fridays · Tuesdays · Sundays)",
    "What subjects do you have today? · When do you have maths?"),
8: ("1. What's your favourite subject? → It's art.  (mồi: It's maths. · music. · science.)\n"
    "2. Why do you like art? → Because I want to be a painter.  (mồi: a singer · a teacher · a doctor)",
    "What's your favourite subject? · Why do you like art?"),
9: ("1. When's your sports day? → It's in October.  (mồi: It's in May. · June. · July.)\n"
    "2. Is your sports day in May? → No, it isn't.  (mồi: Yes, it is.)",
    "When's your sports day? · Is your sports day in May?"),
10: ("1. Where were you last summer? → I was in Tokyo.  (mồi: I was in London. · Sydney. · Bangkok.)\n"
     "2. Were you in the countryside last weekend? → Yes, I was.  (mồi: No, I wasn't.)",
     "Where were you last summer? · Were you at the beach?"),
11: ("1. Where do you live? → I live in Tran Hung Dao Street.  (mồi: khác tên phố, cùng khuôn)\n"
     "2. What's the street like? → It's a busy street.  (mồi: It's a quiet · noisy · big street.)",
     "Where do you live? · What's the street like?"),
12: ("1. What does she do? → She's a doctor.  (mồi: She's a nurse. · a teacher. · a farmer.)\n"
     "2. Where does she work? → She works at a hospital.  (mồi: at a school · at a factory · on a farm)",
     "What does she do? · Where does she work?"),
13: ("1. What does he look like? → He's tall.  (mồi: He's short. · slim. · big.)\n"
     "2. What does she look like? → She has long hair.  (mồi: She has short hair. · a round face. · big eyes.)",
     "What does he look like? · What does she look like?"),
14: ("1. What do you do in the morning? → I clean the floor.  (mồi: I wash the dishes. · wash the clothes. · cook meals.)\n"
     "2. When do you watch TV? → I watch TV in the evening.  (mồi: in the morning · at noon · in the afternoon)",
     "What do you do in the morning? · When do you watch TV?"),
15: ("1. Where does he go on Saturdays? → He goes to the sports centre.  (mồi: to the cinema · gym · swimming pool)\n"
     "2. What does she do on Sundays? → She does yoga.  (mồi: She plays tennis. · watches films. · cooks meals.)",
     "Where does he go on Saturdays? · What does she do on Sundays?"),
16: ("1. What was the weather like last weekend? → It was sunny.  (mồi: It was rainy. · windy. · cloudy.)\n"
     "2. Do you want to go to the water park? → Great! Let's go.  (mồi: Sorry, I can't.)",
     "What was the weather like? · Do you want to go to the water park?"),
17: ("1. What does it say? → It says stop.  (mồi: It says go straight. · turn left. · turn right.)\n"
     "2. How can I get to the bookshop? → Go straight and turn left.  (mồi: … and turn right.)",
     "What does it say? · How can I get to the bookshop?"),
18: ("1. Where's the bookshop? → It's near the bakery.  (mồi: It's opposite · behind · between the bakery.)\n"
     "2. How much is the T-shirt? → It's sixty thousand dong.  (mồi: khác số, cùng khuôn)",
     "Where's the bookshop? · How much is the T-shirt?"),
19: ("1. What are these animals? → They're giraffes.  (mồi: They're lions. · hippos. · peacocks.)\n"
     "2. Why do you like peacocks? → Because they dance beautifully.  (mồi: they roar loudly · run quickly · sing merrily)",
     "What are these animals? · Why do you like peacocks?"),
20: ("1. What's he doing? → He's building a campfire.  (mồi: He's putting up a tent. · taking a photo. · telling a story.)\n"
     "2. What are they doing? → They're playing tug of war.  (mồi: They're playing card games. · singing songs. · dancing.)",
     "What's he doing? · What are they doing?"),
}


# Cặp đáp mẫu của sách — KHÔNG áp luật "mồi cùng khuôn với đáp án", vì chính sách
# dạy chúng thành cặp: Có/Không · nhận lời/từ chối.
YES_NO = ("Yes,", "No,", "Great!", "Sorry,")


def moi_du(hoi: str) -> str:
    """Viết ĐỦ CÂU cho mồi nhử.

    ⚠ Bác duyệt thì phải thấy câu bé sẽ nhìn thấy. Viết tắt kiểu
    "(mồi: It's an eye. · a hand. · an ear.)" thì che mất đúng thứ cần soi: mồi có
    CÙNG KHUÔN với đáp án không. Lớp 3 từng có 33 câu mà đáp án là lựa chọn DUY
    NHẤT mang khuôn của nó — bé chọn đúng bằng mắt, không cần đọc.

    Cặp Có/Không (Yes… / No…) thì KHÔNG áp luật cùng khuôn: đó là cặp đáp mẫu
    hợp lệ của chính sách.
    """
    import re as _re

    def sua(m):
        dap, moi = m.group(1).strip(), [x.strip() for x in m.group(2).split("·")]
        nd = dap.split()
        ra = []
        for x in moi:
            nx = x.split()
            if x.startswith(YES_NO) or x.startswith(("khác", "…")) or len(nx) >= len(nd):
                ra.append(x)
            else:
                ra.append(" ".join(nd[:len(nd) - len(nx)] + nx))
        return f"→ {dap}  (mồi: {' · '.join(ra)})"

    return _re.sub(r"→ (.+?)\s+\(mồi: (.+?)\)", sua, hoi)


def main() -> int:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill

    wb = Workbook()
    ws = wb.active
    ws.title = "Bối cảnh đề xuất"
    dau = ["Quyển", "Bài", "Chủ đề bài", "SÁCH dạy mẫu câu gì",
           "BỐI CẢNH đề xuất", "Ai · đang làm gì", "Đồ vật trong tranh",
           "ĐOẠN ĐỌC đề xuất", "CÂU HỎI sau khi đọc",
           "NÓI · câu CÔ HỎI khi bé bí", "NÓI · đoạn bé phải nói được",
           "Ghi chú", "Bác duyệt"]
    ws.append(dau)
    for i, _ in enumerate(dau, 1):
        o = ws.cell(row=1, column=i)
        o.font = Font(bold=True, color="FFFFFF")
        o.fill = PatternFill("solid", fgColor="0B4EA8")
        o.alignment = Alignment(vertical="center", wrap_text=True)

    for bang, hoi in ((L3, H3), (L4, H4)):
        for so, k in bang.items():
            if so in hoi:
                k["hoi"], k["goi_y"] = moi_du(hoi[so][0]), hoi[so][1]

    for lop, bang in ((3, L3), (4, L4)):
        c = json.loads((GOC / f"data/tienganh/chuan_lop{lop}.json").read_text("utf8"))
        ten = {u["so"]: u["canh"] for u in c["unit"]}
        mau = {u["so"]: " | ".join(m.get("vi_du") or m.get("cong_thuc") or ""
                                   for m in u["mau_cau"]) for u in c["unit"]}
        for so in sorted(bang):
            k = bang[so]
            ws.append([f"lớp {lop}", f"U{so:02d}", ten.get(so, ""), mau.get(so, ""),
                       k["boi_canh"], k["ai"], k["do_vat"], k["doan"],
                       k["hoi"], k["goi_y"], k["dich"], k["ghi"], ""])

    rong = {"A": 8, "B": 6, "C": 28, "D": 42, "E": 38, "F": 38, "G": 30, "H": 52,
            "I": 62, "J": 44, "K": 52, "L": 38, "M": 12}
    for cot, w in rong.items():
        ws.column_dimensions[cot].width = w
    for r in ws.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)
    ws.freeze_panes = "A2"

    w2 = wb.create_sheet("Phòng nói chạy thế nào")
    for r in [
        ["PHÒNG NÓI — BA NHỊP, GIỐNG NHAU Ở MỌI BÀI", ""],
        ["", ""],
        ["Bé thấy gì", "CHỈ bức tranh. Không thấy đoạn văn."],
        ["Cô (AI) có gì", "Bản mô tả tranh bằng chữ — cột “đoạn bé phải nói được”."],
        ["", ""],
        ["Nhịp 1 · MỜI TẢ", "Cô: “Con nhìn bức tranh và tả cho cô nghe nhé.” "
                            "Bé tự nói. Cô KHÔNG đọc đoạn ra."],
        ["Nhịp 2 · GỢI Ý", "Bé bí thì cô HỎI — dùng đúng câu ở cột “câu CÔ HỎI khi bé bí”. "
                           "Bé ĐÁP, không nhại lại câu hỏi. Đáp sai thì cô nhắc lại CÂU HỎI trước, "
                           "rồi mới tới chỗ lệch."],
        ["Nhịp 3 · CẢ ĐOẠN", "Cô xâu chuỗi mấy câu bé vừa nói, rồi mời bé nói LIỀN cả đoạn. "
                             "Buổi chỉ xong khi bé nói được cả đoạn."],
        ["", ""],
        ["KHÔNG có gì khác", "Không bước chào, không bước từ mới, không mẫu câu, "
                             "không thẻ “con thích cái nào nhất”, không bảng “con nói về”."],
        ["Vì sao", "Bác chốt 19-08-2026: “Chỉ để một bức tranh sau đó yêu cầu học sinh mô tả "
                   "bức tranh… Đừng làm những thứ khác ngoài mấy thứ đó ra.”"],
        ["", ""],
        ["⚠ Chỗ từng hỏng", "Phòng nói từng chấm điểm bé theo câu CÔ vừa nói, nên bé nhại lại "
                             "câu hỏi “What can you see?” vẫn được 9/10. Nay mỗi lượt của cô mang "
                             "theo danh sách câu ĐƯỢC TÍNH LÀ ĐÚNG."],
    ]:
        w2.append(r)
    w2.column_dimensions["A"].width = 26
    w2.column_dimensions["B"].width = 96
    for row in w2.iter_rows():
        for o in row:
            o.alignment = Alignment(vertical="top", wrap_text=True)
    w2["A1"].font = Font(bold=True, size=13)

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    print(f"→ {RA.relative_to(GOC)}  ({len(L3) + len(L4)} bài)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
