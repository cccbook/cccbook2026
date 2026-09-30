# 1976 - Miller 質數檢驗

## 案件摘要
1976 年，Gary Miller 發表《Riemann's Hypothesis and Tests for Primality》：在**廣義黎曼假設（ERH）**成立的前提下，質數檢驗可以在**確定性多項式時間**內完成。這是隨機質數檢驗的前奏——他的檢驗形式正是後來 Miller–Rabin 演算法的骨架，只差一個「隨機化」的靈感（Rabin, 1980，見 `1980-Rabin質數檢驗.md`）把它從條件性變成無條件的機率算法。

## 前因 -- 為什麼會有這個案子
質數檢驗是密碼學的基石（RSA, 1977），而 1976 年最快的確定性檢驗是 $O(\sqrt{n})$ 試除——對 100 位數的 RSA 模數完全不可行。同時，數論中有個老工具：**費馬小定理**：

$$a^{n-1} \equiv 1 \pmod n \quad (n \text{ 為質數}, \gcd(a,n)=1)$$

但它有反例（Carmichael 數，如 561 = 3·11·17，所有 $a$ 都通過費馬檢驗卻是合數）。Miller 的洞察：用**平方根的高階結構**堵住這些反例。

## 線索與推理 -- 數學式、程式、理論

### Miller 檢驗的數學
$n$ 為奇質數時，$\mathbb{Z}_n^*$ 是循環群，費馬的平方根結構：

若 $n$ 是奇質數，寫 $n - 1 = 2^s \cdot d$（$d$ 奇數），則對任意 $a$：

$$a^d \equiv 1 \pmod n, \quad \text{或存在 } 0 \le r < s \text{ 使 } a^{2^r d} \equiv -1 \pmod n$$

**為什麼**：在質數模下，$x^2 \equiv 1 \pmod n$ 只有解 $x \equiv \pm 1$（因 $n | (x-1)(x+1) \implies n | x-1$ 或 $n | x+1$）。從 $a^{n-1} = (a^d)^{2^s} \equiv 1$ 逐層開平方根，根號鏈上必然經過 $-1$ 或一開始就是 $1$。

**合數偽證**：若某 $a$ 違反上述條件，則 $n$ 必為合數（$a$ 是「合數性證人」）。

### Miller 的定理
**定理**：若 ERH 成立，則對奇合數 $n$，必存在證人 $a < C \log^2 n$（某常數 $C$）。

**推理**：由 ERH，$L(s, \chi)$ 的零點都在 $\Re(s) = 1/2$ 線上；由此 Ankeny (1952) 的結果給出：每個非二次剩餘群結構的偏差會在 $O(\log^2 n)$ 內出現證人。

於是檢驗只需枚舉 $a = 2, 3, \dots, O(\log^2 n)$——**確定性 $O(\log^4 n)$ 時間**（每個 $a$ 用平方乘法 $O(\log n)$ 次模乘）。

但：**ERH 是未證明的假設**——這個「解」吊在半空中。

### 程式碼：Miller 檢驗的核心

```python
def miller_witness(n, a):
    """檢查 a 是否為 n 的合數性證人"""
    if n % 2 == 0: return n != 2
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    x = pow(a, d, n)                    # a^d mod n
    if x == 1 or x == n - 1:
        return False                    # 不是證人（通過檢驗）
    for _ in range(s - 1):
        x = pow(x, 2, n)                # 逐層平方
        if x == n - 1:
            return False
    return True                         # 違反根號鏈結構 => n 是合數！

print(miller_witness(561, 2))    # True：Carmichael 數 561 被 2 抓包
                                  # （費馬檢驗對 561 完全失效！）
print(miller_witness(97, 2))     # False：97 是質數
```

**偵探筆記**：費馬檢驗查「$a^{n-1} \equiv 1$」，Miller 檢驗進一步查「根號鏈是否經過 $-1$」——Carmichael 數能偽造費馬條件，卻偽造不了**平方根的唯一性結構**（$\pm 1$ 定理在質數模下無可偽造）。這是「用更深的代數結構堵住反例」的推理典範。

### 懸而未決的跳板
Miller 留下的問題：**沒有 ERH，能否多項式時間檢驗質數？**

- Rabin (1980) 的答案：**隨機化**——隨機選 $a$，錯誤機率 $\le 4^{-k}$（見 `1980-Rabin質數檢驗.md`）
- AKS (2002) 的答案：**確定性**——最終解決（見 `../計算理論/2002-AKS質數檢驗.md`）

## 結案 -- 後果與影響
- **Miller–Rabin 演算法**：1980 年 Rabin 將其隨機化，成為至今密碼學產生 RSA 金鑰的標準質數檢驗。
- **BPP 的殺手級應用**：第一次有一個「重要問題，隨機算法遠快於已知確定性算法」——隨機算法學科的成立宣言。
- **密碼學的基礎設施**：HTTPS、區塊鏈的每次金鑰生成都在跑 Miller–Rabin。
- **理論餘波**：質數檢驗在 BPP 中（1976–2002），最終 AKS 證明在 P 中——「BPP 是否 = P」的核心案例之一。

## 關鍵人物與文獻
- **Gary Lee Miller**（1946–）：Riemann's Hypothesis and Tests for Primality (1976, JCSS)
- **Ankeny**：least quadratic non-residue (1952)——$O(\log^2 n)$ 的來源
- **Carmichael**：561 等費馬偽質數（1910）
- 交叉參照：`1980-Rabin質數檢驗.md`、`../計算理論/2002-AKS質數檢驗.md`
