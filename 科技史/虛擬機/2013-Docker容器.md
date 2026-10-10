# 2013 - Docker：把「機器」縮小成一個行程

## 案件摘要
2013 年，Solomon Hykes 在 PyCon 上展示 Docker——一個基於 LXC 的容器工具。它證明了：你不需要模擬硬體，只需用 Linux kernel 的 namespaces 與 cgroups，就能把一個「機器」縮小成一行 `docker run`。

## 前因 -- 為什麼會有這個案子
- 系統虛擬機（VMware、KVM）模擬完整硬體，每台 VM 要帶一個客座作業系統：啟動以分鐘計、記憶體以 GB 計。
- 「在我的機器上能跑」(works on my machine) 是部署界的懸案——環境不一致。
- Linux 早有原料：chroot（1979）、jails（FreeBSD 2000）、LXC（2008），但沒人把它們包裝成好用的產品。dotCloud（PaaS 公司）內部專案 Docker 補上了這塊拼圖。

## 線索與推理 -- 數學式、程式、理論

### 線索 1：OS 級虛擬化 vs 系統虛擬化對照表
| 面向 | 系統虛擬化（VM） | OS 級虛擬化（容器） |
|---|---|---|
| 虛擬層 | hypervisor（模擬硬體） | 共用 host kernel |
| 每實例 OS | 完整客座 OS | 無，共用 kernel |
| 啟動時間 | 分鐘級（BIOS→boot→init） | 毫秒~秒級（直接 exec） |
| 記憶體開銷 | GB 級 | MB 級 |
| 隔離強度 | 強（硬體邊界） | 中（kernel 邊界） |
| 密度（單機實例數） | 十幾台 | 數百個 |

理論上，容器省去每台 VM 的 OS 開銷 $M_{os}$，$n$ 個工作負載的總記憶體：
$$M_{vm} = n(M_{os} + M_{app}), \qquad M_{container} = M_{os} + nM_{app}$$
密度提升比 $\approx \dfrac{n(M_{os}+M_{app})}{M_{os}+nM_{app}}$，當 $M_{os} \gg M_{app}$ 時趨近 $n$ 倍以上。

### 線索 2：容器 = 隔離的行程群組
容器不是「小型機器」，本質是**一組被 namespace 隔離、被 cgroups 限量的普通行程**。Docker 啟動容器約等於：
```shell
# Docker run 背後的核心操作（簡化版）
unshare --pid --net --mount --uts --ipc --fork /bin/sh   # 1. namespaces 隔離
echo "cpu.max 50000 100000" > /sys/fs/cgroup/app/cpu.max # 2. cgroups 限量（0.5 CPU）
```
- **namespaces**：pid（行程編號獨立）、net（網路堆疊獨立）、mnt（檔案系統掛載點）、uts（hostname）、ipc、user——6 大命名空間，讓容器「以為自己是全世界」。
- **cgroups**：控制 CPU、記憶體、I/O 配額，保證單一容器無法拖垮整機。

### 線索 3：映像檔分層（Layers 與 UnionFS）
Docker 映像檔由唯讀層（layer）堆疊而成，容器寫入時在上層加一個可寫層（copy-on-write）：
$$\text{image} = L_1 + L_2 + \cdots + L_k, \qquad \text{container} = \text{image} + L_{rw}$$
UnionFS（AUFS、overlayfs2）把多層「合併」成一棵檔案樹。共用基底層（如同一個 ubuntu 基底）只存一份：
$$\text{儲存總量} = |L_{base}| + \sum_i |L_i^{diff}| \ll n \cdot |image_{full}|$$

### 線索 4：Dockerfile 範例
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
```
```shell
docker build -t myapp .        # 每條指令 = 一層，並被快取
docker run -p 8000:8000 myapp  # 毫秒級啟動
```

### 線索 5：chroot → jail → LXC → Docker 的演進
$$\text{chroot (1979)} \to \text{FreeBSD jail (2000)} \to \text{Solaris Zones (2004)} \to \text{LXC (2008)} \to \text{Docker (2013)}$$
chroot 只隔離檔案系統（易逃逸）；jail 加入多重 namespace；LXC 提供完整容器工具但難用；Docker 加上**映像檔格式 + Registry（Docker Hub）+ CLI**，把容器變成可分發的「軟體貨櫃」。

### 線索 6：Kubernetes（2014）的誕生
Docker 單機可用後，多機編排成為新案。Google 把內部 Borg 的經驗開源為 Kubernetes（2014）：
$$\text{K8s} = \text{排程(scheduler)} + \text{期望狀態(declarative)} + \text{控制迴圈(reconcile loop)}$$
```shell
kubectl scale deployment myapp --replicas=10
```

## 結案 -- 後果與影響
- 容器啟動時間從 VM 的**分鐘級降到毫秒級**，微服務架構與 CI/CD 被徹底解放。
- Docker Hub 讓「映像檔」成為軟體分發的通用單位，等同一場部署界的標準化革命。
- 2014 年 Kubernetes 誕生，2015 年 CNCF 成立，直接鋪往雲端原生時代。
- Docker 公司本身後來式微，但「容器」的觀念已成為基礎設施的地基。

## 關鍵人物與文獻
- **Solomon Hykes**：Docker 創辦人，2013 PyCon 演示者。
- 文獻：Kubernetes 官方文件；*Docker: Lightweight Linux Containers for Consistent Development and Deployment* (Merkel, LISA 2014)；Linux kernel namespaces/cgroups 手冊。
