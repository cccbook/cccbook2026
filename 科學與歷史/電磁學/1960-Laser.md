# 1960-Laser

## 案件摘要
1960 年 5 月 16 日，Hughes 實驗室的 Theodore Maiman 用紅寶石晶體與螺旋閃光燈做出第一台雷射。愛因斯坦 1917 年埋下的「受激輻射」線索，四十三年後終於在實驗室裡變成一束同調光。

## 前因 -- 為什麼會有這個案子
- 1917 年，愛因斯坦在推導黑體輻射 Planck 公式時，被迫引入第三種過程——**受激輻射（stimulated emission）**：一個光子可以「誘發」激發態原子放出與自己完全相同的光子。理論上埋了種子，卻無人知道如何實現。
- 1950 年代微波譜學成熟：Lamb 與 Retherford 的蘭姆位移、氨分子譜線的精確測量。
- Townes 的推理：既然受激輻射光子與入射光子狀態相同，若能造成**粒子數反轉**並放入共振腔，就能「複製」光子產生相干放大——先在微波做（maser），再到光（laser）。
- 1958 年 Townes 與 Schawlow 發表紅外/光頻 maser 的理論可行方案；各實驗室競賽開跑。

## 線索與推理 -- 數學式、程式、理論
### 1. 愛因斯坦係數（1917）
二能階系統中三種過程的速率方程：

$$\dot N_2 = -A_{21}N_2 - B_{21}\rho(\nu)N_2 + B_{12}\rho(\nu)N_1$$

- 自發輻射：$A_{21}$（機率/秒）
- 受激輻射：$B_{21}\rho(\nu)$
- 受激吸收：$B_{12}\rho(\nu)$

熱平衡下與 Planck 公式比較，愛因斯坦證明：

$$B_{12} = B_{21}, \qquad \frac{A_{21}}{B_{21}} = \frac{8\pi h\nu^3}{c^3}$$

關鍵：$A_{21}/B_{21} \propto \nu^3$——**頻率越高，自發輻射越難壓制**，這就是為什麼光頻雷射比微波 maser 難做。

### 2. 粒子數反轉與增益
正常熱平衡 $N_2 < N_1$，介質吸收光。反轉後 $N_2 > N_1$，光穿過介質被放大。單位長度增益：

$$G(\nu) = \sigma(\nu)\,(N_2 - N_1), \qquad I(z) = I_0\, e^{Gz}$$

振盪條件：迴路增益等於損耗，$R_1 R_2\, e^{2GL} \geq 1$。

### 3. Maiman 的三能階紅寶石雷射（1960.5.16）
- 介質：剛玉（Al₂O₃）中摻 Cr³⁺ 的**紅寶石**，Cr³⁺ 提供能階。
- **三能階**設計：閃光燈把電子從基態 $E_1$ 抽到寬能帶 $E_3$，快速無輻射弛豫到亞穩態 $E_2$（壽命約 3 ms）；$E_2$ 在 $E_1$ 之上累積，形成反轉。
- 抽運：螺旋氙氣閃光燈，功率達數千焦耳。
- 共振腔：紅寶石兩端拋光鏡面（一端半反射輸出），法布里–珀羅干涉儀結構。
- 輸出：波長 **694.3 nm** 的深紅色脈衝光。

### 4. 雷射光的三大特性
| 特性 | 數學描述 |
|---|---|
| 單色性 | 線寬 $\Delta\nu \ll \nu$（HeNe 雷射 $\Delta\nu/\nu \sim 10^{-9}$） |
| 同調性 | 相干長度 $L_c = c\,\Delta t = c/\Delta\nu$，遠超任何光源 |
| 方向性 | 繞射極限發散角 $\theta \approx 1.22\,\lambda/D$ |

### 5. Python 模擬：受激輻射速率方程

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 三能階系統速率方程（紅寶石，簡化）
# E1: 基態, E2: 亞穩態(694nm上能階), E3: 抽運能帶
A21 = 1/3e-3      # E2 壽命 3 ms
Wp  = 500.0       # 抽運速率 (1/s)，閃光燈脈衝期間
Ntot = 1e20       # 總粒子數 cm^-3

def rate(y, t):
    N1, N2, N3 = y
    dN3 = Wp*N1 - N3/1e-8          # E3 快速弛豫 (10 ns)
    dN2 = N3/1e-8 - A21*N2          # E2 慢速衰減
    dN1 = A21*N2 - Wp*N1            # 守恆自動成立
    return [dN1, dN2, dN3]

t = np.linspace(0, 20e-3, 2000)
y0 = [Ntot, 0, 0]
sol = odeint(rate, y0, t)

plt.figure(figsize=(8,4.5))
plt.plot(t*1e3, sol[:,0]/Ntot, label='$N_1/N$（基態）')
plt.plot(t*1e3, sol[:,1]/Ntot, label='$N_2/N$（亞穩態）')
plt.plot(t*1e3, sol[:,2]/Ntot, label='$N_3/N$（抽運帶）')
plt.axhline(0.5, ls=':', c='gray')
plt.xlabel('時間 (ms)'); plt.ylabel('相對粒子數')
plt.title(f'三能階抽運：$W_p$={Wp}/s 下 $N_2$ 趨向反轉（>0.5 需更強抽運）')
plt.legend(); plt.grid(True); plt.show()

# 增益指數成長
z = np.linspace(0, 0.1, 200)
G = 0.05*1e2   # 增益係數 1/m（反轉後）
I = np.exp(G*z)
print(f"經 10 cm 介質：增益 {I[-1]:.1f} 倍（e^(Gz)）")
```

模擬顯示抽運速率須夠高才能把 $N_2$ 推過 $N_1/2$（真正反轉），這正是三能階雷射需要高功率閃光燈的原因——也是為什麼 Townes 團隊質疑 Maiman 的設計能成功。

## 結案 -- 後果與影響
- Maiman 僅用 9 個月、5 萬美元預算搶先實現，擊敗擁有更多資源的哥倫比亞與貝爾團隊。
- 1960–61 年：He-Ne 氣體雷射（Javan）、Nd:YAG、半導體雷射（1962，Hall 等）接連問世。
- **1964 年諾貝爾獎**頒給 Townes、Basov、Prokhorov（maser/laser 原理）。
- 應用革命：**光纖通訊**（1970 Corning 低損耗光纖 + 半導體雷射 = 網際網路的物理層）、光碟/Blu-ray、雷射手術與眼科、工業切割、光譜學與 LIGO 重力波探測。
- 受激輻射的「光子複製」思想延伸到原子雷射與量子光學——1917 年的種子長成整棵光子學的大樹。

## 關鍵人物與文獻
| 人物 | 貢獻 |
|---|---|
| Albert Einstein | 1917 受激輻射理論與 A/B 係數 |
| Charles Townes | 1954 氨 maser、1958 laser 藍圖 |
| Arthur Schawlow | Townes 的合作者，雷射共振腔理論 |
| Theodore Maiman | 1960.5.16 第一台紅寶石雷射 |
| Gordon Gould | 雷射專利與 "laser" 一詞 |

**文獻**
- Einstein, A., "Zur Quantentheorie der Strahlung," *Physikalische Zeitschrift*, 18, 121 (1917).
- Schawlow, A. L., Townes, C. H., "Infrared and optical masers," *Phys. Rev.*, 112, 1940 (1958).
- Maiman, T. H., "Stimulated optical radiation in ruby," *Nature*, 187, 493 (1960).
- Townes, C. H., *How the Laser Happened*, Oxford Univ. Press, 1999.
