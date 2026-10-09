# 2011 - Watson 問答系統: 問題分析 -> 假說生成 -> 證據打分 -> 置信排序 (DeepQA-lite)
# 對應本書: 2011-Watson問答系統.md
# 展示: TF-IDF 检索候選 + 詞重疊/類型 bonus 打分 + 逻辑回归式置信, Jeopardy 玩具題全對
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

CORPUS = [  # (篇章, 內含答案)
    ("Paris is the capital of France, famous for the Eiffel Tower.", "Paris"),
    ("Rome is the capital of Italy, home of the Colosseum.", "Rome"),
    ("The Eiffel Tower was completed in 1889 for the Paris exposition.", "1889"),
    ("Shakespeare wrote Hamlet and Macbeth in England.", "Shakespeare"),
    ("Water boils at 100 degrees Celsius at sea level.", "100"),
    ("The human heart has four chambers.", "four"),
    ("Photosynthesis converts carbon dioxide and water into glucose.", "glucose"),
    ("The Great Wall of China stretches over 21000 kilometers.", "21000"),
]
QUESTIONS = [
    ("Which city is famous for the Eiffel Tower?", "Paris"),
    ("Where is the Colosseum?", "Rome"),
    ("When was the Eiffel Tower completed?", "1889"),
    ("Who wrote Hamlet?", "Shakespeare"),
    ("At what temperature does water boil?", "100"),
]


def main():
    docs = [d for d, _ in CORPUS]
    vec = TfidfVectorizer().fit(docs)
    D = vec.transform(docs)
    print("DeepQA-lite: 检索(廣撒網) -> 打分(證據) -> 置信(排序):")
    top1 = 0
    for q, gold in QUESTIONS:
        cand = D @ vec.transform([q]).T          # 假說生成: 全庫打分
        order = np.argsort(-cand.toarray().ravel())[:3]
        scored = []
        for i in order[:3]:                       # 證據打分: TF-IDF + 答案詞 bonus
            bonus = 0.5 if CORPUS[i][1].lower() in q.lower() + " " + docs[i].lower() else 0
            scored.append((float(cand[i, 0]) + bonus, CORPUS[i][1], docs[i][:40]))
        scored.sort(reverse=True)
        conf = 1 / (1 + np.exp(-(scored[0][0] * 4 - 1)))  # 逻辑式置信 (sigmoid 校準縮影)
        ok = scored[0][1] == gold
        top1 += ok
        print(f"  Q: {q}\n    -> {scored[0][1]} (置信={conf:.2f}) {'✓' if ok else '✗'}")
    print(f"Top-1: {top1}/{len(QUESTIONS)} (Jeopardy 玩具版 -- 真 Watson 3472 個模块同精神)")
    print("結論: 廣撒網+百家打分+敢押注 -- Watson 的哲學是集成, 不是單一模型")


if __name__ == "__main__":
    main()
