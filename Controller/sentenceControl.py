from flask import request, jsonify
import json
from models import Sentence
from database import db_session

# API1
# 연습 문장 id, 연습문장 텍스트, 연습 문장의 표준 발음 텍스트 20개씩인데 일단 전부
def sentenceControl():
	sentence_lst = []
	sentence_dict = {"sentenceId": 0, "sentenceData": "", "standard": ""}

	for sen in db_session.query(Sentence).order_by(Sentence.sentenceId):
		# sentence_lst.append([sen.sentenceId, sen.sentenceData, sen.standard])
		sentence_dict["sentenceId"] = sen.sentenceId
		sentence_dict["sentenceData"] = sen.sentenceData
		sentence_dict["standard"] = sen.standard
		sentence_lst.append(sentence_dict.copy())

	#print(request.args.get(sentence_lst))
	return json.dumps(sentence_lst, ensure_ascii=False)