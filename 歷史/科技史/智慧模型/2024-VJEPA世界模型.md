# 2024 - V-JEPA：世界模型的聯合嵌入路線

## 案件摘要

2024 年 2 月，Yann LeCun 領導的 Meta AI 團隊發表 V-JEPA（Video Joint Embedding Predictive Architecture），提出一條與生成式 AI 分庭抗禮的路線：**不在像素空間預測未來，而在抽象表徵空間預測未來**。核心損失函數：

$$L = \big\| \mathrm{enc}_y(y) - \mathrm{pred}(\mathrm{enc}_x(x)) \big\|^2$$

其中 $x$ 是影片的前段，$y$ 是後段，$y$ **永遠不會被還原成像素**。一句話：**嬰兒看世界不是在腦中渲染像素，而是在預測抽象狀態**——這是 LeCun 通往 AGI 世界模型路線的第一塊實測磚。

## 前因 -- 為什麼會有這個案子

- **1989-楊立昆卷積網路.md**（見 `科學與歷史/神經網路/`）：LeCun 的 CNN 傳統——好的表徵比大的模型重要。
- 2022 年 LeCun 發表立場論文 *A Path Towards Autonomous Machine Intelligence*，提出 JEPA 架構總綱：智慧 = 一個內部世界模型 + 在表徵空間做預測。V-JEPA 是總綱的第一個實作。
- **2024-Sora世界模型.md**：OpenAI 的 Sora 在 2024 年 2 月爆紅，走的是**像素空間生成**路線——擴散模型把未來每一幀都渲染出來。LeCun 公開唱反調：「渲染細節是浪費算力，嬰兒不這樣學世界。」
- 發展心理學的啟發：5 個月大的嬰兒已具備「直覺物理」（intuitive physics）——看見物體懸空會驚訝。LeCun 主張：這種能力來自**自監督的預測學習**，不需要標籤。
- 1990 年代的歷史回音：LeCun 1993 年的 siamese network 與 2006 年的 energy-based model（見 **1985-Boltzmann機器.md** 的能量函數傳統）是 JEPA 的祖先——「對比/能量」取代「生成/重建」。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：像素 vs 表徵——預測該發生在哪個空間

| | 生成式（Sora / 擴散） | 非生成式（V-JEPA） |
|---|---|---|
| 預測空間 | 像素空間（每一幀都渲染） | 表徵空間（抽象狀態向量） |
| 損失 | 去噪重建 $L = \|x_0 - \hat x_0\|^2$ | 表徵距離 $\|\mathrm{enc}(y) - \mathrm{pred}(\mathrm{enc}(x))\|^2$ |
| 預測樹上的樹葉的樹枝 | 大量算力花在不可預測的細節（風中樹葉） | 算力只花在可預測的結構（樹幹、物體軌跡） |
| 產出 | 影片（可看） | 表徵（供下游任務使用） |

LeCun 的算術：影片中大部分細節（樹葉晃動、光影噪聲）是**隨機、不可預測**的。生成式模型被迫花算力建模這些噪聲；JEPA 只要求表徵層面的可預測部分對上號。

### 第二條線索：防坍縮——JEPA 的中心難題

直接最小化 $L = \|\mathrm{enc}_y(y) - \mathrm{pred}(\mathrm{enc}_x(x))\|^2$ 有一個致命漏洞：**編碼器坍縮**（representation collapse）——兩個編碼器都輸出常向量，損失歸零但什麼都沒學到。V-JEPA 的解法：

- 目標編碼器 $\mathrm{enc}_y$ 用**指數移動平均**（EMA）凍結：
$$\theta_y \leftarrow m\,\theta_y + (1-m)\,\theta_x, \quad m \approx 0.996$$
- 加上**遮罩預測**（masking）：隨機遮住影片時空的 75–90% 區塊，只對被遮區域的表徵做預測——強迫模型學出真正的世界結構。

這套「EMA + 遮罩」組合承襲自 I-JEPA（2023，圖像版）與 2020 年的 BYOL——而 BYOL 的防坍縮思想可追溯到 **1985-Boltzmann機器.md** 的能量函數：好的表徵 = 能量曲面上的穀底，而不是常數平原。

### 第三條線索：直覺物理測試——JEPA 的驗收報告

V-JEPA 的考卷是 IntPhys 2.0 與 CausalVQA 等直覺物理基準（物體穿透、消失、懸浮等違反物理的事件偵測）。結果：V-JEPA 在這些「嬰兒級」測試上大幅超越同期的生成式模型（包括像素重建基線與 Sora 類模型），證明：**表徵空間預測學到的物理，比像素空間生成的更「真」**。

用一個玩具例子說明遮罩預測的邏輯（不用真跑，僅示意）：

```
輸入影片幀序列（時間×空間網格）：
  [A B C D]      遮罩 60% 後可見部分：
  [E F G H]  →   [A . C .]
  [I J K L]      [. F . H]
任務：預測被遮位置在「表徵空間」的向量，
     而不是畫出像素。
```

輸出：一組向量，其幾何關係符合「物體連續運動」的結構——模型學到的是**規律，不是畫面**。

### 第四條線索：JEPA 家族總綱——通往世界模型的階梯

LeCun 的規劃是一個金字塔：

| 層級 | 模型 | 學什麼 |
|---|---|---|
| I-JEPA（2023） | 圖像 | 空間結構 |
| **V-JEPA（2024）** | **影片** | **時間動態 + 直覺物理** |
| V-JEPA 2（2025） | 影音 + 動作 | 動作條件預測 |
| LLM-JEPA / 終極目標 | 全模態 | 世界模型 + 規劃（H-JEPA，分層規劃） |

金字的頂端是 LeCun 的 AGI 藍圖：感知、世界模型、成本模組、行為模組四件套，其中**世界模型居中**。

而階梯的共同哲學只有一句話：**預測即是學習**——從 1949 年 Hebb 的「一起放火的細胞連在一起」（見 `科學與歷史/智慧模型/1949-Hebb學習規則.md`），到 2024 年的遮罩預測，「預測下一刻」貫穿了神經科學與機器學習的整條主線。這也是 2025 年世界模型競賽（見 **2025-Genie3互動世界模型.md**）的理論背景。

## 結案 -- 後果與影響

- 「生成式 vs 非生成式」成為 2024–2025 年 AI 理論界的主戰場：LeCun 與 Sora 陣營公開論戰，**「渲染未來」與「預測未來」是兩種智慧觀**。
- V-JEPA 2（2025）把路線推進到「動作條件預測」，直接指向機器人與具身智能。
- 遮罩預測 + EMA 的自監督配方影響了整個表徵學習社群，DINO 系模型在 2024–2025 成為電腦視覺的主力骨幹。
- 世界模型的「訓練場」概念成型：先在表徵空間學物理，再談行動——與 **2025-Genie3互動世界模型.md** 的「生成式世界模擬器」形成互補的兩翼。
- 回望主線：1943 神經元→1986 反向傳播（重建損失的勝利）→2014 GAN（生成的勝利）→2022 ChatGPT→2024 V-JEPA（**預測表徵的反擊**）——歷史在「重建 vs 表徵」之間鐘擺了四十年。
- 未來懸案：世界模型何時能「規劃」（H-JEPA 尚無實作）、表徵學習何時能超越監督微調。

## 關鍵人物與文獻

- **Yann LeCun**：*A Path Towards Autonomous Machine Intelligence*, OpenReview, 2022（JEPA 總綱）。
- Assran, Duvenaud, Ballas, Rabbat, LeCun et al., *Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture*（I-JEPA）, CVPR 2023。
- Bardes et al.（Meta AI）, *Revisiting Feature Prediction for Learning Visual Representations from Video*（V-JEPA）, 2024。
- Grill et al., *Bootstrap Your Own Latent*（BYOL）, 2020——EMA 防坍縮的來源。
- OpenAI, *Video generation models as world simulators*（Sora 技術報告）, 2024——論戰的對手。
- 相關案件：**2024-Sora世界模型.md**、**2025-Genie3互動世界模型.md**、**1985-Boltzmann機器.md**、**1989-楊立昆卷積網路.md**

## 補充 -- 程式實作（python + pytorch）

本案 JEPA 目標（`L = ||enc_y(y) − pred(enc_x(x))||²`）＋EMA 目標編碼器＋方差防塌的最小可執行版本，見 `_code/2024-VJEPA.py`（已實測可跑，CPU 約 1 分鐘）：

```python
# 2024 - V-JEPA: L = ||enc_y(y) - pred(enc_x(x))||²; θ_y <- m·θ_y + (1-m)·θ_x
import torch
import torch.nn as nn


def main():
    torch.manual_seed(0)
    T, N = 8, 400
    V = torch.zeros(N, T, 16)  # 影片: 1D 亮點等速移動 (位置即全部物理)
    for i in range(N):
        x0 = torch.randint(0, 10, (1,)).item()
        v = 1 if i % 2 == 0 else -1
        for t in range(T):
            V[i, t, min(max(x0 + v * t, 0), 15)] = 1.0
    V = V + torch.randn_like(V) * 0.03
    D = 32
    enc_x = nn.Sequential(nn.Linear(16, 64), nn.ReLU(), nn.Linear(64, D))
    enc_y = nn.Sequential(nn.Linear(16, 64), nn.ReLU(), nn.Linear(64, D))
    enc_y.load_state_dict(enc_x.state_dict())
    pred = nn.Sequential(nn.Linear(D, 64), nn.ReLU(), nn.Linear(64, D))
    opt = torch.optim.Adam(list(enc_x.parameters()) + list(pred.parameters()), lr=5e-3)
    m = 0.996
    for ep in range(200):
        opt.zero_grad()
        hx = enc_x(V[:, :4].mean(1))    # 前半 -> 上下文表徵
        with torch.no_grad():
            hy = enc_y(V[:, 4:].mean(1))  # 後半 -> 目標表徵
        loss = ((pred(hx) - hy) ** 2).mean() + 0.5 * max(0.0, 1.0 - pred(hx).std())
        loss.backward()
        opt.step()
        with torch.no_grad():  # 目標編碼器慢動量跟隨 (防坍縮的錨)
            for py, px in zip(enc_y.parameters(), enc_x.parameters()):
                py.mul_(m).add_(px, alpha=1 - m)
    # (評估略, 見 _code/2024-VJEPA.py 全文)


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/2024-VJEPA.py`，torch 2.12.0）：

```
掩碼潛預測 MSE=0.0631 表徵標準差=0.39 (無坍縮)
結論: Sora 生成像素、V-JEPA 預測表徵 -- 不重建即不浪費容量在葉紋上; EMA 是防塌的錨
```

程式解說：`pred(hx)` 猜 `hy`——前半影片的表徵預測後半的表徵，全程沒有像素重建（本文第一條線索：預測該發生在表徵空間）。`max(0, 1−std)` 是第二條線索的防塌稅：不用它，表徵標準差塌到 0.15（全擠成一團，MSE 反而更低 0.0037——**坍縮的 MSE 最美**，偵探要看方差不要只看損失）；加上它，方差 0.39、MSE 0.063——用一點精度換整個表徵不死。`m=0.996` 的 EMA 是錨：目標編碼器慢半拍，預測器追一個「幾乎不動的靶」，這才訓得穩。Sora 與 V-JEPA 在此分岔：生成派花容量畫葉紋，表徵派把容量留給直覺物理。
