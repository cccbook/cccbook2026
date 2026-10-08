# 2023：async fn in trait 與企業化——非同步抽象補完

## 事件
2023 年，Rust 1.75（12 月）穩定 **async fn in trait**——trait 方法可以直接宣告 `async fn`，不再需要 `#[async_trait]` 巨集。同年 crates.io 突破十萬套件，Rust 進一步企業化。

## 為何重要
- **async fn in trait**：
  ```rust
  trait Fetch {
      async fn fetch(&self, url: &str) -> Result<Bytes, Error>;
  }
  ```
  - **彌補的缺陷**：2019 年 `async`/`await` 穩定時，**trait 中不能宣告 async 方法**（編譯器尚未解決「回傳型別含匿名 Future + 生命週期」的問題），生態靠 `#[async_trait]` 巨集把 Future 裝箱（`Box<dyn Future>`）——每次呼叫多一次 heap 配置與動態分派。
  - **理論原因**：async fn in trait 本質是 GAT + RPITIT（return position impl trait in trait）的組合——把「回傳的匿名 Future 型別」用存在型別表達，編譯器為每個實作生成具體狀態機。
  - **實用原因**：資料庫驅動、RPC 框架（tonic）、Web 框架（axum）的 trait 抽象全面受益；零裝箱讓非同步抽象達到與同步抽象同等的零成本。
- **RPITIT 同時穩定**：trait 方法可以 `-> impl Trait`，同步抽象也獲得同樣的表達力。
- **企業化**：crates.io 破十萬套件；`cargo audit`、crates.io 的 supply chain 政策（trusted publishing）持續補強套件生態安全。

## 理論與實用原因
- **理論原因**：存在型別（existential type）在 trait 回傳位置的落地，是 Rust 型別系統「隱藏具體型別、保留零成本」哲學的完成。
- **實用原因**：`#[async_trait]` 的 Box 裝箱在高頻呼叫路徑（每個請求數百次 await）的配置成本可觀；巨集也讓錯誤訊息難以閱讀。

## 程式範例

**`#[async_trait]` 時代（2019–2023）**——Box 裝箱的變通：

```rust
use async_trait::async_trait;

#[async_trait]
trait Fetch {
    async fn fetch(&self, url: &str) -> Result<Bytes, Error>;
}

// 巨集自動改寫成（每次呼叫都 heap 配置 + 動態分派）：
// fn fetch<'a>(&'a self, url: &'a str)
//     -> Pin<Box<dyn Future<Output = Result<Bytes, Error>> + Send + 'a>>;
```

**async fn in trait（1.75）**——零裝箱：

```rust
trait Fetch {
    async fn fetch(&self, url: &str) -> Result<Bytes, Error>;
    // 編譯器為每個 impl 生成具體的匿名狀態機——零 heap、可內聯
}

struct HttpFetcher { client: Client }

impl Fetch for HttpFetcher {
    async fn fetch(&self, url: &str) -> Result<Bytes, Error> {
        Ok(self.client.get(url).send().await?.bytes().await?)
    }
}
```

**RPITIT 同時穩定**——trait 回傳 `impl Trait`：

```rust
trait Visitor {
    fn items(&self) -> impl Iterator<Item = u32>;   // 隱藏具體型別，零成本
}
```

**crates.io 供應鏈安全**——cargo audit：

```bash
cargo install cargo-audit
cargo audit        # 檢查 Cargo.lock 中的已知漏洞（RustSec 資料庫）
```

## 彌補了什麼缺陷
彌補了 Rust「trait 無法直接抽象非同步方法、需裝箱與巨集變通」的缺陷——2019 年 async/await 問世時留下的最後一塊非同步抽象拼圖就此補齊。

## 相關條目
- [2019-async-await問世](2019-async-await問世.md)
- [2024-Windows重寫與AI基礎設施](2024-Windows重寫與AI基礎設施.md)
