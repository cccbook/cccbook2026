# 1887 - Michelson–Morley 干涉儀實驗

## 案件摘要
1887 年，Michelson 與 Morley 在克利夫蘭用史上最精巧的干涉儀，偵測地球穿過「乙太」的運動。
實驗靈敏度足以看到預期訊號的百分之一，結果卻是乾淨俐落的**零**。
這個「什麼都沒測到」的零結果，搖撼了整個古典物理，為相對論鋪平了道路。

## 前因 -- 為什麼會有這個案子
- Maxwell（1865）算出光速 $c = 1/\sqrt{\mu_0\epsilon_0}$，但波需要介質——
  當時物理學家假設有一種瀰漫全宇宙、無質量、透明的介質：**乙太（luminiferous aether）**。
- 地球以約 $v \approx 30$ km/s 繞太陽公轉，應該迎面撞上「**乙太風**」，
  就像騎車在風中前進。
- 在乙太風中，光速應該隨方向不同而不同：順風快、逆風慢——
  這個「方向差」就是可以偵測的線索。
- Michelson 在 1881 年柏林做過初版實驗（靈敏度不足），1887 年與 Morley
  在美國改良：加大光臂（11 m，多次反射）、以水銀浮槽減振、旋轉整台儀器 90°。

## 線索與推理 -- 數學式、程式、理論

### 線索 1：干涉儀原理

光源發出的光被 45° 半鍍銀鏡分成兩束，分別沿互相垂直的兩臂往返後會合：
若兩臂光程不同，會產生干涉條紋（fringe）移動。旋轉儀器 90°，兩臂角色互換，
條紋應移動——這就是預期的訊號。

### 線索 2：光程差計算（乙太理論的預言）

設乙太風速為 $v$，臂長均為 $L$。

**(a) 平行臂（順逆流）**：往返平均速度
$$
\bar{v}_\parallel = \frac{2}{\frac{1}{c+v} + \frac{1}{c-v}}
= \frac{c^2-v^2}{c}\cdot\frac{1}{1}\cdot\frac{c^2-v^2}{c^2-v^2}
\quad\Rightarrow\quad
t_\parallel = \frac{L}{c+v} + \frac{L}{c-v} = \frac{2Lc}{c^2-v^2} = \frac{2L}{c}\cdot\frac{c^2}{c^2-v^2}
$$

**(b) 垂直臂（橫向）**：光必須「斜著走」才能回到移動中的鏡子，速度三角形給出
$$
t_\perp = \frac{2L}{\sqrt{c^2-v^2}} = \frac{2L}{c}\cdot\frac{c}{\sqrt{c^2-v^2}}
$$

**(c) 時間差與條紋位移**：
$$
\Delta t = t_\parallel - t_\perp \approx \frac{L v^2}{c^3},\qquad
\Delta N = \frac{c\,\Delta t}{\lambda} \approx \frac{L v^2}{\lambda c^2}
$$
旋轉 90° 後時間差變號，總條紋位移應為
$$
\Delta N_{\text{total}} \approx \frac{2 L v^2}{\lambda c^2}
$$

### 線索 3：數值代入 -- 預期 vs 零結果

以 $L = 11$ m、$\lambda = 500$ nm、$v = 30$ km/s：

```python
import numpy as np

c  = 3e8        # m/s
v  = 3e4        # 地球公轉速率 m/s
L  = 11.0       # 有效臂長（多次反射）m
lam = 500e-9    # 波長 m

t_par = 2*L/(c - v**2/c)         # = 2Lc/(c^2-v^2)
t_perp = 2*L/np.sqrt(c**2 - v**2)
print(f"t_par - t_perp = {t_par - t_perp:.4e} s")

dN = (t_par - t_perp)*c/lam
print(f"單向 fringe shift ≈ {dN:.4f} 條")
print(f"旋轉 90° 總位移  ≈ {2*dN:.4f} 條")   # 預期 ~0.44 條
print(f"儀器可測靈敏度   ≈ {dN/100:.4f} 條")  # ~0.004 條
```

- **預期位移**：約 $0.4$ 條紋。
- **儀器靈敏度**：可偵測小至 $0.01$ 條紋的移動——訊號應該清晰可見。
- **實測結果**：位移小於 $0.01$ 條紋，在誤差範圍內——**零結果**！
  （甚至觀察不同季節、不同海拔，都是零。）

### 線索 4：偵探的反覆排查

為排除「儀器壞了」的可能，他們檢查了所有備選解釋：
- 儀器隨季節轉向？→ 持續觀測半年（地球速度方向反轉），仍是零。
- 溫度、振動、地板應力？→ 水銀浮槽、地下室、重複測量，仍是零。
- 乙太被地球「拖曳」？→ 與星光 aberration（Bradley 1727）觀測矛盾。

## 結案 -- 後果與影響
- **零結果的震撼**：這是物理史上最著名的「否定實驗」。
  Kelvin 1900 年把它列為「物理學天空中的兩朵烏雲」之一。
- **為相對論鋪路**：
  - FitzGerald（1889）與 Lorentz（1892）提出長度收縮假說企圖「補丁式」解釋（見 1892 案）。
  - Einstein（1905）則釜底抽薪：光速對所有慣性觀察者恆為 $c$，根本沒有乙太——
    零結果不是巧合，而是**原理**。
- **Michelson 獲 1907 年諾貝爾物理獎**——美國第一位諾貝爾科學獎得主，
  獲獎理由是「精密光學儀器與以其進行的光譜學與計量學研究」
  （諷刺的是，獎並非頒給「發現乙太」）。
- 現代重做（如 2009 年的雷射版本）靈敏度提高 $10^{10}$ 倍以上，依然是零。

## 關鍵人物與文獻
- **Albert A. Michelson**（1852–1931）：干涉儀發明者，1907 諾貝爾物理獎。
- **Edward W. Morley**（1838–1923）：化學家，精密測量的執行者。
- 文獻：
  - Michelson, A.A. & Morley, E.W. (1887). "On the Relative Motion of the Earth and the Luminiferous Ether". *American Journal of Science* 34: 333–345.
  - Michelson, A.A. (1881). "The Relative Motion of the Earth and the Luminiferous Ether". *Am. J. Sci.* 22: 120–129.
