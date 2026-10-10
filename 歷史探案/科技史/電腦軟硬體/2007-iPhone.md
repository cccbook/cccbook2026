# 2007 - iPhone：觸控革命與智慧型手機的誕生

## 案件摘要
2007 年 1 月 9 日，Steve Jobs 在 Macworld 發表 iPhone，宣告「三項革命性產品」合一：寬螢幕觸控 iPod、革命性手機、突破性上網裝置。此案偵破的真相是：手機的未來不在按鍵，而在「一塊玻璃」——多點觸控螢幕加上真正的行動作業系統。

## 前因 -- 為什麼會有這個案子
- **iPod 的成功（2001–2007）**：Apple 靠 iPod + iTunes 證明自己能統合「硬體 + 軟體 + 服務」，累積了現金與信心；但 iPod 是單功能裝置，手機普及後「何必多帶一台」成為威脅。
- **Nokia 功能機的霸權**：2006 年 Nokia 佔全球手機市場約 35%，Symbian 系統以通話為中心、用 T9 實體鍵盤輸入，軟體生態封閉且碎片化。
- **Palm 與黑莓（BlackBerry）**：Palm Pilot 開創 PDA 與手寫辨識（Graffiti），黑莓以全鍵盤 + 推播郵件征服商務人士——證明「掌上運算」有需求，但都困在「鍵盤思維」。
- **技術成熟度**：電容式觸控、小型 ARM 處理器、鋰電池、行動通訊（2G/2.5G）在同時期到位，只欠一個整合者。

## 線索與推理 -- 數學式、程式、理論
### 三大發明
Jobs 稱 iPhone 具備三大革命：
1. **多點觸控（Multi-Touch）**：捨棄觸控筆與實體鍵盤，直接以手指操作。技術源頭可追溯至 FingerWorks 的手勢專利與 Jeff Han 的多點觸控研究。
2. **寬螢幕 UI**：3.5 吋 320×480 全螢幕介面，以「內容即介面」取代按鈕堆疊。
3. **行動 OS X**：跑在 ARM 上、裁剪自 Mac OS X 的 Unix 級作業系統（Darwin 核心），這是它與「功能機韌體」的根本差異。

### 觸控手勢的語言
iPhone 定義了一套至今通用的人機介面詞彙：`tap`（點選）、`double-tap`（縮放）、`swipe`（滑動換頁）、`pinch`（雙指捏合縮放）、`long-press`（長按）。以數學描述，捏合縮放的比例因子為兩指距離之比值：

$$s = \frac{d_t}{d_0} = \frac{\|p_{1,t} - p_{2,t}\|}{\|p_{1,0} - p_{2,0}\|}, \quad
\theta = \arctan\frac{y_{1,t}-y_{2,t}}{x_{1,t}-x_{2,t}}$$

其中 $d_0$ 是觸控開始時兩指距離，$d_t$ 是當前距離；$\theta$ 可同時用於雙指旋轉。

### Python：觸控座標與手勢判別
以下示範如何從一串觸控事件座標判別手勢型態（簡化的狀態機）：

```python
import math

def classify_gesture(touches):
    """touches: [(t, x, y), ...] 依時間排序的單指觸控序列"""
    if not touches:
        return "none"
    duration = touches[-1][0] - touches[0][0]
    path = sum(
        math.hypot(touches[i][1] - touches[i-1][1],
                   touches[i][2] - touches[i-1][2])
        for i in range(1, len(touches))
    )
    if len(touches) == 1 or (duration < 0.2 and path < 10):
        return "tap"
    if duration < 0.3 and abs(touches[-1][2] - touches[0][2]) < 10 and path > 30:
        return "swipe"
    if duration >= 0.5 and path < 10:
        return "long-press"
    return "drag"

def pinch_scale(p0, p1):
    """p0, p1: 開始與結束時的 [(x1,y1),(x2,y2)] 兩指座標"""
    d0 = math.hypot(p0[1][0]-p0[0][0], p0[1][1]-p0[0][1])
    d1 = math.hypot(p1[1][0]-p1[0][0], p1[1][1]-p1[0][1])
    return d1 / d0 if d0 > 0 else 1.0

print(classify_gesture([(0.0, 100, 200), (0.1, 101, 201)]))          # tap
print(classify_gesture([(0.0, 100, 400), (0.25, 102, 250)]))         # swipe
print(classify_gesture([(0.0, 100, 200), (0.6, 101, 202)]))          # long-press
print(round(pinch_scale([(50,300),(150,300)], [(25,300),(175,300)]), 2))  # 1.6
```

### ARM 晶片與行動 SoC
iPhone 1 代採用 Samsung S5L8900（ARM1176JZF-S 核心，約 412 MHz），整合 CPU、GPU（PowerVR MBX）、記憶體控制器於單晶片（SoC）。ARM 的 RISC 設計以「每瓦效能」取勝——其能效比可粗略表示為：

$$\eta = \frac{\text{MIPS}}{\text{Watt}} \approx \frac{f \cdot \text{IPC}}{C V^2 f} = \frac{\text{IPC}}{C V^2}$$

降低電壓 $V$ 對功耗是平方級的改善，這正是行動裝置選擇 ARM 而非 x86 的數學理由。（2010 年起 Apple 自研 A 系列 SoC，延續此路線。）

### App Store（2008）與應用生態
iPhone 初期只有內建 App 與 Web App；2008 年 7 月 App Store 上線，以 SDK + 審核 + 70/30 分成模式創造雙邊市場。開發者數與應用數相互增強，形成網路效應：

$$V(n) \approx k \cdot n^2$$

$n$ 為應用（或用戶）數量，價值隨平方成長——這是 Nokia Symbian 碎片化生態被擊潰的結構性原因。

## 結案 -- 後果與影響
- **Nokia 衰亡**：2007 年 Nokia 市值約 1,100 億美元，2013 年手機部門賣給微軟；霸主十年內消失。
- **智慧型手機取代 PC**：2014 年起全球行動上網流量超越桌面；2016 年智慧型手機出貨量遠超 PC，PC 產業進入長期衰退。
- **典範轉移**：介面從「檔案與視窗」轉為「觸控與 App」；軟體發行從「光碟安裝」轉為「商店下載」；運算從「桌面中心」轉為「口袋中心」。
- **深遠影響**：行動 SoC 軍備競賽（A 系列、Snapdragon）奠定日後 AI 手機的算力基礎；觸控手勢語言成為所有裝置（平板、車機、錶）的標準介面；App 經濟規模至 2020s 已達每年數千億美元。

## 關鍵人物與文獻
- **Steve Jobs**：2007-01-09 Macworld 主題演講（「An iPod, a phone, and an Internet communicator」）。
- **Scott Forstall**：iPhone 軟體負責人，行動 OS X 與 iOS SDK 的推手。
- **Tony Fadell**：iPod 之父、iPhone 硬體專案（後創 Nest）。
- **Jeff Han**：NYU 多點觸控展示（2006，TED 演講）；**FingerWorks**：手勢專利來源（2005 年被 Apple 收購）。
- 文獻：Isaacson, *Steve Jobs* (2011)；Fadell, *Build* (2022)；Apple "iPhone" 發表會影片（Apple 官方存檔）。
