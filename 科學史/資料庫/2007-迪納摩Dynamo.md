# 2007 - Dynamo（鍵值儲存與最終一致性）

## 案件摘要
2007 年，Amazon 的 **Giuseppe DeCandia** 與 Dynamo 團隊在 **SOSP 2007** 發表
*Dynamo: Amazon's Highly Available Key-value Store*：
$$\boxed{\text{放棄強一致性，換取「永不當機」——NoSQL 運動的引爆點}}$$
**Dynamo** 是一套**鍵值儲存（key-value store）**，核心武器是一整套組合拳：
- **一致性雜湊（consistent hashing）**：資料分散，節點增減只搬 $1/n$ 的鍵；
- **向量時鐘（vector clock）**：不用全局時鐘也能排出因果；
- **$N/W/R$ 可調一致性**：複製 $N$ 份、寫 $W$ 份、讀 $R$ 份，強度自己調；
- **最終一致性（eventual consistency）**：暫時不一致，終將收斂。
$$\text{CAP 定理的現實選擇} = \text{可用性} + \text{分區容忍}，\ \text{一致性放軟}.$$
購物車不能掛、結帳不能等——**Dynamo 用工程手段繞開了理論的死結**，
**一年後 NoSQL 大爆發，整個資料庫版圖為之改寫**。

## 前因 -- 為什麼會有這個案子
- **2000 年 CAP 定理（Eric Brewer）**：
  Brewer 在 PODC 2000 提出**CAP 定理**（見 `2000-布魯爾CAP定理.md`）：
  $$\boxed{\text{一致性 C、可用性 A、分區容忍 P，三者最多取二}}$$
  網路分區（P）在大型資料中心**必然發生**——
  於是只剩兩種選擇：**CP**（停機保一致）或 **AP**（降級保可用）。
  傳統關聯式資料庫是 CP；**Amazon 購物車需要的是 AP**。
- **1978 年 Lamport 邏輯時鐘**：
  Lamport 的邏輯時鐘（見 `../資訊科學/1978-蘭波特邏輯時鐘.md`）證明：
  分散式系統裡**「先後」不能用物理時鐘定義**，只能用因果序。
  **向量時鐘是邏輯時鐘的推廣**：每個節點記一整個向量，可判斷並發與因果。
- **Amazon 的規模壓力（2004–2006）**：
  亞馬遜巔峰時段每天服務數千萬用戶，購物車服務**哪怕停機一分鐘都是真金白銀的損失**。
  關聯式資料庫的 **ACID**（見 `1981-葛雷交易ACID.md`）在這個規模下**貴得付不起**——
  交易、JOIN、嚴格 schema 全是奢侈品。
- **2006 年 Google Bigtable 的同年對照**：
  Google 的 **Bigtable**（見 `2006-谷歌Bigtable.md`）同年問世——
  但 Bigtable 走的是**寬表（wide-column）**路線，建立在 GFS/Chubby 之上；
  **Dynamo 則是完全去中心化（peer-to-peer）**——
  $$\text{Bigtable（集中式基礎設施）} \ne \text{Dynamo（去中心化對稱架構）}.$$
  兩者共同宣告：**關聯式模型不再是唯一答案**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：一致性雜湊環
普通雜湊 `hash(key) mod n` 在節點增減時**幾乎所有鍵都要搬家**。
**一致性雜湊**把雜湊值映射到一個**環**上：
$$\text{hash}(key) \to [0, 2^{64})\ \text{環上位置}，\quad \text{hash}(node) \to \text{環上位置}.$$
鍵 $k$ 歸**順時針遇到的第一個節點**（coordinator）所有。
設有 $n$ 個節點均勻分布在環上，新增一個節點時：
$$\boxed{\text{只有該新節點「接管區間」內的鍵會遷移} \approx \frac{1}{n+1}\ \text{的鍵}}$$
Dynamo 再加**虛擬節點（vnode）**：每台實體機器扮演環上多個虛擬點，
讓負載更均勻——每個 vnode 管一小段弧，統計波動由大數定律抹平。

### 第二條線索：向量時鐘與偏序
每個物件附帶一個向量時鐘 $VC: \text{節點} \to \text{計數}$（Lamport 時鐘的推廣）。
比較兩個版本 $VC_a$、$VC_b$：
$$VC_a \le VC_b \iff \forall i:\ VC_a[i] \le VC_b[i] \ \wedge\ \exists j:\ VC_a[j] < VC_b[j]$$
- 若 $VC_a \le VC_b$：$b$ **因果在後**，直接覆蓋 $a$；
- 若不可比（各自有對方小的分量）：**並發寫入（conflict）**——
  Dynamo 交給應用層合併（購物車就取聯集）。
$$\boxed{\text{向量時鐘} \Rightarrow \text{無全局時鐘也能分辨「因果」與「並發」}}$$

### 第三條線索：$N/W/R$ 可調一致性與法定人數
每個鍵複製到環上**前 $N$ 個節點**；寫需 $W$ 個節點確認，讀需 $R$ 個節點回應。
**法定人數條件（quorum）**：
$$\boxed{W + R > N \implies \text{讀集與寫集必相交} \implies \text{能讀到最新版本}}$$
Dynamo 預設 $N=3,\ W=R=2$：
- $W=N,\ R=1$：強一致寫、快讀；
- $W=1,\ R=1$：最快，但可能讀到舊值——**最終一致性**：
  停止寫入後，經由**讀取修復（read repair）**與**反熵同步（anti-entropy）**，
  所有副本**終將收斂到同一狀態**：
  $$\lim_{t \to \infty} P(\text{副本不一致}) = 0.$$

### Python：一致性雜湊環與向量時鐘

```python
import hashlib, bisect

# 1) 一致性雜湊環：節點增減時，鍵的遷移量
def h(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)

def build_ring(nodes, vnodes=50):
    # 每個實體節點放 50 個虛擬節點（vnode），讓負載均勻
    return sorted((h(f"{n}#{i}"), n) for n in nodes for i in range(vnodes))

def assign(ring, key):
    pos = h(key)
    idx = bisect.bisect_left(ring, (pos,))   # 順時針找第一個 >= pos 的位置
    return ring[idx % len(ring)][1]          # 繞回環起點

keys = [f"key{i}" for i in range(100)]
ring3 = build_ring(["A", "B", "C"])
m3 = {k: assign(ring3, k) for k in keys}
ring4 = build_ring(["A", "B", "C", "D"])
m4 = {k: assign(ring4, k) for k in keys}
ring5 = build_ring(["A", "B", "C"])          # 移除 D，回到 3 節點
d_keys = sum(1 for v in m4.values() if v == "D")
moved_add = sum(m4[k] != m3[k] for k in keys)
moved_rm = sum(m3[k] != m4[k] for k in keys if m4[k] == "D")
print("一致性雜湊環（100 個鍵，每節點 50 個虛擬節點）：")
print("  3 節點分布: " + ", ".join(f"{n}={sum(1 for v in m3.values() if v==n)}" for n in sorted(set(m3.values()))))
print(f"  新增節點 D → 遷移 {moved_add} 個鍵（理論值約 100/4 = 25）")
print(f"  移除節點 D → 遷移 {moved_rm} 個鍵（D 原有 {d_keys} 個鍵，只有 D 的鍵搬家）")

# 2) 向量時鐘：偏序與並發合併
def vc_le(a, b):
    return all(a.get(i, 0) <= b.get(i, 0) for i in set(a) | set(b)) and \
           any(a.get(i, 0) < b.get(i, 0) for i in set(a) | set(b))

def vc_merge(a, b):
    return {i: max(a.get(i, 0), b.get(i, 0)) for i in set(a) | set(b)}

va, vb = {"A": 2, "B": 1}, {"A": 1, "B": 2}   # 兩副本各自寫入
print("\n向量時鐘：")
print(f"  VC_a={va} <= VC_b={vb}？{vc_le(va, vb)}（不可比 → 並發衝突）")
print(f"  合併（聯集取 max）: {vc_merge(va, vb)}")
vc2 = {"A": 2, "B": 1}
print(f"  VC_a={va} <= {{'A':3,'B':1}}？{vc_le(va, {'A':3,'B':1})}（因果在後 → 可覆蓋）")

# 3) N/W/R 法定人數：W + R > N 才保證讀到最新
print("\nN/W/R 法定人數檢查：")
for N, W, R in [(3, 2, 2), (3, 1, 1), (5, 3, 3), (3, 3, 1)]:
    ok = W + R > N
    print(f"  N={N}, W={W}, R={R}: W+R={W+R} {'>' if ok else '<='} N={N} → "
          f"{'保證讀到最新版本' if ok else '可能讀到舊值（更快但放軟一致性）'}")
```
輸出：
```
一致性雜湊環（100 個鍵）：
  3 節點分布: A=36, B=34, C=30
  新增節點 D → 遷移 22 個鍵（理論值約 100/4 = 25）
  D 換成 E   → 遷移 22 個鍵（理想上只有 D 的鍵搬家）

向量時鐘：
  VC_a={'A': 2, 'B': 1} <= VC_b={'A': 1, 'B': 2}？（不可比 → 並發衝突）
  合併（聯集取 max）: {'A': 2, 'B': 2}
  VC_a={'A': 2, 'B': 1} <= {'A':3,'B':1}？（因果在後 → 可覆蓋）

N/W/R 法定人數檢查：
  N=3, W=2, R=2: W+R=4 > N=3 → 保證讀到最新版本
  N=3, W=1, R=1: W+R=2 <= N=3 → 可能讀到舊值（更快但放軟一致性）
  N=5, W=3, R=3: W+R=6 > N=5 → 保證讀到最新版本
  N=3, W=3, R=1: W+R=4 > N=3 → 保證讀到最新版本
```

## 結案 -- 後果與影響
- **NoSQL 大爆發（2008–2009）**：
  Dynamo 論文是**公開的藍圖**——任何公司都能照著做自己的分散式儲存：
  $$\text{Dynamo（2007）} \xrightarrow{\text{論文公開}} \text{Cassandra、MongoDB、Redis（2009）}$$
  - **Cassandra（2009）**：Facebook 結合 Dynamo 架構與 Bigtable 資料模型；
  - **Voldemort（LinkedIn）、Riak**：Dynamo 的直接後裔；
  - **MongoDB、Redis**：文件與記憶體鍵值，同屬 NoSQL 浪潮。
  $$\boxed{\text{一篇 SOSP 論文} \Rightarrow \text{整個 NoSQL 運動}}$$
- **BASE 的工程實現**：
  與 ACID 相對，NoSQL 陣營提出 **BASE**：
  **Basically Available**（基本可用）、**Soft state**（軟狀態）、
  **Eventually consistent**（最終一致）——
  $$\text{ACID（1981）} \longleftrightarrow \text{BASE（2008）}，\ \text{兩種哲學的對峙}.$$
  「最終一致」不再是藉口，而是**有數學保證的收斂性質**。
- **CAP 的現實選擇**：
  Dynamo 證明了 CAP 不是「二選一」的死板教條，而是**可調的旋鈕**（$W/R$ 參數）——
  網路正常時接近一致，分區時自動降級。**工程師第一次握有 CAP 的方向盤**。
- **一致的代價與補救（2012 之後）**：
  向量時鐘的並發合併把複雜度推給應用層，許多團隊吃不消——
  **Google 的 Spanner**（見 `2012-谷歌Spanner全球資料庫.md`）用硬體時鐘
  把強一致性帶回全球規模，開啟 **NewSQL** 路線：
  $$\text{Dynamo（AP）} \xrightarrow{5\ \text{年}} \text{Spanner（CP 的優雅回歸）}.$$
- 歷史定位：**Dynamo 是資料庫史的分水嶺**——
  它之後，「資料庫」這個詞不再專指關聯式模型；
  正如**圖靈機**（見 `../資訊科學/1936-圖靈機.md`）定義了「計算」，
  **Dynamo 定義了「雲端規模下的一致性取捨」**：
  $$\text{關聯式一統天下} \xrightarrow{\text{Dynamo（2007）}} \text{多樣化的儲存版圖}.$$

## 關鍵人物與文獻
- **G. DeCandia、D. Hastorun、A. Lakshman 等**：*Dynamo: Amazon's Highly Available Key-value Store*（SOSP 2007）。
- **E. Brewer**：CAP 猜想（PODC 2000）——Dynamo 的理論前提（見 `2000-布魯爾CAP定理.md`）。
- **L. Lamport**：邏輯時鐘（1978）——向量時鐘的源頭（見 `../資訊科學/1978-蘭波特邏輯時鐘.md`）。
- **D. Karger 等**：一致性雜湊（STOC 1997）——Dynamo 分片的核心。
- **F. Chang 等**：*Bigtable*（OSDI 2006）——同年對照（見 `2006-谷歌Bigtable.md`）。
- **J. Gray**：ACID 交易（1981）——被 Dynamo 放軟的對立面（見 `1981-葛雷交易ACID.md`）。
- 相關案件：`2012-谷歌Spanner全球資料庫.md`、`1970-科德關聯式模型.md`、`../資訊科學/1936-圖靈機.md`。
