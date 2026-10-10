# OpenCode discussion

**Session ID:** ses_ee011ab00ffe0642BOuFtMalZk
**Created:** 10/9/2026, 5:11:15 PM
**Updated:** 10/9/2026, 5:42:38 PM

---

## User

opencode

---

## Assistant (Build · GLM-5.3-Flash · 5.4s)

---

## User

為本書 每個章節，最後加上 該章節中的

## 補充

1. 數學推導證明
2. 簡易範例（計算，程式，....)

如果有程式，就把程式寫在 _code/ 中，按照 章節-名稱.py 來命名，例如 01-yyyy.py

---

## Assistant (Build · GLM-5.3-Flash · 14.5s)

_Thinking:_

The user wants me to add a "補充" (Supplement) section to each chapter of a math book, including mathematical derivations/proofs and simple examples (calculations, programs, etc.). If there's a program, it should be written in `_code/` directory, named by chapter-number.py format like `01-yyyy.py`.

First, I need to explore the working directory to understand the book structure - what chapters exist, their format, etc.

**Tool: bash**

**Input:**
```json
{
  "command": "ls -la"
}
```

**Output:**
```
total 320
drwxr-xr-x@ 25 cccuser  staff   800 Oct  9 17:10 .
drwxr-xr-x@ 58 cccuser  staff  1856 Oct  9 13:19 ..
-rw-r--r--@  1 cccuser  staff  3482 Oct  9 13:05 01.1-神經元與邏輯運算.md
-rw-r--r--@  1 cccuser  staff  3646 Oct  9 13:05 01.2-學習規則與權重更新.md
-rw-r--r--@  1 cccuser  staff  4897 Oct  9 13:13 02.1-感知器與線性分類.md
-rw-r--r--@  1 cccuser  staff  4126 Oct  9 13:05 02.2-損失函數與梯度下降.md
-rw-r--r--@  1 cccuser  staff  3623 Oct  9 13:13 03.1-活化函數與泛近似定理.md
-rw-r--r--@  1 cccuser  staff  4951 Oct  9 13:05 03.2-反向傳播演算法.md
-rw-r--r--@  1 cccuser  staff  4212 Oct  9 13:13 04.1-Hopfield網路與能量函數.md
-rw-r--r--@  1 cccuser  staff  4446 Oct  9 13:13 04.2-Boltzmann機器與softmax.md
-rw-r--r--@  1 cccuser  staff  4289 Oct  9 13:05 04.3-熵KL散度與資訊理論.md
-rw-r--r--@  1 cccuser  staff  4486 Oct  9 13:13 05.1-CNN與權重共享.md
-rw-r--r--@  1 cccuser  staff  4776 Oct  9 13:13 05.2-注意力機制與Transformer.md
-rw-r--r--@  1 cccuser  staff  4456 Oct  9 13:13 05.3-位置編碼與RoPE.md
-rw-r--r--@  1 cccuser  staff  4295 Oct  9 13:13 06.1-機率語言模型.md
-rw-r--r--@  1 cccuser  staff  5587 Oct  9 13:13 06.2-擴散模型與隨機微分方程.md
-rw-r--r--@  1 cccuser  staff  4589 Oct  9 13:05 06.3-規模法則與湧現.md
-rw-r--r--@  1 cccuser  staff  5378 Oct  9 13:05 07.1-MDP與貝爾曼方程.md
-rw-r--r--@  1 cccuser  staff  6122 Oct  9 13:13 07.2-策略梯度與PPO.md
-rw-r--r--@  1 cccuser  staff  6508 Oct  9 13:05 08.1-哈密頓神經網路與守恆學習.md
-rw-r--r--@  1 cccuser  staff  6377 Oct  9 13:13 08.2-世界模型與隱空間規劃.md
-rw-r--r--@  1 cccuser  staff  2398 Oct  9 13:13 A1-數學符號.md
-rw-r--r--@  1 cccuser  staff  6277 Oct  9 13:05 README.md
-rw-r--r--@  1 cccuser  staff  6401 Oct  9 13:34 _chat_世界模型.md
drwxr-xr-x@  2 cccuser  staff    64 Oct  9 17:10 _code

```

**Tool: glob**

**Input:**
```json
{
  "pattern": "**/*.md"
}
```

**Output:**
```
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/01.2-學習規則與權重更新.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/04.3-熵KL散度與資訊理論.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/02.2-損失函數與梯度下降.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/06.2-擴散模型與隨機微分方程.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/04.1-Hopfield網路與能量函數.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/04.2-Boltzmann機器與softmax.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/05.1-CNN與權重共享.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/02.1-感知器與線性分類.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/05.3-位置編碼與RoPE.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/01.1-神經元與邏輯運算.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/08.2-世界模型與隱空間規劃.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/05.2-注意力機制與Transformer.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/README.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/A1-數學符號.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/06.1-機率語言模型.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/_chat_世界模型.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/06.3-規模法則與湧現.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/08.1-哈密頓神經網路與守恆學習.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/07.1-MDP與貝爾曼方程.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/03.2-反向傳播演算法.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/07.2-策略梯度與PPO.md
/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/03.1-活化函數與泛近似定理.md
```

---

## Assistant (Build · GLM-5.3-Flash · 7.8s)

_Thinking:_

There are 20 chapter files (01.1 through 08.2). I need to read them all to understand each chapter's content, then append a 補充 section with derivations and examples, plus create Python code files in _code/.

This is a large task. Let me read all files first. I'll batch read them.

我先讀取所有章節內容，了解每章主題後再逐一加上補充。

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/01.1-神經元與邏輯運算.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/01.1-神經元與邏輯運算.md</path>
<type>file</type>
<content>
1: # 01.1 神經元與邏輯運算
2: 
3: ## 本章導讀
4: 
5: 大腦有約 $10^{11}$ 個神經元，彼此用突觸相連。1943 年，McCulloch 與 Pitts 問了一個大膽的問題：
6: 「神經元能不能用數學描述？」答案是——可以，而且只要一行公式。
7: 這一章我們把生物神經元翻譯成數學，並用它拼出邏輯電路。
8: 
9: ## 淺顯說明
10: 
11: 想像一個神經元像一個「投票箱」：
12: 
13: - 它收到很多輸入訊號 $x_1, x_2, \dots, x_n$ （有的興奮、有的抑制）。
14: - 每個輸入有不同「票值」 $w_1, w_2, \dots, w_n$ （突觸強度）。
15: - 總票數 $\sum_i w_i x_i$ 超過門檻 $\theta$ ，神經元就「放電」輸出 1，否則輸出 0。
16: 
17: 就這麼簡單——加權求和、過門檻、放電。所有深度學習模型，都是從這一行公式長出來的。
18: 
19: ## 正規理論
20: 
21: ### McCulloch–Pitts 神經元
22: 
23: 給定輸入向量 $\mathbf{x} \in \{0,1\}^n$ 、權重 $\mathbf{w} \in \mathbb{R}^n$ 與閾值 $\theta$ ，定義：
24: 
25: $$
26: y = \Theta\!\left(\sum_{i=1}^n w_i x_i - \theta\right), \qquad
27: \Theta(z) = \begin{cases} 1, & z \ge 0 \\ 0, & z < 0 \end{cases}
28: $$
29: 
30: 這是一個**線性閾值單元**（Linear Threshold Unit, LTU）。它把 $\mathbb{R}^n$ 用一個超平面切成兩半。
31: 
32: ### 幾何詮釋：超平面
33: 
34: 方程 $\sum_i w_i x_i = \theta$ 定義 $\mathbb{R}^n$ 中的一個超平面， $\mathbf{w}$ 是其法向量：
35: 
36: $$
37: H = \{\mathbf{x} \in \mathbb{R}^n : \mathbf{w}^\top \mathbf{x} = \theta\}
38: $$
39: 
40: 單元輸出即「 $\mathbf{x}$ 在超平面的哪一側」。
41: 
42: ### 用 M-P 網路拼邏輯閘
43: 
44: - **AND**（ $\theta = 2, w_i = 1$ ）：只有 $x_1 = x_2 = 1$ 時總和 $2 \ge 2$ 。
45: - **OR**（ $\theta = 1, w_i = 1$ ）：任何一個輸入為 1 即放電。
46: - **NOT**（單輸入， $w = -1, \theta = 0$ ）： $x=1 \Rightarrow -1 < 0$ 輸出 0。
47: 
48: 定理（McCulloch–Pitts）：任何有限布林函數都可以用一個兩層的 M-P 網路實現。
49: 因為任何布林函數都可寫成積和範式（DNF），第一層每個單元偵測一個 minterm，第二層做 OR。
50: 
51: ## 簡易範例：XOR 之謎
52: 
53: XOR 的真值表：
54: 
55: | $x_1$ | $x_2$ | $y$ |
56: |---|---|---|
57: | 0 | 0 | 0 |
58: | 0 | 1 | 1 |
59: | 1 | 0 | 1 |
60: | 1 | 1 | 0 |
61: 
62: 單一 LTU 能做 XOR 嗎？需要 $\mathbf{w}^\top(0,1) \ge \theta$ 、 $\mathbf{w}^\top(1,0) \ge \theta$ 、
63: $\mathbf{w}^\top(0,0) < \theta$ 、 $\mathbf{w}^\top(1,1) < \theta$ 。
64: 
65: 前兩式相加得 $w_1 + w_2 \ge 2\theta$ ，但由後兩式得 $w_1 + w_2 < 2\theta$ ——矛盾！
66: 
67: **結論：單一超平面切不開 XOR**（四點構成的對角對無法被一直線分開）。
68: 需要兩層網路： $y = \Theta(x_1 + x_2 - 2\,\Theta(x_1 + x_2 - 1))$ 。
69: 
70: 這個小小的矛盾，延宕了神經網路研究近 20 年（見歷史典故）。
71: 
72: ## 歷史典故
73: 
74: - 1943 年 McCulloch–Pitts 誕生：見卷宗 [../1943-麥卡洛克皮茨邏輯神經元.md](../1943-麥卡洛克皮茨邏輯神經元.md)——一位神經科學家與一位邏輯學家在芝加哥的相遇。
75: - 1969 年 Minsky–Papert 用 XOR 問題批判感知器：見 [../1969-MinskyPapert批判.md](../1969-MinskyPapert批判.md)——一本書讓神經網路寒冬降臨。
76: 
77: ## 習題
78: 
79: 1. 設計一個 M-P 網路實現三輸入的多數決（至少兩個輸入為 1 才輸出 1）。
80: 2. 證明：XOR 可由 $y = (x_1 \lor x_2) \land \lnot(x_1 \land x_2)$ 表達，並將此式翻譯成兩層 M-P 網路。
81: 3. 說明為什麼單一 LTU 是線性分類器，而兩層 M-P 網路可以是非線性的。

(End of file - total 81 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/01.2-學習規則與權重更新.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/01.2-學習規則與權重更新.md</path>
<type>file</type>
<content>
1: # 01.2 學習規則與權重更新
2: 
3: ## 本章導讀
4: 
5: McCulloch–Pitts 的神經元是「固定的」——權重是設計出來的，不是學出來的。
6: 1949 年，心理學家 Hebb 提出一個直覺到近乎顯然的規則：
7: 「一起放電的神經元，連在一起。」這一行話，讓神經網路從「被建造」變成「會學習」。
8: 
9: ## 淺顯說明
10: 
11: Hebb 的想法：如果你的兩個朋友總是一起出現，你會自動把「他們倆」聯想在一起。
12: 數學上：如果神經元 $i$ 和 $j$ **同時**放電（ $x_i = x_j = 1$ ），就把連接它們的權重 $w_{ij}$ 加大一點：
13: 
14: $$
15: w_{ij} \;\leftarrow\; w_{ij} + \eta\, x_i x_j
16: $$
17: 
18: $\eta$ 是「學習速率」。多次重複後，常一起出現的模式就被「烙印」在權重矩陣裡。
19: 
20: ## 正規理論
21: 
22: ### Hebb 學習規則
23: 
24: 給定訓練模式 $\{\mathbf{x}^{(1)}, \dots, \mathbf{x}^{(M)}\}$ ， $\mathbf{x}^{(\mu)} \in \{-1, +1\}^n$ ，Hebb 律定義權重矩陣：
25: 
26: $$
27: W = \eta \sum_{\mu=1}^{M} \mathbf{x}^{(\mu)} \, \mathbf{x}^{(\mu)\top}
28: $$
29: 
30: 這是所有訓練模式的**外積之和**——每個模式貢獻一個秩一矩陣。
31: 
32: ### 外積儲存的幾何
33: 
34: 外積 $\mathbf{x}\mathbf{x}^\top$ 是一個秩一矩陣，把任何向量投影到 $\mathbf{x}$ 方向後放大：
35: 
36: $$
37: (\mathbf{x}\mathbf{x}^\top)\mathbf{v} = \mathbf{x}\,(\mathbf{x}^\top \mathbf{v})
38: $$
39: 
40: 當 $W = \sum_\mu \mathbf{x}^{(\mu)}\mathbf{x}^{(\mu)\top}$ 且各模式近似正交時：
41: 
42: $$
43: W\mathbf{x}^{(\nu)} \approx \mathbf{x}^{(\nu)} + \sum_{\mu \ne \nu} \mathbf{x}^{(\mu)}(\mathbf{x}^{(\mu)\top}\mathbf{x}^{(\nu)}) \approx n\,\mathbf{x}^{(\nu)}
44: $$
45: 
46: 雜訊項因正交性（ $\mathbf{x}^{(\mu)\top}\mathbf{x}^{(\nu)} \approx 0$ ）而消失。
47: **輸入一個殘缺的模式，權重矩陣會把它「補全」成最像的已學模式**——這就是聯想記憶。
48: 
49: ### 儲存容量
50: 
51: $n$ 個神經元、隨機模式，Hebb 聯想記憶的容量約為：
52: 
53: $$
54: M_{\max} \approx \frac{n}{2\ln n}
55: $$
56: 
57: 超過容量，模式間的干涉（cross-talk）會讓回憶失敗。
58: 
59: ## 簡易範例：儲存兩個模式
60: 
61: 儲存 $\mathbf{x}^{(1)} = (1, 1, -1)^\top$ 與 $\mathbf{x}^{(2)} = (-1, 1, 1)^\top$ ， $\eta = 1$ ：
62: 
63: $$
64: \mathbf{x}^{(1)}\mathbf{x}^{(1)\top} = \begin{pmatrix} 1 & 1 & -1 \\ 1 & 1 & -1 \\ -1 & -1 & 1 \end{pmatrix}, \qquad
65: \mathbf{x}^{(2)}\mathbf{x}^{(2)\top} = \begin{pmatrix} 1 & -1 & -1 \\ -1 & 1 & 1 \\ -1 & 1 & 1 \end{pmatrix}
66: $$
67: 
68: $$
69: W = \begin{pmatrix} 2 & 0 & -2 \\ 0 & 2 & 0 \\ -2 & 0 & 2 \end{pmatrix}
70: $$
71: 
72: 現在輸入殘缺版 $\mathbf{v} = (1, 0, -1)^\top$ （第二位遺失）：
73: 
74: $$
75: W\mathbf{v} = (4, 0, -4)^\top \;\xrightarrow{\text{取符號}}\; (1, 1, -1)^\top = \mathbf{x}^{(1)}
76: $$
77: 
78: 遺失的位元被補回來了——網路「想起」了模式一。
79: 
80: ## 歷史典故
81: 
82: - 1949 年 Hebb 學習規則：見卷宗 [../1949-Hebb學習規則.md](../1949-Hebb學習規則.md)——一句「cells that fire together, wire together」改寫了學習理論。
83: - 1890 年 William James 的聯想主義：見 [../1890-WilliamJames聯想主義.md](../1890-WilliamJames聯想主義.md)——Hebb 律的心理學前身，早了 59 年。
84: - Hebb 律的成熟應用（Hopfield 網路）將在第 04.1 節正式登場。
85: 
86: ## 習題
87: 
88: 1. 用 Hebb 律儲存 $\mathbf{x}^{(1)} = (1,-1,1)$ 與 $\mathbf{x}^{(2)} = (1,1,-1)$ ，寫出 $W$ ，並驗證輸入 $(0,-1,1)$ 能回憶出哪個模式。
89: 2. 證明：若所有模式兩兩正交（ $\mathbf{x}^{(\mu)\top}\mathbf{x}^{(\nu)} = 0$ ），則雜訊項恰為零。
90: 3. 討論：為什麼 Hebb 律「只會加強、不會減弱」在生物上與數學上各有什麼問題？（提示：權重會無界增長。）

(End of file - total 90 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/02.1-感知器與線性分類.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/02.1-感知器與線性分類.md</path>
<type>file</type>
<content>
1: # 02.1 感知器與線性分類
2: 
3: ## 本章導讀
4: 
5: 1957 年，Rosenblatt 把 Hebb 的學習規則改造成一個可以「從標籤學習」的演算法——感知器（Perceptron）。
6: 它不只會記憶，還會**根據對錯調整自己**。更驚人的是，它有一個數學保證：只要答案存在，它**必定找得到**。
7: 
8: ## 淺顯說明
9: 
10: 感知器的學習循環像考試訂正：
11: 
12: 1. 作答：用目前的權重 $\mathbf{w}$ 預測 $\hat y$ 。
13: 2. 對答案： $\hat y$ 和正解 $y$ 一樣嗎？
14: 3. 訂正：錯了才改——「預測太小就加權重，太大就減權重」，而且只動有影響的輸入。
15: 
16: 重複直到全對。Rosenblatt 證明：如果資料可以用一條直線分開，這個循環**保證收斂**。
17: 
18: ## 正規理論
19: 
20: ### 感知器模型
21: 
22: 輸入 $\mathbf{x} \in \mathbb{R}^n$ ，標籤 $y \in \{+1, -1\}$ ，權重 $\mathbf{w}$ ，偏置 $b$ ：
23: 
24: $$
25: \hat y = \mathrm{sgn}(\mathbf{w}^\top \mathbf{x} + b)
26: $$
27: 
28: ### 感知器學習演算法
29: 
30: $$
31: \mathbf{w} \leftarrow \mathbf{w} + \eta\, y\, \mathbf{x}, \qquad b \leftarrow b + \eta\, y \qquad \text{（僅當 } \hat y \ne y \text{ 時）}
32: $$
33: 
34: 統一寫法（把 $b$ 併入 $\mathbf{w}$ ， $\mathbf{x}$ 補一個 1）：
35: 
36: $$
37: \mathbf{w} \leftarrow \mathbf{w} + \eta\, y\,\mathbf{x} \quad \text{iff} \quad y(\mathbf{w}^\top\mathbf{x}) \le 0
38: $$
39: 
40: ### 感知器收斂定理（Novikoff, 1962）
41: 
42: **定理**：若存在單位向量 $\mathbf{w}^*$ 與邊距 $\gamma > 0$ 使得所有訓練資料滿足
43: $y_i(\mathbf{w}^{*\top}\mathbf{x}_i) \ge \gamma$ （線性可分且有邊距），
44: 則感知器演算法的更新次數 $k$ 滿足：
45: 
46: $$
47: k \;\le\; \frac{R^2}{\gamma^2}, \qquad R = \max_i \|\mathbf{x}_i\|
48: $$
49: 
50: **證明梗概**：設 $\mathbf{w}^{(k)}$ 為第 $k$ 次更新後的權重（ $\mathbf{w}^{(0)} = \mathbf{0}$ ）。
51: 
52: 1. 每次 update 用了被分錯的 $(\mathbf{x}_i, y_i)$ ：
53: 
54: $$
55: \mathbf{w}^{(k)\top}\mathbf{w}^* = \mathbf{w}^{(k-1)\top}\mathbf{w}^* + \eta\, y_i\, \mathbf{x}_i^\top \mathbf{w}^* \;\ge\; \mathbf{w}^{(k-1)\top}\mathbf{w}^* + \eta\gamma \;\Rightarrow\; \mathbf{w}^{(k)\top}\mathbf{w}^* \ge k\eta\gamma
56: $$
57: 
58: 2. 但每次 update 只加一個大小有界的項：
59: 
60: $$
61: \|\mathbf{w}^{(k)}\|^2 = \|\mathbf{w}^{(k-1)}\|^2 + 2\eta\, y_i\,\mathbf{w}^{(k-1)\top}\mathbf{x}_i + \eta^2\|\mathbf{x}_i\|^2 \;\le\; \|\mathbf{w}^{(k-1)}\|^2 + \eta^2 R^2 \;\Rightarrow\; \|\mathbf{w}^{(k)}\|^2 \le k\eta^2 R^2
62: $$
63: 
64: （因為分錯時 $y_i\,\mathbf{w}^{(k-1)\top}\mathbf{x}_i \le 0$ ，中間項非正。）
65: 
66: 3. 由 Cauchy–Schwarz：
67: 
68: $$
69: k\eta\gamma \;\le\; \mathbf{w}^{(k)\top}\mathbf{w}^* \;\le\; \|\mathbf{w}^{(k)}\|\,\|\mathbf{w}^*\| \;\le\; \sqrt{k}\,\eta R
70: $$
71: 
72: 兩邊除以 $\sqrt{k}\,\eta$ ： $\sqrt{k}\,\gamma \le R$ ，即 $k \le R^2/\gamma^2$ 。 $\blacksquare$
73: 
74: **意義**：更新次數只依賴「邊距與資料範圍的比值」，與維度無關——資料越「分得開」，學得越快。
75: 
76: ### ADALINE：從「對錯」到「誤差大小」
77: 
78: 1960 年 Widrow 的 ADALINE 改用連續誤差：不只在分錯時更新，而是最小化平方誤差
79: $L = (y - \mathbf{w}^\top\mathbf{x})^2$ 。這讓「學習」從離散的對錯，變成連續的優化——為梯度下降鋪路（下一節）。
80: 
81: ## 簡易範例：兩點分類
82: 
83: 資料： $\mathbf{x}_1 = (1,1), y_1 = +1$ ； $\mathbf{x}_2 = (-1,-1), y_2 = -1$ 。 $\eta = 1$ ， $\mathbf{w}^{(0)} = \mathbf{0}$ 。
84: 
85: 1. $(\mathbf{x}_1, +1)$ ： $\mathbf{w}^\top\mathbf{x}_1 = 0 \le 0$ ，分錯 → $\mathbf{w}^{(1)} = (1,1)$ 。
86: 2. $(\mathbf{x}_2, -1)$ ： $y\,\mathbf{w}^\top\mathbf{x} = (-1)\times(-2) = 2 > 0$ ，分對，不更新。
87: 3. 回到 $(\mathbf{x}_1)$ ： $y\,\mathbf{w}^\top\mathbf{x} = 2 > 0$ ，分對。**收斂**： $\mathbf{w} = (1,1), b = 0$ 。
88: 
89: 驗證理論： $R = \sqrt{2}$ ， $\gamma = \mathbf{w}^{*\top}\mathbf{x}_i = \sqrt{2}$ ，上界 $R^2/\gamma^2 = 1$ ——實際更新次數恰為 1。
90: 
91: ## 歷史典故
92: 
93: - 1957 年感知器誕生：見卷宗 [../1957-Perceptron感知器.md](../1957-Perceptron感知器.md)——一台用馬達和電位器組成的「會學習的機器」。
94: - 1960 年 ADALINE：見 [../1960-ADALINE自適應線性元件.md](../1960-ADALINE自適應線性元件.md)——最早被商業化的自適應濾波器，至今仍在降噪應用中活著。
95: - 1969 年的 XOR 批判：見 [../1969-MinskyPapert批判.md](../1969-MinskyPapert批判.md)——單層感知器的極限（01.1 節）成為寒冬的導火線。
96: 
97: ## 習題
98: 
99: 1. 用感知器演算法分類 $\{(2,1),+1\}, \{(-2,-1),-1\}$ ，從 $\mathbf{w}^{(0)}=\mathbf{0}$ 開始，列出每步更新。
100: 2. 證明：對收斂定理中的 $\mathbf{w}^{(k)}$ ，有 $\cos\angle(\mathbf{w}^{(k)}, \mathbf{w}^*) \ge \sqrt{k}\,\gamma / (\sqrt{k} R)$ ，並討論其極限。
101: 3. 資料不是線性可分時，感知器會怎樣？（提示：更新次數無上界，權重會震盪。）這與 01.1 的 XOR 矛盾有何關係？

(End of file - total 101 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/02.2-損失函數與梯度下降.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/02.2-損失函數與梯度下降.md</path>
<type>file</type>
<content>
1: # 02.2 損失函數與梯度下降
2: 
3: ## 本章導讀
4: 
5: 感知器只會「對錯二分」。現代深度學習換了一個更優雅的框架：
6: 把「學得好不好」寫成一個連續函數 $L(\theta)$ （損失函數），然後沿著下坡走——
7: 這就是梯度下降。所有神經網路訓練，本質上都是這一個動作的重複。
8: 
9: ## 淺顯說明
10: 
11: 想像你蒙著眼睛站在山上，想走到山谷最低點：
12: 
13: - 看不見全景，但**腳底感覺得到坡度**（梯度）。
14: - 策略：朝最陡的下坡方向跨一小步，再感覺、再跨。
15: - 步子太大會越過谷底（發散），太小走不到（收斂太慢）。
16: 
17: 數學上：「坡度」是 $\nabla L$ ，「一小步」是學習率 $\eta$ ，「走路」就是
18: $\theta \leftarrow \theta - \eta\nabla L$ 。
19: 
20: ## 正規理論
21: 
22: ### 損失函數
23: 
24: 給定模型 $f_\theta(\mathbf{x})$ 與資料集 $\{(\mathbf{x}_i, y_i)\}_{i=1}^N$ ，損失函數是經驗風險：
25: 
26: $$
27: L(\theta) = \frac{1}{N}\sum_{i=1}^N \ell(f_\theta(\mathbf{x}_i), y_i)
28: $$
29: 
30: 兩個最常用的損失：
31: 
32: - **均方誤差**（回歸）： $\ell(\hat y, y) = \frac{1}{2}(\hat y - y)^2$ 。
33: - **交叉熵**（分類）： $\ell(\hat y, y) = -\sum_k y_k \log \hat y_k$ ，其中 $\hat y_k$ 是 softmax 機率。
34: 
35: ### 梯度下降
36: 
37: 泰勒展開給出一階近似：
38: 
39: $$
40: L(\theta + \delta) \approx L(\theta) + \nabla L^\top \delta
41: $$
42: 
43: 要讓 $L$ 下降最快，取 $\delta = -\eta\,\nabla L$ （與 $\nabla L$ 反向最有效率，因 Cauchy–Schwarz）：
44: 
45: $$
46: \boxed{\;\theta \leftarrow \theta - \eta\, \nabla L(\theta)\;}
47: $$
48: 
49: ### 收斂率（凸函數情形）
50: 
51: 若 $L$ 是 $\beta$ -平滑且 $\alpha$ -強凸的，梯度下降以**線性收斂率**逼近最小值：
52: 
53: $$
54: L(\theta_k) - L(\theta^*) \;\le\; \left(1 - \frac{\alpha}{\beta}\right)^k \big(L(\theta_0) - L(\theta^*)\big)
55: $$
56: 
57: 每一步把「剩餘誤差」乘上一個小於 1 的常數。
58: 
59: ### 隨機梯度下降（SGD）
60: 
61: 資料太大時，用小批量（mini-batch）估計梯度：
62: 
63: $$
64: \theta \leftarrow \theta - \eta\, \nabla L_{\mathcal{B}}(\theta), \qquad L_{\mathcal{B}} = \frac{1}{|\mathcal{B}|}\sum_{i \in \mathcal{B}} \ell_i
65: $$
66: 
67: $\nabla L_{\mathcal{B}}$ 是 $\nabla L$ 的無偏估計： $\mathbb{E}_{\mathcal{B}}[\nabla L_{\mathcal{B}}] = \nabla L$ 。
68: 噪聲雖大，卻能幫助跳出淺的局部極小。
69: 
70: ### 動量與 Adam
71: 
72: - **動量**（Momentum）：累積歷史梯度，像滾球一樣加速：
73: 
74: $$
75: v \leftarrow \beta v + \nabla L, \qquad \theta \leftarrow \theta - \eta\, v
76: $$
77: 
78: - **Adam**：對每個參數自適應調整步長，用梯度的一、二階動量估計：
79: 
80: $$
81: m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t, \qquad
82: s_t = \beta_2 s_{t-1} + (1-\beta_2) g_t^2, \qquad
83: \theta \leftarrow \theta - \eta\, \frac{\hat m_t}{\sqrt{\hat s_t} + \epsilon}
84: $$
85: 
86: ## 簡易範例：一維拋物線
87: 
88: $L(\theta) = \theta^2$ ， $\nabla L = 2\theta$ ， $\eta = 0.1$ ， $\theta_0 = 1$ ：
89: 
90: $$
91: \theta_k = (1 - 2\eta)^k \theta_0 = 0.8^k
92: $$
93: 
94: | $k$ | 0 | 1 | 2 | 3 | 5 |
95: |---|---|---|---|---|---|
96: | $\theta_k$ | 1.000 | 0.800 | 0.640 | 0.512 | 0.328 |
97: 
98: 每步乘 $0.8$ ，正是理論預測的 $(1 - 2\eta)^k$ 。若 $\eta > 1$ ， $|1-2\eta|>1$ ，**發散**——步子太大越過谷底。
99: 
100: ## 歷史典故
101: 
102: - 1986 年反向傳播 + 梯度下降：見卷宗 [../1986-反向傳播演算法.md](../1986-反向傳播演算法.md)——Rumelhart、Hinton、Williams 讓多層網路可以訓練。
103: - 2012 年 AlexNet：見 [../2012-AlexNet影像革命.md](../2012-AlexNet影像革命.md)——GPU 上的 SGD 竟打敗了手工特徵，開啟深度學習革命。
104: - 2022 年 Chinchilla 規模法則：見 [../2022-Chinchilla規模法則.md](../2022-Chinchilla規模法則.md)——訓練多大的模型、用多少資料，由冪律決定（06.3 節）。
105: 
106: ## 習題
107: 
108: 1. 對 $L(\theta) = (\theta - 3)^2$ 套用梯度下降， $\eta = 0.25$ ，求 $\theta_k$ 的封閉式，並求收斂的最大 $\eta$ 。
109: 2. 證明：SGD 的批量梯度是全量梯度的無偏估計。
110: 3. 解釋為什麼動量可以幫助穿越狹長峽谷形的損失面（提示：垂直方向振盪互相抵消，水平方向累積加速）。

(End of file - total 110 lines)
</content>
```

---

## Assistant (Build · GLM-5.3-Flash · 37.7s)

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/03.1-活化函數與泛近似定理.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/03.1-活化函數與泛近似定理.md</path>
<type>file</type>
<content>
1: # 03.1 活化函數與泛近似定理
2: 
3: ## 本章導讀
4: 
5: XOR 告訴我們：單層網路只能切直線。要切出曲線，需要兩件事——
6: **非線性活化函數**與**多層堆疊**。
7: 1989 年，Cybenko 等人證明了一個驚人的定理：只要有一層足夠多的神經元，網路可以逼近任何連續函數。
8: 
9: ## 淺顯說明
10: 
11: 活化函數是神經元的「非線性開關」。沒有它，多層網路只是白疊：
12: 
13: $$
14: f(x) = W_2\,(W_1 x) = (W_2 W_1)\,x = W' x \quad \text{（仍是線性！）}
15: $$
16: 
17: 加了非線性 $\sigma$ ，每層之間「彎一下」，網路就能折出任意形狀——像用很多段小直線逼近曲線，
18: 像用很多塊小積木堆出雕像。
19: 
20: ## 正規理論
21: 
22: ### 常見活化函數
23: 
24: $$
25: \sigma(z) = \frac{1}{1+e^{-z}} \quad (\text{sigmoid}), \qquad
26: \tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}, \qquad
27: \mathrm{ReLU}(z) = \max(0, z)
28: $$
29: 
30: 它們的導數（反向傳播會用到）：
31: 
32: $$
33: \sigma'(z) = \sigma(z)(1 - \sigma(z)), \qquad
34: \tanh'(z) = 1 - \tanh^2(z), \qquad
35: \mathrm{ReLU}'(z) = \mathbb{1}[z > 0]
36: $$
37: 
38: sigmoid 兩端飽和時導數趨近 0（梯度消失）；ReLU 正區導數恆為 1，成為現代網路主流。
39: 
40: ### 多層前饋網路
41: 
42: 一個 $L$ 層前饋網路是複合函數：
43: 
44: $$
45: f_\theta(\mathbf{x}) = W_L\,\sigma(W_{L-1}\,\sigma(\cdots \sigma(W_1\mathbf{x})\cdots))
46: $$
47: 
48: ### 泛近似定理（Universal Approximation Theorem）
49: 
50: **定理**（Cybenko 1989 / Hornik 1991）：設 $\sigma$ 是連續的非常數活化函數，
51: $K \subset \mathbb{R}^n$ 是緊緻集， $g: K \to \mathbb{R}$ 是連續函數。
52: 則對任意 $\varepsilon > 0$ ，存在單隱藏層網路
53: 
54: $$
55: f(\mathbf{x}) = \sum_{j=1}^{M} \alpha_j\, \sigma(\mathbf{w}_j^\top \mathbf{x} + b_j)
56: $$
57: 
58: 使得 $\sup_{\mathbf{x} \in K} |f(\mathbf{x}) - g(\mathbf{x})| < \varepsilon$ 。
59: 
60: **意義**：單層網路在數學上「表達能力無限」。但注意——定理不保證：
61: (1) $M$ 有多大（可能是指數級）；(2) 權重學不學得到。
62: 深度學習的賭注是：**深而窄**比**淺而寬**更容易訓練、更省參數。
63: 
64: ### 為什麼「深」勝過「寬」
65: 
66: 對某些函數（如鋸齒函數的複合），深網路只需 $O(\text{poly})$ 個神經元，
67: 淺網路卻需要指數個——深度帶來**複合的指數效率**，這是 ResNet 等深結構的理論根據。
68: 
69: ## 簡易範例：用兩個神經元折出「階梯」
70: 
71: 取 $\sigma = \mathrm{ReLU}$ ，考慮
72: 
73: $$
74: f(x) = \mathrm{ReLU}(x) - \mathrm{ReLU}(x - 1)
75: $$
76: 
77: - $x < 0$ ：兩項皆 0， $f = 0$ 。
78: - $0 \le x < 1$ ： $f = x$ 。
79: - $x \ge 1$ ： $f = x - (x-1) = 1$ 。
80: 
81: 兩個神經元就折出一個「斜坡加平台」。堆 $2M$ 個 ReLU，就能折出 $M$ 段的階梯；
82: $M \to \infty$ 時逼近任何連續函數——這就是泛近似定理的直覺核心。
83: 
84: ## 歷史典故
85: 
86: - 1986 年反向傳播：見卷宗 [../1986-反向傳播演算法.md](../1986-反向傳播演算法.md)——讓深網路的權重「學得到」的引擎（下一節細講）。
87: - 1989 年 LeCun 的 CNN：見 [../1989-LeCunCNN手寫辨識.md](../1989-LeCunCNN手寫辨識.md)——泛近似的結構化版本：用摺積先驗取代任意函數。
88: - 2015 年 ResNet：見 [../2015-ResNet殘差網路.md](../2015-ResNet殘差網路.md)——152 層網路終於訓得動，深度的複合效率成為主流。
89: 
90: ## 習題
91: 
92: 1. 用 ReLU 神經元表達 $f(x) = |x|$ （提示： $\mathrm{ReLU}(x) + \mathrm{ReLU}(-x)$ ）。
93: 2. 證明：不含活化函數的多層線性網路等價於單層線性網路。
94: 3. sigmoid 在 $|z| > 10$ 時導數約多少？說明這如何導致深網路的「梯度消失」問題。

(End of file - total 94 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/03.2-反向傳播演算法.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/03.2-反向傳播演算法.md</path>
<type>file</type>
<content>
1: # 03.2 反向傳播演算法
2: 
3: ## 本章導讀
4: 
5: 泛近似定理說「學得到」的函數存在，但沒說**怎麼找**。
6: 答案是微積分裡最古老的一行公式——鏈鎖律——配上聰明的計算順序。
7: 反向傳播（Backpropagation）不是新理論，而是鏈鎖律的動態規劃：**每個參數只算一次**。
8: 
9: ## 淺顯說明
10: 
11: 想像一條工廠生產線：原料（輸入）→ 組裝 → 品檢 → 出貨（輸出）。
12: 出貨品質不合格（損失很大），要追責任：
13: 
14: - **前向**：順著生產線算出輸出與損失。
15: - **反向**：從損失往回走，把「責任」（梯度）一層層分回去——
16:   離損失越近的工序，責任越大；每一站的責任 = 上游責任 × 本站敏感度。
17: 
18: 關鍵省力技巧：先用前向把每站的中間結果存起來，回程直接查表乘一乘——
19: 否則每個參數都要重跑整條生產線，計算量會爆炸。
20: 
21: ## 正規理論
22: 
23: ### 問題設定
24: 
25: $L$ 層前饋網路：
26: 
27: $$
28: \mathbf{a}^{(0)} = \mathbf{x}, \qquad
29: \mathbf{z}^{(l)} = W^{(l)} \mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}, \qquad
30: \mathbf{a}^{(l)} = \sigma(\mathbf{z}^{(l)}), \qquad
31: L = \ell(\mathbf{a}^{(L)}, y)
32: $$
33: 
34: 目標：計算 $\dfrac{\partial L}{\partial W^{(l)}}$ （所有層）。
35: 
36: ### 鏈鎖律與誤差項
37: 
38: 定義第 $l$ 層的**誤差向量**：
39: 
40: $$
41: \boldsymbol{\delta}^{(l)} = \frac{\partial L}{\partial \mathbf{z}^{(l)}} \in \mathbb{R}^{n_l}
42: $$
43: 
44: **反向遞推**（鏈鎖律的核心）：
45: 
46: $$
47: \boldsymbol{\delta}^{(L)} = \nabla_{\mathbf{a}^{(L)}} \ell \odot \sigma'(\mathbf{z}^{(L)}), \qquad
48: \boldsymbol{\delta}^{(l)} = \left( W^{(l+1)\top} \boldsymbol{\delta}^{(l+1)} \right) \odot \sigma'(\mathbf{z}^{(l)})
49: $$
50: 
51: 其中 $\odot$ 是逐元素乘（Hadamard 積）。梯度：
52: 
53: $$
54: \boxed{\;
55: \frac{\partial L}{\partial W^{(l)}} = \boldsymbol{\delta}^{(l)} \, \mathbf{a}^{(l-1)\top}, \qquad
56: \frac{\partial L}{\partial \mathbf{b}^{(l)}} = \boldsymbol{\delta}^{(l)}
57: \;}
58: $$
59: 
60: ### 推導
61: 
62: 對單一權重 $W^{(l)}_{ij}$ （連接 $a^{(l-1)}_j$ 到 $z^{(l)}_i$ ）， $z^{(l)}_i = \sum_k W^{(l)}_{ik} a^{(l-1)}_k + b^{(l)}_i$ 直接偏導得
63: $\partial z^{(l)}_i / \partial W^{(l)}_{ij} = a^{(l-1)}_j$ ，故
64: 
65: $$
66: \frac{\partial L}{\partial W^{(l)}_{ij}} = \frac{\partial L}{\partial z^{(l)}_i}\cdot\frac{\partial z^{(l)}_i}{\partial W^{(l)}_{ij}} = \delta^{(l)}_i\, a^{(l-1)}_j
67: $$
68: 
69: 而 $\boldsymbol{\delta}^{(l)}$ 的遞推由鏈鎖律：
70: 
71: $$
72: \delta^{(l)}_j = \frac{\partial L}{\partial z^{(l)}_j}
73: = \sum_i \frac{\partial L}{\partial z^{(l+1)}_i}\frac{\partial z^{(l+1)}_i}{\partial a^{(l)}_j}\frac{\partial a^{(l)}_j}{\partial z^{(l)}_j}
74: = \sum_i \delta^{(l+1)}_i W^{(l+1)}_{ij}\, \sigma'(z^{(l)}_j)
75: $$
76: 
77: ### 計算複雜度
78: 
79: 反向傳播把梯度計算從 $O(P \cdot F)$ （ $P$ 個參數、每次前向 $F$ ）降到**與前向同階**：
80: 總計算量約為前向的 2–3 倍。這是自動微分「反向模式」的特例——
81: **一個輸出、多個輸入時，反向模式壓倒性地快**，而神經網路訓練恰好就是這種情形（損失是唯一輸出）。
82: 
83: ### 自動微分
84: 
85: 現代框架（PyTorch/JAX）把每個基本運算記錄成計算圖，自動執行上述過程：
86: 
87: $$
88: \frac{\partial L}{\partial v} = \sum_{u \in \mathrm{children}(v)} \frac{\partial L}{\partial u}\, \frac{\partial u}{\partial v}
89: $$
90: 
91: Diff-Physics 等可微物理引擎更讓梯度**穿透物理模擬**流動（08.1 節）。
92: 
93: ## 簡易範例：兩層網路手算
94: 
95: 網路： $z^{(1)} = w_1 x$ ， $a^{(1)} = \sigma(z^{(1)})$ ， $z^{(2)} = w_2 a^{(1)}$ ， $L = \frac{1}{2}(z^{(2)} - y)^2$ 。
96: 取 $x = 1$ ， $w_1 = 1$ ， $w_2 = 1$ ， $y = 0$ ， $\sigma = \tanh$ 。
97: 
98: **前向**： $z^{(1)} = 1$ ， $a^{(1)} = \tanh 1 \approx 0.7616$ ， $z^{(2)} = 0.7616$ ， $L \approx 0.290$ 。
99: 
100: **反向**：
101: 
102: $$
103: \delta^{(2)} = \frac{\partial L}{\partial z^{(2)}} = z^{(2)} - y \approx 0.7616
104: $$
105: 
106: $$
107: \delta^{(1)} = w_2\,\delta^{(2)} \cdot \tanh'(z^{(1)}) = 1 \times 0.7616 \times (1 - 0.7616^2) \approx 0.3208
108: $$
109: 
110: **梯度**：
111: 
112: $$
113: \frac{\partial L}{\partial w_2} = \delta^{(2)}\, a^{(1)} \approx 0.580, \qquad
114: \frac{\partial L}{\partial w_1} = \delta^{(1)}\, x \approx 0.321
115: $$
116: 
117: 用 $\eta = 0.5$ 更新後 $L$ 立即下降——誤差自己教了網路。
118: 
119: ## 歷史典故
120: 
121: - 1974 年 Werbos 的先驅工作：見卷宗 [../1974-Werbos反向傳播先驅.md](../1974-Werbos反向傳播先驅.md)——博士論文裡的鏈鎖律，早了 12 年無人問津。
122: - 1986 年反向傳播演算法：見 [../1986-反向傳播演算法.md](../1986-反向傳播演算法.md)——Rumelhart、Hinton、Williams 的 Nature 論文，讓寒冬結束。
123: 
124: ## 習題
125: 
126: 1. 對上例多算一步：更新後的 $w_1, w_2$ 與新的 $L$ ，驗證損失下降。
127: 2. 證明：對 softmax 輸出加交叉熵損失， $\boldsymbol{\delta}^{(L)} = \hat{\mathbf{y}} - \mathbf{y}$ （形式極簡）。
128: 3. 若網路有 10 個輸出與 1 個輸入，前向模式與反向模式自動微分哪個快？為什麼？

(End of file - total 128 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/04.1-Hopfield網路與能量函數.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/04.1-Hopfield網路與能量函數.md</path>
<type>file</type>
<content>
1: # 04.1 Hopfield 網路與能量函數
2: 
3: ## 本章導讀
4: 
5: 1982 年，物理學家 John Hopfield 把統計物理的工具帶進神經網路：
6: 給網路一個「能量函數」，讓回憶變成「滾下山谷」。
7: 這是深度學習史上第一次，智慧被寫成能量——物理與神經科學在此合流。
8: 
9: ## 淺顯說明
10: 
11: 想像一片有許多窪地的地形，每個窪地是一段「記憶」：
12: 
13: - 把殘缺的模式丟進地形，小球會滾進最近的窪地——記憶被「吸」回來。
14: - 滾動的規則：每次翻轉一個讓能量下降的神經元。
15: - 窪地的位置由權重矩陣（Hebb 律，01.2 節）決定。
16: 
17: 物理裡這叫「滾向局部極小」，神經科學裡叫「聯想回憶」，數學裡叫「梯度流」。
18: 
19: ## 正規理論
20: 
21: ### 網路結構
22: 
23: Hopfield 網路是全連接、對稱權重、無自環的網路：
24: 
25: $$
26: W = W^\top, \qquad W_{ii} = 0, \qquad s_i \in \{-1, +1\}
27: $$
28: 
29: 狀態更新（非同步、逐一神經元）：
30: 
31: $$
32: s_i \leftarrow \mathrm{sgn}\!\left(\sum_j W_{ij} s_j\right)
33: $$
34: 
35: ### 能量函數
36: 
37: 定義能量：
38: 
39: $$
40: E(\mathbf{s}) = -\frac{1}{2}\sum_{i \ne j} W_{ij} s_i s_j = -\frac{1}{2}\,\mathbf{s}^\top W \mathbf{s}
41: $$
42: 
43: ### 能量單調下降定理
44: 
45: **定理**：在非同步更新下，只要翻轉的 $s_i$ 真的改變了狀態，能量嚴格下降。
46: 
47: **證明**：翻轉 $s_i \to -s_i$ 只有含 $i$ 的項改變。局部場 $h_i = \sum_j W_{ij}s_j$ ，
48: 能量改變量為
49: 
50: $$
51: \Delta E = -\sum_j W_{ij}(-s_i - s_i)s_j = 2 s_i \sum_j W_{ij} s_j = 2 s_i h_i
52: $$
53: 
54: 而 $\mathrm{sgn}(h_i) \ne s_i$ 時（真的翻轉）， $s_i h_i < 0$ ，故 $\Delta E < 0$ 。 $\blacksquare$
55: 
56: 因為狀態有限（ $2^n$ 個）且能量單調下降，網路**必在有限步內收斂到能量局部極小**——記憶吸子。
57: 
58: ### 記憶儲存（Hebb 律）
59: 
60: 儲存模式 $\{\mathbf{x}^{(\mu)}\}$ ， $\mathbf{x}^{(\mu)} \in \{-1,+1\}^n$ ：
61: 
62: $$
63: W_{ij} = \frac{1}{n}\sum_{\mu} x^{(\mu)}_i x^{(\mu)}_j
64: $$
65: 
66: 代入可驗證每個模式是能量極小： $\mathbf{s} = \mathbf{x}^{(\nu)}$ 時局部場
67: $h_i = \sum_j W_{ij} x^{(\nu)}_j \approx x^{(\nu)}_i$ （正交性消去雜訊），sgn 回原狀態，能量是局部谷底。
68: 
69: ### 與物理的對應
70: 
71: | 統計物理 | Hopfield 網路 |
72: |---|---|
73: | 自旋玻璃 Ising 模型 $E = -\sum J_{ij}s_is_j$ | 能量函數 |
74: | 相變與亞穩態 | 記憶吸子 |
75: | 能量景觀 | 聯想記憶 |
76: 
77: ## 簡易範例：單步回憶
78: 
79: 沿用 01.2 的例子：儲存 $\mathbf{x}^{(1)} = (1,1,-1)$ 、 $\mathbf{x}^{(2)} = (-1,1,1)$ ，
80: 
81: $$
82: W = \frac{1}{3}\begin{pmatrix} 0 & 0 & -2 \\ 0 & 0 & 0 \\ -2 & 0 & 0 \end{pmatrix}
83: $$
84: 
85: 輸入殘缺 $\mathbf{s}^{(0)} = (1, 1, -1)^\top$ ，逐項檢查：
86: 
87: - $i=1$ ： $h_1 = W_{13}\cdot(-1) = \tfrac{2}{3} > 0$ ，sgn = $+1$ ，不翻。
88: - $i=2$ ： $h_2 = 0$ ，sgn = $+1$ ，不翻。
89: - $i=3$ ： $h_3 = W_{31}\cdot 1 = -\tfrac{2}{3} < 0$ ，sgn = $-1$ ，不翻。
90: 
91: 狀態已穩定—— $\mathbf{x}^{(1)}$ 是能量極小，網路「記住」了它。若輸入 $(-1,-1,1)$ （模式一的取反），
92: 同樣穩定——**模式與其反轉都會被儲存**（這是 Hopfield 網路的已知特性）。
93: 
94: ## 歷史典故
95: 
96: - 1982 年 Hopfield 網路：見卷宗 [../1982-Hopfield網路能量函數.md](../1982-Hopfield網路能量函數.md)——諾貝爾獎得主把自旋玻璃變成會回憶的機器。
97: - 1949 年 Hebb 律是其權重的來源：見 [../1949-Hebb學習規則.md](../1949-Hebb學習規則.md)。
98: - 1985 年 Boltzmann 機器：見 [../1985-Boltzmann機器.md](../1985-Boltzmann機器.md)——Hopfield 的學生加上「溫度」，讓能量景觀可以探樣（下一節）。
99: - 2024 年的現代復興：見 [../2024-VJEPA世界模型.md](../2024-VJEPA世界模型.md)——能量式學習思想在自監督世界模型中重現（08.2 節）。
100: 
101: ## 習題
102: 
103: 1. 證明：同步（全體同時）更新可能產生 2-週期震盪，不保證收斂——為什麼非同步更新避開了這個問題。
104: 2. 對本節例題計算 $\mathbf{x}^{(1)}$ 與 $\mathbf{x}^{(2)}$ 的能量，確認它們都是局部極小。
105: 3. 討論：能量函數方法與梯度下降（02.2 節）有何異同？（提示：一個在離散狀態空間、一個在連續參數空間。）

(End of file - total 105 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/04.2-Boltzmann機器與softmax.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/04.2-Boltzmann機器與softmax.md</path>
<type>file</type>
<content>
1: # 04.2 Boltzmann 機器與 softmax
2: 
3: ## 本章導讀
4: 
5: Hopfield 網路有個問題：它總是「確定地」滾進窪地，學到的分布太僵硬。
6: 1985 年，Hinton 與 Sejnowski 加上一味調味料——**溫度**。
7: 有溫度，確定性變成機率；能量景觀變成機率分布；回憶變成「生成」。生成式 AI 就從這裡開始。
8: 
9: ## 淺顯說明
10: 
11: 溫度讓小球不再老老實實滾下坡：
12: 
13: - 溫度高：小球亂跳，什麼窪地都去——探索。
14: - 溫度低：小球乖乖滾下坡——收斂。
15: - 中間溫度：小球「大致」待在低處，偶爾跳一下——這是熱平衡。
16: 
17: 把溫度調到 0，就回到 Hopfield；溫度不為 0，每個狀態都有出現機率，
18: 機率與能量由一條物理公式綁定： $P \propto e^{-E/T}$ 。
19: 今天所有語言模型的 softmax，都是這條公式的直系後代。
20: 
21: ## 正規理論
22: 
23: ### Gibbs 分布
24: 
25: 給定能量函數 $E(\mathbf{s})$ 與溫度 $T$ ，Boltzmann 機器定義狀態機率：
26: 
27: $$
28: P(\mathbf{s}) = \frac{1}{Z}\, e^{-E(\mathbf{s})/T}, \qquad
29: Z = \sum_{\mathbf{s}'} e^{-E(\mathbf{s}')/T}
30: $$
31: 
32: $Z$ 是配分函數（歸一化常數）。能量越低，機率越高；溫度 $T \to 0$ 時機率集中在最低能態， $T \to \infty$ 時趨於均勻。
33: 
34: ### 狀態更新：Gibbs 採樣
35: 
36: 神經元 $i$ 在其局部場 $h_i = \sum_j W_{ij}s_j$ 條件下放電的機率：
37: 
38: $$
39: P(s_i = 1 \mid \mathbf{s}_{-i}) = \sigma\!\left(\frac{h_i}{T}\right) = \frac{1}{1 + e^{-h_i/T}}
40: $$
41: 
42: 重複採樣，狀態分布收斂到 Gibbs 分布——這是馬可夫鏈蒙地卡羅（MCMC）的應用。
43: 
44: ### softmax：溫度公式的多類版
45: 
46: 把單一神經元推廣到 $K$ 類。給定 logits $\mathbf{z}$ ，softmax 定義：
47: 
48: $$
49: \mathrm{softmax}(\mathbf{z})_k = \frac{e^{z_k / T}}{\sum_{k'} e^{z_k' / T}}
50: $$
51: 
52: 這正是 Gibbs 分布離散形式：logits 是「負能量」，softmax 是「有溫度的歸一化」。
53: 語言模型生成時的溫度參數（ $T = 0$ 貪心、 $T > 0$ 採樣），就是這條公式。
54: 
55: ### 學習：最大化對數概似
56: 
57: 訓練目標是讓資料的對數概似最大：
58: 
59: $$
60: \max_W \; \sum_{\mu} \log P(\mathbf{x}^{(\mu)}; W) = \sum_\mu \left[ -\frac{E(\mathbf{x}^{(\mu)})}{T} - \log Z \right]
61: $$
62: 
63: 對 $W$ 求梯度（ $T = 1$ 記）：
64: 
65: $$
66: \frac{\partial \log P}{\partial W_{ij}} = \underbrace{\langle s_i s_j \rangle_{\text{data}}}_{\text{資料驅動}} - \underbrace{\langle s_i s_j \rangle_{\text{model}}}_{\text{模型期望}}
67: $$
68: 
69: **意義**：學習 = 讓「資料裡一起放電的頻率」等於「模型裡一起放電的頻率」——Hebb 律（正項）減去「夢裡的 Hebb 律」（負項）。 $\log Z$ 需要對模型分布採樣，這是最困難的部分。
70: 
71: ### 受限波茲曼機（RBM）
72: 
73: 把連接限制為「可見層—隱藏層」二部圖，採樣可分層進行（block Gibbs）， $Z$ 的估計變得可行：
74: 
75: $$
76: P(\mathbf{v}, \mathbf{h}) = \frac{1}{Z} e^{-E(\mathbf{v}, \mathbf{h})}, \qquad E(\mathbf{v}, \mathbf{h}) = -\mathbf{v}^\top W \mathbf{h} - \mathbf{b}^\top\mathbf{v} - \mathbf{c}^\top\mathbf{h}
77: $$
78: 
79: 2006 年 Hinton 用層疊 RBM（深度信念網路）預訓練深網路，開啟深度學習時代。
80: 
81: ## 簡易範例：兩狀態溫度
82: 
83: 狀態 $s \in \{+1, -1\}$ ，能量 $E(+1) = 0$ ， $E(-1) = 4$ 。
84: 
85: - $T = 1$ ： $P(+1) = \dfrac{e^0}{e^0 + e^{-4}} \approx 0.982$ ， $P(-1) \approx 0.018$ （低溫，集中在低能態）。
86: - $T = 2$ ： $P(+1) = \dfrac{1}{1 + e^{-2}} \approx 0.881$ 。
87: - $T \to \infty$ ： $P(+1) \to 0.5$ （高溫，趨於均勻）。
88: 
89: 溫度就是「探索 vs 收斂」的旋鈕——語言模型的 temperature 參數完全同構。
90: 
91: ## 歷史典故
92: 
93: - 1985 年 Boltzmann 機器：見卷宗 [../1985-Boltzmann機器.md](../1985-Boltzmann機器.md)——Hinton 用物理的溫度，讓網路學會「做夢」。
94: - 2006 年深度信念網路：見 [../2006-Hinton深度信念網路.md](../2006-Hinton深度信念網路.md)——層疊 RBM 預訓練，深度學習的起點。
95: - 2022 年 ChatGPT 與 RLHF：見 [../2022-ChatGPT與RLHF.md](../2022-ChatGPT與RLHF.md)——softmax 採樣 + 溫度，成為人機對話的介面（07 章細講 RL 部分）。
96: 
97: ## 習題
98: 
99: 1. 證明：Gibbs 條件機率 $P(s_i = 1 \mid \mathbf{s}_{-i}) = \sigma(h_i)$ （取 $T=1$ ）。
100: 2. 對兩狀態例子求 $P(+1) = 0.99$ 所需的溫度 $T$ 。
101: 3. 解釋學習梯度的「data 減 model」兩項各對應 Hebb 律的哪個部分，以及為什麼負項需要採樣。

(End of file - total 101 lines)
</content>
```

---

## Assistant (Build · GLM-5.3-Flash · 27.8s)

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/04.3-熵KL散度與資訊理論.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/04.3-熵KL散度與資訊理論.md</path>
<type>file</type>
<content>
1: # 04.3 熵、KL 散度與資訊理論
2: 
3: ## 本章導讀
4: 
5: 前兩節把「智慧」寫成能量。1948 年，Shannon 換了一個更普適的度量——**資訊**。
6: 資訊論給了現代 AI 三件武器：量測不確定性的熵、訓練用的交叉熵損失、
7: 以及比較兩個分布的 KL 散度。LLM 的困惑度、RL 的策略約束，全是這一章的應用。
8: 
9: ## 淺顯說明
10: 
11: - **熵**：一枚公正硬幣的結果「最難猜」（熵 = 1 bit）；一枚兩面都是正面的硬幣「零資訊」（熵 = 0）。
12: - **交叉熵**：你用錯誤的機率去猜，平均要多花的「驚訝量」。
13: - **KL 散度**：兩個機率分布的「距離」——但它是單向的、非負的、可為無窮。
14: 
15: 訓練語言模型 = 最小化交叉熵；對齊模型行為 = 限制 KL 散度。三個量，一個家族。
16: 
17: ## 正規理論
18: 
19: ### Shannon 熵
20: 
21: 離散分布 $p(x)$ 的熵：
22: 
23: $$
24: H(p) = -\sum_x p(x)\log p(x) \quad (\text{bit 時取 } \log_2)
25: $$
26: 
27: **性質**： $H \ge 0$ ，且均勻分布時最大： $H = \log n$ （ $n$ 個等機率結果）。
28: 
29: ### 交叉熵與 KL 散度
30: 
31: 用分布 $q$ 編碼真實分布 $p$ 的平均描述長度：
32: 
33: $$
34: H(p, q) = -\sum_x p(x)\log q(x)
35: $$
36: 
37: KL 散度定義：
38: 
39: $$
40: \boxed{\;
41: D_{\mathrm{KL}}(p \,\|\, q) = \sum_x p(x)\log\frac{p(x)}{q(x)} = H(p,q) - H(p)
42: \;}
43: $$
44: 
45: **Gibbs 不等式**： $D_{\mathrm{KL}}(p\|q) \ge 0$ ，等號成立 iff $p = q$ 。
46: 
47: **證明**：對任意 $x > 0$ 有 $\log x \le x - 1$ （ $\log$ 的凹性、切線在 $x=1$ ）。故
48: 
49: $$
50: -D_{\mathrm{KL}}(p\|q) = \sum_x p(x)\log\frac{q(x)}{p(x)} \le \sum_x p(x)\left(\frac{q(x)}{p(x)} - 1\right) = \sum_x q(x) - \sum_x p(x) = 0 \qquad \blacksquare
51: $$
52: 
53: **意義**：交叉熵損失最小化 $\Leftrightarrow$ KL 散度最小化 $\Leftrightarrow$ 讓模型分布貼近資料分布。
54: 因為 $H(p,q) = D_{\mathrm{KL}}(p\|q) + H(p)$ ，而真實資料的熵 $H(p)$ 是常數。
55: 
56: ### 連續情形與變分推斷
57: 
58: 連續分布： $D_{\mathrm{KL}}(p\|q) = \int p(x)\log\frac{p(x)}{q(x)}\,dx$ 。
59: 
60: 變分自編碼器（VAE, 2013）的損失正是 KL 散度的應用——用簡單的 $q$ 近似難算的後驗 $p$ ：
61: 
62: $$
63: \mathcal{L} = \mathbb{E}_{q}[\underbrace{-\log p(x|z)}_{\text{重建}}] + \underbrace{D_{\mathrm{KL}}(q(z|x)\,\|\,p(z))}_{\text{正則化}}
64: $$
65: 
66: H-JEPA 等自監督世界模型也用 KL／協方差正則化防止隱空間維度崩潰（08.2 節）。
67: 
68: ### 應用一覽
69: 
70: | 應用 | 公式 | 角色 |
71: |---|---|---|
72: | LLM 訓練 | 交叉熵 $-\log P(w_t \mid w_{<t})$ | 損失 |
73: | LLM 評測 | 困惑度 $\mathrm{PPL} = e^{H(p,q)}$ | 生成的不確定性 |
74: | RL (PPO/TRPO) | $D_{\mathrm{KL}}(\pi_{\text{new}}\|\pi_{\text{old}}) \le \delta$ | 限制策略更新步長 |
75: | 蒸餾 | $D_{\mathrm{KL}}(\text{teacher}\|\text{student})$ | 知識轉移 |
76: 
77: ## 簡易範例：硬幣與困惑度
78: 
79: 公正硬幣 $p = (0.5, 0.5)$ ，你的模型 $q = (0.9, 0.1)$ ：
80: 
81: $$
82: H(p,q) = -0.5\log_2 0.9 - 0.5\log_2 0.1 \approx 0.074 + 1.661 = 1.735 \text{ bit}
83: $$
84: 
85: $$
86: D_{\mathrm{KL}}(p\|q) = 1.735 - H(p) = 1.735 - 1 = 0.735 \text{ bit}
87: $$
88: 
89: 你因為過度自信（ $q = 0.9$ ），每次猜硬幣平均多花 0.735 bit 的「驚訝」。
90: 
91: 語言模型的困惑度：若交叉熵 $H(p,q) = 2$ nat，則 $\mathrm{PPL} = e^2 \approx 7.39$ ——
92: 模型在每一步「等 unsure 到」7.4 個詞選項。
93: 
94: ## 歷史典故
95: 
96: - 1948 年 Shannon 的資訊論雖不在本卷宗年表中，但其思想貫穿整個 AI 史——從 1957 年感知器的損失到 2017 年 Transformer 的 softmax。
97: - 2013 年 VAE：見卷宗 [../2013-VAE變分自編碼器.md](../2013-VAE變分自編碼器.md)——KL 散度成為生成模型的核心正則化。
98: - 2013 年 word2vec：見 [../2013-word2vec詞向量.md](../2013-word2vec詞向量.md)——用 softmax 交叉熵學出語義空間（06.1 節）。
99: - 2022 年 RLHF：見 [../2022-ChatGPT與RLHF.md](../2022-ChatGPT與RLHF.md)——KL 散度限制策略漂移，成為對齊技術的支柱。
100: 
101: ## 習題
102: 
103: 1. 證明均勻分布的熵最大： $H(p) \le \log n$ （提示：對 $p = 1/n$ 用 Gibbs 不等式）。
104: 2. 計算 $D_{\mathrm{KL}}(q\|p)$ （反向），與 $D_{\mathrm{KL}}(p\|q) = 0.735$ 比較——驗證 KL 散度不對稱。
105: 3. 說明為什麼「最小化交叉熵」與「最大化對數概似」在訓練中是同一件事。

(End of file - total 105 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/05.1-CNN與權重共享.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/05.1-CNN與權重共享.md</path>
<type>file</type>
<content>
1: # 05.1 CNN 與權重共享
2: 
3: ## 本章導讀
4: 
5: 全連接網路看一張 $224\times224$ 的圖片，第一層就要 $224^2$ 個權重——太浪費。
6: 1989 年，LeCun 觀察到圖片有一個天然的數學結構：**平移對稱**。
7: 貓在圖片左上角和右下角都是貓。把這個對稱「寫進」網路結構，就是卷積神經網路（CNN）。
8: 
9: ## 淺顯說明
10: 
11: 全連接像「每個像素派一個專門偵測員」；CNN 像「一個偵測員拿著濾片在整張圖上掃描」：
12: 
13: - 濾片（kernel）很小，例如 $3 \times 3$ ，只有 9 個權重。
14: - 這 9 個權重在整張圖上**共享**——左上角掃到的邊、右下角掃到的邊，用同一組權重。
15: - 濾片滑過的地方輸出一個數字：「這裡有沒有我偵測的模式」。
16: 
17: 權重共享 = 參數大幅減少 + 平移等變性。這是「把對稱性寫進架構」的第一課。
18: 
19: ## 正規理論
20: 
21: ### 離散二維卷積
22: 
23: 影像 $I$ 與卷積核 $K$ 的（數學）卷積：
24: 
25: $$
26: (I * K)(x, y) = \sum_{m}\sum_{n} I(x - m, y - n)\, K(m, n)
27: $$
28: 
29: 深度學習框架實際用的是**互相關**（cross-correlation），核不翻轉：
30: 
31: $$
32: (I \star K)(x, y) = \sum_{m=0}^{k-1}\sum_{n=0}^{k-1} I(x + m, y + n)\, K(m, n)
33: $$
34: 
35: 兩者等價（學習時核是否翻轉不影響表達能力）。多通道輸入 $C_{\text{in}}$ 、多個濾片 $C_{\text{out}}$ ：
36: 
37: $$
38: O_{j}(x,y) = \phi\!\left(\sum_{c=1}^{C_{\text{in}}} (I_c \star K_{cj})(x,y) + b_j\right)
39: $$
40: 
41: ### 平移等變性與群論觀點
42: 
43: 設平移算子 $(T_{\mathbf{v}} I)(\mathbf{x}) = I(\mathbf{x} - \mathbf{v})$ ，平移構成群 $\mathbb{R}^2$ （更精確地，圖像的離散平移群 $\subset SE(2)$ 的離散子群）。卷積與平移**可交換**：
44: 
45: $$
46: T_{\mathbf{v}}(I * K) = (T_{\mathbf{v}} I) * K
47: $$
48: 
49: **證明**： $(T_{\mathbf{v}}(I*K))(x,y) = (I*K)(x - v_x, y - v_y) = \sum_{m,n} I(x - v_x - m, y - v_y - n)K(m,n) = ((T_{\mathbf{v}}I)*K)(x,y)$ 。 $\blacksquare$
50: 
51: **意義**：
52: - **等變性**：輸入平移 → 特徵圖同樣平移。特徵出現在何處，都會被同一濾片捕捉。
53: - **不變性**：池化（pooling）把等變性進一步壓成不變性——平移後輸出（大致）不變：
54: 
55: $$
56: \mathrm{pool}(T_{\mathbf{v}} F) \approx \mathrm{pool}(F)
57: $$
58: 
59: - 這是「架構先驗」思想的典範：把已知對稱群寫進結構，學習只在剩餘自由度上進行。
60: 
61: ### 感受野與層疊
62: 
63: $k \times k$ 濾片、步距 $s$ 、 $l$ 層後的感受野半徑約為 $1 + \sum (k-1)s$ 。
64: 層疊小濾片比一個大濾片更省參數、更多非線性（兩層 $3\times3$ 感受野 $5\times5$ ，參數 $18 < 25$ ）。
65: 
66: ### 從 PCA 到摺積
67: 
68: 圖像統計的兩個經驗事實支撐 CNN：
69: 1. 局部相關性：相鄰像素高度相關（局部性 → 小濾片）。
70: 2. 統計平移不變：邊緣/紋理的統計在何處都相似（平移對稱 → 權重共享）。
71: 最早的主成分分析（PCA）顯示自然影像的主要成分正是局部邊緣濾片——CNN 的濾片在學什麼，PCA 早已預言。
72: 
73: ## 簡易範例：手算 $3\times3$ 摺積
74: 
75: 影像與邊緣濾片：
76: 
77: $$
78: I = \begin{pmatrix} 1 & 0 & 0 \\ 1 & 0 & 0 \\ 1 & 0 & 0 \end{pmatrix}, \qquad
79: K = \begin{pmatrix} 1 & -1 \\ 1 & -1 \end{pmatrix}
80: $$
81: 
82: 輸出（步距 1）：
83: 
84: - $(0,0)$ ： $1\cdot1 + 0\cdot(-1) + 1\cdot1 + 0\cdot(-1) = 2$
85: - $(0,1)$ ： $0\cdot1 + 0\cdot(-1) + 0\cdot1 + 0\cdot(-1) = 0$
86: - $(1,0)$ ： $2$ ， $(1,1)$ ： $0$
87: 
88: $$
89: O = \begin{pmatrix} 2 & 0 \\ 2 & 0 \end{pmatrix}
90: $$
91: 
92: 垂直邊的位置輸出大——濾片偵測到了邊緣。若把邊移到右邊， $O$ 的大值也移到右邊——平移等變性。
93: 
94: ## 歷史典故
95: 
96: - 1989 年 LeCun 的 CNN：見卷宗 [../1989-LeCunCNN手寫辨識.md](../1989-LeCunCNN手寫辨識.md)——用權重共享讀出手寫郵遞區號，銀行系統用了一二十年。
97: - 1980 年 Neocognitron：見 [../1980-Neocognitron視覺層級模型.md](../1980-Neocognitron視覺層級模型.md)——福島邦彥的視覺層級模型，CNN 的直接前身。
98: - 2012 年 AlexNet：見 [../2012-AlexNet影像革命.md](../2012-AlexNet影像革命.md)——GPU + ImageNet 讓 CNN 一戰成名。
99: 
100: ## 習題
101: 
102: 1. 對本節例題，把影像改為 $I(x,y)$ 的水平邊（上半 1、下半 0），計算輸出。
103: 2. 證明：兩層 $3\times3$ 摺積（步距 1）的感受野是 $5\times5$ ，參數 $18$ 個；一層 $5\times5$ 需 $25$ 個。
104: 3. 討論：旋轉對稱時，卷積還等變嗎？需要什麼修正？（提示：群論的 group equivariant CNN。）

(End of file - total 104 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/05.2-注意力機制與Transformer.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/05.2-注意力機制與Transformer.md</path>
<type>file</type>
<content>
1: # 05.2 注意力機制與 Transformer
2: 
3: ## 本章導讀
4: 
5: CNN 靠「局部掃描」看圖；語言的結構卻是「全圖關聯」——一個代詞可能指向二十句之前的主語。
6: 2017 年，Transformer 用一個公式解決了這個問題：**注意力**。
7: 它讓每個詞直接「看」所有其他詞，並動態決定該看誰多一點。
8: 
9: ## 淺顯說明
10: 
11: 想像一群人在開會，每人發言前要先「聽」其他人：
12: 
13: - 每人有一個**提問**（Query）：「我想知道什麼？」
14: - 每人有一個**名片**（Key）：「我能回答什麼？」
15: - 每人有一個**內容**（Value）：「我實際能提供的訊息。」
16: 
17: 提問和名片做點積（「我們相關嗎？」），經 softmax 歸一化成權重，再加權匯總大家的內容。
18: 沒有固定連線、沒有掃描順序——關聯是**動態計算**出來的。
19: 
20: ## 正規理論
21: 
22: ### Scaled Dot-Product Attention
23: 
24: 給定查詢 $Q$ 、鍵 $K$ 、值 $V$ （皆為矩陣，列是各詞的向量）：
25: 
26: $$
27: \boxed{\;
28: \mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right) V
29: \;}
30: $$
31: 
32: 分解成三步：
33: 
34: 1. **相似度**： $QK^\top$ 的 $(i,j)$ 元素是第 $i$ 個查詢與第 $j$ 個鍵的內積——
35:    內積是高維空間的相似度： $q^\top k = \|q\|\|k\|\cos\theta$ 。
36: 2. **歸一化**：除以 $\sqrt{d_k}$ 。因為 $d_k$ 維隨機向量的內積方差為 $d_k$ ：
37:    若 $q, k$ 的分量獨立、均值 0、方差 1，則 $q^\top k = \sum_{m=1}^{d_k} q_m k_m$ 的方差是 $d_k$ 。
38:    不除的話 logits 太大，softmax 飽和、梯度消失。
39: 3. **加權匯總**：softmax 給出非負、和為 1 的權重行 $\mathbf{a}_i$ ，輸出 $\mathbf{o}_i = \sum_j a_{ij} v_j$ ——
40:    每個輸出是所有值的**凸組合**。
41: 
42: ### 投影與多頭
43: 
44: $Q, K, V$ 由輸入 $\mathbf{x}$ 經線性投影得到：
45: 
46: $$
47: Q = XW_Q, \qquad K = XW_K, \qquad V = XW_V
48: $$
49: 
50: **多頭注意力**：並行做 $h$ 次不同投影，讓網路同時關注不同類型的關聯：
51: 
52: $$
53: \mathrm{MultiHead}(X) = \big[\mathrm{head}_1 \,\|\, \cdots \,\|\, \mathrm{head}_h\big]W_O, \qquad
54: \mathrm{head}_i = \mathrm{Attention}(XW_{Q_i}, XW_{K_i}, XW_{V_i})
55: $$
56: 
57: ### 數學本質：動態權重圖
58: 
59: 把 $A = \mathrm{softmax}(QK^\top/\sqrt{d_k})$ 看成一個**有向圖的權重矩陣**：
60: $A_{ij}$ 是「詞 $i$ 對詞 $j$ 的注意力」。與摺積（固定權重、局部連線）對比：
61: 
62: | | 摺積 | 注意力 |
63: |---|---|---|
64: | 連線範圍 | 局部（感受野） | 全局（所有詞對） |
65: | 權重 | 固定（學出後不變） | 動態（依輸入即時計算） |
66: | 對稱群 | 平移群 | 置換（permutation，配合位置編碼） |
67: 
68: ### 自注意力與序列建模
69: 
70: 自注意力（self-attention）中 $Q, K, V$ 都來自同一序列。因果（causal）版本把未來遮掉：
71: 
72: $$
73: A_{ij} = 0 \quad \text{if } j > i \qquad (\text{softmax 前加 } -\infty)
74: $$
75: 
76: 配合位置編碼（05.3 節），Transformer 變成語言模型的骨幹：
77: 
78: $$
79: P(w_{t+1} \mid w_{\le t}) = \mathrm{softmax}\big(W_{\text{out}}\, \mathrm{Transformer}(w_{\le t})\big)
80: $$
81: 
82: ## 簡易範例：兩詞注意力
83: 
84: 兩詞向量（ $d_k = 2$ ）：
85: 
86: $$
87: Q = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \quad
88: K = \begin{pmatrix} 2 & 0 \\ 0 & 2 \end{pmatrix}, \quad
89: V = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}
90: $$
91: 
92: 1. 相似度： $QK^\top = \begin{pmatrix} 2 & 0 \\ 0 & 2 \end{pmatrix}$ ，除以 $\sqrt{2}$ 得 $\begin{pmatrix} 1.414 & 0 \\ 0 & 1.414 \end{pmatrix}$ 。
93: 2. 歸一化： $\mathrm{softmax}$ 按行 $\Rightarrow A = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$ （各詞只看自己——相似度懸殊）。
94: 3. 匯總： $AV = V$ 。
95: 
96: 若把 $K$ 的第二行改成 $(0, 2)$ 換成 $(2, 2)$ ，注意力權重就會重新分配——關聯是**動態**的。
97: 
98: ## 歷史典故
99: 
100: - 2014 年 Seq2Seq 與注意力：見卷宗 [../2014-Seq2Seq與注意力.md](../2014-Seq2Seq與注意力.md)——注意力最初是翻譯模型的「對齊」機制。
101: - 2017 年 Transformer：見 [../2017-Transformer注意力機制.md](../2017-Transformer注意力機制.md)——「Attention Is All You Need」：丟掉循環，只剩注意力。
102: - 2018 年 BERT 與 GPT：見 [../2018-BERT與GPT預訓練典範.md](../2018-BERT與GPT預訓練典範.md)——同一個注意力架構，兩種訓練哲學。
103: - 2021 年 ViT：見 [../2021-ViT視覺Transformer.md](../2021-ViT視覺Transformer.md)——注意力也統一了視覺，圖塊即詞元。
104: 
105: ## 習題
106: 
107: 1. 證明：若 $q, k$ 的分量獨立標準常態，則 $\mathrm{Var}(q^\top k) = d_k$ ，說明為何要除以 $\sqrt{d_k}$ 。
108: 2. 對本節例題改 $K$ 第二行為 $(2,2)$ ，重算 $A$ 與 $AV$ 。
109: 3. 證明 softmax 的行和為 1，且每個輸出 $o_i = \sum_j a_{ij}v_j$ 是 $V$ 各行的凸組合。

(End of file - total 109 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/05.3-位置編碼與RoPE.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/05.3-位置編碼與RoPE.md</path>
<type>file</type>
<content>
1: # 05.3 位置編碼與 RoPE
2: 
3: ## 本章導讀
4: 
5: 注意力有個天生的盲點：它對「順序」視而不見。
6: 把「貓追狗」和「狗追貓」的字序打亂，注意力算出的關聯完全一樣——因為它對輸入是**置換等變**的。
7: 但語言的順序有意義。怎麼把「位置」塞進無序的注意力？答案是一個優雅的幾何技巧：旋轉。
8: 
9: ## 淺顯說明
10: 
11: 最直覺的做法是給每個詞發一個「座位號碼牌」（加到詞向量上）。
12: 2017 年 Transformer 用正弦號碼牌；2021 年 RoPE 改用更聰明的辦法：
13: 
14: - 不加號碼牌，而是把每個詞的向量**在平面上旋轉**一個與位置成正比的角度。
15: - 位置 $m$ 的詞旋轉 $m\theta$ 度。
16: - 神奇之處：兩個詞做內積時，旋轉角自動**相減**——內積只依賴「相對位置 $m - n$ 」，
17:   而不是絕對位置。
18: 
19: 就像兩隻手錶各自快慢不同，比對時間時只需看**時差**。
20: 
21: ## 正規理論
22: 
23: ### 問題：置換等變性
24: 
25: 自注意力對輸入序列的置換等變：打亂詞序，注意力輸出同樣打亂，語義結構不變。
26: 因此必須**顯式**注入位置資訊。
27: 
28: ### 正弦位置編碼（Transformer, 2017）
29: 
30: 位置 $m$ 、維度偶數位 $2i$ ：
31: 
32: $$
33: PE(m, 2i) = \sin\!\left(\frac{m}{10000^{2i/d}}\right), \qquad
34: PE(m, 2i+1) = \cos\!\left(\frac{m}{10000^{2i/d}}\right)
35: $$
36: 
37: 低維振盪快（編碼精細位置）、高維振盪慢（編碼粗位置）——像二進位計數器的連續版。
38: 用法： $\mathbf{x}_m \leftarrow \mathbf{x}_m + PE(m)$ （加法注入）。
39: 
40: ### RoPE：旋轉位置編碼
41: 
42: 把 $d$ 維向量看成 $d/2$ 個二維平面上的複數。位置 $m$ 的詞，每個平面旋轉 $m\theta_i$ ：
43: 
44: $$
45: R_{\Theta, m} = \mathrm{diag}\!\left(R(\theta_1 m), R(\theta_2 m), \dots, R(\theta_{d/2} m)\right), \qquad
46: R(\phi) = \begin{pmatrix} \cos\phi & -\sin\phi \\ \sin\phi & \cos\phi \end{pmatrix}
47: $$
48: 
49: 其中 $\theta_i = 10000^{-2i/d}$ 。應用： $q_m = R_{\Theta,m}\,q$ ， $k_n = R_{\Theta,n}\,k$ 。
50: 
51: ### 核心性質：相對位置偏置
52: 
53: **定理**：旋轉後的內積只依賴相對位置 $m - n$ ：
54: 
55: $$
56: (R_{\Theta,m}\,q)^\top (R_{\Theta,n}\,k) = q^\top R_{\Theta,n-m}\, k
57: $$
58: 
59: **證明**（複數形式）：每個平面是一個複數 $q_j \in \mathbb{C}$ ，旋轉即乘 $e^{i\theta_j m}$ ：
60: 
61: $$
62: \sum_j \overline{e^{i\theta_j m} q_j}\, e^{i\theta_j n} k_j = \sum_j \overline{q_j}\, e^{i\theta_j(n - m)} k_j = q^\top R_{\Theta, n-m}\, k
63: $$
64: 
65: 實數部分正是二維旋轉下的內積。旋轉矩陣的正交性（ $R^\top R = I$ ）保證： $\blacksquare$
66: 
67: $$
68: R_{\Theta,m}^\top R_{\Theta,n} = R_{\Theta, n-m}
69: $$
70: 
71: **意義**：
72: - 內積天生攜帶相對位置資訊——「誰離誰近」自動進入注意力 logits。
73: - 絕對位置不出現——模型可直接外推到更長的序列（配合尺度調整）。
74: - 正交旋轉不改變向量長度——不擾動詞向量的範數，只改方向。
75: 
76: ## 簡易範例：二維旋轉
77: 
78: $d = 2$ ， $\theta = 30°$ 。詞 A 在位置 $m = 1$ ，詞 B 在位置 $n = 3$ ，都是向量 $(1, 0)$ ：
79: 
80: - A 旋轉 $30°$ ： $(\cos 30°, \sin 30°) \approx (0.866, 0.5)$
81: - B 旋轉 $90°$ ： $(\cos 90°, \sin 90°) = (0, 1)$
82: 
83: 內積： $0.866 \times 0 + 0.5 \times 1 = 0.5$ 。
84: 
85: 驗證定理：相對位置 $n - m = 2$ ，即旋轉 $60°$ ， $q^\top R(60°) k = \cos 60° = 0.5$ 。一致！
86: 
87: 內積 $= \cos(\text{角度差})$ ——旋轉位置編碼的本質就是：**位置差變成角度差，內積變成餘弦**。
88: 
89: ## 歷史典故
90: 
91: - 2017 年 Transformer 的正弦編碼：見卷宗 [../2017-Transformer注意力機制.md](../2017-Transformer注意力機制.md)。
92: - 2018 年 BERT 用「學出來的」位置嵌入：見 [../2018-BERT與GPT預訓練典範.md](../2018-BERT與GPT預訓練典範.md)——可學但無法外推。
93: - 2023 年 LLaMA：見 [../2023-LLaMA開源大模型.md](../2023-LLaMA開源大模型.md)——RoPE 成為開源大模型的標配。
94: - 2025 年 DeepSeek-R1：見 [../2025-DeepSeek-R1.md](../2025-DeepSeek-R1.md)——RoPE 的長序列外推能力支撐長鏈推理。
95: 
96: ## 習題
97: 
98: 1. 證明二維旋轉矩陣 $R(\phi)$ 的正交性： $R^\top R = I$ 。
99: 2. 對 $d=2, \theta=45°$ ，詞在位置 0 與 2（向量 $(1,0)$ ），用兩種方式計算內積（直接旋轉 vs 相對位置），驗證一致。
100: 3. 討論：為什麼「相對位置」比「絕對位置」更適合語言？（提示：語法關係多是相對的，且需長度外推。）

(End of file - total 100 lines)
</content>
```

---

## Assistant (Build · GLM-5.3-Flash · 29.8s)

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/06.1-機率語言模型.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/06.1-機率語言模型.md</path>
<type>file</type>
<content>
1: # 06.1 機率語言模型
2: 
3: ## 本章導讀
4: 
5: 語言模型是什麼？一句話：**一個預測下一個詞的機率分布**。
6: 從 1950 年代的 n-gram 統計，到 2013 年的詞向量，到 2018 年的預訓練典範——
7: 架構一直在變，但目標只有一個： $P(w_{t+1} \mid w_{\le t})$ 。
8: 2018 年之後人們發現：把這一件事做到極致，「智慧」竟開始湧現。
9: 
10: ## 準備說明
11: 
12: 給定一句話「今天天氣真___」，你會猜「好」。語言模型做的是同一件事，但用機率：
13: 
14: - 「好」：0.62，「差」：0.15，「冷」：0.10，……
15: - 每一步都輸出一個機率分布，取樣生成文字。
16: 
17: 數學上，整句話的機率由**連鎖律**拆解：一個高維聯合分布，變成一連串的條件分布。
18: 訓練 = 讓每個條件分布盡量準。就這麼簡單——但規模大了，質變就發生。
19: 
20: ## 正規理論
21: 
22: ### 條件機率連鎖律
23: 
24: 一句話 $w_1, w_2, \dots, w_T$ 的聯合機率，由機率論的連鎖律精確分解：
25: 
26: $$
27: \boxed{\;
28: P(w_1, w_2, \dots, w_T) = \prod_{t=1}^{T} P(w_t \mid w_1, \dots, w_{t-1}) = \prod_{t=1}^{T} P(w_t \mid w_{<t})
29: \;}
30: $$
31: 
32: 這是恆等式（不是近似）——語言模型的目標就是學出這一連串條件分布。
33: 
34: ### n-gram 模型：馬可夫近似
35: 
36: 1950 年代的做法：假設只依賴前 $n-1$ 個詞（馬可夫性）：
37: 
38: $$
39: P(w_t \mid w_{<t}) \approx P(w_t \mid w_{t-n+1}, \dots, w_{t-1})
40: $$
41: 
42: 用最大概似估計（數頻率）： $P(w_t \mid w_{t-1}) = \dfrac{C(w_{t-1}, w_t)}{C(w_{t-1})}$ 。
43: 問題：詞組沒出現過就估為 0（稀疏性），需要平滑（smoothing）。
44: 
45: ### 詞向量：語義空間
46: 
47: 2013 年 word2vec 把每個詞映射成向量 $\mathbf{v}_w \in \mathbb{R}^d$ ，訓練目標（skip-gram）：
48: 
49: $$
50: \max \; \sum_{t}\sum_{-c \le j \le c, j \ne 0} \log P(w_{t+j} \mid w_t), \qquad
51: P(w_{t+j}\mid w_t) = \frac{\exp(\mathbf{v}'_{w_{t+j}\top}\mathbf{v}_{w_t})}{\sum_{w'} \exp(\mathbf{v}'_{w'\top}\mathbf{v}_{w_t})}
52: $$
53: 
54: 驚人的經驗事實：語義關係在向量空間中是**線性**的：
55: 
56: $$
57: \mathbf{v}_{\text{king}} - \mathbf{v}_{\text{man}} + \mathbf{v}_{\text{woman}} \approx \mathbf{v}_{\text{queen}}
58: $$
59: 
60: 詞向量 = 把離散符號嵌入連續空間，語義變幾何。
61: 
62: ### 神經語言模型
63: 
64: 用神經網路 $f_\theta$ 學條件分布（現代 LLM）：
65: 
66: $$
67: P(w_{t+1} \mid w_{\le t}) = \mathrm{softmax}\big(W_{\text{out}}\, f_\theta(w_{\le t})\big)_{w_{t+1}}
68: $$
69: 
70: 訓練目標：最小化負對數概似（= 交叉熵，04.3 節）：
71: 
72: $$
73: \mathcal{L}(\theta) = -\frac{1}{T}\sum_{t=1}^{T} \log P_\theta(w_t \mid w_{<t})
74: $$
75: 
76: ### 困惑度
77: 
78: 模型好壞的標準度量：
79: 
80: $$
81: \mathrm{PPL} = \exp\!\left(\mathcal{L}\right) = \exp\!\left(-\frac{1}{T}\sum_t \log P_\theta(w_t \mid w_{<t})\right)
82: $$
83: 
84: PPL 是每步「平均等 unsure 到」的詞選項數：PPL = 10 表示每步約 10 個等機率選項的不確定性。
85: 
86: ## 簡易範例：手算連鎖律
87: 
88: 玩具語料：「貓追狗」（3 次）、「狗追貓」（1 次）。bigram 頻率：
89: 
90: $$
91: P(\text{狗} \mid \text{貓}) = \frac{3}{3} = 1, \qquad
92: P(\text{貓} \mid \text{狗}) = \frac{1}{4} = 0.25
93: $$
94: 
95: 句子「貓追狗」的機率： $P(\text{貓}) \times P(\text{追}\mid\text{貓}) \times P(\text{狗}\mid\text{貓}) = \frac{1}{2}\times\frac{4}{4}\times\frac{3}{4} = 0.375$ （設「追」總在貓後）。
96: 
97: 若模型預測 $P(\text{狗}\mid\text{貓}) = 0.6$ ，該步的損失 $= -\log 0.6 \approx 0.51$ nat——預測越準，損失越低。
98: 
99: ## 歷史典故
100: 
101: - 2013 年 word2vec：見卷宗 [../2013-word2vec詞向量.md](../2013-word2vec詞向量.md)——king − man + woman = queen 驚豔全世界。
102: - 2018 年預訓練典範：見 [../2018-BERT與GPT預訓練典範.md](../2018-BERT與GPT預訓練典範.md)——「先讀萬卷書、再答題」的兩種哲學。
103: - 2020 年 GPT-3 規模湧現：見 [../2020-GPT-3規模湧現.md](../2020-GPT-3規模湧現.md)——1750 億參數下，下一詞預測開始寫文章、寫程式（06.3 節）。
104: 
105: ## 習題
106: 
107: 1. 用連鎖律寫出三詞句 $P(w_1, w_2, w_3)$ ，並說明每個條件分布在神經語言模型中由什麼計算。
108: 2. 證明：最小化交叉熵等價於最大化對數概似。
109: 3. 對本節範例，計算「狗追貓」在模型 $P(\text{貓}\mid\text{狗})=0.6$ 下的損失。

(End of file - total 109 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/06.2-擴散模型與隨機微分方程.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/06.2-擴散模型與隨機微分方程.md</path>
<type>file</type>
<content>
1: # 06.2 擴散模型與隨機微分方程
2: 
3: ## 本章導讀
4: 
5: 生成模型要回答：「資料是從什麼分布來的？」
6: 2020 年的擴散模型（DDPM）給出了一個反直覺的答案：先**學會破壞**（加噪聲），再**學會逆轉**（去噪）。
7: 其數學基礎是物理裡的老朋友——擴散過程——配上伊藤清的隨機微積分。
8: 
9: ## 準備說明
10: 
11: 想像一滴墨水滴進清水：
12: 
13: - **前向**：墨水慢慢擴散，最後整杯水均勻渾濁——有序變無序，純高斯噪聲。
14: - **反向**：我們問——能不能從渾濁的水「倒放」回一滴墨水？
15: 
16: 物理上倒放幾乎不可能（熵增）。但機器學習的招數是：把每個小步的倒放**學**出來。
17: 每一步只加一點噪聲，逆轉每一步只需要一小段去噪——學幾千個小步，就能從純噪聲一路「倒回」一張圖。
18: 
19: ## 正規理論
20: 
21: ### 前向過程：離散版
22: 
23: 給定資料 $\mathbf{x}_0 \sim q(\mathbf{x}_0)$ ，前向逐步加噪：
24: 
25: $$
26: q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) = \mathcal{N}\!\left(\mathbf{x}_t;\ \sqrt{1-\beta_t}\,\mathbf{x}_{t-1},\ \beta_t \mathbf{I}\right)
27: $$
28: 
29: $\beta_t$ 是噪聲計畫。任意時刻可一步到位（令 $\alpha_t = \prod_{s\le t}(1-\beta_s)$ ）：
30: 
31: $$
32: q(\mathbf{x}_t \mid \mathbf{x}_0) = \mathcal{N}\!\left(\mathbf{x}_t;\ \sqrt{\alpha_t}\,\mathbf{x}_0,\ (1-\alpha_t)\mathbf{I}\right)
33: $$
34: 
35: $t \to \infty$ 時 $\alpha_t \to 0$ ， $\mathbf{x}_t$ 趨於標準高斯——有序變無序。
36: 
37: ### 連續版：隨機微分方程與伊藤清微積分
38: 
39: 令 $t \in [0, T]$ 連續，前向過程是一支隨機微分方程（SDE）：
40: 
41: $$
42: d\mathbf{x} = -\frac{1}{2}\beta(t)\,\mathbf{x}\, dt + \sqrt{\beta(t)}\, d\mathbf{w}
43: $$
44: 
45: $d\mathbf{w}$ 是布朗運動的增量（ $\mathbb{E}[d\mathbf{w}] = 0$ ， $\mathrm{Var}(d\mathbf{w}) = dt$ ）。
46: 伊藤清微積分處理含隨機項的微分：隨機項的「二階效應」不可忽略（ $(d\mathbf{w})^2 = dt$ ）。
47: 
48: **Fokker–Planck 方程**給出機率密度 $p(\mathbf{x}, t)$ 的演化：
49: 
50: $$
51: \frac{\partial p}{\partial t} = -\nabla\cdot\big(f(\mathbf{x},t)\,p\big) + \frac{1}{2}\nabla^2\!\big(g^2(t)\,p\big)
52: $$
53: 
54: 前向 SDE 把 $p$ 逐步推向高斯。
55: 
56: ### 反向過程：時間倒流的 SDE
57: 
58: 安德森（Anderson, 1982）證明：前向 SDE 的時間反演也是一支 SDE：
59: 
60: $$
61: d\mathbf{x} = \left[-\frac{1}{2}\beta(t)\,\mathbf{x} - \beta(t)\, \nabla_{\mathbf{x}} \log p_t(\mathbf{x})\right] dt + \sqrt{\beta(t)}\, d\bar{\mathbf{w}}
62: $$
63: 
64: 關鍵項是**分數函數**（score function） $\nabla_{\mathbf{x}}\log p_t(\mathbf{x})$ ——它指向機率密度上升最快的方向。
65: 
66: ### 學習：去噪即學分數
67: 
68: 分數函數未知，但可用神經網路 $\mathbf{s}_\theta$ 近似，訓練目標出奇地簡單：
69: 
70: $$
71: \mathcal{L}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{\epsilon}}\Big[\big\| \mathbf{s}_\theta(\mathbf{x}_t, t) - \nabla_{\mathbf{x}_t}\log p(\mathbf{x}_t \mid \mathbf{x}_0) \big\|^2\Big]
72: $$
73: 
74: 而對高斯前向， $\nabla\log p(\mathbf{x}_t \mid \mathbf{x}_0) = -\boldsymbol{\epsilon}/\sqrt{1-\alpha_t}$ ，其中 $\boldsymbol{\epsilon}$ 就是那個已知的噪聲——
75: 
76: $$
77: \boxed{\;
78: \mathcal{L}(\theta) = \mathbb{E}\Big[\big\| \mathbf{s}_\theta(\sqrt{\alpha_t}\,\mathbf{x}_0 + \sqrt{1-\alpha_t}\,\boldsymbol{\epsilon},\ t) + \boldsymbol{\epsilon}/\sqrt{1-\alpha_t} \big\|^2\Big) \approx \mathbb{E}\big[\|\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t) - \boldsymbol{\epsilon}\|^2\big]
79: \;}
80: $$
81: 
82: **去噪 = 預測加進去的噪聲**。生成時：從純高斯 $\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 出發，用學到的 $\mathbf{s}_\theta$ 積分反向 SDE，一路走到 $\mathbf{x}_0$ ——純噪聲「倒放」成一張圖。
83: 
84: ### 與變分推斷的等價
85: 
86: DDPM 的證明有兩條路：(1) 變分推斷的證據下界（ELBO，04.3 節的 KL 散度逐層相加）；
87: (2) 分數匹配（score matching）。兩者給出同一個訓練目標——機率論的殊途同歸。
88: 
89: ## 簡易範例：一維擴散與去噪
90: 
91: 一維資料 $x_0 = 2$ ， $\beta = 0.1$ （常數），前向三步：
92: 
93: $$
94: x_1 = \sqrt{0.9}\times 2 + \sqrt{0.1}\,\epsilon_1,\quad
95: x_2 = \sqrt{0.9}\,x_1 + \sqrt{0.1}\,\epsilon_2,\ \dots
96: $$
97: 
98: （取 $\epsilon_i = 0$ 看均值軌跡： $2 \to 1.897 \to 1.800 \to 1.708$ ——均值向 0 衰減，方差向 1 增長。）
99: 
100: 反向一步的去噪目標：給定 $x_1$ ，預測噪聲 $\epsilon_1$ 。若模型預測 $\hat\epsilon = 0.3$ 而真值 $0.5$ ，
101: 損失 $= (0.3 - 0.5)^2 = 0.04$ 。訓練幾千步後，模型「知道」每一步該減掉多少噪聲——
102: 反覆應用，就能從噪聲重建 $x_0 \approx 2$ 。
103: 
104: ## 歷史典故
105: 
106: - 2020 年 DDPM：見卷宗 [../2020-DDPM擴散模型.md](../2020-DDPM擴散模型.md)——Ho 等人把「去噪」變成生成。
107: - 2022 年 Stable Diffusion：見 [../2022-StableDiffusion開源擴散.md](../2022-StableDiffusion開源擴散.md)——在隱空間做擴散，開源引爆文生圖。
108: - 2024 年 Sora：見 [../2024-Sora世界模型.md](../2024-Sora世界模型.md)——擴散 Transformer（DiT）生成影片，「世界模擬器」之爭開始（08.2 節）。
109: 
110: ## 習題
111: 
112: 1. 對常數 $\beta$ 的一維前向，求 $x_t$ 的均值與方差（封閉式），驗證 $t\to\infty$ 時趨於 $\mathcal{N}(0,1)$ 。
113: 2. 證明：高斯前向下 $\nabla_{\mathbf{x}_t}\log p(\mathbf{x}_t\mid\mathbf{x}_0) = -\boldsymbol{\epsilon}/\sqrt{1-\alpha_t}$ （提示：對高斯密度取對數再求導）。
114: 3. 解釋為什麼反向 SDE 中的分數函數是「必需」的，以及為什麼可以直接用噪聲預測替代它。

(End of file - total 114 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/06.3-規模法則與湧現.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/06.3-規模法則與湧現.md</path>
<type>file</type>
<content>
1: # 06.3 規模法則與湧現
2: 
3: ## 本章導讀
4: 
5: 模型要多大、資料要多少、算力要多少？2020 年人們發現答案服從一個簡單的數學規律——**冪律**。
6: 損失隨規模平滑下降，但能力卻在某個規模「突然出現」。規模法則（Scaling Laws）讓訓練大模型
7: 從賭博變成工程。
8: 
9: ## 淺顯說明
10: 
11: 把模型訓練想成「煮菜」：
12: 
13: - 模型大小 $N$ （鍋子）、資料量 $D$ （食材）、算力 $C$ （火候）。
14: - Kaplan 等人發現：損失 $L$ 隨 $N, D, C$ 按**冪律**下降——規模翻倍，損失乘一個固定小於 1 的因子。
15: - Chinchilla 定則更進一步：在固定算力下，「模型大小」與「資料量」要**等比例**增長才最划算。
16: 
17: 更神奇的是：小模型寫不了文章，大模型卻突然會寫——損失平滑下降，能力卻「跳」出來。這叫湧現。
18: 
19: ## 正規理論
20: 
21: ### Kaplan 規模法則（2020）
22: 
23: 損失與模型參數 $N$ 、資料 $D$ 、算力 $C$ 服從冪律：
24: 
25: $$
26: L(N) \approx \left(\frac{N_c}{N}\right)^{\alpha_N}, \qquad
27: L(D) \approx \left(\frac{D_c}{D}\right)^{\alpha_D}, \qquad
28: L(C) \approx \left(\frac{C_c}{C}\right)^{\alpha_C}
29: $$
30: 
31: 實測指數約 $\alpha_N \approx 0.076$ （ $N$ 以非嵌入參數計）。多變量形式（可加分解）：
32: 
33: $$
34: L(N, D) \approx E + \frac{A}{N^{\alpha_N}} + \frac{B}{D^{\alpha_D}}
35: $$
36: 
37: $E$ 是不可約損失（資料本身的熵，04.3 節）。三項分別是「模型不夠大、資料不夠多」的懲罰。
38: 
39: ### Chinchilla 定則（2022）
40: 
41: 在固定算力預算 $C \approx 6ND$ （每參數每 token 約 6 次運算）下，最小化 $L(N, D)$ ：
42: 
43: 對 $L$ 分別對 $N$ 、 $D$ 偏導並令為零（拉格朗日乘子法，帶約束的極值問題）：
44: 
45: $$
46: -\alpha_N \frac{A}{N^{\alpha_N + 1}} = \lambda \cdot 6D, \qquad
47: -\alpha_D \frac{B}{D^{\alpha_D + 1}} = \lambda \cdot 6N
48: $$
49: 
50: 聯立解得最優比例（實測 $\alpha_N \approx \alpha_D \approx 0.3$ 量級時）：
51: 
52: $$
53: D \;\propto\; N \qquad \text{即} \qquad N_{\text{opt}} \propto C^{0.5}, \quad D_{\text{opt}} \propto C^{0.5}
54: $$
55: 
56: **意義**：算力翻倍時，模型大小與資料量應各乘 $\sqrt{2}$ ——GPT-3（175B 參數、300B tokens）
57: 資料餵得太少；Chinchilla（70B、1.4T tokens）更小卻更強。
58: 
59: ### 湧現（Emergence）
60: 
61: 某些下游能力（多步推理、指令遵循）隨規模的曲線呈**相變**狀：
62: 
63: $$
64: \mathrm{Acc}(N) \approx \begin{cases} \approx 0, & N < N_c \\ \text{快速上升}, & N \ge N_c \end{cases}
65: $$
66: 
67: 數學上的可能解釋：
68: 1. **度量問題**：下游指標是「全對才得分」的階梯函數，平滑的損失改善累積成跳躍的指標。
69: 2. **複合能力的相乘**：多步推理的正確率是每步正確率的乘積
70:    $p_{\text{total}} = \prod_t p_t = p^n$ ——每步 $p$ 從 0.9 升到 0.99，20 步任務從 0.12 跳到 0.82。
71: 3. 冪律外推：損失可以外推預測，能力不行——這是規模法則最重要的實用與危險之處。
72: 
73: ## 簡易範例：冪律與外推
74: 
75: 設損失 $L(N) = 8\,N^{-0.076}$ ：
76: 
77: | $N$ | $10^{8}$ | $10^{9}$ | $10^{10}$ | $10^{11}$ |
78: |---|---|---|---|---|
79: | $L$ | 4.20 | 3.50 | 2.92 | 2.43 |
80: 
81: 規模 $\times 10$ ，損失乘 $10^{-0.076} \approx 0.84$ ——平滑可外推。
82: 工程意義：用小模型量測冪律參數，就能**預測**大模型的損失，再決定要不要燒算力。
83: 
84: 多步推理的相乘效應：每步正確率 $p = 0.95$ ， $n = 30$ 步：
85: $p^{30} \approx 0.21$ 。把 $p$ 提到 $0.998$ （更好的模型）， $p^{30} \approx 0.94$ ——
86: 損失只改善一點，30 步任務卻從「幾乎失敗」跳到「幾乎全對」——湧現的一個數學側寫。
87: 
88: ## 歷史典故
89: 
90: - 2020 年 GPT-3 規模湧現：見卷宗 [../2020-GPT-3規模湧現.md](../2020-GPT-3規模湧現.md)——1750 億參數下，in-context learning 開始出現。
91: - 2022 年 Chinchilla：見 [../2022-Chinchilla規模法則.md](../2022-Chinchilla規模法則.md)——「算力最優」重寫了業界的訓練配方。
92: - 2025 年 DeepSeek-R1：見 [../2025-DeepSeek-R1.md](../2025-DeepSeek-R1.md)——用 RL 讓推理能力「湧現」，而不只靠規模（07 章細講）。
93: 
94: ## 習題
95: 
96: 1. 對 $L(N,D) = E + A/N^{\alpha} + B/D^{\alpha}$ （ $\alpha_N = \alpha_D = \alpha$ ），在約束 $C = 6ND$ 下用拉格朗日乘子法推導 $N_{\text{opt}} \propto C^{1/2}$ 。
97: 2. 每步正確率 $p = 0.98$ ，多少步之後總正確率跌破 0.5？這對「長鏈推理」有何啟示？
98: 3. 討論：為什麼「損失可外推、能力不可外推」是規模法則最大的實用價值與最大的風險。

(End of file - total 98 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/07.1-MDP與貝爾曼方程.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/07.1-MDP與貝爾曼方程.md</path>
<type>file</type>
<content>
1: # 07.1 MDP 與貝爾曼方程
2: 
3: ## 本章導讀
4: 
5: 前面的章節都是「監督學習」：有標準答案，照著學。
6: 但走迷宮、下棋、開車——沒人告訴你每一步該做什麼，只有事後的**獎勵**。
7: 強化學習（RL）就是「從獎勵中學決策」的數學。其基石是 1950 年代 Bellman 的一個方程，
8: 以及一個保證收斂的定理——巴拿赫不動點。
9: 
10: ## 淺顯說明
11: 
12: 想像你在迷宮裡，每走一步能撿到金幣（或觸雷）：
13: 
14: - 你的目標不是「這一步撿最多」，而是「**總共**撿最多」——要走長遠。
15: - 貝爾曼的洞見：一個狀態的「價值」= 立即獎勵 + 下一個狀態的價值（打折扣）。
16: - 這是遞迴定義：要算 $V(s)$ ，得先算 $V(s')$ ——看起來是循環，但 Bellman 證明：
17:   這個遞迴有**唯一解**，而且反覆迭代**必定收斂**到它。
18: 
19: 「折扣」 $\gamma$ 就是「未來的錢不如現在的錢值」—— $\gamma = 0$ 只看眼前， $\gamma \to 1$ 走長遠。
20: 
21: ## 正規理論
22: 
23: ### 馬爾可夫決策過程（MDP）
24: 
25: MDP 是五元組 $\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$ ：
26: 
27: - $\mathcal{S}$ ：狀態集； $\mathcal{A}$ ：動作集。
28: - $\mathcal{P}(s' \mid s, a)$ ：轉移機率。
29: - $\mathcal{R}(s, a, s')$ ：獎勵； $\gamma \in [0, 1)$ ：折扣因子。
30: 
31: **馬爾可夫性**（無記憶性）是核心假設：
32: 
33: $$
34: P(S_{t+1} \mid S_t, A_t, S_{t-1}, A_{t-1}, \dots) = P(S_{t+1} \mid S_t, A_t)
35: $$
36: 
37: 未來只依賴當前狀態與動作——歷史可以「壓縮」進 $S_t$ 。
38: 
39: ### 價值函數與貝爾曼方程
40: 
41: 策略 $\pi(a \mid s)$ 是「在狀態 $s$ 採取動作 $a$ 的機率」。狀態價值函數定義為期望累積獎勵：
42: 
43: $$
44: V^\pi(s) = \mathbb{E}_\pi\left[\sum_{t=0}^{\infty} \gamma^t r_t \;\middle|\; S_0 = s\right]
45: $$
46: 
47: 展開期望並用馬爾可夫性，得**貝爾曼期望方程**：
48: 
49: $$
50: \boxed{\;
51: V^\pi(s) = \sum_{a \in \mathcal{A}} \pi(a \mid s) \sum_{s', r} P(s', r \mid s, a) \left[ r + \gamma V^\pi(s') \right]
52: \;}
53: $$
54: 
55: 動作價值函數 $Q^\pi(s, a)$ 同理：
56: 
57: $$
58: Q^\pi(s, a) = \sum_{s', r} P(s', r \mid s, a)\left[r + \gamma \sum_{a'} \pi(a' \mid s') Q^\pi(s', a')\right]
59: $$
60: 
61: ### 貝爾曼算子與壓縮映射
62: 
63: 定義貝爾曼期望算子 $T^\pi$ ：
64: 
65: $$
66: (T^\pi V)(s) = \sum_a \pi(a \mid s) \sum_{s', r} P(s', r \mid s, a)\left[r + \gamma V(s')\right]
67: $$
68: 
69: **定理**（壓縮映射）： $T^\pi$ 在 $\|\cdot\|_\infty$ 下是 $\gamma$ -壓縮的：
70: 
71: $$
72: \|T^\pi V_1 - T^\pi V_2\|_\infty \le \gamma\, \|V_1 - V_2\|_\infty
73: $$
74: 
75: **證明**：逐狀態估計，
76: 
77: $$
78: |(T^\pi V_1)(s) - (T^\pi V_2)(s)| = \gamma\left|\sum_a \pi(a\mid s)\sum_{s'} P(s'\mid s,a)\big(V_1(s') - V_2(s')\big)\right| \le \gamma \max_{s'}|V_1(s') - V_2(s')|
79: $$
80: 
81: （用了 $\sum_a \pi = 1$ 、 $\sum_{s'} P = 1$ 與三角不等式。） $\blacksquare$
82: 
83: **巴拿赫不動點定理**：完備度量空間上的壓縮映射有**唯一不動點**，且從任意點出發的迭代**幾何收斂**到它。因此：
84: 
85: 1. $V^\pi$ 是 $T^\pi$ 的唯一不動點： $V^\pi = T^\pi V^\pi$ ——貝爾曼方程的解**存在且唯一**。
86: 2. 價值迭代 $V_{k+1} = T^\pi V_k$ 收斂，誤差以 $\gamma^k$ 衰減：
87: 
88: $$
89: \|V_k - V^\pi\|_\infty \le \gamma^k \,\|V_0 - V^\pi\|_\infty
90: $$
91: 
92: ### 貝爾曼最佳算子與 Q-Learning
93: 
94: 最佳算子取 max：
95: 
96: $$
97: (T^* V)(s) = \max_a \sum_{s', r} P(s', r \mid s, a)\left[r + \gamma V(s')\right]
98: $$
99: 
100: 同樣是 $\gamma$ -壓縮，唯一不動點 $V^*$ （最佳價值）。Q-learning 的更新：
101: 
102: $$
103: Q(s, a) \leftarrow Q(s, a) + \alpha\left[r + \gamma \max_{a'} Q(s', a') - Q(s, a)\right]
104: $$
105: 
106: 在適當條件（所有狀態動作無窮探訪、 $\alpha$ 滿足 Robbins–Monro 條件 $\sum \alpha_t = \infty$ , $\sum \alpha_t^2 < \infty$ ）下**以機率 1 收斂到 $Q^*$ **——壓縮映射又一次保證了收斂。
107: 
108: ## 簡易範例：兩狀態迷宮
109: 
110: 狀態 $\{A, B\}$ ，動作「走」確定轉移： $A \to B$ 得 $r = 1$ ； $B \to A$ 得 $r = 0$ 。 $\gamma = 0.9$ ， $\pi$ 恆「走」。
111: 
112: 貝爾曼方程：
113: 
114: $$
115: V(A) = 1 + \gamma V(B), \qquad V(B) = 0 + \gamma V(A)
116: $$
117: 
118: 代入解： $V(A) = 1 + 0.9 \times 0.9 V(A) \Rightarrow V(A)(1 - 0.81) = 1 \Rightarrow V(A) \approx 5.26$ ， $V(B) \approx 4.74$ 。
119: 
120: 用價值迭代驗證（ $V_0 = 0$ ）： $V_1(A) = 1, V_1(B) = 0$ ； $V_2(A) = 1.9, V_2(B) = 0.9$ ；
121: $V_3(A) = 1.9, V_3(B) = 1.71$ ……震盪衰減，逐步逼近 $5.26 / 4.74$ ——每步誤差乘 $0.9$ ，正是壓縮映射的幾何收斂。
122: 
123: ## 歷史典故
124: 
125: - 1997 年 Deep Blue：見卷宗 [../1997-DeepBlue搜尋智能.md](../1997-DeepBlue搜尋智能.md)——搜尋 + 評估函數（手工版的價值函數）擊敗世界棋王。
126: - 2016 年 AlphaGo：見 [../2016-AlphaGo.md](../2016-AlphaGo.md)——價值網路 + 策略網路 + 蒙地卡羅樹搜尋，把 Bellman 的思想推上圍棋之巔。
127: - 2022 年 ChatGPT 與 RLHF：見 [../2022-ChatGPT與RLHF.md](../2022-ChatGPT與RLHF.md)——RL 從迷宮走進了對話（下一節細講）。
128: 
129: ## 習題
130: 
131: 1. 對本節兩狀態例子改 $\gamma = 0.5$ ，重解貝爾曼方程與價值迭代的前三步。
132: 2. 證明：貝爾曼最佳算子 $T^*$ 也是 $\gamma$ -壓縮（提示： $\max_a f(a) - \max_a g(a) \le \max_a |f(a) - g(a)|$ ）。
133: 3. 說明為什麼馬爾可夫性是「壓縮」的關鍵：若轉移依賴歷史，貝爾曼方程還成立嗎？

(End of file - total 133 lines)
</content>
```

---

## User

套件可以用 numpy, pytorch, matplotlib, .....

---

## Assistant (Build · GLM-5.3-Flash · 29.9s)

_Thinking:_

The user says packages like numpy, pytorch, matplotlib are available. Now continue reading the remaining chapters (07.2, 08.1, 08.2, README maybe), then append 補充 sections to each chapter and create Python files in _code/.

Let me read the remaining chapters.

了解，numpy/pytorch/matplotlib 皆可用。先讀完剩餘章節。

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/07.2-策略梯度與PPO.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/07.2-策略梯度與PPO.md</path>
<type>file</type>
<content>
1: # 07.2 策略梯度與 PPO
2: 
3: ## 本章導讀
4: 
5: 貝爾曼方程在「狀態離散且可列舉」時最漂亮。但開車、寫文章——狀態是連續的或天文級多的，
6: 列舉不了。策略梯度換一條路：直接把策略 $\pi_\theta$ 寫成參數化函數，
7: 對「總獎勵」求梯度、直接梯度上升。
8: REINFORCE 是它的最簡形式，PPO 是現代最常用的改良——RLHF 就是用它訓出來的。
9: 
10: ## 淺顯說明
11: 
12: 策略梯度像「試誤調參」：
13: 
14: 1. 用目前的策略玩幾局，記下每步的動作與總獎勵。
15: 2. 獎勵高的局：把當時的動作機率**調高**；獎勵低的局：**調低**。
16: 3. 重複——策略慢慢走向高獎區。
17: 
18: 難處在於：總獎勵是隨機環境的期望值，無法直接求梯度。
19: 對數導數技巧（log-derivative trick）把它轉成「可採樣」的形式——這是本節的核心數學。
20: 
21: ## 正規理論
22: 
23: ### 策略梯度目標
24: 
25: 參數化策略 $\pi_\theta(a \mid s)$ ，目標函數是期望累積獎勵：
26: 
27: $$
28: J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}\big[R(\tau)\big], \qquad R(\tau) = \sum_t \gamma^t r_t
29: $$
30: 
31: 軌跡 $\tau = (s_0, a_0, s_1, a_1, \dots)$ 的機率： $P(\tau) = \rho_0(s_0)\prod_t \pi_\theta(a_t \mid s_t) P(s_{t+1} \mid s_t, a_t)$ 。
32: 
33: ### 對數導數技巧（核心推導）
34: 
35: 對 $J$ 求梯度（ $\nabla_\theta P(\tau)$ 中的環境項 $P(s_{t+1}\mid s_t,a_t)$ 與 $\theta$ 無關，可消去）：
36: 
37: $$
38: \nabla_\theta J(\theta) = \int \nabla_\theta P(\tau)\, R(\tau)\, d\tau = \int P(\tau)\, \nabla_\theta \log P(\tau)\, R(\tau)\, d\tau
39: $$
40: 
41: 而 $\nabla_\theta \log P(\tau) = \sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)$ ，故得**策略梯度定理**：
42: 
43: $$
44: \boxed{\;
45: \nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}\left[\sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\, R(\tau)\right]
46: \;}
47: $$
48: 
49: **意義**：期望值的梯度（無法直接算）= 「 $\log$ 策略的梯度 × 獎勵」的期望（**可採樣**）。
50: 用幾局樣本平均即可估計，再做梯度上升。
51: 
52: **REINFORCE**（Monte-Carlo 策略梯度）：
53: 
54: $$
55: \theta \leftarrow \theta + \eta\, \sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\, G_t, \qquad G_t = \sum_{t' \ge t} \gamma^{t'-t} r_{t'}
56: $$
57: 
58: 用「從 $t$ 起的回報 $G_t$ 」取代整局 $R(\tau)$ ，降低方差（因果性：未來的獎勵不影響過去的決策責任）。
59: 
60: ### baseline 與優勢函數
61: 
62: 減去一個與動作無關的基線 $b(s)$ 不改變期望（因 $\mathbb{E}[\nabla\log\pi \cdot b] = b\,\nabla\sum_a\pi = 0$ ），卻能降低方差：
63: 
64: $$
65: \nabla_\theta J = \mathbb{E}\big[\nabla_\theta \log \pi_\theta(a \mid s)\, \big(Q^\pi(s,a) - b(s)\big)\big]
66: $$
67: 
68: 取 $b(s) = V^\pi(s)$ ，括號內就是**優勢函數**：
69: 
70: $$
71: A^\pi(s, a) = Q^\pi(s, a) - V^\pi(s) \quad \text{（這個動作比平均好多少）}
72: $$
73: 
74: ### PPO：信任域與 KL 限制
75: 
76: 一步梯度走太遠會毀掉策略（新策略偏離舊策略太遠，樣本資訊失效）。
77: TRPO/PPO 的想法：**限制新舊策略的距離**。TRPO 用帶約束的優化（拉格朗日乘子）：
78: 
79: $$
80: \max_\theta\; \mathbb{E}\left[\frac{\pi_\theta(a \mid s)}{\pi_{\theta_{\text{old}}}(a \mid s)} A^{\pi_{\text{old}}}(s, a)\right]
81: \quad \text{s.t.} \quad
82: D_{\mathrm{KL}}\big(\pi_{\text{old}} \,\|\, \pi_{\text{new}}\big) \le \delta
83: $$
84: 
85: PPO 用裁剪（clipping）近似同一件事：
86: 
87: $$
88: L^{\mathrm{PPO}}(\theta) = \mathbb{E}\Big[\min\!\big(r_t(\theta) A_t,\ \mathrm{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t\big)\Big], \qquad r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}
89: $$
90: 
91: 概率比被夾在 $[1-\epsilon, 1+\epsilon]$ ——策略每次只許小幅更新。KL 散度（04.3 節）是「策略距離」的度量，
92: 限制它 = 防止策略崩潰。
93: 
94: ### RLHF：把人類偏好寫進獎勵
95: 
96: RLHF（ChatGPT 的訓練法）三步：
97: 
98: 1. 收集人類偏好對 $(y_w \succ y_l)$ ，訓練獎勵模型 $\hat r_\theta(x, y)$ （Bradley–Terry 模型）：
99: 
100: $$
101: P(y_w \succ y_l) = \sigma\big(\hat r(x, y_w) - \hat r(x, y_l)\big)
102: $$
103: 
104: 2. 用 PPO 最大化獎勵： $\max_\pi \mathbb{E}_{x, y \sim \pi}[\hat r(x, y)]$ 。
105: 3. 加 KL 懲罰防止語言模型漂移成「獎勵駭客」：
106: 
107: $$
108: \text{reward} = \hat r(x, y) - \beta\, D_{\mathrm{KL}}\big(\pi \,\|\, \pi_{\text{ref}}\big)
109: $$
110: 
111: ## 簡易範例：兩動作策略上升
112: 
113: 狀態只有一個，動作 $\{a_1, a_2\}$ ， $\pi_\theta(a_1) = \sigma(\theta)$ 。動作 $a_1$ 得獎勵 $+1$ ， $a_2$ 得 $-1$ 。
114: 
115: 策略梯度： $\nabla_\theta J = \mathbb{E}[\nabla_\theta \log \pi_\theta(a)\, r(a)]$ 。
116: 而 $\nabla_\theta \log \sigma(\theta) = 1 - \sigma(\theta)$ 、 $\nabla_\theta \log(1 - \sigma(\theta)) = -\sigma(\theta)$ ：
117: 
118: $$
119: \nabla_\theta J = \pi_\theta(a_1)(1 - \pi_\theta(a_1))(+1) + \pi_\theta(a_2)(-\pi_\theta(a_1))(-1) = \pi(a_1)\big((1-\pi(a_1)) + \pi(a_1)\big) = \pi(a_1)
120: $$
121: 
122: （代入 $\pi(a_2) = 1 - \pi(a_1)$ 。）所以 $\theta \leftarrow \theta + \eta\,\sigma(\theta)$ ——
123: $\theta$ 增大 → $\pi(a_1)$ 增大 → 更常選好動作。取 $\eta = 1$ ， $\theta_0 = 0$ ：
124: 
125: | $k$ | 0 | 1 | 2 | 3 |
126: |---|---|---|---|---|
127: | $\pi(a_1)$ | 0.500 | 0.731 | 0.796 | 0.848 |
128: 
129: 策略單調走向「總選 $a_1$ 」——試誤調參的數學本質。
130: 
131: ## 歷史典故
132: 
133: - 2016 年 AlphaGo：見卷宗 [../2016-AlphaGo.md](../2016-AlphaGo.md)——策略網路的自我對弈訓練，是策略梯度的大規模應用。
134: - 2022 年 ChatGPT 與 RLHF：見 [../2022-ChatGPT與RLHF.md](../2022-ChatGPT與RLHF.md)——PPO + KL 懲罰，把人類偏好寫進語言模型。
135: - 2025 年 DeepSeek-R1：見 [../2025-DeepSeek-R1.md](../2025-DeepSeek-R1.md)——用可驗證獎勵（答案對錯）做 RL，推理鏈「湧現」（06.3 節）。
136: 
137: ## 習題
138: 
139: 1. 證明：減去 baseline 不改變策略梯度的期望（ $\mathbb{E}[\nabla\log\pi\, b(s)] = 0$ ）。
140: 2. 對本節範例求 $J(\theta) = \sigma(\theta)(+1) + (1-\sigma(\theta))(-1) = 2\sigma(\theta) - 1$ ，直接對 $J$ 求導驗證 $\nabla J = \pi(a_1)$ 。
141: 3. 解釋為什麼 PPO 的 clip 等價於「KL 信任域」的軟版本，以及獎勵駭客（reward hacking）為何需要 KL 懲罰來防。

(End of file - total 141 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/08.1-哈密頓神經網路與守恆學習.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/08.1-哈密頓神經網路與守恆學習.md</path>
<type>file</type>
<content>
1: # 08.1 哈密頓神經網路與守恆學習
2: 
3: ## 本章導讀
4: 
5: 前面的網路學什麼都「自由發揮」——包括學物理。但自由的網路學牛頓力學時會漏掉能量守恆：
6: 預測的單擺會越盪越高、行星會慢慢飛散。
7: 2020 年的哈密頓神經網路（HNN）給出解法：**把守恆律寫進架構**。
8: 這是「把對稱性寫進結構」（05.1 節 CNN）思想的力學版。
9: 
10: ## 淺顯說明
11: 
12: 一般神經網路學物理像「看影片學丟球」——學得像，但細節會飄。
13: HNN 換了一個聰明的問法：
14: 
15: - 不直接學「軌跡 $q(t)$ 」，而是學「能量函數 $H_\theta(q, p)$ 」。
16: - 能量學出來後，運動方程**自動**由哈密頓方程給出——而哈密頓方程**天生守恆**（能量是常數）。
17: - 就像與其背食譜的成品照片，不如學食譜本身——成品自然對。
18: 
19: 參考 [../../哈密頓物理學/教材/](../../哈密頓物理學/教材/README.md)：哈密頓力學的主角是能量與相空間，
20: HNN 把這套數學原封不動搬進神經網路。
21: 
22: ## 正規理論
23: 
24: ### 復習：哈密頓方程
25: 
26: 相空間 $(q, p)$ 中，物理系統由哈密頓量 $H(q, p)$ 決定：
27: 
28: $$
29: \dot q = \frac{\partial H}{\partial p}, \qquad \dot p = -\frac{\partial H}{\partial q}
30: $$
31: 
32: **能量守恆**： $\dfrac{dH}{dt} = \dfrac{\partial H}{\partial q}\dot q + \dfrac{\partial H}{\partial p}\dot p = \dfrac{\partial H}{\partial q}\dfrac{\partial H}{\partial p} - \dfrac{\partial H}{\partial p}\dfrac{\partial H}{\partial q} = 0$ 。
33: 
34: ### 辛幾何：結構矩陣 $\mathbf{J}$
35: 
36: 把哈密頓方程寫成矩陣形式：
37: 
38: $$
39: \dot{\mathbf{z}} = \mathbf{J}\, \nabla_{\mathbf{z}} H, \qquad
40: \mathbf{z} = \begin{pmatrix} \mathbf{q} \\ \mathbf{p} \end{pmatrix}, \qquad
41: \mathbf{J} = \begin{pmatrix} \mathbf{0} & \mathbf{I} \\ -\mathbf{I} & \mathbf{0} \end{pmatrix}
42: $$
43: 
44: $\mathbf{J}$ 是**斜對稱矩陣**（ $\mathbf{J}^\top = -\mathbf{J}$ ），它定義了相空間上的辛結構。
45: 
46: **能量守恆的矩陣證明**：
47: 
48: $$
49: \frac{dH}{dt} = \nabla_{\mathbf{z}} H^\top \dot{\mathbf{z}} = \nabla H^\top \mathbf{J} \nabla H = 0
50: $$
51: 
52: （因為 $\mathbf{a}^\top \mathbf{J} \mathbf{a} = 0$ 對任何 $\mathbf{a}$ 成立——斜對稱性。）
53: 
54: **Liouville 定理**：辛流保相空間體積——哈密頓流不壓縮、不膨脹相空間，
55: 這是統計物理與混沌理論的幾何基礎（參考 [../../哈密頓物理學/教材/01.2-相空間與狀態.md](../../哈密頓物理學/教材/01.2-相空間與狀態.md)）。
56: 
57: ### 哈密頓神經網路（HNN）
58: 
59: Gray、Lange、Aitchison 等人（2020）的想法：用神經網路參數化 $H_\theta$ ，運動方程由架構保證：
60: 
61: $$
62: \dot{\mathbf{z}} = \mathbf{J}\, \nabla_{\mathbf{z}} H_\theta(\mathbf{z}), \qquad
63: H_\theta(\mathbf{z}) = \mathrm{MLP}_\theta(\mathbf{z})
64: $$
65: 
66: 訓練目標：讓預測的向量場貼近觀測資料：
67: 
68: $$
69: \mathcal{L}(\theta) = \big\| \dot{\mathbf{z}}_{\text{data}} - \mathbf{J}\, \nabla_{\mathbf{z}} H_\theta(\mathbf{z}) \big\|^2
70: $$
71: 
72: $\nabla_{\mathbf{z}} H_\theta$ 由自動微分算出（03.2 節）。
73: **關鍵**：無論 $\theta$ 學成什麼， $H$ 守恆永遠成立——守恆律是**架構保證**，不是學出來的近似。
74: 
75: ### 辛積分器：數值解也不散逸
76: 
77: 用一般數值方法（如 Runge–Kutta、Euler）積分哈密頓方程，長時間後能量會**緩慢漂移**。
78: 辛積分器（如 leapfrog／Verlet）保住辛結構，能量只在真值附近**有界振盪**：
79: 
80: Leapfrog 半步法：
81: 
82: $$
83: \mathbf{p}_{n+1/2} = \mathbf{p}_n - \frac{\Delta t}{2}\nabla_{\mathbf{q}} H(\mathbf{q}_n), \qquad
84: \mathbf{q}_{n+1} = \mathbf{q}_n + \Delta t\, \nabla_{\mathbf{p}} H(\mathbf{p}_{n+1/2}), \qquad
85: \mathbf{p}_{n+1} = \mathbf{p}_{n+1/2} - \frac{\Delta t}{2}\nabla_{\mathbf{q}} H(\mathbf{q}_{n+1})
86: $$
87: 
88: 物理 AI 引擎（可微物理、Diff-Physics）用「可微模擬器 + 辛積分器」，讓梯度穿透物理引擎流動：
89: $\partial(\text{最終狀態})/\partial(\text{初始參數})$ 直接可算，支援系統識別與控制。
90: 
91: ### 拉格朗日神經網路（LNN）
92: 
93: 另一條路：學 Lagrangian $L_\theta(\mathbf{q}, \dot{\mathbf{q}})$ ，運動方程由 Euler–Lagrange 方程給出：
94: 
95: $$
96: \frac{d}{dt}\frac{\partial L_\theta}{\partial \dot{\mathbf{q}}} - \frac{\partial L_\theta}{\partial \mathbf{q}} = 0
97: $$
98: 
99: （參考 [../../哈密頓物理學/教材/03.1-最小作用量原理.md](../../哈密頓物理學/教材/03.1-最小作用量原理.md)。）
100: LNN 不需要動量 $p$ ，直接從「位置＋速度」資料學，適合只有視覺觀測的場景。
101: 
102: ## 簡易範例：學單擺的能量
103: 
104: 單擺（參考 [../../哈密頓物理學/教材/02.3-簡易範例-自由落體與單擺.md](../../哈密頓物理學/教材/02.3-簡易範例-自由落體與單擺.md)）：
105: 真實哈密頓量 $H = \dfrac{p^2}{2ml^2} + mgl(1 - \cos q)$ 。
106: 
107: 給定觀測資料 $\{(\mathbf{z}_i, \dot{\mathbf{z}}_i)\}$ （相空間點與其速度），HNN 訓練迴圈：
108: 
109: 1. 用 $\nabla_\theta H_\theta$ 計算預測速度場： $\hat{\dot{\mathbf{z}}}_i = \mathbf{J}\,\nabla H_\theta(\mathbf{z}_i)$ 。
110: 2. 損失： $\mathcal{L} = \sum_i \|\dot{\mathbf{z}}_i - \hat{\dot{\mathbf{z}}}_i\|^2$ ，梯度下降更新 $\theta$ 。
111: 
112: 學成後**驗證守恆**：沿學出的向量場積分（用 leapfrog），計算 $H_\theta(\mathbf{z}(t))$ ——
113: 一般網路的預測能量隨時間漂移（單擺越盪越高），HNN 的能量在常數附近振盪不散——
114: 架構保證了守恆，資料只教「能量長什麼樣」。
115: 
116: ## 歷史典故
117: 
118: - 1986–2024 年的 AI 進化鏈：見卷宗 [../README.md](../README.md)——從反向傳播到世界模型。
119: - 2024 年 VJEPA／Sora 世界模型：見 [../2024-VJEPA世界模型.md](../2024-VJEPA世界模型.md) 與 [../2024-Sora世界模型.md](../2024-Sora世界模型.md)——「學世界動力學」成為前沿，HNN 提供守恆版本（下一節）。
120: - 哈密頓力學本身：見 [../../哈密頓物理學/教材/README.md](../../哈密頓物理學/教材/README.md)——1834 年的正則方程，在 2020 年變成了神經網路架構。
121: 
122: ## 習題
123: 
124: 1. 證明：對任何向量 $\mathbf{a} \in \mathbb{R}^{2n}$ ， $\mathbf{a}^\top \mathbf{J} \mathbf{a} = 0$ （ $\mathbf{J}$ 斜對稱）。
125: 2. 對單擺 $H = \frac{p^2}{2ml^2} + mgl(1-\cos q)$ ，寫出哈密頓方程並驗證 $\frac{dH}{dt} = 0$ 。
126: 3. 討論：為什麼「守恆律寫進架構」比「用損失懲罰能量漂移」（soft constraint）更可靠？（提示：懲罰是近似，架構是保證。）

(End of file - total 126 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/08.2-世界模型與隱空間規劃.md"
}
```

**Output:**
```
<path>/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書/08.2-世界模型與隱空間規劃.md</path>
<type>file</type>
<content>
1: # 08.2 世界模型與隱空間規劃
2: 
3: ## 本章導讀
4: 
5: 前面的模型都「被動」：看到什麼學什麼。但生物智慧是**主動**的——
6: 貓在跳上櫃子之前，腦中已經「演練」過整段動作。世界模型（World Models）就是這個能力：
7: **學出環境的動力學，在想像中規劃行動**。
8: 2024 年的 JEPA／V-JEPA、2025 年的 Genie 3，都是這條路的現代篇。
9: 
10: ## 淺顯說明
11: 
12: 世界模型像「心中有一台模擬器」：
13: 
14: - **編碼**：把看到的畫面壓縮成「概念狀態」（不是像素，是語義）。
15: - **預測**：「我這樣做，世界會變成什麼概念狀態？」——在隱空間預測，不生成像素。
16: - **規劃**：在心中模擬多步行動，選最好的那條——像下棋的「心算」。
17: 
18: 在隱空間規劃（而非像素空間生成）的好處：便宜、快速、且只關心「重要的事」——
19: 這是 LeCun 主張 JEPA 優於生成式世界模型的理由。
20: 
21: ## 正規理論
22: 
23: ### 世界模型的三個組件
24: 
25: $$
26: \mathbf{e}_t = E_\phi(\mathbf{o}_t), \qquad
27: \hat{\mathbf{e}}_{t+1} = D_\psi(\mathbf{e}_t, a_t), \qquad
28: \pi_\theta(a_t \mid \mathbf{e}_t)
29: $$
30: 
31: - 編碼器 $E_\phi$ ：觀測 $\to$ 隱狀態。
32: - 動力學 $D_\psi$ ：隱狀態 + 動作 $\to$ 下一隱狀態（**世界模型的數學核心**）。
33: - 策略 $\pi_\theta$ ：在隱狀態上決策（07 章的 RL）。
34: 
35: ### 學習動力學：預測即學習
36: 
37: 訓練目標：讓隱空間的預測貼近真實的下一步：
38: 
39: $$
40: \mathcal{L}(\phi, \psi) = \big\| D_\psi(E_\phi(\mathbf{o}_t), a_t) - E_\phi(\mathbf{o}_{t+1}) \big\|^2
41: $$
42: 
43: 這是「自監督」的：不需要標籤，環境本身就是答案。2014 年的 Seq2Seq、2020 年的世界模型 Ha &
44: Schmidhuber，都是這個目標的不同版本。
45: 
46: ### JEPA：預測抽象表徵
47: 
48: JEPA（Joint-Embedding Predictive Architecture）的關鍵主張：**不要在像素空間預測**。
49: 生成式模型（像擴散模型，06.2 節）要預測每個像素，浪費算力在無關細節（草的搖晃、光的噪聲）上；
50: JEPA 只在「抽象表徵空間」預測：
51: 
52: $$
53: \mathcal{L}_{\mathrm{JEPA}} = \big\| P_\psi(E_\phi(\mathbf{o}_t), a_t) - \bar{E}_{\bar\phi}(\mathbf{o}_{t+1}) \big\|^2
54: $$
55: 
56: （目標編碼器 $\bar{E}_{\bar\phi}$ 是滾動平均或停止梯度版，避免表徵崩潰。）
57: 
58: **表徵崩潰與正則化**：純預測損失有個平凡解——所有 $\mathbf{e}_t$ 都輸出常數（模型「躺平」）。
59: 防崩潰的數學工具：
60: 
61: 1. **協方差正則化**（V-JEPA / SIGReg 的精神）：要求隱向量的協方差矩陣接近單位陣——
62: 
63: $$
64: \mathcal{L}_{\mathrm{reg}} = \big\| \mathrm{Cov}(\mathbf{e}) - \mathbf{I} \big\|^2
65: $$
66: 
67:    這強制各維度都「有資訊」（方差為 1）、彼此不冗餘（相關為 0）——防止維度崩潰。
68:    對 $\mathrm{Cov}$ 的分析也可用**特徵分解**：崩潰 ⇔ 部分特徵值趨於 0。
69: 2. **特徵函數匹配**（SIGReg）：用經驗特徵函數 $\varphi_{\mathbf{e}}(t) = \mathbb{E}[e^{it^\top \mathbf{e}}]$
70:    與高斯分佈的特徵函數比對，強制隱分佈接近各向同性高斯。
71: 
72: ### 模型預測控制（MPC）：在想像中規劃
73: 
74: 學好 $D_\psi$ 後，行動規劃變成最優控制問題：
75: 
76: $$
77: a^*_{0:T-1} = \arg\min_{a_{0:T-1}} \sum_{t=0}^{T-1} c(\mathbf{e}_t, a_t) + c_T(\mathbf{e}_T), \qquad
78: \mathbf{e}_{t+1} = D_\psi(\mathbf{e}_t, a_t)
79: $$
80: 
81: 在**隱空間**中搜尋最優軌跡（不需生成像素）——常用方法：
82: 
83: 1. **梯度法**： $D_\psi$ 可微（03.2 節），梯度可以**穿過動力學**反傳：
84: 
85: $$
86: \frac{\partial}{\partial a_0}\sum_t c(\mathbf{e}_t, a_t) \quad \text{由鏈鎖律穿過 } D_\psi \text{ 多次}
87: $$
88: 
89: 2. **交叉熵方法（CEM）**：抽樣式搜尋——迭代地「抽樣一批候選軌跡 → 取最好的前 10% → 重新擬合抽樣分布」：
90: 
91: $$
92: \boldsymbol{\mu}_{k+1}, \boldsymbol{\Sigma}_{k+1} = \mathrm{fit}\big(\text{top-10\% of } \{a^{(i)} \sim \mathcal{N}(\boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)\}\big)
93: $$
94: 
95: 分布逐步收斂到高獎區——與 04.2 節 Boltzmann 採樣的「探索 vs 收斂」異曲同工。
96: 
97: ### 完整迴路：Dreaming + Acting
98: 
99: $$
100: \underbrace{\mathbf{e}_t \to \hat{\mathbf{e}}_{t+1} \to \hat{\mathbf{e}}_{t+2} \to \cdots}_{\text{在想像中滾動（不碰環境）}}
101: \;\Rightarrow\; a^*_0 \;\xrightarrow{\text{真實環境}}\; \mathbf{o}_{t+1} \;\to\; \text{重新編碼}
102: $$
103: 
104: 每步真實行動後重新編碼，矯正想像的漂移——「做夢，走一步，再校正」。
105: 
106: ## 簡易範例：一維隱空間規劃
107: 
108: 隱空間是一維實數 $e \in \mathbb{R}$ ，動力學已學出： $e_{t+1} = e_t + a_t$ （ $a_t \in \{-1, +1\}$ ），
109: 代價 $c(e, a) = 0.1 + e^2$ （想靠近 0），規劃兩步。
110: 
111: 窮舉四條軌跡（從 $e_0 = 2$ ）：
112: 
113: | $(a_0, a_1)$ | 軌跡 | 總代價 |
114: |---|---|---|
115: | $(-1, -1)$ | $2 \to 1 \to 0$ | $0.1 + 4 + 0.1 + 1 + 0.1 + 0 = 5.3$ |
116: | $(-1, +1)$ | $2 \to 1 \to 2$ | $0.1+4+0.1+1+0.1+4 = 9.3$ |
117: | $(+1, -1)$ | $2 \to 3 \to 2$ | $0.1+4+0.1+9+0.1+4 = 13.3$ |
118: | $(+1, +1)$ | $2 \to 3 \to 4$ | $17.3$ |
119: 
120: 最優行動 $a_0^* = -1$ ——在想像中「心算」兩步，選出最優。規劃步數 $T$ 越長，想像越有用，
121: 但也越容易因動力學誤差而漂移——這就是「再校正」（重新編碼）存在的理由。
122: 
123: ## 歷史典故
124: 
125: - 2024 年 VJEPA：見卷宗 [../2024-VJEPA世界模型.md](../2024-VJEPA世界模型.md)——LeCun 主張「在抽象空間預測」，影片理解不生成像素。
126: - 2024 年 Sora：見 [../2024-Sora世界模型.md](../2024-Sora世界模型.md)——擴散 Transformer 生成影片，「世界模擬器」與 JEPA 兩條路線之爭。
127: - 2025 年 Genie 3：見 [../2025-Genie3互動世界模型.md](../2025-Genie3互動世界模型.md)——可互動的世界模型：動作改變想像。
128: - 2025 年 MCP 智慧代理：見 [../2025-MCP智慧代理.md](../2025-MCP智慧代理.md)——世界模型與代理的介面。
129: 
130: ## 習題
131: 
132: 1. 對本節範例改 $c(e,a) = 0.1 + (e-1)^2$ （想靠近 1），重算最優 $(a_0, a_1)$ 。
133: 2. 證明：若隱向量 $\mathbf{e}$ 的協方差矩陣為 $\mathbf{I}$ ，則各維方差為 1 且兩兩不相關——這如何防止「躺平解」。
134: 3. 討論：生成式世界模型（Sora 路線）與 JEPA 路線的數學差異，各適合什麼場景？（提示：像素級真實感 vs 算力與語義抽象。）

(End of file - total 134 lines)
</content>
```

---

## Assistant (Build · GLM-5.3-Flash · 1424.1s)

_Thinking:_

Now I have all 20 chapters. I need to append "## 補充" sections with:
1. 數學推導證明
2. 簡易範例（計算、程式...）

And create Python files in _code/ named like 01.1-yyyy.py? User said "章節-名稱.py，例如 01-yyyy.py". Chapter labels are like 01.1. I'll use e.g. `01.1-mp-neuron-logic.py` — matches "章節-名稱" format. Good.

This is a large task: 20 chapters. I'll parallelize with general agents. Each agent handles a few chapters: write 補充 section appended to md, and write the python file, and verify python runs.

Plan: 4 agents, 5 chapters each. Give each agent detailed instructions and chapter content knowledge. Actually agents can read the files themselves. I'll instruct them to read the chapter files, then append 補充 with new derivations (not repeating the chapter's existing derivations), plus examples, write python code, test it.

Naming: e.g. 01.1-mp-neuron-logic.py.

Let me dispatch 4 agents in parallel.

所有章節已讀完（共 20 節）。現在分派 4 個平行代理，每個處理 5 節，為每節加上 `## 補充`（數學推導證明 + 簡易範例），並在 `_code/` 建立對應 Python 檔。

**Tool: task**

**Input:**
```json
{
  "subagent_type": "general",
  "description": "補充章節 01.x 02.x",
  "prompt": "工作目錄：/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書\n\n你要為一本數學書（神經網路數學史）的 5 個章節檔案，在最後「加上」一個「## 補充」章節。章節檔案（用 Read 讀取後用 Edit 在檔尾附加）：\n1. 01.1-神經元與邏輯運算.md（McCulloch-Pitts 神經元、邏輯閘、XOR）\n2. 01.2-學習規則與權重更新.md（Hebb 律、外積儲存、聯想記憶）\n3. 02.1-感知器與線性分類.md（感知器演算法、Novikoff 收斂定理）\n4. 02.2-損失函數與梯度下降.md（梯度下降、SGD、動量、Adam）\n5. （第 5 個檔案不存在——忽略，只做上面 4 個）\n\n每個檔案附加的「## 補充」格式（繁體中文，風格與原書一致，用 LaTeX 數學 $...$ / $$...$$）：\n\n## 補充\n\n### 1. 數學推導證明\n（1-2 個**新的**推導或證明，不要重複章節內已有的證明。可選章節習題中的證明題做完整推導，或補充相關定理證明）\n\n### 2. 簡易範例\n（1-2 個簡易計算範例的說明，若有程式則說明程式在 _code/ 中，並描述其輸出）\n\n同時在 _code/ 目錄（已存在）為每個有程式的章節建立 Python 檔，命名「章節-名稱.py」，如：\n- 01.1-mp-neuron-logic.py\n- 01.2-hebb-associative-memory.py\n- 02.1-perceptron-training.py\n- 02.2-gradient-descent.py\n\n程式要求：只用 numpy（不要 pytorch/matplotlib，保持簡單無依賴輸出）、純文字輸出、含中文註解（程式註解允許）、執行該章節的核心數學（如：用 numpy 驗證 M-P 神經元實現 AND/OR/NOT/XOR 兩層網路；Hebb 律儲存模式並回憶；感知器訓練循環收斂；梯度下降含 SGD/動量/Adam 比較）。每個程式執行後應印出數值驗證結果。\n\n必須用 bash 實際執行每個 .py 檔驗證可跑且輸出正確（workdir 設為 _code/ 或用 python3 _code/xxx.py）。\n\n完成後回報：每個檔案做了什麼補充、程式檔名、執行結果是否正確。"
}
```

**Error:**
```
Subagent failed (task_id: ses_ee00aeff9ffeqXu3nUQfuloHFc): Too Many Requests: {"status":429,"title":"Too Many Requests"}
```

**Tool: task**

**Input:**
```json
{
  "description": "補充章節 03.x 04.x",
  "subagent_type": "general",
  "prompt": "工作目錄：/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書\n\n你要為一本數學書（神經網路數學史）的 4 個章節檔案，在最後「加上」一個「## 補充」章節。章節檔案（用 Read 讀取後用 Edit 在檔尾附加）：\n1. 03.1-活化函數與泛近似定理.md（sigmoid/tanh/ReLU、泛近似定理）\n2. 03.2-反向傳播演算法.md（鏈鎖律、誤差項遞推）\n3. 04.1-Hopfield網路與能量函數.md（能量函數、單調下降定理）\n4. 04.2-Boltzmann機器與softmax.md（Gibbs 分布、softmax、溫度）\n\n每個檔案附加的「## 補充」格式（繁體中文，風格與原書一致，用 LaTeX 數學 $...$ / $$...$$）：\n\n## 補充\n\n### 1. 數學推導證明\n（1-2 個**新的**推導或證明，不要重複章節內已有的證明。可選章節習題中的證明題做完整推導，如：ReLU 表達 |x|；softmax+交叉熵得 δ=ŷ−y；均勻分布熵最大；Gibbs 條件機率推導；Hopfield 能量計算）\n\n### 2. 簡易範例\n（1-2 個簡易計算範例的說明，若有程式則說明程式在 _code/ 中，並描述其輸出）\n\n同時在 _code/ 目錄（已存在）為每個有程式的章節建立 Python 檔，命名「章節-名稱.py」，如：\n- 03.1-relu-universal-approximation.py\n- 03.2-backprop-manual.py\n- 04.1-hopfield-energy.py\n- 04.2-softmax-temperature.py\n\n程式要求：只用 numpy（不要 pytorch/matplotlib，保持簡單無依賴輸出）、純文字輸出、含中文註解（程式註解允許）。內容建議：用 ReLU 階梯逼近 sin(x)（數值驗證誤差）；兩層網路手算 backprop 並用數值差分驗證梯度；Hopfield 網路儲存模式、輸入雜訊版回憶並計算能量；softmax 溫度掃描（T 從 0.1 到 10 的機率變化）。每個程式執行後應印出數值驗證結果。\n\n必須用 bash 實際執行每個 .py 檔驗證可跑且輸出正確。\n\n完成後回報：每個檔案做了什麼補充、程式檔名、執行結果是否正確。"
}
```

**Output:**
```
<task id="ses_ee00a6ef3ffef9Ygo6Y146y4t0" state="completed">
<task_result>
全部完成，4 個章節檔案都已在檔尾附加「## 補充」，4 個程式皆實際執行驗證通過。

**1. 03.1-活化函數與泛近似定理.md**
- 補充：證明一（習題 1）兩個 ReLU 表達 $|x|$；證明二：均勻分布熵最大（Lagrange 變分）。範例描述 ReLU 階梯逼近 $\sin$ 與線性網路塌縮。
- 程式：`_code/03.1-relu-universal-approximation.py` ✅ 階梯誤差隨段數下降（M=2→0.21，M=64→0.0003）；ReLU 表達 $|x|$ 誤差 0；線性塌縮差異 2.2e-16。

**2. 03.2-反向傳播演算法.md**
- 補充：完整推導 softmax + 交叉熵得 $\boldsymbol{\delta}^{(L)} = \hat{\mathbf{y}} - \mathbf{y}$（習題 2）；範例含更新一步驗證損失下降。
- 程式：`_code/03.2-backprop-manual.py` ✅ 2-2-1 網路解析梯度與中心差分驗證一致（差異 ≤3.4e-12）；更新一步損失 0.0156→0.00034。

**3. 04.1-Hopfield網路與能量函數.md**
- 補充：習題 2 的能量計算（兩模式皆為 $E=-\tfrac{2}{3}$ 全域極小）+ 能量在 $\mathbf{s}\to-\mathbf{s}$ 下對稱的說明。
- 程式：`_code/04.1-hopfield-energy.py` ✅ 64 神經元、15% 雜訊回憶，能量 $-16.03 \to -31.5$ 嚴格單調下降，回憶正確率 100%。

**4. 04.2-Boltzmann機器與softmax.md**
- 補充：證明 Gibbs 條件機率 $=\sigma(h_i/T)$（習題 1）+ 習題 2 的 $T = 4/\ln 99 \approx 0.87$ 推導。
- 程式：`_code/04.2-softmax-temperature.py` ✅ 溫度掃描 T=0.1→10 顯示貪心→均勻；數值驗證 $T=0.8705$ 時 $P(+1)=0.990000$，與解析解一致。
</task_result>
</task>
```

**Tool: task**

**Input:**
```json
{
  "description": "補充章節 05.x 06.x",
  "prompt": "工作目錄：/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書\n\n你要為一本數學書（神經網路數學史）的 6 個章節檔案，在最後「加上」一個「## 補充」章節。章節檔案（用 Read 讀取後用 Edit 在檔尾附加）：\n1. 05.1-CNN與權重共享.md（離散卷積、平移等變性）\n2. 05.2-注意力機制與Transformer.md（scaled dot-product attention、多頭）\n3. 05.3-位置編碼與RoPE.md（正弦編碼、旋轉矩陣、相對位置）\n4. 06.1-機率語言模型.md（連鎖律、n-gram、困惑度）\n5. 06.2-擴散模型與隨機微分方程.md（前向/反向 SDE、去噪）\n6. 06.3-規模法則與湧現.md（冪律、Chinchilla、多步推理相乘）\n\n每個檔案附加的「## 補充」格式（繁體中文，風格與原書一致，用 LaTeX 數學 $...$ / $$...$$）：\n\n## 補充\n\n### 1. 數學推導證明\n（1-2 個**新的**推導或證明，不要重複章節內已有的證明。可選章節習題中的證明題做完整推導，如：softmax 行和為 1 與凸組合；旋轉矩陣正交性；高斯前向的 score 推導；熵最大性；Var(q·k)=d_k）\n\n### 2. 簡易範例\n（1-2 個簡易計算範例的說明，若有程式則說明程式在 _code/ 中，並描述其輸出）\n\n同時在 _code/ 目錄（已存在）為每個有程式的章節建立 Python 檔，命名「章節-名稱.py」，如：\n- 05.1-cnn-conv2d.py\n- 05.2-scaled-dot-attention.py\n- 05.3-rope-rotation.py\n- 06.1-bigram-lm-perplexity.py\n- 06.2-ddpm-forward-denoise.py\n- 06.3-scaling-law-power.py\n\n程式要求：只用 numpy（不要 pytorch/matplotlib，保持簡單無依賴輸出）、純文字輸出、含中文註解（程式註解允許）。內容建議：numpy 手寫 2D 卷積驗證平移等變；numpy 實作 attention 並驗證 softmax 行和；RoPE 二維旋轉驗證內積只依賴相對位置；bigram 語言模型計算困惑度；1D DDPM 前向加噪＋簡單去噪軌跡；冪律外推與多步正確率 p^n 表格。每個程式執行後應印出數值驗證結果。\n\n必須用 bash 實際執行每個 .py 檔驗證可跑且輸出正確。\n\n完成後回報：每個檔案做了什麼補充、程式檔名、執行結果是否正確。",
  "subagent_type": "general"
}
```

**Error:**
```
Task cancelled
```

**Tool: task**

**Input:**
```json
{
  "description": "補充章節 07.x 08.x",
  "subagent_type": "general",
  "prompt": "工作目錄：/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書\n\n你要為一本數學書（神經網路數學史）的 4 個章節檔案，在最後「加上」一個「## 補充」章節。章節檔案（用 Read 讀取後用 Edit 在檔尾附加）：\n1. 07.1-MDP與貝爾曼方程.md（MDP、貝爾曼方程、壓縮映射、Q-learning）\n2. 07.2-策略梯度與PPO.md（REINFORCE、baseline、PPO clip、RLHF）\n3. 08.1-哈密頓神經網路與守恆學習.md（哈密頓方程、辛矩陣 J、HNN、leapfrog）\n4. 08.2-世界模型與隱空間規劃.md（編碼-動力學-策略、JEPA、MPC/CEM）\n\n每個檔案附加的「## 補充」格式（繁體中文，風格與原書一致，用 LaTeX 數學 $...$ / $$...$$）：\n\n## 補充\n\n### 1. 數學推導證明\n（1-2 個**新的**推導或證明，不要重複章節內已有的證明。可選章節習題中的證明題做完整推導，如：貝爾曼最佳算子 T* 也是 γ-壓縮；baseline 不改變策略梯度期望；斜對稱矩陣 aᵀJa=0；協方差正則化防止崩潰）\n\n### 2. 簡易範例\n（1-2 個簡易計算範例的說明，若有程式則說明程式在 _code/ 中，並描述其輸出）\n\n同時在 _code/ 目錄（已存在）為每個有程式的章節建立 Python 檔，命名「章節-名稱.py」，如：\n- 07.1-bellman-value-iteration.py\n- 07.2-reinforce-policy-gradient.py\n- 08.1-hamiltonian-pendulum-leapfrog.py\n- 08.2-latent-space-planning-cem.py\n\n程式要求：只用 numpy（不要 pytorch/matplotlib，保持簡單無依賴輸出）、純文字輸出、含中文註解（程式註解允許）。內容建議：兩狀態迷宮價值迭代收斂驗證（誤差每步乘 γ）；REINFORCE 在單狀態兩動作上策略上升（或小格子格世界簡例）；單擺 HNN 或純哈密頓方程用 leapfrog vs Euler 積分比較能量漂移；一維隱空間規劃窮舉/CEM 求最優行動。每個程式執行後應印出數值驗證結果。\n\n必須用 bash 實際執行每個 .py 檔驗證可跑且輸出正確。\n\n完成後回報：每個檔案做了什麼補充、程式檔名、執行結果是否正確。"
}
```

**Error:**
```
Task cancelled
```

---

## User

繼續

---

## Assistant (Build · Muse Spark 1.3 Free · 9.5s)

_Thinking:_



繼續完成剩餘 14 節。先確認已完成的部分，再逐批處理。

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "驗證 03.x/04.x 已完成的補充與程式",
      "status": "in_progress",
      "priority": "high"
    },
    {
      "content": "補充 01.1/01.2/02.1/02.2 + 4 個程式",
      "status": "pending",
      "priority": "high"
    },
    {
      "content": "補充 05.1/05.2/05.3 + 3 個程式",
      "status": "pending",
      "priority": "high"
    },
    {
      "content": "補充 06.1/06.2/06.3 + 3 個程式",
      "status": "pending",
      "priority": "high"
    },
    {
      "content": "補充 07.1/07.2/08.1/08.2 + 4 個程式",
      "status": "pending",
      "priority": "high"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "驗證 03.x/04.x 已完成的補充與程式",
    "status": "in_progress",
    "priority": "high"
  },
  {
    "content": "補充 01.1/01.2/02.1/02.2 + 4 個程式",
    "status": "pending",
    "priority": "high"
  },
  {
    "content": "補充 05.1/05.2/05.3 + 3 個程式",
    "status": "pending",
    "priority": "high"
  },
  {
    "content": "補充 06.1/06.2/06.3 + 3 個程式",
    "status": "pending",
    "priority": "high"
  },
  {
    "content": "補充 07.1/07.2/08.1/08.2 + 4 個程式",
    "status": "pending",
    "priority": "high"
  }
]
```

**Tool: bash**

**Input:**
```json
{
  "command": "ls -la _code/",
  "workdir": "/Users/Shared/ccc/115a/cccbook2026/科學與歷史/智慧模型/數學書"
}
```

**Output:**
```
total 144
drwxr-xr-x@ 20 cccuser  staff   640 Oct  9 17:32 .
drwxr-xr-x@ 25 cccuser  staff   800 Oct  9 17:15 ..
-rw-r--r--@  1 cccuser  staff  1932 Oct  9 17:25 01.1-mp-neuron-logic.py
-rw-r--r--@  1 cccuser  staff  2004 Oct  9 17:26 01.2-hebb-associative-memory.py
-rw-r--r--@  1 cccuser  staff  2318 Oct  9 17:29 02.1-perceptron-training.py
-rw-r--r--@  1 cccuser  staff  2420 Oct  9 17:28 02.2-gradient-descent.py
-rw-r--r--@  1 cccuser  staff  2321 Oct  9 17:36 03.1-relu-universal-approximation.py
-rw-r--r--@  1 cccuser  staff  3035 Oct  9 17:34 03.2-backprop-manual.py
-rw-r--r--@  1 cccuser  staff  1917 Oct  9 17:31 04.1-hopfield-energy.py
-rw-r--r--@  1 cccuser  staff  1458 Oct  9 17:32 04.2-softmax-temperature.py
-rw-r--r--@  1 cccuser  staff  1286 Oct  9 17:29 05.1-cnn-conv2d.py
-rw-r--r--@  1 cccuser  staff  1636 Oct  9 17:21 05.2-scaled-dot-attention.py
-rw-r--r--@  1 cccuser  staff  1430 Oct  9 17:21 05.3-rope-rotation.py
-rw-r--r--@  1 cccuser  staff  1784 Oct  9 17:22 06.1-bigram-lm-perplexity.py
-rw-r--r--@  1 cccuser  staff  1792 Oct  9 17:23 06.2-ddpm-forward-denoise.py
-rw-r--r--@  1 cccuser  staff  1635 Oct  9 17:23 06.3-scaling-law-power.py
-rw-r--r--@  1 cccuser  staff  1315 Oct  9 17:20 07.1-bellman-value-iteration.py
-rw-r--r--@  1 cccuser  staff  2661 Oct  9 17:35 07.2-reinforce-policy-gradient.py
-rw-r--r--@  1 cccuser  staff  1650 Oct  9 17:21 08.1-hamiltonian-pendulum-leapfrog.py
-rw-r--r--@  1 cccuser  staff  1634 Oct  9 17:31 08.2-latent-space-planning-cem.py

```

---

## Assistant (Build · Muse Spark 1.3 Free · 2.5s)

_Thinking:_



_code/ 

---

## User

繼續

---

## Assistant (Build · Muse Spark 1.3 Free · 3.1s)

---

## User

繼續

---

## Assistant (Build · GLM-5.3-Flash · 3.6s)

---

