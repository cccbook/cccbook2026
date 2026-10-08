# 2016：問號運算子與 rustup——人體工學的第一次大躍進

## 事件
2016 年，Rust 1.13（11 月）引入 **`?` 錯誤傳播運算子**。同年推出 **rustup**，統一管理工具鏈（stable/beta/nightly、交叉編譯目標）。首屆年度「State of Rust」調查也在此年開始。

## 為何重要
- **`?` 運算子**：把 `match err { Ok(v) => v, Err(e) => return Err(From::from(e)) }` 這類樣板壓縮成一個 `expr?`。這是 Rust 歷史上第一次「純人體工學（ergonomics）」的語言改動——不改變能力，只改變書寫成本。
  - **理論原因**：`?` 是 Result 單子的 do-notation 語法糖（Haskell 的 `?=` bind）；錯誤傳播是**鐵路導向程式設計（railway-oriented programming）**的顯式化。
  - **實用原因**：1.0 之前錯誤處理靠 `try!` 巨集，巢狀一深就可讀性崩壞； surveys 顯示「學不會借用檢查、錯誤處理太囉唆」是學習曲線兩大痛點。
- **rustup 的意義**：補齊工具鏈版本管理——不同專案可用不同編譯器版本、nightly 特性、交叉編譯目標一鍵安裝。彌補了「rustc 手動安裝、版本混亂」的缺陷。
- **社會化轉折**：1.0 後一年，社群體認到「語言的敵人是學習曲線」，2017 Roadmap 由此定調為「生產力、人體工學」。

## 程式範例

**`?` 之前：`try!` 巨集的囉唆**：

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username(path: &str) -> Result<String, io::Error> {
    let f = try!(File::open(path));          // 2016 之前的寫法
    let mut s = String::new();
    try!(f.read_to_string(&mut s));          // 巢狀一深就可讀性崩壞
    Ok(s)
}
```

**`?` 之後（1.13）**——一行傳播錯誤，並自動做型別轉換：

```rust
fn read_username(path: &str) -> Result<String, io::Error> {
    let mut s = String::new();
    File::open(path)?.read_to_string(&mut s)?;   // ? = 出錯就 return Err(From::from(e))
    Ok(s)
}
```

`?` 展開後等價於：

```rust
match expr {
    Ok(v)  => v,
    Err(e) => return Err(From::from(e)),   // From 讓錯誤型別自動轉換
}
```

**rustup：一鍵管理工具鏈**：

```bash
rustup install nightly            # 安裝 nightly
rustup default stable             # 切換預設工具鏈
rustup target add wasm32-unknown-unknown   # 交叉編譯目標
rustup override set nightly-2016-01-01     # 某專案鎖定特定版本
```

## 彌補了什麼缺陷
彌補了 Rust 1.0「錯誤處理樣板過多、`try!` 可讀性差」的缺陷，以及工具鏈「版本管理碎片化、nightly 特性難以試用」的缺陷。

## 相關條目
- [2015-Rust-1-0問世](2015-Rust-1-0問世.md)
- [2017-生態成熟之年](2017-生態成熟之年.md)
