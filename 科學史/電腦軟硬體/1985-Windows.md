# 1985-Windows

## 案件摘要
1985 年 11 月，Windows 1.0 問世——微軟面對 Mac GUI 威脅的防禦性產品。前十年它飽受嘲笑：平鋪視窗、依賴 DOS、又慢又醜。但 1990 年 Windows 3.0 爆發、1995 年 Windows 95 憑 Start 選單登頂，微軟完成從追隨者到 API 壟斷者的蛻變，最終在 1998 年被美國司法部以反壟斷起訴。

## 前因 -- 為什麼會有這個案子
- 1981 年 IBM PC 確立硬體標準，但 DOS 是命令列——Mac（1984）用 GUI 打出易用性差距，商用市場開始動搖。
- 微軟早已承諾為 IBM 開發 GUI（合約追溯到 1985 年前，甚至影響 IBM 的 TopView），但內部真正目的是**自己掌控 GUI 標準**。
- Wintel 聯盟中，硬體已歸 Intel；軟體標準若被 Mac 拿走，微軟將失去一切。
- 因此 Windows 的本質是防禦：不必最好，只需「存在於每一台 PC 上」。

## 線索與推理 -- 數學式、程式、理論
### 線索一：Gates 的防禦策略
Gates 的策略可用平台理論寫成不等式。設平台的價值為：

$$V_{\text{platform}} = V \cdot N^2 \quad (\text{Metcalfe 定律：價值與節點數平方成正比})$$

- Mac 路線：$N$ 小（僅蘋果硬體），$V$ 高（整合體驗佳）。
- Windows 路線：$N$ 巨大（所有 PC 相容機），$V$ 低（體驗粗糙）。

當 clone 產業讓 $N_{\text{Win}} \gg N_{\text{Mac}}$，即使 $V_{\text{Win}} < V_{\text{Mac}}$，仍可使 $V_{\text{platform,Win}} \gg V_{\text{platform,Mac}}$。**以量取勝、以生態鎖定**——這是 Gates 一貫的棋譜。

### 線索二：Windows 1.0 的侷限
1985 年的 Windows 1.0 三大硬傷：
1. **平鋪視窗（tiling windows）**：視窗不可重疊（據說是怕 IBM 的 TopView 抱怨侵權），與 Mac 的重疊視窗相比體驗倒退。
2. **需 DOS**：Windows 只是 DOS 上的殼（shell），不是作業系統。開機流程為：

$$\text{BIOS} \rightarrow \text{DOS（command.com）} \rightarrow \text{win.com} \rightarrow \text{Windows}$$

3. **又慢又吃記憶體**：640KB 的 DOS 記憶體限制下，跑 GUI 捉襟見肘。

Windows 1.0 內附的簡單工具（Notepad、Paint、Clock、Reversi 遊戲）已預告未來的視窗世界，但當年無人看好。

### 線索三：Windows 3.0（1990）與 Windows 95 的 Start 選單
- **Windows 3.0（1990）**：突破 1MB 記憶體限制（保護模式、虛擬記憶體），配合 386 CPU，首次真正流暢。1992 年的 3.1 搭配文書處理與試算表，PC 端殺手級應用到位——VisiCalc 劇本重演，只是舞台換成 Windows。
- **Windows 95**：不再需要先開 DOS（DOS 7.0 整合進來），並以 **Start 選單**解決 GUI 的導航難題：所有程式一鍵可達。它的抽象意義是「單一根入口」：

$$\text{導航成本} = O(\text{搜尋深度}) \quad \Rightarrow \quad \text{Start 選單把搜尋深度壓縮為 } O(1)$$

- 「Start me up」（滾石樂團）廣告曲、午夜排隊搶購——作業系統第一次成為大眾文化事件。

### 線索四：API 壟斷與反壟斷訴訟（1998）
Win32 API 成為事實標準後，微軟的壟斷武器是**應用程式進入障礙（applications barrier to entry）**：

$$\text{新 OS 的存活條件} = \frac{\text{其上可用應用數}}{\text{Windows 應用數}} \to 1 \text{ 才可能存活}$$

開發者只為市占最大的平台寫程式 → 新平台沒有應用 → 使用者不換 → 開發者更不寫。這個正回饋迴圈鎖死了競爭。
- 1995 年 Netscape 瀏覽器威脅此迴圈（瀏覽器可承載跨平台應用），微軟以「綑綁 IE + 打壓 OEM」反擊。
- 1998 年美國司法部與 20 州提出反壟斷訴訟（*United States v. Microsoft*）；2000 年一審判決應分拆，2001 年和解收場。
- 1990 年代 Apple v. Microsoft 的 GUI 訴訟（1988–1994）敗訴，與此案互為鏡像：**觀念無法專利，但 API 生態可以壟斷**。

### 線索五：Python 呼叫 OS API 概念展示
Windows 的本質是「以 API 定義平台」。今天任何作業系統的應用程式都是透過 API 與核心對話，Python 展示這個概念：

```python
import os
import sys

# 1. 系統呼叫：OS API 是應用程式與核心的合約
print("目前工作目錄：", os.getcwd())
print("環境變數 PATH：", os.environ.get("PATH", "")[:60], "...")

# 2. 建立行程（Windows 的 CreateProcess / POSIX 的 fork 的概念）
pid = os.fork() if sys.platform != "win32" else None

# 3. 檔案 API：統一介面掩蓋底層差異
with open("demo.txt", "w") as f:
    f.write("Hello, API!")   # write() 呼叫背後是 OS 系統呼叫

print("檔案存在？", os.path.exists("demo.txt"))
```

就像 1985 年的 Win32 API 把 DOS 的混亂包裝成整齊的函式呼叫，今天的 `os` 模組把 POSIX/Win32 差異包裝成 Python 函式——**平台壟斷的技術本質，就是誰定義了這層 API**。

## 結案 -- 後果與影響
- Windows 3.0/95 讓微軟達到巔峰：1990 年代末市占率超過 90%，Gates 成為世界首富。
- Wintel 雙寡頭確立：Intel 管 CPU 迭代節奏、微軟管軟體標準，PC 產業的利潤被兩家抽走。
- 反壟斷訴訟雖以和解收場，但確立「壟斷者不得利用市場地位扼殺創新」的判例精神，影響後世對 Google、Apple 的監管。
- API 鎖定理論成為平台經濟學的標準模型；IE 綑綁案的教訓在 2020 年代的 App Store 爭議中重演。
- 長期來看，Web 與雲端（瀏覽器作為新平台）最終部分瓦解了 Windows 的 API 壟斷——正如當年 Netscape 所預言。

## 關鍵人物與文獻
- **Bill Gates**：防禦策略與 API 壟斷的總設計師。
- **Steve Ballmer**：「Developers! Developers! Developers!」的生態經營者。
- **David Cutler**：Windows NT（1993）架構師，把 VMS 經驗帶進 Windows。
- **Thomas Penfield Jackson**：反壟斷案一審法官。
- 文獻：*United States v. Microsoft Corp.* 判決書 (1998–2001)；Allison, *The Microsoft Way* (1996)；*U.S. v. Microsoft* 相關報導與 Cusumano & Selby, *Microsoft Secrets* (1995)。
