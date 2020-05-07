from models import Sentence
from database import db_session

# API1
# 연습 문장 id, 연습문장 텍스트, 연습 문장의 표준 발음 텍스트 20개씩인데 일단 전부
def sentenceControl():
    return 'sentence success'
	
def sentenceInfo():
    
	sentence_lst = []

	for instance in db_session.query(Sentence).order_by(Sentence.sentenceId):
		sentence_lst.append([instance.sentenceId, instance.sentenceData, instance.standard])
	
	return sentence_lst
