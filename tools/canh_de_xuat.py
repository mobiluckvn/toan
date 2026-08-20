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


def C(boi_canh, ai, do_vat, doan, ghi=""):
    return {"boi_canh": boi_canh, "ai": ai, "do_vat": do_vat, "doan": doan, "ghi": ghi}


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


def main() -> int:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill

    wb = Workbook()
    ws = wb.active
    ws.title = "Bối cảnh đề xuất"
    dau = ["Quyển", "Bài", "Chủ đề bài", "SÁCH dạy mẫu câu gì",
           "BỐI CẢNH đề xuất", "Ai · đang làm gì", "Đồ vật trong tranh",
           "ĐOẠN ĐỌC đề xuất", "Ghi chú", "Bác duyệt"]
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
                       k["boi_canh"], k["ai"], k["do_vat"], k["doan"], k["ghi"], ""])

    rong = {"A": 8, "B": 6, "C": 30, "D": 46, "E": 40, "F": 40, "G": 34, "H": 56,
            "I": 40, "J": 12}
    for cot, w in rong.items():
        ws.column_dimensions[cot].width = w
    for r in ws.iter_rows(min_row=2):
        for o in r:
            o.alignment = Alignment(vertical="top", wrap_text=True)
    ws.freeze_panes = "A2"

    RA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RA)
    print(f"→ {RA.relative_to(GOC)}  ({len(L3) + len(L4)} bài)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
