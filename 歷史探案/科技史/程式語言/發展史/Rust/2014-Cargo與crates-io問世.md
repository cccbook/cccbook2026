# 2014：Cargo 與 crates.io 問世——工具鏈一體化的典範

## 事件
2014 年，**Cargo** 正式取代 rustpkg，並同步上線集中式套件登錄 **crates.io**。Cargo 1.0 於同年問世，隨 Rust 1.0（2015）一起穩定。

## 為何重要
- **一體化設計**：`Cargo.toml` 宣告依賴與建置設定、`cargo build` / `cargo test` / `cargo doc` 一條龍、**語義化版本（semver）約束 + Cargo.lock 鎖定檔**，解決 rustpkg 的重現建置問題。
- **集中登錄 crates.io**：每個 crate 有唯一名稱與版本，依賴解析確定且可重現——這是 npm 之後最成功的套件生態設計，也成為 Swift Package Manager 等後進工具的參考。
- **開發者體驗即競爭力**：Graydon Hoare 與核心團隊體認到「語言好壞不只是語法，而是工具鏈體驗」。Cargo 讓「三分鐘建好專案」成為 Rust 的招牌。
- 語言方面，2014 年是最後的大刪除期：GC 全面移除，`@`/`~` 語法消失，改為函式庫型別（`Box`、`Rc`、`Arc`）。

## 理論與實用原因
- **理論原因**：依賴解析基於 constraint satisfaction（semver 範圍交集），鎖定檔確保**可重現性**；集中登錄則解決信任與命名問題。
- **實用原因**：rustpkg 時代每個專案抓取 git HEAD，依賴隨時可能壞掉；企業與開源社群都需要「鎖定、可審計、離線可建置」的套件管理。

## 程式範例

**Cargo 的核心設定**——依賴、semver 約束、一條龍指令：

```toml
# Cargo.toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }  # semver：1.0.x 皆可
tokio  = { version = "1",   features = ["full"] }
```

```bash
cargo new myapp        # 建立專案
cargo build            # 建置（自動解析並下載依賴）
cargo test             # 測試
cargo doc --open       # 產生並開啟文件
cargo add serde        # 新增依賴並自動寫入 Cargo.toml
```

**Cargo.lock 確保可重現建置**：

```toml
# Cargo.lock（自動生成，鎖定每個依賴的確切版本）
[[package]]
name = "serde"
version = "1.0.203"   # 今天與明年建置結果完全一致
```

**對照：C++ 沒有標準答案**——每個專案自己想辦法（Makefile、CMake、vcpkg、Conan、git submodule…），同一份程式碼在不同機器上「能不能編過」全憑運氣：

```cmake
# C++：三十年的生態痛點——依賴管理碎片化
find_package(Boost REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})
# Boost 版本、安裝路徑因機器而異，沒有鎖定檔
```

## 彌補了什麼缺陷
彌補了 rustpkg「無集中登錄、無版本鎖定、建置不可重現」的缺陷，也彌補了 C++「沒有標準套件管理、每個專案自己想辦法管依賴」這個四十年的生態痛點。

## 相關條目
- [2012-rustpkg與自舉之路](2012-rustpkg與自舉之路.md)
- [2015-Rust-1-0問世](2015-Rust-1-0問世.md)
