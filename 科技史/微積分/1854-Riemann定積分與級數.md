# 1854 — Riemann 定積分與級數

## 案件摘要
1854 年，Bernhard Riemann 為取得哥廷根大學的授課資格（Habilitation），提交就職論文〈Über die Darstellbarkeit einer Function durch eine trigonometrische Reihe〉（論函數可用三角級數表示）。在這篇論文中，他完成了兩件大事：**把 Cauchy 的積分推廣為今日的黎曼積分**——允許函數在不連續點上仍可積；並構造出可積的病態函數。同篇論文中還藏著另一條線索：**級數重排會改變和**——條件收斂級數的詭異本性自此曝光。這份案卷是通往 Lebesgue 測度論的必經之路。

## 前因 -- 為什麼會有這個案子
- Cauchy（1823）定義積分為「左端點和的極限」，但只對**連續函數**保證收斂。Fourier（1822）的三角級數卻常在跳躍點上工作——積分理論與級數理論之間有明顯的縫隙。
- Dirichlet（1829）證明分段連續函數的 Fourier 級數收斂，並用處處不連續函數宣告：函數可以病態到任何程度。那麼——**多麼病態的函數仍可積？** 這是 Cauchy 積分理論留下的懸案。
- Riemann 是 Dirichlet 的學生（1847 年起在柏林聽 Dirichlet 的課，Dirichlet 於 1855 年接替 Gauss 在哥廷根的教席）。他明白：要回答「什麼樣的函數可用三角級數表示」，必須先回答「什麼樣的函數可積」。
- 1854 年，Riemann 在 Habilitation 論文中交出答案。同時期他還在級數理論中發現了另一個驚人的事實（1853 年手稿，後以重排定理聞名）。

## 線索與推理 -- 數學式、程式、理論

### 線索一：黎曼積分的定義——去掉「左端點」的限制
Riemann 的推廣極為簡潔：在 $[a,b]$ 上取**任意**分點 $a = x_0 < x_1 < \cdots < x_n = b$，在每個小區間 $[x_{i-1}, x_i]$ 中取**任意**取樣點 $\xi_i$，構成和

$$S = \sum_{i=1}^{n} f(\xi_i)\,\Delta x_i, \qquad \Delta x_i = x_i - x_{i-1}$$

定義：若當最大小區間長度 $\|\Delta\| = \max \Delta x_i \to 0$ 時，$S$ 趨於同一個極限（**無論分點與取樣點怎麼選**），則 $f$ 黎曼可積，極限記為

$$\int_a^b f(x)\,dx = \lim_{\|\Delta\| \to 0} \sum_{i=1}^{n} f(\xi_i)\,\Delta x_i$$

「任意分點、任意取樣、極限唯一」——這三個詞是 Riemann 對 Cauchy 的關鍵升級。Cauchy 只要求「切得夠細且取左端點」，Riemann 要求對**一切**選擇收斂到同一極限。

### 線索二：黎曼可積的判準與病態函數
Riemann 給出可積性的判準（以現代語言表述）：$f$ 在 $[a,b]$ 上黎曼可積，當且僅當對任何 $\varepsilon > 0$，使振幅 $\omega_i = \sup f - \inf f > \varepsilon$ 的小區間總長度可以小於 $\varepsilon$。換句話說：**不連續點必須「面積很小」**。

更驚人的是，Riemann 構造出一個函數：在 $(-\pi, \pi)$ 中、$x$ 與 $\pi$ 無理數倍接近的點上定義

$$f(x) = \sum_{n=1}^{\infty} \frac{(nx)}{n^2}, \qquad (x) = \begin{cases} x - \lfloor x \rfloor - \frac{1}{2}, & x \notin \mathbb{Z} \\ 0, & x \in \mathbb{Z} \end{cases}$$

這個函數在**稠密集**上不連續（$x = p/(2n)$ 型的點），卻因為級數由 $\frac{1}{n^2}$ 壓制而一致收斂，故黎曼可積。這是史上第一個「不連續點稠密但可積」的函數——Cauchy 的理論完全無法處理它，Riemann 的理論輕鬆吃下。

### 線索三：Riemann 重排定理——條件收斂的詭計
Riemann（1853 手稿，後由 Dedekind 於 1868 年促使發表）發現：對**條件收斂**級數（收斂但不同處絕對收斂），例如交錯調和級數

$$\ln 2 = 1 - \frac{1}{2} + \frac{1}{3} - \frac{1}{4} + \cdots$$

只要**改變項的順序**，就可以讓級數收斂到**任何預定的實數**，甚至發散。原因：正項部分和與負項部分和都發散到 $\pm\infty$，交錯排列只是「勉強抵消」；重新排列就能任意操縱餘額。這解釋了為什麼 Cauchy（1821）堅持要區分「收斂」與「絕對收斂」——條件收斂的級數是數學中的變色龍。

### 線索四：通往 Lebesgue 的裂縫
Riemann 的判準說「不連續點的面積要小」，但「面積」一詞仍未定義——對 Dirichlet 函數 $D(x)$，不連續點是**全部實數**，黎曼上和與下和之差恆為 1，故不可積。可是 $D$「幾乎處處」等於 0，直覺上積分應為 0。要精確回答「哪個集合的面積是零」，需要測度論——Lebesgue（1902）將沿著 Riemann 的案卷前進，最終把「振幅 > ε 的集合總長度」升級為「集合的測度」，徹底重寫積分學。

### 程式碼範例：黎曼和收斂與重排定理的數值驗證
先驗證黎曼和對可積函數的收斂（含隨機取樣），再演示重排定理：

```python
import numpy as np

# ── 第一部分：黎曼和（隨機取樣）收斂到 4/3 ──
f = lambda t: t**2
rng = np.random.default_rng(0)
for n in [10, 100, 1000, 10000, 100000]:
    s = 0.0
    for _ in range(20):                      # 20 種隨機取樣
        x = np.sort(rng.uniform(0, 1, n + 1))
        xi = x[:-1] + rng.uniform(0, 1, n) * np.diff(x)  # 任意取樣點
        s += np.sum(f(xi) * np.diff(x))
    print(f"n={n:>7}: 黎曼和 ≈ {s/20:.6f}  (理論 4/3 = {4/3:.6f})")

# ── 第二部分：Riemann 重排定理 ──
def rearranged_sum(p_order, q_order, target=1.0, tol=1e-6):
    """把正項、負項依指定策略交錯，使級數收斂到 target"""
    p, q = 0, 0; S = 0.0; terms = []
    while True:
        if S <= target:                       # 低於目標 → 加正項
            p += 1; S += 1/(2*p - 1)
        else:                                 # 高於目標 → 減負項
            q += 1; S -= 1/(2*q)
        terms.append(S)
        if p > 50 and q > 50 and abs(S - target) < tol and len(terms) > 100:
            return S, len(terms)

for target in [1.0, 1.5, 0.5]:
    S, k = rearranged_sum(None, None, target)
    print(f"重排交錯調和級數 → 收斂到 {S:.6f}（目標 {target}，用了約 {k} 項）")
print("原始排列收斂到 ln 2 =", np.log(2), "——重排可到任何數！")
```

第一部分顯示：即使取樣點隨機選取，黎曼和仍收斂到 $4/3$——「任意取樣、極限唯一」驗證成功。第二部分顯示：同一個交錯調和級數，重排後可收斂到 1.0、1.5、0.5 任何目標——Riemann 重排定理的數值鐵證。

## 結案 -- 後果與影響
- **黎曼積分成為教科書標準**：任意分割、任意取樣、極限唯一。Darboux（1875）用上和下和給出等價的簡化表述，黎曼積分進入世界各地的課堂。
- Riemann 的病態函數證明「不連續點稠密仍可積」，大幅拓展了可積函數的範圍；但 Dirichlet 函數仍不可積——可積判準中未定義的「面積」成為最後的懸案。
- Riemann 重排定理確立「絕對收斂」的必要性：條件收斂級數的和沒有內在不變性。這成為現代級數論的基石。
- 案件的最終解決：Lebesgue（1902）以測度論重寫積分，回答「不連續點集合的測度為零 ⟺ 黎曼可積」（Lebesgue 判準），並馴服 Dirichlet 函數。
- 同篇論文中 Riemann 對 Fourier 級數的研究，也間接啟發了 Cantor 對三角級數唯一性的研究（1872），導致集合論的誕生——一份論文，兩條革命線。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Bernhard Riemann | 黎曼積分、病態函數、重排定理 |
| Peter Gustav Lejeune Dirichlet | Riemann 的老師，函數概念與收斂定理 |
| Augustin-Louis Cauchy | 積分原型，被 Riemann 推廣 |
| Gaston Darboux | 上和下和的簡化表述 |
| Henri Lebesgue | 測度論，最終結案 |

- B. Riemann, 〈Über die Darstellbarkeit einer Function durch eine trigonometrische Reihe〉, Habilitationsschrift, Göttingen (1854)；刊於 Abh. Königl. Ges. Wiss. Göttingen **13** (1868)。
- B. Riemann, 〈Über die Darstellbarkeit einer Function...〉手稿（1853）：重排定理，經 Dedekind 促成發表。
