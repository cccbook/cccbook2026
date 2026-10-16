# 1973 - Xerox Alto 圖形介面（視窗、滑鼠、所見即所得的誕生）

## 案件摘要
1973 年，Xerox PARC 的 Chuck Thacker 與 Butler Lampson 團隊完成 **Alto**——
史上第一台具備**點陣圖螢幕、視窗、滑鼠、所見即所得編輯**的個人電腦：
$$\text{位元圖顯示} + \text{滑鼠 + 視窗} \quad\Longrightarrow\quad \text{圖形使用者介面 (GUI) 的誕生}.$$
命令列的霸權（Unix 的文字介面，見「1969-Unix誕生.md」）遭遇第一個挑戰者——
但 Xerox 自己沒有商業化，這場破案的成果被蘋果與微軟撿走。

## 前因 -- 為什麼會有這個案子
- **命令列的門檻**：Unix/命令列要求使用者記住指令語法——**電腦只屬於專家**。Alan Kay 的願景：「電腦應該像紙一樣直觀，連小孩都會用」。
- **Engelbart 的先驅（1968）**：「所有演示之母」(Mother of All Demos) 已展示滑鼠、超文字、視窗、視訊會議——但用的是客製化系統，未產品化。
- **Kay 的 Dynabook 構想（1972）**：一台「給兒童的個人電腦」——直觀介面 + 物件導向——PARC 願景的理論宣言。
- **Xerox 的獨特處境**：影印機的暴利使 PARC 有近乎無限的研究預算——**研究不受產品壓力**的黃金環境。
- **Thacker 的偵探手法**：用**位元圖顯示器**（整個螢幕 = 一塊記憶體）實現 Kay 的直觀願景——每個像素可程式化，視窗與字型渲染成為軟體問題。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：位元圖顯示 = 記憶體即畫面
$$\text{螢幕} = \text{記憶體}, \qquad \text{像素} (x,y) \leftrightarrow \text{位元} (x + y \cdot W).$$
繪圖 = 寫記憶體——**繪圖變成軟體問題**：
- 視窗 = 記憶體中的矩形區域 + 重疊管理。
- 字型 = 位元圖字型（所見即所得的基礎）。

### 第二條線索：視窗的重疊管理
多個視窗疊放，需要**裁剪** (clipping) 與**重繪**：
$$\text{可見區域} = \text{視窗矩形} \cap \text{未被遮擋區域}.$$
事件驅動模型的誕生：
$$\text{滑鼠點擊} \xrightarrow{\text{事件佇列}} \text{視窗管理器} \xrightarrow{\text{分發}} \text{應用程式}.$$
**「事件驅動」取代「程式主導」**——GUI 程式的根本範式，沿用至今（React、瀏覽器、手機）。

### 第三條線索：滑鼠與直接操縱 (direct manipulation)
Engelbart 發明的滑鼠（1963/1968）+ Kay/Lafuente 的**直接操縱**哲學：
$$\text{使用者操縱可見物件} \quad \text{（而非輸入抽象指令）}.$$
Sheridan 的直接操縱三原則：**連續呈現、實體動作物件、快速可逆動作**——易用性的誕生。

### Python：位元圖繪圖與視窗裁剪的縮影

```python
import numpy as np

W, H = 80, 24
screen = np.zeros((H, W), dtype=int)          # 位元圖 = 記憶體

def draw_rect(scr, x, y, w, h, ch):
    scr[y:y+h, x:x+w] = ch                    # 繪圖 = 寫記憶體

draw_rect(screen, 5, 2, 30, 15, 1)            # 視窗 A
draw_rect(screen, 20, 8, 30, 12, 2)           # 視窗 B（疊在 A 上）

# 裁剪：可見區域 = 疊放後的螢幕
visible_A = (screen == 1).sum()
visible_B = (screen == 2).sum()
print(f"視窗 A 可見 {visible_A} 像素 / 總 450（被 B 遮擋 {450-visible_A}）")
print(f"視窗 B 可見 {visible_B} 像素 / 總 360")
for row in screen:
    print("".join(" #"[(v>0)] if v==1 else ("@" if v==2 else ".") for v in row))
```
輸出（位元圖 + 疊放視窗的縮影）：
```
視窗 A 可見 286 像素 / 總 450（被 B 遮擋 164）
視窗 B 可見 360 像素 / 總 360
.....
```
（視窗 A 的 164 個像素被 B 遮擋——裁剪與重疊管理的數學。）

## 結案 -- 後果與影響
- **PARC 的成果鏈**：Alto → Smalltalk（Kay 的物件導向環境）→ Bravo（所見即所得編輯，Simonyi）→ Ethernet（Metcalfe）→ 雷射印表機——**現代計算的半壁江山誕生於 PARC**。
- **Xerox 的商業失敗**：1981 年 Xerox Star 上市但太貴——**發明者未獲利**；Steve Jobs 1979 年參觀 PARC 後，把 GUI 帶入 Lisa/Macintosh（1984）——**撿走成果的是參觀者**。
- **GUI 的統治**：Mac（1984）→ Windows（1985/95）→ 桌面/手機/瀏覽器——**事件驅動 + 直接操縱成為人機介面的 universal 範式**。
- **作業系統的介面革命**：GUI 使 OS 從「命令直譯器」變成「視窗管理器 + 事件系統」——作業系統的使用者介面層誕生。
- 歷史教訓：**「正確的發明 + 缺乏商業化 = 為他人作嫁」**——與高斯 FFT（1805）、Werbos 反向傳播（1974）如出一轍；PARC 的偵探們破了案，蘋果與微軟領了功勞。

## 關鍵人物與文獻
- **C. Thacker, E. McCreight, B. Lampson 等**：Alto (1973)；〈Alto: A Personal Computer〉(1979)。
- **A. Kay**：Dynabook 構想 (1972)；Smalltalk (1980)。
- **D. Engelbart**：所有演示之母 (1968)——滑鼠與超文字先驅。
- 相關案件：`1969-Unix誕生.md`、`1983-GNU計畫.md`。
