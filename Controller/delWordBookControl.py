from models import WordBook
from database import db_session
from flask import request

# API9
# wordbookId 받아서 wordbook 테이블에 있는 데이터 삭제
def delWordBookControl():
    if (request.method == 'POST'):
        wordbookId = request.form['wordbookId']

        # WordBook table 에서 해당 wordbookId row 삭제
        db_session.query(WordBook).filter(WordBook.wordbookId == wordbookId).\
            delete(synchronize_session=False)
        db_session.commit()
    return "delWordBookConrol Success"