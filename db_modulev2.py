from sqlalchemy import create_engine, Column, Integer, String, event, DDL, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

Db_url = DATABASE_URL = 'postgresql+psycopg2://postgres:11355@127.0.0.1/pwd_m'

engine = create_engine(Db_url, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

sessionsql = SessionLocal()


class admin_password(Base):
    __tablename__ = "admin_password"

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(100))
    prev_password = Column(String(100))


class logs(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_of = Column(TIMESTAMP)
    system_name = Column(String(100))


random_password = """
CREATE OR REPLACE FUNCTION random_data()
RETURNS void AS
$$
BEGIN
    DECLARE
        random_password TEXT;
    BEGIN
        random_password := substr(md5(random()::text), 0, 10);
        
        update admin_password
        set password = random_password
        where id = (select id from admin_password);
    END;
END;
$$
LANGUAGE plpgsql;
"""

prev_password = """
CREATE OR REPLACE FUNCTION update_prev_password()
RETURNS TRIGGER AS $$
BEGIN
    NEW.prev_password := OLD.password;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

trg_prev = """
CREATE or replace TRIGGER password_update_trigger
BEFORE INSERT ON admin_password
FOR EACH ROW
EXECUTE FUNCTION update_prev_password();
"""

Base.metadata.create_all(engine)

engine.execute(DDL(random_password))

engine.execute(DDL(prev_password))

engine.execute(DDL(trg_prev))


