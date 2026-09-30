# 1922-Friedmann 膨脹宇宙

## 案件摘要
1922 年，俄國數學家 Alexander Friedmann 求出 Einstein 方程的動態宇宙解：宇宙可以膨脹或收縮。
他挑戰了 Einstein「宇宙必須靜態」的信仰，並在 1925 年早逝前，為大爆炸宇宙學埋下第一顆種子。

## 前因 -- 為什麼會有這個案子
- 1915 年 Einstein 提出廣義相對論，場方程：
  $$G_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$$
- 1917 年 Einstein 將其套用到整個宇宙，但發現純物質宇宙會因重力而塌縮，於是人為加入宇宙常數 $\Lambda$，構造一個靜態宇宙（Einstein 靜態宇宙）。
- 同年 de Sitter 也找到一個（看似靜態、實則膨脹的）空真空解。
- 當時主流信念：宇宙是永恆、靜態、不變的。任何「動態宇宙」都被視為數學遊戲。
- **線索疑點**：靜態解其實不穩定——只要物質分布稍有擾動，宇宙就會開始膨脹或收縮。這是不穩定的平衡，像立在針尖上的筆。

## 線索與推理 -- 數學式、程式、理論

### 1. 對稱性假設：宇宙學原理
Friedmann 假設宇宙在足夠大的尺度上是**均勻（homogeneous）且各向同性（isotropic）**。
在此對稱性下，最一般的度規是 FRW（Friedmann–Robertson–Walker）度規：

$$ds^2 = -c^2dt^2 + a(t)^2\left[\frac{dr^2}{1-kr^2} + r^2(d\theta^2 + \sin^2\theta\, d\phi^2)\right]$$

其中：
- $a(t)$：宇宙尺度因子，描述空間整體的伸縮。
- $k$：空間曲率參數，$k = +1$（正曲率，封閉）、$k = 0$（平坦）、$k = -1$（負曲率，開放）。

### 2. 代入場方程：Friedmann 方程
將 FRW 度規與理想流體能量動量張量 $T_{\mu\nu}$ 代入 Einstein 方程，得到兩個關鍵方程：

**Friedmann 方程（能量）：**
$$\left(\frac{\dot{a}}{a}\right)^2 = \frac{8\pi G}{3}\rho - \frac{kc^2}{a^2} + \frac{\Lambda c^2}{3}$$

**加速度方程：**
$$\frac{\ddot{a}}{a} = -\frac{4\pi G}{3}\left(\rho + \frac{3p}{c^2}\right) + \frac{\Lambda c^2}{3}$$

**線索推理核心**：$\dot{a}/a \neq 0$ 代表宇宙在動！若 $\rho > 0$ 且 $\Lambda = 0$，則：
- $k = +1$：膨脹到最大後回收縮 → 封閉宇宙（大擠壓）
- $k = 0$：永遠膨脹，漸趨停止 → 臨界宇宙
- $k = -1$：永遠加速膨脹 → 開放宇宙

三種幾何對應三種命運，這就是 Friedmann 的推理結論：**宇宙的幾何決定它的命運**。

### 3. Einstein 的「最大錯誤」
- 1922 年 Friedmann 投稿到《Zeitschrift für Physik》，Einstein 起初反駁說他算錯了。
- Friedmann 寫信詳細解釋，Einstein 撤回反駁，承認計算正確——但仍認為「物理上不具意義」。
- 1929 年 Hubble 觀測到宇宙膨脹後，Einstein 承認引入 $\Lambda$ 是「一生最大的錯誤（biggest blunder）」（據 Gamow 回憶）。
- 諷刺的是：1998 年發現宇宙加速膨脹後，$\Lambda$ 以「暗能量」之姿王者歸來。

### 4. Lemaître 1927 的獨立發現
- 1927 年比利時神父 Lemaître 獨立求出同樣的膨脹解，並首次把膨脹與 Slipher 的星系紅移觀測連結，估出「Hubble 常數」（比 Hubble 早兩年）。
- 1931 年更提出「原始原子（primeval atom）」假說——大爆炸理論的直接前身。

### 5. Python numpy 模擬三種 $a(t)$ 演化
塵埃宇宙（$p=0$，$\Lambda=0$），參數化 $a(\eta)$ 有解析解，但用數值積分更直觀：

```python
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Friedmann 方程 (dust, Lambda=0): dadt^2 = M/a - k
def rhs(a, t, M, k):
    dadt = np.sqrt(M/a - k) if M/a - k > 0 else 0.0
    return dadt

M = 1.0
t = np.linspace(0.01, 4, 400)
a0 = 0.01

plt.figure(figsize=(8,5))
for k, label in [(1, 'k=+1 封閉(塌縮)'), (0, 'k=0 平坦(臨界)'), (-1, 'k=-1 開放(永膨)')]:
    sol = odeint(rhs, a0, t, args=(M, k))
    plt.plot(t, sol, label=label)

# 對照：dust 平坦宇宙解析解 a ∝ t^(2/3)
plt.plot(t, (t/1.5)**(2/3), 'k--', label='a ∝ t^(2/3) 理論')
plt.xlabel('時間 (任意單位)'); plt.ylabel('尺度因子 a(t)')
plt.title('Friedmann 宇宙三種命運 (Λ=0, dust)')
plt.legend(); plt.grid(alpha=0.3); plt.show()
```

$k=+1$ 的曲線先升後降（大擠壓），$k=0$ 與 $k=-1$ 永遠上升——三條曲線就是三種宇宙的命運判决書。

## 結案 -- 後果與影響
- **結案**：宇宙不是靜態的。Einstein 方程的通解允許（甚至預言）膨脹宇宙。
- Friedmann 1925 年死於傷寒（37 歲），未親眼見證 Hubble 的觀測。蘇聯封鎖下他的工作長期被西方忽視。
- 影響鏈：Friedmann/Lemaître (1922/27) → Hubble (1929) → Lemaître 原始原子 (1931) → Gamow 熱大爆炸 (1948) → CMB (1965) → 現代宇宙學標準模型。
- 「最大錯誤」的 $\Lambda$ 在 1998 年以暗能量身分復活，成為當代最深的謎題。

## 關鍵人物與文獻
| 人物 | 貢獻 |
|------|------|
| Alexander Friedmann (1888–1925) | 1922/1924 求出膨脹宇宙解 |
| Albert Einstein (1879–1955) | 場方程、$\Lambda$、「最大錯誤」 |
| Willem de Sitter (1872–1934) | 1917 空真空解 |
| Georges Lemaître (1894–1966) | 1927 獨立發現、1931 原始原子 |
| Edwin Hubble (1889–1953) | 1929 觀測證實膨脹 |

**文獻**
- A. Friedmann, "Über die Krümmung des Raumes" (1922), Z. Phys. 10, 377.
- A. Friedmann, "Über die Möglichkeit einer Welt mit konstanter negativer Krümmung des Raumes" (1924).
- G. Lemaître, "Un Univers homogène de masse constante..." (1927), Annales de la Société Scientifique de Bruxelles.
- G. Gamow, "My World Line" (1970)——「biggest blunder」的出處。
