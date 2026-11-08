這是一本為全面探討「控制模型（Control Models）」**從經典理論一路推進至現代神經網路控制、自動駕駛、先進機器人學與遊戲模擬世界所規劃的**擴充版專書目錄。

根據您的指示，前八章維持嚴密的經典與現代控制理論基底，並**自第九章起進行大幅擴充與深化**，聚焦於神經網路動態模型、端到端自動駕駛、人形與四足機器人全身控制，以及基於遊戲引擎與世界模型的虛擬模擬生態系。本書目錄嚴格遵循 GitHub Markdown 標準，數學公式前後皆保留空格。

---

# README.md 目錄結構

* 第1章-經典控制理論的黃金時代：回授與頻域分析（19世紀末至20世紀中葉）
* [1.1-19世紀末-回授機制（Feedback）的數學根源與穩定性判據](https://www.google.com/search?q=1.1-%E5%9B%9E%E6%8E%88%E6%A9%9F%E5%88%B6%E7%9A%84%E6%95%B8%E5%AD%B8%E6%A0%B9%E6%BA%90%E8%88%87%E7%A9%A9%E5%AE%9A%E6%80%A7%E5%88%A4%E6%93%9A.md)
* [1.2-1940年代-傳遞函數（Transfer Functions）與拉普拉斯變換](https://www.google.com/search?q=1.2-%E5%82%B3%E9%81%9E%E5%87%BD%E6%95%B8%E8%88%87%E6%8B%89%E6%99%AE%E6%8B%89%E6%96%AF%E8%AE%8A%E6%8F%9B.md)
* [1.3-1950年代-頻域分析：根軌跡法與伯德圖（Bode Plots）](https://www.google.com/search?q=1.3-%E9%A0%BB%E5%9F%9F%E5%88%86%E6%9E%90%E6%A0%B9%E8%BB%8C%E8%B7%A1%E6%B3%95%E8%88%87%E4%BC%AF%E5%BE%B7%E5%9C%96.md)
* [1.4-1950年代-PID 控制器的閉環設計與調參哲學](https://www.google.com/search?q=1.4-PID%E6%8E%A7%E5%88%B6%E5%99%A8%E7%9A%84%E9%96%89%E7%92%B0%E8%A8%AD%E8%A8%88%E8%88%87%E8%AA%BF%E5%8F%83%E5%93%B2%E5%AD%B8.md)


* 第2章-現代控制理論：狀態空間法與能控能觀性（1960至1970年代）
* [2.1-1960年代-從外部輸入輸出到內部狀態空間（State-Space）的典範轉移](https://www.google.com/search?q=2.1-%E7%8B%80%E6%85%8B%E7%A9%BA%E9%96%93%E7%9A%84%E5%85%B8%E7%AF%84%E8%BD%89%E7%A7%BB.md)
* [2.2-1960年代-線性系統的能控性（Controllability）與能觀性（Observability）矩陣](https://www.google.com/search?q=2.2-%E8%83%BD%E6%8E%A7%E6%80%A7%E8%88%87%E8%83%BD%E8%A7%80%E6%80%A7%E7%9F%A9%E9%99%A3.md)
* [2.3-1960年代-極點配置（Pole Placement）與全狀態回授調節器](https://www.google.com/search?q=2.3-%E6%A5%B5%E9%BB%9E%E9%85%8D%E7%BD%AE%E8%88%87%E5%85%A8%E7%8B%80%E6%85%8B%E5%9B%9E%E6%8E%88%E8%AA%BF%E7%AF%80%E5%99%A8.md)


* 第3章-最佳控制與卡爾曼濾波：面對不確定性的估計（1960至1980年代）
* [3.1-1960年代-最優控制（Optimal Control）與黎卡提方程（Riccati Equation）](https://www.google.com/search?q=3.1-%E6%9C%80%E5%84%AA%E6%8E%A7%E5%88%B6%E8%88%87%E9%BB%8E%E5%8D%A1%E6%8F%90%E6%96%B9%E7%A8%8B.md)
* [3.2-1960年代-線性 quadratic 調整器（LQR）的數學推導與實務應用](https://www.google.com/search?q=3.2-%E7%B7%9A%E6%80%A7quadratic%E8%AA%BF%E6%95%B4%E5%99%A8LQR.md)
* [3.3-1960年代-貝氏估計的巔峰：卡爾曼濾波（Kalman Filter）與雜訊抑制](https://www.google.com/search?q=3.3-%E5%8D%A1%E7%88%BE%E6%9B%BC%E6%BF%BE%E6%B3%A2%E8%88%87%E9%9B%9C%E8%A8%8A%E6%8A%91%E5%88%B6.md)


* 第4章-非線性控制、適應性與強健控制（1980至2000年代）
* [4.1-1980年代-Lyapunov 穩定性理論：能量觀點下的非線性系統穩定分析](https://www.google.com/search?q=4.1-Lyapunov%E7%A9%A9%E5%AE%9A%E6%80%A7%E7%90%86%E8%AB%96.md)
* [4.2-1980年代-適應性控制（Adaptive Control）：應對未知參數與系統辨識](https://www.google.com/search?q=4.2-%E9%81%A9%E6%87%89%E6%80%A7%E6%8E%A7%E5%88%B6%E8%88%87%E6%9C%AA%E7%9F%A5%E5%8F%83%E6%95%B8%E8%BE%A8%E8%AD%98.md)
* [4.3-1990年代-強健控制（Robust Control）與 $H_\infty$ 迴圈塑造](https://www.google.com/search?q=4.3-%E5%BC%B7%E5%81%A5%E6%8E%A7%E5%88%B6%E8%88%87H%E6%97%A0%E7%A9%B7%E8%BF%B4%E5%9C%88%E5%A1%91%E9%80%A0.md)


* 第5章-約束最佳化與模型預測控制（MPC）（1990至2010年代）
* [5.1-1990年代-模型預測控制（Model Predictive Control, MPC）的核心思想與滾動優化](https://www.google.com/search?q=5.1-%E6%A8%A1%E5%9E%8B%E9%A0%90%E6%B8%AC%E6%8E%A7%E5%88%B6%E6%A0%B8%E5%BF%83%E6%80%9D%E6%83%B3%E8%88%87%E6%BB%BE%E5%8B%95%E5%84%AA%E5%8C%96.md)
* [5.2-2000年代-有限視界最佳化問題與約束條件處理（State & Input Constraints）](https://www.google.com/search?q=5.2-%E6%9C%89%E9%99%90%E8%A6%96%E7%95%8C%E6%9C%80%E4%BD%B3%E5%8C%96%E8%88%87%E7%B4%84%E6%9D%9F%E6%A2%9D%E4%BB%B6%E8%99%95%E7%90%86.md)
* [5.3-2010年代-顯式 MPC（Explicit MPC）與即時優化求解器（QP Solvers）](https://www.google.com/search?q=5.3-%E9%A1%AF%E5%BC%8FMPC%E8%88%87%E5%8D%B3%E6%99%82%E5%84%AA%E5%8C%96%E6%B1%82%E8%A7%A3%E5%99%A8.md)


* 第6章-資料驅動控制與強化學習的交匯（2010至2020年代）
* [6.1-2010年代-系統識別（System Identification）與Koopman算子理論](https://www.google.com/search?q=6.1-%E7%B3%BB%E7%B5%B1%E8%AD%98%E5%88%A5%E8%88%87Koopman%E7%AE%97%E5%AD%90%E7%90%86%E8%AB%96.md)
* [6.2-2010年代-無模型強化學習（Model-Free RL）：Q-learning 與策略梯度在控制中的限制](https://www.google.com/search?q=6.2-%E7%84%A1%E6%A8%A1%E5%9E%8B%E5%BC%B7%E5%8C%96%E5%AD%B8%E7%BF%92%E5%9C%A8%E6%8E%A7%E5%88%B6%E4%B8%AD%E7%9A%84%E9%99%90%E5%88%B6.md)
* [6.3-2020年代-模型基底強化學習（Model-Based RL）與神經網路控制函數](https://www.google.com/search?q=6.3-%E6%A8%A1%E5%9E%8B%E5%9F%BA%E5%BA%95%E5%BC%B7%E5%8C%96%E5%AD%B8%E7%BF%92%E8%88%87%E7%A5%9E%E7%B6%93%E7%B6%B2%E8%B7%AF%E6%8E%A7%E5%88%B6.md)


* 第7章-機器人學的基礎運動學與動力學建模
* [7.1-機械臂的正逆運動學（Forward & Inverse Kinematics）與雅可比矩陣](https://www.google.com/search?q=7.1-%E6%A9%9F%E6%A2%B0%E8%87%82%E6%AD%A3%E9%80%86%E9%81%8B%E5%8B%95%E5%AD%B8%E8%88%87%E9%9B%85%E5%8F%AF%E6%AF%94%E7%9F%A9%E9%99%A3.md)
* [7.2-Lagrange 與 Euler-Newton 動力學建模：迴轉矩、科氏力與重力補償](https://www.google.com/search?q=7.2-Lagrange%E8%88%87Euler-Newton%E5%8B%95%E5%8A%9B%E5%AD%B8%E5%BB%BA%E6%A8%A1.md)
* [7.3-操作臂的任務空間與聯合空間阻抗控制（Impedance Control）](https://www.google.com/search?q=7.3-%E6%93%8D%E4%BD%9C%E8%87%82%E4%BB%BB%E5%8B%99%E8%88%87%E8%81%AF%E5%90%88%E7%A9%BA%E9%96%93%E9%98%BB%E6%8A%97%E6%8E%A7%E5%88%B6.md)


* 第8章-傳統自動駕駛與行動載具的運動學控制
* [8.1-車輛動力學模型：單軌模型（Bicycle Model）與非完整約束](https://www.google.com/search?q=8.1-%E8%BB%8A%E8%BC%9B%E5%8B%95%E5%8A%9B%E5%AD%B8%E5%96%AE%E8%BB%8C%E6%A8%A1%E5%9E%8B%E8%88%87%E9%9D%9E%E5%AE%8C%E6%95%B4%E7%B4%84%E6%9D%9F.md)
* [8.2-幾何追蹤控制：純追蹤演算法（Pure Pursuit）與 Stanley 控制器](https://www.google.com/search?q=8.2-%E5%B9%BE%E4%BD%95%E8%BF%BD%E8%B9%A4%E6%8E%A7%E5%88%B6%E7%B4%94%E8%BF%BD%E8%B9%A4%E8%88%87Stanley%E6%8E%A7%E5%88%B6%E5%99%A8.md)
* [8.3-低速與高速行車下的路徑規劃與回授迴圈設計](https://www.google.com/search?q=8.3-%E4%BD%8E%E9%80%9F%E8%88%87%E9%AB%98%E9%80%9F%E8%A1%8C%E8%BB%8A%E4%B8%8B%E7%9A%84%E8%B7%AF%E5%BE%91%E8%A6%8F%E5%8A%83%E8%88%87%E5%9B%9E%E6%8E%88%E8%BF%B4%E5%9C%88%E8%A8%AD%E8%A8%88.md)


* 第9章-現代神經網路的控制模型與深度強化學習架構（2020至2026年）
* [9.1-神經網路作為動態系統：神經常微分方程（Neural ODEs）與連續時間控制](https://www.google.com/search?q=9.1-%E7%A5%9E%E7%B6%93%E5%B8%B8%E5%BE%AE%E5%88%86%E6%96%B9%E7%A8%8B%E8%88%87%E9%80%A3%E7%BA%8C%E6%99%82%E9%96%93%E6%8E%A7%E5%88%B6.md)
* [9.2-深度模型基底強化學習（MBRL）：DreamerV1-V3 與潛在空間控制迴圈](https://www.google.com/search?q=9.2-%E6%B7%B1%E5%BA%A6%E6%A8%A1%E5%9E%8B%E5%9F%BA%E5%BA%95%E5%BC%B7%E5%8C%96%E5%AD%B8%E7%BF%92Dreamer%E8%88%87%E6%BD%9B%E5%9C%A8%E7%A9%BA%E9%96%93%E6%8E%A7%E5%88%B6.md)
* [9.3-物理感知神經網路（PINN）在控制系統辨識與微分物理中的應用](https://www.google.com/search?q=9.3-%E7%89%A9%E7%90%86%E6%84%9F%E7%9F%A5%E7%A5%9E%E7%B6%93%E7%B6%B2%E8%B7%AF%E8%88%87%E5%BE%AE%E5%88%86%E7%89%A9%E7%90%86%E7%B3%BB%E7%B5%B1%E8%BE%A8%E8%AD%98.md)
* [9.4-Transformer架構在時序控制與多模態決策序列中的突破](https://www.google.com/search?q=9.4-%E8%AE%8A%E5%A3%93%E5%99%A8%E6%9E%B6%E6%A7%8B%E5%9C%A8%E6%99%82%E5%BA%8F%E6%8E%A7%E5%88%B6%E8%88%87%E5%A4%9A%E6%A8%A1%E6%85%8B%E6%B1%BA%E7%AD%96%E4%B8%AD%E7%9A%84%E7%AA%81%E7%A0%B4.md)


* 第10章-自動駕駛的現代神經控制與端到端架構（2023至2026年）
* [10.1-模組化自動駕駛控制與端到端（End-to-End）神經控制策略的典範轉移](https://www.google.com/search?q=10.1-%E6%A8%A1%E7%B5%84%E5%8C%96%E8%87%AA%E5%8B%95%E9%A7%95%E9%A7%9B%E8%88%87%E7%AB%AF%E5%88%B0%E7%AB%AF%E7%A5%9E%E7%B6%93%E6%8E%A7%E5%88%B6%E7%AD%96%E7%95%A5.md)
* [10.2-視覺-語言-動作模型（VLA）在複雜路況決策與導航中的控制應用](https://www.google.com/search?q=10.2-%E8%A6%96%E8%A6%BA%E8%AA%9E%E8%A8%80%E5%8B%95%E4%BD%9C%E6%A8%A1%E5%9E%8BVLA%E5%9C%A8%E8%A4%87%E9%9B%9C%E8%B7%AF%E6%B3%81%E6%B1%BA%E7%AD%96%E4%B8%AD%E7%9A%84%E6%87%89%E7%94%A8.md)
* [10.3-基於神經網路的預測性模型預測控制（Neural MPC）與即時軌跡優化](https://www.google.com/search?q=10.3-%E5%9F%BA%E6%96%BC%E7%A5%9E%E7%B6%93%E7%B6%B2%E8%B7%AF%E7%9A%84%E9%A0%90%E6%B8%AC%E6%80%A7%E6%A8%A1%E5%9E%8B%E9%A0%90%E6%B8%AC%E6%8E%A7%E5%88%B6NeuralMPC.md)
* [10.4-高動態駕駛安全防護：結合神經控制與控制屏障函數（CBF）的防撞保障](https://www.google.com/search?q=10.4-%E7%B5%90%E5%90%88%E7%A5%9E%E7%B6%93%E6%8E%A7%E5%88%B6%E8%88%87%E6%8E%A7%E5%88%B6%E5%B1%8F%E9%9A%9C%E5%87%BD%E6%95%B8CBF%E7%9A%84%E9%98%B2%E6%92%9E%E4%BF%9D%E9%9A%9C.md)


* 第11章-先進機器人學：人形、四足與多自由度動態平衡控制（2023至2026年）
* [11.1-步行機器的簡化物理模型：倒單擺模型（LIPM）與質心動力學擴展](https://www.google.com/search?q=11.1-%E6%AD%A5%E8%A1%8C%E6%A9%9F%E6%A2%B0%E7%B0%A1%E5%8C%96%E7%89%A9%E7%90%86%E6%A8%A1%E5%9E%8B%E8%88%87%E5%80%92%E5%96%AE%E6%93%BA%E6%93%B4%E5%B1%95.md)
* [11.2-四足與人形機器人的深度強化學習 locomotion（如 Unitree / Boston Dynamics 策略）](https://www.google.com/search?q=11.2-%E5%9B%9B%E8%B6%B3%E8%88%87%E4%BA%BA%E5%BD%A2%E6%A9%9F%E5%99%A8%E4%BA%BA%E6%B7%B1%E5%BA%A6%E5%BC%B7%E5%8C%96%E5%AD%B8%E7%BF%92locomotion.md)
* [11.3-全身控制（Whole-Body Control, WBC）與二次規劃（QP）的實時神經加速](https://www.google.com/search?q=11.3-%E5%85%A8%E8%BA%AB%E6%8E%A7%E5%88%B6%E8%88%87%E4%BA%8C%E6%AC%A1%E8%A6%8F%E5%8A%83%E7%9A%84%E5%AF%A6%E6%99%82%E7%A5%9E%E7%B6%93%E5%8A%A0%E9%80%9F.md)
* [11.4-具身操作（Embodied Manipulation）：靈巧手與動態抓取的閉環力控](https://www.google.com/search?q=11.4-%E5%85%B7%E8%BA%AB%E6%93%8D%E4%BD%9C%E9%9D%88%E5%B7%A7%E6%89%8B%E8%88%87%E5%8B%95%E6%85%8B%E6%8A%93%E5%8F%96%E7%9A%84%E9%96%89%E7%92%B0%E5%8A%9B%E6%8E%A7.md)


* 第12章-遊戲模擬世界、數位孿生與合成資料生成（2024至2026年）
* [12.1-遊戲模擬器作為控制試驗場：從 Atari、Minecraft 到 Unreal Engine 物理引擎](https://www.google.com/search?q=12.1-%E9%81%8A%E6%88%B2%E6%A8%A1%E6%93%AC%E5%99%A8%E4%BD%9C%E7%82%BA%E6%8E%A7%E5%88%B6%E8%A9%A6%E9%A9%97%E5%A0%B4%E8%88%87%E7%89%A9%E7%90%86%E5%BC%95%E6%93%8E.md)
* [12.2-基於世界模型（World Models）的虛擬環境生成與想象力規劃（Imagination-based Planning）](https://www.google.com/search?q=12.2-%E5%9F%BA%E6%96%BC%E4%B8%96%E7%95%8C%E6%A8%A1%E5%9E%8B%E7%9A%84%E8%99%9B%E6%93%AC%E7%92%B0%E5%A2%83%E7%94%9F%E6%88%90%E8%88%87%E6%83%B3%E8%B1%A1%E5%8A%9B%E8%A6%8F%E5%8A%83.md)
* [12.3-Sim-to-Real 轉移技術：網域隨機化（Domain Randomization）與系統識別對齊](https://www.google.com/search?q=12.3-Sim-to-Real%E8%BD%89%E7%A7%BB%E6%8A%80%E8%A1%93%E8%88%87%E7%B6%B2%E5%9F%9F%E9%9A%A8%E6%A9%9F%E5%8C%96.md)
* [12.4-大規模數位孿生（Digital Twins）與實時智慧體控制網路的未來願景](https://www.google.com/search?q=12.4-%E5%A4%A7%E8%A6%8F%E6%A8%A1%E6%95%B8%E4%BD%8D%E5%AD%BF%E7%94%9F%E8%88%87%E5%AF%A6%E6%99%82%E6%99%BA%E6%85%A7%E9%AB%94%E6%8E%A7%E5%88%B6%E7%B6%B2%E8%B7%AF%E7%9A%84%E6%9C%AA%E4%BE%86%E9%A1%98%E6%99%AF.md)



---