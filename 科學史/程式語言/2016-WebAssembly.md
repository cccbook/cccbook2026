# 2016 WebAssembly：JavaScript 效能天花板之謎

## 案發現場

2013 年，Mozilla 的 Alon Zakai 把一個 C++ 遊戲引擎編譯成 JavaScript（asm.js 專案），在瀏覽器裡跑出了接近原生的效能——但這是硬撐出來的。同一時期，Unity 的開發者抱怨 C# 遊戲編譯到瀏覽器後效能掉了一半以上，AutoCAD、Photoshop 的團隊則根本不敢把核心搬上瀏覽器。

當時的未解之謎：

1. **JavaScript 的效能天花板。** JS 引擎（V8、SpiderMonkey）的 JIT 編譯已經做到極致，但語言本身的動態性是硬傷：型別不確定（`a + b` 可能是數字相加、字串串接或 NaN）、物件形狀多變（hidden class 退化導致去最佳化）、沒有 64 位元整數、GC 停頓不可控。**數值運算與遊戲迴圈的天花板約為原生效能的 50–70%，而且極不穩定。** JIT 的推導瓶頸：引擎必須先「猜」型別、再驗證、猜錯就回退——這個回退（deopt）機制的成本無法根除。
2. **沒有可攜的二進制格式。** 瀏覽器只有一種「程式」：JavaScript 原始碼。C/C++ 的世界有 ELF、PE、Mach-O 等二進制格式，但沒有一種能安全地在瀏覽器沙箱裡執行。asm.js 用「JS 的子集 + 型別標註」硬湊出近似二進制的效能，但解析與驗證依然慢——**瀏覽器需要一種原生支援的二進制格式。**
3. **跨語言的渴望。** 遊戲開發者想用 C++、科學計算想用 Python、系統工程師想用 Rust——而瀏覽器只說一種語言。誰遇到？每一個想把桌面級應用搬上網頁的人。

為何重要？因為瀏覽器已經成為世界上最大的應用平台，而它只有一門語言。2017 年，四大瀏覽器（Chrome、Firefox、Safari、Edge）同時支援 WebAssembly 1.0——這是瀏覽器史上第一次所有廠商一致通過的新標準。

## 偵查過程

WebAssembly（WASM）的推理是一場 VM 技術的「歷史總匯」——它的每個設計決策都能在歷史上找到前身：

**推理一：棧式虛擬機位元組碼。** WASM 是一種棧式虛擬機的指令集，血統直接承襲 [2000-Csharp與DotNet.md](2000-Csharp與DotNet.md) 的 CIL、JVM 位元組碼與更早的 p-code。以兩數相加為例，WASM 的文字格式（WAT）：

```wat
(module
  (func (export "add") (param $a i32) (param $b i32) (result i32)
    local.get $a      ;; 推上堆疊
    local.get $b      ;; 推上堆疊
    i32.add           ;; 彈出兩值相加
  )
)
```

與 CIL 的 `ldc.i4`/`add` 幾乎同構——**VM 時代積累的位元組碼技術，三十年後被瀏覽器完整收割。**

**推理二：靜態型別 + 可驗證性。** WASM 指令帶有明確的型別（`i32`、`i64`、`f32`、`f64`），整個模組在載入時可以在線性時間內完成驗證——這是對 JS「先跑再說」的正面反擊。驗證的核心推導：

$$
\text{linear-time validation} \implies \text{載入即安全，不需 JIT 猜測}
$$

**推理三：沙箱與記憶體模型。** WASM 的記憶體不是任意指標，而是一塊連續的線性記憶體（linear memory），只能透過索引存取：

$$
\text{address} \in [0, \texttt{memory.size}) \quad \text{越界即 trap}
$$

這條規則讓 C++ 的指標被「閹割」成安全的索引——**段錯誤被沙箱邊界攔截，逃不出瀏覽器。** 這與 [2010-Rust.md](2010-Rust.md) 的借用檢查器異曲同工：一個靠型別系統、一個靠沙箱，殊途同歸地消滅了不安全的記憶體存取。

**推理四：二進制 + 文字雙格式。** WASM 有緊湊的二進制格式（.wasm，載入與解析都快）與人類可讀的文字格式（.wat）。二進制格式是給機器的（近似原生效能），文字格式是給人類的（可除錯、可手寫）。

**推理五：從 asm.js 到 WASM 的演進。** Zakai 的 asm.js（2013）證明了「JS 子集 + AOT 編譯」可行；WASM（2016）則是四大瀏覽器聯手，把這條路升級為原生標準。Emscripten 工具鏈讓 C/C++ → JS/WASM 的遷移幾乎自動化。

## 結案報告

WASM 的遺產仍在快速擴張：

1. **瀏覽器裡的第二語言生態。** C/C++（Emscripten）、Rust（wasm-bindgen、wasm-pack）、Go、C#（Blazor）、Python（Pyodide）、Ruby、Kotlin 全部可以編譯到 WASM。**瀏覽器從「JS 獨裁」變成「多語言共享執行環境」**——這正是 CLR 在 2000 年的願景，二十年後在瀏覽器裡實現。
2. **從瀏覽器到通用執行環境。** WASI（WebAssembly System Interface）讓 WASM 跑到瀏覽器之外：伺服器（Fastly 的 compute@edge）、邊緣運算、嵌入式系統、區塊鏈（以太坊的 eWASM 設計）。Docker 創始人 Solomon Hykes 的名言：「如果 WASM + WASI 早在 2008 年就存在，我們根本不需要發明 Docker。」**WASM 正在成為雲端時代的新容器格式。**
3. **效能天花板被打破。** Figma、Photoshop for Web、Google Earth、各種遊戲引擎都在 WASM 上跑出了接近原生的體驗。
4. **影響後續技術**：見 [2020-AI時代的程式語言.md](2020-AI時代的程式語言.md)——WASM 讓 Python 的 ML 生態可以在瀏覽器裡跑（Pyodide + PyTorch 的邊緣化嘗試），也讓「程式碼在哪裡執行」這個問題有了新的答案：**哪裡都可以。**

2016 年的 WASM 用一堆棧式指令與一塊線性記憶體，回答了 JavaScript 的效能天花板之謎——瀏覽器自此有了自己的虛擬機。

## 證據與工具

以下先展示 WAT（WebAssembly 文字格式）的經典範例：

```wat
(module
  ;; 遞迴計算階乘：C 函數的 WASM 化
  (func $fact (export "fact") (param $n i64) (result i64)
    (if (result i64)
      (i64.lt_s (local.get $n) (i64.const 2))
      (then (i64.const 1))
      (else
        (i64.mul
          (local.get $n)
          (call $fact (i64.sub (local.get $n) (i64.const 1)))))))

  ;; 線性記憶體：指標被閹割成索引
  (memory (export "mem") 1)   ;; 1 頁 = 64KB
  (data (i32.const 0) "hello from wasm")
)
```

再用 Python 模擬 WASM 的棧式 VM 執行引擎（驗證 + 執行）：

```python
# 模擬極簡 WASM VM：棧式機 + 型別驗證
TYPE = {"i32.add": ("i32", "i32", "i32"),
        "i64.mul": ("i64", "i64", "i64"),
        "f64.add": ("f64", "f64", "f64")}

def run_wasm(instructions, types={}):
    stack, output = [], []
    for ins in instructions:
        if ins.startswith(("i32.const", "i64.const", "f64.const")):
            kind, val = ins.split()
            stack.append((kind, float(val) if "." in kind else int(val)))
        elif ins in TYPE:                     # 型別驗證：線性時間
            k, ta, tb = TYPE[ins]
            b = stack.pop(); a = stack.pop()
            if a[0] != ta or b[0] != tb:
                raise TypeError(f"type mismatch: {a[0]} {b[0]} for {ins}")
            r = {"add": lambda: a[1] + b[1], "mul": lambda: a[1] * b[1]}[k.split(".")[1]]()
            stack.append((ta, r))
        elif ins == "local.get":
            stack.append(types[ins.split()[1]])
    return stack

# fact(5) 用迴圈展開：5 * 4 * 3 * 2 * 1 的 i64 運算
program = ["i64.const", "5", "i64.const", "4", "i64.mul",
           "i64.const", "3", "i64.mul",
           "i64.const", "2", "i64.mul",
           "i64.const", "1", "i64.mul"]
print(run_wasm(program))  # [('i64', 120)]
```

再模擬 WASM 的線性記憶體沙箱——越界存取被 trap 攔截：

```python
class Trap(Exception): pass

class LinearMemory:
    def __init__(self, pages=1):
        self.size = pages * 65536          # 每頁 64KB
        self.mem = bytearray(self.size)

    def load(self, addr, n=1):
        if addr + n > self.size:           # 沙箱邊界：越界即 trap
            raise Trap(f"out of bounds: load at {addr}")
        return bytes(self.mem[addr:addr+n])

    def store(self, addr, data):
        if addr + len(data) > self.size:
            raise Trap(f"out of bounds: store at {addr}")
        self.mem[addr:addr+len(data)] = data

mem = LinearMemory(pages=1)
mem.store(0, b"hello wasm")
print(mem.load(0, 5))      # b'hello'
try:
    mem.load(65000, 100)   # 越界：C 的段錯誤在這裡被攔截
except Trap as e:
    print("Trap:", e)
```

2016 年的 WebAssembly 用三十年積累的 VM 技術，在瀏覽器裡重建了一個安全的通用執行環境——VM 時代的最後一塊拼圖，就此歸位。
