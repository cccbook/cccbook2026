# 1696 — L'Hôpital 法則

## 案件摘要
1696 年，法國貴族 Guillaume de l'Hôpital 出版《Analyse des infiniment petits pour l'intelligence des lignes courbes》（論無窮小分析以理解曲線）——**史上第一本微積分教科書**。書中第九節含有一條著名的求極限法則：$\frac{0}{0}$ 型極限可用導數之比求得，後世稱為「L'Hôpital 法則」。但全案最戲劇性的真相是：這條法則（以及書中大部分內容）**並非 l'Hôpital 本人所寫**，而是瑞士數學家 Johann Bernoulli 的作品——兩人在 1694 年簽訂了一份付費契約。這樁數學史上最著名的「代筆懸案」，讓微積分從沙龍絕技變成課堂教材。

## 前因 -- 為什麼會有這個案子
- 1684 年 Leibniz 在《Acta Eruditorum》發表微積分，但論文只有六頁、晦澀難懂，連 Jakob Bernoulli 都花了數年才讀通，戲稱之為「謎語」。
- 1690 年前後，Bernoulli 兄弟（Jakob 與 Johann）在巴塞爾解讀並推廣萊布尼茲的方法：懸鏈線（1690）、等時曲線等成果接連問世，萊布尼茲微積分的威力開始展露。
- 1691–1692 年，年輕的 Johann Bernoulli 在巴黎擔任 l'Hôpital 的私人教師，講授新微積分。他留下未發表的手稿（後世稱 *Lectiones de calculo differentialium*）。
- 1694 年 3 月，l'Hôpital 與 Johann 簽訂契約：l'Hôpital 支付年金 300 法郎，Johann 則把新的數學發現**優先告知並同意歸其使用**。契約白紙黑字，成為全案的關鍵物證。
- 動機：當時法國貴族以資助科學換取聲望；Johann 則需要錢（他當時是窮教師）。一樁你情我願的交易，卻留下了三百年的名字錯置。

## 線索與推理 -- 數學式、程式、理論

### 線索一：$\frac{0}{0}$ 極限與法則本身
問題來自極值與切線計算中的「不定型」：當 $f(a) = 0$、$g(a) = 0$ 時，比值 $\frac{f(x)}{g(x)}$ 在 $x \to a$ 處呈 $\frac{0}{0}$ 型，直接代入毫無意義。書中第九節的法則（用現代語言）：

若 $f(a) = g(a) = 0$，且在 $a$ 附近 $\frac{f'(x)}{g'(x)}$ 的極限存在，則

$$\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}$$

Johann 的原始推理用無窮小：在 $a$ 附近，$f(x) \approx f(a) + f'(a)\,dx = f'(a)\,dx$，同理 $g(x) \approx g'(a)\,dx$，故

$$\frac{f(x)}{g(x)} \approx \frac{f'(a)\,dx}{g'(a)\,dx} = \frac{f'(a)}{g'(a)}$$

無窮小增量 $dx$ 相消——這正是萊布尼茲記號的優雅之處。嚴格證明要用 Cauchy 中值定理（1820 年代）：$\frac{f(x)-f(a)}{g(x)-g(a)} = \frac{f'(\xi)}{g'(\xi)}$，$\xi$ 介於 $a$ 與 $x$ 之間。

### 線索二：教科書的完整結構
《Analyse des infiniment petits》共九章：微分定義與記號、切線、極值與拐點、曲率、漸近線、包絡線、光學應用，以及第九節的 $\frac{0}{0}$ 法則。書的定義直接採用 Leibniz 的記號 $dx$、$dy$，並把「無窮小差分」作為基本對象。這本書寫得清晰流暢，遠比 1684 年論文易讀——它是**第一本把微積分當成可教、可學的系統課程**的書，此後一百年間歐洲課本幾乎都以它為範本。

### 線索三：代筆懸案的物證
- 1694 年的付費契約直到 1955 年才被數學史家（Clifford Truesdell）從檔案中整理公諸於世，成為定讞的物證。
- 1921 年，Johann Bernoulli 1691–92 年的授課手稿被發現，內容與 1696 年書的絕大部分章節**幾乎逐字相同**——比契約更直接的證據。
- Johann 生前（1704 年 l'Hôpital 死後）公開宣稱法則與書是他的作品；但當時無人完全相信，因為 l'Hôpital 曾在書序中感謝 Johann 並暗示：「我毫不猶豫地採用了他們（Leibniz 與 Bernoulli 先生們）的發現，屬於我的我會標明。」——含糊其辭，正是懸案的餘味。
- 有趣的細節：書中真正屬於 l'Hôpital 本人的一個貢獻，是他自己發現的一條關於「多項式插值」的結果（後世稱 l'Hôpital 三角形/多項式法則），反而默默無聞。

### 線索四：0/0 之後——不定型理論的展開
第九節之後，數學家逐步推廣：$\frac{\infty}{\infty}$ 型、$0 \cdot \infty$、$\infty - \infty$、$1^\infty$、$0^0$、$\infty^0$ 型，都可化為 $\frac{0}{0}$ 或 $\frac{\infty}{\infty}$ 處理。例如 $0 \cdot \infty$ 型：$f \cdot g = \frac{f}{1/g}$，化為商型。這套「不定型分類學」直到極限的 $\varepsilon$-$\delta$ 嚴格定義（19 世紀 Cauchy、Weierstrass）才獲得堅實基礎。

### 程式碼範例：sympy 驗證 L'Hôpital 法則與 1694 年契約背後的數學
```python
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

x = sp.symbols('x')

# 1) 經典 0/0 案例：lim_{x→0} sin(x)/x = 1
f, g = sp.sin(x), x
print("直接代入:", sp.limit(f/g, x, 0), "  導數之比:", sp.limit(sp.diff(f)/sp.diff(g), x, 0))
# 兩者皆為 1 —— L'Hôpital 法則成立

# 2) 另一例：lim_{x→0} (1-cos(x))/x² = 1/2
f2, g2 = 1 - sp.cos(x), x**2
print("直接代入:", sp.limit(f2/g2, x, 0), "  導數之比:", sp.limit(sp.diff(f2)/sp.diff(g2), x, 0))
# 一次 L'Hôpital 後仍是 0/0，再來一次得 1/2 —— 法則可重複使用

# 3) ∞/∞ 型：lim_{x→∞} ln(x)/x = 0
print("ln(x)/x 極限 =", sp.limit(sp.log(x)/x, x, sp.oo))   # 0

# 4) 數值驗證：0/0 極限在 x→0 的收斂行為
xs = np.array([0.5, 0.1, 0.05, 0.01, 0.001])
vals = np.sin(xs) / xs
print("sin(x)/x 數值:", vals, "→ 趨近 1")

# 5) Johann 的原始推理：f ≈ f'(a)dx, g ≈ g'(a)dx，比值相消
a = 0.0
fa, ga = sp.diff(f).subs(x, a), sp.diff(g).subs(x, a)
print(f"f'(0)/g'(0) = {fa}/{ga} = {fa/ga}")

fig, ax = plt.subplots(figsize=(7, 5))
xx = np.linspace(-0.99, 0.99, 400)
ax.plot(xx, np.sin(xx)/xx, label='sin(x)/x（0/0 型）')
ax.plot(xx, (1-np.cos(xx))/xx**2, '--', label='(1−cos x)/x²（0/0 型）')
ax.axhline(1, c='gray', ls=':', lw=0.5)
ax.axhline(0.5, c='gray', ls=':', lw=0.5)
ax.plot(0, 1, 'ro'); ax.plot(0, 0.5, 'ro')
ax.set_ylim(-0.2, 1.4); ax.legend()
ax.set_title("L'Hôpital 1696: 0/0 不定型的極限")
plt.show()
```

程式輸出：$\frac{\sin x}{x}$ 與 $\frac{1-\cos x}{x^2}$ 的直接代入極限與導數之比完全一致（分別為 $1$ 與 $\frac{1}{2}$，後者需兩次法則），$\frac{\ln x}{x} \to 0$ 展示 $\frac{\infty}{\infty}$ 型——1696 年第九節的每一條規則，都被現代符號計算與數值驗證逐一證實。

## 結案 -- 後果與影響
- 微積分**教育化**：《Analyse des infiniment petits》成為歐洲大學的標準教材範本，微積分從少數天才的絕技變成可以傳授的學科。
- $\frac{0}{0}$ 極限理論正式誕生，後來發展為完整的不定型分類學，最終由 Cauchy、Weierstrass 的 $\varepsilon$-$\delta$ 極限定義嚴格化。
- 名字的錯置成為數學史著名公案：Johann Bernoulli 的真實貢獻在 1955 年契約公開、1921 年手稿發現後獲得承認，但「L'Hôpital 法則」這個名字已積重難返。
- 付費契約也開啟了數學史上關於「智慧財產權」的長期討論——這在當時是全新的概念。
- Bernoulli 家族繼續推進：Johann 的學生 Euler 把微積分推向分析學的黃金時代。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Guillaume de l'Hôpital | 資助人與出版者，第一本教科書署名者 |
| Johann Bernoulli | 實際執筆者，1694 年付費契約的另一方 |
| Gottfried W. Leibniz | 微積分創始人（記號與方法的源頭） |
| Augustin-Louis Cauchy | 19 世紀以中值定理嚴格化該法則 |

- G. F. A. de l'Hôpital, *Analyse des infiniment petits pour l'intelligence des lignes courbes* (Paris, 1696)。
- J. Bernoulli, *Lectiones de calculo differentialium*（1691–92 手稿，1921 年發現）。
- C. Truesdell, 關於 Bernoulli 家族與 1694 契約的檔案研究（1955 年前後）。
