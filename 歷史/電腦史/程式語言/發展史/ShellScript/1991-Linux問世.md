# 1991：Linux 問世與 GNU 工具鏈

## 事件
1991 年，芬蘭赫爾辛基大學學生 **Linus Torvalds** 發佈 **Linux 核心**，並搭配 GNU 專案的工具鏈（gcc、bash、coreutils）組成完整的自由作業系統。**bash 成為 Linux 的預設 shell**，這是 shell 語言史上裝機量的最大轉折點。

## 理論與實用原因

### 1. bash 成為 Linux 預設 shell
- **理論原因**：GPLv2 授權的一致性——Linux 用 GPLv2，bash 用 GPLv3（當時 GPLv2），授權相容。
- **實用原因**：bash 在 POSIX 標準化過程中已是成熟實作，且自由、高品質、跨硬體。
- **彌補缺陷**：商業 UNIX 的 shell 是專有軟體，自由系統不能使用。

### 2. `/bin/sh` 符號連結的彈性
- **實用原因**：Linux 發行版可將 `/bin/sh` 連到 bash、dash 或其他 shell，腳本以 POSIX 語法撰寫即可移植。
- **彌補缺陷**：商業 UNIX 的 `/bin/sh` 綁死特定 shell。

### 3. GNU coreutils 與 shell 的共生
- **理論原因**：「小事處理」哲學的完整重實現——`ls`、`grep`、`sed`、`awk` 全部自由開源。
- **實用原因**：shell script 的價值在於組合工具，GNU 工具鏈讓組合免費。

## 程式範例：Linux 上的 POSIX 可移植腳本

```sh
#!/bin/sh
# POSIX 語法：任何發行版的 /bin/sh 都能跑（bash、dash、busybox ash）
for f in "$@"; do
  [ -f "$f" ] && echo "$f 存在"
done
```

```bash
# bash 擴充：只有 /bin/bash 能跑（含空格檔名安全處理）
#!/bin/bash
files=("$@")                 # bash 陣列
for f in "${files[@]}"; do
  echo "處理: $f"
done
```

```sh
# GNU coreutils + shell 的共生：組合工具免費
grep -r ERROR /var/log | sort | uniq -c | sort -rn | head 5
```

```sh
# 符號連結的彈性：同一腳本，不同 /bin/sh
ls -l /bin/sh
# Ubuntu: /bin/sh -> dash（最小 POSIX，啟動快）
# 其他:   /bin/sh -> bash（POSIX + bash 擴充）
```

## 歷史意義
Linux + bash 的組合讓 Bourne 語法的 shell script 從「商業 UNIX 的專業技能」變成「全球伺服器與開發者的通用技能」。之後 Android（mksh）、嵌入式系統（busybox ash）的 shell 生態也都以 POSIX 語法為中心。

## 彌補了什麼缺陷
彌補了「自由作業系統生態殘缺」的缺陷，也讓 shell script 的可移植性問題（POSIX 標準化的動機）成為全球性議題。

## 相關條目
- [1988-Bash誕生](1988-Bash誕生.md)
- [1992-POSIXShell標準化](1992-POSIXShell標準化.md)
