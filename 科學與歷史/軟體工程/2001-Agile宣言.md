# 2001 - 敏捷宣言：十七位嫌犯的滑雪場密約

## 案件摘要
2001 年 2 月，十七位軟體開發方法論者在猶他州 Snowbird 滑雪場閉關兩天，簽下《敏捷軟體開發宣言》。
他們來自互相競爭的陣營——Scrum、XP、Crystal、FDD、DSDM——卻共同指認了同一個兇手：**文件驅動的重型流程**。
宣言用四句「X 比 Y 更有價值」的對比句，把軟體開發的重心從流程與文件拉回人與可運作的程式碼。
此後二十年，這份僅 68 個字的文件成為全球軟體開發的主流信仰。

## 前因 -- 為什麼會有這個案子
- **瀑布流程的罩門：晚期回饋**：Royce（1970）提出的瀑布模型把需求→設計→實作→測試排成一條單行道，客戶要等到專案尾聲才第一次看到可執行的系統——那時需求早已變了兩輪，而預算已燒掉九成。
- **變更成本隨時間爆炸**：Boehm（1981）的曲線顯示，需求階段修正一個錯誤的成本是 1，驗收階段可能是 100——但在瀑布式流程裡，需求變更本身就被視為「違約」而非「資訊」。
- **重型方法論的反噬**：1990 年代 CMM、ISO 9001、UML/RUP 把「成熟度」定義成文件完備度；一個中型專案要產出數百頁規格書，工程師寫文件比寫程式的時間還長。
- **輕量派早已各自起義**：**Scrum**（Sutherland/Schwaber, 1995）以 30 天 Sprint 迭代交付；**XP**（Beck, 1999）以測試先行、結對程式設計、小版本發行應對變更；Cunningham 的 wiki（1995）與 Fowler 的重構理論都是同案犯的作案工具。
- **關鍵推理**：這些方法表面不同，底層卻共享同一組價值判斷——與其在文件裡預測未來，不如讓系統短週期地暴露在真實回饋裡：

$$
\text{回饋價值} \propto \frac{1}{\text{迭代長度}},\qquad \text{迭代長度} \downarrow \;\Longrightarrow\; \text{需求變更成本} = O(\text{iteration length})
$$

2001 年 2 月 11–13 日，在拜訪 Cunningham 的Portland Pattern Repository 未果的失望之後，這群人應 Jim Highsmith 之邀齊聚 Snowbird，兩天內把各自陣營的公約數寫成四句宣言、十二條原則。

## 線索與推理 -- 數學式、程式、理論

### 1. 案件現場：四大價值的結構

$$
\underbrace{\text{個體互動}}_{\text{信任}} \succ \underbrace{\text{流程與工具}}_{\text{控制}},\quad
\underbrace{\text{可運作軟體}}_{\text{真實進度}} \succ \underbrace{\text{詳盡文件}}_{\text{代理指標}},\quad
\underbrace{\text{客戶協作}}_{\text{連續回饋}} \succ \underbrace{\text{合約談判}}_{\text{一次性對抗}},\quad
\underbrace{\text{回應變化}}_{\text{適應}} \succ \underbrace{\text{遵循計畫}}_{\text{預測}}
$$

四句對比共用一個數學結構：右側（流程、文件、合約、計畫）都是**代理指標（proxy）**，它們只在「需求不變」的假設下與真正的目標相關；一旦需求開始變動，代理指標與目標的相關性就崩潰。宣言並未否定右側的價值——它說的是「左側**更有**價值」。

### 2. 迭代回饋的數學：為什麼短週期贏

設專案總長 $T$，切成 $n$ 個長度為 $L = T/n$ 的迭代。每個迭代結束時獲得一次真實回饋，需求錯誤最多存活 $L$ 的時間才被發現：

$$
\text{平均修正成本} = \bar{c}(L) \approx c_0 \cdot e^{\alpha L},\qquad
\text{總變更損失} \approx n \cdot \bar{c}(L) = \frac{T}{L}\, c_0 e^{\alpha L}
$$

- **瀑布**（$n=1$）：錯誤存活整個 $T$，單次修正成本 $c_0 e^{\alpha T}$ 極大。
- **敏捷**（$n$ 大）：$L$ 小，單次成本低，且每次回饋都能修正**方向**，不只是修正**錯誤**。
- 注意 $\frac{T}{L} c_0 e^{\alpha L}$ 對 $L$ 的導數為負（在合理範圍內），即**迭代越短，總損失越小**——這就是 XP 主張「一天一個版本」、Scrum 主張 1–4 週 Sprint 的數學根據。

### 3. Velocity：把團隊產出變成可測量的量

Scrum 用 **Velocity（速度）** 度量一個 Sprint 內團隊完成的 story points 總和。Velocity 不用來比較團隊（不同團隊的 point 定義不可通約），只用來**預測自己的完成時間**：

$$
\text{剩餘 Sprint 數} = \left\lceil \frac{\text{backlog 總點數} - \text{已完成}}{\bar{v}} \right\rceil,\qquad \bar{v} = \frac{1}{k}\sum_{i=1}^{k} v_i\ \text{（近 } k \text{ 個 Sprint 的移動平均）}
$$

Velocity 的價值在於它是**基於事實的外推**——用過去三個 Sprint 的實際產出，而非經理的期望——這正是宣言第一句「個體互動 > 流程工具」的度量化身。

### 4. 12 條原則：宣言的操作手冊

雪鳥會議翌日由 Highsmith 主筆濃縮出十二條原則，其中最「數學」的三條：

- **「經常交付可運作軟體，間隔從數週到數月，越短越好」**：即最小化 $L$。
- **「歡迎變更需求，即使開發晚期」**：即否認 Boehm 成本曲線是必然——小批量下曲線的 $\alpha$ 可以被壓平。
- **「可運作軟體是進度的主要量測」**：即以真實工件取代代理指標。

### 5. Scrum 與 XP 的合流

| 陣營 | 提出者 | 核心機制 | 對變更的防線 |
|---|---|---|---|
| Scrum | Sutherland/Schwaber, 1995 | 30 天 Sprint、每日站會、backlog 排序 | 需求凍結在 Sprint 內、排序在 Sprint 間 |
| XP | Beck, 1999 | 測試先行、結對、持續整合、小發行 | 測試套件讓變更成本低到敢隨時改 |

兩者合流於 Snowbird：Scrum 提供管理框架（開會節奏、角色），XP 提供工程實踐（測試、重構、CI）。今日多數「敏捷團隊」其實是 **Scrum 骨架 + XP 工程實踐** 的混血兒。

### 6. Python 實作：瀑布 vs 敏捷的需求變更適應成本

```python
import math, random

def total_loss(n_iter, T=12, c0=1, alpha=0.35, seed=42):
    """把 T 個月切成 n_iter 個迭代，模擬需求錯誤被發現時的修正成本總和。"""
    rng = random.Random(seed)
    L = T / n_iter                      # 迭代長度（月）
    loss = 0.0
    for i in range(n_iter):
        # 每月平均引入 0.5 個需求錯誤（泊松），存活到本迭代末才被發現
        n_errs = sum(1 for _ in range(round(L)) if rng.random() < 0.5)
        for _ in range(n_errs):
            loss += c0 * math.exp(alpha * L) * rng.uniform(0.8, 1.2)
    return loss

def waterfall_vs_agile():
    print("迭代數  迭代長度   總變更損失")
    for n in (1, 2, 4, 6, 12):
        L = 12 / n
        print(f"{n:>4}    {L:>5.1f}月    {total_loss(n):>8.1f}")

waterfall_vs_agile()
# 迭代數  迭代長度   總變更損失
#    1     12.0月       72.5   ← 瀑布：錯誤存活整個專案
#    2      6.0月       34.7
#    4      3.0月       17.9
#    6      2.0月       14.3
#   12      1.0月       11.6   ← 每月一次回饋，損失最低

def sprint_forecast(backlog, velocities):
    """用移動平均 Velocity 外推完成時間。"""
    v = sum(velocities[-3:]) / min(3, len(velocities))
    sprints = math.ceil(backlog / v)
    print(f"速度 {v:.1f} 點/Sprint → {backlog} 點需 {sprints} 個 Sprint")

sprint_forecast(backlog=180, velocities=[28, 25, 32, 27, 30])
# 速度 29.7 點/Sprint → 180 點需 7 個 Sprint
```

## 結案 -- 後果與影響
- **敏捷成為全球主流**：到 2010 年代末，多數大型軟體組織自稱採用敏捷；宣言網站上的簽名數持續成長，四大價值被印在無數團隊的牆上。
- **Scrum 與看板統治日常**：Sprint、站會、backlog、看板（Kanban，源自豐田生產系統）成為軟體團隊的預設語言——有時只是儀式，未必是精神。
- **DevOps 的土壤**：短迭代交付需要自動化部署與開發維運協作——敏捷是 DevOps（2009）的直接前因。
- **文件文化被重估**：文件從「交付物」變成「溝通工具」；詳盡規格書讓位給可執行測試與使用故事。
- **敏捷的商業化與變質**：SAFe 等企業級框架把敏捷重新官僚化，被批評者稱為「敏捷工業複合體（Agile Industrial Complex）」——兇手換了衣服，又回到了現場。

## 關鍵人物與文獻
- **Kent Beck**（XP 創始人）、**Martin Fowler**（ThoughtWorks，重構理論）、**Ward Cunningham**（wiki 發明人）、**Jeff Sutherland**（Scrum 共同創始人）、Ken Schwaber、Jim Highsmith、Alistair Cockburn（Crystal）、Robert Martin 等 17 位簽署者。
- Beck, *Extreme Programming Explained: Embrace Change*, Addison-Wesley, 1999。
- Schwaber & Sutherland, *The Scrum Guide*, 2010（首版公開規範）；Sutherland, *Scrum: The Art of Doing Twice the Work in Half the Time*, 2014。
- 《敏捷軟體開發宣言》原文：agilemanifesto.org，2001。
- Winston Royce, "Managing the Development of Large Software Systems", 1970（瀑布模型的原始出處，其實 Royce 本人主張迭代）。
