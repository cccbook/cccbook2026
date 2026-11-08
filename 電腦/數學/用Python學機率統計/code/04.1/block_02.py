# 04.1-密度函數與累計分配
# 由 04.1-密度函數與累計分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# 密度是「每單位長度的機率」：寬度 0.3 的區間，機率 ≈ 密度 × 寬度
print(r.punif(0.5) - r.punif(0.2))   # P(0.2 < X <= 0.5)，U(0,1)
print(r.dunif(0.35) * 0.3)           # 密度(1) x 寬度(0.3) —— 完全一致（均勻時無誤差）

# 單點的機率為 0：寬度越窄，機率越趨近 0
print(r.punif(0.5) - r.punif(0.5 - 0.001))
print(r.punif(0.5) - r.punif(0.5 - 0.000001))
