import os
import json
import re
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

JSON_FILE = 'users.json'

def read_users():
    if not os.path.exists(JSON_FILE):
        return {"users": []}
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"users": []}

def save_users(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.template_filter('mask_phone')
def mask_phone(phone):
    if phone and len(phone) == 10:
        return f"{phone[:4]}****{phone[8:]}"
    return phone

@app.template_filter('format_tw_date')
def format_tw_date(date_str):
    if not date_str: return ""
    try:
        y, m, d = date_str.split('-')
        tw_y = int(y) - 1911
        return f"{tw_y}/{m}/{d}"
    except:
        return date_str

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

        new_user = {
            "username": username,
            "email": email,
            "password": password,
            "phone": phone,
            "birthdate": birthdate,
            "is_admin": (username == 'admin')
        }
        data['users'].append(new_user)
        save_users(data)
        
        return render_template('welcome.html', username=username, email=email, phone=phone, birthdate=birthdate)
    
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
        return redirect(url_for('error_route', message="權限不足"))
    
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