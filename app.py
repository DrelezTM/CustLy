from flask import Flask
from controllers.auth_controller import auth_bp
from controllers.url_controller import url_bp
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(url_bp)

if __name__ == "__main__":
    app.run(debug=True)