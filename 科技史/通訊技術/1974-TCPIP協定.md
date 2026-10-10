# 1974 - TCP/IP 協定（互聯網的「共同語言」）

## 案件摘要
1974 年 12 月，Vint Cerf 與 Bob Kahn 發表〈A Protocol for Packet Network Intercommunication〉：
定義 **TCP**（傳輸控制協定）與 **IP**（網際協定）——讓**不同類型的網路**能互相連接。
$$\text{網際網 (internet)} = \text{網路 (net)} + \text{際 (inter) ——\quad \text{不是「一個大網」}.$$
1983 年 1 月 1 日「Flag Day」，ARPANET 全面切換到 TCP/IP——
**這一天才是互聯網的真正生日**。

## 前因 -- 為什麼會有這個案子
- **網路的碎片化**：1970 年代初，ARPANET 的 IMP 網、PRNET（Packet Radio Network）、SATNET 各自使用**不同的封包格式與協定**——
  要把一個包裹從 PRNET 送到 SATNET，需要**協定轉換閘**，每個閘都可能有錯、都有延遲。
  **N 個網路需要 $N(N-1)$ 個轉換閘**（完全連接的複雜度）。
- **Cerf & Kahn 的偵探直覺**（分層 + 端對端）：
  1. **遮蔽差異**：IP 層面盡可能「隱藏」底下用什麼網路——只要求「能送 500-bit 封包」的最低公倍数能力。
  2. **不做關係**：不在網路內做重傳、流量控制——這些是**端對端**的功能（見「1969-ARPANET分封交換.md」的端對端 argument）。
  3. **閘門變少**：$N$ 個網路只需 $N$ 個網際網關：
  $$\text{完全連接} = N(N-1) \text{ 閘} \quad \text{vs} \quad \text{網際網} = N \text{ 閘}.$$
- **「網際網」vs「網路」**——一次字義的澄清，決定了互聯網的終生。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：分層與端對端（設計哲學）
Cerf & Kahn 論文標題就是 “Packet Network **Inter**communication”——**核心是遮蔽底層差異**。

$$\text{傳輸層 (TCP)} = \text{端到端可靠} \quad \text{vs} \quad \text{網際層 (IP)} = \text{盡力而為、不可靠}.$$

### 第二條線索：不可靠 IP 的設計（關鍵選擇）
IP 本身**不重傳、不保序**——**為什麼？** 端到端論證（Saltzer/Reed/Clark 1984 的正式化）：
- **網路不該假裝可靠**：如果路由器做重傳，則所有流量都承擔重傳成本（包括大部分不需要的）。
- **重傳的話**：TCP 在端點重傳。若路徑上的某段無故障，重傳是**冗餘但便宜**（端到端可恢復）；若全網可靠但端點錯誤，錯誤**無從得知**。
- **結論**：**功能放在端對端**，能滿足端到端需求的放在端點；中間網路只提供「盡力」——**現代互聯網的根本原則**。
$$\boxed{\text{網路：盡力而為（best-effort）}\quad\text{端點：可靠（end-to-end）}}$$

### 第三條線索：IPv4 位址與分封
IPv4 標頭 32-bit 位址，支援最大 $2^{32}$ 個位址——**不夠用（1980s 開始爆量）**——
直接導致 30 年後的 IPv6 過渡問題。
$$\text{位址空間} = 2^{32} = 4.3\times10^9 \quad \text{vs 1990s 開始的使用者數}.$$

### 第四條線索：TCP 三向握手與可靠傳輸
TCP 三向握手（SYN, SYN-ACK, ACK）建立連線，序列號 (sequence number) 確保**不重複、不遺漏、不失序**：
$$\text{確認機制} = \text{ACK} \text{（收到對方 seq 為 } k \text{ 的封包，ACK 回 } k+1\text{）}.$$
可靠性的三要素：序號 + 確認 + 重傳（重傳計時器 RTO + 快速重傳 fast retransmit）。

### Python：TCP 三向握手 + 可靠傳輸的簡易示範

```python
import socket, threading, time, struct, random

def handshake_sim():
    """三向握手模擬：SYN → SYN-ACK → ACK"""
    print("client → server: SYN (seq=0)")
    print("server → client: SYN-ACK (seq=0, ack=1)")
    print("client → server: ACK (ack=1)")
    print("→ 連線建立 (三次握手完成)\n")

def stop_and_wait(n_pkts=5, loss_prob=0.2):
    """可靠傳輸：停等 + 超時重傳"""
    print(f"可靠傳輸 (停等 + 重傳, 丟包率 {loss_prob}):")
    for i in range(1, n_pkts+1):
        for attempt in range(1, 4):
            lost = random.random() < loss_prob
            if not lost:
                print(f"  pk{i} 送達（嘗試 {attempt}）")
                break
            print(f"  pk{i} 遺失 → 超時重傳 (嘗� {attempt})")
        time.sleep(0.1)

random.seed(1)
handshake_sim()
stop_and_wait()
```
輸出：
```
client → server: SYN (seq=0)
server → client: SYN-ACK (seq=0, ack=1)
client → server: ACK (ack=1)
→ 連線建立 (三次握手完成)

可靠傳輸 (停等 + 重傳, 丟包率 0.2):
  pk1 遺失 → 超時重傳 (嘗 1)
  pk1 送達（嘗試 2）
  pk2 送達（嘗試 1）
  ...
```
（TCP 三向握手 + 停等重傳——可靠傳輸的兩個基本組塊。）

## 結案 -- 後果與影響
- **互聯網的統一（1983 Flag Day）**：全球的網路「說同一種語言」——這是**全球資訊化的基礎設施**。
- **網際網的爆炸式增長**：1990s 的商用 ISP、1990s 末的全球網站、2000s 的 Web 2.0、2010s 的雲端與行動——全部在 TCP/IP 之上。
- **TCP 的「拼湊哲學」**（End-to-End argument 的實踐）：IP 盡力、TCP 可靠、HTTP 無狀態——**每一層只做自己的事**。
- **「一切皆 IP」的時代**：2010s 起的 **VXLAN/overlay**、服務网格、雲原生網路（Kubernetes CNI）——**都在 TCP/UDP/IP 之上加**。
- **IPv6 的漫長過渡**：因為 TCP/IP 成功到人人用，IPv4 位址不夠（$2^{32}$）→ IPv6（$2^{128}$）2000s 開始部署，至今仍未完成——
  **互聯網最著名的「未竟工程」**（這是 TCP/IP 設計的必然副作用：全球的信任使得升級極難）。
- 歷史加冕：**Bob Kahn 獲 2004 年圖靈獎**（與 Vint Cerf 同獲）；Cerf 稱互聯網是「他一生中最偉大的作品」——
  **一份論文 + 30 年執行的成果，改變了人類文明的形態**。

## 關鍵人物與文獻
- **V. Cerf & R. Kahn**：〈A Protocol for Packet Network Intercommunication〉, IEEE Trans. Comm. 22, 639 (1974)；2004 圖靈獎。
- **J. Saltzer, D. Reed, T. Clark**：〈End-to-end arguments in system design〉, ACM TOCS 2 (1984)——分層哲學的正式化。
- 相關案件：`1969-ARPANET分封交換.md`、`1983-DNS域名系統.md`、`1991-全球資訊網WWW.md`。
