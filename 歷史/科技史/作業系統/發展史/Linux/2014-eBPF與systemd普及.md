# 2014 - eBPF 與 systemd 普及（核心的可程式化革命）

## 案件摘要
2014 年，兩件大事代表 Linux 的現代演進：
1. **eBPF（extended Berkeley Packet Filter）** 進入核心 3.18——核心第一次變成**安全可程式化**的 VM。
2. **systemd 進入 Debian 8 / RHEL 7**——init 系統的世代交替完成。
$$\text{eBPF（核心可程式化）} + \text{systemd（服務管理現代化）} = \text{Linux 的現代化革命}.$$

## 前因 -- 為什麼會有這個案子
- **BPF 的演化**：經典 BPF（1992，McCanne/Jacobson）只是封包過濾器——**彌補的缺陷：核心觀察與擴展要寫核心模組（有當機風險）**。Alexei Starovoitov 的 **eBPF（2014，3.18）**把 BPF 升級為通用 VM：**驗證器（verifier）保證程式不會當機**。
- **systemd 的戰場**：2014 年 Debian 8、RHEL 7 正式採用——**彌補的缺陷**：SysV init 的序列啟動、不監督服務（見 `../UNIX/2014-systemd與WSL.md`）。
- **理論基礎**：eBPF 的驗證器是**形式化驗證**的實踐——程式載入前逐一模擬所有執行路徑，證明「不越界、不無限迴圈、不當機」。

## 線索與推理 -- 技術面貌（2014）

| 技術 | 狀態 | 版本年份脈絡 | 彌補的缺陷 |
|------|------|-------------|-----------|
| **eBPF** | 核心 3.18（2014.12） | 經典 BPF（1992）的升級 | 核心模組的當機風險 |
| **kprobes/tracepoints** | eBPF 掛鉤點 | 觀察核心 | 寫模組才能觀察 |
| **systemd** | RHEL 7 / Debian 8 | 2010 開發、2014 普及 | SysV init 序列啟動 |
| **Docker 1.0** | 2014.7（生產就緒宣告） | 2013 誕生 | 部署不一致 |
| **Kubernetes 1.0** | 2015.7 | 2014.6 開源 | 容器編排缺位 |
| **cgroup v2 開發** | 2014–16 | 核心 4.6（2016）正式 | v1 碎片化 |

### C 範例：eBPF 的驗證器與載入

```c
/* eBPF (2014)：程式載入前被驗證器檢查——安全可程式化 */
#include <linux/bpf.h>
#include <sys/syscall.h>

char license[] = "GPL";
struct bpf_insn prog[] = {
    /* r0 = 0; exit —— 最小的合法 eBPF 程式 */
    { BPF_ALU64 | BPF_MOV | BPF_K, BPF_R0, 0, 0, 0 },
    { BPF_JMP | BPF_EXIT, 0, 0, 0, 0 },
};

union bpf_attr attr = {
    .prog_type = BPF_PROG_TYPE_KPROBE,
    .insns = (unsigned long)prog,
    .insn_cnt = sizeof(prog) / sizeof(prog[0]),
    .license = (unsigned long)license,
};
int fd = syscall(SYS_bpf, BPF_PROG_LOAD, &attr, sizeof(attr));
/* 驗證器模擬所有路徑：越界/無限迴圈直接拒載——不會當機 */
```

### Shell 範例：eBPF 的觀察革命（bpftrace）

```bash
# 2014 之前：觀察系統呼叫要寫核心模組（有當機風險）
# 2014 之後（bpftrace, 2018）：一行式觀察
$ bpftrace -e 'tracepoint:syscalls:sys_enter_openat { @[comm] = count(); }'
Attaching 1 probe...
^C
@[bash]: 45
@[python3]: 128      # 每個程式開了多少檔案——零風險觀察核心

# execsnoop：誰在啟動行程
$ execsnoop
PCOMM   PID    PPID ARGS
curl    12345  6789 curl https://example.com
```

### Python 範例：eBPF 的 Python 介面（bcc）

```python
from bcc import BPF

# bcc (2015)：用 Python 寫 eBPF 觀察程式
prog = r"""
int hello(void *ctx) {
    bpf_trace_printk("hello from kernel\n");
    return 0;
}
"""
b = BPF(text=prog)
b.attach_kprobe(event=b.get_syscall_fnname("clone"), fn_name="hello")
print(b.trace_fields())   # 觀察所有行程的誕生——不寫模組、不當機
```

### systemd 範例：世代交替完成（2014）

```bash
# 2014 年：RHEL 7 / Debian 8 正式採用 systemd
$ systemctl start nginx      # 取代 /etc/init.d/nginx start
$ systemctl enable nginx     # 開機自啟
$ systemctl status nginx     # cgroups 監督 + 當機重啟
```

## 結案 -- 後果與影響
- **eBPF 的爆發**：Cilium（2017，網路安全）、Falco（2016，安全監控）、bpftrace（2018）——**核心觀察/網路/安全的通用平台**；2021 年 eBPF 成為 Linux Foundation 獨立專案。
- **systemd 的爭議與普及**：Unix 哲學派批評其龐大，但 2020 年代所有主流發行版都是 systemd。
- **可程式化核心的時代**：eBPF 證明核心可以「不重編譯、不重開機、不當機」地擴展——**動態擴展 vs 靜態編譯的大轉向**。
- 歷史教訓：**驗證器（形式化驗證）讓「核心可程式化」從夢想變成現實**——eBPF 是 2010 年代 Linux 最重要的創新。

## 關鍵人物與文獻
- **A. Starovoitov, D. Borkmann**：eBPF (2014, 3.18)。
- **L. Poettering**：systemd 普及 (2014)。
- **B. Gregg**：bpftrace (2018)、效能觀察聖經。
- 相關案件：`../UNIX/2014-systemd與WSL.md`、`2008-cgroups與LXC.md`。
