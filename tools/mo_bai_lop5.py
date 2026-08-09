# -*- coding: utf-8 -*-
"""
LỚP 5 — làm màn MỞ BÀI ngắn lại và nêu thẳng bài toán.

    python3 tools/mo_bai_lop5.py --soat    # in bản soát, KHÔNG ghi
    python3 tools/mo_bai_lop5.py           # ghi vào data/ và web/public/content/

VẤN ĐỀ: màn mở bài nói CÙNG MỘT ĐOẠN HỘI THOẠI hai lần — một lần bằng lời (trung
bình 208 chữ), một lần nữa bằng hình `character_speech` chép lại đúng hai câu ấy
(trung bình 155 chữ). Bé phải đọc 363 chữ mới biết bài này hỏi gì, mà đọc xong
vẫn chưa thấy ĐỀ BÀI ở đâu.

SỬA:
  1. Lời mở = MỘT CÂU NÊU BÀI TOÁN, lấy đúng câu đề mà bài đã soạn sẵn
     (`knowledgeCore.canonicalExamples[0].problem`). Nêu bài toán trước, giải sau.
  2. Hình mở chỉ giữ CÂU SAI — cái bẫy mà bé hay mắc. Câu phản bác bỏ đi: nó
     thuộc phần giảng ở ngay màn sau, để ở đây là nói trước mất.
  3. BÀI HÌNH HỌC thì hình mở phải là HÌNH VẼ THẬT, không phải bong bóng lời
     thoại. Và chính hình ấy đi tiếp vào phần giải (`usedIn` mang cả hai chặng),
     để bé nhìn một hình từ đầu đến cuối chứ không phải mỗi chặng một hình khác.
"""
import copy, hashlib, json, os, sys

GOC_KHO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GOC_KHO, 'figforge'))
DATA = os.path.join(GOC_KHO, 'data', 'lessons')
PUBLIC = os.path.join(GOC_KHO, 'web', 'public', 'content', 'lessons')
HINH = os.path.join(GOC_KHO, 'web', 'public', 'content', 'figures')

# Nguyên mẫu vẽ HÌNH HỌC thật. Bài nào có một trong những hình này thì đó là bài
# hình, và hình ấy phải đứng ngay ở màn mở.
HINH_HOC = {'geo_shape', 'area_split', 'solid_3d', 'plane_geometry'}
DAI_NHAT = 150          # lời mở dài hơn ngần này là một đoạn văn, không phải đề bài

from render import RENDERERS, fname                          # noqa: E402


def ban_de(f):
    """Bản ĐỀ của một hình hình học: cùng hình, cùng số đo, BỎ HẾT đáp án.

    Màn mở nêu bài toán mà hình đã ghi sẵn "S = 30 cm²" thì còn gì để bé nghĩ.
    Nhưng cũng không được vẽ một hình khác: bác dặn phần giải phải theo đúng hình
    ấy. Nên hai bản dùng CHUNG points/segments/nhãn cạnh — chỉ khác phần kết quả.
    """
    g = copy.deepcopy(f)
    p = g['params']
    for k in ('formula', 'note', 'verdict', 'result'):
        p.pop(k, None)
    # nhãn có dấu '=' là nhãn KẾT QUẢ; nhãn số đo cho sẵn ("đáy 12") thì không có
    for sh in p.get('shapes') or []:
        if '=' in str(sh.get('label', '')):
            sh.pop('label', None)
    for se in p.get('segments') or []:
        if '=' in str(se.get('label', '')):
            se.pop('label', None)
    # KHÔNG đặt tiêu đề: lời dẫn ngay trên đã nêu đề bài, ô "Câu hỏi" ngay dưới đã
    # nêu cái bẫy. Ghi thêm chữ lên hình là lặp lần thứ ba — đúng thứ bác kêu.
    p['title'] = ''
    g['id'] = 'F0'
    g['usedIn'] = ['hook']
    g['caption'] = 'Đề bài — số đo đã cho'
    return g


def de_bai(d):
    """Câu nêu bài toán, lấy theo thứ tự ưu tiên của những câu ĐÃ SOẠN SẴN."""
    ce = (d.get('knowledgeCore') or {}).get('canonicalExamples') or []
    for x in [(ce[0].get('problem') if ce else ''),
              (d.get('workedExample') or {}).get('problem', ''),
              (d.get('objective') or {}).get('kidText', '')]:
        x = (x or '').strip()
        if 20 <= len(x) <= DAI_NHAT:
            return x
    return ''


SO_HINH = os.path.join(GOC_KHO, 'data', 'figure_manifest.json')


def main(chi_soat=False):
    n_loi = n_hinh = n_hh = 0
    bo_qua = []
    so_hinh = json.load(open(SO_HINH, encoding='utf-8'))
    for ten in sorted(os.listdir(DATA)):
        if not ten.startswith('DL_KSN5Q1_'):
            continue
        d = json.load(open(os.path.join(DATA, ten), encoding='utf-8'))
        man = (d.get('lecture') or {}).get('screens') or []
        hook = next((s for s in man if s.get('kind') == 'hook'), None)
        figs = d.get('figureSpec') or []
        f_hook = next((f for f in figs if 'hook' in (f.get('usedIn') or [])), None)
        if not hook:
            bo_qua.append((d['id'], 'không có màn mở'))
            continue
        # f_hook có thể là None: bài hình học đã bỏ hình lời thoại ở lượt trước.
        # Đừng bỏ qua cả bài — chính những bài ấy mới cần dựng bản đề.
        doi = False

        # 1 · lời mở = câu nêu bài toán
        de = de_bai(d)
        if not de:
            bo_qua.append((d['id'], 'không tìm được câu đề đủ ngắn'))
        elif hook.get('narration') != de:
            if chi_soat and n_loi < 4:
                print(f"── {d['id']}\n   TRƯỚC ({len(hook.get('narration',''))}): "
                      f"{hook.get('narration','')[:120]}\n   SAU   ({len(de)}): {de}")
            hook['narration'] = de
            n_loi += 1
            doi = True

        # 3 · bài hình học: hình vẽ thật lên màn mở, và đi tiếp vào phần giải
        f_hh = next((f for f in figs if f.get('archetype') in HINH_HOC), None)
        if f_hh is not None and not any(f.get('id') == 'F0' for f in figs):
            # Bỏ 'hook' khỏi hình lời thoại, KHÔNG thì giao diện vẫn lấy hình đầu
            # tiên khớp chặng — tức là vẫn hiện bong bóng chữ như cũ.
            if f_hook is not None:
                f_hook['usedIn'] = [u for u in (f_hook.get('usedIn') or []) if u != 'hook']
                if not f_hook['usedIn'] and f_hook is not f_hh:
                    figs.remove(f_hook)  # không chặng nào dùng thì đừng bắt bé tải
            f_hh['usedIn'] = [u for u in (f_hh.get('usedIn') or []) if u != 'hook'] \
                or ['teach_domain']
            f0 = ban_de(f_hh)
            f0['file'] = 'figures/' + fname(d['id'], 'F0')
            if not chi_soat:
                duong = os.path.join(HINH, os.path.basename(f0['file']))
                RENDERERS[f0['archetype']](f0['params'], duong)
                f0['sha256_16'] = hashlib.sha256(open(duong, 'rb').read()).hexdigest()[:16]
                # Sổ hình là nơi thứ ba chép mã kiểm; thiếu mục là cổng kiểm kêu.
                so_hinh[f"{d['id']}#F0"] = {
                    'file': f0['file'], 'caption': f0['caption'],
                    'archetype': f0['archetype'], 'sha256_16': f0['sha256_16']}
            d['figureSpec'] = [f0] + figs
            n_hh += 1
            doi = True
        # 2 · hình mở lời thoại: chỉ giữ câu SAI
        elif f_hook is not None and f_hook.get('archetype') == 'character_speech':
            ln = (f_hook.get('params') or {}).get('lines') or []
            giu = [l for l in ln if l.get('tone') == 'wrong'] or ln[:1]
            # So theo SỐ LỜI CÒN LẠI, đừng so `len(giu) != len(ln)`: 16 bài có cả
            # hai lời đều là câu sai, hai vế bằng nhau nên luật không chạy, hình
            # vẫn hai bong bóng như cũ mà bảng tổng kết lại báo đã sửa.
            if len(ln) > 1:
                f_hook['params']['lines'] = giu[:1]
                n_hinh += 1
                doi = True

        if doi and not chi_soat:
            for thu_muc in (DATA, PUBLIC):
                with open(os.path.join(thu_muc, ten), 'w', encoding='utf-8') as f:
                    json.dump(d, f, ensure_ascii=False, indent=1)

    if not chi_soat:
        with open(SO_HINH, 'w', encoding='utf-8') as f:
            json.dump(so_hinh, f, ensure_ascii=False, indent=1)
    print(f'{n_loi} lời mở rút thành câu đề · {n_hinh} hình mở bớt lời thoại · '
          f'{n_hh} bài hình học đưa hình vẽ lên màn mở'
          + (' (CHƯA ghi)' if chi_soat else ''))
    for i, ly in bo_qua:
        print(f'  ⚠ {i}: {ly}')
    return n_loi, n_hinh, n_hh


if __name__ == '__main__':
    main('--soat' in sys.argv)
