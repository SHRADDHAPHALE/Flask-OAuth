import os

from werkzeug.wrappers import response
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

from flask import Flask, redirect, url_for, render_template, session
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)



app.config['SECRET_KEY'] = 'secret-key'


blueprint = make_google_blueprint(client_id="######.apps.googleusercontent.com",
    client_secret="####",offline=True,
    scope=["profile", "email"])
app.register_blueprint(blueprint, url_prefix="/login")

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/welcome')
def welcome():
    response = google.get("/oauth2/v2/userinfo")
    assert response.ok, response.text
    email=response.json()["email"]

    return render_template("welcome.html",email=email)

@app.route("/login/google")
def login():
    if not google.authorized:
        return render_template(url_for("google.login"))

    response = google.get("/oauth2/v2/userinfo")
    assert response.ok, response.text
    email = response.json()["email"]

    return render_template("welcome.html",email=email)


if __name__ == "__main__":
    app.run()
