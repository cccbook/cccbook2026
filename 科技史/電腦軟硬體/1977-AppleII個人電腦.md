# 1977-AppleII個人電腦

## 案件摘要
1977 年，Apple II、Commodore PET、TRS-80 同年問世，史稱「1977 三傑」。電腦第一次離開機房、走進家庭，個人電腦（PC）時代正式開幕。兩年後 VisiCalc 現身，讓 Apple II 從玩具變成生財工具。

## 前因 -- 為什麼會有這個案子
- 1971 年 Intel 4004、1974 年 Intel 8080 問世，微處理器讓「一顆晶片 = 一台電腦的大腦」成為可能。
- 1975 年 Altair 8800 套件掀起業餘電腦熱潮，但沒有鍵盤、螢幕、軟體，只能撥開關輸入機器碼。
- Homebrew Computer Club（車庫俱樂部）聚集了 Wozniak、Jobs 等人，人人夢想「擁有一台自己的電腦」。
- 1976 年， Jobs 與 Wozniak 在車庫中創立 Apple，推出手工拼裝的 Apple I——只是一塊電路板，仍不算完整產品。

## 線索與推理 -- 數學式、程式、理論
### 線索一：Wozniak 的工程天才
Wozniak 以極少晶片做出驚人功能：
- **彩色圖形**：Apple II 用一顆 NTSC 視訊產生器，巧妙利用像素與色載波相位差產生彩色。若視訊頻率為 $f_{sc} \approx 3.579545\,\text{MHz}$（NTSC 色副載波），像素位移半個週期，色相偏移：

$$\Delta\phi = 2\pi f_{sc} \cdot \Delta t$$

  不同的水平位元排列模式 → 不同相位 → 不同顏色。這是「用數學騙出彩色」的經典案例。
- **軟碟機控制**：Wozniak 不用昂貴的磁碟控制器晶片，改用軟體精準編碼讀寫時序（Disk II，1978），成本僅為同業的幾分之一。
- 整台主機板晶片數遠少於競品：PET 與 TRS-80 的工程師看到 Apple II 主機板都自嘆不如。

### 線索二：ROM BASIC——開機即用
三傑共同的關鍵決策：**把 BASIC 燒進 ROM**。電腦一開機就進入 BASIC 直譯器，不需要先載入作業系統。這符合「零使用門檻」的產品哲學：

$$\text{可用性} = \frac{1}{1 + \text{學習成本} + \text{設定成本}}$$

Apple II 的 Integer BASIC（後為 Applesoft BASIC，授權自 Microsoft）就駐留在 12KB ROM 中。

### 線索三：BASIC 範例程式碼
在 Apple II 上打出這段程式，是 1970 年代末每個孩子的共同記憶：

```basic
10  HOME
20  HGR
30  HCOLOR = 3
40  FOR I = 0 TO 279 STEP 4
50    HPLOT I, 0 TO I, 159
60  NEXT I
70  FOR X = 1 TO 10
80    PRINT "HELLO, WORLD!";
90  NEXT X
100 END
```

前三行清螢幕、進入高解析度繪圖模式（$280 \times 160$ 像素）、設白色；畫出直線;最後列印問候語。用今天 Python 對照：

```python
# 同樣概念：畫直線 + 列印文字（Python, 2020s）
for x in range(0, 280, 4):
    draw_line((x, 0), (x, 159))
print("HELLO, WORLD! " * 10)
```

### 線索四：VisiCalc——殺手級應用
1979 年 Dan Bricklin 與 Bob Frankston 為 Apple II 寫出 VisiCalc，第一套試算表。其核心抽象是「儲存格依賴圖」：改一格，全部重算。

$$\text{cell}_{i} = f(\text{cell}_{j_1}, \text{cell}_{j_2}, \dots), \quad j_k < i \text{（拓撲序）}$$

商務人士為了買 VisiCalc 而買 Apple II——軟體第一次反過來賣硬體。這證明了「殺手級應用（killer app）」理論：平台成敗取決於其上最好的軟體。

## 結案 -- 後果與影響
- Apple II 一路賣到 1993 年，累計銷售數百萬台，養大了 Apple，也養出個人電腦產業。
- 「硬體平台 + ROM BASIC + 殺手級應用」成為往後 20 年個人電腦的標準商業模型。
- 8-bit 時代確立：6502 CPU、64KB 記憶體空間、磁碟作業系統（Apple DOS → ProDOS）。
- 三傑之中 Apple II 最持久；TRS-80 敗於封閉與品質，PET 敗於不合用的鍵盤與擴充性。
- 為 1981 年 IBM PC 的登場鋪好舞台：市場已被證明存在，剩下的是誰來定標準。

## 關鍵人物與文獻
- **Steve Wozniak**：Apple I/II 的總工程師，工程簡潔主義的典範。
- **Steve Jobs**：產品願景與行銷，「電腦給每個人」的推手。
- **Dan Bricklin / Bob Frankston**：VisiCalc 作者。
- **Mike Markkula**：早期投資人，寫下「The Apple Marketing Philosophy」。
- 文獻：Wozniak, *iWoz* (2006)；Isaacson, *Steve Jobs* (2011)；Freiberger & Swaine, *Fire in the Valley* (1984)。
