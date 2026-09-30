# 1975 - Levin 獨立發現 NP-完備

## 案件摘要
1971 年，Cook 在北美與 Levin 在蘇聯幾乎同時、互不知情地發現了「NP-完備」這一核心概念。Levin 因蘇聯學界資訊封鎖遲至 1973 年才知 Cook 的結果，其論文 1975 年以英文譯本問世。最終史學界以「Cook–Levin 定理」並稱兩人，承認這是一樁冷戰下的獨立雙重發現。

## 前因 -- 為什麼會有這個案子
- 1956 年起蘇聯已有 Bruto Zhukhor 關於「列舉搜索」的前驅工作（甚至早於 Cobham 與 Edmonds 1965 的多項式時間定義）。
- 1960 年代末，計算複雜度理論成形：多項式時間被公認為「可行」的數學刻劃。
- 冷戰鐵幕使蘇聯與西方學界幾乎隔絕：期刊延遲數年、會議難以參加。
- Levin（25 歲，Kolmogorov 的學生）在莫斯科思考：「搜索問題何時本質上困難？」——這正是 Cook 對 SAT 的同一個提問。

## 線索與推理 -- 數學式、程式、理論
### Cook（1971）的表述
Cook 在 STOC 1971 提出：
$$\text{SAT} \in \text{P} \iff \text{P} = \text{NP}$$
並定義「多項式歸約」$A \leq_p^T B$，指出 SAT 是 NP 中「最難」的問題。

### Levin（1971 口頭發表 / 1975 論文）的表述
Levin 1971 年在莫斯科演講中口頭報告，1973 年以俄文發表於《Проблемы передачи информации》（問題傳輸資訊期刊），題為 *Universal Search Problems*（Универсальные задачи перебора），英文譯本 1975 年刊出。

Levin 不用「NP-完備」術語，而用「通用搜索問題」（universal search problem）：

**Levin 的定義（現代轉述）**：一個大量問題（mass problem）$\Pi$ 由可計算的謂詞 $R(x, y)$ 給定——給定輸入 $x$，要找證書 $y$ 使 $R(x,y)$ 成立。若存在多項式 $p$ 使得驗證 $R(x,y)$ 只需 $p(|x|)$ 時間，且存在問題 $\Pi_0$（如 SAT）滿足：
$$\Pi_0 \leq_{\text{Red}} \Pi \implies \Pi \text{ 是通用問題}$$
則稱 $\Pi$ 為通用的。Levin 證明：**六個問題是通用的**：

1. SAT（布爾可滿足性）
2. 整數線性規劃
3. 圖同構的補（非同構性）
4. 3-著色問題
5. 子圖同構（團問題）
6. 磚牆鋪砌（tiling）問題

Levin 的證明思路與 Cook 不同：他不經過圖靈機編碼的細節，而直接用「搜索問題的組合結構」+ 與通用枚舉器的歸約，更接近現代教科書的歸約講法。

### 模擬 Levin 式歸約：3-著色 ≤p SAT
```python
# 3-著色歸約到 SAT：每個頂點 v 與顏色 c 對應變數 x[v][c]
def three_color_to_sat(vertices, edges, k=3):
    clauses = []
    # 每個頂點至少一色
    for v in vertices:
        clauses.append([f"x_{v}_{c}" for c in range(k)])
    # 每個頂點至多一色（兩兩互斥）
    for v in vertices:
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                clauses.append([f"-x_{v}_{c1}", f"-x_{v}_{c2}"])
    # 相鄰頂點顏色不同
    for (u, w) in edges:
        for c in range(k):
            clauses.append([f"-x_{u}_{c}", f"-x_{w}_{c}"])
    return clauses
```
這正是 Levin 六個通用問題之間互相歸約的精神：**把「找解」翻譯成「找滿足賦值」**。

### 理論定義（現代教科書版，Cook–Levin 定理）
$$\text{Cook--Levin 定理：}\quad \text{SAT 是 NP-完備的}$$
即：(1) $\text{SAT} \in \text{NP}$；(2) 對任意 $L \in \text{NP}$，$L \leq_p \text{SAT}$。

## 結案 -- 後果與影響
- **優先權爭議**：誰先？Cook 1971 年 5 月在 STOC 正式發表；Levin 1971 年在莫斯科口頭發表、1973 俄文見刊、1975 英文譯本。史學界（如 Sipser 1992 的歷史註記）裁定為**獨立發現**，並稱「Cook–Levin 定理」。
- **資訊不對稱**：Levin 遲至 1973 年（經 Trakhtenbrot 告知）才知道 Cook 的結果，當時自己的論文已投稿。蘇聯學界則晚數年才理解 NP-完備理論的全貌。
- Levin 後於 1970 年代末移民美國（因政治異見被解職），成為波士頓大學教授，持續貢獻（如 1986 年又獨立提出平均情況複雜度，與 Impagliazzo 並稱）。
- Karp 1972 的 21 個 NP-完備問題接續 Cook，建立歸約的「產業標準」，NP-完備理論迅速席捲整個計算機科學。

## 關鍵人物與文獻
- **Stephen Cook**（多倫多大學）："The Complexity of Theorem-Proving Procedures", STOC 1971。
- **Leonid Levin**（莫斯科 → 波士頓大學）："Universal Search Problems", Проблемы передачи информации, 1973（俄文）；英譯 1975, 9(3):265–266。
- **Richard Karp**："Reducibility Among Combinatorial Problems", 1972。
- Sipser, "The History and Status of the P versus NP Question", STOC 1992（權威歷史梳理）。
- Trakhtenbrot, "A Survey of Russian Approaches to Perebor", Annals of the History of Computing, 1984。
