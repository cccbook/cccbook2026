# 1637 — Fermat 極大極小法

## 案件摘要
1637 年前後，圖盧茲的律師 Pierre de Fermat 在書信〈求極大與極小值的方法〉（Methodus ad disquirendam maximam et minimam）中提出「adequality」（擬等法，法語近似相等）：把函數值 $f(x)$ 與 $f(x+E)$「擬等」，展開後除以 $E$，再令 $E = 0$，就能求出極值點與切線斜率。這正是 $\lim_{E\to 0}\frac{f(x+E)-f(x)}{E} = f'(x) = 0$ 的導數思想——微分學的遠古原型。同年 Descartes 出版《幾何學》（La Géométrie）並提出競爭性的「法線法」，兩人隨即爆發優先權與方法之爭。

## 前因 -- 為什麼會有這個案子
- 古希臘 Apollonius 的《圓錐曲線論》已給出橢圓、拋物線的法線與切線性質，但每條曲線都要個別處理，沒有統一方法。
- 透鏡磨製是 17 世紀的光學核心問題：光線要精確聚焦，就必須知道曲面在每一點的**切線**與**法線**。Descartes 研究光學（《屈光學》與《幾何學》同年出版）正是為了磨鏡片。
- 1636 年，Fermat 已用幾何級數證明 $\int_0^1 x^n dx = \frac{1}{n+1}$（寄給 Mersenne 與 Roberval），在求積上領先；極值與切線是他下一個目標。
- 案件的動機：能不能用**一套代數程序**，對任何多項式曲線統一地找出極值與切線？Fermat 的答案是：可以——用「擬等」。

## 線索與推理 -- 數學式、程式、理論

### 線索一：adequality 求極值
Fermat 的程序：要求 $f(x)$ 的極值，考慮

$$f(x) \overset{\text{adeq}}{=} f(x+E)$$

展開右邊、消去公共項、兩邊同除以 $E$、再令 $E = 0$，得到方程

$$\left.\frac{f(x+E) - f(x)}{E}\right|_{E=0} = 0$$

**範例**：把長度為 $a$ 的線段分成兩段，使兩段乘積最大。設一段為 $x$，則乘積 $f(x) = x(a - x)$。Fermat 寫出

$$x(a-x) \overset{\text{adeq}}{=} (x+E)(a - x - E)$$

展開、消去 $xa - x^2$，得 $0 = Ea - 2xE - E^2$，除以 $E$ 得 $a - 2x - E = 0$，令 $E = 0$：

$$x = \frac{a}{2}$$

答案正確——而且程序對**任何**多項式都通用。

### 線索二：以現代語言重寫
Fermat 的「除以 $E$ 再令 $E = 0$」正是導數的定義：

$$f'(x) = \lim_{E \to 0} \frac{f(x+E) - f(x)}{E}$$

對 $f(x) = x(a-x) = ax - x^2$，$f'(x) = a - 2x$，令 $f'(x) = 0$ 得 $x = \frac{a}{2}$。唯一的差別是：Fermat 用「擬等」這個含糊的詞迴避了 $E = 0$ 時除以零的邏輯問題——這個漏洞要等 150 年後的 Cauchy 極限語言才能補上。

### 線索三：切線法
同樣的招數用於切線：曲線 $y^2 = kx$（拋物線）上一點 $(a, b)$，Fermat 求切線與橫軸交點 $T$。用相似三角形與擬等，得到次切距

$$TS = \frac{b \cdot E}{f(a+E) - f(a)} \bigg|_{E=0} = \frac{f(a)}{f'(a)}$$

對 $y^2 = kx$ 即 $f(x) = \sqrt{kx}$，$f'(a) = \frac{\sqrt{k}}{2\sqrt{a}}$，故 $TS = \frac{\sqrt{ka}}{\sqrt{k}/(2\sqrt{a})} = 2a$——與 Apollonius 的幾何結果一致，但這次是**代數程序算出來的**。

### 線索四：Fermat–Descartes 之爭
1638 年，Descartes 提出自己的「圓法」（法線法）：以曲線上點 $(a,b)$ 為圓上一点作圓，與曲線相切時聯立方程的重根條件給出法線。Descartes 用曲線 $x^3 + y^3 = 3axy$（今稱 Folium of Descartes）挑戰 Fermat，Fermat 迅速正確求出法線，Descartes 只好讓步。但 Descartes 仍攻擊 Fermat 的方法「含糊、不嚴格」。Mersenne 居中調停。最終歷史判定：Fermat 的 adequality 更接近今日的微分學。

### 程式碼範例：數值求極值，驗證 Fermat 的 adequality
```python
import numpy as np

# (1) Fermat 的問題：a 分成兩段使乘積最大
a = 10.0
f = lambda x: x * (a - x)

# 數值掃描找最大值
x = np.linspace(0, a, 100001)
i = np.argmax(f(x))
print(f"數值最大點 x = {x[i]:.4f}（理論 a/2 = {a/2}）")

# (2) 驗證 Fermat 的核心操作：(f(x+E)-f(x))/E 在極值點 -> 0
def diff_quotient(x0, E):
    return (f(x0 + E) - f(x0)) / E

for E in [1e-1, 1e-3, 1e-5, 1e-7]:
    q_extremum = diff_quotient(a/2, E)     # 極值點：應趨近 0
    q_other   = diff_quotient(a/4, E)      # 非極值點：應趨近 f'(a/4)=a/2
    print(f"E={E:.0e}: 商(極值點)={q_extremum:+.2e}, 商(a/4)={q_other:+.4f}")

# (3) 數值微分 f'(x) = a - 2x 全域驗證
h = 1e-6
xp = np.linspace(0.001, a-0.001, 10)
numeric = (f(xp + h) - f(xp - h)) / (2*h)
print("數值導數:", np.round(numeric, 4), "理論 a-2x:", np.round(a - 2*xp, 4))
```

程式輸出：數值最大點在 $x = 5.0 = a/2$；差商 $\frac{f(x+E)-f(x)}{E}$ 在極值點隨 $E$ 縮小趨近 0、在 $a/4$ 處趨近 $a/2 = f'(a/4)$——Fermat 的「除以 $E$ 再令 $E=0$」在數值上就是導數。

### 線索五：adequality 求面積——積分的另一面
Fermat 的招數不止用於極值：他還用「擬等」處理**曲線下的面積**。對 $y = x^n$，他在 $[0, a]$ 上取等比分割的點 $a, ar, ar^2, \dots$（$r$ 為公比），把曲線下的面積近似為矩形之和：

$$S \approx a^{n+1}(1-r) + a^{n+1}(r - r^2)\cdot\text{(修正)} \quad \Rightarrow \quad S \overset{\text{adeq}}{=} \frac{a^{n+1}}{n+1}\ \text{當}\ r \to 1$$

用幾何級數求和後令公比 $r \to 1$，Fermat 證明

$$\int_0^a x^n\,dx = \frac{a^{n+1}}{n+1}$$

這比 Cavalieri 的不可分量法更嚴格（他寄給 Mersenne 的信早於 1637 年）。換句話說：Fermat 一人手握微分（adequality 求極值）與積分（幾何級數求面積）兩件兇器的原型，只差沒有證明它們**互逆**——那一步要等 1666 年 Newton 的流數術。

## 結案 -- 後果與影響
- Fermat 的 adequality 處理了極值、切線、法線，甚至推廣到曲線下的面積（用近似矩形求和求 $\int x^n dx$）——**微分與積分兩件兇器他都有原型**，只差沒有把它們連成基本定理。
- 1637 年 Descartes《幾何學》確立解析幾何：曲線 = 方程，這讓 Fermat 的代數程序可以通用於一切曲線。
- Fermat–Descartes 之爭以 Fermat 的方法論勝告終：後世 Newton、Leibniz 的求極值、切線法都是 adequality 的直系後代。
- Fermat 終身未出版（以書信發表），導致優先權證據鏈薄弱——這也是後來他與 Leibniz/Newton 陣營爭議的伏筆。
- 案件的影響：今日最佳化、機器學習的梯度下降法，本質上仍是「令 $f'(x) = 0$」的 390 年後延續。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Pierre de Fermat | adequality 求極值與切線，微分原型 |
| René Descartes | 《幾何學》解析幾何、法線法、爭論對手 |
| Apollonius | 圓錐曲線切線/法線的幾何先驅 |
| Marin Mersenne | 書信網絡的居中調停者 |
| Roberval | 同時代切線法競爭者 |

- P. de Fermat, *Methodus ad disquirendam maximam et minimam*（1636–1638 書信，寄給 Mersenne）。
- R. Descartes, *La Géométrie*（附於《方法論》，1637）。
- R. Descartes, *La Dioptrique*（1637）：透鏡與切線的動機。
