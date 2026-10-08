# 2008 - Android 以 Linux 為核心（口袋裡的 Unix）

## 案件摘要
2008 年 9 月 23 日，Google 發布 **Android 1.0**——以 **Linux 核心**為基礎的行動作業系統。
$$\text{Linux 核心（1991）} + \text{Java/Dalvik 虛擬機} + \text{Apache 授權} = \text{Android}.$$
**Unix 的思想第三次勝利**：從伺服器（Linux）、Mac（BSD）到手機（Android）——今天逾 70% 的智慧型手機跑著 Linux 核心，**Unix 後裔成為地球上最普及的作業系統**。

## 前因 -- 為什麼會有這個案子
- **Andy Rubin 的動機**：2003 年 Rubin 創辦 Android Inc.，2005 年被 Google 收購——目標是「開放的手機平台」，對抗封閉的 Symbian、Windows Mobile 與即將問世的 iPhone。
- **為何選 Linux 核心**：
  1. **免授權費**：GPL 核心零成本——手機廠商（往往毛利微薄）不用付 Unix 授權費。
  2. **硬體支援最廣**：Linux 核心支援最多的 ARM 晶片與驅動。
  3. **可修改**：GPL 允許廠商客製化（但必須開源核心部分）。
- **彌補的缺陷**：封閉行動 OS（Symbian/WM）的授權費與單一廠商綁定；Android 用 **Apache 授權（使用者空間）+ GPL（核心）** 的雙層授權解決——廠商可閉源客製使用者層，核心必須開源回饋。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：雙層授權的架構
$$\text{Android} = \underbrace{\text{Linux 核心（GPL，必須開源）}}_{\text{核心層}} + \underbrace{\text{使用者空間（Apache，可閉源）}}_{\text{廠商層}}.$$
- **彌補的缺陷**：純 GPL 會嚇跑商業廠商；純 BSD 式授權會讓核心修改不回饋——雙層授權取折衷。

### 第二條線索：Dalvik/ART 虛擬機
Android 不直接跑原生程式，而是用 **Java 語言 + Dalvik 虛擬機（後為 ART）**：
- **理論基礎**：**沙箱隔離**——每個 App 是一個獨立 uid 的行程，跑在 VM 中——一個 App 當掉不影響系統（與微核心的隔離思想殊途同歸）。
- **彌補的缺陷**：手機程式碼來源不可信——VM 提供記憶體安全與權限隔離。

### 第三條線索：Binder IPC
Android 用 **Binder**（OpenBinder 的移植）做行程間通訊：
- **彌補的缺陷**：Linux 傳統 IPC（pipe、socket、SysV IPC）對「物件導向的服務呼叫」太底層——Binder 提供**物件導向的 RPC**，是 Android 架構的脊樑。

### Java 範例：Android App 的沙箱與生命週期

```java
// Android (2008)：每個 App 是獨立 uid 的沙箱行程
public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Binder IPC：呼叫系統服務——物件導向的 RPC
        Vibrator v = (Vibrator) getSystemService(VIBRATOR_SERVICE);
        v.vibrate(100);
    }
}
```

### Shell 範例：Android 就是 Linux

```bash
# adb shell 進入手機——底下就是 Linux 核心
$ adb shell
$ uname -a
Linux localhost 4.14.83 ... aarch64
$ ps -A | head -5        # 每個 App 一個 uid
$ cat /proc/cpuinfo      # 一切皆檔案——1969 年 Unix 的遺產
```

### Python 範例：Binder 式 RPC 的抽象

```python
import xmlrpc.client

# Android Binder 的精神：遠端服務呼叫像本地物件
proxy = xmlrpc.client.ServerProxy("http://localhost:8000")
print(proxy.system.list_services())   # 物件導向的服務發現
```

## 結案 -- 後果與影響
- **手機的征服**：2010 年代 Android 市佔逾 70%——**Linux 核心成為地球上最廣泛部署的核心**（手機+伺服器+物聯網）。
- **GPL 的商業勝利**：證明 copyleft 授權可以承載全球最大規模的商業系統。
- **AOSP 生態**：開放原始碼手機平台 → 各廠商客製（MIUI、One UI）→ 生態多樣性。
- **核心的行動化改造**：wakelocks、low-memory killer、Binder——Linux 核心為行動裝置新增大量機制，反哺伺服器 Linux。
- 歷史教訓：**開放平台 + 雙層授權 = 生態爆炸**——Android 證明「開放」在消費市場也能打敗「封閉」。

## 關鍵人物與文獻
- **A. Rubin**：Android Inc. (2003)、Google 收購 (2005)、Android 1.0 (2008)。
- **Google**：Dalvik 虛擬機、Binder IPC。
- 相關案件：`1991-Linux誕生.md`、`1983-SystemV與GNU計畫.md`。
