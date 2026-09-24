from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os, uuid

BASE=os.path.dirname(os.path.abspath(__file__))
DB=os.path.join(BASE,'database','hdbchat.db')
UPLOADS=os.path.join(BASE,'uploads')
ALLOWED={'png','jpg','jpeg','gif','webp','mp4','webm','mp3','wav','pdf','zip','txt','doc','docx'}
app=Flask(__name__)
app.config['SECRET_KEY']=os.environ.get('HDBCHAT_SECRET','change-this-secret')
app.config['MAX_CONTENT_LENGTH']=32*1024*1024
socketio=SocketIO(app,cors_allowed_origins='*')

def db():
    con = sqlite3.connect(
        DB,
        timeout=15,
        check_same_thread=False
    )
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA busy_timeout=15000")
    return con
def init_db():
    os.makedirs(os.path.dirname(DB),exist_ok=True)
    c=db(); c.executescript('''
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL,text TEXT,file_name TEXT,file_url TEXT,created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
    '''); c.commit(); c.close()

@app.route('/')
def index(): return redirect(url_for('chat') if 'user' in session else url_for('login'))
@app.route('/register',methods=['GET','POST'])
def register():
    error=None
    if request.method=='POST':
        u=request.form.get('username','').strip(); p=request.form.get('password','')
        if len(u)<3 or len(p)<4: error='Username must be 3+ chars and password 4+ chars.'
        else:
            try:
                c=db(); c.execute('INSERT INTO users(username,password) VALUES(?,?)',(u,generate_password_hash(p))); c.commit(); c.close(); return redirect(url_for('login'))
            except sqlite3.IntegrityError: error='Username already exists.'
    return render_template('register.html',error=error)
@app.route('/login',methods=['GET','POST'])
def login():
    error=None
    if request.method=='POST':
        u=request.form.get('username','').strip(); p=request.form.get('password','')
        c=db(); r=c.execute('SELECT * FROM users WHERE username=?',(u,)).fetchone(); c.close()
        if r and check_password_hash(r['password'],p): session['user']=u; return redirect(url_for('chat'))
        error='Invalid username or password.'
    return render_template('login.html',error=error)
@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('login'))
@app.route('/chat')
def chat():
    if 'user' not in session:return redirect(url_for('login'))
    return render_template('chat.html',username=session['user'],version='26.1.2')
@app.route('/history')
def history():
    if 'user' not in session:return jsonify({'error':'login required'}),401
    c=db(); rows=c.execute('SELECT * FROM messages ORDER BY id DESC LIMIT 100').fetchall(); c.close(); return jsonify([dict(x) for x in reversed(rows)])
@app.route('/upload',methods=['POST'])
def upload():
    if 'user' not in session:return jsonify({'error':'login required'}),401
    f=request.files.get('file')
    if not f or not f.filename:return jsonify({'error':'No file'}),400
    ext=f.filename.rsplit('.',1)[-1].lower() if '.' in f.filename else ''
    if ext not in ALLOWED:return jsonify({'error':'File type not allowed'}),400
    safe=secure_filename(f.filename); name=uuid.uuid4().hex+'_'+safe; folder='images' if ext in {'png','jpg','jpeg','gif','webp'} else 'files'
    os.makedirs(os.path.join(UPLOADS,folder),exist_ok=True); f.save(os.path.join(UPLOADS,folder,name)); url=f'/uploads/{folder}/{name}'
    c=db(); cur=c.execute('INSERT INTO messages(username,text,file_name,file_url) VALUES(?,?,?,?)',(session['user'],None,safe,url)); c.commit(); mid=cur.lastrowid; c.close()
    payload={'id':mid,'username':session['user'],'text':None,'file_name':safe,'file_url':url}; socketio.emit('message',payload); return jsonify(payload)
@app.route('/uploads/<folder>/<name>')
def uploaded(folder,name):
    if folder not in {'images','files'}:return 'Not found',404
    return send_from_directory(os.path.join(UPLOADS,folder),name)
@socketio.on('send_message')
def send_message(data):
    if 'user' not in session:return
    text=(data.get('text') or '').strip()
    if not text:return
    c=db(); cur=c.execute('INSERT INTO messages(username,text) VALUES(?,?)',(session['user'],text)); c.commit(); mid=cur.lastrowid; c.close()
    emit('message',{'id':mid,'username':session['user'],'text':text,'file_name':None,'file_url':None},broadcast=True)
@socketio.on('typing')
def typing(data):
    if 'user' in session: emit('typing',{'username':session['user'],'active':bool(data.get('active'))},broadcast=True,include_self=False)
if __name__=='__main__':
    init_db(); socketio.run(app,host='0.0.0.0',port=int(os.environ.get('PORT',5000)),allow_unsafe_werkzeug=True)
