# 2015 - WebAssembly：瀏覽器成為通用虛擬機

## 案件摘要
2015 年，四大瀏覽器廠商（Mozilla、Google、Microsoft、Apple）聯手宣布 WebAssembly（Wasm）計畫，2017 年成為 W3C 標準。嫌犯動機：JavaScript 太慢、太動態，瀏覽器需要一個可預測、接近原生的編譯目標。

## 前因 -- 為什麼會有這個案子
- 瀏覽器裡想跑 C/C++ 遊戲、影像處理、CAD——但 JS 引擎的動態型別與 GC 讓效能捉襟見肘。
- **asm.js（2013，Mozilla Alon Zakai）** 是前驅：把 JS 限制成「可靜態推論型別」的子集，用前置型別註記讓引擎 AOT 編譯。
- NaCl/PNaCl（Google）走沙箱位元碼路線，但綁定過緊、跨瀏覽器不可行。四方聯手把 asm.js 的經驗升級成真正的二進位虛擬機格式。

## 線索與推理 -- 數學式、程式、理論

### 線索 1：asm.js 的前驅推理
asm.js 用型別註記讓 `x|0`（整數）、`+x`（浮點）成為可靜態分析的型別轉換：
```javascript
function fib(n) {
  n = n | 0;                  // n 是 int32
  if ((n | 0) < 2) return 1;
  return (fib((n - 1) | 0) + fib((n - 2) | 0)) | 0;
}
```
引擎驗證整個函式通過型別檢查後，可跳過直譯直接 AOT 編譯——這證明了「驗證型子集 + 提前編譯」路線可行。

### 線索 2：Wasm 二進位格式與堆疊機
Wasm 是**驗證型（type-safe）堆疊機**位元碼。指令明確標注型別：
$$(i32.add\ (local.get\ 0)\ (local.get\ 1)) : i32 \times i32 \to i32$$
模組在載入時經過**單趟驗證**（single-pass validation），驗證通過才編譯執行——沙箱安全的理論根基。

Wat 文字格式與二進位格式一一對應：
```wat
(module
  (func $add (param $a i32) (param $b i32) (result i32)
    local.get $a
    local.get $b
    i32.add)          ;; 堆疊機：push a, push b, pop 兩值相加 push 結果
  (export "add" (func $add)))
```

### 線索 3：驗證型與沙箱安全
Wasm 的安全模型：
1. **結構化控制流**：無任意 goto/跳到資料位址，控制流圖可靜態建構。
2. **線性記憶體**：所有存取限制在模組自己的線性記憶體 $[0, M)$，越界即 trap：
$$\forall \text{ 記憶體存取 } a:\ a + size \le M \ \text{ 否則 trap}$$
3. **無能力外洩**：預設無法直接呼叫系統呼叫、觸碰 host 記憶體，一切需經 host 環境提供的 imported function。

### 線索 4：Emscripten 編譯 C/C++/Rust 到 Wasm
```shell
# C → Wasm
emcc hello.c -o hello.js         # 產生 JS 膠水 + hello.wasm

# Rust → Wasm
cargo build --target wasm32-unknown-unknown
```
Emscripten（Alon Zakai，2011 起）先以 asm.js 為目標、後改 Wasm，把整個 C/C++ 生態（含 LLVM/Clang 管線）搬進瀏覽器：編譯管線為
$$C/C{+}{+} \xrightarrow{\text{clang}} \text{LLVM IR} \xrightarrow{\text{emcc/LLVM}} \text{Wasm}$$

### 線索 5：Python/Wat 範例展示 Wasm 模組載入
```shell
# 安裝 wat 與 wasm 工具鏈
pip install wasmtime
wat2wasm add.wat -o add.wasm   # WABT 工具：wat 文字 → wasm 二進位
```
```python
from wasmtime import Engine, Store, Module, Instance

engine = Engine()
module = Module.from_file(engine, "add.wasm")
store = Store(engine)
instance = Instance(store, module, [])
print(instance.exports(store)["add"](store, 3, 4))  # 7
```

### 線索 6：效能證據
Wasm 執行速度約為原生碼的 **1.5–2 倍慢**（即原生速度的 50–70%）：
$$T_{wasm} \approx (1.5 \sim 2)\,T_{native} \ll T_{js} \approx 10\,T_{native}$$
比 JavaScript 快 5–10 倍，且記憶體使用可預測（無 GC 抖動）。

## 結案 -- 後果與影響
- **瀏覽器成為通用 VM**：Figma、AutoCAD Web、Google Earth、無數遊戲引擎以 Wasm 進入瀏覽器。
- **WASI（2019）**：WebAssembly System Interface 把 Wasm 帶出瀏覽器，成為雲端、邊緣運算的通用執行格式。
- 主流語言全部擁有 Wasm 後端：Rust、C/C++、Go、.NET（Blazor）、Python（Pyodide）。
- Wasm 與 Docker 之争（Docker 創辦人語：「若 Wasm 早存在，我們就不會做 Docker」）鋪往 2020s 的雲端原生戰場。

## 關鍵人物與文獻
- **Alon Zakai**：asm.js 與 Emscripten 之父。
- **Luke Wagner**：Wasm 核心設計者（Mozilla）。
- 文獻：W3C *WebAssembly Core Specification* (2017/2022)；Haas et al., *Bringing the Web up to Speed with WebAssembly* (PLDI 2017)；WASI 官方文件。
