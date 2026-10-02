# 1995-Java與JIT

## 案件摘要
1995 年，James Gosling 在 Sun Microsystems 發表 Java，喊出「一次編譯、到處執行」——程式先編成 bytecode，交給 JVM 執行。但早期 JVM 純直譯太慢，「Java 太慢」的罵名如影隨形。1998-1999 年 HotSpot 靠「先直譯觀察、再投機編譯、錯了就退回」的 JIT 三部曲徹底翻案：靜態編譯永遠看不到的執行期資訊，直譯器卻免費擁有。這樁案件的偵破，讓後來所有動態語言（JavaScript V8、PyPy）全部受益。

## 前因 -- 為什麼會有這個案子
- **C++ 指標之苦**：Gosling 設計 Java 的原始目標是嵌入式系統（代號 Oak），C++ 的手動記憶體管理與指標運算在嵌入式環境是災難——懸空指標、記憶體洩漏、非法越界，Java 以垃圾回收（GC）+ 無指標設計根治。
- **異質平台之苦**：1990s 個人電腦平台林立（Windows、Mac、Solaris、各種嵌入式晶片），C/C++ 必須「每個平台重編一次」。Java 的解法是**位元組碼（bytecode）+ 虛擬機**：編譯一次成平台無關的 bytecode，各平台只要有 JVM 就能執行。
- **純直譯的瓶頸**：早期 JVM 逐條直譯 bytecode，每條指令都有「取指、解碼、分派」的直譯器開銷，比原生編譯碼慢 10-20 倍。「Java 太慢」成為整個 1990s 的標籤。
- **前人的線索**：動態翻譯技術早已存在——Deutsch 與 Schiffman 1984 年為 Smalltalk-80 做出「執行期把 bytecode 快取成機器碼」的動態翻譯；1991 年的 Self 語言發展出型別回饋（type feedback）、內聯快取與去優化。HotSpot 團隊（Lars Bak 等來自 Self 專案）把這些技術帶進 Java。

## 線索與推理 -- 數學式、程式、理論

### bytecode 與堆疊機
JVM 是一台**堆疊機（stack machine）**：指令從運算元堆疊取值，結果推回堆疊。`x = a + b * c` 編譯成：

```
iload_1      // push a          （a 在區域變數槽 1）
iload_2      // push b
imul         // pop b, c -> push b*c
iadd         // pop b*c, a -> push a + b*c
istore_0     // pop -> x        （存入區域變數槽 0）
```

堆疊機的指令碼短（不需要指定位址欄位），適合網路傳輸與驗證（JVM 的 bytecode verifier 可靜態檢查型別安全），但直譯時每條指令都有分派開銷：

$$T_{interp} = N_{instr} \times (t_{fetch} + t_{decode} + t_{dispatch} + t_{exec})$$

其中 $t_{dispatch}$ 往往比 $t_{exec}$ 還大——這就是純直譯慢的數學根源。

### 核心推理：直譯器免費擁有的情報
靜態編譯器（C/C++）在編譯期只能看到原始碼，看不到執行期事實：
- **實際型別**：虛擬呼叫 `obj.f()` 在編譯期不知道 `obj` 的真實型別，只能做間接呼叫。
- **熱點**：哪個方法、哪個迴圈真的被執行一億次？靜態編譯器只能賭。

但直譯器在執行時**免費擁有**這些資訊——它親眼看到每個物件的型別、每個分支的走向。HotSpot 的推理：**何不先直譯來觀察，收集 profile，再對熱點做投機性編譯？**而且投機是可逆的：若假設（如「這個呼叫點只出現過型別 A」）被違反，就**去優化（deoptimization）**退回直譯器重新觀察。這個「觀察 → 投機 → 退回」的閉環，是靜態編譯永遠做不到的。

### 熱點偵測的計數器模型
HotSpot 以方法呼叫計數器與回邊計數器偵測熱點。方法 $m$ 的觸發條件：

$$C_{invoke}(m) + C_{backedge}(m) \geq \Theta$$

其中 $\Theta$ 是編譯門檻（client 模式約 1500，server 模式約 10000）。計數器每到達門檻，方法進入編譯佇列，由背景執行緒編譯——**編譯不阻塞執行**。OSR（On-Stack Replacement）則讓「正在執行的長迴圈」也能中途換成編譯後版本。

### 編譯層級對照表

| 層級 | 系統 | 技術 | 特點 |
|---|---|---|---|
| Smalltalk-80 (1984) | Deutsch & Schiffman | 動態翻譯快取 | bytecode → 機器碼快取，首創 |
| Self (1991) | Chambers/Ungar | 型別回饋、內聯快取、去優化 | 動態優化全套技術誕生 |
| HotSpot Client (1998) | Sun | 方法級 JIT | 快啟動、基本優化 |
| HotSpot Server (1999) | Sun | profile 導向 + SSA 海圖 | 積極內聯、投機優化 |
| V8 (2008→) | Google | 直譯(Ignition)→SparkJS→TurboFan | 多層 JIT，JS 提速 |
| PyPy (2007→) | Python 社群 | 追蹤 JIT（tracing JIT） | 對熱迴圈做線性軌跡編譯 |

### 簡易 JIT 概念：動態生成專用函數
JIT 的本質是「根據執行期資訊，動態生成更專用的程式碼」。Python 可以用 `exec` 模擬這個概念——把通用直譯換成「展開、特化」後的專用碼：

```python
# 熱點偵測 + 投機性特化：模擬 JIT 的核心閉環
def interp_loop(a, n):          # 「直譯器」：通用但慢
    s = 0
    for _ in range(n):
        s = s + a * 2           # 每圈都重複解譯乘法
    return s

# 「profile」：觀察後發現 a 是常數 3、n 是常數 1000000
# 「投機編譯」：動態生成特化程式碼（強度削減 + 展開）
def specialize(const_a, const_n):
    code = f"""
def fast():
    s = 0
    for _ in range({const_n}):
        s += {const_a * 2}      # a*2 已在編譯期算成常數
    return s
"""
    ns = {}
    exec(code, ns)              # 動態「編譯」出專用函數
    return ns['fast']

fast = specialize(3, 1_000_000)
assert fast() == interp_loop(3, 1_000_000)   # 語意不變

import timeit
t1 = timeit.timeit(lambda: interp_loop(3, 1_000_000), number=10)
t2 = timeit.timeit(fast, number=10)
print(f"通用直譯: {t1:.3f}s   特化碼: {t2:.3f}s   提速: {t1/t2:.1f}x")
```

`specialize` 就是 JIT 的縮影：**執行期根據觀察到的常數，生成把常數摺疊進去的專用碼**——HotSpot 對 `a*2` 做強度削減（shift）、V8 對單型別呼叫點做直呼（devirtualization），都是同一個推理。

## 結案 -- 後果與影響
- **Java 翻案**：HotSpot 讓 Java 效能逼近 C++，「Java 太慢」罵名消失；Java 成為企業級後端（銀行、電商）的統治語言，JVM 生態（Scala、Kotlin、Clojure）隨之繁榮。
- **動態語言全面受益**：V8（2008）讓 JavaScript 從玩具變成瀏覽器與 Node.js 的核心；PyPy、LuaJIT、Ruby YARV——所有動態語言的 VM 都採用了「剖析 + 投機編譯 + 去優化」的 HotSpot 模式。
- **架構遺產**：去優化（deoptimization）成為動態語言 VM 的必備機制；分層 JIT（直譯 → C1 → C2）成為標準設計；GraalVM 更把 JVM 本身變成多語言執行平台。
- **考古定位**：Deutsch & Schiffman (1984) 與 Self (1991) 是這樁案件的真正線索來源——Java 是把動態翻譯技術帶給大眾的那個「工程實現」。

## 關鍵人物與文獻
- **James Gosling**（Sun）：Java 語言之父（Oak → Java, 1995）。
- **Lars Bak、Urs Hölzle、David Ungar**：Self 專案 → HotSpot 團隊，動態優化技術的推手。
- 文獻：
  - L. P. Deutsch, A. M. Schiffman, "Efficient Implementation of the Smalltalk-80 System," *POPL* 1984.
  - U. Hölzle, C. Chambers, D. Ungar, "Optimizing Dynamically-Typed Object-Oriented Languages with Polymorphic Inline Caches," *ECOOP* 1991.
  - T. Lindholm et al., *The Java Virtual Machine Specification*, 1996.
  - J. Gosling et al., *The Java Language Specification*, 1996.
