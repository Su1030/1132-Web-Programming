import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
JSON_FILE = 'users.json'

# --- 輔助函式 ---

def init_json_file(file_path: str) -> None:
    """初始化 JSON 檔案，若不存在則建立包含 admin 的預設資料"""
    if not os.path.exists(file_path):
        data = {
            "users": [
                {
                    "username": "admin",
                    "email": "admin@example.com",
                    "password": "admin123",
                    "phone": "0912345678",
                    "birthdate": "1990-01-01"
                }
            ]
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def read_users(file_path: str) -> dict:
    """讀取 JSON 檔案"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(file_path: str, data: dict) -> bool:
    """儲存資料到 JSON 檔案"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def validate_register(form_data: dict, users: list) -> dict:
    """驗證註冊資料"""
    username = form_data.get('username')
    email = form_data.get('email')
    password = form_data.get('password')

    # 基本欄位檢查
    if not username or not email or not password:
        return {"success": False, "error": "所有欄位皆為必填"}
    
    # Email 格式檢查
    if '@' not in email or '.' not in email:
        return {"success": False, "error": "Email 格式錯誤"}

    # 重複檢查
    for u in users:
        if u['username'] == username:
            return {"success": False, "error": "帳號已存在"}
        if u['email'] == email:
            return {"success": False, "error": "Email 已被註冊"}
    
    return {"success": True, "data": form_data}

def verify_login(email: str, password: str, users: list) -> dict:
    """驗證登入資料"""
    for u in users:
        if u['email'] == email and u['password'] == password:
            return {"success": True, "data": u}
    return {"success": False, "error": "帳號或密碼錯誤"}

# 初始化 JSON
init_json_file(JSON_FILE)

# --- 模板過濾器 ---

@app.template_filter('mask_phone')
def mask_phone(phone):
    """將電話號碼中間四碼遮蔽"""
    return phone[:4] + "****" + phone[-2:]

@app.template_filter('format_tw_date')
def format_tw_date(date_str):
    """將日期轉為民國年格式 (YYYY-MM-DD -> YY/MM/DD)"""
    y, m, d = date_str.split('-')
    tw_year = int(y) - 1911
    return f"{tw_year}/{m}/{d}"

# --- 路由 ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        users_data = read_users(JSON_FILE)
        result = validate_register(request.form, users_data['users'])
        
        if result['success']:
            users_data['users'].append(result['data'])
            save_users(JSON_FILE, users_data)
            return redirect(url_for('login_route'))
        else:
            return redirect(url_for('error_route', message=result['error']))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        users_data = read_users(JSON_FILE)
        result = verify_login(request.form.get('email'), request.form.get('password'), users_data['users'])
        
        if result['success']:
            return redirect(url_for('welcome_route', username=result['data']['username']))
        else:
            return redirect(url_for('error_route', message=result['error']))
    return render_template('login.html')

@app.route('/welcome/<username>')
def welcome_route(username):
    users_data = read_users(JSON_FILE)['users']
    user = next((u for u in users_data if u['username'] == username), None)
    if not user:
        return redirect(url_for('error_route', message="找不到該使用者"))
    return render_template('welcome.html', user=user)

@app.route('/users')
def users_list_route():
    users_data = read_users(JSON_FILE)['users']
    return render_template('users.html', users=users_data)

@app.route('/error')
def error_route():
    message = request.args.get('message', '發生未知錯誤')
    return render_template('error.html', message=message)