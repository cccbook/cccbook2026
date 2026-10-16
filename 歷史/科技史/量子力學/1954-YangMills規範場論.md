# 1954 — Yang–Mills 規範場論

## 案件摘要
1954 年，楊振寧與 Robert Mills 發表 "Conservation of Isotopic Spin and Isotopic Gauge Invariance"，把電磁學的 U(1) 規範對稱推廣到非阿貝爾群 SU(2)，開創非阿貝爾規範場論。這座大廈起初因「規範玻色子必須無質量」而處處碰壁，直到 1960s–70s 自發對稱破缺（Higgs 機制）與漸近自由現身，才組裝成粒子物理的標準模型 $SU(3)\times SU(2)\times U(1)$。

## 前因 -- 為什麼會有這個案子
- **電磁學的成功**：Maxwell 方程隱含 U(1) 規範對稱；Weyl 1929 年確立「規範不變性 ⟹ 電荷守恆」的架構。
- **同位旋之謎**：1932 年 Heisenberg 發現質子與中子在強交互作用中幾乎等同（$n$–$p$ 質量差僅 0.14%），可視為同一粒子（核子）的「同位旋」二重態，強作用近似 SU(2) 對稱。
- **守恆律與對稱**：Noether 定理說每個連續對稱對應一個守恆量；楊振寧問：**同位旋守恆能否像電荷守恆一樣，來自一個局域規範對稱？**
- 楊振寧在 Brookhaven 訪問時與研究生 Mills 合作，把 U(1) 推廣到 SU(2)。

## 線索與推理 -- 數學式、程式、理論

### 1. U(1) 電磁規範對稱（阿貝爾）
帶電荷 $q$ 的場 $\psi$ 在局域相位變換下：

$$\psi \to e^{iq\chi(x)/\hbar}\, \psi$$

為保持不變性，導數必須換成協變導數：

$$D_\mu = \partial_\mu + \frac{iq}{\hbar} A_\mu, \qquad A_\mu \to A_\mu + \partial_\mu \chi$$

$A_\mu$ 即電磁四維勢。因 U(1) 是阿貝爾群（元素可交換），變換規則是線性相加，場強 $F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$ 是規範不變的。

### 2. SU(2) 非阿貝爾推廣（Yang–Mills 的核心）
同位旋二重態 $\psi = (\psi_p, \psi_n)^T$，局域 SU(2) 變換：

$$\psi \to U(x)\, \psi, \qquad U(x) = e^{i\alpha^a(x)\, \tau^a/2}$$

其中 $\tau^a$ 為 Pauli 矩陣。**關鍵難點**：$U(x_1)$ 與 $U(x_2)$ 不對易（$[\tau^a, \tau^b] = i\epsilon^{abc}\tau^c \neq 0$），普通的 $A_\mu \to A_\mu + \partial_\mu\chi$ 規則失效。楊與 Mills 發現必須引入**三個**規範場 $A_\mu^a$（$a=1,2,3$），以矩陣形式組合：

$$A_\mu = A_\mu^a \frac{\tau^a}{2}$$

協變導數：

$$D_\mu = \partial_\mu + ig A_\mu$$

規範變換律（非線性！因為非阿貝爾）：

$$A_\mu \to U A_\mu U^{-1} + \frac{i}{g} U \partial_\mu U^{-1}$$

### 3. 場強張量與 Yang–Mills 拉氏量
非阿貝爾場強：

$$F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu + ig[A_\mu, A_\nu] = F_{\mu\nu}^a \frac{\tau^a}{2}$$

比電磁學多出對易子項 $ig[A_\mu, A_\nu]$——這是**規範玻色子自我交互作用**的來源（光子不與光子作用，但 Yang–Mills 玻色子會）。拉氏量：

$$\mathcal{L}_{\text{YM}} = -\frac{1}{4} F_{\mu\nu}^a F^{a\mu\nu} + \bar{\psi}(i\gamma^\mu D_\mu - m)\psi$$

Noether 定理保證同位旋守恆；規範不變性完全決定交互作用的結構——這是「對稱決定動力學」的偵探美學。

### 4. 質量缺口難題（mass gap）
Yang–Mills 拉氏量中規範玻色子無質量項（質量項 $m^2 A_\mu^a A^{a\mu}$ 破壞規範不變性）。但實驗上：
- 強作用的媒介（膠子、介子）有明顯質量尺度；
- 若規範玻色子無質量，強作用應是長程力，實際卻是短程（$\sim 10^{-15}$ m）。

「質量從哪來？」成為 Yang–Mills 理論的第一樁懸案，1954 年 Pauli 在研討會上當場以此質疑楊振寧。

### 5. 1970s 的破案：自發對稱破缺與漸近自由
- **Higgs 機制**（1964，Englert–Brout、Higgs、Guralnik–Hagen–Kibble）：規範對稱**自發破缺**——真空態不對稱但拉氏量對稱。純量場 $\phi$ 獲得真空期望值：

$$\langle \phi \rangle = v/\sqrt{2}, \qquad \mathcal{L} \supset -\mu^2 \phi^\dagger\phi - \lambda(\phi^\dagger\phi)^2 \;(\mu^2 < 0)$$

  Goldstone 玻色子被規範玻色子「吃掉」，後者獲得質量 $m_W = gv/2$——**規範不變性未破壞，玻色子卻有質量**。
- **漸近自由**（1973，Gross–Wilczek、Politzer）：非阿貝爾對易子項使耦合常數隨能量降低：

$$\beta(g) = -\frac{g^3}{16\pi^2}\Big(\frac{11}{3}C_2 - \frac{2}{3}T_R N_f\Big) < 0 \implies \alpha_s(Q^2) \to 0 \text{ 當 } Q^2 \to \infty$$

  這解釋了深度非彈性散射中夸克的「漸近自由」，也確認 SU(3) 色動力學（QCD）為強作用的正確理論。

### 6. 標準模型的組裝
$$G_{\text{SM}} = SU(3)_{\text{color}} \times SU(2)_{\text{weak}} \times U(1)_{\text{hypercharge}}$$

| 群 | 交互作用 | 媒介玻色子 | 質量來源 |
|---|---|---|---|
| SU(3) | 強（QCD） | 8 個膠子 | 色禁閉（無希格斯） |
| SU(2)×U(1) | 電弱 | $W^\pm, Z^0, \gamma$ | Higgs 機制 |
| Higgs 純量場 | — | $H$ (2012 發現) | — |

電弱統一（Glashow–Weinberg–Salam, 1967–68）把 SU(2) 與 U(1) 結合後自發破缺；1970s 't Hooft–Veltman 證明電弱理論可重整化。標準模型至此完工，迄今通過所有實驗檢驗。

### 7. 程式碼範例：驗證非阿貝爾性與場強的對易子項
```python
import numpy as np

# SU(2) 生成元: tau_a / 2 (Pauli 矩陣)
tau = [np.array([[0,1],[1,0]], dtype=complex),
       np.array([[0,-1j],[1j,0]], dtype=complex),
       np.array([[1,0],[0,-1]], dtype=complex)]
G = [t/2 for t in tau]
eps = np.zeros((3,3,3))
eps[0,1,2] = eps[1,2,0] = eps[2,0,1] = 1
eps[0,2,1] = eps[2,1,0] = eps[1,0,2] = -1

# 1. 非阿貝爾性: [T^a, T^b] = i eps^{abc} T^c
a, b = 0, 1
comm = G[a] @ G[b] - G[b] @ G[a]
expected = 1j * eps[a,b,2] * G[2]
print("非阿貝爾對易關係成立:", np.allclose(comm, expected))  # True

# 2. U(1) vs SU(2): U(1) 生成元是 1x1，天然對易
print("U(1) 對易: True (1x1 矩陣)")

# 3. 場強的對易子項示意: F = dA - dA + ig[A, A]
A_mu = 0.3 * G[0] + 0.2 * G[1]
comm_term = 1j * (A_mu @ A_mu - A_mu @ A_mu)  # 若兩個 A 可交換則為 0
print("兩個不同方向的 A 對易子項非零:", not np.allclose(1j*(G[0]@G[1]-G[1]@G[0]), 0))
# 對易子項 != 0 ⟹ Yang-Mills 玻色子自我交互作用（QCD 三頂點/四頂點圖的來源）
```

## 結案 -- 後果與影響
- **結案**（1954–1970s）：非阿貝爾規範場論從「數學上漂亮但物理上碰壁」到「標準模型的骨架」，靠 Higgs 機制（質量）與漸近自由（重整化）兩把鑰匙開鎖。
- **實驗驗證**：W/Z 玻色子（1983）、漸近自由（1970s DIS）、Higgs 玻色子（2012, LHC）——2013 年 Englert、Higgs 獲 Nobel 物理獎。
- **深遠影響**：
  - 標準模型成為人類對物質結構的最佳描述；所有已知基本交互作用（除重力）皆由規範場論描述。
  - **Yang–Mills 存在性與質量缺口**是 Clay 數學研究所列的**千禧年大獎問題**之一（懸賞 100 萬美元）：證明 4 維 Yang–Mills 理論存在嚴格的量子定義且具有質量缺口 $\Delta > 0$。本案的「數學嚴格性」部分至今懸而未決。
  - 規範理論的思想滲透到數學：Donaldson 理論、Seiberg–Witten 方程、鏡像對稱——物理與幾何在 Yang–Mills 上再度交會。
  - 楊振寧因此獲 1957 年 Nobel 物理獎（因宇稱不守恆，非 Yang–Mills）；Mills 則終身在學界推廣此理論。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| 楊振寧（C. N. Yang） | 偵探，非阿貝爾規範場論共同發明人 |
| Robert Mills | 共同發明人 |
| Wolfgang Pauli | 1954 當場質疑質量問題（早期的反方偵探） |
| Higgs, Englert, Kibble | 1964 Higgs 機制 |
| Gross, Wilczek, Politzer | 1973 漸近自由 |
| Glashow, Weinberg, Salam | 電弱統一 |

**文獻**
- C. N. Yang, R. L. Mills, "Conservation of Isotopic Spin and Isotopic Gauge Invariance", *Phys. Rev.* **96**, 191 (1954).
- P. W. Higgs, *Phys. Rev. Lett.* **13**, 508 (1964).
- D. J. Gross, F. Wilczek, *Phys. Rev. Lett.* **30**, 1343 (1973)；H. D. Politzer, *Phys. Rev. Lett.* **30**, 1346 (1973).
- C. N. Yang, *Selected Papers 1945–1980 with Commentary*, Freeman (1983).
- Clay Mathematics Institute, "Yang–Mills Existence and Mass Gap" (2000).
