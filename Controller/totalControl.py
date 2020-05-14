from models import Phoneme, Result, Record, Sentence
from database import db_session
from flask import json
import random

# API3
"""
사용자의 전체적인 결과값들을 클라이언트에 전송한다. 
결과값은 가장 많이 틀린 음소(umb 포함?) 최대 3개, 
그에 맞는 추천 문장 각각 1개, 
최근에 연습한 문장의 일치율 최대 5개이다.
"""
def totalControl():
	most_lst = []
	recommend_temp = []
	recommend_lst = []
	recent_lst = []

	# 가장 많이 틀린 음소와 umb 최대 3개
	for most in db_session.query(Record).order_by(Record.count.desc()).limit(3):
		most_lst.append([most.recordData, most.type])

	# 많이 틀린 음소 3개의 추천문장ID 1개씩 총 3개
	for i in range(0, 3):
		for rec in db_session.query(Phoneme).filter(Phoneme.phonemeData == most_lst[i][0]). \
				filter(Phoneme.type == most_lst[i][1]):
			if rec.sentenceId not in recommend_temp:
				recommend_temp.append(rec.sentenceId)

	# 추천 문장 3개 랜덤으로 선택
	if len(recommend_temp) < 3:
		while len(recommend_lst) != len(recommend_temp):
			item = random.choice(recommend_temp)
			if item not in recommend_lst:
				recommend_lst.append(item)
	else:
		while len(recommend_lst) != 3:
			item = random.choice(recommend_temp)
			if item not in recommend_lst:
				recommend_lst.append(item)

	# 최근에 연습한 문장의 일치율 최대 5개
	for practice in db_session.query(Result).order_by(Result.date).limit(5):
		recent_lst.append(practice.score)

	total = {"mostPhoneme": most_lst, "recommendSentence": recommend_lst, "recentScore": recent_lst}

	#print(request.args.get(jsonify))
	# 틀린 음소와 타입, 추천 문장 1개, 문장 일치율 5개 json으로
	return json.dumps(total, ensure_ascii=False)