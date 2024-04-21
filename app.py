from flask import Flask, render_template, request, redirect, url_for
import db_module

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def auth():
    pwd = db_module.get_pwd()
    if request.method == 'POST':
        passw = request.form['password']
        if passw == pwd:
            return redirect(url_for('decode'))
        else:
            return render_template('login.html', message='Invalid password. Please try again')
    else:
        return render_template('login.html')


@app.route('/decode')
def decode():
    #декоде пароля
    return render_template('decode.html')


if __name__ == '__main__':
    app.run(debug=True)
