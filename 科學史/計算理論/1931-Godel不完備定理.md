# 1931 - Gödel 不完備定理

## 案件摘要
1931 年，25 歲的 Gödel 發表《論〈數學原理〉及相關系統中的形式不可判定命題》，證明：任何足夠強的一致形式系統都存在「真但不可證」的命題，且系統無法證明自身的一致性。Hilbert 綱領就此崩塌，而 Gödel 的編碼技術直接啟發了圖靈機與停機問題。

## 前因 -- 為什麼會有這個案子
Hilbert 綱領（見 `1900-Hilbert23問題.md`）承諾：數學可以被一個完備、一致、可判定的形式系統完全涵蓋。1928 年 Hilbert 在 Bologna 又提出三個具體問題：算術的完備性、一致性、以及 $\forall x \exists y$ 型命題的判定。Gödel 原本想**證明**算術的完備性，卻在調查中發現了相反的真相——這是偵探史上最著名的「反向破案」之一。

## 線索與推理 -- 數學式、程式、理論

### Gödel 編碼（Arithmetization）
Gödel 的關鍵武器：把形式系統中的**符號、公式、證明**全部編碼為**自然數**。例如用質數指數法編碼公式 $s_1 s_2 \dots s_n$：

$$\ulcorner s_1 s_2 \dots s_n \urcorner = 2^{e_1} \cdot 3^{e_2} \cdot 5^{e_3} \cdots p_n^{e_n}$$

其中 $e_i$ 是符號 $s_i$ 的編碼，$p_n$ 是第 $n$ 個質數。如此一來：

- 「$x$ 是一個公式」變成關於 $x$ 的**算術性質** $\mathrm{Formula}(x)$
- 「$y$ 是 $x$ 的證明」變成**算術關係** $\mathrm{Proof}(y, x)$
- 「$x$ 可證明」變成 $\mathrm{Prov}(x) \equiv \exists y\, \mathrm{Proof}(y, x)$

整個「語法」被翻譯成「算術」——形式系統可以**談論自己**！

### 對角線法與自我指涉
利用對角線法（源自 Cantor 的對角線論證），Gödel 構造了一個句子 $G$，它說「我自己不可證明」：

$$G \leftrightarrow \neg\mathrm{Prov}(\ulcorner G \urcorner)$$

技術上，這透過一個可計算的對角線函數 $\delta$ 達成：對每個含一個自由變數的公式 $\varphi(x)$，

$$\delta(\varphi) = \varphi(\ulcorner \varphi \urcorner)$$

存在不動點（對角線引理）：對任意公式 $\psi(x)$，存在句子 $\sigma$ 使得

$$T \vdash \sigma \leftrightarrow \psi(\ulcorner \sigma \urcorner)$$

取 $\psi(x) = \neg\mathrm{Prov}(x)$，即得 $G$。

### 第一不完備定理
**定理**：若 $T$ 是一致的（且遞迴可公理化、包含足夠的算術，如 Robinson 算術 $Q$），則存在句子 $G$ 使得 $T \nvdash G$ 且 $T \nvdash \neg G$。

推理鏈：
1. 若 $T \vdash G$，則存在 $y$ 是 $G$ 的證明，故 $T \vdash \mathrm{Prov}(\ulcorner G \urcorner)$，即 $T \vdash \neg G$ → 矛盾（一致性）。
2. 若 $T \vdash \neg G$，即 $T \vdash \neg\neg\mathrm{Prov}(\ulcorner G\urcorner)$……更細緻地用 $\omega$-一致性（或 Rosser 1936 年改用簡單一致性）導出矛盾。
3. 故 $T$ 不完備。

而在**標準模型** $\mathbb{N}$ 中，$G$ 恰好是**真**的（因為它確實沒有證明）：真 $>$ 可證。

### 第二不完備定理
**定理**：若 $T$ 一致且足夠強，則

$$T \nvdash \mathrm{Con}(T)$$

其中 $\mathrm{Con}(T) \equiv \neg\mathrm{Prov}(\ulcorner 0 = 1 \urcorner)$。

即：系統**無法證明自身的一致性**——Hilbert 綱領的核心目標（用有窮方法證明算術一致性）在原則上不可能達成。

### 程式碼：對角線引理的模擬
```python
# 模擬 Gödel 編碼與自我指涉（玩具版）
def encode(formula):
    """質數指數法：把字串編成自然數"""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    code = 1
    for i, ch in enumerate(formula):
        code *= primes[i] ** ord(ch)
    return code

def provable(code):
    """玩具版證明檢查器：假設 code 是偶數就「可證明」"""
    return code % 2 == 0

# 對角線句 G：「我不可證明」
G = encode("G ↔ not Prov(G)")
print("G 的 Gödel 數：", G)
print("G 可證明嗎？", provable(G))

# 第一不完備定理的邏輯結構：
# 若 provable(G) 為 True，則 provable(not G) 也為 True -> 矛盾
# 若 provable(not G) 為 True，則（用 omega-一致性）矛盾
# 故 G 不可判定：真但不可證。
```

### 對計算理論的直接啟發
Gödel 編碼告訴我們：**推理可以被算術化** ⟹ **計算可以模擬推理**。Turing (1936) 與 Kleene 立即吸收了這一點：

- Gödel 對「不可判定命題」的對角線構造 ⟹ Turing 的「停機問題」對角線證明：$H(M, x) = \neg M(M, x)$（見 `1936-Turing機與停機問題.md`）
- Gödel 的 $\mathrm{Prov}(x)$ 是遞迴可枚舉但非遞迴的集合 ⟹ 不可計算函數的具體例子
- Kleene 的規範形式定理、Church 的不可判定性結果，全部建立在 arithmetization 之上

事實上，可以證明：**停機問題與不完備定理是同一枚硬幣的兩面**——若停機問題可判定，就能構造完備且一致的算術系統。

## 結案 -- 後果與影響
- **擊潰 Hilbert 綱領**：完備性不可能（第一定理）、自我一致性證明不可能（第二定理）。但「有窮方法證明一致性」在 Gentzen (1936) 的改良形式下部分復活（用超越 Peano 算術的歸納法證明 PA 一致）。
- **數學基礎的轉向**：從「尋找完備系統」轉向「研究不可證明性本身」——證明論、遞迴論、模型論三足鼎立。
- **計算理論誕生**：Gödel 編碼 + 對角線法 = 不可計算性的標準工具箱；圖靈機、通用電腦、程式語言皆受其惠。
- **哲學衝擊**：數學真理超越形式證明（Platonism 的強力論證）；Lucas–Penrose 以此論證人心靈超越機器（爭議至今）。
- 1963 年 Cohen 用力迫法證明連續統假設獨立於 ZFC——不完備性從算術蔓延到集合論。

## 關鍵人物與文獻
- **Kurt Gödel**（1906–1978）：Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I (1931, Monatshefte für Mathematik und Physik)
- **J. B. Rosser**（1907–1989）：改進第一定理的證明（1936，只需簡單一致性）
- **David Hilbert, Paul Bernays**：Grundlagen der Mathematik (1934/1939)
- 交叉參照：`1900-Hilbert23問題.md`、`1933-Lambda可定義性.md`、`1936-Turing機與停機問題.md`
