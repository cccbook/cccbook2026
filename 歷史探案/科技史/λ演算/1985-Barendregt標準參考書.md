# 1985 — Barendregt 標準參考書與 Lambda Cube

## 案件摘要
1985 年荷蘭邏輯學家 Henk Barendregt 出版《The Lambda Calculus: Its Syntax and Semantics》，將 λ 演算五十年的散落成果（Church、Curry、Kleene、Scott、Bohm……）整理成一部聖經式的標準參考書。他後來更提出 Lambda Cube，用一個立方體統攝八個型別系統——成為型別理論的「元素週期表」。

## 前因 -- 為什麼會有這個案子
- **成果散落五十年**：自 1928–1932 年 Church 發明 λ 演算以來，相關定理分散在邏輯學期刊、電腦科學會議中：Church–Rosser 合流性（1936）、Scott 的 D∞ 模型（1970）、Bohm 定理（1968）、Staples 的合流性推廣……沒有一部統一的參考書。
- **電腦科學的崛起**：1960–80 年代 Lisp、ISWIM、ML 相繼以 λ 演算為基礎；型別系統研究（System F、依賴型別）快速累積，亟需一本權威教科書統整。
- **命名懸案**：Barendregt 首先系統化「Barendregt convention」——λ 項中變數名必須兩兩相異（$ (\lambda x.\, x\,(\lambda y.\, y\,x))$ 中 $x \neq y$），避免 α 變換時的混淆。這條約定至今寫進每本教科書。

## 線索與推理 -- 數學式、程式、理論

### 全書架構（偵探的檔案櫃）
《The Lambda Calculus》共分四大部分：
1. **語法**：λ 項的定義 $M ::= x \mid \lambda x.\,M \mid M\,N$，自由變數 $\mathsf{FV}(M)$、α 等價、Barendregt convention。
2. **歸約**：β 歸約 $(\lambda x.\,M)\,N \to M[N/x]$、η 歸約 $\lambda x.\,M\,x \to M$（當 $x \notin \mathsf{FV}(M)$）、**合流性（Church–Rosser 定理）**：若 $M \to^* N_1$ 且 $M \to^* N_2$，則存在 $N_3$ 使 $N_1 \to^* N_3$ 且 $N_2 \to^* N_3$——保證計算結果唯一，是整個 λ 演算的基石。
3. **不動點理論**：每個 λ 項都有不動點。Curry 組合子

   $$Y = \lambda f.\,(\lambda x.\,f\,(x\,x))\,(\lambda x.\,f\,(x\,x)) \quad\Rightarrow\quad Y\,f = f\,(Y\,f)$$

   遞迴的基礎：`fact = Y (λf. λn. if n==0 then 1 else n * f (n-1))`。
4. **語義模型**：Dana Scott 的 $D_\infty$ 模型 $D \cong D \to D$（利用 domain theory 與部分序上的連續函數解決「集合論無法自指」的難題）、Plotkin 的 PCF、以及 **Böhm 定理**：兩個 βη-正規形式不同的 λ 項必然「行為可分離」——存在情境 $C$ 使 $C[M] \to^* \mathsf{true}$ 而 $C[N] \to^* \mathsf{false}$。這給了「語義相等」一個操作性的判準，也是 Bohm-out 技巧（Lisp `quote` 防禦）的來源。

### Lambda Cube（八個型別系統）
Barendregt（1991）觀察到：所有重要的型別系統，都是「純基礎系統 λ→（簡單型別 λ 演算）」加上三個獨立維度中的一個或多個：

| 維度 | 增加的能力 | 代表系統 |
|---|---|---|
| $\{*\}$ 頂部：**項依賴於型別** | 多型（polymorphism） | System F（Girard/Reynolds） |
| $\{\Box\}$ 底部：**型別依賴於型別** | 型別運算子 | Fω（higher-order polymorphism） |
| $\{\Box\}$ 頂部：**型別依賴於項** | 依賴型別 | λΠ / Martin-Löf、CC |

Cube 圖示（底角 λ→ 為純簡單型別 λ 演算）：

```text
                System Fω  (λ→ + *↔□)          λΠ2/λP2  (λ→ + *↔□)
                   ●──────────────────────●
                  /│                     /│
                 / │                    / │
        λω/λω ●  │             λPω/λωP●  │     ← 頂點：Calculus of
               /  │                  /  /        Constructions (Coquand-Huet)
              /   ●                 /  /
             ●─────────────────────● /         八個系統：
     λ→ ●    │/λΠ2 (λ→ + □)        │/             λ→（簡單型別）
        │    ●──────────────────────●              F（多型）
        │   /  λP (λ→ + □↔*)    /                  Fω（型別運算子）
        │  /                   /                   λP（依賴型別）
        │ /                   /                    Fω+依賴 …λPω
        ●/───────────────────/                     頂點：λC = Calculus
     （底角：簡單型別 λ 演算）                          of Constructions
```

（正確版——三軸由 λ→ 出發：）
- $\lambda\to \xrightarrow{\text{多型 } *↔□} \lambda 2 = \text{System F}$
- $\lambda\to \xrightarrow{\text{型別運算子 } \Box↔□} \lambda\omega$
- $\lambda\to \xrightarrow{\text{依賴型別 } \Box↔*} \lambda P$（Automath 系統）
- 三者疊加到頂點 $\lambda C$（Calculus of Constructions）——**Coq 的理論基礎就在這個頂點上**。

Cube 的意義：**任何一個型別系統的證明方法學，都可以從 Cube 中其他系統的證明「借鏡」**——Barendregt 統一證明了 Cube 內所有系統的強正規化性質。

### 理論定義（強正規化）
$$\text{若 } \Gamma \vdash M : A \text{，則所有歸約序列 } M \to M' \to \cdots \text{ 必然終止（Strong Normalization）}$$

這個定理在 Cube 的每個頂點都成立——型別正確的程式必然停機，與 Turing 機器的不可判定性形成美麗對比：**λ 演算圖靈完備，但型別化的 λ 演算（不帶遞迴）可判定**。

## 結案 -- 後果與影響
- **聖經地位**：1985 年初版、1984 年修訂版成為所有 λ 演算研究者的必讀書，至今沒有替代品。
- **Lambda Cube 成為標準語言**：所有型別系統教科書（Pierce《Types and Programming Languages》等）都採用 Cube 的分類法。
- **孕育 Coq**：Cube 頂點的 Calculus of Constructions 直接催生了 Coq（1989）。
- **教學影響**：Barendregt convention 成為全球教科書的標準；「合流性 → 不動點 → 語義」的敘事架構成為 λ 演算課程的模板。
- **後續**：Barendregt 學派（荷蘭 Nijmegen）培育出一整代型別理論學家；λ 演算從邏輯學支線正式成為電腦科學的核心理論。

## 關鍵人物與文獻
- **Henk Barendregt**：荷蘭邏輯學家（Utrecht、Nijmegen），佛教禪修與 λ 演算雙棲大師。
- 文獻：
  - Barendregt, H. (1984/1985). *The Lambda Calculus: Its Syntax and Semantics*, North-Holland.
  - Barendregt, H. (1991). *Lambda Calculi with Types* (Handbook of Logic in Computer Science) — Lambda Cube 的原始出處。
  - Barendregt, H. (1997). *The Impact of the Lambda Calculus in Logic and Computer Science*.
- 相關：Church、Curry、Dana Scott（domain theory）、Girard/Reynolds（System F）、Coquand-Huet（CC）。
