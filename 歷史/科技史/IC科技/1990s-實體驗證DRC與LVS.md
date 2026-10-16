# 1990s - 實體驗證（Physical Verification）與 Signoff

## 案件摘要
1990 年代，晶片從百萬電晶體邁向千萬級，佈局圖（layout）錯一條線就可能讓整批晶片報廢。Mentor 的 Calibre 與 IBM 的 ICV 建立了 DRC/LVS/ERC 三重驗證與「signoff」制度：未通過驗證，不得送廠（tape-out）。

## 前因 -- 為什麼會有這個案子
- 微微縮（micron → submicron → deep submicron）使製程規則從幾十條暴增到上千條，人工檢查已不可能。
- 1980 年代初 Mead–Conway 的《Introduction to VLSI Systems》提出可參數化的設計規則（以 $\lambda$ 為單位），為自動化檢查鋪路。
- 佈局由人工改為自動/半自動工具後，「畫出來的圖」與「設計者心中的電路」可能不一致，需要機械式比對。
- 掩膜（mask）成本隨世代攀升，一次流片失敗動輒數十萬美元以上，產業需要「簽名保證」的品質閘門。

## 線索與推理 -- 數學式、程式、理論

### 1. DRC（Design Rule Check）：幾何規則的偵探
DRC 只看幾何，不看電氣意義。典型規則：

| 規則 | 定義 | 典型值（0.35μm） |
|------|------|------------------|
| 最小線寬 | $W \geq W_{\min}$ | 0.4 μm |
| 最小間距 | $S \geq S_{\min}$ | 0.5 μm |
| 最小包覆（enclosure / overlap） | via 周圍金屬至少包覆 $E$ | 0.1 μm |
| 最小面積 | $A \geq A_{\min}$ | 0.16 μm² |

形式化：對圖層 $L$ 上所有圖形對 $(g_i, g_j)$，若兩者不同網路且距離 $d(g_i, g_j) < S_{\min}$，則違規。間距檢測若用兩兩暴力法是 $O(n^2)$；實務用**掃描線（sweep line）演算法**降到約 $O(n \log n)$。

### 2. LVS（Layout vs Schematic）：圖形與網表的比對
LVS 是「對照筆錄」：從佈局萃取（extract）出電路網表，再與 schematic 網表做**圖同構（graph isomorphism）**比對：

- 節點 = 電路節點（net），邊 = 元件端點連接。
- 兩網表同構且元件參數（$W/L$、電容值）在容差內 → LVS clean。
- 圖同構一般問題複雜度未知，但電路網表因有高度規則結構與分割（partitioning by hierarchy）而可實用求解。

### 3. ERC（Electrical Rule Check）
DRC 管幾何、LVS 管連接，ERC 管電氣常識：
- 浮接閘極（floating gate）、浮接 well
- VDD/VSS 短路或未連接
- 輸出對地短路、bulk 端接錯

### 4. 天線效應（Antenna Effect）與 DFM
蝕刻時金屬線累積電荷，若連接到閘極面積過大，比例超限會擊穿閘氧化層。天線比值規則：

$$\text{ANT} = \frac{A_{\text{metal}}}{A_{\text{gate}}} \leq R_{\max}$$

修復方式：跳層（jump up a layer）、加保護二極體。DFM（Design for Manufacturability）則在 DRC 之上加入良率導向規則：冗余 via、金屬填充（fill）、關鍵面積分析（CAA），良率模型可用 Poisson 近似：

$$Y \approx e^{-A \cdot D_0}$$

其中 $A$ 為關鍵面積、$D_0$ 為缺陷密度。

### 5. Signoff 概念
Signoff = 「結案簽名」：DRC clean + LVS clean + ERC clean + 天線 clean +（後期）timing/IR-drop 全數通過，才允許 tape-out。1990s 後期 Calibre 成為 de facto signoff 標準，foundry（台積電、聯電）只認可特定工具版本簽出的結果。

### 6. Python 實作：掃描線最小間距檢測

```python
from dataclasses import dataclass

@dataclass
class Rect:
    x1: float; y1: float; x2: float; y2: float
    net: str

    def gap_x(self, other):  # x 方向間距（若 y 有重疊）
        if self.y1 < other.y2 and other.y1 < self.y2:
            return max(other.x1 - self.x2, self.x1 - other.x2)
        return float('inf')

def min_spacing_drc(rects, s_min):
    """掃描線 DRC：依 x1 排序，只檢查 x 距離 < s_min 的鄰居"""
    events = sorted(rects, key=lambda r: r.x1)
    violations = []
    for i, a in enumerate(events):
        for b in events[i+1:]:
            if b.x1 - a.x2 >= s_min:   # 剪枝：後面更遠，可提前停止
                break
            g = a.gap_x(b)
            if g < s_min and a.net != b.net:
                violations.append((a, b, g))
    return violations

# 演示：兩條金屬線間距 0.3，低於 0.5 規則 → 違規
r1 = Rect(0, 0, 2.0, 0.4, "netA")
r2 = Rect(2.3, 0, 4.0, 0.4, "netB")
print(min_spacing_drc([r1, r2], 0.5))   # 印出違規對與間距 0.3
```

暴力法 1000 個圖形需 50 萬次比較；掃描線＋剪枝在實際佈局上通常只需數千次，這就是 Calibre 級工具的演算法核心思想。

## 結案 -- 後果與影響
- DRC/LVS/ERC + signoff 成為所有先進製程的必經關卡，沿用至今（EUV 世代規則數已上萬條）。
- 掃描線、圖同構、提取等核心演算法成為 EDA 實體驗證的理論基石。
- 天線效應規則推動「製程-設計協同」，催生 DFM 與後來的良率學（yield learning）。
- Signoff 制度使「無晶圓設計公司（fabless）＋專業代工（foundry）」的分工模式可行——雙方靠同一套驗證規則互信。

## 關鍵人物與文獻
- Carver Mead、Lynn Conway：《Introduction to VLSI Systems》(1980)，$\lambda$ 設計規則的起源。
- Mentor Graphics：Calibre（1990s 推出，至今仍是 DRC/LVS signoff 主流）。
- IBM：內部驗證工具與 hierarchical LVS 演算法先驅。
- A. Sangiovanni-Vincentelli 等：EDA 演算法與驗證方法學的學術奠基者。
