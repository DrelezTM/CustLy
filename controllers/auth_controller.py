from flask import Blueprint, request, render_template, redirect, make_response
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY, DB_CONFIG

auth_bp = Blueprint("auth", __name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            cursor.close()
            db.close()
            return render_template(
                "register.html",
                error="Email sudah terdaftar."
            )

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        db.commit()

        cursor.close()
        db.close()

        return redirect('/login')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form_data = {}
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        form_data['email'] = email

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if not user or not check_password_hash(user['password'], password):
            error = "Email or password is incorrect"
            return render_template('login.html', error=error, form_data=form_data)

        token = jwt.encode({
            "user_id": user['id'],
            "exp": datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        resp = make_response(redirect('/'))
        resp.set_cookie("token", token, httponly=True, samesite='Lax')
        return resp

    return render_template('login.html', error=error, form_data=form_data)

@auth_bp.route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.set_cookie("token", "", expires=0)
    return resp
