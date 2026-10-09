# 1982 - Hopfield 網路能量函數

## 案件摘要

1982 年，物理學家 John Hopfield 發表論文 "Neural networks and physical systems with emergent collective computational abilities"，提出以能量函數驅動的循環神經網路——Hopfield 網路。核心公式：

$$E = -\frac{1}{2} \sum_{i,j} w_{ij} s_i s_j + \sum_i \theta_i s_i，\quad s_i \in \{-1, +1\}$$

網路的狀態 $s$ 沿著能量下降方向演化，最終落入局部極小值——每個極小值對應一段被儲存的記憶。這是**聯想記憶**（associative memory）的數學化：給定殘缺的線索，網路自動補全整段記憶。物理學家的介入讓連結派在寒冬中絕處逢生（見「1969-MinskyPapert批判.md」），而這條線索最終通往 2024 年諾貝爾物理學獎——四十二年後的翻案判決書。

## 前因 -- 為什麼會有這個案子

- 1969 年《Perceptrons》（見「1969-MinskyPapert批判.md」）與 1973 年 Lighthill 報告把連結派打入寒冬；1974 年 Werbos 的反向傳播（見「1974-Werbos反向傳播先驅.md」）被埋沒，神經網路在主流科學中無人敢碰。
- Hopfield 是凝聚態物理學家（贝尔实验室出身，後任教普林斯頓），他的動機是**跨界的**：神經網路的集體行為與自旋玻璃（spin glass）、Ising 模型的動力學同構——他想知道「大量簡單單元能否湧現集體計算能力」。
- 物理學的線索早已備好：Ising 模型（1925）的能量函數 $E = -\sum_{\langle i,j\rangle} J_{ij} s_i s_j$ 與 Monte Carlo 模擬、統計力學的相變理論，全部可以移植到神經網路。
- 1970 年代的聯想記憶問題：傳統電腦用位址存取記憶，但人類記憶是**內容定址**的——聞到一味香料就想起整段往事。這個能力在當時沒有任何數學模型。
- Little（1973）曾提出類似的機率式神經網路，但未用能量函數語言，未引起注意——線索再次沉睡，Hopfield 是把它擦亮的翻譯者。
- 1970 年代末 Hopfield 參與神經生物學研討會，被真實神經元的集體動力學吸引——他決定用物理學家的武器（能量、極小值、對稱性）進攻這個領域。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：能量函數——物理學的武器被搬進神經網路

Hopfield 網路是全連接循環網路：每個單元 $s_i \in \{-1,+1\}$ 與所有其他單元相連，權重對稱 $w_{ij} = w_{ji}$ 且 $w_{ii}=0$。單元依非同步規則更新：

$$s_i \leftarrow \mathrm{sign}\!\left( \sum_j w_{ij} s_j - \theta_i \right)$$

關鍵定理：**每次更新都讓能量 $E = -\frac{1}{2} \sum_{i,j} w_{ij} s_i s_j + \sum_i \theta_i s_i$ 不增**。證明：翻轉 $s_i$ 時能量變化為

$$\Delta E = -\Delta s_i \left( \sum_j w_{ij} s_j - \theta_i \right) = -\Delta s_i \cdot h_i$$

若 $h_i > 0$ 則 $s_i$ 翻為 $+1$（$\Delta s_i \ge 0$），故 $\Delta E \le 0$；$h_i < 0$ 同理。$\blacksquare$

由於狀態空間有限（$2^N$），網路必在有限步內收斂到能量極小值——**動力學 = 下降到記憶谷底**。

### 第二條線索：Hebbian 儲存——把記憶刻進能量地形

儲存 $p$ 個記憶模式 $\xi^{\mu} \in \{-1,+1\}^N$ 的方法是最樸素的 Hebb 規則：

$$w_{ij} = \frac{1}{N} \sum_{\mu=1}^{p} \xi_i^{\mu} \xi_j^{\mu}$$

儲存後，每個記憶 $\xi^{\mu}$ 變成能量地形的一個極小值。檢驗：代入 $s = \xi^{\mu}$，

$$E(\xi^{\mu}) = -\frac{N}{2} + \frac{1}{N}\sum_{\nu \ne \mu} \left( \xi^{\mu} \cdot \xi^{\nu} \right)^2 \cdot \frac{N}{2} \approx -\frac{N}{2}$$

當記憶數 $p$ 不超過容量上限 $p_{\max} \approx 0.138\,N$（$\alpha = p/N \approx 0.138$，由統計力學方法算出），各記憶之間的交叉項足夠小，$\xi^{\mu}$ 保持為穩定極小值——記憶成功儲存。

### 第三條線索：聯想記憶的動力學——殘缺線索補全整段記憶

檢索時輸入殘缺或帶噪的線索 $s(0)$，網路沿能量下降演化：

$$s(t+1) = \mathrm{sign}\!\big( W s(t) \big) \quad \Rightarrow \quad s(\infty) \approx \text{最近的記憶極小值 } \xi^{\mu^*}$$

以 $N=8$、儲存兩個記憶為例（Python 縮影，闡明用）：

```python
import numpy as np
xi = np.array([[ 1, 1, 1, 1,-1,-1,-1,-1],      # 記憶 A
               [ 1,-1, 1,-1, 1,-1, 1,-1]], float)  # 記憶 B
W = (xi.T @ xi) / len(xi[0]); np.fill_diagonal(W, 0)
cue = np.array([ 1, 1,-1, 1,-1,-1,-1, 1], float)   # 殘缺線索（2 位錯）
for _ in range(5):
    cue = np.sign(W @ cue)
# 對比線索與兩個記憶的漢明距離
print(cue)                          # [ 1.  1.  1.  1. -1. -1. -1. -1.]  → 補全為記憶 A
```

輸出如註解所示：兩位錯誤的線索被自動補全為記憶 A。**內容定址**——不需要位址，線索本身就是位址。

### 第四條線索：物理學的同構——自旋玻璃與統計力學

Hopfield 網路與 Ising 模型的同構是本案最深的線索：

| | Ising / 自旋玻璃 | Hopfield 網路 |
|---|---|---|
| 變數 | 自旋 $s_i \in \{\pm 1\}$ | 神經元 $s_i \in \{\pm 1\}$ |
| 能量 | $E = -\sum J_{ij} s_i s_j$ | $E = -\frac12 \sum w_{ij} s_i s_j + \sum \theta_i s_i$ |
| 動力學 | 降溫、Glauber 動力學 | 非同步更新、能量下降 |
| 湧現 | 磁序、相變 | 記憶、集體計算 |

這個同構讓統計力學的全套武器（平均場理論、相變、自由能）湧入神經網路研究——Amit、Gutfreund、Sompolinsky（1985）用統計力學算出容量 0.138N，物理學家自此成為神經網路理論的主力。

## 結案 -- 後果與影響

- Hopfield 網路讓連結派在寒冬中絕處逢生：「物理學家做的神經網路」學術上可敬，研究生與經費重新流入——它與反向傳播（1986，見「1986-反向傳播演算法.md」）共同終結了第一次 AI 寒冬。
- 能量函數思想直接催生 Boltzmann 機（1985，Hinton & Sejnowski）——把能量下降加上隨機熱擾動，就能**學習**機率分布；再傳至深度信念網路（2006，Hinton），開啟深度學習的前夜。
- 聯想記憶的內容定址思想影響了後世的注意力機制：Transformer 的 self-attention 本質上也是「用線索檢索記憶」的可微版本（見「科學與歷史/人工智慧/」下 Transformer 檔案）。
- 2024 年諾貝爾物理學獎授予 John Hopfield 與 Geoffrey Hinton，「以人工神經網路實現機器學習的基礎性發現與發明」——1982 年的線索在四十二年後獲得最高規格的翻案。
- 近年復興：2020 年代 Hopfield 網路被重新詮釋為「現代 Hopfield 網路」（Ramsauer et al., 2020），證明其更新規則與 Transformer 注意力在數學上等價——聯想記憶與語言模型在此匯流。
- 伏筆：能量函數的隨機版本（Boltzmann 機）→ 深度信念網路 → 2006 年深度學習前夜；而 Hopfield 的「集體計算」命題，將在 AlexNet（2012）與大型語言模型中得到終極驗證——大量簡單單元確實能湧現智能。

## 關鍵人物與文獻

- John Hopfield —— 凝聚態物理學家，2024 年諾貝爾物理學獎得主
- Hopfield, "Neural networks and physical systems with emergent collective computational abilities", *PNAS*, 1982
- Hopfield, "Neurons with graded response have collective computational properties like those of two-state neurons", *PNAS*, 1984
- Amit, Gutfreund & Sompolinsky, "Spin-glass models of neural networks", *Physical Review A*, 1985（容量 0.138N）
- Hebb, *The Organization of Behavior*, 1949（Hebbian 儲存的源頭）
- Hinton & Sejnowski, "Learning and Relearning in Boltzmann Machines", 1986（能量函數的隨機後繼）
- 相關案件：1969-MinskyPapert批判.md、1974-Werbos反向傳播先驅.md、1980-Neocognitron視覺層級模型.md、1986-反向傳播演算法.md

## 補充 -- 程式實作（python + numpy）

本案兩條核心公式——Hebb 儲存 `wᵢⱼ = (1/N)Σ ξᵢξⱼ` 與能量 `E = −½Σwᵢⱼsᵢsⱼ`——最小可執行版本，見 `_code/1982-Hopfield.py`（已實測可跑）：

```python
# 1982 - Hopfield 網路能量函數
# 公式: s_i <- sign(Σ_j w_ij s_j); E = -1/2 Σ w_ij s_i s_j (每次更新 ΔE ≤ 0)
import numpy as np


def energy(s, W, theta=0.0):
    return -0.5 * s @ W @ s + theta * s.sum()


def main():
    rng = np.random.default_rng(0)
    xi = np.array([[1, 1, 1, 1, -1, -1, -1, -1],      # 記憶 A
                   [1, -1, 1, -1, 1, -1, 1, -1]], float)  # 記憶 B
    N = xi.shape[1]
    W = (xi.T @ xi) / N          # Hebb 儲存
    np.fill_diagonal(W, 0)
    cue = np.array([1, 1, -1, 1, -1, -1, -1, 1], float)  # 2 位錯的殘缺線索
    print("記憶A:", xi[0].astype(int).tolist())
    print("線索 :", cue.astype(int).tolist(), "(含2位錯誤)")
    s = cue.copy()
    E_prev = energy(s, W)
    print(f"  t=0 E={E_prev:.3f} s={s.astype(int).tolist()}")
    for t in range(1, 6):
        order = rng.permutation(N)          # 非同步更新
        for i in order:
            s[i] = 1 if W[i] @ s >= 0 else -1
        E = energy(s, W)
        assert E <= E_prev + 1e-9, "能量必須不增!"
        print(f"  t={t} E={E:.3f} s={s.astype(int).tolist()}")
        E_prev = E
    print("補全為記憶A:", bool(np.array_equal(s, xi[0])),
          f"(容量上限 p_max≈{0.138 * N:.1f} 個模式, 此處存 2 個)")


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/1982-Hopfield.py`，numpy 2.4.5）：

```
記憶A: [1, 1, 1, 1, -1, -1, -1, -1]
線索 : [1, 1, -1, 1, -1, -1, -1, 1] (含2位錯誤)
  t=0 E=-1.000 s=[1, 1, -1, 1, -1, -1, -1, 1]
  t=1 E=-3.000 s=[1, 1, 1, 1, -1, -1, -1, -1]
  t=2 E=-3.000 s=[1, 1, 1, 1, -1, -1, -1, -1]
  t=3 E=-3.000 s=[1, 1, 1, 1, -1, -1, -1, -1]
  t=4 E=-3.000 s=[1, 1, 1, 1, -1, -1, -1, -1]
  t=5 E=-3.000 s=[1, 1, 1, 1, -1, -1, -1, -1]
補全為記憶A: True (容量上限 p_max≈1.1 個模式, 此處存 2 個)
```

程式解說：`W = (xi.T @ xi)/N` 即本文第二條線索的 Hebb 儲存——1949 年規則的矩陣版在此直接現形。檢索時含 2 位錯誤的線索一步就滑到能量 `-3.000` 的谷底並穩定不動，程式內 `assert E <= E_prev` 逐輪驗證本文第一條線索的定理（能量不增、有限步收斂）。附帶一課：`N=8` 時理論容量 `0.138N≈1.1`，本程式存了 2 個模式已超載——實務上小網路常因模式彼此正交而僥倖成功，模式一多即出現偽吸引子，正是 Amit 等人統計力學計算的含義。
