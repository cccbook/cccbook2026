# 1948 — Feynman 路徑積分

## 案件摘要
1948 年，Richard Feynman 在 *Reviews of Modern Physics* 發表 "Space-Time Approach to Non-Relativistic Quantum Mechanics"，提出路徑積分（path integral）形式：量子粒子從 A 到 B，不走「某條」路，而是**同時走過所有可能路徑**，每條路以 $e^{iS/\hbar}$ 加權求和。這是繼矩陣力學、波動力學、Hilbert 空間形式之後的第四套等價表述，也是後來 QED 與量子場論的計算引擎。

## 前因 -- 為什麼會有這個案子
- 1933 年 Dirac 的論文 "The Lagrangian in Quantum Mechanics" 留下關鍵線索：他指出量子力學的傳播函數與 Lagrangian 有關，並寫下「$e^{iS/\hbar}$ 對應於每條路徑的貢獻」的模糊陳述。
- Feynman 在 Princeton（師從 Wheeler）時期研究電磁場的「吸收體理論」，發現 Lagrangian 表述比 Hamiltonian 更適合相對論性問題。
- 當時的 Schrödinger 方程形式在相對論推廣（Klein–Gordon、Dirac 方程）中遇到困難；Feynman 想要一個直接建立在時空（而非 Hilbert 空間）上的量子力學。
- 二戰後在 Cornell，Feynman 把 Dirac 的一句模糊線索發展成完整的數學理論。

## 線索與推理 -- 數學式、程式、理論

### 1. Dirac 的線索
Dirac 1933 觀察到，傳播函數 $K$ 在小時間切片下近似：

$$K(x_b, t_b; x_a, t_a) \approx e^{\frac{i}{\hbar} L(x_b, \dot{x}_b) \Delta t}$$

他寫道此式「corresponds to」作用量——但沒有說「等於」或如何組合多條路徑。Feynman 的偵探工作：**把「對應」變成「等於」**。

### 2. 傳播函數與路徑積分
量子粒子從 $(x_a, t_a)$ 到 $(x_b, t_b)$ 的振幅：

$$\boxed{K(x_b, t_b; x_a, t_a) = \int \mathcal{D}[x(t)]\; e^{\frac{i}{\hbar} S[x]}}$$

其中 $\mathcal{D}[x(t)]$ 是對所有連接兩點的路徑求和的測度，作用量：

$$S[x] = \int_{t_a}^{t_b} L(x, \dot{x})\, dt$$

### 3. 時間切片構造（讓積分有意義）
把時間切成 $N$ 片，每片寬 $\epsilon$，插入完備性關係 $\int dx |x\rangle\langle x| = I$：

$$K = \lim_{N\to\infty} \int \prod_{k=1}^{N-1} dx_k \; \prod_{k=0}^{N-1} \exp\!\Big[\frac{i\epsilon}{\hbar} L\Big(x_k, \frac{x_{k+1}-x_k}{\epsilon}\Big)\Big]$$

對自由粒子（$L = \frac{m\dot{x}^2}{2}$）可嚴格算出：

$$K_{\text{free}} = \sqrt{\frac{m}{2\pi i \hbar (t_b - t_a)}}\; \exp\!\Big[\frac{i m (x_b - x_a)^2}{2\hbar (t_b - t_a)}\Big]$$

### 4. 最小作用量原理的量子推廣
古典力學說：粒子走使 $S[x]$ **極小**的路徑（$\delta S = 0$，Euler–Lagrange 方程）。
量子力學說：粒子走**所有**路徑。那為何古典世界只看到一條？

線索：當 $S \gg \hbar$ 時，$e^{iS/\hbar}$ 是劇烈振盪的相位——鄰近路徑的貢獻互相抵消（destructive interference），唯有 $\delta S = 0$ 附近的路徑（相位平穩，stationary phase）存活。**古典軌跡是量子路徑求和的干涉殘骸**。這是「最小作用量原理」的量子起源。

### 5. 與 Schrödinger 方程等價
傳播函數滿足 Schrödinger 方程（視 $t_b$ 為變數）：

$$i\hbar \frac{\partial K}{\partial t_b} = \Big[-\frac{\hbar^2}{2m}\frac{\partial^2}{\partial x_b^2} + V(x_b)\Big] K$$

因此 $|\psi(t_b)\rangle = \int K(x_b,t_b;x_a,t_a)\, |\psi(t_a)\rangle\, dx_a$ 與波動力學完全等價。三套表述的關係：路徑積分 ⟺ Schrödinger 方程 ⟺ 矩陣力學。

### 6. 雙縫實驗的「所有路徑」解釋
路徑積分提供了最乾淨的雙縫詮釋：到達屏幕的振幅是**所有路徑**之和：

$$K = \int_{\text{縫1}} \mathcal{D}[x]\, e^{iS/\hbar} + \int_{\text{縫2}} \mathcal{D}[x]\, e^{iS/\hbar}$$

機率 $|K|^2$ 含干涉項——這正是條紋的來源。若在縫旁放置探測器（測量問題），路徑資訊使兩項變得可區分，干涉項被退相干抹除，條紋消失。「粒子同時走所有路」與「波函數疊加」是同一事實的兩種敘事。

### 7. Python Monte Carlo 模擬路徑積分
```python
import numpy as np

hbar, m = 1.0, 1.0
N, npaths = 100, 20000        # 時間切片數、Monte Carlo 樣本數
x_a, x_b, T = 0.0, 1.0, 1.0
dt = T / N

def action(path):
    dx = np.diff(path)
    return np.sum(m * (dx/dt)**2 / 2) * dt   # L = m v^2 / 2

# Monte Carlo: 隨機生成路徑，以 exp(iS/hbar) 加權累加
rng = np.random.default_rng(42)
K = 0.0 + 0.0j
for _ in range(npaths):
    path = x_a + np.cumsum(rng.normal(0, np.sqrt(dt), N))  # 隨機遊走
    path[-1] = x_b
    K += np.exp(1j * action(path) / hbar)
K /= npaths

# 精確解（自由粒子）
K_exact = np.sqrt(m/(2*np.pi*1j*hbar*T)) * np.exp(1j*m*x_b**2/(2*hbar*T))
print(f"Monte Carlo |K| = {abs(K):.4f}")
print(f"Exact       |K| = {abs(K_exact):.4f}")
# 量級相符（Monte Carlo 收斂慢，但驗證了 e^{iS/hbar} 加權的結構）
```

### 8. QED 與 Feynman 圖
路徑積分在 1949–1950 年被 Feynman 推廣到量子電動力學（QED）：對場位形 $\mathcal{D}[A, \psi]$ 求和，微扰展開的每一項對應一張 **Feynman 圖**：

$$Z = \int \mathcal{D}[A]\, \mathcal{D}[\psi]\; e^{i S_{\text{QED}}[A,\psi]/\hbar} = \sum_{\text{diagrams}} (\text{振幅})$$

電子自能、真空極化、電子-光子頂點等圖的求和給出電子反常磁矩 $g-2$，理論與實驗相符至 $10^{-12}$ 精度——物理學史上最精確的驗證。Feynman 圖從此成為粒子物理的計算語言。

## 結案 -- 後果與影響
- **結案**：量子力學有四套等價表述（矩陣、波動、Hilbert 空間、路徑積分）；路徑積分把「最小作用量原理」解釋為量子干涉的極限。
- **QED 完成**：1949 Feynman 圖 + Schwinger/Tomonaga 重整化 ⟹ QED 成為第一個成功的相對論性量子場論，1965 年 Nobel 物理獎。
- **深遠影響**：
  - 量子場論的標準工具：規範場論、瞬子、晶格 QCD、非微扰效應皆以路徑積分為語言。
  - 凝聚態物理：即時（imaginary time）路徑積分 ⟹ 統計力學配分函數 $Z = \int \mathcal{D}[x]\, e^{-S_E/\hbar}$，量子相變、Kondo 問題的解法。
  - 現代計算：晶格 Monte Carlo（QCD 數值模擬）、量子蒙地卡羅方法、甚至金融的期權定價（Feynman–Kac 公式）。
  - Feynman 圖激發了圖論式計算與量子場論代數結構的研究。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Richard Feynman | 偵探，路徑積分與 Feynman 圖的發明者 |
| Paul Dirac | 1933 留下關鍵線索（Lagrangian in QM） |
| Julian Schwinger / Tomonaga | 獨立完成 QED 重整化 |
| Mark Kac | Feynman–Kac 公式（統計力學連結） |

**文獻**
- P. A. M. Dirac, "The Lagrangian in Quantum Mechanics", *Phys. Z. Sowjetunion* **3**, 64 (1933).
- R. P. Feynman, "Space-Time Approach to Non-Relativistic Quantum Mechanics", *Rev. Mod. Phys.* **20**, 367 (1948).
- R. P. Feynman, *Quantum Electrodynamics*（Benjamin, 1961）；Feynman & Hibbs, *Quantum Mechanics and Path Integrals* (1965).
