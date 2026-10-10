# 1933 年 Kolmogorov 公理化：機率論的幾何原本謀殺案

> 探案代號 ： 公理法庭
>
> 一句話案情 ： 機率究竟是頻率還是信念 ， 偵探用三條公理終結百年爭吵 。

**案件檔案**

| 項目 | 內容 |
|------|------|
| 案發時間 | 1933 年 |
| 案發地點 | 柏林 ， Springer 出版 Grundbegriffe der Wahrscheinlichkeitsrechnung |
| 主角 | Andrei Kolmogorov ， 承襲 Hilbert 第六問題的遺志 |
| 核心證物 | 三公理 ， 測度論機率空間  $(\Omega,\mathcal{F},P)$  |
| 涉案人物 | Hilbert ， Borel ， Lebesgue ， Fréchet ， von Mises ， de Finetti |
| 案件狀態 | 已破案 ， 現代機率論的地基 |
| 關聯案件 | 1931 年 Kolmogorov 方程 ， 1906 年 Markov 鏈 ， 1942 年 Itô 積分 |

## 案發現場

20 世紀初的機率論 ， 像一座沒有地基的豪宅 。

賭徒談賠率 ， 保險公司談死亡率 ， 物理學家談分子運動 ， 每個人都用機率 ， 卻沒有人說得清機率是什麼 。

von Mises 主張頻率說 ， 以無窮序列的極限定義機率 ， 卻被批評過於依賴經驗 。

古典學派主張等可能原則 ， 一遇到連續樣本空間就陷入 Bertrand 悖論 。

主觀學派才剛萌芽 ， de Finetti 說機率是信念 ， 卻拿不出嚴格演算 。

更麻煩的是 Hilbert 在 1900 年拋出第六問題 ： 物理公理化 ， 機率論能否像幾何一樣公理化 。

Borel 與 Lebesgue 已經備好測度論武器 ， Fréchet 有了抽象空間 ， 萬事俱備 ， 只欠一位偵探 。

1933 年 ， Kolmogorov 推開法庭大門 ， 手中只有薄薄一本德文小冊子 Grundbegriffe 。

他說 ， 別再爭機率的哲學本質 ， 先把遊戲規則寫清楚 ， 剩下的交給數學 。

## 偵查過程

偵探的第一個動作 ， 是把樣本空間抽象化 。

設  $\Omega$  為一切可能結果的集合 ， $\mathcal{F}$  為事件的 σ 代數 ， $P$  為其上的測度 。

於是機率空間被定義為三元組  $(\Omega,\mathcal{F},P)$  ， 這就是本案的第一具屍體 ， 直覺的屍體 。

三條公理簡潔得令人不安 ， 偵探在黑板上寫下 。

第一公理為非負性 ， 對任意事件  $A$  ， 有  $P(A) \ge 0$  。

第二公理為規範性 ， 必然事件的機率為一 ， 即  $P(\Omega) = 1$  。

第三公理為可數可加性 ， 若  $A_n$  互不相交 ， 則  $P(\cup_n A_n) = \sum_n P(A_n)$  。

僅此三條 ， 別無其他 ， 條件機率與獨立性皆為衍生概念 。

條件機率定義為  $P(A \mid B) = P(A \cap B) / P(B)$  ， 其中  $P(B) > 0$  。

獨立性定義為  $P(A \cap B) = P(A)P(B)$  ， 隨機變數的獨立性則由生成 σ 代數的獨立性刻畫 。

隨機變數在新體制下不再神秘 ， 它就是可測函數  $X : \Omega \to \mathbb{R}$  。

期望值即 Lebesgue 積分 ， 記為  $E[X] = \int_{\Omega} X dP$  。

偵探用下表展示新舊語言的對照筆錄 。

| 舊語言 | 新語言 | 數學寫法 |
|--------|--------|----------|
| 樣本點 | 樣本空間元素  $\omega$  |  $\omega \in \Omega$  |
| 事件 | 可測集合  $A$  |  $A \in \mathcal{F}$  |
| 機率 | 測度  $P$  |  $P(A)$  在  $[0,1]$  之間 |
| 隨機變數 | 可測函數  $X$  |  $X^{-1}(B) \in \mathcal{F}$  |
| 期望值 | 積分  $E$  |  $E[X] = \int X dP$  |
| 獨立 | σ 代數獨立 |  $P(A \cap B) = P(A)P(B)$  |
| 條件 | Radon–Nikodym 導數 |  $P(A \mid \mathcal{G}) = E[1_A \mid \mathcal{G}]$  |

關鍵轉折出現在無窮維 ： 如何保證無窮隨機序列的存在 。

Kolmogorov 提出相容性定理 ， 有限維分佈若相容 ， 則存在唯一的無窮乘積測度 。

$$ P_{(X_1,\dots,X_n)} \text{相容} \Rightarrow \exists P \text{於} \mathbb{R}^{\mathbb{N}} $$

這一定理直接為 Markov 鏈與 Wiener 過程提供了合法戶籍 。

偵探還埋下一個伏筆 ， 當時無人察覺 ， 後來震動全城 。

若測度  $Q$  對  $P$  絕對連續 ， 則存在密度函數 ， 即 Radon–Nikodym 導數  $dQ/dP$  。

$$ Q(A) = \int_A \frac{dQ}{dP} dP $$

其中  $dQ/dP$  為非負可測函數 ， 後來成為 Girsanov 定理與鞅定價的核心 。

有了地基 ， 大數法則與中央極限定理終於可以嚴格證明 。

| 定理 | 內容概要 | 所需工具 |
|------|----------|----------|
| 強大數法則 | 獨立同分佈且  $E[\|X_1\|] < \infty$  則均值幾乎必然收斂 | Borel–Cantelli 引理與截斷  $X_n 1_{\|X_n\|\le n}$  |
| 中央極限定理 | 標準化均值弱收斂至常態  $N(0,1)$  | 特徵函數  $\phi(t) = E[e^{itX}]$  |
| 零一律 | 尾事件機率非零即一 | Kolmogorov 零一律與尾 σ 代數  $\mathcal{T}$  |

Hilbert 第六問題至此得到部分回應 ， 機率論與幾何一樣有了公理 。

## 結案報告

兇手不是頻率 ， 也不是信念 ， 而是含糊不清的語言 。

Kolmogorov 用測度論收編了機率 ， 從此機率即測度 ， 期望即積分 ， 條件即投影 。

本案遺產極為深遠 ， 可列為四項 。

第一 ， LLN 與 CLT 有了嚴格舞台 ， Borel–Cantelli 與特徵函數得以全力施展 。

第二 ， 隨機過程被定義為機率空間上的函數族  $X_t(\omega)$  ， 為 1931 年方程與 1942 年積分鋪路 。

第三 ， Radon–Nikodym 導數埋下換測度革命的種子 ， 1960 年 Girsanov 定理與 1979 年鞅定價皆源於此 。

第四 ， 公理化終結了學派混戰 ， 頻率派與主觀派退居詮釋層 ， 數學層統一 。

當然 ， 公理也有盲點 ， 它不告訴你如何選取  $P$  ， 也不處理量子機率的非交換性 。

de Finetti 的主觀詮釋與後來的量子機率仍在法庭外抗議 ， 但那是另一樁案件 。

1933 年的法槌落下 ， 機率論從煉金術變成了化學 。

## 證據與工具

證物一號 ： 三公理全文 ， 以現代符號重寫 。

$$ P(A) \ge 0,\quad P(\Omega) = 1,\quad P(\cup_n A_n) = \sum_n P(A_n) $$

其中  $A_n$  為互不相交事件列 ， 求和可為無窮級數 。

證物二號 ： 期望的 Lebesgue 定義 ， 連結積分與機率 。

$$ E[X] = \int_{\Omega} X(\omega) P(d\omega) $$

其中  $X$  為可測函數 ， $P(d\omega)$  為機率微元 。

證物三號 ： 相容性定理的骨架 ， 無窮序列的存在保證 。

$$ \mu_{1,\dots,n} \text{相容} \Rightarrow \exists \mu \text{於無窮乘積空間} $$

其中  $\mu$  為唯一擴張測度 ， 相容指邊際一致 。

偵探工具 ： 單調類定理 ， Dynkin 系統 ， Borel–Cantelli 引理 ， 特徵函數唯一性 。

數值呼應可參考程式 `_code/1933-clt_demo.py` ， 標準化均值逼近常態即 CLT 的回聲 。

符號速查表如下 。

| 符號 | 意義 | 備註 |
|------|------|------|
|  $\Omega$  | 樣本空間 | 一切可能之集合 |
|  $\mathcal{F}$  | σ 代數 | 事件的全體 |
|  $P$  | 機率測度 | 總質量為一的測度 |
|  $E$  | 期望 | 對  $P$  的積分 |
|  $dQ/dP$  | 密度比 | 換測度的鑰匙 |

## 補充：程式實作

### 對應程式

本節對應程式為 [1933-clt_demo.py](_code/1933-clt_demo.py) ，以指數母體重複抽樣演示中央極限定理的弱收斂。

### 理論呼應

公理化後期望即積分 $E[X] = \int_{\Omega} X dP$ ，大數法則與中央極限定理始有嚴格舞台。
程式取指數分佈母體驗證標準化均值 $Z = \sqrt{n} (\bar{X} - 1)$ 弱收斂至 $N(0, 1)$ 。
偏度接近零且覆蓋率 $P(|Z| < 1.96) \approx 0.95$ ，正是以頻率回聲印證弱收斂的含義。
相容性定理保證此類無窮重複試驗存在唯一的乘積測度 $P$ ，使模擬具有合法戶籍。

### 執行方式

`python3 _code/1933-clt_demo.py`

### 實測輸出

本次實測輸出如下：`Z mean=-0.00204 std=0.99846 skew=0.07311` ，`P(|Z|<1.96)=0.95005` 貼近理論值 0.95 ，結尾印出 `VERIFY 1933 CLT: |skew|=0.0731<0.1 cover=0.9500 err=0.0000<0.01 PASS` 。

### 讀者實驗

將 $n$ 由 500 降為 30 後重跑，觀察偏度與覆蓋率如何偏離常態理論值。

完整程式如下：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1933 CLT 對應 wiki 說明
對應 wiki：1933 年 Kolmogorov 公理化與中央極限定理 (Lindeberg-Levy)。
Exp(1) 母體 mean=1 var=1，標準化樣本均值 Z = sqrt(n)*(Xbar-1) -> N(0,1)。
本程式 n=500、2 萬次重複，驗證偏度 |skew|<0.1 且 P(|Z|<1.96)≈0.95 誤差<0.01。
規範：只用 numpy，固定種子，不畫圖只印數字，結尾印 VERIFY 並用 assert 把關。
"""
import numpy as np

np.random.seed(0)

n = 500
M = 20000

# Exp(1) 抽樣：(M, n) 矩陣，約 1000 萬個樣本
X = np.random.exponential(scale=1.0, size=(M, n))
Xbar = np.mean(X, axis=1)
Z = np.sqrt(n) * (Xbar - 1.0)

zmean = float(np.mean(Z))
zstd = float(np.std(Z))
skew = float(np.mean(((Z - zmean) / zstd) ** 3))
cover = float(np.mean(np.abs(Z) < 1.96))

print(f"CLT Exp(1) n={n} M={M}")
print(f"Z mean={zmean:.5f} std={zstd:.5f} skew={skew:.5f}")
print(f"P(|Z|<1.96)={cover:.5f} (theory 0.95)")

assert abs(skew) < 0.1, f"|skew|={abs(skew)} >= 0.1"
assert abs(cover - 0.95) < 0.01, f"|cover-0.95|={abs(cover-0.95)} >= 0.01"
print(f"VERIFY 1933 CLT: |skew|={abs(skew):.4f}<0.1 cover={cover:.4f} err={abs(cover-0.95):.4f}<0.01 PASS")
```
