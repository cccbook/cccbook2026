# 2004：Scala 誕生

## 事件
Scala 由瑞士洛桑聯邦理工學院（EPFL）的 Martin Odersky 設計，2003 年內部使用，2004 年公開 1.0 版，2006 年的 2.0 版做了重大重新設計。Odersky 先前參與了 Java 泛型的設計：他創造 Pizza 語言（1997），再與 Philip Wadler 合作將其簡化為 GJ（Generic Java），GJ 成為 Java 5 泛型的基礎。Scala 的目標是「可純縮放（scalable）」：將物件導向與函數式程式設計無縫融合於 JVM 之上。

## 語法/特性加入的理論與實用原因

### 1. 函數式 + 物件導向的統合於 JVM
- **理論原因**：Odersky 主張「函數式是值的世界、物件導向是抽象的世界」，兩者可以統一——每個值都是物件、每個運算都是方法呼叫，函數本身是一等公民物件。
- **實用原因**：Java 1.4 沒有函數值、泛型與模式匹配，但擁有龐大的 JVM 生態；編譯到 JVM 位元組碼可以直接重用所有 Java 函式庫。
- **彌補缺陷**：函數式語言（ML、Haskell）無法重用 JVM 生態；Java 沒有函數式表達力——Scala 兩邊都補上。

```scala
// 函數是一等公民，集合操作管道化
val names = people.filter(_.age > 18).map(_.name).sorted
```

對照 Java 1.4：同樣的過濾排序要寫匿名類別與手動迴圈，Scala 一行管道解決：

```java
// Java 1.4：沒有函數值，只能用匿名類別 + 迴圈
List adultNames = new ArrayList();
for (Iterator it = people.iterator(); it.hasNext(); ) {
    Person p = (Person) it.next();            // 強制轉型
    if (p.getAge() > 18) adultNames.add(p.getName());
}
Collections.sort(adultNames);
```

### 2. case class 與模式匹配
- **理論原因**：將 ML 的代數資料型別（ADT）與模式匹配引進物件世界：case class 是「不可變資料 + 自動生成的結構相等性 + 可分解性」，模式匹配在理論上對應資料建構子的對偶（deconstruction）。
- **實用原因**：編譯器會對匹配的完整性（exhaustiveness）做靜態檢查，減少漏處理分支的 bug；這成為 Scala 處理資料的主流風格。
- **彌補缺陷**：Java 的 instanceof + 強制轉型既冗長又不安全；case class 模式匹配提供型別安全的分解。

```scala
sealed trait Shape
case class Circle(r: Double) extends Shape
case class Rect(w: Double, h: Double) extends Shape

def area(s: Shape): Double = s match {
  case Circle(r) => math.Pi * r * r
  case Rect(w, h) => w * h
}
```

對照 Java：同樣的形狀分解要靠 instanceof + 強制轉型，漏分支也不會被編譯器警告：

```java
// Java 1.4：instanceof 冗長、轉型不安全、漏處理分支無法靜態檢查
double area(Shape s) {
    if (s instanceof Circle) {
        return Math.PI * ((Circle) s).r * ((Circle) s).r;
    } else if (s instanceof Rect) {
        Rect r = (Rect) s;
        return r.w * r.h;
    }
    throw new IllegalArgumentException("unknown shape");  // 只能靠執行期才發現
}
```

`sealed trait` 封閉型別階層，編譯器檢查 match 的完整性；模式匹配還能解構嵌套結構：

```scala
sealed trait Expr
case class Add(a: Expr, b: Expr) extends Expr
case class Num(n: Int) extends Expr
case class Neg(a: Expr) extends Expr

// 巢狀模式匹配：直接解構運算式樹
def eval(e: Expr): Int = e match {
  case Num(n)        => n
  case Neg(a)        => -eval(a)
  case Add(Num(a), Num(b)) => a + b          // 特殊分支：兩個常數相加
  case Add(a, b)     => eval(a) + eval(b)
}
```

### 3. trait 與 mix-in 繼承
- **理論原因**：trait 是「無建構子參數的介面 + 部分實作」，以線性化（linearization）規則解決多重繼承的菱形問題，理論上接近 mix-in 模組。
- **實用原因**：比 Java 介面（當時無預設方法）更有表達力，比抽象類別更靈活可組合。
- **彌補缺陷**：Java 介面無法攜帶實作，程式碼重用受限。

trait 混合（mix-in）：以 `with` 疊加多個 trait，線性化規則保證組合順序明確：

```scala
trait Greeter { def greet(name: String): String = s"Hello, $name" }
trait FormalGreeter extends Greeter {
  override def greet(name: String): String = s"Dear ${name},你好"
}

// 線性化：with 的後者覆蓋前者
class Service extends Greeter with FormalGreeter
new Service().greet("阿明")   // "Dear 阿明,你好"
```

### 4. implicit（隱式轉換與隱式參數）
- **理論原因**：以型別推論機制解決「型別類別式多載」：隱式參數讓演算法可以泛化到任意型別而不改變呼叫端語法，理論上是 Haskell 型別類別的替身。
- **實用原因**：2.10（2012）起 implicits 擴展（implicit class、implicit macro）成為生態核心；2021 年 Scala 3 以 given/using 重新設計，讓隱式機制更明確可預測。
- **彌補缺陷**：Java 完全沒有擴展既有型別、泛化多載的機制。

implicit 的兩個典型用法：隱式參數扮演 Haskell 型別類別字典的角色，隱式類別替既有型別加方法：

```scala
// 隱式參數：演算法泛化到任意型別，呼叫端語法不變（Scala 2.10 前樣式）
def max[T](a: T, b: T)(implicit ord: Ordering[T]): T =
  if (ord.gt(a, b)) a else b

max(3, 5)                 // Ordering[Int] 由編譯器自動找到
max("apple", "banana")    // Ordering[String] 同樣自動找到

// 隱式類別（implicit class）：為既有型別「擴充」方法
implicit class RichString(s: String) {
  def shout: String = s.toUpperCase + "!"
}
"hello".shout             // "HELLO!"
```

### 5. Higher-kinded types
- **理論原因**：允許型別抽象以「型別建構子」為參數（如 `F[_]`），理論上支援泛化到容器層次的抽象（monad、functor 抽象）。
- **實用原因**：使 Scalaz、Cats 等函數式函式庫能在 Scala 上重現 Haskell 的抽象層次。
- **彌補缺陷**：Java 泛型（GJ）不支援高階多型，無法表達 `Monad<F>` 這類抽象。

高階型別（Higher-kinded types）：以 `F[_]` 抽象出「容器」層次，這是 Java 泛型做不到的：

```scala
// F[_] 是型別建構子參數：F 可代入 List、Option 等「容器」
trait Functor[F[_]] {
  def fmap[A, B](fa: F[A])(f: A => B): F[B]
}

implicit val listFunctor: Functor[List] = new Functor[List] {
  def fmap[A, B](fa: List[A])(f: A => B): List[B] = fa.map(f)
}

implicit val optFunctor: Functor[Option] = new Functor[Option] {
  def fmap[A, B](fa: Option[A])(f: A => B): Option[B] = fa.map(f)
}

def twice[F[_]](fa: F[Int])(implicit F: Functor[F]): F[Int] =
  F.fmap(fa)(_ * 2)

twice(List(1, 2, 3))    // List(2, 4, 6)
twice(Some(21))         // Some(42)
```

JVM 互操作：Scala 直接呼叫所有 Java API，無需任何橋接層：

```scala
// 直接使用 Java 標準函式庫
import java.util.HashMap
val m = new HashMap[String, Int]()
m.put("one", 1)
m.get("one")    // 1

// Scala 集合與 Java 日期 API 混用
import java.time.LocalDate
val days = (1 to 7).map(LocalDate.now.plusDays(_)).toList
```

## 彌補了什麼缺陷
Scala 彌補了「Java 沒有函數值與模式匹配、函數式語言不能重用 JVM 生態」的雙向缺陷。2008 年 Twitter 為了應對流量成長，將後端從 Ruby 遷移到 Scala，成為著名案例，帶動 Scala 在產業的採用。伏筆也埋下：語言過於複雜、implicit 氾濫、跨版本二進制不相容等問題累積多年，最終促成 2021 年的 Scala 3 大改版。

## 相關條目
- [1996-OCaml誕生](1996-OCaml誕生.md)
- [2005-Fsharp誕生](2005-Fsharp誕生.md)
- [2007-Clojure誕生](2007-Clojure誕生.md)
