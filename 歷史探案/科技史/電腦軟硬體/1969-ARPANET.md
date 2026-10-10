# 1969-ARPANET：網際網路的第一滴血

## 案件摘要
1969 年 10 月 29 日，UCLA 的電腦對 SRI 的電腦說出了「LO」——本想打 LOGIN，卻在輸入 G 時系統當機。這個未完成的單字，正是網際網路誕生時的第一聲啼哭。

## 前因 -- 為什麼會有這個案子
- **冷戰陰影**：1957 年蘇聯發射 Sputnik，美國成立 ARPA（高等研究計畫署），急欲在科技上反超。
- **通訊的脆弱性**：傳統電路交換（circuit switching）網路一旦中央節點被摧毀，全網癱瘓。Paul Baran（RAND）提出分散式通訊構想；英國的 Donald Davies 獨立提出並命名為 **packet switching（分封交換）**。
- **大學電腦互不相通**：ARPE 資助的大學各自擁有不同廠牌電腦，研究人員必須實體出差或郵寄磁帶共享資源。
- **解決方案**：ARPA 於 1968 年批准 ARPANET 計畫，由 BBN 公司建造 **IMP（Interface Message Processor，介面訊息處理器）**——每台主機經由 IMP 連上網路，IMP 負責分包、路由、重傳。1969 年 9 月第一部 IMP 進駐 UCLA，10 月第二部抵達 SRI。

## 線索與推理 -- 數學式、程式、理論

### 分封交換 vs 電路交換

| 特性 | 電路交換 | 分封交換 |
|------|----------|----------|
| 連線方式 | 先建立專屬通道（如傳統電話） | 無連線／虛電路，封包各自路由 |
| 頻寬利用 | 專屬保留，閒置即浪費 | 統計多工，動態共享 |
| 容錯性 | 單一節點故障即斷線 | 封包可繞道，天然抗毀 |
| 延遲 | 固定、可預測 | 變動、可能亂序 |
| 適用場景 | 即時語音 | 突發性資料傳輸 |

理論上，分封交換的延遲可近似 M/D/1 佇列模型：

$$W = \frac{\rho}{2(1-\rho)} \cdot \frac{1}{\mu}, \quad \rho = \frac{\lambda}{\mu}$$

其中 $\lambda$ 為封包到達率，$\mu$ 為服務率。當 $\rho \to 1$ 時延遲爆炸，這解釋了早期網路塞車現象。

### 那則「LO」訊息
程式設計師 Charley Kline 嘗試從 UCLA 的 SDS Sigma 7 對 SRI 的 SDS 940 打字「LOGIN」。每打一個字元，SRI 端就回音確認。打到 G 時，SRI 的 IMP 傳輸緩衝區出錯當機。「LO」成為史上第一則透過分封交換網路傳遞的訊息——約一小時後系統修復，LOGIN 成功。

用現代 Python 模擬這次「可靠傳輸」的回音機制：

```python
def send_message(host, msg, reliable=True):
    sent, acked = [], []
    for ch in msg:
        sent.append(ch)
        try:
            acked.append(host.echo(ch))   # 對方回音
        except ConnectionCrash:
            print(f"當機！最後送出: {''.join(sent)}")
            return ''.join(sent)
    return ''.join(acked)

class SRI_IMP:
    def __init__(self, buffer_size=3):
        self.buffer_size = buffer_size
    def echo(self, ch):
        if self.buffer_size <= 0:
            raise ConnectionCrash("SRI 當機")
        self.buffer_size -= 1
        return ch

print(send_message(SRI_IMP(), "LOGIN"))  # 輸出: LO（當機趣聞重現）
```

### 通往 TCP/IP 與 DNS
- **1974**：Vint Cerf 與 Bob Kahn 發表〈A Protocol for Packet Network Intercommunication〉，提出 **TCP**——讓不同網路互連（internetworking）的通用協定。
- **1983 年 1 月 1 日**：ARPANET 正式從 NCP 切換到 **TCP/IP**，史稱「flag day」。此後 TCP 負責可靠傳輸，IP 負責定址與路由：
  - IP 位址如同門牌：`192.168.1.1`
  - TCP 的三方交握（3-way handshake）：`SYN → SYN-ACK → ACK`
- **1983**：Paul Mockapetris 發明 **DNS（網域名稱系統）**，用階層式命名取代難記的數字位址，`www.ucla.edu` 經遞迴查詢解析為 IP。

## 結案 -- 後果與影響
- 1971 年電子郵件（Ray Tomlinson）成為 ARPANET 殺手級應用；1973 年已佔全網流量 75%。
- 1983 年 TCP/IP 切換後，ARPANET 成為網際網路骨幹；1989 年商用網路允許連入；1991 年 WWW 問世，網際網路飛入尋常百姓家。
- 1990 年 ARPANET 光榮退役，但它的協定（TCP/IP、DNS）至今仍是全球網路的 DNA。
- 分封交換「無連線、可繞道」的設計哲學，影響了後世所有分散式系統：區塊鏈、P2P、CDN 皆是其子孫。

## 關鍵人物與文獻
- **Paul Baran**：〈On Distributed Communications〉（1964，RAND 報告）
- **Donald Davies**：NPL 網路，命名 packet switching
- **Leonard Kleinrock**：UCLA 佇列理論，ARPANET 測量先驅
- **Vint Cerf & Bob Kahn**：〈A Protocol for Packet Network Intercommunication〉，IEEE Trans. Comm.（1974）——「網際網路之父」
- **Paul Mockapetris**：RFC 882/883（1983），DNS 之父
