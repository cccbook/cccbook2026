# 03.1-伯努利試驗與二項分配
# 由 03.1-伯努利試驗與二項分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

g2 = r.Graphics(width=7.0, height=4.5)
g2.barplot(theo, [str(k) for k in ks])          # 理論值長條
for i, t in enumerate(theo):
    g2.rect(i + 0.6, 0, 0.8, sim[i])            # 模擬頻率描邊
g2.save(\"img/binom_pmf_sim.svg\")
