from sqlalchemy import Column, Integer, VARCHAR, CHAR, Float, DateTime, ForeignKey, Boolean
from database import Base, db_session

import datetime

class Sentence(Base):
    __tablename__ = 'sentence'
    sentenceId = Column(Integer, primary_key=True)
    sentenceData = Column(VARCHAR(50))
    standard = Column(VARCHAR(50))
    check = Column(Boolean, default=False)

    def __init__(self, stdata, standard, check):
        self.sentenceData = stdata
        self.standard = standard
        self.check = check

    def __repr__(self):
        return "<Sentence('%d', '%s', '%s', '%d')>" \
               % (self.sentenceId, self.sentenceData, self.standard, self.check)


class Word(Base):
    __tablename__ = 'word'
    wordId = Column(Integer, primary_key=True)
    sentenceId = Column(ForeignKey('sentence.sentenceId'))
    wordData = Column(CHAR(10))
    type = Column(CHAR(10))

    def __init__(self, stid, wddata, type):
        self.sentenceId = stid
        self.wordData = wddata
        self.type = type

    def __repr__(self):
        return "<Word('%d', '%d', '%s', '%s')>" \
               % (self.wordId, self.sentenceId, self.wordData, self.type)


class Result(Base):
    __tablename__ = 'result'
    resultId = Column(Integer, primary_key=True)
    sentenceId = Column(ForeignKey('sentence.sentenceId'))
    resultData = Column(VARCHAR(50))
    score = Column(Float)
    date = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, stid, rsdata, score):
        self.sentenceId = stid
        self.resultData = rsdata
        self.score = score
        self.date = datetime.datetime.now()

    def __repr__(self):
        return "<Result('%d', '%d', '%s', '%f')>" \
               % (self.resultId, self.sentenceId, self.resultData, self.score)


class Record(Base):
    __tablename__ = 'record'
    recordId = Column(Integer, primary_key=True)
    recordData = Column(CHAR(10))
    type = Column(CHAR(10))
    count = Column(Integer, default=0)

    def __init__(self, rcdata, type, count):
        self.recordData = rcdata
        self.type = type
        self.count = count

    def __repr__(self):
        return "<Record('%d', '%s', '%s', '%d')>" \
               % (self.recordId, self.recordData, self.type, self.count)

class WordBook(Base):
    __tablename__ = 'wordbook'
    wordbookId = Column(Integer, primary_key=True)
    wordData = Column(VARCHAR(50))

    def __init__(self, wddata):
        self.wordData = wddata

    def __repr__(self):
        return "<WordBook('%d', '%s')>" \
               % (self.wordbookId, self.wordData)