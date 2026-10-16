# 1829-Jacobi橢圓函數

## 案件摘要
1829 年，雅可比（Carl Gustav Jacobi）出版《橢圓函數理論新基礎》（Fundamenta nova theoriae functionum ellipticarum）。他與阿貝爾（Abel）這對「雙子星」幾乎同時發現：橢圓積分的反函數是**雙週期**的。一個新的函數宇宙就此誕生。

## 前因 -- 為什麼會有這個案子
- 橢圓積分 $\int_0^x \frac{dt}{\sqrt{(1-t^2)(1-k^2t^2)}}$ 自 17 世紀起出現在單擺週期、橢圓弧長中，Fagnano、歐拉發現其**加法公式**（橢圓積分版的 $\sin(a+b)$），卻無法把它「積出來」。
- Abel 的關鍵洞見：積不出來，就**反轉它**——把積分視為新函數的自變數。1827 年 Abel 與 Jacobi 幾乎同時發表反演理論。
- 高斯更早（約 1798 年）私下已有同樣發現但未發表，死後遺稿證實。

## 線索與推理 -- 數學式、程式、理論

### 線索一：反演 —— 橢圓積分的反函數
定義第一類橢圓積分（模數 $k$）：

$$u = F(\phi, k) = \int_0^{\sin\phi} \frac{dt}{\sqrt{(1-t^2)(1-k^2t^2)}}$$

Jacobi 反轉它，定義三個基本函數：

$$\mathrm{sn}(u) = \sin\phi, \qquad \mathrm{cn}(u) = \cos\phi, \qquad \mathrm{dn}(u) = \sqrt{1 - k^2\sin^2\phi}$$

滿足恆等式（sin/cn 版的畢氏定理）：

$$\mathrm{sn}^2(u) + \mathrm{cn}^2(u) = 1, \qquad \mathrm{dn}^2(u) + k^2\,\mathrm{sn}^2(u) = 1$$

當 $k \to 0$：$\mathrm{sn} \to \sin$、$\mathrm{cn} \to \cos$、$\mathrm{dn} \to 1$，退化回三角函數。

### 線索二：雙週期性 —— 最大的意外
$\sin(z + 2\pi) = \sin(z)$ 只有一個（複）週期；而橢圓函數有**兩個**：

$$\mathrm{sn}(z + 4K) = \mathrm{sn}(z), \qquad \mathrm{sn}(z + 2iK') = \mathrm{sn}(z)$$

其中 $K = F(\pi/2, k)$ 是完全橢圓積分，$K' = F(\pi/2, \sqrt{1-k^2})$。一般地，所有橢圓函數都是某個格 $\Lambda = 2\omega_1\mathbb{Z} + 2\omega_2\mathbb{Z}$ 的雙週期亞純函數（這正是 Weierstrass $\wp$ 函數的定義性質）。

### 線索三：theta 函數
Jacobi 用四個 theta 函數把 sn/cn/dn 表示為**商**：

$$\mathrm{sn}(u) = \frac{\theta_3(0)}{\theta_2(0)} \cdot \frac{\theta_1(v)}{\theta_4(v)}, \quad v = \frac{u}{\theta_3(0)^2}, \quad \theta_1(v) = 2\sum_{n=0}^\infty (-1)^n q^{(n+1/2)^2}\sin((2n+1)v)$$

theta 函數是 $q = e^{i\pi\tau}$ 的冪級數，收斂極快，是計算的引擎——也使橢圓函數成為**模形式的前身**：theta 變換公式 $\theta(-1/\tau) = \sqrt{-i\tau}\,\theta(\tau)$ 正是模群作用的雛形。

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import ellipk

k = 0.7
K  = ellipk(k**2)        # 完全橢圓積分 K
Kp = ellipk(1 - k**2)    # K'
print(f"sn 的雙週期: 實週期 4K = {4*K:.4f}, 虛週期 2iK' (K' = {Kp:.4f})")

# 用 mpmath 精確計算並畫出 sn/cn/dn 的雙週期曲線
from mpmath import ellipf, ellipsn, ellipcn, ellipdn
import mpmath as mp

us = np.linspace(0, 4*K, 400)
sn = [float(ellipsn(mp.mpf(u), k)) for u in us]
cn = [float(ellipcn(mp.mpf(u), k)) for u in us]
dn = [float(ellipdn(mp.mpf(u), k)) for u in us]

plt.figure(figsize=(9, 4))
plt.plot(us, sn, label='sn(u)')
plt.plot(us, cn, label='cn(u)')
plt.plot(us, dn, label='dn(u)')
plt.axvline(4*K, ls='--', c='gray', label=f'週期 4K={4*K:.3f}')
plt.axvline(2*K, ls=':', c='gray')
plt.legend(); plt.title(f'Jacobi 橢圓函數 (k={k}) 的實週期性')
plt.xlabel('u'); plt.grid(True); plt.savefig('jacobi_sn_cn_dn.png', dpi=120)
```

曲線像「壓縮過的正弦」——單擺大角度擺動的解正是 $\sin\phi(t) = \mathrm{sn}(u_0 + \omega t)$，橢圓函數第一次讓非線性振盪有了閉式解。

### 線索四：通往費馬最後定理與朗蘭茲
- 橢圓曲線 $y^2 = x^3 + ax + b$ 的積分就是橢圓積分；每一條橢圓曲線配上其週期格 $\Lambda \cong \mathbb{C}/\Lambda$，是 Wiles 證明**費馬最後定理**（1995）的舞台——FLT 歸結為谷山–志村猜想：「每條半穩定橢圓曲線都是模形式」。
- 橢圓曲線的 $L$ 函數滿足 $\Lambda$-函數方程，是**朗蘭茲綱領**中 Galois 表示 ↔ 自守形式的頭號範例；而這一切的源頭正是 1829 年的雙週期函數。

## 結案 -- 後果與影響
- 代數函數積分的「不可能性」被轉化為新函數的誕生：**反轉困難**成為數學的經典策略。
- 雙週期性 → Weierstrass $\wp$ → 緊黎曼面 → 模形式與數論的大統一。
- 密碼學的橢圓曲線 ECC、物理中的孤子方程（KdV、非線性 Schrödinger 的橢圓函數解）都是本案的遠期餘波。

## 關鍵人物與文獻
- **Jacobi, C. G. J.**（1829）：《Fundamenta nova theoriae functionum ellipticarum》。
- **Abel, N. H.**（1827）：《Recherches sur les fonctions elliptiques》，與 Jacobi 並立的雙子星。
- **Gauss, C. F.**：遺稿（約 1798）中的 lemniscatic functions，最早的反演。
- **Lang, S.**（1987）：《Elliptic Functions》現代教材。
