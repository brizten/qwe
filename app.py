import keyring
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
#import db_module
from cryptography.fernet import Fernet, InvalidToken
import pyperclip
import redis_module
import threading
import db_func
from sqlalchemy.orm import sessionmaker
from db_modulev2 import admin_password, engine, sessionsql


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random value

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 600
Session(app)


@app.before_request
def before_request():
    session.modified = True


@app.route('/', methods=['GET', 'POST'])
def auth():
    pwd = db_func.get_pwd(sessionsql)
    if request.method == 'POST':
        passw = request.form['password']
        if passw == pwd:
            session['authenticated'] = True
            return redirect(url_for('decode'))
        else:
            return render_template('login.html', message='Invalid password. Please try again.')
    return render_template('login.html')


@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if not session.get('authenticated'):
        return redirect(url_for('auth'))

    if request.method == 'POST':
        db_name = request.form.get('db_name')
        if db_name:
            try:
                db_name = db_name.lower()
                pwd = db_func.db_pass(db_name)
                if pwd:
                    db_func.write_logs(db_name)
                    decode_tocopy(pwd)
                    redis_module.redis_expire(db_name, 50)
                    return render_template('decode.html', copy='Copied to clipboard.')
                else:
                    return render_template('decode.html', message='Database not found.')
            except InvalidToken:
                return render_template('decode.html', message='Decryption error.')
        else:
            return render_template('decode.html', message='Database name is required.')
    return render_template('decode.html')


def decode_tocopy(pwd):
    key = Fernet(keyring.get_password('vault_key', 'key'))
    encrypted_message = pwd.encode()
    decrypted_message = key.decrypt(encrypted_message).decode()
    pyperclip.copy(decrypted_message)


if __name__ == '__main__':
    threading.Thread(target=redis_module.monitor_redis, daemon=True).start()
    app.run(debug=True)
