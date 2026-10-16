# 1991 - Linux 誕生（網路協作的勝利）

## 案件摘要
1991 年 8 月 25 日，芬蘭赫爾辛基大學 21 歲學生 Linus Torvalds 在 comp.os.minix 新聞群組發文：
> 「我正在做一個（自由的）作業系統……只是興趣，不會像 GNU 那樣大而專業。」

**Linux 核心 0.01 版**（約 1 萬行 C 語言）隨後釋出。
GNU 工具鏈（見「1983-GNU計畫.md」）+ Linux 核心 = **GNU/Linux**——
網路協作開發的第一次大勝利，今天統治伺服器、雲端與手機（Android）的核心。

## 前因 -- 為什麼會有這個案子
- **Torvalds 的處境**：大學課程用 MINIX 教學（見「1987-MINIX微核心.md」）——他買了台 386 PC，想要一個能「充分利用 386 保護模式」的自由系統——MINIX 不用 386 的進階功能、Hurd 遲遲未出。
- **386 的契機**：Intel 386（1985）的**保護模式 + 分頁**使 PC 第一次具備「真正的」多工硬體——**PC 硬體追上了大型機**，只缺一個 OS。
- **GNU 的缺口**：GNU 工具鏈齊備，唯缺核心（Hurd 進度緩慢）——**拼圖缺一塊**。
- **網路的契機**：Usenet/網際網路使原始碼**即時全球分發**——協作開發的基礎設施就位。
- **Torvalds 的偵探直覺**：與其等 Hurd，不如自己寫核心——「只用 C + 386 組語、宏核心、能跑 GCC 就好」——**務實的極簡**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：宏核心 + 386 保護模式
Torvalds 的取捨（與 Tanenbaum 相反，見「1987-MINIX微核心.md」）：
$$\text{宏核心（性能）} + \text{386 分頁保護} \quad \text{vs} \quad \text{微核心（隔離但慢）}.$$
386 的關鍵硬體：
- **分頁**（$4\text{KB}$ 頁）：虛擬記憶體的硬體基礎。
- **保護環**：Ring 0（核心）/ Ring 3（用戶）——特權隔離。

### 第二條線索：GPL + 網路 = 協作的數學
Linux 以 **GPL** 釋出（1992 年 0.12 版起）：
$$\text{任何人} \xrightarrow{\text{GPL + 網路}} \text{修改 → 發布 → 再修改} \quad \text{（滾雪球）}.$$
貢獻者的增長：
$$\text{貢獻者數} \sim \text{指數增長} \quad \text{（1991: 1 人 → 2020s: 每版數千貢獻者、數千萬行）}.$$
**Bazaar vs Cathedral**（Raymond, 1997）：Linux 證明「市集式」的鬆散協作勝過「教堂式」的集中開發——
$$\text{給足夠多的眼睛，所有缺陷都淺顯} \quad \text{（Linus 定律）}.$$

### 第三條線索：版本控制的進化
協作逼出工具進化：BitKeeper（2002）→ **Git**（2005，Torvalds 親寫）——
分散式版本控制成為全球軟體協作的標準（GitHub 時代）。

### Python：Linux 定律（眼睛與缺陷）的模擬

```python
import numpy as np

np.random.seed(0)
def bug_removal(n_reviewers, bugs=100):
    # 每位審查者獨立發現每個 bug 的機率 p
    p = 0.02
    found = 1 - (1-p)**n_reviewers        # 每個 bug 被發現的機率
    remaining = bugs * (1 - found)
    return remaining

for n in [1, 10, 100, 1000]:
    print(f"{n:5d} 位審查者 → 殘留缺陷 {bug_removal(n):6.1f} / 100")
```
輸出：
```
    1 位審查者 → 殘留缺陷   98.0 / 100
   10 位審查者 → 殘留缺陷   81.7 / 100
  100 位審查者 → 殘留缺陷   13.3 / 100
 1000 位審查者 → 殘留缺陷    0.0 / 100
```
（眼睛越多，殘留缺陷指數趨零——**Linus 定律**的鐵證。）

## 結案 -- 後果與影響
- **伺服器統治**：1990 年代末 Linux 佔領 ISP 與網頁伺服器；今天 **全球超級電腦 Top500 全數運行 Linux**、雲端 VM 大多數是 Linux——核心無所不在。
- **Android（2008）**：Google 以 Linux 為核心打造行動系統（見「2008-Android行動作業系統.md」）——**Linux 佔領口袋**，裝機量數十億。
- **開源生態的勝利**：Git/GitHub、Apache、GNOME、KDE——Linux 證明 GPL + 網路協作可以生產**世界級軟體**；之後 AI 的開源模型沿此路線。
- **Tanenbaum–Torvalds 辯論的結局**：宏核心的 Linux 統治了世界，但微核心思想存活在 macOS（XNU）、QNX、seL4 中——**務實與純粹並存**。
- **歷史定位**：Torvalds 獲 2012 年千禧技術獎——**21 歲學生的一萬行程式碼，長成數千萬行的世界基礎設施**。
- 歷史教訓：**「只是興趣」的專案 + GPL + 網路 = 史上最大的協作體系**——動機可以渺小，結構決定規模。

## 關鍵人物與文獻
- **L. Torvalds**：comp.os.minix 宣告 (1991)；Linux 0.01 (1991)；Git (2005)；《Just for Fun》(2001)。
- **E. S. Raymond**：《The Cathedral and the Bazaar》(1997)——Linux 定律。
- **A. S. Tanenbaum**：MINIX（1991 年的開發平台）。
- 相關案件：`1983-GNU計畫.md`、`1987-MINIX微核心.md`、`2006-AWS虛擬化雲端.md`。
