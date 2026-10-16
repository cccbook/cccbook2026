# 2002 年 Metadynamics 增強採樣：填溝擒獸的獵人筆記

> 副標題：Laio 與 Parrinello 往自由能的陷阱裡一鏟一鏟填沙，直到獵物無處藏身。
> 年表定位：第四幕第三案，承接 Metropolis 採樣與 MD 動力學，專治罕見事件。

## 案發現場

2002 年之前，分子動力學有一樁公開的無力感：跑得動，但跨不過。

模擬的牛頓步伐忠實而短視。原子在能量阱裡來回震盪，奈秒級軌跡看似熱鬧，卻跨不過數十 $k_BT$ 的能壘。蛋白質折疊、化學反應、晶體成核—— 這些真正重要的戲碼全是罕見事件，等待時間是微秒到秒，而步長是飛秒。一場 MD 像在山谷裡踱步的獵人，明知隔壁山頭有猛獸，卻一輩子翻不過山口。

當時的嫌疑人有兩名：

第一，時間尺度鴻溝。算力每年成長，但能壘跨越時間隨壘高指數增長，暴力延長軌跡永遠追不上。

第二，自由能未知。體系的平衡分佈由自由能 $F(s)$ 決定，但 $F(s)$ 正是我們想求的。獵人連地圖都沒有，遑論圍捕。

地點轉到瑞士盧加諾。Alessandro Laio 與 Michele Parrinello 盯著這個困局，提出一個帶著泥土氣的想法：既然翻不過山口，就把山谷填平。往走過的地方倒沙子，倒到谷底與山口齊平，體系自然被趕出去探險。這就是 Metadynamics（元動力學）。

## 偵查過程（含數學式/表格/理論）

### 推理一：集體變數，把高維鎖定為低維

全原子座標維度動輒上萬，直接填溝等於填海。第一步是選定少數集體變數（collective variables），記為 $s$ 。 $s$ 可以是距離、配位數、二面角、路徑變數，總之是能區分反應物與產物的慢座標。

體系沿 $s$ 的平衡分佈滿足 $P(s)\propto\exp(-F(s)/k_BT)$ ，其中 $F(s)$ 是待求的自由能面， $k_B$ 是 Boltzmann 常數， $T$ 是溫度。採樣問題於是化約為：如何在低維 $s$ 空間裡逼出 $F(s)$ 。

選 $s$ 是全案最像偵探直覺的一步：

| 好的 $s$ | 壞的 $s$ | 後果 |
|----------|----------|------|
| 區分亞穩態 | 混疊不同態 | 填溝填到錯誤的谷 |
| 包含慢自由度 | 遺漏正交慢模 | 遲滯嚴重，難以收斂 |
| 連續可微 | 不可微或突變 | 偏置力無法計算 |
| 低維（1 至 3 維） | 高維 | 高斯填料指數膨脹 |

### 推理二：填溝偏置，一鏟一鏟趕出山谷

Metadynamics 的詭計是沿軌跡不斷沉積高斯小丘，構築隨時間增長的偏置勢 $V(s,t)$ 。標準寫法是沉積高度為 $w$ 、寬度為 $sigma$ 的高斯之和，形式可記為 $V(s,t)=\sum w\exp(-(s-s_t)^2/2\sigma^2)$ 的累加，其中 $s_t$ 是 $t$ 時刻的 CV 位置。

更嚴謹的連續沉積形式寫成獨立公式：

$$
V(s,t)=\sum_{t'\leq t}w\exp\left(-\frac{(s-s_{t'})^2}{2\sigma^2}\right)
$$

其中求和遍及過去的沉積時刻 $t'$ ， $w$ 為高斯高度， $sigma$ 為高斯寬度， $s_{t'}$ 為當時的 CV 座標。體系感受到的有效自由能變成 $F(s)+V(s,t)$ ，走過的谷被逐漸填平，最終被迫翻山。

直觀的時間表如下：

| 階段 | 谷中景象 | 偏置勢狀態 |
|------|----------|------------|
| 初期 | 在谷底震盪 | 小丘零星出現 |
| 中期 | 谷底變淺，偶爾探出谷口 | 小丘連成土堆 |
| 後期 | 自由穿梭兩谷之間 | 偏置勢與自由能互補 |
| 收斂 | 均勻漫遊 | $V(s,t)$ 起伏即答案 |

### 推理三：自由能重建與 well-tempered 改良

原始 Metadynamics 有個莽撞之處：沙子一直倒，遲早淹沒一切， $V(s,t)$ 永遠震盪不收斂。Laio 與 Parrinello 很快意識到，填溝的終點應是自由能的負像：

$$
F(s)\approx -V(s,t\to\infty)+C
$$

其中 $C$ 為無關緊要的常數。這就是自由能重建公式：把填進去的土堆倒過來看，就是原來的地形。

2008 年 Barducci、Bussi 與 Parrinello 提出 well-tempered 版本，為莽漢套上韁繩。沉積高度隨已累積的偏置勢指數衰減：

$$
w(t)=w_0\exp\left(-\frac{V(s_t,t)}{k_B\Delta T}\right)
$$

其中 $w_0$ 是初始高度， $DeltaT$ 是可調的升溫參數， $k_B$ 是 Boltzmann 常數。當某處已填得很高，新沙自動變小，收斂變得平滑。最終的偏置勢與真實自由能滿足標度關係：

$$
V(s,t\to\infty)=-\frac{\Delta T}{T+\Delta T}F(s)+C
$$

調高 $DeltaT$ 則探索更激進，調低則接近普通 MD。這一招把填溝從爆破變成了園藝。

### 推理四：與傘形採樣的對質

老派方法是傘形採樣（umbrella sampling）：預先在各窗口加諧波束縛，分段算自由能再用 WHAM 拼接。它像預先佈置崗哨，穩但笨，需要事先知道路徑。Metadynamics 則是自我驅動的獵犬，不需預設窗口，自己聞著走過的氣味往前衝。兩者的對比堪稱兩代偵探之別。

## 結案報告

Metadynamics 一舉把罕見事件變成了可計算事件。化學反應路徑、藥物結合與解離、晶體多形、蛋白質構形變化—— 只要選得出 $s$ ，就能填溝擒獲。

它的遺產有三：

其一，方法家族的開枝散葉。well-tempered、bias-exchange、parallel-tempering metadynamics、infrequent metadynamics 求速率，每一種都是填溝術的新槍法。

其二，軟體的普及。PLUMED 外掛讓 GROMACS、AMBER、LAMMPS、Quantum ESPRESSO 全都能填溝，一個輸入檔即開工。

其三，觀念的逆轉。自由能不再是跑無限長軌跡後的統計殘羹，而是主動建構出來的地形。這為後來的機器學習勢能與增強採樣聯手（用神經勢能跑元動力學）鋪平了道路。

結案語：獵人沒有變快，獵人只是學會了填谷。山還在那裡，但地圖已經畫完。

## 證據與工具

- 關鍵公式一：高斯沉積的偏置勢 $V(s,t)$ ，累加形式見偵查過程。
- 關鍵公式二：自由能重建 $F(s)$ 近似為偏置勢的負像，見上式。
- 關鍵公式三：well-tempered 高度衰減 $w(t)$ ，由 $DeltaT$ 控制探索強度。
- 參數表：高度 $w$ 常取零點幾 $k_BT$ ，寬度 $sigma$ 取 CV 起伏的三分之一，沉積間隔數百步，見上表。
- 工具鏈：PLUMED、GROMACS、AMBER、CP2K，CV 庫含距離、配位數、RMSD、路徑變數。
- 辦案心法：先選 $s$ ，再填溝。CV 選錯，沙子全倒進臭水溝。
- 延伸卷宗：前案是 [1999-Rosetta蛋白質預測.md](1999-Rosetta蛋白質預測.md)，後案是 [2007-BehlerParrinello神經勢能.md](2007-BehlerParrinello神經勢能.md)，看勢能本身如何被神經網路接管。

## 補充：程式實作

對應程式：[2002-metadynamics_1d.py](_code/2002-metadynamics_1d.py)

本節用一維雙阱玩具重演本文核心理論：以過阻尼 Langevin 動力學沿集體變數 $s$ 演化，並週期性沉積高斯小丘構築偏置勢 $V(s,t)$ 。

重建公式採用 well-tempered 標度關係，還原自由能 $F(s)$ 為偏置勢的負像，偏置高度隨已累積高度指數衰減，收斂後兩阱應等高。

真實勢取 $V(x)=(x^2-1)^2$ ，兩阱位於 $x=\pm 1$ ，中央勢壘高 1.0 ，恰為 $k_BT=0.25$ 的四倍，是典型的罕見事件佈景。

執行方式：

```bash
python3 _code/2002-metadynamics_1d.py
```

實測關鍵輸出（本次真實執行結果抄錄）：

```text
步數=400000, 沉積 hills=2000, 躍遷次數=414
F(-1)=-2.6245, F(+1)=-2.5975, ΔF=0.0270 = 0.108 kT
驗證: transitions>=10? True ; ΔF<0.5kT? True
VERIFICATION: transitions=414 dF_kT=0.1079 PASS
```

數字解讀：400000 步共沉積 2000 個高斯丘，觸發 414 次左右阱間躍遷，證明偏置勢已把山谷填到可自由翻山。

重建的兩阱自由能分別為 -2.6245 與 -2.5975 ，差值僅 0.0270 ，即 0.108 個 $k_BT$ ，遠小於 0.5 個 $k_BT$ 的驗證門檻。

嫌犯自首了：填進去的土堆倒過來看，果然就是原來的地形，兩座山谷一般深，結案。

讀者可改高斯寬 $sigma$ （如 0.10 或 0.25 ）或偏置因子 $GAMMA$ 做實驗，觀察躍遷次數與 $dF$ 如何消長。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""2002 一維雙阱 well-tempered metadynamics 玩具版 (對應 wiki：計算模擬學 / 增強採樣・metadynamics)。

背景：Laio & Parrinello (2002) metadynamics；Barducci 等 (2008) well-tempered 版。
真實勢 V(x)=(x^2-1)^2，兩阱在 x=±1（等深），勢壘在 x=0 高 1.0。
以過阻尼 Langevin + 週期性高斯偏置 Vb(s) 做玩具模擬，重建自由能
F(s) = -(gamma/(gamma-1)) * Vb(s)，驗證兩阱等高 (ΔF < 0.5 kT) 且發生多次躍遷。

只用 numpy，固定種子。偏置放在均勻網格上（向量化高斯沉積 + 線性內插力）。
"""
import numpy as np

np.random.seed(2002)

# ---- 物理與演算法參數 ----
KT = 0.25          # kT
GAMMA = 5.0        # bias factor (T+dT)/T
SIGMA = 0.15       # 高斯寬
W0 = 0.02          # 初始 hill 高
DT = 0.01
NSTEPS = 400000
DEPOSIT_EVERY = 200
XMIN, XMAX, NBIN = -2.0, 2.0, 400
DX = (XMAX - XMIN) / NBIN
GRID = np.linspace(XMIN + DX / 2, XMAX - DX / 2, NBIN)


def V(x):
    return (x * x - 1.0) ** 2


def dVdx(x):
    return 4.0 * x * (x * x - 1.0)


def bias_force(x, vb):
    idx = int((x - XMIN) / DX - 0.5)
    idx = max(1, min(NBIN - 2, idx))
    return (vb[idx + 1] - vb[idx - 1]) / (2 * DX)


def bias_at(x, vb):
    f = (x - XMIN) / DX - 0.5
    i0 = int(np.floor(f))
    i0 = max(0, min(NBIN - 2, i0))
    t = f - i0
    return (1 - t) * vb[i0] + t * vb[i0 + 1]


def main():
    vb = np.zeros(NBIN)
    # 向量化高斯模板（沉積時平移對齊）
    off = np.arange(NBIN) * DX  # 距離模板用相對座標計算
    x = -1.0
    state = -1
    transitions = 0
    sq = np.sqrt(2 * KT * DT)
    dT_factor = (GAMMA - 1.0) * KT

    for step in range(NSTEPS):
        fb = bias_force(x, vb)
        x = x - (dVdx(x) + fb) * DT + sq * np.random.randn()
        # 反射邊界
        if x < XMIN:
            x = 2 * XMIN - x
        elif x > XMAX:
            x = 2 * XMAX - x
        # 躍遷計數（遲滯：±0.5）
        if x < -0.5:
            s = -1
        elif x > 0.5:
            s = 1
        else:
            s = state
        if s != state:
            # 只計左右阱之間的切換（經由中間區不計，需真的到對側）
            transitions += 1
            state = s
        # 沉積高斯（well-tempered 高度衰減）
        if (step + 1) % DEPOSIT_EVERY == 0:
            h = W0 * np.exp(-bias_at(x, vb) / dT_factor)
            vb += h * np.exp(-0.5 * ((GRID - x) / SIGMA) ** 2)

    # 自由能重建：F = -(gamma/(gamma-1)) Vb；阱底取值為 ±1 附近區間平均以抑制單點雜訊
    scale = GAMMA / (GAMMA - 1.0)
    Fest = -scale * vb
    F_left = float(Fest[(GRID > -1.2) & (GRID < -0.8)].mean())
    F_right = float(Fest[(GRID > 0.8) & (GRID < 1.2)].mean())
    dF = abs(F_left - F_right)
    dF_kT = dF / KT

    print(f"步數={NSTEPS}, 沉積 hills={(NSTEPS // DEPOSIT_EVERY)}, 躍遷次數={transitions}")
    print(f"F(-1)={F_left:.4f}, F(+1)={F_right:.4f}, ΔF={dF:.4f} = {dF_kT:.3f} kT")
    ok_trans = transitions >= 10
    ok_f = dF_kT < 0.5
    print(f"驗證: transitions>=10? {ok_trans} ; ΔF<0.5kT? {ok_f}")
    assert ok_trans, "躍遷次數不足"
    assert ok_f, "自由能兩阱不等高"
    print(f"VERIFICATION: transitions={transitions} dF_kT={dF_kT:.4f} PASS")


if __name__ == "__main__":
    main()
```
