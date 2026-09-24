#!/data/data/com.termux/files/usr/bin/bash

clear

echo "╔══════════════════════════════════════╗"
echo "║              ⚡ NFCDrop              ║"
echo "║       Nearby File Transfer v14.0     ║"
echo "╚══════════════════════════════════════╝"
echo
echo "📤 SHARE FILE / FOLDER"
echo
echo "Examples:"
echo "  /storage/emulated/0/DataBase.json"
echo "  /storage/emulated/0/MyFolder"
echo "  /storage/emulated/0/DCIM"
echo

# ==============================
# RISH
# ==============================

echo "🔐 Checking Shizuku/rish..."

RISH="$(command -v rish 2>/dev/null)"

if [ -z "$RISH" ]; then
    echo "❌ rish not found."
    exit 1
fi

export RISH_APPLICATION_ID="com.termux"

echo "🟢 Shizuku/rish: OK"
echo

# ==============================
# PATH
# ==============================

read -r -p "📁 Path: " TARGET

TARGET="${TARGET/#\~/$HOME}"

if ! rish -c "[ -e '$TARGET' ]" 2>/dev/null; then
    echo
    echo "❌ Path not found or inaccessible:"
    echo "$TARGET"
    exit 1
fi

echo

# ==============================
# TYPE
# ==============================

if rish -c "[ -d '$TARGET' ]" 2>/dev/null; then

    TYPE="FOLDER"
    NAME="$(basename "$TARGET")"

    echo "╭────────────────────────────────────╮"
    echo "│ 📁 FOLDER                          │"
    echo "╰────────────────────────────────────╯"

else

    TYPE="FILE"
    NAME="$(basename "$TARGET")"

    echo "╭────────────────────────────────────╮"
    echo "│ 📄 FILE                            │"
    echo "╰────────────────────────────────────╯"

fi

echo
echo "📌 Name : $NAME"
echo "📂 Path : $TARGET"

# ==============================
# SIZE USING RISH
# ==============================

if [ "$TYPE" = "FOLDER" ]; then

    SIZE_KB=$(
        rish -c "du -sk '$TARGET' 2>/dev/null | head -n 1 | awk '{print \$1}'" \
        2>/dev/null
    )

    if [ -z "$SIZE_KB" ]; then
        SIZE_KB=0
    fi

    SIZE=$((SIZE_KB * 1024))

else

    SIZE=$(
        rish -c "stat -c '%s' '$TARGET' 2>/dev/null" \
        2>/dev/null
    )

    if [ -z "$SIZE" ]; then
        SIZE=0
    fi

fi

HUMAN_SIZE=$(
python - "$SIZE" <<'PY'
import sys

n = int(sys.argv[1])

units = ["B", "KB", "MB", "GB", "TB"]

i = 0

while n >= 1024 and i < len(units) - 1:
    n /= 1024
    i += 1

print(f"{n:.2f} {units[i]}")
PY
)

echo "📦 Size : $SIZE bytes ($HUMAN_SIZE)"
echo

# ==============================
# CONFIRM
# ==============================

read -r -p "Share this $TYPE? [y/N]: " ANSWER

case "$ANSWER" in
    y|Y|yes|YES)
        ;;
    *)
        echo
        echo "❌ Cancelled."
        exit 0
        ;;
esac

echo

# ==============================
# WIFI IP USING RISH
# ==============================

echo "📡 Detecting Wi-Fi..."

LOCAL_IP=$(
    rish -c 'ip -4 addr show wlan0 2>/dev/null' 2>/dev/null |
    awk '
    $1=="inet" {
        x=$2
        sub("/.*","",x)
        if (x != "127.0.0.1") {
            print x
            exit
        }
    }'
)

if [ -z "$LOCAL_IP" ]; then

    LOCAL_IP=$(
        rish -c 'ip -4 addr show 2>/dev/null' 2>/dev/null |
        awk '
        $1=="inet" {
            x=$2
            sub("/.*","",x)
            if (x != "127.0.0.1") {
                print x
                exit
            }
        }'
    )

fi

if [ -z "$LOCAL_IP" ]; then
    echo
    echo "❌ Wi-Fi IP not found."
    exit 1
fi

echo "🟢 Local Wi-Fi IP: $LOCAL_IP"
echo

# ==============================
# PYTHON SERVER
# ==============================

SERVER="$HOME/.nfc_server.py"

cat > "$SERVER" <<'PYEOF'
import os
import sys
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TARGET = sys.argv[1]
NAME = os.path.basename(TARGET)
RISH = "rish"

class Handler(BaseHTTPRequestHandler):

    def log_message(self, *args):
        pass

    def send_file_stream(self, command, filename, content_length=None):

        try:

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL
            )

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/octet-stream"
            )

            self.send_header(
                "Content-Disposition",
                f'attachment; filename="{filename}"'
            )

            if content_length is not None:
                self.send_header(
                    "Content-Length",
                    str(content_length)
                )

            self.end_headers()

            while True:

                chunk = process.stdout.read(1024 * 1024)

                if not chunk:
                    break

                try:
                    self.wfile.write(chunk)
                except:
                    break

            process.wait()

        except Exception as e:

            print(
                "Transfer error:",
                e,
                flush=True
            )

    def do_GET(self):

        if self.path == "/":

            html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<meta
name="viewport"
content="width=device-width,initial-scale=1"
>

<title>NFCDrop</title>

<style>

body {{
    background:#111;
    color:white;
    font-family:Arial;
    text-align:center;
    padding:40px 15px;
}}

.box {{
    max-width:520px;
    margin:auto;
    background:#222;
    padding:30px;
    border-radius:20px;
}}

a {{
    display:inline-block;
    margin-top:20px;
}}

button {{
    border:0;
    padding:16px 30px;
    border-radius:12px;
    font-size:18px;
}}

.name {{
    font-size:22px;
    word-break:break-word;
}}

</style>

</head>

<body>

<div class="box">

<h1>⚡ NFCDrop</h1>

<div class="name">
{NAME}
</div>

<p>Nearby File Transfer</p>

<a href="/download">
<button>📥 Download</button>
</a>

</div>

</body>

</html>
"""

            data = html.encode()

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                str(len(data))
            )

            self.end_headers()

            self.wfile.write(data)

            return

        # ==========================================
        # FILE
        # ==========================================

        if self.path == "/download":

            # File
            check_file = subprocess.run(
                [
                    RISH,
                    "-c",
                    f"[ -f '{TARGET}' ]"
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            if check_file.returncode == 0:

                command = [
                    RISH,
                    "-c",
                    f"cat '{TARGET}'"
                ]

                self.send_file_stream(
                    command,
                    NAME
                )

                return

            # ======================================
            # FOLDER
            # ======================================

            check_folder = subprocess.run(
                [
                    RISH,
                    "-c",
                    f"[ -d '{TARGET}' ]"
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            if check_folder.returncode == 0:

                parent = os.path.dirname(TARGET)
                folder = os.path.basename(TARGET)

                # tar stream مستقیم از rish
                command_string = (
                    f"cd '{parent}' && "
                    f"tar -cf - '{folder}'"
                )

                command = [
                    RISH,
                    "-c",
                    command_string
                ]

                self.send_file_stream(
                    command,
                    folder + ".tar"
                )

                return

        self.send_response(404)
        self.end_headers()


server = ThreadingHTTPServer(
    ("0.0.0.0", 8080),
    Handler
)

print(
    "NFCDrop server running on 8080",
    flush=True
)

try:
    server.serve_forever()

except KeyboardInterrupt:
    pass
PYEOF

# ==============================
# START
# ==============================

PORT=8080

echo "🚀 Starting NFCDrop..."

python "$SERVER" "$TARGET" &
PID=$!

sleep 2

if ! kill -0 "$PID" 2>/dev/null; then
    echo
    echo "❌ Server failed."
    exit 1
fi

clear

echo "╔══════════════════════════════════════╗"
echo "║              ⚡ NFCDrop              ║"
echo "║       Nearby File Transfer v14.0     ║"
echo "╚══════════════════════════════════════╝"
echo
echo "🟢 SERVER ONLINE"
echo
echo "📌 Name : $NAME"
echo "📦 Size : $SIZE bytes"
echo "💾 Size : $HUMAN_SIZE"
echo
echo "📡 Wi-Fi IP : $LOCAL_IP"
echo "🔌 Port     : $PORT"
echo
echo "🌐 SHARE LINK:"
echo
echo "   http://$LOCAL_IP:$PORT"
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
echo "📱 Open this link on the other device."
echo "📥 Press Download."
echo
echo "📁 Folder → downloaded as .tar"
echo
echo "🛑 Press ENTER to stop."
echo

read -r

kill "$PID" 2>/dev/null
wait "$PID" 2>/dev/null

echo
echo "🛑 NFCDrop stopped."
