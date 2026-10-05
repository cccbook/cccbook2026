# 2014 - Kubernetes 編排：機房作業系統的誕生

## 案件摘要
2014 年 6 月，Google 開源 Kubernetes——以 Borg（Google 內部叢集管理系統）的血統，
把數百上千個容器**編排**（orchestration）成機房級的叢集。
Kubernetes 以**宣告式 API**描述期望狀態（desired state），控制器不斷把現實收斂到期望——
容器管單機隔離，K8s 管整個機房。它被稱為「資料中心的作業系統」，
雲原生（cloud native）自此有了作業系統層。

## 前因 -- 為什麼會有這個案子
- **容器的規模問題**：Docker（2013）讓單機跑數百個容器，但跨主機的部署、擴容、故障恢復仍是手工活。
- **Google 的內部經驗**：Borg（2003）管理數十萬個 job——Google 深知「機房即電腦」的架構，且願意開源（見 1964-CDC6600 案的 PPU 異構分工傳統）。
- **Mesos 的先驅**：Twitter 的 Mesos（2011）證明叢集資源共享可行，但 API 太底層。
- **關鍵推理**：管理機房不要命令式腳本，要**宣告式**：

$$
\text{期望狀態} \xrightarrow{\text{控制迴路}} \text{收斂},\qquad \text{現實} \ne \text{期望} \Rightarrow \text{控制器動手}
$$

- **Brendan Burns、Joe Beda、Craig McLuckie**（Google）：以 Go 語言寫出 Kubernetes（希臘語「舵手」，呼應 Docker 的貨櫃），2015 年捐給 CNCF。

## 線索與推理 -- 數學式、程式、理論

### 1. 案件現場：宣告式 API 與控制迴路

Kubernetes 的心臟是**reconcile 控制迴路**：

$$
\text{desired} \xrightarrow{\text{observe}} \text{actual} \xrightarrow{\text{diff}} \text{actions} \xrightarrow{} \text{收斂（循環至 } \text{diff} = 0\text{）}
$$

- 使用者宣告期望（「要有 3 個副本」），控制器持續比對現實，不足就補、超額就刪。
- 自愈（self-healing）是宣告式的副作用：容器掛了，副本數不足，控制器自動重建——**故障恢復不需要人**。

### 2. 調度：bin packing 與資源分配

Pod 是 K8s 的最小單位（一組共用網路與儲存的容器），排程器決定 Pod 落在哪台節點：

$$
\text{node} = \arg\min_{n \in N} \Big(\text{waste}(n)\Big)\ \text{s.t.}\ \text{resources}(pod) \le \text{capacity}(n)
$$

- **bin packing**：把 Pod 裝進節點的資源箱（CPU/記憶體），最小化浪費——NP-hard，K8s 用啟發式（least-requested/balanced）。
- **requests 與 limits**：Pod 聲明資源需求（排程依據）與上限（執行約束），cgroups 落實——資源帳目清楚，超賣與飢餓可控。

### 3. 服務發現與擴容：彈性的數學

- **Service**：一組 Pod 的虛擬 IP 與負載均衡——Pod 隨生隨滅，Service 位址穩定。
- **HPA（Horizontal Pod Autoscaler）**：依負載自動擴縮副本數：

$$
\text{replicas}_{\text{new}} = \left\lceil \frac{\text{當前副本} \times \text{當前負載}}{\text{目標負載}} \right\rceil
$$

- **彈性**：尖峰時擴容、低谷時縮容——雲端計費按用量，成本與負載同步。

### 4. Kubernetes YAML：宣告式的心智模型

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3                      # 期望：永遠 3 個副本
  selector:
    matchLabels: {app: web}
  template:
    metadata:
      labels: {app: web}
    spec:
      containers:
      - name: web
        image: myapp:1.2           # Docker 鏡像（見 2013-Docker容器.md）
        resources:
          requests: {cpu: "100m", memory: "128Mi"}   # 排程依據
          limits:   {cpu: "500m", memory: "512Mi"}   # cgroups 上限
```

- 使用者只寫「要什麼」（3 副本、這個鏡像、這些資源），不寫「怎麼做」——與命令式腳本的根本差異。
- 控制器看到 Pod 掛了就補、節點掛了就搬——**故障恢復是系統行為，不是人的反應**。

### 5. Python 實作：bin packing 與自愈模擬

```python
import math

nodes = [{'cpu': 4.0, 'mem': 8.0, 'used': 0.0, 'mem_used': 0.0, 'pods': []} for _ in range(3)]
pods = [{'cpu': 1.0, 'mem': 2.0} for _ in range(5)]   # 5 個 Pod

def schedule(nodes, pod):            # bin packing：選浪費最小的節點
    best, waste_best = None, None
    for n in nodes:
        if n['cpu'] - n['used'] >= pod['cpu'] and n['mem'] - n['mem_used'] >= pod['mem']:
            waste = (n['cpu'] - n['used'] - pod['cpu']) + (n['mem'] - n['mem_used'] - pod['mem'])
            if waste_best is None or waste < waste_best:
                best, waste_best = n, waste
    if best:
        best['used'] += pod['cpu']; best['mem_used'] += pod['mem']
        best['pods'].append(pod)
    return best

for p in pods:
    n = schedule(nodes, p)
    print(f"Pod({p['cpu']}cpu/{p['mem']}mem) → 節點 {nodes.index(n)}")
# Pod(1cpu/2mem) → 節點 0（連續裝箱，浪費最小）

def hpa(current, current_load, target_load):
    return math.ceil(current * current_load / target_load)

print(f"3 副本、負載 120%、目標 80% → 擴容至 {hpa(3, 1.2, 0.8)} 副本")
print(f"3 副本、負載 40%、目標 80% → 縮容至 {hpa(3, 0.4, 0.8)} 副本")
# 3 副本、負載 120%、目標 80% → 擴容至 5 副本
# 3 副本、負載 40%、目標 80% → 縮容至 2 副本
# （宣告式 + 控制迴路：擴縮容是收斂行為，不是人工反應）

def self_heal(desired, alive):
    return desired - alive           # reconcile：差多少補多少
print(f"期望 5 副本、存活 3 → 控制器重建 {self_heal(5, 3)} 個")
# 期望 5 副本、存活 3 → 控制器重建 2 個
```

## 結案 -- 後果與影響
- **雲原生作業系統**：Kubernetes 成為機房與雲的標準調度層——CNCF（2015）生態（Helm、Istio、Prometheus）全部圍繞它。
- **部署革命完成**：金絲雀發布、藍綠部署、滾動更新成為宣告式配置——DevOps（見 2009 案）的最後一哩被自動化。
- **微服務的載體**：服務網格、分散式追蹤——微服務架構的基礎設施問題被 K8s 收編。
- **產業格局**：AWS/GCP/Azure 全面提供 K8s 服務；Docker 引擎被收編為執行時之一（containerd/CRI-O）——**編排層贏了，容器成為零件**。
- **宣告式思想傳承**：IaC、GitOps、serverless——「聲明期望、系統收斂」成為基礎設施的通用心智模型。

## 關鍵人物與文獻
- **Brendan Burns、Joe Beda、Craig McLuckie**（Google, 2014）：Kubernetes 的創造者；Kelsey Hightower 的佈道。
- **Google Borg 團隊**：B. Burns et al., "Borg, Omega, and Kubernetes", *CACM*, 2016——三代叢集管理的血統。
- **Abhishek Verma 等**（Google）：Borg 系統論文, EuroSys 2015。
- **CNCF**（Cloud Native Computing Foundation, 2015）：Kubernetes 的中立家園。
- 相關案件：`2013-Docker容器.md`、`2009-DevOps與持續部署.md`、`1964-CDC6600超級電腦.md`。
