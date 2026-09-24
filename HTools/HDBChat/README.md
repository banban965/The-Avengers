# HDBChat v26.1.2

Telegram-style educational web chat built with Flask + Socket.IO.

## Termux
pkg update
pkg install python
cd HDBChat
pip install -r requirements.txt
python app.py

Open http://127.0.0.1:5000

Upload limit: 32 MB per request. Change HDBCHAT_SECRET before public deployment.
