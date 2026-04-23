## 📑 專案目錄

  * [功能特點](https://www.google.com/search?q=%23-%E5%8A%9F%E8%83%BD%E7%89%B9%E9%BB%9E)
  * [技術棧](https://www.google.com/search?q=%23-%E6%8A%80%E8%A1%93%E6%A3%A7)
  * [畫面預覽](https://www.google.com/search?q=%23-%E7%95%AB%E9%9D%A2%E9%A0%90%E8%A6%BD)
  * [安裝與執行步驟](https://www.google.com/search?q=%23-%E5%AE%89%E8%A3%9D%E8%88%87%E5%9F%B7%E8%A1%8C%E6%AD%A5%E9%A9%9F)
  * [專案結構](https://www.google.com/search?q=%23-%E5%B0%88%E6%A1%88%E7%B5%90%E6%A7%8B)
  * [開發細節](https://www.google.com/search?q=%23-%E9%96%8B%E7%99%BC%E7%B4%B0%E7%AF%80)
  * [授權條款](https://www.google.com/search?q=%23-%E6%8E%88%E6%AC%8A%E6%A2%9D%E6%AC%BE)

-----

## ✨ 功能特點

  * **帳戶管理**：
      * **註冊功能**：支援帳號、Email、密碼、電話及出生日期輸入，並具備 Email 格式驗證與重複註冊檢查。
      * **登入系統**：驗證用戶憑據，匹配成功後導向個性化歡迎頁面。
  * **資料視覺化**：
      * **會員清單**：以表格形式呈現所有註冊用戶，並內建數據遮蔽（電話號碼）與日期格式轉換（民國年）。
  * **優化體驗**：
      * **統一錯誤處理**：所有邏輯錯誤將引導至統一設計的錯誤頁面，支援返回前頁功能。
      * **自適應設計 (Responsive)**：支援手機與桌面端瀏覽。

-----

## 🛠️ 技術棧

  * **後端**: Python 3.x / Flask
  * **前端**: Jinja2 Template Engine / Pico.css (V2) / Custom CSS Variables
  * **資料庫**: JSON File System (`users.json`)

-----

## 📸 畫面預覽

> *(提示：你可以在此處上傳你的截圖並替換下方連結)*

  * **首頁**: 清爽的導覽列與背景漸層設計。
  * **歡迎頁**: 集中式卡片佈局，清晰顯示使用者註冊資訊。
  * **會員清單**: 自動遮蔽敏感資訊（電話中間四碼）與民國年轉換。

-----

## 🚀 安裝與執行步驟

### 1\. 複製儲存庫

```bash
git clone https://github.com/你的帳號/Flask-UserHub.git
cd Flask-UserHub
```

### 2\. 安裝必要套件

```bash
pip install -r requirements.txt
```

### 3\. 執行程式

```bash
python app.py
# 或使用
flask --debug run
```

啟動後，瀏覽器打開 `http://127.0.0.1:5000` 即可看到成品。

-----

## 📁 專案結構

```text
project/
├── app.py              # Flask 主程式邏輯與 API 路由
├── requirements.txt    # 專案依賴套件清單
├── users.json          # 會員資料儲存檔 (自動生成)
├── static/
│   └── css/
│       └── style.css   # 模塊化 CSS 控制中心 (含顏色變數調控)
└── templates/          # HTML 模板資料夾
    ├── base.html       # 基礎版型 (包含導覽列與頁尾)
    ├── index.html      # 首頁
    ├── register.html   # 註冊頁面
    ├── login.html      # 登入頁面
    ├── welcome.html    # 會員歡迎頁面
    ├── users.html      # 會員清單表格
    └── error.html      # 錯誤訊息處理頁面
```

-----

## 🎨 開發細節

### CSS 控制中心

本專案的 `style.css` 採用了 **顏色變數調控區**，你可以輕鬆修改 `:root` 中的變數來變更全站色系：

  * `--primary-color`: 影響主按鈕與聚焦框。
  * `--bg-gradient`: 藍紫雙色漸層，營造現代感視覺。
  * `--base-text-color`: 確保導覽列與頁尾文字清晰易讀，解決框架預設灰色問題。

### 安全與格式化

  * **電話遮蔽**: 使用 Jinja2 Filter 將 `0912345678` 轉換為 `0912****78`。
  * **民國年轉換**: 自動將 `1990-01-01` 轉換為 `79/01/01`。

-----

## 📜 授權條款

本專案採用 **MIT License** 授權。

-----

### GitHub 基本檔案建議

1.  **About 描述**: `Flask 簡易會員系統 - 1132 Web 程式設計第 2 次小考。具備 JSON 存取、CSS 模塊化設計與自定義 Filter 功能。`
2.  **Topics (標籤)**: `python`, `flask`, `web-development`, `css-variables`, `university-project`.
3.  **LICENSE**: 在 GitHub 介面點擊 "Add file" -\> "Create new file"，輸入檔名 `LICENSE`，選擇 **MIT** 模板即可。
