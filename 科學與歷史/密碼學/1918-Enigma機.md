# 1918 - Enigma 機

## 案件摘要
1918 年，德國工程師 Arthur Scherbius 發明 Enigma 密碼機：轉子步進 + 反射器的電動密碼機，金鑰空間約 $10^{23}$——天文數字。德國軍方 1926 年起全面採用，深信不可破譯。但這台機器有一個「神來之筆」的設計缺陷——**反射器讓字母永遠加密成別的字母**——這個「方便」（自加密）的設計成為 1932 年 Rejewski 數學破譯（見 `1932-Rejewski破譯Enigma.md`）與 1939 年 Turing 炸彈機（見 `1939-BletchleyPark.md`）的突破口。

## 前因 -- 為什麼會有這個案子
一戰的教訓：德國的海底電報密碼被英國破譯（Zimmermann 電報 1917 引美國參戰）。戰後德國軍方全面換新密碼。Scherbius 的商業動機：把機械化的轉子密碼機賣給企業與軍方。Enigma 的設計融合了當時的轉子密碼機浪潮（美國 Hebern、荷蘭 Koch、瑞典 Hagelin）——但它的**反射器（reflector）**是獨有設計。

## 線索與推理 -- 數學式、程式、理論

### Enigma 的結構
每按一個鍵，電流流經：

1. **接線板（plugboard）**：10 對字母互換（$S$）
2. **三個轉子**：各是一個置換（$R_1, R_2, R_3$），右轉子每鍵步進一位
3. **反射器（reflector）**：一個**無不動點的對合置換**（$F$，每個字母映到別的字母）
4. 電流原路返回（轉子反向經過）

加密函數：

$$E = S^{-1} R_1^{-1} R_2^{-1} R_3^{-1} F R_3 R_2 R_1 S$$

每鍵之後轉子步進，$R_1$ 變化——同一字母連按兩次加密成不同字母（消滅了簡單頻率分析）。

### 金鑰空間
- 接線板：$\frac{26!}{10! \, 2^{10} 6!} \approx 1.5 \times 10^{14}$
- 轉子選擇與順序：$26 \times 25 \times 26 \approx 1.7 \times 10^{4}$（海軍版 8 轉子選 3）
- 轉子起始位置：$26^3 = 17576$

**總計約 $10^{23}$**——當時無法窮舉。德國深信「金鑰空間大 = 安全」。

### 致命缺陷：反射器的對合性
**反射器 $F$ 是對合**（involution）：$F(F(x)) = x$，且**無不動點**：$F(x) \ne x$。

**後果**：

$$E(x) \ne x \quad \text{永遠成立！}$$

**任何字母永遠加密成別的字母**——這看似增強（無不動點），實為致命：

1. **排除法攻擊**：明文字母永不對應自己，窮舉時可排除大量可能
2. **循環結構洩漏**：對合性使加密函數具有特殊代數結構——Rejewski 正是用這個結構（見 `1932-Rejewski破譯Enigma.md`）

**偵探筆記**：反射器的「方便性」是誘餌——設計者的理由是「加密 = 解密，操作員不用切換模式」。**工程便利導致數學結構洩漏**——這個教訓與 Kerckhoffs 原則（見 `1883-Kerckhoffs原則.md`）同源：安全性不能依賴「結構沒人看見」。

### 程式碼：模擬 Enigma

```python
class Enigma:
    def __init__(self, rotors, reflector, plugboard, positions):
        # 轉子：置換字典；plugboard: 對合對；positions: 起始步進
        self.rotors = rotors
        self.reflector = reflector
        self.plug = dict(plugboard)
        self.pos = list(positions)

    def step(self):
        """轉子步進（簡化：右轉子每鍵 +1）"""
        self.pos[0] = (self.pos[0] + 1) % 26
        if self.pos[0] == 0:
            self.pos[1] = (self.pos[1] + 1) % 26
            if self.pos[1] == 0:
                self.pos[2] = (self.pos[2] + 1) % 26

    def rotor_pass(self, x, rotor, pos, reverse=False):
        if reverse:
            return sorted(rotor.items(), key=lambda kv: kv[1])[x % 26][0]
        return (rotor[(x + pos) % 26] - pos) % 26

    def encrypt_char(self, x):
        self.step()
        x = self.plug.get(x, x)                    # 接線板
        for i, r in enumerate(self.rotors):
            x = self.rotor_pass(x, r, self.pos[i])
        x = self.reflector[x]                      # 反射器（對合！）
        for i, r in reversed(list(enumerate(self.rotors))):
            x = self.rotor_pass(x, r, self.pos[i], reverse=True)
        x = self.plug.get(x, x)                    # 接線板回程
        return x

A = lambda s: {i: (i + int(n)) % 26 for i, n in enumerate(s)}
# 簡化示範：三轉子、反射器無不動點
reflector = {0: 5, 1: 7, 2: 9, 3: 11, 4: 13, 5: 0, 6: 15, 7: 1, 8: 17, 9: 2,
             10: 19, 11: 3, 12: 21, 13: 4, 14: 23, 15: 6, 16: 25, 17: 8,
             18: 20, 19: 10, 20: 18, 21: 12, 22: 24, 23: 14, 24: 22, 25: 16}
assert all(reflector[reflector[i]] == i and reflector[i] != i for i in range(26))
enigma = Enigma([A("11002541009112234"), A("73019112205411092"),
                 A("1223411009117205")], reflector, [(0, 25), (1, 24)], [0, 0, 0])
print(enigma.encrypt_char(0))    # 同一字母永不加密成自己：E(x) != x 恒成立
```

## 結案 -- 後果與影響
- **破譯的譜系**：Rejewski (1932) 的數學破譯 → Turing (1939–40) 的炸彈機 → Ultra 情報（縮短二戰約兩年，歷史學家估計）。
- **現代電腦的催生**：Bletchley Park 的 Colossus（1943）是第一台電子數位電腦——密碼戰催生了計算機。
- **工程便利 = 安全弱點**：反射器的教訓——現代密碼設計審查「每個工程決定的數學後果」。
- **金鑰空間 ≠ 安全**：$10^{23}$ 的金鑰空間擋不住「結構性破譯」——Shannon (1949) 之後這成為定理級的常識。

## 關鍵人物與文獻
- **Arthur Scherbius**（1878–1929）：Enigma 專利 (1918)
- **Marian Rejewski**（1905–1980）：1932 數學破譯（見 `1932-Rejewski破譯Enigma.md`）
- **Alan Turing**（1912–1954）：炸彈機（見 `1939-BletchleyPark.md`）
- **Gordon Welchman**（1906–1985）：炸彈機的 diagonal board 改進
- 交叉參照：`1932-Rejewski破譯Enigma.md`、`1939-BletchleyPark.md`、`1883-Kerckhoffs原則.md`
