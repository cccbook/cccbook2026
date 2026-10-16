# 1715 — Taylor 級數

## 案件摘要
1715 年，英國數學家 Brook Taylor 出版《Methodus Incrementorum Directa et Inversa》（正逆增量方法），書中從差分插值出發，推出了以今日他命名的公式：函數若足夠光滑，可展開為冪級數

$$f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x-a)^n$$

這條公式成為此後兩百年分析學的萬用鑰匙。但案件有一個著名的「隱藏共犯」：Gregory 與 Newton 早在數十年前就掌握了同一件事，Taylor 只是把它寫得最清楚。而這條公式埋下的收斂性地雷，要到一百多年後才被 Cauchy 與 Weierstrass 拆解。

## 前因 -- 為什麼會有這個案子
- **天文觀測的插值需求**：17 世紀天文學家需要從有限個觀測點推算行星的中間位置，催生了各種插值法。Thomas Harriot、Henry Briggs 都做過差分表的計算。
- **牛頓前向差分公式**：Newton 在 1670 年代利用等距節點的差分，得到
  $$f(x) = f(0) + \binom{x}{1}\Delta f(0) + \binom{x}{2}\Delta^2 f(0) + \cdots$$
  這已是泰勒級數的離散版本，但牛頓視之為工具而非定理，沒有發表成系統論述。
- **James Gregory 的先驅工作**：蘇格蘭數學家 Gregory 在 1667–1671 年的手稿中，已寫出 $\arctan x$、$\tan x$ 等函數的展開式，形式上與泰勒級數完全相同，只是以幾何語言描述，且他 1675 年早逝，影響有限。
- **Leibniz 微積分與英國的對立**：1684 年 Leibniz 發表微積分後，英國學界急於證明牛頓體系不輸給大陸體系。Taylor 的書正是這場競賽的產物——他想要一套「增量」的一般理論，統一插值、級數與微積分。

## 線索與推理 -- 數學式、程式、理論

### 線索一：從差分到微分
Taylor 的原始推理是一場「極限偵查」。考慮牛頓前向差分插值，節點間距為 $h$：

$$f(a + x) \approx f(a) + \frac{x}{h}\Delta f(a) + \frac{x(x-h)}{2h^2}\Delta^2 f(a) + \frac{x(x-h)(x-2h)}{6h^3}\Delta^3 f(a) + \cdots$$

令 $h \to 0$，觀察每一項：
- $\dfrac{\Delta f(a)}{h} \to f'(a)$：一階差商收斂到導數。
- $\dfrac{\Delta^2 f(a)}{h^2} \to f''(a)$：$n$ 階差除以 $h^n$ 收斂到 $n$ 階導數。

把這些極限代入插值公式，分子中的 $x(x-h)(x-2h)\cdots$ 極限為 $x^n$，於是

$$f(a+x) = f(a) + f'(a)x + \frac{f''(a)}{2!}x^2 + \frac{f'''(a)}{3!}x^3 + \cdots$$

這就是 1715 年《Methodus Incrementorum》第 VII 篇、命題 3 的內容。整個推理的精髓是：**冪級數展開是插值法在無窮細節下的極限**。

### 線索二：Maclaurin 的「特例」洗牌
1742 年，蘇格蘭數學家 Colin Maclaurin 在《Treatise of Fluxions》中大量使用了 $a=0$ 的特例：

$$f(x) = f(0) + f'(0)x + \frac{f''(0)}{2!}x^2 + \cdots$$

由於 Maclaurin 用得太多太廣，這個特例被命名為「Maclaurin 級數」——儘管 Maclaurin 本人在書中明確承認這只是 Taylor 級數的特例。歷史的吊詭：發明者得到主罪名，推廣使用者反而得到一個屬於自己的公式名。今日 $\sin x$、$\cos x$、$e^x$ 的展開式都是 Maclaurin 級數：

$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots, \qquad \sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots$$

### 線索三：埋下的地雷——收斂性
Taylor 與同時代的所有人，都默認「只要展開出來就成立」。但這條公式有兩個致命盲區：

1. **收斂半徑**：$f(x) = \dfrac{1}{1+x^2}$ 在 $x=0$ 任意階可微，但它的 Maclaurin 級數只在 $|x|<1$ 收斂——複變函數論（Cauchy, 1820s）才能解釋：奇異點 $\pm i$ 到原點的距離就是收斂半徑。
2. **非零發散級數**：Cauchy 在 1822 年給出反例
   $$f(x) = \begin{cases} e^{-1/x^2}, & x \neq 0 \\ 0, & x = 0 \end{cases}$$
   這個函數在 $x=0$ 的**所有階導數都是 0**，泰勒級數恆為零，卻不等於函數本身。「光滑」不等於「可展開」——泰勒級數成立需要「解析」這個更強的條件。

### 線索四：Lagrange 餘項的雛形
Taylor 自己也在書中給出了誤差的估計雛形。後來 Lagrange（1797）將餘項系統化為

$$f(x) = \sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!}(x-a)^k + \frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1}, \quad \xi \in (a, x)$$

這個「Lagrange 餘項」讓泰勒級數從「無窮和的信仰」變成「可控制誤差的有限工具」，是通往嚴格化的第一座橋。

### 程式碼範例：泰勒多項式逼近 $\sin x$ 與收斂觀察
```python
import numpy as np
import matplotlib.pyplot as plt
from math import factorial

def taylor_sin(x, N):
    """sin x 的 N 階 Maclaurin 級數部分和"""
    s = np.zeros_like(x)
    for n in range(N + 1):
        # 只有奇數次項，符號 (-1)^k
        if n % 2 == 1:
            s += (-1)**((n - 1) // 2) * x**n / factorial(n)
    return s

x = np.linspace(-np.pi, np.pi, 400)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, np.sin(x), "k-", lw=2, label="sin(x)")

# 不同階數的泰勒多項式：階數越高，逼近範圍越廣
for N in [1, 3, 5, 9]:
    ax.plot(x, taylor_sin(x, N), "--", lw=1.2,
            label=f"Taylor degree {N}")

# 收斂性檢查：x = pi/2 處誤差隨階數下降
print("x = pi/2 處的部分和誤差：")
for N in [1, 3, 5, 7, 9, 11]:
    err = abs(np.sin(np.pi/2) - taylor_sin(np.array([np.pi/2]), N)[0])
    print(f"  N={N:2d}, 誤差 = {err:.3e}")

ax.set_ylim(-2, 2)
ax.axhline(0, c="gray", lw=0.5)
ax.legend(); plt.show()
```

數值輸出顯示：誤差約以 $\dfrac{(\pi/2)^{N+2}}{(N+2)!}$ 的速度下降——這正是 Lagrange 餘項的預測。冪級數逼近在收斂半徑內是「越越高階越準」，與線索三的反例形成對照。

## 結案 -- 後果與影響
- **函數展開時代**：此後一百多年，數學家用冪級數處理一切——Euler 用它算出 $e^{i\pi}+1=0$，Lagrange 企圖把整個微積分建立在它上面。
- **實用計算的基石**：對數表、三角函數表、行星軌道計算、牛頓迭代法求根，全部依賴泰勒展開。
- **收斂性地雷**：泰勒級數的濫用製造了大量悖論（逐項積分出錯、級數和錯誤），成為 19 世紀分析嚴格化運動的直接動機。
- **埋線給後世**：Cauchy 的收斂理論、Weierstrass 的解析函數論、乃至複變冪級數理論，都是對這個 1715 年案件的「重審」。
- 影響至今：物理學的微擾論、數值方法的有限差分法、機器學習的二階優化，本質上都是泰勒級數的後代。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Brook Taylor | 1715 年出版《Methodus Incrementorum》，級數以他命名 |
| James Gregory | 先驅，1660s 已知同型展開，早逝影響有限 |
| Isaac Newton | 前向差分插值公式的源頭 |
| Colin Maclaurin | 1742 年發揚 $a=0$ 特例，「Maclaurin 級數」以他命名 |
| Joseph-Louis Lagrange | 系統化餘項，1797 |
| Augustin-Louis Cauchy | 拆解收斂性地雷，1820s |

- B. Taylor, *Methodus Incrementorum Directa et Inversa*, London (1715)。
- C. Maclaurin, *A Treatise of Fluxions*, Edinburgh (1742)。
- J.-L. Lagrange, *Théorie des fonctions analytiques*, Paris (1797)。
