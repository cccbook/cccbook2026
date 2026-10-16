# 1946 - ENIAC 電子計算機（電子時代的第一聲雷）

## 案件摘要
1946 年 2 月 14 日，世界上第一台通用電子數位計算機 **ENIAC**（Electronic Numerical Integrator and Computer）正式問世：
$$18000 \text{ 顆電子管} \quad 30 \text{ 噸} \quad 150\ \text{kW} \quad 5000 \text{ 次/秒（加法）}.$$
ENIAC 首次實現了電子速度的計算（真空管開關 $\sim10^6$ Hz 對比繼電器 $10^3$ Hz），
是**從 Babbage 的機械到電子時代的分水嶺**。但 ENIAC 是「plugboard + 開關設定式」的機器——
**尚未儲存程式**；1950 年代的 EDVAC、Manchester Baby、IBM 704 才是**真正的存儲程式電腦**。

## 前因 -- 為什麼會有這個案子
- **二戰的數字需求（1941–1945）**：
  1. **破譯密碼**：Enigma、Bombe、 Colossus（1943）——統計數字計算需求爆增。
  2. **彈道計算**：炮兵計算表的規模，已超出人工表格計算能力。
  3. **核物理**：中子擴散方程（Monte Carlo 方法，1946，von Neumann）——數千小時的計算。
- **真空管的誕生（1904–1940）**：Fleming 二極管（1904）、Armstrong 五極管（1916）、**de Forest 三極管（1906）**——
  電子管可做**開關（on/off）**與**放大**，開關速度 $\sim 10^6$ Hz（毫秒級反應）——
  **電子速度是真空管帶來的**。
- **Mauchly 與 Eckert 的突破（1943–1946）**：
  - **Mauchly**（天主教大學）+ **Eckert**（陸軍ordinate Corps）於 1943–1944 年在**賓州大學**設計 ENIAC。
  - **J. Presper Eckert** 提煉核心創新：**平行累加器（parallel accumulators）**——
    10 個十進位累加器，**一次完成 10 位數的加法**（而非逐位串接）。
  $$\text{ENIAC 加法速度} = 10000\ \text{次/秒} \quad (\text{vs. 人工 } \sim 5\ \text{次/秒，差距 }2000\times).$$

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：十進位 vs 二進位（ENIAC 的先天缺陷）
ENIAC 使用**十進位**（10 個累加器，每次計算十進位）。缺點：
- 需要大量**進位電路**（10 進位 → 複雜）；
- 儲存數位需要 10 個真空管（二進位只需 2 個）——**真空管數量爆炸**；
- 程式設定需**插線板（plugboard） + 旋鈕設定**——**無法儲存程式**。
$$\text{二進位儲存 1 bit} = 2 \text{ 真空管} \quad \text{vs} \quad \text{十進位儲存 1 digit} = 10 \text{ 真空管}.$$

### 第二條線索：ENIAC 的架構（10 個累加器 + 離散緩衝）
ENIAC 的計算核心（20 個十進位累加器，每個可存 10 位）：
$$\text{ACC}_{i} \in \{0,\ldots,9999999999\}\ \ (\text{10 位十進位}).$$
- **分散式記憶體**：ENIAC 有 20 個累加器（ACC）+ 離散 function tables。
- **控制器**：順序控制單元（Master Programmer）——插線板設定指令序列。
- **儲存程式缺失**：程式（指令）= 插線板連接，**不是記憶體中的資料**——換程式要重新插線（數天）。

### 第三條線索：積累器的十進位進位（ENIAC 的算術核心）
一個累加器的加法操作 = **逐位進位**：
$$\text{ACC}_i \mathrel{+}= \text{X}_i \ \ (\text{其中 } X_i \text{ 為指令指定的輸入}).$$
每次操作需完成 10 個**十進位加 1** 的連鎖進位：
$$9 + 1 + \text{進位} = 10 \ \text{→ 產生進位} \ \text{往下一位}.$$
10 位進位鏈在 1946 年需 $\sim 10\ \mu\text{s}$（真空管開關延遲）。

### Python：ENIAC 的十進位累加器與進位鏈模擬

```python
class ENIAC_Accumulator:
    """ENIAC 十進位累加器（10 位）+ 進位鏈"""
    def __init__(self):
        self.digits = [0]*10      # 十進位 10 位累加器

    def clear(self):
        self.digits = [0]*10

    def add(self, value):
        """十進位加法 + 進位鏈"""
        carry = 0
        for i in range(10):
            s = self.digits[i] + (value % 10) + carry
            self.digits[i] = s % 10
            carry = s // 10
            value //= 10
        return self  # ENIAC 允許 chain

    def __repr__(self):
        return "ACC = " + "".join(map(str, reversed(self.digits)))

acc = ENIAC_Accumulator()
acc.add(1234567890)
print(acc)                     # 累加 1234567890
acc.add(9876543210)
print(acc, "（10 位溢出，最高位進位被丟棄）")

# 進位鏈逐位展示（9876543210 + 1234567890 = 11111111100 → 10 位 = 1111111100）
a, b = 9876543210, 1234567890
carry, digits = 0, []
for i in range(10):
    da, db = (a//10**i)%10, (b//10**i)%10
    s = da + db + carry
    digits.append(s % 10)
    carry = s // 10
print("進位鏈結果:", "".join(map(str, reversed(digits))), f"進位={carry}")
```
輸出：
```
ACC = 1234567890
ACC = 1111111100 （10 位溢出，最高位進位被丟棄）
進位鏈結果: 1111111100 進位=1
```
（11 個 1 = 11111111100 需 11 位；ENIAC 的 10 位累加器溢出最後一個 1——
**正是當時十進位設計的侷限**，後來 von Neumann 力推「改用二進位」直接解決了此問題。）

## 結案 -- 後果與影響
- **歷史地位（1946）**：ENIAC 是**第一台通用電子數位計算機**——正式開啟電子計算時代；
  它的六位女研究員Kathleen Antonucci 曾計算第一顆氫彈的臨界質量。
- **ENIAC 的缺陷促成了三個重要軟體工程**：
  1. **Stored Program（存儲程式，1945 von Neumann）**：EDSAC、Manchester Baby（1948）、
     EDVAC（1949）——**程式存進記憶體**，換程式不用插線。
  2. **Mary Lee Berners-Lee 寫出第一批 ENIAC 程式（1946）**：從畫線圖到「跳線設置」的程式工具。
  3. **貴族式編程問題**：ENIAC 程式須「設定插線板 + 開關」，需六位數學家專職設定 20 條電纜——
     催生了 1940s-50s 的「程式設計師」職業，**啟發了 Brooks《No Silver Bullet》(1986)**。
- **軟體危機的源頭**：ENIAC → 硬體快速演進，軟體慢（手工編寫）→ 1968 年 NATO **「軟體危機」**——
  **硬體史的副作用催生了軟體工程學科**。
- **電子管時代的技術曲線**：ENIAC 18000 管 → 1950s 進步到 1000 管 → 1959 年 **IC（積體電路，見「1958-積體電路.md」）** 取代電子管。
- **歷史定位**：ENIAC 是一聲「電子時代的第一聲雷」——驗證了電子開關能實現算術，
  開啟了電腦的四個時代：**電子管 → 電晶體 → 積體電路 → 奈米**（見「2020-EUV與先進製程.md」）。

## 關鍵人物與文獻
- **J. P. Eckert**、**J. Mauchly**：ENIAC 設計 (1943–1946)。
- **J. von Neumann**：存儲程式架構（EDVAC 報告，1945）；Monte Carlo 方法。
- **M. L. Berners-Lee**：ENIAC 早期程式設計（1946）。
- **A. Turing**：Turing-Welchman Bombe (1939–1945)、Colossus（破譯密碼，非 ENIAC）。
- 相關案件：`1854-Boole邏輯代數.md`、`1936-Turing機.md`、`1947-電晶體.md`、`1958-積體電路.md`。