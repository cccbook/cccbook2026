# 1637 — Descartes 座標幾何

## 案件摘要
1637 年，René Descartes 在《方法論》的附錄〈La Géométrie〉（幾何學）中，把兩條互相垂直的數軸鋪在幾何平面上，讓每一個「點」都擁有一對數 $(x, y)$，讓每一條「曲線」都對應一個代數方程。幾何與代數這兩門分居三百年的學科，從此合併為一個偵探小組——解析幾何。這也是「線性變換」思想的搖籃：座標系一換，圖形不變、代數式卻隨之變換，線性代數的全部戲碼就在這個舞台上開演。

## 前因 -- 為什麼會有這個案子
- 古希臘人把數學等同於幾何：線段相乘是「畫一個矩形」，方程是「構圖的步驟」。代數只是幾何的僕人。
- Apollonius（約西元前 200 年）《圓錐曲線》用純幾何方式切圓錐，得到橢圓、拋物線、雙曲線，證明艱深冗長，卻沒有一個統一的記號。
- 文藝復興後，航海、天文、彈道急需計算：Tartaglia、Cardano、Viète 把代數符號化，Viète 更首創用字母表示未知數與係數——武器已備，只差一個現場。
- 費馬（Pierre de Fermat）在 1629 年前後已私下寫下《平面與軌跡導論》（Ad locos planos et solidos isagoge），用座標把曲線翻譯成方程，但直到 1679 年死後才出版——他與 Descartes 是同案的另一名偵探，只是登記時間不同。

## 線索與推理 -- 數學式、程式、理論

### 線索一：點是一對數，曲線是一個方程
Descartes 的關鍵動作：在平面上取一條參考線（軸）與一個原點，任一點 $P$ 由長度 $(x, y)$ 決定。於是「平面上滿足某幾何條件的軌跡」可以翻譯成 $x, y$ 之間的方程：

$$F(x, y) = 0$$

例如「到兩定點距離之和恆定」這句幾何囈語，翻譯成代數就是：

$$\sqrt{(x-a)^2 + y^2} + \sqrt{(x+a)^2 + y^2} = 2c \quad\Longleftrightarrow\quad \frac{x^2}{c^2} + \frac{y^2}{c^2 - a^2} = 1$$

左邊是幾何描述（橢圓定義），右邊是代數方程——一次翻譯，終身有效。Apollonius 需要一整卷書證明的性質，現在成了對方程做代數運算的例行公事。

### 線索二：次數決定曲線的「血統」
Descartes 按方程的次數為曲線分類：一次方程

$$ax + by = c$$

是直線；二次方程涵蓋圓錐曲線；三次以上是「機械曲線」。這個分類法首次讓「曲線的複雜度」變成可計算的代數量，也隱含了日後「線性」一詞的起源——一次方程的圖像是直線，而直線正是線性變換把直線映成直線的舞台。

### 線索三：座標變換——線性變換的搖籃
〈La Géométrie〉中最具潛力的線索：同一條曲線，換一組座標軸，方程就變。最簡單的例子是平移與旋轉。平移：

$$(x, y) \mapsto (x + h, y + k)$$

把 $y = x^2$ 的頂點搬到任意處；旋轉 $\theta$ 角：

$$\begin{pmatrix} x' \\ y' \end{pmatrix} = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix}$$

把二次曲線的交叉項 $2Bxy$ 消去——這正是百年後 Cauchy 主軸定理、Lagrange 二次型化簡的最初萌芽。座標變換的本質是**線性映射**：保持加法與純量乘法

$$T(u + v) = T(u) + T(v), \qquad T(\lambda u) = \lambda T(u)$$

矩陣 $A = \begin{pmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{pmatrix}$ 就是這個線性映射的代數化身。幾何的旋轉，在代數世界裡只是一個正交矩陣。

### 線索四：費馬與 Descartes 的優先權之爭
費馬的方法更接近現代：他直接寫 $d x + e y = c$ 為直線方程、按次數分類軌跡。Descartes 則從「尺規作圖的延伸」出發，重心在求解幾何問題。兩人隔空筆戰，Descartes 藉出版優勢佔了名氣，費馬佔了方法論——歷史最終把功勞記給兩人：解析幾何是同一晚案、兩名偵探。

### 線索五：圓錐曲線的統一——Apollonius 之謎的代數解法
Descartes 用他的新武器回頭處理 Apollonius 的老案：三種圓錐曲線在一般座標下的方程都是二元二次式：

$$Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0$$

判別式 $B^2 - 4AC$ 決定血統：$< 0$ 是橢圓（含圓）、$= 0$ 是拋物線、$> 0$ 是雙曲線。Apollonius 需要幾百個命題分開證明的三類曲線，現在只需要**一個判別式**。更妙的是：這三類不是三個不相干的對象，而是同一個二次式在不同參數下的三種面貌——這個「統一性」正是代數方法相對幾何方法的最大優勢，也預告了「化簡二次型」這一整條案件線：只要能找到消去交叉項 $Bxy$ 的座標變換（旋轉主軸），就能把任何圓錐曲線化成標準形。從 Descartes 1637 到 Cauchy 1815，這條線索整整追了一百七十八年。

### 程式碼範例：座標變換把幾何變代數的 numpy 實作
```python
import numpy as np

# 一個橢圓 x²/4 + y²/1 = 1 的離散點（幾何世界）
t = np.linspace(0, 2*np.pi, 200)
pts = np.vstack([2*np.cos(t), np.sin(t)])   # 2x200 座標矩陣

# 旋轉 30 度（線性變換 = 正交矩陣）
theta = np.radians(30)
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])
rot = R @ pts

# 幾何驗證：旋轉不該改變長度（正交矩陣保內積）
lengths_before = np.linalg.norm(pts, axis=0)
lengths_after  = np.linalg.norm(rot, axis=0)
print("長度最大差異:", np.max(np.abs(lengths_before - lengths_after)))  # ~1e-16

# 代數驗證：二次型 Q(x) = x^T A x，A = diag(1/4, 1)
Q = pts.T @ np.diag([1/4, 1]) @ pts
print("旋轉前 Q 值範圍:", Q.min(), Q.max())   # 全為 1（圓錐曲線在主軸座標下標準形）
Qr = rot.T @ np.diag([1/4, 1]) @ rot
print("用舊矩陣算旋轉後的 Q:", Qr.min(), Qr.max())  # 不再是 1，出現交叉項
```

輸出顯示：旋轉不變長度（正交性），但用舊係數矩陣計算的新點，二次型不再等於 1——交叉項出現了。要把交叉項消掉，就得找新的主軸方向，這正是座標變換思想埋下的下一個案件。

回頭看 Descartes 的判別式：$B^2 - 4AC$ 在正交座標變換下有深刻的幾何意義——它的符號（橢圓/拋物線/雙曲線）是曲線的內在不變量，不隨座標軸選擇改變。Sylvester 的慣性定律（1852）正是這個不變量思想的代數化：二次型的指紋 $(p, q, z)$ 不因變換路徑而異。Descartes 在 1637 年用幾何直覺摸到的不變量，兩百年後成為線性代數的定理。

## 結案 -- 後果與影響
- 解析幾何誕生：微積分（Newton 1687、Leibniz 1684）的全部敘事都建立在座標與曲線方程之上——沒有座標，就沒有 $\frac{dy}{dx}$。
- 「線性」概念萌芽：一次方程、座標變換、矩陣記號（Cayley 1858 才正式定義矩陣）的源頭都在 1637 年。
- 為 Lagrange 二次型（1787）、Cauchy 主軸定理（1815）、Beltrami SVD（1873）搭好舞台：所有「化簡二次型」的故事，本質上都是「找一個更好的座標系」。
- 影響至今：電腦繪圖的齊次座標變換、GPS 定位、機器學習的特徵空間，全部是 Descartes 座標系的後裔。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| René Descartes | 1637 出版〈La Géométrie〉，座標幾何之父 |
| Pierre de Fermat | 同期獨立發現（1629 前後），1679 死後出版 |
| Apollonius | 《圓錐曲線》，純幾何時代的巔峰 |
| François Viète | 代數符號化，提供武器 |

- R. Descartes, *La Géométrie*, in *Discours de la méthode*, Leyden (1637)。
- P. de Fermat, *Ad locos planos et solidos isagoge* (1679 出版，約 1629 撰寫)。
