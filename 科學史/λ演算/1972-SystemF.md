# 17. 1972 — Jean-Yves Girard 的 System F（與 Reynolds 的獨立發現）

## 案件摘要

1972 年，法國邏輯學家 Jean-Yves Girard 在論文 *Interprétation fonctionnelle et élimination des coupures de l'arithmétique d'ordre supérieur* 中發明了 **System F**（又稱二階 λ 演算、多型 λ 演算）。1974 年，John Reynolds 在 *Towards a Theory of Type Structure* 中獨立發現了同一系統。System F 把「型別也能被量化」帶入 λ 演算，是史上第一個能表達「多型」的系統。

## 前因 -- 為什麼會有這個案子

線索有兩條：

1. **簡單型別 λ 演算的限制**：恆等函數對每個型別都要重寫一遍——$\text{id}_{\mathbb{Int}} : \mathbb{Int} \to \mathbb{Int}$、$\text{id}_{\mathbb{Bool}} : \mathbb{Bool} \to \mathbb{Bool}$……無法寫出「對所有型別都成立的恆等函數」。這違反了 DRY（Don't Repeat Yourself）原則。
2. **Girard 的邏輯動機**：Girard 正在研究「高階算術的切痕消去（cut-elimination）」。他把二階直覺邏輯（允許對命題變數量化 $\forall \alpha.\, \varphi$）與 λ 演算對應起來，得到一個強正規化的系統。Reynolds 則從程式設計的角度（抽象資料型別、parametric polymorphism）獨立推出同一系統。

兩人的推理殊途同歸：**如果型別推導允許「對型別變數的抽象」，那麼多型就有了數學基礎**。

## 線索與推理 -- 數學式、程式、理論

### 1. 全稱量化型別

System F 的型別語法：

$$
\tau ::= \alpha \mid \tau_1 \to \tau_2 \mid \forall \alpha.\, \tau
$$

關鍵型別：**多型恆等函數的型別**

$$
\text{id} : \forall \alpha.\, \alpha \to \alpha
$$

讀作「對所有型別 $\alpha$，$\text{id}$ 是從 $\alpha$ 到 $\alpha$ 的函數」。

### 2. 型別抽象與型別應用

System F 的項語法在 λ 演算上加了兩個建構子：

$$
e ::= x \mid \lambda x:\tau.\, e \mid e_1\ e_2 \mid \Lambda \alpha.\, e \mid e\ [\tau]
$$

- $\Lambda \alpha.\, e$：**型別抽象**（type abstraction）——「把型別 $\alpha$ 當作參數」；
- $e\ [\tau]$：**型別應用**（type application）——「用具體型別 $\tau$ 實例化」。

型別規則：

$$
\frac{\Gamma, \alpha \vdash e : \tau}{\Gamma \vdash \Lambda \alpha.\, e : \forall \alpha.\, \tau}\ (\forall I)
\qquad
\frac{\Gamma \vdash e : \forall \alpha.\, \tau}{\Gamma \vdash e\ [\tau'] : \tau[\tau'/\alpha]}\ (\forall E)
$$

多型恆等函數：

$$
\text{id} = \Lambda \alpha.\, \lambda x:\alpha.\, x
$$

使用：

$$
\text{id}\ [\mathbb{Int}] : \mathbb{Int} \to \mathbb{Int}, \qquad \text{id}\ [\mathbb{Bool}] : \mathbb{Bool} \to \mathbb{Bool}
$$

一個 $\text{id}$，多種型別——DRY 的數學實現。

### 3. System F 的 Church 數字

在簡單型別 λ 演算中，Church 數字無法有單一型別；在 System F 中可以：

$$
\ulcorner n \urcorner \;=\; \Lambda \alpha.\, \lambda f:\alpha \to \alpha.\, \lambda x:\alpha.\, \underbrace{f (f (\cdots (f\ x)\cdots))}_{n \text{ 次}}
$$

例如 $n = 2$：

$$
\ulcorner 2 \urcorner = \Lambda \alpha.\, \lambda f:\alpha \to \alpha.\, \lambda x:\alpha.\, f\ (f\ x)
$$

型別：$\forall \alpha.\, (\alpha \to \alpha) \to (\alpha \to \alpha)$——**Church 數字在 System F 中有了統一的型別**。加法也自然定義：

$$
\text{add} = \Lambda \alpha.\, \lambda m:\forall\alpha.\ldots\ \lambda n:\ldots\ \lambda f:\alpha \to \alpha.\, \lambda x:\alpha.\, m\ [\alpha]\ f\ (n\ [\alpha]\ f\ x)
$$

（簡化寫法：$\text{add}\ m\ n\ f\ x = m\ f\ (n\ f\ x)$。）

### 4. Haskell 式寫法

```haskell
-- System F 的 Haskell 直譯（Haskell 的 RankNTypes 可寫出類似型別）
{-# LANGUAGE RankNTypes #-}

-- 多型恆等函數：Λα. λx:α. x
idF :: forall a. a -> a
idF x = x

-- Church 數字 2：Λα. λf:α→α. λx:α. f (f x)
two :: forall a. (a -> a) -> (a -> a)
two f x = f (f x)

-- Church 數字 3
three :: forall a. (a -> a) -> (a -> a)
three f x = f (f (f x))

-- Church 加法：add m n f x = m f (n f x)
addC :: (forall a. (a->a) -> (a->a))
     -> (forall a. (a->a) -> (a->a))
     -> (forall a. (a->a) -> (a->a))
addC m n f x = m f (n f x)

-- 驗證：2 + 3 = 5
-- addC two three  (*2*) 0  ==  5  （以 Int 實例化）
```

### 5. Girard 論證：強正規化

**定理（Girard, 1972）**：System F 是**強正規化（strongly normalizing）**的——每個型別正確的項，無論以何種歸納順序，都會在有限步內化約到正規形式。

**證明方法**：Girard 發明了「可滿足性候選（candidats de réductibilité / reducibility candidates）」方法：定義一類「好型別」$S_\tau$（正規化、由 neutral terms 或紅縮封閉等），對每個型別 $\tau$ 歸納地建立詮釋 $\llbracket \tau \rrbracket \subseteq S_\tau$，證明所有型別正確的項屬於對應詮釋。這個方法至今仍是依賴型別系統強正規化證明的標準工具。

推論：System F 中**沒有一般遞迴**（否則可寫出不終止的項），因此「圖靈完備」必須靠原始遞迴/資料型別/不動點組合子的受限形式補充。

### 6. 參數性（Parametricity）

Reynolds 的關鍵洞察：$\text{id} : \forall \alpha.\, \alpha \to \alpha$ 的**唯一實現**是恆等函數——多型函數對型別「一視同仁」（parametric）。這導出：

- **Theorems for Free!**（Wadler, 1989）：從型別就能推出函數必須滿足的定理；
- **參數性抽象資料型別**：Abstract Data Type 的數學基礎。

## 結案 -- 後果與影響

1. **Haskell typeclass 的理論基礎**：Haskell 的 `∀ a. Eq a => a -> a -> Bool`、`derive` 機制、generics，都基於 System F 的參數性；GHC 的核心語言 Core 就是 System Fω 的變體；
2. **ML functor**：ML 的模組系統（functor）是 System F 的「階層化（stratified）」版本——把型別抽象與型別應用限制在模組層級，避免型別推論不可判定；
3. **多型的兩大陣營**：
   - **Parametric polymorphism**（System F）→ ML/Haskell 的泛型；
   - **Ad-hoc polymorphism**（overloading）→ typeclass / C++ template 的對比；
4. **依賴型別系統**：Coq 的 Calculus of Constructions（1985）= System F + 依賴型別；強正規化證明的 reducibility candidates 方法成為標準；
5. **邏輯上的二階直覺邏輯**：System F 在 Curry–Howard 對應下就是「二階直覺命題邏輯」的證明系統。

## 關鍵人物與文獻

- **Jean-Yves Girard**（1947–）：法國邏輯學家，後又發明線性邏輯（Linear Logic, 1987）。
- **John C. Reynolds**（1935–2013）：美國計算機科學家，卡內基美隆大學教授，獨立發現 System F。
- J.-Y. Girard, *"Interprétation fonctionnelle et élimination des coupures de l'arithmétique d'ordre supérieur"* (1972, Thèse d'État)。
- J. C. Reynolds, *"Towards a Theory of Type Structure"* (1974, Colloque sur la Programmation)。
- J. C. Reynolds, *"Types, Abstraction and Parametric Polymorphism"* (1983)。
- P. Wadler, *"Theorems for Free!"* (1989, FPCA)。
