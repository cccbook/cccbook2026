# 1980-MeadConwayVLSI

## 案件摘要
1980 年，Caltech 的 Carver Mead 與 Xerox PARC 的 Lynn Conway 出版《Introduction to VLSI Systems》，把晶片設計從「電晶體層級的黑魔法」變成「可教、可規則化、可規模化的工程學」。加上 MPC79 多專案晶圓計畫，他們讓大學生也能設計晶片，引爆了 VLSI 民主化革命。

## 前因 -- 為什麼會有這個案子
- 摩爾定律（1965）預告單晶電晶體數指數成長，但 1970 年代的設計方法跟不上：每家公司有自己一套神秘規則，設計靠老師傅經驗。
- 「設計生產力鴻溝」：製造能力每年翻倍，設計人力卻只有線性成長。
- Mead 在 Caltech 研究互補 MOS（CMOS）的理論極限；Conway 在 Xerox PARC 研究可組合的設計規則與符號佈局系統。
- 1978 年 Conway 與 Mead 決定：把方法學寫成教科書 + 辦一場多專案晶圓實驗，雙管齊下。

## 線索與推理 -- 數學式、程式、理論

### 結構化 VLSI 設計方法學
Mead–Conway 的核心信念：**設計規則必須與製程參數解耦，並以比例常數 λ 表示**。
- 全部尺寸以 $\lambda$（半個 MOS 製程線寬）的倍數表示：線寬、間距、接觸孔都寫成 $n\lambda$。
- 製程升級（線寬縮小）時，只需改變一個常數 $\lambda$，整份版圖不用重畫。
- 注意：此 $\lambda$ 是**幾何縮放常數**，與函數程式的 λ 演算（lambda calculus）完全無關——只是同名的記號巧合。

### 可擴縮設計規則（λ-based design rules）
基於 Dennard 縮放（1974），CMOS 在 $\lambda \to \lambda/S$ 時電氣特性同步改善。典型 λ 規則：

| 規則 | λ 表示 |
|---|---|
| 金屬最小線寬 | $3\lambda$ |
| 金屬最小間距 | $3\lambda$ |
| 多晶矽線寬 | $2\lambda$ |
| 多晶矽–擴散間距 | $1\lambda$ |
| 接觸孔尺寸 | $2\lambda \times 2\lambda$ |
| 電晶體最小寬度 | $2\lambda$ |

Dennard 縮放的數學：尺寸 $\frac{1}{S}$、電壓 $\frac{1}{S}$、電流 $\frac{1}{S}$、延遲 $\frac{CV}{I} = \frac{1}{S}$、功耗密度不變、密度 $S^2$：
$$I_D = \frac{1}{2}\mu_n C_{ox}\frac{W}{L}(V_{GS}-V_{th})^2$$

### MPC79 計畫（多專案晶圓, Multi-Project Chip）
- 1979–80 年，Conway 組織「多專案晶圓」：把**多個不同設計者的晶片**拼到同一片光罩上，分攤昂貴的製造成本。
- 設計以 **Caltech Intermediate Form (CIF)** 文字格式提交，透過 ARPANET 傳送到 PARC，自動合併打罩、批量流片。
- MPC79 首輪就有 12 所大學、數十個學生專案成功流片——證明「教會的方法 + 標準化流程」可行。
- 這是今日 **MPW / shuttle run**（台積電、SMIC 均提供）的直系祖先。

### 設計規則檢查（DRC）的 λ 規則
DRC 就是把 λ 規則寫成演算法自動檢查版圖。核心檢查 = 兩個幾何關係：
$$\text{width}(A) \geq w_{min}, \qquad \text{dist}(A, B) \geq s_{min}(A,B)$$
用 minkowski 膨脹（dilation）實作：把版圖形狀用半徑 $r = \lfloor (w_{min}-\epsilon)/2 \rfloor$ 的方形結構元素膨脹，膨脹前後有差異的區域即違規：
$$A' = A \oplus B_r, \quad \text{violations} = (A' \ominus B_r) \setminus A$$

### 晶片設計民主化與矽編譯的先聲
- 《Introduction to VLSI Systems》成為 1980 年代大學 VLSI 課程聖經，數萬工程師照書自學設計晶片。
- 書中提出「設計規則 + 結構化階層 + 規則性（regularity）+ 模組性（modularity）+ 局部性」，為硬體描述語言（Verilog 1984 / VHDL 1987）與**矽編譯**（silicon compilation）鋪路。
- Mead–Conway 費：CMOS 在 1980 年代取代 NMOS 成為主流——今日所有數位晶片都是 CMOS。

### Python：演示 λ-based DRC 規則縮放
```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches

RULES = {"metal_width": 3, "metal_space": 3, "poly_width": 2, "contact": 2}

def scale_rules(lam):
    """製程縮小時，只需改 lambda，所有規則自動等比縮放"""
    return {k: v * lam for k, v in RULES.items()}

def drc_check(width, space, lam):
    r = scale_rules(lam)
    ok_w = width >= r["metal_width"]
    ok_s = space >= r["metal_space"]
    return ok_w and ok_s

for lam in [2.0, 1.0, 0.5, 0.25]:
    print(f"λ={lam} μm: metal width ≥ {scale_rules(lam)['metal_width']} μm, "
          f"DRC(w=3, s=3) → {'PASS' if drc_check(3,3,lam) else 'FAIL'}")

fig, axes = plt.subplots(1, 4, figsize=(12, 3))
for ax, lam in zip(axes, [2.0, 1.0, 0.5, 0.25]):
    r = scale_rules(lam)
    ax.add_patch(patches.Rectangle((0, 0), r["metal_width"], 10*r["metal_width"],
                                   fc='steelblue', label=f'λ={lam}'))
    ax.set_title(f"λ = {lam} μm\nwidth = {r['metal_width']} μm")
    ax.set_xlim(-1, 8); ax.set_ylim(-1, 8); ax.set_aspect('equal')
plt.suptitle("λ-based design rules scale automatically")
plt.show()
```
同一份設計（比例不變），只改 $\lambda$ 就能從 2 μm 縮到 0.25 μm 製程——這是 Mead–Conway 方法學「可擴縮」本質的最小演示。

## 結案 -- 後果與影響
- VLSI 設計從企業機密變成公開知識，催生 1980 年代美國大學 VLSI 課程與整個 EDA 產業（Cadence、Mentor）。
- MPC79 → MPW shuttle → 今日新創公司花幾萬美元（而非數百萬）就能流片，硬體新創爆發。
- λ 記法成為版圖教育通用語言；結構化設計原則影響 Verilog/VHDL、標準單元、IP 重用、矽編譯與高階合成（HLS）。
- Conway 本人後來成為跨性別權益的傳奇人物；Mead 獲 1999 年 IEEE 榮譽獎章。

## 關鍵人物與文獻
- **Carver Mead**（1934– ）：Caltech 教授，CMOS 理論與神經形態計算先驅。
- **Lynn Conway**（1938–2024）：Xerox PARC/IBM，VLSI 方法學與 MPC79 總工程師。
- C. Mead & L. Conway, *Introduction to VLSI Systems*, Addison-Wesley, 1980.
- L. Conway, "The MPC Adventures," *Microelectronics*, VLSI-81, 1981. Lynn Conway 官方檔案：https://www.ai.eecs.umich.edu/people/conway/
