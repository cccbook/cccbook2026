# 1983：C++ 命名與 virtual 函式——多型就此誕生

## 事件
1983 年，C with Classes 更名為 **C++**（`++` 是 C 的遞增運算子，寓意「C 的下一個版本」）。同年加入了 **virtual 函式**、函式名多載（overloading）、預設參數、`//` 註解等特性。

## 關鍵語法/特性
- **virtual 函式**：宣告為 `virtual` 的成員函式，呼叫時依物件的**動態型別**分派——執行時期多型（runtime polymorphism）。
- **函式名多載**：同名函式可依參數型別不同而有多個版本。
- **預設參數**：`void f(int x = 0);`
- **`//` 單行註解**：從 BCPL 借來，1998 年才正式納入標準。

## 為何重要
- **virtual 是 C++ 物件導向的核心**：有了它，才能「以介面操作、實作可替換」——設計模式（GoF 1994）幾乎全部建立在 virtual 函式上。
- **虛擬函式表（vtable）** 的實作機制：只有用到的物件才付出分派成本——「不使用就付費」零成本抽象原則的具體體現。

## 理論與實用原因
- **理論原因**：Simula 67 的虛擬程序（virtual procedure）、 subtype polymorphism（子型別多型）理論。
- **實用原因**：貝爾實驗室的大型系統（如交換機軟體）需要模組之間以穩定介面解耦，同時在熱點程式碼保有 C 的速度。

## 彌補了什麼缺陷
彌補了 C with Classes「只有靜態分派、無法用統一介面操作不同實作」的缺陷；也彌補了 C「函式名不可重複、無法依型別自動分派」的缺陷。

## 程式範例

**舊寫法**：C 只能用函式指標表手動分派，容易出錯：

```c
/* C 寫法：手動維護函式指標表，新增形狀就要改分派程式碼 */
struct Shape;
typedef double (*area_fn)(struct Shape *);

struct Circle { double r; };
double circle_area(struct Circle *c) { return 3.14159 * c->r * c->r; }

/* 呼叫端必須自己記住「哪種型別對應哪個函式」：
   型別一多，函式指標表與 switch 就成了災難，還沒有型別檢查。 */
```

**新寫法**：`virtual` 函式自動依動態型別分派，達成執行時期多型：

```cpp
#include <cstdio>

class Shape {
public:
    virtual double area() { return 0; }   // virtual：允許衍生類別覆寫
    virtual ~Shape() {}
};

class Circle : public Shape {
    double r;
public:
    Circle(double r) : r(r) {}
    double area() { return 3.14159 * r * r; }  // 覆寫基底實作
};

class Rect : public Shape {
    double w, h;
public:
    Rect(double w, double h) : w(w), h(h) {}
    double area() { return w * h; }
};

int main() {
    Shape *s[2] = { new Circle(1), new Rect(2, 3) };
    for (int i = 0; i < 2; i++)
        printf("%f\n", s[i]->area());  // 呼叫端不需要知道實際型別，自動分派
    delete s[0]; delete s[1];
}
```

同年加入的函式多載與預設參數，彌補了 C「函式名不可重複、無法依型別自動分派」的缺陷：

```cpp
void print(int x)   { printf("%d\n", x); }     // 同名函式，依參數型別分派
void print(double x){ printf("%f\n", x); }

void set_level(int level = 1);  // 預設參數：呼叫時可省略，等價於 set_level(1)
```

## 相關條目
- [1979-CWithClasses誕生](1979-CWithClasses誕生.md)
- [1985-Cfront與C++程式語言一書](1985-Cfront與C++程式語言一書.md)
