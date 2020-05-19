from models import Sentence
from database import db_session
from flask import request
import requests
from urllib import parse
from bs4 import BeautifulSoup


def insSentenceControl():
    if (request.method == 'POST'):
        sentence = request.form['sentence']
        standard = ""  # 표준발음

        # 문자열이 중복되면 "duplicate sentence" 반환
        for sen in db_session.query(Sentence).filter(Sentence.sentenceData == sentence):
            return "duplicate sentence"

        # 부산대 표준발음 변환기
        url = parse.urlparse \
            ("http://pronunciation.cs.pusan.ac.kr/pronunc2.asp?text1=안녕하세요&submit1=확인하기")
        # url parse
        qs = dict(parse.parse_qsl(url.query))
        qs['text1'] = sentence
        url = url._replace(query=parse.urlencode(qs, encoding='euc-kr'))
        new_url = parse.urlunparse(url)
        # print(new_url)

        # 표준발음 변환기에서 표준발음 가져오기
        html = requests.get(new_url).content
        bs = BeautifulSoup(html, 'html.parser')
        search = bs.find_all('td', attrs={'class': 'td2'})
        standard = search[2].text  # 표준발음
        # print(standard)

        # 문장 내용, 표준 발음, check를 sentence table에 insert
        s = Sentence(sentence, standard, True)
        db_session.add(s)
        db_session.commit()

        # 문장 분석 후 phoneme 테이블에 insert
        # TODO

    return "insSentenceControl success"
