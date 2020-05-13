###################### 음소 분해 알고리즘 ########################

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

def phonemeConvert(word):

    pho_lst = []

    ## 영어인 경우 구분해서 작성함.
    if '가'<=word<='힣':            ## 588개 마다 초성이 바뀜.
        up = (ord(word) - ord('가')) // 588
        ## 중성은 총 28가지 종류
        mid = ((ord(word) - ord('가')) - (588*up)) // 28
        bottom = (ord(word) - ord('가')) - (588*up) - 28*mid
        pho_lst = [CHOSUNG_LIST[up], JUNGSUNG_LIST[mid], JONGSUNG_LIST[bottom]]
    else:
        pho_lst.append([word])

    return pho_lst

###############################################################

################# Googel Speech-to-Text API ###################

from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io

def sample_recognize(local_file_path):
    """
    Transcribe a short audio file using synchronous speech recognition
    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1.SpeechClient()

    # 임시 path
    local_file_path = './uploadFile/STTtest.wav'

    # The language of the supplied audio
    language_code = "ko-KR"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # 신뢰도 수준. 무조건 30개가 나오지는 않고 alternatives가 있는만큼 나옴.
    maxalt = 30

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
        "audio_channel_count": 1,
        "max_alternatives": maxalt
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)

    i = 0
    for result in response.results:
        # First alternative is the most probable result
        # alternative = result.alternatives[0]
        # print(u"Transcript: {}".format(alternative.transcript))
        # alternative2 = result.alternatives[1]
        # print(u"Transcript: {}".format(alternative2.transcript))
        for i in range(0, maxalt):
            alternative = result.alternatives[i]
            print(u"Transcript: {}".format(alternative.transcript))

###############################################################

########################## API2 ###############################

from flask import request, jsonify
from werkzeug.utils import secure_filename
from database import db_session
from models import Sentence, Result, Record, Phoneme
import easydict
import os
import random


FILE_DIRECTORY = "./uploadFile/"

# 디렉터리 없으면 생성하기
if not os.path.exists(FILE_DIRECTORY):
    os.makedirs(FILE_DIRECTORY)

# API2
def resultControl():

    if(request.method == 'POST'):

        # 클라이언트에서 sentenceId & wav file 받아옴
        wav = request.files['file']
        sentenceId = request.form['sentenceId']

        # upload 디렉터리에 저장
        wav.save(FILE_DIRECTORY + secure_filename(wav.filename))

        ##### upload 디렉터리에 있는 파일을 STT로 변한

        # 임시 path
        # args = easydict.EasyDict({"local_file_path": "./uploadFile/STTtest.wav"})
        # sample_recognize(args.local_file_path)

        # TODO Credential Error
        # print(sample_recognize(args.local_file_path))

        # sentenceId를 통해 DB에서 표준 발음 텍스트 가져옴
        Sentence_query = db_session.query(Sentence).filter(Sentence.sentenceId == sentenceId)
        Sentence_entry = [dict(sentenceData=sq.sentenceData, standard=sq.standard) for sq in Sentence_query]
        print(Sentence_entry)
        ##### 분석 알고리즘

        # TODO UserSentence 추가
        # receiveData = "Sample1"

        # Test Sentences
        receiveData = "날씨가 참 말다"
        StandardSentence = Sentence_entry[0]['standard']
        sentenceData = Sentence_entry[0]['sentenceData']

        # 문자열 길이가 다르면 다시 요청
        if(len(receiveData) != len(StandardSentence)):
            return 'repeat'

        # 공백 인덱스 리스트 생성
        BlankList = [i for i, value in enumerate(receiveData) if value == " "]
        print(BlankList)

        # 공백 제거
        UserSentence = receiveData.replace(" ", "")
        StandardSentence = StandardSentence.replace(" ", "")
        sentenceData = sentenceData.replace(" ", "")

        print(UserSentence)
        print(StandardSentence)

        Total_pho = 0           # 총 음소 개수
        Wrong_total_pho = 0     # 틀린 음소 개수
        Wrong_word_index = []   # 틀린 글자 데이터가 들어있는 리스
        Wrong_pho_dict = {'u' : {},
                          'm' : {},     # 틀린 음소가 저장되는 딕셔너리
                          'b' : {}}     # u : 자음, m : 모음, b : 받침


        for index, standard in enumerate(StandardSentence):
            StandPho = phonemeConvert(standard)

            # 글자가 일치하는 경우
            if(UserSentence[index] == standard):
                if(StandPho[2] == ' '):
                    Total_pho += 2
                else:
                    Total_pho += 3
            # 글자가 일치하지 않는 경우
            # 음소 분해
            else:
                Wrong_word_index.append(index)
                UserPho = phonemeConvert(UserSentence[index])
                SentencePho = phonemeConvert(sentenceData[index])

                if(UserPho[2] == ' ' and StandPho[2] == ' '):
                    Total_pho += 2
                else:
                    Total_pho += 3

                    if(UserPho[2] != StandPho[2]):
                        Wrong_total_pho += 1
                        if StandPho[2] in Wrong_pho_dict['b']:
                            Wrong_pho_dict['b'][SentencePho[2]] += 1
                        else:
                            Wrong_pho_dict['b'][SentencePho[2]] = 1

                if (UserPho[0] != StandPho[0]):
                    Wrong_total_pho += 1
                    if StandPho[0] in Wrong_pho_dict['u']:
                        Wrong_pho_dict['u'][SentencePho[0]] += 1
                    else:
                        Wrong_pho_dict['u'][SentencePho[0]] = 1

                if (UserPho[1] != StandPho[1]):
                    Wrong_total_pho += 1
                    if StandPho[1] in Wrong_pho_dict['m']:
                        Wrong_pho_dict['m'][SentencePho[1]] += 1
                    else:
                        Wrong_pho_dict['m'][SentencePho[1]] = 1

        print(Wrong_pho_dict)

        #########TODO 틀린 음소 record 테이블에 count 올림 -> TEST
        for type in Wrong_pho_dict:
            for pho in Wrong_pho_dict[type]:
                print(pho)
                updateData = db_session.query(Record).filter(Record.type == type)\
                                                    .filter(Record.recordData == pho).first()
                print(updateData.type, updateData.recordData)
                updateData.count += Wrong_pho_dict[type][pho]
                db_session.commit()


        # 일치율
        Correct_rate = round(1 - (Wrong_total_pho / Total_pho), 4)

        print(Total_pho, Wrong_total_pho, Correct_rate)

        for i in BlankList:
            for index, j in enumerate(Wrong_word_index):
                if(j >= i):
                    Wrong_word_index[index] += 1

        print(Wrong_word_index)

        ######## result 테이블에 결과값 저장 -> TEST SUCCESS
        # resultData = Result(sentenceId=sentenceId, resultData=receiveData, score=Correct_rate)
        # db_session.add(resultData)
        # db_session.commit()

        ########TODO 가장 많이 틀린 음소에 대한 추천 문장 1개
        max = 0
        Max_pho_dict = {'u': [],
                        'm': [],
                        'b': []}

        for type in Wrong_pho_dict:
            for pho in Wrong_pho_dict[type]:
                if(max <= Wrong_pho_dict[type][pho]):
                    if(max < Wrong_pho_dict[type][pho]):
                        Max_pho_dict = {'u': [],
                                        'm': [],
                                        'b': []}
                        max = Wrong_pho_dict[type][pho]
                    Max_pho_dict[type].append(pho)

        print(max)
        print(Max_pho_dict)

        # Random Select
        type_list = ['u', 'm', 'b']
        while(1):
            random_select_type = random.choice(type_list)
            if len(Max_pho_dict[random_select_type]) > 0:
                break
        print(Max_pho_dict[random_select_type])
        random_select_pho_idx = random.randint(0, len(Max_pho_dict[random_select_type])-1)
        random_select_pho = Max_pho_dict[random_select_type][random_select_pho_idx]


        #####################
        # 가장 많이 틀린 음소가 들어있는 문장의 SenteceId
        # Phoneme_query = db_session.query(Phoneme).filter(Phoneme.type == random_select_type)\
        #                                             .filter(Phoneme.phonemeData == random_select_pho)
        # Phoneme_entry = [pq.sentneceId for pq in Phoneme_query]
        # random_select_setencdId = random.choice(Phoneme_entry)
        #
        # Recommend_sentence_query = db_session.query(Sentence).filter(Sentence.sentenceId == random_select_setencdId)
        # Recommend_sentence_entry = [dict(sentenceData=rsq.sentenceData, standard=rsq.standard) for rsq in Recommend_sentence_query]
        #
        # print("recommendSenteceData", Recommend_sentence_entry[0]['sentenceData'])
        # print("recommendStandard", Recommend_sentence_entry[0]['standard'])

    # 결과 데이터를 모두 json으로 묶음
    return jsonify(
        standard = Sentence_entry[0]['standard'],
        resultData = receiveData,
        score = Correct_rate,
        type = random_select_type,
        phonemeData = random_select_pho,
        recommendSenteceData = '',
        recommendStandard = '',
        wrongIndex = Wrong_word_index
    )

###############################################################


