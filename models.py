from sqlalchemy import Column, Integer, VARCHAR, CHAR, Float, DateTime, ForeignKey
from database import Base, db_session

import datetime

class Sentence(Base):
    __tablename__ = 'sentence'
    sentenceId = Column(Integer, primary_key=True)
    sentenceData = Column(VARCHAR(50))
    standard = Column(VARCHAR(50))
	
	def __init__(self, stid, stdata, standard):
		self.sentenceId = stid
		self.sentenceData = stdata
		self.standard = standard

    def __repr__(self):
        return "<Sentence('%d', '%s', '%s')>" % (self.sentenceId, self.sentenceData, self.standard)


class Phoneme(Base):
    __tablename__ = 'phoneme'
    phonemeId = Column(Integer, primary_key=True)
    sentenceId = Column(ForeignKey('sentence.sentenceId'))
    phonemeData = Column(CHAR(10))
    type = Column(CHAR(10))
	
    def __init__(self, phid, stid, phdata, type):
        self.phonemeId=phid
        self.sentenceId = stid
        self.phonemeData = phdata
        self.type = type

    def __repr__(self):
        return "<Phoneme('%d', '%d', '%s', '%s')>" \
               % (self.phonemeId, self.sentenceId, self.phonemeId, self.type)


class Result(Base):
    __tablename__ = 'result'
    resultId = Column(Integer, primary_key=True)
    sentenceId = Column(ForeignKey('sentence.sentenceId'))
    resultData = Column(VARCHAR(50))
    score = Column(Float)
    date = Column(DateTime, default=datetime.datetime.utcnow())
	
    def __init__(self, rsid, stid, rsdata, score):
        self.resultId = rsid
        self.sentenceId = stid
        self.resultData = rsdata
        self.score = score
        self.date = datetime.datetime.utcnow()

    def __repr__(self):
        return "<Result('%d', '%d', '%s', '%f')>" \
               % (self.resultId, self.sentenceId, self.resultId, self.score)


class Record(Base):
    __tablename__ = 'record'
    recordId = Column(Integer, primary_key=True)
    recordData = Column(CHAR(10))
    type = Column(CHAR(10))
    count = Column(Integer, default=0)
	
    def __init__(self, rcid, rcdata, type, count):
        self.recordId = rcid
        self.recordData = rcdata
        self.type = type
        self.count = count

    def __repr__(self):
        return "<Record('%d', '%s', '%s', '%d')>" \
               % (self.recordId, self.recordData, self.type, self.count)
			   
			   
# 임시 데이터
"""
s1 = Sentence(1, "날씨가 맑다", "날씨가 막따")
db_session.add(s1)
s2 = Sentence(2, "공권력", "공꿘녁")
db_session.add(s2)
db_session.commit()

p1 = Phoneme(11, 1, 'ㄱ', 'b')
db_session.add(p1)
p2 = Phoneme(12, 1, 'ㄸ', 'u')
db_session.add(p2)
p3 = Phoneme(13, 2, 'ㄲ', 'u')
db_session.add(p3)
p4 = Phoneme(14, 2, 'ㄴ', 'u')
db_session.add(p4)
db_session.commit()

rs1 = Result(21, 1, "날씨가 말따", 86)
db_session.add(rs1)
rs2 = Result(22, 2, "공궐력", 60)
db_session.add(rs2)
db_session.commit()

rc1 = Record(31, 'ㄱ', 'b', '1')
db_session.add(rc1)
rc2 = Record(32, 'ㄲ', 'u', '1')
db_session.add(rc2)
rc3 = Record(33, 'ㄴ', 'b', '1')
db_session.add(rc3)
rc4 = Record(34, 'ㄴ', 'u', '1')
db_session.add(rc4)
rc5 = Record(35, 'ㄱ', 'u', '2')
db_session.add(rc5)
db_session.commit()
"""