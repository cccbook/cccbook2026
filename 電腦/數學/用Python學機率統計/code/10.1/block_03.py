# 10.1-裝置與版面
# 由 10.1-裝置與版面.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

print("=== r.pretty 的示範 ===")
for rng in ([1.0, 20.0], [0.0, 1.0], [3.14159, 3.14160], [-0.5, 0.5], [0.0, 97.3]):
    print(f"  pretty({rng}, 5) =", r.pretty(list(rng), 5))
print("  pretty([1,20], 4) =", r.pretty([1.0, 20.0], 4))
print("  pretty([1,20], 8) =", r.pretty([1.0, 20.0], 8))
print("  pretty([1,20], 10) =", r.pretty([1.0, 20.0], 10))
