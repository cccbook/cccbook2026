# 1946 - ENIAC

## 案件摘要
1946 年 2 月 14 日，世界第一台通用型電子計算機 ENIAC 在賓州大學公開。它用 18000 個真空管把計算速度提升到每秒 5000 次加法，是機械計算器的千倍以上——但它「用插線寫程式」，也因此催生了後來的儲存程式革命。

## 前因 -- 為什麼會有這個案子
- 二戰期間，美國陸軍彈道研究實驗室（BRL）需要快速計算火砲的「射表」（firing table）。
- 每張射表要對數百個仰角/距離組合積分彈道微分方程，人類計算員（human computer，多為女性數學家）用桌上計算器算一條彈道要 20–40 小時。
- 原有的 Bush 差分分析儀（機械式）速度與精度都不夠。

彈道微分方程（忽略阻力的簡化形式）：

$$\frac{d^2 y}{dt^2} = -g, \qquad \frac{d^2 x}{dt^2} = 0$$

完整版還要考慮空氣阻力 $F_d = \tfrac{1}{2}\rho v^2 C_d A$，是非線性 ODE，無法查表求解，只能數值積分。

## 線索與推理 -- 數學式、程式、理論

### 規格與規模
| 項目 | ENIAC |
|---|---|
| 真空管 | 約 17,468–18,000 支 |
| 重量 | 約 27 噸 |
| 佔地 | 約 167 m² |
| 耗電 | 約 150 kW |
| 加法速度 | 5,000 次/秒 |
| 乘法速度 | 約 357 次/秒 |
| 記憶體 | 20 個累加器，每個 10 位十進位 |

ENIAC 用十進位而非二進位（以 10 個位元的觸發器環表示一個十進位數字），加法本質上是環計數：

$$x + y \Rightarrow \text{pulse}(x) \text{ 驅動 accumulator 從 } y \text{ 計數 } x \text{ 次}$$

### 插線程式與打孔卡
- 程式「寫」在實體接線板上：用纜線把單元（累加器、乘法器、函數表）連接成資料流，再用開關與旋鈕設定。
- 資料與部分常數由 IBM 打孔卡輸入。
- 程式設計師（Kathleen McNulty、Jean Jennings Bartik 等六位女性）要修改程式得重新配線，設定一次可花一至數天。

$$T_{\text{設定程式}} \approx 1\text{–}3\ \text{天} \gg T_{\text{執行程式}} \approx \text{秒}\text{–}分鐘$$

### 每秒 5000 次加法 vs 人類計算員
人類計算員用機械計算器約每秒 0.5 次加法，ENIAC 快 10,000 倍：

$$\frac{5000\ \text{add/s}}{0.5\ \text{add/s}} = 10^4\times$$

一條彈道從 30 小時縮短到約 30 秒——快 3600 倍。

### von Neumann 的加入與 EDVAC
- 1944 年，數學家 von Neumann 在往來華盛頓的火車上偶然得知 ENIAC 計畫，隨即以顧問身份加入。
- 他關心的是 ENIAC 能否用於氫彈相關的可壓縮流體力學計算，發現「改程式要重新插線」是致命瓶頸。
- 1945 年他寫下《First Draft of a Report on the EDVAC》，提出儲存程式架構；EDVAC 於 1949–1951 年運轉，用汞延遲線記憶體同時儲存指令與資料。

### Python 對照：數值積分算彈道
```python
# ENIAC 用數值積分算彈道；這裡用歐拉法重現該計算（無阻力版）
g, dt = 9.8, 0.001
x = y = vx = vy = 0.0
v0, theta = 300.0, 45.0        # 初速 300 m/s、仰角 45 度
vx, vy = v0*0.7071, v0*0.7071
while y >= 0:
    x += vx*dt; y += vy*dt
    vy -= g*dt
print(x)                      # 約 9180 m；ENIAC 幾秒內可對數百個參數組合重複此計算
```

## 結案 -- 後果與影響
- ENIAC 證明了「全電子、通用」計算機的可行性，是電腦時代的起點。
- 「程式即插線」的痛苦直接催生了 stored-program 概念，把程式變成可儲存的資料——軟體產業的種子在 ENIAC 的接線板上萌芽。
- ENIAC 後期由 Adele Goldstine 等人發展出把指令存入函數表的初步「程式儲存」技術，顯示革命已在體內發生。
- 計算從軍事（彈道、氫彈模擬）擴散到氣象、工程與商業，開啟了「計算萬能」的時代精神。

## 關鍵人物與文獻
- **J. Presper Eckert、John Mauchly**：總設計師，之後創辦 Eckert–Mauchly Computer Corporation（UNIVAC）。
- **John von Neumann**：顧問，EDVAC 報告作者。
- **六位 ENIAC 程式設計師**：Kathleen McNulty、Frances Bilas、Jean Jennings Bartik、Ruth Lichterman、Elizabeth Snyder、Marlyn Wescoff——史上第一批程式設計師。
- 文獻：Goldstine, H. & Goldstine, A., "The Electronic Numerical Integrator and Computer (ENIAC)", *Mathematical Tables and Other Aids to Computation*, 1946。
