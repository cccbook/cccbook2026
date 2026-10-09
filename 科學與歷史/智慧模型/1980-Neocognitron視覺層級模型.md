# 1980 - Neocognitron 視覺層級模型

## 案件摘要

1980 年，NHK 的日本科學家福島邦彥（Kunihiko Fukushima）發表 Neocognitron——史上第一個完整的多層視覺層級神經網路，具備「S-cell/C-cell 交替層級」與平移不變性。它的架構直接取材自 Hubel 與 Wiesel 的視覺皮層研究（見「1959-HubelWiesel視覺皮層.md」）：

$$\text{S-cell（簡單細胞）}: \text{特徵偵測}，\quad \text{C-cell（複雜細胞）}: \text{局部 pool} \Rightarrow \text{平移不變}$$

這正是今日卷積神經網路（CNN）的核心公式：卷積層（S）+ 池化層（C）的交替堆疊。Neocognitron 是寒冬天中被凍結的寶石（見「1969-MinskyPapert批判.md」）——它證明了多層視覺層級可行，卻因缺乏反向傳播的加持而沈睡，直到 LeCun（見「1989-LeCunCNN手寫辨識.md」）與 AlexNet（2012）為它翻案。

## 前因 -- 為什麼會有這個案子

- 1959–1962 年，Hubel 與 Wiesel 在貓的視覺皮層發現簡單細胞與複雜細胞的層級結構（見「1959-HubelWiesel視覺皮層.md」）：簡單細胞對特定方向的邊緣敏感，複雜細胞在其接受野內平移後依然反應——這是生物視覺的「層級 + 不變性」鐵證。
- Rosenblatt 的感知器（見「1957-Perceptron感知器.md」）是單層的，無法表達層級特徵；1969 年 Minsky & Papert 的批判（見「1969-MinskyPapert批判.md」）讓連結派研究在西方幾乎停擺。
- 福島邦彥在 1969 年發表了更早的「Cognitron」（自我組織的多層網路），Neocognitron 是其監督式、更精緻的後繼者——他的動機是純粹生物學的：**用網路重現視覺皮層的架構**。
- 日本的連結派研究未受 Minsky & Papert 的寒冬天重創，NHK 放送科學基礎研究所提供了自由的研究環境——線索因此飄洋過海被保存下來。
- 1969 年《Perceptrons》已證明多層網路的表達能力不是問題，缺的是訓練演算法（見「1974-Werbos反向傳播先驅.md」）；福島選擇繞過這個問題：用**監督式的「插值訓練」**直接設定 S-cell 的權重，而非梯度學習。
- 當時的模式辨識主流是統計方法（特徵提取 + 分類器），特徵由人類手工設計——福島的遠見在於**讓特徵由網路層級自動形成**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：S-cell / C-cell 交替層級——卷積架構的遠祖

Neocognitron 的層級結構：$U_0 \to U_{S1} \to U_{C1} \to U_{S2} \to U_{C2} \to \cdots$，S 層與 C 層交替堆疊：

| 層 | 生物對應 | 功能 | 現代 CNN 對應 |
|---|---|---|---|
| S-cell | 簡單細胞（simple cell） | 局部特徵偵測（邊緣、線段） | 卷積層（convolution） |
| C-cell | 複雜細胞（complex cell） | 局部位置容錯（pooling） | 池化層（pooling） |
| 層級 | V1 → V2 → V4 → IT | 特徵越來越抽象、越來越不變 | 深度層級 |

S-cell 的輸入輸出關係是現代卷積層的雛形：

$$u_{S}(x, k) = \phi\!\left( \sum_{k'} a_{k}(x, k')\, u_{C}(x + \delta, k') - \theta_k \right)，\quad \phi(z) = \begin{cases} \dfrac{z}{1+z} & z > 0 \\ 0 & z \le 0 \end{cases}$$

其中 $a_k$ 是連接權重（**空間上共享**——同一特徵在不同位置使用同一組權重，這就是權重共享的起源），$\theta_k$ 是閾值，$\delta$ 遍歷局部接受野。

### 第二條線索：平移不變性——C-cell 的數學

C-cell 對其接受野內的所有 S-cell 取「模糊 OR」：

$$u_C(x, k) = \psi\!\left( \sum_{\delta \in R} c(\delta)\, u_S(x + \delta, k) \right)，\quad \psi(z) = \frac{z}{1+z}$$

只要特徵在接受野 $R$ 內的任何位置出現，C-cell 就會反應。層級堆疊的不變性範圍逐層擴大：

$$\text{S1/C1 不變於幾像素平移} \quad \Rightarrow \quad \text{S4/C2 不變於大幅平移與形變}$$

這正是 Hubel & Wiesel 層級假說的數學化身——也是今天 CNN 中「卷積 + 池化」交替堆疊能對平移、縮放、微小形變保持穩健的原理。

### 第三條線索：監督式插值訓練——繞過梯度迷宮

福島不用梯度下降（反向傳播尚未被西方承認，見「1974-Werbos反向傳播先驅.md」），而用「插值學習」（interpolating learning）：呈現訓練樣本時，挑出反應最強的 S-cell，直接**把輸入設為其權重**：

$$a_k \leftarrow \frac{u_{C}}{\sum_j u_{C,j}} \quad \text{（ winner-take-all 的直接賦值）}$$

這是簡單卻有效的自我組織：特徵逐層形成，無需計算梯度。對照兩條路線：

| | Neocognitron（1980） | LeCun CNN（1989） |
|---|---|---|
| 架構 | S/C 交替層級 | 卷積 + 池化層級 |
| 訓練 | 插值賦值（winner-take-all） | 反向傳播 + 梯度下降 |
| 權重共享 | 有 | 有 |
| 命運 | 被埋沒 | 統治視覺 AI 三十年 |

架構幾乎相同，命運天壤之別——差別在**訓練演算法**。

### 第四條線索：手寫數字的先聲

福島用 Neocognitron 辨識手寫數字（0–9）與簡單圖形，展示對平移與形變的穩健性——這正是九年後 LeCun 用 CNN 解決的同一問題（見「1989-LeCunCNN手寫辨識.md」）。其輸出層採「winner-take-all」：

$$\text{類別} = \arg\max_k \ u_{C_{\text{final}}}(k)$$

線索的完整鏈條因此貫穿：Hubel & Wiesel（生物）→ Fukushima（架構）→ LeCun（訓練 + 工程化）→ AlexNet（2012，GPU 加持的勝利）。

## 結案 -- 後果與影響

- Neocognitron 是卷積神經網路的直接遠祖：LeCun 的 1989 年手寫辨識 CNN（見「1989-LeCunCNN手寫辨識.md」）與 1998 年 LeNet-5 的架構可追溯到 S/C 層級——LeCun 本人多次承認這一血緣。
- 「權重共享 + 層級特徵 + 平移不變性」三原則成為深度視覺模型的基石，2012 年 AlexNet 以 GPU + 反向傳播重現這個架構並贏得 ImageNet（見「科學與歷史/人工智慧/」與「科學與歷史/神經網路/」下對應檔案）——深度學習革命就此引爆。
- 平移不變性的思想延伸到 2017 年的 Vision Transformer：即使 Transformer 捨棄卷積，位置編碼與層級特徵的問題設定依然源自福島的框架。
- 生物視覺層級（V1→V2→V4→IT）與深度網路層級的對應，至今仍是計算神經科學的活躍研究題目——Neocognitron 是兩個學科之間最早的正式橋樑。
- 悲劇與教訓：福島在寒冬天獨立保存了架構線索，卻因缺乏反向傳播的訓練引擎而無法與統計方法競爭；本案再次證實「1974-Werbos反向傳播先驅.md」的教訓——**正確的架構 + 缺失的訓練法 = 被埋沒**。
- 伏筆：福島的 S/C 層級 + Werbos 的 BPTT + Hinton 的深度信念網路（見「1982-Hopfield網路能量函數.md」的結案）三線匯聚，將在 2012 年引爆深度學習盛世——所有能承載智能的模型中，視覺層級模型是第一個被翻案的寒冬天寶石。

## 關鍵人物與文獻

- 福島邦彥（Kunihiko Fukushima）—— Cognitron 與 Neocognitron 設計者，NHK 放送科學基礎研究所
- Hubel & Wiesel —— 視覺皮層研究，1981 年諾貝爾生理醫學獎（見「1959-HubelWiesel視覺皮層.md」）
- Fukushima, "Neocognitron: A self-organizing neural network model for a mechanism of pattern recognition unaffected by shift in position", *Biological Cybernetics*, 1980
- Fukushima, "Cognitron: A self-organizing multilayered neural network", *Biological Cybernetics*, 1975
- Hubel & Wiesel, "Receptive fields, binocular interaction and functional architecture in the cat's visual cortex", *J. Physiology*, 1962
- LeCun et al., "Backpropagation applied to handwritten zip code recognition", *Neural Computation*, 1989（見「1989-LeCunCNN手寫辨識.md」）
- 相關案件：1957-Perceptron感知器.md、1959-HubelWiesel視覺皮層.md、1969-MinskyPapert批判.md、1974-Werbos反向傳播先驅.md、1982-Hopfield網路能量函數.md、1989-LeCunCNN手寫辨識.md
