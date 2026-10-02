# 1977 - Sanger 定序法（DNA 可以被「閱讀」）

## 案件摘要
1977 年，Frederick Sanger 在劍橋發表**鏈終止定序法 (chain-termination / Sanger sequencing)**：
用雙脫氧核苷酸 (ddNTP) 隨機終止 DNA 合成，產生長度不同的片段，
再用**膠體電泳**按長度分離，讀出序列。
他定出噬菌體 $\phi$X174 的完整基因組（**5,386 個鹼基**——第一個被完整定序的生物體）。
**生命的第一本書被讀出**——Sanger 兩度獲諾貝爾獎（1958、1980），
是史上極少數的「雙冠王」。

## 前因 -- 為什麼會有這個案子
- **讀取的不可能**：DNA 是 4 種鹼基的長鏈（人類基因組 30 億鹼基對）。
  1970 年代，沒有任何方法能「讀出」一段 DNA 的序列——
  **讀取是兇手，讀不出序列的遺傳學是黑箱。**
- **Sanger 的蛋白質先驗**：他 1955 年定出**胰島素的完整胺基酸序列**（第一個被定序的蛋白質，
  1958 諾獎）——他早已證明「生物大分子可以被閱讀」。**蛋白質會讀，DNA 為什麼不會？**
- **限制酶的線索（1970–1972）**：限制酶（HindII、EcoRI）能**在特定序列切斷 DNA**——
  DNA 有了「剪刀」，但還缺「讀出的方法」。
- **Sanger 的偵探直覺**：與其「直接讀」，不如**讓 DNA 自己寫出終止訊號**——
  合成時隨機掺入 ddNTP（缺少 3'-OH，鏈在此終止），片段長度 = 鹼基位置。

## 線索與推理 -- 數學式、程式、理論

### 核心推理：隨機終止 = 長度編碼位置
ddNTP 的化學偵探戲：
- dNTP（正常）：有 3'-OH，鏈繼續延長
- ddNTP（終止）：**沒有 3'-OH**，下一個核苷酸無法接上——**鏈在此死亡**

在複製反應中，ddNTP 以低濃度（~1/100）隨機掺入：
$$P(\text{在位置 } k \text{ 終止}) = (1-p)^{k-1}\, p \qquad \text{（幾何分佈）}.$$
**每個位置都有機會終止** → 試管裡產生一族「終止於各位置」的片段。
四管反應（各掺一種 ddNTP：ddATP/ddGTP/ddCTP/ddTTP），
膠體電泳按長度分離（**1 鹼基差 = 可分辨**），從短到長讀出 = 從 5' 到 3' 的序列。

### Python：Sanger 定序的模擬

```python
import numpy as np

COMPLEMENT = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}

def sanger_sequencing(template, p=0.1, rng=None):
    rng = rng or np.random.default_rng()
    # template 是模板股；合成的新股與其互補
    L = len(template)
    reads = {b: [] for b in 'ACGT'}
    for trial in range(2000):                     # 大量合成反應
        seq, done = [], False
        for k, base in enumerate(template):
            nb = COMPLEMENT[base]                 # 新股的鹼基
            if rng.random() < p:                  # 掺入 ddNTP → 終止
                reads[nb].append(k); done = True; break
            seq.append(nb)
        if not done: reads[COMPLEMENT[template[-1]]].append(L-1)
    return reads

def reconstruct(reads, L):
    # 從終止位置重建序列
    seq = [None]*L
    for b, positions in reads.items():
        for k in positions: seq[k] = b
    return ''.join(seq)

rng = np.random.default_rng(0)
template = "ATGCCGTAAGCTTACGGCATTACCGGT"
reads = sanger_sequencing(template, rng=rng)
recovered = reconstruct(reads, len(template))
comp = ''.join(COMPLEMENT[b] for b in template)     # Sanger 讀的是新股（互補股）
print("模板   :", template)
print("讀出的 :", recovered)
print("定序正確:", recovered == comp)
```
輸出：
```
模板   : ATGCCGTAAGCTTACGGCATTACCGGT
讀出的 : TACGGCATTCGAATGCCGTAATGGCCA
定序正確: True
```
（Sanger 讀出的是合成的新股——與模板互補，原序列由此反推。）

### 定序能力的進化
| 年份 | 方法 | 通量 | 第一個定序對象 |
|------|------|------|---------------|
| 1977 | Sanger（鏈終止） | 手工讀膠，~100 bp/次 | $\phi$X174（5,386 bp） |
| 1987 | 自動定序（毛細管電泳） | ~1,000 bp/讀 | 人類基因組計劃的主力 |
| 2005 | 次世代定序 (NGS) | 億級 bp/天 | 全基因組普及化 |
| 2020s | 奈米孔 (Oxford Nanopore) | 長讀、即時 | 完整染色體無組裝 |

## 結案 -- 後果與影響
- **讀取生命的格式**：Sanger 法讓 DNA 序列成為「可讀的文本」——
  遺傳學從黑箱變成資訊科學，**生物學與電腦科學在此合流**（生物資訊學誕生）。
- **人類基因組計劃的引擎**：1990–2003 年的 HGP 用自動化 Sanger 法
  定出 30 億鹼基對（見 `2003-人類基因組計劃.md`）——**沒有 Sanger，沒有 HGP。**
- **生物資訊學的誕生**：序列資料爆炸 → GenBank（1982）資料庫、
  BLAST（1990）搜尋演算法、序列比對——**生命科學的資料科學化**。
- **雙冠王的範本**：Sanger 兩度獲諾獎（1958 蛋白質、1980 DNA 定序）——
  兩次都是「把不可讀變成可讀」。**偵探的方法論可以跨界重演。**
- **法醫與演化**：DNA 指紋（1984, Jeffreys）、古 DNA（Neanderthal 基因組, 2010）——
  序列成為法醫學與演化學的證據鏈。

## 關鍵人物與文獻
- **F. Sanger, S. Nicklen, A. R. Coulson**：PNAS 74, 5463 (1977)。
- **$\phi$X174**：Nature 265, 687 (1977)——第一個完整定序的基因組。
- **限制酶團隊**：HindII (1970, Smith/Wilcox)、EcoRI (1971)——剪刀的提供者。
- 相關案件：`1953-WatsonCrick-DNA雙螺旋.md`、`2003-人類基因組計劃.md`、`2012-CRISPR基因編輯.md`。
