#!/usr/bin/env bash
#
# CÀI DÂY CHUYỀN TTS — Kokoro (tiếng Anh) + Kokoro-Vietnamese (tiếng Việt).
#
# Chạy:  bash tools/tts/cai_dat.sh
#
# ── VÌ SAO CÓ MÔI TRƯỜNG RIÊNG ──
# `figforge/` và mọi tệp trong `tools/*.py` đang chạy bằng Python 3.9 của hệ thống.
# Kokoro đòi Python 3.10-3.12. Cài đè lên python hệ thống là bốn quyển Toán mất
# đường dựng lại hình — nên dây chuyền này ở trong một venv RIÊNG, và không tệp nào
# ngoài thư mục này biết tới nó.
#
# Thư mục .venv/ model/ Kokoro-Vietnamese/ ra/ đều KHÔNG commit (xem .gitignore) —
# gần 1 GB. Máy mới thì chạy lại tệp này.
set -euo pipefail

O="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$O"

# ── 1 · Python 3.12 ──
PY="$(brew --prefix)/opt/python@3.12/bin/python3.12"
[ -x "$PY" ] || { echo "✗ chưa có python@3.12 — chạy: brew install python@3.12"; exit 1; }
command -v espeak-ng >/dev/null || { echo "✗ chưa có espeak-ng — chạy: brew install espeak-ng"; exit 1; }
echo "→ dùng $("$PY" -V)"

# ── 2 · venv ──
[ -d .venv ] || "$PY" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --quiet --upgrade pip wheel

# ── 3 · Kokoro tiếng Anh ──
# torch bản CPU là đủ: cả hai model chỉ 82 M tham số. Bản CUDA nặng thêm ~2 GB mà
# máy này không có GPU NVIDIA.
echo "→ cài Kokoro (tiếng Anh)…"
pip install --quiet torch --index-url https://download.pytorch.org/whl/cpu
pip install --quiet kokoro soundfile

# torch bản CPU cho Python 3.12 hiện là 2.2.2, biên dịch với NumPy 1.x. Để pip tự
# kéo NumPy 2 thì mọi lệnh `import torch` nhả ra một trang cảnh báo "_ARRAY_API not
# found" rồi chạy tiếp — kiểu hỏng khó chịu nhất, vì nó KHÔNG dừng, chỉ làm mọi
# đầu ra lẫn cảnh báo cho tới khi có ai đó đọc kỹ. Ghim lại cho dứt điểm.
pip install --quiet "numpy<2"

# ── 4 · Kokoro tiếng Việt (bản cộng đồng) ──
# `--depth 1` vẫn hay đứt giữa chừng với kho này; HTTP/1.1 + đệm lớn thì qua được.
echo "→ cài Kokoro-Vietnamese…"
[ -d Kokoro-Vietnamese ] || git -c http.version=HTTP/1.1 -c http.postBuffer=524288000 \
  clone --depth 1 https://github.com/iamdinhthuan/Kokoro-Vietnamese.git
pip install --quiet -e ./Kokoro-Vietnamese

# ── 5 · Báo cáo ──
python - <<'PY'
import importlib, sys
print(f"\npython {sys.version.split()[0]}")
for m in ("torch", "kokoro", "misaki", "soundfile", "kokoro_vietnamese"):
    try:
        mod = importlib.import_module(m)
        print(f"  ✓ {m:20s} {getattr(mod, '__version__', 'ok')}")
    except Exception as e:
        print(f"  ✗ {m:20s} {type(e).__name__}: {e}")
PY

echo
echo "Xong. Sinh clip mẫu:  bash tools/tts/nghe_thu.sh"
