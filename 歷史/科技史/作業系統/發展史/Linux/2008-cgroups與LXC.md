# 2008 - cgroups 與 LXC（容器的地基）

## 案件摘要
2008 年，**cgroups（control groups）進入 Linux 核心 2.6.24**，同年 **LXC（Linux Containers）0.1** 發布——
$$\text{cgroups（資源限制）} + \text{namespaces（隔離視野）} + \text{LXC（包裝）} = \text{容器的地基}.$$
**Docker（2013）的全部技術都在 2008 年就緒**——Docker 的功勞是把它們變成一個指令。

## 前因 -- 為什麼會有這個案子
- **Google 的需求**：Google 內部所有服務（包括搜尋）早已跑在「容器」裡（Borg 系統，2003–）——Google 工程師（Paul Menage 等）把 cgroups 貢獻給主線核心——**雲端巨頭的需求逼出核心機制**。
- **namespaces 的逐步積累**：2.4.19（2002）mount ns → 2.6.24（2008）PID/NET ns → 2.6.30（2009）IPC/USER ns——**六維隔離花了 7 年才齊備**。
- **彌補的缺陷**：Unix 傳統無法限制一群行程的資源（nice 只能調優先級、ulimit 只能限制單一行程）——cgroups 讓「**群組級資源配額**」成為一等公民。

## 線索與推理 -- 技術面貌（2008）

| 技術 | 狀態 | 版本年份脈絡 | 彌補的缺陷 |
|------|------|-------------|-----------|
| **cgroups** | 核心 2.6.24（2008.1） | Google 貢獻 | 無群組級資源配額 |
| **namespaces** | PID/NET 齊備 | 2.4.19（2002）起逐步 | chroot 只隔離檔案系統 |
| **LXC** | 0.1（2008.8） | liblxc + 工具 | chroot 太陽春 |
| **KVM** | 核心 2.6.20（2007.2） | 見 `2007-KVM虛擬化.md` | VMware 專閉源 |
| **ext4** | 穩定化中（2008.10 正式，2.6.28） | extent + 延遲分配 | ext3 的效能上限 |
| **GNOME/KDE** | GNOME 2.22、KDE 4.0 | 桌面成熟 | 桌面可用性 |

### Shell 範例：cgroups 的直接使用

```bash
# cgroup v1（2008）：手動掛載與限制
$ mount -t cgroup -o memory none /sys/fs/cgroup/memory
$ mkdir /sys/fs/cgroup/memory/mygroup
$ echo 500M > /sys/fs/cgroup/memory/mygroup/memory.limit_in_bytes
$ echo $$ > /sys/fs/cgroup/memory/mygroup/tasks   # 把自己加進群組
$ # 之後這個 shell 的所有行程記憶體上限 500M

# cgroup v2（2016 核心 4.6 正式）：統一階層
$ echo "+memory +cpu" > /sys/fs/cgroup/cgroup.subtree_control
$ systemd-run --scope -p MemoryMax=500M myjob    # systemd 整合（2014+）
```

### Python 範例：namespaces 的直接呼叫

```python
import os

# unshare（2008+）：建立新的 namespace——隔離視野
# CLONE_NEWPID: 新 PID namespace（容器有自己的 pid 1）
pid = os.fork()
if pid == 0:
    os.unshare(os.CLONE_NEWNS | os.CLONE_NEWPID)
    print("在新 namespace 中，pid:", os.getpid())
else:
    os.wait()
```

### C 範例：LXC 的本質——clone 帶 namespace 旗標

```c
/* LXC 風格：clone() + namespaces 旗標 = 容器的誕生 */
#define _GNU_SOURCE
#include <sched.h>
#include <sys/wait.h>

char child_stack[65536];

int child_main(void *arg) {
    /* 在新 PID/NET/MNT namespace 中執行 */
    execl("/bin/sh", "sh", NULL);
    return 0;
}

int main(void) {
    int flags = CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWNS;
    pid_t pid = clone(child_main, child_stack + 65536, flags, NULL);
    waitpid(pid, NULL, 0);
    return 0;
}
```

### Dockerfile 範例：2008 年的地基 + 2013 年的包裝

```bash
# 2008 年（LXC 时代）：手動設定
$ lxc-create -n mycontainer -t ubuntu
$ lxc-start -n mycontainer

# 2013 年（Docker 时代）：一個指令
$ docker run -it ubuntu bash    # 同樣的 clone+ns+cgroups，體驗天差地遠
```

## 結案 -- 後果與影響
- **Docker（2013）與 Kubernetes（2014）**：全部站在 cgroups/namespaces 的地基上——雲端原生時代。
- **systemd（2014）**：用 cgroups 做服務監督——cgroups 從容器反哺到 init 系統。
- **Android（2008）**：同時用 cgroups 做低記憶體管理（lmkd）。
- **cgroup v2（2016，核心 4.6）**：統一階層、修正 v1 的碎片化——**第一版設計的教訓反哺第二版**。
- 歷史教訓：**地基（核心機制）與包裝（Docker）是兩回事——但包裝決定普及**。

## 關鍵人物與文獻
- **P. Menage, P. Jackson（Google）**：cgroups (2008, 2.6.24)。
- **Linux 核心**：namespaces (2002–2009)。
- **D. Lezcano, S. Soltesz**：LXC、cgroup v2。
- 相關案件：`../UNIX/2013-Docker容器.md`、`2007-KVM虛擬化.md`。
