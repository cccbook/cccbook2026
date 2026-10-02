# 1998 - Hales Kepler 猜想

## 案件摘要
1998 年，Thomas Hales（與博士生 Ferguson）宣布證明**克卜勒猜想**（Kepler conjecture，1611）：**等大球體積的最密堆積是面心立方（FCC）堆積**——密度 $\pi/\sqrt{18} \approx 74.05\%$，即水果攤堆橘子的方式。證明依賴**150 頁人類推理 + 3 GB 電腦運算**（數百種局部堆積的線性規劃檢驗）——**與四色定理（1976，見 `1976-四色定理.md`）同源的第二個電腦證明**。審查 6 年仍未完成（《Annals》99% 確信但 100% 保留）——**2014 年 Hales 的 Flyspeck 計畫用 Coq/Isabelle 完全形式化**，可檢驗性恢復。**1611 年的物理問題 → 1998 年的電腦證明 → 2014 年的形式化**——387 年的譜系。

## 前因 -- 為什麼會有這個案子
**1611 年**，Johannes Kepler（見 `1665-Newton微積分.md` 的 Kepler 三定律）在寫給朋友的新年禮物小冊《論六角雪花》（Strena seu de nive sexangula）中提出：

> 等大的球，怎麼堆最密？——**面心立方（FCC）**：密度 $\pi/\sqrt{18} \approx 74.05\%$

**觀察的來源**：水果攤的橘子堆（**商人的直覺**）、六角雪花的對稱、蜂巢的六角形——**自然界的最佳堆積**。

**陳述**：任何等大球的堆積，密度 $\le \pi/\sqrt{18}$：

$$\delta = \frac{\text{球體積}}{\text{包圍體積}} \le \frac{\pi}{\sqrt{18}} = 0.74048\ldots$$

**387 年的攻擊**：
- **Newton vs Gregory（1694）**：證明局部最優（12 個鄰球）——但局部 ≠ 全域
- **Gauss（1831）**：證明**格堆積**（lattice packing）中最密——**但非格堆積**（不規則堆積）仍懸
- **Hilbert 第 18 問題**（1900，見 `../計算理論/1900-Hilbert23問題.md`）：堆積的分類——Fejes Tóth（1940）證明 2D 的最密（六角堆積 $\pi/\sqrt{12} = 90.7\%$）
- **Fejes Tóth（1953）**：提出「**用電腦檢驗有限類型**」的策略——**Hales 的藍圖**

## 線索與推理 -- 數學式、程式、理論

### 局部化：Voronoi 分解
**核心想法（Fejes Tóth → Hales）**：堆積的密度 = 局部密度的平均——**把堆積分解成局部結構**：

1. **Voronoi 胞**（Voronoi cell）：每個球的「勢力範圍」（到該球比到其他球近的點集）
2. **局部密度**：$\delta_{cell} = V_{球}/V_{胞}$——**胞越小越密**
3. **全域密度 = 局部密度的平均**——**證明每個胞的密度 $\le \pi/\sqrt{18}$（或被鄰居補償）**

**Hales 的計算**：胞的形狀分類為**數百種類型**，每種用**線性規劃**（LP）檢驗上界——**150 頁人類推理 + 3 GB 電腦**。

### 線性規劃的檢驗
**數學**：每個胞的上界化為 LP：

$$\max \delta_{cell} \quad \text{s.t. 球不重疊的約束（線性不等式）}$$

**LP 的對偶性**：用對偶問題的**可行解**（證書）驗證上界——**電腦算出的證書**是可檢驗的（與 Fourier–Motzkin 消去、單純形法 1947 的對偶同源）。

**證明的結構**：

$$\text{分類胞的類型} + \text{每類型的 LP 上界} + \text{平均的補償} \implies \delta \le \frac{\pi}{\sqrt{18}} \quad \blacksquare$$

### 審查與形式化
**審查的困境**（2003–2014）：《Annals》的審查者**6 年無法完全確認**——

- 1999 年審查「99% 確信」——**最後的 1%（電腦部分）無法檢驗**
- 2003 年發表（帶保留聲明）——**與四色定理（1976）同源的可檢驗性危機**

**Flyspeck 計畫（2003–2014）**：Hales 領導，**用 Coq 與 Isabelle 把證明完全形式化**——

$$\text{150 頁人類推理} \to \text{形式化（Coq/Isabelle）} \to \text{機器檢驗的完整邏輯}$$

**2014 年完成**——**可檢驗性恢復**（與 Gonthier 的四色 Coq 證明 2005 同源，見 `1976-四色定理.md`）。**Kepler 猜想成為第二個完全形式化的重大定理**。

### 程式碼：堆積密度

```python
import math

# 2D：六角堆積（Fejes Tóth 1940 證明最密）
def hex_packing_density():
    """2D 六角堆積：密度 π/(2√3) ≈ 90.7%"""
    # 正六角形胞：面積 = (3√3/2)r²（r 是內切圓半徑=球半徑）
    circle = math.pi * 1.0**2
    hexagon = 3 * math.sqrt(3) / 2 * 1.0**2
    return circle / hexagon

# 3D：FCC 堆積（Kepler 猜想）
def fcc_packing_density():
    """3D FCC：密度 π/√18 ≈ 74.05%"""
    # FCC 單胞：4 個球、邊長 a = 2r/√2（對角線相切）
    r = 1.0
    a = 2 * r / math.sqrt(2)          # 晶格常數
    cell_volume = a**3                # 立方單胞
    ball_volume = 4 * (4/3) * math.pi * r**3   # 4 個球
    return ball_volume / cell_volume

print(f"2D 六角堆積密度 = {hex_packing_density():.4f}（π/2√3 = {math.pi/(2*math.sqrt(3)):.4f}）")
print(f"3D FCC 堆積密度 = {fcc_packing_density():.4f}（π/√18 = {math.pi/math.sqrt(18):.4f}）")

# 對照：立方堆積（最差）
def cubic_packing_density():
    r = 1.0
    a = 2 * r                          # 立方：邊長 = 2r
    return (4/3) * math.pi * r**3 / a**3
print(f"3D 立方堆積密度 = {cubic_packing_density():.4f}（52.4%——最差）")

print("\nKepler 猜想（1611）：FCC 是 3D 最密——Hales 1998 電腦證明、2014 Flyspeck 形式化")
```

### 水果攤的數學
**偵探筆記**：Kepler 的推理是「**自然界的最佳堆積**」——橘子、雪花、蜂巢的觀察。**Hales 的推理**是「**局部化 + 電腦檢驗**」——胞的分解 + LP 上界。**387 年的譜系**：觀察（1611）→ 格情形（Gauss 1831）→ 局部化策略（Fejes Tóth 1953）→ 電腦證明（1998）→ 形式化（2014）——**與四色定理（1852→1976→2005）平行的譜系**（見 `1976-四色定理.md`）。

## 結案 -- 後果與影響
- **387 年懸案終結**：Kepler 猜想（1611→1998）——第二個電腦證明的重大定理。
- **形式化驗證的帝國**：四色（2005）→ Kepler（2014）→ Lean 數學庫（2020s）——**機器檢驗的數學**成為標準（Hales 的 Flyspeck 是最大工程）。
- **堆積理論**：2D（六角）、3D（FCC）、高維（**8 維 E8 與 24 維 Leech 格**——Viazovska 2016 證明，Fields 2022）——**堆積的譜系**。
- **線性規劃的應用**：LP 對偶的「證書」驗證——**最佳化與證明的結合**（與單純形法的平滑分析同源，見 `../隨機算法/2004-SpielmanTeng平滑分析.md`）。
- **Viazovska 的奇蹟**（2016）：**E8 與 Leech 格的最密堆積**——用**模形式**（傅立葉的魔杖）證明——**24 維的完整解**（3 維用電腦，8/24 維用模形式——**維度的意外**）。

## 關鍵人物與文獻
- **Johannes Kepler**（1571–1630）：Strena seu de nive sexangula (1611)——新年禮物小冊
- **Thomas Hales**（1958–）：Kepler 猜想 (1998)；Flyspeck 計畫 (2003–2014)
- **Samuel Ferguson**：博士生、共同作者
- **László Fejes Tóth**（1915–2005）：局部化策略 (1953)；2D 最密 (1940)
- **Maryna Viazovska**（1984–）：E8/Leech 格 (2016)；Fields 獎 2022
- **Georges Gonthier**：四色的 Coq 證明 (2005)——形式化的先例
- 交叉參照：`1976-四色定理.md`、`2000-千禧年大獎.md`、`2003-Perelman龐加萊猜想.md`、`../隨機算法/2004-SpielmanTeng平滑分析.md`
