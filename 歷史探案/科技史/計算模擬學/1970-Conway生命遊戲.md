# 1970 年 Conway 生命遊戲：方格紙上的謀殺與復活

> 報案人：數學家 John Conway。案情：三條簡單規則，竟孵出會開槍的生命。
> 偵探在無限棋盤蹲守，目擊滑翔機槍連續作案，證明方格也能圖靈完備。

| 案件檔案 | 內容 |
|----------|------|
| 發生時間 | 1970 年 |
| 發生地點 | 英國劍橋，Gonville and Caius 學院 |
| 報案人 | John Horton Conway |
| 共犯 | Martin Gardner 專欄、PDP-7 電腦 |
| 兇器 | B3/S23 規則、滑翔機槍 |
| 結論 | 細胞自動機爆紅，複雜系統分支開張 |

## 案發現場

1970 年的案發現場是一張無限大的方格紙。

每個格子只有活或死兩態。沒有微分方程，沒有連續變數，
連馮紐曼二十九態的自我複製自動機都被嫌太囉嗦。
Conway 想問：最簡規則能否產生最繁行為。

背景有兩條暗線。一是馮紐曼與 Ulam 的遺產，
證明離散宇宙可自我複製，但規則複雜到無人想玩。
二是電腦進入校園，學生第一次可在螢幕上養東西。

現場矛盾是簡單是否等於平庸。Conway 花近兩年調參，
淘汰無數規則，只為三個願望：圖案不爆炸、不速滅，
還能動態平衡。於是 B3/S23 登場：出生需 3 鄰居，
存活需 2 或 3 鄰居，其餘皆死。

## 偵查過程

偵查從鄰居筆錄開始。每格有 8 鄰居，
活鄰居數記為  $k$  ，當前狀態記為  $s$  。
規則只有三句：死格若  $k = 3$  則出生，
活格若  $k = 2$  或  $k = 3$  則存活，其餘皆死。
簡寫為 B3/S23，其中  $B$  表出生， $S$  表存活。

偵探驗屍三種形態。靜物不動，如方塊與蜂巢。
振盪子週期復活，如閃光燈週期  $T = 3$  。
太空船會移動，滑翔機每 4 代平移一格，
像迴力鏢永不落地。

破案時刻是滑翔機槍。1970 年 11 月，
Bill Gosper 的 MIT 小組找到 Gosper 槍，
以週期  $P = 30$  無限發射滑翔機，棋盤有了生命源。

推理升級為計算理論。圖案與元件對應如下：

| 生命圖案 | 計算角色 | 說明 |
|----------|----------|------|
| 滑翔機 | 信號 | 傳遞位元 |
| 滑翔機槍 | 時鐘槍 | 持續產生信號 |
| 吃豆者 | 吸收器 | 刪除多餘信號 |
| 碰撞反應 | 邏輯閘 | 可造 AND 與 NOT |

由此可構造通用圖靈機，生命遊戲圖靈完備。
判定「此格局是否永不消亡」變成不可判定。
演化方程本質是離散動力系統：

$$
s_i(t+1) = F(s_i(t), k_i(t))
$$

其中  $s_i$  為格點狀態， $k_i$  為鄰居活數，
 $F$  為 B3/S23 布林函數， $t$  為代數。
這預告了 Wolfram 對 256 條一維規則的調查。

## 結案報告

Martin Gardner 在《科學美國人》報導後，
全美機房淪陷，工程師用深夜機時養滑翔機，
生命遊戲成為駭客文化神話。

遺產有三。第一，複雜系統有了吉祥物，
湧現與自組織第一次有了臉。第二，模擬多了一支，
細胞自動機與格子氣同屬離散宇宙觀。
第三，計算邊界改寫，零玩家遊戲也能通用計算。

Conway 證明：極簡規則足以孕育無限複雜。

## 證據與工具

關鍵證物一：單步更新虛擬碼。

```python
# grid 為二值陣列，1 表活，0 表死
def step(grid):
    neigh = count_neighbors(grid)
    birth = (grid == 0) & (neigh == 3)
    survive = (grid == 1) & ((neigh == 2) | (neigh == 3))
    return (birth | survive).astype(int)
```

關鍵證物二：圖案檔案表。

| 名稱 | 類型 | 週期  $P$  | 尺寸 |
|------|------|------------|------|
| 方塊 | 靜物 | 1 代 | 2 乘 2 |
| 閃光燈 | 振盪子 | 3 代 | 3 乘 3 |
| 滑翔機 | 太空船 | 4 代 | 3 乘 3 |
| Gosper 槍 | 槍 | 30 代 | 約 36 乘 9 |

延伸閱讀伏筆：Wolfram 將在 1980 年代驗屍 256 條規則，
寫出《一種新科學》。

## 補充：程式實作

方格紙上沒有目擊者，本探就蹲守四代，親眼看滑翔機往東南潛逃一格。

### 對應程式

[1970-game_of_life_glider.py](_code/1970-game_of_life_glider.py)

### 理論呼應

本文核心是 B3/S23 三句規則，活鄰居數記為 $k$ ，演化全由布林函數決定。

程式在十乘十零邊界上放一架經典滑翔機，逐代數鄰居更新。

滑翔機每四代平移一格且活格恆為五，正是太空船指紋。

四步後座標整體加一，即是文中平移不變性的最小呈堂證據。

### 執行方式

```bash
python3 _code/1970-game_of_life_glider.py
```

### 實測輸出

```text
init live=5 coords=[(2, 3), (3, 4), (4, 2), (4, 3), (4, 4)]
step 1: live=5 coords=[(3, 2), (3, 4), (4, 3), (4, 4), (5, 3)]
step 2: live=5 coords=[(3, 4), (4, 2), (4, 4), (5, 3), (5, 4)]
step 3: live=5 coords=[(3, 3), (4, 4), (4, 5), (5, 3), (5, 4)]
step 4: live=5 coords=[(3, 4), (4, 5), (5, 3), (5, 4), (5, 5)]
VERIFY live_counts=[5, 5, 5, 5, 5] (all==5? True)
VERIFY shift_ok=True
```

關鍵數字有二：五代活格數全為 $5$ ，一步未增一步未減。

四步末座標恰為初座標加 $1$ ，平移驗證顯示 $True$ 。

會走路又不增減的圖案，正是拿來當信號與時鐘槍的料。

### 讀者實驗

把初圖改為方塊或閃光燈，或把步數 $STEPS$ 從 4 改為 30 ，觀察靜物、振盪子與太空船的命運分岔。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""1970 Game of Life 滑翔機 (glider)：Conway 1970
對應 wiki：Conway's Game of Life，滑翔機每 4 步平移一格 (1,1) 且活細胞恆為 5。
10x10 零邊界，跑 4 步做座標比對驗證。只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

N = 10
STEPS = 4
# 經典 glider（相對座標），放在 offset 處以避開邊界
PATTERN = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
OFF = (2, 2)


def make_grid():
    g = np.zeros((N, N), dtype=int)
    for dr, dc in PATTERN:
        g[OFF[0] + dr, OFF[1] + dc] = 1
    return g


def step(g):
    # 零邊界鄰居計數（切片法，不用 wrap）
    nb = np.zeros_like(g)
    nb[1:, 1:] += g[:-1, :-1]
    nb[1:, :] += g[:-1, :]
    nb[1:, :-1] += g[:-1, 1:]
    nb[:, 1:] += g[:, :-1]
    nb[:, :-1] += g[:, 1:]
    nb[:-1, 1:] += g[1:, :-1]
    nb[:-1, :] += g[1:, :]
    nb[:-1, :-1] += g[1:, 1:]
    nxt = ((nb == 3) | ((g == 1) & (nb == 2))).astype(int)
    return nxt


def coords(g):
    return sorted(map(tuple, np.argwhere(g == 1).tolist()))


g = make_grid()
init_c = coords(g)
print(f"init live={len(init_c)} coords={init_c}")
counts = [len(init_c)]
for s in range(1, STEPS + 1):
    g = step(g)
    c = coords(g)
    counts.append(len(c))
    print(f"step {s}: live={len(c)} coords={c}")

expected = sorted([(r + 1, c + 1) for r, c in init_c])
final_c = coords(g)
print(f"expected after 4 steps (shift +1,+1): {expected}")
print(f"VERIFY live_counts={counts} (all==5? {all(v == 5 for v in counts)})")
print(f"VERIFY shift_ok={final_c == expected}")
assert all(v == 5 for v in counts), f"live count changed: {counts}"
assert final_c == expected, f"glider did not translate: {final_c} vs {expected}"
print("PASS")
```
