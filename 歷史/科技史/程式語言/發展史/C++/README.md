# C++ 程式語言發展史年表

> C++ 是 1979 年由 Bjarne Stroustrup 在貝爾實驗室以 C 為基礎開發的語言，
> 目標是「在不犧牲 C 效率的前提下，加入資料抽象與物件導向」。
> 它貫穿一條設計主軸——**零成本抽象（zero-overhead abstraction）**：
> 你不用你沒用到的功能，用到的功能與手寫程式碼一樣快。
> 從類別、virtual、樣板、例外，到 C++11 的移動語義與 Lambda，
> 再到 C++20 的 concepts、coroutines 與 modules，C++ 是史上生命力最長的主流語言之一。

## 前史：理論根源

| 年份 | 事件 | 意義 |
|------|------|------|
| 1969 | [UNIX 問世](1969-UNIX問世.md) | C++ 誕生的土壤：可攜系統程式設計的先驅 |
| 1972 | [C 語言問世](1972-C語言問世.md) | C++ 的直接前身：貼近硬體的系統語言 |
| 1967 | Simula 67 | 類別與虛擬程序的理論源頭（Stroustrup 親身使用過） |
| 1975 | Goodenough 例外理論 | 例外處理的理論基礎 |
| 1978 | K&R《C 程式語言》 | C 語法的事實規範 |

## 正式年表

| 年份 | 標題 | 關鍵語法/特性 |
|------|------|---------------|
| 1979 | [C with Classes 誕生](1979-CWithClasses誕生.md) | class、建構子/解構子、friend——資料抽象的開始 |
| 1983 | [C++ 命名與 virtual 函式](1983-C++命名與virtual函式.md) | virtual（執行時期多型）、函式多載、預設參數 |
| 1985 | [Cfront 與《C++ 程式語言》](1985-Cfront與C++程式語言一書.md) | 轉譯到 C 的策略、《The C++ Programming Language》出版 |
| 1989 | [Cfront 2.0 多重繼承與抽象類別](1989-Cfront-2-0多重繼承與抽象類別.md) | 多重繼承、純虛擬函式、const 成員函式、static 成員 |
| 1991 | [gcc 與 g++ 開源編譯器](1991-gcc與g++開源編譯器.md) | 自由軟體工具鏈：g++、libstdc++、gdb |
| 1993 | [樣板與例外處理問世](1993-樣板與例外處理問世.md) | templates（編譯期多型）、try/catch/throw、namespace、RTTI |
| 1994 | [STL 標準模板庫問世](1994-STL標準模板庫問世.md) | 容器/迭代器/演算法——史上第一個大規模泛型函式庫 |
| 1998 | [C++98 標準化](1998-C++98標準化.md) | ISO/IEC 14882、`namespace std`、語言成年 |
| 2003 | [C++03 修正版](2003-C++03修正版.md) | 缺陷修正報告、值初始化明確化——13 年等待的教訓 |
| 2007 | [Clang 與 LLVM 問世](2007-Clang與LLVM問世.md) | 編譯器即函式庫、LLVM IR、libc++——診斷訊息革命 |
| 2011 | [C++11 自動型別與 Lambda](2011-C++11自動型別與Lambda.md) | auto、移動語義（`T&&`）、Lambda、nullptr、constexpr、執行緒庫——現代 C++ 誕生 |
| 2014 | [C++14 泛型 Lambda](2014-C++14泛型Lambda.md) | 泛型 Lambda、回傳型別推論、放寬 constexpr、make_unique——三年一版節奏開始 |
| 2017 | [C++17 結構化綁定](2017-C++17結構化綁定.md) | 結構化綁定、if constexpr、optional/variant/any、string_view、filesystem |
| 2022 | [Linux 核心與 Clang 互通](2022-Linux核心與Clang互通.md) | 核心可用 Clang 建置、Rust 進核心、C++/Rust 互通議題 |
| 2020 | [C++20 概念與協程](2020-C++20概念與協程.md) | concepts、ranges、coroutines、modules、`<=>`、std::format——四大支柱 |
| 2023 | [C++23 與模組時代](2023-C++23與模組時代.md) | std::expected、std::print、if consteval、Ranges 擴充 |
| 2025 | [C++26 反射與未來](2025-C++26反射與未來.md) | 靜態反射、契約（profiles）、std::execution——編譯期後設程式設計終點站 |

## 工具鏈發展主軸

1. **1985 Cfront → 1991 g++ → 2007 Clang/LLVM** —— 編譯器從「轉譯到 C」到「單體式 GCC」，再到「編譯器即函式庫」的 LLVM 時代；Clang 的診斷訊息革命逼得 GCC 也不得不改進。
2. **1998 libstdc++ / 2011 libc++** —— 標準庫雙雄，STL 的兩大實作。
3. **1999 Boost** —— C++11/14/17 的育成中心：regex、thread、smart_ptr、optional、variant 都是先在 Boost 驗證再收編進標準。
4. **2010 年代 sanitizers** —— Clang 的 ASan/UBSan 讓 C++ 的記憶體安全缺陷可以被動態偵測；2022 年後與 Rust 的競爭共同推動 profiles/contracts 等安全提案。

## 發展主軸

1. **1979–1985：資料抽象** —— 類別、建構子/解構子、virtual：解決「C 無封裝、Simula 效能差」的兩難。
2. **1989–1998：泛型與標準化** —— 樣板、例外、命名空間、STL、ISO 標準：C++ 成為跨平台系統語言。
3. **1998–2011：漫長等待與現代化** —— 13 年不動標準的教訓之後，C++11 一次補齊移動語義、Lambda、auto、執行緒。
4. **2011–至今：三年一版與安全轉型** —— C++14/17/20/23/26 小步快跑；concepts、modules、coroutines 補齊表達力，面對 Rust 競爭，以 profiles、contracts、`std::expected` 回應記憶體安全議題。
