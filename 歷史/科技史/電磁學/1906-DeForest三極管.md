# 1906 - DeForest 三極管

## 案件摘要
1906 年，Lee de Forest 在 Fleming 真空二極體的燈絲與板極之間加入一片金屬**柵極**，發明 Audion 三極管：微小的柵極電壓就能控制巨大的板極電流——**第一個電子放大器與振盪器誕生**。沒有放大就沒有長途電話、廣播與電子時代，而這一切都始於那片插入的柵網。

## 前因 -- 為什麼會有這個案子
- 1904 年 Fleming 的真空二極體（見 [1904-Fleming真空二極體](1904-Fleming真空二極體.md)）解決了檢波問題，但它**只能整流、不能放大**——微弱訊號整流後依然微弱。
- De Forest 是個急於證明自己的發明家：耶魯博士（1899，論文為無線電波反射）、在多家公司碰壁後自立門戶。他的第一個成功產品是「氣體檢波器」（回應式檢波器），但真正的目標是打敗 Fleming 專利。
- 1906 年，De Forest 買了幾支 Fleming valve 研究，在燈絲與板極之間**試插了各種形狀的金屬片**：薄片、柵網、甚至「之」字形金屬絲——他發現**柵網**效果最好，且奇蹟發生了：這個管子不只是檢波器，**還能放大**。
- 案子的懸念：De Forest 當時**並不理解放大原理**（他堅稱管內氣體殘留是關鍵，其實高真空才是），真正物理要到 1919 年後才被 Langmuir、Arnold（AT&T）等人釐清。**發明跑在理解前面**——但那片柵極改變了世界。

## 線索與推理 -- 數學式、程式、理論

### 線索一：三極管的結構與符號
```
        板極 P (anode, +)          電路符號:
        |                          ─┬─ F 燈絲(陰極)
     ┌──┴──┐                      ─┼─ G 柵極
     │ G  ─┼── 柵極 (grid)         ─┴─ P 板極
     │     │
     │ F  ─┼── 燈絲 (filament, 熱電子源)
     └─────┘     真空玻璃管
```

電子在燈絲（陰極）被加熱逸出，受板極正電壓吸引飛向板極，形成板極電流 $I_p$。柵極位於兩者之間——**離燈絲極近**。

### 線索二：放大原理——柵極的槓桿效應（破案核心）
柵極電壓 $V_g$ 微小變化，會強烈改變陰極附近的電場，從而**大幅改變**板極電流：

$$I_p = k\,(V_p + \mu V_g)^{3/2} \quad (\text{三極管 Child–Langmuir 修正式})$$

其中 $\mu$ 為**放大係數**（amplification factor）：柵極電壓對板極電流的控制能力等效於多少倍板極電壓：

$$\boxed{\ \mu = \frac{\Delta V_p}{\Delta V_g}\bigg|_{I_p\text{不變}}\ }$$

**推理**：因為柵極離陰極極近、且對電子「透明」（柵網讓電子穿過），$V_g$ 的小變化 ≫ $V_p$ 的大變化對空間電荷的影響。典型 $\mu = 3\text{–}100$。

**放大電路**：把微弱輸入訊號加在柵極，板極接高壓電源與負載電阻 $R_L$：

$$v_{\mathrm{out}} = -R_L\,\Delta I_p \approx -g_m R_L\, v_{\mathrm{in}}, \qquad g_m = \frac{\partial I_p}{\partial V_g}$$

增益為 $A_v = g_m R_L \gg 1$——**微弱訊號被複製放大了**：能量來自板極電源，柵極只是「閥門的指揮」。

### 線索三：振盪器的誕生
放大器 + 正回授 = 振盪器。1912 年 Armstrong 的再生式電路把板極輸出回授到柵極，當迴路增益滿足 Barkhausen 條件時電路自激振盪：

$$|A_v \beta| \ge 1, \qquad \angle A_v \beta = 2\pi n$$

**推理鏈**：二極體只能檢波 → 三極管能放大 → 放大器能振盪產生連續波（CW）→ 連續波能載語音（調幅廣播）→ **無線電從電報走進聲音的時代**。

### 線索四：增益的數學——分貝 (dB)
放大器的增益以對數刻度表示：

$$G_{\mathrm{dB}} = 20\log_{10}\left(\frac{v_{\mathrm{out}}}{v_{\mathrm{in}}}\right) = 10\log_{10}\left(\frac{P_{\mathrm{out}}}{P_{\mathrm{in}}}\right)$$

例如 $A_v = 10$ → 20 dB；$A_v = 100$ → 40 dB；多級放大增益相加（對數的好處）：三級 20 dB 級聯 = 60 dB = 1,000 倍。

### 程式模擬：三極管放大 (numpy)
模擬微弱語音訊號加在柵極、板極輸出放大的波形，並驗證增益 dB：

```python
import numpy as np
import matplotlib.pyplot as plt

fs = 100e3
t = np.arange(0, 5e-3, 1/fs)

# 微弱輸入訊號 (如麥克風/天線): 10 mV 語音 (以 1 kHz 正弦代表)
vin = 0.01*np.sin(2*np.pi*1e3*t)

# --- 三極管模型: Ip = k*(Vp + mu*Vg)^1.5 (板極偏壓 Vp, 負載 RL) ---
mu, k, Vp, RL = 20.0, 1e-6, 100.0, 10e3
Vg = vin                                    # 柵極訊號 (偏壓為0的簡化)
Ip = k*np.maximum(Vp + mu*Vg, 0)**1.5       # 板極電流 (A)
vout = -RL*Ip                               # 板極輸出電壓
# 去除直流偏置, 取交流分量
vac = vout - vout.mean()

# --- 增益計算 ---
gain = np.sqrt((vac**2).mean()/(vin**2).mean())   # rms 增益
gain_db = 20*np.log10(gain)
print(f"輸入振幅 = {vin.max()*1e3:.1f} mV")
print(f"輸出振幅 = {vac.max():.2f} V")
print(f"電壓增益 A_v = {gain:.1f} 倍 = {gain_db:.1f} dB")
print(f"理論小訊號增益 ≈ gm*RL, gm ≈ dIp/dVg = {k*1.5*(Vp)**0.5*mu*1e3:.3f} mS")
print(f"理論增益 ≈ {k*1.5*(Vp)**0.5*mu*RL:.1f} 倍 (模擬 vs 理論吻合)")

# --- 多級級聯: 3 級 20dB -> 1000 倍 ---
A_stage = 10
print(f"\n3 級 x{A_stage} 級聯: {3*20*np.log10(A_stage):.0f} dB "
      f"= {A_stage**3} 倍 (對數增益相加)")

# --- 驗證 mu 定義: 保持 Ip 不變, ΔVp/ΔVg ---
dVg = 1.0
dVp_needed = -mu*dVg                        # 柵壓+1V 需板壓 -20V 才能抵消
Ip1 = k*(Vp + mu*0)**1.5
Ip2 = k*((Vp+dVp_needed) + mu*dVg)**1.5
print(f"\nμ 定義驗證: ΔVg = +{dVg} V, ΔVp = {dVp_needed} V "
      f"-> Ip 不變? {np.isclose(Ip1, Ip2)} (μ = {abs(dVp_needed/dVg):.0f})")

# 繪圖
fig, ax = plt.subplots(2, 1, figsize=(9, 5), sharex=True)
ax[0].plot(t*1e3, vin*1e3, color='tab:blue')
ax[0].set_ylabel("柵極輸入 (mV)"); ax[0].set_title("Audion 三極管放大: 柵極控制板極電流")
ax[1].plot(t*1e3, vac, color='tab:red')
ax[1].set_ylabel("板極輸出 (V)"); ax[1].set_xlabel("時間 (ms)")
plt.tight_layout(); plt.savefig("audion_amp.png", dpi=120)
print("已儲存波形圖 audion_amp.png")
```

模擬顯示：10 mV 的柵極訊號被放大為數伏的板極輸出，增益與 $g_m R_L$ 理論吻合，$\mu = \Delta V_p/\Delta V_g$ 定義也經數值驗證——**那片柵網的槓桿效應寫成了程式碼**。

## 結案 -- 後果與影響
- **結案陳詞**：柵極使真空管從「閥」變成「放大器」；電子學因此獲得放大、振盪、開關三大能力，整個電子時代的地基完成。
- **廣播時代**：1912 年 Armstrong 再生電路 + De Forest 三極管使收音機靈敏度大增；1920 年 11 月 2 日匹茲堡 **KDKA** 開播——世界第一座正式廣播電台（播報 Harding 當選總統）。1920 年代全美電台爆炸成長，「收音機」從電報員的機器變成客廳家具。De Forest 自己也率先做音樂廣播實驗（1916 年紐約）。
- **專利糾紛與商業人生**：Fleming 控告 De Forest 侵權，美國法院判決 De Forest 專利有效但須付權利金（「閥」的專利屬 Fleming，柵極的用法屬 De Forest）；De Forest 與 Armstrong 的再生式電路專利之爭更纏訟 12 年、上訴 12 次，Armstrong 最終敗訴抑鬱自殺（1954）——電子史上最沉重的訴訟悲劇。De Forest 自稱「廣播之父」，一生獲 300 餘項專利，1950 年代曾嘗試電視投資失敗，1961 年去世。
- **深遠影響**：三極管 → 長途電話中繼放大（1915 年 AT&T 橫貫大陸電話）→ 雷達 → 電視 → 電腦（ENIAC）→ 1947 年電晶體（Bardeen、Brattain、Shockley 在 Bell 實驗室，以固態接面重現「柵極控制電流」的概念）→ 積體電路。「用微小訊號控制大電流」——從真空管的柵極到電晶體的基極，同一個思想統治了電子學百年。

## 關鍵人物與文獻
- **Lee de Forest** (1873–1961)：美國發明家，耶魯博士，Audion 三極管發明人。
- **John Ambrose Fleming**：二極體（Audion 的前身）發明人。
- **Edwin Armstrong** (1890–1954)：再生式電路、超外差、FM 發明人。
- **Irving Langmuir** (1881–1957)：高真空三極管工藝（1913，AT&T），1932 年諾獎（化學）。
- 文獻：
  - de Forest, L., "Oscillation Receiver" (Audion), U.S. Patent 836,070, 1906（申請）/ 841,387, 1907。
  - de Forest, L., "The Audion—A New Receiver for Wireless Telegraphy", *Trans. AIEE* 25, 1906。
  - Armstrong, E.H., "Some Recent Developments of Regenerative Circuits", *Proc. IRE* 10, 1922。
  - Barkhausen, H., *Lehrbuch der Elektronen-Röhren*, 1928（振盪條件）。
- 交叉參照：[1904-Fleming真空二極體](1904-Fleming真空二極體.md)（前身）、[1895-Marconi無線電報](1895-Marconi無線電報.md)（電報→廣播的跨越）。
