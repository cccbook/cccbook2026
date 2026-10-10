# 1572 — Bombelli 虛數運算

## 案件摘要
1572 年，波隆那工程師 Rafael Bombelli 出版《L'Algebra》，正面迎戰 Cardano 公式留下的最大懸案——casus irreducibilis（不可約情況）：方程明明有三個實根，公式中卻出現負數的平方根。Bombelli 做了一件前人不敢做的事：不再迴避「鬼魅」，而是給虛數定義**完整的四則運算規則**，證明這些鬼魅按照規則相加相乘後，鬼魅互相抵消、恰好還原出實根。虛數從此從「心理折磨」變成「計算工具」。

## 前因 -- 為什麼會有這個案子
- 1545 年 Cardano《Ars Magna》公開三次方程解法，但遇到判別式 $(q/2)^2+(p/3)^3 < 0$ 時公式失效——而此時方程明明有實根。
- Cardano 的態度是迴避：此類題目改用其他方法（如試根）處理，或乾脆不碰。
- Tartaglia 曾指出此「不可約情況」的存在，但未給出解法；他隱約察覺這裡藏著「不可能」的深淵（兩百年後才證明：此情況下三次方程**不可能**只用實數根式求解）。
- 16 世紀義大利是工程師的天下：Bombelli 本職是排水工程與土地測量，他在羅馬近郊的水利工程中實際遇到需要解三次方程的問題——鬼魅不是書齋裡的哲學問題，而是工地上的實務障礙。
- Bombelli 在羅馬閱讀 Diophantus《算術》抄本（Vatican 抄本），希臘丟番圖的記號啟發他建立自己的代數語言。

案子就在工地與書齋之間爆發：虛數若無運算規則，工程計算就寸步難行。Bombelli 寫作的態度極其清醒——他不自稱「發明者」，而是自稱「整理者」：把前人的成果（del Ferro、Cardano、Tartaglia 的三次方程理論，Diophantus 的算術問題）整理成一套自洽的系統。但正是在整理的過程中，他被迫面對 Cardano 迴避的鬼魅，並做出前人不敢做的推理。《L'Algebra》分三卷：第一卷是記號與基本運算，第二卷是方程的冪（多次方），第三卷是 Diophantus 風格的應用題——虛數的運算規則就誕生在第一卷與第二卷的夾縫中。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Bombelli 的經典案例 $x^3 = 15x + 4$
考慮 casus irreducibilis 的代表方程：

$$x^3 = 15x + 4 \quad\Longleftrightarrow\quad x^3 - 15x - 4 = 0$$

肉眼可見 $x=4$ 是根（$64 = 60+4$），因式分解得三個實根：

$$x^3 - 15x - 4 = (x-4)(x^2+4x+1) \;\Rightarrow\; x = 4,\; -2\pm\sqrt{3}$$

但套用 Cardano 公式（$p=-15, q=-4$）：

$$x = \sqrt[3]{2+\sqrt{-121}} + \sqrt[3]{2-\sqrt{-121}}$$

判別式 $4-125=-121<0$。公式宣稱答案是 $\sqrt[3]{2+\sqrt{-121}}+\sqrt[3]{2-\sqrt{-121}}$，可是它**必須**等於 $4$——兩個鬼魅之和竟是一個實數。怎麼可能？

### 線索二：Bombelli 的「瘋狂想法」——鬼魅之間也有法則
Bombelli 的推理是：既然兩個鬼魅之和是實數，那麼 $\sqrt[3]{2+\sqrt{-121}}$ 與 $\sqrt[3]{2-\sqrt{-121}}$ 必定各自「含有一個實的部分」與「一個虛的部分」，且虛部互相抵消。他大膽假設：

$$\sqrt[3]{2+\sqrt{-121}} = 2 + n\sqrt{-1}, \qquad \sqrt[3]{2-\sqrt{-121}} = 2 - n\sqrt{-1}$$

立方展開，比較係數：

$$(2+n\sqrt{-1})^3 = 8 + 12n\sqrt{-1} - 6n^2 - n^3\sqrt{-1} = (8-6n^2) + (12n - n^3)\sqrt{-1}$$

要求實部 $8-6n^2 = 2$ 得 $n^2=1$，$n=1$；檢查虛部 $12n-n^3 = 12-1 = 11 = \sqrt{121}$ ✓。於是：

$$\sqrt[3]{2+\sqrt{-121}} = 2+\sqrt{-1}, \qquad x = (2+\sqrt{-1}) + (2-\sqrt{-1}) = 4 ✓$$

Bombelli 自己形容這是「野蠻的想法」（wild thought），但它**運作了**。

### 線索三：虛數的四則運算規則
Bombelli 在《L'Algebra》中把 $+\sqrt{-1}$ 稱為「più di meno」（正負之一），$-\sqrt{-1}$ 稱為「meno di meno」（負負之一），並明確列出乘法規則（以現代記號）：

$$(+\sqrt{-1})(+\sqrt{-1}) = -1, \qquad (+\sqrt{-1})(-\sqrt{-1}) = +1$$

$$(a+b\sqrt{-1})(c+d\sqrt{-1}) = (ac - bd) + (ad+bc)\sqrt{-1}$$

以及加減法：實部與實部、虛部與虛部各自合併。這正是現代複數 $a+bi$ 的加法與乘法公式的第一次系統陳述——虛部不再是可以忽略的雜訊，而是與實部**平起平坐**的運算對象。

### 線索四：共軛的雛形
Bombelli 注意到 $\sqrt[3]{2+\sqrt{-121}}$ 與 $\sqrt[3]{2-\sqrt{-121}}$ 這一對「鏡像」量相加時虛部自動歸零——這是**共軛複數** $z = a+bi$ 與 $\bar{z} = a-bi$ 概念的胚胎。他還觀察到：實係數方程若有虛根，虛根必成對出現（因為共軛配對相乘得實數 $ac-bd$ 項）——這正是兩百年後 Gauss 代數基本定理中「複根成對」定理的先聲。

### 程式碼範例：Bombelli 的 $(2+\sqrt{-121})^{1/3}$ 運算
```python
import numpy as np

# 線索一：casus irreducibilis 的 Cardano 公式
p, q = -15, -4
disc = (q/2)**2 + (p/3)**3
print("判別式 =", disc)  # -121 < 0

# 複數開立方：取主值，再乘三次單位根
z1 = 2 + np.sqrt(complex(disc))   # 2 + 11i
z2 = 2 - np.sqrt(complex(disc))   # 2 - 11i
w = np.exp(2j*np.pi*np.arange(3)/3)

print("z1 的三個立方根:", [complex(round(c,6)) for c in z1**(1/3)*w])
# 應含 2+1i（Bombelli 的答案！）

# 線索二的驗證：配對立方根之和為實根
for c1 in z1**(1/3)*w:
    for c2 in z2**(1/3)*w:
        s = c1 + c2
        if abs(s.imag) < 1e-9:
            print(f"({c1:.6f}) + ({c2:.6f}) = {s.real:.6f}  ← 實根！")

# 線索三：四則運算規則
a, b, c, d = 2, 1, 2, -1
prod = (a + b*1j) * (c + d*1j)
print("(2+i)(2-i) =", prod, " 虛部抵消，實部 =", prod.real)
```

輸出顯示 $z1 = 2+11i$ 的三個立方根中含 $2+1i$（Bombelli 的猜測被數值證實），且 $(2+i)+(2-i) = 4$ 正是原方程的實根——鬼魅按法則相加，鬼魅消失，實數現身。

## 結案 -- 後果與影響
- 虛數從「不可理解的怪物」變成**有法則的計算工具**：Bombelli 的運算規則（實部/虛部分離、共軛配對）就是現代複數算術的祖先。
- casus irreducibilis 的答案被「救回」：工程師可以繼續用 Cardano 公式解三次方程，不必再繞道。
- 1685 年 John Wallis 嘗試用幾何詮釋虛數；1797–1799 年 Wessel、Argand、Gauss 給出複數平面，虛數終於獲得幾何合法性。
- 1832 年 Galois 證明：casus irreducibilis 情況下三次方程**不可能**只用實數根式求解——虛數不是可有可無的捷徑，而是**必經之路**。Bombelli 當年的「野蠻想法」其實是數學的必然。
- Descartes 1637 年創造「imaginary」（虛構的）一詞帶有貶義，但諷刺的是：這個「虛構」的數系後來成為量子力學、電磁學、訊號處理的基礎語言。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Rafael Bombelli | 《L'Algebra》作者，定義虛數運算規則 |
| Gerolamo Cardano | 前案：《Ars Magna》留下 casus irreducibilis 懸案 |
| Niccolò Tartaglia | 指出不可約情況的存在 |
| Diophantus | 《算術》抄本啟發 Bombelli 的代數記號 |

- R. Bombelli, *L'Algebra*, Bologna (1572；全本 1579)：「più di meno」與虛數四則運算。
- J. M. Child (ed.), *The Geometrical Lectures of Isaac Newton* 附錄對 Bombelli 的英譯與研究（1911）。
