#!/usr/bin/env bash
# gh-build.sh — 在本機用和 GitHub Actions (.github/workflows/pages.yml) 相同的步驟
# 建置網站，並以 gh-pages 的子路徑 /cccbook2026/ 提供瀏覽，確認上線後的呈現。
#
# 用法:
#   ./gh-build.sh               # 建置 + Pagefind 搜尋索引 + 啟動伺服器 (port 8000)
#   ./gh-build.sh --no-search   # 略過 Pagefind (較快，只是搜尋不能用)
#   PORT=8080 ./gh-build.sh     # 換 port
#
# 第一次執行會在 .venv/ 建立 Python 虛擬環境並安裝套件（.venv 已在 .gitignore）。

set -euo pipefail

cd "$(dirname "$0")"

port="${PORT:-8000}"
search=1
[[ "${1:-}" == "--no-search" ]] && search=0

venv=".venv"
if [[ ! -x "$venv/bin/mkdocs" ]]; then
  echo "==> 建立 $venv 並安裝 mkdocs 套件"
  python3 -m venv "$venv"
  "$venv/bin/pip" install -q mkdocs-material mkdocs-gen-files mkdocs-literate-nav mkdocs-minify-plugin
fi

echo "==> mkdocs build"
DISABLE_MKDOCS_2_WARNING=true NO_MKDOCS_2_WARNING=1 "$venv/bin/mkdocs" build -q

if [[ $search == 1 ]]; then
  echo "==> pagefind 搜尋索引"
  npx -y pagefind@latest --site site
fi

# gh-pages 網址是 https://cccbook.github.io/cccbook2026/，
# 本機也放在同樣的子路徑下，相對路徑問題才看得出來。
root="$(mktemp -d)"
trap 'rm -rf "$root"' EXIT
ln -s "$PWD/site" "$root/cccbook2026"

url="http://localhost:$port/cccbook2026/"
echo "==> 瀏覽 $url  (Ctrl+C 結束)"
(sleep 1 && command -v open >/dev/null && open "$url") &
cd "$root" && python3 -m http.server "$port"
