# 1662 - Graunt 出版死亡表觀察

## 案件摘要
1662 年，倫敦雜貨商 John Graunt 出版《Natural and Political Observations Made upon the Bills of Mortality》。他分析倫敦死亡登記表，製作出史上第一張生命表，開創了從樣本推論母體的統計方法——社會數據第一次成為科學研究的對象。

## 前因 -- 為什麼會有這個案子
16 世紀起，倫敦因瘟疫頻繁，教區開始每週發布**死亡登記表（Bills of Mortality）**，記錄死亡人數與死因（如 plague、fever、consumption 等），自 1629 年起更附上受洗人數。這些表格原本是為了讓富人判斷「該不該逃離倫敦避疫」，是行政檔案而非科學數據。

Graunt 是一位經營紐扣與雜貨的商人，自學拉丁文與法文。他注意到這些堆積如山的登記表中**埋藏著整個城市的秘密**：人口的規模、性別比、壽命分佈、瘟疫的規律。他花了數年手工整理 1632–1660 年間的數據，於 1662 年出版觀察報告。此書獲得國王查理二世青睞，Graunt 更被推薦進入剛成立的皇家學會——一位雜貨商靠「數數」成為科學家，轟動一時。

## 線索與推理 -- 數學式、程式、理論

### 生命表的誕生

Graunt 最偉大的發明是**生命表**：把死亡數據轉換成「每 100 名新生兒中，還有多少人活到各個年齡」的表格。他從瘟疫年代 records 中估計出各死因的年齡層比例，再合成出倫敦人口的存活曲線。原始版本如下：

| 年齡 | 存活人數（每 100 名出生） |
|---|---|
| 0   | 100 |
| 6   | 64  |
| 16  | 40  |
| 26  | 25  |
| 36  | 16  |
| 46  | 10  |
| 56  | 6   |
| 66  | 3   |
| 76  | 1   |
| 80  | 0   |

用現代記號，Graunt 的表給出了存活函數 $S(x) = P(X > x)$ 的離散估計，其中 $X$ 為壽命。例如由表可得條件存活率：

$$P(\text{活到 } 26 \mid \text{活到 } 16) = \frac{S(26)}{S(16)} = \frac{25}{40} = \frac{5}{8}$$

### 粗略估計壽命分佈

由生命表可估計**平均壽命**（life expectancy at birth）。以 Graunt 的表做離散近似（取區間中點加權）：

```python
ages  = [0, 6, 16, 26, 36, 46, 56, 66, 76, 80]
lived = [100, 64, 40, 25, 16, 10, 6, 3, 1, 0]

# 區間 [ages[i], ages[i+1]) 內死亡人數 = lived[i] - lived[i+1]
total_years = 0
for i in range(len(ages)-1):
    mid = (ages[i] + ages[i+1]) / 2
    total_years += mid * (lived[i] - lived[i+1])
print("平均壽命估計 ≈", total_years / lived[0], "歲")   # ≈ 18 歲左右
```

Graunt 自己估計倫敦人的平均壽命約 18 歲（受高嬰兒死亡率拖累）。這個數字雖粗糙，卻是人類第一次用數據回答「人平均能活多久」。

### 統計推論的萌芽：從樣本推母體

Graunt 的方法論突破在於：**倫敦死亡登記只涵蓋部分教區與部分死因，他卻能推估整個城市的人口**。他的推論鏈包括：

1. 估計倫敦每年出生約 12,000 人（由受洗記錄）。
2. 估計出生率上限：可生育婦女（約為總人口 $\frac{1}{5}$ 強）每年約 4 人中 1 人產子，故總人口約 $12{,}000 \times ... \approx 384{,}000$ 人。
3. 估計人口年增長率約 $\frac{1}{32}$，並用「兩對父母生兩個存活子女」論證人口可倍增。
4. 發現性別比：男嬰出生略多於女嬰（約 14:13），此規律在後世被證實為 $p \approx 0.513$ 的二項現象。

Graunt 明白地說，他的目的是給出「比未知真值小一點」與「比未知真值大一點」的界線——這正是**區間估計**的思想先聲，比 Neyman 的置信區間早了將近 300 年。

### 用 Python 重演 Graunt 的性別比觀察

```python
import random

p = 14 / 27          # Graunt 觀察到的男嬰比例 ≈ 0.5185
n, N = 10_000, 2000  # 每年 1 萬名新生兒，重複 2000 年
means = [sum(random.random() < p for _ in range(n)) / n for _ in range(N)]

import statistics
print("男嬰比例均值 =", statistics.mean(means))            # ≈ 0.5185
print("標準差 ≈", statistics.stdev(means))                  # ≈ 0.005
ci = (statistics.mean(means) - 2*statistics.stdev(means),
      statistics.mean(means) + 2*statistics.stdev(means))
print("95% 界線估計 =", ci)                                  # Graunt 式的上下界
```

## 結案 -- 後果與影響
Graunt 的生命表直接催生了**人口統計學**（demography）與**精算科學**。Edmond Halley（哈雷彗星的發現者）1693 年以布雷斯勞（Breslau）的出生死亡記錄製作出更精確的生命表，並據此計算年金價格——保險精算學自此誕生。Graunt 的「從部分推全體」方法啟發了 William Petty 的政治算術（Political Arithmetic），也為後來 Bernoulli 的大數法則與 Laplace 的統計推論鋪路。今天的壽命表、精算表、疫情監測，全是 Graunt 這張粗表的直系後裔。

## 關鍵人物與文獻
- **John Graunt**（1620–1674）：倫敦雜貨商、自學統計學家，皇家學會第一位非學院派成員。
- **William Petty**（1623–1687）：Graunt 的友人與政治算術倡導者（部分史家懷疑他參與了本書寫作）。
- **Edmond Halley**（1656–1742）：1693 年發表布雷斯勞生命表，開創精算數學。
- 文獻：J. Graunt, *Natural and Political Observations Made upon the Bills of Mortality*（1662, London）。
