# 1966-LandinSECD與ISWIM

## 案件摘要

1960 年代初，λ-Calculus 的理論與實際機器執行之間存在一道鴻溝：Church 的演算優雅，卻沒有人知道如何在電腦上一步步執行它。Peter Landin（Oxford 出身，任職於 Unvic/Carnegie）在 1964 年的論文 "The mechanical evaluation of expressions" 中，偵造出 SECD 虛擬機——一台以四個暫存器驅動的抽象機器，能機械化地求值任何表示式。1966 年，他再以 "The next 700 programming languages" 提出共同核心 ISWIM，宣稱未來的七百種語言都應該長得像它。破案時刻在於 closure 一詞的誕生：Landin 不只造了機器，還造了整個函數式編程的詞彙。

## 前因 -- 為什麼會有這個案子

- 理論與機器的鴻溝：λ-Calculus 有 Church-Rosser 定理保證語義，但沒有對應的執行模型，LISP 的 `eval` 缺乏形式化。
- Algol 60 委員會的混亂：報告以自然語言描述語義，call-by-name、own 等概念定義不清，連委員自己都爭論不休。
- LISP 的問題：S-expression 語法（大量括號）不受主流程式設計師歡迎，McCarthy 的 M-expression 始終未實作。
- Landin 的野心：為「下一個七百種語言」找一個共同核心，讓語言設計變成「核心 + 語法糖」的工程。
- ALGOL 家族的繼承問題：需要一種方式同時容納函數式與命令式風格。

## 線索與推理 -- 數學式、程式、理論

### 線索一：SECD 虛擬機的四個暫存器

Landin 的機器有四個狀態成分，整個機器狀態是一個四元組：

$$
\text{State} = (S, E, C, D)
$$

- Stack：儲存中間結果
- Environment：變數到值的綁定
- Control：待執行的指令串
- Dump：呼叫函數時保存的舊狀態

轉移規則（transition rules）以小步語義描述，例如變數求值：

$$
([], E, (\text{id}) :: C, D) \longrightarrow (E(\text{id}) :: [], E, C, D)
$$

函數應用則把 dump 當作返回地址：保存舊的 $(S, E, C)$，建立新環境求值函數體，結束後從 dump 回復。

### 線索二：closure 的誕生

Landin 定義了 closure 這個詞：函數值不只是 $\lambda x.M$，還必須攜帶定義時的環境 $\rho$：

$$
\text{closure} = (\lambda x.\, M,\; \rho)
$$

這解決了自由變數的歸屬問題——函數「封裝」（close over）其定義環境。SECD 機器中，函數求值就產生 closure 推入堆疊；應用時以 closure 的環境為基底擴充新綁定。

### 線索三：ISWIM 的語法革命

ISWIM（If you See What I Mean）以 M-expression 為基礎，加上兩項發明：

- where 子句：`x = a where f = ...` 把定義放在使用之後，呼應數學寫作習慣。
- offside rule（縮排規則）：以縮排取代括號——「有東西在右邊突出就是運算元」。此規則後進入 Haskell 與 Python 的語法。
- letrec：遞迴綁定，$\text{letrec}\; f = e \;\text{in}\; b$ 的語義由 SECD 機器中的循環環境實現。

### 破案時刻：Python 實作 mini-SECD 機器

```python
def secd_run(code):
    # code: 指令串；閉包為 ('LDF', body)，應用為 ('AP',)
    s, env, c, d = [], {}, list(code), []
    while c:
        op, c = c[0], c[1:]
        op0, arg = op[0], op[1] if isinstance(op, tuple) and len(op) > 1 else None
        if op0 == 'LD':          s.append(env[arg])
        elif op0 == 'LDC':       s.append(arg)
        elif op0 == 'LDF':       s.append(('closure', arg, dict(env)))
        elif op0 == 'AP':
            closure, x = s.pop(), s.pop()
            _, body, fenv = closure
            d.append((s, env, c))            # 保存舊狀態
            s, env, c = [], dict(fenv, x=x), list(body)
        elif op0 == 'RTN':
            result = s.pop()
            s, env, c = d.pop()
            s.append(result)
        elif op0 == 'OP':        # 算術
            b, a = s.pop(), s.pop()
            s.append({'+': a + b, '-': a - b, '*': a * b}[arg])
    return s[0]

# 計算 (3 + 4) * 5 = 35
# body: 加上 5 後返回
code = [
    ('LDC', 3), ('LDC', 4), ('OP', '+'),
    ('LDC', 5), ('OP', '*'),
]
print(secd_run(code))  # 35

# 應用閉包：(lambda x. x + 1) 10 = 11
code2 = [
    ('LDC', 10),
    ('LDF', [('LD', 'x'), ('LDC', 1), ('OP', '+'), ('RTN')]),
    ('AP',),
]
print(secd_run(code2))  # 11
```

這台機器重現了 Landin 1964 年的轉移規則：`AP` 保存狀態進入 dump，`RTN` 從 dump 回復——函數呼叫的機械本質一目了然。

### 補充線索

- Church-Rosser 性質：$\beta$-歸約的順序不影響最終結果（合流性），保證 SECD 的小步求值語義一致：

$$
\text{若 } M \to^* P \text{ 且 } M \to^* Q,\ \text{則存在 } N \text{ 使 } P \to^* N \text{ 且 } Q \to^* N
$$

- "program = evaluated expression"：Landin 的函數式世界觀——語言只是表示式的包裝，求值才是本體。
- Landin 1965 年的 "A correspondence between ALGOL 60 and Church's lambda-notation" 證明命令式結構也能編碼進 λ-Calculus。

## 結案 -- 後果與影響

- ML（Gordon, 1970s）、Miranda（Turner, 1985）、Haskell（1990）的語法與語義基礎皆可追溯到 ISWIM。
- offside rule 進入 Haskell 與 Python：Python 的縮排語法可視為 Landin 1966 年的直系後裔。
- SECD 成為所有函數式虛擬機的祖先：STG（Spineless Tagless G-machine，Peyton Jones）、CEK 機器、Krivine 機器皆屬 SECD 系譜。
- closure 一詞沿用至今，成為所有現代語言（JS、Python、Scala、Rust）的核心概念。
- 「核心語言 + 語法糖」的設計方法論成為語言工程標準，影響 Scheme 的 R報告傳統。

## 關鍵人物與文獻（條列）

- Peter J. Landin, "The mechanical evaluation of expressions", The Computer Journal, 6(4), 1964, pp. 308–320（SECD 機器）.
- Peter J. Landin, "A correspondence between ALGOL 60 and Church's lambda-notation", Communications of the ACM, 8(2-3), 1965, pp. 89–101, 158–165.
- Peter J. Landin, "The next 700 programming languages", Communications of the ACM, 9(3), 1966, pp. 157–166（ISWIM）.
- Alonzo Church, "The Calculi of Lambda-Conversion", Princeton University Press, 1941（λ-Calculus 與 Church-Rosser 定理）.
- J. Barkley Rosser, "A New Proof of the Church-Rosser Theorem", The Journal of Symbolic Logic, 20(2), 1955, pp. 157–163.
- Simon L. Peyton Jones, The Implementation of Functional Programming Languages, Prentice Hall, 1987（STG 與 SECD 傳統）.
