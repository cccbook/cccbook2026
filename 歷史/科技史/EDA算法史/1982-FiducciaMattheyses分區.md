# 1982-FiducciaMattheyses分區

## 案件摘要
KL 演算法（1970）讓平衡分區可用，但一輪要 $O(n^2)$：每次只交換一對、每次要重掃全圖找最佳對——百萬節點時代撐不住。1982 年 DAC，C. M. Fiduccia 與 R. M. Mattheyses 發表 FM 演算法，兩個關鍵換裝：**成對交換改單點搬移**（對側隨時可不必平衡，只在過程中保持約束）、**增益記帳改桶串（bucket list）**（每次搬移只影響鄰居，增益更新 $O(\deg)$）。一輪複雜度降到 $O(|E|)$——與圖的邊數成正比，線性時間。FM 至今仍是所有分區器（hMetis、MLPart、多層佈局）最粗層的核心引擎，是 KL 之後四十年分區案的真正主角。

## 前因 -- 為什麼會有這個案子
- **KL 的兩個瓶頸**：一輪 $O(n^2)$ 太慢；且只允許「成對交換」，兩側必須先等大——處理不平衡 netlist（如巨集設計）很彆扭。
- **VLSI 規模爆炸**：1980 年代晶片達十萬閘級，分區要嵌入佈局迴圈反覆執行，複雜度是生死線。
- **超圖的出現**：net 是「多 pin 連接」，用圖的兩兩邊近似會失真——需要直接處理超邊（hyperedge）。
- **KL 的增益記帳已就緒**：$D(a) = E(a) - I(a)$ 的思想可繼承，缺的是更快的資料結構。

## 線索與推理 -- 數學式、程式、理論

### 改良一：單點搬移取代成對交換
動作從 swap(a, b) 換成 move(a)：把一個節點從 $A$ 搬到 $B$。增益定義不變：

$$g(v) = \text{cut size after move} - \text{cut size before move} \quad (\text{取負為收益})$$

單點搬移的好處：(1) 候選從 $\binom{n}{2}$ 對降為 $n$ 個；(2) 可以處理兩側不等大；(3) 一次搬移可以連續改善。

### 改良二：桶串記帳
增益值有界：$g(v) \in [-p_{\max}, +p_{\max}]$（$p_{\max}$ 是最大 pin 數）。建 $2p_{\max}+1$ 個桶，按增益分桶存放節點：

```
gain:  +4   +3   +2   +1    0   -1  ...
bucket:[]   [v1] [v3] []   [v2] []  ...
```

- 選最大增益節點：直取最右非空桶 $O(1)$；
- 搬移 $v$ 後，只有 $v$ 的**鄰居**增益改變，逐個 $O(\deg)$ 更新（從舊桶刪、插新桶）。

一輪（pass）的總成本：每條超邊在每次穿越變化時被觸碰常數次 ⇒ $O(|E|)$，其中 $|E| = \sum |\text{net pins}|$。

### 平衡約束與最佳前綴
搬移中允許暫時違反平衡，但須滿足鬆約束：

$$\lceil r|V| \rceil - \text{maxcell} \le |A| \le \lfloor r|V| \rfloor + \text{maxcell}$$

（$r$ 是目標比例，maxcell 是最大單元大小。）每輪仍繼承 KL 的**最佳前綴回溯**：記錄每步的累計割數，取最小處回溯。

### 範例：超邊的增益計算
net $\{a, b, c\}$ 側 $A$，僅 $d$ 在側 $B$。搬移 $a$ 的增益：net 從 cut（$A$/$B$ 各有）變為不 cut（$b,c$ 留 $A$、$a$ 到 $B$？不——$a$ 去了 $B$ 則 net 仍 cut）。細算：$a$ 走後 $A$ 剩 $\{b,c\}$、$B$ 剩 $\{a,d\}$，net 仍 cut ⇒ $g = 0$；若先搬 $d$ 再搬 $a$，net 從 cut 變不 cut，兩步合計 $-1$——FM 的單點搬移允許這種「兩步序列」，KL 的成對交換做不到。這正是 FM 常勝 KL 的結構性原因。

## 結案 -- 後果與影響
- **線性時間分區成為現實**：FM 讓分區可嵌入佈局迴圈反覆執行，min-cut 佈局（recursive bisection placement）自此可規模化到十萬節點。
- **多層時代的引擎**：hMetis（1997）、MLPart 等多層分區器，最粗層跑的就是 FM；FM 至今仍是 TritonPart（OpenROAD）等開源工具的內核。
- **超圖直處理的先例**：FM 直接以 net 為超邊記帳，確立「分區用超圖」的共識，影響所有後繼演算法。
- **KL 的落幕**：KL 幾乎完全被 FM 取代（僅存於教科書與特定點權重場景）——演算法史上少見的「直系子代全面接班」。

## 關鍵人物與文獻
- **Charles M. Fiduccia**（1949–）：IBM，超圖分區與線性時間演算法。
- **Robert M. Mattheyses**：IBM Watson，VLSI 分區實作。
- 文獻：
  - C. M. Fiduccia, R. M. Mattheyses, "A Linear-Time Heuristic for Improving Network Partitions," *DAC* 1982, 175–181.
  - B. W. Kernighan, S. Lin, *Bell Syst. Tech. J.* 49, 291 (1970)（前身）。
  - G. Karypis et al., "Multilevel Hypergraph Partitioning," *DAC* 1997（多層接班）。
