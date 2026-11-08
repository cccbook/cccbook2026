# 10.1-裝置與版面
# 由 10.1-裝置與版面.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

gr = r.Graphics(width=7.0, height=5.0)
print("mar =", gr.mar)
print("mgp =", gr.mgp)
print("cex =", gr.cex, " pch =", gr.pch, " lwd =", gr.lwd)
print("mfrow =", gr.mfrow)
print("usr（尚未 plot，預設）=", gr.usr)
