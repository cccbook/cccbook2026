# 1979：C with Classes 誕生——第一個「類別」

## 事件
1979 年，Bjarne Stroustrup 在貝爾實驗室以 C 為基礎開發 **C with Classes**（也稱「帶類別的 C」），這是 C++ 的前身。

## 關鍵語法/特性
- **class（類別）**：成員可分為 `private`/`public`，實現封裝。
- **建構子與解構子**：物件誕生與死亡時自動呼叫的函式。
- **呼叫／被呼叫函式的參數檢查**：函式宣告的完整型別檢查（C 當時可省略參數型別）。
- **friend 函式**：允許特定外部函式存取私有成員。

## 為何重要
- 這是「**在不犧牲 C 效率的前提下加入資料抽象**」的第一次嘗試——C++ 一生的設計主軸。
- 建構子/解構子成為後來 **RAII**（資源取得即初始化）的基礎：資源的生命週期與物件的生命週期绑在一起。

## 理論與實用原因
- **理論原因**：Simula 67 的類別概念（Stroustrup 在劍橋寫論文時用過 Simula，深受其啟發）＋ BCPL/C 的效率傳統。
- **實用原因**：Stroustrup 當時在開發分散式系統模擬器，需要 Simula 式的抽象，但 Simula 太慢、C 太難用——「兩者之間的語言」就是 C with Classes。

## 彌補了什麼缺陷
彌補了 C「無封裝、無抽象、全域變數與函式氾濫、大型專案難以模組化」的缺陷；也彌補了 Simula「抽象好但效能差」的缺陷。

## 程式範例

**舊寫法**：C 的 `struct` + 自由函式，資料與操作分離、毫無保護：

```c
/* C 寫法：任何程式碼都能直接改成員，忘記 free 就漏記憶體 */
struct Buffer {
    char *data;
    int   size;
};

void buffer_init(struct Buffer *b, int size) {
    b->data = malloc(size);
    b->size = size;
}

/* 呼叫端必須記得手動呼叫 buffer_free(b)，否則記憶體洩漏 */
void buffer_free(struct Buffer *b) {
    free(b->data);
}
```

**新寫法**：C with Classes 用 `class` 封裝 + 建構子/解構子（RAII 雛形）：

```cpp
class Buffer {
private:                 // 封裝：外部程式碼碰不到成員
    char *data;
    int   size;

public:
    Buffer(int n) {      // 建構子：物件誕生時自動取得資源
        data = new char[n];
        size = n;
    }
    ~Buffer() {          // 解構子：物件死亡時自動釋放資源
        delete[] data;
    }
    int get_size() { return size; }

    friend int peek(Buffer &b, int i);  // friend：允許特定函式存取私有成員
};

int peek(Buffer &b, int i) {
    return b.data[i];    // 因為是 friend，可以存取 private 成員
}
```

```cpp
int main() {
    Buffer b(100);       // 建構子自動取得資源
    // b.size = -1;      // 編譯錯誤：private 成員受保護（彌補 C 的無封裝缺陷）
    return 0;
}                        // 解構子自動釋放，不會忘記 free（RAII 雛形）
```

## 相關條目
- [1972-C語言問世](1972-C語言問世.md)
- [1983-C++命名與virtual函式](1983-C++命名與virtual函式.md)
