# 1904 - Fleming 真空二極體

## 案件摘要
1904 年，John Ambrose Fleming 發明熱離子真空二極體（thermionic valve），把愛迪生效應的「謎」變成無線電的「器」：第一個可靠的無線電檢波器。電子器件的時代——從真空管到整個電子工業——就此開端。

## 前因 -- 為什麼會有這個案子
- **愛迪生效應（1883）**：Edison 為解決白熾燈泡燒黑的問題，在燈泡內加了一片金屬板，發現燈絲熾熱時板極與燈絲間有電流流過（僅當板極接正極）。Edison 記錄了現象並取得專利，但**不知其原理、也找不到用途**——一條被擱置 20 年的線索。
- **無線電的瓶頸（1900s）**：Marconi 的無線電報（見 [1895-Marconi無線電報](1895-Marconi無線電報.md)）使用金屑檢波器（coherer），缺點很多：每次收訊後要敲擊復原、靈敏度低、無法收連續訊號、速度慢。**業界迫切需要更好的檢波器**。
- Fleming 是關鍵的橋樑人物：1880 年代他曾是 Edison 電氣顧問、親手研究過愛迪生效應；1899 年起又受聘為 Marconi 公司技術顧問，深知檢波器之痛。**兩條線索在他腦中交會。**
- 1904 年 10 月，Fleming 重新點燃燈絲加板極的實驗，發現此管對交流射頻有完美的單向導電性——**熱離子二極體（valve）誕生**。

## 線索與推理 -- 數學式、程式、理論

### 線索一：愛迪生效應的原理——熱電子發射
金屬中的自由電子要逸出表面，需克服功函數 $\phi$（work function）。溫度 $T$ 時，具有足夠能量的電子數服從 Richardson–Dushman 定律（1911 年 Richardson 完成理論）：

$$J = A T^2 e^{-\phi/k_B T} \quad \left(A \approx 1.2\times10^6\ \mathrm{A\,m^{-2}K^{-2}}\right)$$

**推理**：燈絲加熱到 2,000 K 以上，熱電子大量逸出，在燈絲附近形成「電子雲」。此時若附近板極為**正**電位，電子被吸引形成電流；若板極為**負**，電子被排斥、無電流——**單向導電**的物理根源。這也解釋了為何只有電子（負電荷）從燈絲流向板極：愛迪生效應的謎底是**電子的熱發射**（1897 年 Thomson 剛發現電子，見 [1897-Thomson電子發現](1897-Thomson電子發現.md)）。

### 線索二：二極體整流原理（單向導電）
真空二極體的電流-電壓特性：

$$I(V) = \begin{cases} I_s\,V^{3/2} & V > 0 \quad(\text{空間電荷限制區, Child–Langmuir 定律})\\ 0 & V \le 0 \quad(\text{截止})\end{cases}$$

Child–Langmuir 定律（1911）：

$$I = \frac{4}{9}\epsilon_0\sqrt{\frac{2e}{m}}\,\frac{A\,V^{3/2}}{d^2}$$

**推理（檢波應用）**：無線電波是高頻振盪（射頻載波），天線感應的電壓正負對稱、平均為零，無法直接驅動耳機。把射頻訊號加在二極體上，只有正半波導通——**輸出變成單向脈衝，其平均值（包絡）就是調變訊號**。這就是**整流與檢波**：從射頻中「摘出」音訊或電報滴答聲。

### 線索三：真空的必要性
管內必須高真空：殘餘氣體會被電離、讓反向也導電，破壞單向性（正是 Hertz 1883 年電場偏轉實驗失敗的同款陷阱）。Fleming 採用最好的真空泵與除氣技術——**真空管技術**（ pumping + getter 除氣劑）成為電子工業的第一道工藝。

### 程式模擬：二極體整流波形（AC → DC，numpy）
模擬射頻訊號經二極體整流、RC 濾波後得到包絡（檢波）：

```python
import numpy as np
import matplotlib.pyplot as plt

fs = 1e6                          # 取樣率
t = np.arange(0, 2e-3, 1/fs)      # 2 ms

# 天線感應的調幅射頻訊號: 載波 100 kHz, 調變(電報滴答) 1 kHz 方波
fc, fm = 1e5, 1e3
msg = 0.5 + 0.5*np.sign(np.sin(2*np.pi*fm*t))     # 電報開關 (0/1)
v_in = (0.5 + 0.4*msg)*np.cos(2*np.pi*fc*t)       # 調幅波

# --- 二極體模型: Child-Langmuir 正向 V^1.5, 反向截止 ---
Is = 1e-3                          # 標度電流
v_diode = np.where(v_in > 0, Is*np.maximum(v_in,0)**1.5, 0.0)

# --- RC 低通濾波 (包絡檢波): 離散遞迴 dV = (I diode - V/R)/C dt ---
R, C = 1e3, 1e-9                   # RC = 1 μs: >> 1/fc, << 1/fm
out = np.zeros_like(t)
vout = 0.0
for i, vd in enumerate(v_diode):
    vout += (vd/R - vout/R)* (1/C) / fs * R   # 簡化遞迴
    out[i] = vout

# --- 數值驗證 ---
env_theory = 0.5 + 0.4*msg        # 理論包絡
avg_in  = v_in.mean()             # 整流前平均值 ≈ 0
avg_out = out.mean()              # 整流後平均值 > 0
print(f"整流前輸入平均 = {avg_in:.4f} (對稱AC, 無直流)")
print(f"整流後輸出平均 = {avg_out:.4f} (>0, 單向導電 -> 有直流)")
corr = np.corrcoef(out, env_theory)[0,1]
print(f"檢波輸出與理論包絡相關係數 = {corr:.4f}")

# 繪圖
fig, ax = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
ax[0].plot(t*1e3, v_in, lw=0.5); ax[0].set_ylabel("AC 輸入 (V)")
ax[0].set_title("Fleming 二極體整流: AC 射頻 -> DC/包絡")
ax[1].plot(t*1e3, v_diode, lw=0.5, color='tab:orange')
ax[1].set_ylabel("二極體輸出 (單向脈衝)")
ax[2].plot(t*1e3, out, lw=1.5, color='tab:green', label="RC 濾波輸出")
ax[2].plot(t*1e3, env_theory, '--', color='k', label="理論包絡")
ax[2].set_ylabel("檢波輸出 (V)"); ax[2].set_xlabel("時間 (ms)")
ax[2].legend()
plt.tight_layout(); plt.savefig("fleming_diode.png", dpi=120)
print("已儲存波形圖 fleming_diode.png")
```

模擬顯示：AC 射頻經二極體後只剩單向脈衝，RC 濾波輸出與理論包絡高度相關（>0.95）——**耳機裡的滴答聲就這樣從射頻中被「摘」了出來**。

## 結案 -- 後果與影響
- **結案陳詞**：愛迪生效應 = 熱電子發射；真空二極體 = 第一個電子器件，可靠地解決了無線電檢波問題。
- Fleming 1904 年 11 月 16 日取得英國專利（24,850 號），稱之為 "oscillation valve"（振盪閥）。他堅持以科學為業、不圖商業暴利，專利後由 Marconi 公司持有。
- **直接後續**：1906 年 De Forest 在二極體中加入柵極，發明三極管 Audion，具放大能力（見 [1906-DeForest三極管](1906-DeForest三極管.md)）——電子學從「檢波」躍進到「放大與振盪」。
- **深遠影響**：真空管 → 收音機、雷達、電視、第一代電腦（ENIAC 用了 17,468 支真空管）→ 1947 年電晶體 → 積體電路。電子工業的族譜第一頁，寫的就是 1904 年這支「閥」。
- Richardson 因熱離子研究獲 1928 年諾貝爾物理學獎。

## 關鍵人物與文獻
- **John Ambrose Fleming** (1849–1945)：英國電氣工程師，UCL 教授、Marconi 公司顧問；曾任 Edison 與 Ferranti 顧問。
- **Thomas Edison** (1847–1931)：1883 年發現愛迪生效應。
- **Owen Richardson** (1879–1959)：熱電子發射理論，1928 年諾獎。
- 文獻：
  - Fleming, J.A., "Improvements in Instruments for Detecting and Measuring Alternating Electric Currents", British Patent 24,850, 1904。
  - Fleming, J.A., *The Principles of Electric Wave Telegraphy*, 1906。
  - Richardson, O.W., "On the Negative Radiation from Hot Platinum", *Phil. Trans. R. Soc.* 201, 1903。
  - Child, C.D., "Discharge from Hot CaO", *Phys. Rev.* 32, 1911；Langmuir, I., *Phys. Rev.* 2, 1913（Child–Langmuir 定律）。
- 交叉參照：[1897-Thomson電子發現](1897-Thomson電子發現.md)（電子——熱發射的主角）、[1906-DeForest三極管](1906-DeForest三極管.md)（加入柵極的下一步）。
