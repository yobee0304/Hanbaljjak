import json
from models import WordBook, Word, Sentence
from database import db_session
import random


# API 7
# wordbook 테이블에 있는 모든 wordbookId와 wordbookData, 추천 문장 object 1개 반환
def wordbookControl():
    wordbook_lst = []    # wordbookId, wordbookData, 추천 문장 object 저장
    recommend_sen_id_lst = []    # 추천 문장 후보 ID 저장
    sentence_dict = {"sentenceId" : 0, "sentenceData" : "", "standard" : ""}
    wordbook_dict = {"wordbookId" : 0, "wordData" : "", "recommend" : sentence_dict}

    # wordbook 테이블에서 wordbookId와 wordData 가져오기
    for wordbook_entry in db_session.query(WordBook).order_by(WordBook.wordbookId):
        wordbook_dict["wordbookId"] = wordbook_entry.wordbookId
        #wordbook_dict["wordData"] = wordbook_entry.wordData

        # wordData가 같은 sentenceId(=추천 문장 후보 ID) 가져오기
        for word_entry in db_session.query(Word).\
                filter(Word.wordData == wordbook_entry.wordData):
            recommend_sen_id_lst.append(word_entry.sentenceId)
            # 용언일때 "다" 붙이기
            if word_entry.type == 'P':
                wordbook_dict["wordData"] = wordbook_entry.wordData + "다"

            # 체언일 때
            else:
                wordbook_dict["wordData"] = wordbook_entry.wordData

        # 추천문장 후보 ID list(recommend_sen_id_lst)가 empty가 아니면 랜덤으로 하나 선택
        if recommend_sen_id_lst:
            sentence_dict["sentenceId"] = random.choice(recommend_sen_id_lst)
            # 선택된 sentenceId로 sentenceData, standard 가져오기
            for sen_entry in db_session.query(Sentence).\
                    filter(Sentence.sentenceId == sentence_dict["sentenceId"]):
                sentence_dict["sentenceData"] = sen_entry.sentenceData
                sentence_dict["standard"] = sen_entry.standard

        # wordbook 테이블에 있는 단어가 word, sentence 테이블에는 없는 경우
        # wordbook 테이블에 있는 그대로 반환하고
        # 추천문장은 {"senteneId"=-1, sentenceData="", standard=""} 반환
        else:
            sentence_dict["sentenceId"] = -1
            sentence_dict["sentenceData"] = ""
            sentence_dict["standard"] = ""
            wordbook_dict["wordData"] = wordbook_entry.wordData

        wordbook_dict["recommend"] = sentence_dict.copy()
        wordbook_lst.append(wordbook_dict.copy())
        recommend_sen_id_lst = []

    return json.dumps(wordbook_lst, ensure_ascii=False)