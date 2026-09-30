# 1965 - 摩爾定律（Moore's Law）

## 案件摘要
1965 年，Fairchild 的 Gordon Moore 在《Electronics》雜誌上發表一篇短文，觀察到積體電路上的電晶體數量「每年倍增」。這條經驗曲線後來成為半導體產業五十年自我實現的預言與路線圖。

## 前因 -- 為什麼會有這個案子
- 1947 年 Bell Labs 發明電晶體，1958 年 Kilby 與 Noyce 各自發明積體電路（IC）。
- 1959–1965 年間，平面製程（planar process）讓晶片上的元件數快速成長：從單一電晶體到含數十個元件的 IC。
- Moore 手上有 1959–1965 共六年的資料點：1, 2, 4, 8, 16, 32……他只是把這條直線（在半對數座標上）往未來延伸十年。
- 當時的動機很單純：預測 IC 會在哪些應用（家用電腦、汽車、手錶）變得划算——結果這句話反而成了產業的軍備競賽合約。

## 線索與推理 -- 數學式、程式、理論

### 1. 原始觀察與 1975 修正
- **1965 原始版本**：晶片上最低成本複雜度（元件數）每年倍增。
- **1975 修正版本**：Moore 依實際資料（Intel 8086 前）把倍增週期修正為**兩年**（晶圓面積貢獻變小、行寬縮小成主導）。
- 大眾常說「18 個月」其實是 1975 年 David House（Intel）的版本：考慮速度提升後的整體效能每 18 個月翻倍。

### 2. 電晶體密度成長曲線
$$N(t) = N_0 \cdot 2^{t/2}$$
其中 $t$ 以年為單位，$N_0$ 是起始密度。取對數：
$$\log_2 N(t) = \log_2 N_0 + \frac{t}{2}$$
即半對數圖上的一條直線，斜率 $1/2$（每兩年 $\log_2 N$ 加 1）。

對照真實資料（Intel 處理器電晶體數）：
| 年份 | 晶片 | 電晶體數 | $\log_2 N$ |
|------|------|----------|------------|
| 1971 | 4004 | 2,300 | ≈11.2 |
| 1978 | 8086 | 29,000 | ≈14.8 |
| 1989 | 486 | 1,200,000 | ≈20.2 |
| 2000 | Pentium 4 | 42,000,000 | ≈25.3 |
| 2010 | Core i7 | 1,170,000,000 | ≈30.1 |
| 2020 | Core i9-10900K 級 | ~10 億+ / GPU 更高 | ≈33+ |
| 2024 | Apple M4 / NVIDIA GPU | 數百億 | ≈37+ |

### 3. 經濟面：每電晶體成本下降
Moore 原文的核心其實是**成本**：最低單位成本對應的元件數隨時間倍增。若晶片面積放大 $a$、密度提升 $d$，總電晶體數 $N \sim a \cdot d$，而製造成本增長遠慢於 $N$，故：
$$\text{Cost per transistor} \approx \frac{C_{\text{wafer}}}{N} \propto 2^{-t/2}$$
即每兩年降一半——這是數位革命取代類比世界的經濟動力。

### 4. Dennard 縮放（1974）與頻率極限
Robert Dennard 提出：電晶體縮小時，**功率密度不變**——尺寸縮 $k$ 倍，電壓與電流也縮 $k$ 倍，功率 $\sim V I$ 縮 $k^2$ 倍，恰好抵銷面積縮小。這讓摩爾定律與「頻率提升」同時成立（2000 年前 CPU 頻率從 MHz 衝到 GHz）。

$$P_{\text{density}} = \frac{V I / k^2}{A / k^2} = \frac{VI}{A} = \text{const}$$

但 2005 年前後，漏電流與閘極氧化層太薄（量子穿隧）打破了 Dennard 縮放：電壓無法再降，功率密度暴增 → **頻率卡在 ~3–5 GHz**，產業轉向多核心（「免費午餐結束了」）。

### 5. 摩爾定律的終結爭議（2010s）
- 2016 年《Nature》文章 "The chips are down for Moore's law" 指出電晶體成長已明顯放緩。
- 3D 堆疊（FinFET、GAA）、極紫外光微影（EUV）、晶片封裝（chiplet）成為延命手段。
- 許多人主張「摩爾定律已死」，但 Moore 本人說過：這條定律的真正精神是「**指数進步是可能達成的**」——AI 時代的 GPU（NVIDIA 宣稱 "Huang's Law"）接棒了這條曲線。

### 6. Python 畫出電晶體數量的對數成長圖

```python
import numpy as np
import matplotlib.pyplot as plt

# Intel 4004 到現代 GPU 的電晶體數量（約數）
chips = {
    "4004 (1971)":       2_300,
    "8086 (1978)":      29_000,
    "386 (1985)":      275_000,
    "486 (1989)":    1_200_000,
    "Pentium (1993)":  3_100_000,
    "Pentium 4 (2000)":42_000_000,
    "Core 2 Duo (2006)": 291_000_000,
    "Core i7 (2010)":  1_170_000_000,
    "M1 (2020)":      16_000_000_000,
    "M4 (2024)":      28_000_000_000,
    "H100 GPU (2022)": 80_000_000_000,
}

names = list(chips.keys())
years = [n.split("(")[1].rstrip(")") for n in names]
counts = np.array([chips[n] for n in names], dtype=float)

fig, ax = plt.subplots(figsize=(10, 6))
ax.semilogy(range(len(names)), counts, "o-", color="tab:blue")
ax.set_xticks(range(len(names)))
ax.set_xticklabels(names, rotation=45, ha="right")
ax.set_ylabel("Transistor count (log scale)")
ax.set_title("Moore's Law: Transistor Count from Intel 4004 to Modern GPU")

# 疊加摩爾定律預測線 N = 2300 * 2^(t/2)
t = np.arange(len(names))
pred = 2300 * 2 ** ((years[-1].__class__(0) + 0) if False else 0)  # placeholder
pred = 2300 * 2 ** (t / 2)   # 每兩年倍增
ax.semilogy(t, pred, "--", color="tab:red", label="N(t) = 2300 * 2^(t/2)")
ax.legend()
plt.tight_layout()
plt.savefig("moore_law.png", dpi=120)
plt.show()
```

半對數圖上真實資料與 $N(t)=N_0 2^{t/2}$ 幾乎平行——這就是偵探眼中的「證據鏈」。

## 結案 -- 後果與影響
- 摩爾定律成為 ITRS（國際半導體技術路線圖）的依據，產業按「路線圖」投資數千億美元。
- 個人電腦、手機、網際網路、AI 全部建立在這條成本曲線上。
- 摩爾定律精神（指數進步）延伸到基因定序、太陽能電池、儲存密度（Kryder's Law）。
- 結案評語：這不是物理定律，而是**經濟學與人類意志的定律**——當足夠多人相信指數進步，指數進步就會發生。

## 關鍵人物與文獻
- **Gordon Moore**（1929–2023）：Intel 共同創辦人，1965 提出觀察，1975 修正。
- G. E. Moore, "Cramming more components onto integrated circuits," *Electronics*, vol. 38, no. 8, 1965.
- R. H. Dennard et al., "Design of ion-implanted MOSFET's with very small physical dimensions," *IEEE JSSC*, 1974.
- C. Mack, "The multiple lives of Moore's law," *IEEE Spectrum*, 2015.
