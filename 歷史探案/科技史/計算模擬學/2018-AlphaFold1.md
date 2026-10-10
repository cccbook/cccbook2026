# 2018：AlphaFold 1——距離圖革命，折疊迷案初現裂縫

> 卷宗編號：AF-2018-CASP13。報案人：結構生物學界。案情：五十年未破的蛋白質折疊懸案，在第 13 屆 CASP 盲測現場出現一名神祕的新偵探。

## 案發現場

時間是 2018 年 12 月，地點是 CASP13（Critical Assessment of Structure Prediction）盲測會場。

蛋白質折疊問題盤踞懸案榜首已超過半世紀：已知胺基酸序列，能否算出三維結構？Anfinsen 證明序列決定結構，Levinthal 卻算出窮舉構象要花上宇宙年齡。現場慘狀如下：

- 最難的自由建模（FM）類別，最佳方法的  $GDT$  分數長期在 40 分上下浮動，形同在濃霧中摸象。
- 物理派（分子動力學）算不動大蛋白；知識派（Rosetta 片段組裝）靠碎片拼圖，遇到無同源模板的新折疊就束手無策。
- 基因定序如雪崩，序列資料庫暴漲，但實驗解析結構（X 光、冷凍電鏡）緩慢昂貴，序列—結構鴻溝越裂越大。

就在此時，DeepMind 派出的 AlphaFold 1 初登場，便以平均  $GDT$  約 70 的成績橫掃 FM 類別，把第二名甩開一大截。全場譁然：這名新手，到底在案發現場看到了什麼別人沒看到的東西？

## 偵查過程（含數學式/表格/理論）

AlphaFold 1 團隊的偵查筆記，開頭只寫了一句話：「不要直接猜座標，先猜距離。」

### 靈感一：共演化是殘留的指紋

偵探回頭翻閱舊卷宗：若兩個殘基在空間中相鄰，一處突變會迫使另一處補償突變。把大量同源序列排成多序列比對（MSA），共演化耦合就是折疊留下的間接指紋。傳統直接耦合分析（DCA）用 Potts 模型擬合，但雜訊大、只能給接觸與否的二值判斷。

AlphaFold 1 的突破是：把共演化訊號交給深層殘差網路（ResNet），直接預測殘基對距離的完整機率分布  $P(d_{ij}|MSA)$ ，而非二元接觸圖。

### 靈感二：距離圖比接觸圖誠實

接觸圖只說「近或不近」，距離圖說「有多近、信心多高」。網路輸出對每對殘基  $i$  與  $j$ ，把 2–22 埃切成 64 個區間，外加一個大於 22 埃的區間，輸出離散分布：

$$
P(d_{ij} = b_k | MSA) = \mathrm{softmax}(f_{\theta}(MSA))_k
$$

其中  $f_{\theta}$  為深層 ResNet（約 220 個殘差塊、空洞卷積擴大感受野），輸入為 MSA 統計特徵與成對特徵， $b_k$  為第  $k$  個距離區間， $\theta$  為網路參數。

同時另一個網路頭預測二面角分布  $P(\phi_i,\psi_i|MSA)$ ，提供主鏈扭轉的先驗。

### 靈感三：把機率變成能量，再折疊

偵查的關鍵轉折，是把深度學習的輸出翻譯成物理學聽得懂的語言——勢能。對候選結構  $x$ ，構造統計勢：

$$
V(x) = -\sum_{i<j} \log P(d_{ij}(x)|MSA) - \sum_i \log P(\phi_i,\psi_i|MSA) + V_{vdw}(x)
$$

其中  $d_{ij}(x)$  為結構  $x$  中殘基對距離， $V_{vdw}(x)$  為防止原子碰撞的凡得瓦排斥項。於是折疊變成最佳化問題：用梯度下降＋模擬退火在可微勢能面上尋找最低點，產生多個候選再聚類取共識。

| 偵查工具 | 傳統做法 | AlphaFold 1 的新招 |
|----------|----------|---------------------|
| 輸入訊號 | 單序列或薄 MSA | 深 MSA＋共演化統計＋成對特徵 |
| 預測目標 | 接觸與否（0/1） | 距離分布  $P(d_{ij}|MSA)$ （64 區間） |
| 網路 | 淺層 CNN | 深層 ResNet＋空洞卷積 |
| 折疊手段 | 片段組裝抽樣 | 可微勢能＋梯度最佳化 |
| CASP13 FM 平均  $GDT$  | 約 40 | 約 70 |

一言以蔽之：AlphaFold 1 不是更會猜結構，而是把「演化留下的距離證詞」先重建出來，再讓物理去結案。

## 結案報告

CASP13 結果公布：AlphaFold 1 在 43 個 FM 目標中拿下 25 個第一，平均  $GDT$  約 70，意味著拓撲基本正確。這是折疊懸案第一次出現結構性鬆動。

但本案並未完全偵破：

- 模型仍是「兩段式」：神經網路只負責預測約束，真正的三維組裝仍靠傳統最佳化，端到端尚未打通。
- 側鏈精度不足，距離區間顆粒粗，物理勢能面仍有雜訊。
- 高度依賴深 MSA；序列孤兒（同源序列稀少）依然難解。

儘管如此，AlphaFold 1 證明了一件事：摺疊問題不是物理不對，而是約束不夠。當距離圖被高精度重建，Levinthal 的組合爆炸便不攻自破。兩年後，更徹底的偵探即將登場——那就是 AlphaFold 2。

### 卷末附記：三個未結之問

結案不等於完結。AlphaFold 1 在卷宗末頁留下三個問號，指引後續偵查方向：

- 第一問：距離分布的 64 個區間是人為切分，能否讓網路直接回歸連續距離，甚至直接輸出三維座標？
- 第二問：MSA 只是靜態輸入，若讓網路在推理中動態提煉 MSA，共演化訊號會不會更乾淨？
- 第三問：梯度下降＋退火的後端最佳化又慢又糙，能否把整個折疊過程做成可微分的端到端網路？

這三問的答案，全寫在下一份卷宗（2020 年 AlphaFold 2）的封面上。而 CASP 主席團也開始擔心：盲測競賽的計分板，會不會從此只剩一個名字？

## 證據與工具

- 關鍵方程：距離分布預測  $P(d_{ij}|MSA)$  、統計勢  $V(x)$  、交叉熵損失對距離區間分類訓練。
- 核心工具：ResNet＋空洞卷積、MSA 構建（HHblits / JackHMMER）、GDT-TS 評分、梯度下降＋退火折疊流程。
- 延伸閱讀線索：CASP13 官方評估報告、Senior 等人 2020 年 Nature 論文《Improved protein structure prediction using potentials from deep learning》、DCA 與 Potts 模型文獻。
- 給讀者的動手實驗：取一個 Pfam 家族的 MSA，計算兩列間的互訊息，觀察接觸對的共演化訊號；再思考為何分布預測比二值接觸更利於最佳化。

| 關鍵超參數 | 取值 | 備註 |
|------------|------|------|
| 距離區間數 | 64＋1 | 2–22 埃等寬，外加溢出區間 |
| 殘差塊數 | 約 220 | 空洞卷積，感受野覆蓋全鏈 |
| 折疊採樣 | 多次退火＋聚類 | 取共識結構為最終答案 |
| 評分標準 | GDT-TS | FM 類別平均約 70 即為橫掃 |

- 術語對照：FM（自由建模，無模板）、 $GDT$ （整體距離測試分數）、DCA（直接耦合分析）、MSA（多序列比對）。
- 時間線：1994 年 CASP 開幕 → 1999 年 Rosetta → 2018 年 AF1 → 2020 年 AF2，詳見本目錄 README 的因果鏈總覽。

## 補充：程式實作

對應程式：[2018-contact_mi_toy.py](_code/2018-contact_mi_toy.py)

本節以玩具 MSA 重演本文核心理論：共演化位點對的互訊息 $MI(i,j)$ 顯著偏高，暗示空間接觸，正是 DCA 與 AlphaFold 1 距離預測的源頭思想。

程式生成 200 條、10 位點、字母表大小為 4 的隨機比對，並在位點 2 與 8 植入 95% 相同字母的共演化訊號，再計算完整的互訊息矩陣。

判讀標準呼應 $P(d_{ij}|MSA)$ 的精神：真接觸的統計訊號必須鶴立雞群，最大值需超過次大值 2 倍以上，否則後續的勢能最佳化無從下手。

執行方式：

```bash
python3 _code/2018-contact_mi_toy.py
```

實測關鍵輸出（本次真實執行結果抄錄）：

```text
MSA: 200 條 × 10 位點, q=4, 植入共演化位點 (2, 8)
  MI[2,8] = 1.1150
  MI[0,9] = 0.0585
最大 MI[2,8]=1.1150, 次大 MI[0,9]=0.0585, 比值=19.06 (要求>2)
VERIFICATION: MI28=1.1150 second=0.0585 ratio=19.06 PASS
```

數字解讀：植入的共演化對互訊息高達 1.1150 nats ，次大背景值僅 0.0585 ，比值達 19.06 倍，遠超 2 倍門檻，訊號乾淨俐落。

其餘位點對的 $MI$ 值全在 0.06 以下浮動，恰如真實 MSA 中大量非接觸對的雜訊海，唯有真兇浮出水面。

指紋比對成功：演化留在比對中的那枚指紋，互訊息一眼就認出來了，全案從此可結。

讀者可改序列數 $NSEQ$ （如 50 或 500 ）或雜訊率 $NOISE$ 做實驗，觀察比值如何隨資料量消長。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""2018 玩具 MSA 互資訊接觸預測 (對應 wiki：計算模擬學 / 蛋白質共演化・DCA/互資訊)。

背景：Morcos 等 (2011) DCA、Marks 等 (2011) EVfold：MSA 中共演化位點對
互資訊 (MI) 高，暗示空間接觸。此處玩具 MSA：200 條序列、10 位點、字母表 q=4，
預設位點 2 與 8（0-based）共演化（95% 相同字母），其餘獨立均勻。
計算 10×10 MI 矩陣（nats），驗證 MI[2,8] 為最大值且超過次大值 2 倍以上。

只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(2018)

NSEQ, L, Q = 200, 10, 4
PAIR = (2, 8)
NOISE = 0.05


def compute_mi(msa):
    n, L = msa.shape
    mi = np.zeros((L, L))
    for i in range(L):
        for j in range(i + 1, L):
            joint = np.zeros((Q, Q))
            for a in range(n):
                joint[msa[a, i], msa[a, j]] += 1
            joint /= n
            pi = joint.sum(axis=1, keepdims=True)
            pj = joint.sum(axis=0, keepdims=True)
            m = 0.0
            for a in range(Q):
                for b in range(Q):
                    if joint[a, b] > 0:
                        m += joint[a, b] * np.log(joint[a, b] / (pi[a, 0] * pj[0, b]))
            mi[i, j] = mi[j, i] = m
    return mi


def main():
    msa = np.random.randint(0, Q, size=(NSEQ, L))
    # 植入共演化：位點 2、8 以 95% 機率取相同字母
    for s in range(NSEQ):
        val = np.random.randint(0, Q)
        msa[s, PAIR[0]] = val
        if np.random.rand() > NOISE:
            msa[s, PAIR[1]] = val
        else:
            msa[s, PAIR[1]] = np.random.randint(0, Q)

    mi = compute_mi(msa)
    # 找最大與次大（上三角、排除對角線）
    triu = [(mi[i, j], i, j) for i in range(L) for j in range(i + 1, L)]
    triu.sort(reverse=True)
    (m1, i1, j1), (m2, i2, j2) = triu[0], triu[1]
    ratio = m1 / (m2 + 1e-12)

    print(f"MSA: {NSEQ} 條 × {L} 位點, q={Q}, 植入共演化位點 {PAIR}")
    print("MI 矩陣 (nats, 取上三角前幾大):")
    for val, i, j in triu[:5]:
        print(f"  MI[{i},{j}] = {val:.4f}")
    print(f"最大 MI[{i1},{j1}]={m1:.4f}, 次大 MI[{i2},{j2}]={m2:.4f}, 比值={ratio:.2f} (要求>2)")
    ok = ((i1, j1) == PAIR) and (ratio > 2.0)
    assert ok, "MI 驗證失敗"
    print(f"VERIFICATION: MI28={m1:.4f} second={m2:.4f} ratio={ratio:.2f} PASS")


if __name__ == "__main__":
    main()
```
