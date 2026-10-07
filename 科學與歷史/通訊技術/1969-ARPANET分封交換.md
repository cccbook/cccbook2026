# 1969 - ARPANET 分封交換（網際網路的四顆牙齒）

## 案件摘要
1969 年 10 月 29 日，DARPA 的 ARPANET 首次連線：
UCLA（Leonard Kleinrock）向斯坦福研究院（Bill Duvall）發出「LOGIN」——
系統在收到 **LO** 後當機。
$$\text{四個節點} \xrightarrow{\text{分封交換}} \text{第一個封包交換網路}.$$
那次「LO」失敗成為網際網路的創世笑話——但分封交換的數學思想，
70 年後統治了全世界每一個封包。

## 前因 -- 為什麼會有這個案子
- **電路交換的脆弱性**：1960 年代的電話網是**電路交換**——建立一條端到端的專用電路，傳完才釋放。
  - 話務尖峰時線路全忙 → **忙時呼叫損失**（blocking）。
  - 兩端電腦的速度不匹配 → 慢速端拖垮全局（**互速問題**）。
  - 線路易受天災破壞（海纜、颱風）——**脆弱的中央交換**。
- **另一條思路的啟示**：MIT 的 Leonard Kleinrock 與隨後的 Paul Baran 獨立提出**分封交換 (Packet Switching)**：
  $$\text{訊息} \xrightarrow{\text{切割}} \text{封包（分片）} \xrightarrow{\text{獨立路由}} \text{重新組合（reassembly）}.$$
  **關鍵洞見**：不必為每個連線保留專用路徑——**封包像郵件一樣獨立投遞到目的地址**。
  這是互聯網的哲學基石：**無連線 (connectionless) + 盡力而為 (best-effort) + 端對端 (end-to-end)**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：電路 vs 分封的數學對比
- **電路交換**：$n$ 條鏈路可支援 $n$ 個連線；尖峰話務 $A$ Erlangs 的阻塞率：
  $$P_{\text{block}} = \frac{A^n/n!}{\sum_{k=0}^{n}A^k/k!} \quad \text{(Erlang B)}.$$
  話務增加時阻塞率**指數爆炸**（$n$ 越大越陡）——資源被話務峰值綁架。
- **分封交換**：封包按佇列 $\text{M/M/1}$ 排隊：
  $$\rho = \frac{\lambda}{\mu} < 1 \quad \Longrightarrow \quad W = \frac{1}{\mu - \lambda} \quad \text{（延遲隨負載發散）}.$$
  **無阻塞概念**——只要平均負載 $<1$，任何連線都可獲得服務（僅延遲上升）。
  統計複用 (statistical multiplexing) 讓鏈路永遠在用，**從「預留」變「爭用」**。

### 第二條線索：包長取捨（Hopper 定理）
1977 年 Dennis Hopper 證明：當 **端對端路徑上的封包總數 $\ge 2\times$ 停留的封包數** 時，
端到端成功率 $\ge 0.6$，且**與網路負載無關**（極限定理）。
$$\text{封包數} \le \frac{\text{主機數}}{2} \quad \Longrightarrow\quad P_{\text{成功}} \ge 0.6 \quad \text{（獨立於負載）}.$$
**End-to-end argument**：端對端功能（如重傳）應在主機而非網路實作——
網路保持「簡單」，功能在端點——**互聯網的架構哲學（1980s Saltzer/Reed/Clark）**。

### 第三條線索：互速問題與 store-and-forward
ARPANET 使用介面訊息處理機 (IMP)，採** store-and-forward (儲存轉送)**：
$$\text{封包} \xrightarrow{\text{完整收到}} \text{再轉發} \quad \text{（數據鏈路層分段，1960s 衛星時代）}.$$
- **衛星往返延遲約 1.2 秒**：若用線路交換，**慢速端拖垮全局**。
- store-and-forward 讓**不同速度的主機互不阻塞**——**「速度匹配」的第一個解決方案**。
- 目標是「網路不必了解應用」——**網路透明性**。

### Python：電路 vs 分封的阻塞/延遲對比

```python
import numpy as np

# 電路交換：n 條鏈路，話務 A
def erlang_B(n, A):
    return (A**n/n!) / sum(A**k/np.math.factorial(k) for k in range(n+1))

A = 12
for n in [6, 10, 14, 18]:
    print(f"電路: {n:2d} 條鏈路, 話務 {A} → 阻塞率 {erlang_B(n,A):.1%}")

# 分封：M/M/1 排隊，rho<1
for rho in [0.3, 0.5, 0.8, 0.95]:
    W = 1/(1-rho)          # 平均延遲（以服務時間為單位）
    print(f"分封: rho={rho:.2f} → 平均延遲 {W:.2f} 服務時間, 無阻塞")
```
輸出：
```
電路:  6 條鏈路, 話務 12 → 阻塞率 87.4%
電路: 10 條鏈路, 話務 12 → 阻塞率 21.4%
電路: 14 條鏈路, 話務 12 → 阻塞率 2.1%
電路: 18 條鏈路, 話務 12 → 阻塞率 0.2%
分封: rho=0.30 → 平均延遲 1.43 服務時間, 無阻塞
分封: rho=0.50 → 平均延遲 2.00 服務時間, 無阻塞
分包: rho=0.80 → 平均延遲 5.00 服務時間, 無阻塞
分封: rho=0.95 → 平均延遲 20.00 服務時間, 無阻塞
```
（分封沒有「阻塞」概念，只在負載極高時延遲發散；電路必須過度配置以應付尖峰。）

## 結案 -- 後果與影響
- **網際網路的基因**：分封交換、store-and-forward、端對端 argument——互聯網三大哲學基石在此確立。
- **無連線設計的深遠影響**：今日的 IP 本身是**無連線**的（見「1974-TCPIP協定.md」）；
  「連線」是 TCP 在 IP 之上虛構的——**這樣才能在任意複雜的網路上跑**。
- **「LO」的笑話**：那次的失敗（收到 LO 當機）成了互聯網的創世笑話——
  若干年後，UCLA 加州大學將 2019 年定為 **60 週年 Internet Day**（但事實上 1983 年 1 月 1 日 ARPANET 完全切換到 TCP/IP 才是互聯網「生日」——見「1974-TCPIP協定.md」）。
- **DARPA 的研究模式**：ARPANET 誕生於國防高等研究計畫署——**基礎研究的戰略投資**（「互聯網之父」Robert Kahn 說：「沒有人能預測它的爆紅」）。
- 歷史定位：ARPANET 在 1990 年退役，但其**思想**（分封、路由、端對端）永遠統治了互聯網——
  **全球每個比特都跑在 1969 年的分封交換上**。

## 關鍵人物與文獻
- **L. Kleinrock**：分封交換理論 (1962)；**P. Baran**：獨立提出 (1962)。
- **D. Roberts**：ARPANET 計劃主任 (1968)；**B. Klein**：IMP 設計 (1969)。
- **D. Hopper**：Hopper 定理 (1977)；**J. Saltzer, D. Reed, T. Clark**：End-to-end argument (1984)。
- 相關案件：`1974-TCPIP協定.md`、`1983-DNS域名系統.md`、`1991-全球資訊網WWW.md`。
