# 1991 - Linux 誕生（網路協作的勝利）

## 案件摘要
1991 年 8 月 25 日，芬蘭赫爾辛基大學 21 歲學生 **Linus Torvalds** 在 comp.os.minix 新聞群組發出那封著名的信：
> 「我正在做一個（自由的）作業系統，只是嗜好，不會像 GNU 那樣龐大專業……」

9 月 17 日，**Linux 0.01**（約 10,000 行 C 與組語）上傳到 FTP——
$$\text{MINIX（教學）} + \text{GNU 工具（自由）} + \text{網路（Usenet 協作）} = \text{Linux}.$$
**史上第一個靠網路協作、從零開始的自由 Unix 核心**——今天全球伺服器、手機、超級電腦的基礎。

## 前因 -- 為什麼會有這個案子
- **MINIX 的限制**：Torvalds 買了 MINIX 學習，但 Tanenbaum 不接受 patch（要保持教學純潔）、不許商用——**彌補的缺陷：MINIX 不夠自由、不許成長**。Torvalds 決定自己寫一個「可以隨意擴充」的核心。
- **386 PC 的硬體契機**：1991 年的 Intel 80386 有保護模式與分頁（paging）——Torvalds 想學習 386 的多工與虛擬記憶體，**學習硬體逼出了作業系統**（與 1969 年 Thompson 玩遊戲逼出 Unix 如出一轍）。
- **GNU 的拼圖**：GNU 已有 GCC、bash、glibc、Emacs，**獨缺可用核心**——Linux 正好補上這塊拼圖。
- **Usenet 的基礎建設**：網路新聞群組讓「一人專案」變成「全球協作」——**網路是 Linux 與所有 Unix 先驅最大的不同**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：GPL 授權的選擇
Torvalds 把 Linux 以 **GPL** 釋出（1992 年 2 月 0.12 版起）——
- **彌補的缺陷**：若用 BSD 授權，商業公司可以拿去閉源分叉、不回饋；GPL 的 copyleft 確保**所有修改必須回饋**——理論上讓核心以最快速度演化。

### 第二條線索：巨核心的務實選擇
Linux 選擇**巨核心（monolithic kernel）**，與 MINIX 的微核心相反：
- **理論爭議**：1992 年 Tanenbaum 批評 Linux 巨核心過時；Torvalds 回應「實用優先」。
- **務實理由**：巨核心的函式呼叫比微核心的 IPC 快數倍——1991 年的 386 效能有限，**務實主義贏了理論純潔**（但微核心的理論後來在嵌入式領域翻案）。

### 第三條線索：網路協作的發行模式
$$\text{郵件列表/patch/FTP} \;\Longrightarrow\; \text{數千人的鬆散協作}.$$
- **彌補的缺陷**：傳統軟體靠公司內部團隊（Brooks 定律：加人反而慢）；Linux 證明**鬆散協作的網路社群可以打敗公司**——後來 Linux 用 Git（2005，Torvalds 自己寫的）解決了 patch 混亂的問題。

### C 範例：Linux 0.01 的核心風格

```c
/* Linux 0.01 (1991)：極簡的行程排班 */
void schedule(void) {
    int i, next = 0, c = -1;
    for (i = 0; i < NR_TASKS; i++) {
        /* 時間片最大的先跑——就這麼簡單 */
        if (task[i] && task[i]->state == TASK_RUNNING &&
            task[i]->counter > c) {
            c = task[i]->counter;
            next = i;
        }
    }
    switch_to(next);
}
```
（0.01 版核心僅約 10,000 行——**一個學生一個暑假可以讀完**，與 1969 年 Unix 的極簡一脈相承。）

### Shell 範例：GNU + Linux = 完整系統

```bash
# 1992 年：Linux 核心 + GNU 工具 = 完整的自由 Unix
$ uname -a
Linux mypc 0.12 #1 ... i386
$ gcc --version          # GNU 編譯器
$ bash --version         # GNU shell
$ ls | grep .c | wc -l   # GNU 工具的管道組合
```

### Shell 範例：Git（2005）的協作模型

```bash
# Torvalds 為 Linux 開發的 Git——分散式版本控制的勝利
$ git clone https://github.com/torvalds/linux.git
$ git checkout -b my-feature
$ git commit -m "my change"
$ git request-pull main origin   # 請求拉取——郵件列表協作的現代版
```

## 結案 -- 後果與影響
- **發行版時代**：1993 年 Slackware、Debian；1994 年 Red Hat；2004 年 Ubuntu——Linux 的發行版生態爆發（見 `1993-發行版與FreeBSD誕生.md`）。
- **伺服器的征服**：2000 年代 Linux 佔領網頁伺服器（LAMP）、2010 年代佔領雲端（AWS 逾 90% 為 Linux）、超級電腦 Top500 全部是 Linux。
- **手機的征服**：2008 年 Android 以 Linux 為核心（見 `2008-Android以Linux為核心.md`）——今天逾 70% 手機跑著 Linux 核心。
- **1983 GNU + 1991 Linux**：Stallman 的工具 + Torvalds 的核心 = 完整自由系統——兩人性格迥異、互相嫌棄，卻共同改變了世界。
- 歷史教訓：**網路協作 + copyleft 授權 = 史上最快的軟體演化機器**。

## 關鍵人物與文獻
- **L. Torvalds**：Linux 0.01 (1991)；Git (2005)；《Just for Fun》(2001)。
- **R. M. Stallman**：GNU 計畫 (1983)、GPL (1989)。
- **A. S. Tanenbaum**：MINIX (1987)、1992 年辯論。
- 相關案件：`1987-MINIX微核心.md`、`1993-發行版與FreeBSD誕生.md`。
