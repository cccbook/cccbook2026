# 1973 - Unix 以 C 重寫與管道（可移植性與組合性雙勝利）

## 案件摘要
1973 年，**Dennis Ritchie 用 C 語言重寫 Unix**（Version 4）——作業系統史上第一次，核心脫離組合語言，變成**可移植**的系統。
同年 **Thompson 發明管道（pipe）**——把一個程式的輸出接到另一個的輸入，開啟 Unix 最深遠的發明：**組合性**。
$$\text{可移植性（C 重寫）} \;+\; \text{組合性（管道）} \;=\; \text{Unix 征服世界的兩大武器}.$$

## 前因 -- 為什麼會有這個案子
- **PDP-11 換代與可移植的渴望**：每次換機器就要重寫數萬行組語——**彌補的缺陷：不可移植**。B 語言（Thompson 1969）太快、太無型別、無法表達硬體細節，Ritchie 因此設計 **NB→C**：有型別、可編譯出高效率程式碼。
- **管道的動機**：McIlroy 觀察到大家一直在寫「把 A 的輸出接給 B」的臨時程式——與其在每個程式裡重複寫，不如讓 shell **一次統一支援**。
- **理論基礎**：管道本質是**串流（stream）與協程（coroutine）**——生產者與消費者並行、以有限緩衝解耦。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：C 重寫——「高階語言寫 OS」的證明
$$\text{C 程式碼} \;\xrightarrow{\text{PDP-11 編譯器}}\; \text{機器碼} \;\approx\; \text{手寫組語的效率}.$$
- **彌補的缺陷**：組語不可移植、不可讀、維護成本高。
- **理論意義**：證明 OS 核心可以「機器無關」——只需要為每台新機器重寫一小部分（編譯器 + 少數機器相關檔案）。
- 從此 Unix 從 PDP-11 移到 Interdata 8/32、VAX……**一次寫作，處處編譯**。

### 第二條線索：管道——組合的代數
$$\text{工具}_1 \;|\; \text{工具}_2 \;|\; \text{工具}_3 \quad\Longrightarrow\quad \text{組合爆炸的生產力}.$$
- 實作：`pipe(fd)` 產生一對檔案描述子，配合 `fork`，父行程寫入端、子行程讀出端——**一切皆檔案**的完美應用。
- 哲學（McIlroy 總結）：
  > 寫只做一件事但做好的程式；寫能協作的程式；寫能處理文字流的程式，因為那是通用介面。

### 第三條線索：stdlib 的雛形
C 重寫同時確立 `stdio`（`printf/fopen`）——把 I/O 抽象成字元流，與管道思想同源：**文字流是通用介面**。

### C 範例：管道的系統呼叫本質

```c
#include <unistd.h>
#include <stdio.h>

int main(void) {
    int fd[2];
    pipe(fd);                 /* fd[1] 寫入端, fd[0] 讀出端 */
    if (fork() == 0) {        /* 子行程：充當「下游工具」 */
        dup2(fd[0], 0);       /* 把讀出端接到 stdin */
        close(fd[1]);
        execlp("wc", "wc", "-l", NULL);   /* 統計行數 */
    }
    dup2(fd[1], 1);           /* 父行程：把寫入端接到 stdout */
    close(fd[0]);
    execlp("ls", "ls", NULL); /* 相當於 shell: ls | wc -l */
    return 0;
}
```

### Shell 範例：組合性的鐵證

```bash
# 相當於 shell: cat /etc/passwd | cut -d: -f1 | sort | head -5
$ cat /etc/passwd | cut -d: -f1 | sort | head -5
```
（四個只做一件事的工具，用管道組合成複雜任務——**不需要寫任何新程式**。）

### Python 範例：重現 Unix 管道

```python
import subprocess

p1 = subprocess.Popen(["cat", "/etc/passwd"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["cut", "-d:", "-f1"], stdin=p1.stdout, stdout=subprocess.PIPE)
p3 = subprocess.Popen(["sort"], stdin=p2.stdout, stdout=subprocess.PIPE)
out = subprocess.check_output(["head", "-5"], stdin=p3.stdout).decode()
print(out)
```

## 結案 -- 後果與影響
- **可移植性** → Unix 佔領所有機型；C 成為此後 50 年系統軟體通用語言（Linux、Windows 核心、Git 全是 C）。
- **管道** → shell 腳本、資料管道、今天的 DevOps 與 `|`、`|&`、`xargs` 全是後裔。
- 1974 年 CACM 論文發表（見 `1974-CACM論文與授權擴散.md`）。
- 歷史教訓：**不是功能多者勝，而是介面統一、可組合者勝**。

## 關鍵人物與文獻
- **D. M. Ritchie**：C 語言設計者；〈The Development of the C Language〉(1993)。
- **D. McIlroy**：管道構想 (1964 早已提出，1973 落實)；〈A Research UNIX Reader〉。
- 相關案件：`1969-Unix誕生.md`、`1974-CACM論文與授權擴散.md`。
