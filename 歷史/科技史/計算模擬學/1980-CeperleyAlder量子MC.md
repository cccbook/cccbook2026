# 1980 年 Ceperley-Alder 量子 Monte Carlo：電子氣的基準口供

> 報案人：密度泛函的缺口。案情：交換相關能無人算準，LDA 是空中樓閣。
> 偵探 Ceperley 與 Alder 用節點固定 DMC 逼供電子氣，交出  $r_s$  相圖。

| 案件檔案 | 內容 |
|----------|------|
| 發生時間 | 1980 年 |
| 發生地點 | 美國 Livermore、Berkeley 連線 |
| 報案人 | Kohn-Sham DFT、Wigner 晶體預言 |
| 偵探 | David Ceperley、B. J. Alder |
| 兇器 | 節點固定 DMC、電子氣、 $r_s$  |
| 結論 | LDA 有了數據地基，QMC 成年 |

## 案發現場

1980 年的電子結構是一間證據不足的法庭。

Hohenberg-Kohn 說密度決定一切，Kohn-Sham 化為單粒子，
只剩交換相關能  $E_{xc}$  無人能算。LDA 把不均勻電子比作均勻氣，
卻連均勻氣精確能量都拿不出來。

另有古老懸案。Wigner 在 1934 年預言低密度電子結晶，
中等密度或鐵磁或順磁，相界全靠猜。
微擾在高密度尚可，低密度失守，變分法又被試驗函數綁架。

Ceperley 師承 Alder，決定用擴散 Monte Carlo 養電子，
虛時間演化投影基態，節點固定馴服費米符號問題。
均勻電子氣是完美被害人：只有密度參數  $r_s$  ，
即電子間距以 Bohr 半徑為單位，算準它等於為 LDA 打樁。

## 偵查過程

偵查從虛時間方程開始，波函數隨  $\tau$  演化：

$$
-\frac{\partial \Psi}{\partial \tau} = (H - E_T)\Psi
$$

其中  $\Psi$  為波函數， $H$  為哈密頓量，
 $E_T$  為試驗能量， $\tau$  為虛時間。
長時演化投影到基態，行走者分支殺死實現加權。

費米統計是內鬼。節點把空間切成正負區，
直接採樣正負相消。節點固定下令不許穿越試驗節點面，
代價是能量變成變分上界。

偵探用 Slater-Jastrow 帶路：

$$
\Psi_T = D_\uparrow D_\downarrow \exp(-U)
$$

其中  $D$  為 Slater 行列式， $U$  為 Jastrow 因子。
計算用  $N = 38$  至 250 電子，外推熱力學極限，
掃描  $r_s$  ，三相對質。

| 密度參數  $r_s$  | 基態相 | 磁性 |
|------------------|--------|------|
| 小  $r_s$  | 順磁流體 | 未極化 |
| 中  $r_s$  | 鐵磁過渡 | 部分極化 |
| 大  $r_s$  約 100 | Wigner 晶體 | 局域化 |

相關能擬合成  $r_s$  函數，Perdew-Zunger 參數化為 LDA 標準，
每套 DFT 軟體至今傳喚此口供。有限尺寸、步長、節點三重外推，
缺一不可。

## 結案報告

1980 年論文發表，均勻氣有了基準答案，
LDA 從猜測變成有地基的大樓。

遺產有三：DFT 可用化，沒有此數據，
Kohn-Sham 只是空殼；QMC 成年，節點問題成顯學；
相圖定案，Wigner 晶體從爭吵變事實。

兇手近似誤差改判可控上界，電子氣每個數字都被抄進法典。

## 證據與工具

關鍵證物一：DMC 隨機行走虛擬碼。

```python
# walkers 為行走者系綜，tau 為虛時間步
for step in range(nsteps):
    drift_diffuse(walkers, psi_trial, tau)
    for w in walkers:
        if crosses_node(w, psi_trial):
            kill(w)  # 禁止穿越節點
        else:
            branch_or_kill(w, local_energy(w))
```

關鍵證物二： $r_s$  速查。

| 符號 | 定義 | 意義 |
|------|------|------|
|  $r_s$  | 間距除以 Bohr 半徑 | 密度標尺 |
| 高密度 | 小  $r_s$  | 動能主宰 |
| 低密度 | 大  $r_s$  | 庫侖主宰 |

延伸閱讀伏筆：此地基將支撐 1985 年 Car-Parrinello 從頭 MD。
