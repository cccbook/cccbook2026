# 1975：Scheme 誕生

## 事件
1975年，**Gerald Sussman** 與 **Guy Steele** 在 MIT 人工智慧實驗室創造了 **Scheme**——LISP 的方言，原名「Schemer」（因作業系統檔名長度限制去掉 r）。他們發表的論文《SCHEME: An Interpreter for Extended Lambda Calculus》（1975），以及 1975–1978 年間著名的 **Lambda Papers**（《Lambda: The Ultimate GOTO》等），重新定義了 LISP 與整個函數式程式設計。

## 語法/特性加入的理論與實用原因

### 1. 詞法作用域（Lexical Scoping）
- **理論原因**：λ 演算本來就是詞法作用域——束縛變數的意義由 λ 定義處決定。Sussman 與 Steele 決定讓 Scheme 的實作忠實於理論，而非沿襲 LISP 1.5 的動態作用域。
- **實用原因**：一級函數作為傳回值（funarg）時，必須捕捉定義時的環境，行為才可預測——這就是**閉包（closure）**。
- **彌補缺陷**：LISP 的動態作用域使自由變數在執行期才綁定，FUNARG 問題讓函數的行為難以推理；詞法作用域讓變數綁定在編譯（讀取）期就完全確定。

動態作用域 vs 詞法作用域的行為差異實例：同一個函數，動態作用域下自由變數跟著呼叫者變動，詞法作用域下永遠鎖定定義處：

```lisp
;; 動態作用域（LISP 1.5 風）：自由變數 x 由「呼叫處」決定
(define (f) (* x x))     ; x 是自由變數

(define (test)
  (let ((x 3)) (f)))     ; 呼叫 f 時，test 的 x=3 進入作用域
(define x 100)
(test)                   ; => 9   （x 是 test 裡的 3！）
(f)                      ; => 10000（x 是全域的 100）
;; 同一個函數，行為隨呼叫環境改變——無法局部推理
```

```scheme
;; 詞法作用域（Scheme）：x 在定義處就綁定
(define x 100)
(define (f) (* x x))
(define (test)
  (let ((x 3)) (f)))
(test)                   ; => 10000（永遠是定義處的 x=100）
;; 函數的行為與呼叫環境無關，可局部推理
```

### 2. 尾端呼叫優化（Proper Tail Calls）
- **理論原因**：`tail-call` 的語義等同於 goto——呼叫者已無事可做，直接跳轉即可。理論上「遞迴 = 迭代」，遞迴不需要消耗堆疊空間。
- **實用原因**：若遞迴總是消耗堆疊，函數式風格在深遞迴時會崩潰；尾端呼叫優化讓迴圈可以用純遞迴寫出，且空間消耗為常數。
- **彌補缺陷**：LISP 的遞迴在深度大時堆疊溢位；Lambda Paper《Lambda: The Ultimate GOTO》論證了尾端呼叫可消除這個問題。

```
(define (loop i)
  (if (= i 0) 'done
      (loop (- i 1))))   ; 尾端呼叫：常數空間，等同 while 迴圈
```

尾遞迴與非尾遞迴的對比：關鍵在於遞迴呼叫之後還有沒有「未完成的工作」（如乘法）：

```scheme
;; 非尾遞迴：乘法在遞迴傳回後才做 → 堆疊深度 O(n)
(define (fact n)
  (if (= n 0) 1
      (* n (fact (- n 1)))))     ; (* n ...) 等遞迴結果——不是尾呼叫

;; 尾遞迴：用累加器把「結果」帶進遞迴，呼叫後無事可做 → 常數空間
(define (fact-iter n acc)
  (if (= n 0) acc
      (fact-iter (- n 1) (* acc n))))   ; 尾呼叫，直接跳轉

(fact-iter 100000 1)   ; => 一個 456 位的大數，Scheme 不會堆疊溢位
(fact 100000)          ; 沒有尾呼叫優化的語言在這裡會堆疊溢位
```

named let 是 Scheme 慣用的尾遞迴寫法，迴圈變數就地命名：

```scheme
;; named let：迴圈與變數宣告合為一體
(let fact-iter ((n 5) (acc 1))
  (if (= n 0) acc
      (fact-iter (- n 1) (* acc n))))   ; => 120

;; 求列表長度：尾遞迴迴圈
(define (length l)
  (let loop ((l l) (n 0))
    (if (null? l) n
        (loop (cdr l) (+ n 1)))))
```

### 3. 一級閉包（First-class Closure）
- **理論原因**：λ 演算中「函數 + 其環境」就是閉包的數學原型；函數是一級公民，閉包自然也是。
- **實用原因**：閉包可用來實作物件、狀態機、延遲求值——Sussman 與 Steele 用閉包示範了各種控制結構的實作。
- **彌補缺陷**：傳統 LISP 的 funarg 因動態作用域而殘缺；Scheme 的閉包是完整、可預測的一級值。

閉包可以捕捉並攜帶可變狀態——用閉包做出「物件」：

```scheme
;; 閉包計數器：state 被閉包捕捉，外界無法直接碰觸
(define (make-counter)
  (let ((count 0))
    (lambda ()
      (set! count (+ count 1))
      count)))

(define c1 (make-counter))
(define c2 (make-counter))
(c1)   ; => 1
(c1)   ; => 2   c1 記得自己的 count
(c2)   ; => 1   c2 有各自獨立的 count——兩個閉包、兩份狀態
```

閉包捕捉的是「環境」而非「當下的值」——這正是 funarg 問題的正解：

```scheme
;; 三個加法器各自捕捉不同的 n
(define (make-adders)
  (map (lambda (n) (lambda (x) (+ x n))) '(1 10 100)))

(define adders (make-adders))
((car adders) 5)          ; => 6    捕捉 n=1
((cadr adders) 5)         ; => 15   捕捉 n=10
((caddr adders) 5)        ; => 105  捕捉 n=100
```

### 4. Continuation（續體）
- **理論原因**：`call/cc`（call-with-current-continuation）把「接下來的計算」本身變成一級值，理論上等價於 λ 演算的 CPS（Continuation-Passing Style）變換。
- **實用原因**：一個極簡原語就能實作例外處理、產生器、協程、非決定性計算等所有控制結構。
- **彌補缺陷**：傳統語言的控制流（goto、return）是硬編在語言裡的；continuation 讓控制結構成為函式庫而非語言特性。

`call/cc` 最經典的簡例：「提早傳回」不必靠 return 敘述——續體本身可以逃出計算：

```scheme
;; 找到第一個大於 100 的元素，立刻用續體跳脫整個遍歷
(define (find-big lst)
  (call/cc
    (lambda (return)                     ; return = 「目前的計算的其餘部分」
      (for-each (lambda (x)
                  (if (> x 100) (return x)))  ; 呼叫續體 = 提早離開
                lst)
      'not-found)))

(find-big '(3 7 250 9))   ; => 250
(find-big '(3 7 9))       ; => NOT-FOUND

;; 續體甚至可以在離開後再次被呼叫（可儲存、可重入）
(define saved #f)
(+ 1 (call/cc (lambda (k) (set! saved k) 1)))   ; => 2
(saved 10)                                       ; => 11（跳回 + 1 處，帶著 10）
```

### 5. 極簡核心
- **理論原因**：忠於 λ 演算——一切從函數應用出發，特殊形式越少越好。
- **實用原因**：第一版 Scheme 的報告只有一頁，極小的核心使直譯器容易移植，也容易作為教學與研究載具。
- **彌補缺陷**：LISP 1.5 累積了大量內建結構；Scheme 證明語言可以小而強大。

第一版 Scheme 直譯器的核心幾乎就是 λ 演算的直接翻譯——eval 只處理少數幾種形式，其餘一切交給函數應用：

```scheme
;; 極簡 Scheme 核心示意（R5RS 風）：eval 只有少數特殊形式
(define (eval expr env)
  (cond ((number? expr) expr)                    ; 自我求值
        ((symbol? expr) (lookup expr env))       ; 變數查環境
        ((eq? (car expr) 'lambda)
         (make-closure (cadr expr) (caddr expr) env))  ; 函數抽象
        ((eq? (car expr) 'quote) (cadr expr))    ; 引用
        (else (apply (eval (car expr) env)       ; 函數應用——核心引擎
                     (map (lambda (e) (eval e env))
                          (cdr expr))))))
;; 整個語言的語義一頁寫得完：特殊形式只有 lambda 與 quote
```

## 彌補了什麼缺陷
Scheme 解決了自 LISP 1.5 以來懸宕二十年的 FUNARG 問題：詞法作用域讓理論與實作終於一致；尾端呼叫優化讓遞迴真正等同於迭代；一級閉包與 continuation 讓所有控制結構可以用函數表達。Scheme 是第一個「忠實實作 λ 演算」的 LISP 方言，其設計直接影響了 Common Lisp、Racket、JavaScript（閉包與一級函數）與 Rust 等後世語言。

## 相關條目
- [1936-lambda演算邱奇奇點](1936-lambda演算邱奇奇點.md)
- [1962-LISP-1-5與GC巨集](1962-LISP-1-5與GC巨集.md)
- [1977-Backus函數式風格宣言](1977-Backus函數式風格宣言.md)
