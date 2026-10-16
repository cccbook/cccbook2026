# 演進式架構實戰：從單體、微服務到 Docker、Kubernetes 與 AI 雲原生轉型

> 問題驅動（Problem-Driven）：不先拋 Docker / K8s 概念，而是重現從 100 併發到千萬級併發的 14 次架構演進，讓讀者在堆疊的運維痛點中，自然產生「這裡必須用容器與編排來解決」的需求。
> 情境載體：以淘寶架構演變簡史為主線（教學模型，非淘寶真實路徑），一路銜接至 Serverless、FinOps 與 AI 雲原生。

## 第一篇：單體與集中式架構（從零到一）

- 一、單體架構的起點與極限
   - [1.1 淘寶初期的 Web 架構：單機 Tomcat + 資料庫](1.1.md)
   - [1.2 第一次演進：Web 伺服器與資料庫分離部署](1.2.md)
   - [1.3 應用伺服器的效能瓶頸：CPU、內存與 I/O 競爭](1.3.md)
   - [1.4 單體什麼時候不夠用：擴展性 vs 效能](1.4.md)

- 二、引入快取與快取一致性
   - [2.1 資料庫讀寫瓶頸與快取救星](2.1.md)
   - [2.2 本地快取與分散式快取：Memcached / Redis / Tair](2.2.md)
   - [2.3 快取實戰痛點：穿透、擊穿、雪崩與熱點失效](2.3.md)
   - [2.4 快取與資料庫的一致性難題](2.4.md)

## 第二篇：規模化與資料庫拆分（Scale-out）

- 三、無狀態應用與負載均衡
   - [3.1 反向代理與 Web 集群：Nginx / HAProxy](3.1.md)
   - [3.2 無狀態設計與 Session 共享](3.2.md)
   - [3.3 四層與七層負載的搭配：LVS / F5 + Keepalived](3.3.md)
   - [3.4 機房入口：DNS 輪詢、CDN 與異地多活基礎](3.4.md)

- 四、資料庫的高可用與分庫分表
   - [4.1 讀寫分離與主從同步：Mycat 與資料一致性](4.1.md)
   - [4.2 按業務垂直分庫：降低資源競爭](4.2.md)
   - [4.3 大表拆小表：Hash / 時間分片與水平擴展](4.3.md)
   - [4.4 拆分後的代價：分散式事務、跨庫 Join 與 MPP 資料庫](4.4.md)

## 第三篇：服務化與微服務架構（SOA & Microservices）

- 五、拆分單體：垂直應用與微服務抽離
   - [5.1 大應用拆小應用：業務邊界與 DDD 簡介](5.1.md)
   - [5.2 公共模組服務化：Dubbo / Spring Cloud RPC](5.2.md)
   - [5.3 分散式協調：Zookeeper / Nacos 配置中心與服務發現](5.3.md)
   - [5.4 微服務三板斧：限流、熔斷與降級](5.4.md)

- 六、多樣化數據與服務治理
   - [6.1 異構儲存：HDFS / HBase / Elasticsearch / 大數據場景](6.1.md)
   - [6.2 訊息佇列：RocketMQ / Kafka 異步解耦與削峰](6.2.md)
   - [6.3 ESB 與 API Gateway：統一協議與路由](6.3.md)
   - [6.4 傳統微服務運維地獄：環境不一致與部署死胡同](6.4.md)

## 第四篇：容器化革命（Docker 入門與銜接）

- 七、打破部署地獄：Docker 容器技術登場
   - [7.1 虛擬機 vs 容器：本質差異與隔離模型](7.1.md)
   - [7.2 Docker 三要素：Image / Container / Repository](7.2.md)
   - [7.3 編寫 Dockerfile：把微服務打包為標準單元](7.3.md)
   - [7.4 Docker Compose 實戰：一鍵啟動 微服務 + Redis + MySQL + Nginx](7.4.md)

- 八、Docker 網路與儲存管理
   - [8.1 Docker 網路模型：Bridge / Host / Overlay](8.1.md)
   - [8.2 數據持久化：Volume 與 Bind Mount](8.2.md)
   - [8.3 單機容器的極限：成百上千容器誰來管](8.3.md)

## 第五篇：雲原生編排（Kubernetes 實戰）

- 九、雲原生指揮官：Kubernetes 核心架構
   - [9.1 為什麼需要容器編排](9.1.md)
   - [9.2 K8s 架構解密：Control Plane 與 Worker Node](9.2.md)
   - [9.3 核心物件入門：Pod / ReplicaSet / Deployment](9.3.md)
   - [9.4 重新定義部署：滾動更新與版本回滾](9.4.md)

- 十、K8s 服務發現、路由與儲存
   - [10.1 Service：ClusterIP / NodePort / LoadBalancer](10.1.md)
   - [10.2 對外入口：Ingress 與雲原生網關 Envoy / Higress](10.2.md)
   - [10.3 服務網格：Istio 無侵入治理與 mTLS](10.3.md)
   - [10.4 儲存與配置：PV / PVC / StorageClass / ConfigMap / Secret](10.4.md)

- 十一、彈性擴縮與自癒系統
   - [11.1 自癒：Liveness 與 Readiness 探針](11.1.md)
   - [11.2 應對大促：HPA / Cluster Autoscaler / KEDA](11.2.md)
   - [11.3 資源治理：Requests & Limits 與 OOM 防護](11.3.md)
   - [11.4 多機房多集群：Affinity / Taints / Tolerations / Karmada](11.4.md)

## 第六篇：最新進展——Serverless、FinOps 與 AI 雲原生

- 十二、現代微服務反思：Serverless 與模組化單體
   - [12.1 微服務過度拆分的技術債](12.1.md)
   - [12.2 模組化單體的復興：幾時該拆、幾時該合](12.2.md)
   - [12.3 全面 Serverless 化：Knative 與冷啟動優化](12.3.md)
   - [12.4 從微服務到 FaaS：前端與業務平台實踐](12.4.md)

- 十三、雲原生生態：GitOps、可觀測性與 FinOps
   - [13.1 GitOps 持續部署：ArgoCD 實戰](13.1.md)
   - [13.2 可觀測性三支柱：Log / Metric / Trace 與 OpenTelemetry](13.2.md)
   - [13.3 成本治理 FinOps：混部與資源利用率](13.3.md)
   - [13.4 公有雲託管 K8s：ACK / EKS / GKE 最佳實踐](13.4.md)

- 十四、AI 時代的架構革新
   - [14.1 從千人千面到生成式 UI 與 AI Agent 導購](14.1.md)
   - [14.2 K8s 調度 GPU：vGPU / MIG / RDMA 高速網路](14.2.md)
   - [14.3 推理服務雲原生部署：vLLM / Triton + K8s](14.3.md)
   - [14.4 邊緣與 WASM：輕量容器在邊緣路由的應用](14.4.md)
   - [14.5 雲原生 AI 推理棧新進展：AI Serving Stack / 機密推理 / GPU 共享與彈性](14.5.md)

- 十五、最新進展一：AI 原生應用架構與 Agent Infra（🆕 2025–2026）
   - [15.1 從雲原生到 AI 原生：2025 白皮書與雲智一體](15.1.md)
   - [15.2 AgentRun 八大組件：AI 運行時 / AI 網關 / AI MQ / Memory / 可觀測 / 評估 / 安全](15.2.md)
   - [15.3 FunctionAI 與 Agent Infra：AWS AgentCore / Azure / FunctionAI 長時運行與會話親和](15.3.md)
   - [15.4 MCP / A2A / Kagent on Knative：Agent 協議的 Serverless 託管](15.4.md)

- 十六、最新進展二：AI 網關、AIOps 與淘寶實戰（🆕 2025–2026）
   - [16.1 AI 網關：推理路由、Token 限流、多模型協議適配與 Gateway API](16.1.md)
   - [16.2 AI 中間件演進：Spring AI Alibaba / Higress / MSE / RocketMQ](16.2.md)
   - [16.3 淘寶 AI OS 實戰：搜索推薦全圖架構、RTP / XDL / OpenSearch 百萬 QPS](16.3.md)
   - [16.4 淘寶最新落地：Node.js Serverless 核心鏈路、智能客服亞秒級、Wenwen 生成式導購](16.4.md)

- 十七、總結與前瞻：ACK 新能力與未來
   - [17.1 ACK 2025–2026 新能力：Auto Mode / Virtual Node / ACK One 多集群 / AI Assistant](17.1.md)
   - [17.2 全景複盤：單體 → 分散式 → 微服務 → 雲原生 → AI 原生](17.2.md)
   - [17.3 技術選型白皮書：避免為了雲原生 / AI 而雲原生 / AI](17.3.md)
   - [17.4 架構設計原則：N+1、回滾、禁用、監控、多活、水平擴展、FinOps 與 AI 安全](17.4.md)

## 附錄

- 附錄 A：實驗環境與工具速查
   - [A.1 本地實驗環境：Docker Desktop / kind / minikube](A.1.md)
   - [A.2 Dockerfile 與 Compose 速查](A.2.md)
   - [A.3 kubectl 與 YAML 速查](A.3.md)

- 附錄 B：對照表與案例集
   - [B.1 淘寶 14 次演進 vs 本書章節對照表](B.1.md)
   - [B.2 雙十一大促案例：削峰、降級與彈性擴縮](B.2.md)
   - [B.3 2025–2026 新名詞表：AI 原生 / AgentRun / FunctionAI / MCP / A2A / AI Serving Stack](B.3.md)
   - [B.4 架構演進教學指引：如何用本書上課](B.4.md)
