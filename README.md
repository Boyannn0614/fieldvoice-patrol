# 田語智巡 FieldVoice Patrol

田語智巡是一個以在地語音驅動的無人機積水巡檢原型。農民可用華語或臺語下達巡檢需求；系統以 Taiwan Tongues ASR CE 將語音轉為文字，經任務解析與人工確認後啟動巡檢。展示階段使用藍色色塊模擬不同程度的田區積水，再由影像辨識估算位置與面積比例，回傳地面站並以語音播報結果。

> 本專案目前是競賽用概念驗證。藍色色塊是可控的「積水替代標記」，不能宣稱已能辨識真實農田積水；真實環境仍需蒐集影像、標註資料並完成模型驗證。

## 專案特色

- 在地語音操作：規劃介接數位發展部數位產業署開源的 Taiwan Tongues ASR CE，降低長者與不熟悉文字介面農民的操作門檻。
- 實體展示可行：按下確認按鈕後，由小型無人機或移動載具沿固定路徑巡檢四色分區模型。
- 可驗證的影像模組：目前以 Pillow 與 NumPy 進行藍色色塊分割，輸出積水比例、主要位置與警示等級。
- 人機協作安全：語音辨識後必須由使用者確認，才會送出飛行任務。
- 可持續擴充：後續可把模擬色塊替換成真實農田影像分割模型，並回饋繁中與臺語修正語料。

## 系統流程

```text
農民語音
   ↓
Taiwan Tongues ASR CE
   ↓
任務解析與畫面確認
   ↓
無人機固定航線巡檢
   ↓
相機影像／藍色色塊積水模擬
   ↓
位置與面積比例分析
   ↓
地面站地圖、文字與語音回報
```

## 核心開源模型

- 模型：Taiwan Tongues ASR CE
- 開源來源：[adi-gov-tw/Taiwan-Tongues-ASR-CE](https://github.com/adi-gov-tw/Taiwan-Tongues-ASR-CE)
- 用途：將農民的華語或臺語巡檢指令轉為文字，作為任務解析輸入。
- 整合狀態：目前完成介接規格與指令格式設計，待硬體與模型執行環境就緒後進行端對端串接。

模型版本、授權與整合界線詳見 [MODEL_SOURCES.md](MODEL_SOURCES.md)。

## 目前可執行的色塊辨識示範

### 1. 安裝

```bash
python -m pip install -r requirements.txt
```

### 2. 產生模擬農田影像

```bash
python create_sample_field.py
```

### 3. 執行辨識

```bash
python vision_demo.py simulated_field.png \
  --output-image annotated_result.png \
  --output-json sample_result.json
```

程式會把畫面切成左上、右上、左下、右下四區，計算各區藍色像素比例，再輸出 `normal`、`watch` 或 `warning`。RGB 門檻可依拍攝燈光調整。

## 目錄

```text
fieldvoice-patrol/
├─ vision_demo.py          # 藍色色塊偵測與區域判斷
├─ mission_parser.py       # 語音轉寫文字的任務解析雛形
├─ create_sample_field.py  # 產生可重現的模擬農田影像
├─ simulated_field.png     # 模擬農田測試圖
├─ annotated_result.png    # 分析結果示意圖
├─ MODEL_SOURCES.md        # 模型與資料治理說明
└─ ARCHITECTURE.md         # 系統架構與安全界線
```

## 資料與隱私原則

- 公開資料以模擬影像與去識別文字為主。
- 不上傳原始個人語音、精確農地座標、帳號憑證或 API 金鑰。
- 未來建立語料回饋機制時，須先取得同意、去識別並保留人工審核流程。

## 開發里程碑

1. 完成色塊辨識、任務解析與地面站介面雛形。
2. 串接 Taiwan Tongues ASR CE，測試華語與臺語農業指令。
3. 串接無人機或安全的縮尺移動載具，加入實體確認按鈕。
4. 蒐集經同意的在地語料與真實農田影像，建立量化評估。

## 授權

本專案自行開發的程式碼採 MIT License。外部模型、資料與套件仍依各自原始授權條款使用。
