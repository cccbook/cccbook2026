# 2013 - Docker 容器（部署的工業革命）

## 案件摘要
2013 年 3 月，**Solomon Hykes** 在 PyCon 發表 **Docker**——把 Linux 的 **cgroups + namespaces** 包裝成「一個指令就能跑的容器」。
$$\text{容器} = \text{namespaces（隔離視野）} + \text{cgroups（資源限制）} + \text{映像檔（image，不可變）}.$$
**作業系統層虛擬化**：不需要虛擬機的重量級模擬，直接共享主機核心——部署從「小時級」降到「秒級」，**部署的工業革命**。

## 前因 -- 為什麼會有這個案子
- **虛擬機的缺陷**：VM（VMware、KVM）每台要完整 guest OS（GB 級）、啟動數分鐘、記憶體重複——**彌補的缺陷：太重、太慢**。容器共享主機核心：MB 級、秒級啟動。
- **「在我機器上可以跑」的詛咒**：開發環境與生產環境不一致是軟體工程永恆的痛——Docker 用**不可變映像檔**一次解決：
  $$\text{映像檔（image）} = \text{環境的完整快照} \quad \Rightarrow \quad \text{處處一致}.$$
- **Linux 核心的技術積累**：namespaces（2002 年起逐步加入核心）、cgroups（2008 年加入核心 2.6.24）、LXC（2008）——Docker 的功勞不在發明這些，而是**把它們變成人人可用的一個指令**。
- **理論基礎**：不可變基礎設施（immutable infrastructure）——系統狀態不再「修改」，而是「整個換掉」——消除狀態漂移（configuration drift）。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：namespaces——隔離的六個維度
$$\text{namespaces} = \{\text{PID, NET, MNT, UTS, IPC, USER}\}.$$
- **每個 namespace 隔離一種視野**：PID ns 讓容器有自己的行程編號 1；NET ns 讓容器有自己的網路堆疊；MNT ns 讓容器有自己的檔案樹。
- **彌補的缺陷**：chroot（1979）只能隔離檔案系統一個維度——namespaces 把隔離推到六個維度。

### 第二條線索：cgroups——資源的會計與限制
$$\text{cgroups} = \{\text{CPU, memory, IO, network}\} \text{ 的配額}.$$
- **彌補的缺陷**：Unix 傳統上無法限制某群行程的資源用量（nice 只能調優先級）——cgroups 讓「資源配額」成為一等公民。

### 第三條線索：映像檔的分層（layered image）
$$\text{映像檔} = \text{基底層} + \text{層}_1 + \text{層}_2 + \cdots \quad (\text{層可共享、可快取})$$
- **彌補的缺陷**：VM 映像數 GB 不可共享——容器映像分層，基底層（如 ubuntu:22.04）全機只存一份，**儲存與傳輸的數量級節省**。

### Shell 範例：容器的日常使用

```bash
# 1969 年的組合哲學 + 2013 年的容器 = 現代 DevOps
$ docker run -d -p 80:80 nginx        # 秒級啟動一個網頁伺服器
$ docker ps                            # 容器即行程
CONTAINER ID   IMAGE   ...   NAMES
a1b2c3d4e5f6   nginx   ...   fervent_liskov

# 映像檔的分層
$ docker history nginx
IMAGE          CREATED BY              SIZE
c3d4e5f6...    CMD ["nginx" "-g"...]   0B
...            RUN apt-get install     15MB
...            ADD ubuntu:22.04        77MB   # 基底層全機共享

# 一切皆檔案：進入容器看行程樹
$ docker exec mycontainer ps aux
```

### Python 範例：cgroups 的資源限制

```python
import resource, subprocess

# cgroups 的精神：限制子行程的資源
def limit_cpu(seconds):
    resource.setrlimit(resource.RLIMIT_CPU, (seconds, seconds))

p = subprocess.Popen(["bash", "-c", "while true; do :; done"],
                     preexec_fn=limit_cpu)
# 10 秒 CPU 後子行程被核心殺掉——資源配額成為一等公民
```

### Dockerfile 範例：不可變映像

```dockerfile
# Dockerfile：環境即程式碼（infrastructure as code）
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3
COPY app.py /app/
CMD ["python3", "/app/app.py"]
```
（同一段 Dockerfile 在任何機器上建出**位元組級相同**的環境——「在我機器上可以跑」的詛咒終結。）

## 結案 -- 後果與影響
- **DevOps 與微服務**：容器讓微服務架構（每個服務一個容器）可行——今天的雲端原生（Kubernetes 2014）建立在 Docker 之上。
- **Kubernetes（2014，Google）**：容器編排——把「跑一個容器」升級為「管理數千個容器」——Borg 論文的開源實現。
- **標準化**：OCI（Open Container Initiative, 2015）——容器格式成為開放標準。
- **Unix 哲學的回歸**：容器 = 「一個容器做一件事」——Unix「Do one thing well」在 2013 年的轉世。
- 歷史教訓：**Docker 的勝利不在發明（cgroups/ns 早就在），而在體驗——把複雜技術包裝成一個指令**。

## 關鍵人物與文獻
- **S. Hykes**：Docker (2013)、dotCloud。
- **Linux 核心**：namespaces (2002–)、cgroups (2008)。
- **Google**：Kubernetes (2014)、Borg 論文 (2015)。
- 相關案件：`1991-Linux誕生.md`、`2006-AWS虛擬化雲端.md`。
