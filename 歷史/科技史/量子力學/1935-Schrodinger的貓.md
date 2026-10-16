# 1935 — Schrödinger 的貓

## 案件摘要
1935 年，Erwin Schrödinger 在回應 EPR 的文章中提出「貓」思想實驗：把微觀的量子疊加透過探測裝置放大到宏觀生物，得到一隻「又死又活」的貓。他用這隻貓控訴哥本哈根詮釋的測量問題：疊加態何時、如何坍縮？現代偵查結論是：**退相干（decoherence）**解釋了疊加為何「看起來」消失，但測量問題的「為何是這一個結果」至今仍是懸案。

## 前因 -- 為什麼會有這個案子
- 1926 年 Schrödinger 提出波動力學；1927 年起哥本哈根詮釋主導：測量前系統處於所有可能結果的疊加，測量瞬間「坍縮」為其中之一。
- 1935 年 EPR 論文激起完備性論戰，Schrödinger 應邀在 *Naturwissenschaften* 連載三篇文章（"Die gegenwärtige Situation in der Quantenmechanik"）。
- 他設計一個極端案例：把 $\sim 10^{23}$ 原子的宏觀物體（貓）綁在單一原子的量子事件上——若疊加原理是普適的，貓必須同時又死又活，這顯然荒謬。

## 線索與推理 -- 數學式、程式、理論

### 1. 案發現場：裝置設計
密閉箱內依序串聯：
1. **放射性原子**：一小時內衰變機率 50%（$\lambda$ = 衰變常數）。
2. **蓋格計數器**：偵測衰變粒子，觸發錘子。
3. **毒氣瓶**：錘子擊破，釋放氫氰酸。
4. **貓**：毒氣釋放則死，否則活。

### 2. 疊加態的數學
設一小時後原子態為 $|\text{decayed}\rangle$ 或 $|\text{intact}\rangle$，則箱內總態（依量子力學線性演化）：

$$|\psi(t{=}1\mathrm{h})\rangle = \frac{1}{\sqrt{2}}\Big(|\text{decayed}\rangle\,|\text{dead}\rangle + |\text{intact}\rangle\,|\text{alive}\rangle\Big)$$

注意這不只是「原子疊加」，而是**原子、探測器、貓全體的糾纏態**（entangled state）——這正是同年 Schrödinger 命名 entanglement 的具體展示。宏觀疊加的極端形式常記為：

$$|\psi\rangle = \frac{1}{\sqrt{2}}\big(|\text{alive}\rangle + |\text{dead}\rangle\big)$$

### 3. 測量問題（Measurement Problem）
三個互相糾結的疑點：
1. **演化有兩套規則**：平時遵守么正演化 $i\hbar\,\dot{|\psi\rangle} = \hat{H}|\psi\rangle$（線性、決定論、可逆）；測量時遵守投影公設（非線性、隨機、不可逆）。兩者何時切換？
2. **切換的判準是什麼**：蓋格計數器算不算「測量」？還是要等「意識」？（Wigner 的朋友）
3. **若沒有坍縮呢**：那貓真的又死又活，但為什麼沒人見過？

### 4. 現代解釋：退相干（Decoherence）
關鍵線索：箱子內外並非孤立，貓與環境（空氣分子、光子、熱輻射）有 $10^{23}$ 以上的自由度耦合。環境像一個「不斷窺探的測量者」。

設 $|E_i\rangle$ 為環境態，總態演化為：

$$\big(\alpha|\text{alive}\rangle + \beta|\text{dead}\rangle\big)|E_0\rangle \;\longrightarrow\; \alpha|\text{alive}\rangle|E_{\text{alive}}\rangle + \beta|\text{dead}\rangle|E_{\text{dead}}\rangle$$

對環境取偏跡，得到貓的約化密度矩陣：

$$\rho_{\text{cat}} = |\alpha|^2|\text{alive}\rangle\langle\text{alive}| + |\beta|^2|\text{dead}\rangle\langle\text{dead}| + \underbrace{\alpha\beta^*\,\langle E_{\text{dead}}|E_{\text{alive}}\rangle}_{\text{干涉項}} |\text{alive}\rangle\langle\text{dead}| + \cdots$$

環境態近似正交：$\langle E_{\text{dead}}|E_{\text{alive}}\rangle \approx e^{-\Gamma t} \to 0$（宏觀系統 $\Gamma$ 極大，退相干時間可短至 $10^{-20}$ 秒）。**干涉項消失**，疊加在實務上「看不出來」——貓呈現經典的統計混合。

> 理論定義（退相干時間）：相干性 $\rho_{ad}(t) = \rho_{ad}(0)\, e^{-t/T_2}$，$T_2$ 為退相干時間；宏觀疊加的 $T_2 \propto (\Delta x)^{-2}$，隨疊加尺度平方急劇縮短。

但注意：退相干**只解釋「為何看不到疊加」**（干涉項消失），**不解决「為何出現這一個結果」**——機率詮釋仍需額外假設（Born 法則）。測量問題的部分仍在偵辦中。

### 5. 量子位元中的體現
貓的困境在量子計算中化為資源。單一量子位元（qubit）的疊加：

$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle, \qquad |\alpha|^2 + |\beta|^2 = 1$$

$|\alpha\rangle, |\beta\rangle$ 相當於「活/死」的微觀版本；n 個量子位元的疊加空間維度為 $2^n$，這是量子平行計算的來源。但退相干正是量子計算的最大敵人——量子位元的 $T_1/T_2$ 時間決定了可執行的電路深度，量子糾錯（surface code）是現代對策。

### 6. Python 模擬：退相干過程
```python
import numpy as np

I = np.eye(2, dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)   # |alive> - |dead> 方向
alive = np.array([1, 0], dtype=complex)

def dephasing_rho(t, alpha, T2=1.0):
    """貓的約化密度矩陣在 dephasing 通道下演化"""
    rho0 = (alpha*alive + np.sqrt(1-alpha**2)*np.array([0,1],dtype=complex))
    rho = np.outer(rho0, rho0.conj())
    phi = np.exp(-t/T2)                      # 干涉項衰減因子
    # Kraus 算符: K1 = sqrt((1+phi)/2) I, K2 = sqrt((1-phi)/2) Z
    K1 = np.sqrt((1+phi)/2)*I; K2 = np.sqrt((1-phi)/2)*sz
    return K1 @ rho @ K1.conj().T + K2 @ rho @ K2.conj().T

alpha = 1/np.sqrt(2)  # 又死又活的等權疊加
for t in [0, 0.5, 2.0, 10.0]:
    rho = dephasing_rho(t, alpha)
    coh = abs(rho[0, 1])
    print(f"t={t:5.1f}  P(alive)={rho[0,0].real:.3f}  |干涉項|={coh:.4f}")
# t=0   干涉項=0.5（完整疊加）→ t=10 干涉項≈0（經典混合，貓「看起來」非死即活）
```

## 結案 -- 後果與影響
- **部分結案**（1980s–）：Zurek、Zeh 等人以退相干理論說明宏觀疊加在實務上不可觀測，「貓態」被環境瞬間「窺探」而成為經典混合；preferred basis（pointer basis）問題也獲得解釋。
- **仍未結案**：退相干不產生單一結果——「為何是這一次測量得到死？」仍需詮釋補充（Copenhagen、many-worlds、QBism、objective collapse/GRW 各執一詞）。
- **深遠影響**：
  - 「貓態」（cat state）成為實驗物理的正式目標：SQUID 中的宏觀電流疊加（2000）、離子阱、光學腔中的貓態已逐一實現。
  - 退相干理論直接催生量子資訊工程：量子位元相干時間 $T_1/T_2$、量子糾錯、退相干抑制都是它的工程化產物。
  - Schrödinger 的貓從「荒謬的反例」變成「量子與經典邊界的偵探藍圖」。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Erwin Schrödinger | 提出貓思想實驗，控訴測量問題 |
| Niels Bohr | 哥本哈根詮釋的被控訴方 |
| H. Dieter Zeh | 1970 提出退相干概念 |
| Wojciech Zurek | 1980s 系統化退相干與 pointer basis |
| Einstein | 貓實驗的啟發者（EPR 論戰） |

**文獻**
- E. Schrödinger, "Die gegenwärtige Situation in der Quantenmechanik", *Naturwissenschaften* **23** (1935).
- H. D. Zeh, *Found. Phys.* **1**, 69 (1970).
- W. H. Zurek, "Decoherence, einselection, and the quantum origins of the classical", *Rev. Mod. Phys.* **75**, 715 (2003).
- J. R. Friedman et al., *Nature* **406**, 43 (2000)（SQUID 貓態實驗）.
