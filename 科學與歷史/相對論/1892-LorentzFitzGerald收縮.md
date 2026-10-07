# 1892 - Lorentz–FitzGerald 收縮假說

## 案件摘要
面對 Michelson–Morley 的零結果，FitzGerald（1889）與 Lorentz（1892）各自提出一個大膽假說：
物體在運動方向上會「收縮」，收縮量恰好抵銷乙太風造成的光程差。
這是「數學補丁」與「物理革命」之間的關鍵轉折——補丁開始長出革命的骨頭。

## 前因 -- 為什麼會有這個案子
- 1887 年 Michelson–Morley 實驗：預期 $\Delta N \approx 0.4$ 條紋的位移，實測為零。
- 乙太理論的預言（見 1887 案）：
  $$\Delta t = \frac{2L}{c}\cdot\frac{c^2}{c^2-v^2} - \frac{2L}{c}\cdot\frac{c}{\sqrt{c^2-v^2}} \approx \frac{L v^2}{c^3}$$
- 偵探的問題：**什麼機制能讓 $\Delta t$ 恰好歸零？**
- 同時代已有 Heaviside（1888）計算：運動中帶電體的電場會沿運動方向壓扁
  ——這給了 FitzGerald/Lorentz 一個「物質由電磁力束縛」的物理動機。

## 線索與推理 -- 數學式、程式、理論

### 線索 1：需要多大的收縮？

設臂長 $L$ 在運動方向縮為 $L' = L\sqrt{1-v^2/c^2}$（垂直臂不變），則
$$
t_\parallel = \frac{2L'\,c}{c^2-v^2}
= \frac{2L\sqrt{1-v^2/c^2}\;c}{c^2(1-v^2/c^2)}
= \frac{2L}{c}\cdot\frac{1}{\sqrt{1-v^2/c^2}}
= t_\perp
$$
**兩臂時間差精確歸零**——這就是 FitzGerald 1889 年在 *Science* 上以
短短三段話提出的假說，Lorentz 1892 年獨立提出並給出更嚴謹的理論框架。

### 線索 2：收縮公式

$$
\boxed{\,L = L_0\sqrt{1-\frac{v^2}{c^2}}\,}
$$
其中 $L_0$ 是物體相對乙太靜止時的「真實長度」。以 $\gamma$ 記號（後人引入）：
$$
L = \frac{L_0}{\gamma},\qquad \gamma = \frac{1}{\sqrt{1-v^2/c^2}}
$$
對 $v = 30$ km/s：$\gamma \approx 1 + \dfrac{v^2}{2c^2} \approx 1 + 5\times10^{-9}$，
即地球公轉只造成約**五十億分之一**的收縮——小到日常完全無感，卻恰好夠抵銷干涉儀訊號。

```python
import numpy as np

c = 3e8; v = 3e4
gamma = 1/np.sqrt(1 - (v/c)**2)
print(f"gamma = 1 + {gamma-1:.2e}  (收縮比 ~1/2e9)")

# 驗證收縮使時間差歸零
L = 11.0
L_contract = L*np.sqrt(1 - (v/c)**2)
t_par = 2*L_contract*c/(c**2 - v**2)
t_perp = 2*L/np.sqrt(c**2 - v**2)
print(f"t_par - t_perp = {t_par - t_perp:.2e} s  -> 精確為 0")
```

### 線索 3：Lorentz 的電子理論與「局部時間」

Lorentz 不是只提出收縮——他在 1892–1895 年間建立了**電子的電磁理論**：
物質由帶電粒子（電子）組成，電磁力透過乙太傳遞。收縮是電磁力的自然後果
（Heaviside 已算出運動電荷的場會壓扁）。為使變換後的 Maxwell 方程形式不變，
他引入了一個輔助量——**局部時間（local time）**：

$$
t' = t - \frac{v x}{c^2}
$$

其中 $x$ 是觀察點在運動方向上的座標。這表示：不同位置的鐘彼此「有點不同步」，
偏差量正比於位置與速度。Lorentz 自己稱之為「只是數學技巧」
（a ingenious transformed time），並不認為它是真實的時間效應。

搭配一階變換（Lorentz 1895 版）：
$$
x' = x - vt,\qquad t' = t - \frac{v x}{c^2}
$$
在此變換下，Maxwell 方程在**一階** $v/c$ 精度內不變——正好解釋所有
一階乙太實驗（含 Michelson–Morley 收縮補充、Fizeau 曳引、光行差）的零結果。

### 線索 4：數學補丁 vs 物理革命的分野

| 面向 | FitzGerald–Lorentz（補丁路線） | Einstein（革命路線，1905） |
|---|---|---|
| 乙太 | 仍然保留（静止乙太參考系） | 直接拋棄 |
| 收縮 | 物體相對乙太的真實力學收縮 | 運動學效應：相對運動的觀察者測得較短 |
| 局部時間 $t' = t - vx/c^2$ | 數學輔助工具，非真實時間 | 時間就是相對的，同時性是觀察者相依的 |
| 動機 | 保存 Maxwell 理論 + 乙太 | 保存 Maxwell 理論 + 相對性原理 |

**偵探的判斷**：FitzGerald/Lorentz 拿到了正確的公式，卻把公式的「意義」留在了舊世界觀裡。
他們解決了謎題，但沒有發現謎題其實指向一個全新的宇宙。

## 結案 -- 後果與影響
- **成功之處**：收縮假說精確解釋 Michelson–Morley 零結果，且 Lorentz 電子理論
  成功預言 Zeeman 效應（Lorentz 因此獲 1902 諾貝爾物理獎）。
- **未竟之處**：收縮是「真實的」但「不可偵測的」（相對乙太靜止系才有 $L_0$），
  這種不可證偽的補丁使物理學家越來越不安（Poincaré 的批評，見 1904 案）。
- **鋪路 1904**：局部時間 $t' = t - vx/c^2$ 是完整 Lorentz 變換的種子；
  1904 年 Lorentz 將它推廣到所有階精度，完成完整變換方程。
- 後見之明：1905 年 Einstein 指出，若同時性是相對的，收縮根本不需要「乙太風」動機
  ——它自然從 $t' = \gamma(t - vx/c^2)$ 中掉出來。

## 關鍵人物與文獻
- **George Francis FitzGerald**（1851–1901）：愛爾蘭物理學家，1889 年率先提出收縮。
  - FitzGerald, G.F. (1889). "The Ether and the Earth's Atmosphere". *Science* 13: 390.
- **Hendrik Antoon Lorentz**（1853–1928）：荷蘭物理學家，電子論創立者，1902 諾貝爾物理獎（與 Zeeman）。
  - Lorentz, H.A. (1892). "The Relative Motion of the Earth and the Ether". *Verhandelingen der Koninklijke Akademie van Wetenschappen* 1: 74–79.
  - Lorentz, H.A. (1895). *Versuch einer Theorie der elektrischen und optischen Erscheinungen in bewegten Körpern*.
- **Oliver Heaviside**（1850–1925）：1888 年算出運動電荷場的壓扁，提供收縮的物理動機。
