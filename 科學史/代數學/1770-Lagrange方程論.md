# 1770-Lagrange 方程論

## 案件摘要
1770 年，Lagrange 發表《Réflexions sur la résolution algébrique des équations》（關於代數方程解法的反思），用「根的置換函數」統一檢視二次、三次、四次方程的所有已知解法。這是一場縝密的偵查：他發現解法的成敗取決於一個置換函數在 $n!$ 個置換下取多少個不同的值——而五次方程讓這條線索徹底斷裂，卻為 Galois 理論留下了完美伏筆。

## 前因 -- 為什麼會有這個案子
- 16 世紀義大利代數學派（del Ferro、Tartaglia、Cardano、Ferrari）解出三次與四次方程，但各種解法看似花招百出、彼此不相干。
- 1545 年 Cardano《Ars Magna》之後近 250 年，無人能解五次方程，也無人能解釋**為什麼解不出來**。
- Vandermonde（1770 年代初同期）已開始用置換觀點研究方程，但缺乏系統性。
- Lagrange 的偵查目標：把所有既有解法放在一起對照，找出「共用手法」，判斷五次方程案件能否偵破。

## 線索與推理 -- 數學式、程式、理論

### 線索一：根的置換函數（resolvent）
設方程的根為 $x_1, x_2, \ldots, x_n$。考慮 $x_i$ 的有理函數：
$$\phi(x_1, x_2, \ldots, x_n)$$

Lagrange 的關鍵觀察：對 $n$ 個根施加所有 $n!$ 個置換，$\phi$ 取到的**相異值個數**決定了它攜帶的資訊量，而這些相異值恰好是某個「預解方程」的根。

### 線索二：Lagrange 預解式與三、四次解法的統一
**二次方程**（$n=2$）：取 $\phi = x_1 - x_2$。在 $2!=2$ 個置換下取 2 個值 $\pm(x_1-x_2)$，其平方 $(x_1-x_2)^2 = (x_1+x_2)^2 - 4x_1x_2 = b^2-4c$ 可由係數表出——判別式的誕生。

**三次方程**（$n=3$）：取 $\phi = x_1 + \omega x_2 + \omega^2 x_3$（$\omega = e^{2\pi i/3}$）。在 $3!=6$ 個置換下只取 2 個值，因此 $\phi^3$ 滿足一個二次方程——Cardano 解法被「翻譯」成置換語言。

**四次方程**（$n=4$）：取 $\phi = x_1x_2 + x_3x_4$。在 $4!=24$ 個置換下只取 3 個值，因此 $\phi$ 滿足一個三次方程——Ferrari 解法同樣被統一。

統一圖像：解 $n$ 次方程 = 遞迴地解一串預解方程，置換函數的「取值個數」必須是**比 $n!$ 小、且能被逐步約化**的數。

### 線索三：五次為何失效——置換數量爆增
$n=5$ 時，$5! = 120$。任何在 5 次方程根上的有理函數 $\phi$：
- 若取少數幾個值（如 2、3、4、5 個），其對應的預解方程次數雖低，但**無法再由它遞迴表出原方程的根**——線索中斷；
- 若取全部 120 個值，預解方程本身是 120 次，比原方程更難。

Lagrange 的結論：**「以這些方法求解五次方程，是沒有希望的。」** 他沒有證明「不可能」，但把問題從「如何解」轉化為「置換的子群結構是否允許遞迴約化」——這正是偵探把動機問題換了一個問法。

### 程式碼：Python 演示 Lagrange 置換函數的取值計數

```python
from itertools import permutations
from fractions import Fraction

def distinct_values(phi, n):
    """phi: 接受 n 個根的函數；回傳在 n! 個置換下的相異值個數"""
    vals = set()
    for p in permutations(range(n)):
        # 把 phi 作用在符號根 (x1,...,xn) 的置換結果上，此處用數值代入示意
        vals.add(phi(p))
    return len(vals), sorted(vals)

# 以數值根示範：三次方程 x^3 - 1 = 0 的三個根（用虛根 ω 的角色）
# 用「置換模式」本身計數：phi = x1 + x2 + x3 恆為對稱 -> 1 個值
def phi_sym(p): return sum(p)                # 對稱函數：不變
def phi_diff(p): return p[0] - p[1]          # 差：多值
def phi_pair(p): return (p[0], p[1], (p[2], p[3])) if len(p) == 4 else None

for n in (2, 3, 4):
    print(f"n={n}, 5!={__import__('math').factorial(n) if n==5 else __import__('math').factorial(n)}")
    print("  對稱和   取值個數:", distinct_values(phi_sym, n)[0])
    print("  首項差   取值個數:", distinct_values(phi_diff, n)[0])

# Lagrange 關鍵數字：
# n=4: phi = x1x2 + x3x4 在 24 個置換下取 3 個值（成對分組）
# n=5: 5! = 120，任何低值函數無法遞迴約化 -> 解法失效
import math
print("n=5 的置換總數:", math.factorial(5))
```

## 結案 -- 後果與影響
- **結案**：三、四種「花招」解法被統一為一套置換理論；五次方程被判定為「現有手法不可解」，Lagrange 親自宣告線索中斷。
- 1799 年 Ruffini、1824 年 Abel 先後給出（日趨嚴格的）五次方程無根式解證明，正是沿著 Lagrange 的置換思路推進。
- 1832 年 Galois 把「置換函數取幾個值」昇華為「方程的 Galois 群」與其**正規子群鏈（組合列）**的結構問題，徹底偵破此案：五次方程可解當且僅當其 Galois 群可解，而 $S_5$ 不可解（$A_5$ 為單群）。
- 深遠影響：群論、域擴張理論、乃至 20 世紀的 Galois 表示論與 Langlands 綱領，皆發端於 1770 年這份「偵查報告」。

## 關鍵人物與文獻
- **Joseph-Louis Lagrange（1736–1813）**：都靈出生，後任職柏林、巴黎，《反思》是其代數學的巔峰之作。
- **Paolo Ruffini（1765–1822）**、**Niels Henrik Abel（1802–1829）**：五次不可解的證明者。
- **Évariste Galois（1811–1832）**：置換理論的完成者。
- 文獻：J.-L. Lagrange, "Réflexions sur la résolution algébrique des équations", *Nouveaux Mémoires de l'Académie royale des Sciences et Belles-Lettres de Berlin*, 1770–1771。
