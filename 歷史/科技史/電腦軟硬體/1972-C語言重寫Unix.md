# 1972-C語言重寫Unix：一場異端的可攜性革命

## 案件摘要
1972 年，貝爾實驗室的 Dennis Ritchie 做了一件當時被視為異端的事：用高階語言 C 重寫作業系統 Unix。當時的教科書都說 OS 必須用組合語言寫——Ritchie 證明他們錯了，並讓 Unix 從此獲得「可移植」的生命。

## 前因 -- 為什麼會有這個案子
- **Unix 的誕生**：1969 年 Ken Thompson 在貝爾實驗室的廢棄 PDP-7 上寫出第一版 Unix（組合語言）。1971 年移植到 PDP-11，但仍受制於組語——換一種 CPU 就要全部重寫。
- **當時的教條**：1970 年代主流觀點認為作業系統必須手寫組合語言，因為需要精確控制暫存器、記憶體位址與硬體中斷。高階語言（如 FORTRAN）的執行效率與底層控制被認為不足以勝任。
- **BCPL 與 B 語言的伏筆**：Thompson 先以 Martin Richards 的 BCPL 為本簡化出 B 語言（無型別、直譯式）嘗試重寫 OS，但 B 的效率不足（word-addressed、無 byte 型別）。Ritchie 在 1971–72 年間為 B 加入型別（int、char、指標）、編譯成機器碼，誕生 **New B → C 語言**。
- **PDP-11 的硬體特性**：PDP-11 有 byte 定址、豐富的定址模式，剛好適合 C 的指標語意——硬體與語言在此刻天作之合。

## 線索與推理 -- 數學式、程式、理論

### 為何用高階語言寫 OS 是異端
當時的反對理由：OS 需要 (1) 精確的記憶體位址操作、(2) 中斷處理、(3) 極致效能。Ritchie 的解法是讓 C 同時具備三者：
- **指標**：C 的指標就是位址，`*p` 直接對映記憶體操作，可寫裝置驅動器
- **低階存取**：可內嵌組語（inline asm）處理極少數無法表達的指令
- **接近組語的效能**：C 的設計原則是「每個語言結構對應極少量機器指令」，編譯器不隱藏成本

### C 與組合語言的對照範例

以「複製字串」為例：

```asm
; PDP-11 組合語言版本
        MOV   #SRC, R1     ; R1 = 來源位址
        MOV   #DST, R2     ; R2 = 目的位址
LOOP:   MOVB  (R1)+, (R2)+ ; 位元組複製，指標遞增
        BNE   LOOP          ; 非零則繼續
        HALT
```

```c
/* C 語言版本（可移植到任何 CPU） */
void strcpy(char *dst, const char *src) {
    while ((*dst++ = *src++))
        ;                      /* 複製直到 '\0' */
}
```

兩者幾乎一一對應，但 C 版可編譯到 PDP-11、VAX、任何機器。**效能犧牲趨近於零，可移植性獲得無限大**——這正是這場革命的本質：

$$\text{Value} = \frac{\text{Portability} \to \infty}{\text{Performance loss} \to 0}$$

### Portability 的革命
- **1972–73**：Ritchie 重寫 Unix 核心，1973 年第四版 Unix 已有 95% 以上是 C（僅少數底層仍是組語）。
- **1977–78**：Unix 首度移植到 Interdata 8/32，證明「一次編寫、處處執行」。隨後移植到 VAX，誕生 32-bit 的 **32V**，成為 BSD 系的祖先。
- 可移植性的數學意義：若 OS 有 $n$ 個模組、面對 $m$ 種 CPU：

$$\text{組語成本} = n \times m, \quad \text{C 成本} = n + m \quad (\text{只需 } m \text{ 個編譯器})$$

從乘法到加法——這是軟體工程的線性化革命，與分封交換之於通訊、PageRank 之於搜尋同構。

### C 編譯器作為系統軟體基石
C 編譯器本身也是「自我編譯」（self-hosting）：用 C 寫 C 編譯器，然後用舊編譯器編譯新編譯器。這個自舉（bootstrapping）過程：

```
舊編譯器 (C) → 編譯新編譯器原始碼 (C) → 新編譯器
     ↑                                    │
     └────────── 自舉閉環 ←───────────────┘
```

C 編譯器從此成為每個新平台的「第一塊基石」：先移植 C 編譯器，整個 Unix 生態（shell、工具鏈、應用）就能跟著移植。

### Unix + C 的共生體系
語言、shell、工具鏈構成三位一體：

| 層 | 元件 | 語言 |
|----|------|------|
| 核心（kernel） | 行程、記憶體、檔案系統 | C（+少量組語） |
| Shell | 命令解譯、管線 | C |
| 工具鏈 | compiler（cc）、grep、awk、sed | C |
| 應用 | ed、vi、一切 | C |

Unix 哲學「小工具組合」用管線實現：

```bash
$ cat access.log | grep "404" | awk '{print $1}' | sort | uniq -c | sort -rn
```

每個工具只做一件事、以純文字流（stdin/stdout）介接——這種「組合式設計」影響了後世所有軟體架構，從 Unix 管線到函數式程式設計的資料流皆然。

## 結案 -- 後果與影響
- **Unix 家族開枝散葉**：BSD、System V、SunOS、AIX、HP-UX 皆為 C 重寫 Unix 的子孫；1978 年《The C Programming Language》（K&R）出版，C 成為系統程式設計的標準語言。
- **1983 年 ANSI C 標準化**、1989 年 C89 標準發布，C 成為跨平台的事實標準。
- **對現代 OS 的直接影響**：
  - **Linux 核心**：以 C 語言寫成（GCC 編譯），是 Unix 可攜革命的直系繼承者
  - **macOS**：核心 XNU 為 Mach（C）+ BSD（C）混合
  - **Windows NT 核心**：Dave Cutler 團隊以 C 語言開發，可移植到 x86、Alpha、MIPS
- 幾乎所有現代語言的直譯器與編譯器（Python、Ruby、Go、Rust 的初期工具鏈）皆以 C 實作——C 是「語言之母」。
- Ritchie 於 1983 年與 Thompson 同獲圖靈獎，表彰 Unix 與 C 對系統軟體的奠基貢獻。

## 關鍵人物與文獻
- **Dennis Ritchie**：〈The Development of the C Language〉（1993）、C 語言之父
- **Ken Thompson**：Unix 原創者、B 語言、UTF-8（晚期貢獻）
- **Brian Kernighan & Dennis Ritchie**：《The C Programming Language》（1978，K&R）
- **Martin Richards**：BCPL（1966）——C 的祖父
- **AT&T 貝爾實驗室**：1956 反壟斷協定無意間促成 Unix 原始碼流向學術界
