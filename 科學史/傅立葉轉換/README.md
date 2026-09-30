# 傅立葉轉換史 -- AI 偵探風格

以「推理探案」的方式，追查傅立葉轉換從琴弦振動之謎到 JPEG 影像壓縮的每一步：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個數學、物理與數位世界？
核心謎題只有一個：**任何訊號，真的都能拆成一堆正弦波的疊加嗎？**

## 案件卷宗（歷史年表）

### 前奏：琴弦與複數的啟蒙（1748–1805）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1748 | Euler 發表尤拉公式 $e^{i\theta} = \cos\theta + i\sin\theta$，複指數成為萬用基底 | [1748-Euler公式.md](1748-Euler公式.md) |
| 1753 | Daniel Bernoulli 主張琴弦振動是無限多個簡正模的疊加 | [1753-Bernoulli疊加原理.md](1753-Bernoulli疊加原理.md) |
| 1805 | 高斯在未發表的插值手稿中，暗中發明了 FFT 的核心思想 | [1805-高斯的隱藏FFT.md](1805-高斯的隱藏FFT.md) |

### 案發與論戰：傅立葉級數的誕生（1807–1848）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1807 | Fourier 提交熱傳導論文，大膽主張「任意函數皆可展開為三角級數」 | [1807-Fourier熱傳導論文.md](1807-Fourier熱傳導論文.md) |
| 1822 | Fourier 出版《熱的分析理論》，級數展開正式問世 | [1822-熱的分析理論.md](1822-熱的分析理論.md) |
| 1829 | Dirichlet 嚴格證明收斂條件，平息「任意函數」論戰 | [1829-Dirichlet收斂定理.md](1829-Dirichlet收斂定理.md) |
| 1848 | Wilbraham 首度發現方波展開的不振盪尖角（後稱 Gibbs 現象） | [1848-WilbrahamGibbs現象.md](1848-WilbrahamGibbs現象.md) |

### 從級數到積分與取樣（1898–1948）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1898 | Gibbs 解釋方波躍變處的 9% 超越量，現象定名「Gibbs 現象」 | [1898-Gibbs現象定名.md](1898-Gibbs現象定名.md) |
| 1948 | Shannon 發表取樣定理：帶寬 $B$ 的訊號只需 $2B$ 取樣率即可完全重建 | [1948-Shannon取樣定理.md](1948-Shannon取樣定理.md) |

### 數位革命：FFT 與應用（1965–1992）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1965 | Cooley 與 Tukey 發表 FFT 演算法，$O(N^2) \to O(N\log N)$，傅立葉分析走進所有電腦 | [1965-FFT快速傅立葉轉換.md](1965-FFT快速傅立葉轉換.md) |
| 1984 | Morlet 與 Grossmann 提出小波轉換，突破傅立葉的「全域頻率」限制 | [1984-Morlet小波轉換.md](1984-Morlet小波轉換.md) |
| 1992 | JPEG 標準採用離散餘弦變換（DCT），傅立葉家族壓縮全世界影像 | [1992-JPEG離散餘弦變換.md](1992-JPEG離散餘弦變換.md) |

## 關鍵人物年表

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 1748 | Leonhard Euler | 尤拉公式、複指數基底 |
| 1753 | Daniel Bernoulli | 簡正模疊加原理 |
| 1805 | Carl Friedrich Gauss | 未發表的 FFT 雛形 |
| 1807/1822 | Joseph Fourier | 熱傳導、傅立葉級數 |
| 1829 | Peter Gustav Dirichlet | 級數收斂條件 |
| 1848 | Henry Wilbraham | Gibbs 現象首度記錄 |
| 1898 | Josiah Willard Gibbs | Gibbs 現象的解釋與定名 |
| 1948 | Claude Shannon | 取樣定理 |
| 1965 | James Cooley / John Tukey | FFT 演算法 |
| 1984 | Jean Morlet / Alex Grossmann | 小波轉換 |
| 1992 | JPEG 團隊（Wallace 等） | DCT 影像壓縮標準 |
