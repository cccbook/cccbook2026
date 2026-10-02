# 1748-Euler 分析引論

## 案件摘要
1748 年，Euler 出版《Introductio in analysin infinitorum》（無窮分析引論），把「函數」從幾何曲線的附屬品升格為分析學的核心研究對象，並系統化處理指數、對數與三角函數。這本書是「代數」與「分析」兩大陸塊正式交會的現場，Euler 恒等式 $e^{i\pi}+1=0$ 就是交會點上最耀眼的物證。

## 前因 -- 為什麼會有這個案子
- 17 世紀 Newton 與 Leibniz 建立微積分，但當時「函數」仍指一條幾何曲線，或一個由式子「拼出來」的表達式，缺乏獨立地位。
- 1727 年前後 Euler 在研究指數函數時，發現 $(1+x/n)^n \to e^x$，並且透過級數比較，發現指數函數與三角函數之間存在神秘的關聯（複數即將登場）。
- Bernoulli 家族（Johann、Daniel）在級數、對數論證（如 $\log(-1)$ 是否等於 $\log(1)$ 的爭論）上留下大量線索，迫使數學家認真對待「什麼是函數」這個問題。
- Euler 意識到：要讓分析學成為一門嚴密的科學，必須先有一部「函數學」的基礎教材——這就是《引論》的誕生動機。

## 線索與推理 -- 數學式、程式、理論

### 線索一：函數概念的現代化
Euler 在《引論》第一節就寫下定義：**「函數是由變數與常數以任何方式組成的解析表達式」**（A function of a variable quantity is an analytic expression composed in any way from that variable quantity and numbers or constant quantities）。

他推廣並普及了記號 $f(x)$（此記法由 Johann Bernoulli 於 1718 年首用，Euler 將其發揚光大成為標準）：
$$y = f(x), \quad f(x) = x^2 + ax + b$$

並區分：
- 單變數與多變數函數：$f(x)$、$f(x,y)$
- 顯函數與隱函數
- 代數函數與超越函數（$e^x$、$\sin x$、$\log x$ 屬後者）

這個定義雖然仍限於「解析表達式」，但已把函數變成**研究的對象本身**，而非曲線的影子——這是通往 Dirichlet「任意對應」定義（1837）的第一步。

### 線索二：$e^x$ 與三角函數的分析處理
Euler 用純代數手段（二項式展開）「煉出」指數函數：
$$e^x = \lim_{n\to\infty}\left(1+\frac{x}{n}\right)^n = \sum_{n=0}^{\infty}\frac{x^n}{n!}$$

三角函數也以級數現身：
$$\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots, \qquad \cos x = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \cdots$$

並建立極限式（今日稱 Euler 極限）：
$$\lim_{x\to 0}\frac{\sin x}{x} = 1$$

### 線索三：Euler 恒等式——代數與分析的交會
把 $x = i\theta$ 代入指數級數：
$$e^{i\theta} = \sum_{n=0}^\infty \frac{(i\theta)^n}{n!}
= \sum_{k=0}^\infty \frac{(-1)^k \theta^{2k}}{(2k)!} + i\sum_{k=0}^\infty \frac{(-1)^k \theta^{2k+1}}{(2k+1)!}
= \cos\theta + i\sin\theta$$

取 $\theta = \pi$，得 Euler 恒等式：
$$e^{i\pi} + 1 = 0$$

五個最重要的常數 $e,\ i,\ \pi,\ 1,\ 0$ 在一個式子裡會師——這正是「代數」（常數與多項式）與「分析」（極限與級數）的交會證據。

### 程式碼：Python numpy 驗證 Euler 恒等式

```python
import numpy as np

# 用級數與 numpy 的複數運算雙重驗證 e^{i*pi} + 1 = 0

# 方法一：直接用 numpy 複數指數
lhs1 = np.exp(1j * np.pi) + 1
print("numpy exp:", lhs1)  # 接近 1.2246e-16j + 1，誤差為浮點極限

# 方法二：用級數重造 e^{i*pi}
N = 30
n = np.arange(N)
series = np.sum((1j * np.pi) ** n / np.array([np.math.factorial(k) for k in n]))
print("級數逼近:", series + 1)  # 幾乎為 0

# 方法三：檢驗 cos(pi) + i sin(pi)
lhs3 = np.cos(np.pi) + 1j * np.sin(np.pi) + 1
print("cos + i sin:", lhs3)
```

## 結案 -- 後果與影響
- **結案**：《引論》使「函數」成為分析學的原子概念；指數、對數、三角函數被統一在複數的框架下（Euler 公式）。分析學從此有了「以函數為中心」的教科書範式。
- 深遠影響一：Cauchy、Weierstrass 的嚴格分析（極限、連續、級數收斂）都建立在 Euler 的函數概念之上。
- 深遠影響二：Euler 公式成為複分析、Fourier 分析、量子力學（相位因子 $e^{i\theta}$）的基石。
- 深遠影響三：函數概念一路演進——Dirichlet（1837，任意對應）→ Dedekind（映射觀點）→ 集合論（20 世紀），皆源於 1748 年這次「函數獨立宣言」。

## 關鍵人物與文獻
- **Leonhard Euler（1707–1783）**：史上最多產的數學家，《引論》被譽為數學史上最偉大的教科書之一。
- **Johann Bernoulli（1667–1748）**：Euler 的老師，$f(x)$ 記法的首創者。
- 文獻：L. Euler, *Introductio in analysin infinitorum*, Tomus I, Lausanne, 1748。
- 延伸：Euler, *Institutiones calculi differentialis* (1755)；Dirichlet, "Über die Darstellung ganz willkürlicher Functionen..." (1837)。
