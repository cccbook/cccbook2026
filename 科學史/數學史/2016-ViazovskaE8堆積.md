# 2016 - Viazovska E8 堆積

## 案件摘要
2016 年 3 月，32 歲的烏克蘭數學家 Maryna Viazovska 在 arXiv 貼出一篇論文：**證明 8 維空間中等大球的最密堆積是 E8 格**——密度 $\frac{\pi^4}{2^8 4!} = \frac{\pi^4}{384}$。**170 年懸案**（Gauss 1831 證明 3 維格情形以來的最重大突破），**方法卻簡潔得驚人**：**模形式**（傅立葉的魔杖）構造一個「輔助函數」，一次證明——**數學界震驚**：「沒有人想到會是模形式」。一週後（與 Cohn–Kumar–Miller 合作），她用同方法證明 **24 維的 Leech 格**。**Fields 獎 2022**——首位烏克蘭得主。**3 維用電腦（Hales 1998，見 `1998-HalesKepler猜想.md`），8/24 維用模形式——維度的意外**。

## 前因 -- 為什麼會有這個案子
**堆積問題的譜系**（見 `1998-HalesKepler猜想.md`）：

- **2 維**：六角堆積，$\pi/\sqrt{12} \approx 90.7\%$（Fejes Tóth 1940 證明）——**幾何的證明**
- **3 維**：FCC，$\pi/\sqrt{18} \approx 74.05\%$（Gauss 1831 格情形、Hales 1998 完整）——**電腦的證明**
- **4–7 維**：**懸**——沒有方法
- **8 維**：**E8 格**猜想（1960s 猜想）——**懸**
- **24 維**：**Leech 格**猜想——**懸**

**E8 格**：8 維中最對稱的格（248 維李群 $E_8$ 的根格）——**「完美的格」**（Cohn–Kumar 2009 猜想：E8 是 8 維最密、也是最均勻分佈）。

**Viazovska 的問題**：E8 是 8 維最密堆積嗎？——**Cohn–Kumar 的線性規劃方法**（LP bound）卡在「輔助函數的構造」——**需要一個魔杖般的函數**。

## 線索與推理 -- 數學式、程式、理論

### 線性規劃上界（LP bound）
**Cohn–Elkies 的方法（2003）**：構造函數 $f: \mathbb{R}^n \to \mathbb{R}$ 滿足：

1. $f(x) \le 0$ 當 $|x| \ge 2r$（球外非正）
2. 傅立葉變換 $\hat{f}(x) \ge 0$（**頻域非負**）

**則密度上界**：

$$\delta \le \frac{f(0)}{\hat{f}(0)} \cdot \frac{\text{Vol}(\text{球})}{2^n}$$

**難點**：構造**剛好最優**的 $f$——**魔杖函數**（圓整個上界）——**Cohn–Kumar 卡在這裡 13 年**。

### Viazovska 的模形式魔杖
**2016 年 3 月的突破**：用**模形式**（與歐拉公式、ζ 函數同源的傅立葉傳統，見 `1748-Euler公式.md`、`1859-Riemann假設.md`）構造 $f$：

**Viazovska 的函數**：

$$\varphi(x) = \int_{\mathcal{F}} \left(\frac{\sin(\pi y / 2)}{\pi y}\right)^{-2} \frac{d y}{y^{8}} \cdot \text{（theta 級數的組合）}$$

**「圓函數」的構造**：用 **Eisenstein 級數**與 **theta 級數**（格的特徵）——**一次構造、剛好最優**：

$$f(x) \le 0 \text{（球外）}， \hat{f} \ge 0 \text{，} \frac{f(0)}{\hat{f}(0)} = \text{E8 的密度} \quad \blacksquare$$

**數學界的震驚**：「**沒有人想到會是模形式**」——3 維用電腦（LP 的暴力），8 維用模形式（傅立葉的魔杖）——**維度的意外**。

**一週後**：Viazovska 與 Cohn–Kumar–Miller 用同方法證明 **24 維 Leech 格**——**兩篇論文，兩個世紀懸案**。

### 程式碼：E8 格與密度

### 密度的表列與 E8 的計數
**各維度最密堆積密度**：

| 維度 | 格 | 密度公式 | 數值 |
|------|-----|----------|------|
| 2 | 六角 | $\dfrac{\pi}{2\sqrt{3}}$ | 0.9069（90.69%） |
| 3 | FCC | $\dfrac{\pi}{\sqrt{18}}$ | 0.7405（74.05%） |
| 8 | E8 | $\dfrac{\pi^4}{384}$ | 0.2537（25.37%） |
| 24 | Leech | $\dfrac{\pi^{12}}{12!}$ | $\approx 0.00193$ |

**E8 最小向量數的計數**（240 個）：兩類向量——

$$240 = \underbrace{2^7}_{\text{半整數型 } \left(\pm\tfrac12\right)^8 \text{（符號和為偶）}} + \underbrace{8 \times 7 \times 2}_{\text{整數型 } (\pm1, \pm1, 0^6)} = 128 + 112$$

——**240 個最小向量**：8 維李群 $E_8$ 的根格，「最對稱的格」。**Leech 格**（24 維）有 $196560$ 個最小向量——**最均勻的分佈**。

**Viazovska 2016**：E8 與 Leech 的最密堆積——**模形式的魔杖**（傅立葉係數編碼格的幾何）；Fields 2022——首位烏克蘭得主。

### 模形式的魔杖
**模形式**（與 Riemann 假設同源，見 `1859-Riemann假設.md`）：上半平面的高度對稱函數——**Eisenstein 級數**、**theta 級數**——格的「特徵指紋」。

**為什麼模形式是魔杖**：**傅立葉係數編碼格的幾何**（向量數、密度）——**數論（模形式）與幾何（格）的深層連結**——與 Wiles 的費馬證明（谷山–志村，見 `1994-Wiles費馬定理.md`）同源：**模形式是數論與幾何的統一語言**。

**偵探筆記**：Viazovska 的推理是「**魔杖函數**」——LP bound 卡在輔助函數，Viazovska 用模形式一次構造。**「沒有人想到會是模形式」**——與 Apéry 的土法（1978，見 `1978-AperyZeta3.md`）、張益唐的繞過（2013，見 `2013-ZhangYitang素數間距.md`）同源：**突破常來自意想不到的方法**——而且 Viazovska 只有 32 歲（與 Galois 20 歲、Ramanujan 25 歲的年輕傳統）。

## 結案 -- 後果與影響
- **170 年懸案終結**：E8 與 Leech 格的最密堆積——**維度的意外**（電腦 vs 模形式）。
- **Fields 2022**：Viazovska——**首位烏克蘭得主、女性 Fields 的第二人**（與 Mirzakhani 2014 並列，見 `1918-Noether定理.md`）。
- **模形式的帝國**：Wiles 的費馬、BSD 猜想、Viazovska 的堆積——**數論與幾何的統一語言**。
- **球堆積的完整譜系**：2 維（幾何）、3 維（電腦）、8/24 維（模形式）——**方法的維度依賴**。
- **E8 與物理**：$E_8$ 李群——弦論（heterotic string）的對稱群——**數學物理的樞紐**（與指標定理同源，見 `1965-AtiyahSinger指標定理.md`）。
- **戰爭中的數學**：2022 年俄烏戰爭——Viazovska 的家鄉（基輔）被轟炸，Fields 頒獎（2022 年 7 月）成為**和平的象徵**。

## 關鍵人物與文獻
- **Maryna Viazovska**（1984–）：The sphere packing problem in dimension eight (2016, arXiv)；Fields 獎 2022——EPFL（洛桑）
- **Henry Cohn / Abhinav Kumar / Stephen Miller**：24 維合作（Leech 格）
- **Cohn & Elkies**：LP bound (2003)——Viazovska 的基礎
- **John Leech**（1926–1977）：Leech 格 (1967)——24 維的完美格
- **Thomas Hales**：3 維的電腦證明（見 `1998-HalesKepler猜想.md`）
- 交叉參照：`1998-HalesKepler猜想.md`、`1859-Riemann假設.md`、`1748-Euler公式.md`、`1994-Wiles費馬定理.md`、`1918-Noether定理.md`
