from flask import Flask, render_template
from scanner import scan_network

app = Flask(__name__)

@app.route("/")
def index():
    try:
        devices = scan_network()
    except Exception as e:
        devices = []
        print(f"Scan Error: {e}")

    return render_template("index.html", devices=devices)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10128, debug=True)
