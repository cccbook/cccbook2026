# 2013 - Docker 容器（部署的工業革命）

## 案件摘要
2013 年，Solomon Hykes 在 Python 研討會上演示 **Docker**——
作業系統層虛擬化 (OS-level virtualization) 的商品化：
$$\text{應用 + 依賴 + 設定} \xrightarrow{\text{映像檔}} \text{任何機器上一致的執行環境}.$$
「在我機器上能跑」的永恆痛點被謀殺——
虛擬機的重量級隔離（見「2006-AWS虛擬化雲端.md」）與 Linux 核心的輕量級 namespaces/cgroups 聯手，
**部署成為工業革命**。

## 前因 -- 為什麼會有這個案子
- **「在我機器上能跑」的命案**：開發環境 ≠ 測試環境 ≠ 生產環境——依賴版本、系統庫、設定差異使部署成為賭博——**環境不一致是 DevOps 的头号殺手**。
- **虛擬機的重量**：VM 啟動數十秒、每台數 GB——微服務需要**秒級啟動、MB 級體積**——VM 太重。
- **Linux 核心的先驅線索**（2000s）：
  - **namespaces（2002–2008）**：PID、網路、掛載、UTS 等命名空間——行程看到「自己的世界」。
  - **cgroups（2008）**：控制群組——行程群的資源（CPU、記憶體、I/O）限額。
  - **chroot（1979）**：根目錄隔離的先驅。
- **LXC 的先行**（2008）：Linux Containers 已組合 namespaces + cgroups，但介面複雜、無生態——**技術就位，缺的是易用性**。
- **Hykes 的偵探手法**：把 LXC 的能力包裝成**三個簡單動作**——build（打包）、ship（分發）、run（執行）——加上映像檔倉庫（Docker Hub）——**易用性引爆採用**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：namespaces —— 行程的「私人世界」
每個 namespace 給行程群一個隔離的視圖：
| Namespace | 隔離什麼 |
|-----------|----------|
| PID | 行程編號（容器內 PID 從 1 開始） |
| NET | 網路介面、埠 |
| MNT | 掛載點、檔案系統 |
| UTS | 主機名 |
| USER | UID/GID 映射 |
| IPC | 行程間通訊 |

$$\text{容器內的行程} \quad \text{以為自己獨佔整台機器}.$$
**Multics 的保護思想（1965）+ CTSS 的「感覺獨佔」思想（1961）的容器版**。

### 第二條線索：cgroups —— 資源限額
$$\text{cgroup} = \{\text{CPU 限額}, \text{記憶體限額}, \text{I/O 限額}, \text{pids 限額}\}.$$
容器不會吃光主機資源——**「吵鬧鄰居」(noisy neighbor) 被制服**：
$$\text{每個容器的資源} \le \text{cgroup 限額} \quad \text{（超出即節流或 OOM）}.$$

### 第三條線索：映像檔的分層 (layers)
Docker 映像檔是**唯讀分層** + 聯合掛載：
$$\text{映像} = \text{base 層} + \text{依賴層} + \cdots + \text{應用層（唯讀）} \quad \xrightarrow{\text{聯合掛載}} \quad \text{容器（+ 可寫層）}.$$
- **分層共用**：100 個容器共用同一個 base 層——儲存空間節省數十倍。
- **分發**：只需下載未有的層——**部署速度的關鍵**。

### Python：容器 vs VM 的資源對比模擬

```python
import numpy as np

n = 100                                      # 100 個應用
vm_base, vm_each = 0, 2.0                    # VM：每台 2 GB（含客戶 OS）
ct_base, ct_each = 0.5, 0.05                 # 容器：共享 0.5 GB base，每個 50 MB

vm_total = vm_base + n*vm_each
ct_total = ct_base + n*ct_each
print(f"100 個 VM: {vm_total:.1f} GB")
print(f"100 個容器: {ct_total:.2f} GB  （節省 {1-ct_total/vm_total:.0%}）")

# 啟動速度：VM = 開機 + 核心 init；容器 = 直接 exec
vm_boot, ct_start = 30.0, 0.3                # 秒
print(f"啟動時間: VM {vm_boot}s vs 容器 {ct_start}s （快 {vm_boot/ct_start:.0f} 倍）")
```
輸出：
```
100 個 VM: 200.0 GB
100 個容器: 5.50 GB  （節省 97%）
啟動時間: VM 30.0s vs 容器 0.3s （快 100 倍）
```
（容器以 namespaces 的輕量隔離，資源與速度全面碾壓 VM——部署革命的鐵證。）

## 結案 -- 後果與影響
- **部署的工業革命**：「build once, run anywhere」成為標準；CI/CD 全面容器化——DevOps 的生產力革命。
- **微服務架構的載體**：秒級啟動 + 輕量隔離使「一個服務一個容器」可行——Netflix、Uber 的微服務革命由此而生。
- **編排的進化**：容器數量爆炸 → **Kubernetes**（2014，Google 基於 Borg 經驗）成為容器編排之王——雲原生的標準。
- **標準化的統一**：OCI（開放容器倡議，2015）使映像檔與執行時標準化——**容器的「ISA」**。
- **歷史定位**：Linux 核心的 namespaces/cgroups（2000s）+ Docker 的易用性（2013）+ Kubernetes 的編排（2014）——**技術就位、易用性引爆、編排收尾**的完整破案鏈。
- 歷史教訓：**技術就位未必成功，易用性才是引爆點**——LXC 先行三年卻由 Docker 一夜成名（與 Cooley–Tukey、Rumelhart–Hinton 的模式如出一轍）。

## 關鍵人物與文獻
- **S. Hykes / Docker Inc.**：Docker (2013)；dotCloud 演示。
- **Linux 核心**：namespaces (2002–2008)、cgroups (2008)、LXC (2008)——先驅。
- **Google**：Kubernetes (2014)、Borg（內部先驅）。
- 相關案件：`2006-AWS虛擬化雲端.md`、`1991-Linux誕生.md`、`1961-CTSS分時系統.md`。
