# 2015 - Zephyr 與物聯網（嵌入式版的發行版）

## 案件摘要
2015 年，**Intel** 發起、**Linux 基金會**庇護的 **Zephyr Project** 發布——
Apache 2.0 授權的物聯網即時 OS：借用 **Linux 的設備樹（devicetree）與 Kconfig**，
把「每張板子一份硬編碼」的嵌入世界，升級成**宣告式硬體描述 + 組態裁剪**的發行版模式。

## 前因 -- 為什麼會有這個案子
- **板子硬編碼的缺陷**：傳統嵌入式每換一張板就改一份 `board.h`——數千張板 = 數千份分岔——**彌補的缺陷：硬體描述碎片化**。
- **物聯網的硬體契機**：低功耗 BLE、LoRa、802.15.4 晶片爆發——需要**安全更新、連線協定堆疊、多硬體支援**的 OS。
- **Linux 生態的拼圖**：Kconfig（1990s）、devicetree（2005 進主線）都是現成理論——Zephyr **把 Linux 的組態工程移植到 MCU**。

## 線索與推理 -- Zephyr 的技術面貌（2015）

| 技術 | Zephyr 狀態 | 彌補的缺陷 |
|------|-------------|-----------|
| **devicetree** | 宣告式硬體描述（DTS 編譯期展開） | 每張板一份 board.h |
| **Kconfig** | 組態空間裁剪（數千個選項） | 一刀切的功能組合 |
| **footprint** | 最小組態 **約 8KB flash** | 物聯網 MCU 資源受限 |
| **安全更新** | MCUboot（2017）+ 簽章驗證 | 無 OTA 的裝置被駭 |
| **通訊** | BLE、802.15.4、CoAP、LwM2M | 協定堆疊自己拼湊 |

### 設備樹範例：宣告式硬體描述

```dts
/* board.dts：硬體用宣告描述，不用改 C 碼 */
/ {
    leds {
        led0: led_0 {
            gpios = <&gpio0 13 GPIO_ACTIVE_LOW>;
        };
    };
    uart0: uart@40002000 {
        current-speed = <115200>;
        status = "okay";
    };
};
```
（**devicetree 來自 Linux（2005）**——資料與程式分離，嵌入式版的「一切皆檔案」。）

### Shell 範例：Kconfig 的組態裁剪

```bash
# west：Zephyr 的「apt + repo」混合工具（2018）
$ west init -p zephyr && west update
$ west build -b nucleo_f401re samples/hello_world
$ west build -t menuconfig        # 數千個組態選項，裁出 8KB 核心
$ west flash
$ west build -t rom_report        # footprint 報告——footprint 是生存條件
```

### C 範例：Zephyr 的執行緒

```c
#include <zephyr/kernel.h>

K_THREAD_DEFINE(sensor, 512, sensor_fn, NULL, NULL, NULL,
                2, 0, 0);            /* 編譯期宣告執行緒 */

void sensor_fn(void) {
    const struct gpio_dt_spec led =
        GPIO_DT_SPEC_GET(DT_NODELABEL(led0), gpios);
    gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
    for (;;) {
        gpio_pin_toggle_dt(&led);    /* 硬體來自 devicetree */
        k_sleep(K_MSEC(500));
    }
}
```

## 結案 -- 後果與影響
- 數百家會員（Nordic、NXP、TI...）共建——**嵌入式界的 Linux 基金會模式**。
- MCUboot、TF-M（Trusted Firmware-M）成為物聯網安全更新的事實標準。
- 2020 年代：藍牙耳機、智慧錶、感測器節點——Zephyr 成為 FreeRTOS 之外的最大開源選項。
- 歷史教訓：**宣告式硬體描述 + 組態裁剪 + 社群發行版 = 把 Linux 工程紀律搬進 MCU**。

## 關鍵人物與文獻
- **Intel / Linux 基金會**：Zephyr Project (2015)。
- **G. Kroah-Hartman**：devicetree 生態（Linux 主線，2005）。
- 相關案件：`2003-FreeRTOS誕生.md`、`../UNIX/1993-發行版與FreeBSD誕生.md`、`2020-Rust嵌入式與RTIC.md`。
