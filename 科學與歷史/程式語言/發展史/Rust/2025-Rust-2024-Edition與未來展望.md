# 2025：Rust 2024 Edition 與未來展望

## 事件
2025 年 2 月，Rust 1.85 發佈 **Rust 2024 Edition**。同年，Rust 語言規範（spec）持續標準化，實驗性借用檢查器 Polonius 逼近穩定，Linux 核心中 Rust 程式碼持續擴張（GPU 驅動 Nova、Apple Silicon 支援等）。

## 為何重要
- **Rust 2024 Edition 的具體改動**：
  - **RPIT lifetime capture 規則改變**：`-> impl Trait` 捕獲所有 in-scope 生命週期，語意更可預期。
  - **`unsafe` 屬性要求**：`#[no_mangle]`、`#[export_name]` 等必須寫在 `unsafe` 區塊/屬性中，讓 FFI 邊界的安全責任顯式化。
  - **`static mut` 存取改為 unsafe**：直接存取 `static mut` 現在需要 unsafe，補上一個 long-standing 的安全缺口。
  - **閉包捕獲精確化（`impl` 生命週期）、未來相容性保留字**（`gen` 成為保留字，為生成器語法鋪路）。
- **Polonius 借用檢查器**：以資流分析（dataflow）重寫借用檢查，解決 NLL 仍會誤報的「條件式借用回傳」問題（著名的 Polonius 案例）——讓借用檢查「更少誤判」而非「更少檢查」。
- **規範標準化**：Ferrocene 等標準化嘗試與官方 spec 讓 Rust 進入汽車（ISO 26262）、航太等安全關鍵（safety-critical）產業。
- **未來方向**：產生器（generator）語法、effect systems 討論、特化（specialization）穩定化、與 C++ 的互通（interop initiative）持續推進。

## 理論與實用原因
- **理論原因**：Edition 的生命周期規則修正是「型別系統精度 vs 可預期性」的取捨；Polonius 基於資流分析的借貸（loan）理論，是借用檢查理論的第三代。
- **實用原因**：`static mut` 與 FFI 屬性是實務中最容易被濫用的 unsafe 邊界；安全關鍵產業（汽車、醫療）需要標準化規範才能採用。

## 程式範例

**Rust 2024 Edition：`unsafe` 屬性要求**——FFI 邊界責任顯式化：

```rust
// 2021 edition：#[no_mangle] 直接寫，安全責任隱形
// #[no_mangle]
// pub extern "C" fn my_export() {}

// 2024 edition：必須明確標 unsafe——「這個匯出改變了連結器行為」
#[unsafe(no_mangle)]
pub extern "C" fn my_export() {}
```

**`static mut` 存取改為 unsafe**——補上 long-standing 安全缺口：

```rust
static mut COUNTER: u32 = 0;

// 2021 edition：直接存取，沒有警告——資料競爭的可能來源
// unsafe-free: COUNTER += 1;

// 2024 edition：必須 unsafe，迫使開發者正視共享可變狀態
unsafe { COUNTER += 1 }
// 正確做法早就存在：AtomicU32 或 Mutex
let counter = std::sync::atomic::AtomicU32::new(0);
counter.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
```

**Polonius：借用檢查器的第三代**——解決 NLL 仍會誤報的條件式借用：

```rust
fn get_default<'a>(map: &'a mut HashMap<String, String>, key: &str) -> &'a String {
    // NLL 誤判的經典案例：借用 map 查 key，又要借用 map 寫入預設值
    match map.get(key) {
        Some(v) => v,                    // NLL 之前：編譯錯誤（誤報）
        None => { map.insert(key.into(), "default".into()); &map[key] }
    }
    // Polonius 以資流分析重寫借貸邏輯，讓這類合法程式通過——
    // 更少誤判，而非更少檢查
}
```

**`gen` 保留字**——為生成器語法鋪路：

```rust
// 未來的 generator 語法（預告，gen 已成為保留字）：
// fn fibonacci() -> gen i32 {
//     let (mut a, mut b) = (0, 1);
//     while true { yield a; (a, b) = (b, a + b); }
// }
```

## 彌補了什麼缺陷
彌補了 Rust「unsafe 邊界責任不明確（2024 Edition）」與「借用檢查器殘留誤報（Polonius）」的缺陷；規範標準化則彌補了「安全關鍵產業無法採用非標準化語言」的缺陷。

## 發展主軸總結
從 2006 年一部壞電梯的靈感，到 2025 年 Windows、Linux、Android 核心與白宮政策——Rust 用二十年證明：**記憶體安全不必犧牲速度，理論（型別系統）可以成為產業（資安政策）**。

## 相關條目
- [2024-Windows重寫與AI基礎設施](2024-Windows重寫與AI基礎設施.md)
- [2015-Rust-1-0問世](2015-Rust-1-0問世.md)
