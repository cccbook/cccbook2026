# 2022：GAT、let-else 與 Linux 核心合併——主流化的元年

## 事件
2022 年的三件大事：**GAT**（1.65，11 月）、**let-else**（1.65）、以及 **Linux 6.1 正式合併 Rust 支援**（12 月）——Rust 成為第一個（C 之外）進入 Linux 核心的語言。

## 為何重要
- **GAT（Generic Associated Types）**：trait 的關聯型別終於可以自帶泛型參數——
  ```rust
  trait LendingIterator {
      type Item<'a> where Self: 'a;
      fn next(&mut self) -> Option<Self::Item<'_>>;
  }
  ```
  - **彌補的缺陷**：1.0 的關聯型別無法表達「借用自 `&mut self` 的項目」，導致迭代器借用自身資料的抽象（如資料庫驅動、串流處理）寫不出來，只能靠 unsafe 或 HRTB 變通。
  - **理論原因**：GAT 讓 trait 更接近**高階型別構造子（higher-kinded types）**的表達力，是 Rust 型別系統對 ML 型別類理論的再次追趕。
- **let-else**：`let Some(x) = opt else { return; };`——把「不符則提前離開」的模式比對壓縮成一行，補齊 `?` 之後的人體工學缺口。
- **Linux 核心合併**：Linus Torvalds 親自合併。意義：記憶體安全從應用層進入**世界上最受審計的核心**；CISA/NSA 同年發佈記憶體安全指引，Rust 成為官方建議。

## 理論與實用原因
- **理論原因**：let-else 是「early return」模式的顯式化（與 `?` 同一家族）；GAT 則是型別系統理論（關聯型別的參數化）在工程上的落地。
- **實用原因**：核心與驅動程式是記憶體漏洞重災區；Google 統計顯示 Android 約七成安全漏洞源於記憶體錯誤，Rust 導入後 Rust 相關元件漏洞比例趨近於零。

## 程式範例

**GAT 之前**——借用式迭代抽象寫不出來：

```rust
// 想要：迭代器借用自身資料，每次 next 回傳借用項
// 1.0 的關聯型別無法表達「Item 的壽命綁定 &mut self」：
trait LendingIterator {
    type Item;                    // 無法寫成 type Item<'a>
    fn next(&mut self) -> Option<&Self::Item>;   // 壽命關係表達不了
}
// 只能靠 unsafe 或終身 HRTB 變通，或者 Box 裝箱犧牲效能
```

**GAT 之後（1.65）**——關聯型別自帶泛型參數：

```rust
trait LendingIterator {
    type Item<'a> where Self: 'a;               // Item 有自己的壽命參數
    fn next(&mut self) -> Option<Self::Item<'_>>;
}

struct Counter { data: Vec<u32>, pos: usize }

impl LendingIterator for Counter {
    type Item<'a> = &'a u32 where Self: 'a;
    fn next(&mut self) -> Option<&u32> {
        let item = self.data.get(self.pos)?;
        self.pos += 1;
        Some(item)
    }
}
```

**let-else（1.65）**——前置條件檢查一行搞定：

```rust
fn parse(config: &str) -> u16 {
    // 之前：
    // let port = match config.parse::<u16>() {
    //     Ok(p) => p,
    //     Err(_) => return 8080,
    // };

    // let-else：不符則提前離開
    let Ok(port) = config.parse::<u16>() else { return 8080; };
    let Some(timeout) = std::env::var("TIMEOUT").ok() else { return port; };
    port + timeout.parse().unwrap_or(0)
}
```

**Linux 核心：Rust 驅動的安全寫法**：

```rust
// Linux 6.1 起：Rust 核心模組（如 Rust for Linux 的字元裝置範例）
use kernel::prelude::*;

module! {
    type: RustChrdev,
    name: "rust_chrdev",
    license: "GPL",
}
// 核心內的緩衝區、指標操作由型別系統檢查——C 驅動的
// 緩衝區溢位類漏洞在這裡編譯不過
```

## 彌補了什麼缺陷
彌補了 Rust「無法表達借用式迭代抽象（GAT）」與「前置條件檢查樣板過多（let-else）」的缺陷；Linux 合併則彌補了「作業系統核心只有 C 一種選擇、記憶體漏洞無法根除」的歷史缺陷。

## 相關條目
- [2021-const泛型與Rust-2021-Edition](2021-const泛型與Rust-2021-Edition.md)
- [2023-async-fn-in-trait與企業化](2023-async-fn-in-trait與企業化.md)
