# -*- coding: utf-8 -*-
# 06.1 機率語言模型：numpy 實作 bigram 語言模型，計算困惑度（PPL）
import numpy as np

# 玩具語料（詞以索引表示）：貓=0, 追=1, 狗=2
# 句子：「貓 追 狗」x3、「狗 追 貓」x1
sentences = [[0, 1, 2], [0, 1, 2], [0, 1, 2], [2, 1, 0]]
V = 3  # 詞彙表大小

# 統計 bigram 頻率（含句首 <s>=3、句尾 </s>=4 的虛擬詞）
BOS, EOS = 3, 4
counts = np.ones((V + 2, V + 2))  # +1 平滑（Laplace smoothing）
for s in sentences:
    seq = [BOS] + s + [EOS]
    for a, b in zip(seq[:-1], seq[1:]):
        counts[a, b] += 1

# 最大概似 + 平滑：P(b|a) = C(a,b) / C(a)
P = counts / counts.sum(axis=1, keepdims=True)

names = {0: "貓", 1: "追", 2: "狗", 3: "<s>", 4: "</s>"}
print("bigram 條件機率（加 1 平滑後）：")
print(f"  P(狗|貓) = {P[0,2]:.4f}    P(貓|狗) = {P[2,0]:.4f}")
print(f"  P(追|貓) = {P[0,1]:.4f}    P(追|狗) = {P[2,1]:.4f}")

# 測試句：「貓 追 狗」，計算困惑度
test = [0, 1, 2]
seq = [BOS] + test + [EOS]
loglik = 0.0
probs = []
for a, b in zip(seq[:-1], seq[1:]):
    p = P[a, b]
    probs.append(p)
    loglik += np.log(p)
T = len(probs)
ppl = np.exp(-loglik / T)
print(f"\n測試句「貓 追 狗」各步機率：{[f'{p:.3f}' for p in probs]}")
print(f"平均負對數概似（交叉熵）= {-loglik/T:.4f} nat")
print(f"困惑度 PPL = exp(交叉熵) = {ppl:.4f}")
print(f"PPL ≈ 每步平均等 unsure 到的選項數：{ppl:.2f} 個等機率選項")

# 對照：完美模型（每步機率都接近 1）困惑度接近 1
perfect_probs = [0.99, 0.99, 0.99, 0.99]
ppl_perfect = np.exp(-np.sum(np.log(perfect_probs)) / len(perfect_probs))
print(f"\n對照：若每步機率 0.99，PPL = {ppl_perfect:.4f}（預測越準，PPL 越接近 1）")
