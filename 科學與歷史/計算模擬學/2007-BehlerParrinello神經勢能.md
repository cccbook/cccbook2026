# 2007 年 Behler–Parrinello 神經勢能：原子各懷神經的結社之案

> 副標題：每個原子都藏了一顆小腦袋，合起來騙過了薛丁格方程。
> 年表定位：第四幕第四案，承接 DFT 與 Car–Parrinello，開啟機器學習勢能時代。

## 案發現場

2007 年之前，計算化學卡在一道兩難的鐵門前，門上刻著精度與速度不可兼得。

門左邊是密度泛函理論（DFT）。它能算鍵結、能算反應，精度足以讓化學家點頭，但代價是立方標度：體系翻倍，耗時變八倍。幾百個原子跑幾十皮秒已是壯舉，想看水相變、材料斷裂、大蛋白動態？門都沒有。

門右邊是經驗力場。Lennard-Jones 加庫侖加諧波，跑百萬原子如喝水，但遇到成鍵斷鍵就露餡。參數是人手調的，換個體系就得重調，像只會背口供不會推理的線人。

案發現場還有第三道陰影：神經網路在當時仍是可疑人物。2007 年深度學習尚未爆發，用神經網路擬合勢能面聽起來像江湖把戲。審稿人皺眉：黑箱、無物理、外推必死，你拿什麼保證能量守恆與旋轉不變？

就在此時，Jörg Behler 與 Michele Parrinello（沒錯，又是那位填溝獵人）聯手遞上一份結社計畫書：不訓練一個大腦預測總能量，而是讓每個原子各懷一顆小神經網路，再把原子能量加起來。這篇 2007 年發表於 Physical Review Letters 的論文，就是機器學習勢能的開山之案。

## 偵查過程（含數學式/表格/理論）

### 推理一：原子能量求和，把廣延性寫進基因

總能量必須是廣延量：體系 double，能量 double。Behler–Parrinello 的第一推理是把總能量拆成原子貢獻之和。設體系有 $N$ 個原子，第 $i$ 個原子的環境描述符為 $G_i$ ，其原子神經網路輸出原子能量 $E_i$ ，則總能量 $E$ 為 $E=\sum E_i(G_i)$ 的求和形式。

寫成獨立公式即：

$$
E=\sum_{i=1}^{N}E_i(G_i)
$$

其中 $E_i$ 由同一元素共用的神經網路給出， $G_i$ 是對稱函數向量， $N$ 是原子總數。力則由解析微分得到：

$$
F_{i,\alpha}=-\frac{\partial E}{\partial R_{i,\alpha}}
$$

其中 $R_{i,\alpha}$ 是第 $i$ 個原子在 $alpha$ 方向的座標。因為能量是座標的可微函數，能量守恆與動量守恆自動成立。這是全案物理合法性的第一根支柱。

### 推理二：對稱函數，把物理對稱變成指紋

神經網路不能直接吃直角座標，否則平移旋轉一下就認不得人。Behler 與 Parrinello 設計了對稱函數（symmetry functions），把原子周圍的環境編碼成不變量。

徑向函數捕捉距離分佈，設鄰居為 $j$ ，截斷半徑為 $R_c$ ，距離為 $R_{ij}$ ，則一類徑向描述符 $G_i^{rad}$ 可寫為高斯殼層求和；角向函數捕捉三體夾角，涉及 $theta_{ijk}$ 與距離衰減。概念表如下：

| 函數類 | 輸入 | 不變性 | 物理意義 |
|--------|------|--------|----------|
| 徑向對稱函數 | 鄰居距離 $R_{ij}$ | 平移、旋轉、置換不變 | 配位殼層密度 |
| 角向對稱函數 | 夾角 $theta_{ijk}$ | 同上 | 鍵角與四面體性 |
| 截斷函數 | $R_c$ 內平滑衰減 | 保證連續性 | 有限程交互，力無跳變 |

截斷函數的典型形式為餘弦型：當 $R_{ij}$ 小於 $R_c$ 時平滑降到零，超出則恆為零。這保證原子進出截斷球時能量連續，MD 不會被脈衝震散。

訓練目標則是同時擬合能量與力：

$$
L=w_E|E^{NN}-E^{DFT}|^2+w_F\sum_{i,\alpha}|F_{i,\alpha}^{NN}-F_{i,\alpha}^{DFT}|^2
$$

其中上標 $NN$ 代表神經網路預測，上標 $DFT$ 代表第一性原理標籤， $w_E$ 與 $w_F$ 為權重。數據來自 DFT 計算的構形採樣，一個矽、一個水、一個銅，逐一攻破。

### 推理三：DFT 精度、MD 速度的驗屍對比

功效如何？以當年展示的矽與水為例，BP 神經勢能把 DFT 勢能面的誤差壓到每原子數個 meV，力誤差約零點幾 eV 每埃，而速度比 DFT 快三到四個數量級。下表是辦案前後的對比筆錄：

| 指標 | DFT（證人 A） | 經驗力場（證人 B） | BP 神經勢能（新偵探） |
|------|---------------|--------------------|------------------------|
| 能量精度 | 基準真相 | 誤差大，鍵斷即錯 | 逼近 DFT，meV 量級 |
| 反應與成鍵 | 可處理 | 基本無能 | 可處理，隨數據而定 |
| 速度 | 慢，百原子級 | 快，百萬原子級 | 居中偏快，萬原子級起 |
| 可遷移性 | 通用 | 需重參數化 | 內插強，外推弱 |

代價是數據飢渴：每個新體系都要跑上萬個 DFT 構形當教材，且外推到未見相空間時可能一本正經地胡說八道。這為後來的 active learning 與不確定性量化埋下伏筆。

### 推理四：為何是 2007？天時地利

此案能破，有三個共犯：DFT 數據管夠（PBE 泛函加平面波已成熟）、前饋神經網路訓練可行（LM 與反向傳播夠用）、Parrinello 的 MD 眼光（知道什麼精度才夠跑相變）。Behler 帶來神經網路手藝，Parrinello 帶來問題意識，兩人一拍即合。十年後 DeePMD、ANI、SchNet、MACE 全是這個結社的後裔。

## 結案報告

Behler–Parrinello 2007 沒有終結 DFT，也沒有殺死力場，但它撬開了第三條路：用機器學習縫合精度與速度。

遺產有三：

其一，範式遺產。原子能量求和加不變描述符，成為此後十五年機器學習勢能的標準作業程序。等變圖神經網路只是把它做得更優雅。

其二，應用遺產。水、矽、銅氧化物、高壓相變，許多 DFT 算不動的相圖第一次被高精度走通。增強採樣（如元動力學）配上神經勢能，更是如虎添翼。

其三，警示遺產。外推危險、數據偏差、長程作用缺失（靜電、色散需另行處理），這些 2007 年的案底，至今仍是每一代新模型的必考題。

結案語：真相（DFT 精度）不必每次都親臨現場，訓練一個可靠的線人（神經勢能）去跑腿，也是一種破案。

## 證據與工具

- 關鍵公式一：原子能量求和 $E=\sum E_i(G_i)$ ，廣延性由構造保證。
- 關鍵公式二：力解析微分 $F_{i,\alpha}$ ，見偵查過程，守恆自動成立。
- 關鍵公式三：能量加力聯合損失 $L$ ，權重 $w_E$ 與 $w_F$ 需調校。
- 描述符表：徑向加角向對稱函數，截斷半徑 $R_c$ 常取 6 至 10 埃。
- 工具鏈：DFT（VASP、Quantum ESPRESSO）產數據，RuNNer、n2p2、DeePMD-kit 跑訓練與 MD。
- 辦案心法：先保證對稱性，再談擬合精度。吃直角座標的神經網路，一律視為嫌疑犯。
- 延伸卷宗：前案是 [2002-Metadynamics增強採樣.md](2002-Metadynamics增強採樣.md)，後案是 [2013-多尺度模擬諾貝爾獎.md](2013-多尺度模擬諾貝爾獎.md)，看多尺度思想如何加冕。

## 補充：程式實作

對應程式：[2007-neural_pair_potential.py](_code/2007-neural_pair_potential.py)

本節以一維 Morse 勢玩具重演本文核心理論：用全手刻小 MLP 擬合勢能面 $V(x)$ ，再以數值微分求力，驗證能量與力雙達標。

網路結構為 1-16-16-1 的 tanh 前饋網路，以 Adam 訓練 2000 步，訓練資料來自解析 Morse 勢，呼應原文以 DFT 數據蒸餾神經勢能的手法。

力的驗證呼應 $F=-\partial E/\partial R$ 的解析微分精神：勢能擬合得好還不夠，微分後的力場必須同樣可靠，MD 才不會散架。

執行方式：

```bash
python3 _code/2007-neural_pair_potential.py
```

實測關鍵輸出（本次真實執行結果抄錄）：

```text
MLP 1-16-16-1 tanh, Adam 2000 步, lr=0.01
測試能量 RMSE = 0.00089 (要求 < 0.02)
測試力 RMSE   = 0.08436 (要求 < 0.1)
VERIFICATION: rmse=0.00089 force_rmse=0.08436 PASS
```

數字解讀：測試集能量均方根誤差僅 0.00089 ，遠低於 0.02 的門檻，約為容忍值的二十分之一，勢能面幾乎完全重合。

力的均方根誤差為 0.08436 ，同樣壓進 0.1 以內，證明數值微分力場可用，這正是原文聯合損失 $L$ 同時要求能量與力的用意。

線人通過測謊：這個小 MLP 背下的口供，與 Morse 真相逐字相符，可以派去跑腿了。

讀者可改隱藏層寬度 $H$ （如 8 或 32 ）或訓練步數 $STEPS$ 做實驗，觀察能量與力誤差如何消長。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""2007 以 numpy 手刻小 MLP 擬合 1D Morse 勢 (對應 wiki：計算模擬學 / 機器學習勢・Behler-Parrinello)。

背景：Behler & Parrinello (2007) 用神經網路擬合勢能面。
此處玩具版：Morse 勢 V(x)=D(1-exp(-a(x-re)))^2，MLP 結構 1-16-16-1 (tanh)，
全手刻反向傳播 + Adam 訓練 2000 步。驗證測試 RMSE<0.02、力 RMSE<0.1。

只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(2007)

# Morse 參數
D, A, RE = 1.0, 1.5, 1.0
NTR, NTE = 200, 100
H1 = H2 = 16
STEPS = 2000
LR = 0.01


def morse(x):
    return D * (1.0 - np.exp(-A * (x - RE))) ** 2


def morse_force(x):
    e = np.exp(-A * (x - RE))
    return -2 * D * A * (1 - e) * e  # F = -dV/dx


def init(n_in, n_out):
    return np.random.randn(n_in, n_out) * np.sqrt(1.0 / n_in)


def forward(xn, P):
    W1, b1, W2, b2, W3, b3 = P
    z1 = xn @ W1 + b1
    a1 = np.tanh(z1)
    z2 = a1 @ W2 + b2
    a2 = np.tanh(z2)
    out = a2 @ W3 + b3
    return out, (xn, z1, a1, z2, a2)


def main():
    xtr = np.random.uniform(0.4, 3.0, NTR)
    xte = np.random.uniform(0.4, 3.0, NTE)
    ytr = morse(xtr)
    yte = morse(xte)

    # 標準化（用訓練集統計）
    xm, xs = xtr.mean(), xtr.std()
    ym, ys = ytr.mean(), ytr.std()
    XTR = ((xtr - xm) / xs).reshape(-1, 1)
    YTR = ((ytr - ym) / ys).reshape(-1, 1)
    XTE = ((xte - xm) / xs).reshape(-1, 1)

    W1, b1 = init(1, H1), np.zeros(H1)
    W2, b2 = init(H1, H2), np.zeros(H2)
    W3, b3 = init(H2, 1), np.zeros(1)
    P = [W1, b1, W2, b2, W3, b3]
    # Adam 狀態
    m = [np.zeros_like(p) for p in P]
    v = [np.zeros_like(p) for p in P]
    b1a, b2a, eps = 0.9, 0.999, 1e-8

    N = NTR
    for t in range(1, STEPS + 1):
        out, (xn, z1, a1, z2, a2) = forward(XTR, P)
        err = (out - YTR) / N  # d(MSE)/d out（含 1/N；MSE=mean(err^2) 的梯度為 2*.../N，此處合併常數由 lr 吸收）
        # 反傳
        dW3 = a2.T @ (2 * err)
        db3 = (2 * err).sum(axis=0)
        da2 = (2 * err) @ W3.T
        dz2 = da2 * (1 - a2 ** 2)
        dW2 = a1.T @ dz2
        db2 = dz2.sum(axis=0)
        da1 = dz2 @ W2.T
        dz1 = da1 * (1 - a1 ** 2)
        dW1 = xn.T @ dz1
        db1 = dz1.sum(axis=0)
        grads = [dW1, db1, dW2, db2, dW3, db3]
        for i in range(len(P)):
            m[i] = b1a * m[i] + (1 - b1a) * grads[i]
            v[i] = b2a * v[i] + (1 - b2a) * grads[i] ** 2
            mh = m[i] / (1 - b1a ** t)
            vh = v[i] / (1 - b2a ** t)
            P[i] -= LR * mh / (np.sqrt(vh) + eps)

    W1, b1, W2, b2, W3, b3 = P

    def predict(x):
        xn = ((x - xm) / xs).reshape(-1, 1)
        out, _ = forward(xn, P)
        return (out.ravel() * ys + ym)

    pred_te = predict(xte)
    rmse = float(np.sqrt(np.mean((pred_te - yte) ** 2)))
    # 力：MLP 數值微分 vs 解析力
    h = 1e-4
    f_pred = -(predict(xte + h) - predict(xte - h)) / (2 * h)
    f_true = morse_force(xte)
    frmse = float(np.sqrt(np.mean((f_pred - f_true) ** 2)))

    print(f"MLP 1-16-16-1 tanh, Adam {STEPS} 步, lr={LR}")
    print(f"測試能量 RMSE = {rmse:.5f} (要求 < 0.02)")
    print(f"測試力 RMSE   = {frmse:.5f} (要求 < 0.1)")
    ok = (rmse < 0.02) and (frmse < 0.1)
    assert ok, "精度未達標"
    print(f"VERIFICATION: rmse={rmse:.5f} force_rmse={frmse:.5f} PASS")


if __name__ == "__main__":
    main()
```
