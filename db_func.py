from sqlalchemy.orm import Session
from db_modulev2 import admin_password, sessionsql


def get_pwd(db: Session):
    password_record = db.query(admin_password).first()
    return password_record.password


print(get_pwd(sessionsql))


def db_pass(db_name):
    pass

def write_logs(db_name):
    pass