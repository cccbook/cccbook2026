# 1984-Macintosh與GUI

## 案件摘要
1984 年 1 月 24 日，Macintosh 隨著超級盃「1984」廣告問世。這台機器的每個點子——視窗、滑鼠、圖示、下拉選單——都不是蘋果發明的，而是從 Xerox PARC「偷」來的。案件的本質是：**偉大的發明者沒有賺到錢，最好的整合者改變了世界**。

## 前因 -- 為什麼會有這個案子
- 命令列（CLI）時代：電腦只聽得懂 `COPY A: B:` 這類咒語，普通人根本無法使用。
- 1968 年 Engelbart 的「所有演示之母」展示滑鼠與超連結；1973 年 Xerox PARC 做出 Alto——第一台 GUI 電腦。
- Xerox 高層看不懂自家寶藏，PARC 的發明被鎖在實驗室裡。
- 1979 年，Jobs 以讓 Xerox 投資蘋果（100 萬美元）為條件，換得進入 PARC 朝聖。

## 線索與推理 -- 數學式、程式、理論
### 線索一：Xerox Alto 與 PARC 的 GUI 發明
Alto（1973）已具備 GUI 的全部要素：
- **WYSIWYG**（What You See Is What You Get）：螢幕上的文件就是列印結果。位元映射顯示器（bitmapped display）是前提：解析度 $W \times H$ 的螢幕需要 $W \times H$ 位元的顯示記憶體，Alto 為 $606 \times 808 \approx 490\,\text{Kb}$。
- **滑鼠**：Engelbart 1964 年發明，PARC 改良為三鍵光學滑鼠。
- **重疊視窗（overlapping windows）與下拉選單**：Alan Kay 的 Smalltalk 環境首創。
- PARC 還發明了乙太網路與雷射印表機——整座金山卻沒人開採。

### 線索二：Jobs 的 PARC 朝聖（1980）
Jobs 看到圖形介面的第一反應是：「你們坐在一座金礦上！」他立刻把構念帶回蘋果，先用在 Lisa（1983，售價 $9{,}995$ 美元，商業上失敗），再簡化為 Macintosh。這就是所謂「好的藝術家抄襲，偉大的藝術家偷竊」：

$$\text{價值} = \text{發明} \times \text{整合} \times \text{量產}$$

Xerox 有發明（$\times 1$），蘋果補上後兩項（$\times 1$），因此 $V_{Apple} \gg V_{Xerox}$。

### 線索三：Macintosh 的設計
- **CPU**：Motorola 68000，32-bit 內部架構（16-bit 匯流排），7.83 MHz。
- **RAM**：128KB——這是刻意壓低的成本妥協，也成為 Mac 早期最大的限制。
- **ROM**：64KB，內含 QuickDraw 圖形函式庫與 Toolbox，實現「ROM 裡的 GUI」。
- 記憶體預算的殘酷數學：

$$\underbrace{128\,\text{KB}}_{\text{總 RAM}} = \underbrace{22\,\text{KB}}_{\text{系統}} + \underbrace{\approx 42\,\text{KB}}_{\text{顯示緩衝區 } 512 \times 342 / 8} + \text{僅剩約 } 64\,\text{KB 給應用程式}$$

### 線索四：GUI 的心理學與易用性革命
GUI 的理論基礎是「直接操縱」（direct manipulation，Shneiderman）：物件可見、動作即時回饋、以辨識取代記憶。用認知負荷理論量化：

$$\text{總認知負荷} = \text{內在負荷} + \text{外在負荷（extraneous load）}$$

CLI 要求使用者「記憶」命令語法（高外在負荷）；GUI 讓使用者「辨識」圖示與選單（低外在負荷）。心理學的法則：**辨識遠比回憶容易**（recognition over recall）。這就是易用性革命的數學核心。

### 線索五：圖形介面 vs 命令列的對照表

| 任務 | CLI（DOS） | GUI（Macintosh） |
|---|---|---|
| 複製檔案 | `COPY A:FILE.TXT B:` | 拖曳圖示到磁碟圖示上 |
| 刪除檔案 | `DEL FILE.TXT` | 把圖示丟進垃圾桶 |
| 開啟程式 | 記住路徑鍵入 `WORD` | 雙擊圖示 |
| 學習曲線 | 需數週背命令 | 數分鐘即可上手 |
| 回饋方式 | 文字訊息、錯誤代碼 | 視覺即時回應（WYSIWYG） |

以 Python 模擬 GUI 的事件迴圈概念——GUI 程式的本質是「事件驅動」而非「流程驅動」：

```python
# GUI 事件迴圈的概念模型（Macintosh Toolbox 的精神）
events = ["mouse_down(icon='file')", "drag(to='trash')", "mouse_up"]

while True:
    if not events:
        break
    e = events.pop(0)      # 從事件佇列取事件
    dispatch(e)            # 分派給對應的物件處理
    redraw()               # 重繪畫面（即時回饋）
```

## 結案 -- 後果與影響
- Macintosh 銷量初期平平（128KB 記憶體太少、無軟體生態），但 LaserWriter 與 PageMaker（1985）開創桌上排版（DTP）市場救了它。
- GUI 從此成為主流：1985 Windows 跟進、1989 Mac 介面訴訟（Apple v. Microsoft）敗訴，GUI 觀念成為公共財。
- Xerox PARC 成為「發明者的墳墓、朝聖者的聖地」的永恆寓言；管理學稱之為「創新者的窘境」原型之一。
- 易用性（usability）成為產品設計的第一指標，奠定 HCI（人機互動）學科地位。
- 1997 年 Jobs 回歸後，封閉整合路線在 iMac、iPhone 上完成復仇——證明 GUI 案的長期解答是「體驗整合」而非「開放零組件」。

## 關鍵人物與文獻
- **Douglas Engelbart**：滑鼠發明人，「所有演示之母」（1968）。
- **Alan Kay**：Smalltalk、重疊視窗、「預測未來最好的方式就是發明它」。
- **Steve Jobs**：PARC 朝聖與 Macintosh 產品定義。
- **Bill Atkinson**：QuickDraw 與 MacPaint 的作者，Mac GUI 的總工程師。
- **Jef Raskin**：Macintosh 專案發起人，「以人為本」易用性主張。
- 文獻：Kay, *The Early History of Smalltalk* (1993)；Atkinson 的 QuickDraw 文件；Isaacson, *Steve Jobs* (2011)；Hiltzik, *Dealers of Lightning* (1999)。
