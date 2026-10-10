# 2024：Windows 重寫與 AI 基礎設施——記憶體安全成為國家政策

## 事件
2024 年，**Microsoft 開始在 Windows 11 核心元件（如 win32k 的 DDI 實作）以 Rust 重寫**；Google 宣佈 Android 新程式碼中 Rust 已超過 C/C++（Rust 相關元件的記憶體漏洞比例降至趨近於零）；Rust 也成為 AI 基礎設施（推理引擎 candle、llama.cpp 生態、資料處理工具）的熱門選擇。

## 為何重要
- **記憶體安全成為政策**：2024 年 2 月 **白宮 ONCD（國家網路主任辦公室）發佈報告**，正式呼籲業界採用記憶體安全語言（Rust 是無 GC 的唯一選項）；CISA、NSA 持續發佈指引。
- **Windows 重寫的意義**：30 年的 win32k 核心攻擊面（歷史上最多藍屏與漏洞的元件之一）開始以 Rust 重寫——「安全修復不再依賴人工 code review，而是編譯器強制」。
- **Google 的數據**：Android 團隊公佈，Rust 導入後記憶體安全漏洞佔比從 76%（2019）降到 24%（2024），且 Rust 元件**零記憶體漏洞**——這是語言理論第一次以如此規模的生產數據驗證。
- **語言與工具鏈持續演進**：2024 年 nightly 開始試驗新一代借用檢查器 **Polonius**（解決 NLL 的「貸款分析」誤報）、`cargo script` 討論、crates.io 供應鏈安全強化。

## 理論與實用原因
- **理論原因**：所有權系統的安全性經過大規模生產驗證——「編譯期證明記憶體安全」從論文（RustBelt, 2017–2018 的形式化驗證）變成產業事實。
- **實用原因**：資安攻擊成本（勒索軟體、供應鏈攻擊）遠高於重寫成本；AI 推理需要 C 級效能與 GPU 直接控制，又需要安全的多執行緒。

## 程式範例

**Windows 核心重寫**——win32k 的 DDI 以 Rust 實作後，編譯器強制安全：

```rust
// Windows 核心元件（概念示意）：使用者傳入的指標由型別系統把關
// C 版本：直接解引用使用者指標 → 藍屏/提權漏洞的經典來源
// void NtUserFoo(PVOID user_ptr) { UCHAR *p = user_ptr; *p = 1; }

// Rust 版本：使用者記憶體必須先安全讀取，錯誤處理是語言強制的
unsafe fn copy_user(dst: &mut [u8], src: *const u8) -> Result<(), KernelError> {
    for (i, d) in dst.iter_mut().enumerate() {
        *d = core::ptr::read_volatile(src.add(i));   // volatile 讀取使用者頁
    }
    Ok(())
    // C 版本常見的 Off-by-one、null 指標解引用，在這裡編譯不過
}
```

**Google Android 的數據**：

```
Android 記憶體安全漏洞佔比：
  2019：76%（C/C++ 為主）
  2024：24%——且新導入的 Rust 元件：零記憶體漏洞
  → 結論：新程式碼中 Rust 已超過 C/C++
```

**AI 推理引擎**——C 級效能 + GPU 直接控制 + 安全多執行緒：

```rust
// candle 風格的 tensor 操作：零成本抽象，借用檢查防止資料競爭
let device = candle_core::Device::cuda_if_available(0)?;
let a = candle_core::Tensor::randn(0f32, 1f32, (1024, 1024), &device)?;
let b = a.matmul(&a)?;      // 與 C++/CUDA 綁定同等效能，無 GC、無資料競爭
```

## 彌補了什麼缺陷
彌補了「作業系統與基礎設施的記憶體漏洞無法以人工審查根除」的缺陷——2024 是記憶體安全從「Rust 的賣點」變成「政府與產業的共同政策」的一年。

## 相關條目
- [2023-async-fn-in-trait與企業化](2023-async-fn-in-trait與企業化.md)
- [2025-Rust-2024-Edition與未來展望](2025-Rust-2024-Edition與未來展望.md)
