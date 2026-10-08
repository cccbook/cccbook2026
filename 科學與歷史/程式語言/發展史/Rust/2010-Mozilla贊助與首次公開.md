# 2010：Mozilla 贊助與首次公開——自舉之路開始

## 事件
2010 年，Mozilla 正式贊助 Rust 專案並**首次公開發佈**。同年，Mozilla 宣佈以 Rust 打造實驗性瀏覽器引擎 **Servo**，作為語言的「第一個大型試煉場」。Rust 編譯器也開始**自舉（self-hosting）**：放棄原本的 OCaml 版編譯器，改用 Rust 寫 Rust 編譯器。

## 為何重要
- **Mozilla 的動機**：Firefox 與 IE、Chrome 的競爭中，瀏覽器是世界上最複雜的 C++ 軟體之一，當機與安全漏洞不斷。Mozilla 需要「並行、安全的下一代引擎」，Servo + Rust 是答案。
- **自舉的意義**：「吃自己的狗糧」——編譯器本身成為最大的 Rust 程式，語言缺陷會最先在編譯器開發中暴露並修正。
- Servo 的平行渲染架構，迫使 Rust 認真處理**無資料競爭（data-race-free）的並行**，這直接催生了後來的 `Send`/`Sync` trait。

## 理論與實用原因
- **理論原因**：借用檢查器的理論核心「Fearless Concurrency」來自型別系統文獻中的 region-based type systems 與 effect systems——把「借用」和「壽命」當成型別系統的一部分來檢查。
- **實用原因**：OCaml 寫的早期編譯器效能與維護性不足；自舉讓編譯器開發者與語言使用者是同一群人，回饋迴路最短。

## 程式範例

**C++ 的資料競爭**——兩個執行緒同時修改同一資料，編譯器無從檢查：

```cpp
#include <thread>
int counter = 0;            // 共享可變狀態，沒有任何保護
void increment() { for (int i = 0; i < 100000; i++) counter++; }
int main() {
    std::thread t1(increment), t2(increment);
    t1.join(); t2.join();
    // counter 可能不是 200000——資料競爭是未定義行為
}
```

**Rust 的解法**——`Send`/`Sync` 讓「跨執行緒共享」在編譯期被檢查：

```rust
use std::thread;

fn main() {
    // 直接在多個執行緒借用可變資料：編譯錯誤
    // let mut counter = 0;
    // thread::spawn(|| counter += 1);  // closure may outlive borrowed value

    // 正確做法：Mutex 保護共享狀態，Arc 跨執行緒共享所有權
    let counter = std::sync::Arc::new(std::sync::Mutex::new(0u64));
    let handles: Vec<_> = (0..2).map(|_| {
        let c = counter.clone();
        thread::spawn(move || {
            for _ in 0..100_000 { *c.lock().unwrap() += 1; }
        })
    }).collect();
    for h in handles { h.join().unwrap(); }
    println!("{}", *counter.lock().unwrap());  // 一定是 200000
}
```

這正是 Servo 需要的能力：**平行渲染的瀏覽器引擎，資料競爭在編譯期就被消滅**——C++ 做不到，Java/Go 靠執行期檢查（或根本不檢查），Rust 靠型別系統。

## 彌補了什麼缺陷
彌補了 Mozilla「瀏覽器引擎的並行化在 C++ 中幾乎不可能安全完成」的缺陷——C++ 的資料競爭是未定義行為，編譯器無從檢查；Rust 讓「並行程式在編譯期就被證明沒有資料競爭」成為可能。

## 相關條目
- [2006-GraydonHoare的個人專案](2006-GraydonHoare的個人專案.md)
- [2012-rustpkg與自舉之路](2012-rustpkg與自舉之路.md)
