# 2001 - Breiman 隨機森林（Random Forests）

## 案件摘要
2001 年 Leo Breiman 發表《Random Forests》，將 bagging、隨機特徵子集與 CART 決策樹組合成一個幾乎不需要調參、天然抗過擬合的集成學習演算法。這同時也是他宣示「演算法模型文化」的代表作：不問資料背後的機制，只求預測準確。

## 前因 -- 為什麼會有這個案子
- **CART（1984）**：Breiman 與 Friedman 等人提出的二元決策樹，用 Gini 不純度或變異數遞迴切分，靈活但「不穩定」——資料稍微變動，樹的結構就大幅改變。不穩定通常是缺點，但 Breiman 反過來想：不穩定正是「平均多棵樹能變準」的前提。
- **Bagging（1996）**：Breiman 對 bootstrap 樣本各建一個模型再平均，證明對不穩定模型特別有效，方差下降 $\sigma^2/\rho$ 的精神（$\rho$ 為樹間相關性）成為隨機森林的理論伏筆：**光降低方差不夠，還要降低樹之間的相關性 $\rho$**。
- **Random Subspace Method（Ho, 1998）**：Tin Kam Ho 在特徵維度上做隨機（每棵樹只看隨機抽出的特徵子集），直接壓低樹間相關。Breiman 吸收了這條線索，將「樣本隨機」與「特徵隨機」合而為一。

## 線索與推理 -- 數學式、程式、理論

### 雙重隨機性
對 $b = 1, \dots, B$：
1. 從訓練集 $D$ 以有放回抽樣（bootstrap）取出 $D_b$；
2. 在每個節點切分時，不掃描全部 $p$ 個特徵，而是隨機抽 $m$ 個候選特徵（分類建議 $m \approx \sqrt{p}$，迴歸常用 $m \approx p/3$）；
3. 在 $D_b$ 上用最佳切分建一棵 CART 樹 $T_b$。

分類任務的預測為多數決投票：

$$
\hat{y}(x) = \text{majority}\big(\{T_b(x)\}_{b=1}^{B}\big)
$$

迴歸任務則取平均 $\hat{y}(x) = \frac{1}{B}\sum_b T_b(x)$。

### 為什麼這樣會準（Breiman 的泛化界）
Breiman 以「強度（strength）$s$ 與相關性 $\bar\rho$」給出泛化誤差上界：

$$
PE \le \frac{\bar\rho\,(1 - s^2)}{s^2}
$$

推理鏈：bagging 降低方差、Ho 的特徵隨機降低 $\bar\rho$、單棵深樹低偏差高強度——三者相加，誤差自然下降。這是「均值不穩定學習器 + 去相關」的偵探式答案。

### Out-of-Bag（OOB）誤差
每棵樹 $T_b$ 建構時約有 $1 - e^{-1} \approx 36.8\%$ 的樣本未被抽到（OOB 樣本）。對每個樣本 $i$，只用「沒看過 $i$ 的那些樹」投票：

$$
\hat{y}^{\text{oob}}(i) = \text{majority}\{T_b(x_i) : i \notin D_b\}, \qquad
\widehat{err}^{\text{oob}} = \frac{1}{n}\sum_i \mathbb{1}\{\hat{y}^{\text{oob}}(i) \ne y_i\}
$$

OOB 誤差是免費的交叉驗證（理論上等價於 leave-one-out 的 bootstrap 估計），不需要另外切驗證集。

### 特徵重要性
- **Gini importance（MDI）**：累加特徵在所有樹中參與切分所帶來的不純度下降

$$
\text{Imp}(X_j) = \frac{1}{B}\sum_{b=1}^{B}\sum_{t \in T_b} \Delta I_{jt}(t)\,\mathbb{1}\{\text{split at } t \text{ uses } X_j\}
$$

- **Permutation importance（MDI，Breiman 亦提出）**：隨機打亂第 $j$ 個特徵，看 OOB 誤差上升多少：

$$
\text{PI}(X_j) = \widehat{err}^{\text{oob}}_{\text{perm}(X_j)} - \widehat{err}^{\text{oob}}
$$

打亂後誤差升越多，代表該特徵越重要——這是「模型無關」的模型化偵探指紋鑑定。

### Python（sklearn）實作

```python
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
import numpy as np

X, y = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42)

rf = RandomForestClassifier(
    n_estimators=500,     # B：樹的數量
    max_features="sqrt",  # m ≈ √p：節點隨機特徵子集
    oob_score=True,       # OOB 誤差估計
    n_jobs=-1,
    random_state=42,
)
rf.fit(Xtr, ytr)

print(f"OOB accuracy: {rf.oob_score_:.4f}")          # 免費的驗證
print(f"Test accuracy: {rf.score(Xte, yte):.4f}")    # 投票後的預測力

# Gini importance（MDI）
gini_imp = rf.feature_importances_
names = load_breast_cancer.feature_names
top = np.argsort(gini_imp)[::-1][:5]
print("Gini importance Top-5:")
for i in top:
    print(f"  {names[i]:<25} {gini_imp[i]:.4f}")

# Permutation importance（基於測試集）
perm = permutation_importance(rf, Xte, yte, n_repeats=10, random_state=42)
top2 = np.argsort(perm.importances_mean)[::-1][:5]
print("Permutation importance Top-5:")
for i in top2:
    print(f"  {names[i]:<25} {perm.importances_mean[i]:.4f}")
```

## 結案 -- 後果與影響
- **兩種文化（Breiman, 2001《Statistical Modeling: The Two Cultures》）**：同一年，Breiman 宣告統計界存在兩種文化——「**資料模型文化**」（假設 $y = f(\mathbf{x}, \boldsymbol\beta) + \epsilon$，如線性/邏輯迴歸，追求可解釋的機制）與「**演算法模型文化**」（視 $f$ 為黑箱，如隨機森林、神經網路，只求預測準確）。他主張演算法文化才是處理高維複雜資料的正道，這篇文章引發統計與機器學習兩界長達二十年的路線論戰。
- **實用上的勝利**：隨機森林「開箱即準、免調參、有 OOB、有重要性」，成為 2010 年代表格資料（tabular data）的預設強力基線。
- **Kaggle 時代與梯度提升譜系**：Friedman 的梯度提升（2001 年前後）加上隨機森林的「行隨機 + 列隨機」思想，催生 XGBoost（2014/2016）、LightGBM（2017）、CatBoost（2018），長期霸佔 Kaggle 表格賽道；Breiman 的樹系血統是這整個譜系的祖先。隨機森林至今仍是 sklearn 中最常用的分類器之一，也是深度學習時代表格資料上 tree-based 模型依然強勢的歷史起點。

## 關鍵人物與文獻
- **Leo Breiman**（1928–2005）：UC Berkeley 統計教授，CART、bagging、隨機森林的作者，兩種文化論戰的發動者。
- **Tin Kam Ho**：Bell Labs，random subspace method（1998）。
- Breiman, L. (2001). *Random Forests*. Machine Learning, 45(1), 5–32.
- Breiman, L. (2001). *Statistical Modeling: The Two Cultures*. Statistical Science, 16(3), 199–231.
- Breiman, L. et al. (1984). *Classification and Regression Trees*. Wadsworth.
- Breiman, L. (1996). *Bagging Predictors*. Machine Learning, 24(2), 123–140.
- Ho, T. K. (1998). *The Random Subspace Method for Constructing Decision Forests*. IEEE TPAMI.
