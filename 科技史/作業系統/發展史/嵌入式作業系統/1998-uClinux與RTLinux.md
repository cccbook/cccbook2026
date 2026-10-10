# 1998 - uClinux 與 RTLinux（Linux 進入嵌入式）

## 案件摘要
1998 年，**Greg Ungerer** 推出 **uClinux**：把 Linux 跑在**沒有 MMU 的微控制器**上——
`mmap` 不見了，`fork` 改用 `vfork`，行程共用位址空間。
同年 **Victor Yodaiken** 的 **RTLinux** 用「雙核心」補丁讓 Linux 擁有**微秒級硬即時**——
**Linux 從伺服器走進微控制器與工業控制**。

## 前因 -- 為什麼會有這個案子
- **Linux 需要 MMU 的限制**：1991 年的 Linux（見 UNIX 書）依賴 386 分頁——微控制器（68k/ColdFire、ARM7）**根本沒有 MMU**——**彌補的缺陷：沒 MMU 跑不了**。
- **Linux 排班不確定**：標準核心的中斷延遲是**毫秒級 jitter**——工業控制要**微秒級決定**——**彌補的缺陷：不夠即時**。
- **GPL 的拼圖**：Linux 原始碼開放——任何人都能裁剪——**開放原始碼讓嵌入式改造成為可能**（封閉 RTOS 做不到）。

## 線索與推理 -- 技術面貌（1998）

| 技術 | 狀態 | 彌補的缺陷 |
|------|------|-----------|
| **uClinux** | 無 MMU Linux；`vfork` 取代 `fork` | Linux 需要 MMU |
| **flat 可執行格式** | bFLT：位置無關程式碼 | ELF 需要分頁載入 |
| **RTLinux 雙核心** | 即時小核心在底下，Linux 是它的閒置任務 | Linux 排班不確定 |
| **RT-FIFO** | `/dev/rtf0` 即時行程與 Linux 行程通訊 | 兩個世界無法交換資料 |
| **footprint** | uClinux 可裁到 **約 512KB RAM** | 桌面 Linux 數 MB |

### C 範例：無 MMU 的世界——fork 的代價

```c
/* 有 MMU 的 Linux：fork 用寫時複製（COW），便宜 */
pid = fork();

/* uClinux（無 MMU）：無法 COW——fork 要完整複製資料段，太貴
   => 只提供 vfork：父子共用同一個位址空間，父行程被暫停 */
pid = vfork();
if (pid == 0) {
    execve("/bin/app", argv, envp);  /* 子行程立即 exec */
    _exit(1);                        /* 不 exec 就不能 return */
}
```
（**硬體缺什麼，API 就變形**——無 MMU 逼出 vfork 語意。）

### C 範例：RTLinux 的雙核心——Linux 是閒置任務

```c
/* RTLinux（1998）：即時小核心搶走所有中斷，
   Linux 變成「永遠最後才跑」的閒置任務 */
#include <rtl.h>

pthread_t thread;
void * rt_handler(void *arg) {       /* 20kHz 的即時執行緒 */
    pthread_make_periodic_np(pthread_self(), gettime(), 50000);
    while (1) {
        pthread_wait_np();           /* 等下一個週期 */
        rtf_put(0, &sample, sizeof sample);  /* 寫 RT-FIFO */
    }
}
/* Linux 行程從 /dev/rtf0 讀資料——兩個世界用 FIFO 連接 */
```

### Shell 範例：雙核心的即時性差異

```bash
# 標準 Linux：中斷延遲毫秒級 jitter
$ cyclictest -m -p99
  Max: 2,340 us

# RTLinux/PREEMPT_RT：微秒級決定
$ cyclictest -m -p99
  Max: 48 us        # 決定性 = 最壞情況可預測
```

## 結案 -- 後果與影響
- uClinux 的程式碼後來**合併進主線 Linux**（2003 起 `nommu` 支援）——嵌入式裁剪成為 Linux 的內建能力。
- RTLinux 的思路演化為 **PREEMPT_RT 補丁**（2005, Ingo Molnar）→ 2024 年**進入主線核心**——雙核心與單核心之辯以務實收場。
- 為 2008 年 Android（Linux 核心）鋪路——嵌入式 Linux 從此稱霸行動裝置。
- 歷史教訓：**開放原始碼 + 硬體多樣性 = OS 被迫學會「變形」**；決定性問題最終靠主線吸收解決。

## 關鍵人物與文獻
- **G. Ungerer**：uClinux (1998)。
- **V. Yodaiken / M. Barabanov**：RTLinux (〈A Real-Time Linux〉, 1997–98)。
- 相關案件：`../UNIX/1991-Linux誕生.md`、`../UNIX/2008-Android以Linux為核心.md`、`1993-VxWorks與POSIX即時標準.md`。
