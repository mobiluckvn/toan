#!/usr/bin/env python3
"""Gắn đáp án viết tay vào các khối đấu Quyển 2 — để máy chấm được.

    python3 tools/dapan_quyen2.py

VÌ SAO CÓ TỆP NÀY: `tools/chuan_quyen2.py` rút đáp số bằng luật, và cố ý rút rất dè
(lời chữa của sách là văn xuôi, đoán bừa "con số cuối cùng" là chấm oan con). Kết quả
102/314 câu máy chấm, 212 câu để con tự chấm. Tự chấm thì đúng tinh thần "chữa đề kiểu
giám khảo", NHƯNG sổ phụ huynh và bảng cô giáo không đo được gì ở quyển luyện thi — mà
đó lại là quyển cần đo nhất.

`data/quyen2_dapan_tay.json` là phần người làm: đọc tay từng lời chữa rồi khai đáp án.
Tệp này chỉ VÁ vào, không dựng lại từ đầu.

⚠ VÁ CHỨ KHÔNG DỰNG LẠI — đây là chỗ dễ mất trắng nhất:
`web/public/content/quyen2/` đã qua `tools/dinh_dang.py` (markdown + LaTeX), còn
`data/quyen2/` thì chưa. Chạy lại `chuan_quyen2.py` là ghi đè trọn tệp và MẤT SẠCH
định dạng, mà dữ liệu vẫn hợp lệ nên KHÔNG CÓ GÌ BÁO. Nên ở đây chỉ đụng vào đúng ba
trường `answerKey`, `format`, `choices` của từng câu, giữ nguyên mọi thứ khác.

Chạy lại bao nhiêu lần cũng ra một kết quả (idempotent).
"""
import json
import os

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAY = os.path.join(GOC, 'data', 'quyen2_dapan_tay.json')
THU_MUC = [os.path.join(GOC, 'data', 'quyen2'),
           os.path.join(GOC, 'web', 'public', 'content', 'quyen2')]


def doc_tay():
    """Bỏ các khoá ghi chú (bắt đầu bằng '_'), giữ lại đúng bảng đáp án."""
    d = json.load(open(TAY, encoding='utf-8'))
    return {k: v for k, v in d.items() if not k.startswith('_')}


def ma_khoi(khoi_id):
    """'DR:KSN5Q2.V01' → 'V01'"""
    return khoi_id.rsplit('.', 1)[-1]


def main():
    tay = doc_tay()
    dung, thua = 0, set(tay)
    tong, may = 0, 0

    for thu_muc in THU_MUC:
        for ten in sorted(os.listdir(thu_muc)):
            if not ten.startswith('DR_KSN5Q2_') or not ten.endswith('.json'):
                continue
            p = os.path.join(thu_muc, ten)
            d = json.load(open(p, encoding='utf-8'))
            mk = ma_khoi(d['id'])
            doi = False

            for c in d.get('cau', []):
                khoa = f"{mk}#{c['id']}"
                if thu_muc is THU_MUC[0]:
                    tong += 1
                v = tay.get(khoa)
                if v is None:
                    if thu_muc is THU_MUC[0] and c.get('answerKey'):
                        may += 1
                    continue
                thua.discard(khoa)
                if thu_muc is THU_MUC[0]:
                    dung += 1
                    may += 1
                c['answerKey'] = v['answerKey']
                if v.get('choices'):
                    # Đáp án bằng CHỮ → trắc nghiệm: bắt con gõ đúng từng chữ
                    # "KHÔNG chắc đúng" là kiểm kỹ năng gõ, không kiểm toán.
                    c['format'] = 'mcq'
                    c['choices'] = v['choices']
                else:
                    c.pop('format', None)
                    c.pop('choices', None)
                # Câu đã máy chấm được thì không còn là câu tự luận nữa.
                c.pop('tuLuan', None)
                doi = True

            if doi:
                with open(p, 'w', encoding='utf-8') as f:
                    json.dump(d, f, ensure_ascii=False, indent=1)

    if thua:
        raise SystemExit('⚠ khoá trong sổ tay không khớp câu nào: '
                         + ', '.join(sorted(thua)))

    print(f'{dung} câu được gắn đáp án tay')
    print(f'   máy chấm {may}/{tong} câu ({round(may / tong * 100)}%)'
          f' · còn {tong - may} câu tự chấm')


if __name__ == '__main__':
    main()
