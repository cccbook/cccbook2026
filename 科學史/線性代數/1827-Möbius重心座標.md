# 1827 — Möbius 重心座標

## 案件摘要
1827 年，August Ferdinand Möbius 出版《Der barycentrische Calcul》（重心演算），發明了一套以「重量」為線索的幾何代數：平面上任一點都可以表示為三個頂點的加權組合，權重之和為一。這套「重心座標」讓幾何關係第一次可以用純粹的係數運算表達，是向量空間、仿射幾何與 Grassmann 外代數的直接前驅——幾何被「代數化」的第一樁正式案件。

## 前因 -- 為什麼會有這個案子
- **Leibniz 的幾何代數夢想**：1679 年 Leibniz 在寫給 Huygens 的信中抱怨，笛卡兒座標太笨拙——處理幾何位置關係時要繞遠路。他夢想一種「位置的字元」（characteristica geometrica），能直接對「點的相對位置」做代數運算。這個夢想沉睡了一百五十年。
- **力學的重心概念**：Archimedes 以來，「重心」就是力學的熟客——若干質點的合力作用點。若質點 $(m_i, P_i)$ 的重心為 $G$，則 $G$ 由力矩平衡決定。力學已經暗中使用了「點的加權組合」，卻沒有人把它提煉成幾何語言。
- **Lagrange 的解析力學**：1788 年 Lagrange 在《Mécanique analytique》中處理重心時，已寫出加權平均形式的公式，但只當作計算技巧，未視為新的幾何架構。
- Möbius 在萊比錫天文台工作，長年做球面天文計算，深感座標計算的繁瑣。他問：能否有一套座標，讓幾何的「位置」關係直接現形？

## 線索與推理 -- 數學式、程式、理論

### 線索一：重心座標的定義
Möbius 的核心想法：在三角形 $ABC$ 中，給每一頂點掛上一個「重量」$\alpha, \beta, \gamma$，其重心為 $P$。Möbius 規定重量可以為負、可以任意縮放，並以**重量比例**定義 $P$ 的座標。現代形式為：若

$$P = \frac{\alpha A + \beta B + \gamma C}{\alpha + \beta + \gamma}, \qquad \alpha + \beta + \gamma \neq 0$$

則 $(\alpha : \beta : \gamma)$ 稱為 $P$ 對三角形 $ABC$ 的**重心座標**（barycentric coordinates）。注意這是**齊次座標**（比例才有意義）——這正是後來射影幾何齊次座標的雛形。

### 線索二：點的線性組合——幾何的代數化
Möbius 發現驚人的規則：判斷幾何關係，只需要係數運算。

- **三點共線**：$A, B, C$ 共線 $\iff$ 存在不全為零的係數使 $\alpha A + \beta B + \gamma C = 0$ 且 $\alpha + \beta + \gamma = 0$。
- **四點共面**：$P_1, \dots, P_4$ 共面 $\iff$ 存在 $\sum c_i = 0$、$\sum c_i P_i = 0$ 的非平凡解。

這就是把 Leibniz 的夢想付諸實現：**位置關係變成線性方程**。「點可以加權相加」在當年是駭人聽聞的——點不是數，怎能相加？但 Möbius 用力學的重量概念賦予它意義，現在我們知道這就是**仿射組合**：係數和為一的線性組合。

### 線索三：仿射變換與座標不變性
Möbius 證明：在任何**仿射變換**（平移、旋轉、縮放、剪切）$T$ 之下，

$$T(P) = \frac{\alpha T(A) + \beta T(B) + \gamma T(C)}{\alpha + \beta + \gamma}$$

即重心座標在仿射變換下**不變**。這意味著重心座標抓住的是幾何中「與度量無關、只與平行與比例有關」的部分——正是後來 Erlangen 綱領意義下的**仿射幾何**的內在不變量。Möbius 還用它重新證明了 Ceva、Menelaus 定理：這些古典幾何難題，在重心座標下變成一行係數等式。

### 程式碼範例：numpy 實作重心座標與三角形內插
```python
import numpy as np

A = np.array([0.0, 0.0])
B = np.array([4.0, 0.0])
C = np.array([1.0, 3.0])

def barycentric(P, A, B, C):
    """將點 P 分解為 A,B,C 的仿射組合：P = a*A + b*B + c*C, a+b+c=1"""
    M = np.column_stack([A - C, B - C])
    a, b = np.linalg.solve(M, P - C)
    c = 1 - a - b
    return np.array([a, b, c])

P = np.array([1.5, 1.0])
lam = barycentric(P, A, B, C)
print("重心座標 (a,b,c) =", lam)          # 和為 1
print("還原 P =", lam @ np.array([A, B, C]))

# 重心（centroid）= 三頂點等權：α:β:γ = 1:1:1
G = (np.array([1, 1, 1]) / 3) @ np.array([A, B, C])
print("形心 G =", G)                      # (5/3, 1)

# 仿射變換下的不變性：旋轉 + 平移後，重心座標不變
c, s = np.cos(0.7), np.sin(0.7)
T = lambda P: np.array([[c, -s], [s, c]]) @ P + np.array([2.0, 3.0])
lam2 = barycentric(T(P), T(A), T(B), T(C))
print("變換後重心座標 =", lam2, " 與原相同? ", np.allclose(lam, lam2))

# 三點共線的代數判別：找 c_i 使 sum(c_i P_i)=0 且 sum(c_i)=0
P3 = A + 2 * (B - A)                      # 在直線 AB 上
M2 = np.vstack([np.column_stack([A, B, P3]), np.ones(3)])
_, sv, Vt = np.linalg.svd(M2)
coef = Vt[-1]
print("共線係數 =", np.round(coef, 4), "  最小奇異值 =", sv[-1])  # sv[-1]≈0 → 共線
P3b = C + np.array([0.2, 0.1])            # 不在直線 AB 上
M3 = np.vstack([np.column_stack([A, B, P3b]), np.ones(3)])
_, sv3, _ = np.linalg.svd(M3)
print("不共線時最小奇異值 =", sv3[sv3 > 1e-12].min())  # 明顯不為 0
```

輸出顯示：$P$ 被還原為 $aA + bB + cC$，形心即等權重心座標 $(1:1:1)$，仿射變換前後重心座標完全不變；共線判定中奇異值 $\approx 0$、不共線時奇異值明顯不為零——Möbius 的係數判別法在數值上一目了然。

### 線索四：Menelaus 與 Ceva 的重新偵辦
Möbius 用重心座標把兩個古典難題變成一行等式。設 $A'$ 在 $BC$ 上，用重心座標記 $A' = (0 : \beta : \gamma)$（對 $\triangle ABC$），則比值 $\frac{BA'}{A'C} = \frac{\gamma}{\beta}$——**線段比就是係數比**。於是：

- **Menelaus 定理**：$A', B', C'$ 三點共線 $\iff$ $\frac{\gamma}{\beta} \cdot \frac{\alpha}{\gamma'} \cdot \frac{\beta'}{\alpha'} = -1$（有向線段）。
- **Ceva 定理**：$AA', BB', CC'$ 三線共點 $\iff$ 同一乘積 $= +1$。

在純歐氏幾何的證明裡，這兩個定理各需巧妙的輔助線；在重心座標下，它們只是「共線判別法」的係數版本。這正是新語言的力量：**舊時代的難題，在新框架下自動降級為計算題**。

## 結案 -- 後果與影響
- **Grassmann 1844**：Hermann Grassmann 在《Ausdehnungslehre》（延拓論）中把 Möbius 的「點的組合」推廣成完整的線性代數——向量空間、線性無關、外積。Grassmann 明言受 Möbius 啟發；Möbius 也撰文評論 Grassmann（雖然坦承沒讀懂）。
- **仿射幾何誕生**：重心座標的不變性劃出了「仿射性質」的領地，為 1872 年 Klein 的 Erlangen 綱領鋪路。
- **射影幾何的齊次座標**：Möbius 的比例式座標是齊次座標的前身，與 Plücker 的工作共同催生了十九世紀的射影幾何黃金時代。
- **現代應用**：有限元方法（FEM）的形狀函數、電腦圖學的三角形內插與網格變形、貝茲曲線的 de Casteljau 演算法，本質上全是 Möbius 重心座標。
- Leibniz 的夢想結案：幾何終於有了自己的代數。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| August Ferdinand Möbius | 案件主嫌：發明重心座標（1827） |
| Gottfried Wilhelm Leibniz | 提出幾何代數夢想（1679） |
| Hermann Grassmann | 直接繼承者：外代數（1844） |
| Lagrange | 力學中已用加權重心 |

- A. F. Möbius, *Der barycentrische Calcul*, Leipzig (1827)。
- H. Grassmann, *Die lineale Ausdehnungslehre* (1844)。
- M. J. Crowe, *A History of Vector Analysis* (1967)：Möbius 到 Grassmann 的傳承敘事。
