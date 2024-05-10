import keyring
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import db_module
from cryptography.fernet import Fernet, InvalidToken
import pyperclip
import socket

app = Flask(__name__)
app.secret_key = '123'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 60
Session(app)


@app.before_request
def before_request():
    session.modified = True


@app.route('/', methods=['GET', 'POST'])
def auth():
    pwd = db_module.get_pwd()
    if request.method == 'POST':
        passw = request.form['password']
        if passw == pwd:
            session['authenticated'] = True
            return redirect(url_for('decode'))
        else:
            return render_template('login.html', message='Invalid password. Please try again')
    else:
        return render_template('login.html')


@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if not session.get('authenticated'):
        return redirect(url_for('auth'))

    if request.method == 'POST':
        if 'db_name' in request.form:
            try:
                pwd = db_module.db_pass(request.form['db_name'])
                if pwd:
                    db_module.write_logs(request.form['db_name'], socket.gethostname())
                    key = Fernet(keyring.get_password('vault_key', 'key'))
                    encrypted_message = pwd.encode()
                    decrypted_message = key.decrypt(encrypted_message).decode()
                    pyperclip.copy(decrypted_message)
                    return render_template('decode.html', copy='Скопирован в буфер обмена')
                else:
                    return render_template('decode.html', message='такой нет :)')
            except InvalidToken:
                return render_template('decode.html', message='Ошибка расшифровки')
        else:
            return render_template('decode.html', message='Ошибка')
    else:
        return render_template('decode.html')


if __name__ == '__main__':
    app.run(debug=True)
