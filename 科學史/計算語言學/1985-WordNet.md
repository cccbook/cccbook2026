# 1985-WordNet

## 案件摘要

1985 年起，Princeton 大學的心理語言學家 George Miller 開始建構 WordNet——一部以「同義詞集合」（synset）而非「詞」為單位的機器可讀詞庫。1990 年以《Five Papers on WordNet》首次發表，到 1998 年 3.0 版已收錄 15 萬多詞彙、11 萬多同義詞集。本案的懸案是：紙本詞典對機器毫無用處，該如何讓電腦「懂得」詞與詞之間的關係？破案關鍵：把詞彙組織成語義關係網路，讓上位詞鏈、整體部分關係成為可計算的路徑。

## 前因 -- 為什麼會有這個案子

- Miller 1956 年的經典研究指出人類短期記憶容量是 7±2 個組塊（chunk），心理語言學一直追問：詞彙知識在人心智中如何組織？
- 1960s-1980s 的機器可讀詞典嚴重缺乏：紙本詞典的排版格式是給人看的，無法直接供程式使用。
- Miller 主張應用「同義詞集合」組織詞彙：`car`、`automobile`、`auto` 指同一概念，應綁成一個節點而非三個獨立條目。
- 當時 NLP 的詞義消歧（word sense disambiguation）急需機器可用的語義資源。
- 早期的詞庫（thesaurus，如 Roget）只有主題分類，沒有明確的語義關係圖。

## 線索與推理 -- 數學式、程式、理論

### synset 的組織

WordNet 的名詞從 25 個起始類別（beginner concepts）出發，如 `animal`、`artifact`、`food`、`vehicle` 等，向下展開層層的下位詞樹。每個 synset 是概念的節點：

$$
\text{synset} = \{w_1, w_2, \ldots, w_k\} \quad \text{代表一個概念節點}
$$

### 語義關係

WordNet 定義了多種可計算的語義關係：

- hypernym/hyponym：上位/下位關係（`car` 的上位是 `vehicle`）。
- meronym/holonym：部分/整體關係（`輪子` 是 `汽車` 的 meronym）。
- antonym：反義關係（`hot` 與 `cold`）。
- holonym：整體關係（`wheel` 的 holonym 是 `car`）。

名詞關係主要是 hypernym 樹；動詞則以「事件框架」表示——每個動詞 synset 帶有論元結構（誰做、對誰、用什麼）。

### 名詞的繼承樹

`vehicle → car → sports car` 的上位鏈形成繼承樹：下位節點繼承上位節點的屬性，如同框架理論的 default 繼承。語義相似度可用路徑距離估計：

$$
\text{sim}(c_1, c_2) = \frac{1}{1 + \text{dist}(c_1, c_2)}
$$

其中 dist 是兩 synset 在上位樹上的最短路徑邊數。Resnik 1995 年改用資訊內容（information content）加權：

$$
\text{sim}_{\text{Resnik}}(c_1, c_2) = \max_{c \in S(c_1, c_2)} \left( -\log P(c) \right)
$$

### WordNet 與詞庫的差異

| 特性 | Roget 詞庫 | WordNet |
|------|-----------|---------|
| 單位 | 詞（主題分組） | synset（概念節點） |
| 關係 | 隱含、不精確 | 明確的語義關係邊 |
| 機器可計算 | 否 | 是（圖上可跑演算法） |

### Python 實作 mini WordNet

```python
# mini WordNet: synset dict + hypernym 鏈查詢 + 路徑相似度
synsets = {
    "vehicle.n.01": {"words": ["vehicle"], "hypernym": None},
    "car.n.01":     {"words": ["car", "auto", "automobile"], "hypernym": "vehicle.n.01"},
    "sports_car.n.01": {"words": ["sports_car"], "hypernym": "car.n.01"},
    "bus.n.01":     {"words": ["bus"], "hypernym": "vehicle.n.01"},
    "wheel.n.01":   {"words": ["wheel"], "hypernym": None},
    "animal.n.01":  {"words": ["animal"], "hypernym": None},
    "dog.n.01":     {"words": ["dog"], "hypernym": "animal.n.01"},
}

meronyms = {  # 整體 -> 部分
    "car.n.01": ["wheel.n.01"],
}

def hypernym_chain(synset_id, chain=None):
    chain = chain or []
    entry = synsets.get(synset_id)
    if entry is None:
        return chain
    chain.append(synset_id)
    if entry["hypernym"]:
        return hypernym_chain(entry["hypernym"], chain)
    return chain

def path_distance(s1, s2):
    """在上位樹上的最短路徑邊數"""
    c1, c2 = hypernym_chain(s1), hypernym_chain(s2)
    if not c1 or not c2 or c1[-1] != c2[-1]:
        return None   # 不同樹，無路徑
    common = set(c1) & set(c2)
    lca_len = max(len(hypernym_chain(c)) for c in common)  # 最近共同祖先深度
    return (len(c1) - lca_len) + (len(c2) - lca_len)

def similarity(s1, s2):
    d = path_distance(s1, s2)
    return None if d is None else 1 / (1 + d)

def lookup(word):
    return [sid for sid, e in synsets.items() if word in e["words"]]

print(lookup("car"))                       # 同義詞集合查詢
print(hypernym_chain("sports_car.n.01"))   # 繼承樹：sports car -> car -> vehicle
print(path_distance("sports_car.n.01", "bus.n.01"))   # 路徑距離
print(similarity("sports_car.n.01", "bus.n.01"))      # 相似度 1/(1+d)
print(similarity("sports_car.n.01", "dog.n.01"))      # None（不同樹）
```

## 結案 -- 後果與影響

- WordNet 成為 NLP 的標準詞庫，支撐詞義消歧（WSD）與語義相似度研究數十年。
- 相似度度量形成一門小產業：path-based（Leacock-Chodorow 1998）與 information content（Resnik 1995、Lin 1998）。
- SentiWordNet 在 WordNet 的 synset 上標註情感極性，成為情感分析的基礎資源。
- SemEval 評測以 WordNet 為金標準之一，詞義標註競賽至今仍以它為參照。
- WordNet 是知識圖譜（knowledge graph）的先聲：以節點（概念）與邊（關係）組織知識，啟發日後的 DBpedia、Wikidata 與 BabelNet。

## 關鍵人物與文獻

- George A. Miller (1990). Five Papers on WordNet. International Journal of Lexicography 3(4), 235-312（WordNet 特刊）.
- George A. Miller, Richard Beckwith, Christiane Fellbaum, Derek Gross & Katherine Miller (1990). Introduction to WordNet: An On-line Lexical Database. International Journal of Lexicography 3(4), 235-244.
- George A. Miller (1956). The Magical Number Seven, Plus or Minus Two. Psychological Review 63(2), 81-97.
- Philip Resnik (1995). Using Information Content to Evaluate Semantic Similarity in a Taxonomy. IJCAI 1995, 448-450.
- Claudia Leacock & Martin Chodorow (1998). Combining Local Context and WordNet Similarity for Word Sense Identification. In Fellbaum (ed.), WordNet: An Electronic Lexical Database. MIT Press.
- Christiane Fellbaum (ed.) (1998). WordNet: An Electronic Lexical Database. MIT Press.
- Eneko Agirre & Oier Lopez de Lacalle (2009). Supervised Domain Adaptation for WSD. SemEval 2009.
