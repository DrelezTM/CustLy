from flask import Flask
from flask import render_template
from controllers.auth_controller import auth_bp
from controllers.url_controller import url_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(url_bp)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("not-found.html"), 404

if __name__ == "__main__":
    app.run(debug=True)