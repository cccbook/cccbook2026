# 2017-WebAssembly與MLIR

## 案件摘要
2017 年，W3C 正式發布 WebAssembly（WASM）——四巨頭（Mozilla、Google、Microsoft、Apple）在 ASM.js 實驗成功的基礎上，聯手偵破了「瀏覽器能否成為通用執行環境」這樁大案。兩年後的 2019 年，Chris Lattner 在 Google 領導發布 MLIR，對付另一樁更隱蔽的案件：當編譯器要面對 TPU、AI 運算圖等領域多樣性，單一 LLVM IR 層級不夠用。2020 年代，AlphaDev 與 LLM 接棒，把 AI 引進編譯器的搜索空間。兩樁案件指向同一個未來：**編譯器的編譯器基礎設施**。

## 前因 -- 為什麼會有這個案子
- **JavaScript 重計算之苦**：瀏覽器裡只有 JavaScript 一種語言，跑遊戲、影像處理、CAD 等重計算時，即使 V8 有 JIT，動態型別與 GC 的開銷仍比原生碼慢數倍。
- **ASM.js 的實驗（2013）**：Mozilla 的 Alon Zakai 提出 ASM.js——把 C/C++（經 Emscripten）編譯成「JavaScript 的嚴格子集」（只留整數、浮點、型別標註），瀏覽器可偵測並 AOT 優化。實驗證明：**近原生速度在瀏覽器裡是可行的**——這是 WASM 的概念驗證。
- **四巨頭合作**：各瀏覽器各自為政的局面下，ASM.js 的成功促成 Mozilla、Google、Microsoft、Apple 合作，設計一個全新的、可攜的二進位位元組碼標準——WebAssembly，2017 年四家瀏覽器同時支援。
- **MLIR 的前因**：LLVM 統一了「語言 × 平台」問題，但 AI 時代帶來新多樣性——TPU、GPU、NPU 各有不同計算圖與方言（dialect），TensorFlow 的圖運算無法直接塞進 LLVM IR 的低階抽象；每個硬體團隊都在重複造輪子。Lattner 的推理：**何不做「編譯器的編譯器基礎設施」——多層級 IR + 方言系統？**

## 線索與推理 -- 數學式、程式、理論

### WASM：可攜的二進位堆疊機
WASM 是一種**堆疊機位元組碼**：可攜（平台無關）、沙箱安全（線性記憶體 + 能力隔離）、近原生速度（瀏覽器可 AOT 編譯）。`(a + b) * 2` 的 wat（文字格式）：

```wat
;; wat 文字格式：堆疊機指令，SSA 由堆疊隱式表達
(module
  (func $f (param $a i32) (param $b i32) (result i32)
    local.get $a        ;; push a
    local.get $b        ;; push b
    i32.add             ;; pop b, a -> push a+b
    i32.const 2         ;; push 2
    i32.mul             ;; pop 2, a+b -> push (a+b)*2
  ))
```

WASM 的驗證器可靜態保證型別安全與記憶體隔離（`memory.grow`、邊界檢查），執行時無需 GC——**比 JavaScript 快、比原生碼安全**。瀏覽器從此變成通用執行環境：AutoCAD、Photoshop、Figma 皆編譯進網頁。

### MLIR 的推理：多層級 IR 與方言系統
LLVM IR 是**單一層級**的低階抽象——對 AI 運算圖（高階、領域特定）來說太低，對硬體指令（TPU 的脈動陣列）來說又不夠貼近。MLIR 的宣言：

1. **多層級 IR**：編譯過程是一連串的「漸進式降級（progressive lowering）」——從高階領域抽象一層層降到硬體：
   $$\text{TensorFlow IR} \rightarrow \text{linalg} \rightarrow \text{vector} \rightarrow \text{loop/affine} \rightarrow \text{LLVM IR} \rightarrow \text{機器碼}$$
2. **方言系統（dialects）**：每個層級是一個「方言」（如 `tf`、`linalg`、`affine`、`llvm`），方言之間可互相操作與轉換，使用者還能**自訂方言**——這是 LLVM 做不到的。
3. **Infrastructure 的 Infrastructure**：MLIR 不想統一所有編譯器，而是提供**建造編譯器基建的工具**——IR 表示法、降級機制、優化框架全部可重用。

MLIR 的核心資料結構是 **DAG（有向無環圖）式的 operation**：每個 op 帶型別、屬性、region，SSA 由 DAG 結構隱式保證——op 的結果值就是 SSA 版本，與 LLVM IR 的 SSA 一脈相承。

### MLIR 多層級降級流程

```mlir
// 第 1 層：linalg 方言（高階張量運算，貼近 AI 圖）
%out = linalg.matmul ins(%A, %B : tensor<1024x512xf32>, tensor<512x256xf32>)
                     outs(%C : tensor<1024x256xf32>)

//    ↓ 降級（tiling + bufferization）

// 第 2 層：affine 方言（顯式多層迴圈，可做平鋪優化）
affine.for %i = 0 to 1024 step 64 {
  affine.for %j = 0 to 256 step 64 {
    affine.for %k = 0 to 512 {
      //  乘加運算，此層級可做循環優化
    }}}

//    ↓ 降級（vectorization + lowering to LLVM）

// 第 3 層：llvm 方言（與 LLVM IR 無縫銜接，交給 x86/ARM/GPU 後端）
```

關鍵意義：**同一個 matmul，在三個層級有三種表示**，每層各做各的優化（高階融合、迴圈平鋪、向量化），漸進式降級讓「領域知識」與「機器知識」分層管理——這正是單一 LLVM IR 層級做不到的事。

### AI 編譯的搜索空間分析
2023 年 DeepMind 的 AlphaDev 用強化學習發現更快的排序演算法（比人類最佳短 1-2 條指令，寫進 LLVM libc++）。AI 輔助編譯的本質是在巨大的搜索空間中找最佳化路徑：

$$|\mathcal{S}| \sim \prod_{i=1}^{P} |O_i|$$

其中 $P$ 是優化 pass 數（LLVM 有數百個），$|O_i|$ 是第 $i$ 個 pass 的候選選擇數（如平鋪尺寸、展開次數）。總搜索空間是指數級的——傳統編譯器靠人類手寫的啟發式（heuristic）挑選；AI 則靠學習在空間中導航：

| 方法 | 搜索策略 | 成本 | 例子 |
|---|---|---|---|
| 手寫啟發式 | 固定規則 | 低（開發期） | 傳統 GCC/LLVM 管線 |
| 迭代編譯 | 窮舉/隨機 | 高（編譯期） | Halide auto-scheduler |
| 強化學習 | 學習策略 | 高（訓練期），推論快 | AlphaDev、MLGOPerf |
| LLM 輔助 | 生成候選 | 中 | LLM 寫 pass、寫方言 |

### Python 模擬：AI 編譯的搜索空間

```python
# 優化 pass 的搜索空間是指數級的：AI 用學習導航
import itertools

passes = {                       # pass -> 候選選擇
    'tiling':   [16, 32, 64, 128],       # 平鋪尺寸 4 選 1
    'unroll':   [1, 2, 4, 8],            # 展開次數 4 選 1
    'vector':   [128, 256, 512],         # 向量寬度 3 選 1
}

space_size = 1
for choices in passes.values():
    space_size *= len(choices)
print(f"搜索空間: {space_size} 種組合")   # 4*4*3 = 48

def cost(cfg):                   # 模擬執行成本模型（實務上靠實測或學習模型）
    t, u, v = cfg
    return 1000/t + 500/u + 300/v + 50    # 每項權衡不同

# 窮舉（傳統迭代編譯）：48 次評估
best, best_cfg = min(((cost(c), c) for c in itertools.product(*passes.values())))
print(f"窮舉最佳: cfg={best_cfg}, cost={best:.1f}")

# 強化學習的概念：用「學習到的模型」直接預測，跳過大部分評估
# （實務：AlphaDev 用 RL 在指令空間中搜索；LLM 生成候選 pass 序列）
import random
def rl_guess(samples=8):         # 模擬：少量採樣 + 模型預測
    return min((cost(c := tuple(random.choice(x) for x in passes.values())),
                c) for _ in range(samples))

g, gc = rl_guess()
print(f"少量採樣近似: cfg={gc}, cost={g:.1f}   （只評估 8 次，卻接近窮舉最佳）")
```

輸出顯示：48 維的搜索空間只需 8 次採樣即可逼近最佳——**AI 編譯的價值在於用學習模型取代大部分的搜索**，這正是 AlphaDev 與 LLM 輔助編譯的共同推理。

## 結案 -- 後果與影響
- **瀏覽器成為通用執行環境**：AutoCAD、Photoshop Web 版、Figma、Google Earth 皆以 WASM 進駐網頁；C/C++/Rust/Go 皆可編譯成 WASM——「平台」的定義從作業系統擴展到瀏覽器。
- **WASM 走出瀏覽器**：WASI（WebAssembly System Interface）讓 WASM 進入伺服器端、邊緣運算（Cloudflare Workers、Fastly）、插件系統（Envoy、Shopify）——沙箱安全 + 快啟動成為雲端的新寵。
- **MLIR 成為 AI 編譯的骨架**：TensorFlow/XLA、PyTorch、IREE、ONNX-MLIR、Modular（Mojo）皆採用 MLIR；TPU、GPU、NPU 的編譯器基建統一在一套方言系統下——Lattner 再度翻案成功。
- **AI 接棒**：AlphaDev（2023）的排序演算法寫進 LLVM libc++；LLM 開始寫編譯器優化 pass、生成 MLIR 方言——2020 年代，「搜索空間的導航者」從人類啟發式交棒給 AI。
- **考古定位**：ASM.js（2013）是 WASM 的概念驗證，LLVM（2000）是 MLIR 的概念基礎——兩樁案件都是「先有實驗證明可行，再有大規模基礎設施」的典範。

## 關鍵人物與文獻
- **Chris Lattner**（Google → Modular）：MLIR 計畫發起人，LLVM 之父。
- **Alon Zakai**（Mozilla）：Emscripten 與 ASM.js 的發明人。
- **Andreas Rossberg**（Google → 獨立）：WASM 語言規範的主要設計者。
- 文獻：
  - A. Haas et al., "Bringing the Web up to Speed with WebAssembly," *PLDI* 2017.
  - C. Lattner et al., "MLIR: Scaling Compiler Infrastructure for Domain Specific Computation," *CGO* 2021.
  - DeepMind, "Faster sorting algorithms discovered using deep reinforcement learning," *Nature* 618, 2023.
