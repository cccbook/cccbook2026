# 1545 — Cardano 虛數

## 案件摘要
1545 年，米蘭醫師兼博學家 Gerolamo Cardano 出版《Ars Magna》（大術），首次公開三次與四次方程的一般解法。然而書中一個看似無害的問題——把 10 分成兩數，使其積為 40——逼出了方程 $x(10-x)=40$ 的解 $5\pm\sqrt{-15}$。Cardano 稱這種「負數的平方根」是「心理折磨」（mental tortures），卻又發現：若硬著頭皮按運算規則操作，結果居然自洽。這是虛數在西方文獻中的第一次正式登場——不是被發明，而是被**逼供**出來的。

## 前因 -- 為什麼會有這個案子
- **巴比倫（約公元前 1800 年）**：泥板已記載二次方程的解法，本質上就是配方法。只要判別式非負，答案總是「實在」的長度或面積，數學與幾何測量不分家。
- **古希臘**：幾何代數把方程化為線段與面積的構作，任何「不存在的量」都被幾何直覺排除在外。
- **9 世紀 al-Khwārizmī**：《代數學》系統化二次方程求解，但堅持一切量必須對應可測量的幾何對象，負根一概不取。
- **1202 年 Fibonacci**：《Liber Abaci》把印度—阿拉伯數碼與伊斯蘭代數帶入歐洲，三次方程的競賽文化在義大利逐漸升溫。
- **16 世紀義大利數學競賽**：數學家公開下戰帖互解對方出的題目，勝者贏得名聲與職位。三次方程是當時的「聖杯」——巴比倫以降兩千年無人能解。

案子就在這種競賽文化中點火：誰先解出三次方程，誰就名留青史——但解法本身藏著一顆定時炸彈。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Scipione del Ferro 與 Tartaglia 的秘密
約 1515 年，波隆那大學教授 Scipione del Ferro 解出了**缺二次項**的三次方程：

$$x^3 + px = q$$

他臨終前把秘密傳給學生 Antonio Fior。1535 年，Fior 向布雷西亞的 Niccolò Tartaglia 下戰帖，Tartaglia 在比賽前夜重新發現解法，大獲全勝。Tartaglia 把解法寫成晦澀的詩歌保密——直到 1539 年 Cardano 以「絕不外傳」的誓言換得口述版本。

### 線索二：Cardano 公式的誕生
對 $x^3 + px = q$，設 $x = u + v$ 且約束 $3uv = -p$（即 $u^3v^3 = -p^3/27$），代入展開：

$$x^3 = u^3 + v^3 + 3uv(u+v) = (u^3+v^3) - p(u+v) = q$$

於是 $u^3, v^3$ 是二次方程 $t^2 - qt - \frac{p^3}{27} = 0$ 的兩根，解得：

$$u^3, v^3 = \frac{q}{2} \pm \sqrt{\frac{q^2}{4} + \frac{p^3}{27}}, \qquad x = \sqrt[3]{\frac{q}{2} + \sqrt{\frac{q^2}{4} + \frac{p^3}{27}}} + \sqrt[3]{\frac{q}{2} - \sqrt{\frac{q^2}{4} + \frac{p^3}{27}}}$$

### 線索三：炸彈引信——$\sqrt{-15}$ 現身
Cardano 在《Ars Magna》第 37 章提出挑戰題：「把 10 分成兩部分，乘積為 40。」設兩數為 $x$ 與 $10-x$：

$$x(10-x) = 40 \;\Rightarrow\; x^2 - 10x + 40 = 0 \;\Rightarrow\; x = 5 \pm \sqrt{-15}$$

Cardano 寫道：「如果有人說 $5 \pm \sqrt{-15}$ 的乘積是 40，這看似精巧卻毫無用處（as subtle as it is useless）。」他驗算了：$(5+\sqrt{-15})(5-\sqrt{-15}) = 25 - (-15) = 40$——數學上自洽，幾何上無解。數學第一次**超越**了「量必須可測量」的兩千年教條。

### 線索四：優先權之爭
1543 年 Cardano 與學生 Ferrari 到波隆那查訪 del Ferro 的遺稿，確認 del Ferro 確實更早解出三次方程（也包含四次方程的退化情形），於是在《Ars Magna》中（違背對 Tartaglia 的誓言）公開解法並註明功勞屬 del Ferro 與 Tartaglia。Tartaglia 憤怒抗議，雙方展開長年罵戰、互發詆毀詩文；1548 年 8 月 10 日，Ferrari 與 Tartaglia 在米蘭公開辯論，第一回合 Tartaglia 佔上風，但次日他未出席續場，判決落敗，聲名盡毀，晚年貧困死於威尼斯。這場優先權之爭是科學史上最早的「學術醜聞」之一，但也讓三次方程解法迅速傳遍歐洲。

值得注意的是《Ars Magna》在數學史上的地位：Cardano 本人是醫師、占星家與賭徒，一生波折不斷（兒子被判死刑、自己曾因算耶穌星盤入獄），他寫書的動機之一正是賭博與機率——《Ars Magna》第 37 章同時包含最早的概率計算（骰子問題），是 Pascal 與 Fermat 1654 年機率論的先聲。虛數與機率，兩門被「懷疑」的數學，竟在同一章裡誕生。

### 程式碼範例：Cardano 三次方程求解
```python
import numpy as np

def cardano(p, q):
    """解 x^3 + p x = q，返回三個根（複數）"""
    disc = (q/2)**2 + (p/3)**3          # 判別式
    u = np.cbrt(q/2 + np.sqrt(disc + 0j))  # 複數開立方
    v = np.cbrt(q/2 - np.sqrt(disc + 0j))
    # 三個立方根（乘以三次單位根）
    w = np.exp(2j*np.pi*np.arange(3)/3)
    roots = set()
    for ui in u*w:
        for vi in v*w:
            if abs(3*ui*vi + p) < 1e-8:   # 約束 3uv = -p
                roots.add(complex(round(ui+vi, 8)))
    return sorted(roots, key=lambda z: (z.real, z.imag))

# 案例 1：x^3 + 6x = 20（Tartaglia 的考題），根為 x=2
print("x^3+6x=20 的根:", cardano(6, 20))

# 案例 2：casus irreducibilis —— x^3 - 15x - 4 = 0，三實根 x=4,-2±√3
# 判別式為負，Cardano 公式被迫出現 √(-1)！
print("x^3-15x-4=0 的根:", cardano(-15, -4))

# 案例 3：Cardano 的「心理折磨」題
a = 5 + np.sqrt(-15+0j); b = 5 - np.sqrt(-15+0j)
print("5+√-15 的積 =", a*b, "（Cardano 驗證：應為 40）")
```

程式輸出顯示：$x^3+6x=20$ 得實根 $2$（$(3)^2+(2)^3=9+8>0$，公式乾淨俐落）；但 $x^3-15x-4=0$ 明明有三個實根 $4,\,-2\pm\sqrt{3}$，判別式 $(q/2)^2+(p/3)^3 = 4-125 = -121 < 0$，Cardano 公式出現 $\sqrt{-121}$，被迫在實數世界裡引入虛數——明明題目與答案都是「實在」的，中間過程卻必須鬧鬼。此案正是 1572 年 Bombelli 案的伏筆。而 $5\pm\sqrt{-15}$ 的積確實等於 $40$。

## 結案 -- 後果與影響
- 《Ars Magna》被視為**近代數學的起點**：方程式第一次擺脫幾何構作，成為獨立的代數對象。
- 四次方程解法（Ferrari，代換化為輔助三次方程）同書發表；五次方程的「不可能性」懸案則要等到 1824 年 Abel 才結案。
- 虛數被迫誕生：Cardano 雖稱其「無用」，卻承認其運算自洽，為 1572 年 Bombelli 的系統化鋪路。
- casus irreducibilis 的悖論——「三個實根卻必須經過虛數才能算出」——成為日後證明「實數域上不存在三次方程純實根式解」的關鍵，間接催生了 Galois 理論。
- 優先權之爭留下教訓：保密文化與公開發表的衝突，正是現代學術出版制度的反面教材。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Gerolamo Cardano | 出版《Ars Magna》，虛數首次登場 |
| Scipione del Ferro | 約 1515 年最早解出缺二次項三次方程 |
| Niccolò Tartaglia | 1535 年獨立再發現，與 Cardano 爭優先權 |
| Lodovico Ferrari | Cardano 學生，解四次方程，辯論擊敗 Tartaglia |

- G. Cardano, *Ars Magna*, Nuremberg: Petreius (1545)，第 37 章：「心理折磨」式虛數。
- N. Tartaglia, *Quesiti et Inventioni Diverse* (1546)：Tartaglia 版本的解法與爭議記述。
