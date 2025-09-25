# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import bcrypt, json, os
import eventlet
import eventlet.wsgi

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

socketio = SocketIO(app, async_mode="threading")

USERS_FILE = "users.json"
clients = {}  

# ---------------- User DB ----------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    # migration: convert old-format users to new format automatically
    migrated = False
    for u, data in list(users.items()):
        if isinstance(data, str):
            users[u] = {"password": data, "is_logged_in": False}
            migrated = True
    if migrated:
        save_users(users)

    return users

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# reset all logins on server start (prevents stale locks)
def reset_all_logins():
    users = load_users()
    changed = False
    for u, d in users.items():
        if isinstance(d, dict) and d.get("is_logged_in"):
            users[u]["is_logged_in"] = False
            changed = True
    if changed:
        save_users(users)

reset_all_logins()

# ---------------- Routes ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        user = users.get(username)

        if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
            if user.get("is_logged_in", False):
                return render_template("login.html", error="User already logged in elsewhere!")
            user["is_logged_in"] = True
            save_users(users)
            session["username"] = username
            return redirect(url_for("chat"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        if username in users:
            return render_template("signup.html", error="User already exists!")

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        users[username] = {"password": hashed_pw, "is_logged_in": False}
        save_users(users)
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("chat.html", username=session["username"])


@app.route("/logout")
def logout():
    username = session.pop("username", None)
    if username:
        users = load_users()
        if username in users:
            users[username]["is_logged_in"] = False
            save_users(users)
    return redirect(url_for("login"))

# ---------------- WebSocket ----------------
@socketio.on("connect")
def handle_connect():
    from flask import request
    username = session.get("username")
    if not username:
        return False
    clients[request.sid] = username
    emit('system', f'{username} joined the chat', broadcast=True)

@socketio.on("message")
def handle_message(msg):
    from flask import request
    username = clients.get(request.sid)
    if msg == "/quit":
        emit('system', f'{username} left the chat', broadcast=True)
        return
    emit('chat', {'username': username, 'message': msg}, broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    from flask import request
    username = clients.pop(request.sid, None)
    if username:
        users = load_users()
        if username in users:
            users[username]["is_logged_in"] = False
            save_users(users)
        emit('system', f'{username} disconnected', broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False, allow_unsafe_werkzeug=True)


