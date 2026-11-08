# 附錄 A.1：Veryl 與 SystemVerilog 對照表

本附錄整理 Veryl 與 SystemVerilog 的語法對照，供有 SV 背景的讀者快速遷移。Veryl 經 `veryl build` 轉譯為 SV，因此每一條對照都對應實際產出的程式碼。以官方手冊（https://doc.veryl-lang.org）為最終依據。

## 模組與埠

| Veryl | SystemVerilog |
|---|---|
| `module Foo ( port a: input logic<8>, ) { }` | `module Foo (input logic [7:0] a); ... endmodule` |
| `module Foo::<W: u32 = 8> ( port a: input logic<W>, ) { }` | `module Foo #(parameter int W = 8) (input logic [W-1:0] a); ... endmodule` |
| 埠方向可省略，由編譯器推導 | 方向必須明寫 |
| `inst u: Foo;` | `Foo u (/* .port 連線 */);` |
| `inst u: Foo::<8>;` | `Foo #(.W(8)) u (...);` |
| `inst u: Foo (bus);` | `Foo u (.bus(bus));`（interface 連接） |
| `module Fifo for FifoIF { }` | （SV 無直接對應，以命名慣例約束） |

## 宣告與賦值

| Veryl | SystemVerilog |
|---|---|
| `var x: logic<8>;` | `logic [7:0] x;` |
| `let y: logic<32> = a * b;` | `logic [31:0] y; assign y = a * b;` |
| `const C: u32 = 1;` | `localparam int C = 1;` |
| `param P: u32 = 8;` | `parameter int P = 8;`（module 內） |
| `x = 1;`（always 區塊內） | `x = 1;`（blocking）或 `x <= 1;`（nonblocking，Veryl 依時序/組合域決定） |
| `u32` / `i32` | `int unsigned` / `int` |
| `logic<W>` | `logic [W-1:0]` |
| `logic<N><M>`（二維） | `logic [M-1:0] x [N]`（對應 unpacked 陣列，形態以官方文件為準） |
| 位串接 `a << b` | `{a, b}` |
| 位選切 `a[7:4]`、`a[4 +: 4]` | 同 SV |

## always 區塊與 reset

| Veryl | SystemVerilog |
|---|---|
| `always_comb { ... }` | `always_comb begin ... end` |
| `always_ff (clk, rst) { if_reset { ... } else { ... } }` | `always_ff @(posedge clk or posedge rst) begin if (rst) ... else ... end`（依 reset 型別決定同步/非同步） |
| `reset`、`reset_async_high`、`reset_async_low`、`reset_sync_high` 等型別 | 由 sensitivity list 與極性決定，無型別保障 |
| `x += 1;`（在 always_ff 內） | `x <= x + 1;` |

## 控制流程

| Veryl | SystemVerilog |
|---|---|
| `if c { } else if d { } else { }` | `if (c) ... else if (d) ... else ...` |
| `case x { A: {}, default: {} }` | `case (x) A: ...; default: ...; endcase` |
| `for i: u32 in 0..W { }` | `for (int i = 0; i < W; i++) ...` |
| `while c { }` | `while (c) ...` |

## enum / struct / package / function

| Veryl | SystemVerilog |
|---|---|
| `enum State: logic<2> { Idle = 0, Run, Done }` | `typedef enum logic [1:0] { Idle = 2'd0, Run, Done } State;` |
| `State::Idle` | `Idle`（SV enum 值不用 scope 存取） |
| `struct S { a: logic<8>, b: logic<4> }` | `typedef struct packed { logic [7:0] a; logic [3:0] b; } S;` |
| `s.a` | `s.a` |
| `package P { const A: u32 = 1; }` | `package P; parameter int A = 1; endpackage` |
| `P::A` | `P::A` |
| `function F(a: u32) -> u32 { return a + 1; }` | `function automatic int unsigned F(int unsigned a); return a + 1; endfunction` |

## interface 與 modport

| Veryl | SystemVerilog |
|---|---|
| `interface Bus { var vld: logic; modport m { vld: output } }` | `interface Bus; logic vld; modport m(output vld); endinterface` |
| `interface Bus::<W: u32> { ... }` | `interface Bus #(parameter int W = 8); ... endinterface`（SV interface 可參數化，但 tooling 支援不一） |
| `inst b: Bus;` | `Bus b();` |

## generate

| Veryl | SystemVerilog |
|---|---|
| `if COND: u32 == 0 { }`（labelled generate if） | `if (COND == 0) begin : u32 ... end` |
| `for i: u32 in 0..W { }`（generate for） | `for (genvar i = 0; i < W; i++) begin ... end` |

## embed 與外部連接

| Veryl | SystemVerilog |
|---|---|
| `embed (inline) {{ ... }}` | 內容原樣嵌入輸出 SV |
| `embed (cocotb) sv {{ ... }}` 配 `#[test(name)]` | 以 cocotb（Python）做驗證，SV 側為接合程式碼 |
| `$sv::identifier` | 直接引用 SV 識別字（Veryl 內以 `$sv` namespace 表示） |
| 內建函式如 `$clog2(W)` | `$clog2(W)`（系統函式直接沿用） |

## 工具鏈對照

| Veryl | 對標概念 |
|---|---|
| `verylup` | rustup（工具鏈版本管理） |
| `veryl build` / `veryl check` | cargo build / cargo check（check 不產檔，僅檢查） |
| `veryl fmt` | rustfmt |
| `veryl doc` | rustdoc |
| `veryl test` | cargo test |
| `veryl publish` | cargo publish |
| `Veryl.toml`（[project]/[build]/[format]/[test]/[doc]） | Cargo.toml |
