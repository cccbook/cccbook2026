# 1991：Linux 誕生——C 與自由工具鏈的勝利

## 事件
1991 年，芬蘭赫爾辛基大學學生 Linus Torvalds 以 C 語言（夾雜少量組合語言）撰寫出 Linux 核心 0.01 版並放上網路徵求協作者。Linux + GNU 工具鏈（gcc、glibc、bash、make）組合成完整的自由作業系統，成為史上最大規模的 C 語言協作專案。

## 為何重要
- **C 的最大舞台**：Linux 核心至今約三千萬行 C 程式碼，是 C 語言工程實踐、程式碼風格（kernel coding style）、審查文化的最大實驗場。
- **證明 GCC 與 C89/C90 的成熟**：一個大學生用免費工具鏈就能寫出可用的作業系統，徹底證明自由 C 工具鏈的可用性。
- **開源模式的誕生**：GPL + 網路協作 + C 語言的「小而清晰」特性，讓全球志工得以共同維護一份龐大程式碼——這個模式後來被所有開源專案複製。

## 理論與實用原因
- **理論原因**：Linus 沿用 UNIX「一切皆檔案、極簡核心」的設計理論，並以「早發佈、常發佈」的實用主義取代學院派的瀑布開發。
- **實用原因**：386 PC 普及、GCC 免費、Minix 教學系統提供了參考，唯獨缺一個「真實可用且自由」的核心——Linux 正是補上這一塊。

## 彌補了什麼缺陷
彌補了「自由軟體陣營缺一個可用核心」的缺陷（GNU 計畫的 Hurd 遲遲未成），也彌補了商業 UNIX 分裂、昂貴、硬體綁定的缺陷。Linux 讓 C 語言在伺服器、手機（Android）、超級電腦上統治至今。

## 程式範例
Linux 0.01 的早期核心程式碼（C 語言 + kernel coding style 的原點）：

```c
/* linux/kernel/sched.c 概念示意——「小而清晰」的 C 風格 */
struct task_struct {
    long state;             /* -1 unrunnable, 0 runnable, >0 stopped */
    long counter;
    long priority;
    struct task_struct *next;   /* 指標串成雙向鏈結串列 */
};

void schedule(void)
{
    struct task_struct **p;
    while (1) {
        int c = -1;
        for (p = &LAST_TASK; p > &FIRST_TASK; --p)   /* 指標反向走訪任務表 */
            if (*p && (*p)->state == 0 && (*p)->counter > c)
                c = (*p)->counter;
        if (c) break;
        /* 無可執行任務，等待中斷 */
    }
}
```

使用者空間——用 GNU 工具鏈寫的第一個 Linux 程式（1991 年的樣貌）：

```c
/* hello.c —— gcc 在 1991 年就能編譯這樣的程式 */
#include <stdio.h>

int main(void)
{
    printf("Hello world!\n");
    return 0;
}
```

```sh
$ gcc -o hello hello.c
$ ./hello
Hello world!
```

GNU 生態的小工具組合（C 寫的 coreutils）：

```sh
$ ps aux | grep gcc | wc -l    # ps/grep/wc 皆為 C 程式，管道組合
```

## 相關條目
- [1969-UNIX誕生](1969-UNIX誕生.md)
- [1983-GCC與GNU計畫誕生](1983-GCC與GNU計畫誕生.md)
- [2011-C11執行緒與泛型](2011-C11執行緒與泛型.md)
