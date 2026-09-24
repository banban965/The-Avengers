from flask import (
    Flask,
    request,
    render_template_string,
    redirect,
    url_for,
    session,
    abort
)
import json
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# برای محیط واقعی این مقدار را با یک SECRET امن عوض کنید.
app.secret_key = os.environ.get(
    "USERCOLLECTOR_SECRET",
    "change-this-secret-key"
)

DATABASE = "DataBase.json"

# رمز Admin را از Environment بگیر.
# مثال:
# export ADMIN_PASSWORD='your-password'
ADMIN_PASSWORD = os.environ.get(
    "USERCOLLECTOR_ADMIN_PASSWORD",
    "change-me"
)


# =========================================================
# DATABASE
# =========================================================

def load_database():
    if not os.path.exists(DATABASE):
        return []

    try:
        with open(DATABASE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data if isinstance(data, list) else []

    except (OSError, json.JSONDecodeError):
        return []


def save_database(data):
    temp = DATABASE + ".tmp"

    with open(temp, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

    os.replace(temp, DATABASE)


# =========================================================
# ADMIN AUTH
# =========================================================

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))

        return func(*args, **kwargs)

    return wrapper


# =========================================================
# USER PAGE
# =========================================================

USER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>UserCollector</title>

<style>

* {
    box-sizing: border-box;
    font-family: Arial, sans-serif;
}

body {
    margin: 0;
    padding: 20px;
    min-height: 100vh;
    background: #10131a;
    color: white;
}

.container {
    max-width: 600px;
    margin: auto;
}

.header {
    text-align: center;
    margin-bottom: 20px;
}

.header h1 {
    margin-bottom: 5px;
}

.header p {
    color: #8e99aa;
}

.card {
    background: #191e29;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,.3);
}

label {
    display: block;
    margin-top: 15px;
    margin-bottom: 7px;
    color: #c3cad6;
}

input,
select {
    width: 100%;
    padding: 13px;
    border: 0;
    outline: 0;
    border-radius: 10px;
    background: #252c39;
    color: white;
    font-size: 15px;
}

input:focus,
select:focus {
    outline: 2px solid #4d8cff;
}

.consent {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 20px;
}

.consent input {
    width: auto;
}

button {
    width: 100%;
    margin-top: 20px;
    padding: 14px;
    border: 0;
    border-radius: 12px;
    background: #4d8cff;
    color: white;
    font-size: 16px;
    font-weight: bold;
}

.success {
    background: #164d2b;
    color: #7dffae;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 15px;
}

.footer {
    text-align: center;
    margin-top: 20px;
    color: #697386;
    font-size: 12px;
}

.admin-link {
    display: block;
    text-align: center;
    margin-top: 15px;
    color: #8fb4ff;
    text-decoration: none;
}

</style>

</head>

<body>

<div class="container">

<div class="header">
    <h1>UserCollector</h1>
    <p>Profile Information</p>
</div>

{% if success %}

<div class="success">
    ✓ Information saved successfully
</div>

{% endif %}

<div class="card">

<form method="POST">

<label>Email</label>
<input
    type="email"
    name="email"
    placeholder="example@email.com"
>

<label>Username</label>
<input
    type="text"
    name="username"
    placeholder="Your username"
>

<label>First Name</label>
<input
    type="text"
    name="first_name"
    placeholder="First name"
>

<label>Last Name</label>
<input
    type="text"
    name="last_name"
    placeholder="Last name"
>

<label>Your Device</label>
<input
    type="text"
    name="device"
    placeholder="Example: Samsung Galaxy A14"
>

<label>Best Music</label>
<input
    type="text"
    name="best_music"
    placeholder="Favorite music"
>

<label>Best YouTube User</label>
<input
    type="text"
    name="best_youtube_user"
    placeholder="Favorite creator"
>

<label>Instagram Installed</label>

<select name="instagram_installed">
    <option value="Unknown">Unknown</option>
    <option value="Yes">Yes</option>
    <option value="No">No</option>
</select>

<div class="consent">

<input
    type="checkbox"
    name="consent"
    required
>

<span>
    I agree to save this information.
</span>

</div>

<button type="submit">
    Submit
</button>

</form>

</div>

<a class="admin-link"
   href="/admin">
   Admin Panel
</a>

<div class="footer">
    UserCollector
</div>

</div>

</body>
</html>
"""


# =========================================================
# ADMIN LOGIN
# =========================================================

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Admin Login</title>

<style>

* {
    box-sizing: border-box;
    font-family: Arial, sans-serif;
}

body {
    margin: 0;
    min-height: 100vh;
    background: #10131a;
    color: white;

    display: flex;
    justify-content: center;
    align-items: center;

    padding: 20px;
}

.card {
    width: 100%;
    max-width: 400px;

    background: #191e29;

    padding: 25px;

    border-radius: 18px;
}

h1 {
    text-align: center;
}

input {
    width: 100%;

    padding: 14px;

    margin-top: 15px;

    border: 0;
    outline: 0;

    border-radius: 10px;

    background: #252c39;

    color: white;
}

button {
    width: 100%;

    margin-top: 15px;

    padding: 14px;

    border: 0;

    border-radius: 10px;

    background: #4d8cff;

    color: white;

    font-weight: bold;
}

.error {
    background: #542020;

    color: #ff9b9b;

    padding: 10px;

    border-radius: 8px;

    margin-top: 15px;
}

</style>

</head>

<body>

<div class="card">

<h1>Admin Login</h1>

<form method="POST">

<input
    type="password"
    name="password"
    placeholder="Admin password"
    required
>

<button type="submit">
    Login
</button>

</form>

{% if error %}

<div class="error">
    {{ error }}
</div>

{% endif %}

</div>

</body>
</html>
"""


# =========================================================
# ADMIN DASHBOARD
# =========================================================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Admin Dashboard</title>

<style>

* {
    box-sizing: border-box;
    font-family: Arial, sans-serif;
}

body {
    margin: 0;

    background: #10131a;

    color: white;

    padding: 20px;
}

.container {
    max-width: 1000px;
    margin: auto;
}

.header {
    display: flex;

    justify-content: space-between;

    align-items: center;

    gap: 10px;

    margin-bottom: 20px;
}

.logout {
    background: #722c2c;

    color: white;

    text-decoration: none;

    padding: 10px 14px;

    border-radius: 9px;
}

.stats {
    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(180px, 1fr));

    gap: 15px;

    margin-bottom: 20px;
}

.stat {
    background: #191e29;

    padding: 20px;

    border-radius: 15px;
}

.stat-number {
    font-size: 30px;

    font-weight: bold;
}

.users {
    display: grid;

    gap: 15px;
}

.user {
    background: #191e29;

    padding: 18px;

    border-radius: 15px;
}

.row {
    padding: 7px 0;

    border-bottom:
        1px solid #29303d;
}

.row:last-child {
    border-bottom: 0;
}

.key {
    color: #8fa0b8;
}

.delete {
    display: inline-block;

    margin-top: 12px;

    padding: 9px 13px;

    border-radius: 8px;

    background: #722c2c;

    color: white;

    text-decoration: none;
}

.empty {
    text-align: center;

    background: #191e29;

    padding: 30px;

    border-radius: 15px;

    color: #8e99aa;
}

</style>

</head>

<body>

<div class="container">

<div class="header">

<div>
    <h1>Admin Dashboard</h1>
    <p>Registered users</p>
</div>

<a
    class="logout"
    href="/admin/logout">
    Logout
</a>

</div>

<div class="stats">

<div class="stat">
    <div class="stat-number">
        {{ users|length }}
    </div>

    <div>
        Users
    </div>
</div>

<div class="stat">
    <div class="stat-number">
        {{ database_size }}
    </div>

    <div>
        Database entries
    </div>
</div>

</div>

{% if users %}

<div class="users">

{% for user in users %}

<div class="user">

<div class="row">
<span class="key">Email:</span>
{{ user.get("email", "") }}
</div>

<div class="row">
<span class="key">Username:</span>
{{ user.get("username", "") }}
</div>

<div class="row">
<span class="key">First Name:</span>
{{ user.get("first_name", "") }}
</div>

<div class="row">
<span class="key">Last Name:</span>
{{ user.get("last_name", "") }}
</div>

<div class="row">
<span class="key">Device:</span>
{{ user.get("device", "") }}
</div>

<div class="row">
<span class="key">Best Music:</span>
{{ user.get("best_music", "") }}
</div>

<div class="row">
<span class="key">YouTube:</span>
{{ user.get("best_youtube_user", "") }}
</div>

<div class="row">
<span class="key">Instagram:</span>
{{ user.get("instagram_installed", "Unknown") }}
</div>

<div class="row">
<span class="key">Saved:</span>
{{ user.get("saved_at", "") }}
</div>

<a
    class="delete"
    href="/admin/delete/{{ loop.index0 }}"
    onclick="return confirm('Delete this user?');">
    Delete
</a>

</div>

{% endfor %}

</div>

{% else %}

<div class="empty">
    No users registered.
</div>

{% endif %}

</div>

</body>
</html>
"""


# =========================================================
# USER SUBMIT
# =========================================================

@app.route("/", methods=["GET", "POST"])
def index():

    success = False

    if request.method == "POST":

        if not request.form.get("consent"):
            abort(400, "Consent is required.")

        user = {
            "email": request.form.get(
                "email", ""
            ).strip(),

            "username": request.form.get(
                "username", ""
            ).strip(),

            "first_name": request.form.get(
                "first_name", ""
            ).strip(),

            "last_name": request.form.get(
                "last_name", ""
            ).strip(),

            "device": request.form.get(
                "device", ""
            ).strip(),

            "best_music": request.form.get(
                "best_music", ""
            ).strip(),

            "best_youtube_user": request.form.get(
                "best_youtube_user", ""
            ).strip(),

            "instagram_installed": request.form.get(
                "instagram_installed",
                "Unknown"
            ),

            "saved_at": datetime.now().isoformat(
                timespec="seconds"
            )
        }

        database = load_database()

        database.append(user)

        save_database(database)

        success = True

    return render_template_string(
        USER_HTML,
        success=success
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    if session.get("admin_logged_in"):
        return redirect(
            url_for("admin_dashboard")
        )

    error = None

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

        if password == ADMIN_PASSWORD:

            session.clear()

            session["admin_logged_in"] = True

            return redirect(
                url_for("admin_dashboard")
            )

        error = "Invalid admin password."

    return render_template_string(
        LOGIN_HTML,
        error=error
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():

    users = load_database()

    return render_template_string(
        DASHBOARD_HTML,

        users=users,

        database_size=len(users)
    )


# =========================================================
# DELETE USER
# =========================================================

@app.route("/admin/delete/<int:user_id>")
@admin_required
def delete_user(user_id):

    database = load_database()

    if user_id < 0 or user_id >= len(database):
        abort(404)

    database.pop(user_id)

    save_database(database)

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(
        url_for("admin_login")
    )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    if not os.path.exists(DATABASE):
        save_database([])

    print("=" * 50)
    print("              UserCollector")
    print("=" * 50)
    print("User page  : http://127.0.0.1:5000/")
    print("Admin page : http://127.0.0.1:5000/admin")
    print("Database   :", DATABASE)
    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )