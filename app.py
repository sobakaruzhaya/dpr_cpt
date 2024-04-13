from flask import Flask, render_template, request, session, redirect
from werkzeug.utils import secure_filename
import os, random
import hashlib, hmac
import sqlite3
from main import main
from flask_session import Session


conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users(
			   id TEXT,
			   username TEXT,
			   first_name TEXT,
			   img_url TEXT,
               foto_count TEXT DEFAULT '0'
)""")
conn.commit()

app = Flask(__name__)
app.secret_key = 'bebe'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

UPLOAD_FOLDER = 'static/img/uploads'

# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'jpg'}
# конфигурируем
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/uploaded', methods=['GET', 'POST'])
# def tickets():
#     if request.method == 'POST':

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/index', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    if request.method == 'POST':
        if 'id' not in session:
            return redirect("/")
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = f"{random.randint(11000, 99999)}" + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main(filename.replace(".jpg", ""))
            c.execute("SELECT * FROM data WHERE img = ?",(filename,))
            data = c.fetchone()
            print(data)
            c.execute("UPDATE users SET `foto_count`=`foto_count`+1 WHERE id = (?)",(session['id'],))
            return render_template("product.html", filename=filename, name=data[1], rub=data[2],kop=data[3])
    return render_template("index.html",session=session)



@app.route('/profile')
def profile():
    tele_id = request.args.get('id', None)
    if ('id' not in session) or (session['id'] == None):
        session['id'] = tele_id
    c.execute("SELECT * FROM users WHERE id = (?)",(session['id'] ,))
    user = c.fetchone()
    if user == None:
        c.execute("""
                INSERT  INTO users (id, username, first_name, img_url) VALUES (?, ?, ?, ?);
            """, (tele_id, request.args.get('username', None), request.args.get('first_name', None), request.args.get('photo_url', None)))
        conn.commit()

    c.execute("SELECT * FROM users WHERE id = (?)",(session['id'],))
    user = c.fetchone()
    return render_template("profile.html",username=user[2],avatar=user[3],colvo=user[4])


@app.route('/login/telegram')
def login_telegram():
    data = {
        'id': request.args.get('id', None),
        'first_name': request.args.get('first_name', None),
        'last_name': request.args.get('last_name', None),
        'username': request.args.get('username', None),
        'photo_url': request.args.get('photo_url', None),
        'auth_date': request.args.get('auth_date', None),
        'hash': request.args.get('hash', None)
    }

    return data

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
