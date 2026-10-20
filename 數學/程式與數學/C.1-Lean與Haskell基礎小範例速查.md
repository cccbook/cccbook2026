# 附錄 C：Lean / Haskell 基礎小範例速查

> 本附錄提供可直接複製執行的小程式，涵蓋本書各章的核心概念，供讀者動手驗證理論。

## C.1 Haskell 速查

### C.1.1 基本型別與 Curry–Howard

```haskell
-- 命題 P -> Q 的證明，就是一個函數
modusPonens :: (P -> Q) -> P -> Q
modusPonens f p = f p

-- 「且」的消去律
proj1 :: (a, b) -> a
proj1 (a, _) = a

-- 「或」的引入律
introLeft :: a -> Either a b
introLeft a = Left a

-- 分配律：(A and (B or C)) -> ((A and B) or (A and C))
distrib :: (a, Either b c) -> Either (a, b) (a, c)
distrib (a, Left b)  = Left (a, b)
distrib (a, Right c) = Right (a, c)
```

### C.1.2 代數資料型別

```haskell
data Nat = Z | S Nat

data List a = Nil | Cons a (List a)

data Tree a = Leaf | Node (Tree a) a (Tree a)

-- fold 的型別（初始代數的消去子）
foldr :: (a -> b -> b) -> b -> [a] -> b
foldr f z []     = z
foldr f z (x:xs) = f x (foldr f z xs)
```

### C.1.3 Functor / Applicative / Monad

```haskell
class Functor f where
  fmap :: (a -> b) -> f a -> f b

class Functor f => Applicative f where
  pure  :: a -> f a
  (<*>) :: f (a -> b) -> f a -> f b

class Applicative f => Monad f where
  (>>=) :: f a -> (a -> f b) -> f b
```

### C.1.4 Maybe Monad

```haskell
data Maybe a = Nothing | Just a

instance Functor Maybe where
  fmap _ Nothing  = Nothing
  fmap g (Just x) = Just (g x)

instance Monad Maybe where
  return = Just
  Nothing  >>= _ = Nothing
  Just x   >>= f = f x

safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv x y = Just (x `div` y)

-- 錯誤處理的鏈式合成
example :: Maybe Int
example = safeDiv 10 2 >>= safeDiv 5
```

### C.1.5 State Monad

```haskell
newtype State s a = State { runState :: s -> (a, s) }

instance Monad (State s) where
  return a = State $ \s -> (a, s)
  m >>= f  = State $ \s ->
    let (a, s') = runState m s
    in runState (f a) s'
```

### C.1.6 柯里化

```haskell
curry :: ((a, b) -> c) -> a -> b -> c
curry f a b = f (a, b)

uncurry :: (a -> b -> c) -> (a, b) -> c
uncurry f (a, b) = f a b
```

## C.2 Lean 速查

### C.2.1 基本證明

```lean
-- 恆等函數
def id' (a : Nat) : Nat := a

-- 簡單定理
theorem add_zero (n : Nat) : n + 0 = n := by simp

theorem add_comm_proof (n m : Nat) : n + m = m + n := by
  rw [Nat.add_comm]
```

### C.2.2 依賴型別

```lean
-- 依賴型別：向量長度在型別中
inductive Vec (α : Type) : Nat → Type where
  | nil : Vec α 0
  | cons : α → Vec α n → Vec α (n + 1)

-- head 的型別保證不會出界
def Vec.head : Vec α (n + 1) → α
  | .cons x _ => x
```

### C.2.3 量詞

```lean
-- ∀ 的證明就是一個（依賴）函數
example : ∀ n : Nat, n = n := fun n => rfl

-- ∃ 的證明是「一個值 + 一個性質證明」
example : ∃ n : Nat, n * n = 25 := ⟨5, rfl⟩
```

### C.2.4 遞迴與歸納

```lean
def add : Nat → Nat → Nat
  | 0,     m => m
  | n + 1, m => (add n m) + 1

theorem add_zero' (n : Nat) : add n 0 = n := by
  induction n with
  | zero => rfl
  | succ k ih => rw [add, ih]
```

### C.2.5 從 Curry–Howard 到真實命題

```lean
-- 在 Lean 中，本書第一篇的所有邏輯恆等式都能機器檢查
theorem and_distrib (A B C : Prop) :
    A ∧ (B ∨ C) → (A ∧ B) ∨ (A ∧ C) := by
  intro ⟨a, bOrC⟩
  match bOrC with
  | .inl b => exact .inl ⟨a, b⟩
  | .inr c => exact .inr ⟨a, c⟩
```

## C.3 建議練習

1. **Haskell**：實作 `Either` 的 `Functor` 與 `Monad` instance。
2. **Haskell**：用 `foldr` 實作 `map`、`filter`、`length`。
3. **Lean**：證明 `(A → B) → (B → C) → (A → C)`。
4. **Lean**：定義 `Stream` 的共歸納結構，驗證第 9 章的觀點。
5. **Lean**：證明費馬小定理（可參考 mathlib 中 `Nat.mod_pow` 相關定理）。

## C.4 工具安裝建議

- Haskell：安裝 GHCup，即可使用 GHC + cabal。
- Lean：安裝 elan，`lean4` 編譯器 + VS Code 擴充（`leanprover.lean4`）。
- 線上環境：Lean Web Playground（live.lean-lang.org）可直接在瀏覽器練習。
