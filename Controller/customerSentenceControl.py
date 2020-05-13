import json
from models import Phoneme, Result, Record, Sentence
from database import db_session

def customerSentenceControl():
    cust_sentence_lst = []
    cust_sentence_dict = {"sentenceId": 0, "sentenceData": "", "standard": ""}

    for sen in db_session.query(Sentence).order_by(Sentence.sentenceId).filter(Sentence.check == True):
        cust_sentence_dict["sentenceId"] = sen.sentenceId
        cust_sentence_dict["sentenceData"] = sen.sentenceData
        cust_sentence_dict["standard"] = sen.standard
        cust_sentence_lst.append(cust_sentence_dict.copy())

    return json.dumps(cust_sentence_lst, ensure_ascii=False)
