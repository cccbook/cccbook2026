# B.3 2025–2026 新名詞表：AI 原生 / AgentRun / FunctionAI / MCP / A2A / AI Serving Stack

本表每詞一行定義 + 對應章節，定位是「看到新聞能對回書裡位置」。詳細論述見 Ch 15–16。

| 名詞 | 一行定義 | 對應章節 |
|------|---------|---------|
| AI 原生 | 以模型與 Agent 為一等公民設計架構，而非把 AI 當外掛 | Ch 15.1 |
| AgentRun | AI Agent 的運行時框架：八大組件（運行時/網關/MQ/Memory/可觀測/評估/安全） | Ch 15.2 |
| FunctionAI | 讓 Agent 長時運行、有會話親和的 Serverless 函數形態 | Ch 15.3 |
| MCP | 模型上下文協議：Agent 調工具的統一接口標準 | Ch 15.4 |
| A2A | Agent 對 Agent 協議：多 Agent 互調與協作標準 | Ch 15.4 |
| AI Serving Stack | K8s 上的推理服務棧：vLLM/Triton + 調度 + 彈性 + 共享 | Ch 14.5 |
| AI 網關 | 推理入口：路由、Token 限流、多模型協議適配 | Ch 16.1 |
| Kagent | 跑在 Knative 上的 Agent 託管方案：Serverless 化 Agent | Ch 15.4 |

```bash
# 對應實驗速查
kubectl get pods -l app=ai-gateway       # AI 網關是否在線（Ch 16.1）
kubectl get ksvc                          # Knative 託管的 Agent（Ch 15.4）
kubectl top pods --sort-by=memory         # 推理服務顯存壓力（Ch 14.2）
```

## 記憶口訣

- 兩協議：MCP（調工具） vs A2A（調 Agent）。
- 兩運行：AgentRun（框架） vs FunctionAI（函數形態）。
- 兩入口：AI 網關（流量） vs AI Serving Stack（推理服務）。

## 易混淆辨析

| 對比 | 差異一句話 | 例子 |
|------|-----------|------|
| MCP vs A2A | MCP 連工具，A2A 連 Agent | 查庫存調 MCP；導購 Agent 調客服 Agent 用 A2A |
| AgentRun vs FunctionAI | 前者是框架全家桶，後者是函數運行形態 | 八大組件 vs 長時會話親和 |
| AI 網關 vs API 網關 | 新增 Token 限流與多模型適配 | OpenAI 協議轉 Anthropic（Ch 16.1） |
| AI Serving Stack vs 普通 Deployment | 多了 GPU 調度、共享與彈性 | vLLM + MIG + HPA（Ch 14.2/14.5） |

## 新舊對照（舊知識如何遷移）

| 舊（Ch 5–11） | 新（Ch 15–16） | 遷移要點 |
|--------------|---------------|---------|
| API 網關（Ch 6.3） | AI 網關 | 加推理路由與 Token 計費 |
| MQ 削峰（Ch 6.2） | AI MQ | 改傳 Prompt/上下文，保會話順序 |
| HPA（Ch 11.2） | KEDA + GPU 彈性 | 按隊列長度與 Token 速率擴縮 |
| 微服務可觀測（Ch 13.2） | Agent 可觀測/評估 | 加 Trace 到工具調用、加評分迴路 |

```bash
# 看到新聞時的三問
# 1. 它是協議 / 運行時 / 網關哪一類？ 2. 對應本書哪章？ 3. 解決什麼瓶頸？
kubectl get gatewayclass            # AI 網關底座（Gateway API，Ch 16.1）
kubectl get scaledobjects           # KEDA 彈性物件（Ch 11.2 / 15.3）
```

## 本章小結

- 8 個詞分三組記：協議組、運行組、服務組。
- 凡是「網關」「MQ」「可觀測」前面加 AI，大多是舊雲原生件的 AI 化（Ch 16.2）。
- 面試被問到任一詞，先說定義，再說「對應本書哪章、解決什麼瓶頸」。

## 想一想

1. MCP 與 A2A 一句話區別是什麼？各舉一個本書場景。
2. 為什麼 Agent 需要 FunctionAI 的「長時運行 + 會話親和」？普通 FaaS 缺什麼？
3. AI 網關與傳統 API 網關（Ch 6.3）最大的新增職責是什麼？
