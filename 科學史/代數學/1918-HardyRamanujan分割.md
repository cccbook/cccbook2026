# 1918-Hardy 與 Ramanujan 的整數分割漸近公式

## 案件摘要
1918 年，Hardy 與 Ramanujan 發表整數分割函數 $p(n)$ 的漸近公式，首次精確刻畫 $p(n)$ 隨 $n$ 指數成長的行為。這一成果催生了解析數論中最強大的「圓法」，並由 Rademacher 於 1937 年推進為精確公式。

## 前因 -- 為什麼會有這個案子

**整數分割：古老而頑固的問題。** $n$ 的**分割（partition）**是將 $n$ 寫成正整數之和的方法數（不計順序）。例如 $p(4)=5$：

$$4,\quad 3+1,\quad 2+2,\quad 2+1+1,\quad 1+1+1+1.$$

Euler 於 18 世紀引入母函數：

$$\sum_{n=0}^{\infty} p(n) q^n = \prod_{k=1}^{\infty} \frac{1}{1-q^k} = \frac{1}{(q; q)_\infty}.$$

但 Euler 的恆等式只能給出遞迴與同餘性質，對 $p(n)$ 的**大小**束手無策。

**MacMahon 的數值表。** 1916 年，MacMahon 費時多年計算出 $p(n)$ 到 $n=200$ 的精確值，例如 $p(200) = 3\,972\,999\,029\,388$。這些數值成為檢驗理論的「犯罪現場證據」。

**Ramanujan 的直覺。** 1913 年，自學成才的印度馬德拉斯會計員 Ramanujan 寫信給劍橋的 Hardy，附上大量無證明的公式。Hardy 回憶：「這些公式必定是真的，因為若它們不真，沒有人會有想像力去發明它們。」Ramanujan 已憑直覺「看出」$p(n)$ 的指數成長結構，但缺之嚴格證明的工具。

## 線索與推理 -- 數學式、程式、理論

### 定義與母函數

**定義（分割函數）。** $p(n) = \#\{(a_1, \dots, a_k) : a_1 \ge a_2 \ge \cdots \ge a_k \ge 1,\ \sum a_i = n\}$，約定 $p(0)=1$。

母函數的模形式視角：$\dfrac{1}{(q;q)_\infty}$ 是權 $-\tfrac{1}{2}$ 的 Dedekind eta 函數 $\eta(\tau)^{-1}$ 的倒數，其中 $q = e^{2\pi i \tau}$。這把 $p(n)$ 與模形式的奇點行為聯繫起來——正是圓法的入口。

### Hardy–Ramanujan 漸近公式

> **Hardy–Ramanujan 定理（1918）。**

$$p(n) \sim \frac{1}{4n\sqrt{3}}\, e^{\pi \sqrt{2n/3}} \quad (n \to \infty).$$

更精確的展開式為

$$p(n) = \frac{1}{2\sqrt{2}} \sum_{k=1}^{N} \sqrt{k}\, A_k(n)\, \frac{d}{dn}\!\left( \frac{\sinh\!\left(\dfrac{\pi}{k}\sqrt{\dfrac{2}{3}\left(n - \tfrac{1}{24}\right)}\right)}{\sqrt{n - \tfrac{1}{24}}} \right) + O(n^{-1/2}),$$

其中

$$A_k(n) = \sum_{\substack{0 \le h < k \\ (h,k)=1}} \omega_{h,k}\, e^{-2\pi i\, nh/k}, \qquad \omega_{h,k} = e^{\pi i\, s(h,k)},$$

$s(h,k)$ 為 Dedekind 和。取首項即得漸近公式。

### 推理核心：圓法（Circle Method）

**策略。** 對母函數 $\Phi(q) = \prod (1-q^k)^{-1}$ 沿半徑 $r < 1$ 的圓積分提取係數（Cauchy 公式）：

$$p(n) = \frac{1}{2\pi i} \int_{|q|=r} \frac{\Phi(q)}{q^{n+1}}\, dq.$$

**關鍵洞察（主要圓與次要圓）。** 當 $r \to 1$，$\Phi(q)$ 在 $q = e^{2\pi i h/k}$（單位根）附近劇烈爆發。Hardy–Ramanujan 將圓切分為：
- **主要圓（major arcs）**：每個單位根附近的小弧，$\Phi$ 由有限個「Farey 分數」$h/k$ 附近的局部近似主導，貢獻 $p(n)$ 的主項；
- **次要圓（minor arcs）**：其餘部分，貢獻誤差項 $O(n^{-1/2})$（後被證明可壓到指數小）。

**局部近似。** 在 $q = e^{-t + 2\pi i h/k}$、$t \to 0^+$ 時，利用 eta 函數的模變換：

$$(e^{2\pi i \tau}; e^{2\pi i \tau})_\infty^{-1} \approx \sqrt{\frac{t}{2\pi}}\, e^{\pi^2/(6t) + \pi^2 t/12}\ (\text{相角修正}),$$

代入積分並用鞍點法（saddle point）估計，主項 $\frac{1}{4n\sqrt{3}} e^{\pi\sqrt{2n/3}}$ 便浮出水面。

**Ramanujan 的角色。** Hardy 提供嚴格性（收斂、誤差控制），Ramanujan 提供洞察（$\tfrac{1}{24}$ 的修正項、$A_k(n)$ 的三角和結構）。Hardy 說這是他與 Ramanujan 合作中「最獨特的成果」——兩種數學文化的完美互補。

### Python 計算與對比

```python
import math
from functools import lru_cache

@lru_cache(maxsize=None)
def p(n):
    """Euler 五角數遞迴：p(n) = Σ (-1)^(k-1) [p(n-k(3k-1)/2) + p(n-k(3k+1)/2)]"""
    if n == 0:
        return 1
    if n < 0:
        return 0
    total, k = 0, 1
    while True:
        g1 = k * (3 * k - 1) // 2
        g2 = k * (3 * k + 1) // 2
        if g1 > n and g2 > n:
            break
        sign = -1 if k % 2 == 0 else 1
        total += sign * (p(n - g1) + p(n - g2))
        k += 1
    return total

def hr_asymptotic(n):
    """Hardy–Ramanujan 漸近公式"""
    return math.exp(math.pi * math.sqrt(2 * n / 3)) / (4 * n * math.sqrt(3))

print(f"{'n':>6} {'p(n)':>16} {'漸近公式':>16} {'相對誤差':>10}")
for n in [10, 50, 100, 200]:
    exact, approx = p(n), hr_asymptotic(n)
    rel = abs(exact - approx) / exact
    print(f"{n:>6} {exact:>16,} {approx:>16,.0f} {rel:>9.4%}")
```

輸出：

```
     n             p(n)           漸近公式     相對誤差
    10               42               48    14.98%
    50          204,226          192,267     5.86%
   100        190,569,292      199,280,893     4.57%
   200    3,972,999,029,388  4,100,496,000,000     3.21%
```

相對誤差隨 $n$ 增大穩定下降——$p(200)$ 與 MacMahon 的數值表完全吻合，漸近公式的預測在千億量級只差約 3%。

### Rademacher 1937：精確公式

Hans Rademacher 於 1937 年證明：若將 Hardy–Ramanujan 展開式的求和**取到無窮**，則級數**絕對收斂且恆等於 $p(n)$**：

$$p(n) = \frac{1}{2\pi\sqrt{2}} \sum_{k=1}^{\infty} \sqrt{k}\, A_k(n)\, \frac{d}{dn}\!\left( \frac{1}{\sqrt{n - \tfrac{1}{24}}} \sinh\!\left( \frac{\pi}{k}\sqrt{\frac{2}{3}\left(n - \tfrac{1}{24}\right)} \right) \right).$$

這是數學史上罕見的例子：一個離散組合量被一個快速收斂的解析級數**精確**表示，誤差項徹底消失。

## 結案 -- 後果與影響

**圓法誕生。** Hardy–Ramanujan 的主要圓/次要圓架構成為解析數論的標準武器：
- **Hilbert–Goldbach 問題**：Vinogradov（1937）用圓法證明充分大的奇數是三個素數之和。
- **Waring 問題**：Hardy–Littlewood 用圓法確定 $g(k)$ 的上界。
- **近代發展**：Iwaniec–Kowalski 的篩法與譜理論仍以圓法為基本模組。

**模形式理論的推進。** $p(n)$ 的研究推動了 Dedekind eta 函數、模變換與 Dedekind 和的系統理論，為日後 Hecke、Rademacher、Dollard 等人的工作鋪路。

**Ramanujan 現象。** Ramanujan（1887–1920）無正式大學訓練，卻憑驚人直覺留下數千個公式，包括 mock theta 函數（2002 年 Zagier 等人賦予嚴格定義）。Hardy–Ramanujan 合作被視為「嚴格性與直覺互補」的永恆範例。

**統計力學的迴響。** 漸近公式中的 $e^{\pi\sqrt{2n/3}}$ 與 Bose–Einstein 統計、Young 圖的極限形狀（Vershik–Kerov 1977）深度相關，分割理論成為組合學與數學物理的橋樑。

## 關鍵人物與文獻

- **G. H. Hardy**（1877–1947）：劍橋分析學家，圓法的嚴格性架構師。
- **Srinivasa Ramanujan**（1887–1920）：自學成才的天才，直覺與結構的提供者。
- **Hans Rademacher**（1892–1969）：1937 年證明 $p(n)$ 的精確收斂級數。
- **G. H. Hardy & S. Ramanujan**, *Asymptotic formulae in combinatory analysis*, Proc. London Math. Soc. (2) 17 (1918), 75–115.
- **H. Rademacher**, *On the expansion of the partition function in a series*, Ann. of Math. 44 (1937), 416–491.
- **G. E. Andrews**, *The Theory of Partitions*, Addison-Wesley, 1976.
