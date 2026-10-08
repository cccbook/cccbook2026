# 1975 - Version 6 與 BSD 起源（西岸的變種開端）

## 案件摘要
1975 年，Bell 實驗室發布 **Version 6 Unix**——第一個廣泛流傳到大學的版本（約 9,000 行核心，含完整原始碼）。
同年 **Ken Thompson 休假（sabbatical）到 UC Berkeley**，把 Unix 帶進西海岸——**BSD（Berkeley Software Distribution）的種子就此埋下**。
$$\text{V6 原始碼流出} \;+\; \text{Thompson 進入 Berkeley} \;=\; \text{Unix 史上最重要的分岔：BSD 誕生}.$$

## 前因 -- 為什麼會有這個案子
- **V6 的地位**：1975–77 年間，全球逾 75% 授權的 Unix 都是 V6——它是「標準 Unix」的第一個事實版本。
- **Thompson 的休假**：1975–76 年，Thompson 帶著 V6 到 Berkeley，與學生（包括 **Bill Joy**、Chuck Haley）一起改進系統——**用一學期時間，把 Bell 的系統變成學生的遊樂場**。
- **Pascal 編譯器的需求**：Berkeley 想在 Unix 上跑 Pascal（Thompson 寫了第一版）——編譯器與作業系統的合作，逼出了 BSD 的第一批改進。
- **彌補的缺陷**：V6 的 PDP-11 只能定址 64KB——學生們需要虛擬記憶體、更好的編輯器、網路——**所有 V6 缺的，都是 BSD 要補的**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：1BSD 與 2BSD（1977–78）
Berkeley 發布的第一批「發行版」其實只是**附加軟體**（Pascal 編譯器、ex 編輯器）——
$$\text{BSD} = \text{Unix 基底} + \text{Berkeley 的附加層}.$$
- **歷史意義**：這是「發行版（distribution）」概念的起源——今天 Debian、Ubuntu、Red Hat 的模式，原型就是 BSD。

### 第二條線索：vi 的誕生（1976）
Bill Joy 把 `ed` 的行編輯擴充為 `ex`，再加上**全螢幕視覺模式**成為 `vi`：
$$\text{ed（行導向）} \Rightarrow \text{ex（擴充）} \Rightarrow \text{vi（全螢幕視覺）}.$$
- **彌補的缺陷**：1976 年的終端機（ADM-3A）終於能做游標定位——ed 的行編輯已浪費了硬體能力。**硬體進步逼出編輯器革命**。

### 第三條線索：C Shell（1978）
Bill Joy 寫出 `csh`——C 語言風格語法 + **工作控制（job control）**：
- **彌補的缺陷**：Thompson shell（sh）無法暫停/恢復行程、無法把行程丟到背景、無歷史記錄。csh 的 `&`、`jobs`、`fg`、`bg`、`!` 歷史——讓互動操作第一次「像管理一群行程」。

### 範例：vi 的模式切換（1976 年的革命）

```text
vi 的核心抽象：模式（mode）
  Normal mode  -- 移動、刪除、複製（dd, yy, p）
  Insert mode  -- 打字（i, a, o）
  Command mode -- ex 指令（:w, :q, :s/pat/rep/g）

按鍵序列：ESC i hello ESC :wq
（從 ed 的「每行重打」到 vi 的「游標任意移動」——編輯效率的數量級躍升。）
```

### Shell 範例：csh 的工作控制

```bash
# csh (1978) 之後的 shell 都支援工作控制
$ longjob &
[1] 12345          # 丟到背景
$ jobs
[1]  + Running     longjob
$ fg %1            # 拉回前景
$ Ctrl-Z           # 暫停
$ bg %1            # 繼續在背景執行
```

## 結案 -- 後果與影響
- **BSD 成為 Unix 的第二極**：Berkeley 與 AT&T 兩支後裔分庭抗禮——Sun OS、4.xBSD、FreeBSD、NetBSD、macOS 都是 BSD 後裔。
- **vi 與 Emacs** 成為 50 年來編輯器的兩大傳統；今天 VS Code 的 Vim 模式仍是 vi 的直系後裔。
- **工作控制**成為所有 Unix shell 的標準功能，並進入 POSIX 標準。
- 下一階段：VAX 上的虛擬記憶體與 TCP/IP（見 `1979-Version7與System_III.md`、`1983-BSD4.2TCP_IP與Sun.md`）。
- 歷史教訓：**系統的命運常取決於一個休假的教授與一群有空的學生**。

## 關鍵人物與文獻
- **K. Thompson**：1975–76 Berkeley 休假，Pascal 編譯器。
- **Bill Joy**：vi (1976)、csh (1978)、1BSD/2BSD 發行。
- 相關案件：`1974-CACM論文與授權擴散.md`、`1978-2.8BSD與vi及C_Shell.md`。
