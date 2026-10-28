## 1995 - Alendronate 與骨質疏鬆治療（骨折之前，先打一場化學防禦戰）

## 案件摘要

**本案的兇器，是一顆會「騙過破骨細胞」的白色藥片。**

1995 年 9 月，美國 FDA 核准 Merck 的 alendronate（福善美，Fosamax）治療骨質疏鬆症——第一個以「大規模降低骨折率」為上市目標的口服抗骨吸收藥。雙磷酸鹽（bisphosphonate）的化學結構模仿焦磷酸鹽（pyrophosphate），沉積於骨基質、被破骨細胞吞入後毒殺其上；大規模試驗（FIT, 1994）顯示椎體骨折率下降近半。骨科從「修補斷骨」的技藝，第一次擁有**預防性藥物武器**——戰場從手術室，前移到藥櫃。

## 前因 -- 為什麼會有這個案子

- **流行病學的覺醒**：1960s Fuller Albright 早已以雌激素治療骨質疏鬆；1980s 髖部骨折的老齡化海嘯（全球每年 170 萬例）使「骨折流行病」成為公共衛生危機。
- **雙磷酸鹽的誕生**：1960 年代 Fleisch（Bâle）發現焦磷酸鹽抑制鈣化，進而合成不被酶水解的 P-C-P 類似物（雙磷酸鹽）；最初用於水管除垢與 Paget 病，後在動物實驗中展現抗骨吸收神力。
- **骨生物學的通路解密**：破骨細胞的皺褶緣（ruffled border）、骨吸收酸性環境、以及後來的 RANKL/RANK/OPG 軸（1997–99）——藥物作用機制被逐步看清。
- **測量技術就位**：1990 年代 DXA 雙能 X 光吸收法成為骨密度標準測量，讓「療效」可量化、藥物可審批。

## 線索與推理 -- 背後的理論

骨重塑（remodeling）的偶聯失衡是骨質疏鬆的本質：破骨>成骨。雙磷酸鹽的推理：

$$ \text{雙磷酸鹽} \xrightarrow{\text{沉積於骨}} \text{破骨細胞吞入} \Rightarrow \begin{cases} \text{含氮類: 抑制 FPPS 酶（膽固醇/異戊二烯途徑）→ 細胞凋亡} \\ \text{非含氮類（舊代）: 代谢成 ATP 類似物毒殺} \end{cases} $$

```python
# 骨重塑偶聯模型
def bone_balance(osteoclast_activity, osteoblast_activity):
    net = osteoblast_activity - osteoclast_activity
    if net < 0:
        return "骨量流失（骨質疏鬆）→ 抗吸收藥介入"
    return "骨量維持/增加"

# alendronate: 破骨活性 ↓40-70% → BMD ↑3-8%/3年 → 椎體骨折率 ↓~50%
```

FIT 試驗（Fracture Intervention Trial, Black et al. NEJM 1996）的證據鏈：>4000 名絕經後女性，椎體骨折相對風險下降 ~47%、髖部骨折亦有顯著下降——**以「骨折」而非「骨密度」為終點**的設計，把骨科從影象學安慰劑的陷阱中拉出。

治療哲學的躍遷：傳統骨科修「斷」，預防醫學防「斷」。從 alendronate 起，骨科與內分泌、老年醫學、婦產科結成「骨骼健康聯盟」——骨折聯絡服務（Fracture Liaison Services, FLS）成為各國標配：髖部骨折病人出院後自動轉入藥物與跌倒預防管理。

## 結案 -- 後果與影響

- **藥物族譜爆發**：Raloxifene（1997 SERM）、teriparatide（2002，第一個促骨合成藥）、denosumab（2010，RANKL 單抗）、romosozumab（2019，硬骨抑素單抗）——從「只剎車」到「既剎車又踩油門」。
- **罕見的副作用懸案**：頜骨壞死（MRONJ, 2003 起報告）與非典型股骨骨折（AFF, 2008 起）——「抑制骨重塑太久，微損傷累積」正是 Wolff 定律（`1892-Wolff定律.md`）的暗面；藥物假期（drug holiday）策略隨之誕生。
- **骨科的預防轉身**：髖部骨折的「骨科-老年共管」（orthogeriatric co-management）模式使死亡率下降；「脆弱性骨折」（fragility fracture）成為骨科的新病人族。
- **公共衛生的落差**：全球多數脆弱性骨折患者從未被評估治療（治療缺口 >80%）——藥有了，接通制度是下一段戰役。

## 關鍵人物與文獻

- Herbert Fleisch（1933–2019）——伯恩大學，雙磷酸鹽研究的奠基者。
- Gideon Rodan 與 G. A. Rodan——雙磷酸鹽作用機制（FPPS 抑制）的分子闡明者。
- Dennis Black 與 Steven Cummings——FIT 與 Study of Osteoporotic Fractures（SOF）的核心研究者。
- Black, D. M. et al., *Randomised trial of effect of alendronate on risk of fracture in postmenopausal women with osteoporosis*, Lancet/NEJM, 1996。
- Pierre Delmas 與 IOF——骨質疏鬆的國際防治綱領與 FLS 模式的推手。
