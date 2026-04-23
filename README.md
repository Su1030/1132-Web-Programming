## 📑 專案目錄

  * 功能特點
  * 技術棧
  * 畫面預覽
  * 安裝與執行步驟
  * 專案結構
  * 開發細節
  * 授權條款

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

 <img width="1919" height="770" alt="image" src="https://github.com/user-attachments/assets/b0a81a0a-7aae-4114-b44c-813ff7d4f509" />

 <img width="1900" height="907" alt="image" src="https://github.com/user-attachments/assets/ef85964d-7534-43c7-8868-7d2934d4f35f" />

 <img width="1919" height="912" alt="image" src="https://github.com/user-attachments/assets/ce2894a8-116b-43ab-8cd7-7a3be16cc951" />

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
