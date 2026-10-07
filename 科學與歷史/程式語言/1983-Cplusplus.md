# 1983 C++ 誕生：Stroustrup 的「帶類別的 C」與抽象化零成本之謎

## 案發現場

1979 年，丹麥電腦科學家 Bjarne Stroustrup 加入貝爾實驗室，投入分散式系統的模擬研究。他很快發現自己需要的東西不存在：

- **Simula 67** 的類別與繼承非常適合建模，但太慢——模擬跑不動。
- **C**（[1972-C語言.md](1972-C語言.md)）快且可攜，但太低階——大型系統的模組化無從下手。

未解之謎是：**能不能在保留 C 的效能、低階控制與可攜性的同時，加上 Simula 式的資料抽象化與物件導向？換句話說：「抽象化的代價能不能是零？」**

這個問題為何重要？當時（與之後四十年）的語言設計主流是二分法：要嘛選動態語言（Lisp、Smalltalk）享受抽象但犧牲效能，要嘛選組合語言級的語言享受效能但放棄抽象。Stroustrup 的信念是：**靜態型別 + 編譯期解析 + 精心設計的語言機制，可以讓抽象化不付出執行期代價。**

他從 1979 年的「C with Classes」開始，1983 年更名為 C++，加入虛擬函數、運算子重載、參考、模板等關鍵特性。1985 年《The C++ Programming Language》出版，1989 年實作移植到多種機器，1998 年 ISO 標準化。

## 偵查過程

Stroustrup 的核心技術推理：

**第一步：虛擬函數表（vtable）。** C++ 的關鍵發明是把多型編譯成零成本的位址表查找。對每個含虛擬函數的類別，編譯器產生一張靜態函數指標表：

```
class Shape { virtual void draw(); virtual double area(); }
vtable[Shape] = [&Shape::draw, &Shape::area]

class Circle : public Shape { void draw() override; double area() override; }
vtable[Circle] = [&Circle::draw, &Circle::area]   // 覆寫的槽位指向 Circle 版本
```

每個物件多一個隱藏欄位 `vptr` 指向其類別的 vtable。呼叫 `p->draw()` 被編譯為：

$$\text{call}\ \ vptr[0](p)$$

這是兩次間接定址，對比 Smalltalk 的執行期方法查找（字串/符號比對）或 Lisp 的泛型函數派發，vtable 幾乎免費——而且可以被 CPU 分支預測優化。**這就是「零成本抽象化」的第一個範例。**

**第二步：模板與泛型程式設計。** 1988 年 Stroustrup 加入模板，原本只是為了泛型的容器類別，卻意外開啟了圖靈完備的編譯期計算：

```cpp
template <class T>
class vector { T* data; int size; ... };

template <int N>
struct factorial {
    static const int value = N * factorial<N-1>::value;
};
template <> struct factorial<0> { static const int value = 1; };
// factorial<5>::value == 120，編譯期算出
```

模板實例化在編譯期為每個型別生成專屬程式碼，泛型不付出任何執行期代價——與 ML（[1973-ML型別推導.md](1973-ML型別推導.md)）的多型同源異趣：ML 用單一程式碼+型別變數，C++ 用編譯期複製程式碼。

**第三步：RAII。** C++ 的記憶體管理策略：資源的取得與釋放綁定到**物件的生命週期**。建構子取得資源、解構子釋放資源，而解構子在物件離開作用域時由編譯器自動呼叫：

```cpp
class File {
    FILE* f;
public:
    File(const char* name) : f(fopen(name, "r")) {}   // 取得
    ~File() { if (f) fclose(f); }                      // 釋放（自動）
};
```

這用確定性的作用域規則解決了 C 的手動 `free` 遺漏問題，又不需垃圾回收。RAII 成為現代語言資源管理的範本——Rust 的所有權與 drop、Python 的 `with` 都是其思想後裔。

## 結案報告

C++ 的遺產：

- **效能與抽象兼得的典範**：「零成本抽象化」成為語言設計的黃金準則，Rust、Swift、Rust 的 `zero-cost` 口號都直接繼承。
- **語言系譜**：Java（[1995-Java.md](1995-Java.md)）取其類別語法捨棄指標；C#、D、Rust（所有權取代手動記憶體）都是 C++ 的回應。
- **STL 與現代泛型**：Alexander Stepanov 的 STL（1994）證明了「以迭代器 + 演算法 + 概念」組成的泛型程式設計，模板元程式設計（TMP）開啟了編譯期計算的大門，影響了 D 的 `static if`、Rust 的 const generics、C++20 的 concepts。
- **工業霸權**：遊戲引擎、瀏覽器（Chrome）、金融交易系統、作業系統核心模組，C++ 至今是高效能系統的標準。

C++ 證明：**抽象化的代價可以降到零——只要你願意把複雜度移到編譯期。**

## 證據與工具

C++ 示範——vtable 多型、模板、RAII：

```cpp
#include <cstdio>
#include <memory>

class Shape {
public:
    virtual double area() const = 0;      // 虛擬函數 → vtable
    virtual ~Shape() = default;
};

class Circle : public Shape {
    double r;
public:
    explicit Circle(double r) : r(r) {}
    double area() const override { return 3.14159 * r * r; }
};

template <int N>                            // 編譯期階乘
struct Fact { static const int value = N * Fact<N-1>::value; };
template <> struct Fact<0> { static const int value = 1; };

class Timer {                               // RAII
    const char* tag;
public:
    explicit Timer(const char* t) : tag(t) { printf("[%s] start\n", tag); }
    ~Timer() { printf("[%s] end（自動釋放）\n", tag); }
};

int main() {
    std::unique_ptr<Shape> s = std::make_unique<Circle>(2);
    printf("area = %f\n", s->area());       // 經 vtable 派發
    printf("5! = %d\n", Fact<5>::value);    // 編譯期 120
    { Timer t("scope"); }                   // 離開作用域自動呼叫解構子
    return 0;
}
```

用 Python 模擬 vtable 派發與 RAII：

```python
class Shape:
    _vtable = {"area": None}

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2
    Circle._vtable["area"] = area       # 覆寫 vtable 槽位

def virtual_call(obj, method):          # 模擬 p->draw() 的編譯結果
    return type(obj)._vtable[method](obj)

print(virtual_call(Circle(2), "area"))  # 12.57

class Timer:                            # 模擬 RAII
    def __init__(self, tag): self.tag = tag; print(f"[{tag}] start")
    def __enter__(self): return self
    def __exit__(self, *exc): print(f"[{self.tag}] end（自動釋放）")

with Timer("scope"):
    pass
```
