from flask import Blueprint, render_template, request, redirect
import mysql.connector
import jwt
from functools import wraps
from config import SECRET_KEY, DB_CONFIG
import string, random

url_bp = Blueprint("url", __name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from flask import request, redirect
        token = request.cookies.get('token')
        if not token:
            return redirect('/login')
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = data['user_id']
        except:
            return redirect('/login')
        return f(user_id, *args, **kwargs)
    return decorated

def generate_slug(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@url_bp.route('/')
@token_required
def index(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM urls WHERE user_id=%s", (user_id,))
    urls = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('index.html', urls=urls)

@url_bp.route('/add', methods=['POST', 'GET'])
@token_required
def add(user_id):
    if request.method == 'POST':
        url = request.form['url']
        slug = generate_slug()
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO urls (user_id, slug, url) VALUES (%s, %s, %s)",
                       (user_id, slug, url))
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('add-url.html')

@url_bp.route('/edit/<int:id>', methods=['POST', 'GET'])
@token_required
def edit(user_id, id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        url = request.form['url']
        cursor.execute("UPDATE urls SET url=%s, updated_at=NOW() WHERE id=%s AND user_id=%s",
                       (url, id, user_id))
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    cursor.execute("SELECT * FROM urls WHERE id=%s AND user_id=%s", (id, user_id))
    url_record = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('edit-url.html', url=url_record)

@url_bp.route('/delete/<int:id>')
@token_required
def delete(user_id, id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM urls WHERE id=%s AND user_id=%s", (id, user_id))
    db.commit()
    cursor.close()
    db.close()
    return redirect('/')

# Redirect short URL
@url_bp.route('/<slug>')
def redirect_slug(slug):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT url FROM urls WHERE slug=%s", (slug,))
    record = cursor.fetchone()
    cursor.close()
    db.close()
    if record:
        return redirect(record['url'])
    return "URL not found", 404