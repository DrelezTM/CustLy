from flask import Blueprint, render_template, request, redirect, jsonify
import mysql.connector
import jwt
from functools import wraps
from config import SECRET_KEY, DB_CONFIG
import string, random
from datetime import datetime
import user_agents
import requests
from werkzeug.security import generate_password_hash, check_password_hash

url_bp = Blueprint("url", __name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
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

def get_country_from_ip(ip):
    if ip in ('127.0.0.1', '::1'):
        return "Local"
    try:
        r = requests.get(f"https://ipapi.co/{ip}/country_name/")
        if r.status_code == 200:
            return r.text
    except:
        pass
    return "Unknown"

@url_bp.route('/')
@token_required
def index(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM urls WHERE user_id=%s", (user_id,))
    urls = cursor.fetchall()

    for url in urls:
        cursor.execute("SELECT COUNT(*) as total FROM visitors WHERE url_id=%s", (url['id'],))
        url['visits'] = cursor.fetchone()['total']

    cursor.close()
    db.close()
    return render_template('index.html', urls=urls)

@url_bp.route('/add', methods=['POST', 'GET'])
@token_required
def add(user_id):
    error_message = None
    if request.method == 'POST':
        url = request.form['url']
        slug = request.form.get('slug') or generate_slug()
        expires_at = request.form.get('expires_at') or None

        password_val = request.form.get('password') or None
        if password_val:
            password_val = generate_password_hash(password_val)

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT id FROM urls WHERE slug=%s", (slug,))
        if cursor.fetchone():
            error_message = "Slug sudah digunakan, pilih yang lain"
            cursor.close()
            db.close()
            return render_template('add-url.html', error=error_message, form_data=request.form)

        cursor.execute(
            "INSERT INTO urls (user_id, slug, url, password, expires_at) VALUES (%s,%s,%s,%s,%s)",
            (user_id, slug, url, password_val, expires_at)
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect('/')
    return render_template('add-url.html', error=error_message)

@url_bp.route('/edit/<int:id>', methods=['POST', 'GET'])
@token_required
def edit(user_id, id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        url_val = request.form['url'].strip()
        expires_at = request.form.get('expires_at') or None
        
        password_val = request.form.get('password') or None
        if password_val:
            password_val = generate_password_hash(password_val)

        if expires_at:
            expires_at = expires_at.replace('T', ' ')

        cursor.execute(
            "UPDATE urls SET url=%s, password=%s, updated_at=NOW(), expires_at=%s WHERE id=%s AND user_id=%s",
            (url_val, password_val, expires_at, id, user_id)
        )
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

@url_bp.route('/<slug>', methods=['GET', 'POST'])
def redirect_slug(slug):
    if "." in slug:
        return render_template("not-found.html"), 404
        
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM urls WHERE slug=%s", (slug,))
    url_record = cursor.fetchone()
    if not url_record:
        cursor.close()
        db.close()
        return render_template("not-found.html"), 404

    if url_record.get('expires_at') and url_record['expires_at'] < datetime.now():
        cursor.close()
        db.close()
        return render_template("expired-url.html", url=url_record), 410

    if url_record.get('password'):
        if request.method == 'POST':
            input_pass = request.form.get('password')
            if check_password_hash(url_record['password'], input_pass):
                pass
            else:
                cursor.close()
                db.close()
                return render_template('password.html', slug=slug, error="Password salah!")
        else:
            cursor.close()
            db.close()
            return render_template('password.html', slug=slug)

    ip = request.remote_addr
    ua_string = request.headers.get('User-Agent', '')
    ua = user_agents.parse(ua_string)
    browser = ua.browser.family
    os = ua.os.family
    country = get_country_from_ip(ip)
    referrer = request.referrer

    cursor.execute(
        "INSERT INTO visitors (url_id, ip, country, os, browser, referrer) VALUES (%s,%s,%s,%s,%s,%s)",
        (url_record['id'], ip, country, os, browser, referrer)
    )
    db.commit()
    cursor.close()
    db.close()

    return redirect(url_record['url'])

@url_bp.route('/stats/<int:id>')
@token_required
def stats(user_id, id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM urls WHERE id=%s AND user_id=%s", (id, user_id))
    url = cursor.fetchone()
    if not url:
        cursor.close()
        db.close()
        return jsonify({"error": "Not found"}), 404

    cursor.execute("SELECT COUNT(*) as total FROM visitors WHERE url_id=%s", (id,))
    total_visits = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(DISTINCT ip) as unique_count FROM visitors WHERE url_id=%s", (id,))
    unique_visitors = cursor.fetchone()['unique_count']

    cursor.execute("""
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM visitors
        WHERE url_id=%s AND created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    """, (id,))
    daily_visits = [{"date": r['date'].strftime("%d-%m-%Y"), "count": r['count']} for r in cursor.fetchall()]

    cursor.execute("SELECT os, COUNT(*) as value FROM visitors WHERE url_id=%s GROUP BY os", (id,))
    devices = [{"name": r['os'] or 'Unknown', "value": r['value']} for r in cursor.fetchall()]

    cursor.execute("SELECT referrer, COUNT(*) as value FROM visitors WHERE url_id=%s GROUP BY referrer", (id,))
    sources = [{"name": r['referrer'] or "Direct", "value": r['value']} for r in cursor.fetchall()]

    cursor.execute("""
        SELECT created_at, ip, country, os, browser, referrer
        FROM visitors
        WHERE url_id=%s
        ORDER BY created_at DESC
        LIMIT 5
    """, (id,))
    recent_visits = []
    for r in cursor.fetchall():
        recent_visits.append({
            "time": r['created_at'].strftime("%d-%m-%Y %H:%M"),
            "ip": r['ip'],
            "location": r['country'] or "Unknown",
            "device": f"{r['os']}/{r['browser']}" if r['os'] else "-",
            "referrer": r['referrer'] or "Direct"
        })

    cursor.close()
    db.close()

    return jsonify({
        "total_visits": total_visits,
        "unique_visitors": unique_visitors,
        "daily_visits": daily_visits,
        "devices": devices,
        "sources": sources,
        "recent_visits": recent_visits,
        "top_device": devices[0]['name'] if devices else "-"
    })