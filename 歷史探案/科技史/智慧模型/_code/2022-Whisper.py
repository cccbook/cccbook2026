# 2022 - Whisper 語音辨識: log-mel + 多任務 token +編解碼器
# 對應本書: 2022-Whisper語音辨識.md
# 公式: [sot][lang][transcribe|translate][ts] -> audio -> text [eot]; 68萬小時弱監督
# 展示: 合成四音調序列 -> numpy STFT log-mel -> BiGRU 幀分類 -> 坍縮去重 (CTC 解碼的精神縮影)
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

SR, TONE_LEN, GAP = 8000, 1600, 800
FREQS = [440.0, 554.4, 659.3, 880.0]  # 四音調 = 四個「詞」


def synth(seq, seed=0):
    rng = np.random.default_rng(seed)
    parts = []
    for s in seq:
        t = np.arange(TONE_LEN) / SR
        parts.append(np.sin(2 * np.pi * FREQS[s] * t) * 0.8)
        parts.append(np.zeros(GAP))
    wav = np.concatenate(parts) + rng.normal(0, 0.02, sum(len(p) for p in parts))
    return wav


def logmel(wav, n_fft=512, hop=256, n_mels=16):
    frames = [wav[i:i + n_fft] * np.hanning(n_fft)
              for i in range(0, len(wav) - n_fft + 1, hop)]
    spec = np.abs(np.fft.rfft(frames, axis=1)) ** 2
    # mel 縮影: 把頻率軸對數分桶 (phenomenon 級近似, 夠演示)
    edges = np.logspace(np.log10(80), np.log10(4000), n_mels + 1)
    freqs = np.fft.rfftfreq(n_fft, 1 / SR)
    mel = np.array([[spec[:, (freqs >= edges[m]) & (freqs < edges[m + 1])].sum(1)]
                    for m in range(n_mels)]).squeeze(1).T  # (幀, mel帶)
    return np.log(mel + 1e-6).astype(np.float32)  # log-mel


def collapse(path, blank=4):
    out = []
    for p in path:
        if p != blank and (not out or p != out[-1]):
            out.append(p)
    return out


def main():
    torch.manual_seed(0)
    rng = np.random.default_rng(0)
    # 資料: 5 音調隨機序列 (無連續重複 -- CTC 坍縮會吃掉重複, 故需 blank 隔開, 見解說)
    seqs = []
    while len(seqs) < 120:
        s = rng.integers(0, 4, 5).tolist()
        if all(a != b for a, b in zip(s, s[1:])):
            seqs.append(s)
    feats = torch.stack([torch.tensor(logmel(synth(s, i))) for i, s in enumerate(seqs)])
    per_seq = feats.size(1)
    # 幀標籤: 音調段標本調, 靜音段標 blank(4)
    frames_per_tone = TONE_LEN // 256 + 1
    gap_frames = GAP // 256 + 1
    def frame_labels(s):
        lab = []
        for tone in s:
            lab += [tone] * frames_per_tone + [4] * gap_frames
        return (lab + [4] * per_seq)[:per_seq]
    Y = torch.tensor([frame_labels(s) for s in seqs])

    class FrameCls(nn.Module):  # BiGRU 編碼器 + 幀分類頭 (編解碼器的精神縮影)
        def __init__(self):
            super().__init__()
            self.gru = nn.GRU(16, 64, batch_first=True, bidirectional=True)
            self.head = nn.Linear(128, 5)

        def forward(self, f):
            return self.head(self.gru(f)[0])

    net = FrameCls()
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    for ep in range(40):
        opt.zero_grad()
        loss = F.cross_entropy(net(feats).reshape(-1, 5), Y.reshape(-1))
        loss.backward()
        opt.step()
    with torch.no_grad():
        pred = net(feats).argmax(-1)
        frame_acc = (pred == Y).float().mean().item()
        seq_ok = sum(1 for p, s in zip(pred.tolist(), seqs) if collapse(p) == s)
    print(f"幀準確率={frame_acc:.3f} 整句全對={seq_ok}/{len(seqs)} (坍縮解碼 -- CTC 的精神)")
    print("示範: 真值=", seqs[0], "解碼=", collapse(pred[0].tolist()))
    print("結論: 譜圖->編解碼->文本; 任務前綴+時間戳同一套輸出 -- 魯棒性來自規模與雜訊")


if __name__ == "__main__":
    main()
