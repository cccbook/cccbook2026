# 1918 - Noether 定理

## 案件摘要
1918 年，Emmy Noether 在 Göttingen 發表《不變變分問題》（Invariante Variationsprobleme）——**Noether 定理**：

$$\text{每一個連續對稱性} \iff \text{一個守恆律}$$

- **時間平移對稱** ⟺ 能量守恆
- **空間平移對稱** ⟺ 動量守恆
- **旋轉對稱** ⟺ 角動量守恆

**物理學最深刻的原理**——對稱性是守恆律的「原因」。**Einstein 親自為她爭取 Göttingen 的講座**（婦女不能任教！），**抽象代數的誕生**（環論、理想——與 Galois 的群論、Hamilton 的非交換同源的「結構」傳統）。**20 世紀數學與物理的女性先驅。**

## 前因 -- 為什麼會有這個案子
**守恆律的困惑**：牛頓力學（1687，見 `1665-Newton微積分.md`）的守恆律（能量、動量、角動量）——**為什麼守恆**？

- **能量守恆**：能量從哪來、到哪去？——總量不變
- **為什麼**：直覺的解釋（「封閉系統」）不深刻——**沒有數學的原因**

**1915 年廣義相對論的危機**：Einstein 的廣義相對論（見 `1854-Riemann幾何.md`）有**疑難**——廣義協變性（所有座標系等價）下，**能量守恆怎麼辦**？（時空是彎的，能量「消失」？）——Einstein 向 Hilbert 求助，Hilbert 轉介 **Emmy Noether**。

**Noether 的背景**（1882–1935）：Erlangen 數學教授 Max Noether 的女兒——**婦女不能任教**（1908 年才允許「私人講師」、不支薪；Göttingen 的教席被拒——Hilbert 的抗議：「**大學不是澡堂**」）。

## 線索與推理 -- 數學式、程式、理論

### Noether 定理
**陳述**：若作用量 $S = \int L\, dt$（拉格朗日量，見 `1697-Bernoulli最速降線.md`）在某連續變換下**不變**，則存在對應的**守恆量**。

**證明骨架**：變換 $q_i \to q_i + \epsilon \delta q_i$（$\epsilon$ 小），不變性：

$$\delta L = \sum_i \frac{\partial L}{\partial q_i}\delta q_i + \frac{\partial L}{\partial \dot{q}_i}\delta \dot{q}_i + \frac{\partial L}{\partial t}\delta t = \frac{d(\ldots)}{dt}$$

**歐拉–拉格朗日方程**（$\frac{\partial L}{\partial q_i} = \frac{d}{dt}\frac{\partial L}{\partial \dot{q}_i}$）代入——守恆量的導數為零：

$$\frac{d}{dt}\left(\text{守恆量}\right) = 0 \quad \blacksquare$$

**三大守恆律**：

| 對稱性 | 守恆量 |
|--------|--------|
| 時間平移（$t \to t + \epsilon$） | 能量 $E = \sum \dot{q}_i \frac{\partial L}{\partial \dot{q}_i} - L$ |
| 空間平移（$x \to x + \epsilon$） | 動量 $p = \sum \frac{\partial L}{\partial \dot{q}_i}$ |
| 旋轉（$\theta \to \theta + \epsilon$） | 角動量 $L_z = x p_y - y p_x$ |

**深刻之處**：守恆律的**原因**是對稱性——**能量守恆是因為物理定律不隨時間改變**（昨天與今天的 $F = ma$ 相同）——**對稱性是「本質」，守恆律是「現象」**。

### 廣義相對論的能量
**Noether 的第二定理**（同論文）：**規範對稱**（gauge symmetry，座標系的自由）⟺ **恆等式**（如 Bianchi 恆等式）——**廣義相對論的能量守恆的特殊結構**由此解釋——**Einstein 的疑難解決**。

**規範場論的帝國**（Yang–Mills 1954、標準模型）：規範對稱（$U(1), SU(2), SU(3)$）⟺ 守恆荷（電荷、弱荷、色荷）——**粒子物理的全部結構源於 Noether**。

### 程式碼：對稱與守恆

```python
import math, random

# 對稱性 ⟺ 守恆律（數值驗證：諧振子）
def oscillator_simulate(q0, p0, m=1.0, k=1.0, steps=10000, dt=0.001):
    """諧振子：能量守恆（時間平移對稱）"""
    q, p = q0, p0
    energies = []
    for _ in range(steps):
        # 能量 = 動能 + 位能
        E = p*p/(2*m) + k*q*q/2
        energies.append(E)
        # 歐拉–拉格朗日（辛歐拉）
        p += -k*q*dt
        q += p/m*dt
    return energies

random.seed(42)
energies = oscillator_simulate(1.0, 0.0)
print(f"諧振子能量：初始 = {energies[0]:.6f}，終點 = {energies[-1]:.6f}")
print(f"能量漂移 = {abs(energies[-1]-energies[0]):.2e}——守恆 ✓（時間平移對稱）")

# 動量守恆（空間平移對稱）：兩體碰撞
def momentum_conservation():
    """動量守恆：彈性碰撞"""
    m1, m2 = 1.0, 2.0
    v1, v2 = 3.0, -1.0
    p_before = m1*v1 + m2*v2
    # 彈性碰撞後
    v1f = (m1-m2)*v1/(m1+m2) + 2*m2*v2/(m1+m2)
    v2f = 2*m1*v1/(m1+m2) + (m2-m1)*v2/(m1+m2)
    p_after = m1*v1f + m2*v2f
    return p_before, p_after

pb, pa = momentum_conservation()
print(f"\n動量：碰撞前 = {pb}，碰撞後 = {pa}——守恆 ✓（空間平移對稱）")

# Noether 的深刻：對稱是原因，守恆是現象
print("\nNoether 定理（1918）：每一個連續對稱性 ⟺ 一個守恆律")
print("  時間平移 → 能量守恆")
print("  空間平移 → 動量守恆")
print("  旋轉 → 角動量守恆")
print("  規範對稱 → 電荷守恆（規範場論）")
```

### 抽象代數的誕生
**Noether 的第二帝國**：**抽象代數**——

- **環論與理想**：《Idealtheorie in Ringbereichen》(1921)——**交換環的理想**（Kummer 理想數的抽象化，見 `1994-Wiles費馬定理.md` 的 Kummer）
- **環論的公理**：與 Hamilton 的非交換四元數（1843，見 `1843-Hamilton四元數.md`）、Galois 的群論（1832，見 `1832-Galois群論.md`）同源的「結構」傳統
- **Noether 環**：升鏈條件（ACC）——**代數幾何與代數數論的基礎**

**「Emmy Noether 的定理改變了物理，她的環論改變了代數」**——20 世紀數學與物理的雙棲先驅。

### 婦女與數學
**Noether 的悲劇**：
- **不支薪講師**（1908–1915）：Göttingen 拒絕女教席——Hilbert 的抗議「大學不是澡堂」
- **1933 年納粹驅逐**：猶太裔——逃亡美國（Bryn Mawr 女子學院）
- **1935 年逝世**：手術併發症——**53 歲**

**Einstein 的悼詞**：「**Emmy Noether 是自婦女受高等教育以來最重要的創造性數學天才**」——**正名的勝利**（與 Ada Lovelace、Maryam Mirzakhani（Fields 2014，伊朗女數學家）的譜系）。

**偵探筆記**：Noether 的推理是「**對稱 ⟺ 守恆**」——從作用量的不變性推導守恆量。**「為什麼守恆」的深刻答案**——與費馬原理（最短時間，見 `1697-Bernoulli最速降線.md`）、最小作用量同源：**物理的原理是「不變性」**——變分法的語言。

## 結案 -- 後果與影響
- **物理學最深刻的原理**：對稱性 ⟺ 守恆律——能量、動量、角動量、電荷守恆的「原因」。
- **規範場論的基礎**：Noether 第二定理——Yang–Mills（1954）、標準模型（$SU(3)\times SU(2)\times U(1)$）的結構源於對稱。
- **抽象代數的誕生**：環論與理想（1921）——Kummer 理想數的抽象化、代數幾何的基礎（Grothendieck 的概形，見 `1935-Bourbaki結構革命.md`）。
- **廣義相對論的能量**：Noether 解決 Einstein 的疑難——**時空能量守恆的特殊結構**。
- **婦女與數學**：Noether → Mirzakhani（Fields 2014）——**性別平等的數學史**。
- **納粹的災難**：1933 驅逐猶太數學家——**數學人才的流失**（哥廷根學派的終結）。

## 關鍵人物與文獻
- **Emmy Noether**（1882–1935）：Invariante Variationsprobleme (1918)；Idealtheorie in Ringbereichen (1921)
- **David Hilbert / Felix Klein**：Göttingen 的支持者——「大學不是澡堂」
- **Albert Einstein**（1879–1955）：廣義相對論的疑難、Noether 的悼詞
- **Emmy 的影響**：Yang–Mills (1954)、標準模型、抽象代數（Bourbaki 的基礎，見 `1935-Bourbaki結構革命.md`）
- **Maryam Mirzakhani**（1977–2017）：Fields 2014——首位女性 Fields 得主
- 交叉參照：`1697-Bernoulli最速降線.md`、`1854-Riemann幾何.md`、`1843-Hamilton四元數.md`、`1832-Galois群論.md`、`1935-Bourbaki結構革命.md`
