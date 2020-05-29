from models import Sentence, Word
from database import db_session
from flask import request
import requests
from urllib import parse
from bs4 import BeautifulSoup
from konlpy.tag import Hannanum


# API 5
# 문장 받고 변환 되면 형태소 분석해서 word table 안에 insert
# 1. sentenceData를 공백 기준으로 split 후 표준발음으로 변환. 변환되면 다시 합쳐서 표준발음 문장으로 만든다
# 2. 변환 안되면 "sentence cannot be converted" 반환

def insSentenceControl():
    if (request.method == 'POST'):
        sentence_data = request.form['sentenceData']  # 프론트에서 받은 문장Data
        standard = ""  # 표준발음

        # 문장이 중복되면 "duplicate sentence" 반환
        for sen in db_session.query(Sentence).filter(Sentence.sentenceData == sentence_data):
            return "duplicate sentence"

        # 부산대 표준발음 변환기
        url = parse.urlparse \
            ("http://pronunciation.cs.pusan.ac.kr/pronunc2.asp?text1=안녕하세요&submit1=확인하기")
        # url parse
        qs = dict(parse.parse_qsl(url.query))

        # sentence_data를 공백 기준으로(어절로) split 후 표준발음으로 변환. 변환되면 다시 합쳐서
        standard_lst = []  # 어절로 나눈 표준발음 list
        # sentence_data를 어절로 나누어서 sentence_data_split에 저장
        sentence_data_split = sentence_data.split(" ")
        for sen_data in sentence_data_split:
            qs['text1'] = sen_data
            url = url._replace(query=parse.urlencode(qs, encoding='euc-kr'))
            new_url = parse.urlunparse(url)

            # 표준발음 변환기에서 표준발음 가져오기
            html = requests.get(new_url).content
            bs = BeautifulSoup(html, 'html.parser')

            # 표준 발음으로 변환할 수 없는 경우 "sentence cannot be converted" 반환
            if bs.body == None:
                return "sentence cannot be converted"

            # 표준발음으로 변환할 수 있는 경우
            else:
                search = bs.find_all('td', attrs={'class': 'td2'})
                search_standard = search[2].text[:-1]
                # 발음이 여러개일 때 앞에 것만 가져오기
                search_standard = search_standard.split('/')
                standard_lst.append(search_standard[0])  # 표준발음

        # 표준발음 어절을 문장으로 합침
        standard = " ".join(standard_lst)
        # print(standard)
        # 문장 내용, 표준 발음, userCheck를 sentence table에 insert
        ins_sen = Sentence(sentence_data, standard, True)
        db_session.add(ins_sen)
        db_session.commit()

        # 문장 분석 후 word 테이블에  insert
        han = Hannanum()
        sentence_analyze = han.pos(sentence_data)
        # print(sentence_analyze)

        # word 테이블에 wordData insert
        for word_analyze in sentence_analyze:
            if word_analyze[1] == 'N' or word_analyze[1] == 'P':
                ins_word = Word(ins_sen.sentenceId, word_analyze[0], word_analyze[1])
                db_session.add(ins_word)
                db_session.commit()
                # print(word_analyze[0])

        return "insSentenceControl success"
