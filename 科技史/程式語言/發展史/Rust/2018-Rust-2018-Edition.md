# 2018：Rust 2018 Edition——模組系統改革與 dyn Trait

## 事件
2018 年 12 月，Rust 1.31 發佈第一個 **Edition：Rust 2018**。Edition 機制讓語言可以做出「不相容的語法改動」，同時維持整體生態的向後相容——新舊 edition 的 crate 可以互相依賴。

## 為何重要
- **Edition 機制本身**：解決了「語言要進化就需要 break 相容性」的兩難。C++ 花了數十年對抗這個問題；Python 2/3 的分裂則是反例。Rust 的解法：edition 是可選的編譯模式，Cargo 協調跨 edition 依賴。
- **Rust 2018 的具體改動**：
  - **模組系統改革**：`crate::`、`use crate::...` 路徑統一、2018 不再需要 `extern crate`——模組規則簡化為「路徑即是路徑」。
  - **`async`/`await` 語法預告**：2018 edition 為未來的 async 保留關鍵字。
  - **`dyn Trait`**：trait 物件必須寫 `dyn`，讓「動態分派」在語法上顯式可見。
  - **`impl Trait`**（1.26，2018/5）：回傳型別可以寫 `fn f() -> impl Iterator<Item=u32>`，隱藏具體型別又不付 heap 配置代價。
- **工具鏈同步改進**：`cargo fix` 自動遷移舊程式碼到新 edition。

## 理論與實用原因
- **理論原因**：`impl Trait` 是**存在型別（existential types）**的受限形式；`dyn Trait` 則是顯式標註動態分派（type erasure），讓效能成本在原始碼層面可見。
- **實用原因**：舊模組系統的 `mod`/`extern crate`/`use` 三套規則是新手最大困惑源；`Box<Iterator>` 這類寫法則太囉唆且暗示不必要的 heap 配置。

## 程式範例

**舊模組系統（2015）**——三套規則並行：

```rust
// 2015 edition
extern crate serde;              // 要先宣告外部 crate
mod utils;                       // 模組宣告
use utils::helpers::format_path; // 路徑相對於 crate root，規則混亂
fn main() { format_path("a"); }
```

**新模組系統（2018）**——路徑就是路徑：

```rust
// 2018 edition：不再需要 extern crate
use serde::Serialize;
use crate::utils::helpers::format_path;   // crate:: 明確指向本 crate
fn main() { format_path("a"); }
```

**`dyn Trait`**——動態分派顯式可見：

```rust
trait Draw { fn draw(&self); }

// 2015：Box<Draw> 看不出是 trait 物件
fn render(items: Vec<Box<Draw>>) { for i in items { i.draw(); } }

// 2018：dyn 必寫，效能成本（動態分派）一眼可見
fn render(items: Vec<Box<dyn Draw>>) { for i in items { i.draw(); } }
```

**`impl Trait`（1.26）**——存在型別，隱藏具體型別又不付 heap 代價：

```rust
// 之前：必須 Box 裝箱（heap 配置 + 動態分派）
fn evens(n: u32) -> Box<dyn Iterator<Item = u32>> {
    Box::new((0..n).filter(|x| x % 2 == 0))
}

// 之後：零成本——編譯器知道具體型別，可內聯最佳化
fn evens(n: u32) -> impl Iterator<Item = u32> {
    (0..n).filter(|x| x % 2 == 0)
}
```

**cargo fix：自動遷移到新 edition**：

```bash
cargo fix --edition           # 自動改寫舊程式碼
cargo fix --edition --allow-dirty
```

## 彌補了什麼缺陷
彌補了 Rust「模組系統規則混亂、新手困惑」的缺陷，以及「trait 物件與泛型在語法上無法區分、效能成本不可見」的缺陷；Edition 機制本身則彌補了「語言演化 vs 相容性」的長期兩難。

## 相關條目
- [2019-async-await問世](2019-async-await問世.md)
- [2017-生態成熟之年](2017-生態成熟之年.md)
