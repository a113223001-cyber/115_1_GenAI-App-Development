# 外食族飲食營養粗估器

這是一個以 Streamlit 與 OpenAI Structured Outputs 製作的期中個人小專題。使用者貼上一整天的飲食文字，App 會辨識餐點、估算熱量範圍、評估蛋白質攝取並提供飲食建議。

> 本工具僅供日常飲食參考，不是醫療診斷或營養治療建議。熱量與營養估算可能不準確，需由使用者自行核對。

## 1. 使用者與問題

目標使用者是外食族、控制飲食或體重者，以及想快速了解一整天飲食結構的學生與上班族。

使用情境：

1. 使用者把早餐、午餐、晚餐與飲料內容貼入文字框。
2. 使用者確認 API 開關後送出。
3. App 回傳五個結構化欄位並依欄位呈現。
4. 使用者對照原文，判讀餐點辨識與營養估算是否合理。

## 2. 主要功能

- 提供一個清楚的飲食文字輸入區與送出按鈕。
- 預設關閉 API；勾選開關並送出有效內容才會呼叫 OpenAI。
- 送出前檢查空白文字與 6000 字元上限。
- 使用 Pydantic 定義輸出契約與 Strict Structured Outputs。
- 驗證回應完成狀態、拒答、解析結果與非空文字欄位。
- 成功後保存當筆原文與結果，並顯示原始 JSON 供人工核對。
- 新送出失敗時清除舊結果，避免將舊成功結果誤認為本次成果。

## 3. Structured Outputs 路線

本專案採用 Pydantic 路線，而不是只要求模型「回傳 JSON」。理由如下：

- 使用 `BaseModel` 建立清楚的資料結構。
- 使用 `ConfigDict(extra="forbid", strict=True)` 禁止多餘欄位及型別自動轉換。
- 使用 `client.responses.parse(text_format=ProjectResult)` 讓回應依 Pydantic 模型解析。
- 稱職的欄位檢查可以直接與畫面呈現、人工核對對應。

## 4. 輸出欄位

| 欄位 | 型別 | 用途 |
|---|---|---|
| `identified_meals` | `str` |辨識輸入中的餐點與飲料；無法辨識時填「資訊不足」。 |
| `estimated_calories` | `str` | 估算一天飲食的熱量範圍；無法估算時填「無法估算」。 |
| `protein_assessment` | `str` | 評估蛋白質攝取可能為足夠、偏低、過高或無法評估。 |
| `is_sufficient_info` | `str` | 評估輸入是否包含足夠資訊，填 `true` 或 `false`。 |
| `dietary_advice` | `str` | 針對具體餐點提供一至兩點飲食建議；資訊不足時請使用者補充。 |

## 5. 專案結構

```text
Midterm Mini-Project/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── 第08週_課堂簡化版_專題設計與驗收紀錄.md
└── .streamlit/
    └── secrets.example.toml
```

## 6. 安裝與啟動

建議在專案資料夾內建立虛擬環境。以下以 Windows PowerShell 與專案資料夾為例：

```powershell
cd "c:\你的路徑\Midterm Mini-Project"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

實際安裝版本請以你的 README 與 `requirements.txt` 為準；雲端部署使用的 Python 版本需另外確認。

## 7. 設定 API 金鑰

### 本機設定

在專案資料夾建立 `.env`：

```env
OPENAI_API_KEY=你的金鑰
OPENAI_MODEL=gpt-5.4-mini
```

程式會優先讀取 `.streamlit/secrets`，接著讀取環境變數。若平台或本機沒有設定模型，也會預設為 `gpt-5.4-mini`。

### Streamlit Community Cloud

在 App 的 Secrets 加入：

```toml
OPENAI_API_KEY = "你的金鑰"
OPENAI_MODEL = "gpt-5.4-mini"
```

- 不要提交 `.env`。
- 不要提交 `.streamlit/secrets.toml`。
- 不要提交 `.venv`、`__pycache__` 或快取目錄。
- `.env.example` 與 `.streamlit/secrets.example.toml` 可提交，只能放假值或格式範例。

## 8. 操作範例

正常案例：

```text
早餐吃鮪魚蛋餅配無糖豆漿，午餐吃排骨便當飯半碗。
```

預期結果應包含：

- 辨識出的餐點與飲料。
- 熱量範圍。
- 蛋白質攝取評估。
- `is_sufficient_info` 為 `true`。
- 針對原文的飲食建議。

資訊不足案例：

```text
我今天有吃飯跟喝水。
```

理想情況是將 `is_sufficient_info` 設為 `false`，避免編造餐點、份量與熱量，並提示使用者補充具體餐點。

離線操作時即使不勾選 API，也會先檢查空白、6000 字元限制與專題設計；離線檢查通過不能視為模型成功結果。

## 9. 測試與驗收

詳細的設計與測試紀錄見[第08週專題設計與驗收紀錄](第08週_課堂簡化版_專題設計與驗收紀錄.md)。

| 項目 | 狀態 |
|---|---|
| 空白輸入檢查 | 已由程式實作；可執行離線驗證。 |
| 6000 字元上限檢查 | 已由程式實作；可執行離線驗證。 |
| API 預設關閉 | 已由程式實作。 |
| 缺少 API 金鑰處理 | 已由程式實作。 |
| Pydantic Structured Outputs | 已由程式實作；真實結果需實際 API 驗證。 |
| 本機正常資料真實 API 測試 | 已完成；實際輸入、五欄輸出與人工核對見驗收紀錄；1 次請求。 |
| 本機資訊不足真實 API 測試 | 已完成；模型正確識別不足、未補造資料；1 次請求。 |
| Streamlit Community Cloud 部署 | 已完成；App 網址：https://1151genai-app-development-bw9sgbzjgs3abx5zotcg7.streamlit.app |
| 雲端正常資料真實 API 測試 | 已完成；識別早餐與午餐、估算熱量並逐欄核對；1 次請求。 |
| 雲端資訊不足真實 API 測試 | 已完成；正確拒絕估算並要求補充餐點與份量；1 次請求。 |

Cloud 部署與驗收資訊：

```text
App 網址：https://1151genai-app-development-bw9sgbzjgs3abx5zotcg7.streamlit.app
部署日期：2026-11-09
部署分支：main
Cloud Main file path：app.py
專案實際入口：Midterm Mini-Project/app.py
雲端 Python 版本：待正式查看 Logs 後補填
雲端驗證模型：gpt-5.4-mini（以 Cloud Secrets 設定為準）
雲端正常案例：已完成；1 次 API request
雲端資訊不足案例：已完成；1 次 API request
雲端 API 合計：2 次請求
```

## 10. 成本與限制

- 每次有效送出最多呼叫一次 API。
- 每次 API 送出的文字最多 6000 字元。
- 程式設定 `max_retries=0`，避免自動重試增加請求數與費用。
- 網路逾時設定為 60 秒，但不代表整體執行一定能在 60 秒內完成。
- `store=False` 不要求 OpenAI 保存本次回應，但仍需遵守平台帳號、金鑰與計費規則。
- 熱量與蛋白質評估可能受餐點份量、料理方式與營養資料誤差影響。
- App 不驗證餐點是否符合個人健康狀況、過敏原、疾病限制或醫療需求。

## 11. 個人設計與修改

相較於教師摘要器，本專案有以下個人化修改：

1. 題目改為外食族日常飲食營養粗估，而不是文章摘要。
2. 新增 `identified_meals`、`estimated_calories`、`protein_assessment`、`is_sufficient_info` 與 `dietary_advice` 等專屬欄位。
3. 新增 `is_sufficient_info` 作為資訊不足護欄。
4. 使用雙欄 `st.metric` 與建議區呈現結果，而不是純文字或表格。
5. 保留 API 開關、長度限制、拒答檢查、完成狀態檢查與 session state 結果保存。
