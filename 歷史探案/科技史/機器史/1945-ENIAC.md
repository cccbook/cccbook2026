# 1945-ENIAC

## 案件摘要

1945 年底（1946 年 2 月 14 日公開發表），美國賓州大學摩爾電機工程學院（Moore School of Electrical Engineering）的 ENIAC（Electronic Numerical Integrator and Computer）正式完成：17,468 支真空管、重 27 噸、占地 167 平方公尺、耗電 150 千瓦——史上第一台通用型電子計算機。這樁案件的「兇手」是一屋子嗡嗡作響的真空管：它把彈道計算從人力查表數天縮到 30 秒，也開啟了整個數位時代。

## 前因 -- 為什麼會有這個案子

- 二戰期間美國陸軍彈道研究實驗室（Ballistic Research Laboratory, BRL, 馬里蘭州 Aberdeen）需要大量彈道射表（firing tables），每張表要計算數百條彈道。
- 每條彈道靠「計算員」（human computer，多為女性數學系畢業生）用機械計算器手算，約需 20–40 小時——前線等不起。
- 已有機電式計算機（如 IBM 的 Harvard Mark I，1944 年，繼電器式）但速度以「每秒數次加法」為上限，繼電器開關慢且易磨損。
- 1943 年，物理學家 John Mauchly 與年輕工程師 J. Presper Eckert 向陸軍提案：用真空管做計算機。真空管每秒可開關十萬次——這是把速度提升四個量級的唯一路徑。

## 線索與推理 -- 數學式、程式、理論

### 理論一：彈道計算的數學——數值積分

砲彈飛行受重力與空氣阻力支配，阻力隨速度與空氣密度變化，無解析解，只能數值積分：

$$m \frac{d\vec{v}}{dt} = m\vec{g} - \frac{1}{2}\rho(h)\, C_d(v)\, A\, |\vec{v}|\,\vec{v}$$

用歐拉法或龍格—庫塔法（Runge–Kutta）以步長 $h$ 逐步推進：

$$\vec{v}_{n+1} = \vec{v}_n + \frac{\vec{F}(\vec{v}_n, h_n)}{m}\,\Delta t$$

一條彈道要數千步的乘加運算，數百條彈道 × 數十個仰角組合，正是 ENIAC 誕生的任務背景。

### 理論二：真空管開關速度與十進位架構

ENIAC 採用十進位（ring counter）而非二進位，每個數字用 10 支真空管的環形計數器表示。真空管開關時間約 1 微秒：

$$t_{\text{加法}} \approx 200\,\mu s \Rightarrow \sim 5{,}000 \text{ 次加法/秒}$$

比繼電器式 Mark I（約 3 次加法/秒）快千倍以上。Eckert 的工程關鍵：以較低電壓運轉真空管延長壽命（真空管燒毀是最大風險，實際運轉中平均每兩天燒毀一支，靠快速更換維持）。

### 理論三：程式化靠接線——通用性與瓶頸

ENIAC 沒有儲存程式的記憶體：「程式」靠插入電纜與撥動 3,000 個開關設定，重新程式化要數天。乘法用累加器（accumulator）連續加法實現：

$$a \times b = \underbrace{b + b + \cdots + b}_{a \text{ 次（十進位逐位）}}$$

ENIAC 有 20 個累加器、可並行運算，是「通用」的關鍵——但「接線即程式」的瓶頸直接催生了 1945 年 von Neumann 的《EDVAC 報告》：把程式與資料一起存進記憶體（stored-program concept）。

### 理論四：可靠性的統計現實

17,468 支真空管，若每支每千小時故障率為 $\lambda$，全系統故障率為

$$\Lambda = N \lambda = 17468 \times \lambda$$

即使單管壽命很長，串聯系統平均故障間隔（MTBF）依然以小時計。ENIAC 實際 MTBF 約數天，工程團隊靠「降壓運轉 + 快速診斷更換」把可用率維持在 90% 以上——這是大規模電子系統可靠性的第一課，也是日後電晶體取代真空管的直接動機。

### Python 驗證：數值積分算彈道

```python
import math

g, m, rho0, Cd, A = 9.81, 30.0, 1.225, 0.3, 0.006
dt = 0.001
v, x, t = 800.0, 0.0, 0.0          # 仰角 0 度的簡化水平彈道
while v > 0.1:
    drag = 0.5 * rho0 * Cd * A * v * v
    v -= drag/m * dt
    x += v * dt
    t += dt
print(f"停止距離 ≈ {x:.0f} m, 時間 ≈ {t:.1f} s, 步數 ≈ {t/dt:.0f}")

# 真空管 MTBF
N, lam = 17468, 1/50000   # 每管每 5 萬小時一故障
print(f"系統 MTBF ≈ {1/(N*lam):.1f} 小時")
```

## 破案時刻

1943 年 6 月陸軍簽約（代號 Project PX），Mauchly 與 Eckert 領導，Kathleen McNulty、Jean Bartik、Frances Bilas 等六位女性數學家負責「程式設定」。1945 年 11 月完成、1946 年 2 月 14 日公開亮相：計算一條彈道 30 秒——比砲彈本身飛得還快，記者驚呼「比腦更快」。首個公開演示程式計算砲彈軌跡；1948 年改裝為儲存程式式（converter code），1955 年 10 月 2 日退役。

## 後果 -- 改變了什麼

- 1945 年 von Neumann 的《First Draft of a Report on the EDVAC》確立儲存程式架構（von Neumann architecture），成為今日所有電腦的藍圖。
- Mauchly 與 Eckert 1946 年創立公司推出 UNIVAC I（1951），電腦從軍用實驗走向商業；Honeywell v. Sperry Rand（1973）判決使 ENIAC 專利失效，承認 Atanasoff 的 ABC 機（1942）為部分概念先驅——「第一台」的頭銜至今仍有學術爭議。
- 真空管的可靠性極限直接催生 1947 年電晶體（Bell Labs），1950 年代末電晶體電腦全面取代真空管電腦。
- 計算員（human computer）職業消失，女性軟體工程師（ENIAC 六女）成為程式設計職業的開端。
- 教訓：軍事需求（射表、後來的氫彈模擬）是早期計算機最大推手；通用性（可重程式化）比單一速度更決定後世影響。
