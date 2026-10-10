# 2015-ePlace靜電佈局

## 案件摘要
Kraftwerk（1998）的「彈簧 + 密度斥力」框架好用，但斥力模型要調參、密度場求解慢——百萬單元的設計仍是數小時。2015 年，交通大學（NCTU）的 Jing-Wei Lu、Pei-Yu Chen 等人發表 **ePlace**：把密度斥力升級成**靜電場**——把單元視為帶電粒子、密度視為電荷密度，用**帕松方程**（Poisson equation）解出電位與電場，電場的負梯度就是移動方向。物理類比從力學升級到電磁學，FFT 求解帕松方程 + Nesterov 加速梯度讓迭代數與每步成本雙降——ePlace 在 ISPD 2015 競賽奪冠級表現，成為 RePlAce（2019）與 GPU 佈局時代的直接祖先。這是 EDA「物理類比」主線的第三次升級：力學 → 統計 → 電磁學。

## 前因 -- 為什麼會有這個案子
- **斥力模型的工程痛點**：Kraftwerk 式密度斥力需要調「斥力強度/影響半徑」參數，且密度場的梯度計算用直方圖近似，精度與速度都不理想。
- **規模繼續爆炸**：2010s 晶片達千萬單元級；佈局的每輪迭代若不能平行化與加速，就是瓶頸。
- **物理工具就緒**：帕松方程的 FFT 求解器（$O(n \log n)$）、Nesterov 加速梯度法（2004，凸優化的理論突破）——數學零件齊備。
- **靜電場的直覺**：同性電荷互斥、異性相吸——「帶電單元互斥、pad 吸附」的物理直覺，正是攤開機制需要的。

## 線索與推理 -- 數學式、程式、理論

### 核心：靜電位場的三步映射
| 靜電學 | 佈局 |
|--------|------|
| 電荷密度 $\rho(x)$ | 單元密度場（擬合為可微函數）|
| 電位 $\phi$ | 未知量 |
| 電場 $F = -\nabla \phi$ | 移動方向 |

1. **密度 → 電荷**：把單元密度 $\rho(x)$ 擬合成**可微分**的電荷密度（用高斯/三角形核展開）；
2. **帕松方程**：電位由電荷決定：

$$\nabla^2 \phi(x) = -\rho(x)/\epsilon$$

   用 FFT 在 $O(n \log n)$ 內求解（週期邊界），梯度 $\nabla \phi$ 同時可得；
3. **電場 = 移動方向**：單元沿電場力 $F_i = q_i \cdot E(x_i) = -q_i \nabla \phi(x_i)$ 移動，配 Nesterov 加速梯度更新：

$$v_{k+1} = \beta v_k - \eta \nabla E(x_k + \beta v_k), \quad x_{k+1} = x_k + v_{k+1}$$

**為什麼比斥力模型好**：帕松方程給出**全域自洽**的斥力場（不是局部直方圖），且電位處處可微——梯度下降的數學條件（凸性/光滑性）更乾淨。Nesterov 的理論保證凸優化的收斂速率 $O(1/k^2)$，比普通梯度快一階。

### 為什麼快：FFT + 加速的乘法
| | Kraftwerk（1998）| ePlace（2015）|
|---|---|---|
| 斥力場 | 局部直方圖梯度 | 全域帕松電場 |
| 求解 | CG 迭代 $O(n \cdot \text{iter})$ | FFT $O(n \log n)$ |
| 梯度法 | 普通梯度 | Nesterov 加速 |
| 總時間 | 時小級 | 時分級 |

兩個改進相乘——迭代數（Nesterov）與每步成本（FFT）同降，這是解析法速度的再一次跳躍。

### 工程化：density smoothing
密度場的擬合（coulomb/高斯核展開）是精度的關鍵：核太寬則斥力過散，太窄則不可微——ePlace 用可調核寬隨迭代縮小（先粗後細），與退火的溫度排程（1983）、多層分區的粗化（1997）同一「由粗到細」的哲學。

## 結案 -- 後果與影響
- **現代佈局的引擎**：ePlace 的靜電框架被 RePlAce（Cheng-Kahng, 2019，OpenROAD 採用）繼承，成為開源與商用佈局器的主引擎。
- **物理類比的第三階**：虎克彈簧（力學）→ 密度斥力（統計）→ 靜電場（電磁學）——「物理回歸」主線在佈局的完整升級軌跡。
- **競賽文化的驗證**：ePlace 在 ISPD 2015 佈局競賽的表現，讓學術演算法再次證明可打——競賽（DAC/ISPD contests）作為「立案偵辦」的驗證場。
- **GPU 時代的伏筆**：FFT 與梯度下降天然適合 GPU 平行化——ePlace 的數學結構直接為 DREAMPlace（2019）的 GPU 加速鋪路。

## 關鍵人物與文獻
- **Jing-Wei Lu, Pei-Yu Chen, Chin-Chih Chang, Lu-Cheng Tsai** 等：交通大學（NCTU）ePlace 團隊。
- 文獻：
  - J. Lu, P. Chen, C.-C. Chang, L.-C. Tsai, "ePlace: Electrostatics-Based Placement Using Fast Fourier Transform and Nesterov's Method," *ISPD* 2015.
  - C.-K. Cheng, A. B. Kahng, I. Kang, L. Wang, "RePlAce: Advancing Solution Quality and Routability Validation in Global Placement," *IEEE TCAD* 38, 1717 (2019)（後繼）。
  - Y. Nesterov, "A Method for Solving the Convex Programming Problem with Convergence Rate $O(1/k^2)$," *Dokl. Akad. Nauk SSSR* 269, 543 (1983)（加速梯度理論）。
