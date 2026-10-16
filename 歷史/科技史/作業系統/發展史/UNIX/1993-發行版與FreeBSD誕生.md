# 1993 - 發行版與 FreeBSD 誕生（自由的兩支後裔）

## 案件摘要
1993 年，自由 Unix 的兩支後裔同年誕生：
1. **NetBSD（3 月）與 FreeBSD（12 月）**——386BSD 的兩個分叉，BSD 授權的繼承者。
2. **Slackware（7 月）與 Debian（8 月）**——第一批 Linux 發行版（distributions）。
$$\text{386BSD} \Rightarrow \text{NetBSD / FreeBSD} \qquad \text{Linux 核心} \Rightarrow \text{Slackware / Debian}.$$
**「發行版」模式成型**：核心 + 工具 + 套件管理 = 可安裝的完整系統。

## 前因 -- 為什麼會有這個案子
- **386BSD 的官司**：1992 年 Bill Jolitz 的 386BSD（VAX BSD 移植到 386）流行一時，但維護緩慢、社群 patch 無人整合——**彌補的缺陷：單人專案無法吸納社群貢獻**。1993 年 NetBSD/FreeBSD 分叉而出。
- **AT&T vs BSD 官司**：1992 年 USL（AT&T 子公司）控告 Berkeley 使用 AT&T 程式碼——官司凍結了 BSD 三年，**Linux 趁機坐大**。1994 年和解，BSD 4.4BSD-Lite 釋出（零 AT&T 碼）。
- **Linux 需要「發行版」**：1991–92 年的 Linux 只有一個核心，使用者要自己湊 GNU 工具、自己 mount 磁碟——**彌補的缺陷：安裝體驗極差**。Slackware/Debian 把「核心+工具+安裝器」打包成可安裝系統。
- **Debian 的社會實驗**：Ian Murdock 主張發行版應由**社群民主治理**而非個人——Debian Social Contract（1997）成為開源治理的經典。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：發行版 = 核心 + 生態
$$\text{發行版} = \text{核心（Linux/BSD）} + \text{使用者空間（GNU/utilities）} + \text{套件管理} + \text{安裝器}.$$
- **歷史意義**：BSD 的「distribution」概念（1977 年 1BSD 起源）在 1993 年被 Linux 發揚光大——**今天 Ubuntu、Red Hat 的模式，原型就是 BSD**。

### 第二條線索：套件管理——依賴解決的演算法
- Slackware：tgz 壓縮包，無依賴解決（手動）。
- **Debian：dpkg + APT（1998）**——自動解決依賴關係：
  $$\text{套件 A 依賴 B、C} \;\xrightarrow{\text{APT}}\; \text{拓撲排序安裝}.$$
- **彌補的缺陷**：手動安裝會陷入「依賴地獄」（dependency hell）——APT 用圖論（依賴圖 + 拓撲排序）一次解決。

### 第三條線索：三支 BSD 的分工
- **NetBSD**：「當然能跑 NetBSD」——移植到最多硬體平台（彌補缺陷：硬體支援碎片化）。
- **FreeBSD**：效能與伺服器市場（Yahoo!、Netflix 早期都用 FreeBSD）。
- **OpenBSD（1995，Theo de Raadt 從 NetBSD 分叉）**：安全性優先——**程式碼稽核（code audit）**文化，30 年來僅兩個遠端漏洞。

### Shell 範例：套件管理的演化

```bash
# 1993 Slackware：手動安裝 tgz
$ installpkg vim-4.5.tgz          # 無依賴解決——自己想辦法

# 1998 Debian APT：自動解決依賴
$ apt-get install vim             # 自動拉下所有依賴套件
Reading package lists... Done
The following NEW packages will be installed:
  vim vim-runtime libtinfo6 ...   # 依賴圖自動展開
```

### Python 範例：依賴解決的拓撲排序

```python
from graphlib import TopologicalSorter

deps = {"vim": ["libtinfo6", "vim-runtime"],
        "vim-runtime": ["libc6"],
        "libtinfo6": ["libc6"],
        "libc6": []}

ts = TopologicalSorter(deps)
print(list(ts.static_order()))
# ['libc6', 'libtinfo6', 'vim-runtime', 'vim']——安裝順序的數學解
```

## 結案 -- 後果與影響
- **Red Hat（1994）→ RHEL（2000）→ Fedora**：Linux 商業化的勝利——企業支援模式的開創。
- **Debian → Ubuntu（2004）**：社群治理 + 易用性——今天逾半數 Linux 伺服器衍生自 Debian 系。
- **OpenBSD 的安全遺產**：OpenSSH（1999，OpenBSD 的計畫）成為全世界遠端登入的標準工具。
- **BSD 的商業後裔**：macOS（2001）、Sony PlayStation OS、Netflix CDN——BSD 授權的寬容讓企業敢用。
- 歷史教訓：**官司凍結 BSD 的三年，成就了 Linux 的黃金三年——開放與授權清晰比技術更決定命運**。

## 關鍵人物與文獻
- **I. Murdock**：Debian 宣言 (1993)。
- **P. Volkerding**：Slackware (1993)。
- **T. de Raadt**：OpenBSD (1995)、OpenSSH (1999)。
- 相關案件：`1991-Linux誕生.md`、`1989-POSIX標準與BSD授權.md`。
