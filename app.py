from flask import Flask, flash, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import os, random
import hashlib, hmac
import sqlite3
from main import main
from flask_session import Session


conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()



app = Flask(__name__)
app.secret_key = 'bebe'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

UPLOAD_FOLDER = 'static/img/uploads'

# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# конфигурируем
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/uploaded', methods=['GET', 'POST'])
# def tickets():
#     if request.method == 'POST':



@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = f"{random.randint(11000, 99999)}" + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main(filename.replace(".jpg", ""))
            c.execute("SELECT * FROM data WHERE img = ?",(filename,))
            data = c.fetchone()
            print(data)
            return render_template("uploaded.html", filename=filename, name=data[1], rub=data[2],kop=data[3])
    return render_template("main.html",session=session)
@app.route('/profile')
def profile():
    tele_id = request.args.get('id', None)
    c.execute("""
            INSERT OR REPLACE INTO users (id, username, first_name, img_url) VALUES (?, ?, ?, ?);
        """, (tele_id, request.args.get('username', None), request.args.get('first_name', None), request.args.get('photo_url', None)))
    conn.commit()
    session['id'] = tele_id
    return render_template("profile.html")


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
