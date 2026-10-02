# 1801 - Jacquard 織布機（可程式機器的原型）

## 案件摘要
1801 年，Joseph-Marie Jacquard 發明 **Jacquard Loom**（雅卡織布機）：
首次用**打孔卡片 (punched cards)** 控制織機圖案：
$$\text{打孔卡} = \text{程式碼} \quad \Longrightarrow \quad \text{織布機} = \text{解譯器}.$$
一副卡片 = 一個花樣。**織布這件事，第一次被「資料」而非「工人記憶」所控制**。
這個思想 35 年後啟發了 Babbage（見「1837-Babbage差分機.md」），70 年後啟發了 Hollerith（1890 美國人口普查機），直接導致 20 世紀初期的**打孔卡資料處理時代**。

## 前因 -- 為什麼會有這個案子
- **複雜花樣的瓶頸**：18 世紀末，法國里昂的絲織業競爭激烈——精緻花邊與圖案需要極高技藝的「提花工人」（drawboy）：
  一幅複雜圖案需數千個提針動作，**記憶錯誤 = 整匹布報廢**。
- **織布機的機械限制**：當時的提花織機（drawloom）靠一個小男孩（drawboy）手動拉線，根據花樣順序拉起特定經線——
  **速度、準確度與複雜度受限於人力**。
- **Jacquard 的偵探直覺**：把「花樣」這個**循環序列**從人的記憶**外部化（externalize）**到一張紙卡上：
  - 每一張打孔卡代表一行織紋（一個經緯循環的一步）。
  - 孔洞 = 讓針通過（提起經線）；無孔 = 阻擋（不提起）。
  - 卡片串成一條鏈，循環或連續帶動織機——**機器自己「讀程式」**。
- **革命性的一點**：**機器的動作不再固定，而由輸入資料決定**——這是**可程式性（programmability）**的第一次實際應用。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：可程式性 = 資料與指令的分離
在 Jacquard Loom 前，機械裝置的功能是**固定**的（齒輪決定運動）。
Jacquard Loom 的功能由**打孔卡序列**決定：
$$\text{動作序列}_t = f(\text{card}_t), \qquad t=1,\ldots,N.$$
**控制與機構分離**：同一台織機可織出完全不同的花樣——只要換一副卡片。
這正是現代電腦的**軟體與硬體分離**的雛形。

### 第二條線索：有限狀態機（循環控制）
織機是一個循環執行的機械裝置：
$$S_{t+1} = \delta(S_t, \text{input}_t), \qquad \text{output}_t = \lambda(S_t, \text{input}_t).$$
- $S_t$：經線的提起狀態（warp harness）
- $\text{input}_t = \text{card}_t$（打孔模式）
- $\text{output}_t$：織出的紋路（一行 weft）
- **打孔卡序列 = 輸入序列 = 程式**。
這是**有限狀態機（FSM）+ 外部輸入**的機械實現——先於 Turing 機（1936）的工程範例。

### 第三條線索：重複與遞迴的效率
複雜花樣常有重複單元（border, motif）。打孔卡可重複循環：
$$\{\text{card}_1,\ldots,\text{card}_k,\;\text{card}_1,\ldots,\text{card}_k,\ldots\}.$$
**迴圈（loop）**在機械層面首次被「資料序列」實現，而非靠齒輪比率——
工程上的**子程式/迴圈**思想。

### Python：Jacquard 卡片序列的模擬

```python
class JacquardLoom:
    """Jacquard Loom 模擬：打孔卡控制每行的經線提起模式"""
    def __init__(self, warp_count=8):
        self.warp_count = warp_count

    def weave(self, punched_cards):
        """
        punched_cards: list of tuples/bitmask，每張卡 = 一行
        1 = 孔洞（提起 warp），0 = 無孔（不提起）
        """
        rows = []
        for i, card in enumerate(punched_cards):
            # 一行織紋：提起的經線決定與緯線交錯
            pattern = ""
            for w in range(self.warp_count):
                up = card[w] if w < len(card) else 0
                pattern += "█" if up else "·"
            rows.append(pattern)
            print(f"Row {i+1:2d} (card {i+1}): {pattern}")
        return rows

# 簡單的二維棋盤花樣（重複迴圈）
cards = []
for r in range(4):  # 4 行重複
    card = [(w + r) % 2 for w in range(8)]  # chessboard
    cards.append(tuple(card))
JacquardLoom().weave(cards)
```
輸出：
```
Row  1 (card 1): █·█·█·█·
Row  2 (card 2): ·█·█·█·█
Row  3 (card 3): █·█·█·█·
Row  4 (card 4): ·█·█·█·█
```
（一副打孔卡序列決定整個花樣循環——**「程式 = 資料序列」**的最早示範。）

## 結案 -- 後果與影響
- **工業革命的軟體化**：Jacquard Loom（1801）是**第一台可程式機械裝置**——
  控制邏輯從機構內部（齒輪）移到外部（卡片）。
- **直接啟發 Babbage**：Charles Babbage 在 1834 年拜訪法國時研究 Jacquard Loom，
  決定將**打孔卡**用於差分機（Analytical Engine）的「記憶」與「輸入」（見「1837-Babbage差分機.md」）。
  Ada Lovelace（拜訪 1843）明確指出：「打孔卡可指揮機器執行任意運算」——**程式的概念萌芽**。
- **Hollerith 與人口普查（1890）**：Herman Hollerith 借鑑 Jacquard 打孔卡，製造機電式打孔卡制表機，完成美國 1890 人口普查（提前 6 年完成），成立 Tabulating Machine Company（後合併為 IBM）。
- **打孔卡時代（1900–1950）**：IBM Holerith 卡（80 欄）成為 20 世紀前半葉資料處理的標準——
  UNIVAC、早期 IBM 大型機全部用打孔卡輸入，直到 1950 年代終端機取代。
- **歷史定位**：Jacquard Loom 把「模式（pattern）」從**藝術記憶**變成**可重複的資料**——
  **可重複性（reproducibility）+ 可程式性（programmability）**是工業自動化的兩大支柱。

## 關鍵人物與文獻
- **J.-M. Jacquard**：Jacquard Loom, 法國專利 (1801)；里昂絲織業（1804–1810）廣泛採用。
- **C. Babbage**：Analytical Engine（1837）直接受其啟發。
- **A. Lovelace**：〈Notes on the Analytical Engine〉(1843)——最早的程式設計筆記。
- **H. Hollerith**：Tabulating Machine（1889），美國人口普查（1890）。
- 相關案件：`1642-Pascal進位法計算機.md`、`1837-Babbage差分機.md`、`1936-Turing機.md`。
