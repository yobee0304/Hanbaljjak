import json
from models import WordBook, Word, Sentence
from database import db_session
from flask import request
from konlpy.tag import Hannanum

# API 7
# wordbook 테이블에 있는 모든 wordbookId와 wordbookData, 추천 문장 object 1개 반환
def getWordbook():
    word_lst = []
    word_dict = {"wordbookId": 0, "wordData": ""}

    for wd in db_session.query(WordBook).order_by(WordBook.wordbookId):
        word_dict["wordbookId"] = wd.wordbookId
        word_dict["wordData"] = wd.wordData
        word_lst.append(word_dict.copy())

    return json.dumps(word_lst, ensure_ascii=False)

# API 7-1
def getSentenceByWord():
    if(request.method == 'POST'):

        hannanum = Hannanum()
        word_data = hannanum.pos(request.form['wordData'])[0][0]

        # print(word_data)
        sentence_dict = {"sentenceId": 0, "sentenceData": "", "standard": ""}
        sentence_id_list = []
        sentence_list = []

        for wd in db_session.query(Word).order_by(Word.wordId).filter(Word.wordData == word_data):
            sentence_id_list.append(wd.sentenceId)

        # print(sentence_id_list)
        for sid in sentence_id_list:
            sentence = db_session.query(Sentence).filter(Sentence.sentenceId == sid).first()
            sentence_dict["sentenceId"] = sentence.sentenceId
            sentence_dict["sentenceData"] = sentence.sentenceData
            sentence_dict["standard"] = sentence.standard
            sentence_list.append(sentence_dict.copy())

        return json.dumps(sentence_list, ensure_ascii=False)
