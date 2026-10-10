# 1977：Bourne Shell（sh）問世

## 事件
1977 年，貝爾實驗室的 **Stephen Bourne** 發表 **Bourne Shell**（程式名仍為 `sh`），隨 UNIX 第七版（Version 7 Unix）問世。這是 shell script 語言史上最重要的一年：現代 shell 腳本語法至此奠定，五十年來幾乎所有 shell 都以它為祖先。

## 新語法的年份、理論與實用原因

### 1. 變數與參數展開（`name=value`、`$name`）
- **理論原因**：shell 要成為「語言」而非「命令列表」，變數是狀態的最低要求。
- **實用原因**：路徑、檔名、設定值可以集中管理（如 `$PATH`），腳本可移植。
- **彌補缺陷**：Thompson Shell 完全沒有變數，同樣的值必須重複寫死。

### 2. 控制流程：`if/then/elif/else/fi`
- **理論原因**：條件判斷是圖靈完備性的最低要求。
- **實用原因**：腳本可以「檔案存在才執行」「參數正確才繼續」。
- **彌補缺陷**：Mashey Shell（1975）的 `if` 是粗糙的巨集展開；Thompson Shell 完全無條件判斷。
- **語法特色**：Bourne 故意用 `fi`、`esac`、`done` 收尾——他刻意**不採用 C 語法**（當時 shell 用 Algol 風格的前置處理器寫成），讓語法在視覺上與 C 程式區隔，腳本讀起來像英文敘述。

### 3. 迴圈：`for ... in ... do ... done`、`while ... do ... done`
- **理論原因**：重複執行是腳本自動化的本質。
- **實用原因**：批次處理檔案（`for f in *.txt; do ...`）是系統管理最常見的需求。
- **彌補缺陷**：以前只能用外部工具（如 `find` 的 `-exec`）或重複呼叫腳本。

### 4. 多重分支：`case ... esac`
- **理論原因**：多重分支是結構化程式設計（Dijkstra 學派）的標準配備。
- **實用原因**：處理選項（`-a`、`-b`、`-c`）或系統類型分支時比一串 `if` 清晰。
- **彌補缺陷**：巢狀 `if` 的可讀性災難。

### 5. 函數（1978/1980 加入）
- **理論原因**：結構化程式設計的函數抽象，避免重複程式碼。
- **實用原因**：大型系統啟動腳本（如 `/etc/rc`）需要模組化。
- **彌補缺陷**：只能靠「呼叫另一支腳本」模擬函數，開銷大且無回傳值。

### 6. Here-document（`<<`）——1977 年發明
- **發明年份**：1977 年由 **Stephen Bourne** 在 Bourne Shell 中發明（`<<` 語法），shell 於 1979 年隨 **UNIX 第 7 版**正式對外發佈。這是 shell 語言史上「多行文字內嵌」語法的誕生點，之後 Perl（1987）、Ruby（1995）、PHP（1995）等語言都直接繼承了 `<<EOF` 的語法形式。
- **理論原因**：把「多行文字」內嵌在腳本中作為某程式的標準輸入——文字流（1973）與重導向（1971）的組合必然產物。
- **實用原因**：產生設定檔、送郵件、內嵌文件、批次建立測試輸入。
- **彌補缺陷**：多行輸入必須另建暫存檔，既慢（磁碟 I/O）又要在腳本中管理暫存檔的生命週期。
- **後續演化**：bash 3.0（2004）加入 here-string `<<<`（單行文字內嵌，不需 EOF 結尾）；zsh 支援未閉合引號的 EOF 防展開變體。

### 7. 環境變數（`export`）
- **理論原因**：行程的環境（environment）概念——子行程繼承父行程的狀態。
- **實用原因**：`PATH`、`TERM` 等設定可傳遞給所有子程式，成為 UNIX 設定的通用機制。
- **彌補缺陷**：一般變數無法跨行程傳遞。

### 8. 標準輸入/輸出/錯誤與 `2>` 重導向
- **實用原因**：錯誤訊息與正常輸出分流，管線才不會被錯誤訊息污染。
- **彌補缺陷**：Thompson/早期 shell 只有一個輸出流。

## 語法設計的爭議
Bourne 拒絕 C 語法（`if (x) {}`）換來了腳本可讀性，但代價是後來的 csh 使用者抱怨 Bourne 語法「不像 C」，這直接催生了 1978 年的 C Shell，也埋下了「csh 好交互、sh 好腳本」的長期分裂。

## 程式範例：Bourne Shell 的語法全貌

```sh
#!/bin/sh
# 1. 變數與參數展開：狀態集中管理
BACKUP_DIR=/backup
SRC=$1                      # 腳本參數
echo "備份 $SRC 到 $BACKUP_DIR"
```

```sh
# 2. 條件判斷：檔案存在才執行
if [ -d "$SRC" ]; then
  echo "目錄存在"
elif [ -f "$SRC" ]; then
  echo "是檔案"
else
  echo "不存在"; exit 1
fi
```

```sh
# 3. 迴圈：批次處理檔案
for f in *.txt; do
  cp "$f" "$BACKUP_DIR/$f"    # 引號防止空格檔名出錯
done

# while 迴圈：逐行讀檔
while read line; do
  echo "處理: $line"
done < list.txt
```

```sh
# 4. 多重分支：處理選項
case "$1" in
  -a) echo "全部" ;;
  -b) echo "備份" ;;
  *)  echo "用法: $0 [-a|-b]"; exit 1 ;;
esac
```

```sh
# 5. 函數：模組化
usage() {
  echo "用法: $0 <來源> <目的>"
}
```

```sh
# 6. Here-document（1977 年發明）：多行文字內嵌
mail -s "備份完成" admin <<EOF
備份作業已完成
時間: $(date)
EOF

# here-doc 中「quoted EOF」防止變數展開
cat <<'EOF' > config.txt
路徑是 $PATH（原文輸出，不展開）
EOF
```

```bash
# 2004 年 bash 3.0 的 here-string `<<<`：單行內嵌，不需 EOF 結尾
grep "$USER" <<< "$(who)"
tr a-z A-Z <<< "hello"
```

```sh
# 7. 環境變數：跨行程傳遞設定
export PATH="$PATH:/usr/local/bin"   # 子行程繼承

# 8. 錯誤分流：stdout 與 stderr 分開
prog > out.txt 2> err.txt
prog > all.txt 2>&1     # 2>&1 表示「stderr 併入 stdout」
```

## 彌補了什麼缺陷
彌補了 Thompson/Mashey Shell「無變數、無控制流程、無函數」的缺陷，讓 shell 從命令列表升級為圖靈完備的腳本語言，並成為 1992 年 POSIX shell 標準的直接藍本。

## 相關條目
- [1971-ThompsonShell問世](1971-ThompsonShell問世.md)
- [1973-管線pipe問世](1973-管線pipe問世.md)
- [1978-CShell-csh問世](1978-CShell-csh問世.md)
- [1992-POSIXShell標準化](1992-POSIXShell標準化.md)
