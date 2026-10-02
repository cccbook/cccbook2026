# 1991-Linux：一封新聞群組信件引發的作業系統革命

## 案件摘要
1991 年 8 月 25 日，芬蘭赫爾辛基大學 21 歲學生 Linus Torvalds 在 Usenet 上寫道：「我正在做一個（免費）作業系統，只是興趣，不會像 GNU 那樣大又專業。」這封謙遜的信，開啟了人類史上最大規模的協作軟體工程。

## 前因 -- 為什麼會有這個案子
- **Unix 的授權困境**：Unix 原本在 AT&T 貝爾實驗室誕生，但因 1956 年反壟斷協定不能賣軟體，原始碼反而流向大學（1975 年起）。1980 年代 AT&T 商業化 Unix（System V），授權費昂貴，校園用不起。
- **Minix 的啟蒙**：1987 年荷蘭教授 Andrew Tanenbaum 為教學寫出 Minix——可在 PC 上執行的類 Unix 系統，附完整原始碼，僅 69 美元。Linus 買了一台 386 PC 跑 Minix，發現它缺乏終端模擬功能，於是動手自己寫。
- **GNU 計畫的缺口**：1983 年 Richard Stallman 發起 GNU（GNU's Not Unix），目標打造完全自由的 Unix 替代品，並創作 GPL 授權。到 1991 年，GNU 的編譯器（GCC）、編輯器（Emacs）、shell、工具鏈齊備——**只缺一個可用的核心**（GNU 自己的 Hurd 核心難產）。
- **前人的失敗**：1989 年 William & Lynne Jolitz 的 386BSD 尚未成熟；坊間沒有免費又完整的 PC Unix。歷史等一個填補缺口的人。

## 線索與推理 -- 數學式、程式、理論

### 那封信（1991.8.25, comp.os.minix）

> Hello everybody out there using minix-
> I'm doing a (free) operating system (just a hobby, won't be big and
> professional like gnu) for 386(486) AT clones...

當時 Linus 已在 7 月發布 Linux 0.01（約 10,259 行 C 與組合語言）。核心的第一行程式碼（boot/bootsect.S 附近）就是從 BIOS 接手控制權：

```asm
! bootsect.S 概念：把核心載入記憶體
mov ax,#0x9000    ! 載入位址
mov es,ax
mov cx,#256       ! 256 words
```

### 核心（kernel）與 Shell 的分工

作業系統的核心負責行程、記憶體、檔案系統、裝置；shell 是包在外面的命令解譯器。經典的 fork-exec 模型：

```c
/* 核心行程建立（概念，參照 kernel/fork.c） */
pid_t pid = fork();          // 複製自己，兩個行程從此並行
if (pid == 0) {
    execve("/bin/ls", argv, envp);  // 子行程換成 ls 的程式碼
} else {
    wait(NULL);              // 父行程等待
}
```

Linux 0.01 的核心排程器極簡——round-robin 加優先權：

```python
# 簡化版 round-robin 排程（模擬 Linux 0.01 的概念）
def schedule(tasks):
    # tasks: [(name, counter, priority)]
    tasks.sort(key=lambda t: -t[1])          # counter 最大者先跑
    current = tasks[0]
    current = (current[0], current[1] // 2, current[2])  # 時間片減半
    for i, t in enumerate(tasks[1:], 1):     # 其餘補回 counter
        tasks[i] = (t[0], t[1] + t[2], t[2])
    return tasks

tasks = [("init", 15, 15), ("shell", 5, 5), ("gcc", 10, 10)]
print(schedule(tasks))  # gcc 先被排程，counter 遞補機制運作
```

### GPL 與開源開發模式
- **GPL（1989, GPL v1；1991, v2）**：Copyleft 授權——可以自由使用、修改、散布，但衍生作品必須同樣以 GPL 釋出。數學化表達：GPL 對軟體定義了一個「閉包」運算

$$GPL(S) = \{ \text{所有 } S \text{ 的衍生作品} \} \subseteq GPL\text{-授權軟體集}$$

- **Linux + GNU 的合流**：Linus 決定以 GPL 釋出 Linux 核心，GNU 的工具鏈填補了使用者空間。1992 年 Tanenbaum 與 Torvalds 著名的「Monolithic vs microkernel」筆戰中，Tanenbaum 批評 Linux 是「過時設計」——歷史卻證明單體核心（monolithic kernel）+ GPL 的組合贏了效能與生態。
- **Bazaar vs Cathedral**：1997 年 Eric Raymond 發表〈The Cathedral and the Bazaar〉，指出 Linux 的開發模式（人人可改、快速釋出、群體除錯）優於傳統封閉團隊。其背後是 Linus' Law：

$$\text{「給予足夠多的眼睛，所有臭蟲都淺顯易見」} \implies E[\text{bug 發現率}] \propto N_{\text{開發者}}$$

分散式協作的除錯能力隨人數近線性增長——這是開源模式的數學優勢。

## 結案 -- 後果與影響
- **伺服器霸主**：超過 70% 的網頁伺服器執行 Linux；全球雲端基礎設施幾乎以 Linux 為底。
- **Android 之父**：Android 核心即 Linux kernel，讓 Linux 成為使用者數最多的作業系統（數十億台手機）。
- **超級電腦**：TOP500 榜單 100% 的超級電腦執行 Linux。
- **商業模式革命**：Red Hat、SUSE 證明「賣服務不賣軟體」可行；IBM、微軟相繼擁抱 Linux。
- 2000 年代「大教堂倒下、市集接管」，開源成為軟體業的預設模式——從 Python、Git 到 AI 框架，皆是市集的子孫。

## 關鍵人物與文獻
- **Linus Torvalds**：comp.os.minix 宣告（1991.8.25）、Just for Fun（自傳，2001）
- **Richard Stallman**：GNU 宣言（1983）、GPL 授權（1989）
- **Andrew Tanenbaum**：Minix（1987）、Tanenbaum–Torvalds 筆戰（1992）
- **Eric Raymond**：〈The Cathedral and the Bazaar〉（1997）
- **Ken Thompson & Dennis Ritchie**：Unix 原創者——Linux 的精神祖師
