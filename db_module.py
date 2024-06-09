import psycopg2
import keyring
import time

def db_connect():
    try:
        conn = psycopg2.connect(
            dbname="passwordM",
            user="postgres",
            password=keyring.get_password('pg', 'pwd'),
            host="127.0.0.1",
            port="5432"
        )
        print("Database connected successfully")

        return conn

    except psycopg2.Error as e:
        print("Ошибка при работе с PostgreSQL:", e)


def get_pwd():
    conn = db_connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('select password from admin_passwords;')
            data = cursor.fetchone()

            if data:
                return data[0]

        except psycopg2.Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

def db_pass(db_name):
    conn = db_connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT actual_password FROM passwords_test_vault WHERE db_name = '{db_name}';")
            data = cursor.fetchone()

            if data:
                return data[0]

        except psycopg2.Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


def write_logs(system_name, computer_name):
    conn = db_connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO logs (date_of, system_name, computer_name) VALUES (NOW(), %s, %s)", (system_name, computer_name ))
            conn.commit()
            print('logs commited')
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

# async def password_changer():
#     conn = db_connect()
#     if conn:
#         try:
#             cursor = conn.cursor()
#             await asyncio.sleep(20)
#             cursor.execute('select random_data()')
#             conn.commit()
#             print('password changed')
#         except (Exception, psycopg2.DatabaseError) as e:
#             print(e)
#         finally:
#             cursor.close()
#             conn.close()


print(get_pwd())
