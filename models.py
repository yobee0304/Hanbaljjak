from sqlalchemy import Column, Integer, VARCHAR, CHAR, Float, DateTime, ForeignKey
from database import Base

import datetime

class Sentence(Base):
    __tablename__ = 'sentence'
    sentenceId = Column(Integer, primary_key=True)
    sentenceData = Column(VARCHAR(50))
    standard = Column(VARCHAR(50))

class Phoneme(Base):
    __tablename__ = 'phoneme'
    phonemeId = Column(Integer, primary_key=True)
    sentenceId = Column(ForeignKey('sentence.sentenceId'))
    phonemeData = Column(CHAR(10))
    type = Column(CHAR(10))

class Result(Base):
    __tablename__ = 'result'
    resultId = Column(Integer, primary_key=True)
    sentenceId = Column(ForeignKey('sentence.sentenceId'))
    resultData = Column(VARCHAR(50))
    score = Column(Float)
    date = Column(DateTime, default=datetime.datetime.now())

class Record(Base):
    __tablename__ = 'record'
    recordId = Column(Integer, primary_key=True)
    recordData = Column(CHAR(10))
    type = Column(CHAR(10))
    count = Column(Integer, default=0)