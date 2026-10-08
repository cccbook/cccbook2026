# 2022：Linux 核心與 Clang 互通——工具鏈大一統

## 事件
2022 年前後的幾個里程碑：
1. **Linux 核心**逐步支援以 **Clang/LLVM** 建置（Google 的 Android 核心自 2018 年改用 Clang，2022 年 Linux 5.18 起官方 Clang 建置趨於完善）——打破「核心只能用 GCC 編譯」的 30 年慣例。
2. 同年，Linux 6.1 正式納入 **Rust** 支援——C++ 之外的記憶體安全語言進入核心，帶動 C++ 社群對安全性的反思。
3. **C++ 與 Rust 互通性**（interop）成為 WG21 與社群的熱門議題。

## 為何重要
- **Clang 進入核心**：證明 LLVM 生態已能承擔最嚴苛的系統程式碼建置——編譯器基礎設施從「雙雄並立」走向「可替換的模組」。
- **Rust 進入核心的壓力**：Microsoft（2019 宣布用 Rust 重寫 Windows 元件）、Google（Android 記憶體安全報告：CVE 70% 源於記憶體安全）先後採用 Rust，促使 C++ 社群加速推進 profiles（安全性設定檔）與 `std::expected`、邊界檢查等安全提案。
- **互通性議題**：Rust 與 C++ 的混合程式碼庫（cxx、bindgen）成為系統開發新常態。

## 理論與實用原因
- **理論原因**：編譯器後端可替換性——LLVM IR 的穩定介面讓核心建置不再綁定特定編譯器。
- **實用原因**：Android 生態需要 Clang 的 sanitizers（ASan/UBSan）；國家級資安報告（NSA 2022、CISA）點名記憶體安全語言——C++ 的安全缺陷成為政策議題。

## 彌補了什麼缺陷
彌補了「核心建置绑死 GCC、C++ 記憶體安全缺陷無系統性解方」的缺陷——Clang 的 sanitizers 與 Rust 的競爭共同推動 C++ 安全演進。

## 程式範例

以 Clang/LLVM 工具鏈建置 Linux 核心，並用 sanitizers 檢查 C++ 程式的記憶體問題：

```sh
# 以 Clang 建置 Linux 核心（LLVM=1 表示整套工具鏈都用 LLVM）
make CC=clang LLVM=1 -j$(nproc)

# 用 AddressSanitizer + UndefinedBehaviorSanitizer 編譯 C++ 程式
clang++ -std=c++17 -fsanitize=address,undefined -g main.cpp -o main

# 執行時若偵測到越界或未定義行為，會自動印出報告
./main
```

C++ 與 Rust 互通的場景示意——Rust 透過 `extern "C"` 匯出函式，C++ 端宣告後即可呼叫：

```rust
// Rust 端：libadd.rs，編譯成動態函式庫
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

```cpp
// C++ 端：main.cpp，宣告並呼叫 Rust 匯出的函式
extern "C" int add(int a, int b);  // 對應 Rust 的 extern "C" 匯出

#include <iostream>

int main() {
    std::cout << "1 + 2 = " << add(1, 2) << std::endl;
    return 0;
}
```

更複雜的型別與物件互通，社群則常用 **cxx** 橋接工具自動產生兩側的繫結程式碼。

## 相關條目
- [2007-Clang與LLVM問世](2007-Clang與LLVM問世.md)
- [2017-C++17結構化綁定](2017-C++17結構化綁定.md)
- [2023-C++23與模組時代](2023-C++23與模組時代.md)
