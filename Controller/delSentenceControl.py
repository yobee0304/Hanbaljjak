from models import Phoneme, Result, Sentence
from database import db_session
from flask import request


def delSentenceControl():
    if (request.method == 'POST'):

        sentenceId = request.form['sentenceId']

        # Phoneme table 에서 해당 sentenceId row 삭제
        db_session.query(Phoneme).filter(Phoneme.sentenceId == sentenceId). \
            delete(synchronize_session=False)
        # Result table 에서 해당 sentenceId row 삭제
        db_session.query(Result).filter(Result.sentenceId == sentenceId). \
            delete(synchronize_session=False)
        # Sentence table 에서 해당 sentenceId row 삭제
        db_session.query(Sentence).filter(Sentence.sentenceId == sentenceId). \
            delete(synchronize_session=False)
        db_session.commit()

    return "delSentenceControl success"
