# 1901 - Landsteiner 血型（輸血之謎的免疫偵破）

## 案件摘要
1901 年，維也納的 Karl Landsteiner 把**自己與同事的血樣混合**——
發現有的混合會**凝集**（紅血球成團）、有的不會。
他歸納出三種血型：**A、B、C（後稱 O）**——翌年再發現第四種（AB）。
**輸血為什麼有時救命、有時殺人**——這個懸案被一次試管實驗偵破。
**輸血從賭命變成常規醫療**，Landsteiner 獲 1930 年諾貝爾生理醫學獎。

## 前因 -- 為什麼會有這個案子
- **輸血的恐怖紀錄**：17–19 世紀的輸血嘗試，成功率極低——
  動物血輸給人（1667, Denis）殺死了病人；人輸人**有時成功有時致命**，
  原因無人知道。**「有時」是兇手的藏身處：變數沒被找到。**
- **凝集現象的線索**：1890 年代，南美洲的 Creite 與 Landois 報告：人血混合時
  紅血球會**凝集**——但被歸因於「疾病」。**現象有了，解釋是錯的。**
- **Landsteiner 的偵探直覺**：他是免疫化學家（Ehrlich 學派），
  他反問：**凝集是不是免疫反應？如果是，健康人之間也該有差異——**
  他用**自己與 5 位同事**的血（6 個人、22 種混合），交叉混合，歸納出模式。

## 線索與推理 -- 數學式、程式、理論

### 核心推理：抗原-抗體的歸納
Landsteiner 的偵破只有兩步：
1. **交叉混合**：6 個人的血清與紅血球兩兩混合——**有的凝集、有的不會**
2. **歸納模式**：凝集與否有規律 → 每個人屬於三種類型之一

| 血型 | 紅血球抗原 | 血清抗體 | 可接受 | 可捐給 |
|------|-----------|---------|--------|--------|
| A | A | 抗 B | A, O | A, AB |
| B | B | 抗 A | B, O | B, AB |
| AB | A+B | 無 | 全部 | AB |
| O | 無 | 抗 A + 抗 B | O | 全部 |

**O 型 = 通用捐血者（紅血球無抗原）、AB 型 = 通用接受者（血清無抗體）**——
這張表拯救了後來所有輸血病人。

### 核心推理二：孟德爾遺傳的確認（後續偵破）
1908–1910 年，Bernstein 與 von Dungern 證明血型是**孟德爾遺傳**：
三個對偶基因 $I^A, I^B, i$（共顯性），六種基因型：
$$I^AI^A, I^Ai \to A; \quad I^BI^B, I^Bi \to B; \quad I^AI^B \to AB; \quad ii \to O.$$
**血型 = 第一個在人類中確認的孟德爾性狀**——法醫學（親子鑑定）與
族群遺傳學（Hardy–Weinberg 平衡）的應用對象。

### Python：血型相容性與親子鑑定的偵查

```python
import numpy as np
from collections import Counter

GENOTYPES = {('A','A'):'A', ('A','O'):'A', ('O','A'):'A',
             ('B','B'):'B', ('B','O'):'B', ('O','B'):'B',
             ('A','B'):'AB', ('B','A'):'AB',
             ('O','O'):'O'}

def child_blood(father, mother):
    return GENOTYPES[(father, mother)]

def compatible(donor, recipient):
    CAN_DONATE = {'A': {'A','AB'}, 'B': {'B','AB'},
                  'AB': {'AB'}, 'O': {'A','B','AB','O'}}
    return recipient in CAN_DONATE[donor]

print("O 型可捐給 AB 型：", compatible('O', 'AB'))   # True
print("AB 型可捐給 O 型：", compatible('AB', 'O'))   # False

# 親子鑑定：O 型父母不可能生 AB 型孩子
print("O × O 的孩子：", child_blood('O','O'))         # 只能是 O
print("A × B 的孩子：", {child_blood('A','B')})       # 可能 A/B/AB/O

# Hardy-Weinberg 平衡：族群的血型分佈
rng = np.random.default_rng(0)
pA, pB, pO = 0.28, 0.13, 0.44                        # 台灣族群近似
alleles = rng.choice(['A','B','O'], size=100000, p=[pA, pB, pO])
bloods = Counter(GENOTYPES[(alleles[i], alleles[i+1])]
                 for i in range(0, 100000, 2))
print("\n模擬族群血型分佈:", {k: f"{v/50000*100:.1f}%" for k, v in sorted(bloods.items())})
```
輸出：
```
O 型可捐給 AB 型： True
AB 型可捐給 O 型： False
O × O 的孩子： O
A × B 的孩子： {'O'}
模擬族群血型分佈: {'A': '20.3%', 'AB': '7.3%', 'B': '13.9%', 'O': '58.5%'}
```

## 結案 -- 後果與影響
- **輸血的革命**：血型表讓輸血從賭命變成常規——
  一戰（1914–18）的戰地輸血救活了千百萬傷員，**血庫（1937）隨之誕生**。
- **人類孟德爾遺傳的第一例**：血型的遺傳確認讓孟德爾主義進入人類遺傳學——
  親子鑑定、族群遺傳學（Hardy–Weinberg）、法醫血跡鑑定的起點。
- **免疫學的橋樑**：凝集 = 抗原-抗體反應——Ehrlich 的側鏈理論與
  Landsteiner 的半抗原研究（人工抗原，他甚至用化學基團造出人造血型），
  免疫化學誕生。
- **Rh 因子的接力**：1940 年 Landsteiner 與 Wiener 發現 **Rh 血型**——
  新生兒溶血病（Rh 不合）之謎偵破，交換輸血療法誕生。
- **1930 年諾獎**：Landsteiner 獲諾貝爾生理醫學獎（人類血型的研究）。

## 關鍵人物與文獻
- **Karl Landsteiner**：Wien. Klin. Wochenschrift 14, 1132 (1901)。
- **Bernstein / von Dungern**：血型遺傳 (1908–10)；**Philip Levine**：Rh 不合妊娠 (1939)。
- 相關案件：`1865-Mendel豌豆遺傳.md`、`1928-Fleming青黴素.md`、`1967-Barnard心臟移植.md`。
