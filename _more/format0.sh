#!/usr/bin/env bash
# format.sh — 將資料夾下所有 .md 的 TeX 數學式修正為 GitHub 可正確渲染的格式
#
# 用法:
#   ./format.sh          # 處理當前資料夾（含子資料夾）
#   ./format.sh docs/    # 處理指定資料夾
#
# 處理規則:
#   1. 行內公式 $...$ 前後補上空格（行首、行尾不補）
#   2. 移除 $ 內側多餘空白：$ x $ -> $x$（GitHub 要求 $ 內側不可有空白）
#   3. \( ... \) 轉成 $...$
#   4. 不動程式碼區塊（``` / ~~~）、行內程式碼（`...`）、$$ 區塊公式
#
# 建議先 git commit，處理完用 git diff 檢查。

set -euo pipefail

dir="${1:-.}"

if [[ ! -d "$dir" ]]; then
  echo "找不到資料夾: $dir" >&2
  exit 1
fi

count=0
while IFS= read -r -d '' f; do
  perl -i -CSD -ne '
    BEGIN { $fence = 0; $blk = 0; }

    # 程式碼區塊
    if (/^\s*(?:```|~~~)/) { $fence = !$fence; print; next; }
    if ($fence)            { print; next; }

    # 獨立成行的 $$ 區塊公式
    if (/^\s*\$\$\s*$/)    { $blk = !$blk; print; next; }
    if ($blk)              { print; next; }

    # \( ... \) -> $...$
    s/\\\((.+?)\\\)/\$$1\$/g;

    # 保護行內程式碼與單行 $$...$$
    my @keep;
    s/`[^`]*`|\$\$.+?\$\$/push @keep, $&; "\x00" . $#keep . "\x00"/ge;

    # 找出行內公式，去除內側空白，用暫時標記包起來
    s{(?<![\\\$])\$(?!\$)((?:\\.|[^\$\\])+?)\$(?!\$)}{
      my $m = $1; $m =~ s/^\s+|\s+$//g;
      ($m eq "") ? $& : "\x01$m\x02";
    }ge;

    # 前後補空格（行首、行尾不補）
    s/(?<=\S)\x01/ \x01/g;
    s/\x02(?=\S)/\x02 /g;
    s/[\x01\x02]/\$/g;

    # 還原被保護的內容
    s/\x00(\d+)\x00/$keep[$1]/g;

    print;
  ' "$f"
  echo "已處理: $f"
  count=$((count + 1))
done < <(find "$dir" -type f -name '*.md' \
           -not -path '*/.git/*' -not -path '*/node_modules/*' -print0)

echo "完成，共處理 $count 個檔案。"