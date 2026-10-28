# 1995：Perl/Python 衝擊——Shell 退守本業

## 事件
1990 年代中期，**Perl**（1987，1995 年進入 Perl 5 时代）與 **Python**（1991，1995 年 Python 1.3）快速崛起，奪走了 shell script 的大量應用場景。shell script 從「系統管理的萬能語言」退守到「啟動、設定、管線組合」的本業。

## 理論與實用原因

### 1. Perl/Python 搶走複雜腳本
- **理論原因**：shell 語言的資料結構只有字串與（晚期的）陣列——沒有雜湊、物件、正則內建（POSIX 層面）、除錯器、模組系統。
- **實用原因**：複雜邏輯（解析日誌、資料轉換、網路程式）用 Perl/Python 生產力高出一個量級。
- **彌補缺陷（反向）**：shell 的「膠水」定位反而成為它的極限——變數都是字串、無型別、算術要 `$(( ))`、錯誤處理只有 `$?`。

### 2. shell 保留的不可取代性
- **理論原因**：shell 是**行程與管線的 orchestration 語言**——啟動、組合、重導向行程是它的母語，Perl/Python 都要靠 subprocess 程式庫勉強模擬。
- **實用原因**：系統啟動腳本（`/etc/init.d`）、CI 腳本、`Makefile` 中的命令、Dockerfile 的 `RUN` 指令——這些「組合命令」的場景 shell 永遠最自然。

### 3. 當時 shell 生態的因應
- **ksh93（1993 前後）**：加入關聯陣列、浮點算術、函數指標（`nameref`）——試圖把 shell 變成通用語言，但太複雜而未普及。
- **bash 2.0（1996）**：重寫解析器，加入陣列與國際化——走的是「把本業做好」的路線。
- **scsh（Scheme Shell，1994）**：以 Scheme 的語意做 shell——學術實驗，影響深遠但使用者稀少。

## 程式範例：同一件事——shell vs Perl vs Python

「讀取檔案、統計 ERROR 行數、寫成報告」：

```sh
#!/bin/sh
# shell 版：適合「行程組合」，但邏輯擴充受限
grep ERROR app.log > report.txt || exit 1
echo "錯誤數: $(grep -c ERROR app.log)" >> report.txt
```

```perl
#!/usr/bin/perl
# Perl 版：正則內建、雜湊、模組——複雜邏輯的生產力差距
my %count;
while (<>) {
    $count{$1}++ if /ERROR (\w+)/;   # 正則 + 雜湊內建
}
print "$_: $count{$_}\n" for sort keys %count;
```

```python
#!/usr/bin/env python3
# Python 版：可讀性、資料結構、錯誤處理
from collections import Counter
counts = Counter()
try:
    with open("app.log") as f:
        for line in f:
            if "ERROR" in line:
                counts[line.split()[1]] += 1
except FileNotFoundError:
    exit(1)
for name, n in counts.most_common():
    print(f"{name}: {n}")
```

```sh
# shell 不可取代的場景：行程組合是它的母語
# Perl/Python 要靠 subprocess 程式庫勉強模擬
make && ./test.sh && ./deploy.sh --env prod | tee deploy.log
```

```sh
# shell 的極限示範：字串型別、無浮點、無雜湊（1995 年當時）
x="hello"; echo ${#x}          # 字串長度——shell 的變數都是字串
# echo $(( x * 1.5 ))          # 錯！bash 2.0 之前無法這樣，POSIX sh 更無浮點
```

## 歷史意義
這場衝擊確立了至今的分工：**複雜邏輯用 Perl/Python/Ruby，行程組合用 shell**。也讓「shell 不是通用語言」成為共識，之後的新 shell（fish、nushell）都專注在互動體驗與結構化資料，而非搶通用腳本的位子。

## 彌補了什麼缺陷
這一年不是「加了新語法」，而是暴露了 shell 語言的根本極限：字串中心的型別系統、貧乏的資料結構與錯誤處理。這些缺陷定義了後續所有 shell 的演進方向。

## 相關條目
- [1977-BourneShell-sh問世](1977-BourneShell-sh問世.md)
- [2000-Bash2-0重寫](2000-Bash2-0重寫.md)
- [2005-Fish問世](2005-Fish問世.md)
