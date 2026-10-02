# 1953 Ziegler-Natta 催化聚合

## 案發現場

1950 年代初，高分子化學已經由 Staudinger 與 Carothers 奠定基礎，聚乙烯與聚丙烯的潛力眾所周知，但工業上卻有兩個大瓶頸。第一：乙烯（$\mathrm{C_2H_4}$）的高壓自由基聚合需要上千個大氣壓與高溫，設備昂貴危險，而且產物是「低密度聚乙烯」——分子鏈上有大量分支，結晶性差、強度不足。第二：聚丙烯更麻煩，丙烯（$\mathrm{CH_3CH{=}CH_2}$）聚合後，每個單體的立體中心（帶甲基的手性碳）可以隨機排列，形成「無規聚丙烯」（atactic polypropylene），甲基方向雜亂無章，分子鏈無法緊密堆疊，是毫無用處的蠟狀軟膠。

化學家心中有一個未解之謎：**能不能讓乙烯在低壓下聚合？能不能控制聚合物鏈的立體化學，讓甲基整齊排列？** 如果能做到，將創造出高強度、可結晶的新材料，徹底改變塑膠工業。當時沒有人知道該怎麼做——直到一次意外的實驗室「怪事」打開了大門。

德國 Mülheim 的 Max-Planck 研究所所長卡爾·齊格勒（Karl Ziegler）是金屬有機化學的權威，長期研究有機鋁化合物。他發現的「齊格勒增長反應」可以用 $\mathrm{Al(C_2H_5)_3}$ 把乙烯一步步加成成長鏈，但鏈長總是停在約一百個碳左右，無法真正聚合。1953 年，他的學生 Breil 在一次實驗中加入了一種意想不到的雜質——四氯化鈦（$\mathrm{TiCl_4}$），結果乙烯竟然在常壓下劇烈聚合，反應器中湧出雪白固體。齊格勒意識到：這不是雜質，而是全新的催化劑。

## 偵查過程

齊格勒團隊的偵查分三步。第一步是意外中的觀察：增長反應被鎳催化劑「毒化」的現象，引導他們想到「過渡金屬會改變有機鋁的行為」；順著這條線，他們系統性地測試各種過渡金屬鹽，發現第 IV 族的鈦、鋯鹽效果最佳。第二步是配方優化：最終確定經典配方為

$$\mathrm{TiCl_4} + \mathrm{Al(C_2H_5)_3} \longrightarrow \text{Ziegler 催化劑（異相觸媒）}$$

兩種試劑反應生成還原態的鈦物种，附著在固體表面上，構成活性中心。第三步是示範威力：乙烯在 1–10 個大氣壓、室溫附近即可聚合，產物是「高密度聚乙烯」——線性無分支，分子鏈可以緊密結晶，密度與強度遠勝高壓法產品。

聚合機制的核心，可用 Cossee-Arlman 機理（1964 年提出，解釋齊格勒發現）來理解。活性中心是鈦原子上的一個空配位與一條增長中的烷基鏈：

1. 乙烯配位到鈦的空軌域上：
$$\mathrm{Ti{-}CH_2CH_3} + \mathrm{CH_2{=}CH_2} \rightarrow \mathrm{Ti}(\eta^2\text{-乙烯})\mathrm{{-}CH_2CH_3}$$
2. 遷移插入（migratory insertion）：烷基鏈遷移到配位的乙烯上，C=C 雙鍵打開，鏈增長兩個碳，同時再生出一個空配位：
$$\mathrm{Ti{-}R} + \mathrm{CH_2{=}CH_2} \rightarrow \mathrm{Ti{-}CH_2{-}CH_2{-}R}$$

每一步插入都嚴格經過金屬中心，因此分子鏈是完美線性的——這就是低壓聚乙烯沒有分支的原因。

但更精彩的一章來自義大利米蘭的納塔（Giulio Natta）。1954 年，納塔在聽取齊格勒的演講後（齊格勒展示了聚合技術，卻未公開全部細節），立刻回到實驗室用類似催化劑聚合丙烯。他發現用改性的 $\mathrm{TiCl_3/Al(C_2H_5)_3}$ 體系，可以得到一種前所未見的產物：用 X 射線繞射分析後證實，聚合物中所有甲基都整齊地排在分子鏈的同一側。納塔將其命名為「等規聚丙烯」（isotactic polypropylene）。

立體化學的控制可以形式化描述：聚合物鏈中相鄰立體中心的相對組態若全部相同（全同），則稱等規；若嚴格交替，則稱間規（syndiotactic）；若隨機，則為無規。等規聚丙烯因為分子鏈採取規則的螺旋構象（每 3 個單體轉一圈），可以緊密結晶，熔點高達 165 °C、強度高——而無規聚丙烯只是軟蠟。**催化劑的立體環境決定了單體插入時的取向**：鈦表面手性位點迫使丙烯以固定方式配位插入，使同一構型不斷複製——這是化學史上第一次用人造催化劑實現「立體規則性聚合」（stereoregular polymerization），媲美生物酶的精準度。

納塔進一步發展了立體化學的定量描述與 NMR 表徵方法，建立了「立體規則性聚合物」的整個理論框架，還製備出間規聚丙烯等多種新立體結構。

## 結案報告

這項工作以驚人的速度改變了世界：從 1953 年實驗室意外到 1957 年第一座聚丙烯工廠投產，只用了四年。1963 年，齊格勒與納塔共同獲得諾貝爾化學獎。

遺產包括：

1. **塑膠工業革命**：高密度聚乙烯（HDPE）與等規聚丙烯（iPP）成為全世界產量最大的塑膠之二，從包裝、汽車、醫療到日常用品無所不在。當今全球每年數千萬噸聚丙烯的生產，全部奠基於 Ziegler-Natta 催化劑。
2. **金屬有機催化化學的黃金時代**：Cossee-Arlman 機理確立了「遷移插入」這一核心基元反應，直接啟發了後來的氫甲醯化、烯烴複分解（2005 年諾貝爾獎）等整個金屬有機催化領域。
3. **催化劑的持續進化**：1980 年代 Kaminsky 發現的「單活性位金屬茂催化劑」（metallocene catalysts）繼承了 Ziegler-Natta 的思想，能更精準控制分子量分布與立體化學；後續甚至發展出可以「自由切換」立體結構的催化劑，寫出高分子鏈的立體「密碼」。
4. **高分子科學的範式**：納塔證明聚合物的立體化學可以用催化劑「程式化」，把高分子從隨機材料變成可設計的精密材料，這個思想延伸到生物高分子研究，也間接支持了 [1953-WatsonCrickDNA.md](1953-WatsonCrickDNA.md) 所揭示的「序列決定功能」的分子生物學世界觀。

一次學生實驗中的「怪事」，加上兩位化學家的敏銳與競爭，讓人類獲得了二十世紀產量最大的合成材料。Ziegler-Natta 催化劑至今仍活躍在每一座聚烯烴工廠裡——這是化學史上從意外到工業帝國最短的路。

## 證據與工具

以下用 Python 模擬等規 vs 無規聚丙烯的結晶傾向差異，並以簡單模型示範 Cossee-Arlman 鏈增長的 Monte Carlo 過程。

```python
import numpy as np
import matplotlib.pyplot as plt

# --- 模擬 1：立體規則性 vs 結晶傾向 ---
# 用簡化模型：相鄰單體構型相同 → 可堆疊加分，不同 → 扣分
def crystallinity(chain):
    score = 0
    for i in range(1, len(chain)):
        score += 1 if chain[i] == chain[i-1] else -1
    return max(score, 0) / (len(chain) - 1)

n = 200
atactic   = np.random.choice([0, 1], size=n)                    # 無規：隨機
isotactic = np.ones(n, dtype=int)                               # 等規：全同
print(f"無規聚丙烯結晶傾向: {crystallinity(atactic):.2f}")
print(f"等規聚丙烯結晶傾向: {crystallinity(isotactic):.2f}")

# --- 模擬 2：Cossee-Arlman 鏈增長 (Monte Carlo) ---
# 活性中心每次插入一個丙烯，插入取向由催化劑立體環境決定(機率 p_same)
def polymerize(n_units, p_same=0.98):
    chain, inserts = [], 0
    orientation = 1                      # 初始取向
    for _ in range(n_units):
        if np.random.rand() < p_same:    # 手性位點強迫同向插入
            chain.append(orientation)
        else:                            # 偶爾「出錯」
            orientation *= -1
            chain.append(orientation)
        inserts += 1
    return chain

chain = polymerize(100, p_same=0.98)
print(f"鏈長 100，等規度(連續同向比例): {crystallinity(chain):.2f}")

# 不同 p_same 對等規度的影響
ps = np.linspace(0.5, 1.0, 11)
tacticity = [np.mean([crystallinity(polymerize(200, p)) for _ in range(20)]) for p in ps]
plt.plot(ps, tacticity, 'o-')
plt.xlabel('插入取向一致性機率 p_same')
plt.ylabel('等規度')
plt.title('催化劑立體環境決定聚合物立體規則性')
plt.show()
```
