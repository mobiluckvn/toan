#!/usr/bin/env python3
"""
KHUNG DỰNG CHƯƠNG 3 — hàm vẽ dùng chung cho năm phần nội dung.

Tách riêng khỏi phần nội dung vì một lý do thực dụng: nội dung Chương 3 dài, và
để chung một tệp thì mỗi lần sửa một mục phải mở cả nghìn dòng. Năm tệp
`chuong3_p1.py` … `chuong3_p4.py` chỉ chứa CHỮ; tệp này chỉ chứa CÁCH VẼ.

⚠ Mọi con số trong phần nội dung đều phải đối chiếu được với mã nguồn hoặc tệp
dữ liệu đang chạy. Chỗ nào là con số CHỌN chứ không phải con số ĐO thì phải nói
ra — xem `docs/xac_nhan_chuong2.docx` mục C-6 để biết vì sao.
"""
from __future__ import annotations

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

DO = RGBColor(0xB0, 0x22, 0x22)
XANH = RGBColor(0x1F, 0x5C, 0x2E)
XAM = RGBColor(0x55, 0x55, 0x55)


def do(p, chu, dam=False, mau=None, nghieng=False, ma=False):
    """Một mẩu chữ trong đoạn. `ma=True` cho tên tệp, tên hàm, mã nút."""
    r = p.add_run(chu)
    r.bold = dam
    r.italic = nghieng
    if ma:
        r.font.name = "Consolas"
        r.font.size = Pt(10.5)
    if mau:
        r.font.color.rgb = mau
    return r


def doan(d, chu, dam_dau=None):
    """Đoạn văn thường. `dam_dau` in đậm phần mở đầu (kiểu 'Đầu vào: ...')."""
    p = d.add_paragraph()
    if dam_dau:
        do(p, dam_dau, dam=True)
    do(p, chu)
    return p


def cham(d, ds, danh_so=False):
    """Danh sách gạch đầu dòng hoặc đánh số."""
    ki = "List Number" if danh_so else "List Bullet"
    for x in ds:
        if isinstance(x, tuple):
            p = d.add_paragraph(style=ki)
            do(p, x[0], dam=True)
            do(p, x[1])
        else:
            d.add_paragraph(x, style=ki)


def canh_bao(d, chu):
    """Khối cảnh báo — chỗ dễ sai, hoặc giới hạn phải nêu."""
    p = d.add_paragraph()
    p.paragraph_format.left_indent = Pt(18)
    p.paragraph_format.space_before = Pt(4)
    do(p, "⚠ ", dam=True, mau=DO)
    do(p, chu, nghieng=True)
    return p


def bang(d, dau_cot, hang, ten=None, co_chu=9.5):
    """Bảng có tiêu đề. `ten` là dòng 'Bảng 3.x: ...' đứng TRÊN bảng."""
    if ten:
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        do(p, ten, dam=True)
    t = d.add_table(rows=1, cols=len(dau_cot))
    t.style = "Light Grid Accent 1"
    for i, x in enumerate(dau_cot):
        o = t.rows[0].cells[i]
        o.text = ""
        do(o.paragraphs[0], x, dam=True)
    for h in hang:
        c = t.add_row().cells
        for i, x in enumerate(h):
            c[i].text = ""
            do(c[i].paragraphs[0], str(x))
    for r in t.rows:
        for o in r.cells:
            for p in o.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(co_chu)
    d.add_paragraph()
    return t


def ma_lenh(d, dong_ds, ten=None):
    """Khối giả mã. Mỗi phần tử là một dòng; giữ nguyên khoảng trắng đầu dòng."""
    if ten:
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        do(p, ten, dam=True)
    for dong in dong_ds:
        p = d.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.left_indent = Pt(18)
        r = p.add_run(dong if dong else " ")
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
    d.add_paragraph()


def cong_thuc(d, chu, ghi_chu=None):
    """Công thức toán, căn giữa."""
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(chu)
    r.italic = True
    r.font.size = Pt(12.5)
    if ghi_chu:
        q = d.add_paragraph()
        q.alignment = WD_ALIGN_PARAGRAPH.CENTER
        do(q, ghi_chu, nghieng=True, mau=XAM)
    return p


def hinh_chu(d, dong_ds, ten=None):
    """Sơ đồ vẽ bằng ký tự. `ten` là dòng 'Hình 3.x: ...' đứng DƯỚI hình."""
    for dong in dong_ds:
        p = d.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(dong if dong else " ")
        r.font.name = "Consolas"
        r.font.size = Pt(9)
    if ten:
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        do(p, ten, dam=True)
    d.add_paragraph()


def thuat_toan(d, so, ten, dau_vao, dau_ra, dong_ds, ghi_chu=None):
    """Một thuật toán trọn gói: tiêu đề · đầu vào · đầu ra · thủ tục · ghi chú."""
    p = d.add_paragraph()
    do(p, f"Thuật toán {so}: {ten}", dam=True)
    doan(d, dau_vao, dam_dau="Đầu vào: ")
    doan(d, dau_ra, dam_dau="Đầu ra: ")
    p = d.add_paragraph()
    do(p, "Thủ tục:", dam=True)
    ma_lenh(d, dong_ds)
    if ghi_chu:
        for g in ghi_chu:
            canh_bao(d, g)
