# 2023：AI 天氣超越 NWP——圖神經與地球 Transformer 的逆襲

> 卷宗編號：WX-2023-GRAPHCAST。報案人：歐洲中期預報中心（ECMWF）。案情：統治天氣預報七十年的數值天氣預報（NWP），在自家最擅長的 10 天預報上，被兩個 AI 模型正面超越。

## 案發現場

2023 年夏秋，Science 連發兩案通報：DeepMind 的 GraphCast 與華為的 Pangu-Weather，在 ERA5 回測與實時預報中，多項指標擊敗 ECMWF HRES——那可是全世界最準的確定性數值預報系統。

現場證據觸目驚心：

- 傳統 NWP 需解 Navier–Stokes 與熱力方程組，0.1 度全球 10 天預報要在超算上跑數小時；AI 模型推理僅需數十秒，號稱 847 倍乃至上千倍加速。
- Richardson 1922 年的夢想（算出天氣）與 Charney 1950 年的成功、Lorenz 1963 年的混沌警告，至此被逼到牆角：若 AI 不解方程也能預報，物理方程的地位何在？
- 氣象學家最在意的不是平均分數，而是極端事件（颱風路徑、熱浪、暴雨）：AI 會不會只是「平均的好學生」，大案要案就露餡？

兩名新偵探的手法截然不同，值得分頭訊問。

## 偵查過程（含數學式/表格/理論）

### 嫌犯甲：GraphCast，地球即圖

GraphCast 把地球網格化為多尺度網格圖（icosahedral multi-mesh），節點為格點，邊為空間鄰接，用圖神經網路做訊息傳遞。輸入為當前與 6 小時前兩個時刻的三維大氣狀態  $X_t$  與  $X_{t-1}$ ，輸出 6 小時後狀態：

$$
X_{t+1} = X_t + \mathrm{GNN}_{\theta}(X_t, X_{t-1}, F_t)
$$

其中  $F_t$  為強迫特徵（太陽輻射、地理資訊）， $\theta$  為網路參數。靠自迴歸滾動 40 步即得 10 天預報。訓練損失為多步加權均方誤差，越遠的 lead time 權重經特別設計，避免誤差累積爆炸。

### 嫌犯乙：Pangu-Weather，3D Earth Transformer

盤古氣象走 Transformer 路線，提出 3D Earth-Specific Transformer：把氣壓層高度當第三維，注意力偏置嵌入地球球面幾何與靜力平衡先驗。訓練採用層級時域聚合——對 1、3、6、24 小時間隔各訓一個模型，長預報用大步長模型跳躍，減少滾動步數：

$$
\hat{X}_{t+\Delta} = \mathrm{Pangu}_{\Delta}(X_t), \quad \Delta \in \{1,3,6,24\}h
$$

兩者皆以 ERA5 再分析為「案卷教材」（1979–2021），以  $RMSE$  與  $ACC$  為考績：

$$
RMSE = \sqrt{\overline{(F-O)^2}}, \quad ACC = \mathrm{corr}(F-C, O-C)
$$

其中  $F$  為預報， $O$  為觀測或分析， $C$  為氣候態。上式中  $RMSE$  越小越好， $ACC$  越接近 1 越好（0.6 常視為可用預報上限）。

| 勘驗指標（10 天內多數層級） | ECMWF HRES | GraphCast / Pangu-Weather |
|----------------------------|------------|----------------------------|
| 500 hPa 位勢  $RMSE$  | 基準線 | 全面更低，GraphCast 約 90% 變數勝出 |
| 2 米溫度、10 米風速  $ACC$  | 基準線 | 多數 lead time 反超 |
| 颱風路徑誤差 | 物理系綜黃金標準 | 單模型可比肩，系綜仍待考 |
| 推理耗時 | 超算數小時 | 單卡數十秒，加速約 847 倍以上 |
| 物理一致性 | 質量能量守恆內建 | 無硬約束，偶發不連續與譜模糊 |

偵探的結論出人意料：AI 並未推翻 Navier–Stokes，而是把 ERA5（本身就是 NWP 同化的產物）當老師傅，用函數逼近學會了「解算子」的捷徑。NWP 仍是資料之母，AI 是加速的學徒。

### 關鍵證詞：比分怎麼算才算數？

WeatherBench 規定按等面積加權與氣壓層分層彙整  $RMSE$  與  $ACC$ ，避免極區小格喧賓奪主。AI 模型的勝利不是單一變數的僥倖：在 500 hPa 位勢、850 hPa 溫度、2 米溫度等核心場上全面開花，統計顯著性經配對檢定確認，這才讓 ECMWF 服氣。

## 結案報告

2023 年結案：確定性中期預報的王座易主。就平均技巧分而言，AI 天氣模型正式超越最強 NWP；2024 年 ECMWF 自己的 AIFS 也轉向 AI 路線，等於官方認輸並招安。

但三條尾巴未結：

- 外推風險：氣候暖化下的未見極端，純資料模型能否外推？物理約束（守恆、譜連續）如何加回？
- 機率預報：防災要的是不確定性，確定性單值再準也不夠——此缺口由 2024–2025 年的 GenCast 等機率模型補上。
- 資料依賴：ERA5 既是訓練集又是評分尺，有「用考題練功再考同一題」的循環論證之虞；實時 operational 評估仍在進行。

儘管如此，本案的歷史地位已定：繼蛋白質折疊之後，流體地球的模擬也被 AI 攻陷，計算模擬學從「解方程」走向「學算子」。

### 卷末附記：Lorenz 的幽靈還在嗎？

混沌並未被贖買。AI 的可用預報只比 HRES 長約 1 天，10 天之後  $ACC$  照樣跌破 0.6——蝴蝶還在扇翅膀，只是 AI 把翅膀扇動前的每一步走得更穩。真正的決戰在機率預報：誰能誠實地說出「我不知道」，誰才是下一個時代的偵探。

## 證據與工具

- 關鍵公式：自迴歸動力學  $X_{t+1}$  、多步  $RMSE$  損失、異常相關  $ACC$  、球面圖訊息傳遞更新。
- 核心工具：ERA5 再分析資料、GraphCast 開源權重（JAX）、Pangu-Weather 推理碼、WeatherBench 評測基準、 $RMSE$  與  $ACC$  按氣壓層與 lead time 分層表。
- 動手線索：用 WeatherBench 載入 500 hPa 位勢場，計算持續性預報的  $ACC$  隨 lead time 衰減曲線，再疊上 GraphCast 論文曲線，體會 AI 把可用預報延長了約 1 天的含義。

| 模型檔案 | 步長 | 用途 |
|----------|------|------|
| GraphCast 6h 步進 | 6 小時 | 滾動 40 步得 10 天預報 |
| Pangu 1/3/6/24h | 多步長 | 長 lead time 用大步模型跳躍 |
| AIFS（ECMWF 接班人） | 6 小時 | 官方 AI 化，2024 年上線試驗 |

- 術語對照：HRES（高解析確定性預報）、ENS（系綜預報）、 $RMSE$ （均方根誤差）、 $ACC$ （異常相關係數）。
- 史料座標：Richardson（1922）→ Charney（1950）→ Lorenz（1963）→ GraphCast/Pangu（2023），NWP 百年線一次收束。

## 補充：程式實作

對應程式：[2023-neural_weather_toy.py](_code/2023-neural_weather_toy.py)

本節以一維平流擴散玩具重演本文核心理論：以線性迴歸充當最小版 AI 算子，學習單步動力學 $X_{t+1}=f(X_t)$ ，對決持續性預報。

真值由平流 Courant 數 0.4 與擴散數 0.04 生成，AI 以鄰點模板 $w$ 預報下一時刻，呼應 GraphCast 自迴歸滾動與多步 $RMSE$ 評分的精神。

評分沿用 $RMSE$ 越小越好之準則：在後半 1000 步測試段上，要求 AI 相對改進至少 20% ，方算真正超越數值基線。

執行方式：

```bash
python3 _code/2023-neural_weather_toy.py
```

實測關鍵輸出（本次真實執行結果抄錄）：

```text
真值: 1D 平流擴散 N=32, C=0.4, R=0.04, 測試步數=1000
持續性 RMSE = 0.06515
AI 線性迴歸 RMSE = 0.05020
相對改進 = 23.0% (要求 >= 20%)
VERIFICATION: persist=0.06515 ai=0.05020 improve=0.230 PASS
```

數字解讀：持續性基線誤差為 0.06515 ，AI 降至 0.05020 ，相對改進達 23.0% ，跨過 20% 門檻，學得模板約為 $w=[0.436,0.525,0.038]$ 。

這正是 2023 年案情的縮影：不解方程、只學算子，單步穩一點，滾動 40 步後便是可用預報多出約 1 天的差距。

兇手認罪了：平均分數的王座易主，蝴蝶雖還在扇翅膀，但學徒已比老師傅走得更穩。

讀者可改 Courant 數 $C$ （如 0.2 或 0.6 ）或強迫強度 $SIG$ 做實驗，觀察改進幅度如何消長。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""2023 一維平流擴散「AI 天氣預報」玩具 (對應 wiki：計算模擬學 / AI 預報・GraphCast 等)。

背景：2023 年 GraphCast 等 AI 天氣模型以數據驅動超越傳統數值預報。
此處一維平流-擴散真值：u_t + c u_x = D u_xx + 隨機強迫（維持變異），
比較 (a) 持續性預報（明天=今天） vs (b) 線性迴歸「AI」（以 [u_{i-1},u_i,u_{i+1}] 預報下一時刻），
在測試段驗證 AI 的 RMSE 至少比持續性好 20%。

只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(2023)

N = 32        # 格點數（週期邊界）
C = 0.4       # Courant 數 c*dt/dx
R = 0.04      # 擴散數 D*dt/dx^2
SIG = 0.05    # 隨機強迫強度
T = 2000      # 總步數
SPLIT = 1000  # 前半訓練、後半測試


def step(u):
    un = (u - C * (u - np.roll(u, 1)) + R * (np.roll(u, -1) - 2 * u + np.roll(u, 1)))
    un += SIG * np.random.randn(N)
    return un


def main():
    # 初值：正弦疊加
    x = np.arange(N)
    u = np.sin(2 * np.pi * x / N) + 0.5 * np.sin(4 * np.pi * x / N + 1.0)
    traj = np.zeros((T + 1, N))
    traj[0] = u
    for t in range(T):
        u = step(u)
        traj[t + 1] = u

    # 訓練：特徵 [u_{i-1}, u_i, u_{i+1}, 1] -> u_i(t+1)
    def build(seg):
        Xs, ys = [], []
        for t in range(seg.start, seg.stop):
            ut = traj[t]
            Xs.append(np.stack([np.roll(ut, 1), ut, np.roll(ut, -1),
                                np.ones(N)], axis=1))
            ys.append(traj[t + 1])
        return np.concatenate(Xs), np.concatenate(ys)

    Xtr, ytr = build(range(SPLIT))
    Xte, yte = build(range(SPLIT, T))
    w, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)

    # 測試段：持續性 vs AI
    persist_err2, ai_err2, cnt = 0.0, 0.0, 0
    for t in range(SPLIT, T):
        ut, unext = traj[t], traj[t + 1]
        persist_err2 += np.mean((unext - ut) ** 2)
        ai_pred = np.stack([np.roll(ut, 1), ut, np.roll(ut, -1),
                            np.ones(N)], axis=1) @ w
        ai_err2 += np.mean((unext - ai_pred) ** 2)
        cnt += 1
    rmse_p = float(np.sqrt(persist_err2 / cnt))
    rmse_ai = float(np.sqrt(ai_err2 / cnt))
    improve = (rmse_p - rmse_ai) / rmse_p

    print(f"真值: 1D 平流擴散 N={N}, C={C}, R={R}, 測試步數={cnt}")
    print(f"學得權重 ( stencil + bias ): {w}")
    print(f"持續性 RMSE = {rmse_p:.5f}")
    print(f"AI 線性迴歸 RMSE = {rmse_ai:.5f}")
    print(f"相對改進 = {improve * 100:.1f}% (要求 >= 20%)")
    assert improve >= 0.20, "AI 未顯著優於持續性"
    print(f"VERIFICATION: persist={rmse_p:.5f} ai={rmse_ai:.5f} improve={improve:.3f} PASS")


if __name__ == "__main__":
    main()
```
