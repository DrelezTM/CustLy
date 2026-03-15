from flask import Blueprint, request, render_template, redirect, make_response
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY, DB_CONFIG

auth_bp = Blueprint("auth", __name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed = generate_password_hash(password, method='sha256')
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed))
        db.commit()
        cursor.close()
        db.close()
        
        return redirect('/login')
    return render_template('register.html')

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if not user or not check_password_hash(user['password'], password):
            return "Invalid email or password", 401

        token = jwt.encode({
            "user_id": user['id'],
            "exp": datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        resp = make_response(redirect('/'))
        resp.set_cookie("token", token)
        return resp

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.set_cookie("token", "", expires=0)
    return resp