# 1545 - 卡爾達諾三次方程

## 案件摘要
1545 年，米蘭的 Girolamo Cardano 出版《大術》（Ars Magna）：發表三次方程的根式解——**但這個解揭開了一個數學怪物**：即使實根存在，中間步驟被迫出現「負數的平方根」$\sqrt{-121}$。Bombelli（1572）給它命名「虛數」並規定運算規則——**複數從三次方程的「不情願的產物」成為數學的核心**。一場三人恩怨（Tartaglia、Cardano、Ferrari）伴隨這個發現——數學史上最戲劇性的優先權之爭。

## 前因 -- 為什麼會有這個案子
16 世紀的義大利：數學家的地位靠**公開比賽**——解出對方出不了的題目，贏得聲望與職位。二次方程已解（花拉子米，見 `0820-Khwarizmi代數學.md`），**三次方程**是聖杯：

$$x^3 + ax + b = 0$$

**競賽**：
- 1515 年 Scipione del Ferro 解出 $x^3 + ax = b$ 型（死前傳給學生 Fior）
- 1535 年 Tartaglia（口吃者）宣稱解出所有三次型——Fior 挑戰失敗
- 1539 年 Cardano 誓不外洩，騙得 Tartaglia 的解法（以暗語詩的形式）
- 1543 年 Cardano 發現 del Ferro 早已解出——**誓約無效**，1545 年出版《大術》（並註明 del Ferro 與 Tartaglia 的貢獻）
- Tartaglia 暴怒——**優先權之爭**，學生 Ferrari 又解出四次方程

## 線索與推理 -- 數學式、程式、理論

### Cardano 公式
三次方程 $x^3 + px + q = 0$（先消去二次項）的解：

$$x = \sqrt[3]{-\frac{q}{2} + \sqrt{\frac{q^2}{4} + \frac{p^3}{27}}} + \sqrt[3]{-\frac{q}{2} - \sqrt{\frac{q^2}{4} + \frac{p^3}{27}}}$$

**方法（Tartaglia 的洞察）**：設 $x = u + v$，代入：

$$u^3 + v^3 + (3uv + p)(u + v) + q = 0$$

令 $3uv = -p$（消去中間項）且 $u^3 + v^3 = -q$——化為二次方程解 $u^3, v^3$，再開三次方根。

### 卡丹諾怪物（casus irreducibilis）
**驚人的案例**：$x^3 = 15x + 4$（即 $x^3 - 15x - 4 = 0$）——明顯有實根 $x = 4$（$64 = 60 + 4$）。

但套公式：

$$\sqrt{\frac{q^2}{4} + \frac{p^3}{27}} = \sqrt{4 - 125} = \sqrt{-121}$$

**負數的平方根**！公式「失效」——但實根明明存在。

**Bombelli 的解法（1572）**：硬著頭皮運算 $\sqrt{-121} = 11i$（「plus of minus」）：

$$\sqrt[3]{2 + 11i} = 2 + i, \quad \sqrt[3]{2 - 11i} = 2 - i \implies x = (2+i) + (2-i) = 4 \quad \checkmark$$

**虛數「不是實的」，但運算規則自洽**——$(a+bi)(c+di) = (ac-bd) + (ad+bc)i$。

**深遠的定理（後來的發現）**：casus irreducibilis 中，**三個實根無法用實數根式表示**——虛數的出現**不可避免**。**實數問題被迫穿越虛數王國**——這個定理（Wantzel 1843 證明）證明虛數不是「技巧」，是**必經之路**。

### 程式碼：Cardano 公式與虛數

```python
import cmath, math

def cardano(p, q):
    """三次方程 x^3 + px + q = 0 的 Cardano 解"""
    disc = q*q/4 + p**3/27
    u = (-q/2 + cmath.sqrt(disc)) ** (1/3)
    v = (-q/2 - cmath.sqrt(disc)) ** (1/3)
    return u + v

# 卡丹諾怪物：x^3 = 15x + 4，實根 x = 4
x = cardano(-15, -4)
print(f"x = {x}")                       # (4+1.1e-16j) ≈ 4——中間出現 sqrt(-121)！
print(f"中間量 sqrt(-121) = {cmath.sqrt(-121)}")   # 11j：虛數被迫出現

# 驗證：x = 4 是實根
print(f"4^3 = 15*4 + 4：{64 == 15*4 + 4}")

# 三個實根（casus irreducibilis）：都存在，但根式中間必經虛數
roots = [cmath.sqrt(64/4 + (-15)**3/27) * cmath.exp(2j*math.pi*k/3) for k in range(3)]
print(f"判別式 < 0：三個實根，根式解必經虛數王國")
```

### 四次與五次：譜系
- **Ferrari（1545）**：四次方程解（化為三次）
- **五次方程**：懸案 250 年——Abel（1824，見 `1824-Abel五次方程.md`）證明**無根式解**，Galois（1832，見 `1832-Galois群論.md`）給出判準
- **代數基本定理**：Gauss（1799，見 `1799-Gauss代數基本定理.md`）——$n$ 次方程在複數域中必有一根（**虛數是完整的**）

## 結案 -- 後果與影響
- **虛數的誕生**：從「不情願的技巧」到「數學核心」——Euler（1748，見 `1748-Euler公式.md`）的 $e^{i\pi}+1=0$、Argand 平面、複變函數論。
- **優先權之爭的教訓**：數學的優先權文化——公開發表 vs 誓約保密（Cardano 的出版雖不光榮，卻讓知識傳播）。
- **casus irreducibilis 的定理**：實根無法用實數根式表示——虛數的不可避免性（Wantzel 1843）。
- **五次方程的懸案**：Cardano 公式的成功引發「五次能否也解」——250 年的攻擊最終證明**不可能**（Abel–Ruffini 定理）。
- **代數基本定理**：複數域的代數封閉性——虛數從怪物變成「更大的家」。

## 關鍵人物與文獻
- **Scipione del Ferro**（1465–1526）：最早解三次方程（未發表）
- **Niccolò Tartaglia**（1500–1557）：1535 獨立解出、暗語詩傳給 Cardano
- **Girolamo Cardano**（1501–1576）：Ars Magna (1545)——醫生、賭徒、數學家
- **Lodovico Ferrari**（1522–1565）：四次方程
- **Rafael Bombelli**（1526–1572）：Algebra (1572)——虛數的運算規則
- 交叉參照：`0820-Khwarizmi代數學.md`、`1799-Gauss代數基本定理.md`、`1824-Abel五次方程.md`、`1832-Galois群論.md`、`1748-Euler公式.md`
