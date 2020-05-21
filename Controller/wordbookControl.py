import json
from models import WordBook, Word
from database import db_session
import random

# API 7
# wordbook 테이블에 있는 모든 wordbookId와 wordbookData, 추천 문장ID 데이터 반환
def wordbookControl():
    wordbook_lst=[]    # wordbookId, wordbookData, 추천 문장Id 딕셔너리 저장
    recommend_temp = []
    recommend_lst = []    # 추천 문장 ID 최대 3개 저장
    wordbook_dict = {"wordbookId" : 0, "wordData" : "", "recommendSentenceId" : []}

    # wordbook 테이블에서 wordbookId와 wordData 가져오기
    for wb in db_session.query(WordBook).order_by(WordBook.wordbookId):
        wordbook_dict["wordbookId"] = wb.wordbookId
        wordbook_dict["wordData"] = wb.wordData
        # wordData가 같은 sentenceId 가져오기
        for word in db_session.query(Word).filter(Word.wordData == wb.wordData):
            recommend_temp.append(word.sentenceId)

        # sentenceId가 3개 미만일 때 추천 문장id 반환
        if len(recommend_temp) < 3:
            recommend_lst = recommend_temp

        # sentenceId가 3개 이상일 때 추천 문장id 3개 랜덤 선택
        else:
            while len(recommend_lst) != 3:
                item = random.choice(recommend_temp)
                if item not in recommend_lst:
                    recommend_lst.append(item)

        wordbook_dict["recommendSentenceId"] = recommend_lst

        wordbook_lst.append(wordbook_dict.copy())

    return json.dumps(wordbook_lst, ensure_ascii=False)