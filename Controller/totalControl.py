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
	most_lst = []
	recommend_temp = []
	recommend_lst = []
	recent_lst = []

	# 가장 많이 틀린 음소와 umb 최대 3개
	for most in db_session.query(Record).order_by(Record.count.desc()).limit(3):
		most_lst.append([most.recordData, most.type])

	# 많이 틀린 음소 3개의 추천문장ID 1개씩 총 3개
	for rec in db_session.query(Phoneme).filter(Phoneme.phonemeData == most_lst[0][0]). \
			filter(Phoneme.type == most_lst[0][1]):
		recommend_temp.append(rec.sentenceId)

	for rec in db_session.query(Phoneme).filter(Phoneme.phonemeData == most_lst[1][0]). \
			filter(Phoneme.type == most_lst[1][1]):
		recommend_temp.append(rec.sentenceId)

	for rec in db_session.query(Phoneme).filter(Phoneme.phonemeData == most_lst[2][0]). \
			filter(Phoneme.type == most_lst[2][1]):
		recommend_temp.append(rec.sentenceId)

	recommend_temp = list(set(recommend_temp))
	# 추천 문장 3개 랜덤으로 선택
	recommend_lst.append(random.choice(recommend_temp))
	recommend_lst.append(random.choice(recommend_temp))
	recommend_lst.append(random.choice(recommend_temp))
	recommend_lst = list(set(recommend_lst))

	# 최근에 연습한 문장의 일치율 최대 5개
	for practice in db_session.query(Result).order_by(Result.date).limit(5):
		recent_lst.append(practice.score)

	total = {"mostPhoneme": most_lst, "recommendSentence": recommend_lst, recentScore: recent_lst}

	#print(request.args.get(jsonify))
	# 틀린 음소와 타입, 추천 문장 1개, 문장 일치율 5개 json으로
	return json.dumps(total, ensure_ascii=False)