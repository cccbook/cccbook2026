# 1985 - Boltzmann 機器

## 案件摘要

1985 年，Hinton 與 Sejnowski 提出 **Boltzmann 機器**：一個帶隱藏變數、以統計物理為骨架的隨機神經網路。網路的狀態分佈服從波茲曼定律：

$$P(s) = \frac{e^{-E(s)/T}}{\sum_{u} e^{-E(u)/T}}, \qquad E(s) = -\sum_{i<j} w_{ij}\, s_i s_j - \sum_i b_i s_i$$

這是第一次，一個神經網路模型能「學習」自己的機率分佈——不只是回憶（Hopfield），而是生成。它是 2002 年對比散度（Contrastive Divergence）與 2006 年深度信念網路的直系遠祖。

## 前因 -- 為什麼會有這個案子

- **1969-MinskyPapert批判.md** 判了單層感知器死刑：線性不可分問題（如 XOR）無解，AI 進入寒冬。學界急需要一個「多層、可學」的模型。
- **1982-Hopfield網路能量函數.md** 證明了能量函數 $E(s)$ 極小化對應網路收斂，讓物理學家相信神經網路可以用統計力學描述——但 Hopfield 網路只有記憶（吸引子），沒有學習，且對稱連接下無隱藏單元。
- Ackley、Hinton、Sejnowski 的動機：能否在 Hopfield 的能量框架上，加入**隱藏單元**與**隨機性**，讓網路透過調整權重去「擬合」外部資料的統計結構？三人的合作地點是羅徹斯特與約翰霍普金斯——認知科學與神經科學的交界，正是本書「智慧模型」的主題所在。
- 更廣的前驅線索：1890 年 William James 的聯想主義（見 **1890-WilliamJames聯想主義.md**）主張「心智是聯想的網路」——Boltzmann 機器把這個百年直覺第一次寫成可學習的數學。
- 當時的理論障礙：有隱藏單元時，看不出哪些權重該為資料負責——「歸因問題」懸而未決（1986 年反向傳播是另一條解法線索）。
- 統計物理的 Ising 模型與模擬退火（Metropolis, 1953；Kirkpatrick, 1983）提供了現成的數學工具箱。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：從確定到隨機——溫度 $T$ 的引入

Hopfield 網路每個神經元確定性地取 $\mathrm{sign}(\sum_j w_{ij} s_j)$，能量只能下降，容易卡在局部極小。Boltzmann 機器讓神經元以機率翻轉：

$$P(s_i = 1) = \frac{1}{1 + e^{-\Delta E_i / T}}$$

其中 $\Delta E_i$ 是翻轉 $s_i$ 帶來的能量變化。高溫時網路亂走（逃離局部極小），降溫後收斂到低能組態——這正是模擬退火。

### 第二條線索：學習法則——兩種「統計」的角力

網路在兩種模式下運行：**夾住（clamped）可見單元**（資料 $P_{\text{data}}$）與**自由運行**（模型 $P_{\text{model}}$）。學習法則驚人地簡單對稱：

$$\Delta w_{ij} = \eta \left( \langle s_i s_j \rangle_{\text{data}} - \langle s_i s_j \rangle_{\text{model}} \right)$$

| 項 | 統計意義 | 物理意義 |
|---|---|---|
| $+\langle s_i s_j \rangle_{\text{data}}$ | 資料中兩單元共同激活的頻率 | 推高權重，讓模型喜歡資料 |
| $-\langle s_i s_j \rangle_{\text{model}}$ | 模型自由幻想時的共現頻率 | 壓低權重，抑制幻覺 |

這條法則等價於極大化資料的對數概似 $\log P(v)$，其梯度恰是上式。推理至此清晰：**歸因問題被隨機共現統計解決**——隱藏單元與可見單元的相關性，自動分配了功勞。

### 第二條線索補遺：與 Hopfield 的關鍵差異

| | Hopfield 網路（1982） | Boltzmann 機器（1985） |
|---|---|---|
| 神經元更新 | 確定性 $\mathrm{sign}(\cdot)$ | 隨機性 $P(s_i=1)=\frac{1}{1+e^{-\Delta E_i/T}}$ |
| 隱藏單元 | 無 | 有（歸因問題的核心） |
| 能量走向 | 單調下降，卡局部極小 | 可上升（逃離局部極小） |
| 學習 | 權重寫死或 Hebb 式微調 | 機率分佈的極大概似 |
| 輸出性質 | 記憶（吸引子） | **生成（機率分佈）** |

偵探的判讀：從「回憶」到「生成」的一步之差，是本案件的本質——Boltzmann 機器不只是把 Hopfield 加溫，而是把網路從動力系統升格為**機率模型**。



隱藏單元不對應任何單一概念，而是多個隱藏單元的聯合狀態共同編碼一個模式。這是**分佈式表徵（distributed representation）**的最早實例：一個概念由許多神經元共同表示，一個神經元參與表示許多概念。XOR 這類線性不可分問題，在隱藏空間中被自動攤平成線性可分。

### 第三條線索補遺：兩個任務——回憶與完成

Boltzmann 機器同時是記憶與補全模型：

| 任務 | 操作 | 物理類比 |
|---|---|---|
| 模式記憶 | 夾住部分可見單元，自由單元收斂 | 彼此吸引的粒子聚成低能組態 |
| 模式補全 | 遮住影像一角，網路「幻想」出缺失部分 | 能量面把殘缺狀態拉向完整吸引子 |

推理的偵探視角：**權重 $w_{ij}$ 就是能量地形的地圖**——學習即雕刻地形，推論即地形上的滾動。這個「能量地形」意象日後滲透整個深度學習：損失曲面的局部極小、鞍點與平滑度，都是同一語言。

### 第四條線索：計算的代價

學習法則中 $\langle s_i s_j \rangle_{\text{model}}$ 需要馬可夫鏈蒙地卡羅跑到平衡，代價是 $O(\text{網路規模})$ 次迭代每一步——對大網路完全不可行。這個「瓶頸」正是下一個案件的伏筆：Hinton 二十年後用對比散度（只跑 1–2 步）破解了它。

## 結案 -- 後果與影響

- 確立了「能量模型 + 機率詮釋 + 隨機學習」三合一框架，成為生成式神經網路的起點。
- 「幻想（hallucination）」第一次成為術語：模型自由運行時生成的組態被稱為幻想——四十年後同一個詞成為 LLM 時代的中心議題。
- 分佈式表徵的理念直接催生了 1986 年反向傳播網路的表徵理論（見 **1986-反向傳播演算法.md**）。
- 學習法則的正負兩項，是 2002 年對比散度與 2014 年 GAN 對抗訓練的思想原型（對比散度保留正負兩項；GAN 則把「壓低模型統計」交給另一個網路判別器）。
- 2006 年深度信念網路（見 **2006-Hinton深度信念網路.md**）正是「多層受限波茲曼機器」，開啟深度學習時代。
- 侷限：訓練太慢、隱藏單元間的連接使採樣混亂——後來的受限波茲曼機器（RBM, Smolensky 1986 的和諧理論）乾脆砍掉隱藏單元之間的連接，只留跨層連接。
- 影像任務的延伸：1990 年代 RBM 被嘗試用於手寫與臉部影像，但規模有限；直到 2006 年 DBN 才證明多層堆疊可行（見 **2006-Hinton深度信念網路.md**）。
- 知識表示的旁支：Boltzmann 機器與同期的專家系統（見 **1965-DENDRAL專家系統.md**）代表兩種智能觀——知識由專家寫入，或由統計學出。本卷的結論是後者勝出。
- 伏筆：能量模型的路在深度學習爆發後暫時讓位給判別式模型，但 2019 年後又以 Energy-Based Models 之名復活（見 **2017-Transformer.md** 之後的生成模型譜系）。

## 關鍵人物與文獻

- **Geoffrey Hinton / Terrence Sejnowski**：Boltzmann 機器的共同提出者。
- Ackley, Hinton & Sejnowski, *A Learning Algorithm for Boltzmann Machines*, Cognitive Science, 1985。
- Sherrington & Kirkpatrick, Solvable Model of a Spin-Glass, 1975；Kirkpatrick et al., Optimization by Simulated Annealing, 1983（模擬退火）。
- Smolensky, *Information Processing in Dynamical Systems: Harmony Theory*, 1986（RBM 的前身）。
- James, *The Principles of Psychology*, 1890（聯想主義的百年直覺）。
- Hopfield, *Neural networks and physical systems with emergent collective computational abilities*, PNAS, 1982。
- Hinton, *Training Products of Experts by Minimizing Contrastive Divergence*, 2002（對比散度，遠祖的回聲）。
- 相關案件：**1982-Hopfield網路能量函數.md**、**1986-反向傳播演算法.md**、**2006-Hinton深度信念網路.md**、**1969-MinskyPapert批判.md**（見「科學與歷史/神經網路/」）

## 補充 -- 程式實作（python + numpy）

本案兩條核心公式——隨機翻轉 `P(sᵢ=1) = 1/(1+e^(−ΔEᵢ/T))` 與學習法則 `Δw = η(⟨ss⟩data − ⟨ss⟩model)`——最小可執行版本，見 `_code/1985-BoltzmannMachine.py`（已實測可跑）：

```python
# 1985 - Boltzmann 機器
# 公式: P(s_i=1) = 1/(1+exp(-ΔE_i/T)); Δw_ij = η(<s_i s_j>_data - <s_i s_j>_model)
import numpy as np


def sample_p(h):
    return 1.0 / (1.0 + np.exp(-h))


def gibbs_step(state, W, b, T):
    for i in np.random.permutation(len(state)):
        h = (W[i] @ state + b[i]) / T
        state[i] = 1 if np.random.rand() < sample_p(h) else -1
    return state


def cooccur(samples):
    return np.mean([np.outer(s, s) for s in samples], axis=0)


def main():
    rng = np.random.default_rng(0)
    np.random.seed(0)
    data = [np.array([1, 1, -1, -1]), np.array([-1, -1, 1, 1])] * 50
    N = 4
    W = np.zeros((N, N))
    b = np.zeros(N)
    eta, T = 0.1, 1.0
    for epoch in range(60):
        Cd = cooccur(data)                    # clamped (data) 統計
        fantasies = []
        for _ in range(50):
            s = rng.choice([-1, 1], size=N).astype(float)
            fantasies.append(gibbs_step(s, W, b, T).copy())
        Cm = cooccur(fantasies)               # free-running (model) 統計
        dW = eta * (Cd - Cm)                  # 核心: 資料共現推高, 幻想共現壓低
        dW[np.diag_indices(N)] = 0
        W += dW
    print("學到的 W (符號):\n", np.sign(W).astype(int))
    print("含義: (0,1) 與 (2,3) 內部正相關、兩群間負相關 = 記住兩個模式的共現結構")
    print("T=10 時 P(翻轉|h=1):", round(float(sample_p(-1 / 10)), 3), "(近隨機亂走)")
    print("T=0.1 時 P(翻轉|h=1):", round(float(sample_p(-1 / 0.1)), 5), "(近確定性=Hopfield)")


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/1985-BoltzmannMachine.py`，numpy 2.4.5）：

```
學到的 W (符號):
 [[ 0  1 -1 -1]
  [ 1  0 -1 -1]
  [-1 -1  0  1]
  [-1 -1  1  0]]
含義: (0,1) 與 (2,3) 內部正相關、兩群間負相關 = 記住兩個模式的共現結構
T=10 時 P(翻轉|h=1): 0.475 (近隨機亂走)
T=0.1 時 P(翻轉|h=1): 5e-05 (近確定性=Hopfield)
```

程式解說：`dW = η(Cd − Cm)` 即本文第二條線索的學習法則全文——資料中共現的單元對被推高權重，模型自由幻想中共現的被壓低，兩種統計角力至平衡時 `p_model ≈ p_data`，等價於極大化對數概似。學到的符號矩陣顯示網路確實刻出兩個模式的共現結構。末兩行演示溫度 `T` 的角色：高溫 `T=10` 翻轉機率近五成（逃離局部極小），低溫 `T=0.1` 機率近零（退化為確定性的 Hopfield）——模擬退火的精神全在這兩個數字裡。
