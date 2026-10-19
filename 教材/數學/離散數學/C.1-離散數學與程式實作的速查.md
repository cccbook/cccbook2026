# 附錄 C：離散數學與程式實作的速查（Python）

> 本書各章的 Python 範例散落各節，本附錄集中提供最常用的十段「即戰力」程式碼，供複習與實驗。

## C.1 邏輯運算與真值表（第 1 章）

```python
import itertools

def truth_table(expr, vars):
    for vals in itertools.product([0,1], repeat=len(vars)):
        env = dict(zip(vars, vals))
        print(env, '->', expr(env))

# 檢驗 De Morgan：not(P and Q) == (not P) or (not Q)
for p, q in itertools.product([0,1], repeat=2):
    assert (not (p and q)) == (not p or not q)
```

## C.2 子集與冪集（第 2 章）

```python
def powerset(S):
    S = list(S)
    n = len(S)
    return [frozenset(S[i] for i in range(n) if mask>>i & 1)
            for mask in range(2**n)]

print(len(powerset({1,2,3})))  # 8
```

## C.3 排列組合（第 3 章）

```python
from math import comb, perm
from itertools import combinations, permutations

print(comb(52,5))       # 2,598,960：德州撲克手牌
print(perm(10,3))       # 720
```

## C.4 遞迴與動態規劃（第 4 章）

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

def hanoi(n, a='A', b='B', c='C'):
    if n:
        hanoi(n-1, a, c, b)
        print(f"{a} -> {c}")
        hanoi(n-1, b, a, c)
```

## C.5 生成函數（第 4 章）

```python
# (1+x)^n 係數 = 二項式係數；兌換問題用捲積
from functools import reduce
import numpy as np

def coins_change(coins, upto):
    f = np.zeros(upto+1); f[0] = 1
    for c in coins:                     # 每種硬幣乘上 1+x^c+x^{2c}+...
        for i in range(c, upto+1):
            f[i] += f[i-c]
    return f

print(int(coins_change([1,2,5], 10)[10]))  # 10 元兌法數
```

## C.6 圖與最短路徑（第 5–6 章）

```python
import heapq

def dijkstra(adj, s):
    dist = {s: 0}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float('inf')): continue
        for v, w in adj[u]:
            if d + w < dist.get(v, float('inf')):
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist

# 最小生成樹（Kruskal）
def kruskal(n, edges):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    mst = []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if find(u) != find(v):
            parent[find(u)] = find(v)
            mst.append((u, v, w))
    return mst
```

## C.7 圖著色與平面性（第 6 章）

```python
def is_bipartite(adj, n):
    color = [None]*n
    for s in range(n):
        if color[s] is None:
            color[s] = 0
            stack = [s]
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if color[v] is None:
                        color[v] = color[u]^1; stack.append(v)
                    elif color[v] == color[u]:
                        return False
    return True
```

## C.8 模運算與 RSA（第 7 章）

```python
def egcd(a, b):
    if b == 0: return (a, 1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a//b)*y)

def modinv(a, n):
    g, x, _ = egcd(a % n, n)
    assert g == 1
    return x % n

def is_prime(n):
    if n < 2: return False
    i = 2
    while i*i <= n:
        if n % i == 0: return False
        i += 1
    return True

# pow(base, exp, mod) 內建即快速冪，RSA 核心一行
m, e, d, N = 42, 65537, 12345, 97*101
assert pow(pow(m, e, N), d, N) == m
```

## C.9 群的階與 Burnside（第 8 章）

```python
def order(g, n):
    k, cur = 1, g % n
    while cur != 1:
        cur = cur * g % n; k += 1
    return k

print(order(3, 7))   # 6：3 是模 7 的原根
```

## C.10 有限自動機（第 8 章）

```python
def run_dfa(delta, start, accept, s):
    q = start
    for ch in s:
        q = delta[(q, ch)]
    return q in accept

# 接受含偶數個 a 的字串
delta = {(0,'a'):1, (0,'b'):0, (1,'a'):0, (1,'b'):1}
assert run_dfa(delta, 0, {0}, "abba")
assert not run_dfa(delta, 0, {0}, "ab")
```

## 小結

這些片段共同展示了本書的核心論點：**離散數學的每一個抽象結構（邏輯、集合、遞迴、圖、群、自動機），都能在幾行程式碼中「活起來」**。建議讀者把每段程式跑一遍、改參數、破壞它、再修好——這是最快的理解方式。
