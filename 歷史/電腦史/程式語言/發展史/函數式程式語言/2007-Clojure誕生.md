# 2007：Clojure 誕生

## 事件
2007 年，Rich Hickey 發布了 Clojure 的第一個公開版本。Clojure 是一個 Lisp 方言，編譯為 JVM 位元碼，與 Java 完整互操作。Hickey 的核心主張是：在多核心時代，「以可變物件與鎖為基礎」的程式設計模型已經破產，語言應該把「不可變性」與「函數式併發」變成預設。此後陸續推出 ClojureScript（2011，編譯到 JavaScript）與 ClojureCLR，並發展出自有的建置工具 Leiningen（2010）與 CLI/deps.edn（2017）。

## 語法/特性加入的理論與實用原因
### 1. 不可變資料結構為預設（persistent data structures）
- **理論原因**：承襲 Okasaki《Purely Functional Data Structures》（1996 博士論文，1998 出書）的成果——純函數式資料結構可以透過 path copying 與結構共享（structural sharing）達到接近可變結構的效能。Clojure 進一步採用 HAMT（Hash Array Mapped Trie，源自 Bagwell 2001）實作 map/set，使更新操作只複製 O(log n) 的路徑，而非整個結構。
- **實用原因**：不可變值可自由跨執行緒共享，不需加鎖；等價性檢查、快取、撤銷（undo）都變得簡單。
- **彌補缺陷**：Java 的可變物件在併發下需要散彈槍式的同步設計；傳統 Lisp（Common Lisp、Scheme）的 list/set 也是可變操作為主。

```clojure
(def m {:a 1 :b 2})
(def m2 (assoc m :c 3))  ; m 不變，m2 是共享大部分結構的新 map
m   ;=> {:a 1, :b 2}
m2  ;=> {:a 1, :b 2, :c 3}
```

不可變 vector 的操作同樣只複製 O(log n) 的路徑，新版與舊版共享尾端結構，因此「保留歷史版本」幾乎不需額外成本：

```clojure
(def v [1 2 3])           ; persistent vector 字面量
(def v2 (assoc v 2 99))   ; v 不變，v2 共享前段結構
v   ;=> [1 2 3]
v2  ;=> [1 2 99]
(conj v 4)                ;=> [1 2 3 4]，v 仍不變
```

對照組：Java 的可變 list 在併發下必須靠鎖保護每個存取點，漏掉任何一處就是競態：

```java
// Java：可變 list + 鎖，每個使用點都要記得同步
List<Integer> list = Collections.synchronizedList(new ArrayList<>());
synchronized (list) {      // 迭代時仍須手動加鎖，容易遺漏
    for (Integer x : list) { process(x); }
}
```

Clojure 則因為資料不可變，跨執行緒共享完全不需鎖，「安全」由資料結構本身保證而非由紀律保證。

### 2. STM（軟體事務記憶體）與 refs、atoms、agents
- **理論原因**：源自資料庫事務與 STM 研究的 optimistic concurrency——讀寫共享狀態如同交易，衝突時重試，避免死鎖。
- **實用原因**：把「協調多個狀態的改變」交給 `ref` + `dosync`，把「獨立單一狀態」交給 `atom`，把「非同步、最終一致」交給 `agent`，語義分明。
- **彌補缺陷**：Java 的 synchronized 與 Lock 组合容易死鎖、競態，且難以組合（composability）。

```clojure
(def counter (atom 0))
(swap! counter inc)  ; CAS 式更新，無鎖
@counter             ;=> 1，讀取永遠看到一致的快照
```

對照組：Java 的 synchronized 版本不僅冗長，兩把鎖的取得順序不對還會死鎖：

```java
// Java：可變狀態 + synchronized
class Counter {
    private int n = 0;
    synchronized void inc() { n++; }  // 依賴紀律，組合多個狀態易出錯
}
```

單一狀態用 `atom`；需要「原子性地同時改多個狀態」時用 `ref` + `dosync`，STM 會在衝突時自動重試整個交易：

```clojure
(def balance-a (ref 100))
(def balance-b (ref 0))

(dosync                       ; 整個區塊是原子交易
  (alter balance-a - 30)
  (alter balance-b + 30))     ; 若期間他人改過 a 或 b，整筆交易自動重試
```

兩個 ref 的更新要不就全部生效、要不全部不算，這正是 Java 鎖難以做到的 composability。

### 3. 巨集與「資料即程式」
- **理論原因**：Lisp 的 homoiconicity——程式碼就是資料，巨集在編譯期以一般程式操作語法樹。
- **實用原因**：缺什麼語法自己長什麼（如 `core.async` 的 `go` 區塊即為巨集變換）；比 Java 的註解處理器更有表達力。
- **彌補缺陷**：Java 缺乏編譯期語法擴充能力；CL 的巨集傳統則缺少現代函數式核心。

巨集接收的是語法樹（list 形式的資料），因此可以用一般程式操作它。例如自訂一個 `unless`：

```clojure
(defmacro unless [test then else]
  `(if (not ~test) ~then ~else))   ; ` 為語法引用，~ 為解引用

(unless false :ok :ng)  ;=> :ok，展開為 (if (not false) :ok :ng)
```

另一個例子：用巨集自動產生多個相似的定義，展現「程式產生程式」：

```clojure
(defmacro defgetters [m & ks]
  `(do ~@(map (fn [k] `(defn ~(symbol (str k "-of")) [] (get ~m ~k))) ks)))

(defgetters {:a 1 :b 2} :a :b)  ; 一次產生 a-of、b-of 兩個函數
(a-of)  ;=> 1
```

### 4. 函數式併發取代鎖（core.async，2013）
- **理論原因**：CSP（Communicating Sequential Processes）的 channel 模型。
- **實用原因**：`go` 巨集把 callback 地獄變成同步風格程式碼，同一套 API 適用 JVM 與 JavaScript。
- **彌補缺陷**：直接操作執行緒與鎖的心智負擔。

`go` 巨集把同步風格程式碼改寫成狀態機，channel 則承襲 CSP 的溝通模型：

```clojure
(require '[clojure.core.async :as a])

(a/go-loop [n 0]                 ; go 巨集讓迴圈看起來同步，實為非同步狀態機
  (let [x (a/<! ch)]             ; <! 從 channel 取值，不阻塞執行緒
    (when (< n 3)
      (println "收到" x)
      (a/recur (inc n)))))

(a/>!! ch 42)                    ; 送值進 channel
```

core.async 的同一套 API（`<!`/`>!`）在 JVM 與 JavaScript 上都能用，是巨集變換威力的實證。

Clojure 也以 threading macro（`->`）把嵌套呼叫改寫成資料流方向，可讀性大幅提升：

```clojure
; 嵌套寫法：由內往外讀
(inc (reduce + (filter odd? [1 2 3 4 5])))
; threading macro：由上往下讀，資料流一目了然
(->> [1 2 3 4 5]
     (filter odd?)
     (reduce +)
     (inc))   ;=> 10
```

## 彌補了什麼缺陷
Clojure 證明了「不可變為預設 + 函數式併發」可以在主流平台（JVM）上實用且高效，解決了 Java 併發地獄與傳統 Lisp 缺乏現代語義的問題。其 persistent data structures 的成功帶動風潮：Swift 的 value semantics、C++ 的 `std::span`/immutable views、Java 的 records 與 Unmodifiable collections，乃至 Rust 的所有權模型，都可見「預設不可變」的影子。

## 相關條目
- [1958-LISP誕生](1958-LISP誕生.md)
- [1998-Haskell-98標準化](1998-Haskell-98標準化.md)
- [2004-Scala誕生](2004-Scala誕生.md)
- [2010-Haskell2010標準](2010-Haskell2010標準.md)
- [2025-函數式程式語言的未來展望](2025-函數式程式語言的未來展望.md)
