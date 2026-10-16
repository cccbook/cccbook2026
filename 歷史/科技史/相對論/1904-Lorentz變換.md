# 1904 - Lorentz 變換完成

## 案件摘要
1904 年，Lorentz 在聖路易斯演講中完成了對所有速度階都成立的完整變換方程；
1905 年 Poincaré 將其命名為「Lorentz 變換」並補上數學嚴格性與相對性原理。
公式已經完備，但跨出「拋棄乙太與絕對時間」最後一步的，卻是 1905 年的專利職員 Einstein。

## 前因 -- 為什麼會有這個案子
- 1892–1895 年 Lorentz 已有收縮假說與一階局部時間 $t' = t - vx/c^2$（見 1892 案）。
- 但一階變換只對 $v/c$ 的一次方有效；**二階以上**的實驗（如 Rayleigh–Brace 1902、
  Trouton–Noble 1903 等二階零結果）逼出更完整的理論。
- 1900 年前後，Kaufmann（1901–1905）測量高速電子的質量隨速度變化，
  要求理論給出 $\gamma$ 級的精確預言。
- Poincaré 對「乙太被運動擠壓」類補丁提出哲學批評：物理定律應對所有觀察者形式相同。

## 線索與推理 -- 數學式、程式、理論

### 線索 1：完整 Lorentz 變換（Lorentz 1904，Poincaré 1905 命名與修飾）

以 $\gamma$ 記號：
$$
\boxed{
x' = \gamma\,(x - vt),\qquad
t' = \gamma\left(t - \frac{v x}{c^2}\right),\qquad
\gamma = \frac{1}{\sqrt{1-\dfrac{v^2}{c^2}}}
}
$$
（垂直方向不變：$y' = y,\ z' = z$；Poincaré 補上 $x'^\mu = \Lambda^\mu{}_\nu x^\nu$ 的矩陣形式，
並證明它構成群——**Lorentz 群**，1905 年 6 月提交巴黎科學院。）

長度收縮與時間膨脹都自然從中掉出來：
$$
L = \frac{L_0}{\gamma}\quad(\text{收縮}),\qquad
\Delta t = \gamma\,\Delta\tau\quad(\text{時間膨脹})
$$

### 線索 2：不變量 -- 這才是「真正的指紋」

Galilean 變換下空間距離是不變量；Lorentz 變換下的不變量是**時空間隔**：
$$
s^2 = c^2t^2 - x^2 - y^2 - z^2 = c^2t'^2 - x'^2 - y'^2 - z'^2
$$

```python
import numpy as np

def lorentz_transform(x, t, v, c=1.0):
    gamma = 1/np.sqrt(1 - v**2/c**2)
    x2 = gamma*(x - v*t)
    t2 = gamma*(t - v*x/c**2)
    return x2, t2

c = 1.0
v = 0.6*c
x, t = 3.0, 2.0                 # 任意時空事件
x2, t2 = lorentz_transform(x, t, v, c)

s1 = c**2*t**2 - x**2
s2 = c**2*t2**2 - x2**2
print(f"s^2 (S frame)  = {s1:.6f}")
print(f"s^2 (S' frame) = {s2:.6f}")
print(f"不變量成立: {np.isclose(s1, s2)}")
print(f"gamma = {1/np.sqrt(1-v**2/c**2):.4f}")
```

輸出顯示兩個座標系算出的 $s^2$ 完全相同——時空間隔是 Lorentz 變換的「不變指紋」，
這正是 Minkowski（1908）四維時空幾何的起點。

### 線索 3：速度加法公式 -- 光速不可超越的證明

由變換式可導出速度合成律（Poincaré 1905 明確寫出）：
$$
w = \frac{u + v}{1 + \dfrac{uv}{c^2}}
$$
若 $u = c$（光），則
$$
w = \frac{c + v}{1 + v/c} = c
$$
**光速對任何慣性觀察者都是 $c$**——Michelson–Morley 的零結果不再是巧合，而是原理！

```python
import numpy as np
c = 1.0
for u, v in [(0.8, 0.6), (0.99, 0.99), (1.0, 0.9), (0.5, -0.5)]:
    w = (u + v)/(1 + u*v/c**2)
    print(f"u={u:+.2f}, v={v:+.2f}  ->  w={w:+.6f}")
# 0.8+0.6 -> 0.945945（小於 1！古典會給 1.4）
# 0.99+0.99 -> 0.99995
# 1.0+0.9 -> 1.0（光速不變）
```

### 線索 4：Poincaré 的相對性原理與同時性批判

- **相對性原理（Poincaré 1904 聖路易斯演講）**：
  「物理定律的表述，對固定觀察者與對做等速運動的觀察者，應該完全相同，
  以致我們沒有、也不可能有任何方法分辨我們是否處於等速運動之中。」
- **同時性批判**：Poincaré 在《科學的價值》中指出，
  「同時」的定義依賴光速訊號的交換，而光速的測量又預設了同時性——這是循環定義。
  他早於 Einstein 就指出**絕對同時性無法定義**。
- 但 Poincaré 仍保留乙太作為「數學上最方便的參考系」，未宣布它不存在。

### 線索 5：Lorentz 與 Poincaré 為何沒有跨出最後一步？

| | Lorentz | Poincaré |
|---|---|---|
| 保留乙太 | 是——乙太是「真實」參考系 | 是——只是「方便的約定」 |
| 時間觀 | $t'$ 是數學輔助；真時間是乙太系的 $t$ | 同時性是約定，但未建立運動學 |
| 動機 | 保存電子論與 Maxwell 理論 | 追求數學優雅與原理 |
| 未竟之步 | 沒有說「時間本身是相對的」 | 沒有建立完整的動力學與運動學體系 |

兩人手握所有零件：變換式、$\gamma$、速度加法、相對性原理——
卻始終把它們裝回「乙太 + 絕對時間」的舊骨架裡。

## 結案 -- 後果與影響
- **Einstein 1905 的最後一步**：直接宣布乙太多餘、時間與同時性是觀察者相依的，
  從兩條公設（相對性原理 + 光速不變）演繹出整個狹義相對論。
- **與 Einstein 1905 的對照表**：

| 項目 | Lorentz/Poincaré（1904–05） | Einstein（1905） |
|---|---|---|
| 出發點 | 修補乙太理論、解釋實驗 | 兩條公設的公理化演繹 |
| 變換式 | 有（形式相同） | 重新導出（意義不同） |
| 乙太 | 保留 | 拋棄（「多餘的假說」） |
| 時間 | 絕對（乙太系） | 相對，隨觀察者定義 |
| 收縮/膨脹 | 物體的力學性質 | 運動學測量效應 |
| 後續 | Lorentz 堅守乙太至晚年 | 1908 Minkowski 幾何化 → 1915 廣義相對論 |

- **歷史定位**：Lorentz 變換以 Lorentz 命名（Poincaré 1905 命名）實至名歸——
  但「相對論」的思想框架屬於 Einstein。
  Lorentz 本人晚年風度地承認：「我失敗的原因，是我把 $t'$ 當成了純粹的數學量。」
- Minkowski（1908）名言：「從今以後，空間與時間各自都將化為幻影，
  只有兩者的某種結合才能保持獨立的實在。」——偵探總結：案件的真相是**時空一體**。

## 關鍵人物與文獻
- **Hendrik A. Lorentz**（1853–1928）：1902 諾貝爾物理獎；1904 完成變換。
  - Lorentz, H.A. (1904). "Electromagnetic Phenomena in a System Moving with any Velocity Less than that of Light". *Proc. Acad. Sci. Amsterdam* 6: 809–855.
- **Henri Poincaré**（1854–1912）：數學家；命名「Lorentz 變換」、補上群論結構與相對性原理。
  - Poincaré, H. (1904). "L'état actuel et l'avenir de la physique mathématique"（聖路易斯演講）.
  - Poincaré, H. (1905/06). "Sur la dynamique de l'électron". *Rendiconti del Circolo Matematico di Palermo* 21: 129–176.
- **Albert Einstein**（1879–1955）：1905 年〈論動體的電動力學〉，完成最後一步。
- **Hermann Minkowski**（1864–1909）：1908 年將時空幾何化。
