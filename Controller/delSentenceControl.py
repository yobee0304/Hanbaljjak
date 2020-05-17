from models import Word, Result, Sentence
from database import db_session
from flask import request

# API 6
# <연습 문장 삭제>
# senteceId로 sentece, result, word 테이블 데이터 삭제
def delSentenceControl():
    if (request.method == 'POST'):

        sentenceId = request.form['sentenceId']

        # Word table 에서 해당 sentenceId row 삭제
        db_session.query(Word).filter(Word.sentenceId == sentenceId).\
            delete(synchronize_session=False)
        # Result table 에서 해당 sentenceId row 삭제
        db_session.query(Result).filter(Result.sentenceId == sentenceId). \
            delete(synchronize_session=False)
        # Sentence table 에서 해당 sentenceId row 삭제
        db_session.query(Sentence).filter(Sentence.sentenceId == sentenceId). \
            delete(synchronize_session=False)
        db_session.commit()

    return "delSentenceControl success"
