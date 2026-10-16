# 2006 - Hinton 深度信念網路

## 案件摘要

2006 年，Hinton、Osindero 與 Teh 發表**深度信念網路（DBN）**：用逐層無監督預訓練（greedy layer-wise pre-training）馴服深網路——每一層是一個受限波茲曼機器（RBM），用對比散度快速學習：

$$\Delta w_{ij} = \eta \left( \langle v_i h_j \rangle_{\text{data}} - \langle v_i h_j \rangle_{1} \right)$$

一句話：**一層一層地學，先學結構再調整**。這是「deep learning」一詞誕生的時刻——深度網路第一次被證明**可訓練**，冬天的最後一道冰牆裂開了。

## 前因 -- 為什麼會有這個案子

- **1986-反向傳播演算法.md** 的陰影：梯度逐層乘上 $\sigma'$ 與權重，深於三、四層就指數消失——二十 年來「深即不可訓練」是學界共識，神經網路在 1990 年代末被 SVM 壓到邊緣。
- **1985-Boltzmann機器.md** 的遺產：能量模型 + 隨機學習理論上優美，但 $\langle s_i s_j \rangle_{\text{model}}$ 需要蒙地卡羅跑到平衡，大網路完全不可行——**學習的代價是瓶頸**。
- 2002 年 Hinton 的對比散度（CD-1）：只跑 1 步蒙地卡羅就估梯度——快幾百倍，雖然是有偏估計，實務上卻異常好用。**瓶頸被破解**。
- Hinton 的動機：他在神經網路寒冬中堅守三十年（見「科學與歷史/神經網路/」），相信大腦就是深層分佈式表徵；他要證明深度不是錯誤，只是**還沒找到正確的訓練法**。他常以「大腦視覺皮層有十幾層」作為反證：如果深不可訓練，大自然為何造出深度？
- 1990 年代的局部極小值迷思：大家以為深網路訓不動是因為卡在壞的局部極小——2006 年的真相是：問題主要出在**初始化**，預訓練提供了好的起點。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：RBM——砍掉側連的 Boltzmann 機器

受限波茲曼機器把 Boltzmann 機器的層內連接全部砍掉（可見層之間、隱藏層之間互不相連），只留跨層連接：

$$P(v, h) = \frac{e^{-E(v,h)}}{Z}, \qquad E(v,h) = -\sum_i b_i v_i - \sum_j c_j h_j - \sum_{i,j} v_i w_{ij} h_j$$

結構上的對稱性使條件機率可以**一次解析算出**（不用逐步採樣）：

$$P(h_j = 1 \mid v) = \sigma\left(c_j + \sum_i v_i w_{ij}\right), \qquad P(v_i = 1 \mid h) = \sigma\left(b_i + \sum_j h_j w_{ij}\right)$$

層內無連接 = 採樣可並行 = **GPU 友善**——這個工程性質在六年後的 AlexNet 上大放異彩。

### 第二條線索：對比散度——只跑一步的蒙地卡羅

完整概似梯度需要模型分佈的期望：

$$\frac{\partial \log P(v)}{\partial w_{ij}} = \langle v_i h_j \rangle_{\text{data}} - \langle v_i h_j \rangle_{\text{model}}$$

CD-1 的賭注：第二項不用平衡分佈，只用「資料 → 隱藏 → 一步重建」估計：

| 方法 | 估計 $\langle v_i h_j \rangle_{\text{model}}$ | 代價 |
|---|---|---|
| 精確 / 長鏈 MCMC | 跑到馬可夫鏈平衡 | $O(\text{網路規模})$，不可行 |
| **CD-1** | 資料出發只走 1 步 | 幾乎免費，有偏但方向正確 |

直覺：學習早期模型分佈與資料分佈差距大，一步重建已足以指出「往哪裡調」；隨著模型變好，偏差自然縮小。

### 第二條線索補遺：RBM 的兩種「面貌」

| 面貌 | 用法 | 意義 |
|---|---|---|
| 生成模型 | 從隱藏採樣重建可見 | 學出 $P(v)$，可補全與生成 |
| **特徵偵測器** | 從可見推隱藏活化 | DBN 逐層堆疊時的角色 |

偵探的判讀：同一組權重 $w_{ij}$ 有兩個方向——「由上看下」是識別，「由下看上」是生成。這個對稱性是 RBM 最美的性質，也是 DBN 能逐層堆疊的原因：上一層的「識別輸出」就是下一層的「資料」。

DBN 的訓練是貪心逐層：第 1 層 RBM 用資料學好 → 凍結，其隱藏活化當作第 2 層 RBM 的資料 → 依此類推；最後一層加上標籤，用反向傳播**微調**（fine-tune）整個網路：

$$\text{資料} \xrightarrow{\text{RBM}_1} h^{(1)} \xrightarrow{\text{RBM}_2} h^{(2)} \xrightarrow{\text{RBM}_3} h^{(3)} \xrightarrow{\text{微調}} \text{輸出}$$

每一層都在做**無監督的特徵學習**：底層學邊緣與筆畫，中層學部件，頂層學物件概念——層級表徵第一次在深網路中自動湧現。2000 年代中期可視化第一層 RBM 的權重：濾波器自動長成邊緣與筆畫偵測器——與 **1989-LeCunCNN手寫辨識.md** 中 CNN 第一層的所學驚人地相似，殊途同歸。MNIST 上的實證：同樣架構，隨機初始化的深網錯誤率 $\sim 1.6\%$ 以上且常不收斂，逐層預訓練 + 微調壓到 $\sim 1.2\%$ 以下，且**深層穩定可訓練**——「深即不可訓練」被證偽。

### 第三條線索補遺：DBN 與 RNN/MLP 的對照

| | 淺層 MLP（隨機初始化） | 深層 DBN（逐層預訓練） |
|---|---|---|
| 初始權重 | 隨機，靠近輸入的「盲區」 | 每層已對齊資料統計 |
| 梯度流動 | 深層時消失 | 微調階段已接近好的盆地 |
| MNIST 錯誤率 | $\gtrsim 1.6\%$，常不收斂 | $\lesssim 1.2\%$，穩定 |
| 產出表徵 | 黑箱 | 層級可視化（邊緣→部件→概念） |

偵探的判讀：預訓練的本質不是「學到知識」，而是**初始化的智慧**——把網路放進損失曲面上正確的盆地，微調只是沿著盆底滑下去。這個洞見日後被 ReLU + 初始化理論（2010 Glorot、2015 He）工程化，預訓練退居選配。

### 第四條線索：命名的誕生與隨後的誤解

- 2006 年論文用了「deep belief nets」一詞；Hinton 團隊刻意用「**deep learning**」取代被污名化的「neural networks」——一個新的品牌，開啟一個新的時代。
- 2007 年「課程學習（curriculum learning）」的提出（Bengio 等與 Hinton 合著）深化了同一哲學：**由易到難、由淺到深的學習順序本身就是一種偏置**——正如兒童先學簡單概念。
- 誤解：大家以為是「逐層預訓練」本身神奇；2010 年後的真相是——**ReLU、良好的初始化、大資料**之後，預訓練變得不再必要（AlexNet 只用監督學習端對端）。但 2006 年的歷史角色無可取代：它證明了深度的可行性，把社群帶回牌桌。

## 結案 -- 後果與影響

- 「深度學習」正式誕生：2006–2012 年間，逐層預訓練 + 微調是訓練深網的標準流程，語音辨識（2009 年 Hinton 團隊的 DNN 聲學模型）率先獲利。
- 對比散度使 RBM/DBN 成為 2006–2011 年最熱門的研究主題，Hinton 2018 年圖靈獎的根基之一。
- 無監督預訓練的理念日後演化為**自監督學習**：word2vec、BERT 的遮罩預訓練、GPT 的下一詞預測——「先學結構再調整」的哲學在 **2017-Transformer.md** 之後以更大規模復活。
- 能量模型譜系延續：2014 年 GAN、2019 年 Energy-Based Models，皆是 Boltzmann 機器的遠房後裔。
- 伏筆：DBN 證明「深度可訓練」，但真正引爆還缺兩塊拼圖——**大資料**（**2009-ImageNet資料集.md**）與 **GPU 算力**。兩者會合於 **2012-AlexNet影像革命.md**，深度學習革命正式開場。

## 關鍵人物與文獻

- **Geoffrey Hinton / Simon Osindero / Yee-Whye Teh**：DBN 與逐層預訓練的提出者。
- Hinton, Osindero & Teh, *A Fast Learning Algorithm for Deep Belief Nets*, Neural Computation, 2006。
- Hinton, *Training Products of Experts by Minimizing Contrastive Divergence*, Neural Computation, 2002。
- Smolensky, *Information Processing in Dynamical Systems: Harmony Theory*, 1986（RBM 的前身）。
- Ackley, Hinton & Sejnowski, *A Learning Algorithm for Boltzmann Machines*, 1985。
- Mohamed, Dahl & Hinton, *Deep Belief Networks for Phone Recognition*, 2009（語音應用）。
- 相關案件：**1985-Boltzmann機器.md**、**1986-反向傳播演算法.md**、**2009-ImageNet資料集.md**、**2012-AlexNet影像革命.md**、**2017-Transformer.md**

## 補充 -- 程式實作（python + numpy）

本案 RBM 與 CD-1（`Δw = η(⟨vh⟩data − ⟨vh⟩₁)`）及貪婪逐層堆疊的最小可執行版本，見 `_code/2006-DBN.py`（已實測可跑）：

```python
# 2006 - 深度信念網路 DBN: RBM + 對比散度 CD-1 + 貪婪逐層堆疊
import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def train_rbm(X, nh, lr=0.5, epochs=30, seed=0, binary=True):
    """CD-1 訓練單層 RBM, 回傳 (W, b, c, 重建誤差)."""
    rng = np.random.default_rng(seed)
    nv = X.shape[1]
    W = rng.normal(0, 0.1, (nv, nh))
    b, c = np.zeros(nv), np.zeros(nh)
    for _ in range(epochs):
        h_prob = sigmoid(X @ W + c)                       # <vh>_data
        h = (rng.random(h_prob.shape) < h_prob).astype(float)
        v1_prob = sigmoid(h @ W.T + b)                    # Gibbs 一步 (CD-1)
        v1 = (rng.random(v1_prob.shape) < v1_prob).astype(float)
        h1_prob = sigmoid(v1 @ W + c)                     # <vh>_1
        W += lr * (X.T @ h_prob - v1.T @ h1_prob) / len(X)
        b += lr * (X - v1).mean(0)
        c += lr * (h_prob - h1_prob).mean(0)
    recon_p = sigmoid(sigmoid(X @ W + c) @ W.T + b)
    recon = (recon_p > 0.5).astype(float) if binary else recon_p
    return W, b, c, float(((recon - X) ** 2).mean())


def main():
    rng = np.random.default_rng(0)
    horiz = np.array([1, 1, 1, 0, 0, 0])
    vert = np.array([0, 0, 0, 1, 1, 1])
    X = np.array([(horiz if i % 2 == 0 else vert) ^ (rng.random(6) < 0.1)
                  for i in range(400)]).astype(float)
    W1, b1, c1, err1 = train_rbm(X, nh=4, seed=1)
    print(f"第1層 RBM(6->4): 重建誤差={err1:.3f} (隨機猜≈0.5)")
    print("學到的特徵 (W每列≈橫條/直條偵測器):\n", np.round(W1, 1))
    H1 = sigmoid(X @ W1 + c1)          # 第1層隱藏表徵當新資料 -- 貪婪逐層
    W2, b2, c2, err2 = train_rbm(H1, nh=2, seed=2, binary=False)
    print(f"第2層 RBM(4->2): 重建誤差={err2:.3f} (在特徵空間再壓縮)")
    H2 = sigmoid(H1 @ W2 + c2)
    d_in = np.abs(H2[0::2] - H2[0]).mean() + np.abs(H2[1::2] - H2[1]).mean()
    d_out = np.abs(H2[0::2].mean(0) - H2[1::2].mean(0)).mean()
    print(f"頂層表徵: 類內散佈={d_in:.3f}, 類間距離={d_out:.3f} "
          f"({'分開 -- 深層學到類別' if d_out > d_in else '未分開'})")
    print("結論: 逐層預訓練把深網初值放在好位置 -- 2006 年深網第一次訓得動")


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/2006-DBN.py`，numpy 2.4.5）：

```
第1層 RBM(6->4): 重建誤差=0.108 (隨機猜≈0.5)
學到的特徵 (W每列≈橫條/直條偵測器):
 [[ 0.4  0.4 -0.2 -0.5]
 [ 0.4  0.4 -0.2 -0.4]
 [ 0.4  0.4 -0.2 -0.4]
 [-0.4 -0.4  0.2  0.5]
 [-0.4 -0.4  0.1  0.5]
 [-0.4 -0.4  0.2  0.5]]
第2層 RBM(4->2): 重建誤差=0.047 (在特徵空間再壓縮)
頂層表徵: 類內散佈=0.007, 類間距離=0.016 (分開 -- 深層學到類別)
結論: 逐層預訓練把深網初值放在好位置 -- 2006 年深網第一次訓得動
```

程式解說：`train_rbm` 即本文第二條線索的 CD-1 全文——資料分布的共現 `X.T@h_prob` 推高權重，只跑一步 Gibbs 的重建共現 `v1.T@h1_prob` 壓低權重；跑一步而非跑到收斂，正是「對比散度」省算力的偷天換日。第 1 層權重矩陣肉眼可讀：前兩列認橫條、後兩列認直條（正負號即是）。第 2 層把第 1 層的隱藏機率當新資料，頂層 2 維表徵類間距離已超類內散佈——深層「看到」了類別。此即 2006 年的歷史意義：深網第一次不靠標籤就找到好初值，梯度消失的陰影（見 **1986-反向傳播演算法.md**）首次被驅散。
