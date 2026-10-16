# 1939 - Bletchley Park 與 Turing 炸彈機

## 案件摘要
1939 年二戰爆發，英國在 Bletchley Park 集結數學家、密碼學家、國際象棋冠軍與填字遊戲高手，破解德國 Enigma。1940 年，Turing 設計的「炸彈機（Bombe）」——基於**已知明文攻擊（crib）+ 邏輯矛盾排除法**——實現工業化破譯。Ultra 情報讓盟軍讀懂德國海空軍命令，歷史學家估計縮短二戰約兩年。這裡也誕生了 Colossus——第一台電子數位電腦。**密碼戰是計算機與資訊時代的搖籃。**

## 前因 -- 為什麼會有這個案子
波蘭 1939 年移交的成果（見 `1932-Rejewski破譯Enigma.md`）與 1938 年德軍的改進（訊息金鑰不再連打兩次、海軍 Enigma 增加轉子）：循環指標法失效，bomba 過時。英國的問題：**德軍改進後的 Enigma，如何工業化破譯？** Turing 的洞察：**已知明文（crib）+ 矛盾排除**。

## 線索與推理 -- 數學式、程式、理論

### 線索：crib（已知明文）
德國軍情的可預測片段：
- **天氣報告**：每晨 6 點，必有 `WETTER`（天氣）
- **無線電靜默結束**：指揮官的 `AN DIE GRUPPE`、`KEINE BESONDEREN EREIGNISSE`（無特別事件）
- **例行格式**：`HEIL HITLER` 結尾

**推理**：若知道明文片段（crib）在密文中的位置，就得到**明文-密文字母對**：

$$x_1 x_2 \dots x_n \to c_1 c_2 \dots c_n \quad \text{（} c_i = E(x_i)\text{）}$$

### Turing 的邏輯鏈（loop）
加密函數 $c = E(x)$ 展開為接線板 $S$ 與轉子的組合。Turing 的觀察：

$$c_i = S^{-1} R_i S (x_i) \implies S(x_i) = R_i^{-1} S(c_i)$$

若 crib 中有字母循環（如位置 1 的字母 = 位置 4 的字母），沿鏈推導得到**自洽性條件**：

$$S = R_{i_1}^{-1} S R_{i_2}^{-1} S \cdots R_{i_k}^{-1} S \quad \text{（繞一圈回到 } S\text{）}$$

**矛盾排除法**：假設某字母的接線板配對（如 A→Z），沿邏輯鏈推導——若推導出「A→A」（自配對，不可能，因 S 是對合且由接線板規則不配自己）或「A→兩個不同字母」（矛盾），則假設錯誤。

**炸彈機**：36 台 Enigma 等價機器串聯，機械化執行矛盾排除——每個假設配對電路連動，燈亮 = 矛盾。Welchman 的 **diagonal board** 改進利用 $S$ 的對合性加倍排除效率。窮舉 $26^3$ 轉子位置 × 26 配對假設，機器數小時內找出轉子組態。

### 程式碼：矛盾排除的概念

```python
import random

def bombe_elimination(crib, cipher, rotor_perms):
    """概念：假設配對 -> 邏輯鏈 -> 矛盾排除"""
    pairs = {}                       # 已確定的接線板配對
    for x, c in zip(crib, cipher):
        # 若 x 的配對已知，沿鏈傳播
        contradiction = False
        if x in pairs and pairs[x] == x: contradiction = True  # 自配對
        if x in pairs and c in pairs and pairs[x] != pairs[c]:
            contradiction = True     # 一字兩配
        if contradiction:
            return False             # 此假設錯誤
        pairs[x], pairs[c] = pairs[c], x
    return True

random.seed(42)
# 概念示範：E(x) != x 的排除法
plug = {0: 25, 1: 24, 2: 3, 3: 2}
# 炸彈機的推理：假設 A↔Z，推導中若出現 A↔A（自配）即矛盾
print("炸彈機：36 台 Enigma 串聯，機械化矛盾排除")
print("Welchman 的 diagonal board：利用 S 對合性加倍排除")
```

### Colossus：第一台電子電腦（1943）
德國高層通訊用**Lorenz 密碼機**（12 轉子 teleprinter 密碼）。Max Newman 與 Tommy Flowers 建造 **Colossus**：1500 個真空管，機械化執行**統計相關性分析**（找 Lorenz 輪盤的設定）——**第一台電子數位可程式化電腦**（1943 年運作，比 ENIAC 早兩年）。

**Turing 的圖靈機**（1936，見 `../計算理論/1936-Turing機與停機問題.md`）的理論在此變成工程現實：**可程式化的機器**——炸彈機、Colossus 都是圖靈機的先行工程實現，直接催生戰後的 ACE、Manchester 機。

### 超越：Ultra 情報的運用
- **大西洋海戰**：破譯 U-boat 通訊，護航船隊避開狼群——1941 年 5 月起船損大減
- **北非**：Rommel 的補給線被斷
- **諾曼第**：D-Day 前的德軍調動全被監視
- **歷史估計**：Ultra 縮短戰爭約兩年（Hinsley）

**保密的鐵律**：破譯成果絕不直接使用（否則德國察覺），只「恰好」派偵察機確認——**情報的運用本身也是密碼戰的一部分**。

## 結案 -- 後果與影響
- **二戰勝利**：Ultra 情報縮短戰爭、改變戰局——密碼學第一次決定世界史。
- **計算機的誕生**：Colossus（1943）、bomba 的工程經驗直接催生戰後電腦（Turing 的 ACE、Manchester Baby 1948）。
- **密碼分析的工業化**：矛盾排除法、統計分析、機械化窮舉——現代密碼分析（差分、線性分析）的祖先。
- **Turing 的兩面**：1936 年的圖靈機（理論）與 1940 年的炸彈機（工程）——理論與工程的閉環。
- **保密文化**：Bletchley Park 的工作保密至 1974 年（《Ultra Secret》出版）——Turing 的戰時功績在他死後 20 年才公開。

## 關鍵人物與文獻
- **Alan Turing**（1912–1954）：炸彈機設計（1940）；1952 年因同性戀定罪，1954 年逝世，2013 年王室赦免
- **Gordon Welchman**：diagonal board
- **Tommy Flowers**（1905–1998）：Colossus
- **Max Newman**：Colossus 概念
- **F. H. Hinsley**：British Intelligence in the Second World War——「縮短兩年」的估計
- **Harry Hinsley / Winterbotham**：The Ultra Secret (1974)——解密揭露
- 交叉參照：`1932-Rejewski破譯Enigma.md`、`1918-Enigma機.md`、`../計算理論/1936-Turing機與停機問題.md`
