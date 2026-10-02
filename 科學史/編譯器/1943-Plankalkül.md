# 1943-Plankalkül

## 案件摘要
1943 年，Konrad Zuse 在二戰的砲火中，為他的 Z4 機器設計了一套「紙上的程式語言」——Plankalkül（「規劃演算」）。它包含陣列、記錄、賦值、副作用函數、斷言，超前時代至少半世紀。然而這門語言直到 1972 年才完整出版，2000 年（Zuse 死前五年）才第一次被真正實作——史上最孤獨的語言，凶手是戰爭、流亡與它那令人望而生畏的二維記法。

## 前因 -- 為什麼會有這個案子
- **Z1 到 Z4 的工程實踐**：Zuse 從 1935 年起陸續建造 Z1–Z3 機械與繼電器電腦，親身體會「用手寫機器指令」的痛苦。他需要一種能描述演算法本身、而非機器細節的語言。
- **戰爭的隔離**：Z3/Z4 是德國官方計畫（ aerodynamic 計算），但 Zuse 與英美學界完全隔絕——他不知道 Turing（1936）、不知 Shannon（1937）、更不知後來的 EDVAC 報告。他的一切都是獨立發明。
- **紙上語言**：Plankalkül 從未被機器執行過——Z4 的記憶體只有 64 字，根本容不下任何編譯器。它是純理論建構，像一份「兇手寫好卻無人偵讀的自白書」。
- **二戰的摧毀**：1943 年 Zuse 的公寓與文件在轟炸中被毀，他帶著 Z4 逃亡，輾轉搬到瑞士阿爾卑斯山的小村 Hinterstein。語言的論文遲至 1948 年才在德國發表（未被重視），完整版 1972 年才問世。

## 線索與推理 -- 數學式、程式、理論

### 案件的證物：Plankalkül 到底有什麼？
Zuse 的語言包含（以現代眼光看）：

| 概念 | Plankalkül 記法 | 現代對應 |
|---|---|---|
| 賦值 | `V ⇒ R` | `R = V` |
| 陣列 | `A` 行（Angaben） | array |
| 記錄 | `S` 行（Struktur） | struct |
| 副函數 | `P` 行 | procedure |
| 斷言 | `→ x` 條件 | assert |
| 條件 | `if x then else` | if-else |

它的**二維記法**是最大的障礙：每一行程式分成四行，分別寫「敘述本身、下標、結構指示、註解」——例如 `V0[K] + V0[K] ⇒ R0` 這個簡單賦值，在 Plankalkül 中要寫成：

```text
  V    0    K      +  V    0    K  ⇒  R    0
  F                        F
                          A
```

上半行是主記法，第二行 `F` 是結構型別標記，第三行 `A` 是陣列維度標記——閱讀者必須「縱向掃描」，這在 1948 年後的學界完全無人跟隨。

### 賦值的理論意義
Zuse 首次把「記憶體狀態的改變」抽象成賦值運算。若程式狀態為 $\sigma: \text{Var} \to \text{Val}$，則執行 `V ⇒ R` 的語意是：

$$\sigma' = \sigma[R \mapsto \mathcal{V}(V)]$$

這個「狀態轉移」觀點，正是 1960 年代操作語意學（operational semantics）的雛形——Zuse 在 1943 年就用紙筆寫出來了。

### 資料結構：陣列與記錄的先行
Zuse 允許巢狀結構：一個記錄可以包含多個陣列，一個陣列元素也可以是記錄。用現代 Python 重現他的意思：

```python
# Plankalkül 的結構宣告（S 行）重現：
#   S := [field1: n bits, field2: m bits]
# 現代 Python 對應：
from dataclasses import dataclass

@dataclass
class Point:          # 對應 S 行：兩個 bit-向量欄位
    x: int            # 8 bits（Zuse 用 bit 長度宣告，非型別名稱）
    y: int

P = [Point(x=i, y=i*i) for i in range(8)]   # 對應 A 行（陣列）

def K(P, k):          # 對應 P 行（副函數）——讀取陣列元素
    assert 0 <= k < len(P), "Plankalkül 的斷言先行！"
    return P[k].x + P[k].y

print(K(P, 3))        # 3*3 + 3 = 12
```

注意 `assert`——Zuse 在 1943 年就把「執行時檢查」寫進語言規格，比 Hoare 的斷言邏輯（1969）早了 26 年。

### 函數副作用：超前時代的爭議
Zuse 的副函數允許修改呼叫者的變數（即現代的「副作用函數」），這在當時是異端——多年後 FORTRAN/ALGOL 都還在爭論傳值 vs 傳址。Zuse 直接兩者都給。

## 結案 -- 後果與影響
- **半世紀的雪藏**：1948 年德文發表無人理會；1972 年完整報告出版時，FORTRAN、ALGOL、LISP 早已統治世界。Zuse 的許多構思（陣列、記錄、斷言）被他人「重新發明」。
- **Kalkül 的詛咒**：二維記法讓後人望而卻步——直到 2000 年，柏林自由大學的團隊才用現代語法（一維化）寫出第一個 Plankalkül 編譯器/直譯器，此時 Zuse 已 90 歲。
- **歷史定位**：Plankalkül 證明「高階語言」的概念在 1943 年就已被完整構思——不是工程不夠，而是戰爭隔絕了知識的傳播。它是程式語言史的「失落環節」。
- Zuse 的 Z4 是二戰後歐陸唯一倖存並運作的電腦，1950 年賣給瑞士蘇黎世聯邦理工（ETH）——Rutishauser 正是在那裡寫出最早的「自動編碼」。

## 關鍵人物與文獻
- **Konrad Zuse**：Z1(1938)–Z4(1945)，Plankalkül(1943-1946 設計)。
- 文獻：
  - K. Zuse, "Über den allgemeinen Plankalkül als Mittel zur Formulierung schematisch-kombinativer Aufgaben," *Archiv der Mathematik* 1, 441-441 (1948).
  - K. Zuse, "Der Plankalkül," *Gesellschaft für Mathematik und Datenverarbeitung*, Report Nr. 63 (1972) — 完整版。
  - R. Rojas et al., "The Structure of the Zuse Z4," *IEEE Annals of the History of Computing* (2006).
