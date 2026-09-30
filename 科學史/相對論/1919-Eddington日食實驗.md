# 1919-Eddington 日食實驗

## 案件摘要
1919 年 5 月 29 日，Arthur Eddington 率隊在 Príncipe 島與巴西 Sobral 觀測日全食，測量星光經過太陽的偏折角。結果宣告：「牛頓被推翻了？」 Einstein 一夜之間從德國物理學家變成世界名人。這是一次大戰後最著名的科學外交，也是一場至今仍有爭議的偵辦。

## 前因 -- 為什麼會有這個案子
- **理論上的兩個預言**：
  - 牛頓（發射說/微粒說）：光線如粒子般被太陽吸引，偏折 $\alpha_N = \frac{2GM}{c^2 R} \approx 0.875''$（1904 年 Soldner 已算出）。
  - 廣義相對論（1915）：空間彎曲 + 時間彎曲各貢獻一半，**加倍**：

    $$\boxed{\alpha = \frac{4GM}{c^2 R} \approx 1.75''}$$
- **戰後的科學封鎖**：一戰（1914–1918）期間英德科學界隔絕，德國科學家被抵制。劍橋天文學家 Eddington 是貴格會教徒（和平主義者），堅持戰後應恢復國際科學合作。
- **關鍵人物巧合**：Eddington 因反戰立場面臨免役審判，天文學家 Frank Dyson 向當局陳情：他的「戰爭任務」應是領導 1919 年日食遠征——驗證「敵國科學家」Einstein 的理論。愛國理由與科學外交完美結合。
- **日食的必要性**：平時太陽旁的星光被日光大氣淹沒，唯有全食時月亮遮住太陽，才能拍到太陽附近的恆星。

## 線索與推理 -- 數學式、程式、理論

### 1. 偏折角的推導
在 Schwarzschild 幾何中，光線走零測地線（$ds^2 = 0$）。對近日點距離 $R$ 做微擾積分，可得偏折角：

$$\alpha = \frac{4GM}{c^2 R}$$

**物理拆解**（Einstein 1911 年的早期版本只算了一半）：
- 空間曲率貢獻：$\frac{2GM}{c^2R}$（1915 年新增，來自 $g_{rr}$ 項）
- 時間彎曲貢獻：$\frac{2GM}{c^2R}$（1911 年已有，來自 $g_{tt}$ 項）

**數值計算**：

```python
import numpy as np

G = 6.674e-11
c = 2.998e8
M = 1.989e30      # 太陽質量
R = 6.96e8        # 太陽半徑 (m)

alpha_GR = 4*G*M / (c**2 * R)              # rad
alpha_N  = 2*G*M / (c**2 * R)              # 牛頓值
arcsec = lambda x: np.degrees(x) * 3600

print(f"牛頓預測:      {arcsec(alpha_N):.3f}\"")   # 0.875
print(f"廣義相對論:    {arcsec(alpha_GR):.3f}\"")  # 1.750
```

### 2. 兩地觀測的計畫
全食帶橫跨大西洋，Dyson 規劃兩隊：

| 遠征隊 | 地點 | 儀器 | 天氣/結果 |
|--------|------|------|-----------|
| Greenwish 隊（Crommelin、Davidson） | 巴西 **Sobral** | 4 吋折射鏡 + 天體照相儀 | 晴朗；4 吋鏡數據優良，天體照相儀因鏡片受熱失焦（數據傾向牛頓值但系統誤差大） |
| Eddington 隊 | 西非外海 **Príncipe 島** | 天體照相儀 | 遇陰雨，全食最後關頭雲開；僅 2–3 張可用底片 |

### 3. 底片的測量與「偵辦」
方法：比較同一片星空（太陽在場時 vs 太陽不在場時，即數月後重拍同一區域）中恆星的相對位置，量出偏移量。

```python
import numpy as np
# 1919 年公布的結果（單位：角秒）
results = {
    "Sobral 4吋鏡":  (1.98, 0.16),    # (值, 誤差) → 支持 GR
    "Príncipe":      (1.61, 0.40),    # 誤差大，支持 GR
    "Sobral 天體照相儀": (0.93, None),  # 傾向牛頓，後判為系統誤差
}
for k, (v, err) in results.items():
    print(f"{k}: {v:.2f}\"" + (f" ± {err}" if err else "（系統誤差，未採計）"))
print("牛頓: 0.875\" | GR: 1.750\"")
```

1919 年 11 月 6 日，皇家學會與皇家天文學會聯席會議公布結果：偏折角 $\approx 1.75''$，**支持廣義相對論**。

**歷史爭議**：Eddington 在分析中捨棄了 Sobral 天體照相儀的數據（傾向牛頓值），理由是「鏡片受熱系統誤差」。現代史家（如 Collins & Pinch）質疑這是否為偏袒；不過 1919 年後的大量獨立驗證（1922 Lick、1953、1973 Texas 隊等）與無線電/VLBI 測量，最終確認了 GR 值——結論本身站得住腳。

### 4. 媒體轟動與世界名人
- 1919 年 11 月 7 日倫敦《泰晤士報》頭版：**「科學革命——新的宇宙理論——牛頓的觀念被推翻」**（Revolution in Science — New Theory of the Universe — Newtonian Ideas Overthrown）。
- 11 月 10 日《紐約時報》以六個標題報導，包括「天空中的光全部歪斜」。
- 標題問題的真相：牛頓力學在日常尺度仍完美有效（GR 在弱場退化回牛頓理論），被「推翻」的只是「重力是超距作用力」的概念——正確說法是「被超越」。
- Einstein 從此成為全球第一位「科學超級明星」。1921 年訪美引起狂熱，他的形象（亂髮、簡樸）成為天才的符號。

### 5. 後續驗證的精進
```python
import numpy as np
# 偏折測量的世紀精進
tests = {
    "1919 Eddington 日食":  (1.75, "±20%"),
    "1973 Texas 日食":      (1.55, "±10%"),
    "VLBI 無線電類星體(1975)": (1.76, "±3%"),
    "HIPPARCOS 衛星(1990s)":  (1.75, "0.1%"),
    "卡西尼號太陽系測量(2003)": (1.75, "2×10^-5 (gamma)"),
}
for k, (v, e) in tests.items():
    print(f"{k}: {v}\" {e}")
```

現代測量已達 $10^{-5}$ 精度（Cassini 對 PPN 參數 $\gamma$ 的測定），廣義相對論的 $\gamma = 1$ 完美成立。

## 結案 -- 後果與影響
- **科學外交典範**：Eddington 推廣「敵國科學家」的理論，一戰後快速修復國際科學共同體；1922 年起 Solvay 會議恢復，德國科學家重回國際舞台。
- **廣義相對論成為主流**：1919 年後 GR 從邊緣理論變成物理學前沿，催生 1920 年代的相對論研究熱潮與宇宙學（Friedmann、Lemaître）。
- **Einstein 的公眾角色**：此後 36 年，Einstein 以世界良心（和平主義、反戰、後來的原子彈議題）的姿態活在大眾視野中。
- **實驗方法學**：大規模國際遠征觀測成為科學典範；底片數據取捨的爭議也成為科學社會學的經典案例。
- **遺緒**：2019 年事件視界望遠鏡的 M87 黑洞影像，被視為百年後對同一個理論的致敬。

## 關鍵人物與文獻
| 人物 | 角色 |
|------|------|
| Arthur Eddington | Príncipe 隊領隊、理論推廣者 |
| Frank Dyson | 皇家天文學家、遠征總策劃 |
| Andrew Crommelin / Charles Davidson | Sobral 隊 |
| Albert Einstein | 被驗證的理論提出者、受益的世界名人 |
| Johann Soldner | 1804 年算出牛頓值 0.875" |

**文獻**
1. Dyson, F. W., Eddington, A. S., Davidson, C. (1920). *A Determination of the Deflection of Light by the Sun's Gravitation*, Phil. Trans. R. Soc. A 220.
2. Einstein, A. (1915/1916). 廣義相對論原始論文（偏折預言來源）。
3. Collins, H. & Pinch, T. (1993). *The Golem: What You Should Know about Science*（第 1 章：日食實驗的爭議）。
4. Stanley, M. (2003). *Practical Mystic: Religion, Science, and A. S. Eddington.*
