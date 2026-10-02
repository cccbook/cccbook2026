# 1837 - Babbage 差分機（機械電腦時代的頂點）

## 案件摘要
1822 年（設計）與 1837 年（奠基），Charles Babbage 設計了 **Difference Engine**（差分機）：
一台純機械的「多項式計算機器」，可自動計算：
$$f(x) = a_0 + a_1 x + a_2 x^2 + \cdots + a_n x^n \qquad \text{共 } n+1 \text{ 階差分。}$$
至 1840 年代更提出 **Analytical Engine**（分析機）——含**儲存裝置、邏輯單元、控制流**，
是史上第一台**通用可程式電腦**的完整設計：
$$\text{存儲器（mill）+ 算術單元（mill）+ 條件分支（IF）} = \text{現代 CPU 三大件}.$$
但 Babbage 一生只造出部分零件：**他超前了 100 年**——1840 年代的機械無法支撐他的設計。

## 前因 -- 為什麼會有這個案子
- **天文表的瓶頸**：法國測量局（1790–1799）製作了巨大的天文測量表，
  但製表員用手工逐項歸約，耗費數十年——**資料處理成為科學進步的瓶頸**。
- **18 世紀的線索**：Gaspard de Prony（1799）提出用差分法加速計算：
  $$\Delta f(x) = f(x+1) - f(x), \qquad \Delta^k f \ \text{為常數（若 } k > \deg f).$$
  **關鍵偵探**：若已知一串函數值 $f(0),\dots,f(n)$，只需用**差分表**外推下一值，無需再做乘除。
- **Babbage 的頓悟（1822）**：不要「每一步都算」，而是「**一次算出差分表的全部係數**，往後只要**加法**」。
- **1834 的第二頓悟**：拜訪 Jacquard 織布機後，Babbage 構思了**差分機的延伸——分析機**：
  - 加一個**存儲單元**（存中間結果）、一個**「mill」**（乘除單元）與**打孔卡輸入**（存放運算序列）。
  - **條件分支（IF）**——卡片疊加與減去以改變控制流。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：差分表（差分機的數學核心）
對一個 $n$ 階多項式，$k$ 階差分為常數：
$$\Delta^k f = \text{const}\quad(\forall k \ge \deg f).$$
例：$f(n) = n^3$（天體立方）：
$$\begin{array}{c|c|c|c}
n & f(n) & \Delta f & \Delta^2 f \\
\hline
0 & 0 & 1 & 6 \\
1 & 1 & 7 & 6 \\
2 & 8 & 19 & - \\
3 & 27 & - & - \\
\end{array}$$
**外推**：$f(4) = f(3) + \Delta f(3) = 27 + 19 = 46$（只要知道 $f(3)$ 與 $\Delta f(3)$）。
差分機在每一步只做**加法**（差分表列的固定加法器），因此整台機器的乘法、除法複雜度為 **0**——
$$\text{多項式計算} \quad \text{以純加法器完成（省下乘法器）}.$$

### 第二條線索：差分的二項式恆等式（機械設計的數學）
Newton 前向差分公式：
$$f(x) = \sum_{k=0}^{n} \binom{x}{k}\,\Delta^k f(0).$$
- 差分機的軸 $\binom{x}{k}$ 是**帶齒輪（adding engine）**的形式。
- 每個軸的齒輪數可變（0–9），通過位置決定係數——**可程式性：改軸齒數 = 改程式**。
  $$\text{軸齒數設定} = \text{多項式係數設定}.$$

### 第三條線索：分析機的架構（現代 CPU 的藍圖）
| 分析機單元 | 功能 | 現代對應 |
|------------|------|----------|
| Store（存儲器） | 存 1000 個 50 位十進位數 | RAM |
| Mill（磨坊） | 乘除單元 | ALU（乘除部分） |
| Cards（打孔卡） | 輸入指令序列 | 程式（軟體） |
| IF / Branch | 條件分支 | 控制單元 |
| Barrel（鼓） | 列印輸出 | 輸出具體 |

**現代電腦的 CPU = Store + Mill + Control + Instruction Sequence**，Babbage 全部預見。

### Python：差分表與外推

```python
def diff_table(f_vals):
    """建立差分表：最後一列為常數（0 階差分）"""
    table = [f_vals]
    while len(table[-1]) > 1:
        table.append([table[-1][i+1]-table[-1][i] for i in range(len(table[-1])-1)])
    return table

def extrapolate(f_vals):
    """差分機外推：下一項 = 從最後一列往回累加"""
    t = diff_table(f_vals)
    # 從最高階差分開始，沿對角線加回去
    next_vals = [row[-1] for row in t]      # 對角線最後一列
    for i in range(len(next_vals)-2, -1, -1):
        next_vals[i] += next_vals[i+1]
    return next_vals[0]

f = [n**3 for n in range(6)]   # 0,1,8,27,64,125
print("f(n)=n^3:", f)
t = diff_table(f)
for i,row in enumerate(t): print(f"  Δ^{i}: {row}")
print("外推 f(6) =", extrapolate(f), "(真值 216)")
print("再外推 f(7) =", extrapolate(f+[216]), "(真值 343)")
```
輸出：
```
f(n)=n^3: [0, 1, 8, 27, 64, 125]
  Δ^0: [0, 1, 8, 27, 64, 125]
  Δ^1: [1, 7, 19, 37, 61]
  Δ^2: [6, 12, 18, 24]
  Δ^3: [6, 6, 6]
外推 f(6) = 216 (真值 216)
再外推 f(7) = 343 (真值 343)
```
（差分機只需**加法器**就能外推任意 $n$ 階多項式——**Babbage 的核心發明**。）

## 結案 -- 後果與影響
- **差分機的命運**：1842 年完成部分列印機（≈ 4000 齒），能計算 $f(x)$ 並輸出——**Babbage 親手運轉的零件至今保存在倫敦科學博物館**。
- **分析機超前 100 年**：1843 年出版（Menabrea 譯註）到 20 世紀初才有電子管能實作；
  1940s 的 Howard Aiken 依分析機設計了 **Harvard Mark I**（1944，IBM 資助，規模放大的分析機）——
  **第一台電子/繼電器實作**。
- **Ada Lovelace 的註釋（1843）**：譯註中她指出**分析機可處理任意符號**（不限於數字），
  且可「**編寫程序**」使其運算——**第一份公開的演算法**（Bernoulli 數演算法）與「程式」概念的最早記載。
- **機械時代的天花板**：Babbage 的失敗不是概念錯，是**1840 年代金屬加工精度不足**——
  差分機需數千顆精密齒輪，無法製造到位。**這個「原理正確、製程不足」的教訓，在後來的積體電路時代重演**（見「1958-積體電路.md」）。
- **歷史定位**：Babbage 是**第一位提出通用可程式電腦完整架構的人**——雖無實作，其設計影響了
  ENIAC、Turing、John von Neumann，**所有現代電腦都是「Babbage 機 + 電子」的組合**。

## 關鍵人物與文獻
- **C. Babbage**：Difference Engine (1822, 1837)；Analytical Engine (1837, 1843)。
- **A. Lovelace**：〈Sketch of the Analytical Engine〉(1843)；**Bernoulli 演算法**（首個演算法）。
- **G. de Prony**：差分法 (1799)——啟發 Babbage。
- **H. Aiken**：Harvard Mark I（依 Babbage 設計，1944）。
- 相關案件：`1801-Jacard織布機.md`、`1936-Turing機.md`、`1946-ENIAC電子計算機.md`。