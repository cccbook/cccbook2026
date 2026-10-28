## 1954 - Harrington 脊柱側彎矯正（從鐵肺裡的駝背，到手術台上的直背）

## 案件摘要

**本案的兇器，是一根帶鉤的金屬棒——把彎成 C 形的脊柱，像撐帳篷一樣撐直。**

1954 年起，休士頓 Baylor 醫學院的 Paul Harrington 專攻一種當時的絕症：**小兒麻痺後脊柱側彎**。他設計「內置牽引系統」——在凹側以棘輪鉤撐開（distraction rod）、凸側以螺紋鉤壓縮（compression rod），結合術後石膏，把側彎從「矯形支架只能緩慢拖延」推進到手術矯正。1962 年發表首個大系列（226 例），Harrington 器械統治脊柱外科整整 20 年，直到 1980 年代被 Luque 與 Cotrel–Dubousset 的節段固定取代——**脊柱側彎從「臥床與鐵肺」時代，走進「手術矯正」時代。**

## 前因 -- 為什麼會有這個案子

- **小兒麻痺的浩劫**：1940–50 年代美國每年數萬例脊灰癱瘓；脊柱旁肌肉失衡造成迅速惡化的長 C 形側彎，患者被放入石膏與鐵肺，嚴重者心肺衰竭。
- **休士頓的 Southwestern Poliomyelitis Respiratory Center**：Harrington 所在的全國脊灰呼吸中心，供應了臨床最密集、最嚴重的一批病例。
- **保守治療的失敗**：石膏矯正（Risser 局部石膏）與支具只能減緩；重度側彎（>60°）的死亡率與肺功能崩壞逼出手術需求。
- **麻醉與無菌已就位**：長時間脊柱手術在 1950 年代初剛剛安全可行（`1846-麻醉降臨與骨科手術革命.md`、`1867-Lister無菌術拯救開放性骨折.md`）。

## 線索與推理 -- 背後的理論

Harrington 的推理：側彎的三維畸形（冠狀面彎+軸向旋轉）中，**冠狀面撐開**是最可控的力——棘輪撐開棒提供持續牽引力，每次手術可逐步撐開。力學：

$$ F_{\text{撐開}} \propto \text{棘輪齒距} \times \text{撐開次數} \quad ; \quad \text{Cobb 角矯正率} \approx 30\text{–}50\% $$

他刻意選擇「兩點固定」（上端穩定椎、下端穩定椎）而非多點——因為小兒麻痺骨質鬆軟，多點鉤容易脫鉤。這是「骨質→固定策略」的力學推理範式。

```python
# Harrington 撐開的效果估算
def harrington(cobb_pre, distraction_perc=0.4):
    cobb_post = cobb_pre * (1 - distraction_perc)
    return f"Cobb 角 {cobb_pre}° → {cobb_post:.0f}°"

print(harrington(70))   # 70° → 42°
```

代價也要偵查：兩點撐開產生「平背畸形」（失去胸椎後凸）、鉤脫位、假關節率高（~15–40%）、且**不矯正旋轉**——凸側皮質棒與日後的節段固定（Luque 鋼絲、CD 椎弓根螺釘）正是對這些缺陷的逐點修正。脊柱側彎矯正的生物學核心「融合床」（自體髂骨植骨+去皮質）也由 Harrington 標準化——**矯形（instrumentation）+融合（fusion）**的雙支柱哲學至今未變。

## 結案 -- 後果與影響

- **脊柱外科成為獨立次專科**：從「神經科/骨科邊陲」到有自己的器械學、生物力學與分類（King、Lenke 分類）。
- **器械族譜**：Harrington（1954）→ Luque 節段鋼絲（1976）→ Cotrel–Dubousset（1984，三維矯正+橫連）→ 椎弓根螺釘時代（1990s 至今）→ 微創與非融合（生長棒、椎體拴系 tethering, 2019 FDA 核准）——每代都在修 Harrington 的力學漏洞。
- **特發性側彎的轉向**：小兒麻痺疫苗（1955 Salk）使脊灰側彎驟減，手術對象轉向青少年特發性側彎（AIS）——疫苗改變了脊柱外科的病人組成。
- **篩檢與支具的政策線**：學校篩檢（1963 起）、Milwaukee 支具與 Boston 支具、BrAIST 試驗（2013 證明支具有效）——與手術線並行的保守線持續演化。

## 關鍵人物與文獻

- Paul R. Harrington（1911–1980）——休士頓 Baylor 醫學院骨科主任，「Harrington 棒」之父。
- Eduardo Luque——墨西哥，節段鋼絲固定（1976）。
- Yves Cotrel 與 Jean Dubousset——法國，1984 年三維節段固定革命。
- Harrington, P. R., *Treatment of scoliosis: correction and internal fixation by spine instrumentation*, J Bone Joint Surg Am, 1962。
- John Lonstein 與Robert B. Winter 的 Minnesota 學派脊柱側彎自然史研究。
