# 1953 Watson-Crick DNA 雙螺旋

## 案發現場

1950 年代初，生物學最重要的懸案只有一個：**遺傳物質 DNA 的結構是什麼？** 線索已經堆積如山，卻拼不出圖像：

1. **DNA 是遺傳物質**：1944 年 Avery 的轉化實驗、1952 年 Hershey-Chase 的噬菌體實驗確認攜帶遺傳訊息的是 DNA 而非蛋白質。
2. **鹼基比例之謎（Chargaff 規則）**：1950 年 Chargaff 測得各種生物 DNA 中，腺嘌呤（A）的量總等於胸腺嘧啶（T），鳥糞嘌呤（G）總等於胞嘧啶（C）：

$$[\mathrm{A}] = [\mathrm{T}], \qquad [\mathrm{G}] = [\mathrm{C}]$$

為什麼如此成對？沒有人知道。
3. **X 射線繞射**：倫敦國王學院的 Rosalind Franklin 與 Maurice Wilkins 拍出了史上最清晰的 DNA 纖維繞射圖——著名的 Photo 51 顯示清晰的 X 形交叉紋與強烈的子午線反射，暗示螺旋結構與特定螺距，但圖像的完整解讀尚未完成。
4. **結構組件**：核酸化學家已確定 DNA 由去氧核糖、磷酸與四種鹼基組成，磷酸骨架在外面。

誰能先拼出 DNA 的三維結構，誰就解開遺傳的秘密。劍橋卡文迪許實驗室的年輕人華生（James Watson, 1928–）與克里克（Francis Crick, 1916–2004）接下了這個案子——而他們最大的競爭對手，正是剛破解蛋白質 $\alpha$-螺旋的鮑林（見 [1951-Pauling螺旋結構.md](1951-Pauling螺旋結構.md)）。

## 偵查過程

**第一步：Photo 51 的情報。** 1953 年初，Wilkins 在未經 Franklin 同意的情況下，把 Photo 51 給了 Watson 看。Watson 一眼看出：清晰的 X 形繞射紋是**螺旋**的鐵證，而且子午線上的強反射給出螺距與直徑的數據：螺旋直徑約 20 Å、每圈螺距約 34 Å、每圈約 10 個鹼基對。Franklin 更早的定量分析還指出磷酸骨架在**外側**——這是關鍵情報。

**第二步：模型的試錯。** Watson 與 Crick 用金屬片搭建分子模型（同樣是「理論偵探 + 紙上偵查」的手法）。第一版模型（三螺旋、骨架在內）被 Franklin 的數據否決——骨架在外、含水量也對不上。鮑林的錯誤三螺旋模型（1953 年初寄出論文預印本）反而成了警鐘：不能只靠漂亮模型，必須符合全部化學與繞射數據。

**第三步：鹼基配對（破案關鍵）。** Chargaff 的 A=T、G=C 比例是最大的謎。破案靈感來自兩處：一是 Jerry Donohue 指出 Watson 用了錯誤的酮式/烯醇式互變異構體——用**酮式**才能正確配對；二是 Watson 意識到 A 與 T 之間恰好能形成**兩個氫鍵**、G 與 C 之間形成**三個氫鍵**，且配對後兩對的幾何尺寸幾乎相同：

$$\mathrm{A = T} \ (\text{雙氫鍵}), \qquad \mathrm{G \equiv C} \ (\text{三氫鍵})$$

嘌呤配嘧啶，寬度固定——**螺旋的直徑才能恆定為 20 Å**！Chargaff 比例之謎的答案呼之欲出：A 配 T、G 配 C，是幾何與氫鍵的必然。

**第四步：反向平行雙螺旋。** 兩條骨架以**反向平行**（antiparallel）方式纏繞，每 34 Å 轉一圈、10 個鹼基對，鹼基對平疊在螺旋內部（鹼基堆疊作用提供額外穩定），疏水的鹼基藏內、親水的骨架朝外。1953 年 4 月 25 日，Nature 上三篇論文同時發表：Watson-Crick 的結構論文（一頁多！）、Wilkins 與 Franklin 的繞射數據論文。論文的最後一句成為科學史上最著名的伏筆：

> 「我們注意到的這種配對方式，直接暗示了遺傳物質可能的複製機制。」

## 結案報告

1962 年 Watson、Crick 與 Wilkins 獲諾貝爾生醫獎。而最令人遺憾的是 Rosalind Franklin——她 1958 年死於卵巢癌（年僅 37 歲，很可能與 X 射線暴露有關），諾貝爾獎不追授逝者，她的關鍵貢獻數十年來被嚴重低估，近年才獲得遲來的公認。

DNA 雙螺旋引發的分子生物學革命：

1. **半保留複製**：Watson-Crick 配對直接預言複製機制，1958 年 Meselson-Stahl 實驗證實。
2. **中心法則**：DNA → RNA → 蛋白質的訊息流動框架，遺傳密碼在 1960 年代破解。
3. **結構決定功能**：雙螺旋的互補性解釋了遺傳、突變、重組——分子生物學正式誕生。
4. **生物技術**：基因工程、PCR、定序、CRISPR，全部站立在雙螺旋的地基上；也呼應了後來計算生物學的發展（見 [1995-計算化學.md](1995-計算化學.md)）。

## 證據與工具

```python
# 驗證 Chargaff 規則與鹼基配對：氫鍵數與分子寬度
import numpy as np

# 模擬一段隨機 DNA 序列，檢驗 Chargaff 規則（A=T, G=C）
rng = np.random.default_rng(7)
bases = list("ATGC")
seq = "".join(rng.choice(bases, 10000))
counts = {b: seq.count(b) for b in bases}
print("Chargaff 規則檢驗（10000 個隨機鹼基）：")
print(f"  A = {counts['A']}, T = {counts['T']}  → 相等？{counts['A']==counts['T']}")
print(f"  G = {counts['G']}, C = {counts['C']}  → 相等？{counts['G']==counts['C']}")

# 鹼基配對：互補配對函數（氫鍵數）
complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
h_bonds = {"A": 2, "T": 2, "G": 3, "C": 3}

def complement_strand(seq):
    """產生反向平行的互補股"""
    return "".join(complement[b] for b in reversed(seq))

demo = "ATGCGTA"
print(f"\n範例序列      5'-{demo}-3'")
print(f"互補股(反平行) 3'-{complement_strand(demo)}-5'")

total = sum(h_bonds[b] for b in zip(demo, complement_strand(demo)[::-1]) 
            for b in [b[0]])
print(f"此段鹼基對氫鍵總數 = {sum(h_bonds[b] for b in demo)}")

# 幾何驗證：嘌呤(A/G)配嘧啶(T/C) → 配對寬度恆定
purines, pyrimidines = "AG", "TC"
pairs = ["A-T", "G-C", "T-A", "C-G"]
print("\n配對寬度檢驗（嘌呤-嘧啶 → 寬度恆定，螺旋直徑 20 Å 才能維持）：")
for p in pairs:
    a, b = p.split("-")
    ok = (a in purines and b in pyrimidines) or (a in pyrimidines and b in purines)
    print(f"  {p}: 嘌呤-嘧啶？{ok}，氫鍵數 {h_bonds[a]}")
```
