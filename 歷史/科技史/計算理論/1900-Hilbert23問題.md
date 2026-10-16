# 1900 - Hilbert 的 23 個問題

## 案件摘要
1900 年 8 月 8 日，Hilbert 在巴黎第二屆國際數學家大會上提出 23 個數學問題，為 20 世紀數學開出「懸案清單」。其中第 10 問題（Diophantine 方程可解性）與判定問題（Entscheidungsproblem）最終催生了「不可計算性」這門全新的學科。

## 前因 -- 為什麼會有這個案子
19 世紀末，數學基礎歷經三次危機：非歐幾何的誕生、集合論悖論（Russell 悖論 1901 年才出現，但 Burali-Forti 悖論已現端倪）、以及分析中實數理論的嚴格化需求。Hilbert 剛完成《幾何基礎》（1899），深信數學可以透過公理化方法徹底鞏固。他倡導的 **Hilbert 綱領** 主張：

1. **完備性（Completeness）**：每個命題 $P$，在系統 $T$ 中，$T \vdash P$ 或 $T \vdash \neg P$，二者必居其一。
2. **一致性（Consistency）**：不存在命題 $P$ 使得 $T \vdash P$ 且 $T \vdash \neg P$。
3. **可判定性（Decidability）**：存在一個機械程序（演算法），對任意命題 $P$，能在有限步驟內判定 $T \vdash P$ 是否成立——這就是後來的 **Entscheidungsproblem**（判定問題）。

巴黎演說正是這套哲學的宣示：數學是一座可完全建成、可完全檢驗的大廈。

## 線索與推理 -- 數學式、程式、理論

### 第 10 問題：Diophantine 方程
給定整係數多項式方程 $P(x_1, \dots, x_n) = 0$，找出一個程序，在有限步驟內判定它是否有整數解。

形式化地：

$$D = \{ (e_1,\dots,e_n) \in \mathbb{Z}^n \mid P(x_1,\dots,x_n) = 0 \text{ 有整數解} \}$$

問題是：集合 $D$ 是否「可判定」（recursive）？

例如 Pell 方程 $x^2 - 61y^2 = 1$ 有解（最小解 $x=1766319049$），但一般的多項式方程有沒有解？

**偵探筆記**：這個問題問的其實不是「怎麼解」，而是「存不存在機械化的解法」——這在 1900 年根本沒有嚴格定義！「程序」、「有效方法」這些詞要到 1930 年代（Turing、Church）才有了精確的數學化身。

### 判定問題的源頭
Hilbert 後來在《理論邏輯基礎》（1928）中明確提出：

> 給定一階邏輯公式 $\varphi$，是否存在演算法判定 $\varphi$ 是否有效（有效 = 在所有模型中為真）？

即判定集合：

$$\mathrm{VAL} = \{ \varphi \mid \models \varphi \}$$

Hilbert 相信答案是肯定的——「沒有不可解的問題」（ignoramus et ignorabimus 的反面宣言）。

### 其他關鍵問題
- **第 1 問題**：連續統假設 $2^{\aleph_0} = \aleph_1$ 是否成立（1940 年 Gödel 證明不可否證、1963 年 Cohen 證明不可證明——獨立於 ZFC！）
- **第 2 問題**：算術公理的一致性（1931 年被 Gödel 不完備定理重擊）
- **第 8 問題**：Riemann 假設（至今未解）

### 程式碼：Diophantine 方程的暴力搜尋（有解時可驗證）
```python
def has_solution(P, bound=1000):
    """P 是係數列表，暴力搜尋 x^2 - 61y^2 = 1 型方程"""
    for x in range(bound):
        for y in range(bound):
            # P(x, y) = x**2 - 61*y**2 - 1
            if x*x - 61*y*y - 1 == 0:
                return True, (x, y)
    return False, None  # 永遠無法確認「無解」！

# 問題核心：找到解可以停，但「沒找到」不代表「無解」
# 這正是第 10 問題的精髓——「無解」是否可判定？
print(has_solution(None, bound=10**7))  # bound 再大也只證明「在此範圍內無解」
```

## 結案 -- 後果與影響
- **第 10 問題**：1970 年 Matiyasevich（結合 Davis–Putnam–Robinson 的工作）證明：Diophantine 方程的可解性**不可判定**。核心是證明每個遞迴可枚舉集合都能表示為 Diophantine 集合（DPRM 定理）。
- **判定問題**：1936 年 Church（用 λ 演算）與 Turing（用圖靈機）獨立證明一階邏輯有效性**不可判定**。
- **第 2 問題**：1931 年 Gödel 不完備定理證明 Hilbert 綱領的完備性與自我一致性不可能同時達成。
- 諷刺的是：這些「失敗」反而誕生了**可計算性理論**（遞迴論）、圖靈機、通用電腦的概念——20 世紀最重要的科技革命由此案間接引爆。

## 關鍵人物與文獻
- **David Hilbert**（1862–1943）：巴黎演說 "Mathematische Probleme" (1900)；《數學基礎》(Grundlagen der Mathematik, 1928, 與 Bernays 合著)
- **Yuri Matiyasevich**（1947–）：Matiyasevich 定理 (1970)
- **Martin Davis, Hilary Putnam, Julia Robinson**：DPRM 定理的前置工作（1961）
- 交叉參照：`1931-Godel不完備定理.md`、`1936-Turing機與停機問題.md`
