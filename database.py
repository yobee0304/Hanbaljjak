from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 로컬 주소로 변경
# mysql+pymysql://'id':'password'@localhost/'DB_name'
engine = create_engine('mysql+pymysql://root:root@localhost/voice', convert_unicode=False)
# TODO 서버 DB 코드 추가
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

conn = engine.connect()

def init_db():

    import models
    Base.metadata.create_all(engine)

    print("init_db")






