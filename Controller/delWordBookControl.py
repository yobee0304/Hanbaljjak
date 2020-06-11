from models import WordBook
from database import db_session
from flask import request, jsonify


# API9
# wordbook_id_lst 받아서 wordbook 테이블에 있는 데이터 삭제
def delWordBookControl():
    if (request.method == 'POST'):
        wordbook_id_lst = request.form.getlist('wordbookId')

        for wordbook_id in wordbook_id_lst:
            # WordBook table 에서 해당 wordbookId row 삭제
            db_session.query(WordBook).filter(WordBook.wordbookId == wordbook_id).\
                delete(synchronize_session=False)

            db_session.commit()

    return jsonify(
        message="delWordBookControl Success"
    )