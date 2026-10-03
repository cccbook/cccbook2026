# 1936-Church-Turing 論題與不可判定性

## 案件摘要

1936 年是計算理論史上最不可思議的一年：Church 在 4 月號《Annals of Mathematics》發表 "A note on the Entscheidungsproblem"，Turing 在《Proc. London Math. Soc.》發表 "On Computable Numbers, with an Application to the Entscheidungsproblem"——兩人使用完全不同的工具（λ-Calculus 與圖靈機），在同一年獨立證明了同一個結果：Hilbert 的判定問題無解。更戲劇性的是，Turing 在論文附錄中證明了兩個模型互相模擬、完全等價。這起「雙偵探同時破案」事件，誕生了「什麼是可計算」的正式定義。

## 前因 -- 為什麼會有這個案子

- Hilbert 在 1928 年國際數學家大會（Bologna）正式提出 Entscheidungsproblem（判定問題）：是否存在一個機械程序，能對任意一階邏輯命題判定其是否可證？
- 這是 Hilbert 計畫的最後堡壘：若判定問題可解，則一切數學問題原則上都能被機械回答。
- Gödel 1931 年的不完備定理已經打了 Hilbert 計畫一記重拳：任何足夠強的一致系統必有不可證的真命題。但「機械程序是否存在」仍需正式定義「機械程序」本身。
- 案件的偵探難題：要證明「不存在這樣的程序」，必須先精確定義「程序」——這是人類史上第一次需要定義「計算」。
- Church 選擇 λ-可定義性作為「可有效計算」的形式化；Turing 選擇了他設想的單一紙帶機器。兩條完全獨立的偵查路線，指向同一個兇手。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Church 的路線——λ-可定義性

Church 的論證結構（用現代語言重述）：

$$\text{可有效計算} \;\Longleftrightarrow\; \lambda\text{-可定義}$$

- Church 與 Kleene 已證明： Gödel 的原始遞迴函數都是 λ-可定義的；Kleene 1936 年更證明所有一般遞迴函數都是 λ-可定義的。
- 既然一階邏輯的可證性可被編碼為自然數上的關係，而 λ-Calculus 中可以證明「判定可證性的函數」不是 λ-可定義的（透過對角化/Richard 式論證），因此判定問題無解。
- Church 在論文中明確承認這個定義的選擇需要辯護——這個辯護後來被稱為 Church 論題。

### 線索二：Turing 的路線——停機問題與對角化

Turing 定義了圖靈機：紙帶、讀寫頭、有限狀態。停機問題：是否存在機器 $H$，對任意 $(M, w)$ 判定 $M$ 是否在輸入 $w$ 上停機？

假設 $H$ 存在，構造「唱反調者」$D$：

$$D(x) = \begin{cases} \text{無限迴圈} & \text{if } H(x, x) = \text{停機} \\ \text{停機} & \text{if } H(x, x) = \text{不停機} \end{cases}$$

則 $D(D)$ 導致矛盾：$D(D)$ 停機若且唯若 $D(D)$ 不停機。因此 $H$ 不存在——這就是破案時刻。

Python 對角化模擬：

```python
# 停機問題對角化（符號模擬）
# 假設「所有程式」構成完整清單，且存在停機判定器 H
HALTS = {f"P{i}": (i % 2 == 0) for i in range(4)}   # 每個程式對自己的行為

def H_(p):
    return HALTS[p]

def D(p):
    "D(x): 若 x 對自己停機，則 D 不停機；否則 D 停機"
    if H_(p):
        return "loops forever"
    return "halts"

# 對每個 i：D(Pi) 的行為與 Pi 對自己的行為必然「相反」
for i in range(4):
    pi = f"P{i}"
    pi_self = H_(pi)
    d_on_pi = (D(pi) == "halts")
    assert d_on_pi != pi_self, "D 與清單中的程式相同？矛盾！"

# 所以 D 與清單中每一個程式的行為都相異
# -> D 不在「所有程式」清單中 -> H 不存在
print("對角線論證驗證：D 與清單中所有程式相異 => H 不存在")
```

### 線索三：Turing 的附錄——兩個模型互相模擬

Turing 在 1936 年論文的附錄（1937 年刊出）中證明：任何 λ-可定義函數都可以由圖靈機計算，反之亦然。他建構了一個在圖靈機上模擬 λ 歸約的編碼方案（λ 項編碼為紙帶上的字串，歸約步驟編碼為機器狀態轉移）：

$$\lambda\text{-可定義} \;\Longleftrightarrow\; \text{圖靈可計算}$$

這個等價性使兩條獨立偵查路線合流：Church 論題與 Turing 論題合併為 Church-Turing 論題。

### 線索四：Church-Turing 論題

一切「可有效計算」的函數，恰好就是：

$$\text{可有效計算} = \text{圖靈可計算} = \lambda\text{-可定義} = \text{一般遞迴}$$

- 這是一個「論題」而非定理：它的「可有效計算」一側是非形式概念，無法被形式證明。
- 但所有被提出的計算模型（無限多種）最後都被證明等價於圖靈機——強力的經驗證據。
- 推論：存在不可計算的函數（如停機問題），也存在不可判定的數學命題。

### 線索五：通用圖靈機

Turing 論文中最深遠的發現：存在一台「通用圖靈機」$U$，讀入任意機器 $M$ 的編碼 $\langle M \rangle$ 與輸入 $w$，即可模擬 $M(w)$：

$$U(\langle M \rangle, w) = M(w)$$

這是「軟體」概念的誕生：程式可以作為資料被另一支程式處理——現代電腦、直譯器、虛擬機器全部由此而來。λ-Calculus 中的自應用（$x\,x$）與 Y 組合子，正是這個自我指涉能力的函數式版本。

## 結案 -- 後果與影響

- 案件偵破：判定問題無解；「可有效計算」獲得精確定義，計算理論（computability theory）正式誕生。
- λ-Calculus 從邏輯工具升格為計算模型，與圖靈機平起平坐。
- Gödel 起初對 Church 的 λ 定義存疑（1935 年左右曾表示不滿意），但在讀到 Turing 的分析後完全信服——他認為 Turing 的證明才是決定性的。
- 1936-38 年：Kleene 發展遞迴函數論、Post 提出郵機（Post machine）；所有模型等價。
- 1956 年 Dartmouth 會議（AI 誕生）的參與者（McCarthy、Minsky、Shannon）都直接繼承這條血脈；McCarthy 的 LISP 選擇 λ-Calculus 而非圖靈機作為哲學根基。
- 可計算性理論成為理論電腦科的基礎：P vs NP、不可判定性、歸約（reduction）全部源自本案。
- 哲學餘波：Church-Turing 論題的擴充版本（物理 Church-Turing 論題、hypercomputation 爭論）至今仍在辯論。

## 關鍵人物與文獻

- Alonzo Church（1903-1995）：λ-Calculus 之父，以 λ-可定義性破解判定問題。
  - A. Church, "A note on the Entscheidungsproblem", Journal of Symbolic Logic, 1(1):40-41, 1936; 修正與附註：1(3):101-102, 1936.（另見 American Journal of Mathematics, 58:345-363, 1936）
- Alan M. Turing（1912-1954）：圖靈機與停機問題的發明者。
  - A. M. Turing, "On Computable Numbers, with an Application to the Entscheidungsproblem", Proceedings of the London Mathematical Society, s2-42:230-265, 1936（1937 年刊出）; 修正：s2-43:544-546, 1937.
- David Hilbert（1862-1943）：判定問題的提出者，Hilbert 計畫的核心。
- Kurt Gödel（1906-1978）：不完備定理的發現者，使「機械程序」的定義成為必要。
- Stephen Kleene（1909-1994）：遞迴函數論與 λ-可定義性的系統化。
  - S. C. Kleene, "General recursive functions of natural numbers", Mathematische Annalen, 112:727-742, 1936.
- Emil Post（1897-1954）：獨立發展等價的計算模型。
  - E. L. Post, "Finite combinatory processes - formulation 1", Journal of Symbolic Logic, 1(3):103-105, 1936.
- 參考：Martin Davis, "Computability and Unsolvability", McGraw-Hill, 1958; "The Universal Computer: The Road from Leibniz to Turing", W. W. Norton, 2000.
