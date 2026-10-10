# 1820-Oersted 電流磁效應

## 案件摘要
1820 年 4 月，丹麥物理學家厄斯特（Hans Christian Ørsted）在一次課堂示範中，發現通電導線能使附近的指南針偏轉。這是電與磁之間存在關聯的第一個實驗證據，開啟了電磁學統一的百年工程。

## 前因 -- 為什麼會有這個案子
- **百年謎團**：自 Gilbert（1600）以來，電（琥珀摩擦）與磁（磁石）被視為兩種完全不同的現象。Coulomb（1785）更以精確實驗顯示電力與磁力都服從平方反比律，但兩者互不相關——他甚至做過實驗「證明」電荷不影響磁針。
- **哲學背景**：Oersted 深受德國自然哲學（Naturphilosophie，Kant、Schelling）影響，相信自然界各種力量具有深層的統一性，電與磁必然有某種轉換通道。
- **線索暗示**：雷擊使鐵器磁化、閃電使指南針失靈等零星報告，長期被視為軼聞而非證據。
- 當時已知電流通過細導線會發熱、發光，Oersted 便想：通電導線會不會也有某種「放射」影響磁針？

## 線索與推理 -- 數學式、程式、理論

### 實驗細節（1820 年 4 月）
- Oersted 將一條鉑導線南北向放置於玻璃罩上的小磁針**上方**——首次嘗試時導線偏離磁針過遠，效果不明顯。
- 當他把導線移到磁針**正下方**並接通電池時，磁針明顯偏轉，指向東西方向附近。
- **決定性觀察**：將電流反向，磁針即反向偏轉；把導線移到磁針上方，偏轉方向又再次反轉。
- 這排除了「熱」或任何沿導線方向傳播的作用：效果必是**繞著導線的橫向作用**。7 月 21 日他以拉丁文短文《關於電流衝擊對磁針效應的實驗》（*Experimenta circa effectum conflictus electrici in acum magneticam*）寄發歐洲各科學機構。

### 理論：圓形磁場
磁針的偏轉顯示磁場 $\mathbf{B}$ 環繞電流呈**同心圓**分布，方向由右手定則給出（拇指沿電流 $I$，四指即 $\mathbf{B}$ 方向）。距長直導線 $r$ 處的磁場大小為：

$$
\mathbf{B}(r) = \frac{\mu_0 I}{2\pi r}\,\hat{\phi}, \qquad \mu_0 = 4\pi\times 10^{-7}\ \mathrm{T\cdot m/A}
$$

這是**超距作用框架無法自然描述**的現象：電流沿導線方向作用，磁針卻被推向垂直方向——作用力不沿兩體連線，破壞了牛頓式力學的「中央力」假設。這正是「電與磁統一的第一道門」。

### Python：畫出載流導線的圓形磁場線

```python
import numpy as np
import matplotlib.pyplot as plt

# 長直導線沿 z 軸，電流 I 流出紙面（指向讀者）
mu0 = 4*np.pi*1e-7
I   = 1.0

fig, ax = plt.subplots(figsize=(6, 6))
# 磁場線是以原點為圓心的同心圓，方向為 phi-hat（逆時針，右手定則）
for r in [0.3, 0.6, 0.5*np.sqrt(2), 1.0, 1.25, 0.75*np.sqrt(2)]:
    t = np.linspace(0, 2*np.pi, 200)
    ax.plot(r*np.cos(t), r*np.sin(t), 'b-', lw=1)
# 標示磁場方向箭頭
t = np.linspace(0.2, 2.0, 6)
for r in [0.3, 0.6, 1.0]:
    ax.quiver(r*np.cos(t), r*np.sin(t), -np.sin(t), np.cos(t),
              color='red', scale=12, width=0.004)
ax.plot(0, 0, 'ko', ms=10)                 # 導線截面
ax.text(0.03, 0.03, 'I ⊙', fontsize=14)
ax.set_aspect('equal'); ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
ax.set_title('Oersted (1820): B-field circles a current-carrying wire\n'
             r'$\vec{B} = \frac{\mu_0 I}{2\pi r}\hat{\phi}$')
plt.savefig('oersted_field.png', dpi=120); plt.show()
```

### 推理驗證：為何偏轉方向會反轉？
磁針指向 $\mathbf{B}$ 方向；電流反向（$I \to -I$）則 $\mathbf{B} \to -\mathbf{B}$，故磁針偏轉 $180^\circ$ 反向。導線由下方移到上方，相對磁針的 $\hat{\phi}$ 方向也反轉——兩個觀察都與「圓形磁場」模型一致，與「導線放射熱流」模型矛盾。

## 結案 -- 後果與影響
- **3 個月的跟進風暴**：法國科學院收到短文後，Arago 於 1820 年 9 月 4 日在科學院公開重演實驗；Ampère 在數週內建立電動力學（見下一篇）；Arago 與 Davy 各自發現電流可使鐵屑磁化，製成**電磁鐵**。
- **科學史意義**：第一次有人以實驗證明電與磁相關，統一工程自此啟動——Ampère（1820）→ Faraday 感應（1831）→ Maxwell 方程組（1865）→ Hertz 電磁波（1887）。
- Oersted 獲英國皇家學會 Copley 獎章（1820）；「磁場強度」單位 Oersted（Oe）以他命名。
- 一堂臨時起意的示範實驗，改寫了物理學的地圖。

## 關鍵人物與文獻
- **Hans Christian Ørsted**（1777–1851），哥本哈根大學教授。
- Ørsted, H. C. (1820). *Experimenta circa effectum conflictus electrici in acum magneticam*. Copenhagen.
- 參照：Coulomb, C. (1785) 扭秤實驗；Ampère, A.-M. (1820) 電動力學；Gilbert, W. (1600) *De Magnete*。
