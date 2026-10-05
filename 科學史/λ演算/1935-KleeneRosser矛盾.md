# 1935 - Kleene–Rosser 矛盾

## 案件摘要
1935 年，Church 的兩位學生 Kleene 與 Rosser 證明了一件讓老師難堪的事：
Church 的邏輯系統是**矛盾的** —— 它能證出「命題 $P$ 與 $\neg P$ 同時成立」。
推理手法正是 Richard 悖論式的自我指涉。Church 的回應成為科學誠實的典範：
承認錯誤、放棄邏輯部分、保留純計算部分。

## 前因 -- 為什麼會有這個案子
- 1932–1933 年 Church 發表他的邏輯系統：無類型 λ 演算 + 邏輯常數（否定 $\mathcal{N}$、蘊含 $\mathcal{I}$、全稱量詞 $\Sigma$）+ 若干公設，野心是「以計算為基礎重建邏輯」。
- 世紀初的教訓歷歷在目：
  - **Richard 悖論**（1905）：「所有可用有限語句定義的實數」本身也可以被定義，於是構造出「不在自己名單上的第一個數」。
  - **Russell 悖論**（1901）：集合 $R = \{x \mid x \notin x\}$，問 $R \in R$？
  - 共同病灶：**不受限的全稱量化 + 自我指涉**。
- Church 的系統允許「對所有項（函數）」做量化 —— 這正是病灶重現的溫床。Kleene 與 Rosser 嗅到了血腥味。

## 線索與推理 -- 數學式、程式、理論

### 1. 矛盾的證明手法概述（Richard 式推理）
Kleene–Rosser 定理（1935，發表於 *On inconsistency of the simple theory of types* 之前的系列結果，正式論文為 1936 年 JSL 的 *On inconsistency of a certain set of postulates for the foundation of logic*）的核心思路：

**第一步：在系統內定義「可定義性謂詞」。**
因為系統允許全稱量化，可以在系統內部談論「哪些 λ 項可證明對應一個（唯一）自然數」：

$$
D(x) \;:\Longleftrightarrow\; \text{存在 λ 項 } M \text{，使得 } M \text{ 可證且 } M \text{ 代表唯一自然數 } x
$$

（這就是系統的「算術化」—— 一切項都是符號串，系統可以為符號串編碼，並在系統內談論自己的可證性。）

**第二步：Richard 式對角線構造。**
定義函數：
$$
f(n) = \begin{cases} n + 1 & \text{若 } \neg D(n) \\ n & \text{若 } D(n) \end{cases}
$$

這個 $f$ 本身可以由一個 λ 項 $F$ 定義（因為條件分支與 $D$ 都可在系統內表達）。

**第三步：引爆矛盾。**
令 $k = F$ 所對應的「定義編號」，問 $D(k)$？

- 若 $D(k)$（$k$ 在可定義名單上）：則依 $f$ 的定義 $f(k) = k$，但 $F$ 是對角線構造，$f(k)$ 應該偏離 $k$ —— 矛盾。
- 若 $\neg D(k)$：則 $f(k) = k+1 \neq k$，但「$F$ 定義的正是 $f$」這件事又使 $k$ 可被定義 —— 矛盾。

兩邊都矛盾，因此系統可證
$$
\vdash\ P \quad\text{且}\quad \vdash\ \neg P
$$

形式上，Kleene–Rosser 在系統內導出了類似
$$
\vdash\ (A \wedge \neg A)
$$
的定理，宣告系統不一致。

**與 Gödel 不完備定理的對照**：Gödel（1931）用的是「不可證明性」對角線，得到「真但不可證」的語句（不完備）；Kleene–Rosser 用「可定義性」對角線，在更強的公設下直接得到**可證的矛盾**。對角線手法相同，結局不同 —— 差別在公設的強度。

### 2. 以程式類比這個矛盾
自我指涉 + 不受限抽象的災難，在程式裡的類比：

```python
# Ω 組合子：無類型 λ 演算中最簡單的「不停機」項
Ω = (lambda x: x(x))(lambda x: x(x))
# 呼叫 Ω 會無限遞迴 —— 自我應用沒有任何約束

# 悖論式自我指涉的偽碼類比：
def is_definable(n): ...
def f(n): return n + 1 if not is_definable(n) else n
# 問 f 自己的定義編號 k：f(k) 的值與定義互相否定 —— 沒有一致的答案
```

### 3. Church 的回應：斷尾求生
面對學生的證明，Church 的處理堪稱典範：
1. **承認**：在 1934–1935 年的通信與後續論文中明確承認系統不一致。
2. **撤退**：撤除全部邏輯公設（否定、蘊含、量詞），**只保留純計算部分** —— 無類型 λ 演算本身。1941 年《The Calculi of Lambda-Conversion》就是這個「淨化版」。
3. **重建**：1940 年提出**簡單類型 λ 演算**（simply typed λ-calculus），以類型分層禁止自我應用：
   $$
   \tau ::= \iota \mid \tau \to \tau
   $$
   在此系統中 $\lambda x.\, x\ x$ **不合型**（$x$ 不能同時有型 $\sigma$ 與 $\sigma \to \sigma$），從而阻絕悖論，且簡單類型系統被證明（相對）一致。

## 結案 -- 後果與影響
- Church 邏輯系統正式死亡（1936 年 Kleene–Rosser 論文發表即結案），但它留下兩個強大的遺產：
  1. **無類型 λ 演算**：純計算骨架，成為 Lisp、函數式程式設計與可計算性理論的基石。
  2. **簡單類型 λ 演算**：成為型別理論、Haskell/ML 型別系統、Curry–Howard 對應的起點。
- 歷史教訓寫入教科書：**在無類型的全稱系統裡談論「所有函數」，就是打開悖論之門。** Russell 類型論、簡單類型 λ 演算、以及現代依值型別（dependent types），全是這個教訓的產物。
- 有趣的餘波：同年（1936）Church 用 λ 演算證明判定問題不可判定 —— 邏輯夢想死了，計算科學卻在此誕生。

## 關鍵人物與文獻
- **Stephen C. Kleene**、**J. Barkley Rosser**：證明者，亦是 Church 的學生 —— 學生終結了老師的系統，卻成就了老師的遺產。
- **Alonzo Church**：承認錯誤、斷尾求生、轉向類型論。
- S. C. Kleene & J. B. Rosser, *On inconsistency of a certain set of postulates for the foundation of logic*, Annals of Mathematics 36 (1935)。
- A. Church, *A formulation of the simple theory of types*, Journal of Symbolic Logic 5 (1940)。
- J. B. Rosser, *Highlights of the history of the lambda-calculus*, Annals of the History of Computing 6 (1984)：當事人的歷史回顧。
