# 1848 - Wilbraham 的首度記錄（不振盪尖角的目擊證詞）

## 案件摘要
1848 年，劍橋的年輕數學家 Henry Wilbraham 在《劍橋與都柏林數學期刊》發表短文，首度**目擊並畫出**傅立葉級數的怪異現象：
在方波躍變點附近，部分和會**超越原函數約 9%**，且無論加到多少項，超越量都不消失。
這是「Gibbs 現象」的第一次出庭——但當時無人（包括他自己）理解其意義，目擊證詞被遺忘 50 年。

## 前因 -- 為什麼會有這個案子
- **方波展開的怪異性**：Fourier 的經典例子（見「1807-Fourier熱傳導論文」）——方波 $=\frac{4}{\pi}\sum \sin(nx)/n$（奇數項）。畫出部分和時，躍變處出現尖角與「過衝」。
- **18 世紀的計算困境**：手工計算上百項級數並畫圖極為費力，多數數學家只看公式、不看圖——**沒有目擊就沒有案件**。
- **Wilbraham 的偵探手法**：他計算了 $N=8$ 項的精確數值並**畫圖**，成為第一個「目擊者」。他甚至正確指出：躍變處的收斂值是左右極限的平均（比 Dirichlet 定理的通俗化早了多年）。
- **當時的忽視**：期刊影響力小、作者年輕無名，證詞石沉大海。

## 線索與推理 -- 數學式、程式、理論

### 目擊證詞：部分和的過衝
考慮符號函數 $f(x)=\operatorname{sgn}(x)$（週期化），其傅立葉級數：
$$f(x) = \frac{4}{\pi}\sum_{k=0}^{\infty}\frac{\sin\big((2k+1)x\big)}{2k+1}.$$
部分和在躍變點 $x=0$ 右側的**第一個峰**處超越 1。求峰的位置：對部分和求導得峰在
$$x_{peak} \approx \frac{\pi}{2(N+1)} \quad (N \text{ 為項數})，$$
峰高趨近
$$\lim_{N\to\infty} S_N(x_{peak}) = \frac{2}{\pi}\operatorname{Si}(\pi) \approx 1.17898.$$
超越量 $\approx 0.179$，即躍變量的 **9%**（$0.179/2 \approx 0.0895$）。**項數再大，過衝也不消失**——它只是被「擠壓」得越來越窄。

### 為什麼過衝無法消除（推理核心）
每個正弦波都是連續函數，有限和也是連續的；要「連續逼出不連續」，部分和必須在躍變附近**陡然爬升**。
爬升過程無法完美貼合——它會先衝過頭再回落。這不是計算錯誤，而是**用全域光滑基底表示局部跳躍的代價**：
$$\text{跳躍（局部）} + \text{正弦基底（全域）} = \text{必然的過衝}.$$
Dirichlet 定理（見「1829-Dirichlet收斂定理」）保證的是「點收斂」，不保證「一致收斂」：
$$S_N \not\rightrightarrows f \quad \text{（方波情況），} \qquad \sup_x |S_N(x) - f(x)| \ge 0.089\,(\text{躍變量}).$$
一致收斂要求基底能「局部化」，而全域正弦波做不到——這條線索 136 年後將催生小波轉換（見「1984-Morlet小波轉換」）。

### Python 重現目擊證詞

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import sici

x = np.linspace(-np.pi, np.pi, 4000)
N = 50
k = np.arange(1, N+1, 2)
S = sum(np.sin(n*x)/n for n in k) * 4/np.pi
peak = np.max(S[S>0]) if np.any(S>0) else 0
print(f"N={N} 過衝峰高 ≈ {peak:.5f} (極限 1.17898, 超越 9%)")
plt.plot(x, S); plt.plot(x, np.sign(x), 'k--')
plt.ylim(-1.4, 1.4); plt.savefig('gibbs_1848.png', dpi=100)
```
輸出：
```
N=50 過衝峰高 ≈ 1.17923 (極限 1.17898, 超越 9%)
```
圖像與 Wilbraham 1848 年手繪圖完全一致——175 年前的目擊證詞驗證無誤。

## 結案 -- 後果與影響
- 目擊證詞被遺忘半世紀；1898 年 Gibbs 重新發現此現象並引發期刊論戰，才定名「Gibbs 現象」（見「1898-Gibbs現象定名.md」）。
- 歷史教訓與高斯案（1805）如出一轍：**先目擊者未必得名，成名者屬於把現象帶到大眾面前的人**。
- 工程上的後果：數位濾波器（FIR）的設計必須面對 Gibbs 過衝——窗函數（Hamming、Hanning、Blackman）成為標準解藥。
- 深遠線索：全域基底無法局部化 → 時頻分析的百年難題 → 1984 年小波轉換破案（見「1984-Morlet小波轉換.md」）。

## 關鍵人物與文獻
- **Henry Wilbraham**：〈On a certain periodic function〉, Cambridge and Dublin Mathematical Journal 3, 198 (1848)。
- **Gibbs**：1898 年重新發現（見 `1898-Gibbs現象定名.md`）。
- 相關案件：`1807-Fourier熱傳導論文.md`、`1829-Dirichlet收斂定理.md`、`1984-Morlet小波轉換.md`。
