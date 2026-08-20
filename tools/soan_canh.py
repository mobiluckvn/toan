#!/usr/bin/env python3
"""SOẠN BẢN KHAI 42 CẢNH → data/tienganh/canh_lop3.json · canh_lop4.json

    tools/tts/.venv/bin/python tools/soan_canh.py

Nội dung chữ (đoạn đọc · câu hỏi · câu gợi ý · mô tả tranh) lấy thẳng từ
`tools/canh_de_xuat.py` — chính bảng bác đã duyệt. KHÔNG chép tay sang đây:
chép tay là mở ra hai bản sự thật rồi lệch nhau lúc nào không biết, đúng cái
bẫy [[ban-dung-lai-de-mat-ban-sua-tay]].

Tệp này thêm phần bảng ấy không có: BỐ CỤC — nền gì, vật nào, đặt ở đâu.

── VÌ SAO BỐ CỤC VIẾT TAY TỪNG BÀI ──
Bác chỉ ra cái sai sâu nhất của lần trước: *"Vấn đề là làm mẫu xong bạn nhân
bản một cách không chấp nhận được à."* Bức mẫu làm tay thì tốt; rồi tôi viết bộ
nhân bản 20 bài còn lại, mà bộ ấy chỉ biết xếp đồ lên ba cái kệ. Nên ở đây
KHÔNG có vòng lặp nào sinh ra bố cục. 42 cảnh, 42 khối khai tay.

Toạ độ: khung 1280×720, dải tiêu đề chiếm 96 điểm trên cùng. Người khai theo
BÀN CHÂN. Vật khai trước nằm DƯỚI vật khai sau — nên hậu cảnh viết trước.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "tools"))
from canh_de_xuat import L3, L4  # noqa: E402

XANH, DO, VANG, LUC, TIM, TRANG = ("#3D8BD4", "#E4574C", "#F9B233",
                                   "#1FCBAB", "#7E57C2", "#FFFFFF")
QUAN = "#2F4A6B"

# ══════════════════════════════ LỚP 3 ══════════════════════════════
B3 = {
0: ("Trong lớp học", "In the classroom", {"kieu": "lop", "san": 556}, [
    {"ve": "bang", "x": 100, "y": 148, "w": 400, "h": 236},
    {"ve": "cuaSo", "x": 940, "y": 150, "w": 280, "h": 200},
    {"ve": "nguoi", "x": 620, "y": 556, "cao": 252, "ao": XANH, "vay_ao": QUAN,
     "toc_dai": True, "dang": "chi", "huong": -1},
    {"ve": "ghe", "x": 900, "y": 646, "cao": 108},
    {"ve": "nguoi", "x": 900, "y": 646, "cao": 182, "ao": DO, "dang": "ngoi", "huong": 1},
    {"ve": "ban", "x": 900, "y": 646, "w": 208, "cao": 118},
    {"tu": "book", "x": 900, "y": 512, "co": 50},
    {"ve": "ghe", "x": 320, "y": 714, "cao": 128},
    {"ve": "nguoi", "x": 320, "y": 714, "cao": 214, "ao": VANG, "vay_ao": TIM,
     "tet": True, "dang": "ngoi", "huong": 1},
    {"ve": "ban", "x": 320, "y": 714, "w": 248, "cao": 144},
    {"tu": "book", "x": 320, "y": 546, "co": 58},
    {"tu": "bag", "x": 556, "y": 686, "co": 84},
]),
1: ("Ở cổng trường buổi sáng", "At the school gate", {"kieu": "san", "san": 536}, [
    {"ve": "may", "x": 250, "y": 180, "rong": 190},
    {"ve": "may", "x": 1030, "y": 152, "rong": 160},
    {"ve": "nha", "x": 1010, "y": 536, "rong": 330, "cao": 236, "xa": 0.30},
    {"ve": "cay", "x": 190, "y": 540, "cao": 300, "xa": 0.14},
    {"ve": "nguoi", "x": 520, "y": 702, "cao": 258, "ao": TRANG, "quan": XANH,
     "dang": "vay", "huong": 1},
    {"ve": "nguoi", "x": 812, "y": 700, "cao": 252, "ao": "#F49AC1", "vay_ao": "#E4574C",
     "toc_dai": True, "dang": "vay", "huong": -1},
    {"tu": "bag", "x": 418, "y": 646, "co": 74},
    {"tu": "bag", "x": 916, "y": 646, "co": 74},
    {"tu": "bike", "x": 170, "y": 664, "co": 150},
    {"tu": "bike", "x": 1110, "y": 664, "co": 150},
]),
2: ("Hai bạn ở bàn học", "Two friends at the desk", {"kieu": "lop", "san": 560}, [
    {"ve": "bang", "x": 830, "y": 140, "w": 380, "h": 220},
    {"ve": "ghe", "x": 430, "y": 700, "cao": 126},
    {"ve": "nguoi", "x": 430, "y": 700, "cao": 232, "ao": VANG, "toc_dai": True,
     "dang": "ngoi", "huong": 1},
    {"ve": "ghe", "x": 830, "y": 700, "cao": 126},
    {"ve": "nguoi", "x": 830, "y": 700, "cao": 232, "ao": XANH,
     "dang": "ngoi", "huong": -1},
    {"ve": "ban", "x": 630, "y": 716, "w": 560, "cao": 112},
    # HAI TẤM BẢNG TÊN gấp đôi — mặt bảng ĐỂ TRỐNG, bé phải tự tìm chữ mà tả
    {"ve": "bangLuoi", "x": 430, "y": 566, "w": 92, "h": 40, "cot": 1},
    {"ve": "bangLuoi", "x": 830, "y": 566, "w": 92, "h": 40, "cot": 1},
    {"tu": "book", "x": 630, "y": 578, "co": 58},
]),
3: ("Ở sân trường", "In the school yard", {"kieu": "san", "san": 528}, [
    {"ve": "may", "x": 300, "y": 168, "rong": 180},
    {"ve": "nha", "x": 1060, "y": 528, "rong": 320, "cao": 226, "xa": 0.30},
    {"ve": "cay", "x": 210, "y": 532, "cao": 300, "xa": 0.16},
    {"ve": "nguoi", "x": 380, "y": 690, "cao": 236, "ao": TRANG, "quan": QUAN,
     "dang": "chi", "huong": 1},
    {"ve": "nguoi", "x": 690, "y": 704, "cao": 330, "ao": "#9FC6E8", "vay_ao": "#6FA8DC",
     "toc_dai": True, "dang": "dung"},
    {"ve": "nguoi", "x": 960, "y": 676, "cao": 312, "ao": TRANG, "quan": "#3A3A4A",
     "dang": "dung", "xa": 0.10},
    {"tu": "bag", "x": 500, "y": 674, "co": 86},
]),
4: ("Trước tấm gương", "In front of the mirror", {"kieu": "lop", "san": 566}, [
    {"ve": "guong", "x": 430, "y": 140, "w": 250, "h": 320},
    {"ve": "nguoi", "x": 430, "y": 712, "cao": 420, "ao": "#F49AC1", "vay_ao": TIM,
     "toc_dai": True, "dang": "chi", "huong": -1},
    {"ve": "nguoi", "x": 950, "y": 706, "cao": 336, "ao": XANH, "vay_ao": QUAN,
     "toc_dai": True, "dang": "chi", "huong": -1},
]),
5: ("Ở góc sinh hoạt", "At the activity corner", {"kieu": "phong", "san": 552}, [
    {"ve": "anhNho", "x": 640, "y": 150, "w": 220, "h": 166, "canh": "cay"},
    {"ve": "ban", "x": 640, "y": 622, "w": 210, "cao": 118},
    {"tu": "cooking", "x": 330, "y": 566, "co": 300},
    {"ve": "ban", "x": 330, "y": 700, "w": 250, "cao": 128},
    {"ve": "nguoi", "x": 960, "y": 700, "cao": 262, "ao": TIM, "vay_ao": "#8E5AC8",
     "dang": "gio", "huong": 1},
]),
6: ("Ở hành lang trường", "In the school corridor", {"kieu": "lop", "san": 548}, [
    {"ve": "cua", "x": 90, "y": 250, "w": 170, "h": 298, "mo": True},
    {"ve": "cua", "x": 330, "y": 250, "w": 170, "h": 298},
    {"ve": "cua", "x": 570, "y": 250, "w": 170, "h": 298, "mo": True},
    {"ve": "bangLuoi", "x": 175, "y": 176, "w": 140, "h": 58, "cot": 1},
    {"ve": "bangLuoi", "x": 415, "y": 176, "w": 140, "h": 58, "cot": 1},
    {"ve": "bangLuoi", "x": 655, "y": 176, "w": 140, "h": 58, "cot": 1},
    {"ve": "cuaSo", "x": 1010, "y": 190, "w": 230, "h": 190},
    {"ve": "nguoi", "x": 880, "y": 700, "cao": 258, "ao": TRANG, "quan": QUAN,
     "dang": "chi", "huong": -1},
    {"ve": "nguoi", "x": 1090, "y": 698, "cao": 250, "ao": "#F49AC1", "vay_ao": DO,
     "toc_dai": True, "dang": "dung"},
]),
7: ("Ở cửa lớp", "At the classroom door", {"kieu": "lop", "san": 556}, [
    {"ve": "bang", "x": 120, "y": 150, "w": 360, "h": 218},
    {"ve": "cua", "x": 980, "y": 216, "w": 210, "h": 342, "mo": True},
    {"ve": "nguoi", "x": 1080, "y": 556, "cao": 250, "ao": XANH, "quan": QUAN,
     "dang": "vay", "huong": -1},
    {"tu": "bag", "x": 950, "y": 486, "co": 76},
    {"ve": "nguoi", "x": 700, "y": 560, "cao": 258, "ao": LUC, "vay_ao": QUAN,
     "toc_dai": True, "dang": "chi", "huong": 1},
    {"ve": "ghe", "x": 250, "y": 706, "cao": 124},
    {"ve": "nguoi", "x": 250, "y": 706, "cao": 208, "ao": DO, "dang": "ngoi", "huong": 1},
    {"ve": "ban", "x": 250, "y": 706, "w": 236, "cao": 140},
    {"ve": "ghe", "x": 520, "y": 660, "cao": 112},
    {"ve": "nguoi", "x": 520, "y": 660, "cao": 188, "ao": VANG, "tet": True,
     "dang": "ngoi", "huong": 1},
    {"ve": "ban", "x": 520, "y": 660, "w": 212, "cao": 122},
]),
8: ("Ở bàn học của mình", "At my desk", {"kieu": "lop", "san": 470}, [
    {"ve": "cuaSo", "x": 950, "y": 138, "w": 260, "h": 200},
    {"ve": "ban", "x": 640, "y": 716, "w": 1160, "cao": 258},
    # Đồ bày RẢI RÁC, mỗi thứ một tầm cao — không xếp thành hàng ngang. Xếp
    # hàng đều tăm tắp chính là cái kệ mà bác bác bỏ, chỉ đổi tên thành "bàn".
    {"tu": "book", "x": 500, "y": 512, "co": 132},
    {"tu": "pencil case", "x": 880, "y": 528, "co": 138},
    {"tu": "ruler", "x": 720, "y": 486, "co": 120},
    {"tu": "eraser", "x": 1060, "y": 518, "co": 82},
    {"ve": "nguoi", "x": 250, "y": 716, "cao": 330, "ao": VANG, "tet": True,
     "dang": "chi", "huong": 1},
    {"tu": "pen", "x": 430, "y": 566, "co": 96},
]),
9: ("Ở góc mĩ thuật", "At the art corner", {"kieu": "phong", "san": 540}, [
    {"ve": "bangMau", "x": 640, "y": 258, "r": 96},
    {"ve": "nguoi", "x": 640, "y": 640, "cao": 262, "ao": TRANG, "vay_ao": XANH,
     "tet": True, "dang": "gio", "huong": 1},
    {"ve": "ban", "x": 640, "y": 716, "w": 900, "cao": 176},
    {"tu": "ball", "x": 300, "y": 500, "co": 108},
    {"tu": "pen", "x": 640, "y": 502, "co": 96},
    {"tu": "book", "x": 970, "y": 500, "co": 100},
]),
10: ("Ở sân chơi giờ ra chơi", "At break time", {"kieu": "san", "san": 512}, [
    {"ve": "may", "x": 240, "y": 166, "rong": 176},
    {"ve": "may", "x": 1040, "y": 148, "rong": 150},
    {"ve": "nha", "x": 640, "y": 512, "rong": 360, "cao": 240, "xa": 0.34},
    {"ve": "cay", "x": 130, "y": 516, "cao": 280, "xa": 0.20},
    {"ve": "cay", "x": 1170, "y": 516, "cao": 260, "xa": 0.22},
    {"ve": "nguoi", "x": 300, "y": 690, "cao": 244, "ao": DO, "quan": QUAN,
     "dang": "chay", "huong": 1},
    {"ve": "nguoi", "x": 520, "y": 704, "cao": 250, "ao": XANH, "quan": QUAN,
     "dang": "gio", "huong": -1},
    {"tu": "football", "x": 412, "y": 700, "co": 84},
    {"ve": "nguoi", "x": 850, "y": 700, "cao": 246, "ao": VANG, "vay_ao": TIM,
     "tet": True, "dang": "gio", "huong": 1},
    {"ve": "nguoi", "x": 1080, "y": 698, "cao": 242, "ao": LUC, "vay_ao": QUAN,
     "toc_dai": True, "dang": "gio", "huong": -1},
]),
11: ("Trong phòng khách", "In the living room", {"kieu": "phong", "san": 548}, [
    # KHUNG ẢNH GIA ĐÌNH treo tường — bốn người trong ảnh, vẽ nhỏ và nhạt
    {"ve": "khungAnh", "x": 700, "y": 132, "w": 430, "h": 250},
    {"ve": "nguoi", "x": 570, "y": 356, "cao": 168, "ao": QUAN, "xa": 0.12},
    {"ve": "nguoi", "x": 660, "y": 356, "cao": 162, "ao": "#F49AC1",
     "vay_ao": DO, "toc_dai": True, "xa": 0.12},
    {"ve": "nguoi", "x": 745, "y": 356, "cao": 132, "ao": VANG, "vay_ao": TIM,
     "tet": True, "xa": 0.12},
    {"ve": "nguoi", "x": 820, "y": 356, "cao": 112, "ao": LUC, "xa": 0.12},
    {"ve": "sofa", "x": 980, "y": 704, "w": 300, "cao": 168},
    {"ve": "nguoi", "x": 980, "y": 704, "cao": 240, "ao": "#F49AC1", "vay_ao": DO,
     "toc_dai": True, "dang": "ngoi", "huong": -1},
    {"ve": "ban", "x": 640, "y": 700, "w": 200, "cao": 104},
    {"ve": "nguoi", "x": 300, "y": 706, "cao": 262, "ao": XANH, "quan": QUAN,
     "dang": "chi", "huong": 1},
]),
12: ("Ngày hội nghề nghiệp", "Careers day", {"kieu": "san", "san": 520}, [
    {"ve": "may", "x": 300, "y": 164, "rong": 180},
    {"ve": "nha", "x": 1090, "y": 520, "rong": 300, "cao": 216, "xa": 0.34},
    {"ve": "tuKinh", "x": 330, "y": 620, "w": 330, "cao": 300},
    {"ve": "tuKinh", "x": 790, "y": 620, "w": 330, "cao": 300, "mau": "#EBD3A0"},
    {"tu": "doctor", "x": 330, "y": 494, "co": 150},
    {"tu": "farmer", "x": 790, "y": 494, "co": 150},
    {"ve": "nguoi", "x": 560, "y": 716, "cao": 250, "ao": VANG, "quan": QUAN,
     "dang": "chi", "huong": -1},
]),
13: ("Trong ngôi nhà", "Inside my house", {"kieu": "phong", "san": 560}, [
    # MẶT CẮT NGÔI NHÀ — bốn ô phòng, như ngôi nhà búp bê mở ra
    {"ve": "bangLuoi", "x": 640, "y": 128, "w": 800, "h": 420, "cot": 2, "hang": 2},
    {"ve": "giuong", "x": 440, "y": 320, "w": 210, "cao": 110},
    {"ve": "ban", "x": 840, "y": 320, "w": 150, "cao": 92},
    {"ve": "sofa", "x": 440, "y": 528, "w": 220, "cao": 128},
    {"ve": "ban", "x": 840, "y": 528, "w": 160, "cao": 96},
    {"tu": "kitchen", "x": 900, "y": 470, "co": 74},
    {"ve": "nguoi", "x": 200, "y": 700, "cao": 262, "ao": XANH, "quan": QUAN,
     "dang": "chi", "huong": 1},
]),
14: ("Trong phòng ngủ", "In my bedroom", {"kieu": "phong", "san": 552}, [
    {"ve": "cuaSo", "x": 120, "y": 156, "w": 260, "h": 210},
    {"ve": "cua", "x": 1020, "y": 226, "w": 200, "h": 330, "mo": True},
    {"ve": "giuong", "x": 470, "y": 690, "w": 340, "cao": 180},
    {"ve": "ban", "x": 810, "y": 664, "w": 190, "cao": 130},
    {"tu": "lamp", "x": 810, "y": 496, "co": 86},
    {"ve": "nguoi", "x": 210, "y": 706, "cao": 258, "ao": VANG, "vay_ao": TIM,
     "tet": True, "dang": "gio", "huong": 1},
]),
15: ("Ở bàn ăn", "At the dining table", {"kieu": "phong", "san": 540}, [
    {"ve": "giaSach", "x": 1130, "y": 548, "w": 180, "cao": 208},
    {"ve": "nguoi", "x": 640, "y": 640, "cao": 320, "ao": "#F49AC1", "vay_ao": VANG,
     "toc_dai": True, "dang": "cui", "huong": 1},
    {"ve": "ghe", "x": 330, "y": 700, "cao": 126, "huong": -1},
    {"ve": "nguoi", "x": 330, "y": 700, "cao": 216, "ao": XANH, "dang": "ngoi", "huong": 1},
    {"ve": "ghe", "x": 950, "y": 700, "cao": 126},
    {"ve": "nguoi", "x": 950, "y": 700, "cao": 216, "ao": DO, "tet": True,
     "dang": "ngoi", "huong": -1},
    {"ve": "ban", "x": 640, "y": 716, "w": 760, "cao": 128},
    {"tu": "bread", "x": 640, "y": 552, "co": 92},
    {"tu": "rice", "x": 452, "y": 556, "co": 80},
    {"tu": "milk", "x": 812, "y": 554, "co": 74},
    {"tu": "milk", "x": 916, "y": 554, "co": 74},
]),
16: ("Ở góc thú nuôi", "At the pet corner", {"kieu": "co", "san": 520}, [
    {"ve": "hangRao", "x1": 40, "x2": 1240, "y": 528, "cao": 96, "buoc": 96},
    {"ve": "cay", "x": 1120, "y": 524, "cao": 230, "xa": 0.24},
    {"ve": "nguoi", "x": 300, "y": 706, "cao": 262, "ao": VANG, "vay_ao": TIM,
     "tet": True, "dang": "cui", "huong": 1},
    {"tu": "cat", "x": 404, "y": 672, "co": 104},
    {"ve": "nguoi", "x": 790, "y": 704, "cao": 256, "ao": XANH, "quan": QUAN,
     "dang": "dung"},
    {"tu": "dog", "x": 916, "y": 676, "co": 86},
    {"tu": "dog", "x": 1030, "y": 676, "co": 86},
    {"ve": "longChim", "x": 596, "y": 528, "cao": 236},
    {"tu": "bird", "x": 664, "y": 358, "co": 60},
]),
17: ("Ở góc đồ chơi", "At the toy corner", {"kieu": "phong", "san": 548}, [
    {"ve": "giaSach", "x": 1110, "y": 548, "w": 200, "cao": 240},
    {"ve": "ban", "x": 640, "y": 690, "w": 300, "cao": 130},
    {"tu": "top", "x": 580, "y": 528, "co": 72},
    {"tu": "ship", "x": 700, "y": 526, "co": 78},
    {"ve": "nguoi", "x": 270, "y": 700, "cao": 262, "ao": LUC, "vay_ao": QUAN,
     "toc_dai": True, "dang": "gio", "huong": 1},
    {"tu": "kite", "x": 270, "y": 452, "co": 104},
    {"ve": "nguoi", "x": 950, "y": 704, "cao": 236, "ao": DO, "dang": "cui", "huong": -1},
    {"tu": "car", "x": 838, "y": 682, "co": 88},
]),
18: ("Trong phòng sinh hoạt", "In the common room", {"kieu": "phong", "san": 540}, [
    {"ve": "cuaSo", "x": 520, "y": 148, "w": 280, "h": 216},
    {"ve": "giaSach", "x": 1100, "y": 540, "w": 200, "cao": 226},
    {"ve": "sofa", "x": 290, "y": 706, "w": 300, "cao": 170},
    {"tu": "reading", "x": 290, "y": 566, "co": 290},
    {"ve": "ghe", "x": 880, "y": 706, "cao": 126},
    {"tu": "writing", "x": 880, "y": 572, "co": 290},
    {"ve": "ban", "x": 880, "y": 716, "w": 280, "cao": 116},
]),
19: ("Ở sân chơi buổi chiều", "At the playground", {"kieu": "co", "san": 500}, [
    {"ve": "matTroi", "x": 1120, "y": 190, "r": 52},
    {"ve": "may", "x": 330, "y": 176, "rong": 176},
    {"ve": "cay", "x": 1080, "y": 512, "cao": 268, "xa": 0.22},
    {"ve": "cay", "x": 120, "y": 508, "cao": 240, "xa": 0.26},
    {"tu": "cycling", "x": 380, "y": 560, "co": 330},
    {"tu": "skipping", "x": 900, "y": 552, "co": 330},
]),
20: ("Trong vườn thú", "At the zoo", {"kieu": "co", "san": 486}, [
    {"ve": "may", "x": 250, "y": 168, "rong": 168},
    {"ve": "cay", "x": 1140, "y": 496, "cao": 300, "xa": 0.22},
    {"tu": "tiger", "x": 400, "y": 430, "co": 190},
    {"tu": "monkey", "x": 800, "y": 400, "co": 160},
    {"ve": "songSat", "x": 210, "y": 180, "w": 800, "h": 360, "buoc": 66},
    {"ve": "nguoi", "x": 320, "y": 706, "cao": 248, "ao": DO, "quan": QUAN,
     "dang": "chi", "huong": 1},
    {"ve": "nguoi", "x": 620, "y": 704, "cao": 240, "ao": VANG, "vay_ao": TIM,
     "tet": True, "dang": "dung"},
    {"ve": "nguoi", "x": 950, "y": 712, "cao": 276, "ao": XANH, "vay_ao": QUAN,
     "toc_dai": True, "dang": "dung"},
]),
}


# ══════════════════════════════ LỚP 4 ══════════════════════════════
# Bác dặn: *"các bài đọc, nói, viết sẽ dài hơn lớp 3 nhé"*. Dài hơn MỘT NHỊP —
# thêm một câu tả, KHÔNG thêm một câu chuyện thứ hai. Bức tranh cũng vậy: thêm
# một chi tiết đáng tả, không thêm một góc cảnh nữa.
B4 = {
0: ("Ở sân trường ngày tựu trường", "The first day of school", {"kieu": "san", "san": 528}, [
    {"ve": "may", "x": 260, "y": 172, "rong": 186},
    {"ve": "may", "x": 1020, "y": 146, "rong": 156},
    {"ve": "nha", "x": 1010, "y": 528, "rong": 340, "cao": 250, "xa": 0.30},
    {"ve": "cay", "x": 170, "y": 532, "cao": 300, "xa": 0.16},
    # HAI BẠN BẮT TAY NHAU — đây là chỗ bác bắt: bài tên "Hello Again" mà bức cũ
    # không có ai chào ai, chỉ có diều, mèo và mũ nằm trên kệ.
    {"ve": "nguoi", "x": 530, "y": 706, "cao": 266, "ao": "#F49AC1", "vay_ao": XANH,
     "toc_dai": True, "dang": "chi", "huong": 1},
    {"ve": "nguoi", "x": 790, "y": 704, "cao": 262, "ao": TRANG, "quan": XANH,
     "dang": "chi", "huong": -1},
    {"tu": "bag", "x": 402, "y": 650, "co": 74},
    {"tu": "bag", "x": 920, "y": 650, "co": 74},
    {"tu": "bike", "x": 160, "y": 660, "co": 148},
    {"tu": "bike", "x": 1120, "y": 660, "co": 148},
]),
1: ("Trước tấm bản đồ thế giới", "In front of the world map", {"kieu": "phong", "san": 552}, [
    # ⚠ CỜ QUỐC GIA emoji vẽ ra RỖNG HẲN — phông không có. Cảnh này dùng BẢN ĐỒ.
    {"ve": "banDo", "x": 620, "y": 132, "w": 640, "h": 330},
    {"ve": "nguoi", "x": 430, "y": 706, "cao": 270, "ao": TRANG, "vay_ao": QUAN,
     "toc_dai": True, "dang": "chi", "huong": 1},
    {"ve": "nguoi", "x": 800, "y": 704, "cao": 264, "ao": "#F49AC1", "vay_ao": DO,
     "dang": "dung"},
    {"ve": "ban", "x": 1080, "y": 712, "w": 250, "cao": 132},
    {"tu": "bag", "x": 1080, "y": 542, "co": 82},
]),
2: ("Trong phòng ngủ buổi sáng", "In the bedroom in the morning", {"kieu": "phong", "san": 552}, [
    {"ve": "cuaSo", "x": 120, "y": 150, "w": 270, "h": 216},
    {"ve": "giuong", "x": 520, "y": 700, "w": 380, "cao": 190},
    {"ve": "nguoi", "x": 520, "y": 700, "cao": 250, "ao": "#9FC6E8", "dang": "gio",
     "huong": 1},
    {"ve": "ban", "x": 880, "y": 668, "w": 200, "cao": 136},
    {"ve": "dongHo", "x": 880, "y": 486, "r": 56, "gio": 6, "phut": 0},
    {"tu": "bag", "x": 1080, "y": 668, "co": 92},
]),
3: ("Trước tấm lịch tuần", "In front of the weekly calendar", {"kieu": "lop", "san": 556}, [
    {"ve": "bangLuoi", "x": 480, "y": 138, "w": 640, "h": 240, "cot": 7, "to": 0},
    {"ve": "nguoi", "x": 930, "y": 560, "cao": 330, "ao": XANH, "vay_ao": QUAN,
     "toc_dai": True, "dang": "chi", "huong": -1},
    {"ve": "ghe", "x": 300, "y": 712, "cao": 126},
    {"ve": "nguoi", "x": 300, "y": 712, "cao": 218, "ao": DO, "dang": "gio", "huong": 1},
    {"ve": "ban", "x": 300, "y": 716, "w": 250, "cao": 120},
    {"tu": "book", "x": 300, "y": 566, "co": 56},
    {"ve": "ghe", "x": 640, "y": 700, "cao": 118},
    {"ve": "nguoi", "x": 640, "y": 700, "cao": 204, "ao": VANG, "tet": True,
     "dang": "ngoi", "huong": 1},
    {"ve": "ban", "x": 640, "y": 706, "w": 236, "cao": 112},
]),
4: ("Ở bàn tiệc sinh nhật", "At the birthday party", {"kieu": "phong", "san": 540}, [
    {"ve": "bangGhim", "x": 640, "y": 122, "w": 480, "h": 130, "o": 5},
    {"ve": "nguoi", "x": 400, "y": 640, "cao": 254, "ao": VANG, "vay_ao": DO,
     "tet": True, "dang": "cui", "huong": 1},
    {"ve": "nguoi", "x": 880, "y": 636, "cao": 322, "ao": "#F49AC1", "vay_ao": TIM,
     "toc_dai": True, "dang": "dung"},
    {"ve": "ban", "x": 640, "y": 716, "w": 800, "cao": 132},
    {"tu": "cake", "x": 640, "y": 546, "co": 108},
    {"tu": "chips", "x": 400, "y": 556, "co": 84},
    {"tu": "grapes", "x": 862, "y": 552, "co": 86},
    {"tu": "jam", "x": 986, "y": 552, "co": 78},
]),
5: ("Ở góc tài năng của lớp", "At the class talent corner", {"kieu": "phong", "san": 548}, [
    {"ve": "bangGhim", "x": 1090, "y": 140, "w": 300, "h": 200, "o": 2},
    {"tu": "cycling", "x": 330, "y": 560, "co": 330},
    {"ve": "giaVe", "x": 850, "y": 706, "cao": 300},
    {"ve": "nguoi", "x": 1010, "y": 708, "cao": 262, "ao": TRANG, "vay_ao": LUC,
     "tet": True, "dang": "chi", "huong": -1},
]),
6: ("Nhìn toàn cảnh trường mình", "Our whole school", {"kieu": "san", "san": 468}, [
    {"ve": "may", "x": 240, "y": 156, "rong": 170},
    {"ve": "may", "x": 1030, "y": 140, "rong": 150},
    {"ve": "nha", "x": 250, "y": 474, "rong": 300, "cao": 246, "xa": 0.22},
    {"ve": "nha", "x": 640, "y": 470, "rong": 300, "cao": 240, "xa": 0.26},
    {"ve": "tuKinh", "x": 1060, "y": 480, "w": 330, "cao": 230},
    {"tu": "book", "x": 990, "y": 366, "co": 72},
    {"tu": "book", "x": 1120, "y": 368, "co": 72},
    {"ve": "cay", "x": 60, "y": 480, "cao": 230, "xa": 0.30},
    {"ve": "nguoi", "x": 470, "y": 712, "cao": 268, "ao": DO, "quan": QUAN,
     "dang": "chi", "huong": 1},
    {"ve": "nguoi", "x": 740, "y": 710, "cao": 262, "ao": VANG, "vay_ao": TIM,
     "tet": True, "dang": "dung"},
]),
7: ("Trước thời khoá biểu", "In front of the timetable", {"kieu": "lop", "san": 556}, [
    {"ve": "bangLuoi", "x": 560, "y": 132, "w": 620, "h": 300, "cot": 5, "hang": 3,
     "to": [0, 1]},
    {"ve": "nguoi", "x": 300, "y": 712, "cao": 268, "ao": TRANG, "quan": QUAN,
     "dang": "chi", "huong": 1},
    {"ve": "nguoi", "x": 960, "y": 710, "cao": 262, "ao": LUC, "vay_ao": QUAN,
     "toc_dai": True, "dang": "dung"},
    {"tu": "book", "x": 1078, "y": 606, "co": 76},
    {"ve": "ban", "x": 640, "y": 720, "w": 240, "cao": 104},
    {"tu": "bag", "x": 640, "y": 570, "co": 78},
]),
8: ("Ở góc trưng bày môn Mĩ thuật", "At the art display corner", {"kieu": "phong", "san": 546}, [
    {"ve": "bangGhim", "x": 480, "y": 122, "w": 520, "h": 286, "o": 3},
    {"ve": "anhNho", "x": 330, "y": 174, "w": 138, "h": 182, "canh": "nha"},
    {"ve": "anhNho", "x": 480, "y": 174, "w": 138, "h": 182, "canh": "cay"},
    {"ve": "anhNho", "x": 630, "y": 174, "w": 138, "h": 182, "canh": "troi"},
    {"ve": "giaVe", "x": 1010, "y": 700, "cao": 290},
    {"ve": "nguoi", "x": 400, "y": 706, "cao": 268, "ao": TRANG, "vay_ao": XANH,
     "toc_dai": True, "dang": "chi", "huong": -1},
    {"ve": "ban", "x": 700, "y": 716, "w": 300, "cao": 122},
    {"tu": "pen", "x": 700, "y": 560, "co": 88},
]),
9: ("Ngày hội thể thao", "Our sports day", {"kieu": "co", "san": 486}, [
    {"ve": "may", "x": 280, "y": 158, "rong": 176},
    {"ve": "nha", "x": 1080, "y": 492, "rong": 280, "cao": 200, "xa": 0.34},
    {"ve": "cay", "x": 120, "y": 494, "cao": 250, "xa": 0.28},
    {"ve": "nguoi", "x": 330, "y": 700, "cao": 250, "ao": DO, "quan": QUAN,
     "dang": "chay", "huong": 1},
    {"ve": "nguoi", "x": 560, "y": 704, "cao": 252, "ao": XANH, "quan": QUAN,
     "dang": "chay", "huong": 1},
    {"ve": "nguoi", "x": 790, "y": 702, "cao": 248, "ao": VANG, "quan": QUAN,
     "dang": "chay", "huong": 1},
    {"ve": "nguoi", "x": 1080, "y": 706, "cao": 330, "ao": LUC, "vay_ao": QUAN,
     "toc_dai": True, "dang": "gio", "huong": -1},
    {"tu": "ball", "x": 170, "y": 672, "co": 88},
    {"ve": "huyChuong", "x": 1176, "y": 512, "r": 34},
]),
10: ("Trước bảng ảnh kì nghỉ hè", "In front of the holiday photos", {"kieu": "lop", "san": 552}, [
    {"ve": "bangGhim", "x": 560, "y": 122, "w": 580, "h": 300, "o": 3},
    {"ve": "anhNho", "x": 392, "y": 178, "w": 156, "h": 188, "canh": "bien"},
    {"ve": "anhNho", "x": 560, "y": 178, "w": 156, "h": 188, "canh": "que"},
    {"ve": "anhNho", "x": 728, "y": 178, "w": 156, "h": 188, "canh": "pho"},
    {"ve": "nguoi", "x": 330, "y": 710, "cao": 266, "ao": XANH, "quan": QUAN,
     "dang": "chi", "huong": 1},
    {"ve": "nguoi", "x": 900, "y": 708, "cao": 260, "ao": "#F49AC1", "vay_ao": DO,
     "toc_dai": True, "dang": "dung"},
    {"ve": "ban", "x": 1130, "y": 716, "w": 230, "cao": 118},
]),
11: ("Trên con phố trước nhà", "On my street", {"kieu": "pho", "he": 500, "duong": 596}, [
    {"ve": "nha", "x": 200, "y": 500, "rong": 320, "cao": 300, "mau": "#F2E3C6"},
    {"ve": "nha", "x": 620, "y": 500, "rong": 260, "cao": 240, "xa": 0.22},
    {"ve": "nha", "x": 980, "y": 500, "rong": 280, "cao": 262, "xa": 0.30},
    # BIỂN TÊN PHỐ — tấm biển xanh ĐỂ TRỐNG, không viết chữ
    {"ve": "bangLuoi", "x": 352, "y": 236, "w": 132, "h": 46, "cot": 1},
    {"ve": "oto", "x": 420, "y": 690, "dai": 230, "mau": "#C0392B"},
    {"ve": "oto", "x": 940, "y": 662, "dai": 200, "mau": "#0B4EA8", "xa": 0.12},
    {"ve": "nguoi", "x": 150, "y": 590, "cao": 236, "ao": TRANG, "quan": QUAN,
     "dang": "chi", "huong": 1},
    {"ve": "nguoi", "x": 330, "y": 588, "cao": 230, "ao": VANG, "vay_ao": TIM,
     "tet": True, "dang": "dung"},
]),
12: ("Ở bệnh viện nơi mẹ làm việc", "At the hospital where my mother works",
     {"kieu": "lop", "san": 556}, [
    {"ve": "cua", "x": 120, "y": 210, "w": 220, "h": 346, "mo": True},
    {"ve": "cuaSo", "x": 980, "y": 156, "w": 240, "h": 190},
    {"tu": "doctor", "x": 560, "y": 500, "co": 330},
    {"ve": "nguoi", "x": 800, "y": 712, "cao": 258, "ao": VANG, "vay_ao": TIM,
     "tet": True, "dang": "dung"},
    {"tu": "bag", "x": 918, "y": 640, "co": 80},
    {"ve": "ghe", "x": 1120, "y": 700, "cao": 126},
]),
13: ("Trước tấm ảnh lớp", "In front of the class photo", {"kieu": "lop", "san": 552}, [
    {"ve": "khungAnh", "x": 620, "y": 126, "w": 640, "h": 300},
    # BỐN BẠN TRONG ẢNH — cao · tóc dài · thấp · mặt tròn, để bé tả được từng người
    {"ve": "nguoi", "x": 420, "y": 396, "cao": 236, "ao": XANH, "xa": 0.10},
    {"ve": "nguoi", "x": 550, "y": 396, "cao": 200, "ao": "#F49AC1", "vay_ao": DO,
     "toc_dai": True, "xa": 0.10},
    {"ve": "nguoi", "x": 680, "y": 396, "cao": 168, "ao": VANG, "xa": 0.10},
    {"ve": "nguoi", "x": 800, "y": 396, "cao": 196, "ao": LUC, "vay_ao": TIM,
     "tet": True, "xa": 0.10},
    {"ve": "nguoi", "x": 250, "y": 710, "cao": 262, "ao": DO, "vay_ao": QUAN,
     "toc_dai": True, "dang": "chi", "huong": 1},
    {"ve": "nguoi", "x": 1060, "y": 712, "cao": 330, "ao": XANH, "vay_ao": QUAN,
     "toc_dai": True, "dang": "dung"},
]),
14: ("Trong nhà buổi sáng", "At home in the morning", {"kieu": "phong", "san": 548}, [
    {"ve": "cuaSo", "x": 110, "y": 150, "w": 250, "h": 206},
    {"ve": "sofa", "x": 330, "y": 706, "w": 290, "cao": 164},
    {"ve": "ban", "x": 620, "y": 704, "w": 210, "cao": 106},
    {"tu": "mops", "x": 800, "y": 596, "co": 270},
    {"ve": "ban", "x": 1090, "y": 700, "w": 220, "cao": 150},
    {"tu": "watch TV", "x": 1090, "y": 486, "co": 130},
]),
15: ("Trước trung tâm thể thao", "In front of the sports centre",
     {"kieu": "pho", "he": 512, "duong": 616}, [
    {"ve": "nha", "x": 760, "y": 512, "rong": 420, "cao": 330, "mau": "#EBD3A0"},
    {"ve": "nha", "x": 190, "y": 512, "rong": 260, "cao": 236, "xa": 0.28},
    {"ve": "nguoi", "x": 620, "y": 604, "cao": 330, "ao": LUC, "quan": QUAN,
     "dang": "chi", "huong": 1},
    {"ve": "nguoi", "x": 350, "y": 600, "cao": 236, "ao": VANG, "vay_ao": TIM,
     "tet": True, "dang": "vay", "huong": 1},
    {"tu": "ball", "x": 496, "y": 566, "co": 76},
    {"tu": "bike", "x": 200, "y": 590, "co": 140},
    {"ve": "oto", "x": 1060, "y": 692, "dai": 210, "mau": "#0B4EA8"},
]),
16: ("Bên cửa sổ lớp học", "By the classroom window", {"kieu": "lop", "san": 556}, [
    {"ve": "cuaSo", "x": 880, "y": 140, "w": 330, "h": 260},
    {"ve": "matTroi", "x": 1100, "y": 208, "r": 40},
    # BẢNG THỜI TIẾT bốn ô — ô mặt trời được khoanh đỏ
    {"ve": "bangThoiTiet", "x": 270, "y": 150, "w": 420, "h": 200, "khoanh": 0},
    {"ve": "nguoi", "x": 560, "y": 560, "cao": 330, "ao": XANH, "vay_ao": QUAN,
     "toc_dai": True, "dang": "chi", "huong": -1},
    {"ve": "ghe", "x": 640, "y": 712, "cao": 126},
    {"ve": "nguoi", "x": 640, "y": 712, "cao": 218, "ao": DO, "dang": "ngoi", "huong": 1},
    {"ve": "ban", "x": 640, "y": 716, "w": 250, "cao": 116},
]),
17: ("Ở một ngã tư trong phố", "At a crossroads in the city",
     {"kieu": "pho", "he": 498, "duong": 590}, [
    {"ve": "nha", "x": 210, "y": 498, "rong": 300, "cao": 280, "xa": 0.20},
    {"ve": "tuKinh", "x": 1010, "y": 502, "w": 340, "cao": 280},
    {"tu": "book", "x": 940, "y": 388, "co": 80},
    {"tu": "book", "x": 1070, "y": 392, "co": 80},
    {"ve": "bienBao", "x": 150, "y": 588, "cao": 250},
    {"ve": "oto", "x": 430, "y": 686, "dai": 220, "mau": "#F9B233"},
    {"ve": "oto", "x": 880, "y": 660, "dai": 190, "mau": "#C0392B", "xa": 0.14},
    {"ve": "nguoi", "x": 380, "y": 582, "cao": 226, "ao": XANH, "quan": QUAN,
     "dang": "dung"},
    {"ve": "nguoi", "x": 620, "y": 586, "cao": 322, "ao": TRANG, "quan": "#3A3A4A",
     "dang": "chi", "huong": -1},
]),
18: ("Trong trung tâm mua sắm", "At the shopping centre", {"kieu": "lop", "san": 560}, [
    {"ve": "tuKinh", "x": 350, "y": 560, "w": 380, "cao": 320},
    {"tu": "book", "x": 270, "y": 400, "co": 92},
    {"tu": "book", "x": 430, "y": 404, "co": 92},
    {"ve": "tuKinh", "x": 830, "y": 560, "w": 380, "cao": 320, "mau": "#EBD3A0"},
    {"tu": "bread", "x": 750, "y": 402, "co": 92},
    {"tu": "cake", "x": 910, "y": 404, "co": 92},
    {"ve": "nguoi", "x": 250, "y": 714, "cao": 264, "ao": "#F49AC1", "vay_ao": TIM,
     "toc_dai": True, "dang": "chi", "huong": 1},
    {"ve": "nguoi", "x": 470, "y": 712, "cao": 258, "ao": XANH, "quan": QUAN,
     "dang": "dung"},
    {"tu": "T-shirt", "x": 1130, "y": 636, "co": 150},
]),
19: ("Trước chuồng hươu cao cổ", "In front of the giraffe enclosure",
     {"kieu": "co", "san": 470}, [
    {"ve": "may", "x": 240, "y": 156, "rong": 168},
    {"ve": "cay", "x": 560, "y": 480, "cao": 360, "xa": 0.14},
    {"tu": "giraffe", "x": 300, "y": 330, "co": 300},
    {"tu": "giraffe", "x": 450, "y": 356, "co": 260},
    {"ve": "hangRao", "x1": 60, "x2": 700, "y": 500, "cao": 100, "buoc": 92},
    {"tu": "peacock", "x": 960, "y": 420, "co": 250},
    {"ve": "nguoi", "x": 800, "y": 712, "cao": 330, "ao": XANH, "vay_ao": QUAN,
     "toc_dai": True, "dang": "chi", "huong": -1},
    {"ve": "nguoi", "x": 1080, "y": 710, "cao": 258, "ao": VANG, "vay_ao": TIM,
     "tet": True, "dang": "dung"},
]),
20: ("Ở trại hè bên hồ", "At summer camp by the lake", {"kieu": "toi", "san": 462}, [
    {"ve": "leu", "x": 220, "y": 640, "rong": 300, "cao": 240},
    {"ve": "cay", "x": 1180, "y": 566, "cao": 280, "xa": 0.30},
    {"ve": "luaTrai", "x": 640, "y": 690, "cao": 170},
    {"ve": "nguoi", "x": 470, "y": 700, "cao": 250, "ao": DO, "quan": QUAN,
     "dang": "cui", "huong": 1},
    {"ve": "nguoi", "x": 880, "y": 702, "cao": 246, "ao": VANG, "vay_ao": TIM,
     "tet": True, "dang": "gio", "huong": -1},
    {"ve": "nguoi", "x": 1060, "y": 700, "cao": 242, "ao": LUC, "quan": QUAN,
     "dang": "gio", "huong": -1},
]),
}


# ══════════════════ LỜI VIỆT CHO CÂU HỎI ══════════════════
# Dòng phụ tiếng Việt dưới câu hỏi tiếng Anh — chỗ bám cho bé chưa đọc nổi đề.
# Bốn lựa chọn thì THUẦN tiếng Anh: đó mới là chỗ bé luyện đọc thật.
#
# ⚠ Khai ĐỦ hay không thì `_vi()` kêu ngay, không im lặng bỏ trống. Bản trước
# `phu` là trường tuỳ chọn nên thiếu cũng không ai biết, bé chỉ thấy một dòng
# trống dưới câu hỏi.
HOI_VI = {
 "What can you see?": "Con nhìn thấy gì trong tranh?",
 "Who is this?": "Đây là ai?",
 "Who's this?": "Đây là ai?",
 "What's this?": "Đây là cái gì?",
 "What's she doing?": "Bạn ấy đang làm gì?",
 "What's he doing?": "Bạn ấy đang làm gì?",
 "What is he doing?": "Bạn ấy đang làm gì?",
 "What are they doing?": "Các bạn ấy đang làm gì?",
 "What's the monkey doing?": "Con khỉ đang làm gì?",
 "Where are they?": "Các bạn ấy đang ở đâu?",
 "Where are you?": "Con đang ở đâu?",
 "Where is he?": "Bạn ấy đang ở đâu?",
 "How many bags can you see?": "Con thấy mấy cái cặp?",
 "How many desks can you see?": "Con thấy mấy cái bàn?",
 "How many friends can you see?": "Con thấy mấy người bạn?",
 "How many people can you see?": "Con thấy mấy người?",
 "How many buildings are there?": "Có mấy dãy nhà?",
 "How many cars can you see?": "Con thấy mấy chiếc ô tô?",
 "How many cups can you see?": "Con thấy mấy cái cốc?",
 "How many dogs can you see?": "Con thấy mấy con chó?",
 "How many giraffes can you see?": "Con thấy mấy con hươu cao cổ?",
 "How many pictures can you see?": "Con thấy mấy bức tranh?",
 "How old is Mary?": "Mary mấy tuổi?",
 "Is the door big?": "Cánh cửa có to không?",
 "Is he a farmer?": "Bác ấy có phải nông dân không?",
 "What are these animals?": "Đây là những con vật gì?",
 "What can he do?": "Bạn ấy làm được gì?",
 "What can she do?": "Bạn ấy làm được gì?",
 "Can you ride a bike?": "Con đi xe đạp được không?",
 "What colour is the ball?": "Quả bóng màu gì?",
 "What colour is the pen?": "Cây bút màu gì?",
 "What day is it today?": "Hôm nay là thứ mấy?",
 "What do you do at break time?": "Giờ ra chơi con làm gì?",
 "What do you do in the morning?": "Buổi sáng con làm gì?",
 "What do you do on Mondays?": "Thứ Hai con làm gì?",
 "What do you have?": "Con có gì?",
 "What do you want to be?": "Lớn lên con muốn làm nghề gì?",
 "What does he do on Sundays?": "Chủ nhật bố làm gì?",
 "What does he have?": "Bạn ấy có gì?",
 "What does she have?": "Bạn ấy có gì?",
 "What does he look like?": "Bạn ấy trông thế nào?",
 "What does she look like?": "Bạn ấy trông thế nào?",
 "What does she do?": "Mẹ làm nghề gì?",
 "What subjects do you have today?": "Hôm nay con học những môn gì?",
 "What time is it?": "Mấy giờ rồi?",
 "What was the weather like?": "Hôm ấy trời thế nào?",
 "What was the weather like last weekend?": "Cuối tuần trước trời thế nào?",
 "What's her job?": "Cô ấy làm nghề gì?",
 "What's his job?": "Bác ấy làm nghề gì?",
 "What's in the room?": "Trong phòng có gì?",
 "What's the street like?": "Con phố ấy thế nào?",
 "What's your favourite subject?": "Môn con thích nhất là môn gì?",
 "What's your hobby?": "Sở thích của con là gì?",
 "When do you have maths?": "Con học Toán vào thứ mấy?",
 "When do you watch TV?": "Con xem ti vi lúc nào?",
 "When's your birthday?": "Sinh nhật con vào tháng nào?",
 "When's your sports day?": "Ngày hội thể thao vào tháng nào?",
 "Where are the chairs?": "Mấy cái ghế ở đâu?",
 "Where are you from?": "Con đến từ đâu?",
 "Where's she from?": "Bạn ấy đến từ đâu?",
 "Where do you live?": "Con sống ở đâu?",
 "Where does he go on Saturdays?": "Thứ Bảy bố đi đâu?",
 "Where does she work?": "Mẹ làm việc ở đâu?",
 "Where were you last summer?": "Hè năm ngoái con ở đâu?",
 "Where's the bookshop?": "Hiệu sách ở chỗ nào?",
 "Where's the bed?": "Cái giường ở phòng nào?",
 "What do you want to be?": "Lớn lên con muốn làm nghề gì?",
 "How many bikes can you see?": "Con thấy mấy chiếc xe đạp?",
 "How many toys can you see?": "Con thấy mấy món đồ chơi?",
 "Where's your school?": "Trường con ở đâu?",
 "Would you like some bread?": "Con ăn bánh mì nhé?",
 "Touch your face!": "Con sờ vào mặt mình nào!",
}


def _vi(cau: str) -> str:
    if cau not in HOI_VI:
        raise SystemExit(f"✗ chưa có lời Việt cho câu hỏi: {cau!r}\n"
                         f"  Khai vào HOI_VI trong tools/soan_canh.py.")
    return HOI_VI[cau]


def _hoi(k: dict) -> list[dict]:
    """Tách cột câu hỏi của bảng đã duyệt thành dữ liệu.

    Dạng trong bảng:  "1. What can you see? → I can see a ball.  (mồi: A · B · C)"
    Mồi nhử khai TAY ở bảng chứ không sinh bằng máy: mồi phải SAI với bức tranh
    này, mà máy không biết bức tranh có gì. Đoán ở đây là đẻ ra câu hỏi hai đáp
    án đúng — lỗi đã dính một lần ở bản trước.
    """
    ra = []
    for dong in k["hoi"].split("\n"):
        dong = dong.strip()
        if not dong:
            continue
        dong = dong.split(". ", 1)[1] if dong[0].isdigit() else dong
        cau, phan = dong.split(" → ", 1)
        dap, moi = phan.split("(mồi:", 1)
        ra.append({"hoi": cau.strip(), "vi": _vi(cau.strip()), "dap": dap.strip(),
                   "moi": [m.strip() for m in moi.rstrip(")").split("·")
                           if m.strip() and not m.strip().startswith("cùng khuôn")]})
    return ra


def soan(lop: int, van: dict, bo: dict) -> list[dict]:
    # CHƯƠNG của từng unit — lấy từ bản chuẩn, không đoán.
    # ⚠ Thiếu trường này thì `sinh_bai_tranh.py` mặc định chương 1, và cổng soi
    # chữ dựng túi từ "đã học tới chương 1" cho CẢ 21 bài — U20 mất trắng vốn từ
    # của bốn chương, cổng kêu 168 chữ lạ mà không chữ nào lạ thật.
    cn = json.loads((GOC / f"data/tienganh/chuan_lop{lop}.json").read_text("utf8"))
    chuong = {u: int(c) for c, m in cn["chuong"].items() for u in m["unit"]}
    ra = []
    for so in sorted(van):
        if so not in bo:
            raise SystemExit(f"✗ lớp {lop} U{so:02d}: có nội dung mà CHƯA CÓ BỐ CỤC")
        ten, ten_en, nen, vat = bo[so]
        k = van[so]
        ra.append({
            "id": f"TRANH:TA{lop}.U{so:02d}", "unit": so,
            "chuong": chuong[so],
            "ten": ten, "ten_en": ten_en,
            "moTa": k["mo_ta"],
            "nen": nen, "vat": vat,
            "doan": [c.strip().rstrip(".") + "."
                     for c in k["doan"].split(". ") if c.strip(". ")],
            "hoi": _hoi(k),
            "goiY": [{"hoi": g.strip(), "vi": _vi(g.strip())}
                     for g in k["goi_y"].split("·")],
        })
    return ra


def main() -> int:
    tong = 0
    for lop, van, bo in ((3, L3, B3), (4, L4, B4)):
        ds = soan(lop, van, bo)
        tep = GOC / f"data/tienganh/canh_lop{lop}.json"
        tep.write_text(json.dumps(ds, ensure_ascii=False, indent=1), "utf8")
        print(f"→ {tep.relative_to(GOC)}  ({len(ds)} cảnh)")
        tong += len(ds)
    print(f"tổng {tong} cảnh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
