# 2019：macOS 改用 Zsh

## 事件
2019 年 10 月，蘋果發佈 **macOS Catalina**（10.15），正式將預設 shell 從 **bash 改為 zsh**。這是 zsh 誕生（1990）近三十年後首次登上大眾作業系統的預設寶座。

## 理論與實用原因

### 1. GPLv3 授權因素
- **理論原因**：自由軟體授權的相容性——bash 自 4.0 起採用 GPLv3，蘋果對 GPLv3 的反專利條款（Tivoization）有顧慮，長期停留在 GPLv2 的 bash 3.2（2007）。
- **實用原因**：zsh 採用 MIT-like 寬鬆授權，蘋果可以自由修改與散布而不受 GPLv3 約束。
- **彌補缺陷**：蘋果的 bash 停在 2007 年版本，十餘年沒有新語法（無關聯陣列、無 globstar）；改用 zsh 一次獲得所有現代語法。

### 2. zsh 的現代功能
- **實用原因**：可編程補全、`**` 遞迴 glob、進階字串操作——這些 bash 3.2 都沒有。
- **彌補缺陷**：蘋果預設 shell 語法能力落後現代標準十餘年。

### 3. Oh My Zsh 生態的推波助瀾
- **實用原因**：2010 年 Oh My Zsh 問世後，zsh 已是開發者社群的主流選擇，蘋果順應生態。
- **彌補缺陷**：macOS 預設 shell 與開發者習慣脫節。

### 4. 向下相容的安排
- **實用原因**：bash 3.2 仍保留在系統中（`/bin/bash`），既有腳本不受影響；`#!/bin/sh` 仍指向 bash 的 POSIX 模式。
- **彌補缺陷**：改變預設 shell 對腳本生態的衝擊被降到最低。

## 程式範例：bash 3.2（蘋果舊預設）vs zsh 的新語法

```bash
# 蘋果的 bash 3.2 沒有關聯陣列（declare -A 是 bash 4.0 才有）
# 也沒有遞迴 glob **，只能用 find：
find . -name '*.c'
```

```zsh
# zsh（2019 起的 macOS 預設）：遞迴 glob 一行搞定
ls **/*.c

# zsh 的關聯陣列
typeset -A ver
ver[bash]=3.2
ver[zsh]=5.9
echo $ver[bash]

# zsh 的參數展開修飾符
f=archive.tar.gz
echo ${f:r}     # archive.tar（去副檔名）
echo ${f:e}     # gz（取副檔名）

# zsh 的修改用整段腳本取代傳統 alias
autoload -Uz vcs_info
```

```bash
# 腳本相容性：既有腳本不受影響
#!/bin/bash   # 仍是 bash 3.2，照常執行
#!/bin/sh     # 仍指向 bash 的 POSIX 模式
```

## 歷史意義
這是 shell 語言史上的重要轉折：**授權（GPLv3）第一次直接改變了大眾作業系統的預設 shell**。此後 zsh（macOS、開發者社群）與 bash（Linux 伺服器）分庭抗禮。

## 相關條目
- [1990-Zsh誕生](1990-Zsh誕生.md)
- [2010-OhMyZsh問世](2010-OhMyZsh問世.md)
- [2009-Bash4-0關聯陣列](2009-Bash4-0關聯陣列.md)
