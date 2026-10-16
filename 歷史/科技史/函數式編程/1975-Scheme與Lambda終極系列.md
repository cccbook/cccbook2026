# 1975-Scheme與Lambda終極系列

## 案件摘要

1975 年，Gerald Sussman 與 Guy Steele 在 MIT AI Lab 創造了 Scheme——史上最極簡的 Lisp 方言。Steele 隨後在 1975-1978 年間發表「Lambda: the Ultimate GOTO」等系列論文（AI Memo 443 等），證明了一個驚人的命題：函數呼叫就是 goto，尾呼叫不需要增長堆疊。加上詞法範疇、continuation-passing style 與 call/cc，Scheme 把「控制流」從機器細節提升為一等公民的數學物件，深刻影響了此後所有語言的設計。

## 前因 -- 為什麼會有這個案子

- 1970 年代初，MacLisp 已經太龐雜：幾十個 special forms、動態範疇、各種歷史包袱，不適合做語言實驗。
- Sussman 當時在研究 Carl Hewitt 的 actor 模型（1973），想弄清楚「actor 模型 vs closure」的真正差異是什麼——兩者看起來都像「帶行為的物件」。
- 他需要一個最小 Lisp 來做實驗：把不必要的機制全部砍掉，只留最核心的幾個構造。
- Steele 加入後，兩人在幾個月內寫出了第一版 Scheme 直譯器，意外發現了一個理論金礦：如果函數呼叫永遠不增長 stack，那「呼叫」與「跳躍」在語義上無法區分。
- 破案時刻：Steele 意識到這不只是實作技巧，而是一個理論命題——lambda 是 ultimate goto，於是寫成系列論文。

## 線索與推理 -- 數學式、程式、理論

### 線索一：極簡 Lisp

Scheme 的設計原則：語法只保留最少的 special forms——`lambda`、`if`、`define`、`quote`，其餘一切都是函數或 macro。第一版直譯器只有幾十行。

### 線索二：詞法範疇（lexical scoping）

與 MacLisp 的動態範疇不同，Scheme 的變數查 lookup 由程式文本的靜態結構決定：

```scheme
(define (make-adder n)
  (lambda (x) (+ x n)))    ; n 由定義處的詞法環境捕捉

(define add5 (make-adder 5))
(add5 3)                     ; => 8
```

這讓 lambda 真正成為「閉包」（closure）：函數值捕捉其定義環境，行為可預測、可數學推論。

### 線索三：適當尾端呼叫（proper tail call）-- 破案時刻

尾呼叫（tail call）是函數體的最後一個操作。Steele 證明：尾呼叫不需要保留呼叫者的堆疊框，因此不增長 stack：

```scheme
; 尾遞迴：最後的操作是呼叫自己，stack 不增長
(define (fact n acc)
  (if (= n 0)
      acc
      (fact n (- n 1) (* n acc))))   ; 尾呼叫

(fact 100000 1)                       ; 不會 stack overflow
```

實作上，直譯器把尾呼叫編譯成跳躍：

```python
# Python 模擬尾呼叫優化：trampoline
def trampoline(f, *args):
    while callable(result := f(*args)):
        args = result[1:] if isinstance(result, tuple) else ()
        f = result[0] if isinstance(result, tuple) else result
    return result

def fact_trampoline(n, acc=1):
    if n == 0:
        return acc              # 返回真值，跳出 trampoline
    return (fact_trampoline, n - 1, n * acc)  # 返回「跳躍目標」

print(trampoline(fact_trampoline, 100000))     # 算得出 100000!
```

「函數呼叫 = goto」的意義：尾呼叫優化讓迴圈只是尾遞迴的特例，控制結構可以全部用函數呼叫表達。

### 線索四：continuation-passing style（CPS）

CPS 是把控制流顯式化的變換：每個函數多一個參數 `k`（continuation，代表「接下來要做什麼」），所有呼叫都是尾呼叫：

$$\llbracket e \rrbracket_{\mathrm{cps}} : (\text{值} \to \text{答案}) \to \text{答案}$$

```scheme
; CPS 版本的 fact：k 是 continuation
(define (fact/k n k)
  (if (= n 0)
      (k 1)                          ; 尾呼叫
      (fact/k (- n 1)
              (lambda (v) (k (* n v))))))  ; 也是尾呼叫

(fact/k 5 (lambda (x) x))            ; => 120
```

CPS 中控制流完全由 continuation 參數決定，堆疊變成堆上的資料結構。這成為編譯器中間表示的基礎。

### 線索五：call/cc -- 一等公民續體

Scheme 的 `call-with-current-continuation`（call/cc）把「當前 continuation」做成一等公民的值：

```scheme
; call/cc 實作 non-local exit
(define (find-first pred lst)
  (call/cc
    (lambda (return)
      (for-each (lambda (x)
                  (when (pred x)
                    (return x)))    ; 跳出整個 for-each
                lst)
      #f)))

(find-first even? '(1 3 5 6 7))     ; => 6
```

continuation 是「程式剩餘部分」的具體化：呼叫它就跳到那個時刻繼續執行。這是控制流的最一般理論。

### 線索六：R5RS 的 define-syntax macro

後續 Scheme 標準（R5RS, 1998）加入衛生 macro（hygienic macro）`define-syntax`，讓使用者可以用語法規則擴充語言，同時不破壞詞法範疇。

## 結案 -- 後果與影響

- Scheme 成為 MIT 6.001 課程教材的基礎，催生經典教科書《Structure and Interpretation of Computer Programs》（SICP, Abelson 與 Sussman, 1985）。
- Racket（前 PLT Scheme）、Guile（GNU 的延伸語言）都是 Scheme 直系後裔。
- proper tail call 進入 ECMAScript 6 標準（實作於 JavaScriptCore/Safari），成為語言標準的一部分。
- CPS 成為編譯器中間表示：Andrew Appel 的 CPS 變換、GHC 的 STG（Spineless Tagless G-machine）皆為其後裔。
- continuation 影響 async/await：JavaScript、C#、Python 的 async/await 語法本質上是有限版本的 continuation 機制。
- 詞法範疇成為所有現代語言的標準；actor 模型的疑惑也促成了 Sussman 對「物件導向 vs 函數式」的持續思考。

## 關鍵人物與文獻

- Steele, G. L. and Sussman, G. J., *Scheme: An Interpreter for Extended Lambda Calculus*, MIT AI Memo 349, 1975。
- Steele, G. L., *Debunking the "Expensive Procedure Call" Myth or, Procedure Call Implementations Reconsidered*, MIT AI Memo 443, 1977。
- Steele, G. L., *Lambda: The Ultimate GOTO*, Proceedings of the ACM Conference on AI and Programming Languages, 1977。
- Steele, G. L., *Lambda: The Ultimate GOTO* 系列後續：*Lambda: The Ultimate Declarative* (AI Memo 379)、*The Art of the Interpreter* (Sussman and Steele, AI Memo 453, 1978)。
- Abelson, H. and Sussman, G. J., *Structure and Interpretation of Computer Programs*, MIT Press, 1985。
- Kelsey, R., Clinger, W., Rees, J. (eds.), *Revised^5 Report on the Algorithmic Language Scheme (R5RS)*, 1998。
- Hewitt, C., Bishop, P., Steiger, R., *A Universal Modular ACTOR Formalism for Artificial Intelligence*, IJCAI, 1973。
