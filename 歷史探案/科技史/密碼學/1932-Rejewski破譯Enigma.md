# 1932 - Rejewski 破譯 Enigma

## 案件摘要
1932 年 12 月，28 歲的波蘭數學家 Marian Rejewski 用**純代數**（置換群論）破譯了德國 Enigma 機——不是靠頻率分析，而是靠「循環指標」的代數結構。波蘭密碼局（Biuro Szyfrów）從此能讀德國軍情，並在 1939 年戰爭爆發前夕把全部成果移交英法——英國 Bletchley Park 的 Turing 炸彈機（見 `1939-BletchleyPark.md`）正是站在 Rejewski 的肩膀上。**數學第一次在密碼戰中擊敗機器。**

## 前因 -- 為什麼會有這個案子
1926 年起，波蘭軍方發現德國通訊使用 Enigma，傳統頻率分析完全失效（轉子步進消滅了單表統計）。波蘭密碼局做了關鍵決定：**招募數學家**——從 Poznań 大學數學系選拔（Rejewski、Różycki、Zygalski）。Rejewski 的問題：**Enigma 的置換結構，能否用代數直接破解？**

## 線索與推理 -- 數學式、程式、理論

### 線索一：每日金鑰的「指示器」程序
1932 年時，德軍的密鑰程序：每日金鑰（接線板、轉子順序、起始位置）由密碼本規定，操作員自選**訊息金鑰**（message key）——三個字母，**連打兩次**加密後作為指示器發出：

$$\text{指示器} = E(K_{msg})E(K_{msg}) = E(k_1)E(k_2)E(k_3)E(k_1)E(k_2)E(k_3)$$

（第 1 與第 4 個字母是同一字母 $k_1$ 的兩次加密，因間隔 3 步，加密函數不同。）

**這個「連打兩次」的安全冗餘程序，成為破譯的線索。**

### 循環指標（cycle index）的代數
定義：$A$ = 第 1 位置的加密置換，$B$ = 第 4 位置的加密置換。指示器的第 1、4 字母關係：

$$B = P^3 A P^{-3} \quad \text{（其中 } P \text{ 是轉子步進置換）}$$

Rejewski 定義**特徵置換**：

$$Q = A B^{-1}$$

**關鍵定理**：$Q$ 的循環結構（cycle index：循環的長度分佈，如 (13)(4)(4)(2)(1)(1)(1)）**只依賴轉子順序與起始位置，不依賴接線板**！

（證明骨架：接線板 $S$ 是共軛操作——$Q$ 與其共軛版本循環結構相同。）

**於是**：窮舉所有轉子組態（$26^3 \times 3! \approx 10^5$ 種），建表記錄每種的循環指標；從實際通訊計算 $Q$ 的循環指標，**查表**得到轉子組態——**接線板再複雜都無關緊要**。

### 求解接線板
轉子組態已知後，Rejewski 用置換代數直接解接線板：由 $E = S^{-1} R S$ 型關係，解線性方程組般的置換方程——**數學取代窮舉**。

### Rejewski 的機器：bomba（波蘭炸彈機）
1938 年，德軍改進密鑰程序（訊息金鑰不再連打兩次），循環指標法失效。Rejewski 發明「bomba」機器：6 台 Enigma 串聯機械窮舉轉子組態——**機械化的代數**。Zygalski 另發明「Zygalski 板」（打孔卡片排除法）。

### 程式碼：循環指標的概念

```python
import random

def perm_compose(p, q):
    return {x: p[q[x]] for x in p}

def perm_inverse(p):
    return {v: k for k, v in p.items()}

def perm_apply(p, x):
    return p[x]

def cycle_index(p):
    """置換的循環長度分佈"""
    seen, cycles = set(), []
    for x in p:
        if x not in seen:
            c, y = 0, x
            while y not in seen:
                seen.add(y); y = p[y]; c += 1
            cycles.append(c)
    return sorted(cycles, reverse=True)

random.seed(42)
# 反射器（對合、無不動點）
F = {0: 5, 1: 7, 2: 9, 3: 11, 4: 13, 5: 0, 6: 15, 7: 1, 8: 17, 9: 2,
     10: 19, 11: 3, 12: 21, 13: 4, 14: 23, 15: 6, 16: 25, 17: 8,
     18: 20, 19: 10, 20: 18, 21: 12, 22: 24, 23: 14, 24: 22, 25: 16}
step = lambda x: (x + 3) % 26                     # 3 步進置換 P^3

def enigma_perm(plug, pos1, pos2, pos3):
    """簡化：接線板 + 三轉子 + 反射器的置換"""
    rot = lambda x: (x + pos1) % 26
    E = {}
    for x in range(26):
        y = plug.get(x, x)
        y = (y + pos1) % 26
        y = (y + pos2) % 26
        y = (y + pos3) % 26
        y = F[y]
        y = (y - pos3) % 26
        y = (y - pos2) % 26
        y = (y - pos1) % 26
        E[x] = plug.get(y, y)
    return E

plug = {0: 25, 1: 24, 2: 3, 3: 2}
E1 = enigma_perm(plug, 0, 0, 0)                   # 第 1 位置
E4 = perm_compose(E1, perm_compose(step, perm_inverse(step)))  # 概念
Q = perm_compose(E1, perm_inverse(E4))
print(f"Q 的循環指標 = {cycle_index(Q)}")
# Rejewski 的洞察：循環指標不依賴接線板 S——可查表得轉子組態
```

### 1939 年的移交
1939 年 7 月，波蘭在華沙附近 Pyry 森林召開秘密會議，把 Rejewski 的全部成果（bomba、Zygalski 板、複製的 Enigma）移交英法。英國 Bletchley Park 的 Turing 三週後寫出炸彈機草圖——**英國的破譯建築在波蘭的數學上**。

## 結案 -- 後果與影響
- **Ultra 情報**：Bletchley Park 的破譯（大西洋海戰、北非戰場）縮短二戰約兩年，拯救數百萬人命。
- **數學密碼分析的誕生**：置換群論、代數結構攻擊成為密碼分析的標準武器（至今的線性/差分密碼分析都是其後代）。
- **招募數學家的範式**：密碼機構從「語言學家」轉向「數學家」——NSA、GCHQ 的數學家團隊。
- **計算機的誕生**：bomba → Colossus → 現代電腦，密碼戰是計算機的搖籃。
- **Rejewski 的正名**：戰後他被共產波蘭忽視數十年，1970 年代才獲承認——密碼學史的最大冤案之一。

## 關鍵人物與文獻
- **Marian Rejewski**（1905–1980）：循環指標法、bomba
- **Jerzy Różycki、Henryk Zygalski**：波蘭密碼三傑
- Rejewski: An Application of the Theory of Permutations... (1980 回顧，原始成果 1932–38 為機密)
- **Bletchley Park**：見 `1939-BletchleyPark.md`
- 交叉參照：`1918-Enigma機.md`、`1939-BletchleyPark.md`、`1883-Kerckhoffs原則.md`
