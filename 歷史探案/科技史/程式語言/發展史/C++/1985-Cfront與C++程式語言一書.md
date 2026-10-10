# 1985：Cfront 與《C++ 程式語言》——語言第一次公開

## 事件
1985 年，兩件大事同時發生：
1. Stroustrup 出版《**The C++ Programming Language**》第一版，C++ 正式面向世界。
2. 第一個 C++ 編譯器 **Cfront 1.0** 問世——它把 C++ **轉譯成 C**，再交給 C 編譯器編譯。

## 為何重要
- 「**轉譯到 C**」的策略讓 C++ 立刻在所有有 C 編譯器的機器上可用——借用既有生態，快速普及（後來 Objective-C、早期 TypeScript 也採用同樣策略）。
- 《The C++ Programming Language》成為語言的事實規範，直到 1998 年 ISO 標準化為止。
- 本書確立了 C++ 的設計原則：**零成本抽象、不為效率妥協的表達力、直接支援多種範式**。

## 理論與實用原因
- **理論原因**：資料抽象（data abstraction）與物件導向的融合，Stroustrup 的論文《What is "Object-Oriented Programming"?》（1988）進一步闡述。
- **實用原因**：貝爾實驗室內部已有大量使用者在等一個可發佈的版本。

## 彌補了什麼缺陷
彌補了「C with Classes 只是內部實驗、無文件無編譯器散佈」的缺陷——語言要活，必須有規範與工具。

## 程式範例

1985 年 C++ 1.0 的典型寫法——類別封裝 + `iostream` 輸出：

```cpp
#include <iostream>

class Greeter {
    char name[20];
public:
    Greeter(const char* n) {           // 建構子：C 語言沒有的物件初始化機制
        int i = 0;
        while (n[i] != '\0') { name[i] = n[i]; i++; }
        name[i] = '\0';
    }
    void greet() {
        // iostream 的 << 運算子重載：型別安全，不像 printf 的 %s/%d 易出錯
        std::cout << "Hello, " << name << "!\n";
    }
};

int main() {
    Greeter g("world");
    g.greet();                          // 輸出：Hello, world!
    return 0;
}
```

同一份程式碼可透過 **Cfront 轉譯成 C**，再交給各平台的 C 編譯器編譯：

```text
hello.cc --Cfront--> hello.c --cc--> 各平台（Unix、VMS、MS-DOS...）皆可執行
```

這正是「借用既有 C 生態、快速跨平台普及」的策略——C++ 程式碼不需要每個平台重新實作編譯器，只要該機器有 C 編譯器就能跑。

## 相關條目
- [1983-C++命名與virtual函式](1983-C++命名與virtual函式.md)
- [1989-Cfront-2-0多重繼承與抽象類別](1989-Cfront-2-0多重繼承與抽象類別.md)
