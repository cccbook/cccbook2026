# 1976 年 Warshel-Levitt QM/MM：酵素的多尺度手術刀

> 報案人：溶菌酶的催化之謎。案情：量子太貴，古典太瞎，活性中心無人敢算。
> 偵探 Warshel 與 Levitt 動起多尺度手術，把酵素切成 QM 與 MM 兩半。

| 案件檔案 | 內容 |
|----------|------|
| 發生時間 | 1976 年 |
| 發生地點 | 英國 Cambridge，MRC 實驗室 |
| 報案人 | 溶菌酶機制、Karplus 實驗室 |
| 偵探 | Arieh Warshel、Michael Levitt |
| 兇器 | 能量分割  $E$  、半經驗 QM、古典力場 |
| 結論 | QM/MM 開山，2013 年諾貝爾獎伏筆埋下 |

## 案發現場

1976 年的酵素模擬是一間收費昂貴的手術室。

X 光已拍出溶菌酶結構，催化殘基躺在裂縫裡，
但如何催化仍是懸案。鍵斷裂是量子事件，
整個酵素加水卻上萬原子，全量子計算無人敢接。

現場有兩個無能證人。量子化學能算小分子，
一到蛋白就標度爆炸。分子力學能算大體系，
卻用彈簧冒充化學鍵，電子重排一概不認。
更棘手的是環境，活性中心被蛋白靜電場調製，
真空計算與晶體事實不符。

Warshel 與 Levitt 分而治之：活性中心用量子，
其餘用古典，交界再動精細手術。多尺度不是妥協，
而是承認不同尺度有不同物理。

## 偵查過程

偵探把總能量剖成三塊，主兇器現形：

$$
E = E_{QM} + E_{MM} + E_{QM/MM}
$$

其中  $E_{QM}$  為量子區能量， $E_{MM}$  為古典區能量，
 $E_{QM/MM}$  為兩區耦合項， $E$  為總能量。

第一場審訊量子區。底物與關鍵殘基劃入  $QM$  ，
用半經驗方法處理，可極化可斷鍵。
第二場審訊古典區。骨架與水用分子力場描述：

$$
E_{MM} = E_{bond} + E_{angle} + E_{dihedral} + E_{vdW} + E_{elec}
$$

其中各項為鍵、角、二面角、凡得瓦與靜電，
 $E_{MM}$  便宜而穩定。

第三場審訊耦合項，最見刀工。含 QM 與 MM 電荷靜電作用、
兩區凡得瓦作用，以及切斷共價鍵的連接原子處理。

| 區域 | 方法 | 處理對象 | 精度代價 |
|------|------|----------|----------|
| QM 區 | 半經驗 QM | 底物加殘基 | 高精度高代價 |
| MM 區 | 古典力場 | 骨架加溶劑 | 低精度極便宜 |
| 邊界 | 連接原子 | 被切共價鍵 | 需校準 |
| 耦合 | 靜電嵌入 | 極化電場 | 成敗關鍵 |

溶菌酶一案中，蛋白靜電場把過渡態穩定數十千卡，
靜電催化假說第一次有了數字證詞。
連接原子必須小心約束，否則邊界變成新兇手。

## 結案報告

1976 年論文後，QM/MM 從奇技變顯學。
Warshel 發展 EVB，Field 引入從頭 QM/MM，
P450 與激酶機制紛紛被剖開。

遺產有三。第一，多尺度正名，縫合本身是科學，
2013 年諾貝爾獎即結案陳詞。第二，計算酶學誕生，
突變與反應壘可在電腦預演。第三，嵌入思想擴散，
DFT 嵌入 DMFT 全是同把刀的不同刀片。

兇手是靜電環境，幫兇是預組織骨架。

## 證據與工具

關鍵證物一：QM/MM 組裝虛擬碼。

```python
# qm_region 為活性中心，mm_region 為環境
e_qm = semi_empirical(qm_region, charges_mm)
e_mm = force_field(mm_region)
e_coupling = electrostatic(qm_region, mm_region) + vdw_boundary()
```

關鍵證物二：溶菌酶筆錄。

| 證物 | 內容 | 角色 |
|------|------|------|
| 底物 | 糖鏈六聚體 | 被害人 |
| Glu35 | 質子供體 | 主嫌 |
| Asp52 | 靜電穩定子 | 共犯 |

延伸閱讀伏筆：2013 年諾貝爾獎將為本案蓋棺。

## 補充：程式實作

> 嫌犯嫌量子太貴、古典太瞎，偵探乾脆把雙阱一切為二，讓兩派各守一攤對質。

對應程式：[1976-qmmm_double_well.py](_code/1976-qmmm_double_well.py)

本程式把真勢 $V(x) = (x^2-1)^2$ 切成 QM 與 MM 兩區，正是本文 $E = E_{QM} + E_{MM} + E_{QM/MM}$ 的迷你翻版。
左阱底盆地 $abs(x+1) < 0.25$ 用諧波近似 $V_{MM} = 4(x+1)^2$ 充當便宜的古典力場，其餘含能障與右阱全用精確勢充當量子區。
能障高度對稱地鎖在 1.0，MM 絕不越界去碰能障，以免諧波外推把粒子冤枉鎖死。
採樣用過阻尼 Langevin 在 $kT = 0.5$ 下跑 30 萬步，捨去前 3 萬步熱身，驗左右阱佔比是否回到對稱的 1 比 1。
分區精神正在此：反應中心精確處理，環境盆地近似代勞，耦合處共用同一條 Langevin 動力學縫合。

執行指令：

```bash
python3 _code/1976-qmmm_double_well.py
```

實測口供（種子固定為 0）：

```text
kT=0.5 dt=0.01 nstep=300000 burn=30000
frac_left=0.5258 frac_right=0.4742
VERIFY |frac_left-0.5|=0.0258 (<0.1? True)
PASS
```

解讀要點：

- 左阱佔比 0.5258、右阱 0.4742，偏離 0.5 僅 0.0258，通過 0.1 的結案門檻。
- 對稱雙阱在 $kT = 0.5$ 下本就該各據一半，數字證明 MM 近似沒有偏袒任何一邊。
- 步長 $dt = 0.01$ 配合 Euler-Maruyama 積分，30 萬步約數秒內收口供。
- 若把 MM 盆地硬擴到整個左半軸，能障會被高估到 4.0，粒子將被鎖死，這正是分區不當的反面教材。

讀者可改有效溫度 $kT$ （如降到 0.3 看跨障變難、佔比漲落變大）或 MM 盆地半徑 0.25，重跑看對稱性何時破功。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""1976 QM/MM 玩具模型：一維雙阱 + Langevin 採樣
對應 wiki：Warshel & Levitt (1976) QM/MM 多尺度；玩具實現左阱諧波近似(MM)+右阱精確(QM)。
真勢 V(x)=(x^2-1)^2，極小在 ±1；模型勢：左阱盆地內 (|x+1|<0.5) 用
V_MM=4(x+1)^2（在 -1 處二階泰勒，MM 區），其餘（含能障與右阱）用
V_QM=(x^2-1)^2（QM 區）。MM 區取阱底盆地 |x+1|<0.25（泰勒準確範圍），
能障對稱高度 1.0，過阻尼 Langevin 採樣驗證兩阱佔比≈1:1（誤差<0.1）。
註：若左半軸全用諧波，左能障高達 4.0 會把粒子鎖死，故 MM 只用於阱底盆地、
能障區共用精確勢，這正是 QM/MM 分區精神（反應中心精確、環境近似）。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

kT = 0.5
dt = 0.01
NSTEP = 300000
BURN = 30000


def qm_force(xi):
    return -4.0 * xi * (xi ** 2 - 1.0)


def mm_force(xi):
    return -8.0 * (xi + 1.0)


def force(x):
    # MM 盆地 (|x+1|<0.25) / 其餘 QM，純 numpy 向量化
    f = np.empty_like(x)
    m = np.abs(x + 1.0) < 0.25
    m = m & (x < 0)
    f[m] = -8.0 * (x[m] + 1.0)
    xr = x[~m]
    f[~m] = -4.0 * xr * (xr ** 2 - 1.0)
    return f


# 預先產生雜訊（向量化加速，<10 秒）
noise = np.random.randn(NSTEP)
x = np.empty(NSTEP, dtype=float)
x[0] = -1.0
sdt = np.sqrt(2.0 * kT * dt)
for i in range(1, NSTEP):
    # 單步 Euler-Maruyama：左阱底用 MM 諧波力，其餘用 QM 精確力
    xi = x[i - 1]
    if xi < 0 and abs(xi + 1.0) < 0.25:
        f = -8.0 * (xi + 1.0)  # MM
    else:
        f = -4.0 * xi * (xi ** 2 - 1.0)  # QM
    x[i] = xi + f * dt + sdt * noise[i]

xs = x[BURN:]
fL = float(np.mean(xs < 0))
fR = float(np.mean(xs >= 0))
err = abs(fL - 0.5)
print(f"kT={kT} dt={dt} nstep={NSTEP} burn={BURN}")
print(f"frac_left={fL:.4f} frac_right={fR:.4f}")
print(f"VERIFY |frac_left-0.5|={err:.4f} (<0.1? {err < 0.1})")
assert err < 0.1, f"well occupation biased: {fL} vs 0.5"
print("PASS")
```
