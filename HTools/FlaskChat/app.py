from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime
import uuid

app = Flask(__name__)
app.config["SECRET_KEY"] = "flaskchat-secret"

socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)

users = {}
messages = []

@app.route("/")
def index():
    return render_template("index.html")


def get_ip():
    # IP اتصال مستقیم
    return request.remote_addr or "Unknown"


def public_users():
    result = []

    for sid, user in users.items():
        result.append({
            "sid": sid,
            "name": user["name"],
            "ip": user["ip"]
        })

    return result


@socketio.on("join")
def handle_join(data):
    name = str(data.get("name", "")).strip()

    if not name:
        name = "Guest"

    # محدود کردن طول اسم
    name = name[:30]

    sid = request.sid
    ip = get_ip()

    users[sid] = {
        "name": name,
        "ip": ip
    }

    join_room(sid)

    emit(
        "system",
        {
            "text": f"{name} joined the chat",
            "time": datetime.now().strftime("%H:%M:%S")
        },
        broadcast=True
    )

    emit(
        "me",
        {
            "sid": sid,
            "name": name,
            "ip": ip
        }
    )

    emit(
        "users",
        public_users(),
        broadcast=True
    )


@socketio.on("message")
def handle_message(data):
    sender = users.get(request.sid)

    if not sender:
        return

    text = str(data.get("text", "")).strip()

    if not text:
        return

    text = text[:2000]

    target = data.get("target")

    message = {
        "id": str(uuid.uuid4()),
        "sender_sid": request.sid,
        "sender": sender["name"],
        "text": text,
        "time": datetime.now().strftime("%H:%M:%S")
    }

    # چت خصوصی
    if target and target in users:

        message["private"] = True
        message["target"] = target

        emit(
            "message",
            message,
            room=request.sid
        )

        emit(
            "message",
            message,
            room=target
        )

    # چت عمومی
    else:
        message["private"] = False

        emit(
            "message",
            message,
            broadcast=True
        )


@socketio.on("disconnect")
def handle_disconnect():

    user = users.pop(request.sid, None)

    if user:

        emit(
            "system",
            {
                "text": f'{user["name"]} left the chat',
                "time": datetime.now().strftime("%H:%M:%S")
            },
            broadcast=True
        )

        emit(
            "users",
            public_users(),
            broadcast=True
        )


if __name__ == "__main__":
    print("")
    print("===================================")
    print("       ⚡ FlaskChat v1.0")
    print("===================================")
    print("Local:   http://127.0.0.1:5000")
    print("Network: http://YOUR-IP:5000")
    print("===================================")
    print("")

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=False
    )
