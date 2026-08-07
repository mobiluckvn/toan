# Công cụ

* `../web/tools/seed_content_index.mjs` — nạp chỉ mục 168 micro lên Firestore
* `../figforge/render.py` — render hình từ figureSpec
* `../figforge/gen_figurespec.py` — sinh figureSpec khái niệm bằng luật suy dẫn

## Render lại toàn bộ hình
```bash
cd figforge && python3 render.py --specs figspecs_all.json --out ../web/public/content/figures
```
