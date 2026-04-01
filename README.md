# CustLy
<p align="center">
  <img alt="@urlshortener" style="width: 150px;" src="https://github.com/DrelezTM/URL-Shortener/blob/main/public/CustLy.png">
</p>
<div align="center">
  <h3>URL Shortener</h3>
  <p>A URL Shortener application with analytics dashboard built using <a href="https://flask.palletsprojects.com/">Flask</a> and <a href="https://www.mysql.com/">MySQL</a></p>
</div>
<div align="center">
  <a href="https://dsc.gg/DrelezTM">Report Bug</a> | <a href="https://github.com/DrelezTM/CustLy/issues">Issues</a>
</div>

## Installation 📑
* Clone Repository
  ```sh
    git clone https://github.com/DrelezTM/CustLy.git
  ```
* Open Directory
  ```sh
    cd CustLy
  ```
* Install Dependencies
  ```sh
    pip install -r requirements.txt
  ```
* Configure Environment
  ```sh
    cp config.py.example config.py
    # Edit config.py with your SECRET_KEY and DB_CONFIG
  ```
* Upload Database
  - Create a database with the name "telstweet" in MySQL/phpmyadmin
  - Click "Import"
  - Click "Choose File" then insert the <a href="https://github.com/DrelezTM/CustLy/blob/main/custly.sql">custly.sql</a> file in the <a href="https://github.com/DrelezTM/CustLy/blob/main/custly.sql">/custly.sql</a> folder.
* Start Project
  ```sh
    python app.py
  ```

## Features ✨
* 🔗 Shorten long URLs with custom slugs
* 🔒 Password-protected short links
* ⏳ Expirable links with expiration date
* 📊 Visitor analytics (browser, OS, country, referrer)
* 📈 Daily visit charts (last 7 days)
* 👤 User authentication (register/login)

## User Interface 🖼
* Register / Sign Up Page
  <img width="1920" height="904" alt="register" src="https://github.com/user-attachments/assets/54a2537f-318f-418f-b98f-39f5623e34ee" />
* Login / Sign In Page
  <img width="1920" height="868" alt="login" src="https://github.com/user-attachments/assets/5aa4f5b9-2b86-4994-b0ec-e66e6c181aec" />
* Dashboard & Stats / Analytics Page
  <img width="1920" height="1837" alt="analytics" src="https://github.com/user-attachments/assets/535e644d-54f4-459b-8bd8-dd30a4fb8761" />
* Add URL Page
  <img width="1920" height="950" alt="add-url" src="https://github.com/user-attachments/assets/e1697c2f-e284-416a-b94b-004c5d06c280" />
* Edit URL Page
  <img width="1920" height="868" alt="edit-url" src="https://github.com/user-attachments/assets/1a357c85-c2b6-428a-9e2b-6411d61361ec" />
* Expired URL Page
  <img width="1920" height="871" alt="expired-url" src="https://github.com/user-attachments/assets/05968610-060e-4b9c-a352-35673846f754" />
* Password Protected URL Page
  <img width="1920" height="868" alt="password-protected" src="https://github.com/user-attachments/assets/36380e6b-f12b-46f0-8e76-b6f40db5a893" />

## Built With 🛠
* [Flask](https://flask.palletsprojects.com/)
* [MySQL](https://www.mysql.com/)
* [PyJWT](https://pyjwt.readthedocs.io/)
* [Werkzeug](https://werkzeug.palletsprojects.com/)
* [user-agents](https://pypi.org/project/user-agents/)
* [ipapi.co](https://ipapi.co/) — IP Geolocation

## Error or Bug 🐞
* [Discord](https://dsc.gg/DrelezTM)
* [YouTube](https://www.youtube.com/p/DrelezTM)
* [Instagram](https://www.instagram.com/DrelezTM)
* [Issues](https://github.com/DrelezTM/CustLy/issues)

## License 📜
* [License](https://github.com/DrelezTM/CustLy/blob/main/LICENSE)