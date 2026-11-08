# 附錄 A.2：關鍵字與內建函式清單

本附錄以概括方式列出 Veryl 的關鍵字與常用內建系統函式。語言仍在演進，完整且最新的清單一律以官方手冊（https://doc.veryl-lang.org）為準。

## 結構關鍵字

| 關鍵字 | 用途 |
|---|---|
| `module` | 定義模組，硬體的基本單位 |
| `interface` | 定義介面，封裝一群相關訊號 |
| `modport` | 在 interface 內宣告各方向的存取視角 |
| `proto` | 定義 proto module / proto interface（契約），實作側以 `module Foo for FooIF` 綁定 |
| `package` | 定義套件，收納 const/struct/enum/function |
| `struct` | 定義結構體型別 |
| `enum` | 定義列舉型別 |
| `union` | 定義聯合型別（概列） |
| `function` | 定義函式 |
| `impl` | 實作 trait（概列，最新語意以官方手冊為準） |
| `embed` | 嵌入原生 SV / cocotb 程式碼區塊 |

## 宣告關鍵字

| 關鍵字 | 用途 |
|---|---|
| `var` | 可變變數宣告 |
| `let` | 單一賦值變數宣告 |
| `const` | 常數宣告 |
| `param` | 參數宣告（module 內） |
| `port` | 埠宣告（module 定義內） |
| `inst` | 實例化 module 或 interface |
| `bind` | 將模組綁定到其他模組/介面（概列） |
| `assign` | 連續賦值 |
| `pub` | 公開可見性（package 內項目對外可見） |
| `import` | 匯入 package 的項目 |
| `alias` | 建立別名（型別或識別字，概列） |

## 行為關鍵字

| 關鍵字 | 用途 |
|---|---|
| `always_comb` | 組合邏輯區塊 |
| `always_ff` | 時序邏輯區塊，帶時脈與 reset 引數 |
| `if_reset` | always_ff 內的 reset 分支 |
| `initial`（概列） | 初始區塊（主要用於模擬） |
| `if` / `else` | 條件 |
| `case` / `default` | 多路分支（`case`/`casem`/`casez` 變體以官方手冊為準） |
| `for` / `in` / `step` | 迴圈（合成用 generate for 與行為 for 共用語法） |
| `while` | 迴圈 |
| `return` | 函式返回 |
| `break` / `continue` | 迴圈控制（概列） |
| `and` / `or` / `not` / `xor` / `sll` / `srl` / `sra`（概列） | 建議留意：Veryl 部分位元運算子採關鍵字形式，最新清單見官方手冊 |

## 型別與方向關鍵字

| 關鍵字 | 用途 |
|---|---|
| `logic` / `bit` | 位向量型別基底 |
| `input` / `output` / `inout` / `modport` | 埠方向 |
| `clock` / `clock_posedge` / `clock_negedge` | 時脈型別 |
| `reset` / `reset_async_high` / `reset_async_low` / `reset_sync_high` / `reset_sync_low` | reset 型別（極性與同步性由型別決定） |
| `u32` / `u64` / `i32` / `i64` / `f32` / `f64` | 整數與浮點型別 |
| `string` | 字串型別（主要用於模擬） |
| `tri` | 三態型別（概列） |
| `as` | 型別轉換 |
| `widthof` / `$bits`（概列） | 取得位寬 |

## 生成與屬性

| 關鍵字 | 用途 |
|---|---|
| `if COND: label { }` | labelled generate if（label 為強制） |
| `for i: u32 in 0..W { }` | generate for |
| `#[...]` | 屬性（attribute），如 `#[test(name)]` 標記測試 |

## 內建系統函式（概列）

| 函式 | 用途 | SV 對應 |
|---|---|---|
| `$clog2(x)` | 取上取 2 為底對數，位寬計算常客 | `$clog2` |
| `$bits(x)` | 運算式的總位元數 | `$bits` |
| `$readmemh` / `$readmemb` | 從檔案載入記憶體內容（模擬用） | 同名 |
| `$display` / `$write` | 模擬輸出 | 同名 |
| `$finish` | 結束模擬 | 同名 |

系統函式與仿真專用功能在 Veryl 中多為直接沿用 SV 的 `$` 函式；未列出的項目（時間函式、隨機數、斷言相關等）以官方手冊為準。使用 `embed (inline)` 區塊時，任何 SV 系統任務也可透過 `$sv` namespace 直接呼叫。
