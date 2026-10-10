# 計算模擬學的歷史年表（科學史）

> 計算模擬學是「用計算代替實驗」的科學：把物理、化學、生物寫成數學，再把數學交給電腦一步步算。從阿基米德的窮竭法、牛頓的運動方程、尤拉的數值格式，到薛丁格方程、蒙地卡羅、分子動力學、密度泛函、有限元素、氣象預報，再到 QM/MM、增強採樣、機器學習勢能，直到 AlphaFold 解開蛋白質折疊、AI 天氣超越數值預報——這部歷史就是人類追問「世界能否在電腦裡重演」的三百年探案史。
>
> 本書以「推理探案」的方式，為每個歷史事件寫一篇 wiki，包含前因後果、理論與公式。每篇檔名以年份開頭。

## 目錄（Wiki 書篇目）

### 第一幕：萌芽 — 世界寫成方程（前230–1930）

| 年份 | 事件 | Wiki |
|------|------|------|
| 前230 | 阿基米德窮竭法：最早的數值逼近，圓周率與浮力 | [-0230-Archimedes窮竭法.md](-0230-Archimedes窮竭法.md) |
| 1687 | Newton《自然哲學之數學原理》：運動方程成為一切模擬的起點 | [1687-Newton運動方程.md](1687-Newton運動方程.md) |
| 1768 | Euler 方法：第一個常微分方程數值解法 | [1768-Euler方法.md](1768-Euler方法.md) |
| 1822 | Fourier 熱傳與 Navier–Stokes 方程：連續體模擬的母方程 | [1822-Fourier與NavierStokes.md](1822-Fourier與NavierStokes.md) |
| 1922 | Richardson 數值天氣夢：六萬人算房的預報工廠與失敗 | [1922-Richardson數值天氣.md](1922-Richardson數值天氣.md) |
| 1926 | Schrödinger 方程：量子模擬的目標函數誕生 | [1926-Schrodinger方程.md](1926-Schrodinger方程.md) |
| 1927 | Hartree 自洽場：第一個量子化學迭代演算法 | [1927-Hartree自洽場.md](1927-Hartree自洽場.md) |
| 1930 | Hartree–Fock＋Slater 行列式：交換反對稱的正軌 | [1930-HartreeFock與Slater.md](1930-HartreeFock與Slater.md) |

### 第二幕：電腦誕生 — 暴力計算開闢新疆（1946–1965）

| 年份 | 事件 | Wiki |
|------|------|------|
| 1946 | ENIAC 彈道計算與 Monte Carlo 誕生：Ulam、von Neumann 的賭局 | [1946-ENIAC與MonteCarlo誕生.md](1946-ENIAC與MonteCarlo誕生.md) |
| 1950 | Charney 的 ENIAC 氣象預報：數值天氣第一次成功 | [1950-Charney數值天氣預報.md](1950-Charney數值天氣預報.md) |
| 1952 | Hodgkin–Huxley 神經模擬：手搖計算機算出的動作電位 | [1952-HodgkinHuxley神經模擬.md](1952-HodgkinHuxley神經模擬.md) |
| 1953 | Metropolis Monte Carlo：MANIAC 上的狀態方程 | [1953-MetropolisMonteCarlo.md](1953-MetropolisMonteCarlo.md) |
| 1956 | 有限元素法 FEM：Turner–Clough 的飛機翅膀算法 | [1956-有限元素法FEM.md](1956-有限元素法FEM.md) |
| 1957 | Alder–Wainwright 硬球 MD：第一次分子動力學，相變的電腦證據 | [1957-AlderWainwright硬球MD.md](1957-AlderWainwright硬球MD.md) |
| 1963 | Lorenz 混沌模擬：蝴蝶效應，數值天氣的極限 | [1963-Lorenz混沌模擬.md](1963-Lorenz混沌模擬.md) |
| 1964 | Rahman 液態氬 MD：Lennard-Jones 流體的逼真重演 | [1964-Rahman液態氬MD.md](1964-Rahman液態氬MD.md) |
| 1965 | Hohenberg–Kohn 定理：密度泛函理論 DFT 的存在性證明 | [1965-HohenbergKohn定理.md](1965-HohenbergKohn定理.md) |
| 1965 | Kohn–Sham 方程：讓 DFT 可算的軌道技巧 | [1965-KohnSham方程.md](1965-KohnSham方程.md) |

### 第三幕：分子動力學與多尺度 — 原子世界動起來（1967–1985）

| 年份 | 事件 | Wiki |
|------|------|------|
| 1967 | Verlet 積分：MD 的辛結構守護神 | [1967-Verlet積分.md](1967-Verlet積分.md) |
| 1970 | Conway 生命遊戲：細胞自動機的爆發 | [1970-Conway生命遊戲.md](1970-Conway生命遊戲.md) |
| 1974 | Wilson 格點 QCD：時空離散化的強交互作用 | [1974-Wilson格點QCD.md](1974-Wilson格點QCD.md) |
| 1976 | Gillespie SSA：化學主方程的精確隨機模擬 | [1976-Gillespie隨機模擬.md](1976-Gillespie隨機模擬.md) |
| 1976 | Warshel–Levitt QM/MM：酵素的多尺度手術刀 | [1976-WarshelLevittQMMM.md](1976-WarshelLevittQMMM.md) |
| 1977 | BPTI 蛋白質 MD：McCammon–Karplus 第一次折疊蛋白 | [1977-BPTI蛋白質MD.md](1977-BPTI蛋白質MD.md) |
| 1977 | SPH 光滑粒子流體：Lucy、Gingold–Monaghan 的無網格法 | [1977-SPH流體粒子法.md](1977-SPH流體粒子法.md) |
| 1980 | Ceperley–Alder 量子 Monte Carlo：均勻電子氣的基準答案 | [1980-CeperleyAlder量子MC.md](1980-CeperleyAlder量子MC.md) |
| 1984 | Nosé–Hoover 恆溫器：擴展系綜的溫度控制 | [1984-NoseHoover恆溫器.md](1984-NoseHoover恆溫器.md) |
| 1985 | Car–Parrinello 從頭 MD：DFT 與 MD 的統一 | [1985-CarParrinello從頭MD.md](1985-CarParrinello從頭MD.md) |

### 第四幕：採樣與預測 — 罕見事件與結構預測（1994–2013）

| 年份 | 事件 | Wiki |
|------|------|------|
| 1994 | CASP 蛋白質結構預測競賽開幕：盲測的試金石 | [1994-CASP結構預測競賽.md](1994-CASP結構預測競賽.md) |
| 1999 | Rosetta：Baker 的片段組裝折疊術 | [1999-Rosetta蛋白質預測.md](1999-Rosetta蛋白質預測.md) |
| 2002 | Metadynamics：Laio–Parrinello 的填溝增強採樣 | [2002-Metadynamics增強採樣.md](2002-Metadynamics增強採樣.md) |
| 2007 | Behler–Parrinello 神經網路勢能：機器學習勢的開端 | [2007-BehlerParrinello神經勢能.md](2007-BehlerParrinello神經勢能.md) |
| 2013 | 多尺度模擬諾貝爾獎：Karplus、Levitt、Warshel | [2013-多尺度模擬諾貝爾獎.md](2013-多尺度模擬諾貝爾獎.md) |

### 第五幕：AI 革命 — 從 AlphaFold 到科學基礎模型（2018–至今）

| 年份 | 事件 | Wiki |
|------|------|------|
| 2018 | AlphaFold 1：CASP13 橫空出世，距離圖革命 | [2018-AlphaFold1.md](2018-AlphaFold1.md) |
| 2020 | AlphaFold 2：CASP14 原子精度，折疊問題落幕 | [2020-AlphaFold2.md](2020-AlphaFold2.md) |
| 2021 | 開放折疊時代：AF2 開源＋RoseTTAFold＋ESMFold | [2021-開放折疊時代.md](2021-開放折疊時代.md) |
| 2023 | AI 天氣超越 NWP：GraphCast、Pangu-Weather | [2023-AI天氣超越NWP.md](2023-AI天氣超越NWP.md) |
| 2024 | AlphaFold 3 與諾貝爾化學獎：Hassabis、Jumper、Baker | [2024-AlphaFold3與諾貝爾獎.md](2024-AlphaFold3與諾貝爾獎.md) |
| 2025 | 科學基礎模型現況：MACE、MatterSim、GenCast 與通用原子模擬 | [2025-科學基礎模型現況.md](2025-科學基礎模型現況.md) |

## 程式實作（_code/，檔名：年份-程式名稱.py，全數 numpy 可執行）

| 程式 | 對應 Wiki | 驗證要點 |
|------|-----------|----------|
| [_code/-0230-archimedes_pi.py](_code/-0230-archimedes_pi.py) | 前230 窮竭法 | 96 邊夾擊 $3.1408 < \pi < 3.1429$ |
| [_code/1768-euler_method.py](_code/1768-euler_method.py) | 1768 Euler 方法 | 誤差比約 10 倍， $O(h)$ |
| [_code/1822-heat_equation_ftcs.py](_code/1822-heat_equation_ftcs.py) | 1822 Fourier／NS | 穩定 $r \le 0.5$ 、 $r=0.6$ 發散 |
| [_code/1922-advection_cfl.py](_code/1922-advection_cfl.py) | 1922 Richardson／1950 Charney | 迎風穩定、中心差發散（CFL） |
| [_code/1926-schrodinger_box.py](_code/1926-schrodinger_box.py) | 1926 Schrödinger | 有限差分本徵值誤差 $< 2\%$ |
| [_code/1946-monte_carlo_pi.py](_code/1946-monte_carlo_pi.py) | 1946 Monte Carlo | 誤差 $\sim 1/\sqrt N$ |
| [_code/1952-hodgkin_huxley.py](_code/1952-hodgkin_huxley.py) | 1952 H–H | 動作電位峰值 $> 0$ mV |
| [_code/1953-metropolis_ising.py](_code/1953-metropolis_ising.py) | 1953 Metropolis | 低溫有序／高溫無序 |
| [_code/1956-fem_1d_poisson.py](_code/1956-fem_1d_poisson.py) | 1956 FEM | P1 元誤差 $< 10^{-3}$ |
| [_code/1957-hardsphere_gas.py](_code/1957-hardsphere_gas.py) | 1957 硬球 MD | 碰撞動量能量守恆 |
| [_code/1963-lorenz_butterfly.py](_code/1963-lorenz_butterfly.py) | 1963 Lorenz | 初值差 $10^{-8}$ 指數分離 |
| [_code/1964-lennard_jones_md.py](_code/1964-lennard_jones_md.py) | 1964 Rahman | NVE 能量漂移 $< 2\%$ |
| [_code/1967-verlet_oscillator.py](_code/1967-verlet_oscillator.py) | 1967 Verlet | Verlet 保能量、Euler 發散 |
| [_code/1970-game_of_life_glider.py](_code/1970-game_of_life_glider.py) | 1970 生命遊戲 | 滑翔機 4 步平移 |
| [_code/1976-gillespie_ssa.py](_code/1976-gillespie_ssa.py) | 1976 Gillespie | 均值 $\approx \lambda/\mu$ |
| [_code/1976-qmmm_double_well.py](_code/1976-qmmm_double_well.py) | 1976 QM/MM | 雙阱佔比 $\approx$ 1:1 |
| [_code/1977-sph_density.py](_code/1977-sph_density.py) | 1977 SPH | 密度估計 L2 $< 0.05$ |
| [_code/1984-nose_hoover.py](_code/1984-nose_hoover.py) | 1984 Nosé–Hoover | 平均動能 $\approx T/2$ |
| [_code/1999-hp_lattice_folding.py](_code/1999-hp_lattice_folding.py) | 1999 Rosetta | HP 格點最低能量構形 |
| [_code/2002-metadynamics_1d.py](_code/2002-metadynamics_1d.py) | 2002 Metadynamics | 自由能重建、多次躍遷 |
| [_code/2007-neural_pair_potential.py](_code/2007-neural_pair_potential.py) | 2007 神經勢能 | MLP 擬合 Morse 勢 |
| [_code/2018-contact_mi_toy.py](_code/2018-contact_mi_toy.py) | 2018 AlphaFold1 | 共演化互資訊找接觸 |
| [_code/2023-neural_weather_toy.py](_code/2023-neural_weather_toy.py) | 2023 AI 天氣 | AI 勝持續性 $> 20\%$ |
| [_code/2025-equivariant_filter_toy.py](_code/2025-equivariant_filter_toy.py) | 2025 基礎模型 | 旋轉等變 $F(Rx) = RF(x)$ |

## 因果鏈總覽

```
Archimedes (-230) ── 窮竭逼近 ── Newton (1687) ── 運動方程 ── Euler (1768) ── 數值格式
     │                                                              │
     │                                                              ├─ Fourier/NS (1822) ── PDE ── FEM (1956) / SPH (1977)
     │                                                              ├─ Richardson (1922) ── NWP夢 ── Charney (1950) ── Lorenz (1963) ── AI天氣 (2023)
     │                                                              └─ Schrödinger (1926) ── Hartree (1927) ── HF (1930)
     │                                                                                                          │
     ├─ ENIAC/MC (1946) ── Metropolis (1953) ── QMC (1980) ── 採樣 ── Metadynamics (2002)
     │         │                                                              │
     │         └─ Alder MD (1957) ── Rahman (1964) ── Verlet (1967) ── BPTI (1977)
     │                                                              │
     │                                                              ├─ HK/KS (1965) ── DFT ── Car-Parrinello (1985)
     │                                                              ├─ Nosé-Hoover (1984) ── 恆溫恆壓系綜
     │                                                              └─ QM/MM (1976) ── Nobel (2013)
     │
     ├─ HH (1952) ── 生物模擬 ── Gillespie (1976) ── 隨機化學動力學
     │
     ├─ Wilson QCD (1974) ── 格點場論 ── 高能模擬分支
     │
     ├─ Life (1970) ── CA ── 複雜系統模擬分支
     │
     └─ CASP (1994) ── Rosetta (1999) ── BP神經勢 (2007) ── AF1 (2018) ── AF2 (2020)
              │                                                              │
              └─ 開放折疊 (2021) ── AF3+Nobel (2024) ── 基礎模型 (2025)
```

## 寫作方式說明

每篇 wiki 採「推理探案」結構：

1. **案發現場（前因）**：當時的未解之謎是什麼？誰遇到的？為何重要？
2. **偵查過程（推理）**：主角如何思考？關鍵靈感為何？核心技術（方程、演算法、勢能、採樣策略）如何推導，含數學式與表格。
3. **結案報告（後果）**：謎題如何解？留下什麼遺產？影響了哪些後續事件？
4. **證據與工具**：關鍵公式、演算法虛擬碼或 Python 模擬程式、參數表（非必要不硬寫程式，優先講清理論）。
