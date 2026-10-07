# 1925-Heisenberg 矩陣力學

## 案件摘要
1925 年 6 月，24 歲的 Werner Heisenberg 為躲避花粉症獨自到北海的 Helgoland 島，決心拋棄電子軌道等不可觀測的概念，只用可觀測量（躍遷頻率與強度）重建力學。7 月與 Born、Jordan 合作完成「三人論文」，創立矩陣力學——第一套完整、邏輯自洽的量子力學。

## 前因 -- 為什麼會有這個案子
- Bohr 模型與 Sommerfeld 的舊量子論在氫原子之外處處碰壁（氦原子、反常 Zeeman 效應均失敗）。
- 電子軌道無法觀測，躍遷輻射的頻率與強度才是實驗事實——「理論應只建立在可觀測量之上」是 Heisenberg 的方法論信念（深受 Einstein 影響）。
- Kramers 與 Heisenberg 1925 年初的色散理論工作，已出現「躍遷振幅的乘法組合」的雛形。
- 頻率組合原則（Ritz, 1908）早已指出：譜線頻率滿足 $\nu_{nm} = (E_n - E_m)/h$ 的組合規則。

## 線索與推理 -- 數學式、程式、理論

### Umdeutung 論文
1925 年 7 月，*Über quantentheoretische Umdeutung kinematischer und mechanischer Beziehungen*（論運動學與力學關係的量子理論重新詮釋）發表。核心思想：以「躍遷振幅」$X(n,m) \sim e^{i\omega_{nm} t}$ 取代經典座標 $x(t)$，其中

$$
\omega_{nm} = \frac{E_n - E_m}{\hbar}
$$

滿足頻率組合原則 $\omega_{nm} = \omega_{nk} + \omega_{km}$。

### 乘法規則的發現
經典中兩個量的乘積對應 Fourier 分量的乘積；量子版如何相乘？Heisenberg 提出：

$$
X(n,m) = \sum_k X(n,k)\,X(k,m)
$$

這正是**矩陣乘法**的定義！Heisenberg 當時不知道矩陣這個數學物件（矩陣代數當時是純數學冷門領域），只覺得「這種乘法很奇怪」。

### Born–Jordan–Heisenberg 三人論文
Max Born 意識到這是矩陣，與 Jordan、Heisenberg 於 1925 年底發表 *Zur Quantenmechanik II*，建立完整形式體系：

- 座標與動量是無窮維矩陣 $Q, P$；
- 運動方程 $i\hbar\dot{Q} = [Q, H]$，$i\hbar\dot{P} = [P, H]$（Heisenberg 運動方程）；
- 最深處的核心關係——**正則對易關係**：

$$
QP - PQ = i\hbar I
$$

矩陣乘法**不可交換**：$QP \neq PQ$。這是量子世界與經典世界最本質的差異，日後直接引出 Heisenberg 測不準原理 $\Delta x\,\Delta p \geq \hbar/2$。

### 諧振子能階的矩陣力學解
對諧振子 $H = \frac{P^2}{2m} + \frac{m\omega^2 Q^2}{2}$，定義升降算符（矩陣）：

$$
a = \sqrt{\frac{m\omega}{2\hbar}}\left(Q + \frac{i}{m\omega}P\right), \qquad
a^\dagger = \sqrt{\frac{m\omega}{2\hbar}}\left(Q - \frac{i}{m\omega}P\right)
$$

由對易關係可推得 $[a, a^\dagger] = I$、$H = \hbar\omega\left(a^\dagger a + \frac{1}{2}\right)$，能階為

$$
E_n = \hbar\omega\left(n + \frac{1}{2}\right)
$$

零點能量 $\frac{1}{2}\hbar\omega$ 自然浮現——這是舊量子論完全無法給出的。

### Python numpy 驗證矩陣力學
```python
import numpy as np

N = 6                                      # 截斷到 6 個能階
n = np.arange(1, N)
a  = np.diag(np.sqrt(n), 1)                # 降算符矩陣
ad = np.diag(np.sqrt(n), -1)               # 升算符矩陣
I  = np.eye(N)

print("[a, a†] = I ?", np.allclose(a @ ad - ad @ a, I))

hbar, omega, m = 1.0, 1.0, 1.0
Q = np.sqrt(hbar/(2*m*omega)) * (a + ad)
P = -1j * np.sqrt(hbar*m*omega/2) * (a - ad)
H = (P @ P)/(2*m) + (m*omega**2)*(Q @ Q)/2

E = np.diag(H).real[:5]
print("E_n =", E)                          # 期望 [0.5, 1.5, 2.5, 3.5, 4.5]·ħω
print("E_n = ħω(n+1/2) ?", np.allclose(E, hbar*omega*(np.arange(5)+0.5)))
print("QP - PQ = iħI ?", np.allclose(Q @ P - P @ Q, 1j*hbar*I))
```

## 結案 -- 後果與影響
- 判決：量子力學的第一套完整形式誕生。矩陣力學 = 可觀測量 + 不可交換代數。
- 1926 年 Schrödinger 波動力學問世後，Dirac 與 Schrödinger 自己證明兩者數學等價——矩陣力學是波動力學在能量表象的化身。
- 對易關係 $[Q,P]=i\hbar I$ 引出測不準原理、EPR 爭論、以及整個量子測量理論。
- Heisenberg 獲 1932 年諾貝爾物理獎；Born 遲至 1954 年才因統計詮釋獲獎。
- 現代應用：矩陣力學形式是量子計算（量子位元態空間與么正演化）的直接前身。

## 關鍵人物與文獻
- **Werner Heisenberg**（1901–1976），哥廷根/哥本哈根學派。
- **Max Born**（1882–1970）與 **Pascual Jordan**（1902–1980）。
- W. Heisenberg, Z. Phys. 33, 879 (1925)（Umdeutung 論文）。
- M. Born & P. Jordan, Z. Phys. 34, 858 (1925)；M. Born, W. Heisenberg & P. Jordan, Z. Phys. 35, 557 (1926)（三人論文）。
