# 2005：LLVM 與 Clang 問世——編譯器的第二勢力

## 事件
2000 年起，伊利諾大學的 Chris Lattner 開發 LLVM（Low Level Virtual Machine），2005 年 Apple 延攬 Lattner 全職投入，2007 年 Clang C 編譯器首次公開。2010 年代 Clang 逐步取代 GCC 成為 BSD、macOS 的預設編譯器。

## 為何重要
- **打破 GCC 壟斷**：GCC 服役二十年後架構老化（單體式、RTL 中間表示難以擴充、GPLv3 授權爭議），LLVM 以模組化 IR（LLVM IR）重新設計。
- **Clang 的優勢**：錯誤訊息人性化（精確指出錯誤位置與修復建議）、編譯速度快、架構是函式庫（可嵌入 IDE、分析工具、JIT）。
- **催生生態系**：LLVM 之上長出 rustc、Swift、Zig 等新語言編譯器；clang-tidy、clangd（IDE 後端）、AddressSanitizer、UBSan 等工具重新定義了 C/C++ 的品質保證。

## 理論與實用原因
- **理論原因**：LLVM IR 是 SSA（靜態單賦值）形式的中間表示，理論上更利於最佳化——比 GCC 的 RTL 更容易做資料流分析。
- **實用原因**：Apple 的 Xcode 需要 IDE 級的即時語意分析，GCC 的單體式架構做不到「編譯器即函式庫」；Clang 把詞法、語法、語意分析全部拆成函式庫，任何工具都能重複使用。

## 彌補了什麼缺陷
彌補了 GCC「架構單體、錯誤訊息難讀、編譯慢、難以嵌入工具、授權僵化（GPLv3）」的缺陷。ASan/UBSan 更彌補了 C 語言「記憶體錯誤無工具可查、只能靠人眼 review」的長期缺陷。

## 程式範例
**GCC 與 Clang 的錯誤訊息對比**——Clang 人性化錯誤訊息的殺手級特色：

```c
/* bug.c —— 一個常見的打字錯誤 */
#include <stdio.h>

int main(void) {
    int x = 1
    printf("%d\n", x);   /* 上一行少了分號 */
    return 0;
}
```

```text
$ gcc bug.c
bug.c: In function 'main':
bug.c:5: error: expected ';' before 'printf'      ← 只說第 5 行，要自己猜

$ clang bug.c
bug.c:4:10: error: expected ';' after expression
    int x = 1
            ^
            ;                                      ← 精確指出位置，還畫出修復建議
bug.c:5:12: warning: implicit conversion ... 
```

**AddressSanitizer**——記憶體錯誤從「靠人眼 review」變成「工具自動抓」：

```c
/* heap_overflow.c —— C 最經典的錯誤：寫出陣列邊界 */
#include <stdlib.h>

int main(void) {
    int *a = malloc(4 * sizeof(int));   /* 4 格陣列 */
    a[4] = 42;                          /* 越界寫入——C90/C99 完全抓不到 */
    free(a);
    return 0;
}
```

```text
$ gcc -fsanitize=address heap_overflow.c && ./a.out
==12345==ERROR: AddressSanitizer: heap-buffer-overflow on address ...
WRITE of size 4 at 0x602000000014 thread T0
    #0 0x108... in main heap_overflow.c:6          ← 精確指出第 6 行越界！
```

**LLVM IR**——SSA 形式的中間表示（最佳化理論的基石）：

```c
/* 每個變數只被賦值一次（Static Single Assignment），資料流分析更容易 */
define i32 @f(i32 %a) {
entry:
  %b = add i32 %a, 1        ; b = a + 1（SSA：只賦值一次）
  %c = mul i32 %b, 2        ; c = b * 2
  ret i32 %c
}
```

## 相關條目
- [1983-GCC與GNU計畫誕生](1983-GCC與GNU計畫誕生.md)
- [2011-C11執行緒與泛型](2011-C11執行緒與泛型.md)
