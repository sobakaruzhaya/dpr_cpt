from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os, random
import hashlib, hmac
import sqlite3
from detection import detect_price






app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_TYPE'] = 'filesystem'

UPLOAD_FOLDER = 'static/img/uploads'

# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# создаем экземпляр приложения
app = Flask(__name__)
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
            price = detect_price(url_for('static', filename="img/uploads/" + filename))
            return render_template("uploaded.html", filename=filename)
    return render_template("main.html")
@app.route('/profile')
def profile():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
            INSERT OR REPLACE INTO users (id, username, first_name, img_url) VALUES (?, ?, ?, ?);
        """, (request.args.get('id', None), request.args.get('username', None), request.args.get('first_name', None), request.args.get('photo_url', None)))
    conn.commit()
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
