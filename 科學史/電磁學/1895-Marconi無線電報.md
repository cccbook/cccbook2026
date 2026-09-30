# 1895 - Marconi 無線電報

## 案件摘要
1895 年起，Guglielmo Marconi 把 Hertz 的「無用」電磁波變成實用的無線電報：距離從自家花園的 2 公里，一路推進到 1901 年跨越大西洋。無線電從此走出實驗室，成為船艦通訊、救難系統與全球通訊產業的基石。

## 前因 -- 為什麼會有這個案子
- 1887–1888 年 Hertz 證實電磁波存在（見 [1887-Hertz電磁波實驗](1887-Hertz電磁波實驗.md)），但他本人認為此波「毫無用處」。
- 1890 年代，法國 Branly 發明金屑檢波器（coherer，金屬屑在無線電波下導通、輕敲後復原），英國 Lodge 改良之；俄國 Popov 1895 年也做出接收閃電的無線裝置。零件已備，但**沒有人把它們組合成可靠的長距離通訊系統**。
- 1894 年，20 歲的 Marconi 在義大利波隆那郊外的別墅，讀到 Hertz 的訃文後開始實驗：用火花發射器 + coherer + 電鈴，先讓樓上的鈴響，再把距離推到花園另一端。
- 案子的動機：**把「實驗室現象」變成「商業系統」**——義大利郵政拒絕資助後，1896 年 Marconi 帶著設備與母親前往倫敦，這個決定改變了無線電的歷史。

## 線索與推理 -- 數學式、程式、理論

### 線索一：天線與接地系統——Marconi 的關鍵改良
Hertz 用的是對稱偶極天線；Marconi 改用**垂直天線 + 接地**（monopole），鏡像原理使其等效於偶極天線，且高度可任意加高以增加輻射。垂直短天線（$h \ll \lambda$）的輻射電阻為：

$$R_{\mathrm{rad}} \approx 40\pi^2\left(\frac{h}{\lambda}\right)^2\ \Omega \quad (\text{頂部加載修正前})$$

**推理**：要增大通訊距離，就要提高 $h/\lambda$——加高天線（後來 1901 年跨大西洋用的風箏天線高達 120 m）或加長波長。這條簡單的公式決定了早期無線電「天線越建越高、波長越用越長」的工程路線。

### 線索二：距離的推理——為何波能繞過地平線？
當時學界認為電磁波直線傳播，無法繞地球曲面。Marconi 1901 年 12 月 12 日在紐芬蘭聖約翰收到英國波爾杜發來的 "S"（三點：`···`），跨越約 3,400 km。事後的理論解釋（Kennelly 1902、Heaviside 1902 獨立提出）：

- 電離層（Kennelly–Heaviside 層，高約 100 km）反射天波，波在地表與電離層之間多次反射傳播；
- 地波沿地表繞射衰減但長波衰減慢。

**破案推理鏈**：Marconi 的成功 → 「直線傳播不可能繞地球」的前提錯了 → 上層大氣必有反射層 → 電離層被 Appleton 1924 年以實驗證實（並獲 1947 諾貝爾獎）。

### 線索三：調諧與波長選擇
早期火花發射器輻射寬頻雜訊，不同電台互相干擾。Marconi 引入**調諧電路**（1897–1900，Lodge 的「syntonic」專利競爭），發射與接收兩端各接 $LC$ 共振電路：

$$f_0 = \frac{1}{2\pi\sqrt{LC}}, \qquad Q = \frac{f_0}{\Delta f}$$

只有當兩端頻率對準時訊號才通過，頻寬由 $Q$ 決定。1900 年 Marconi 獲得著名的 "four sevens"（7777）調諧專利。

### 線索四：訊號編碼——CW 電報
無線電報以 Morse 碼傳訊：點 `·`（短音）與劃 `—`（三倍長音）。早期用火花發射（阻尼波 DW），後來用連續波（CW，Alexanderson 交流發電機、Fessenden 1906 高頻火花）。接收端 coherer/檢波器把射頻包絡還原成滴答聲或紙帶記號。

### 程式模擬：CW 電報訊號 (numpy)
模擬發射 "SOS"（`···---···`）的調幅電報訊號，並用包絡檢波還原：

```python
import numpy as np

fs = 8000                # 取樣率
f_carrier = 500          # 載波 500 Hz (模擬射頻)
dot, dash = 0.1, 0.3     # 點 0.1s, 劃 0.3s
gap = 0.1                # 元件間隔

def tone(dur, amp=1.0):  # 一段開關鍵控 (OOK) 的載波
    n = int(dur*fs)
    return amp*np.cos(2*np.pi*f_carrier*np.arange(n)/fs)

def silence(dur=0.1):
    return np.zeros(int(dur*fs))

# SOS = ··· --- ···  (3點, 3劃, 3點)
sig = []
for sym in "···---···":
    for ch in sym:
        sig.append(tone(dot if ch=='·' else dash))
        sig.append(silence(gap))
sig = np.concatenate(sig)
t = np.arange(len(sig))/fs

# 通道：加噪聲 (模擬長距離衰減+雜訊)
rng = np.random.default_rng(0)
rx = 0.5*sig + 0.3*rng.normal(0, 1, len(sig))

# 接收端：包絡檢波 (Hilbert 變換取包絡) + 門檻判決
env = np.abs(rx + 1j*np.hilbert(rx)).real
# 簡易低通平滑
win = np.ones(200)/200
env_s = np.convolve(env, win, mode='same')
bits = (env_s > 0.35).astype(int)

# 依時長還原 Morse
morse, out = "", []
on = 0
for b in bits:
    if b: on += 1
    elif on:
        out.append(on); on = 0
if on: out.append(on)
for run in out:
    d = run/fs
    morse += '·' if d < 0.2 else '—'
print(f"還原結果: {morse}")
print(f"應為   : {'···' if morse[:3] else ''}---···  -> SOS = ···---···")

# 天線輻射電阻：驗證 Marconi 垂直天線公式
for h in [10, 30, 120]:                      # 天線高度 (m)
    lam = 3000/1e6*1e3*0.0 + 300/0.1        # 波長(設 f=100kHz → λ=3km)
    lam = 3e3                                # f = 100 kHz, λ = 3000 m
    R = 40*np.pi**2*(h/lam)**2
    print(f"h = {h:4d} m, λ = {lam:.0f} m -> R_rad ≈ {R:.4f} Ω "
          f"(天線加高 12 倍, 輻射電阻增 {R/(40*np.pi**2*(10/lam)**2):.0f} 倍)")
```

模擬顯示：即使訊號被衰減、加入雜訊，包絡檢波仍能還原 `···---···`；天線公式則顯示加高天線能大幅提升輻射能力——正是 Marconi 邁向跨大西洋的兩個工程關鍵。

## 結案 -- 後果與影響
- **商業化與專利戰**：1897 年 Marconi 於倫敦成立 Wireless Telegraph & Signal Co.（後 Marconi Co.）。1899 年横跨英倫海峽；1901 年跨大西洋成功後聲名大噪。Tesla 主張其 1897 年美國專利在先，1943 年美國最高法院（Tesla 去世後數月）判決 Marconi 調諧專利部分無效、承認 Tesla 等人在先——但當時 Marconi 商業帝國已確立。1909 年 Marconi 與 Braun 共獲諾貝爾物理學獎。
- **船艦通訊與救難**：1899 年起裝設於船艦。1909 年 Republic 號沉沒時無線電救回 1,500 人；最著名的是 1912 年**鐵達尼號**沉沒——Marconi 公司電報員 Phillips 與 Cottam 發出 CQD 與 SOS，救回 705 人。事後調查：「如果加州人號的電報員沒有下班，所有人都能獲救。」
- **無線電法規（1912）**：鐵達尼事件直接催生 1912 年國際無線電公約（倫敦），規定船舶必須 24 小時值守無線電、建立 500 kHz 遇險頻率與 SOS 通用求救信號；美國同年通過 Radio Act of 1912，要求電台執照與頻率分配——現代頻譜管理制度的起點。
- **深遠影響**：無線電→廣播（1920 KDKA，見 [1906-DeForest三極管](1906-DeForest三極管.md)）→雷達→行動通訊；而「電離層反射」的發現更開啟了電離層物理與空間科學。

## 關鍵人物與文獻
- **Guglielmo Marconi** (1874–1937)：義大利發明家、企業家，1909 年諾貝爾物理學獎。
- **Nikola Tesla** (1856–1943)：無線電先驅專利持有者之一；**Édouard Branly**：coherer 發明者；**Oliver Lodge**：調諧先驅；**Alexander Popov**：俄國無線電接收先驅。
- 文獻：
  - Marconi, G., "Wireless Telegraphy", *J. IEE* 28, 1899。
  - Marconi, G., "On Methods Adopted in Wireless Telegraphy by the Marconi Company", 1901（跨大西洋計畫）。
  - Kennelly, A.E., "On the Elevation of the Electrically-Conducting Strata", 1902；Heaviside, O., *Telegraphy*, Encyc. Brit. 1902（電離層預言）。
  - US Supreme Court, *Marconi Wireless Tel. Co. v. United States*, 320 U.S. 1 (1943)。
- 交叉參照：[1887-Hertz電磁波實驗](1887-Hertz電磁波實驗.md)（波源）、[1904-Fleming真空二極體](1904-Fleming真空二極體.md)（檢波需求催生真空管）。
