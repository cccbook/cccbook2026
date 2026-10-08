# 1984：Common Lisp 標準化

## 事件
1984 年，由 **Guy Steele** 主編的《Common Lisp: The Language》（俗稱 CLtL1）問世，宣告了 LISP 方言大戰的終結。到了 1994 年，美國國家標準學會正式核准 **ANSI X3.226**，Common Lisp 成為 ISO 級別的官方標準。這是第一門由委員會統合數十種方言而成的大型多範式語言。

## 語法/特性加入的理論與實用原因
### 1. 統一數十種方言
- **理論原因**：1980 年代 LISP 世界分裂嚴重——Maclisp、Zetalisp、Scheme、Interlisp、Spice Lisp、NIL 等方言各自發展，語意互不相容，阻礙了學術成果的累積。Common Lisp 以 Maclisp 血統為主幹，吸收各家優點，建立單一共通核心。
- **實用原因**：商業 AI 產業與 **Lisp Machine** 市場（Symbolics、Lisp Machines Inc.）急切需要一個可攜的標準，使程式能跨硬體平台執行。
- **彌補缺陷**：方言分裂造成的可攜性災難與重複投資。

同一份 Common Lisp 程式（defun、條件系統、CLOS）在所有符合標準的實作上（SBCL、CCL、LispWorks）行為一致，對照相當年 Maclisp 與 Zetalisp 在 `eq`、字串處理、錯誤機制上互不相容的處境。可選參數與關鍵字參數也是標準化的產物：

```lisp
;; 可選參數與關鍵字參數：各方言以往各有不同的參數傳遞慣例
(defun transpose (matrix &optional (n (length matrix)) &key (fill 0))
  (if (null matrix)
      nil
      (cons (mapcar (lambda (row) (or (nth n row) fill)) matrix)
            nil)))
```

### 2. CLOS：多重分派物件系統
- **理論原因**：**Common Lisp Object System（CLOS，1988 年併入標準）**採用**多重分派（multiple dispatch）**——方法選擇依所有參數的型別決定，而非僅第一個參數。這在理論上比 Smalltalk/Single-dispatch 更貼近 multimethod 的數學一般化，並以 generic function 將方法與類別解耦。
- **實用原因**：AI 知識表示需要彈性的物件模型；CLOS 後來被證明可用 metaobject protocol 形式化描述。
- **彌補缺陷**：Flavors 與 New Flavors 等前代物件系統的不一致。

```lisp
(defmethod collide ((a asteroid) (b spaceship)) ...)
(defmethod collide ((a spaceship) (b asteroid)) ...)
;; 分派依「所有」參數型別決定——多重分派
```

完整的多重分派範例：兩個參數的型別「組合」共同決定呼叫哪個方法，這是 single-dispatch 語言（如 Smalltalk）做不到的——後者只有 `a` 能決定分派：

```lisp
(defclass asteroid () ())
(defclass spaceship () ())
(defclass planet () ())

(defgeneric collide (x y))

(defmethod collide ((a asteroid) (s spaceship))
  (format t "小行星撞飛船：船體受損~%"))
(defmethod collide ((a asteroid) (p planet))
  (format t "小行星撞行星：地表留下隕石坑~%"))
(defmethod collide ((s spaceship) (p planet))
  (format t "飛船降落行星：成功著陸~%"))

(collide (make-instance 'asteroid) (make-instance 'planet))
;; → 小行星撞行星：地表留下隕石坑（由「兩個」參數型別共同決定）
```

### 3. 條件系統（condition system）
- **理論原因**：Common Lisp 的 condition system 將「**訊號（signal）**」與「**處理（handler）**」徹底分離，並加入**條件式重啟（restarts）**——錯誤發生後，堆疊上層可提供多種恢復策略（如重試、使用預設值），由更上層或互動式除錯器選擇。理論上這比後來 Java/Python 的 try/catch（只能「跳脫」）更先進：try/catch 只能展開堆疊，condition system 能在錯誤點**恢復執行**。
- **實用原因**：互動式開發（REPL）文化中，除錯器本身就是語言的一部分。
- **彌補缺陷**：早期方言僅有的 `errset`、`catch/throw` 過於原始。

以下簡例展示「錯誤點可恢復執行」：`divide` 內部註冊了 `use-value` 重啟，上層 handler 選擇它之後，執行**回到錯誤點繼續**，而非展開堆疊——這是 Java/Python try/catch 做不到的：

```lisp
(defun safe-divide (x y)
  (restart-case
      (if (zerop y)
          (error "除以零：~a / ~a" x y)
          (/ x y))
    (use-value (v) v)))          ; 提供重啟：改用呼叫者給的值

(handler-case
    (safe-divide 10 0)
  (error () (invoke-restart 'use-value 999)))   ; 選擇重啟 → 回到錯誤點
;; → 999（執行未中斷，對照 try/catch 只能跳脫）
```

### 4. 巨集標準化
- **理論原因**：LISP 的 code-as-data（同像性，homoiconicity）配合 `defmacro`，讓語言本身可用巨集擴充；標準化確保巨集在所有實作中行為一致。
- **實用原因**：AI 研究者常用巨集發展領域專用語言（DSL）。
- **彌補缺陷**：各方言巨集語意差異。

defmacro 以 code-as-data 在編譯期展開，是發展 DSL 的基礎工具：

```lisp
;; defmacro：編譯期把 (unless-nil x a b) 展開成 cond 形式
(defmacro unless-nil (var then &optional else)
  `(cond ((null ,var) ,else)
         (t ,then)))

(unless-nil '(1 2) '有值 '空的)   ;; → 有值
```

## 彌補了什麼缺陷
Common Lisp 彌補了 **LISP 生態的方言分裂**，以單一可攜標準統合 Maclisp、Zetalisp、Scheme、Interlisp 等數十種方言，支撐了 1980 年代商業 AI 產業。但它也付出了代價：為相容舊方言而**保留動態作用域遺跡**（special variables），且語言**龐大複雜**——這反而促使[1975-Scheme誕生](1975-Scheme誕生.md)的極簡主義路線繼續獨立發展。其條件系統與 CLOS 至今仍是語言設計的標竿。

## 相關條目
- [1958-LISP誕生](1958-LISP誕生.md)
- [1975-Scheme誕生](1975-Scheme誕生.md)
- [1983-StandardML誕生](1983-StandardML誕生.md)
- [1985-Miranda誕生](1985-Miranda誕生.md)
