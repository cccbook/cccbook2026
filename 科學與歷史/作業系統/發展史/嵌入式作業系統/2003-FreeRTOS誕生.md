# 2003 - FreeRTOS 誕生（開放原始碼的即時核心）

## 案件摘要
2003 年，英國工程師 **Richard Barry** 發布 **FreeRTOS**：一個**約 4,000 行 C、MIT 授權**的即時核心。
**史上被下載最多、跑進最多晶片的 RTOS**——2026 年每小時有數以萬計的新裝置啟動它。

## 前因 -- 為什麼會有這個案子
- **商用 RTOS 的授權費**：VxWorks、VRTX 一份授權數萬美元，原始碼封閉——**彌補的缺陷：封閉又昂貴**。
- **微控制器的平民化**：ARM Cortex-M（2004）把 32 位元 MCU 價格拉到一美元級——**硬體平民化逼出軟體平民化**。
- **Barry 的洞察**：嵌入式世界有上千種晶片——**只有開放原始碼 + 極簡可移植層**才能覆蓋這麼多硬體。

## 線索與推理 -- FreeRTOS 的技術面貌（2003）

| 技術 | FreeRTOS 狀態 | 彌補的缺陷 |
|------|---------------|-----------|
| 核心元件 | 任務、佇列、信號量、串流緩衝——**就這樣** | 商用 RTOS 功能臃腫 |
| 可移植層 | `portable/` 每個 CPU 一小撮組語 | 與硬體耦合 |
| footprint | **約 6KB flash / 1KB RAM** 起跳 | 主機 OS 的 1/100000 |
| 授權 | **MIT**（無 copyleft 負擔） | GPL 嚇跑商業廠商 |
| 排班 | 搶佔式 / 協作式 / 時間片皆可設定 | 一刀切的排班策略 |

### C 範例：FreeRTOS 的任務與佇列

```c
/* FreeRTOS：一切圍繞「任務 + 佇列」 */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

QueueHandle_t xQueue;

void vSensorTask(void *pv) {          /* 生產者 */
    for (;;) {
        int sample = read_sensor();
        xQueueSend(xQueue, &sample, portMAX_DELAY);
        vTaskDelay(pdMS_TO_TICKS(10));/* 10ms 週期 */
    }
}

void vLoggerTask(void *pv) {          /* 消費者 */
    int v;
    for (;;) {
        xQueueReceive(xQueue, &v, portMAX_DELAY);
        log(v);
    }
}

int main(void) {
    xQueue = xQueueCreate(8, sizeof(int));
    xTaskCreate(vSensorTask, "sensor", 128, NULL, 2, NULL);
    xTaskCreate(vLoggerTask, "logger", 128, NULL, 1, NULL);
    vTaskStartScheduler();            /* 核心就這麼小 */
    for (;;);
}
```
（**任務 + 佇列 = 嵌入式世界的 fork/exec + pipe**——Unix 抽象的 1KB 版。）

### Shell 範例：交叉編譯與燒錄

```bash
# 交叉編譯 FreeRTOS 專案（Cortex-M）
$ arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -O2 -o app.elf main.c
$ arm-none-eabi-size app.elf
   text    data     bss
   6420      12    1048      # flash 6KB、RAM 1KB——footprint 鐵律
$ openocd -f board/st_nucleo_f4.cfg -c "program app.elf"
```

## 結案 -- 後果與影響
- 2017 年 FreeRTOS 被 **Amazon 併購**，長期安全維護（FreeRTOS LTS）——開源專案的商業庇護模式。
- 徒弟潮：OpenRTOS、SafeRTOS（安全認證版）、各家 CMSIS-RTOS——開源 RTOS 成為主流。
- 物聯網時代：Wi-Fi 模組、藍牙晶片、馬達控制器——**幾乎每顆聯網 MCU 都有一份 FreeRTOS**。
- 歷史教訓：**MIT 授權 + 極簡 + 跨硬體 = 滲透率最高的核心**（與 Linux GPL 路線形成對照組）。

## 關鍵人物與文獻
- **R. Barry**：FreeRTOS (2003)；《Using the FreeRTOS Real Time Kernel》。
- **Amazon / AWS**：FreeRTOS LTS (2017)。
- 相關案件：`1993-VxWorks與POSIX即時標準.md`、`2015-Zephyr與物聯網.md`、`../UNIX/2013-Docker容器.md`。
