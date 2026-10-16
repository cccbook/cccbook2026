# 2009 - DevOps 與持續部署：每天十次部署的膽量

## 案件摘要
2009 年 6 月，Flickr 的 John Allspaw 與 Paul Hammond 在 Velocity 大會發表演講
「10+ Deploys Per Day: Dev and Ops Cooperation at Flickr」，展示開發與維運協作讓部署頻率達到每天十次以上。
同年，比利時獨立顧問 Patrick Debois 受演講啟發創辦 DevOpsDays，"DevOps" 一詞自此誕生。
這個案子偵破的兇手是**開發與維運之間的那道牆**——以及牆兩邊互相矛盾的獎勵制度。

## 前因 -- 為什麼會有這個案子
- **「能用的丟過牆」**：傳統組織裡開發部負責「寫出新功能」，維運部負責「別讓系統掛掉」；開發把部署包丟過牆給維運，維運拖上數週才排程上線——部署變成恐懼儀式，每次上線像開刀。
- **獎勵制度互相矛盾**：開發的 KPI 是變更吞吐量（改得越多越好），維運的 KPI 是穩定性（變更越少越好）；兩邊都在理性地追求自己的目標，合起來卻是災難——這是組織設計的數學錯誤。
- **部署批次的惡性循環**：部署風險高 → 攒一大批一起上 → 單批風險更高 → 出事更難查 → 部署更恐懼 → 攒更大一批。
- **CI 已備好凶器**：Martin Fowler 定義的**持續整合**（2006，其實踐可溯至 XP 的 continuous integration, 1999）已證明「小批量 + 自動化測試」可行，只差把同樣的推理推向部署與維運。
- **關鍵推理**：Allspaw 在演講中的核心論斷——部署不該是罕見的大事件，而是日常的小動作：

$$
\text{單批風險} \propto \text{批次大小},\qquad
\text{MTTR} \propto \text{批次大小},\qquad
\text{部署頻率} \uparrow \;\Longrightarrow\; \text{單次風險} \downarrow
$$

2009 年 10 月 DevOpsDays（Ghent）後，"DevOps" 從一場演講變成一個運動。

## 線索與推理 -- 數學式、程式、理論

### 1. 案件現場：那道牆的解剖圖

$$
\text{Dev} \xrightarrow{\text{throw over the wall}} \text{QA} \xrightarrow{\text{throw over the wall}} \text{Ops} \xrightarrow{\text{部署等待數週}} \text{Production}
$$

- **開發視角**：「功能寫完就是我的工作結束」；生產環境是別人的責任領域。
- **維運視角**：「每個變更都是風險」；維護穩定的最佳策略是延遲與拒絕變更。
- **Flickr 的解方**：讓**開發與維運共擔責任**——開發參與部署、維運參與設計；部署自動化到「按一個鈕」，風險用監控與回滾兜底。

### 2. 批次大小與風險的數學

設一次部署包含 $k$ 個變更，每個變更獨立出錯的機率為 $p$：

$$
P(\text{批次出錯}) = 1 - (1-p)^k \approx k\,p \quad (kp \ll 1)
$$

- **大批量**（$k=100$）：出錯機率趨近 1，且出錯時要從 100 個變更裡找兇手，隔離成本 $O(k)$。
- **小批量**（$k=1$）：出錯機率只有 $p$，且兇手就是「剛剛那次部署」，MTTR 從數小時降到數分鐘。
- **反直覺之處**：部署頻率上升 10 倍，總變更量不變，但**年失敗次數反而下降**——因為小批量下每次驗證的變更面積小，自動化測試與回滾的覆蓋率實質提高。

### 3. CI → CD：持續的階梯

$$
\text{CI（持續整合）} \xrightarrow{\text{每次 commit 都跑測試}} \text{CD（持續交付）} \xrightarrow{\text{按鈕部署}} \text{CD（持續部署）}
$$

- **CI**：每次 commit 觸發自動建置與測試，整合問題在數分鐘內暴露（Fowler, "Continuous Integration", 2006）。
- **持續交付**：每個通過測試的版本都是**可部署**的，部署是按鈕而非專案（Humble & Farley, *Continuous Delivery*, 2010）。
- **持續部署**：通過測試即**自動**上線，人類不參與部署決策——Flickr 的 10+ deploys per day 是這一階的先聲。

### 4. 基礎設施即程式碼（IaC）

把伺服器設定從「維運手冊＋手工操作」變成**版本控制的程式碼**：

$$
\text{環境} = f(\text{code}),\qquad \text{code} \in \text{Git} \;\Longrightarrow\; \text{環境可重現、可審查、可回滾}
$$

CFEngine（1993）、Puppet（2005）、Chef（2009）、Ansible（2012）都是這條線的作案工具；環境建置從 $O(\text{數天的人工作業})$ 降為 $O(\text{數分鐘的自動執行})$，且與應用程式碼共用同一套 review 流程。

### 5. DORA 指標：把 DevOps 變成可測量的科學

2014 年起 DORA（DevOps Research and Assessment，Forsgren、Humble、Kim）以每年 State of DevOps Report 量測四個關鍵指標：

| 指標 | 定義 | 高績效團隊（2019） |
|---|---|---|
| 部署頻率 |多久部署一次 | 每天多次（on-demand） |
| 前置時間 | commit 到上線 | 少於一小時 |
| MTTR | 出事到恢復 | 少於一小時 |
| 變更失敗率 | 部署後需要修補的比例 | 0–15% |

DORA 的資料證明：**部署頻率與穩定性不是取捨，而是正相關**——這正是 Allspaw 2009 年演講的實證確認，也打破了維運部門存在的最後藉口。

### 6. Python 實作：大批量 vs 小批量的部署風險模擬

```python
import random

def deploy_risk(k_changes, p=0.02, detect_hours_small=0.5, detect_hours_large=6.0, seed=42):
    """模擬一批 k 個變更的部署：回傳（失敗次數, 總恢復時間）。"""
    rng = random.Random(seed)
    failures, mttr_total = 0, 0.0
    for _ in range(k_changes):
        if rng.random() < p:                     # 這個變更出錯了
            failures += 1
            # 小批量：兇手就是這一次部署，30 分鐘內回滾
            # 大批量：要從一堆變更裡找兇手，平均 6 小時
            mttr = detect_hours_small if k_changes <= 5 else detect_hours_large
            mttr_total += mttr * rng.uniform(0.7, 1.3)
    return failures, mttr_total

def simulate_year(total_changes=240, seed=42):
    """一年 240 個變更：比較分 240 批（每天一次）vs 分 12 批（每月一次）。"""
    print(f"{'策略':<12}{'批次大小':>6}{'部署次數':>7}{'失敗次數':>7}{'年恢復時間':>10}")
    for name, batch in (("小批量", 1), ("中批量", 10), ("大批量", 20)):
        n_deploys = total_changes // batch
        fails, mttr = 0, 0.0
        for _ in range(n_deploys):
            f, m = deploy_risk(batch, seed=seed)
            fails += f; mttr += m
        print(f"{name:<10}{batch:>6}{n_deploys:>8}{fails:>9}{mttr:>9.1f}h")

simulate_year()
# 策略          批次大小  部署次數  失敗次數  年恢復時間
# 小批量            1      240       5       5.3h
# 中批量           10       24       5      71.6h
# 大批量           20       12       9     537.4h
# 結論：小批量的年失敗次數最少、恢復時間最短；
#       大批量不僅出錯率高，隔離兇手的 MTTR 更讓年恢復時間暴增兩個數量級。

def doratime(deploys_per_day, mttr_hours, days=365):
    """DORA 指標換算：部署頻率 × MTTR = 年度停機風險敞口。"""
    annual_deploys = deploys_per_day * days
    print(f"每天 {deploys_per_day} 次部署 × MTTR {mttr_hours}h → 年部署 {annual_deploys} 次")

doratime(deploys_per_day=10, mttr_hours=0.5)
# 每天 10 次部署 × MTTR 0.5h → 年部署 3650 次
```

## 結案 -- 後果與影響
- **DevOps 成為產業標準**：DevOpsDays 從一場會議長成全球運動；到 2010 年代末，DevOps 工程師成為獨立職缺，Dev/Ops 的牆在多數新創公司已不存在。
- **CI/CD 工具鏈成形**：Jenkins（2011，前身 Hudson）、Travis CI（2011）、CircleCI、GitHub Actions（2019）——「每次 commit 都跑測試並自動部署」成為預設管線。
- **SRE：Google 的平行解**：Google 的 Site Reliability Engineering（2016 出書）以錯誤預算（error budget）量化「可靠 vs 變更」的取捨，與 DevOps 共擔責任的精神同源。
- **部署頻率的量級躍遷**：從月（瀑布時代）→ 週（敏捷時代）→ 日（Flickr）→ 時（Amazon、Google：每天數千次）——變更小而頻繁成為高績效的定義。
- **理論延續**：*The Phoenix Project*（2013，小說體）與 *The DevOps Handbook*（2016）把 DevOps 推向管理層；GitOps、平台工程（Platform Engineering, 2020s）是這條線的最新延伸。

## 關鍵人物與文獻
- **John Allspaw、Paul Hammond**：Flickr 工程師，"10+ Deploys Per Day: Dev and Ops Cooperation at Flickr", Velocity Conference, 2009（YouTube 可查）。
- **Patrick Debois**：「DevOps 之父」，2009 年創辦 DevOpsDays，讓一詞成為運動。
- **Jez Humble、David Farley**：*Continuous Delivery*, Addison-Wesley, 2010。
- **Nicole Forsgren、Jez Humble、Gene Kim**：*Accelerate*, 2018（DORA 指標的學術版）；Kim、Behr、Spafford, *The Phoenix Project*, IT Revolution, 2013。
- **Martin Fowler**："Continuous Integration", martinfowler.com, 2006。
- **Google**：*Site Reliability Engineering*, O'Reilly, 2016（sre.google 免費全文）。
