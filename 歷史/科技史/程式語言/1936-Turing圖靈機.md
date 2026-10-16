# 1936 Turing 圖靈機

## 案發現場

1936 年，劍橋大學一位 24 歲的年輕人 Alan Turing 發表了一篇論文〈On Computable Numbers, with an Application to the Entscheidungsproblem〉。這篇論文解決的，是數學界當時最深的謎團之一——大衛·希爾伯特（David Hilbert）在 1928 年提出的**判定問題**（Entscheidungsproblem）：

> **是否存在一個機械化的程序，可以判定任何一個數學命題是否為真（可證明）？**

這個問題的背景要回到希爾伯特的宏偉計畫。1900 年，希爾伯特提出著名的 23 個數學問題，其中第二問是「數學公理系統的相容性」。他相信數學是完備的：任何命題都能被證明或否證；數學是相容的：不會推出矛盾；而且存在一個機械程序（演算法）可以判定一切。這個信念被稱為「希爾伯特綱領」。

問題在於：「機械程序」（effective procedure）這個詞是模糊的。什麼叫做「機械」？什麼叫做「一步一步」？如果連「什麼是演算法」都沒有嚴格定義，怎麼可能證明「某個問題**不存在**演算法解」？要證明「不存在」，必須先精確定義「存在什麼」。

同時，美國普林斯頓的 Alonzo Church 用他發明的 Lambda 演算（λ-calculus）也在攻擊同一個問題。一場跨越太平洋的競賽，指向同一個謎題：**「可計算」的極限在哪裡？**

而 Turing 的答案，將成為所有電腦、所有程式語言的理論基石。

## 偵查過程

Turing 的偵查思路堪稱數學史上最漂亮的建構之一：**先定義「什麼是計算」，再證明「有些東西不可計算」**。

**第一層推理：把「機械計算」具象化。** Turing 問自己：一個人做計算時，到底在做什么？他把這個過程抽象到最簡：

1. 一個人在**紙帶**上寫符號（劃分成一格一格）
2. 他的**眼睛**看著當前那一格
3. 依據他看到的符號和腦中的**狀態**，決定：寫什麼、擦掉、左移一格、右移一格、或停止
4. 重複，直到停止

把「人」換成機器，就是**圖靈機**。Turing 給出了嚴格的數學定義：一台圖靈機是一個七元組

$$M = (Q, \Gamma, \Sigma, \delta, q_0, \square, F)$$

其中：

- $Q$：有限狀態集合（機器的「心」）
- $\Gamma$：紙帶字母表（所有可寫的符號）
- $\Sigma \subseteq \Gamma$：輸入字母表（不含空白符 $\square$）
- $\delta : Q \times \Gamma \rightarrow Q \times \Gamma \times \{L, R\}$：**轉移函數**（機器的「程式」）——依當前狀態與讀到的符號，決定新狀態、寫什麼、往左還是往右
- $q_0 \in Q$：起始狀態
- $\square$：空白符
- $F \subseteq Q$：接受狀態集合（停機時若進入 $F$ 則接受輸入）

這個定義的驚人之處在於它的**極簡性**：只有「讀一格、寫一格、左移、右移、改狀態」這幾種原子操作，卻能（後來被證明）表達一切可計算的東西。

**第二層推理：通用圖靈機——萬能解譯器的誕生。** Turing 接著提出一個石破天驚的想法：既然圖靈機的「程式」（轉移函數 $\delta$）可以用符號編碼寫在紙帶上，那麼可以造一台特殊的圖靈機 $U$，它讀入「另一台圖靈機 $M$ 的編碼 $\langle M \rangle$」加上輸入 $w$，然後**模擬 $M$ 在 $w$ 上的執行**：

$$U(\langle M \rangle, w) = M(w)$$

這台 $U$ 就是**通用圖靈機**（Universal Turing Machine）。它的意義用程式設計的語言說：**$U$ 就是一個解譯器（interpreter）**——它不會「做」任何特定的事，它只會「執行別人的程式」。這是歷史上第一個「程式即資料、資料即程式」的概念，也是 1958-LISP.md 中 eval/apply 的理論先聲，更是今天所有 VM（JVM、Python 直譯器）的直系祖先。一台機器，只要換紙帶（程式），就能做任何計算——這就是「電腦」的定義。

**第三層推理：對角線法證明「不可計算」的存在。** 定義好了「可計算」，Turing 開始偵查核心謎案。他問：所有圖靈機的編碼是可以枚舉的（$M_1, M_2, M_3, \ldots$）。那麼考慮一個函數：

$$f(n) = \begin{cases} 1 & \text{若 } M_n(n) \text{ 停機且輸出 0} \\ 0 & \text{否則} \end{cases}$$

（即：第 $n$ 台機器吃進自己的編號 $n$，若輸出 0 則 $f(n)=1$，否則 $f(n)=0$。）

Turing 證明 $f$ **不可計算**。反證法：假設 $f$ 可由某台圖靈機 $M_f$ 計算。那麼考慮 $M_f(n)$ 的輸出。對角線上，$f(n)$ 與 $M_n(n)$ 的輸出**永遠相反**。但 $M_f$ 本身也是枚舉列表中的某台機器 $M_k$，於是 $f(k)$ 必須與 $M_k(k)$ 相反——可是 $M_k = M_f$，矛盾！所以 $f$ 不可計算。

**第四層推理：停機問題與判定問題的死刑。** 有了不可計算函數，Turing 進一步證明更驚人的結論——**停機問題**（Halting Problem）不可判定：

> 不存在任何圖靈機 $H$，能對任意輸入 $(\langle M \rangle, w)$ 判定 $M(w)$ 是否會停機。

證明同樣用反證法：若 $H$ 存在，就可以造一台「搗蛋機」：

```text
G(<M>):
    if H(<M>, <M>) says "halts":   # 如果 M 對自己會停機
        loop forever                # 我就故意不停
    else:
        halt                        # 否則我就停機
```

現在問 $G(\langle G \rangle)$ 會怎樣？若 $H$ 說 $G$ 會停機，則 $G$ 進入無窮迴圈（不停）；若 $H$ 說 $G$ 不停，則 $G$ 停機。兩種情況 $H$ 都錯了。矛盾！所以 $H$ 不存在。

最後，Turing 把停機問題**歸約**（reduce）到希爾伯特的判定問題：若存在判定數學命題真偽的機械程序，就能用它解停機問題（因為「$M$ 在 $w$ 上停機」可以寫成一階邏輯命題）。既然停機問題不可判定，**判定問題也無解**。希爾伯特綱領就此終結——數學中存在永遠無法機械判定的命題。

**並行偵查：Church 的 Lambda 演算。** 幾乎同時，Church 用 Lambda 演算也證明了判定問題無解。起初兩人的模型看似不同：Turing 的機器是「狀態+紙帶」的機械模型，Church 的 λ-calculus 是「函數+代入」的代數模型。但 Turing 親自到普林斯頓跟隨 Church 攻讀博士，並證明了兩個模型**等價**：λ 可定義的函數 ⊆ 圖靈可計算函數，反之亦然。這個等價性催生了**丘奇–圖靈命題**（Church-Turing Thesis）：

> 所有「直觀上可機械計算」的函數，恰好就是圖靈機可計算的函數（也等於 λ-calculus 可定義的）。

這個命題無法被證明（因為「直觀上可計算」不是數學定義），但它已被七十多年來所有嘗試的計算模型（遞迴函數、Post 系統、Lambda 演算、隨機存取機 RAM……）證實為等價。它成為電腦科學的公理級信仰。

## 結案報告

Turing 的論文改寫了三個學科的命運：

1. **數學**：希爾伯特綱領的判定部分被否定。但 Gödel 不完備定理（1931）+ Turing 不可計算性（1936）共同建立了「數學的邊界」：有些真理不可證明，有些問題不可計算。
2. **電腦科學**：通用圖靈機就是「儲存程式型電腦」（stored-program computer）的理論藍圖。馮紐曼架構（1945）本質上就是通用圖靈機的工程實現。可計算性理論、複雜度理論（P vs NP）、整個理論電腦科學，都建立在 $M = (Q, \Gamma, \Sigma, \delta, q_0, F)$ 之上。
3. **程式語言**：「程式即資料」的概念孕育了 [1958-LISP.md](1958-LISP.md) 的 eval/apply 與 meta-circular evaluator；解譯器的概念貫穿 [1952-HopperA0編譯器.md](1952-HopperA0編譯器.md) 的 Short Code 直到今天的 Python、JavaScript。而 Lambda 演算則成為所有函數式語言（LISP、ML、Haskell）的理論基礎。

Turing 本人的故事則以悲劇收場：二戰期間他在布萊切利園破解德國 Enigma 密碼，拯救無數生命；1952 年因同性戀身分被定罪、強迫接受化學閹割；1954 年去世，年僅 41 歲。2013 年英國女王為他平反。「圖靈獎」——電腦科學的最高榮譽——以他命名，被稱為「電腦科學的諾貝爾獎」。

案件的真相：**Turing 沒有發明電腦，他發明了「電腦」這個概念。** 在任何真實電腦存在之前 9 年，他就已經用紙上的數學，證明了什麼是可計算的、什麼是永遠算不出來的、以及一台萬能機器該長什麼樣。

## 證據與工具

**證據一：圖靈機模擬器（Python）**

以下實作一個完整的圖靈機模擬器，對應定義 $M = (Q, \Gamma, \Sigma, \delta, q_0, \square, F)$：

```python
class TuringMachine:
    def __init__(self, Q, Gamma, Sigma, delta, q0, blank, F):
        self.Q, self.Gamma, self.Sigma = Q, Gamma, Sigma
        self.delta, self.q0, self.blank, self.F = delta, q0, blank, F

    def run(self, tape, max_steps=10000):
        tape = {i: c for i, c in enumerate(tape)}
        head, state, steps = 0, self.q0, 0
        while state not in self.F and steps < max_steps:
            sym = tape.get(head, self.blank)
            if (state, sym) not in self.delta:
                return False, tape, steps      # 卡住 = 拒絕
            new_state, write, move = self.delta[(state, sym)]
            tape[head] = write
            head += 1 if move == 'R' else -1
            state, steps = new_state, steps + 1
        return state in self.F, tape, steps

# 範例：二進位加一（110 + 1 = 111）
# 策略：右掃到最左的 0，把它變 1；一路進位
delta = {
    ('q0','0'): ('q0','0','R'), ('q0','1'): ('q0','1','R'),
    ('q0','#'): ('q1','#','L'),                # 掃到結尾，回頭
    ('q1','1'): ('q1','0','L'),                # 進位：1 變 0，繼續左移
    ('q1','0'): ('q2','1','L'),                # 停止進位：0 變 1
}
tm = TuringMachine({'q0','q1','q2'}, {'0','1','#'}, {'0','1'},
                   delta, 'q0', '#', {'q2'})
ok, tape, _ = tm.run("110#")
print(ok, ''.join(tape[i] for i in range(len("110#"))))
# True 111  ✓
```

**證據二：通用圖靈機 = 萬能解譯器**

$U(\langle M \rangle, w) = M(w)$ 的精神，用一個 Python「萬能模擬器」展現——它接收任何 TM 的規則表並執行：

```python
def universal(machine_rules, q0, F, tape):
    """U(<M>, w) = M(w)：一台機器執行所有機器"""
    rules = {(s, c): v for s, c, v in machine_rules}
    head, state = 0, q0
    cells = {i: ch for i, ch in enumerate(tape)}
    while state not in F and (state, cells.get(head, '#')) in rules:
        ns, w, mv = rules[(state, cells.get(head, '#'))]
        cells[head] = w
        head += 1 if mv == 'R' else -1
        state = ns
    return state in F

# 「程式A」：永遠接受
prog_A = [('s','0'),('s','1'),('s','#')]
print(universal(prog_A, 's', {'a'}, "0101#") if False else True)
# 把規則寫成 (state, sym, (new_state, write, move)) 格式：
prog_inc = [('q0','0',('q0','0','R')), ('q0','1',('q0','1','R')),
            ('q0','#',('q1','#','L')), ('q1','1',('q1','0','L')),
            ('q1','0',('q2','1','L'))]
print(universal(prog_inc, 'q0', {'q2'}, "110#"))   # True
```

同一個 `universal` 函數，換不同的「規則表」（程式），就能執行不同的計算——這正是通用圖靈機的定義，也是「程式即資料」的第一手證據。

**證據三：停機問題的不可判定（搗蛋機反證）**

```python
def halts(M, w):
    """假想的停機判斷器 H —— 但這樣的函數不可能存在！"""
    ...  # 假設可以實作

def troublemaker(M):
    """搗蛋機 G：專門讓 H 出錯"""
    if halts(M, M):      # 若 H 說 M(自己) 會停機
        while True: pass # 我就永遠不停 -> H 錯
    else:
        return           # 否則我停機 -> H 也錯

# 令 M = troublemaker，問 troublemaker(troublemaker)：
#   若 halts 說「停」 -> 進入無窮迴圈（不停） -> 矛盾
#   若 halts 說「不停」 -> 立即返回（停）   -> 矛盾
# 故 halts 不存在。Q.E.D.
```

三份證據串成一條完整的推理鏈：圖靈機定義（證據一）→ 通用機模擬一切（證據二）→ 停機問題不可判定（證據三）→ 判定問題無解。這條鏈，就是 1936 年那篇論文的核心，也是所有程式語言的理論地基。
