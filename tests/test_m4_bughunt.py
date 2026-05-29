from flask import Flask, render_template
from flask-login import LoginManager, login_required

app = Flask(__name__)

#test of import for M4 bughunt
def test_import():
    from app import app, login_manager  



login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")