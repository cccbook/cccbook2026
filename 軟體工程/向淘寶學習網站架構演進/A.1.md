# A.1 本地實驗環境：Docker Desktop / kind / minikube

本書所有實驗只需一台筆電（8 核 / 16GB 記憶體建議）。三種本地環境定位不同：Docker Desktop 求快，kind 求貼近 CI 與多節點，minikube 求功能全（Ingress、Addon）。

## 三者對比一覽

| 項目 | Docker Desktop | kind | minikube |
|------|---------------|------|----------|
| 本質 | 桌面版 Docker + 內嵌單節點 K8s | 用 Docker 容器跑 K8s 節點 | 本地 VM / Docker 驅動跑完整 K8s |
| 優點 | 安裝最簡單，Compose 最順 | 啟動快，多節點、CI 友善 | Addon 豐富，貼近真實集群 |
| 缺點 | 吃資源、多節點難 | 無內建 Ingress、Registry 要另配 | 啟動較慢、較吃資源 |
| 適合章節 | Ch 7–8（Docker、Compose） | Ch 9–11（Deployment、HPA） | Ch 10–11（Ingress、Storage、KEDA） |

## 安裝與啟動

```bash
# 共通：確認 Docker 可用
docker version
docker run --rm hello-world
```

```bash
# 方案一：Docker Desktop（含 Kubernetes）
# 官網下載安裝後，在 Settings > Kubernetes 勾選 Enable Kubernetes
kubectl config use-context docker-desktop
kubectl get nodes
```

```bash
# 方案二：kind（推薦做 Ch 9–11 實驗）
brew install kind kubectl        # macOS；Linux 改用 apt / Windows 用 choco
kind create cluster --name lab --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
EOF
kubectl cluster-info --context kind-lab
```

```bash
# 方案三：minikube（要玩 Ingress / Addon 時用）
brew install minikube            # 或見官網安裝包
minikube start --driver=docker --cpus=4 --memory=8192
minikube addons enable ingress
minikube addons enable metrics-server
kubectl get nodes
```

## 驗證命令（任選一種環境，逐行通過即合格）

```bash
kubectl version --client
kubectl get nodes -o wide
kubectl create deployment hello --image=nginx:1.25 --replicas=2
kubectl get pods -o wide
kubectl expose deployment hello --port=80 --type=NodePort
kubectl get svc hello
kubectl delete deployment hello && kubectl delete svc hello
```

## 切換與清理

```bash
kubectl config get-contexts
kubectl config use-context kind-lab   # 在 docker-desktop / minikube 間切換
kind delete cluster --name lab
minikube stop && minikube delete
docker system prune -f
```

## 常見排錯

| 症狀 | 排查命令 | 解法 |
|------|---------|------|
| kubectl 連不上 | `kubectl config current-context` | 切到正確 context |
| Pod 一直 Pending | `kubectl describe pod <name>` | 記憶體不足，調小 replicas 或重啟集群 |
| Port 被佔用 | `lsof -i :8080` / `docker ps` | 換 `--port` 或停掉舊容器 |
| minikube 太慢 | `minikube status` | 改 `--driver=docker`，加 CPU/記憶體 |

## 本章小結

- Docker Desktop 入門最快；kind 最適合練 Deployment 與 HPA；minikube 最適合練 Ingress 與 Addon。
- 驗證標準：`get nodes` 就緒 + 能跑起 2 副本 nginx 並 expose 成功。
- 筆電資源不足時，一次只保留一個本地集群。

## 練一練

1. 分別用 kind（2 worker）與 minikube 啟動集群，比較 `kubectl get nodes` 輸出與啟動耗時，記錄差異。
2. 在任一集群部署 2 副本 nginx，用 `kubectl get pod -o wide` 觀察 Pod 落在哪個 Node，再 scale 到 5 副本觀察變化。
3. 故意切錯 context（`use-context` 切到不存在的），再用 `get-contexts` 與排錯表把它修好。
