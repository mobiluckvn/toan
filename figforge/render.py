# -*- coding: utf-8 -*-
"""render.py — đọc figureSpec → gọi đúng renderer → xuất PNG + manifest."""
import json, os, sys, hashlib, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arch_a import formula_card, character_speech, two_way_compare, motion_track
from arch_b import plane_geometry, solid_3d, clock_face, ladder_steps
from arch_c import (bar_diagram, balance_scale, grid_count, fraction_split,
                    place_value_chart, fence_posts, venn_two, cycle_ring, pair_sum,
                    area_split, chain_cancel, level_bars, sum_diff_bars,
                    before_after_parts, stack_compare, venn_three, geo_shape)

# Phải đăng ký ĐỦ 25 nguyên mẫu đang dùng trong dữ liệu. Trước đây chỉ có 12, nên
# 91 hình rơi vào nhánh lỗi và im lặng giữ nguyên bản cũ mỗi lần vẽ lại.
RENDERERS = dict(formula_card=formula_card, character_speech=character_speech,
                 two_way_compare=two_way_compare, motion_track=motion_track,
                 plane_geometry=plane_geometry, solid_3d=solid_3d, clock_face=clock_face,
                 ladder_steps=ladder_steps, bar_diagram=bar_diagram, balance_scale=balance_scale,
                 grid_count=grid_count, fraction_split=fraction_split,
                 place_value_chart=place_value_chart, fence_posts=fence_posts,
                 venn_two=venn_two, cycle_ring=cycle_ring, pair_sum=pair_sum,
                 area_split=area_split, chain_cancel=chain_cancel, level_bars=level_bars,
                 sum_diff_bars=sum_diff_bars, before_after_parts=before_after_parts,
                 stack_compare=stack_compare, venn_three=venn_three, geo_shape=geo_shape)

def fname(mid, fid):
    return mid.replace('DL:', '').replace('.', '_') + f'_{fid}.png'

def render_all(specs, outdir, only=None):
    os.makedirs(outdir, exist_ok=True)
    man, errs = {}, []
    for mid, figs in specs.items():
        if only and not any(only(mid) for _ in [0]):
            continue
        for f in figs:
            fn = fname(mid, f['id'])
            path = os.path.join(outdir, fn)
            try:
                RENDERERS[f['archetype']](f['params'], path)
                h = hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]
                man[f"{mid}#{f['id']}"] = dict(file=fn, archetype=f['archetype'],
                                               caption=f.get('caption', ''), sha256_16=h)
            except Exception as e:
                errs.append((mid, f['id'], f['archetype'], repr(e)[:120]))
    return man, errs

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--specs', default='/home/claude/figspecs.json')
    ap.add_argument('--out', default='/home/claude/figs/all')
    ap.add_argument('--chapter', type=int, default=None)
    a = ap.parse_args()
    specs = json.load(open(a.specs))
    if a.chapter:
        lo, hi = (a.chapter-1)*4 + 1, a.chapter*4
        specs = {k: v for k, v in specs.items()
                 if lo <= int(k.split('.B')[1].split('.M')[0]) <= hi}
    man, errs = render_all(specs, a.out)
    json.dump(man, open(os.path.join(a.out, 'figure_manifest.json'), 'w'),
              ensure_ascii=False, indent=1)
    print(f'render: {len(man)} hình · lỗi: {len(errs)}')
    for e in errs[:12]: print('  ✗', e)
