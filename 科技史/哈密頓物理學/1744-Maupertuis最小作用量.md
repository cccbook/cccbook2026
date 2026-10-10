# 1744 - Maupertuis 最小作用量原理

## 案件摘要
1744 年，Maupertuis 在法國科學院宣讀《一致律》(Accord de différentes lois de la nature)，
提出：自然界的運動使「作用量」**最小**。
$$\delta S = 0, \qquad S = \int m v \, ds = \int m v^2\, dt$$
這是物理史上第一條「全局性」原理——不描述「這一步怎麼走」，而描述「整條路徑的總帳」。
哲學味濃厚（Maupertuis 稱之為上帝節約的證據），但數學上被 Euler 與 Lagrange 救活，最終成為哈密頓物理學的基石。

## 前因
- **Fermat 原理（1662）**：光走「時間最短」的路徑，正確預言折射定律 $\frac{\sin\theta_1}{\sin\theta_2} = \frac{v_1}{v_2}$。全局極值原理的第一個成功案例。
- **萊布尼茨的「活力」(vis viva)**：$mv^2$ 才是真正的運動量（今稱 2 倍動能），與笛卡兒的 $mv$ 之爭纏鬥數十年。
- **Euler 的能量積分（1736）**：證明 $mv^2$ 型的量在自然路徑上取極值，鼓勵了 Maupertuis。
- **Johann Bernoulli 的最速降線問題（1696）**：$$\text{求 } y(x) \text{ 使 } T = \int \frac{\sqrt{1+y'^2}}{\sqrt{2gy}}\,dx \text{ 最小}$$ 牛頓、萊布尼茨、伯努利兄弟都解出擺線——「路徑取極值」的思想已是時代氛圍。

## 線索與推理

### 從 Fermat 到 Maupertuis 的類比
| | 光（Fermat, 1662） | 物質（Maupertuis, 1744） |
|---|---|---|
| 極小化的量 | 時間 $\int dt = \int \frac{ds}{v}$ | 作用量 $\int m v\, ds$ |
| 折射類比 | $\sin\theta_1/\sin\theta_2 = v_1/v_2$ | $\sin\theta_1/\sin\theta_2 = v_1/v_2$（若「物質折射率」$\propto v$） |
| 問題 | $v$ 與什麼有關？ | 為何是「最小」而非「穩定值」？ |

Maupertuis 用光的折射類比大膽推廣：若光走極值路，物質為何不會？

### 原理的檢驗：彈性碰撞
Maupertuis 用兩體彈性碰撞檢驗：碰撞前後系統總作用量 $\sum m v^2$ 守恆且碰撞路徑使其取極值，正確給出速度交換結果。
但批評者（König，並懷疑有 Euler 支持的學術鬥爭）指出證明有漏洞——**哲學原理需要數學重構**。

### 嚴格化：最小其實是「穩定」
後續數學家澄清：
$$\delta S = 0 \quad \text{（穩定點，未必是最小點）}$$
例如諧振子從 $A$ 到 $B$（半周期內）的作用量確實最小；但超過半周期，路徑只是「鞍點」。
「最小」是修辭，「穩定」是數學。真正致命的問題是：**$S = \int mv\,ds$ 只對無約束單質點好用**，
推廣到一般系統要等 Lagrange 的 $L = T - V$（見 [1788-分析力學.md](1788-分析力學.md)）。

### 伏筆：作用量的量子化
$$S = \int L\,dt \quad\longrightarrow\quad e^{iS/\hbar}\ (\text{Feynman, 1948})$$
Maupertuis 不可能預見：兩百年後，「作用量」會成為量子力學的中心量，Planck 常數 $\hbar$ 的單位正是「作用量」。

## 結案
- 全局變分原理正式進入物理；與 Fermat 光學原理形成對稱結構。
- 伏線直通三處：Lagrange 的分析力學（1788）、Hamilton 的特徵函數（1835）、Feynman 的路徑積分（1948）。
- 教訓：Maupertuis 提出正確方向的「不完整理論」，靠 Euler/Lagrange 的數學才站穩——**物理直覺 + 數學嚴格 = 完整的科學**。
