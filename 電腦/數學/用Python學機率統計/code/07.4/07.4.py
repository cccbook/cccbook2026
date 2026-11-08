# 07.4-比例檢定與卡方檢定
# 由 07.4-比例檢定與卡方檢定.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r
print(r.binom_test(12, 100, 0.05, alternative='greater'))


# --- 區塊 2 ---
print(r.prop_test(12, 100, 0.05, alternative='greater'))


# --- 區塊 3 ---
print(r.prop_test(12, 100, 0.05, alternative='greater', correct=False))


# --- 區塊 4 ---
obs = [315, 101, 108, 32]
p_theory = [9/16, 3/16, 3/16, 1/16]

print(r.chisq_test(obs, p_theory))


# --- 區塊 5 ---
print("形狀（圓 vs 皺）:", r.chisq_test([315+108, 101+32], [3/4, 1/4]))
print("顏色（黃 vs 綠）:", r.chisq_test([315+101, 108+32], [3/4, 1/4]))


# --- 區塊 6 ---
gender = ['M']*45 + ['F']*55
pref   = ['coffee']*30 + ['tea']*15 + ['coffee']*25 + ['tea']*30

t = r.table(gender, pref, x_name='性別', y_name='偏好')
print(t)


# --- 區塊 7 ---
print(r.chisq_test_table([[25, 30], [30, 15]]))


# --- 區塊 8 ---
print(r.chisq_test_table([[25, 30], [30, 15]], correct=False))
