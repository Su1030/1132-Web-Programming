<<<<<<< HEAD
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
=======
import os
import json
import re
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# 設定 Secret Key 以啟用 Session
app.secret_key = 'your_secret_key_here'

JSON_FILE = 'users.json'

# --- 工具函式區 ---

def read_users():
    """讀取 JSON 檔案，若檔案損壞或不存在則初始化"""
    if not os.path.exists(JSON_FILE):
        return {"users": []}
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"users": []}

def save_users(data):
    """寫入 JSON 檔案"""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- Jinja2 自定義過濾器 ---

@app.template_filter('mask_phone')
def mask_phone(phone):
    """電話遮罩：0912345678 -> 0912****78"""
    if phone and len(phone) == 10:
        return f"{phone[:4]}****{phone[8:]}"
    return phone

@app.template_filter('format_tw_date')
def format_tw_date(date_str):
    """西元年轉民國年：1990-01-01 -> 79/01/01"""
    if not date_str: return ""
    try:
        y, m, d = date_str.split('-')
        tw_y = int(y) - 1911
        return f"{tw_y}/{m}/{d}"
    except:
        return date_str

# --- 路由與邏輯區 ---

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone', '')
        birthdate = request.form.get('birthdate')

        # 基礎驗證
        if not (username and email and password and birthdate):
            return redirect(url_for('error_route', message="所有必填欄位不可為空"))
        
        if not (re.match(r"[^@]+@[^@]+\.[^@]+", email)):
            return redirect(url_for('error_route', message="Email 格式不正確"))
        
        if not (6 <= len(password) <= 16):
            return redirect(url_for('error_route', message="密碼長度需為 6-16 字元"))

        if phone and (not re.match(r"^09\d{8}$", phone)):
            return redirect(url_for('error_route', message="電話需為09開頭的10位數字"))

        data = read_users()
        for u in data['users']:
            if u['username'] == username or u['email'] == email:
                return redirect(url_for('error_route', message="帳號或 Email 已被註冊"))

        # 寫入資料
        new_user = {
            "username": username,
            "email": email,
            "password": password,
            "phone": phone,
            "birthdate": birthdate,
            "is_admin": (username == 'admin') # 預設 admin 帳號為管理者
        }
        data['users'].append(new_user)
        save_users(data)
        return redirect(url_for('login_route'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        data = read_users()
        for u in data['users']:
            if u['email'] == email and u['password'] == password:
                session['username'] = u['username']
                session['is_admin'] = u.get('is_admin', False) or (u['username'] == 'admin')
                return redirect(url_for('announcement'))
        
        return redirect(url_for('error_route', message="Email 或密碼錯誤"))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/announcement')
def announcement():
    if 'username' not in session:
        return redirect(url_for('error_route', message="請先登入"))
    return render_template('announcement.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('error_route', message="請先登入"))
    
    data = read_users()
    current_user = next((u for u in data['users'] if u['username'] == session['username']), None)

    if request.method == 'POST':
        new_email = request.form.get('email')
        new_phone = request.form.get('phone')
        new_birthdate = request.form.get('birthdate')
        new_password = request.form.get('password')

        # 檢查 Email 是否與他人重複
        for u in data['users']:
            if u['email'] == new_email and u['username'] != session['username']:
                return redirect(url_for('error_route', message="Email 已被其他會員使用"))

        current_user['email'] = new_email
        current_user['phone'] = new_phone
        current_user['birthdate'] = new_birthdate
        if new_password:
            current_user['password'] = new_password
            
        save_users(data)
        return redirect(url_for('announcement'))

    return render_template('profile.html', user=current_user)

@app.route('/users')
def users_list_route():
    if not session.get('is_admin'):
        return redirect(url_for('error_route', message="權限不足"))
    data = read_users()
    return render_template('users.html', users=data['users'])

@app.route('/users/<username>/edit', methods=['GET', 'POST'])
def edit_user_route(username):
    if not session.get('is_admin'):
        return redirect(url_for('error_route', message="權解不足"))
    
    data = read_users()
    target_user = next((u for u in data['users'] if u['username'] == username), None)
    
    if request.method == 'POST':
        target_user['phone'] = request.form.get('phone')
        target_user['birthdate'] = request.form.get('birthdate')
        new_pwd = request.form.get('password')
        if new_pwd:
            target_user['password'] = new_pwd
        save_users(data)
        return redirect(url_for('users_list_route'))
        
    return render_template('edit_user.html', user=target_user)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user_route(username):
    if not session.get('is_admin'):
        return redirect(url_for('error_route', message="權限不足"))
    
    if username == 'admin' or username == session['username']:
        return redirect(url_for('error_route', message="不可刪除管理員或自己"))
    
    data = read_users()
    data['users'] = [u for u in data['users'] if u['username'] != username]
    save_users(data)
    return redirect(url_for('users_list_route'))

@app.route('/error')
def error_route():
    msg = request.args.get('message', '未知錯誤')
    return render_template('error.html', message=msg)
>>>>>>> 61954bd (feat: 初次採用GIT更動程式架構)
