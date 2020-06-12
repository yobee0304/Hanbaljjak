from models import WordBook
from database import db_session
from flask import request, jsonify
from konlpy.tag import Hannanum


# API8
# wordData를 받아서 wordbook 테이블에 단어 등록
# 중복검사
# TODO 검토 필요
"""
* word 테이블과 wordbook 테이블의 wordData에는 “맑”이 저장되어야 한다.

안드에서 “맑습니다”를 “맑”으로 바꿔서 보낸다.
or
안드에서 “맑습니다” 보내고 서버에서 “맑”으로 바꿔서 테이블에 저장한다.

"""
def insWordBookControl():
    if (request.method == 'POST'):
        word_data = request.form['wordData']
        wordbook_dict = {"wordbookId": 0, "wordData": ""}

        # 중복검사
        for wd in db_session.query(WordBook).filter(WordBook.wordData == word_data):
            return jsonify(
                message="duplicate word"
            )

        # wordData를 받아서 wordbook 테이블에 단어 등록
        ins_wordbook = WordBook(word_data)
        db_session.add(ins_wordbook)
        db_session.commit()

        for wordbook_entry in db_session.query(WordBook).filter(WordBook.wordData == word_data):
            wordbook_dict["wordbookId"] = wordbook_entry.wordbookId
            wordbook_dict["wordData"] = wordbook_entry.wordbookData


    return jsonify(
        message="insWordBookControl Success",
        newWordBook=wordbook_dict
    )