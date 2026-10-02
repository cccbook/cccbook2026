# 1843 — Hamilton 四元數

## 案件摘要
1843 年 10 月 16 日傍晚，William Rowan Hamilton 與妻子沿都柏林皇家運河散步。行至 Broombridge（Brougham 橋）時，一個靈感擊中了他：三維旋轉的代數需要**放棄乘法交換律**。他當場用小刀在橋石上刻下：

$$i^2 = j^2 = k^2 = ijk = -1$$

四元數（quaternion）就此誕生。這是數學史上第一次有人系統地放棄一條看似神聖的運算律——交換律——卻仍得到一個自洽而強大的代數系統。

## 前因 -- 為什麼會有這個案子
- 複數 $a+bi$ 完美表示平面上的旋轉與伸縮：乘以 $e^{i\theta}$ 就是旋轉 $\theta$ 角。Hamilton 稱複數為「二元數的有序對」並給出嚴格理論（1837 年論文）。
- Hamilton 的執念：既然二元數如此優雅，那麼**三元數** $(a, b, c)$ 應該能表示三維空間的旋轉。他花了十幾年（約 1830–1843）試圖讓三元數滿足除法與模長規則，全部失敗。
- 失敗的癥結：三維向量 $a\mathbf{i}+b\mathbf{j}+c\mathbf{k}$ 的乘法無法同時滿足 (1) 每個非零元有逆、(2) 模長相乘 $|uv|=|u||v|$、(3) 交換律。這正是後世 Frobenius 定理（1878）會證明的結論：$\mathbb{R}$ 上的結合可除代數只有 $\mathbb{R},\mathbb{C},\mathbb{H}$ 三種——三元數根本不存在。
- 同時代背景：Gauss 1819 年左右在私人手稿中也得到過四元數（未發表）；Grassmann 1844 年的擴張論走的是另一條路。
- 案件核心疑問：三維旋轉的「代數兇器」究竟是什麼？為什麼十年的追捕一無所獲？

## 線索與推理 -- 數學式、程式、理論

### 線索一：橋上的刻痕
Hamilton 的靈感是把「三元」改為「四元」：一個實部加三個虛部：

$$q = a + b\,i + c\,j + d\,k$$

乘法由刻痕的關係式定義（配合 $ij=k,\ jk=i,\ ki=j$ 與 $ji=-k,\ kj=-i,\ ik=-j$——注意**不交換**）：

$$i^2=j^2=k^2=ijk=-1$$

檢驗模長律：$\bar{q} = a - bi - cj - dk$（共軛），$q\bar{q} = a^2+b^2+c^2+d^2$，故

$$|q\bar{q}| = |q|^2, \qquad |q_1 q_2| = |q_1||q_2|$$

這正是著名的**四平方和恆等式**（Euler 1748 年已發現），Hamilton 當場看穿：它就是四元數乘法的模長律。十年追捕失敗的原因也水落石出——他一直在錯誤的維度（3）搜查，真相在維度 4。

### 線索二：放棄交換律的第一次
四元數滿足結合律，但 $ij = k \neq -k = ji$。Hamilton 的勇氣在於：他沒有把「不交換」視為矛盾（兇手逃逸），而是把它視為**新代數的特徵指紋**。用今日術語，四元數 $\mathbb{H}$ 是一個**非交換體（除法環）**——「體」（field）一詞的公理化要再等半個多世紀，但 $\mathbb{H}$ 是第一個非交換的可除代數實例，預告了 19 世紀後半抽象代數（環、體、群的公理化）的誕生。交換律不再是代數的先驗假設，而是**每個系統要個別驗證的偵查項目**。

### 線索三：旋轉表示
四元數表示三維旋轉的公式：對單位四元數 $q = \cos\frac{\theta}{2} + \sin\frac{\theta}{2}\,\mathbf{u}$（$\mathbf{u}$ 為單位虛向量，旋轉軸），向量 $v$（純虛四元數）的旋轉為：

$$v' = q\, v\, q^{-1}$$

這是 **共軛作用**：繞軸 $\mathbf{u}$ 旋轉 $\theta$ 角。與旋轉矩陣相比，四元數只需 4 個參數（矩陣要 9 個）、無萬向鎖（gimbal lock）問題、插值平滑（Slerp）。兩個旋轉的合成就是四元數乘法 $q_2 q_1$——注意順序：先 $q_1$ 後 $q_2$，非交換性在此正是「旋轉順序不可交換」的代數反映。這不是缺陷，是物理事實的忠實記錄。

### 程式碼範例：四元數旋轉數值驗證
```python
import numpy as np

def qmul(q1, q2):                      # Hamilton 積
    a1, b1, c1, d1 = q1; a2, b2, c2, d2 = q2
    return np.array([
        a1*a2 - b1*b2 - c1*c2 - d1*d2,
        a1*b2 + b1*a2 + c1*d2 - d1*c2,
        a1*c2 - b1*d2 + c1*a2 + d1*b2,
        a1*d2 + b1*c2 - c1*b2 + d1*a2])

def qconj(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])

def qrotate(q, v):                     # v' = q v q^{-1}
    vq = np.array([0.0, *v])
    return qmul(qmul(q, vq), qconj(q))[1:]

# 驗證刻痕：i² = j² = k² = ijk = -1
i = np.array([0, 1, 0, 0]); j = np.array([0, 0, 1, 0]); k = np.array([0, 0, 0, 1])
print("i² =", qmul(i, i), " j² =", qmul(j, j), " k² =", qmul(k, k))
print("ijk =", qmul(qmul(i, j), k))
print("ij =", qmul(i, j), "  ji =", qmul(j, i), "  <- 不交換！")

# 模長律 |q1 q2| = |q1||q2|
q1 = np.array([1, 2, 3, 4]) / np.sqrt(30)
q2 = np.array([2, 1, -1, 1]) / np.sqrt(7)
print("|q1 q2| =", np.linalg.norm(qmul(q1, q2)),
      " |q1||q2| =", np.linalg.norm(q1)*np.linalg.norm(q2))

# 繞 z 軸轉 90°：(1,0,0) -> (0,1,0)
theta = np.pi/2
qz = np.array([np.cos(theta/2), 0, 0, np.sin(theta/2)])
print("旋轉 (1,0,0) ->", np.round(qrotate(qz, [1, 0, 0]), 6))

# 與旋轉矩陣對照
Rz = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
print("矩陣結果 =", Rz @ np.array([1, 0, 0]))

# 合成順序：先繞 z 90° 再繞 x 90°（順序不可交換）
qx = np.array([np.cos(theta/2), np.sin(theta/2), 0, 0])
v = [0, 0, 1]
print("先 z 後 x =", np.round(qrotate(qx, qrotate(qz, v)), 6))
print("先 x 後 z =", np.round(qrotate(qz, qrotate(qx, v)), 6))
```

輸出確認：$i^2=j^2=k^2=ijk=-1$、$ij=-ji$、模長律成立、$q v q^{-1}$ 與旋轉矩陣一致，且「先 $z$ 後 $x$」與「先 $x$ 後 $z$」結果不同——非交換性忠實反映旋轉順序。

## 結案 -- 後果與影響
- Hamilton 餘生（1843–1865）致力於四元數理論，1866 年出版《Elements of Quaternions》。
- 1880 年代 Gibbs、Heaviside 從四元數中抽取向量部分，建立**向量代數**（點積、叉積）：叉積 $\mathbf{u}\times\mathbf{v}$ 正是四元數乘積的虛部。四元數是向量分析的生父。
- 四元數是第一個非交換可除代數，直接啟發抽象代數：1878 年 Frobenius 定理分類實結合可除代數、Cayley–Dickson 構造生出八元數（$\mathbb{O}$，連結合律都放棄）。
- 現代應用：電腦圖學（遊戲引擎、動畫）、太空船姿態控制（SpaceX、衛星）、機器人學、量子計算（單量子位元旋轉與 $\mathbb{H}$ 的結構同構於 $SU(2)$ 的局部結構）——都柏林橋上的刻痕至今仍在每一台手機的陀螺儀裡運轉。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| William Rowan Hamilton | 四元數的發明者，橋上刻痕 |
| Carl Friedrich Gauss | 私人手稿中的先行者（未發表） |
| Josiah Willard Gibbs / Oliver Heaviside | 從四元數抽出向量代數 |
| Ferdinand Georg Frobenius | 1878 分類實可除代數 |

- W. R. Hamilton, *On Quaternions; or on a new System of Imaginaries in Algebra*, Phil. Mag. (1844–1850 系列信件論文)。
- W. R. Hamilton, *Elements of Quaternions*, London: Longmans, Green, & Co. (1866, 身後由其子編輯出版)。
