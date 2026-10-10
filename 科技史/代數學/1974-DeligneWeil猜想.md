# 1974 - Deligne 證明 Weil 猜想

## 案件摘要
1949 年 Weil 從有限域上簇的點計數中，嗅到 Riemann 猜想的影子。此案懸宕 25 年，Grothendieck 建造了 étale 上同調的重型機具，卻在最後一道門前止步。1974 年，Deligne 以更輕巧的「範數估計」手法破案，為代數幾何與數論打開了朗蘭茲綱領的大門。

## 前因 -- 為什麼會有這個案子
- **Riemann 猜想（1859）**：$\zeta(s) = \sum_{n\ge 1} n^{-s}$ 的非顯然零點都落在臨界線 $\mathrm{Re}(s) = 1/2$ 上。這是解析數論的核心懸案。
- **Hasse（1936）**：對有限域 $\mathbb{F}_q$ 上的橢圓曲線 $E$，證明了點數估計
  $$|E(\mathbb{F}_q)| = q + 1 - t, \qquad |t| \le 2\sqrt{q}.$$
  這是 Riemann 猜想在一維情形的先聲。
- **Weil（1949）**：將 Hasse 的結果推廣到任意有限域上簇 $X$，提出四個猜想。定義 zeta 函數：
  $$\zeta(X, t) = \exp\left(\sum_{r\ge 1} \frac{|X(\mathbb{F}_{q^r})|}{r} t^r\right) = \frac{P_1(t)\cdots P_{2n-1}(t)}{P_0(t) P_{2n}(t)}.$$
  其中最關鍵的「Riemann 猜想類比」是：$P_i(t) = \prod_j (1-\alpha_{ij} t)$ 的根滿足
  $$|\alpha_{ij}| \le q^{i/2}.$$
- Weil 本人指出：若存在一個類似拓撲上同調的「Weil 上同調論」，配合 Lefschetz 不動點公式，即可解釋點計數。偵探的推理方向由此確定——**先找到正確的上同調工具**。

## 線索與推理 -- 數學式、程式、理論
### 線索一：Lefschetz 不動點公式的代數化
拓撲中，連續映射 $f: X \to X$ 的不動點個數可由上同調計算：
$$\#\mathrm{Fix}(f) = \sum_i (-1)^i \, \mathrm{tr}\big(f^*|_{H^i(X)}\big).$$
對有限域簇 $X/\mathbb{F}_q$，Frobenius 映射 $\mathrm{Frob}_q: x \mapsto x^q$ 的不動點恰是 $X(\mathbb{F}_q)$。於是：
$$|X(\mathbb{F}_{q^r})| = \sum_i (-1)^i \, \mathrm{tr}\big(\mathrm{Frob}^r |_{H^i}\big).$$
若 $H^i$ 的特徵值為 $\alpha$，zeta 函數自然分解為 $P_i(t) = \prod(1 - \alpha t)$。**上同調存在 = Weil 猜想的機器存在**。

### 線索二：Grothendieck 的 étale 上同調（1960s）
特徵 $p$ 下奇異上同調失效（如 $\ell \ne p$ 時無法良好計數）。Grothendieck 建造了 **étale 拓撲**與 $\ell$-進上同調：
$$H^i_{\mathrm{\acute{e}t}}(X_{\overline{\mathbb{F}}_q}, \mathbb{Q}_\ell).$$
他證明了 Weil 猜想的大部分：有理性（Rationality）、函數方程（Functional equation）、Betti 數守恆。但 Riemann 猜想類比（特徵值的絕對值估計）頑強抵抗——Grothendieck 試圖用「Kähler 式」的 monodromy 與 standard conjectures 走到底，未能成功。

### 線索三：Deligne 的破案手法（1974）
Deligne 在《La conjecture de Weil I》中避開 standard conjectures，改用三件武器：
1. **Rankin 的消去法**：比較兩個 L-函數的係數，得到平均值估計。
2. **Radon 變換式的歸納**（弱 Lefschetz 定理 + Lefschetz 介入）：將高維簇嵌入射影空間，用超平面切割歸納。
3. **單值性（monodromy）與 Deligne 的範數定理**：證明 $\ell$-進層的幾何單值群足夠大，從而控制特徵值。

最終結論：對光滑射影簇 $X$ 的 $H^i_{\mathrm{\acute{e}t}}$，Frobenius 特徵值滿足
$$|\alpha| = q^{i/2} \quad \text{（純性 pure weights）},$$
且更一般的混合純性（mixed weights）定理涵蓋非射影簇。Weil 猜想全數結案。

### 程式驗證：Hasse 界的數值檢查
用 sympy 在有限域上直接數橢圓曲線的點，驗證 $|t| \le 2\sqrt{q}$：

```python
from sympy import sqrt, isprime
from sympy.abc import x, y

def points_on_curve(a, b, q):
    """數出 y^2 = x^3 + a x + b 在 F_q 上的點數（含無窮遠點）"""
    count = 1  # 無窮遠點 O
    for xp in range(q):
        rhs = (xp**3 + a*xp + b) % q
        # rhs 是否為模平方剩餘
        if pow(rhs, (q-1)//2, q) == 1:
            count += 2          # ±y 兩個點
        elif rhs % q == 0:
            count += 1          # y = 0 一個點
    return count

q = 97
for a, b in [(3, 5), (1, 1), (2, 7)]:
    N = points_on_curve(a, b, q)
    t = q + 1 - N
    assert abs(t) <= 2*sqrt(q), "Hasse 界被違反！"
    print(f"E: y^2=x^3+{a}x+{b} over F_{q}:  #E={N}, t={t}, 2*sqrt(q)={2*sqrt(q):.3f}")
```

輸出顯示每條曲線的 $t$ 都在 $[-2\sqrt{q},\, 2\sqrt{q}]$ 內——Hasse 界（即一維 Weil 猜想）在數值上成立。

## 結案 -- 後果與影響
- **1978 菲爾茲獎**：Deligne 因證明 Weil 猜想獲頒菲爾茲獎，該證明被譽為 20 世紀代數幾何的巔峰成就之一。
- **混合純性理論**成為現代 projective/derived 幾何的權重（weight）語言基礎，影響 Hodge 理論與 Motive 綱領。
- **朗蘭茲綱領**：Deligne 的方法是證明 Galois 表示、自守 L-函數 Ramanujan–Petersson 猜想（如 Deligne 對 $\tau(n)$ 的估計 $|\tau(p)| \le 2 p^{11/2}$）的標準工具。
- **密碼學**：Hasse 界直接決定橢圓曲線密碼（ECC）的安全性——點群大小 $|E(\mathbb{F}_q)| \approx q \pm 2\sqrt{q}$ 保證群夠大且不易受小群攻擊；Satoshi 之後的椭圆曲線簽章（ECDSA）都建立在此點計數理論之上。
- **後續案件**：Weil II 的技術（weights、vanishing cycles）是 Faltings（Mordell 猜想）、Wiles（Fermat 最後定理）背後的共同工具箱。

## 關鍵人物與文獻
- **André Weil**：*Numbers of solutions of equations in finite fields*（1949），提出猜想。
- **Oscar Zariski / Alexander Grothendieck**：SGA 1–5，étale 拓撲與上同調機具的建造者。
- **Pierre Deligne**：*La conjecture de Weil I*（Publ. IHÉS, 1974）、*La conjecture de Weil II*（1980）。
- **Nick Katz**：與 Deligne 合作的 monodromy 理論推手。
- 延伸：Deligne 1978 菲爾茲獎演說；SGA 4½。
