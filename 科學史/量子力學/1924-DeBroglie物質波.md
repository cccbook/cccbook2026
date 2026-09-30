# 1924-DeBroglie 物質波

## 案件摘要
1924 年，法國王子 Louis de Broglie 在博士論文中提出驚人假說：不只光有粒子性，電子等物質粒子也應有波性，波長 $\lambda = h/p$。他用「電子駐波」重新解釋 Bohr 軌道量子化，並預言電子繞射。三年後 Davisson–Germer 實驗證實，Schrödinger 也因此寫下波動力學。

## 前因 -- 為什麼會有這個案子
- 1923 年 Compton 效應證實光子動量 $\mathbf{p}=\hbar\mathbf{k}$，光的「波粒二象」令物理學界困惑。
- Bohr 模型 (1913) 以「湊出來的」量子化條件 $L = n\hbar$ 描述氫原子，缺乏理論根基。
- de Broglie 的對稱性直覺：大自然應有深刻的對稱——光的波粒二象，必有物質的波粒二象與之對應。
- 他的哥哥 Maurice de Broglie 是實驗 X 射線物理學家，讓他早早接觸輻射量子問題。

## 線索與推理 -- 數學式、程式、理論

### 博士論文的核心假說
1924 年 11 月，*Recherches sur la théorie des quanta*（Sur les quanta）通過答辯。核心關係式：

$$
\lambda = \frac{h}{p} = \frac{h}{mv}, \qquad E = \hbar\omega, \qquad \mathbf{p} = \hbar\mathbf{k}
$$

物質波以相速度與群速度傳播；de Broglie 證明對相對論性粒子，波包的群速度恰等於粒子速度 $v$，而相速度 $v_p = c^2/v > c$（不違反相對論，因相速度不攜帶資訊）。

### 駐波與軌道量子化的新解釋
電子繞核公轉時，其物質波必須首尾相接形成穩定駐波：

$$
2\pi r = n\lambda = n\frac{h}{mv} \quad\Longrightarrow\quad L = mvr = n\frac{h}{2\pi} = n\hbar
$$

Bohr 硬性假設的角動量量子化，瞬間變成「整數個波長才能形成駐波」的幾何必然——如同琴弦只有特定泛音。這是量子化條件第一次擁有物理圖像。

### Davisson–Germer 實驗 (1927)
Bell 實驗室的 Davisson 與 Germer 以 54 eV 電子束轟擊鎳單晶，在 $\phi = 50°$ 觀測到繞射極大。Bragg 條件給出晶格面間距對應的波長：

$$
\lambda_{\text{exp}} = \frac{d\sin\phi}{n} \approx 0.165\,\mathrm{nm}
$$

而 de Broglie 預言：

$$
\lambda = \frac{h}{\sqrt{2m_e K}} \approx 0.167\,\mathrm{nm}
$$

兩者吻合。同年 G. P. Thomson 以電子穿透薄膜獲得繞射環，雙重確認。有趣的是：J. J. Thomson 發現電子是粒子，其子 G. P. Thomson 證明電子是波。

### Python 模擬電子波長隨能量變化
```python
import numpy as np

h, me = 6.62607015e-34, 9.1093837015e-31

def electron_wavelength(eV):
    K = eV * 1.602176634e-19                  # 動能 (J)
    lam = h / np.sqrt(2 * me * K)
    return lam * 1e9                          # nm

for E in [10, 54, 100, 1000]:
    print(f"K = {E:5d} eV  ->  λ = {electron_wavelength(E):.4f} nm")

# 檢驗 Bohr 駐波：n=1 軌道 r≈0.0529 nm，周長 2πr≈0.332 nm
# λ(n=1) = h/(me·c/137·...) ≈ 0.332 nm，恰為周長 → 駐波條件成立
```

## 結案 -- 後果與影響
- 判決：物質具有波性，波粒二象是普适原理，$\lambda=h/p$ 適用一切粒子（電子、中子、原子、分子）。
- **直接啟發 Schrödinger**：1926 年初，Debye 建議 Schrödinger「既然有波，就該有波動方程」，Schrödinger 承認「我的理論受了 de Broglie 週期性思想的啟發」，數個月內寫下著名的 Schrödinger 方程。
- 1929 年 de Broglie 獲諾貝爾物理獎（博士論文獲獎是史上首例）。
- 現代應用：電子顯微鏡（波長遠短於可見光，解析度極高）、中子繞射分析晶體結構、電子束微影。

## 關鍵人物與文獻
- **Louis-Victor de Broglie**（1892–1987），第七代布羅意公爵。
- L. de Broglie, *Recherches sur la théorie des quanta*, Annales de Physique 3, 22 (1925)；答辯導師：Paul Langevin。
- 驗證：C. Davisson & L. Germer, Phys. Rev. 30, 705 (1927)；G. P. Thomson & A. Reid, Nature 119, 890 (1927)。
