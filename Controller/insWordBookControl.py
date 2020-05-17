from models import WordBook
from database import db_session
from flask import request

# API8
# wordData를 받아서 wordbook 테이블에 단어 등록
# 중복검사
def insWordBookControl():
    if (request.method == 'POST'):
        wordData = request.form['wordData']

        # 중복검사
        for wd in db_session.query(WordBook).filter(WordBook.wordData == wordData):
            return "duplicate word"

        # wordData를 받아서 wordbook 테이블에 단어 등록
        wb = WordBook(wordData)
        db_session.add(wb)
        db_session.commit()

    return "insWordBookControl Success"