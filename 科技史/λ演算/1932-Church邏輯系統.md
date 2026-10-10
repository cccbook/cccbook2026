# 1932 - Church 的邏輯系統

## 案件摘要
1932–1936 年，Church 嘗試做一件大膽的事：以 λ 演算為基底，
建立一套能「同時處理邏輯與計算」的公理化邏輯系統。
這個系統後來被證明是矛盾的 —— 但它留下了純計算的骨架（λ 演算本身），反而更加長壽。

## 前因 -- 為什麼會有這個案子
- **Hilbert 綱領**（1917–1930）：Hilbert 主張用有限、機械的方法為整個數學建立一致且完備的公理系統，並期望判定問題（Entscheidungsproblem）有解。
- **邏輯主義**：Russell 與 Whitehead 在《Principia Mathematica》中嘗試把數學還原為邏輯，但其「還原函數」記法 $\hat{x}.M$ 繁瑣、且需要複雜的類型論。
- Church 的野心更大：不只還原數學，而是把**邏輯本身**也變成函數 —— 命題就是某種 λ 項，推理就是 β-歸約。若成功，「數學即計算」。
- 當時 Gödel 的不完備定理（1931）剛剛擊碎 Hilbert 綱領的「完備」部分，但「一致 + 可判定」的希望尚未熄滅，Church 想接手這個案子。

## 線索與推理 -- 數學式、程式、理論

### 1. 系統的基本形式
Church 的系統（發表於 *A set of postulates for the foundation of logic*, Annals of Math., 1932/1933）是一個**無類型的 λ 演算**，再加上一組邏輯常數與公設（postulates）。

基本體系：
- **底層**：無類型 λ 演算，項由 $x \mid \lambda x.\, M \mid M\ N$ 構成，計算靠 β-歸約
  $$
  (\lambda x.\, M)\, N \to_\beta M\,[N/x]
  $$
- **邏輯常數**（以組合子形式引入），例如：
  - 否定 $\mathcal{N}$、蘊含 $\mathcal{I}$、全稱量詞 $\Sigma$（即「對所有」的函數式版本）
  - 等詞：Church 以 Leibniz 律定義相等：
    $$
    E = \lambda x.\, \lambda y.\, \forall f.\, (f\ x \Rightarrow f\ y)
    $$
    「$x$ 與 $y$ 相等，若且唯若 $x$ 的所有性質 $f$，$y$ 都有。」

### 2. 公設的形式（概述）
Church 的公設分為兩類：
1. **形式規則**：如 $\beta$-歸約、替換規則、以及「若 $M$ 可證且 $M \to_\beta N$ 則 $N$ 可證」（歸約保持可證性）。
2. **邏輯公設**：如
   $$
   \mathcal{I}\ M\ (\mathcal{I}\ M\ N)\ \vdash\ \mathcal{I}\ M\ N \quad \text{（蘊含的傳遞式公設之一）}
   $$
   以及全稱量詞的引入/消去規則，形式上類似現代自然演繹，但一切寫成 λ 項的函數應用。

### 3. 系統的特性
- **萬能函數**：系統中允許「對所有項」做量化，等價於允許不限制的全稱抽象 —— 這正是它能表達 Richard 悖論式推理的漏洞所在。
- **無類型**：不設類型檢查，$\lambda x.\, x\ x$ 是合法項（今日稱為 untyped lambda calculus 的特徵）。
- **一致的期望**：Church 起初相信系統一致，並在論文中宣稱「若不一致，修改公設即可」—— 這句話不久就被現實打臉。
- Church 也嘗試用它定義自然數與算術（後由 Kleene 發展成 Church 數字），證明原則上「數學可內建於此邏輯系統」。

### 4. 以現代眼光看這個系統
```text
系統 = 無類型 λ 演算           （計算層：β-歸約）
     + 邏輯常數 N, I, Σ, E    （把否定/蘊含/量詞/相等寫成函數）
     + 若干邏輯公設            （允許全稱量化）
```

以 Python 對照「把邏輯寫成函數」的直覺：

```python
TRUE  = lambda a: lambda b: a        # 選擇第一個
FALSE = lambda a: lambda b: b        # 選擇第二個
NOT   = lambda p: p(FALSE)(TRUE)     # 否定：翻轉選擇
AND   = lambda p: lambda q: p(q)(FALSE)
OR    = lambda p: lambda q: p(TRUE)(q)

assert NOT(TRUE) is FALSE
assert AND(TRUE)(FALSE) is FALSE
```

「命題即函數、推理即歸約」—— 這個夢想本身是對的，錯的是那組允許全稱量化的公設。

## 結案 -- 後果與影響
- 1935 年，Church 自己的學生 Kleene 與 Rosser 證明這個系統**矛盾**（見〈1935 - Kleene–Rosser 矛盾〉一案）。
- Church 的回應：**放棄邏輯部分，保留純計算部分**。他把公設全數撤除，只留下無類型 λ 演算 —— 這個「殘骸」反而成為 20 世紀最重要的計算模型之一。
- 教訓深刻：**在無類型系統中，把「對所有函數」量化，等於允許自我指涉，等於擁抱悖論。** 後來的解藥是**類型論**：Church 於 1940 年提出簡單類型 λ 演算（simply typed lambda calculus），以類型分層阻絕 $\lambda x.\, x\ x$，這正是 Russell 類型論的函數式轉世，也是今日 Haskell、ML 型別系統的祖先。
- Curry–Howard 對應（1958 後）最終實現了 Church 的夢想（命題即類型、證明即程式）—— 但那是在「有類型」的世界裡。

## 關鍵人物與文獻
- **Alonzo Church**：系統的提出者，也是承認錯誤並轉向的人。
- **Stephen C. Kleene**、**J. Barkley Rosser**：Church 的學生，系統的「終結者」。
- A. Church, *A set of postulates for the foundation of logic*, Annals of Mathematics (2), 33:346–360 (1932)；34:839–864 (1933)。
- A. Church, *The Calculi of Lambda-Conversion* (1941)：撤除邏輯公設後的純計算版本。
- A. Church, *A formulation of the simple theory of types*, JSL 5 (1940)：矛盾之後的類型化解藥。
