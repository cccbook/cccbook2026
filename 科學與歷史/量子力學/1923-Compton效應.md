# 1923-Compton 效應

## 案件摘要
1923 年，Arthur Compton 讓 X 射線射入石墨中的自由電子，發現散射光波長變長了。經典電磁學完全無法解釋這個偏移，但把光當成「一顆顆帶動量的粒子」與電子做彈性碰撞，偏移量精確算出。這是光子存在最直接的鐵證。

## 前因 -- 為什麼會有這個案子
- 1905 年 Einstein 用光量子解釋光電效應，但只涉及能量 $E=h\nu$，未處理動量；學界仍視光量子為「形式假設」。
- 1916 年 Milikan 的光電實驗、1917 年 Einstein 推導輻射動量 $p = E/c$ 的理論工作，逐漸累積證據。
- 經典 Thomson 散射（低頻極限）預言：散射光頻率應與入射光完全相同，僅強度隨角度變化——Compton 的實驗卻出現兩條譜線：一條原波長 $\lambda$，一條變長的 $\lambda'$。
- 辯題：光是波還是粒子？Compton 效應是「二審」的關鍵新證據。

## 線索與推理 -- 數學式、程式、理論

### 現象
Compton 以鉬靶產生的 X 射線（$\lambda \approx 0.07\,\mathrm{nm}$）散射石墨，觀察到波長偏移：

$$
\Delta\lambda = \lambda' - \lambda = \frac{h}{m_e c}(1-\cos\theta)
$$

其中 $\theta$ 為散射角，$\frac{h}{m_e c} \approx 2.426\,\mathrm{pm}$ 稱為電子的 **Compton 波長**。關鍵特徵：$\Delta\lambda$ 與入射波長、材料種類無關，只依賴散射角。

### 動量與能量守恆的向量推導
把光子視為能量 $E = h\nu = \hbar\omega$、動量 $\mathbf{p} = \hbar\mathbf{k}$（$|\mathbf{k}| = \omega/c$）的粒子，與靜止電子（質量 $m_e$）彈性碰撞。設電子反衝動量為 $\mathbf{p}_e$：

$$
\hbar\mathbf{k} = \hbar\mathbf{k}' + \mathbf{p}_e \quad\Rightarrow\quad p_e^2 = \hbar^2(k^2 + k'^2 - 2kk'\cos\theta)
$$

能量守恆：

$$
\hbar\omega + m_e c^2 = \hbar\omega' + \sqrt{p_e^2 c^2 + m_e^2 c^4}
$$

兩式消去 $\mathbf{p}_e$（將能量式平方並代入動量式），整理得：

$$
\frac{1}{\omega'} - \frac{1}{\omega} = \frac{\hbar}{m_e c^2}(1-\cos\theta)
\;\Longrightarrow\;
\Delta\lambda = \frac{h}{m_e c}(1-\cos\theta)
$$

### 為何經典理論失敗
Thomson 散射中電子在入射波電場中做強迫振盪、以同頻率再輻射，$\Delta\lambda$ 必為零。只有把輻射場「量子化為粒子」並要求單次碰撞滿足相對論性守恆律，才能得到 $(1-\cos\theta)$ 項。Compton 最初甚至以「束縛電子+某種虛構輻射」掙扎解釋，最終承認：粒子圖像是唯一解。

### Python 數值驗證
```python
import numpy as np

h, me, c = 6.62607015e-34, 9.1093837015e-31, 2.99792458e8
lam_c = h / (me * c)          # 電子 Compton 波長 ≈ 2.426 pm
print(f"Compton wavelength = {lam_c*1e12:.3f} pm")

lam = 0.070e-9                # 入射 X 射線波長
theta = np.deg2rad(90)
dl = lam_c * (1 - np.cos(theta))
lam_p = lam + dl
print(f"theta=90deg: dλ={dl*1e12:.3f} pm, λ'={lam_p*1e12:.3f} pm")

theta = np.deg2rad(135)
print(f"theta=135deg: dλ={lam_c*(1-np.cos(theta))*1e12:.3f} pm")
# 實驗值：90° 時 Δλ≈2.43 pm、135° 時 Δλ≈4.50 pm，與計算一致
```

## 結案 -- 後果與影響
- 判決：光具有粒子性，光子攜帶能量與動量 $E=\hbar\omega$、$\mathbf{p}=\hbar\mathbf{k}$。
- 1927 年 Compton 獲諾貝爾物理獎；光電效應（能量）+ Compton 效應（動量）共同奠定光子概念。
- 直接啟發 de Broglie：既然光波有動量，為何物質粒子不能有波長？→ 1924 年物質波假說。
- 現代應用：Compton 望遠鏡、醫學 CT 成像、γ 射線探測都依賴此散射機制。

## 關鍵人物與文獻
- **Arthur H. Compton**（1892–1962），華盛頓大學聖路易分校。
- A. H. Compton, *A Quantum Theory of the Scattering of X-Rays by Light Elements*, Phys. Rev. 21, 483 (1923).
- 相關：A. H. Compton & A. W. Simon (1925) 驗證反衝電子軌跡；J. J. Thomson 經典散射理論（1906）。
