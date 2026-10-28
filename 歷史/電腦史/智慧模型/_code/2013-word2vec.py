# 2013 - word2vec 詞向量 (Mikolov): Skip-gram + 負取樣
# 對應本書: 2013-word2vec詞向量.md
# 公式: log σ(v_O'·v_I) + Σ_k E[log σ(-v_k'·v_I)] (二元分類取代整表 softmax)
# 展示: 極小語料上, 共現詞的餘弦相似度 > 無關詞 (分佈假說的可執行版)
import torch
import torch.nn as nn
import torch.nn.functional as F


def main():
    torch.manual_seed(0)
    # 極小語料: 重複「國王/王后/男人/女人」與「巴黎/法國/羅馬/義大利」的共現句型
    sents = ([["king", "man", "palace"], ["queen", "woman", "palace"],
              ["king", "queen", "crown"], ["man", "woman", "people"],
              ["paris", "france", "city"], ["rome", "italy", "city"],
              ["france", "italy", "europe"], ["paris", "rome", "capital"]] * 30)
    vocab = sorted({w for s in sents for w in s})
    wi = {w: i for i, w in enumerate(vocab)}
    V, D = len(vocab), 8
    emb_in = nn.Embedding(V, D)
    emb_out = nn.Embedding(V, D)
    opt = torch.optim.Adam(list(emb_in.parameters()) + list(emb_out.parameters()), lr=5e-2)
    pairs = [(wi[w], wi[c]) for s in sents for w in s for c in s if c != w]
    for ep in range(60):
        idx = torch.randperm(len(pairs))[:256]
        ci = torch.tensor([pairs[i][0] for i in idx])
        pi = torch.tensor([pairs[i][1] for i in idx])
        neg = torch.randint(0, V, (len(idx), 5))
        opt.zero_grad()
        pos = F.logsigmoid((emb_in(ci) * emb_out(pi)).sum(1)).mean()
        neg_s = F.logsigmoid(-(emb_in(ci).unsqueeze(1) * emb_out(neg)).sum(2)).mean()
        (-(pos + neg_s)).backward()   # 負取樣目標: 真上下文推高, 雜訊詞壓低
        opt.step()
    with torch.no_grad():
        E = emb_in.weight
        E = E / E.norm(dim=1, keepdim=True)
        S = E @ E.T
        def sim(a, b):
            return float(S[wi[a], wi[b]])
        print("共現詞相似度 (應高): king-queen=%.2f  paris-france=%.2f  man-woman=%.2f"
              % (sim("king", "queen"), sim("paris", "france"), sim("man", "woman")))
        print("無關詞相似度 (應低): king-paris=%.2f  queen-italy=%.2f  crown-europe=%.2f"
              % (sim("king", "paris"), sim("queen", "italy"), sim("crown", "europe")))
        # 語義聚類: 地理群 vs 王室群 -- 群內應緊, 群間應鬆 (分佈假說的量化版)
        import itertools
        geo = ["paris", "france", "rome", "italy", "city", "europe", "capital"]
        roy = ["king", "queen", "man", "woman", "palace", "crown", "people"]
        intra = sum(float(S[wi[a], wi[b]]) for g in (geo, roy)
                    for a, b in itertools.combinations(g, 2))
        n_intra = sum(len(g) * (len(g) - 1) // 2 for g in (geo, roy))
        inter = sum(float(S[wi[a], wi[b]]) for a in geo for b in roy) / (len(geo) * len(roy))
        print(f"群內平均cos={intra / n_intra:.2f} 群間平均cos={inter:.2f} "
              f"(同義群聚在一起 -- You shall know a word by the company it keeps)")
        # 語義算術縮影: paris - france + italy 的方向 (小語料下看前三名落在哪群)
        v = E[wi["paris"]] - E[wi["france"]] + E[wi["italy"]]
        v = v / v.norm()
        top3 = sorted(((w, float(v @ E[wi[w]])) for w in vocab
                       if w not in ("paris", "france", "italy")),
                      key=lambda t: -t[1])[:3]
        print("paris - france + italy 前三名:", [(w, round(s, 2)) for w, s in top3],
              "(大語料時第一名即 rome -- 方向攜帶語義)")


if __name__ == "__main__":
    main()
