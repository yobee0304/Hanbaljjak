from models import Phoneme, Result, Record, Sentence
from database import db_session

# API3
"""
사용자의 전체적인 결과값들을 클라이언트에 전송한다. 
결과값은 가장 많이 틀린 음소(umb 포함?) 최대 3개, 
그에 맞는 추천 문장 각각 1개, 
최근에 연습한 문장의 일치율 최대 5개이다.
"""
def totalControl():
    return 'total success'
	
def totalResult():
    most_lst = []
	recommend_lst = []
	recent_lst = []

	# 가장 많이 틀린 음소(umb 포함?) 최대 3개
	for most in db_session.query(Record).order_by(Record.count.desc()).limit(3):
		#most_lst.append([most.recordId, most.recordData, most.type, most.count])
		most_lst.append(most.recordData)

	# 많이 틀린 음소 3개의 추천문장 1개씩
	# TODO

	#최근에 연습한 문장의 일치율 최대 5개
	for practice in db_session.query(Result).order_by(Result.date).limit(5):
		recent_lst.append(practice.score)


	return most_lst, recommend_lst, recent_lst
	