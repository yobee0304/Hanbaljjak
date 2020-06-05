from models import Result, Record, Sentence
from database import db_session
from flask import json


# API3
"""
사용자의 전체적인 결과값들을 클라이언트에 전송한다. 
결과값은 가장 많이 틀린 음소(umb 포함) 최대 3개,
최근에 연습한 문장의 일치율 최대 5개이다.
"""
def totalControl():
	most_lst = []
	recent_lst = []

	# 가장 많이 틀린 음소 최대 3개와 그 타입(u/m/b)
	for most in db_session.query(Record).order_by(Record.count.desc()).\
			filter(Record.count != 0).limit(3):
		most_lst.append([most.recordData, most.recordType])

	# 최근에 연습한 문장의 일치율 최대 5개
	for practice in db_session.query(Result).order_by(Result.resultId.desc()).limit(5):
		recent_lst.append(practice.score)
	#for practice in db_session.query(Result).order_by(Result.date.desc()).limit(5):
		#recent_lst.append(practice.score)
		#print(practice.score)

	recent_lst.reverse()

	total = {"mostPhoneme": most_lst, "recentScore": recent_lst}

	# 틀린 음소와 타입, 최근 문장 일치율 5개 json으로
	return json.dumps(total, ensure_ascii=False)


