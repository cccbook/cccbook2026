# 2007：Clang 與 LLVM 問世——編譯器基礎設施革命

## 事件
2000 年 Chris Lattner 在伊利諾大學展開 **LLVM** 計畫；2007 年 Apple 發佈 **Clang**——以 LLVM 為後端的 C/C++/Objective-C 編譯器。2010 年代，Clang 逐步成為與 GCC 分庭抗禮的主流 C++ 編譯器。

## 為何重要
- **LLVM 的「編譯器即函式庫」思想**：把編譯器拆成前端（Clang）、中間表示（LLVM IR）、後端（目標碼生成）三大模組——任何語言（Rust、Swift、Zig、Julia）都可以借用 LLVM 的最佳化與後端。
- **Clang 的診斷訊息**：錯誤訊息精確指出位置與修復建議，遠勝當時的 GCC——逼得 GCC 也不得不改進。
- **Clang 逐步成為 C++ 標準演進的實驗場**：C++11/14/17/20 的新特性常由 Clang 與 libc++ 率先完整實作。
- **libc++**（LLVM 的 C++ 標準庫，2011）與 **libstdc++**（GCC）形成標準庫雙雄。

## 理論與實用原因
- **理論原因**：LLVM IR 是一種 SSA（靜態單賦值）形式的中間表示——最佳化理論（資料流分析）在此最能發揮；模組化編譯器架構源自 Lattner 的論文《LLVM: An Infrastructure for Multi-Stage Optimization》（2002）。
- **實用原因**：Apple 的 Xcode 需要 IDE 級的語言服務（自動補全、重構），GCC 的單體式架構做不到——Clang 從一開始就設計成函式庫。

## 彌補了什麼缺陷
彌補了 GCC「單體式架構、難以作為函式庫使用、診斷訊息不友善」的缺陷——編譯器基礎設施從此從「單一工具」進化為「可組合的平台」。

## 程式範例

用 Clang 編譯 C++ 程式：

```sh
# 以 Clang 編譯（-Wall 開啟警告）
clang++ -std=c++11 -Wall hello.cpp -o hello

# 執行
./hello

# 查詢版本
clang --version
```

Clang 以友善的診斷訊息著稱。假設 `hello.cpp` 寫錯了一行：

```cpp
#include <iostream>

int main() {
    int x = 10
    std::cout << x << std::endl;  // 上一行少了分號
    return 0;
}
```

Clang 的錯誤訊息會精確指出位置並提出修復建議：

```
hello.cpp:4:15: error: expected ';' after expression
    int x = 10
              ^
              ;
1 error generated.
```

同樣的程式在當時的 GCC 上，錯誤訊息往往簡陋許多，只回報語法錯誤、未必提示該補上分號。Clang 逼得 GCC 後來也不得不改進診斷品質。

Clang 前端 → LLVM IR → 後端的模組化架構示意——同一份 LLVM IR 可以交給不同後端生成 x86、ARM 等目標碼：

```llvm
; clang -S -emit-llvm add.cpp 產生的 LLVM IR（節錄示意）
define i32 @add(i32 %a, i32 %b) {
entry:
  ; %add = a + b
  %add = add nsw i32 %b, %a
  ret i32 %add
}
```

```sh
# 產生 LLVM IR
clang++ -S -emit-llvm add.cpp -o add.ll
# 再由 LLVM 後端編譯成目的檔
llc add.ll -o add.s
```

## 相關條目
- [1991-gcc與g++開源編譯器](1991-gcc與g++開源編譯器.md)
- [2011-C++11自動型別與Lambda](2011-C++11自動型別與Lambda.md)
