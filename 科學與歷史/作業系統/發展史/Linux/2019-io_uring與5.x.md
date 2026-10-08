# 2019 - io_uring 與 5.x 核心（非同步 I/O 的終極解法）

## 案件摘要
2019 年 5 月，**io_uring 進入 Linux 核心 5.1**（Jens Axboe）——
$$\text{io_uring} = \text{提交佇列（SQ）} + \text{完成佇列（CQ）} + \text{共享記憶體環}.$$
**非同步 I/O 的終極解法**——用兩個共享記憶體的環形佇列，把系統呼叫開銷降到接近零。

## 前因 -- 為什麼會有這個案子
- **歷代非同步 I/O 的缺陷**：
  1. **select/poll（1990s）**：O(n) 掃描、fd 上限 1024——**彌補的缺陷：規模天花板**。
  2. **epoll（2003，2.5.44/2.6）**：O(1) 事件通知——但仍**每次要系統呼叫**（epoll_wait）。
  3. **libaio（2006）**：只支援 O_DIRECT 檔案 I/O，網路/普通檔案都不行——**彌補的缺陷：支援範圍窄**。
- **NVMe SSD 的硬體契機**：2015 年代 NVMe SSD 的 IOPS 達百萬級——**每次 I/O 一次系統呼叫的開銷成為瓶頸**（系統呼叫比 I/O 本身還慢）。
- **理論基礎**：**生產者-消費者環形緩衝**——應用程式（生產者）與核心（消費者）透過**共享記憶體**通訊，不需系統呼叫——把「系統呼叫邊界」這個最後的效能牆拆掉。

## 線索與推理 -- 技術面貌（2019+）

| 技術 | 狀態 | 版本年份脈絡 | 彌補的缺陷 |
|------|------|-------------|-----------|
| **io_uring** | 核心 5.1（2019.5） | Axboe | libaio 支援窄、epoll 系統呼叫開銷 |
| **批次提交** | SQ 一次交多筆 I/O | 5.1 | 一次一筆的呼叫開銷 |
| **IORING_OP_POLL** | 非同步 poll | 5.1+ | epoll_wait 的阻塞 |
| **I/O 零拷貝** | send/recv with rings | 5.6（2020.3） | 資料在核心/使用者間拷貝 |
| **NVMe** | 原生支援 | 4.x 世代 | SATA 的佇列上限 |

### C 範例：io_uring 的環形佇列

```c
/* io_uring (2019)：共享記憶體的提交/完成環 */
#include <liburing.h>

int main(void) {
    struct io_uring ring;
    io_uring_queue_init(8, &ring, 0);        /* 深度 8 的環 */

    struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
    io_uring_prep_read(sqe, fd, buf, 4096, 0);  /* 提交讀取（不阻塞） */

    io_uring_submit(&ring);                   /* 批次提交（可多筆） */

    struct io_uring_cqe *cqe;
    io_uring_wait_cqe(&ring, &cqe);           /* 等完成佇列 */
    printf("讀取 %d bytes\n", cqe->res);
    io_uring_cqe_seen(&ring, cqe);
    io_uring_queue_exit(&ring);
}
```
（理論：SQE 提交、CQE 完成——**共享記憶體環**取代系統呼叫邊界，批次提交攤薄開銷。）

### C 範例：歷代 I/O 模型的對照

```c
/* 1990s: select——O(n) 掃描、fd 上限 1024 */
fd_set readfds;
select(maxfd + 1, &readfds, NULL, NULL, NULL);   /* 每次要重建集合 */

/* 2003: epoll——O(1) 事件，但仍要系統呼叫 */
int ep = epoll_create1(0);
epoll_ctl(ep, EPOLL_CTL_ADD, fd, &ev);
epoll_wait(ep, events, MAX, -1);                 /* 每次一個系統呼叫 */

/* 2019: io_uring——共享記憶體，可零系統呼叫（SQPOLL 模式） */
io_uring_prep_read(sqe, fd, buf, n, off);        /* 只寫共享記憶體 */
```

### Python 範例：非同步 I/O 的演化

```python
import selectors, socket

# 2003 模型：selectors（epoll 的封裝）
sel = selectors.DefaultSelector()
s = socket.socket()
sel.register(s, selectors.EVENT_READ)
for key, _ in sel.select():        # 每次一個系統呼叫
    data = key.fileobj.recv(1024)

# 2019 模型（io_uring 的精神）：批次、非同步、零拷貝
# Python 3.10+ 可用 liburing 綁定（example with uvloop-like speed）
```

### Shell 範例：效能的實證

```bash
# fio 效能測試：io_uring vs libaio（NVMe SSD 上）
$ fio --name=t --ioengine=io_uring --rw=read --bs=4k \
      --iodepth=32 --numjobs=1 --filename=/dev/nvme0n1
# io_uring：可達 100 萬+ IOPS，CPU 使用率更低
$ fio --name=t --ioengine=libaio --rw=read --bs=4k \
      --iodepth=32 --filename=/dev/nvme0n1
# libaio：IOPS 相近但 CPU 開銷高、不支援網路
```

## 結案 -- 後果與影響
- **高效能伺服器的新基礎**：Redis、PostgreSQL（2021 起實驗支援）、NGINX 陸續採用 io_uring——**非同步 I/O 的統一介面**。
- **網路與檔案的統一**：io_uring 同時支援檔案與 socket——**一切皆檔案**的 I/O 層完成（1969 年理想的 2019 年實現）。
- **零系統呼叫（SQPOLL）**：核心執行緒代為提交——**系統呼叫邊界**這道 50 年的牆被拆掉。
- **演化**：io_uring 5.1（2019）→ 5.6 零拷貝（2020）→ 6.0 世代支援 network zero-copy（2022+）。
- 歷史教訓：**當硬體快 100 倍，軟體的每次邊界開銷都成為瓶頸**——io_uring 是「共享記憶體通訊」對系統呼叫的勝利。

## 關鍵人物與文獻
- **J. Axboe**：io_uring (2019, 5.1)；〈Efficient IO with io_uring〉。
- **epoll 作者**：D. Probst / SGI 團隊 (2003)。
- 相關案件：`2003-2.6核心革命.md`、`2014-eBPF與systemd普及.md`。
