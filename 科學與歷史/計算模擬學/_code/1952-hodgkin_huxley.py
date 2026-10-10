# -*- coding: utf-8 -*-
"""1952 Hodgkin-Huxley 單房室模型 (對應 wiki: 計算模擬學 / HH 動作電位)
只用 numpy,固定種子。電流脈衝 I=10 uA/cm^2 持續 5ms,Euler dt=0.01ms 跑 50ms。
驗證:產生動作電位(V 峰值 > 0 mV)且靜息約 -65 mV。
"""
import numpy as np

np.random.seed(0)

# --- 參數 (經典 HH) ---
C = 1.0        # uF/cm^2
gNa = 120.0    # mS/cm^2
gK = 36.0
gL = 0.3
ENa = 50.0     # mV
EK = -77.0
EL = -54.387

dt = 0.01      # ms
T = 50.0       # ms
steps = int(T / dt)

def alpha_m(V): return 0.1 * (V + 40.0) / (1.0 - np.exp(-(V + 40.0) / 10.0)) if abs(V + 40.0) > 1e-7 else 1.0
def beta_m(V):  return 4.0 * np.exp(-(V + 65.0) / 18.0)
def alpha_h(V): return 0.07 * np.exp(-(V + 65.0) / 20.0)
def beta_h(V):  return 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))
def alpha_n(V): return 0.01 * (V + 55.0) / (1.0 - np.exp(-(V + 55.0) / 10.0)) if abs(V + 55.0) > 1e-7 else 0.1
def beta_n(V):  return 0.125 * np.exp(-(V + 65.0) / 80.0)

V = -65.0
m = alpha_m(V) / (alpha_m(V) + beta_m(V))
h = alpha_h(V) / (alpha_h(V) + beta_h(V))
n = alpha_n(V) / (alpha_n(V) + beta_n(V))

Vs = np.empty(steps)
for i in range(steps):
    t = i * dt
    I = 10.0 if 5.0 <= t < 10.0 else 0.0  # 10 uA/cm^2 持續 5ms
    INa = gNa * m**3 * h * (V - ENa)
    IK = gK * n**4 * (V - EK)
    IL = gL * (V - EL)
    V = V + dt * (I - INa - IK - IL) / C
    m = m + dt * (alpha_m(V) * (1 - m) - beta_m(V) * m)
    h = h + dt * (alpha_h(V) * (1 - h) - beta_h(V) * h)
    n = n + dt * (alpha_n(V) * (1 - n) - beta_n(V) * n)
    Vs[i] = V

V_peak = float(np.max(Vs))
V_rest_init = float(Vs[0])
V_rest_end = float(np.mean(Vs[-500:]))  # 最後 5ms 平均
ok_peak = V_peak > 0.0
ok_rest = (-75.0 < V_rest_end < -60.0) and (-75.0 < V_rest_init < -60.0)

print(f"V_peak={V_peak:.3f} mV (驗證 > 0 mV: {'PASS' if ok_peak else 'FAIL'})")
print(f"V_rest_init={V_rest_init:.3f} mV, V_rest_end={V_rest_end:.3f} mV (驗證約 -65 mV: {'PASS' if ok_rest else 'FAIL'})")
print(f"VERIFY: V_peak={V_peak:.6f}, V_rest_end={V_rest_end:.6f}")
assert ok_peak, "未產生動作電位"
assert ok_rest, "靜息電位偏離 -65 mV"
print("ALL CHECKS PASS")
