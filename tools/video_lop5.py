#!/usr/bin/env python3
"""NỐI VIDEO GIẢNG VÀO BÀI LỚP 5.

    python3 tools/video_lop5.py            (sửa web/public/content/lessons/*.json)
    python3 tools/video_lop5.py --thu      (chỉ in, không ghi)

── VÌ SAO LỚP 5 PHẢI CÓ BỘ RIÊNG ──

Ba quyển kia có bước "dựng theo khuôn chung" (`dung_khuon_chung*.py`) — chỗ ấy vừa
sinh bản cho app vừa nối video. Lớp 5 KHÔNG có bước ấy: sách viết thẳng ra đúng
khuôn đích, `data/lessons/` là bản gốc còn `web/public/content/lessons/` là bản làm
việc mà các bước sau (`dinh_dang` · `bai_mau` · `goi_y`) sửa tại chỗ.

Nên bộ này phải LÀM ĐI LÀM LẠI ĐƯỢC (idempotent): chạy hai lần cho cùng kết quả,
và chạy khi chưa có video thì không đụng gì. Có thế mới xen được vào dây chuyền mà
không sợ thứ tự.

── THU BÀI VỀ ĐÚNG HÌNH DẠNG BA QUYỂN KIA ──

Video thay MỞ BÀI và BÀI GIẢNG, nên:
    knowledgeCore.statements → rỗng
    knowledgeCore.mantra     → rỗng   (không thì `buildFlow` còn một bước chữ)
    lecture.screens          → CHỈ giữ màn có `item`
    figureSpec               → chỉ giữ hình gắn vào câu hỏi

⚠ KHÁC BA QUYỂN KIA MỘT CHỖ: chặng giảng của lớp 5 có bước `check` — một CÂU HỎI
tương tác lấy từ màn `checkpoint`, không phải màn chữ. Bỏ nó đi là mất một câu hỏi
thật. Nên lọc theo `s.get('item')` chứ đừng lọc theo `kind`.

⚠ VÀ HÌNH `mantra`: mỗi micro khai một hình `F3` dùng cho bước `mantra`, mà bước ấy
KHÔNG mang khoá hình nào — 168 hình chưa từng hiện lên kể từ ngày dựng. Bộ này dọn
luôn, nên `hinh_co_ai_ve.test.mjs` phải hạ ngưỡng `lessons` theo.
"""
import argparse
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
BAI = GOC / 'web' / 'public' / 'content' / 'lessons'
VIDEO = GOC / 'web' / 'public' / 'content' / 'toan' / 'video'


def thu_gon(d: dict, ten_tep: str) -> bool:
    """Trả về True nếu có gì đó thay đổi."""
    doi = False
    if d.get('video', {}).get('giang') != f'{ten_tep}_giang.mp4':
        d['video'] = {'giang': f'{ten_tep}_giang.mp4'}
        doi = True

    kc = d.setdefault('knowledgeCore', {})
    if kc.get('statements'):
        kc['statements'] = []
        doi = True
    if kc.get('mantra'):
        kc['mantra'] = ''
        doi = True
    # ⚠ PHẢI DỌN CẢ `vocabulary`. Bước `mantra` trong `flow.js` sống nếu CÓ MỘT
    # TRONG HAI: câu chốt, hoặc danh sách từ. Xoá mỗi câu chốt thì bước ấy vẫn dựng,
    # chỉ là hiện một thẻ toàn từ khoá — vẫn là chữ giảng, đúng thứ video vừa thay.
    # Tệ hơn: mục đầu của danh sách ấy là "nhân vật: Su Kem, Trí Long…", nên bé xem
    # xong một video KHÔNG nhân vật lại bị dội ngay tên nhân vật vào mặt.
    # Với môn Toán, `vocabulary` chỉ được vẽ ở đúng bước này (StepView), nên dọn ở
    # đây là dọn sạch. Bản gốc `data/lessons/` giữ nguyên, không đụng tới.
    if kc.get('vocabulary'):
        kc['vocabulary'] = []
        doi = True

    sc = (d.get('lecture') or {}).get('screens') or []
    giu = [s for s in sc if s.get('item')]
    if len(giu) != len(sc):
        d['lecture']['screens'] = giu
        doi = True

    fs = d.get('figureSpec') or []
    con = [h for h in fs
           if all(str(u).startswith('item:') for u in (h.get('usedIn') or []))]
    if len(con) != len(fs):
        d['figureSpec'] = con
        doi = True
    return doi


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--thu', action='store_true', help='chỉ in, không ghi')
    ns = ap.parse_args(argv)

    co = doi = chua = 0
    bo_hinh = bo_man = 0
    for p in sorted(BAI.glob('DL_*.json')):
        ten = p.stem
        if not (VIDEO / f'{ten}_giang.mp4').exists():
            chua += 1
            continue
        co += 1
        d = json.loads(p.read_text('utf8'))
        truoc_h = len(d.get('figureSpec') or [])
        truoc_m = len((d.get('lecture') or {}).get('screens') or [])
        if thu_gon(d, ten):
            doi += 1
            bo_hinh += truoc_h - len(d.get('figureSpec') or [])
            bo_man += truoc_m - len(d['lecture']['screens'])
            if not ns.thu:
                p.write_text(json.dumps(d, ensure_ascii=False, indent=1), 'utf8')

    print(f'lớp 5: {co} micro có video · {doi} bài vừa thu gọn · '
          f'{chua} micro chưa có video')
    if doi:
        print(f'   bỏ {bo_man} màn giảng chữ · {bo_hinh} hình không màn nào vẽ')
    if ns.thu:
        print('(--thu: chưa ghi gì cả)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
