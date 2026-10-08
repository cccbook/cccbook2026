# 2014：C++14 泛型 Lambda——三年一版節奏的開始

## 事件
2014 年 12 月，**C++14**（ISO/IEC 14882:2014）發佈。這是第一個遵循「**三年一版**」節奏的標準——以小步快跑取代 C++11 的大爆發。

## 關鍵語法/特性
- **泛型 Lambda**：`[](auto x, auto y) { return x + y; }`——參數可用 `auto`，Lambda 參數型別由呼叫處推導。
- **函式回傳型別推論**：`auto f() { return 42; }`。
- **放寬的 constexpr**：可含區域變數、迴圈、分支——幾乎是完整的編譯期程式語言。
- **變數樣板**：`template<class T> constexpr T pi = T(3.14...);`
- **`std::make_unique`**：補上 C++11 遺漏的一角（`make_shared` 有、`make_unique` 卻沒有）。
- **二進位字面值 `0b1010`、數字分隔符 `1'000'000`、`[[deprecated]]` 屬性**。

## 為何重要
- **泛型 Lambda 讓「以行為為參數」的風格完整**：C++11 的 Lambda 只能寫死參數型別，C++14 之後才能寫出真正泛型的組合式程式碼——與 STL 演算法、ranges（C++20 的前身）無縫銜接。
- **放寬 constexpr**：編譯期計算從「只能寫一行遞迴」進化成「能寫迴圈的完整程式」——`constexpr` 函式庫（如編譯期字串處理）就此萌芽。
- **三年一版節奏**：確立了 C++ 不再讓標準與實務脫節 13 年的承諾。

## 理論與實用原因
- **理論原因**：泛型 Lambda 即「隱式參數化多型」（implicit polymorphism）——語法糖背後是樣板展開；放寬 constexpr 源自「常數求值器即直譯器」的編譯器理論。
- **實用原因**：C++11 來不及完成的細節（make_unique、泛型 Lambda、放寬 constexpr）在三年內補齊，讓「現代 C++」風格可以完全落地。

## 彌補了什麼缺陷
彌補了 C++11「Lambda 參數型別必须寫死、constexpr 太受限、make_unique 缺漏」的缺陷——這是「現代 C++」的第二塊拼圖。

## 程式範例

**泛型 Lambda：參數型別不再寫死**

```cpp
#include <string>
#include <vector>

// C++11 舊寫法：Lambda 參數型別必須寫死，想支援多型別要寫好幾份
auto add_int    = [](int a, int b) { return a + b; };
auto add_double = [](double a, double b) { return a + b; };

// C++14：參數用 auto，一次支援所有可用 + 的型別（背後是樣板展開）
auto add = [](auto a, auto b) { return a + b; };

int    i = add(1, 2);          // int 版本
double d = add(1.5, 2.5);      // double 版本
std::string s = add(std::string("a"), std::string("b")); // 字串串接
```

**函式回傳型別推論**

```cpp
// C++11：回傳型別要用尾置宣告，冗長
auto add11(int a, int b) -> int { return a + b; }

// C++14：回傳型別直接推論
auto add14(int a, int b) { return a + b; } // 推論為 int

template <class T>
auto pick(bool flag, T a, T b) { return flag ? a : b; } // 推論為 T
```

**放寬 constexpr：編譯期可以寫迴圈**

```cpp
// C++11 舊寫法：constexpr 函式只能一行遞迴
constexpr int fact11(int n) {
    return n <= 1 ? 1 : n * fact11(n - 1);
}

// C++14：constexpr 可含區域變數與迴圈，幾乎是完整編譯期語言
constexpr int fact14(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) result *= i;
    return result;
}

constexpr int x = fact14(5); // 編譯期算出 120，可當陣列大小
int arr[x];
```

**`std::make_unique`：補上 C++11 的缺漏**

```cpp
#include <memory>

void f() {
    // C++11 舊寫法：new 與 unique_ptr 分開寫，例外安全性較差
    std::unique_ptr<int> p1(new int(42));

    // C++14：make_unique 終於進標準庫——與 make_shared 對稱
    auto p2 = std::make_unique<int>(42);
}
```

## 相關條目
- [2011-C++11自動型別與Lambda](2011-C++11自動型別與Lambda.md)
- [2017-C++17結構化綁定](2017-C++17結構化綁定.md)
