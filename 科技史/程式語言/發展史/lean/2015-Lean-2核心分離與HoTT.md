# 2015：Lean 2——核心分離與 HoTT 模式

## 事件
2015 年，**Lean 2** 發佈。最重要的改變是**核心分離**：kernel 拆成兩種模式——
**standard 模式**（含命题相等性 `propext`、選擇公理 `choice`、商類型 quotient）
與 **HoTT 模式**（同倫類型論 homotopy type theory，關閉 K 公理、
加入 univalence 相容的架構），兩者用同一份原始碼、不同編譯旗標。

## 為何重要
- **雙核心模式**：標準數學需要 `propext`/`choice`（經典邏輯），
  HoTT/Univalent foundations 則要求公理 K 可選、univalence 相容——
  Lean 2 用「同一核心、不同公理集合」一次滿足兩個數學社群。
- **巢狀與相互歸納類型（nested/mutual inductive types）**：
  補足 Lean 1 只支援簡單歸納的缺陷。
- **kernel 簡化重寫**：終止檢查與歸納類型檢查重寫，kernel 更小更快。
- **`using_well_founded` 與良基遞迴**：遞迴定義不再只能結構遞迴，
  可以用測度（measure）證明終止。

## 理論與實用原因
- **理論原因**：Voevodsky 的 univalent foundations（2009–2013）主張
  「等價即相等」（univalence axiom），與 K 公理矛盾。HoTT 模式讓
  Lean 可以形式化 HoTT 而不必放棄標準數學。
- **實用原因**：Lean 1 的單一核心讓 HoTT 使用者必須接受 `choice`
  （否認 HoTT），標準數學使用者則被迫共用同一組公理；分離後
  兩個社群都能用同一套語法。

## 程式範例

**相互歸納類型**——Lean 2 補上的表達力：

```lean
-- 樹與森林相互定義：Lean 1 做不到，Lean 2 原生支援
mutual
  inductive Tree where
    | node : List' Tree → Tree
  inductive List' (α : Type) where
    | nil  : List' α
    | cons : α → List' α → List' α
end
```

**良基遞迴**——用測度證明終止，不只是結構遞迴：

```lean
--Ackermann 函式：沒有明顯的結構遞迴，必須用良基關係
def ack : Nat → Nat → Nat
  | 0, n => n + 1
  | m + 1, 0 => ack m 1
  | m + 1, n + 1 => ack m (ack (m + 1) n)
  decreasing_by  -- 以 (m, n) 的字典序證明遞減
    simp_wf
    omega
```

**HoTT 模式 vs 標準模式**——公理集合可以選擇：

```lean
-- 標準模式：這三條公理可用
#check @propext    -- propext : {a b : Prop} → (a ↔ b) → a = b
#check @choice     -- choice : ∀ {α : Sort u}, Nonempty α → ∃ x, x ∈ α
#check @Quot.sound -- 商類型的函出性

-- HoTT 模式（Lean 2 用 -Dlean hottest 之類旗標建置）：
-- propext/choice 不在預設環境，K 公理關閉，
-- univalence 相容的 idpath/transport 可用
```

**univalence 的精神**——「等價即相等」：

```lean
-- HoTT 的世界裡，兩個同構的類型可以被視為相等；
-- 標準模式裡只能用 Equiv 與 propext 近似
universe u
def Equiv (A B : Type u) := A → B × (B → A)
```

## 彌補了什麼缺陷
彌補了 Lean 1「單一公理集合無法同時支援經典數學與 HoTT、
歸納類型只支援簡單形式」的缺陷——Lean 2 用雙核心模式與
巢狀/相互歸納，讓同一套語法服務兩個數學傳統。

## 相關條目
- [2013-Lean誕生於微軟研究院](2013-Lean誕生於微軟研究院.md)
- [2016-VS-Code擴充與Lean3預覽](2016-VS-Code擴充與Lean3預覽.md)
