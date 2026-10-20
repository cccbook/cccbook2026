# 用 Rust 學 Linux 系統程式

一本以 Rust 為工具、以 Linux 系統程式為主軸的實作型教科書。全書貫穿兩條主線：一是 Rust 的所有權與型別系統如何在語言層面防止系統程式五十年來的記憶體與併發錯誤；二是從系統呼叫一路做到自製微型 Docker 的完整技術線。

## 目錄

* 第1章-Rust與系統程式基礎
    * [1.1-2015-Rust 1.0 與記憶體安全的系統語言之爭](01.1-2015-Rust1.0與記憶體安全的系統語言之爭.md)
    * [1.2-所有權、借用與生命週期](01.2-所有權借用與生命週期.md)
    * [1.3-cargo生態系與unsafe的邊界](01.3-cargo生態系與unsafe的邊界.md)
* 第2章-Linux系統呼叫與程序
    * [2.1-系統呼叫與libc crate](02.1-系統呼叫與libc-crate.md)
    * [2.2-訊號處理與signal-hook](02.2-訊號處理與signal-hook.md)
    * [2.3-管線檔案描述器與std-os-unix-io](02.3-管線檔案描述器與std-os-unix-io.md)
* 第3章-併發與非同步
    * [3.1-執行緒Mutex與Send-Sync型別系統保證](03.1-執行緒Mutex與Send-Sync型別系統保證.md)
    * [3.2-epoll與事件迴圈](03.2-epoll與事件迴圈.md)
    * [3.3-async-await與tokio的原理](03.3-async-await與tokio的原理.md)
* 第4章-網路程式與IPC
    * [4.1-socket程式設計](04.1-socket程式設計.md)
    * [4.2-UnixDomainSocket與共享記憶體](04.2-UnixDomainSocket與共享記憶體.md)
    * [4.3-HTTP伺服器實作](04.3-HTTP伺服器實作.md)
* 第5章-自製微型Docker
    * [5.1-容器技術史：chroot到Docker](05.1-容器技術史chroot到Docker.md)
    * [5.2-用Rust實作容器隔離：namespace](05.2-用Rust實作容器隔離namespace.md)
    * [5.3-cgroups與overlayfs與微型容器執行器](05.3-cgroups-overlayfs與微型容器執行器.md)

## 環境需求

- Linux（本書大量使用 `clone`、`epoll`、`cgroups` 等 Linux 專屬功能）
- Rust 1.75 以上（`rustup update stable`）
- root 權限（第 5 章實驗需要）

## 學習路線建議

```mermaid
graph LR
    A[第1章 語言基礎] --> B[第2章 系統呼叫]
    B --> C[第3章 併發]
    C --> D[第4章 網路]
    D --> E[第5章 mini-docker]
```

每一節的程式碼都可以直接放進一個 `cargo new` 出來的專案編譯執行。建議讀者邊讀邊打，遇到編譯錯誤時，把 Rustc 的錯誤訊息當作老師——它是本書最重要的助教。
