# 1952-GraceHopperA0編譯器

## 案件摘要
1952 年，Grace Hopper 在 UNIVAC 上讓 A-0 首次運作——史上第一個「編譯器」。她從 Mark I 時代的「coder」經驗體悟：同樣的副程式被一遍遍手寫，是純粹的浪費。她把「compiler」這個字從「編纂目錄」搬到程式世界——把副程式庫「編譯」成一支可執行程式。當時學界質疑「機器只會算術，不會翻譯」，Hopper 用機器自己給了答案。

## 前因 -- 為什麼會有這個案子
- **Mark I 的 coder 文化**：1944 年 Hopper 加入哈佛 Mark I 團隊，當時「程式設計師」（coder）的地位是「跟在機器旁邊抄表的人」——每個問題都要手寫一遍求 sin、開方、線性代數的機器碼。
- **重複的浪費**：Hopper 發現，寫一個彈道表的程式與寫一個統計程式，80% 的副程式內容幾乎一樣——只差常數與參數。她推論：這些副程式應該被「寫一次、存起來、反覆使用」。
- **副程式庫的誕生**：Mark I 時代她已開始建立手寫副程式庫；到 UNIVAC 時代，她的問題變成——如何讓**機器自己**把這些副程式組裝成完整程式？
- **「機器不會翻譯」的質疑**：當時主流觀點認為電腦是「數值計算機器」，讓它處理符號（翻譯程式）既浪費又不可靠。Hopper 回應：機器做的正是它最擅長的事——**查表與搬運**。

## 線索與推理 -- 數學式、程式、理論

### 案件的關鍵：A-0 到底做了什麼？
A-0 的本質不是「翻譯語言」，而是「**連結器 + 載入器**」的祖先：程式師寫一連串「副程式呼叫」（以偽碼描述），A-0 把它們與**磁帶上的副程式庫**比對，選出對應的機器碼，串接成一支可執行程式。

流程（伪代碼）：

```text
A-0 編譯流程：
1. 輸入：一串偽碼指令，如 "R = A + B"（以 UNIVAC 指令碼編碼）
2. 查表：在副程式庫（磁帶）中尋找對應的機器碼段
3. 連結：把各機器碼段依序串接，填入參數位址
4. 輸出：一支完整的機器語言程式，可直接執行
```

用現代 Python 模擬這個「副程式庫連結」的抽象：

```python
# A-0 的核心抽象：副程式庫 + 連結
LIBRARY = {
    "ADD":   "LOAD {a}; ADD {b}; STORE {r}",
    "SUB":   "LOAD {a}; SUB {b}; STORE {r}",
    "SIN":   "CALL sin_routine; STORE {r}",
    "PRINT": "WRITE {r}",
}

def a0_compile(pseudo_instructions):
    """Hopper 的洞察：把偽碼『編譯』成機器碼，本質是查表 + 字串拼接"""
    machine_code = []
    for op, args in pseudo_instructions:
        template = LIBRARY[op]                    # 1. 查副程式庫
        code = template.format(**args)            # 2. 填入參數位址
        machine_code.append(code)                 # 3. 串接
    return "; ".join(machine_code)                # 4. 輸出完整程式

program = [
    ("ADD",   {"a": "A", "b": "B", "r": "R"}),
    ("SIN",   {"r": "S"}),
    ("PRINT", {"r": "S"}),
]
print(a0_compile(program))
# 輸出: LOAD A; ADD B; STORE R; CALL sin_routine; STORE S; WRITE S
```

這段模擬說明 Hopper 的核心抽象：**編譯 = 從庫中選取現成機器碼段 + 參數代換 + 線性串接**。它還不是現代的「語言翻譯」，但已把「程式」從「機器碼的逐字手寫」解放出來。

### 「compiler」一詞的考據
Hopper 借用「compile」的字源——「編纂」（如 compile a dictionary）。她的原始意義是「把副程式庫編纂成一支程式」：

$$\text{Compiler} : \{\text{Subroutine}_1, \dots, \text{Subroutine}_n\} \times \text{Call Script} \to \text{Executable}$$

這個定義與現代「編譯器 = 語言到語言的翻譯器」不同——真正的語言翻譯，要等到 1951 年 Böhm 的博士論文。

### 同案的另兩位兇手
- **Corrado Böhm（1951）**：瑞士 ETH 的博士論文，設計了一門語言 $\mathcal{L}$，並**用 $\mathcal{L}$ 自己**寫出 $\mathcal{L}$ 的編譯器——史上第一個「自舉」（self-compiling）的編譯器，這個概念後來成為所有編譯器理論的基石。
- **Heinz Rutishauser（1950-1952）**：在 Z4 上提出「B0 自動編碼」——用數學式記號描述公式，讓機器展開為機器碼。他是 ALGOL 的前身思想。

### 三案對照
| | Hopper A-0 (1952) | Böhm (1951) | Rutishauser (1950) |
|---|---|---|---|
| 本質 | 副程式庫連結 | 真編譯器 + 自舉 | 公式自動展開 |
| 語言層次 | 偽碼呼叫 | 完整語言 | 數學式 |
| 意義 | 編譯器概念誕生 | 自舉的先驅 | ALGOL 思想源頭 |

## 結案 -- 後果與影響
- **A-0 到 A-2 到 FLOW-MATIC**：Hopper 持續演進她的系統，1958 年的 FLOW-MATIC 已接近商業資料處理語言——直接催生 COBOL（1959）。
- **程式設計師的解放**：A-0 證明「機器可以替人寫程式」，程式設計師從「抄表員」變成「語言的使用者」——軟體工業的社會學基礎由此建立。
- **「自動編碼」的公理化**：Hopper、Böhm、Rutishauser 三人幾乎同時證明：高階描述到機器碼的翻譯不僅可行，而且必要——這直接為 FORTRAN（1957）的優化編譯器鋪路。
- **COBOL 的母親**：Hopper 1959 年主導 CODASYL，把 FLOW-MATIC 的英語化風格帶進 COBOL——史上最長壽的商業語言。

## 關鍵人物與文獻
- **Grace Hopper**：Mark I coder → UNIVAC A-0 (1952) → FLOW-MATIC → COBOL 之母。
- **Corrado Böhm**：1951 博士論文，自舉編譯器先驅，後為 λ 演算與 Böhm tree 著名。
- **Heinz Rutishauser**：Z4 自動編碼，後為 ALGOL 六人小組成員。
- 文獻：
  - G. M. Hopper, "The Education of a Computer," *Proc. ACM National Meeting*, Pittsburgh (1952).
  - C. Böhm, "Calculatrices digitales. Du déchiffrage des formules logico-mathématiques par la machine même," PhD thesis, ETH Zürich (1951).
  - H. Rutishauser, "Automatische Rechenplanfertigung bei programmgesteuerten Rechenmaschinen," (1952).
