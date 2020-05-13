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
    date = Column(DateTime, default=datetime.datetime.now())
	
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
			   
			   
