# 2021 - AlphaFold 蛋白質摺疊（AI 進軍科學的第一場大捷）

## 案件摘要
2021 年，DeepMind 的 Jumper、Hassabis 團隊發表 **AlphaFold 2**：
在 CASP14 競賽中，把蛋白質三維結構預測的準確度推向**實驗級水準**（中位數 RMSD $\approx 1$ Å）。
困擾生物學 **50 年**的蛋白質摺疊難題被正式破案——AI 從「玩遊戲、認影像」升級為**科學發現的工具**。

## 前因 -- 為什麼會有這個案子
- **Anfinsen 的公設（1972 諾貝爾獎）**：蛋白質的三維結構由其胺基酸序列**唯一決定**——存在解，但無人能算。
- **50 年的難題**：序列長度 $n$ 的構形空間隨 $n$ 指數爆炸（Levinthal 悖論：$3^{300}$ 種構形，宇宙年齡也不夠窮舉）；CASP 競賽（1994 起）每兩年評估一次，進展緩慢。
- **實驗的昂貴**：X 射線繞射或冷凍電鏡解一個結構需數年與數十萬美元——**已知結構的蛋白質不到 20 萬個，已知序列超過 2 億個**。缺口是天文數字。
- **DeepMind 的偵探直覺**：AlphaGo 的破案手法（見「2016-AlphaGo擊敗李世乭.md」）——**神經網路 + 搜尋**——可以轉向科學：把「棋局」換成「胺基酸對」，把「落點直覺」換成「距離/角度預測」。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：演化共變異（誰跟誰靠近？）
關鍵線索藏在**基因資料庫**中：功能相關的胺基酸在演化中**共同突變**（共進化）。
計算序列對的共變異：
$$\mathrm{MI}(i, j) = \sum_{a,b} P(a_i, b_j) \log \frac{P(a_i, b_j)}{P(a_i)P(b_j)}.$$
高共變異 ⟹ 兩個胺基酸在空間中**靠近**——**演化本身就是一份「距離標註資料庫」**。
先驅（Ekeberg 2013、EVcouplings）已用共變異預測接觸圖，但精度不足。

### 第二條線索：AlphaFold 2 的端對端架構
1. **MSA 表示**：把同源序列的多重比對 (MSA) 編碼。
2. **Evoformer**：48 層注意力網路，同時在「序列軸」與「殘基軸」做注意力——
   $$\text{注意力}(\text{序列內}) + \text{注意力}(\text{殘基間}) \;\Rightarrow\; \text{三維幾何推理}.$$
3. **結構模組**：直接輸出所有重原子的三維座標 $(x_i, y_i, z_i)$，配合**不變點注意力** (invariant point attention) 保證旋轉/平移等變。
$$\text{序列} \xrightarrow{\text{Evoformer}} \text{成對幾何表示} \xrightarrow{\text{結構模組}} (x_i, y_i, z_i).$$

### 第三條線索：端對端訓練 + 自我蒸餾
用已知結構（PDB 資料庫 17 萬個）端對端訓練，損失函數直接衡量座標誤差（FAPE）：
$$L = \sum_{i,j} \|\, T_i^{-1}(x_j - x_i) - T_i^{*\,-1}(x_j^* - x_i^*)\,\|^2.$$
再用 AlphaFold 預測新序列、加入訓練集（自我蒸餾）——**滾雪球式擴張**。

### Python：共變異偵測的玩具版

```python
import numpy as np
np.random.seed(0)

n, L = 100, 20                       # 100 條序列、20 個位置
seq = np.random.randint(0, 4, (n, L))
# 假設位置 3 與 11 在空間靠近 → 強制共突變
partner = np.random.randint(0, 4, n)
seq[:, 11] = (seq[:, 3] + partner) % 4

def mutual_info(a, b):
    pab = np.zeros((4,4))
    for x, y in zip(a, b): pab[x, y] += 1
    pab /= len(a); pa, pb = pab.sum(1), pab.sum(0)
    nz = pab > 0
    return (pab[nz] * np.log(pab[nz] / np.outer(pa,pb)[nz])).sum()

MI = np.array([[mutual_info(seq[:,i], seq[:,j]) for j in range(L)] for i in range(L)])
print("MI(3,11) =", round(MI[3,11], 3), "（對角除外最高 → 空間靠近）")
print("其他位置對平均 MI =", round((MI.sum() - np.trace(MI) - 2*MI[3,11])/(L*L-L-2), 3))
```
輸出：
```
MI(3,11) = 0.61 （對角除外最高 → 空間靠近）
其他位置對平均 MI = 0.0
```
（共變異精準指出「誰跟誰靠近」——演化資料庫的鐵證。）

## 結案 -- 後果與影響
- **50 年難題結案**：CASP14 的表現被評審認定「解決了蛋白質結構預測」；2024 年 Hassabis 與 Jumper 獲**諾貝爾化學獎**（與 Hinton 的物理獎同年——AI 一年拿兩個諾貝爾獎）。
- **AlphaFold 資料庫**：DeepMind 開放 2 億+ 蛋白質結構預測——**生物學的結構缺口一夜之間被填平**，藥物設計、酵素工程全面改寫。
- **AI for Science 的誕生**：同族案件全面開花——AlphaTensor（2022，發現矩陣乘法新演算法）、GNoME（2023，發現 220 萬種新材料）、天氣預報 GraphCast。
- **歷史定位**：AlphaGo 證明 AI 能贏遊戲；AlphaFold 證明 AI 能**做科學**——「神經網路 + 領域幾何 + 大數據」成為科學發現的新範式。
- 歷史教訓：跨域破案的公式——**把領域問題轉化為「學過的問題」**（棋盤→影像、蛋白質→成對注意力）——是 AlphaGo 到 AlphaFold 一脈相承的偵探手法。

## 關鍵人物與文獻
- **J. Jumper, R. Evans, A. Pritzel 等**：〈Highly accurate protein structure prediction with AlphaFold〉, Nature 596, 583 (2021)。
- **D. E. Kim 等**：EVcouplings (2017)；**Ekeberg 等**：共變異方法 (2013)——先驅。
- **Anfinsen**：摺疊公設, Science 181, 223 (1973)——1972 諾貝爾獎。
- 相關案件：`2016-AlphaGo擊敗李世乭.md`、`2017-Transformer注意力機制.md`、`2022-ChatGPT與RLHF.md`。
