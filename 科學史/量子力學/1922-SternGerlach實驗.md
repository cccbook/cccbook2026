# 1922 - Stern–Gerlach 實驗

## 案件摘要
1922 年，Stern 與 Gerlach 讓銀原子束通過非均勻磁場，發現原子束分裂為**兩條**而非連續分佈——「空間量子化」首次被直接觀測，但當時無人能解釋為何只有兩條，這個謎為 1925 年電子自旋鋪路。

## 前因 -- 為什麼會有這個案子
- **1913 年 Bohr 模型**雖成功解釋氫光譜，但「電子軌道在空間中是否取離散方向」純屬假設。
- **Sommerfeld（1916）** 引入空間量子化 $m_l$ 量子數解釋 Zeeman 效應——但從未被直接觀測。
- **Stern（1921）** 設計實驗：用銀原子束檢驗空間量子化，並測量 Bohr 磁子的真偽。
- 經典物理預測：原子磁矩方向隨機連續分佈，原子束應展開為**連續帶**。

## 線索與推理 -- 數學式、程式、理論

### 線索一：磁矩與非均勻磁場中的力
原子帶有磁矩 $\vec{\mu}$（來自電子軌道運動）。在**均勻**磁場中只受力矩（進動），無平移力；但在**非均勻**磁場中，磁矩不同取向受到不同大小的力：

$$
F_z = \nabla(\vec{\mu} \cdot \vec{B})\Big|_z \approx \mu_z \frac{\partial B_z}{\partial z}
$$

其中 $\mu_z$ 是磁矩在 $z$ 方向的分量。若 $\mu_z$ 連續分佈 → 原子束連續展開；若 $\mu_z$ 離散 → 原子束分裂為分立線。

**Bohr 磁子**：

$$
\mu_B = \frac{e\hbar}{2m_e} = 9.274\times 10^{-24}\,\text{J/T}
$$

### 線索二：Stern–Gerlach 裝置與驚人結果
**裝置**：銀原子在爐中蒸發 → 狹縫準直成束 → 通過強度大、梯度陡的非均勻磁場（$\partial B_z/\partial z \sim 10\,\text{T/m}$，磁場長 3.5 cm）→ 沉積在冷凝板上（玻璃板上的銀膜呈可見影像）。

**實驗結果（1922 年 2 月）**：
- 經典預測：連續的橢圓形銀斑。
- 實際觀測：**兩條清晰分離的銀線**！

偏移量估算：原子在磁場中飛行時間 $t = L/v$，橫向位移

$$
z = \frac{1}{2}\frac{F_z}{m_{Ag}} t^2 = \frac{1}{2}\frac{\mu_z}{m_{Ag}}\frac{\partial B_z}{\partial z}\left(\frac{L}{v}\right)^2
$$

代入 $\mu_z \sim \mu_B$、$v \sim 500\,\text{m/s}$、$L \sim 3.5\,\text{cm}$，得 $z \sim 0.1\,\text{mm}$——恰好可觀測。實驗測得的分裂量也證實磁矩大小約為 $1\,\mu_B$（Bohr 磁子存在）。

### 推理一：空間量子化被證實，但藏著謎
由 Sommerfeld 量子化，軌道角動量 $l$ 的 $z$ 分量取 $2l+1$ 個值：

$$
\mu_z = -m_l \mu_B, \quad m_l = -l, -l+1, \dots, l
$$

問題：銀原子基態應該是 $l = 1$（依當時理解），預測 $2(1)+1 = 3$ 條線（$m_l = -1, 0, +1$）——但實驗只有**兩條**！

### 推理二：$l = 0$ 卻有兩條線之謎
Stern 與 Gerlach 當時無法解釋。謎底要等到量子力學完備之後：

- 依 **Schrödinger 方程（1926）** + Pauli 不相容原理，銀原子 47 個電子中，46 個填滿內殼層（軌道角動量兩兩抵消），最外層 $5s$ 電子處於 **$l = 0$** 態——軌道磁矩為零，$m_l$ 只有 1 個值（0），按軌道理論應只有**一條線**（不偏折）！
- 實驗卻有兩條——唯一解釋：這個未配對電子擁有一種全新的、內禀的自由度——**電子自旋** $s = 1/2$，其 $z$ 分量只有兩個值：

$$
m_s = \pm\frac{1}{2} \;\Rightarrow\; \mu_z = \pm g_s \mu_B m_s \approx \pm\mu_B
$$

（電子 $g$ 因子 $g_s \approx 2$，故自旋磁矩大小恰為一個 Bohr 磁子。）兩條線 = 自旋向上 vs 向下。

1925 年 **Uhlenbeck 與 Goudsmit** 提出電子自旋假說，Pauli 以二分量波函數（Pauli 矩陣）形式化——Stern–Gerlach 的謎團結案。

### 程式驗證：經典連續 vs 量子兩條分線

```python
import numpy as np
import matplotlib.pyplot as plt

muB = 9.274e-24
mAg, L, dBdz = 1.79e-25, 0.035, 10.0
v = np.random.normal(500, 50, 20000)      # 原子速度分佈
t = L / v
z_classic = 0.5 * (muB*np.random.uniform(-1,1,len(v))/mAg) * dBdz * t**2
z_quantum = 0.5 * (np.random.choice([-1,1],len(v))*muB/mAg) * dBdz * t**2

plt.figure(figsize=(8,4))
plt.subplot(1,2,1)
plt.hist(z_classic*1e3, bins=80, color='gray')
plt.title('Classical: continuous band'); plt.xlabel('z (mm)')
plt.subplot(1,2,2)
plt.hist(z_quantum*1e3, bins=80, color='steelblue')
plt.title('Quantum: two spots (spin up/down)'); plt.xlabel('z (mm)')
plt.tight_layout(); plt.show()
```

執行結果：左圖（經典隨機 $\mu_z$）是單一連續帶；右圖（$\mu_z = \pm\mu_B$）分裂為兩條——與 Stern–Gerlach 實驗影像一致。

### 結案推理：量子測量的原型
以量子力學語言重述：SG 實驗是對自旋態的**測量**。測量算符 $S_z$ 的本徵值只有 $\pm\hbar/2$，任何輸入態都被「投影」到兩個本徵態之一：

$$
|\psi\rangle = \alpha|{\uparrow}\rangle + \beta|{\downarrow}\rangle
\;\xrightarrow{\;S_z \text{ 測量}\;}\;
|{\uparrow}\rangle \;(\text{機率 } |\alpha|^2) \;\text{或}\; |{\downarrow}\rangle \;(\text{機率 } |\beta|^2)
$$

級聯 SG 實驗（再串一個旋轉 90° 的磁場）更顯示測量的不可逆投影性——這成為**量子測量問題**與量子資訊（量子位元 qubit $|0\rangle, |1\rangle$）的原型。

## 結案 -- 後果與影響
- 空間量子化首次被直接證實；「兩條線之謎」由 1925 電子自旋結案。
- 自旋成為一切粒子（電子、質子、中子）的基本性質；Pauli 不相容原理（1925）→ 元素週期表的量子解釋 → 化學鍵理論。
- Stern–Gerlach 裝置成為量子測量的教科書原型：qubit 的物理實現、量子退相干實驗、分子束技術皆源於此。
- Stern 得 1943 年諾貝爾獎（分子束方法與質子磁矩）；Gerlach 因二戰角色未獲獎。
- 深遠影響：SG 實驗證明「測量會改變系統」——哥本哈根詮釋的核心證據。

## 關鍵人物與文獻
- **O. Stern & W. Gerlach**：Zeitschrift für Physik 8, 110 (1922)；9, 349 (1922)；Stern 諾貝爾獎 1943。
- **G. Uhlenbeck & S. Goudsmit**：Naturwissenschaften 13, 953 (1925)（電子自旋假說）。
- **W. Pauli**：Zeitschrift für Physik 31, 765 (1925)（不相容原理）；諾貝爾獎 1945。
- **A. Sommerfeld**：空間量子化（1916）。
