# 附錄 B：範疇論名詞在泛函編程中的中英對照字典

> 範疇論的名詞在進入程式設計社群後，常出現「同詞不同義」或「譯名分歧」的現象。本字典列出本書使用的譯名與英文原文，並標註對應的程式概念。

## B.1.1 基礎概念

| 中文譯名 | 英文 | 程式概念 | Haskell 中出現 |
|---|---|---|---|
| 範疇 | Category | 型別 + 純函數的世界 | `Category` typeclass |
| 物件 | Object | 型別（Type） | `*`（kind） |
| 態射 | Morphism | 純函數（Pure Function） | `a -> b` |
| 態射合成 | Composition | 函數合成 | `(.)` |
| 恆等態射 | Identity | 恆等函數 | `id` |
| 同構 | Isomorphism | 雙向可轉換的型別 | `Iso`、`newtype` 包裝 |

## B.1.2 建構子

| 中文譯名 | 英文 | 程式概念 |
|---|---|---|
| 積 | Product | `(a, b)`、struct |
| 餘積／和 | Coproduct / Sum | `Either a b`、enum |
| 指數物件 | Exponential | 函數型別 `b -> a` |
| 極限 | Limit | 廣義的「解方程式」型別 |
| 餘極限 | Colimit | 廣義的「合併」型別 |
| 起始物件 | Initial Object | `Void`（無值型別） |
| 終端物件 | Terminal Object | `()`（單位型別） |

## B.1.3 結構保持

| 中文譯名 | 英文 | 程式概念 |
|---|---|---|
| 函子 | Functor | `Functor` typeclass：`fmap :: (a->b) -> f a -> f b` |
| 自然變換 | Natural Transformation | `forall a. f a -> g a` |
| 恆等函子 | Identity Functor | `Identity` |
| 積函子 | Product Functor | `(,)` |
| 自函子 | Endofunctor | 從型別範疇到自己的映射 |

## B.1.4 Monad 相關

| 中文譯名 | 英文 | 程式概念 |
|---|---|---|
| 單子 | Monad | `Monad` typeclass |
| 單元（回傳） | Unit / Return / η | `return :: a -> m a` |
| 連接／延伸 | Bind / Multiplication / μ | `(>>=)`、`join` |
| 自 Monoid | Monoid in Category of Endofunctors | Mac Lane 的著名定義 |
| 可應用函子 | Applicative Functor | 介於 Functor 與 Monad 之間 |
| 自然變換之垂直合成 | God welding | Applicative 的 `<*>` |

## B.1.5 代數結構

| 中文譯名 | 英文 | 程式概念 |
|---|---|---|
| 半群 | Semigroup | `Semigroup`：只有 `<>` |
| 幺半群 | Monoid | `Monoid`：`<>` + `mempty` |
| 群 | Group | Semigroup + 逆元（少見於主流語言） |
| 環 | Ring | 數值型別上的 `+` 與 `*` |
| F-代數 | F-Algebra | 摺疊（fold）的數學基礎 |
| F-餘代數 | F-Coalgebra | 展開（unfold）與無限流的基礎 |
| 起始代數 | Initial Algebra | 代數資料型別（如 `Nat`、`List`） |
| 終餘代數 | Terminal Coalgebra | 無限結構（如 `Stream`） |
| 參數性 | Parametricity | 「免費定理」的來源 |

## B.1.6 常見易混淆詞

- **Functor（函子）** vs **Function（函數）**：函子是「型別之間的映射」，函數是「值之間的映射」。
- **Monoid（幺半群）** vs **Monad（單子）**：兩者皆含「單位元 + 結合」的概念，但 Monad 是「型別層次的幺半群」。
- **Product（積）**：數學中的卡氏積；程式中的 tuple。**注意**：在 OOP 中 "product" 常指產品，意義完全不同。
- **Subtype（子型別）** vs **Subset（子集）**：子型別關係在原則上不必是集合包含（例如「可排序」的子型別）。

## 小結

範疇論術語在程式設計中的用法，本質上是數學原義的「具象化」：理解這張字典，就能在閱讀 Haskell 型別類文件與範疇論教科書時對號入座，避免誤解。
