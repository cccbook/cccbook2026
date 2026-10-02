# 0628-Brahmagupta零與二次方程

## 案件摘要
628 年，印度天文學家婆羅摩笈多（Brahmagupta）完成《婆羅摩修正體系》（Brahmasphutasiddhanta）。這是人類歷史上第一次把「零」當作一個**數**來運算，並系統化處理負數與二次方程。代數從此有了完整的數系地基。

## 前因 -- 為什麼會有這個案子
- 天文曆法計算需要處理「欠債」（負數）與「空無」（零），巴比倫人只把零當佔位符號，希臘人則拒絕把無理量納入「數」。
- 印度數學自阿耶波多（Aryabhata, 499 年）以來累積了大量「庫塔卡」（kuṭṭaka，不定方程）與面積、體積算法。
- 628 年婆羅摩笈多 30 歲時寫下此書，把前人散落的規則整理成**演算法手册**，並首次給出零的運算律。

## 線索與推理 -- 數學式、程式、理論

### 線索一：零與負數的第一次系統化
書中第 18 章定義（原文意譯為現代記號）：

$$a + 0 = a, \quad a \times 0 = 0, \quad a - 0 = a, \quad 0/0 = 0 \text{（此條有誤，卻是史上首次嘗試）}$$

負數記為上方加點（如 $\dot{a} = -a$），並給出符號法則：

$$(-a) \times (+b) = -ab, \quad (-a) \times (-b) = +ab$$

「債減去債是財產，財減去債是債之和」——這是現代符號法則最早的文字記錄。今日我們寫：

```python
# Brahmagupta 的符號法則（628 年）在 Python 中原封不動地成立
assert (-3) * (-5) == 15   # 債 × 債 = 財產
assert (+3) * (-5) == -15  # 財產 × 債 = 債
assert 7 + 0 == 7          # 零是加法單位元
```

### 線索二：二次方程的早期通解
書中以文字敘述給出：對 $x^2 + px = q$ 型方程，取

$$x = \frac{\sqrt{4q + p^2} - p}{2}$$

用現代語言，對 $ax^2 + bx + c = 0$：

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

婆羅摩笈多允許兩個根（含負根），這在當時是革命性的——希臘幾何代數只接受正的幾何量。

```python
import math

def solve_quadratic(a, b, c):
    """Brahmagupta (628): x = (-b ± sqrt(b^2 - 4ac)) / 2a"""
    disc = b*b - 4*a*c
    if disc < 0:
        return None  # 婆氏不處理複數根
    r = math.sqrt(disc)
    return ((-b + r) / (2*a), (-b - r) / (2*a))

print(solve_quadratic(1, -5, 6))   # (3.0, 2.0)
print(solve_quadratic(1, -1, -1))  # 黃金比例相關根 (1.618..., -0.618...)
```

### 線索三：婆羅摩笈多恆等式（Brahmagupta–Fibonacci identity）
書中第 18 章為解 Pell 方程 $Ny^2 + 1 = x^2$ 而給出「合成律」（samāsa）：

$$(a^2 + nb^2)(c^2 + nd^2) = (ac - nbd)^2 + n(ad + bc)^2$$

（對稱形式亦取 $ac + nbd$ 與 $ad - bc$。）這條恆等式說明「形如 $a^2 + nb^2$ 的數在乘法下封閉」，是後來二次域、Pell 方程 chakravala（輪轉）算法、乃至高斯複數乘法 $(a^2+b^2)(c^2+d^2)=(ac-bd)^2+(ad+bc)^2$ 的原型。

```python
def brahmagupta_identity(a, b, c, d, n):
    """驗證 (a²+nb²)(c²+nd²) = (ac-nbd)² + n(ad+bc)²"""
    lhs = (a*a + n*b*b) * (c*c + n*d*d)
    rhs = (a*c - n*b*d)**2 + n*(a*d + b*c)**2
    return lhs == rhs

print(brahmagupta_identity(2, 1, 3, 1, 2))  # True: (5)(11) = (4)² + 2(5)²
```

### 線索四：印度代數的傳承
婆羅摩笈多 → 婆什迦羅第二（Bhāskara II, 1150 年《Lilavati》引入 chakravala 解 Pell 方程）→ 費馬（1657 年重新提出 Pell 問題）→ 歐拉、拉格朗日（證明 Pell 方程必可解）。這條傳承線把 7 世紀印度與 17–18 世紀歐洲代數連成一體。

## 結案 -- 後果與影響
- 零成為「數」：算術從計量工具升級為**代數結構**（加法群、環的雛形）。
- 二次方程通解納入教材近 1400 年，至今未變。
- 婆羅摩笈多恆等式成為代數數論的種子：Pell 方程、二次型理論、理想分解皆由此生。
- 透過花拉子米（al-Khwarizmi）的阿拉伯轉譯與斐波那契的拉丁引入，印度數字與零最終統治全世界。

## 關鍵人物與文獻
- **婆羅摩笈多（Brahmagupta, 598–668）**：《Brahmasphutasiddhanta》（628，20 章），《Khandakhadyaka》（665）。
- **Bhāskara II**：《Lilavati》《Bijaganita》（1150）。
- **Colebrooke, H. T.**（1817）：英譯《Algebra, with Arithmetic and Mensuration from the Sanskrit of Brahmagupta and Bhaskara》。
