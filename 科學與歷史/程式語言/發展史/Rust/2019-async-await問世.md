# 2019：async/await 問世——非同步語法的塵埃落定

## 事件
2019 年 11 月，Rust 1.39 穩定 **`async fn` 與 `.await`** 語法。非同步程式從 combinator 地獄（`future.and_then(|x| ... .map_err(...))`）變成看似同步的直覺寫法。

## 為何重要
- **語法**：`async fn f() -> Result<T, E>` 回傳一個 Future；在 async 語境中用 `f().await` 等待結果。編譯器把 async fn 編譯成**狀態機（state machine）**，零 heap 配置、零執行緒開銷。
- **零成本非同步的意義**：與 Go 的 goroutine（runtime 排程、stack 切換）不同，Rust 的 async 是**編譯期展開**——與 C++/Node.js 的事件迴圈相比，寫法直覺；與 goroutine 相比，成本接近裸 C 的手寫狀態機。
- **非同步生態戰國結束**：2018–2019 年間 futures 0.1/0.3、tokio、async-std 各自為政；`async`/`await` 語法穩定後，生態統一於 `std::future::Future` 標準介面。
- **工具鏈**：2019 年 **rust-analyzer** 開始成為主流 IDE 後端（後於 2020 年成為官方推薦）——以「編譯器即函式庫」思路補齊 rustc 的 IDE 缺陷。

## 理論與實用原因
- **理論原因**：`Future` 是一個單子式的懶求值抽象；`async`/`await` 來自 C#（2012）與 F#（2007）的實踐、以及 do-notation 的理論——把 CPS（續體傳遞風格）的巢狀回呼轉為線性程式碼。Rust 特殊之處在於 Future 是**無 pinning 狀態機**，需要 `Pin` 型別保證自引用結構不被移動。
- **實用原因**：網路服務（Docker 生態、資料庫驅動）需要處理數萬並發連線；OS 執行緒每個要數 MB stack，切換成本高；callback 寫法則導致可讀性崩壞與所有權問題。

## 程式範例

**`async`/`await` 之前：combinator 地獄（futures 0.1 時代）**：

```rust
// 2018 年前後：巢狀回呼式的 combinator
fn fetch_data(client: &Client, url: &str) -> impl Future<Item = String, Error = Error> {
    client.get(url)
        .and_then(|res| res.into_body().concat2())
        .map(|body| String::from_utf8_lossy(&body).to_string())
        .map_err(|e| e.into())
}
// 兩層還好，五層之後所有權、錯誤型別、可讀性全部崩壞
```

**`async`/`await` 之後（1.39）**——看似同步的直覺寫法：

```rust
use std::future::Future;

async fn fetch_data(client: &Client, url: &str) -> Result<String, Error> {
    let res = client.get(url).send().await?;     // await + ? 組合
    let body = res.text().await?;
    Ok(body)
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    let a = fetch_data(&client, "https://a.example").await?;
    let b = fetch_data(&client, "https://b.example").await?;
    // 並發：兩個請求同時跑，await 等待全部
    let (x, y) = tokio::join!(
        fetch_data(&client, "https://a.example"),
        fetch_data(&client, "https://b.example"),
    );
    Ok(())
}
```

**編譯器把 async fn 展開成狀態機**——零 heap、零執行緒切換：

```rust
// async fn f() { let a = step1().await; let b = step2(&a).await; }
// 編譯器大致生成：
enum F {
    Start,
    Wait1(Step1F),
    Wait2(Step2F, String),   // a 存在狀態機裡——自引用，需要 Pin 保證不被移動
    Done,
}
// poll() 被呼叫時推進狀態——與手寫狀態機同等效能，但寫法直覺
```

**rust-analyzer：IDE 後端**：

```bash
# 2020 年起成為官方推薦的 IDE 後端（VS Code / Neovim / Emacs）
rustup component add rust-analyzer
```

## 彌補了什麼缺陷
彌補了 Rust「非同步只能靠 combinator，可讀性與人體工學崩壞」的缺陷——這是 Rust 1.0 後被最多人詬病的地方。`async`/`await` + NLL（1.36 穩定）讓非同步與借用檢查終於和諧共存。

## 相關條目
- [2018-Rust-2018-Edition](2018-Rust-2018-Edition.md)
- [2023-async-fn-in-trait與企業化](2023-async-fn-in-trait與企業化.md)
