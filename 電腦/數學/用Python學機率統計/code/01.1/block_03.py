# 01.1-從母體到樣本
# 由 01.1-從母體到樣本.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

g2 = r.Graphics(width=7.0, height=4.5)
g2.hist(means, main="1000 個樣本平均數的分布", xlab="樣本平均數 (cm)")
g2.save(\"img/sampling_dist.svg\")
