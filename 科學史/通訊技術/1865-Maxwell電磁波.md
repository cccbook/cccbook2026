# 1865 - Maxwell 電磁波（光的真相與無線電的預言）

## 案件摘要
1865 年，James Clerk Maxwell 發表〈A Dynamical Theory of the Electromagnetic Field〉：
提出**位移電流**，並證明電磁場以有限速度傳播：
$$\frac{\partial^2 \mathbf{E}}{\partial x^2} = \mu_0\varepsilon_0\,\frac{\partial^2 \mathbf{E}}{\partial t^2}
\quad\Longrightarrow\quad c = \frac{1}{\sqrt{\mu_0\varepsilon_0}} \approx 3\times10^8\ \text{m/s}.$$
**光就是電磁波**。這個等式同時預言了無線電的存在（1887 Hertz 驗證）與相對論的光速不變（見「相對論/1905-狹義相對論.md」）——
通訊技術的物理地基在此奠定。

## 前因 -- 為什麼會有這個案子
- **電與磁的分立**：Oersted（1820）發現電生磁、Ampère 發現磁生電，但兩套理論各自為政——**沒有統一**。
- **Faraday 的線索（1831–1843）**：Faraday 發現**電磁感應**（變化的磁場生電）與「力線」的場觀點——但**沒有數學**。馬克斯威爾的任務：把 Faraday 的直覺寫成方程式。
- **一個致命的矛盾**：Ampère–Maxwell 電路定律在**充電的電容器**中失效——
  $$\oint \mathbf{B}\cdot d\boldsymbol{\ell} = \mu_0\left(I_{\text{導線}} + \varepsilon_0\frac{d\Phi_E}{dt}\right).$$
  Maxwell 加上**位移電流**項 $\varepsilon_0\,d\Phi_E/dt$ 修好漏洞——
  $$\boxed{\text{位移電流} = \text{導線電流}}$$
  這是 19 世紀最深刻的一步：它證明電場與磁場是同一個場的兩面。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：Maxwell 方程組（四式統一）
$$\begin{aligned}
\nabla\cdot\mathbf{E} &= \frac{\rho}{\varepsilon_0} & \text{(高斯定律)}\\
\nabla\times\mathbf{E} &= -\frac{\partial\mathbf{B}}{\partial t} & \text{(Faraday 感應)}\\
\nabla\cdot\mathbf{B} &= 0 & \text{(無磁單極子)}\\
\nabla\times\mathbf{B} &= \mu_0\mathbf{J} + \mu_0\varepsilon_0\frac{\partial\mathbf{E}}{\partial t} & \text{(Ampère-Maxwell)}
\end{aligned}$$
推導波動方程（**通訊方程的原型**）：
$$\nabla^2\mathbf{E} = \mu_0\varepsilon_0\,\frac{\partial^2\mathbf{E}}{\partial t^2}.$$
**場的擾動像波一樣傳播**——這是「以有限速度傳遞訊息」第一次被寫成方程式。

### 第二條線索：光的統一
光是電磁波：光是波（1820，Biot）、光在介質中（Maxwell 認為以太）——匹配全中。
$$\text{光的折射率} = \frac{c}{\sqrt{\varepsilon_r\mu_r}}.$$
這個預言 1887 年由 Hertz 用微波驗證——**物理學從此統一**（光、電、磁同一套方程）。

### 第三條線索：通訊的物理預言
波動方程的解是**任意波形以速度 c 傳播**——這意味著**可以透過調變波來傳送資訊**：
$$\mathbf{E}(z,t) = E_0 \cos(\omega t - kz)\quad \xrightarrow{\text{調變載波}} \text{傳送訊號}.$$
- 1887 Hertz 用火花隙（$1$ 米火花）產生並接收 8 mm 微波——**無線電的實驗證明**。
- 1895 Marconi 用更靈敏的接收器（coherer，$\text{金屬粉末}$）——見「1895-馬可尼無線電報.md」。

### 證據與工具：波速預言的數值檢驗

Maxwell 的理論給出一個可以立刻檢驗的數值預言：真空波速完全由兩個電磁常數決定，

$$c = \frac{1}{\sqrt{\mu_0 \varepsilon_0}} = \frac{1}{\sqrt{(4\pi\times10^{-7})(8.854\times10^{-12})}} \approx 2.9979\times10^{8}\ \text{m/s}.$$

| 項目 | 數值 |
|------|------|
| Maxwell 預言（$1/\sqrt{\mu_0\varepsilon_0}$） | $2.9979\times10^{8}$ m/s |
| 實測光速（定義值） | $2.99792458\times10^{8}$ m/s |
| 相對誤差 | $< 0.01\%$ |

這個吻合度是 19 世紀最深刻的物理統一證據——電、磁、光被同一套方程收編。配套的關鍵概念是**位移電流**：對平行板電容器（面積 $A$、間距 $d$），即使極板間沒有電荷流過，充電時電場仍在變化，

$$I_{\text{位移}} = \varepsilon_0 \frac{d\Phi_E}{dt} = \varepsilon_0 A \frac{dE}{dt} = I_{\text{導線}},$$

位移電流恰好等於導線電流，修補了 Ampère 定律在電容器處的漏洞，使 $\nabla\times\mathbf{B}$ 方程對所有情形自洽——波動方程於焉誕生。

## 結案 -- 後果與影響
- **光 = 電磁波**：統一光學與電磁學，徹底改變物理學。
- **無線電的預言與實現**：Hertz 1887 驗證微波 → Marconi 無線電報（見「1895-馬可尼無線電報.md」）→ 廣播、電視、雷達——**整個無線時代的物理來源**。
- **相對論的前提**：光速不變是 Maxwell 方程的內稟性質——Einstein 1905 的起點（見「相對論/1905-狹義相對論.md」）。
- **通訊方程的源頭**：波動方程 = 今日天線理論、導波理論、光纖理論的母方程。
- 歷史定位：Maxwell 不是實驗家，是**純數學推導**出不可見的電磁波——**理論預言實驗**的典範案例。1887 年 Hertz 的實驗比 Maxwell 逝世的 1879 年還晚 8 年。

## 關鍵人物與文獻
- **J. C. Maxwell**：〈A Dynamical Theory of the Electromagnetic Field〉, Phil. Trans. R. Soc. 155, 325 (1865)；《Treatise on Electricity and Magnetism》(1873)。
- **M. Faraday**：電磁感應 (1831)；**H. Hertz**：微波實驗 (1887)。
- 相關案件：`1838-摩斯電報.md`、`1895-馬可尼無線電報.md`、`相對論/1905-狹義相對論.md`。
