CREATE OR REPLACE FUNCTION random_data()
RETURNS void AS
$$
BEGIN
    DECLARE
        random_password TEXT;
    BEGIN
        random_password := substr(md5(random()::text), 0, 10);
        
        update admin_passwords
        set password = random_password
        where id = (select id from admin_passwords);
    END;
END;
$$
LANGUAGE plpgsql;


SELECT random_data();

select *
from admin_passwords

delete from admin_passwords


CREATE OR REPLACE FUNCTION update_prev_password()
RETURNS TRIGGER AS
$$
BEGIN
    IF OLD.password IS NOT NULL THEN
        NEW.prev_password := OLD.password;
    END IF;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER before_password_update
BEFORE UPDATE ON admin_passwords
FOR EACH ROW
EXECUTE FUNCTION update_prev_password();


DROP TRIGGER IF EXISTS before_password_update ON admin_passwords;














@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if not session.get('authenticated'):
        return redirect(url_for('auth'))
    db_names = vault.Secrets.read_keys()
    try:
        if request.method == 'POST':
            env_name = request.form.get('env_name')
            db_name = request.form.get('db_name')
            if db_name:
                try:
                    db_name = db_name.lower()
                    pwd = vault.Secrets.read_secret(db_name)
                    if pwd:
                        db_module.write_logs(db_name, socket.gethostname())
                        pyperclip.copy(pwd)
                        redis_module.redis_expire(db_name, 30)
                        return render_template('decode.html', copy='Copied to clipboard.')
                    else:
                        return render_template('decode.html', message='Not found.')
                except InvalidToken:
                    return render_template('decode.html', message='Decryption error.')
            else:
                return render_template('decode.html', message='Database name is required.')
    except Exception as e:
        return render_template('decode.html', message='Not found.')

    return render_template('decode.html', db_names=db_names)

<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="static/style/style_for_decode.css">
    <title>decode</title>
</head>
<body>
    <form method="post">
        <label for="env_name">Environment Name:</label>
        <label for="db_name">Database Name:</label>
        <select id="env_name" name="env_name">
            <option value="test">test</option>
            <option value="prod">prod</option>
            <input type="submit" value="Выбрать">
        </select>
        <select id="db_name" name="db_name">
            <option value="">Select a database</option>
            {% for db_name in db_names %}
            <option value="{{ db_name }}">{{ db_name }}</option>
            {% endfor %}
        </select>
        <br><br>
        <input type="submit" value="Get Password">
        {% if message %}
        <p style="color: red;">{{ message }}</p>
        {% endif %}
    </form>
    {% if copy %}
     <p style="text-align: center;">{{ copy }}</p>
    {% endif %}

    <script>
        setTimeout(function() {
            window.location.href = "/";
        }, 60000);
    </script>
</body>
</html>


