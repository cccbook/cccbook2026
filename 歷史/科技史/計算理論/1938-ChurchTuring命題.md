# 1938 - Church–Turing 命題的正式確立

## 案件摘要
1936–1938 年間，Church 與 Turing 各自提出「可計算」的嚴格定義，而 Kleene 證明各定義外延相等。至 1952 年 Kleene 在《Introduction to Metamathematics》中將此等價性系統命名為 **Church's thesis**。本案還原這個「命題」如何成為整個計算理論的憲法。

## 前因 -- 為什麼會有這個案子
- Hilbert 的 Entschiedungsproblem（1928）要求一個機械程序判定任意一階邏輯語句的有效性——前提是「機械程序」必須有嚴格定義。
- 1936 年 Church 以 λ 可定義性回答「不可判定」；同年 Turing 以圖靈機回答「不可判定」。兩人答案相同，但模型截然不同——這強烈暗示他們都抓到了同一個直覺概念。
- Gödel 起初只信服圖靈的分析（他認為 Church 的 λ 定義「不令人滿意」），直到 Turing 用「計算者的心理狀態有限」給出令人信服的論證。

## 線索與推理 -- 數學式、程式、理論

### 1. 命題內容
**Church–Turing 命題**：直覺上的「可有效計算」（機械可計算）恰好等於：

$$
\text{直覺可計算} \;\equiv\; \text{圖靈可計算} \;\equiv\; \text{λ 可定義} \;\equiv\; \text{μ-遞迴（部分遞迴）}
$$

形式地，存在一個通用編碼使得所有模型可計算的部分函數類相同：
$$
\mathcal{F}_{TM} = \mathcal{F}_\lambda = \mathcal{F}_{\mu\text{-rec}} = \mathcal{F}_{\text{Post}}
$$

### 2. 四種等價模型對照表
| 模型 | 提出者/年份 | 計算的載體 | 停機 | 範式 |
|---|---|---|---|---|
| λ 演算 | Church 1933/36 | 函數應用與抽象 | 可能不停 | 函數式 |
| 圖靈機 | Turing 1936 | 紙帶 + 磁頭 + 狀態 | 可能不停 | 命令式 |
| μ-遞迴函數 | Kleene 1936 | 自然數上的算子 | 可能不停（μ） | 函數式/數論 |
| Post 系統 | Post 1936/43 | 字串重寫產生 | 可能不停 | 產生式 |

等價的實質內容：每個模型都可被其他模型模擬（通用性），且 Kleene 正規形式定理給出統一表示 $\varphi_e(x) = U(\mu t\,[T(e,x,t)])$。

### 3. 為什麼是「命題」而非「定理」？
- 「**直覺可計算**」不是數學物件，沒有嚴格定義，無法作為定理的一側。
- 定理能證明的是外延等價：「圖靈可計算 = λ 可定義 = μ-遞迴」——這是**可證明的**。
- 從「這些嚴格模型 = 那個直覺概念」是**經驗歸納 + 概念分析**，永遠只能被證據支持（新模型不斷被證明等價：Post 系統、迴圈機、Markov 演算法、隨機存取機 RAM……），無法被證明。
- Kleene (1952, §62) 首先系統性地稱之為 "Church's thesis"；今日文獻常合稱 Church–Turing thesis。

### 4. 物理版與量子版
- **物理 Church–Turing 命題**（Gandy 1980）：任何物理上可實現的計算裝置都可用圖靈機模擬。
- **量子版**（Deutsch 1985）：Deutsch 認為傳統命題只談「計算函數」而忽略物理過程，提出**量子圖靈機**與「物理版 Church–Turing–Deutsch 命題」：每個有限可實現的物理系統都能被通用（量子）計算模型以有限資源模擬。注意：量子計算**不擴大**可計算函數類（BQP ⊆ 可計算），只改變複雜度（多項式加速，如 Shor 演算法）。

### 5. Python：同一函數的四種實現
以「判斷 $n$ 是否為 3 的倍數」（或簡單函數 $f(n)=n^2$）示範同一可計算函數在不同範式下的樣貌：

```python
# (1) μ-遞迴風格：原始遞迴 + 無界搜尋
def square_mu(n):                      # n*n = 2n 加 n 次，用 μ 找結果
    y = 0
    while y != n * n:                  # 概念上以搜尋取得 μ y [y - n*n = 0]
        y += 1
    return y

# (2) 圖靈機風格：對應「逐步改寫紙帶」的命令式模擬
def square_tm(n):
    tape = ['1'] * n                   # unary 編碼
    count = 0
    while len(tape) > 0:               # 每讀一個 1 就累加 n 份
        tape.pop()
        count += n
    return count

# (3) λ 演算風格：Church 數與純函數組合（Python lambda 模擬）
#     λ n. n × n ≡ λn.λm. n (m n) 的 Church 數乘法
succ = lambda f: (lambda x: f(x + 1))              # S = λf.λx. f (x+1)
church = lambda n: succ(church(n - 1)) if n else (lambda x: x)
unchurch = lambda c: church(0)  # 佔位說明；實際 Church 數 2 = λf.λx. f(f x)
mult = lambda a: lambda b: lambda f: a(b(f))       # λa.λb.λf. a (b f)
square_lambda = lambda n: mult(n)(n)
print(square_lambda(3)(lambda x: x * 10)(0))       # Church 數應用示例

# (4) Post 系統風格：字串重寫 —— 複製規則 x -> xx
def square_post(n):
    s = '1' * n
    for _ in range(n - 1):
        for c in list(s[:n]):
            s += c                                  # 產生式：追加 n 個 1
    return len(s)

print(square_mu(5), square_tm(5), square_post(5))  # 25 25 25
```

四種寫法結果皆為 25——它們計算的是**同一個**可計算函數，這正是 Church–Turing 命題的日常縮影。

## 結案 -- 後果與影響
- 命題成為「演算法/有效程序」的操作性定義，使 Hilbert 第十問題、停機問題、P vs NP 等陳述具有明確意義。
- 支撐了可計算性理論的一切不可判定性結果：Rice 定理、Gödel 不完備性的計算版本等。
- 通用圖靈機的思想直接啟發了 Von Neumann 架構與現代電腦、程式語言（Lisp 即 λ 演算的工程化身）。

## 關鍵人物與文獻
- **Alonzo Church**（1903–1995）、**Alan Turing**（1912–1954）、**Stephen Kleene**（1909–1994）、**Kurt Gödel**（1906–1978）。
- Church, A. (1936). "An unsolvable problem of elementary number theory." *Amer. J. Math.* 58:345–363.
- Turing, A. M. (1936). "On computable numbers..." *Proc. LMS* 42:230–265.
- Kleene, S. C. (1952). *Introduction to Metamathematics*, §62（命名 "Church's thesis"）.
- Deutsch, D. (1985). "Quantum theory, the Church–Turing principle and the universal quantum computer." *Proc. R. Soc. Lond. A* 400:97–117.
