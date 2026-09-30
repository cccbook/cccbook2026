# 2004 Scala：JVM 上的函數式革命

## 案發現場

2004 年，瑞士洛桑聯邦理工學院（EPFL）的 Martin Odersky 發布了 Scala 第一版。要理解這門語言為何誕生，得先看清楚當時 JVM 世界的「未解之謎」。

Java 在企業市場大獲全勝，但到 2000 年代中期，它的設計缺陷開始處處碰壁：

1. **函數式程式設計在企業界復興**，但 Java 拒絕它。Haskell 社群高談 Monad，學界推崇不變性與高階函數，而 Java 連「把函數當參數傳」都做不到——你只能寫一個只有一個方法的匿名類別，外加五行樣板程式碼。1990 年代末期，Odersky 本人參與設計了 Generic Java（Java 泛型的前身），深知在 Java 語言委員會內推動任何變更有多痛苦。
2. **多核心處理器時代來臨。** 2005 年前後，摩爾定律從「提升時脈」轉向「增加核心」。可變狀態 + 鎖的並行程式設計被證明極易出錯，函數式的不可變資料與純函數成為並行運算的救星。但 Java 的物件模型是「一切皆可變的物件」，與這個趨勢正面衝突。
3. **Java 語法臃腫。** `public static void main(String[] args)`、大量的 getter/setter、 Factory 工廠模式……開發者戲稱 Java 是「樣板碼產生器」。

誰遇到這個問題？數百萬被鎖在 JVM 生態上的企業開發者——他們離不開 JVM（類別庫太龐大、組織投資太深），卻渴望更強大的表達力。這就是 Scala 的案發現場：**如何在「不能離開 JVM」的約束下，設計一門融合物件導向與函數式的語言？**

## 偵查過程

Odersky 的履歷本身就是線索：他是 Pascal 之父 Niklaus Wirth 的學生（這不是巧合，瑞士洛桑正是 Wirth 的母校）、參與過 Java 泛型設計、還曾把 Pizza 語言編譯到 JVM。他的推理可拆解成四個關鍵靈感：

**靈感一：統一物件與函數。** 大多數語言把「物件」和「函數」當成兩個世界。Odersky 的核心推導是：**函數就是物件。** 在 Scala 裡，`Int => Int` 不過是 `Function1[Int, Int]` 這個 trait 的語法糖：

```scala
val f: Int => Int = (x: Int) => x * 2
// 等價於：
val g = new Function1[Int, Int] {
  def apply(x: Int): Int = x * 2
}
f(3)      // 6，其實是 f.apply(3)
```

這個統一讓兩大範式不再對立：方法可以被當值傳遞，高階函數只是「接收 Function 物件的方法」。

**靈感二：型別推導。** Java 要求到處寫型別，Haskell 幾乎不寫。Scala 選了中間路線：區域性型別推導。編譯器對 `val x = 3` 能推導出 `Int`，對函數參數則可要求顯式標註（避免全域 Hindley-Milner 推導與物件導向子型別結合時的爆炸問題）。2011 年 Java 8 終於補上 lambda，2014 年 Java 10 補上 `var`——都是朝 Scala 靠攏。

**靈感三：case class 與模式匹配。** 這是 Scala 對「代數資料型別」（ADT）的物件導向翻譯。Haskell 寫：

```haskell
data Shape = Circle Float | Rect Float Float
area (Circle r)     = pi * r * r
area (Rect w h)     = w * h
```

Scala 把它變成：

```scala
sealed trait Shape
case class Circle(r: Double) extends Shape
case class Rect(w: Double, h: Double) extends Shape

def area(s: Shape): Double = s match {
  case Circle(r)    => math.Pi * r * r
  case Rect(w, h)   => w * h
}
```

關鍵推導在於 `case class` 自動生成：不可變欄位、結構相等的 `equals`/`hashCode`、以及 `apply`/`unapply` 對（後者正是模式匹配解構的機制）。`sealed` 關鍵字讓編譯器能靜態檢查匹配的完備性——把 Haskell 型別系統的嚴謹，嫁接到 JVM 物件模型上。

**靈感四：trait。** Java 的介面不能有實作，多重繼承又臭名昭著（C++ 的菱形問題）。Scala 的 trait 可以有具體方法與欄位，用**線性化**（linearization）規則解決菱形衝突：

$$
\text{class } C \text{ extends } B \text{ with } A \implies \text{linearization} = C \succ A \succ B
$$

呼叫 `super` 時沿線性化順序往右找，讓 mixin 行為可預測。Java 8 的 default method 正是向 trait 致敬。

## 結案報告

Scala 的遺產可以說是「以一門語言撬動了整個 JVM 生態」：

1. **Spark 大數據之母。** 2009 年，UC Berkeley 的 Matei Zaharia 在 Scala 上寫出了 Apache Spark。為何選 Scala？因為 Spark 的核心正是「把函數與資料集一起傳給叢集」——`rdd.map(f).filter(...)` 這種 API 只有 Scala 的函數式基因能優雅支撐。沒有 Scala，就沒有今天的大數據生態。
2. **Twitter、LinkedIn 的生產實戰**，證明了函數式語言可以在企業級規模下運作，替 Kotlin 鋪平了道路。
3. **逼 Java 進化。** Java 8（2014）的 lambda 與 Stream API、Java 9 的模組系統、後來的 record 與 sealed 類別——幾乎每一項都能在 Scala 找到前身。這就是著名的「更好的 Java」之辯：Scala 支持者說「Scala 就是那個更好的 Java」；反對者說「Scala 太複雜，更好的 Java 是 Kotlin」。無論誰對，赢家都是 JVM 生態。
4. **類型系統研究的前線。** Scala 的型別系統（依賴型別、higher-kinded types）成為學界實驗場，其後繼者 Scala 3 更引入了與 Idris 血緣相近的 dependent function types。

Scala 的教訓同樣深刻：表達力與簡潔性的張力無法完全消除。它的符號過載（`::`、`:::`、`_`）與隱式轉換嚇退了不少開發者——這條教訓被後來的 Kotlin 與 Rust 記住了。

## 證據與工具

用 Scala 展示核心遺產：case class、模式匹配與高階函數（Spark API 的原型）：

```scala
// sealed trait + case class：代數資料型別的 OO 化
sealed trait Expr
case class Num(n: Int) extends Expr
case class Add(a: Expr, b: Expr) extends Expr
case class Mul(a: Expr, b: Expr) extends Expr

// 模式匹配：遞迴求值器
def eval(e: Expr): Int = e match {
  case Num(n)    => n
  case Add(a, b) => eval(a) + eval(b)
  case Mul(a, b) => eval(a) * eval(b)
}

val e = Mul(Add(Num(1), Num(2)), Num(3))  // (1+2)*3
println(eval(e))  // 9

// 高階函數：Spark API 的原型
val xs = List(1, 2, 3, 4, 5)
val result = xs.map(_ * 2).filter(_ > 4).sum
println(result)  // map 後為 2,4,6,8,10，filter 後為 6,8,10，sum = 24
```

再用 Python 模擬 Scala 的型別推導核心——對一個小型運算式語言做區域性型別推導：

```python
# 模擬區域性型別推導：根據運算式結構推導型別
def infer(expr, env={}):
    if isinstance(expr, (int, float)):
        return type(expr).__name__
    if isinstance(expr, str):           # 變數：查環境
        if expr not in env:
            raise TypeError(f"not found: {expr}")
        return env[expr]
    op, a, b = expr
    ta, tb = infer(a, env), infer(b, env)
    if op in "+-*" :
        if {ta, tb} <= {"int"}:
            return "int"
        if {ta, tb} <= {"int", "double"}:
            return "double"
        raise TypeError(f"cannot {op} {ta} and {tb}")
    raise TypeError(f"unknown op {op}")

env = {"x": "int", "y": "double"}
print(infer(("+", "x", 3)))            # int
print(infer(("*", "y", ("+", "x", 1))))# double
try:
    infer(("+", "y", "x", ))           # int 與 double 混合在 * 之外被拒
except TypeError as e:
    print("TypeError:", e)
```

這個推導器展現了 Scala 編譯器的日常：沿著語法樹下行，由局部資訊合成型別。2004 年 Odersky 把這套機制搬上 JVM，從此函數式程式設計不再是學院的奢侈品，而是大數據時代的工業基礎。
