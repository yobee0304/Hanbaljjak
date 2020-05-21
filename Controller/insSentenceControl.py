from models import Sentence, Word
from database import db_session
from flask import request
import requests
from urllib import parse
from bs4 import BeautifulSoup
from konlpy.tag import Hannanum


# API 5
# 문장 받고 변환 되면 형태소 분석해서 word table 안에 insert
# 1. sentenceData를 공백 기준으로 split 후 표준발음으로 변환. 변환되면 다시 합쳐서 json
# 2. 변환 안되면 "sentence cannot be converted" 반환

def insSentenceControl():
    if (request.method == 'POST'):
        sentenceData = request.form['sentenceData']  # 프론트에서 받은 문장Data
        standard = ""  # 표준발음

        # 문장이 중복되면 "duplicate sentence" 반환
        for sen in db_session.query(Sentence).filter(Sentence.sentenceData == sentenceData):
            return "duplicate sentence"

        # 부산대 표준발음 변환기
        url = parse.urlparse \
            ("http://pronunciation.cs.pusan.ac.kr/pronunc2.asp?text1=안녕하세요&submit1=확인하기")
        # url parse
        qs = dict(parse.parse_qsl(url.query))

        # sentenceData를 공백 기준으로 split 후 표준발음으로 변환. 변환되면 다시 합쳐서
        standard_lst = []
        sentenceDataSplit = sentenceData.split(" ")
        for senDSEntry in sentenceDataSplit:
            qs['text1'] = senDSEntry
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
                # print(standard)

        # 문장 내용, 표준 발음, check를 sentence table에 insert
        standard = " ".join(standard_lst)
        new_sen = Sentence(sentenceData, standard, True)
        db_session.add(new_sen)
        db_session.commit()

        # 문장 분석 후 word 테이블에  insert
        # 명사만 word 테이블에 insert
        han = Hannanum()
        senAnalyze = han.nouns(sentenceData)

        # word 테이블에 wordData insert
        for noun in senAnalyze:
            new_word = Word(new_sen.sentenceId, noun, 'N')
            db_session.add(new_word)
            db_session.commit()

        return "insSentenceControl success"
