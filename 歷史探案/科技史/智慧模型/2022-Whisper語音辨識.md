# 2022 - Whisper 語音辨識

## 案件摘要

2022 年 9 月，OpenAI 發表 **Whisper**：一個以 **68 萬小時**弱監督語音資料訓練的多語言、多任務語音辨識系統。核心主張：**不需要人工標註，只要規模夠大、資料夠雜，Transformer 就能從網路上「髒」的語音資料中學出接近人類水平的辨識能力**。

$$\text{多任務序列} = [\text{語言偵測},\ \text{辨識},\ \text{翻譯},\ \text{時間戳}],\quad D \approx 680{,}000\ \text{小時}$$

Whisper 開源權重，零樣本（zero-shot）即在各基準上逼近甚至超越專門微調的 SOTA 模型——這是語音辨識的「GPT-3 時刻」，也是弱監督規模化在聲學世界的勝訴判決。

## 前因 -- 為什麼會有這個案子

- 語音辨識（ASR）長期被端到端神經網路統治：2015 年的 Listen-Attend-Spell、2016 年的 RNN-Transducer，但都依賴**數百至數千小時的乾淨人工標註資料**（LibriSpeech 只有 960 小時）。
- 2016 年 WaveNet（見「2016-WaveNet語音合成.md」）證明聲學訊號可以被自迴歸神經網路完整建模；但那是**合成**方向，辨識方向仍卡在標註資料的天花板。
- 2017 年 Transformer（見「科學與歷史/神經網路/」對應檔案）取代 RNN，但 ASR 界的共識是：架構改進的邊際效益遠小於資料量。
- 2020 年 GPT-3（見「2020-GPT-3規模湧現.md」）與 WebText 的教訓：**網路資料 + 大規模弱監督**可以擊敗精工細作的監督學習。OpenAI 內部追問：這條路在語音上走得通嗎？
- 2011 年 Siri（見「2011-Siri語音助理.md」）開啟了語音助理時代，但辨識錯誤率仍是體驗瓶頸；OpenAI 看到的動機是：**若有免費且強大的辨識 API 等價物，語音互動可以成為通用介面**。
- 關鍵洞見（Alec Radford、Jong Wook Kim 等人）：網路上大量 podcast、YouTube 影片的字幕雖然有噪音，但**噪音本身可以被訓練成過濾器**——弱監督不是妥協，是資源。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：弱監督資料的規模化

Whisper 的訓練集從網路爬取，經過自動過濾（去重、去音樂、去品質過差者），最終保留 68 萬小時：

| 來源特性 | 傳統 ASR 資料 | Whisper 資料 |
|---|---|---|
| 規模 | ~1,000 小時 | 680,000 小時 |
| 標註品質 | 人工精標 | 自動/弱標（含噪） |
| 語言 | 單語為主 | 96 種語言 |
| 領域 | 朗讀式 | 對話、演講、嘈雜環境 |

規模化曲線成立：錯誤率隨訓練資料量冪律下降，且**10 倍資料的收益尚未飽和**——暗示標註天花板根本不存在。

### 第二條線索：多任務 token 化——一個模型，四種工作

Whisper 把任務規格**編碼進輸入序列的開頭**（special tokens），讓單一 encoder-decoder Transformer 完成所有工作：

$$[\text{sot}]\ [\text{lang}]\ [\text{transcribe}|\text{translate}]\ [\text{ts}_{\text{start}}] \to \text{audio} \to \text{text}\ [\text{eot}]$$

- encoder：log-Mel 頻譜圖 → Transformer 編碼（表徵聲學內容）
- decoder：自迴歸生成文字 token，可選輸出**時間戳**
- `$<|translate|>$` token：X→英語翻譯任務直接從同樣的資料中學到，**不需要平行語料以外的任何工程**

這延續了 GPT-3「任務即提示」的哲學，但把它推廣到非文字模態。

### 第三條線索：零樣本效能的判決書

Whisper 未在 LibriSpeech 上微調，零樣本表現：

| 基準 | Whisper（零樣本） | 最佳微調 SOTA |
|---|---|---|
| LibriSpeech test-clean WER | ~1.8% | ~1.4–1.9% |
| LibriSpeech test-other WER | ~3.6% | ~2.5–3.3% |
| Common Voice 15（多語言平均） | 接近或超過監督 SOTA | — |

在乾淨朗讀資料上略遜於過擬合的專用模型，但在**嘈雜、口音、真實場景**的 robustness 上全面獲勝——因為訓練資料本身就是真實世界的雜訊分布。**弱監督買到的是泛化，不是基準分數**。

### 第四條線索：對齊的副產品——語言偵測

decoder 的語言 token 同時學會了語言辨識（LID），準確率在主要語言上超過 98%。這暗示：**多任務學習中的「順手任務」往往免費**——聲學表徵要能辨識轉錄目標，自然得先學會分辨語言。

### 第五條線索：魯棒性的來源——雜訊即正則化

傳統 ASR 在乾淨資料上過擬合，遇到真實環境就崩壞；Whisper 的訓練資料本身就是**真實世界的雜訊分布**：

$$\text{泛化誤差} \approx \text{訓練分布與測試分布的落差}$$

當訓練分布涵蓋 podcast、口音、背景音樂、遠場收音，落差自然縮小——**弱監督的「弱」，意外成為最強的正則化**。這是規模化哲學在聲學域的完整判決：規模不僅帶來能力，還帶來魯棒性。

## 結案 -- 後果與影響

- **語音辨識的民主化**：權重開源（MIT 授權），本地部署、離線轉錄、無隱私顧慮成為可能；大量下游工具（字幕、會議記錄、Podcast 搜尋）在數月內爆發。
- 下游生態的多樣性：faster-whisper（推理加速）、WhisperX（強制對齊）、Distil-Whisper（蒸餾版）相繼出現——與 Stable Diffusion 同期，開源權重再次證明「分發即革命」。
- **弱監督規模化的勝訴**：確認了「GPT-3 法則」在聲學域同樣成立，為跨模態大規模資料訓練（影像、視訊）提供先例。
- **翻譯任務的意外收穫**：X→英語語音翻譯零樣本可達監督系統水準，開啟語音翻譯的新研究方向。
- **低資源語言的破口與限制**：主要語言（英、西、法）表現頂級，但低資源語言（部分非洲語言）錯誤率仍高——弱監督的天花板仍在，只是被推高了；這成為後續低資源 ASR 研究的路標。
- 埋下伏筆：Whisper 的「任務 token」設計成為**多模態指令訓練**的雛形——2023 年 RT-2（見「2023-RT-2視覺語言動作模型.md」）把動作 token 塞進視覺語言模型，正是同一手法在機器人上的重演。
- 在本書主線中，Whisper 是**對話革命**的聲學支柱：ChatGPT 讓文字對話通用化，Whisper 讓語音進入同一介面——通往「2023-GPT-4多模態.md」的多模態整合。
- 偵探結語：Whisper 的勝訴關鍵不在架構（架構只是平凡的 encoder-decoder Transformer），而在**資料策略的翻案**——六十年前 ELIZA 證明人類會把智慧投射到字串機器上，Whisper 證明字串（字幕）機器能真的學出聽懂人類的能力。弱監督不是監督學習的妥協版，而是另一條通往智能的路。

## 關鍵人物與文獻

- Alec Radford、Jong Wook Kim、Tao Xu、Greg Brockman 等（OpenAI）：《Robust Speech Recognition via Large-Scale Weak Supervision》（2022，Whisper）。
- Aaron van den Oord 等：《WaveNet: A Generative Model for Raw Audio》（2016）——聲學神經建模的前案。
- Alex Graves 等：《Listen, Attend and Spell》（2015）——端到端 ASR 前驅。
- OpenAI：《Language Models are Few-Shot Learners》（2020）——弱監督規模化哲學的源頭。
- 偵探手記：本篇與「2020-GPT-3規模湧現.md」構成同一命題的兩份判決——文字域（GPT-3）與聲學域（Whisper）先後證明：弱監督 + 規模 > 精標 + 小資料。
- Greg Brockman、Sam Altman：Whisper 發布決策（2022 年 9 月）——權重開源在 OpenAI 內部並非共識，卻成為其開源策略少數的成功先例。
- 相關案件：2016-WaveNet語音合成.md、2011-Siri語音助理.md、2023-RT-2視覺語言動作模型.md、2023-GPT-4多模態.md

## 補充 -- 程式實作（python + numpy + pytorch）

本案管線（波形→log-mel→編解碼→文本＋坍縮解碼）的最小可執行版本，見 `_code/2022-Whisper.py`（已實測可跑，CPU 約 1 分鐘；四音調序列代替語音）：

```python
# 2022 - Whisper: log-mel + BiGRU 幀分類 + 坍縮解碼 (CTC 的精神縮影)
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

SR, TONE_LEN, GAP = 8000, 1600, 800
FREQS = [440.0, 554.4, 659.3, 880.0]  # 四音調 = 四個「詞」


def synth(seq, seed=0):  # 合成波形 (音調段+靜音間隙)
    rng = np.random.default_rng(seed)
    parts = []
    for s in seq:
        t = np.arange(TONE_LEN) / SR
        parts.append(np.sin(2 * np.pi * FREQS[s] * t) * 0.8)
        parts.append(np.zeros(GAP))
    wav = np.concatenate(parts) + rng.normal(0, 0.02, sum(len(p) for p in parts))
    return wav


def logmel(wav, n_fft=512, hop=256, n_mels=16):  # STFT -> mel分桶 -> log
    frames = [wav[i:i + n_fft] * np.hanning(n_fft)
              for i in range(0, len(wav) - n_fft + 1, hop)]
    spec = np.abs(np.fft.rfft(frames, axis=1)) ** 2
    edges = np.logspace(np.log10(80), np.log10(4000), n_mels + 1)
    freqs = np.fft.rfftfreq(n_fft, 1 / SR)
    mel = np.array([[spec[:, (freqs >= edges[m]) & (freqs < edges[m + 1])].sum(1)]
                    for m in range(n_mels)]).squeeze(1).T
    return np.log(mel + 1e-6).astype(np.float32)


def collapse(path, blank=4):  # 去重+去blank (CTC 解碼)
    out = []
    for p in path:
        if p != blank and (not out or p != out[-1]):
            out.append(p)
    return out


def main():
    torch.manual_seed(0)
    rng = np.random.default_rng(0)
    seqs = []  # 無連續重複 (坍縮會吃掉重複 -- blank 存在的理由)
    while len(seqs) < 120:
        s = rng.integers(0, 4, 5).tolist()
        if all(a != b for a, b in zip(s, s[1:])):
            seqs.append(s)
    feats = torch.stack([torch.tensor(logmel(synth(s, i))) for i, s in enumerate(seqs)])
    # (幀標籤 / BiGRU 訓練 / 評估略, 見 _code/2022-Whisper.py 全文)


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/2022-Whisper.py`，torch 2.12.0）：

```
幀準確率=0.989 整句全對=120/120 (坍縮解碼 -- CTC 的精神)
示範: 真值= [1, 3, 2, 0, 1] 解碼= [1, 3, 2, 0, 1]
結論: 譜圖->編解碼->文本; 任務前綴+時間戳同一套輸出 -- 魯棒性來自規模與雜訊
```

程式解說：`logmel` 即 Whisper 輸入的全部秘密——STFT 能量譜按對數分桶再取對數，人耳的非線性（mel 尺度）被寫死在特徵裡，後面才輪到神經網路。`collapse` 是 CTC 解碼的最小骨架：去重＋去 blank，幀準確率 98.9% 經它一壓，120 句全對。實測附帶真課：連續重複音（如 `[3,2,2,1,1]`）會被坍縮吃成 `[3,2,1]`——這正是 CTC 需要 blank 符號的理由，玩具把理論的牙口咬出來了。真 Whisper 把同一套輸出格式套上 `[lang][transcribe|translate][時間戳]` 前綴（本文第二條線索），68 萬小時弱監督把雜訊變成正則化（第五條線索）。
