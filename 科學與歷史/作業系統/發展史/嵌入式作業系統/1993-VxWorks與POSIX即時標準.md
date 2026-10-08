# 1993 - VxWorks 與 POSIX 即時標準（火星車的心臟）

## 案件摘要
1993 年，IEEE 發布 **POSIX 1003.1b**（即時擴充）：優先級搶佔排班、優先級繼承信號量、即時信號成為標準。
同年 **Wind River** 的 **VxWorks 5.x** 全面實現這些標準——
**API 碎片化的 RTOS 戰國被標準統一**；VxWorks 更成為 **Sojourner 火星探測車（1997）** 的心臟。

## 前因 -- 為什麼會有這個案子
- **RTOS 的 API 戰國**：VRTX、pSOS、iRMX 各家一套 API——換硬體就重寫——**彌補的缺陷：碎片化**。
- **優先級反轉的理論武器**：1990 年 **Lui Sha / Rajkumar / Lehoczky** 的優先級繼承協定理論成熟——即時排班從經驗變成科學。
- **Mars Pathfinder 的硬體契機**：JPL 需要一個能跑在 RAD750 前身晶片上、**可驗證決定性**的 OS——VxWorks 補上這塊。

## 線索與推理 -- 技術面貌（1993）

| 技術 | 狀態 | 彌補的缺陷 |
|------|------|-----------|
| **POSIX.1b 即時排班** | `SCHED_FIFO` / `SCHED_RR` | 各家 RTOS API 不同 |
| **優先級繼承信號量** | `PTHREAD_PRIO_INHERIT` | 優先級反轉（火車事件的前科） |
| **即時信號** | `SIGRTMIN` 可排隊 | 傳統信號不排隊、會丟失 |
| **微秒級延遲** | 中斷延遲可測可驗證 | Linux 排班不確定性 |
| **交叉開發** | Tornado IDE（1995）+ 目標機 agent | printf 除錯時代結束 |

### C 範例：優先級繼承——火星車事件的重演與修正

```c
/* POSIX.1b：優先級繼承信號量（1997 火星車當機的修正） */
#include <pthread.h>

pthread_mutexattr_t attr;
pthread_mutexattr_init(&attr);
/* 沒有這行的話：低優先級任務拿著鎖，
   高優先級任務等鎖，中間優先級任務搶跑
   => 高優先級被無限期延遲 => 看門狗重置（火星車事件） */
pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT);
pthread_mutex_init(&bus_mutex, &attr);
```

### Shell 範例：VxWorks 的即時性驗證

```bash
# 在目標機 shell 上量中斷延遲——決定性是可驗證的
-> priorityTest()         # 排班測試
-> intLatencyShow()
  max latency: 12 us      # 最壞情況可計算——即時的本質
-> taskIdList()           # 任務即行程
```

## 結案 -- 後果與影響
- 1997 年 Mars Pathfinder 的**優先級反轉當機**（ watchdog 重置數十次）由 JPL 遠端改用優先級繼承修復——**教科書案例流傳至今**。
- Linux 後來補上 `PREEMPT_RT` 補丁（2005 起）搶攻軟即時市場——POSIX.1b 讓兩陣營同台。
- 工業、航太、電信設備的標準 OS；Wind River 成為嵌入式軟體龍頭。
- 歷史教訓：**標準介面（POSIX.1b）+ 理論（優先級繼承）= 即時系統從工藝變科學**。

## 關鍵人物與文獻
- **L. Sha / R. Rajkumar / J. Lehoczky**：Priority Inheritance Protocols (1990)。
- **Wind River / J. Fiddler**：VxWorks；JPL Mars Pathfinder (1997)。
- 相關案件：`1976-VRTX與即時核心誕生.md`、`../UNIX/1989-POSIX標準與BSD授權.md`、`1998-uClinux與RTLinux.md`。
