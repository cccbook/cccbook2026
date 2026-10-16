# 2020 - Rust 嵌入式與 RTIC（記憶體安全進入 1KB 核心）

## 案件摘要
2020 年前後，**Rust 嵌入式生態**（embedded-hal、cortex-m-rt、RTIC）成熟——
在**沒有堆積、沒有 MMU 的微控制器**上，用**所有權型別系統**做到：
指標漏洞編譯期擋下、中斷與主迴圈的資料競爭**編譯期驗證**。
**嵌入式從「C 的 40 年指標漏洞時代」走進記憶體安全時代。**

## 前因 -- 為什麼會有這個案子
- **C 指標漏洞的代價**：CVE 年報中**約七成是記憶體安全問題**——嵌入式裝置無防護、修補困難——**彌補的缺陷：指標漏洞**。
- **中斷資料競爭**：主迴圈與 ISR 共用變數靠 `volatile` 與經驗——競態是隱形炸彈——**彌補的缺陷：執行期才炸**。
- **RTIC 的洞察**：Rust 的借用檢查天生就是「**互斥**」——硬體優先級 × 型別系統 = **編譯期排班驗證**。

## 線索與推理 -- 技術面貌（2020）

| 技術 | 狀態 | 彌補的缺陷 |
|------|------|-----------|
| **embedded-hal** | 硬體抽象 trait（GPIO/SPI/I2C） | 驅動與晶片耦合 |
| **cortex-m-rt** | no_std 啟動、無堆積 | 嵌入式沒有動態記憶體 |
| **RTIC** | 中斷驅動並行框架：借用檢查 = 互斥 | volatile + 經驗的競態 |
| **MFCC 統計** | Rust 程式碼 CVE 密度低一個量級 | C 指標漏洞 |
| **footprint** | no_std 二進位可小到數 KB | 嵌入式資源受限 |

### C 範例：volatile 與競態——隱形炸彈

```c
/* C：主迴圈與 ISR 共用變數——編譯器不會檢查競態 */
volatile int shared;

void EXTI0_IRQHandler(void) {   /* ISR */
    shared = read_sensor();
}

int main(void) {
    for (;;) {
        int x = shared;         /* 競態：讀到一半被 ISR 打斷？
                                   32 位元以下還好，64 位元就炸 */
        use(x);
    }
}
```

### Rust 範例：RTIC——借用檢查就是互斥

```rust
/* RTIC：編譯期保證 shared 永遠不會同時被兩個上下文碰到 */
#![no_std]
#![no_main]

#[rtic::app(device = stm32f4)]
mod app {
    use stm32f4xx_hal::prelude::*;

    #[shared]
    struct Shared {                 /* 高優先級才能碰的資源 */
        sensor: Sensor,
    }

    #[local]
    struct Local { led: LedPin }

    #[init]
    fn init(ctx: init::Context) -> (Shared, Local, ...) {
        /* 硬體設定、啟動排班 */
    }

    #[task(binds = EXTI0, priority = 2, shared = [sensor])]
    fn sensor_isr(ctx: sensor_isr::Context) {  /* ISR 拿借用 */
        let sample = ctx.shared.sensor.read();
    }

    #[task(priority = 1, shared = [sensor])]
    fn logger(ctx: logger_task::Context) {
        /* 若這裡不安全的借用 sensor，編譯直接失敗
           => 競態在編譯期擋下，不在執行期爆炸 */
    }
}
```
（**優先級 × 所有權 = 編譯期優先級繼承**——1993 年火星車教訓的最終解。）

### Shell 範例：無堆積的 footprint

```bash
$ cargo build --release        # no_std：沒有 std，沒有堆積
$ cargo size --release -- -A
  text    data     bss
  7216       0     380         # 數 KB——記憶體安全零 footprint 額外成本
$ probe-run --chip STM32F401RE target/thumbv7em-none-eabihf/release/app
  (Running with code reset and set to App)
```

## 結案 -- 後果與影響
- 2021 年起 Linux 核心**接受 Rust 子系統**——記憶體安全語言進入巨核心；嵌入式早一步在 RTIC 落地。
- 工業界採用：汽車（安全關鍵）、航太（NASA/SpaceX 內部工具）、IoT 韌體——C 的壟斷被打破。
- 2024 年美國政府報告（CISA）明示**新專案應使用記憶體安全語言**——CVE 統計變成政策。
- 歷史教訓：**把執行期問題搬進編譯期 = 安全革命**（與 WAL 把當機恢復搬進日誌、systemd 把啟動搬進依賴圖同一句法）。

## 關鍵人物與文獻
- **J. Aparicio**：embedded-hal 與 cortex-m 生態 (2017–)。
- **J. Munns et al.**：RTIC 框架 (2019–)。
- **CISA**：Products Should Unravel Memory Safety (2024)。
- 相關案件：`2015-Zephyr與物聯網.md`、`1993-VxWorks與POSIX即時標準.md`、`../Linux/2007-CFS排班與2.6.23.md`。
