# 2021：const 泛型與 Rust 2021 Edition——表達力補完

## 事件
2021 年的兩件大事：**const 泛型**（1.51，3 月）與 **Rust 2021 Edition**（1.56，10 月）。同年 2 月 Rust 基金會正式成立。

## 為何重要
- **const 泛型（const generics, MVP）**：泛型參數不再限於型別，可以是值——`struct ArrayWrapper<const N: usize> { data: [u8; N] }`。
  - **彌補的缺陷**：1.0 之前 `[u8; N]` 無法泛型化，陣列長度只能寫死或靠 macro；標準函式庫的陣列方法（如 `iter()`）必須為每個長度手動實作到 32——const 泛型從根上消滅這個「32 上限」的尷尬。
  - **理論原因**：依賴型別（dependent types）的受限形式——把「值層級的參數」納入型別參數，讓編譯器檢查長度等不變量（例如矩陣乘法的維度）。
  - **實用原因**：密碼學、數值運算、嵌入式程式設計大量需要「編譯期已知大小的緩衝區」；MVP 限制 N 只能是整數/bool/char，避免全功能依賴型別的複雜度。
- **Rust 2021 Edition 具體改動**：
  - **閉包捕獲改革（disjoint capture）**：閉包只捕獲用到的欄位而非整個物件，減少借用衝突。
  - **`IntoIterator` for arrays**：`for x in [1,2,3]` 直接迭代值，不再呼叫 `.iter()`。
  - **panic! 巨集統一**：`panic!("{}", x)` 與 `format!` 語意一致，消除「只傳一個參數時行為不同」的歷史包袱。
  - **保留字前綴 `r#` 泛化**與 prelude 擴充（加入 `TryFrom`、`TryInto` 等）。

## 理論與實用原因
- **理論原因**：disjoint capture 來自「捕獲語義應最小化」的原則（與 C++ 的 `[=]` 捕獲整個物件相反）；避免捕獲整個變數導致的借用過寬。
- **實用原因**：閉包捕獲整個物件常導致「只是想讀一個欄位，卻把整個 self 借死了」的借用錯誤——這是 Rust 問題回報中最常見的困惑之一。

## 程式範例

**const 泛型之前**——陣列長度寫死，標準函式庫有「32 上限」：

```rust
// 1.0 之前：長度只能寫死
struct Buffer { data: [u8; 64] }          // 換長度就要重寫整個型別

// 標準函式庫的尷尬：tuple/陣列 trait 實作只到 32
// fn f<T>(t: (T, T, ..., T))             // 第 33 個元素？不支援
```

**const 泛型之後（1.51）**——長度成為編譯期參數：

```rust
struct Buffer<const N: usize> {
    data: [u8; N],          // N 是編譯期已知的值
}

fn sum(buf: &[u8]) -> u32 { buf.iter().map(|&b| b as u32).sum() }

// 編譯器檢查維度等不變量——矩陣乘法範例
struct Matrix<const R: usize, const C: usize> { m: [[f64; C]; R] }

fn multiply<const R: usize, const C: usize, const K: usize>(
    a: &Matrix<R, C>, b: &Matrix<C, K>,
) -> Matrix<R, K> {
    let mut out = Matrix { m: [[0.0; K]; R] };
    for i in 0..R { for j in 0..K { for k in 0..C {
        out.m[i][j] += a.m[i][k] * b.m[k][j];
    }}}
    out   // 維度不符（如 3x4 乘 3x4）直接編譯錯誤
}
```

**閉包捕獲改革（2021 Edition）**——disjoint capture：

```rust
struct Config { name: String, port: u16 }

let cfg = Config { name: "app".into(), port: 8080 };

// 2015 edition：用到 cfg.port，卻把整個 cfg 借死
// let get = || cfg.port;        // 借用整個 cfg

// 2021 edition：只捕獲用到的欄位 cfg.port——cfg.name 仍可自由使用
let get_port = || cfg.port;
println!("{}", cfg.name);        // OK，name 沒被閉包捕獲
```

**IntoIterator for arrays**：

```rust
// 2015：for x in [1,2,3] 迭代的是引用，需寫 .iter()
for x in [1, 2, 3].iter() { println!("{x}"); }
// 2021：直接迭代值
for x in [1, 2, 3] { println!("{x}"); }
```

## 彌補了什麼缺陷
彌補了 Rust「陣列長度無法泛型化（32 上限）」與「閉包捕獲過寬、借用衝突頻繁」的缺陷——2021 是「補表達力 + 補人體工學」並行的一年。

## 相關條目
- [2020-Rust基金會前夜](2020-Rust基金會前夜.md)
- [2022-GAT-let-else與Linux核心合併](2022-GAT-let-else與Linux核心合併.md)
