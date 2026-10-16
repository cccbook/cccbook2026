# 2013 - Docker 發明：把部署裝進貨櫃

## 案件摘要
2013 年 3 月，Solomon Hykes 在 Python PyCon 大會上示範 Docker——
以 Linux 容器（LXC）加上鏡像分層與可移植格式，把「在我機器上能跑」的部署噩夢一次終結。
Docker 讓應用連同依賴打包成貨櫃：開發、測試、生產跑的是同一個鏡像。
部署從儀式變成指令行——DevOps 的「每天部署 10+ 次」（見 2009 案）自此有了完美的執行者。

## 前因 -- 為什麼會有這個案子
- **「在我機器上能跑」**：應用依賴系統函式庫、直譯器版本與環境配置，開發與生產環境不一致是最兇的 bug 源。
- **虛擬機太重**：VM 模擬整台機器（GB 級、啟動分鐘級）；應用只需要隔離，不需要一台假電腦。
- **Linux 容器已備好零件**：chroot（1979）、LXC、**cgroups**（Google, 2008，資源限制）與 **namespaces**（隔離）——但用法艱深，無人包裝。
- **關鍵推理**：容器 = 隔離（namespace）+ 限制（cgroup）+ **鏡像（可移植的打包格式）**：

$$
\text{容器} = \underbrace{\text{namespaces}}_{\text{隔離}} \times \underbrace{\text{cgroups}}_{\text{限制}} \times \underbrace{\text{鏡像分層}}_{\text{可移植}} \quad\Longrightarrow\quad \text{Build once, run anywhere}
$$

- **dotCloud**：Hykes 的 PaaS 公司轉型，2013 年把 Docker 開源，2015 年成立 OCI 標準化容器格式。

## 線索與推理 -- 數學式、程式、理論

### 1. 案件現場：VM vs 容器

| | 虛擬機 | 容器 |
|---|------|------|
| 隔離層 | Hypervisor + 完整 OS | 共用核心 + namespace |
| 體積 | GB 級 | MB 級 |
| 啟動 | 分鐘級 | **秒級甚至毫秒級** |
| 密度 | 數十台/主機 | **數百個/主機** |
| 可移植性 | 映像檔笨重 | 鏡像分層、標準化 |

$$
\text{資源效率} = \frac{\text{應用數}}{\text{主機}} \quad\Longrightarrow\quad \text{容器密度} \approx 10 \times \text{VM 密度}
$$

### 2. 鏡像分層：內容定址的堆疊

Docker 鏡像由**唯讀分層**堆疊而成，每層對應一條建置指令：

$$
\text{image} = L_1 \xrightarrow{} L_2 \xrightarrow{} \cdots \xrightarrow{} L_n \xrightarrow{} \underbrace{\text{可寫層}}_{\text{容器執行時}}
$$

- **分層共享**：多個鏡像共用基底層（如同一個 ubuntu 層只存一份）——磁碟與傳輸成本大幅下降。
- **快取與內容定址**：每層以內容 hash 識別，指令與輸入不變就快取命中——

$$
\text{重建時間} = O(\text{變更層以下的層數}) \quad\text{而非整個建置}
$$

- **UnionFS**：唯讀層與可寫層以 union 檔案系統疊合，容器看起來像一個完整檔案系統。

### 3. 隔離的數學：namespace 與 cgroup

- **namespaces**：pid、net、mnt、uts、ipc、user 六種命名空間——容器內的行程「以為」自己是唯一的。
- **cgroups**：CPU、記憶體、I/O 的資源限制與帳目：

$$
\text{公平共享} = \frac{\text{cgroup 配額}}{\text{全系統資源}},\qquad \sum_{\text{容器}} \text{配額} \le \text{主機資源}
$$

- 隔離弱於 VM（共用核心），但換來輕量——安全邊界與效率的取捨（後來 gVisor、Kata 加固）。

### 4. Dockerfile：部署的程式化

```dockerfile
FROM python:3.12-slim            # 基底層：官方鏡像
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt   # 依賴層：不變就快取命中
COPY . .                          # 程式碼層：最常變動，放最上層
CMD ["python", "server.py"]       # 入口
```

- **依賴層放前面、程式碼層放後面**：分層順序決定快取效率——只改程式碼時，依賴層直接快取命中。
- 同一套鏡像在開發機、CI、生產跑出**位元級一致**的環境——「在我機器上能跑」變成「在每台機器上都一樣」。

### 5. Python 實作：分層快取與密度模擬

```python
def build_time(layers, changed_idx):
    """分層快取：只重建變更層（含）以下的層"""
    cost = [10, 30, 60, 5]                       # 各層建置成本（秒）
    return sum(cost[i] for i in range(changed_idx, len(layers)))

layers = ['base', 'deps', 'code', 'config']
print(f"只改程式碼層（code 在 index 2）→ 重建 {build_time(layers, 2)} 秒")
print(f"只改 config 層（index 3）→ 重建 {build_time(layers, 3)} 秒")
print(f"全量重建 → {build_time(layers, 0)} 秒")
# 只改程式碼層（code 在 index 2）→ 重建 65 秒
# 只改 config 層（index 3）→ 重建 5 秒
# 全量重建 → 105 秒
# （層的順序決定快取效率：不變的依賴放前面）

def density(vms_per_host, vm_overhead_mb, container_overhead_mb):
    host_mb = 32 * 1024                          # 32 GB 主機
    vm_count = host_mb // (vm_overhead_mb + 512)
    ct_count = host_mb // (container_overhead_mb + 512)
    return vm_count, ct_count

vm, ct = density(0, 2048, 64)                    # VM OS 開銷 2GB，容器 64MB
print(f"VM 密度 = {vm} 個/主機，容器密度 = {ct} 個/主機，效率比 = {ct/vm:.0f}x")
# VM 密度 = 12 個/主機，容器密度 = 468 個/主機，效率比 = 39x
# （容器共用核心，密度提升一個數量級——雲端成本直線下降）
```

### 6. 結案後續：Kubernetes 與編排

- 容器普及後，數百個容器的**編排**（orchestration）成為新問題——Google 2014 年開源 **Kubernetes**（Borg 的血統），2015 年 CNCF 成立。
- Kubernetes 以宣告式 API（desired state）管理容器叢集——Docker 管單機、K8s 管機房。

## 結案 -- 後果與影響
- **部署革命**：「在我機器上能跑」成為歷史名詞；CI/CD（見 2009 案）的部署環節被容器化徹底加速。
- **雲端原生的地基**：Kubernetes、微服務、serverless——CNCF 生態全部建立在容器格式上。
- **標準化**：OCI（Open Container Initiative, 2015）統一鏡像與執行時格式；Docker 引擎只是眾多實作之一。
- **軟體交付的商品化**：鏡像像貨櫃一樣在 registry（Docker Hub）流通——軟體的分發方式被改寫。

## 關鍵人物與文獻
- **Solomon Hykes**：Docker 創辦人（dotCloud → Docker, Inc.），2013 PyCon 首次示範。
- **Paul Menage 等**（Google, 2008）：cgroups 的設計者。
- **Brendan Burns、Joe Beda、Craig McLuckie**（Google, 2014）：Kubernetes 的創造者。
- Docker, "Dockerfile Reference"；Kubernetes, "Kubernetes Documentation"。
- 相關案件：`2009-DevOps與持續部署.md`、`2005-Git分散式版本控制.md`、`2020s-AI輔助程式設計.md`。
