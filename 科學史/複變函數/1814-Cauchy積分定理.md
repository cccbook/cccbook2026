# 1814 — Cauchy 積分定理

## 案件摘要
1814 年，巴黎綜合理工學院（École Polytechnique）的年輕數學家 Augustin-Louis Cauchy 向法蘭西科學院宣讀論文〈Mémoire sur les intégrales définies〉，其中埋藏著一條驚人的線索：若函數在區域內處處可微（解析），則複積分的值與路徑無關——沿閉曲線積分一圈恆得零。1825 年他在〈Mémoires sur les intégrales définies prises entre des limites imaginaires〉中正式完成這條定理。這就是複變函數論的「大憲章」：一條 $\oint_\gamma f(z)\,dz = 0$，撐起此後一百年整座複分析大廈。

## 前因 -- 為什麼會有這個案子
- 18 世紀 Euler、d'Alembert 在流體力學與積分變換中大量使用複變函數，d'Alembert 1752 年已寫下連結實部虛部偏導數的關係式（後稱 Cauchy–Riemann 方程），Euler 也用它解偏微分方程——但兩人都把它當「解題技巧」，沒人追問它背後的結構。
- Gauss 在 1811 年寫給 Bessel 的私人信件中，已經明確陳述複積分的路徑無關性：「當函數在閉曲線內處處可微，繞行一圈積分必為零；否則可以有許多不同的值。」——這是一條藏了數十年的證詞，直到 1878 年信件出版才曝光。
- 實積分的嚴格定義當時仍是懸案：Cauchy 本人在 1823 年《Résumé des leçons...》中才以「和的極限」首次嚴格定義定積分（今稱 Cauchy 積分，Riemann 1854 年再精煉）。
- 複積分 $\int_a^b f(z)\,dz$ 的「上下限是虛數」在當時看來根本是無稽之談——路徑是什麼？積分變數沿什麼走？這就是案發現場。

核心疑問是：**複積分到底積的是什麼？為什麼有的路徑積分相同、有的不同？**

## 線索與推理 -- 數學式、程式、理論

### 線索一：複積分的定義
Cauchy 的做法：設 $\gamma$ 是複平面上從 $z_1$ 到 $z_2$ 的光滑曲線，$f$ 沿線連續。把曲線切成小段，定義：

$$\int_\gamma f(z)\,dz = \lim_{n\to\infty}\sum_{k=1}^{n} f(\zeta_k)(z_k - z_{k-1})$$

其中 $\zeta_k$ 是第 $k$ 小段上的取樣點。用參數化 $z(t) = x(t) + iy(t)$，$t\in[a,b]$，複積分拆成兩個實積分：

$$\int_\gamma f\,dz = \int_a^b \left(u\,dx - v\,dy\right) + i\int_a^b \left(v\,dx + u\,dy\right)$$

其中 $f = u + iv$，$u, v$ 是實部與虛部。**積的對象現身了**：複積分是兩個「第二類曲線積分」的複數組合。

### 線索二：Cauchy–Riemann 方程——路徑無關的關鍵
$d$'Alembert 與 Euler 早已寫下的關係式，Cauchy 給了它判決書：若 $f$ 解析（實部虛部可微且滿足偏導關係），則

$$\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}, \qquad \frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}$$

用它檢查被積式 $u\,dx - v\,dy$：記 $P = u$、$Q = -v$，則

$$\frac{\partial P}{\partial y} = \frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x} = \frac{\partial Q}{\partial x}$$

正是 Green 定理（Green 1828 年發表，Cauchy 當時未見）中「曲線積分與路徑無關」的充要條件！於是：

$$\oint_\gamma f(z)\,dz = 0$$

**定理正式結案**：在單連通域 $D$ 內解析的函數 $f$，沿 $D$ 內任何閉曲線積分恆為零；等價地，積分只依賴端點、與路徑無關。Gauss 1811 年信件中的直覺，被 Cauchy 以實積分理論嚴格證明。

### 線索三：反例——路徑為什麼會「有案底」
定理的威力在於反例：$\displaystyle\oint_\gamma \frac{dz}{z}$ 繞原點一圈：

- 取 $\gamma: z = e^{it}$，$t\in[0,2\pi]$，則 $dz = ie^{it}dt$，
$$\oint_\gamma \frac{dz}{z} = \int_0^{2\pi} \frac{ie^{it}}{e^{it}}\,dt = 2\pi i$$

不為零！因為 $f(z) = 1/z$ 在原點不解析——區域不是單連通的，函數有「案底」（奇點）。積分值 $2\pi i \times (\text{繞行圈數})$ 取決於路徑繞了奇點幾圈。這條「案底」就是 1826 年 Cauchy 留數定理的伏筆。

### 線索四：單連通與原函數
定理的另一面：若 $f$ 在單連通域解析，則定義

$$F(z) = \int_{z_0}^{z} f(\zeta)\,d\zeta$$

因為路徑無關，$F$ 是良定的（well-defined）單值函數，且 $F'(z) = f(z)$——**解析函數在單連通域內必有原函數**。這使得複積分可以像實積分一樣用 Newton–Leibniz 公式：$\int_{z_1}^{z_2} f\,dz = F(z_2) - F(z_1)$，但前提是路徑不得穿越奇點。

### 程式碼範例：複平面路徑積分的數值驗證
```python
import numpy as np

f = lambda z: z**2                      # 解析函數
g = lambda z: 1/z                       # 在原點有奇點

def path_integral(func, zs):
    """沿折線路徑 zs 數值計算複積分（中點法）"""
    total = 0 + 0j
    for k in range(1, len(zs)):
        t = np.linspace(0, 1, 1000)
        z = zs[k-1] + (zs[k]-zs[k-1])*t
        dz = (zs[k]-zs[k-1])/1000
        total += np.sum(func(z)*dz)
    return total

# 案件一：兩條不同路徑從 1 到 i，解析函數 f(z)=z^2 路徑無關
p1 = np.array([1, 1+1j, 1j])            # 先右轉上
p2 = np.array([1, 0+1j*0+0j, 0+1j])     # 沿直線
p2 = np.linspace(1, 1j, 100)            # 直線路徑
print("f(z)=z^2, 折線路徑:", path_integral(f, p1))
print("f(z)=z^2, 直線路徑:", path_integral(f, p2))
# 理論值 F(z)=z^3/3: (i^3 - 1)/3 = (-i - 1)/3
print("理論值  :", (-1j - 1)/3)

# 案件二：解析函數的閉曲線積分 = 0
c = np.exp(1j*np.linspace(0, 2*np.pi, 1000))  # 單位圓（不含原點問題，f解析）
print("閉曲線 ∮ z^2 dz =", path_integral(f, np.append(c, c[0])))

# 案件三：g(z)=1/z 有奇點，繞單位圓一圈不為零
print("閉曲線 ∮ dz/z =", path_integral(g, np.append(c, c[0])), "（理論 2πi =", 2*np.pi*1j, "）")

# 案件四：不繞原點的閉曲線，∮dz/z = 0（路徑平移到圓心 3+0j）
c2 = 3 + np.exp(1j*np.linspace(0, 2*np.pi, 1000))
print("∮dz/z (圓心3):", path_integral(g, np.append(c2, c2[0])))
```

數值輸出顯示：解析函數的積分與路徑無關且閉曲線為零；$1/z$ 繞原點一圈得 $2\pi i$、不繞原點則為零——Cauchy 積分定理與其反例同時驗證。

## 結案 -- 後果與影響
- 複變函數論的**大憲章**：$\oint_\gamma f\,dz = 0$ 成為整座理論的公理級基礎，Cauchy 由它推出積分公式（1825）、留數定理（1826）、Taylor 展開與函數的无窮可微性。
- 路徑無關性 + 奇點「案底」的對比，開啟**多值函數與 Riemann 面**的研究（Riemann 1851）。
- Cauchy–Riemann 方程從技巧升格為解析性的定義核心，解析函數論（holomorphic function theory）正式誕生。
- 實積分的嚴格定義（1823《Résumé》）同時建立，為 Riemann 積分（1854）鋪路。
- 影響至今：保角映射（流體力學、電磁學）、複變數方法計算實積分、控制理論（Nyquist 判據基於圍道積分）皆源於此案。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Augustin-Louis Cauchy | 1814/1825 年提出並證明積分定理 |
| Carl Friedrich Gauss | 1811 年信件中陳述路徑無關性，未公開發表 |
| Leonhard Euler / d'Alembert | Cauchy–Riemann 方程的先行者 |
| George Green | 1828 年 Green 定理（等價的二維論證） |

- A.-L. Cauchy, 〈Mémoire sur les intégrales définies〉, 法蘭西科學院 (1814，1827 刊出)。
- A.-L. Cauchy, 〈Mémoires sur les intégrales définies prises entre des limites imaginaires〉(1825)。
- A.-L. Cauchy, *Résumé des leçons données à l'École royale polytechnique sur le calcul infinitésimal*, Paris (1823)。
- C. F. Gauss, 致 Bessel 信件 (1811)，1878 年出版。
