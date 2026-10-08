# 2004 - Ubuntu 與桌面化（Linux for Human Beings）

## 案件摘要
2004 年 10 月 20 日，**Ubuntu 4.10（Warty Warthog）** 發布——Mark Shuttleworth（Canonical 創辦人）的宣言：
> **"Linux for Human Beings"**——把 Debian 的穩固 + 桌面的易用，變成人人可裝的系統。
$$\text{Debian（穩固但艱澀）} \;\xrightarrow{\text{Ubuntu}}\; \text{半年一版、預裝桌面、免費光碟}.$$
**Linux 桌面化的關鍵一步**——今天逾半數雲端伺服器與大量開發者工作站衍生自 Ubuntu。

## 前因 -- 為什麼會有這個案子
- **Debian 的缺陷**：Debian（1993）穩固但**發行週期長（1–3 年）**、安裝艱澀、桌面預設環境複雜——**彌補的缺陷：發行慢、不易用**。Shuttleworth 2002 年自費上太空後，決心打造「友善的 Debian」。
- **桌面硬體的普及**：2004 年 USB 隨身碟、寬頻網路普及——**Live CD（免安裝試用）**成為可能。
- **半年發行週期的理由**：Mozilla Firefox（2004.11）等桌面軟體更新快——發行版也必須**快速迭代**才能跟上桌面軟體的腳步。

## 線索與推理 -- 技術面貌（2004）

| 技術 | Ubuntu 4.10 狀態 | 彌補的缺陷 |
|------|-----------------|-----------|
| **Live CD** | 免安裝、可試用 | 要裝了才知道好不好用 |
| **半年一版** | 4.10 → 5.04 → 5.10 | Debian 1–3 年才一版 |
| **GDM 圖形安裝** | 圖形化安裝器 | 文字安裝器嚇跑新手 |
| **APT 整合** | 繼承 Debian APT（1998） | RPM 的依賴地獄 |
| **音效** | ESD/ALSA 預設可用 | 桌面音效設定繁瑣 |
| 後續 | **sudo 預設取代 root** | 直接用 root 的危險 |

### Shell 範例：Ubuntu 的易用性革命

```bash
# Debian 傳統：切換 root 才能做管理
$ su -                      # 輸入 root 密碼——危險且難以審計

# Ubuntu (2004)：sudo 預設——個人權限提升 + 完整審計
$ sudo apt install firefox
[sudo] password for user:   # 只用個人密碼，動作記錄在案
$ sudo journalctl -u ssh    # 完整審計軌跡
```

### Shell 範例：APT 的半年度迭代

```bash
# Ubuntu 的 APT：半年一版，升級一個指令
$ sudo apt update && sudo apt dist-upgrade
Reading package lists... Done
Calculating upgrade... Done

# PPA（Personal Package Archive，2007）：社群套件庫的爆發
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt install python3.12    # 社群維護的新版軟體
```

### Python 範例：發行週期對安全的影響

```python
import datetime

def security_lag(release_interval_days, cve_disclosure):
    """發行週期越短，CVE 修補到達使用者的延遲越短"""
    return cve_disclosure + datetime.timedelta(
        days=release_interval_days / 2)   # 平均半個週期

debian_lag = security_lag(365, datetime.date(2024, 1, 1))
ubuntu_lag = security_lag(182, datetime.date(2024, 1, 1))
print("Debian 系平均補丁到達:", debian_lag)   # 慢
print("Ubuntu 系平均補丁到達:", ubuntu_lag)   # 快半年
```

## 結案 -- 後果與影響
- **雲端的標準**：AWS 官方 AMI、OpenStack 預設——Ubuntu 成為雲端伺服器最常見的發行版。
- **衍生家族**：Linux Mint（2006）、Kubuntu/Xubuntu/Lubuntu——發行版的發行版。
- **Snap（2016）**：容器化套件格式——依賴地獄的另一種解法（但引發社群爭議）。
- **Debian 的反哺**：Ubuntu 的成功證明 Debian 的底子穩固——兩支傳統互相成就。
- 歷史教訓：**發行版的戰場不在技術而在體驗——「Linux for Human Beings」是產品思維的勝利**。

## 關鍵人物與文獻
- **M. Shuttleworth**：Canonical (2004)、Ubuntu 4.10。
- **Debian 專案**：APT (1998)、Social Contract (1997)。
- 相關案件：`../UNIX/1993-發行版與FreeBSD誕生.md`、`2014-systemd與WSL.md`。
