# A.3 kubectl 與 YAML 速查

對應 Ch 9–11。本節只收「考試與實驗會用到的 20%」，熟練這張表就能跟完全書 K8s 實驗。

## 高頻命令（背下來）

```bash
kubectl get pods -o wide              # 看 Pod 落在哪
kubectl get deploy,svc,ingress        # 一次看三種
kubectl describe pod <pod>            # Pending / CrashLoop 先看它
kubectl logs -f deploy/shop --tail=100
kubectl exec -it <pod> -- sh          # 進容器排查
kubectl apply -f shop.yaml            # 宣告式部署（本書標準）
kubectl delete -f shop.yaml
kubectl rollout status deploy/shop
kubectl rollout undo deploy/shop      # 回滾（Ch 9.4）
kubectl top pods                      # 要先裝 metrics-server
kubectl scale deploy shop --replicas=5
```

| 動詞 | 用途 | 例子 |
|------|------|------|
| get | 查狀態 | `get pods -A` |
| describe | 查詳情與事件 | `describe svc shop` |
| apply | 部署/更新 | `apply -f shop.yaml` |
| logs | 看日誌 | `logs -l app=shop` |
| exec | 進容器 | `exec -it <pod> -- sh` |
| scale | 擴縮 | `scale deploy shop --replicas=5` |

## 最小 YAML 四件套

```yaml
# Deployment（Ch 9.3）：管副本與滾動更新
apiVersion: apps/v1
kind: Deployment
metadata: {name: shop}
spec:
  replicas: 3
  selector: {matchLabels: {app: shop}}
  template:
    metadata: {labels: {app: shop}}
    spec:
      containers:
      - name: shop
        image: shop:v1
        ports: [{containerPort: 8080}]
```

```yaml
# Service（Ch 10.1）：集群內固定入口
apiVersion: v1
kind: Service
metadata: {name: shop}
spec:
  selector: {app: shop}
  ports: [{port: 80, targetPort: 8080}]
```

```yaml
# Ingress（Ch 10.2）：對外路由
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: {name: shop}
spec:
  rules:
  - host: shop.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend: {service: {name: shop, port: {number: 80}}}
```

```yaml
# HPA（Ch 11.2）：按 CPU 自動擴縮
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: {name: shop}
spec:
  scaleTargetRef: {apiVersion: apps/v1, kind: Deployment, name: shop}
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource: {name: cpu, target: {type: Utilization, averageUtilization: 60}}
```

## 排錯流程（固定三步）

```bash
kubectl get pods                        # 1. 先看狀態：Pending / CrashLoop / OOMKilled？
kubectl describe pod <pod>              # 2. 看 Events：鏡像拉不到？探針失敗？
kubectl logs <pod> --previous           # 3. 看上次崩潰前日誌
```

| 現象 | 排查 | 常見解法 |
|------|------|---------|
| ImagePullBackOff | `describe` 看 Events | 修正 image 名、補 imagePullSecrets |
| CrashLoopBackOff | `logs --previous` | 修啟動命令、補環境變數 |
| OOMKilled / Service 不通 | `describe` + `get endpoints shop` | 調 limits、對齊 selector（Ch 11.3） |

## 本章小結

- 六命令：get / describe / apply / logs / exec / scale；四 YAML：Deployment / Service / Ingress / HPA；排錯：狀態 → Events → 日誌。
## 練一練

1. 用本節四段 YAML 部署 shop，`get pods -o wide` 確認 3 副本分散，再 `scale` 到 1 副本觀察變化。
2. 故意把 image 寫錯一個字，用三步排錯法定位到 ImagePullBackOff 並修復。
3. 加一條 HPA（60% CPU），用 `kubectl top pods` 觀察，並說明 HPA 與 `scale` 手動擴縮的關係。
