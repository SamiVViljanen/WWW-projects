from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from livereload import Server
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "super_salainen_avain"

bcrypt = Bcrypt(app)

#--- Database ---

def init_db():
    if not os.path.exists("database.db"):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
        """)

        conn.commit()
        conn.close()

init_db()


#--- Helpers ---

def get_user(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(username, password_hash):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO users(username, password_hash) VALUES (?,?)",
              (username, password_hash))
    
    conn.commit()
    conn.close()


#--- Routes ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user(username)

        if user and bcrypt.check_password_hash(user[2], password):
            session["username"] = username
            return redirect("/home")
        
        else:
            return "Wrong username or password"
        
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        try:
            create_user(username, password_hash)
            return redirect("/login")
        except:
            return "Käyttäjänimi on jo olemassa"

    return render_template("register.html")


@app.route("/home")
def home():
    if "username" not in session:
        return redirect("/login")
    
    return render_template("home.html", username=session["username"])


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")


if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.serve(debug=True)