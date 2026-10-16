# 2020s — 先進封裝與 Chiplet：把大晶片拆開再拼回去

## 案件摘要
摩爾定律放緩、單一大晶片面積越大良率越低的數學宿命（$Y = e^{-DA}$），逼出「分拆再拼裝」的 Chiplet 思路。AMD、Apple 以拆晶片維持效能成長，CoWoS/TSV/hybrid bonding 與 UCIe 標準（2022）構築拼裝基礎，HBM 讓 AI 晶片吃飽頻寬。

## 前因 -- 為什麼會有這個案子
- 電晶體微縮成本飆升，5nm/3nm 一片 12 吋晶圓要數萬美元，單靠製程微縮已不划算。
- 晶片面積越大、缺陷機率越高，良率隨面積**指數崩塌**；SoC 面積已達 600–800 mm²（如 NVIDIA H100 約 814 mm²），良率成為致命傷。
- 設計與光罩（mask）成本隨製程指數上升，單一製程節點單一 SoC 的開發費動輒上億美元。嫌犯：**良率與成本曲線**。

## 線索與推理 -- 數學式、程式、理論（本體）

### 線索一：泊松良率模型 —— 面積的指數宿命
晶圓缺陷密度為 $D$（defects/cm²），晶片面積為 $A$。若缺陷服從泊松分布（平均 $DA$ 顆缺陷落在晶片上），晶片「零缺陷」機率即良率：

$$
Y = P(\text{零缺陷}) = \frac{(DA)^0 e^{-DA}}{0!} = e^{-DA}
$$

每片晶圓可產出的好晶片數：

$$
N_{\text{good}} = \frac{A_{\text{wafer}} \cdot Y}{A} = \frac{A_{\text{wafer}} \cdot e^{-DA}}{A}
$$

**推理**：$A$ 越大，$e^{-DA}$ 崩得比 $1/A$ 還快。實務上常用負二項式模型修正聚集效應：

$$
Y = \left(1 + \frac{D A}{\alpha}\right)^{-\alpha}, \quad \alpha \text{ 為聚集參數}
$$

### 線索二：Chiplet 分拆 —— 用乘法定律對抗指數定律
把大晶片拆成 $n$ 個小 Chiplet，每片面積 $A_i = A/n$，良率變成：

$$
Y_{\text{total}} \approx \prod_{i=1}^{n} Y_i \cdot Y_{\text{int}}, \quad Y_i = e^{-D A_i}
$$

例如 $DA=4$ 時 $Y = e^{-4} \approx 1.8\%$；拆成 4 片各 $DA=1$，則每片 $Y_i = e^{-1} \approx 36.8\%$。只要互連良率 $Y_{\text{int}}$ 夠高，總體遠優於單一大晶片。代表作：
- **AMD EPYC（Zen 架構）**：把 8 核心 CCD 與 I/O die 分拆，跨製程混合（CCD 用先進製程、I/O 用成熟製程省錢）。
- **Apple M1 Ultra / UltraFusion**：兩顆 M1 Max 用 2.5D 矽中介層拼成一顆，頻寬達 2.5 TB/s。

### 線索三：2.5D / 3D 先進封裝技術
| 技術 | 說明 |
|---|---|
| **CoWoS**（TSMC, Chip-on-Wafer-on-Substrate） | 晶片先裝在矽中介層（interposer）再上基板，GPU+HBM 的標配 |
| **TSV**（Through-Silicon Via，矽穿孔） | 貫穿矽晶圓的垂直銅導線，讓晶片垂直堆疊互連 |
| **Hybrid bonding**（混合鍵合） | 直接銅-銅鍵合，無凸點，間距可低至 10 µm 以下，3D 堆疊密度最高 |
| **InFO / FOWLP** | 扇出型晶圓級封裝，省去中介層成本 |

理論定義：**die-to-die 頻寬** $B = f \times W \times \text{bits/beat}$，hybrid bonding 以超短距離（µm 級）使 $f$ 提升且功耗/pb 大降（可達 <1 pJ/bit）。

### 線索四：Die-to-Die 互連標準
- **UCIe**（Universal Chiplet Interconnect Express，2022 年 3 月由 Intel、AMD、Arm、TSMC、Samsung、微軟、Meta、Google 等共組聯盟）：統一 chiplet 間封裝內互連協定，含 PHY、die-to-die adapter 與 PCIe/CXL 相容層。
- **AIB**（Advanced Interface Bus，Intel 2019 開放）：UCIe 前身，以並行訊號實作高頻寬低延遲互連。
- 標準化的意義：chiplet 像「IC 界的樂高」，不同廠、不同製程、不同功能的 die 可以互拼。

### 線索五：HBM —— AI 晶片的頻寬解藥
**HBM**（High Bandwidth Memory）：8–12 層 DRAM 用 TSV 垂直堆疊，與 GPU 同封裝（CoWoS）。頻寬：

$$
B = f_{\text{io}} \times \text{channels} \times \text{bits/channel}
$$

HBM3e 達 ~1.2 TB/s/顆，H100 用 5 顆 HBM3 達 3.35 TB/s —— 遠勝 GDDR。AI 訓練瓶頸在記憶體頻寬（roofline model：$\text{perf} = \min(\text{算力}, B \times \text{算術強度})$），HBM+先進封裝因此成為 AI 晶片的命脈。

### 先進封裝 vs 傳統封裝對照表
| 項目 | 傳統封裝（wire bond / flip chip） | 先進封裝（2.5D/3D, Chiplet） |
|---|---|---|
| 互連方式 | 打線 / 凸塊 + 基板 | TSV、矽中介層、hybrid bonding |
| 異構整合 | 幾乎不可 | 異構異質（混合製程/材料） |
| 互連密度 | ~100 µm 級 | 10 µm 級以下 |
| 頻寬/功耗 | 數十 GB/s、數 pJ/bit | TB/s 級、<1 pJ/bit |
| 良率策略 | 全押單一晶片 | 分拆 Chiplet，已知良品拼裝 |
| 代表 | BGA、QFP | CoWoS、InFO、SoIC、Foveros |

### Python：良率 vs 晶片面積曲線（大晶片 vs Chiplet）
```python
import math
import matplotlib.pyplot as plt

D = 0.1            # 缺陷密度 (defects/cm^2)，示意值

def yield_poisson(A):                 # Y = e^{-DA}
    return math.exp(-D * A)

def yield_negbinomial(A, alpha=2.0):  # 聚集修正模型
    return (1 + D * A / alpha) ** (-alpha)

areas = [50, 100, 150, 200, 300, 400, 500, 600, 700, 800]

# 單一大晶片 vs 拆成 n 個等面積 chiplet（假設互連良率 99%）
for model, name in [(yield_poisson, "Poisson"), (yield_negbinomial, "Neg-Binomial")]:
    print(f"\n【{name} 模型】 D={D}")
    print(f"{'面積(mm^2)':>10} {'單一晶片良率':>12} {'4-Chiplet 總良率':>14}")
    for A in areas:
        y_single = model(A)
        y_chip = (model(A / 4) ** 4) * 0.99   # 4 片 + 互連良率
        print(f"{A:>10} {y_single:>12.1%} {y_chip:>14.1%}")

# 畫曲線
xs = [a * 0.5 for a in range(2, 1601)]     # 1 ~ 800 mm^2
plt.plot(xs, [yield_poisson(x) for x in xs], label="Single die (Poisson)")
plt.plot(xs, [(yield_poisson(x/4)**4)*0.99 for x in xs], label="4 Chiplets")
plt.plot(xs, [yield_negbinomial(x) for x in xs], "--", label="Single die (Neg-Bin)")
plt.xlabel("Die area (mm^2)"); plt.ylabel("Yield")
plt.title("Yield vs Die Area: Monolithic vs Chiplet")
plt.legend(); plt.grid(True); plt.savefig("yield_vs_area.png")
```
執行可見：面積越大，單一晶片良率指數崩落，而 Chiplet 分拆的總良率顯著更高 —— 這正是 2020s 業界全面轉向 chiplet 的數學鐵證。

## 結案 -- 後果與影響
- **結案陳詞**：$Y=e^{-DA}$ 的指數宿命無法靠微縮擺脫，只能靠「拆開 + 高密度拼裝」繞道破解 —— Chiplet 與先進封裝是摩爾定律放緩時代的新摩爾定律（「摩爾定律 2.0：從電晶體微縮到系統拼裝」）。
- AMD EPYC 靠 chiplet 從市占邊緣攻上伺服器主流；Apple UltraFusion 展示拼裝的效能上限；TSMC CoWoS 產能成為 AI 晶片供應的戰略瓶頸（2023–2026 年 GPU 荒的核心）。
- 深遠影響：產業分工重組 —— 出現 IP 供應商、chiplet 供應商、封裝廠（OSAT）的新價值鏈；UCIe 讓異構整合標準化；未來「3D IC + hybrid bonding」讓封裝從後段製程變成前段效能引擎，封裝技術正式成為晶片設計的核心學科。

## 關鍵人物與文獻
- **Jim Keller**：AMD Zen 架構（2017）的 chiplet 化推手，後續於 Intel/Tenstorrent 繼續倡議模組化晶片。
- **Lisa Su**：AMD 執行長，以 chiplet 策略（EPYC 2017 起量產）翻轉伺服器市場。
- **TSMC**：CoWoS（2012 首用於 Xilinx Virtex-7）、SoIC/InFO、hybrid bonding 技術平台。
- **Intel**：EMIB、Foveros、AIB（2019 開放）與 UCIe 聯盟（2022）發起者。
- 文獻：UCIe Specification 1.0（2022）；C. S. Tan（MIT）等 TSV/hybrid bonding 綜述；Murphy,《Cost-size optima of monolithic integrated circuits》, Proc. IEEE (1964) —— 良率模型的經典出處。
