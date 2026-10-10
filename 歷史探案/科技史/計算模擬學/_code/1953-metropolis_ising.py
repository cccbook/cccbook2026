# -*- coding: utf-8 -*-
"""1953 Metropolis + Ising 2D 模型 (對應 wiki: 計算模擬學 / 蒙地卡羅統計物理)
只用 numpy,固定種子。20x20,T=1.0(有序)與 T=4.0(無序),Metropolis 各 2000 sweeps。
驗證:低溫 |M|>0.9、高溫 |M|<0.4。
"""
import numpy as np

np.random.seed(0)
L = 20
SWEEPS = 2000

def run_ising(T):
    spins = np.random.choice(np.array([-1, 1]), size=(L, L))
    # dE 只可能為 -8,-4,0,4,8,預先算接受率
    p4 = np.exp(-4.0 / T)
    p8 = np.exp(-8.0 / T)
    for _ in range(SWEEPS):
        ii = np.random.randint(0, L, size=L * L)
        jj = np.random.randint(0, L, size=L * L)
        rr = np.random.rand(L * L)
        for k in range(L * L):
            i = int(ii[k]); j = int(jj[k])
            s = spins[i, j]
            nb = spins[(i + 1) % L, j] + spins[(i - 1) % L, j] + spins[i, (j + 1) % L] + spins[i, (j - 1) % L]
            dE = 2 * s * nb
            if dE <= 0:
                spins[i, j] = -s
            elif dE == 4:
                if rr[k] < p4:
                    spins[i, j] = -s
            else:  # dE == 8
                if rr[k] < p8:
                    spins[i, j] = -s
    mag = abs(float(np.sum(spins))) / (L * L)
    return mag

m_low = run_ising(1.0)
m_high = run_ising(4.0)
ok_low = m_low > 0.9
ok_high = m_high < 0.4
print(f"T=1.0 |M|={m_low:.4f} (驗證 >0.9: {'PASS' if ok_low else 'FAIL'})")
print(f"T=4.0 |M|={m_high:.4f} (驗證 <0.4: {'PASS' if ok_high else 'FAIL'})")
print(f"VERIFY: M_low={m_low:.6f}, M_high={m_high:.6f}")
assert ok_low, "低溫未有序"
assert ok_high, "高溫未無序"
print("ALL CHECKS PASS")
