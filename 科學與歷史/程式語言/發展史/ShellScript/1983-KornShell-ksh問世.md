# 1983：Korn Shell（ksh）問世

## 事件
1983 年，貝爾實驗室的 **David Korn** 發表 **Korn Shell**（`ksh`），隨 AT&T System V UNIX 問世。ksh 的目標雄心明確：**完全向後相容 Bourne Shell 的腳本語法，同時吸收 C Shell 的全部交互功能**——終結「交互用 csh、腳本用 sh」的分裂。

## 新語法與特性及其理論、實用原因

### 1. 算術展開 `$(( expr ))`
- **理論原因**：腳本語言需要圖靈完備的整數運算，內建運算可避免行程 fork 開銷。
- **實用原因**：`x=$(( x + 1 ))` 比 `x=\`expr $x + 1\`` 快一個數量級（不用 fork 外部程式）且可讀。
- **彌補缺陷**：Bourne Shell 沒有內建算術，每次運算都要 fork `expr` 或 `test`；csh 的 `@` 語法只存在於 csh。

### 2. 陣列（`set -A arr` / 後期 ksh93 的 `arr=( ... )`）
- **理論原因**：序列資料是一等抽象，變數只能存一個值太貧乏。
- **實用原因**：批次處理檔案清單、設定值清單。
- **彌補缺陷**：Bourne Shell 只能用位置參數 `$1 $2 ...` 模擬。

### 3. 命令列編輯（vi/emacs 模式）
- **理論原因**：交互體驗的一等公民化——命令列是可編輯的緩衝區。
- **實用原因**：可用 vi/emacs 按鍵修改指令再執行。
- **彌補缺陷**：Bourne Shell 互動時只能重打整行；csh 只有歷史取代語法（`!!`）而非真正的行編輯。

### 4. 函數強化與 `print` 內建
- **實用原因**：`print` 比 `echo` 行為更可預測（跨平台一致）。

### 5. coprocess（雙向管線，ksh93，1988）
- **理論原因**：管線只有單向流，行程間無法互動。
- **實用原因**：`|&` 讓腳本可以與長駐行程雙向溝通。
- **彌補缺陷**：管線單向性的限制（後來 bash 4.0 於 2009 年跟進）。

## 歷史意義
ksh 證明了「腳本相容性」與「交互體驗」可以兼得，成為之後所有主流 shell（bash、zsh）的設計藍本。AT&T 後來將 ksh93 開源（2000 年），其程式碼直接影響了 bash 的實作。

## 程式範例：Korn Shell 的語法

```sh
# 1. 算術展開：不需 fork expr
x=10
x=$(( x + 1 ))          # 快一個數量級（vs `expr $x + 1`）
echo $(( 2 ** 10 ))     # 次方運算

# 對比：Bourne Shell 只能這樣（每次 fork 外部程式）
# x=`expr $x + 1`
```

```sh
# 2. 陣列：序列資料
set -A files a.txt b.txt c.txt
echo ${files[0]}        # a.txt
echo ${#files[@]}       # 3（元素個數）
```

```sh
# 3. 命令列編輯：vi/emacs 模式
set -o vi      # 用 vi 按鍵編輯指令
set -o emacs   # 或 emacs 按鍵
```

```sh
# 4. 函數與 print 內建
greet() {
  print "Hello, $1"
}
greet World
```

```sh
# 5. coprocess（ksh93）：雙向管線
ls |&                  # ls 成為 co-process
read -p line           # 從 coprocess 讀取輸出
print -p "*.c"         # 送命令給 coprocess
```

```sh
# 融合示範：腳本相容 sh、交互媲美 csh——兩者兼得
#!/bin/ksh
for f in *.txt; do              # sh 語法的迴圈
  print "處理 $f：$(( $(wc -l < $f) )) 行"   # ksh 算術
done
```

## 彌補了什麼缺陷
彌補了「csh 好交互但腳本爛、sh 好腳本但交互爛」的二元分裂——ksh 是第一個兩者兼優的 shell。

## 相關條目
- [1977-BourneShell-sh問世](1977-BourneShell-sh問世.md)
- [1978-CShell-csh問世](1978-CShell-csh問世.md)
- [1988-Bash誕生](1988-Bash誕生.md)
