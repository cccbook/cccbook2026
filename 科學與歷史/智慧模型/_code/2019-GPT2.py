# 2019 - GPT-2: 規模 + 採樣即產品 (溫度 / top-k 整形分佈)
# 對應本書: 2019-GPT-2危險模型.md
# 公式: p(輸出) = p(下一token | 任務描述也寫進上下文); L = Σ_doc Σ_i log p(x_i|x_<i)
# 展示: 詞級 bigram 上, 溫度/top-k 如何整形下一詞分佈 (銳化 vs 拉平) 與生成熵,
#       以及「任務寫進上下文」的格式 (bigram 太弱只學格式, 語義需規模 -- 誠實標註)
import math
import torch


def shape(p, temperature=1.0, top_k=0):
    p = p.float()
    if top_k > 0:  # 只留前 k (GPT-2 採樣標配)
        v, _ = torch.topk(p, top_k)
        p = torch.where(p >= v[-1], p, torch.zeros_like(p))
        p = p / p.sum()
    p = (p.clamp_min(1e-9).log() / temperature).exp()  # 溫度: 重塑分佈銳度
    return p / p.sum()


def main():
    torch.manual_seed(0)
    docs = (["translate hello : hola", "translate cat : gato", "translate dog : perro",
             "summarize cats eat fish : cats fed", "summarize dogs run fast : dogs quick",
             "question who eats fish : cats", "question who barks : dogs",
             "see bird sings sweetly : song"] * 40)
    vocab = sorted({w for d in docs for w in d.split()})
    wi = {w: i for i, w in enumerate(vocab)}
    V = len(vocab)
    C = torch.ones(V, V)  # 加一平滑; 無監督多任務目標 L 的最小骨架
    for d in docs:
        ids = [wi[w] for w in d.split()]
        for a, b in zip(ids, ids[1:]):
            C[a, b] += 1
    P = C / C.sum(1, keepdim=True)
    ppl = math.exp(-sum(math.log(float(P[wi[a], wi[b]]))
                        for d in docs for a, b in zip(d.split(), d.split()[1:]))
                   / sum(len(d.split()) - 1 for d in docs))
    print(f"詞彙 {V} 詞, bigram 困惑度={ppl:.2f} (GPT-2: 同一目標, 10億參數, 網路級語料)")

    # 採樣整形: 同一上下文 'translate', 三種溫度的下一詞分佈
    print("上下文 'translate' 的下一詞分佈 (top3):")
    for name, kw in [("T=0.5+top3", {"temperature": 0.5, "top_k": 3}),
                     ("T=1.0", {}),
                     ("T=1.5", {"temperature": 1.5})]:
        q = shape(P[wi["translate"]], **kw)
        top = torch.topk(q, 3)
        ent = -(q * q.clamp_min(1e-9).log()).sum().item() / math.log(2)
        words = [(vocab[i], round(float(p), 2)) for p, i in zip(top.values, top.indices)]
        print(f"  {name}: {words} 熵={ent:.2f} bits (低溫銳化保守, 高溫拉平發散)")

    # 生成流的熵: 各設定的 200 詞輸出 unigram 熵
    for name, kw in [("T=0.5+top3", {"temperature": 0.5, "top_k": 3}),
                     ("T=1.5", {"temperature": 1.5})]:
        torch.manual_seed(7)
        cur, cnt = wi["translate"], torch.zeros(V)
        for _ in range(200):
            cur = torch.multinomial(shape(P[cur], **kw), 1).item()
            cnt[cur] += 1
        f = cnt / cnt.sum()
        ent = -(f * f.clamp_min(1e-9).log()).sum().item() / math.log(2)
        print(f"  生成流熵 {name}: {ent:.2f} bits")
    print("結論: 採樣是產品的性格旋鈕; bigram 只學到『任務: 前綴格式』, "
          "真正的零樣本語義需 GPT-2 級規模 -- 規模即能力 (見 2020-GPT-3規模湧現.md)")


if __name__ == "__main__":
    main()
