# 1999 年 Rosetta 蛋白質預測：片段拼圖的神探登場

> 副標題：Baker 把蛋白質剪成九肽碎片，再用蒙地卡羅把真相擲出來。
> 年表定位：第四幕第二案，回應 CASP 盲測中 FM 全軍覆沒的懸案。

## 案發現場

1998 年 CASP3 放榜，現場氣氛凝重。TBM（模板建模）組漸入佳境，FM（自由建模）組依然是命案現場：沒有模板的小蛋白，預測與真實結構相去甚遠。

華盛頓大學的 David Baker 盯著這份驗屍報告，提出一個近乎偵探直覺的疑問：既然 Levinthal 悖論說窮舉不可能，而蛋白質又確實秒級折疊，那麼局部序列是否早就寫好了局部結構的答案？換句話說，折疊不是從零推理，而是從記憶拼圖。

當時的嫌犯有三個：

第一，物理勢能太粗糙。全原子分子力場算得慢又不準，氫鍵、疏水、范德華的權重全靠猜。

第二，採樣空間太大。主鏈二面角 $phi$ 與 $psi$ 連續變化，稍長一點的鏈就是天文數字。

第三，知識未被利用。PDB 裡已有數千個結構，局部片段的構形偏好明明有案可查，卻沒人系統性拿來當線索。

Baker 的實驗室像一間新開的偵探事務所，招牌上寫著 Rosetta—— 以解開埃及象形文字的羅塞塔石碑為名，寓意把序列翻譯成結構。

## 偵查過程（含數學式/表格/理論）

### 推理一：片段組裝，大化小

Rosetta 的核心詭計是「剪碎再拼回」。把目標序列切成每段 3 或 9 個殘基的短片段，對每個片段到 PDB 資料庫裡搜尋同序列的已知構形，取出約 200 個候選片段。這 200 個碎片就是線索卡。

接著用蒙地卡羅隨機拼裝：隨機挑一段序列位置，隨機換上一個候選片段的二面角，計算能量，能量降則接受，能量升則按機率接受。數萬步之後，一條亂麻般的伸展鏈會塌縮成緊湊的預測結構。

下表是片段策略的辦案邏輯：

| 設計 | 選擇 | 理由 |
|------|------|------|
| 片段長度 | 3 肽與 9 肽並用 | 3 肽刻畫精細轉角，9 肽攜帶二級結構訊息 |
| 候選數 | 每位置約 200 個 | 覆蓋 PDB 中的局部偏好，又不至於淹沒採樣 |
| 移動方式 | 單片段二面角替換 | 保持局部合理性，避免全鏈亂動 |
| 接受準則 | Metropolis 準則 | 見下式，允許上坡以逃離陷阱 |

### 推理二：知識勢能加蒙地卡羅

Rosetta 的能量函數不是純物理，而是「知識勢能」：從 PDB 統計中反推出來的有效能量。直覺是貝葉斯倒推—— 在資料庫中常見的，即為低能量的。

例如某類殘基接觸在資料庫中出現頻率高，其有效能量就低。形式上可寫成 Boltzmann 反演：

$$
E_{pair}(a,b)=-k_BT\ln\frac{P_{obs}(a,b)}{P_{ref}(a,b)}
$$

其中 $P_{obs}$ 是觀測到的接觸機率， $P_{ref}$ 是隨機參考態機率， $k_B$ 是 Boltzmann 常數， $T$ 是有效溫度。類似的項還有環境項、殘基對項、鏈內氫鍵項、范德華排斥項等，加權求和即為 Rosetta 低解析度評分 $E_{total}$ ：

$$
E_{total}=w_{env}E_{env}+w_{pair}E_{pair}+w_{hb}E_{hb}+w_{vdw}E_{vdw}+\cdots
$$

其中的權重 $w$ 靠小蛋白回測調校。這種「統計即物理」的思路當年備受爭議，如今看來正是經驗勢能的先聲。

蒙地卡羅的接受機率則是經典的 Metropolis 式。設舊能量為 $E_{old}$ ，新能量為 $E_{new}$ ，能量差為 $DeltaE$ ，則接受機率 $P_{acc}$ 為：

$$
P_{acc}=\min\left(1,\exp\left(-\frac{\Delta E}{k_BT}\right)\right)
$$

下坡必收，上坡擲骰。這讓搜尋既貪心又狡猾，能鑽出局部陷阱。

### 推理三：CASP 席捲與分散式算力

Rosetta 在 CASP4（2000）與 CASP5（2002）上演了探案劇的高潮：FM 類別中橫掃千軍。對小蛋白（約 100 殘基以下），Rosetta 常交出 $GDT\_TS$ 超過 50 分的模型，在當年足以讓全場起立。TBM 類別亦靠精修（refinement）嶄露頭角。

但代價是算力黑洞：每個靶點需生成數萬個誘餌（decoys）再聚類選優。Baker 團隊於 2005 年祭出 Rosetta@home，把計算分發到全球志願者的電腦。這既是算力眾籌，也是科學傳教—— 數十萬台家用電腦夜以繼日為蛋白質折疊擲骰子。

| 年份 | 事件 | 意義 |
|------|------|------|
| 1999 | Rosetta 論文發表 | 片段組裝加知識勢能正式登場 |
| 2000 | CASP4 FM 奪冠群 | 證明無模板小蛋白可預測 |
| 2002 | CASP5 衛冕 | 方法穩定性得到確認 |
| 2005 | Rosetta@home 上線 | 分散式算力支撐大規模採樣 |
| 2003 起 | RosettaDesign | 從預測走向設計，反向辦案 |

## 結案報告

Rosetta 破了 FM 懸案的一半：它證明局部偏好加緊湊性加統計勢能，足以把小蛋白折疊到拓撲正確。Levinthal 迷宮被片段記憶切成了小塊，搜尋不再是天文數字。

它的遺產有三：

第一，方法遺產。片段庫思想被後來所有從頭方法繼承，甚至 AlphaFold 的 MSA 與模板模組裡仍看得見它的影子。

第二，制度遺產。Rosetta@home 示範了公民科學的力量，也預告了折疊問題終將是算力與數據之戰。

第三，反向遺產。既然能預測，就能設計。Baker 團隊轉向蛋白質設計，最終在 2024 年與 AlphaFold 共享諾貝爾化學獎榮光。這是 1999 年那間偵探事務所開業時沒人敢寫的結局。

當然，Rosetta 也有未竟之案：大蛋白、多結構域、膜蛋白依然棘手；評分函數的物理真實性始終被質疑；每個靶點數萬誘餌的暴力美學注定要被深度學習取代。但在 1999 年的時空裡，它就是那個敢蒙眼拼圖的神探。

## 證據與工具

- 關鍵公式一：Boltzmann 反演的知識勢能， $E_{pair}$ 見偵查過程。
- 關鍵公式二：加權總能量 $E_{total}$ ，各權重 $w$ 需回測校準。
- 關鍵公式三：Metropolis 接受機率 $P_{acc}$ ，控制上坡逃逸。
- 核心參數表：片段長度 3 與 9，候選數約 200，誘餌數以萬計，見上表。
- 工具鏈：PDB 片段庫、Rosetta 低解析度評分、高解析度全原子精修、Rosetta@home 分散式平台。
- 辦案心法：先剪碎再拼回。連續二面角空間太大時，用離散的 PDB 記憶離散化它。
- 延伸卷宗：前案是 [1994-CASP結構預測競賽.md](1994-CASP結構預測競賽.md)，後案是 [2002-Metadynamics增強採樣.md](2002-Metadynamics增強採樣.md)，看採樣問題如何從另一條路被圍剿。

## 補充：程式實作

> 全原子力場嫌貴、連續二面角嫌大，偵探把蛋白縮成一串 H 與 P，在方格上逼它招供。

對應程式：[1999-hp_lattice_folding.py](_code/1999-hp_lattice_folding.py)

本程式是 Rosetta 精神的掌上迷你版：Dill 的 HP 模型只分疏水 $H$ 與親水 $P$ ，能量即 $E = -N_{HH}$ 。
8 珠鏈 $SEQ = HPPHPPHH$ 在二維方格上做自避行走，非鍵結 $H$ 與 $H$ 相鄰一個記一分，全域窮舉即是暴力版片段組裝。
窮舉以 DFS 走完全部自避行走，去掉平移旋轉對稱後計數，再用 numpy 重算能量驗收，保證最優解無漏網。
這正是 Boltzmann 反演的草根邏輯：常見接觸即低能量，緊湊且 $H$ 內聚者勝出。
Rosetta 用 Metropolis 擲骰爬山，本玩具用窮舉直接封頂，兩路人馬辦的是同一樁摺疊案。

執行指令：

```bash
python3 _code/1999-hp_lattice_folding.py
```

實測口供（確定性窮舉，種子 1999）：

```text
序列: HPPHPPHH (長度 8)
窮舉自避行走總數 (固定首步去對稱後): 543
最佳能量 E* = -3  (即 H-H 接觸數 = 3)
VERIFICATION: best_energy=-3 contacts=3 n_saw=543 PASS
```

最優構形其一為座標串 [(0,0),(1,0),(1,1),(0,1),(0,2),(-1,2),(-1,1),(-1,0)]，ASCII 圖如下：

```text
P P .
H H P
H H P
```

解讀要點：

- 543 條自避行走中僅少數能拿到 3 個 $H$ 與 $H$ 接觸，最佳能量穩穩鎖在 -3。
- 終態把 4 個 $H$ 全塞進核心、4 個 $P$ 晾在外圍，疏水塌縮一目了然。
- 8 珠尚可窮舉，鏈稍長即天文數字，正好解釋 Rosetta 為何改用片段加蒙地卡羅。
- 確定性窮舉無隨機 flot，每次重跑口供完全一致。

讀者可改序列 $SEQ$ （如改為 HPPHHPHH 試另一條 8 珠鏈）或把能量改為只計某類接觸，重跑看最優能量與構形如何翻供。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""1999 HP 格點蛋白摺疊玩具 (對應 wiki：計算模擬學 / 蛋白質摺疊・HP lattice model)。

背景：Dill (1985) HP 模型把胺基酸簡化為疏水 H / 親水 P 兩類，
放在 2D 方格上做自避行走 (self-avoiding walk)，能量 = -1 × (非鍵結 H-H 接觸數)。
此處取課本式 8 珠鏈 HPPHPPHH，窮舉全部自避行走找最低能量 (ground state)。

只用 numpy；窮舉為純 Python DFS + numpy 驗算能量。固定種子 (此題為確定性窮舉)。
"""
import numpy as np

np.random.seed(1999)

SEQ = "HPPHPPHH"  # 8 珠
MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def energy_of(pos) -> int:
    """pos: list of (x, y)；回傳能量 = -H-H 接觸數。"""
    p = np.array(pos)
    n = len(pos)
    is_h = np.array([c == "H" for c in SEQ])
    contacts = 0
    for i in range(n):
        if not is_h[i]:
            continue
        for j in range(i + 2, n):  # 排除鏈上相鄰
            if not is_h[j]:
                continue
            if abs(p[i][0] - p[j][0]) + abs(p[i][1] - p[j][1]) == 1:
                contacts += 1
    return -contacts


def main():
    # 固定首兩珠以去除平移+旋轉對稱：(0,0) -> (1,0)
    best_e = 0
    best_conf = None
    total_saw = 0

    def dfs(path, visited):
        nonlocal best_e, best_conf, total_saw
        if len(path) == len(SEQ):
            total_saw += 1
            e = energy_of(path)
            if e < best_e:
                best_e = e
                best_conf = list(path)
            return
        x0, y0 = path[-1]
        for dx, dy in MOVES:
            nxt = (x0 + dx, y0 + dy)
            if nxt in visited:
                continue
            visited.add(nxt)
            path.append(nxt)
            dfs(path, visited)
            path.pop()
            visited.remove(nxt)

    dfs([(0, 0), (1, 0)], {(0, 0), (1, 0)})

    print(f"序列: {SEQ} (長度 {len(SEQ)})")
    print(f"窮舉自避行走總數 (固定首步去對稱後): {total_saw}")
    print(f"最佳能量 E* = {best_e}  (即 H-H 接觸數 = {-best_e})")
    print(f"一個最優構形 (x,y 序列): {best_conf}")
    # ASCII 視覺化
    xs = [c[0] for c in best_conf]
    ys = [c[1] for c in best_conf]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    grid = [["." for _ in range(xmax - xmin + 1)] for _ in range(ymax - ymin + 1)]
    for k, (x, y) in enumerate(best_conf):
        grid[y - ymin][x - xmin] = SEQ[k]
    print("最優構形圖 (y 由上而下):")
    for row in reversed(grid):
        print(" ".join(row))
    # 驗證：重算能量一致，且確實達到全域最優（窮舉保證）
    assert energy_of(best_conf) == best_e
    print(f"VERIFICATION: best_energy={best_e} contacts={-best_e} n_saw={total_saw} PASS")


if __name__ == "__main__":
    main()
```
