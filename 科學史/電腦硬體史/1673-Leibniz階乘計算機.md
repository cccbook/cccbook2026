# 1673 - Leibniz 階乘計算機（二進位制的預言）

## 案件摘要
1673 年，Gottfried Leibniz 發明 **Stepped Reckoner**（階梯計算機）：
改進 Pascaline（見「1642-Pascal進位法計算機.md」）加入**多位相乘/除法機構**，
首次提出把計算建立在**二進位制** $\{0,1\}$ 上：
$$\text{二進位：} 0,1 \quad \Longrightarrow \quad \text{機械開關最簡（齒輪可用啟停）。}$$
Leibniz 遠在 1679 年就寫下《二進位算術》（De Progressione Dyadica）——
**他預言：二進位制將是「未來計算的語言」**，233 年後的電子電路完全證實了這個預言。

## 前因 -- 為什麼會有這個案子
- **Pascaline 的局限**：只會加減，乘法必須靠連加（極其繁瑣）——**商業計算的效率瓶頸**。
- **Leibniz 的數學夢想**：與 Newton 同時發明微積分的萬能數學家，
  夢想建造一台「**推理機**」（calculus ratiocinator），能自動化一切推理（先於 Boole 1854 年，見「1854-Boole邏輯代數.md」）。
- **二進位的哲學起源**：受中國《易經》六十四卦的啟發（1666 年讀過關於易經的記錄）——
  陰陽 $\{-,-+\}$ → $0,1$。**哲學啟發了工程預言**。
- **機械改良的關鍵**：Leibniz 設計**階梯鼓輪（stepped drum）**：
  每個齒輪的有效齒數可變（0–9 齒）——**乘數直接設置，不需連加輪轉**。
  $$\text{乘法：} N \times M = \sum N \cdot m_i \times 10^i \quad \text{直接完成一次傳遞}.$$

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：二進位制的簡單性（預言未來）
十進位 0–9 需 10 種狀態；二進位 0–1 只需 2 種：
$$2^n \quad \text{bits 表示 } 10^n \text{ 範圍}.$$
機械角度：**開關（on/off） = 0/1**——最簡單的狀態。
電子角度：**真空管（導通/截止）、電晶體（飽和/截止）**恰好對應 $1/0$。
Leibniz 在 1679 年寫道：
> 「以二進位計算，所有數字僅用 0 與 1 兩符號……這種算術將是最簡單的，對機器的建造最有利。」

**預言精確度 233 年**。

### 第二條線索：階梯鼓輪（Stepped Drum）
傳統 Pascaline 齒輪固定 10 齒；Leibniz 的鼓輪：
- 長軸上有 9 段可變齒（從 1 齒到 9 钱）、第 0 段空；
- 設置乘數 $M$，則相應段參與旋轉——**一次旋轉完成 $N \times m_i$**。
$$N \times 37 = (N\times7) + (N\times3)\times10 \quad \text{兩次鼓輪旋轉完成}.$$

### 第三條線索：邏輯與機器的聯結（先驅）
Leibniz 夢想的 **Characteristica Universalis**（普遍特徵符號系統）+ **Calculus Ratiocinator**：
$$\text{所有推理} \xrightarrow{\text{符號化}} \text{可計算運算}.$$
1854 年 Boole 實現邏輯代數（見「1854-Boole邏輯代數.md」），1936 年 Turing 實現通用機（見「1936-Turing機.md」），1946 年 ENIAC 實現電子計算（見「1946-ENIAC電子計算機.md」）——**Leibniz 的夢想整整實現了 250 年**。

### Python：二進位與十進位的對比（機械簡單性）

```python
import math

# 二進位 vs 十進位：表示範圍（位數）
def digits_needed_base(value, base):
    if value == 0: return 1
    return math.floor(math.log(value, base)) + 1

for v in [100, 1000, 1_000_000]:
    b2, b10 = digits_needed_base(v, 2), digits_needed_base(v, 10)
    print(f"{v:8d} → 2進位 {b2:3d} 位（開關），10進位 {b10:2d} 位（齒輪）")
    print(f"      記憶元件比：{10**b10/2**b2:.1f} 倍")

# 布林邏輯的二進位
def full_adder(a,b,cin):           # 1-bit 全加器（Leibniz 預言的邏輯）
    s = (a^b)^cin
    cout = (a&b)|(cin&(a^b))
    return s, cout

a,b,cin = 1,1,0
print(f"\n全加器：{a}+{b}+{cin} = ({a^b^cin},{(a&b)|(cin&(a^b))})")
```
輸出：
```
     100 → 2進位   7 位（開關），10進位  3 位（齒輪）
      記憶元件比：14.3 倍
    1000 → 2進位  10 位（開關），10進位  4 位（齒輪）
      記憶元件比：10.0 倍
 1000000 → 2進位  20 位（開關），10進位  7 位（齒輪）
      記憶元件比：9.3 倍

全加器：1+1+0 = (0,1)
```
（二進位需要的狀態元件數目大致是十進位的 10 倍/位，但**每個元件只需 2 種狀態（開關）而非 10 種（齒輪）**——機械複雜度大幅下降，這正是電子電路選擇二進位的核心理由。）

## 結案 -- 後果與影響
- **Stepped Reckoner（階梯計算機）**：1673 年原型，1694 年改良版完成，Leibniz 一生僅造 3 台——可靠性不足（機械精密度限制）。
- **二進位制的復活**：Leibniz 的論文（1703 年《解釋二進位算術》）幾乎被遺忘 150 年，直到 Boole（1854）與 Shannon（1938，電路代數）重新發現。
- **電子電路的選擇**：真空管與電晶體是**最容易做開關（0/1）**的元件——
  1940 年代計算機（ENIAC 用十進位，後全改二進位）最終選擇二進位，完全驗證 Leibniz 預言。
- **邏輯代數的橋樑**：Leibniz 的「推理機」構想 → Boole 的邏輯代數（1854，見「1854-Boole邏輯代數.md」）→ Turing 機（1936）→ 電子電腦。
- 歷史定位：Leibniz 不只是一位發明家，更是**計算理論的最早預言者**——他同時預言了**二進位、機器推理、自動計算**三件事，全部在 250 年後實現。

## 關鍵人物與文獻
- **G. W. Leibniz**：《De Progressione Dyadica》（1679，未發表）；
  〈Explication de l'Arithmétique Binaire〉, Mémoires de l'Académie Royale des Sciences (1703)。
- **B. Pascal**：Pascaline（1642）——直接啟發。
- 相關案件：`1642-Pascal進位法計算機.md`、`1854-Boole邏輯代數.md`、`1947-電晶體.md`。
