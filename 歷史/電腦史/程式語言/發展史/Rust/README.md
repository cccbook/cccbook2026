# Rust 程式語言發展史年表

> Rust 是 2006 年由 Graydon Hoare 在 Mozilla 以個人側專案開始的語言，
> 目標是「系統程式設計的速度，加上記憶體安全的保證」。
> 它融合了 ML/Haskell（型別系統）、C++（零成本抽象）、Cyclone（區域型別）等傳統，
> 並以「所有權（ownership）與借用檢查器（borrow checker）」在編譯期消滅記憶體錯誤，
> 成為第一個不用垃圾回收、卻保證記憶體安全的主流語言。

## 前史：理論根源

| 年份 | 事件 | 意義 |
|------|------|------|
| 1958 | LISP 問世 | 垃圾回收與高階抽象的先驅（Rust 選擇了反向路線：無 GC） |
| 1972 | C 語言 | 系統程式設計的事實標準，也是記憶體安全問題的根源 |
| 1978 | ML 語言 | Hindley–Milner 型別推論：型別標註可省略，由編譯器推導 |
| 1985 | C++ | RAII（資源取得即初始化）：物件解構時釋放資源，Rust drop 的思想源頭 |
| 1988 | Objective Caml 前身 | 模式比對、代數資料類型（enum/struct）、trait 式多型的基礎 |
| 2001 | Cyclone 語言 | C 的安全方言，區域（region）型別檢查記憶體壽命——借用檢查的理論前身 |
| 2003 | Cppcheck/CVE 時代 | 統計顯示 Microsoft/Google 的大型 C/C++ 專案約 70% 嚴重漏洞源於記憶體安全 |

## 正式年表

| 年份 | 標題 | 關鍵語法/特性 |
|------|------|---------------|
| 2006 | [Graydon Hoare 的個人專案](2006-GraydonHoare的個人專案.md) | 語言誕生：所有權構想、無 GC 的記憶體安全目標 |
| 2010 | [Mozilla 贊助與首次公開](2010-Mozilla贊助與首次公開.md) | Rust 公開發佈、自舉編譯器啟動、初期型別類（kind）系統 |
| 2012 | [rustpkg 與自舉之路](2012-rustpkg與自舉之路.md) | rustc 0.4 自舉、rustpkg 套件管理實驗、類別系統簡化 |
| 2014 | [Cargo 與 crates.io 問世](2014-Cargo與crates-io問世.md) | Cargo 1.0、crates.io 上線、語言刪除 GC 完成最後瘦身 |
| 2015 | [Rust 1.0 問世](2015-Rust-1-0問世.md) | 1.0 穩定承諾、所有權/借用/生命週期、trait、宏、模式比對定型 |
| 2016 | [問號運算子與 rustup](2016-問號運算子與rustup.md) | `?` 錯誤傳播運算子（1.13）、rustup 工具鏈管理器、首屆 State of Rust |
| 2017 | [生態成熟之年](2017-生態成熟之年.md) | impl Trait 前身討論、2017 Roadmap：生產力、1.x 小步快跑模式確立 |
| 2018 | [Rust 2018 Edition](2018-Rust-2018-Edition.md) | 第一個 Edition、`async`/`await` 語法預告、模組系統改革、`dyn Trait` |
| 2019 | [async/await 問世](2019-async-await問世.md) | `async fn`/`.await`（1.39）、未來的 rust-analyzer、非同步生態戰國結束 |
| 2020 | [Rust 基金會前夜](2020-Rust基金會前夜.md) | AWS/Microsoft/Google 全面採用、零成本非同步、編譯器效能大作戰 |
| 2021 | [const 泛型與 Rust 2021 Edition](2021-const泛型與Rust-2021-Edition.md) | const 泛型（1.51）、2021 Edition：閉包捕獲改革、IntoIterator for arrays、panic 巨集統一 |
| 2022 | [GAT、let-else 與 Linux 核心合併](2022-GAT-let-else與Linux核心合併.md) | GAT（1.65）、let-else、Linux 6.1 正式納入 Rust 支援 |
| 2023 | [async fn in trait 與企業化](2023-async-fn-in-trait與企業化.md) | async fn in trait（1.75）、C++/Rust 互通倡議、crates.io 破十萬套件 |
| 2024 | [Windows 重寫與 AI 基礎設施](2024-Windows重寫與AI基礎設施.md) | Windows 核心元件以 Rust 重寫、Rust 進入 Android/雲端 AI 基礎設施 |
| 2025 | [Rust 2024 Edition 與未來展望](2025-Rust-2024-Edition與未來展望.md) | 2024 Edition（1.85）、spec 標準化、實驗性借用檢查器 Polonius |

## 工具鏈發展主軸

1. **2012 rustpkg → 2014 Cargo** —— 套件管理從實驗走向一體化設計：`Cargo.toml`、語義化版本、依賴鎖定，成為後世語言工具鏈（如 Swift、Zig）的參考對象。
2. **2016 rustup** —— 統一管理 stable/beta/nightly 與跨平台目標，消除工具鏈版本地獄。
3. **2019 rust-analyzer** —— 以「編譯器即函式庫」思路打造 IDE 後端，補齊 rustc 的 IDE 補全缺陷。
4. **crates.io** —— 2014 年上線，2023 年突破十萬套件，安全性靠 `cargo audit` 與 supply chain 政策持續補強。

## 發展主軸

1. **2006–2010：個人專案與 Mozilla 接手** —— 一場車庫裡的實驗，為了解決「網頁瀏覽器這種 C++ 大型軟體的當機噩夢」。
2. **2010–2015：大瘦身與定型** —— 砍掉 GC、刪除過多類型理論特性，在 1.0 前完成「少而精」的語言設計。
3. **2015–2018：生態打底** —— Cargo/crates.io、rustup、`?` 運算子，讓語言好用。
4. **2018–至今：Edition 時代與企業採用** —— 非同步、const 泛型、GAT 逐步補齊表達力；Linux、Windows、Android 核心相繼採用，記憶體安全從理論變成國家級資安政策。
