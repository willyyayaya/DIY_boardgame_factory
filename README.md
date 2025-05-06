# AI 桌遊推薦工廠

這是一個基於AI的桌遊推薦系統，能夠根據用戶偏好（如玩家人數、時間限制、複雜度、主題和機制等）提供個性化的桌遊推薦。

## 功能特點

- 基於AI的個性化桌遊推薦
- 全面的桌遊偏好設置（玩家人數、時間、複雜度等）
- 詳細的主題和機制多選項
- 視覺化推薦結果展示
- 移動端友好設計
- 支持結果列印

## 技術棧

- **後端**: Python with FastAPI
- **前端**: HTML, CSS, JavaScript, Tailwind CSS
- **模板引擎**: Jinja2
- **表單增強**: Select2.js (多選下拉框)
- **數據存儲**: 本地JSON文件
- **AI集成**: OpenAI API (可選)

## 快速開始

### 先決條件

- Python 3.7+
- pip

### 安裝步驟

1. 克隆此儲存庫：
```bash
git clone https://github.com/your-username/ai-boardgame-factory.git
cd ai-boardgame-factory
```

2. 創建並激活虛擬環境（可選但推薦）：
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. 安裝依賴：
```bash
pip install -r requirements.txt
```

4. 配置 OpenAI API（可選）：
   - 在項目根目錄創建 `.env` 文件
   - 添加您的 API 密鑰：`OPENAI_API_KEY=your-api-key-here`
   - 打開 `main.py` 並取消註釋 OpenAI 相關代碼

### 運行應用

```bash
uvicorn main:app --reload
```

應用將在 http://localhost:8000 上啟動。

## 項目結構

```
AI-boardgame-factory/
├── main.py                  # 主應用程式和API路由
├── static/                  # 靜態資源
│   ├── css/style.css        # 樣式表
│   └── js/main.js           # JavaScript功能
├── templates/               # HTML模板
│   ├── index.html           # 首頁
│   ├── preferences.html     # 偏好設置頁面
│   └── recommendation.html  # 推薦結果頁面
├── data/                    # 數據存儲
│   ├── preferences/         # 用戶偏好JSON
│   └── recommendations/     # 推薦結果JSON
└── requirements.txt         # 項目依賴
```

## 使用說明

1. 在首頁點擊"開始尋找您的完美桌遊"按鈕
2. 填寫您的偏好表單，包括玩家人數、遊戲時間、複雜度等
3. 提交表單，系統將生成適合您的桌遊推薦
4. 查看推薦結果，包含推薦理由和遊戲詳情
5. 可以列印結果或重新設置偏好

## OpenAI集成

此項目包含與OpenAI API的可選集成：

1. 獲取您的 [OpenAI API密鑰](https://platform.openai.com/)
2. 配置 `.env` 文件（如上所述）
3. 在 `main.py` 中取消註釋相關代碼
4. 重新啟動應用

## 未來計劃

- 添加更多桌遊特性和偏好選項
- 實現用戶登錄和推薦歷史
- 集成真實桌遊數據庫
- 添加直接購買鏈接
- 支持桌遊組合推薦

## 貢獻

歡迎提交問題和貢獻代碼。請遵循標準的開源貢獻流程。

## 授權

[MIT License](LICENSE) 