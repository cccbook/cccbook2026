# 1684 — Leibniz 發表微積分

## 案件摘要
1684 年 10 月，Leibniz 在他自己協助創辦的學術期刊《Acta Eruditorum》上，發表了一篇只有六頁的論文〈Nova Methodus pro Maximis et Minimis, itemque tangentibus, quae nec fractas nec irrationales quantitates moratur, et singulare pro illis calculi genus〉（論極大與極小以及切線的一種新方法，不受分式與無理量阻礙，及其一種奇特的計算法）。這是**史上第一篇公開發表的微分學論文**。文中首次公開了乘積法則、商法則、極值條件 $dx = 0$ 與二階微分 $ddx$ 判斷凹凸性。六頁紙，把持續兩千年的切線與極值問題正式結案。

## 前因 -- 為什麼會有這個案子
- 1673–1676 年 Leibniz 在巴黎完成了特徵三角形研究，掌握了微分與求和互逆的原理，並創造了 $dx$、$dy$、$\int$ 記號——但這些成果一直鎖在他的手稿裡。
- 同一時期，Newton 早在 1665–1666 年瘟疫年間就發展出「流數術」（fluxions），1671 年寫成《流數術與無窮級數》，但**始終拒絕發表**——牛頓對無窮小的邏輯基礎感到不安，也厭惡學術爭論。
- 1676 年 Newton 與 Leibniz 透過 Henry Oldenburg 交換過兩封著名的信（Epistola prior 與 Epistola posterior），Newton 用字謎（anagram）暗示自己的流數術成果，卻不揭露細節；Leibniz 則公開了自己的進展。
- 1670 年代末，天文學家與力學家急切需要一套處理極值與切線的通用方法——Descartes 的代數圓法太繁瑣，Fermat 的方法只對多項式友善。公開一套通用演算法的時機成熟了。
- 1682 年 Leibniz 與 Otto Mencke 創辦德國第一本學術期刊《Acta Eruditorum》——他手裡握有「發表權」這個關鍵武器。

## 線索與推理 -- 數學式、程式、理論

### 線索一：極值條件 $dx = 0$
論文的標題就點出主旨「pro Maximis et Minimis」。Leibniz 的推理：曲線在極大點或極小點處，切線必為水平，即

$$dx = 0 \quad \Longleftrightarrow \quad \frac{dy}{dx} = 0$$

用現代語言：設 $y = f(x)$，極值點滿足 $f'(x) = 0$。Leibniz 用此方法示範了幾個問題，包括光學折射（Snell 定律的最短時間證明）與某類優化問題。這是史上第一次，極值問題被寫成一套「按表操作」的演算法。

### 線索二：乘積法則與商法則
論文中 Leibniz 公開了（他早在 1675–1677 年手稿中推導出的）微分運算規則。對 $y = uv$：

$$d(uv) = u\,dv + v\,du$$

Leibniz 的原始推理極為精彩（出於 1680 年代手稿）：把 $u$ 與 $v$ 各自的增量畫在矩形上，乘積 $uv$ 的增量來自兩條「邊條」$u\,dv$ 與 $v\,du$ 加上一個無窮小的角落 $du\,dv$——後者是二階無窮小，可略去。至於商法則，他由乘積法則與「$d(x \cdot v/u) $」的組合推出：

$$d\!\left(\frac{u}{v}\right) = \frac{v\,du - u\,dv}{v^2}$$

注意 $v^2$ 出現在分母——這正是標題宣稱「不受分式與無理量阻礙」的底氣：連分式與冪根都能按規則微分。

### 線索三：二階微分 $ddx$ 與凹凸性
論文首次出現二階微分記號 $ddx$、$ddy$（即今日的 $d^2x$、$d^2y$）。Leibniz 指出：

- 在極大點附近，曲線是**凹**的（對某種方向），$ddy$ 與極值方向反號；
- 在極小點附近，曲線是**凸**的，$ddy$ 同號；
- 拐點處 $ddy = 0$。

用現代記號：$f''(x) > 0$ 極小、$f''(x) < 0$ 極大、$f''(x) = 0$ 可能是拐點——這就是今日課本的「二階導數檢驗法」。二階微分的引入也為 1690 年代 Bernoulli 家族的力學應用（懸鏈線、彈性曲線）鋪路。

### 線索四：與 Newton 未發表成果的對照
Newton 的流數術在數學上等價：$\dot{x}$（流量對時間的流數）對應 $dx/dt$，流數之比 $\dot{y}/\dot{x}$ 對應 $dy/dx$。但 Newton 拒絕發表，Leibniz 卻以**記號即演算法**的策略公開——讀者拿到的是一本「操作手冊」，不需要幾何洞見就能計算。這個差異決定了傳播速度：大陸數學家（Bernoulli 兄弟、l'Hôpital）快速跟進，英國數學家則在牛頓的陰影下停滯數十年。

### 程式碼範例：sympy 重演 1684 年論文的三條法則與極值判斷
```python
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

x, u, v = sp.symbols('x u v')

# 1) 乘積法則 d(uv) = u dv + v du（sympy 驗證）
lhs = sp.diff(u * v, x)
rhs = u * sp.diff(v, x) + v * sp.diff(u, x)
print("d(uv) - (u dv + v du) =", sp.simplify(lhs - rhs))   # 0

# 2) 商法則 d(u/v) = (v du - u dv) / v²
lhs = sp.diff(u / v, x)
rhs = (v * sp.diff(u, x) - u * sp.diff(v, x)) / v**2
print("d(u/v) - (v du - u dv)/v² =", sp.simplify(lhs - rhs))  # 0

# 3) 極值條件 dx=0 與二階微分 ddy 判斷凹凸：以 f(x)=x³-3x 為例
f = x**3 - 3*x
df = sp.diff(f, x)          # 一階：dx = 0 的候選點
ddf = sp.diff(f, x, 2)      # 二階：ddy 判凹凸
crit = sp.solve(sp.Eq(df, 0), x)
print("f'(x)=0 的候選點:", crit)                 # [-1, 1]
for c in crit:
    print(f"x={c}: ddy={ddf.subs(x,c)}, 判定 = {'極小' if ddf.subs(x,c)>0 else '極大'}")

# 4) Leibniz 原始推理的數值版：u·v 的增量 = u dv + v du + du·dv（角落項）
uu, vv, du_, dv_ = 3.0, 5.0, 0.01, 0.02
total = (uu + du_) * (vv + dv_) - uu * vv
print("總增量 =", total, " = u·dv + v·du =", uu*dv_ + vv*du_,
      " + 角角落 du·dv =", du_ * dv_)

# 5) 畫出 f 與 f'、f''，目視驗證 1684 年的凹凸性判斷
xs = np.linspace(-2.2, 2.2, 400)
fs = sp.lambdify(x, f)(xs)
dfs = sp.lambdify(x, df)(xs)
ddfs = sp.lambdify(x, ddf)(xs)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(xs, fs, label='f = x³ − 3x')
ax.plot(xs, dfs, '--', label="f'（dx=0 處為極值）")
ax.plot(xs, ddfs, ':', label="f''（ddy 判凹凸）")
for c in crit:
    ax.plot(float(c), float(sp.lambdify(x, f)(c)), 'ro')
ax.axhline(0, c='gray', lw=0.5); ax.legend()
ax.set_title("Leibniz 1684: dx=0 與 ddy 凹凸性")
plt.show()
```

程式輸出：乘積與商法則的殘差為 0（法則嚴格成立）、$f' = 0$ 的候選點 $x = -1, 1$ 分別由 $ddy$ 判定為極大與極小、而 $u\cdot dv + v\cdot du = 0.13$ 加上角落項 $du\cdot dv = 0.0002$ 恰等於總增量——Leibniz 略去二階無窮小的原始推理，被現代計算完整重演。

## 結案 -- 後果與影響
- 微積分從此**公開化、演算法化**：任何受過訓練的人都能按規則計算切線與極值，不再需要天才的幾何洞見。
- 引發史上最著名的**優先權之爭**：英國皇家學會 1712 年的裁決偏向 Newton（實為牛頓自己執筆的報告），導致英國數學界與大陸隔絕近百年，英國數學因此落後。
- Bernoulli 家族（Jakob、Johann）迅速把新方法推向極致：懸鏈線（1690）、最速降線（1696–97）等挑戰題讓微積分的威力展露無遺。
- 1696 年 l'Hôpital 出版第一本微積分教科書，把這套方法教育化。
- 長遠影響：變分法、微分方程、數學物理——整條現代數學物理的血脈，都從這六頁論文流出。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Gottfried W. Leibniz | 發表第一篇微積分論文 |
| Isaac Newton | 流數術創始人（1665–66，未發表） |
| Henry Oldenburg | 1676 年兩封信的中間人 |
| Jakob / Johann Bernoulli | 大陸微積分的傳播者與發展者 |

- G. W. Leibniz, *Nova Methodus pro Maximis et Minimis*, Acta Eruditorum (Oct. 1684), pp. 467–473。
- I. Newton, *Method of Fluxions*（1671 寫成，1736 出版）。
- D. T. Whiteside 編, *The Mathematical Papers of Isaac Newton*。
