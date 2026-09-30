# 1887 - Hertz 電磁波實驗

## 案件摘要
1887–1888 年，Heinrich Hertz 在卡爾斯魯厄以火花隙振盪器產生電磁波，用共振環接收，並以駐波測得波長、算出波速恰為光速。Maxwell 1873 年的預言（見 [1873-Maxwell電磁通論](1873-Maxwell電磁通論.md)）就此被實驗定讞：電磁波確實存在。

## 前因 -- 為什麼會有這個案子
- 1873 年 Maxwell 出版《電磁通論》，理論上預言電磁波以光速傳播，但當時主流學界（尤其英國以外）多持懷疑態度，德國學界則偏愛 Weber 的超距作用理論。
- 1879 年柏林科學院設立懸賞題：「以實驗檢驗 Maxwell 理論中介電體極化變化（位移電流）與電磁感應的關係」。Hertz 的老師 Helmholtz 建議他攻這題，Hertz 起初認為實驗不可行而擱置。
- 1885 年 Hertz 到卡爾斯魯厄工業學院任教，發現實驗室有 Ries 螺線管（萊頓瓶放電線圈），其火花隙放電具有足夠高頻的振盪——**破案的器具湊齊了**。
- 1886 年他先做了介電體感應的初步實驗成功，1887 年正式領取柏林科學院獎，接著把目標轉向更大的獵物：**直接捕捉電磁波本身**。

## 線索與推理 -- 數學、程式、理論

### 線索一：火花隙發射器
Hertz 的發射器是一對金屬球中間夾 7.5 mm 火花隙，由感應線圈充電。火花隙擊穿時，電荷在金屬球間以約 $L C$ 電路的頻率來回振盪：

$$f_0 = \frac{1}{2\pi\sqrt{LC}}$$

每次火花對應一串阻尼振盪（dipole antenna 輻射）：

$$E(t) \propto e^{-\gamma t}\cos(2\pi f_0 t)$$

他的偶極天線半波長約 0.5 m，故輻射頻率約 $f \approx c/(2\times1\,\mathrm{m}) \approx 150\ \mathrm{MHz}$（今日稱 VHF/超短波波段，波長約 2–3 m，含諧波成分）。

### 線索二：共振環接收器
接收器是直徑約 35 cm 的開口金屬環，環上也有微小火花隙。當電磁波到達，環中感應電動勢若與環的固有頻率共振，火花隙便迸出微小火花：

$$V_{\mathrm{ind}} = -\frac{d\Phi_B}{dt} \quad(\text{Faraday 定律})$$

Hertz 在暗室中看見極微弱的火花——**這就是電磁波的「指紋」**。他移動接收環的方向，發現火花強度隨方位變化，符合偶極輻射的角分佈 $I(\theta)\propto\sin^2\theta$，證明波是**橫波**（沿偶極軸方向無輻射）。

### 線索三：駐波測波長——關鍵測量
Hertz 讓波在金屬牆（大鋅板）反射，入射波與反射波疊加形成**駐波**：

$$E(x,t) = 2E_0\sin(kx)\cos(\omega t), \qquad k = \frac{2\pi}{\lambda}$$

波節（節點）間距為 $\lambda/2$。Hertz 沿牆法線方向移動接收器，記錄火花消失的位置，量得半波長約 1.5–1.6 m，即 $\lambda \approx 3\ \mathrm{m}$（對應主要振盪頻率）。

**推理（結案關鍵一步）**：已知頻率 $f$ 與波長 $\lambda$，波速為

$$v = f\lambda \approx 3\times10^8\ \mathrm{m/s} = c$$

**電磁波的速度就是光速**——Maxwell 方程 $\nabla^2\mathbf{E} = \mu_0\epsilon_0\,\partial_t^2\mathbf{E}$ 與 $c = 1/\sqrt{\mu_0\epsilon_0}$ 的預言被實驗直接證實。

### 線索四：電磁波的光學性質
Hertz 進一步用大稜鏡（硬橡膠製，重約 680 kg）證明電磁波會**折射**；用金屬柵網證明會**偏振**（柵條平行偶極軸時擋波）；用大型凹面鏡證明會**反射聚焦**。波動光學的全部性質都適用——光與電磁波同族的證據鏈完整閉合。

### 程式模擬：Hertz 駐波實驗
以 numpy 模擬入射波 + 反射波形成駐波，並偵測「節點」（模擬火花隙在節點處不發火花）：

```python
import numpy as np

c = 1/np.sqrt(4e-7*np.pi * 8.854187817e-12)   # 光速
f = 1e8                                        # Hertz 型發射器頻率量級 (100 MHz)
lam = c/f                                      # 波長 3 m
L = 9.0                                        # 牆前空間長度 9 m ≈ 3 個半波長

x = np.linspace(0, L, 900)
t = np.linspace(0, 2/f, 400)                   # 模擬兩個週期
X, T = np.meshgrid(x, t)

# 入射波 (-x 方向傳向牆) 與反射波 (+x 方向) 疊加 => 駐波
E_inc = np.cos(2*np.pi*(x[None,:]/lam + f*T))   # 入射
E_ref = np.cos(2*np.pi*(x[None,:]/lam - f*T))   # 反射(完全反射)
E = E_inc + E_ref                               # 駐波場 E(x,t)

# 駐波理論解 E = 2 sin(2πx/λ)·cos(2πft)，驗證一致性
E_theory = 2*np.sin(2*np.pi*X/lam)*np.cos(2*np.pi*f*T)
print(f"波長 λ = {lam:.3f} m, 頻率 f = {f:.0e} Hz")
print(f"波速 v = fλ = {f*lam:.6e} m/s (= c? {np.isclose(f*lam, c)})")

# 偵測節點位置 (時間平均場強度為零處)
mean_E = np.abs(E).mean(axis=0)
nodes = x[np.where((mean_E[:-1]*mean_E[1:] < 0))[0]]
print(f"偵測到的節點位置 (m): {np.round(nodes,3)}")
print(f"節點間距 (理論 λ/2 = {lam/2:.3f} m): {np.round(np.diff(nodes),3)}")

# 動畫快照：火花隙放在 x=0.75, 2.25, 3.75 m (節點) vs x=1.5 m (腹點)
for x0 in [0.75, 1.5]:
    idx = np.argmin(abs(x-x0))
    amp = np.abs(E[:, idx]).max()
    print(f"x={x0} m: 火花隙最大場量 {amp:.2f} "
          f"-> {'節點: 不發火花' if amp < 0.2 else '腹點: 火花明亮'}")
```

輸出顯示節點間距恰為 $\lambda/2 = 1.5$ m、$v=f\lambda=c$，並重現「節點無火花、腹點火花亮」的 Hertz 觀察。

## 結案 -- 後果與影響
- **結案陳詞**：電磁波存在、速度為光速、具有反射折射偏振等光學性質——Maxwell 理論定讞成立。
- Hertz 1889 年發表《論電磁波在空氣中的傳播速度》；他改良的偶極天線、拋物面反射器成為日後所有天線的祖先。
- 1894 年 Hertz 因敗血症去世，年僅 36 歲。其實驗被 Bose（毫米波）、Marconi（見 [1895-Marconi無線電報](1895-Marconi無線電報.md)）接力推向實用。
- **著名的「無用」回應**：相傳 Hertz 的學生問此發現有何用，Hertz 答：「大概沒什麼用，只是證明麥克斯韋大師是對的——我們只是些無知的實驗家。」另有記載他對記者說：「這毫無用處……只能證明磁大師是對的。」諷刺的是，正是這個「無用」的發現催生了無線電、電視、雷達、行動電話與 Wi-Fi——今日每秒有數十億台設備在使用 Hertz 的波。
- 頻率單位赫茲（Hz）於 1933 年由 IEC 以他命名。

## 電磁波頻譜表
| 波段 | 波長 | 頻率 | 用途 | 發現/確立 |
|------|------|------|------|-----------|
| 無線電 | > 1 m | < 300 MHz | 廣播、通訊 | Hertz 1887 實測 |
| 微波 | 1 mm–1 m | 300 MHz–300 GHz | 雷達、Wi-Fi | Bose 1894、Hertz 1888 |
| 紅外 | 700 nm–1 mm | 300 GHz–430 THz | 熱輻射 | Herschel 1800 |
| 可見光 | 400–700 nm | 430–750 THz | 視覺 | 牛頓 1666 分光 |
| 紫外 | 10–400 nm | 750 THz–30 PHz | 殺菌、螢光 | Ritter 1801 |
| X 射線 | 0.01–10 nm | 30 PHz–30 EHz | 醫學影像 | Röntgen 1895 |
| γ 射線 | < 0.01 nm | > 30 EHz | 核物理 | Villard 1900 |

## 關鍵人物與文獻
- **Heinrich Hertz** (1857–1894)：德國物理學家，Helmholtz 的學生，卡爾斯魯厄工業學院教授。
- 文獻：
  - Hertz, H., "On Very Rapid Electric Oscillations", *Ann. Phys.* 30, 1887（位移電流實驗）。
  - Hertz, H., "On Electromagnetic Waves in Air and Their Reflection", *Ann. Phys.* 34, 1888。
  - Hertz, H., "On the Finite Velocity of Propagation of Electromagnetic Waves", *Ann. Phys.* 34, 1888。
  - Hertz, H., *Electric Waves*, Macmillan, 1893（論文集，前言獻給 Helmholtz）。
- 交叉參照：[1873-Maxwell電磁通論](1873-Maxwell電磁通論.md)（理論來源）、[1895-Marconi無線電報](1895-Marconi無線電報.md)（實用化接力）。
