# 1923 Bronsted酸鹼理論

## 案發現場

1887 年，Arrhenius 提出電解質解離理論（見 [1887-Arrhenius電解解離.md](1887-Arrhenius電解解離.md)），定義酸是溶於水放出 $\mathrm{H^+}$ 的物質，鹼是溶於水放出 $\mathrm{OH^-}$ 的物質。這個定義在水中運作良好，成為此後三十餘年的教科書標準。

但到了 1920 年代，「案發現場」出現越來越多 Arrhenius 定義無法處理的疑點：

1. **氣相反應**：氨氣與氯化氫氣體在無水的空氣中相遇，直接生成白煙（氯化銨），這明顯是酸鹼反應，卻沒有任何「水溶液」與 $\mathrm{H^+}$、$\mathrm{OH^-}$ 的解離。
2. **非水溶劑**：液氨中 $\mathrm{NH_4^+}$ 扮演酸的角色、$\mathrm{NH_2^-}$ 扮演鹼，酸鹼行為明顯存在，卻與水無關。
3. **不含 OH 的鹼**：碳酸鈉 $\mathrm{Na_2CO_3}$ 水溶液顯鹼性，但 $\mathrm{CO_3^{2-}}$ 並不含氫氧根——它為何是鹼？

丹麥哥本哈根的 Johannes Nicolaus Brønsted 與英國的 Thomas Martin Lowry 在同一年（1923年）各自獨立提出新理論，試圖破解這些疑點。酸鹼化學需要一次典範轉移。

## 偵查過程

Brønsted 的偵查思路是抓住所有疑點的**共同本質**：質子（$\mathrm{H^+}$，即氫原子核）的轉移。氣相中 $\mathrm{HCl}$ 把質子交給 $\mathrm{NH_3}$；水中 $\mathrm{Na_2CO_3}$ 的 $\mathrm{CO_3^{2-}}$ 從 $\mathrm{H_2O}$ 搶走質子——只要盯著「誰給質子、誰受質子」，一切酸鹼現象都現出原形。

他定義：**酸是質子的給予者（proton donor），鹼是質子的接受者（proton acceptor）**。由此自然導出**共軛酸鹼對**的概念：

$$\mathrm{HA + B \rightleftharpoons A^- + HB^+}$$

其中 $\mathrm{HA/A^-}$ 是一對共軛酸鹼，$\mathrm{HB^+/B}$ 是另一對。酸鹼反應的本質是兩對共軛酸鹼之間的質子接力。以氨氣遇氯化氫為例：

$$\mathrm{HCl + NH_3 \rightleftharpoons Cl^- + NH_4^+}$$

$\mathrm{HCl}$ 給質子是酸，$\mathrm{NH_3}$ 受質子是鹼——不需要水，反應照樣成立。以碳酸根為例：

$$\mathrm{CO_3^{2-} + H_2O \rightleftharpoons HCO_3^- + OH^-}$$

$\mathrm{CO_3^{2-}}$ 從水搶質子，所以它是鹼（水在此扮演酸）——不含 $\mathrm{OH^+}$ 的物質照樣可以是鹼。

Brønsted 進一步推理出酸鹼強度的量化。酸給出質子的傾向可由平衡常數描述：

$$K_a = \frac{[\mathrm{A^-}][\mathrm{H^+}]}{[\mathrm{HA}]}, \qquad \mathrm{p}K_a = -\log_{10} K_a$$

$\mathrm{p}K_a$ 越小，酸越強；其共軛鹼則越弱。這把酸鹼從「定性分類」升級為「定量標尺」：任何酸鹼反應的方向都可由 $\mathrm{p}K_a$ 差預測——質子總是從強酸（低 $\mathrm{p}K_a$）流向強鹼，反應平衡常數為

$$\log_{10} K_{\text{反應}} = \mathrm{p}K_a(\text{產物酸}) - \mathrm{p}K_a(\text{反應物酸})$$

## 結案報告

Brønsted–Lowry 理論結案之後，酸鹼化學的版圖大幅擴張：氣相反應、非水溶劑、弱鹼水解、緩衝溶液，全部納入統一框架。它超越 Arrhenius 卻不推翻它——Arrhenius 定義成為質子理論在水溶液中的特例（$\mathrm{H_3O^+}$ 就是酸、$\mathrm{OH^-}$ 就是鹼），科學史上少見的溫柔典範轉移。

這個理論與 1909 年 Sørensen 的 pH 標度（見 [1909-Haber合成氨與pH.md](1909-Haber合成氨與pH.md)）珠聯璧合：pH 量測提供儀器，$\mathrm{p}K_a$ 提供標尺，酸鹼化學從此有了完整的度量體系。緩衝溶液的 Henderson–Hasselbalch 方程式

$$\mathrm{pH} = \mathrm{p}K_a + \log_{10}\frac{[\mathrm{A^-}]}{[\mathrm{HA}]}$$

成為生物化學的命脈——血液 pH 維持在 7.4 上下，靠的正是碳酸氫鹼緩衝對。後續 1963 年 Lewis 的電子對理論則再進一步擴張到無質子參與的反應。質子接力，至今仍是化學中最有用的偵探法則。

## 證據與工具

```python
import numpy as np

# --- 共軛酸鹼對：驗算 pKa 與 Ka ---
Ka = 1.8e-5   # 醋酸 CH3COOH 的 Ka（25°C）
pKa = -np.log10(Ka)
print(f"醋酸: Ka = {Ka:.1e}  →  pKa = {pKa:.2f}")

# 共軛鹼醋酸根：Kw = Ka * Kb
Kw = 1.0e-14
Kb = Kw / Ka
print(f"醋酸根: Kb = {Kb:.1e}  →  pKb = {-np.log10(Kb):.2f}")
print(f"驗證 pKa + pKb = {pKa + (-np.log10(Kb)):.2f} = pKw = 14.00")

# --- 預測反應方向：質子從強酸流向強鹼 ---
# HCl (pKa≈-7) + NH3 (NH4+ pKa≈9.25) → NH4+ + Cl-
logK = 9.25 - (-7)
print(f"\nHCl + NH3 → NH4+ + Cl- 的 logK ≈ {logK}  →  K ≈ 1e{logK:.0f}（徹底右傾）")

# --- Henderson–Hasselbalch：緩衝溶液 pH ---
pKa_acetic = 4.74
ratio = 0.5   # [A-]/[HA]
print(f"\n[A-]/[HA] = {ratio} 時，緩衝 pH = {pKa_acetic + np.log10(ratio):.2f}")
# 血液碳酸氫緩衝：pKa(H2CO3)≈6.1，[HCO3-]/[H2CO3]≈20
print(f"血液緩衝 pH ≈ {6.1 + np.log10(20):.1f}（生理正常值 7.4）")
```
