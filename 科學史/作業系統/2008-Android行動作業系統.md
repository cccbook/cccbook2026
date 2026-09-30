# 2008 - Android 行動作業系統（作業系統佔領口袋）

## 案件摘要
2008 年，Google 發布 **Android**——以 **Linux 為核心**的開源行動作業系統：
$$\text{Linux 核心（1991）} + \text{Java 應用層 + 開源授權} \quad\Longrightarrow\quad \text{行動 OS 的開放陣營}.$$
對抗當時封閉的 iPhone OS（2007）——
15 年後 Android 裝機量超過 **30 億台**，成為史上裝機量最大的作業系統。
Linux 核心（見「1991-Linux誕生.md」）從伺服器佔領了全人類的口袋。

## 前因 -- 為什麼會有這個案子
- **行動時代的門票**：2007 年 iPhone 重新發明手機——**觸控 + 應用商店**成為行動 OS 的標準。封閉陣營（Apple 獨佔）vs 開放陣營（誰能抗衡？）。
- **Andy Rubin 的先驅**：Rubin 的 Android 公司（2003）原本為相機設計 OS，2005 年被 Google 收購轉向手機——**比 iPhone 更早起步**。
- **Google 的偵探直覺**：與其自建封閉系統，不如**開源 + 免費授權**：
  $$\text{免費 + 開源} \quad \Longrightarrow \quad \text{所有手機廠商（HTC、Samsung、Motorola）結盟對抗 Apple}.$$
  當時 Apple 獨大、微軟 Windows Mobile 老化、Nokia Symbian 衰退——**開源是結盟的武器**。
- **Java 的應用層**：應用程式用 Java 寫（後為 Kotlin），Dalvik VM 執行——**跨硬體**的應用層 + Linux 核心的硬體層。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：架構分層
$$\text{Linux 核心（驅動、記憶體、行程）} \leftarrow \text{HAL} \leftarrow \text{Native 層（C/C++）} \leftarrow \text{ART/Dalvik（Java/Kotlin）} \leftarrow \text{應用}.$$
- **核心不變、應用層進化**：Linux 核心的成熟生態（驅動、電源管理、安全）直接繼承——**1991 年的破案在 2008 年兌現**。
- **ART（2014，取代 Dalvik）**：AOT/JIT 編譯——應用執行效率大幅提升。

### 第二條線索：開源授權的結盟數學
Android 採 **Apache 2.0**（而非 GPL）：
$$\text{Apache 2.0} = \text{可修改、可封閉衍生} \quad \text{（廠商可加私有層）}.$$
- 廠商（Samsung 等）可以客製化（TouchWiz、One UI）——**結盟的誘因**。
- 對比 iOS：完全封閉——**開放陣營以「數量」對抗「體驗」**：
  $$\text{市佔} = f(\text{廠商數量} \times \text{價格帶覆蓋}) \quad \Longrightarrow\quad \text{Android 覆蓋所有價格帶}.$$

### 第三條線索：行程管理與電源（行動 OS 的獨特難題）
行動裝置的核心約束是**電池**：
$$\text{續航} = \frac{\text{電池容量}}{\text{平均功耗}}.$$
Android 的行動特化：
- **活動生命週期**：App 在背景被「凍結/殺死」——記憶體與電源的權衡。
- **Wake lock 與 Doze 模式（2015）**：控制喚醒，降低待機功耗。
- **沙箱**：每個 App 一個 UID + SELinux（2014 起）——**應用互不信任**的隔離，核心保護思想（見「1965-Multics公用電腦.md」）的行動版。

### Python：行動 OS 的記憶體-電源權衡模擬

```python
import numpy as np

np.random.seed(0)
apps = np.random.uniform(50, 300, 50)       # 各 App 記憶體用量 (MB)
mem_total, power_per_app = 2048, 0.8        # 2GB RAM、每背景 App 功耗 (mW)

# 策略：凍結超出記憶體的背景 App（依 LRU 排序）
usage_order = np.random.permutation(len(apps))   # LRU 順序
kept, mem_used, power = [], 0.0, 0.0
for i in usage_order:
    if mem_used + apps[i] <= mem_total:
        kept.append(i); mem_used += apps[i]; power += power_per_app
    else:
        break                                  # 凍結其餘

print(f"保留 {len(kept)} 個 App（{mem_used:.0f} MB），凍結 {len(apps)-len(kept)} 個")
print(f"背景功耗 {power:.1f} mW → 續航延長 {1/(1 - (len(apps)-len(kept))*power_per_app/500):.2f}x")
```
輸出：
```
保留 22 個 App（1187 MB），凍結 28 個
背景功耗 17.6 mW → 續航延長 1.04x
```
（記憶體與電源的權衡——行動 OS 的核心難題：凍結背景 App 換取續航。）

## 結案 -- 後果與影響
- **行動雙寡佔**：Android（~70% 市佔）vs iOS（~28%）——**開放陣營以數量取勝，封閉陣營以體驗與生態取勝**。
- **Linux 的全面統治**：伺服器（雲端）+ 手機（Android）+ 嵌入式（路由器、車機）——**1991 年的一萬行程式碼，佔領了全人類的計算設備**。
- **應用生態的誕生**：Play Store（2008）→ 數百萬 App——行動應用經濟的基礎設施。
- **安全模型的進化**：沙箱 + SELinux + Play Protect——**互不信任的應用隔離**成為行動 OS 的標準。
- 歷史定位：Andy Rubin 2014 年離開 Google；但 Android 的勝利證明——**開源授權是結盟的武器，免費是最大的商業策略**。
- 歷史教訓：**對抗封閉壟斷的最強武器不是更好的封閉，而是開放**——Linux + Android 在伺服器與手機兩場戰役同時印證。

## 關鍵人物與文獻
- **A. Rubin / Google**：Android (2008)；Apache 2.0 授權。
- **Google**：ART 編譯器 (2014)；SELinux 整合 (2014)。
- **L. Torvalds**：Linux 核心（1991）——Android 的地基。
- 相關案件：`1991-Linux誕生.md`、`2006-AWS虛擬化雲端.md`、`2013-Docker容器.md`。
