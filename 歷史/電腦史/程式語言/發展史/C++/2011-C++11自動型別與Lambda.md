# 2011：C++11 自動型別、Lambda 與移動語義——現代 C++ 誕生

## 事件
2011 年 9 月，**C++11**（ISO/IEC 14882:2011）正式發佈。這是 C++98 之後 13 年來最大的一次更新，被稱為「**現代 C++**」的起點——彷彿是一門新語言。

## 關鍵語法/特性
- **`auto`**：型別推論，由編譯器從初始值推導變數型別——省去冗長的迭代器型別宣告。
- **右值引用與移動語義**：`T&&`、`std::move`——資源可以「搬移」而非複製，`vector` 的搬移只付指標交換的成本。
- **Lambda 運算式**：`[](int x){ return x*2; }`——匿名函式，可捕捉區域變數。
- **範圍 for**：`for (auto& x : v)`。
- **`nullptr`**：型別安全的空指標，取代易出錯的 `NULL`（整數 0）。
- **`constexpr`**：編譯期求值的函式與變數。
- **可變參數樣板（variadic templates）**：`template<class... Args>`——`emplace_back`、`make_unique` 的基礎。
- **智慧指標**：`unique_ptr`、`shared_ptr`（移入標準庫）——RAII 管理記憶體。
- **執行緒庫**：`std::thread`、`mutex`、`atomic`、`future`——C++ 第一次有標準執行緒支援。
- **`decltype`、`static_assert`、委派建構子、override/final、enum class、統一初始化 `{}`、`std::initializer_list`**。

## 為何重要
- **移動語義是革命**：解決了「臨時物件被無謂深拷貝」的效能問題——C++ 效能從此不輸手寫的指標操作。
- **Lambda 讓 STL 演算法真正可用**：以前要定義 functor 類別才能傳行為，現在行內即可——`std::sort(v.begin(), v.end(), [](a,b){...})`。
- **`auto` 讓泛型程式碼可讀**：`map<string, vector<int>>::const_iterator` 一去不返。
- **執行緒庫讓多核心時代有標準答案**：C++98 時代並行只能靠平台 API（pthreads/Win32）。

## 理論與實用原因
- **理論原因**：移動語義源自「資源所有權轉移」的形式化（左值/右值二分，源自 C 的 value categories 理論）；`auto` 源自 Hindley–Milner 型別推論；`constexpr` 是純函式求值理論的落地。
- **實用原因**：13 年的硬體革命（多核心、行動裝置）累積了太多缺口；Boost 社群（regex、thread、smart_ptr、function）已驗證了大部分設計——「Boost 是 C++11 的育成中心」。

## 彌補了什麼缺陷
彌補了 C++98「型別宣告冗長、無匿名函式、臨時物件效能浪費、`NULL` 型別不安全、無標準執行緒、無編譯期求值」等一整個時代的缺陷——這是一次總清算。

## 程式範例

**`auto`：告別冗長的迭代器型別**

```cpp
#include <map>
#include <string>
#include <vector>

std::map<std::string, std::vector<int>> m;

void iter_old() {
    // C++98 舊寫法：型別宣告冗長又易寫錯
    std::map<std::string, std::vector<int>>::const_iterator it = m.begin();
}

void iter_new() {
    // C++11：auto 由編譯器推論型別——同一個型別，一行搞定
    auto it = m.begin(); // 型別為 std::map<string, vector<int>>::const_iterator
}
```

**移動語義：搬移取代深拷貝**

```cpp
#include <string>
#include <utility>
#include <vector>

std::vector<std::string> make_big_vector(); // 產生大資料

void old_way() {
    // C++98：臨時物件被無謂深拷貝——整個 vector 的字串逐一複製
    std::vector<std::string> v = make_big_vector();
}

void new_way() {
    // C++11：std::move 觸發搬移——只交換內部指標，常數時間
    std::vector<std::string> a = make_big_vector();
    std::vector<std::string> b = std::move(a); // a 之後不可再用
}
```

**Lambda + STL：行內定義比較器**

```cpp
#include <algorithm>
#include <vector>

struct GreaterThan { // C++98 舊寫法：必須先定義 functor 結構
    bool operator()(int a, int b) const { return a > b; }
};

int main() {
    std::vector<int> v{3, 1, 4, 1, 5};
    std::sort(v.begin(), v.end(), GreaterThan()); // 舊：要另寫類別

    // C++11：Lambda 行內即可，還能用範圍 for 走訪
    std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });
    for (int x : v) { /* ... */ }
}
```

**`nullptr` 與智慧指標**

```cpp
#include <memory>

void use(int* p);

void f() {
    int* a = NULL;      // 舊：NULL 是整數 0，可能傳到 int 多載版本
    int* b = nullptr;   // C++11：型別安全的空指標，只匹配指標多載

    // 智慧指標：RAII 管理，離開作用域自動釋放，不需手動 delete
    auto u = std::unique_ptr<int>(new int(42)); // 獨佔所有權
    auto s = std::shared_ptr<int>(new int(42)); // 共享所有權、引用計數
}
```

## 相關條目
- [2003-C++03修正版](2003-C++03修正版.md)
- [2007-Clang與LLVM問世](2007-Clang與LLVM問世.md)
- [2014-C++14泛型Lambda](2014-C++14泛型Lambda.md)
