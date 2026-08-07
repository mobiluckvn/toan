# -*- coding: utf-8 -*-
"""Sinh figureSpec cho 168 micro bằng LUẬT SUY DẪN từ cấu trúc dữ liệu sẵn có.
Không đoán nội dung: mọi tham số đều lấy từ trường đã có trong DL json."""
import json, re, unicodedata

CHARS = ['Su Kem', 'Trí Long', 'Cáo Đề', 'Su Bống', 'sư phụ Trí Dũng']

_BAD = re.compile(r'[\U0001F000-\U0001FAFF\u2700-\u27BF\u2B00-\u2BFF]')

def _clip(s, n):
    s = _BAD.sub('', str(s))          # bỏ emoji/ký hiệu font không có (✓ ✗ 🟨…)
    s = ' '.join(s.split())
    if len(s) <= n:
        return s
    cut = s[:n-1].rsplit(' ', 1)[0]
    # không kết thúc ngay sau dấu toán tử hoặc giữa một con số thập phân dở dang
    while cut and (cut[-1] in '×+-=:/(' or re.search(r'\d[,.]$', cut)
                   or (re.search(r'\d$', cut) and re.match(r'^[,.]\d', s[len(cut):]))):
        cut = cut.rsplit(' ', 1)[0] if ' ' in cut else cut[:-1]
    return cut.rstrip(' ,;:') + '…'

# ── F1: character_speech từ màn hook ──────────────────────────────
def f_speech(p):
    hook = next((s for s in p['lecture']['screens'] if s['kind'] == 'hook'), None)
    if not hook or not hook.get('narration'): return None
    nar = ' '.join(hook['narration'].split())
    lines = []
    # tìm mẫu: <Tên> ... : "lời thoại"  (hoặc lời thoại trong ngoặc kép sau tên)
    for m in re.finditer(r'(' + '|'.join(map(re.escape, CHARS)) + r')([^"“]{0,60}?)[:\-–—]?\s*["“]([^"”]{5,150})["”]', nar):
        who, say = m.group(1), m.group(3)
        tone = 'wrong' if who in ('Trí Long', 'Cáo Đề') else 'right'
        say = say.strip().strip('"“”')
        if len(say) >= 10 or re.search(r'\d', say):
            lines.append(dict(who=who, say=_clip(say, 120), tone=tone))
    if len(lines) < 2:
        # dự phòng: cắt câu đầu cho Trí Long (tình huống), câu có Su Kem cho Su Kem
        parts = re.split(r'(?<=[.!?])\s+', nar)
        first = _clip(parts[0], 120) if parts else ''
        sk = next((x for x in parts if 'Su Kem' in x or 'Su Bống' in x), '')
        if len(first) < 14:
            first = _clip(' '.join(parts[:2]), 120) if len(parts) > 1 else first
        lines = [dict(who='Trí Long', say=first, tone='wrong')]
        if sk: lines.append(dict(who='Su Kem', say=_clip(re.sub(r'^.*?Su Kem[^:]*:?\s*', '', sk), 120), tone='right'))
    cap = (hook.get('display') or {}).get('caption') or ''
    return dict(archetype='character_speech',
                params=dict(title=_clip(cap or 'TÌNH HUỐNG MỞ BÀI', 60), lines=lines[:2]),
                caption='Tình huống mở bài — chỗ bạn Trí Long hay nhầm')

# ── F2: hình lõi — ưu tiên cấu trúc sẵn có ────────────────────────
def f_core(p):
    scr = p['lecture']['screens']
    # (a) counter_example → two_way_compare
    for s in scr:
        d = s.get('display') or {}
        if d.get('type') == 'counter_example' and d.get('cases'):
            bad = next((c for c in d['cases'] if not c.get('valid')), None)
            good = next((c for c in d['cases'] if c.get('valid')), None)
            if bad and good:
                return dict(archetype='two_way_compare',
                    params=dict(title='CÙNG MỘT ĐỀ — HAI CÁCH LÀM',
                        wrong=dict(head='CÁCH SAI', steps=[_clip(bad['input'], 34)],
                                   result=_clip(re.sub(r'^[✗✓]\s*', '', bad['output']), 26)),
                        right=dict(head='CÁCH ĐÚNG', steps=[_clip(good['input'], 34)],
                                   result=_clip(re.sub(r'^[✗✓]\s*', '', good['output']), 26)),
                        verdict=_clip(good.get('reason') or '', 52)),
                    caption='Hai ngả — một đúng một sai, khác nhau đúng một bước')
    # (b) step_by_step (≤4 dòng ngắn) → ladder_steps
    for s in scr:
        d = s.get('display') or {}
        if d.get('type') == 'step_by_step' and d.get('lines') and 2 <= len(d['lines']) <= 4:
            if max(len(x) for x in d['lines']) <= 52:
                return dict(archetype='ladder_steps',
                    params=dict(title=_clip(p['objective']['text'].split('—')[0].split(':')[0], 58),
                                steps=[dict(text=_clip(x, 40)) for x in d['lines']],
                                note='Làm đúng thứ tự từng bậc'),
                    caption='Các bước leo dần — bậc dưới xong mới lên bậc trên')
    # (c) display.spec dict → formula_card nhiều dòng
    for s in scr:
        d = s.get('display') or {}
        sp = d.get('spec')
        if isinstance(sp, dict) and len(sp) >= 2:
            tones = ['navy', 'teal', 'gold']
            rows = [dict(text=_clip(v, 46), tone=tones[i % 3])
                    for i, v in enumerate(list(sp.values())[:3]) if isinstance(v, str)]
            if len(rows) >= 2:
                return dict(archetype='formula_card',
                    params=dict(title=_clip(p['title'].split('—')[0], 58), formulas=rows),
                    caption='Ý chính của bài gói trong mấy dòng')
    # (d) dự phòng: ca mẫu chuẩn → thẻ đề + lời giải
    ces = p['knowledgeCore'].get('canonicalExamples') or []
    if ces:
        c = ces[0]
        return dict(archetype='formula_card',
            params=dict(title=_clip('CA MẪU · ' + c.get('case', ''), 56),
                        formulas=[dict(label='ĐỀ', text=_clip(c['problem'], 46), tone='navy'),
                                  dict(label='LỜI GIẢI', text=_clip(c['solution'], 46), tone='teal')]),
            caption='Ca mẫu chuẩn của bài')
    return None

# ── F3: thẻ nguyên tắc + thần chú ─────────────────────────────────
def f_rule(p):
    K = p['knowledgeCore']
    rows = []
    for i, st in enumerate(K['statements'][:2]):
        txt = ' '.join(st['text'].split())
        head = txt.split(':')[0] if ':' in txt else txt
        body = txt.split(':', 1)[1].strip() if ':' in txt else ''
        # lấy mệnh đề đầu tiên, ưu tiên cắt ở ';' rồi ',' — không cắt giữa công thức
        for sep in (';', ' — '):
            if sep in body and len(body) > 42:
                body = body.split(sep)[0].strip()
        if len(body) > 46:                      # dấu phẩy KHÔNG đứng trước chữ số mới là ngắt câu
            parts = re.split(r',(?!\s*\d)', body)
            if len(parts) > 1 and len(parts[0]) >= 18:
                body = parts[0].strip()
        # ưu tiên GIỮ phần công thức: đoạn sau dấu ':' cuối thường là công thức
        if body and ':' in body:
            cand = body.split(':')[-1].strip()
            if 8 <= len(cand) <= 46 and ('=' in cand or '×' in cand):
                body = cand
        if not body:
            body, head = head, ''
        elif len(body) > 46:
            body = _clip(body, 46)          # cắt an toàn, không phá số thập phân
        rows.append(dict(label=_clip(head, 50) if head else None,
                         text=_clip(body, 46), tone=['navy', 'teal'][i]))
    rows = [{k: v for k, v in r.items() if v} for r in rows]
    return dict(archetype='formula_card',
                params=dict(title='NGUYÊN TẮC CẦN NHỚ', formulas=rows,
                            mantra=_clip(K['mantra'], 56)),
                caption='Thẻ ghi nhớ — con đọc to trước khi làm bài')

# ── ghép ──────────────────────────────────────────────────────────
def build(mid, p):
    out, uses = [], ['hook', 'teach_core', 'mantra']
    for i, fn in enumerate((f_speech, f_core, f_rule)):
        f = fn(p)
        if f:
            f['id'] = f'F{len(out)+1}'
            f['usedIn'] = [uses[i]]
            out.append(f)
    return out

if __name__ == '__main__':
    km = json.load(open('/mnt/user-data/outputs/km_v1_23.json'))
    N = km['nodes']
    ids = [f'DL:KSN5Q1.B{b}.M{k}' for b in range(1, 57) for k in (1, 2, 3)]
    total, byarch = 0, {}
    specs = {}
    for mid in ids:
        fs = build(mid, N[mid]['payload'])
        specs[mid] = fs
        total += len(fs)
        for f in fs: byarch[f['archetype']] = byarch.get(f['archetype'], 0) + 1
    json.dump(specs, open('/home/claude/figspecs.json', 'w'), ensure_ascii=False, indent=1)
    print('tổng hình:', total, '| trung bình/micro:', round(total/168, 2))
    for k, v in sorted(byarch.items(), key=lambda x: -x[1]): print(f'  {v:4d}  {k}')
    print('micro thiếu hình lõi:', sum(1 for v in specs.values() if len(v) < 3))
