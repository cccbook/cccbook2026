# 1545 - Cardano 大術

## 案件摘要
1545 年，米蘭的 Girolamo Cardano 出版《Ars Magna》（《大術》），刊出三次與四次方程的求根公式。但公式背後藏著一樁背叛誓言的偵探故事（Tartaglia 的保密解法被 Cardano 出版），而公式在「不可約情形」中逼出了**複數**的意外現身——虛數不是發明的，是被逼出來的。

## 前因 -- 為什麼會有這個案子
- **義大利數學競賽文化**：文藝復興時期數學家靠公開解題比賽博取教職與名聲，二次方程早在巴比倫與 al-Khwarizmi 就已結案，**三次方程**是當時最大的懸案。
- **del Ferro 的秘密**：波隆那大學的 Scipione del Ferro（約 1515）其實率先解出了缺二次項的三次方程 $x^3 + px = q$，但秘而不宣，臨終前傳給弟子 Fior。
- **Fior 挑戰 Tartaglia**（1535）：Fior 憑遺產向 Tartaglia 挑戰，Tartaglia 在比賽前夜（1535 年 2 月 12/13 日）重新發現解法，8 天內解完 Fior 全部題目獲勝。

## 線索與推理 -- 數學式、程式、理論

### 線索一：保密誓言的偵探故事
1539 年，Cardano 聽聞 Tartaglia 的解法，多次懇求分享。Tartaglia 以**詩歌密碼**的形式透露解法，但附帶條件：Cardano 必須發誓**絕不出版**（打算日後自己寫書）。

**推理（偵探式反轉）**：Cardano 與弟子 Ferrari 後來輾轉取得 del Ferro 的遺稿，發現解法**最早屬於 del Ferro**——誓言的「版權」對象本就另有其人。Cardano 認為誓言失效，1545 年在《Ars Magna》中出版了解法，並**明確標註**：「del Ferro 發現，Tartaglia 獨立再發現，經其允許公佈」。Tartaglia 大怒，雙方展開多年筆戰與公開論戰——這場糾紛毀掉了 Tartaglia 的晚年名聲，也讓《Ars Magna》的出版更富戲劇性。

### 線索二：卡丹諾公式
對「缺二次項」的**簡約三次方程**（除以 $a$、令 $x = t - \frac{b}{3a}$ 消去二次項可得）：

$$t^3 + pt + q = 0$$

**推理**：設 $t = u + v$，代入得

$$u^3 + v^3 + (3uv + p)(u + v) + q = 0$$

選 $u, v$ 使 $3uv + p = 0$，即 $uv = -\frac{p}{3}$；則 $u^3 + v^3 = -q$，$u^3 v^3 = -\frac{p^3}{27}$。於是 $u^3, v^3$ 是二次方程

$$z^2 + qz - \frac{p^3}{27} = 0$$

的兩根，由求根公式得

$$u^3, v^3 = \frac{q}{2} \pm \sqrt{\left(\frac{q}{2}\right)^2 + \left(\frac{p}{3}\right)^3}$$

（注意 $\sqrt{\frac{q^2}{4} + \frac{p^3}{27}} = \sqrt{(\frac{q}{2})^2 + (\frac{p}{3})^3}$。）故得**卡丹諾公式**：

$$x = \sqrt[3]{\frac{q}{2}+\sqrt{\left(\frac{q}{2}\right)^2+\left(\frac{p}{3}\right)^3}} + \sqrt[3]{\frac{q}{2}-\sqrt{\left(\frac{q}{2}\right)^2+\left(\frac{p}{3}\right)^3}}$$

一個三次方程的解，竟靠「先降維成二次、再倒推回去」完成——降階代換 $x = t - \frac{b}{3a}$ 是整個推理的樞紐。

### 線索三：casus irreducibilis 與複數的意外現身
當判別式 $\Delta = \left(\frac{q}{2}\right)^2 + \left(\frac{p}{3}\right)^3 < 0$ 時（**casus irreducibilis，不可約情形**），公式中出現**負數的平方根**——例如 Bombelli（1572）處理

$$x^3 - 15x - 4 = 0$$

公式給出 $x = \sqrt[3]{2 + \sqrt{-121}} + \sqrt[3]{2 - \sqrt{-121}} = \sqrt[3]{2 + 11i} + \sqrt[3]{2 - 11i}$，但此方程顯然有實根 $x = 4$（$64 - 60 - 4 = 0$）。

**推理**：Bombelli 壯著膽子「按虛數的規則運算」：$(2+11i) = (2+i)^3$，故 $x = (2+i) + (2-i) = 4$——虛數互相對消，實根從「不可能的符號」中復活。更深的不可能性（Wantzel 1843 年證明）：**不可約情形下，三次方程的三個實根無法僅用實數根式表示**——複數不是可有可無的技巧，而是根式解的邏輯必經之路。虛數就這樣「被迫現身」，最終由 Euler、Gauss、Argand 建立複數理論。

### 線索四：Ferrari 四次方程
Ferrari（Cardano 的弟子，1540 年前後）解出**四次方程**：把 $x^4 + bx^2 + d = e x$ 改寫為

$$\left(x^2 + \frac{b}{2} + y\right)^2 = \left(2y + b\right)x^2 + e x + \left(y^2 + by + \frac{b^2}{4} + d\right)$$

選 $y$ 使右邊成為完全平方（三次方程！），再用平方差分解為兩個二次方程。**推理**：四次 → 依賴三次 → 依賴二次，層層降階。這條「降階鏈」自然引出終極追問：五次方程呢？——答案是否定的（Abell–Ruffini 1824，Galois 1832 結案），群論正是沿著這條鏈的盡頭誕生的。

### Python：用 Cardano 公式解三次方程
```python
import cmath

def cardano(p, q):
    """解 t^3 + p*t + q = 0（卡丹諾公式，複數運算）"""
    disc = (q/2)**2 + (p/3)**3
    u = (-q/2 + cmath.sqrt(disc)) ** (1/3)
    v = (-q/2 - cmath.sqrt(disc)) ** (1/3)
    # 補上三個三次根的組合（乘以 1, ω, ω^2）
    w = complex(-0.5, cmath.sqrt(3)/2)
    roots = []
    for i in range(3):
        for j in range(3):
            if abs((u * w**i) * (v * w**j) + p/3) < 1e-9:
                roots.append(u * w**i + v * w**j)
    return roots

def solve_cubic(a, b, c, d):
    """解 a*x^3 + b*x^2 + c*x + d = 0（先降階成簡約式）"""
    t = -b / (3*a)                        # 降階代換 x = t - b/(3a)
    p = (3*a*c - b*b) / (3*a*a)
    q = (2*b**3 - 9*a*b*c + 27*a*a*d) / (27*a**3)
    return [r - t for r in cardano(p, q)]

# Bombelli 原題：x^3 - 15x - 4 = 0，實根 x = 4
for r in cardano(-15, -4):
    print(r)  # (4+0j) —— 虛數對消，實根復活！

for r in solve_cubic(1, 0, -15, -4):
    print(round(r.real, 10))
```

## 結案 -- 後果與影響
- **結案陳詞**：三次與四次方程的懸案正式結案，公式入檔《Ars Magna》；但誓言糾紛與「不可約情形」的詭異現象，才是案件真正的深水區。
- 複數從「被迫的技巧」逐步升格：Bombelli（1572 虛數運算規則）→ Euler（1777 記號 $i$）→ Gauss、Argand（複平面）→ 現代數學與物理（量子力學、電機工程）的基石。
- 「降階鏈到五次即斷」的追問（Abel–Ruffini、Galois）催生了**群論**——代數學史上最深刻的典範轉移。
- 《Ars Magna》被譽為「文藝復興數學的頂峰」，與哥白尼《天體運行論》（1543）、維薩里《人體構造》（1543）同年代並列科學革命前夜。

## 關鍵人物與文獻
- **Scipione del Ferro**（1465–1526）：第一個解出三次方程的「原始兇手」，秘而不宣。
- **Niccolò Tartaglia**（1500–1557）：獨立再發現解法，誓言受損的「受害者」。
- **Girolamo Cardano**（1501–1576）：出版《Ars Magna》的「結案者」，同時也是「破誓者」。
- **Lodovico Ferrari**（1522–1565）：四次方程解法的發現者。
- **Rafael Bombelli**（1526–1572）：《Algebra》（1572）建立虛數運算規則，讓實根從虛數中復活。
- Cardano, *Ars Magna*（1545）；Witmer 英譯本, MIT Press, 1968。
