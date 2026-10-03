# 2014-Java8Lambda

## 案件摘要

2014 年 3 月，Oracle 發布 Java 8，正式引入 lambda 表達式、Stream API 與方法引用——這是全球最大的語言群體（Java 程式設計師）第一次在日常程式碼中直接使用 λ-Calculus 的語法。本案的主偵探是 Brian Goetz，他從 2008 年起主導 Project Lambda，歷時六年。案發背景是：Java 的匿名內部類寫回呼極其冗長，而多核時代 Java 缺乏平行抽象；同時 C# LINQ（2007）、F#（2005）、Scala（2004）已示範函數式語法的工業價值。Goetz 的破案哲學是「函數式進化而非革命」：lambda 不是新東西，而是既有 SAM 型別的語法糖。Java 8 於是成為函數式思想「全面內建」的關鍵證據。

## 前因 -- 為什麼會有這個案子

- Java 的匿名內部類（anonymous inner class）寫一個回呼要五行以上，GUI 監聽器與回呼地獄讓程式碼冗長不堪。
- 2005 年後多核 CPU 成為主流，Java 缺乏輕量的平行抽象，開發者只能手寫執行緒與鎖。
- C# LINQ（2007）、F#（2005）、Scala（2004）已在工業界示範：lambda + 高階函數能寫出更短、更安全、更容易平行化的程式。
- Goetz 的立場：Java 的文化是穩定與向後相容，需要「進化」而非「革命」——lambda 必須能無縫接入既有型別系統，而非另起爐灶。
- Java 語言的現狀：`interface` 只能放抽象方法，任何語法演化都必須回答「lambda 的型別是什麼」這個根本問題。

## 線索與推理 -- 數學式、程式、理論

### 線索一：SAM 型別與脫糖（desugaring）

Java 沒有獨立的函數型別。Goetz 的解法：lambda 就是 **functional interface**（只有一個抽象方法的介面，SAM，Single Abstract Method）的實例。編譯器做「脫糖」：

```java
// 原始寫法（匿名內部類）
Comparator<String> c = new Comparator<String>() {
    public int compare(String a, String b) { return a.length() - b.length(); }
};

// Java 8 lambda：同一件事，編譯器脫糖成上述結構的變體
Comparator<String> c2 = (a, b) -> a.length() - b.length();
```

型別論上，若介面 $I$ 只有一個抽象方法 $m: A \to R$，則 lambda $\lambda x . \ e(x)$ 的型別即為 $I$：

$$
\frac{I \text{ 是 SAM，} \ m : A \to R}{(\lambda x . \ e(x)) : I}
$$

這讓 λ-Calculus 的語法進入了 Java，但型別仍是熟悉的介面——「進化而非革命」的破案關鍵。

### 線索二：Stream API 的 lazy 與 eager

Stream API 把運算分兩類：

- **惰性中間操作（lazy）**：`map`、`filter`、`sorted`——只建立運算描述，不執行。
- **終端操作（eager）**：`collect`、`forEach`、`reduce`——觸發整條流水線執行。

數學上，`map` 是函子（functor）映射，`reduce` 是摺疊（fold）：

$$
\text{map}(f, [x_1, x_2, \ldots]) = [f(x_1), f(x_2), \ldots] \quad ; \quad \text{reduce}(f, z, [x_1, x_2, x_3]) = f(x_1, f(x_2, f(x_3, z)))
$$

lazy 的價值：`(a, b) -> a.length() - b.length()` 這類描述能被融合（fusion），元素像流水線一樣逐一通過 map 與 filter，中間集合不落地。

### 線索三：java.util.function 與 default method

Java 8 內建 `java.util.function` 套件，提供核心函數型別：

- `Function<T, R>`：$T \to R$，映射；
- `Supplier<T>`：$() \to T$，供給；
- `Consumer<T>`：$T \to ()$，消費；
- `Predicate<T>`：$T \to \text{bool}$，判斷。

同時引入 **default method**：介面可以有預設實作。這解決了演化難題——若給 `Collection` 加 `stream()` 方法，所有實作類別都會壞掉；default method 讓介面能演化而不破壞相容性。

### 線索四：parallel stream（fork-join 的函數式包裝）

`.parallelStream()` 把流水線交給 ForkJoinPool 執行。為什麼函數式寫法才能輕鬆平行？因為純函數不共享可變狀態，reduce 的結合律保證任意切分都正確：

$$
f(f(a, b), c) = f(a, f(b, c)) \ \Rightarrow \ \text{任意分治皆同值}
$$

這是資料平行化的數學基礎：結合律 + 純函數 = 免鎖平行。

### 破案時刻：可執行程式碼示範

```java
import java.util.List;
import java.util.stream.Collectors;

public class Java8Demo {
    public static void main(String[] args) {
        List<String> names = List.of("Ada", "Alan", "Grace", "Edsger", "Turing");

        // Stream：map / filter lazy，collect 觸發
        List<String> longOnes = names.stream()
                .filter(n -> n.length() > 3)        // Predicate
                .map(String::toUpperCase)           // 方法引用
                .collect(Collectors.toList());
        System.out.println(longOnes);               // [ALAN, GRACE, EDSGER, TURING]

        // reduce：摺疊求總長度
        int total = names.stream()
                .map(String::length)
                .reduce(0, Integer::sum);
        System.out.println(total);                  // 25

        // parallel stream：同一條純函數流水線，換個入口即平行
        int total2 = names.parallelStream()
                .map(String::length)
                .reduce(0, Integer::sum);
        System.out.println(total2);                 // 25（結合律保證同值）
    }
}
```

同一段 `map + reduce`，只需把 `stream()` 換成 `parallelStream()` 就能平行——這是匿名內部類時代做不到的破案證據。

## 結案 -- 後果與影響

- Java 生態全面函數式化：`Optional`、`CompletableFuture`、`Map.computeIfAbsent` 等 API 都以 lambda 為使用介面。
- 全球最大的語言群體（Java 程式設計師）第一次在日常程式碼中使用 λ-Calculus 的語法——函數式思想「全面內建」的關鍵證據。
- Kotlin（2011 發布、2016 1.0）與 C# 持續對照發展，函數式語法成為主流靜態語言標配。
- Stream API 的 lazy + 融合模型成為資料處理流水線的工業範式，與 Spark 的 RDD 思想同源。
- 證明了「函數式進化而非革命」可行：不推翻型別系統，用語法糖與介面演化也能讓數十年的舊語言獲得新生命。

## 關鍵人物與文獻（條例，含真實文獻書目）

- **Brian Goetz**：Project Lambda 主導者，Java Language Architect（Oracle，前 Sun）；**Alex Buckley、Mark Reinhold** 為 Java 8 語言規範與平台演化的關鍵人物。
- Goetz, B. (2008). *State of the Lambda*（Project Lambda 設計文件）. OpenJDK, http://cr.openjdk.java.net/~briangoetz/lambda/lambda-state-final.html
- Gosling, J., et al. (2014). *The Java Language Specification, Java SE 8 Edition*. Oracle.
- Meijer, E., Beckman, B., & Bierman, G. (2006). *LINQ: Reconciling Object, Relations and XML in the .NET Framework*. Proceedings of SIGMOD '06, 706.
- Church, A. (1941). *The Calculi of Lambda-Conversion*. Princeton University Press.（lambda 語法的數學源頭）
