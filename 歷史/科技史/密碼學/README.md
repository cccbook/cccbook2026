# 密碼學史 -- AI 偵探風格

以「推理探案」的方式，追查密碼學從 Caesar 密碼到零知識證明與後量子密碼的每一步：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個數位世界？

密碼學的核心信念是：**秘密可以數學化**——保密不再是「藏得更好」，而是「即使敵人看到全部演算法，沒有金鑰就解不開」。

## 案件卷宗（歷史年表）

### 序幕：古典密碼與戰時破譯（西元前 50–1949）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 前 50 | Caesar 密碼：最早的替換密碼 | [-0050-Caesar密碼.md](-0050-Caesar密碼.md) |
| 1550 | Vigenère 密碼：「不可破譯」的密碼與其被破 | [1550-Vigenere密碼.md](1550-Vigenere密碼.md) |
| 1883 | Kerckhoffs 原則：保密在金鑰，不在演算法 | [1883-Kerckhoffs原則.md](1883-Kerckhoffs原則.md) |
| 1918 | Enigma 機：轉子密碼機的誕生 | [1918-Enigma機.md](1918-Enigma機.md) |
| 1932 | Rejewski 破譯 Enigma：數學擊敗機器 | [1932-Rejewski破譯Enigma.md](1932-Rejewski破譯Enigma.md) |
| 1939–1944 | Bletchley Park 與 Turing 炸彈機：Ultra 情報改變二戰 | [1939-BletchleyPark.md](1939-BletchleyPark.md) |
| 1949 | Shannon 保密系統理論：密碼學成為數學 | [1949-Shannon保密理論.md](1949-Shannon保密理論.md) |

### 現代密碼學的誕生（1970–1977）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1970 | IBM 的 Lucifer：對稱區塊密碼的雛形 | [1970-Lucifer.md](1970-Lucifer.md) |
| 1974 | Diffie–Hellman 與公鑰構想的誕生 | [1974-Diffie公鑰構想.md](1974-Diffie公鑰構想.md) |
| 1976 | Diffie–Hellman 金鑰交換：公鑰密碼學問世 | [1976-DiffieHellman金鑰交換.md](1976-DiffieHellman金鑰交換.md) |
| 1977 | RSA：公鑰加密的完整實現 | [1977-RSA.md](1977-RSA.md) |
| 1977 | DES 標準化：對稱加密的國家標準 | [1977-DES.md](1977-DES.md) |

### 現代密碼學的成熟（1979–2000）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1979 | Merkle–Hellman 背包密碼與其被破 | [1979-MerkleHellman背包密碼.md](1979-MerkleHellman背包密碼.md) |
| 1979 | Shamir 秘密分享：秘密拆成 n 片，k 片才能重組 | [1979-Shamir秘密分享.md](1979-Shamir秘密分享.md) |
| 1979 | Carter–Wegman 通用雜湊與訊息認證碼 | [1979-CarterWegman通用雜湊.md](1979-CarterWegman通用雜湊.md) |
| 1985 | ElGamal：離散對數加密與數位簽章 | [1985-ElGamal.md](1985-ElGamal.md) |
| 1985 | RSA 指紋 vs 隨機化：雜湊函數與 MD 系列 | [1985-密碼學雜湊函數.md](1985-密碼學雜湊函數.md) |
| 1989 | 零知識證明：證明我知道，但不告訴你 | [1989-零知識證明.md](1989-零知識證明.md) |
| 1994 | Shor 演算法：量子電腦威脅 RSA 與 ElGamal | [1994-Shor演算法.md](1994-Shor演算法.md) |
| 1998 | SSL/TLS 與網路加密的普及 | [1998-SSL與網路加密.md](1998-SSL與網路加密.md) |

### 現代密碼學（2001–至今）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2001 | AES 標準化：DES 的繼任者 | [2001-AES.md](2001-AES.md) |
| 2002 | AKS 質數檢驗（交叉參照計算理論史） | [../計算理論/2002-AKS質數檢驗.md](../計算理論/2002-AKS質數檢驗.md) |
| 2005 | 橢圓曲線密碼學（ECC）標準化與普及 | [2005-橢圓曲線密碼學.md](2005-橢圓曲線密碼學.md) |
| 2009 | 全同態加密：在密文上直接計算 | [2009-全同態加密.md](2009-全同態加密.md) |
| 2016 | 區塊鏈與比特幣的密碼學基礎設施 | [2016-區塊鏈密碼學.md](2016-區塊鏈密碼學.md) |
| 2017 | 後量子密碼學：NIST 標準化競賽 | [2017-後量子密碼學.md](2017-後量子密碼學.md) |
| 2022 | LLM 時代的密碼學：從訓練到推理的保密 | [2022-LLM時代密碼學.md](2022-LLM時代密碼學.md) |

## 關鍵人物年表

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 前 50 | Julius Caesar | Caesar 密碼 |
| 1550 | Blaise de Vigenère | Vigenère 密碼 |
| 1883 | Auguste Kerckhoffs | Kerckhoffs 原則 |
| 1918 | Arthur Scherbius | Enigma 機 |
| 1932 | Marian Rejewski | 數學破譯 Enigma |
| 1939–1944 | Alan Turing / Gordon Welchman | 炸彈機、Ultra 情報 |
| 1949 | Claude Shannon | 保密系統理論 |
| 1970 | Horst Feistel | Lucifer / Feistel 結構 |
| 1976 | Whitfield Diffie / Martin Hellman | 公鑰密碼學、金鑰交換 |
| 1977 | Ron Rivest / Adi Shamir / Len Adleman | RSA |
| 1979 | Adi Shamir | 秘密分享 |
| 1979 | Carter / Wegman | 通用雜湊、MAC |
| 1985 | Taher ElGamal | ElGamal 加密/簽章 |
| 1989 | Goldwasser / Micali / Rackoff | 零知識證明 |
| 1994 | Peter Shor | Shor 演算法 |
| 1998 | Netscape / IETF | SSL/TLS |
| 2001 | Vincent Rijmen / Joan Daemen | AES |
| 2005 | Neal Koblitz / Victor Miller | 橢圓曲線密碼學 |
| 2009 | Craig Gentry | 全同態加密 |
| 2017 | NIST | 後量子密碼學標準化 |

## 核心概念速查

### 對稱 vs 非對稱加密

| 類型 | 金鑰 | 速度 | 代表 |
|------|------|------|------|
| 對稱 | 加解密同一把 | 快（GB/s） | AES、ChaCha20 |
| 非對稱 | 公鑰加密、私鑰解密 | 慢（KB/s） | RSA、ECC |
| 雜湊 | 無金鑰（單向） | 快 | SHA-256 |

### 難解問題與密碼學

| 問題 | 支撐的密碼系統 | 量子威脅 |
|------|----------------|----------|
| 大數分解 | RSA | Shor 演算法（1994） |
| 離散對數 | Diffie–Hellman、ElGamal | Shor 演算法 |
| 格問題（LWE/SVP） | 後量子密碼 | 未知有效攻擊 |
| 雜湊抗碰撞 | 簽章、區塊鏈 | Grover 演算法（平方加速） |

### 交錯參照
- 計算理論史：[../計算理論/README.md](../計算理論/README.md)
- 隨機算法史（PRG、Miller–Rabin）：[../隨機算法/README.md](../隨機算法/README.md)
- 機率統計史：[../機率統計/README.md](../機率統計/README.md)
