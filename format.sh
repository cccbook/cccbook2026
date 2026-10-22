#!/usr/bin/env bash
# format.sh — 將資料夾下所有 .md 的公式修正：
#   1. 區塊公式: 統一拆成獨立行 $$ ... $$ 並留空行
#   2. 行內公式: 一律轉為 GitHub 專用 $`...`$（徹底防止 Markdown 語法干擾）
#
# 用法:
#   ./format.sh
#   ./format.sh docs/

set -euo pipefail

dir="${1:-.}"

if [[ ! -d "$dir" ]]; then
  echo "找不到資料夾: $dir" >&2
  exit 1
fi

count=0
while IFS= read -r -d '' f; do
  perl -i -CSD -0777 -pe '
    # 1. 保護 Code Block (``` 或 ~~~)
    my @codeblocks;
    s{(```|~~~)[^\n]*\n.*?\n\s*\1}{
      push @codeblocks, $&;
      "__CODE_BLOCK_" . $#codeblocks . "__"
    }gse;

    # 2. 保護原本已經是 $`...`$ 的內容（避免重複包覆）
    my @gh_math;
    s{\$`([^`\n]+)`\$}{
      push @gh_math, $&;
      "__GH_MATH_" . $#gh_math . "__"
    }ge;

    # 3. 保護一般行內程式碼 (`...`)
    my @inline_codes;
    s{`[^`\n]+`}{
      push @inline_codes, $&;
      "__INLINE_CODE_" . $#inline_codes . "__"
    }ge;

    # 4. 將 \( ... \) 先轉為 $...$
    s/\\\((.+?)\\\)/\$$1\$/gs;

    # 5. 處理 $$...$$ 區塊公式：
    #    - 確保前後有空行隔開
    #    - 確保 $$ 各自獨立成行
    #    - 吸收外側黏著的標點符號至公式內
    s{(?:\n\s*)?\$\$\s*(.+?)\s*\$\$\s*([.,;!?，。！？])?}{
      my $content = $1;
      my $punct = $2 // "";
      $content =~ s/^\s+|\s+$//g;
      $content =~ s/&amp;/&/g; # 消除錯誤轉義
      if ($punct ne "") {
        $content .= " " . $punct;
      }
      "\n\n\$\$\n" . $content . "\n\$\$\n\n"
    }gse;

    # 6. 其餘所有的行內公式 $...$ 一律改為 $`...`$
    s{(?<![\\\$])\$(?!\$)((?:\\.|[^\$\n\\])+?)\$(?!\$)}{
      my $m = $1;
      $m =~ s/^\s+|\s+$//g;
      $m =~ s/&amp;/&/g; # 消除錯誤轉義

      if ($m eq "") {
        "\$"
      } else {
        # 標記成 GitHub 的 $`...`$
        "\x01`" . $m . "`\x02"
      }
    }ge;

    # 7. 行內公式外側補空格（避免中文字與公式直接黏在一起造成解析困擾）
    s/(?<=\S)\x01/ \x01/g;
    s/\x02(?=\S)/\x02 /g;
    s/[\x01\x02]/\$/g;

    # 8. 清理多餘連續空行（超過2行縮成1行）
    s/\n{3,}/\n\n/g;

    # 9. 還原保護內容
    s/__INLINE_CODE_(\d+)__/$inline_codes[$1]/ge;
    s/__GH_MATH_(\d+)__/$gh_math[$1]/ge;
    s/__CODE_BLOCK_(\d+)__/$codeblocks[$1]/ge;
  ' "$f"
  echo "已處理: $f"
  count=$((count + 1))
done < <(find "$dir" -type f -name '*.md' \
           -not -path '*/.git/*' -not -path '*/node_modules/*' -print0)

echo "完成，共處理 $count 個檔案。"