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

from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1 import enums
import io

def sample_recognize(file_path):

    client = speech_v1p1beta1.SpeechClient()

    # 임시 path
    local_file_path = file_path

    # The language of the supplied audio
    language_code = "ko-KR"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 44100

    # 신뢰도 수준. 무조건 30개가 나오지는 않고 alternatives가 있는만큼 나옴.
    maxalt = 30

    # enable_word_confidence = True

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        # "enable_word_confidence": enable_word_confidence,
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
        "audio_channel_count": 2,
        "max_alternatives": maxalt,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)

    speech_to_text_results = []
    for result in response.results:
        for i in range(0, len(result.alternatives)):
            speech_to_text_results.append(result.alternatives[i])

    # 신뢰도를 기준으로 오름차순
    speech_to_text_results = sorted(speech_to_text_results, key=lambda text: text.confidence)
    print("RAW STT RESULT :")
    for i in speech_to_text_results:
        print(i.transcript, i.confidence)
    print()

    if len(speech_to_text_results) > 0:
        return speech_to_text_results
    else:
        return ""
		

########################## 유사도 비교 알고리즘 ###############################
from difflib import SequenceMatcher
from urllib import parse
from bs4 import BeautifulSoup
import requests
import re

def hasNumberAlphabet(inputString):
	return bool(re.search(r'[a-zA-Z0-9]', inputString))


def similaritySentence(stt_results, sentence_standard):
    stt_r = stt_results
    #speech_to_text_results = stt_results
    speech_to_text_results = []		# stt 결과 중 표준발음과 길이 같은것만 저장.
    standard = sentence_standard    # 문장의 표준 발음
    result_lst = []    # stt 결과 문장을 스플릿한 결과와 confidence 저장
    measure_lst = []   # 유사도 비교 기준 단어 리스트
    max_similarity_word_lst = []    # 유사도가 가장 높은 word list
    max_similarity_word = ""
    pronounce_lst = []
	
	# 표준 발음 스플릿
    standard_lst = standard.split()

	# stt 결과 중 표준발음과 길이 다른 것, 숫자, 영어 들어가는 것 제외.
    for i in range(0, len(stt_r)):
		stt_r_lst = str(stt_r[i].transcript).split(" ")
		word_len_same = True
        if len(standard_lst) == len(stt_r_lst) and not hasNumberAlphabet(stt_r[i].transcript):
			for word_index in range(0, len(standard_lst)):
				if len(standard_lst[word_index]) != len(stt_r_lst[word_index]):
					word_len_same = False
					break
			if word_len_same:
				speech_to_text_results.append(stt_r[i])

    if len(speech_to_text_results) == 0:
        return ""

    # result_lst에 stt 결과와 confidence 를
    # [['오늘', '날씨가', '참', '맞다', 0.7228566408157349]] 와 같은 형식으로 변환
    for i in range(0, len(speech_to_text_results)):
        entry = (str(speech_to_text_results[i].transcript)).split()
        entry.append(speech_to_text_results[i].confidence)
        result_lst.append(entry)
    
	print("result_lst :")
    for i in range(0, len(result_lst)):
        print(result_lst[i])
    print()

    # speech_to_text_results에서 유사도 비교 기준 뽑기
    for i in range(0, len(standard_lst)):
        measure_entry = {}
        measure_entry = set()

        for j in range (0, len(result_lst)):
            if len(standard_lst[i]) == len(result_lst[j][i]):
                measure_entry.add(result_lst[j][i])

        measure_lst.append(list(measure_entry))

    #print("measure_lst : ",measure_lst)

    for i in range(0, len(measure_lst)):
        pre_max_similarity_measure = 0
        for j in range(0, len(result_lst)):
            word_score = 0
            for k in range(0, len(measure_lst[i])):
                # 원래 단어와 변환한 단어 음소 분해해서 비교
                Total_pho = 0  # 총 음소 개수
                Wrong_total_pho = 0  # 틀린 음소 개수

                for index, word_one in enumerate(measure_lst[i][k]):
                    StandPho = phonemeConvert(word_one)

                    # 글자가 일치하는 경우
                    if (result_lst[j][i][index] == word_one):
                        if (StandPho[2] == ''):
                            Total_pho += 2
                        else:
                            Total_pho += 3

                    # 글자가 일치하지 않는 경우
                    # 음소 분해
                    else:
                        UserPho = phonemeConvert(result_lst[j][i][index])

                        if (UserPho[2] == ' ' and StandPho[2] == ' '):
                            Total_pho += 2
                        else:
                            Total_pho += 3

                            if (UserPho[2] != StandPho[2]):
                                Wrong_total_pho += 1

                        if (UserPho[0] != StandPho[0]):
                            Wrong_total_pho += 1

                        if (UserPho[1] != StandPho[1]):
                            Wrong_total_pho += 1

                    word_score = word_score + 1 - (Wrong_total_pho / Total_pho) * result_lst[j][-1]
                #print(word_score)
            similarity_measure = word_score
            if similarity_measure > pre_max_similarity_measure:
                max_similarity_word = result_lst[j][i]
        max_similarity_word_lst.append(max_similarity_word)

    print("유사도 선택 결과 : ", max_similarity_word_lst)

    # 부산대 표준발음 변환기
    url = parse.urlparse \
        ("http://pronunciation.cs.pusan.ac.kr/pronunc2.asp?text1=안녕하세요&submit1=확인하기")
    # url parse
    qs = dict(parse.parse_qsl(url.query))

    for standard_index, word_data in enumerate(max_similarity_word_lst):
        qs['text1'] = word_data
        url = url._replace(query=parse.urlencode(qs, encoding='euc-kr'))
        new_url = parse.urlunparse(url)

        # 표준발음 변환기에서 표준발음 가져오기
        html = requests.get(new_url).content
        bs = BeautifulSoup(html, 'html.parser')

        # 표준 발음으로 변환할 수 없는 경우 원래 단어로
        if bs.body == None:
            pronounce_lst.append(word_data)

        # 표준발음으로 변환할 수 있는 경우
        else:
            search = bs.find_all('td', attrs={'class': 'td2'})
            search_standard = search[2].text[:-1]
            # 발음이 여러개일 때 앞에 것만 가져오기
            search_standard = search_standard.split('/')
			if word_data == "이":
				search_standard[0] = "이"

            # 원래 단어와 변환한 단어 음소 분해해서 비교
            Total_pho = 0  # 총 음소 개수
            Wrong_total_pho = 0  # 틀린 음소 개수

            for index, word_one in enumerate(search_standard[0]):
                StandPho = phonemeConvert(word_one)

                # 글자가 일치하는 경우
                if(word_data[index] == word_one):
                    if(StandPho[2] == ''):
                        Total_pho += 2
                    else:
                        Total_pho += 3

                # 글자가 일치하지 않는 경우
                # 음소 분해
                else:
                    UserPho = phonemeConvert(word_data[index])

                    if (UserPho[2] == ' ' and StandPho[2] == ' '):
                        Total_pho += 2
                    else:
                        Total_pho += 3

                        if (UserPho[2] != StandPho[2]):
                            Wrong_total_pho += 1

                    if (UserPho[0] != StandPho[0]):
                        Wrong_total_pho += 1

                    if (UserPho[1] != StandPho[1]):
                        Wrong_total_pho += 1

                #print(Total_pho)
                #print(Wrong_total_pho)

            if search_standard[0]==standard_lst[standard_index]:
                pronounce_lst.append(search_standard[0])

            # 표준 발음으로 변환한 결과가 아예 다른 단어로 바뀔 경우 원래 단어로 ex) 만땅 -> 가득
            elif Wrong_total_pho / Total_pho > 0.3:
                #print(Wrong_total_pho / Total_pho)
                pronounce_lst.append(word_data)
            else:
                pronounce_lst.append(search_standard[0])

    # 유사도가 가장 높은 word로 만든 sentence
    pronounce_sentence = " ".join(pronounce_lst)
    print("최종 결과 : ", pronounce_sentence)
    return pronounce_sentence



########################## API2 ###############################

from flask import request, jsonify
from werkzeug.utils import secure_filename
from database import db_session
from models import Sentence, Result, Record, Word
import easydict
import os
import random
from konlpy.tag import Hannanum
from difflib import SequenceMatcher


FILE_DIRECTORY = "./uploadFile/"
#
# # 디렉터리 없으면 생성하기
# if not os.path.exists(FILE_DIRECTORY):
#     os.makedirs(FILE_DIRECTORY)

# API2
def resultControl():
    if(request.method == 'POST'):

        # 클라이언트에서 sentenceId & wav file 받아옴
        wav = request.files['receiveFile']
        filename = request.form['fileName']
        sentenceId = request.form['sentenceId']

        # upload 디렉터리에 저장
        wav.save(FILE_DIRECTORY + secure_filename(wav.filename))

        ##### upload 디렉터리에 있는 파일을 STT로 변한

        # 임시 path
        args = easydict.EasyDict({"local_file_path": "./uploadFile/"+filename})

        # TODO Credential Error
        # print(sample_recognize(args.local_file_path))


        # sentenceId를 통해 DB에서 표준 발음 텍스트 가져옴
        Pick_sentence = db_session.query(Sentence).filter(Sentence.sentenceId == sentenceId).first()

        receiveSTTData = sample_recognize(args.local_file_path)
        receiveData = similaritySentence(receiveSTTData, Pick_sentence.standard)
        #receiveData = "날시가 참 말따"
        print("STT result : ", receiveData)

        # print(Pick_sentence)
        ##### 분석 알고리즘

        hannanum = Hannanum()

        StandardSentence = Pick_sentence.standard
        sentenceData = Pick_sentence.sentenceData

        # 공백 인덱스 리스트 생성
        # 공백 개수는 일치
        userBlankList = [i for i, value in enumerate(receiveData) if value == " "]
        standardBlankList = [i for i, value in enumerate(StandardSentence) if value == " "]
        # print(BlankList)

        # 문자열 길이가 다르거나 공백 개수가 다르면
        # 재시도 요청
        if (len(receiveData) != len(StandardSentence) or len(userBlankList) != len(standardBlankList)):
            os.remove("./uploadFile/"+filename)

            return jsonify(
                status="failure",
                resultData=receiveData,
                errorMessage="repeat",
            )

        # 공백 제거
        UserSentence = receiveData.replace(" ", "")
        StandardSentence = StandardSentence.replace(" ", "")
        sentenceData = sentenceData.replace(" ", "")

        # print(UserSentence)
        # print(StandardSentence)

        Total_pho = 0           # 총 음소 개수
        Wrong_total_pho = 0     # 틀린 음소 개수
        Wrong_word_index_list = []   # 틀린 글자 데이터가 들어있는 리스트
        Wrong_word_list = []         # 틀린 단어 데이터가 들어있는 리스트
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
                Wrong_word_index_list.append(index)
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

        # print(Wrong_pho_dict)


        ######### 틀린 음소 record 테이블에 count 올림 -> TEST SUCCESS
        for type in Wrong_pho_dict:
            for pho in Wrong_pho_dict[type]:
                # print(pho)
                updateData = db_session.query(Record).filter(Record.recordType == type)\
                                                    .filter(Record.recordData == pho).first()
                # print(updateData.type, updateData.recordData)
                updateData.count += Wrong_pho_dict[type][pho]
                db_session.commit()



        # 일치율
        Correct_rate = round(1 - (Wrong_total_pho / Total_pho), 4)
        """
        # 일치율 100%인 경우
        if Correct_rate == 1:
            os.remove("./uploadFile/" + filename)

            return jsonify(
                status="perfect",
                resultData=receiveData,
                score=Correct_rate,
            )
        """
        # print(Wrong_word_list)

        # 변경 후
        # print(Wrong_word_index_list)
        sentenceData_split = Pick_sentence.sentenceData.split()
        # print(sentenceData_split)
        # 틀린 인덱스가 포함된 단어 선택
        word_start_point = 0
        for sentence_word in sentenceData_split:
            word_end_point = word_start_point + len(sentence_word)-1

            # print(word_start_point, word_end_point)

            for wrong_index in Wrong_word_index_list:
                if word_start_point <= wrong_index and word_end_point >= wrong_index:
                    word_to_pos = hannanum.pos(sentence_word)

                    # print(word_to_pos)
                    wrong_word_pho_list = phonemeConvert(sentenceData[wrong_index])
                    # print(wrong_word_pho_list)
                    for pos in word_to_pos:
                        #TODO 틀린 단어에 N이나 P가 여러개 들어있으면??
                        if pos[1] == 'N' or pos[1] == 'P':
                            for pos_word in pos[0]:
                                pos_word_pho_list = phonemeConvert(pos_word)
                                # print(pos_word_pho_list)
                                if wrong_word_pho_list[0] == pos_word_pho_list[0]:
                                    Wrong_word_list.append(pos)

                    break

            word_start_point += len(sentence_word)

        print(Wrong_word_list)

        # 틀린 글자 인덱스를 원래 문장을 기준으로 변경
        for i in userBlankList:
            for index, j in enumerate(Wrong_word_index_list):
                if(j >= i):
                    Wrong_word_index_list[index] += 1

        # print(Wrong_word_index)

        ######## result 테이블에 결과값 저장 -> TEST SUCCESS
        resultData = Result(stid=sentenceId, rsdata=receiveData, score=Correct_rate)
        db_session.add(resultData)
        db_session.commit()


        # 일치율 100%인 경우
        if Correct_rate == 1:
            os.remove("./uploadFile/" + filename)

            return jsonify(
                status="perfect",
                resultData=receiveData,
                score=Correct_rate,
            )

        ######## 가장 많이 틀린 단어에 대한 추천 문장 1개

        recommend_OtoD = dict(sentenceId=-1, sentenceData="", standard="")
        recommend_word = ""

        # 틀린 단어 리스트에 단어가 존재할 경우
        if Wrong_word_list:
            random.shuffle(Wrong_word_list)

            for random_select_word in Wrong_word_list:
                Word_query = db_session.query(Word).filter(Word.wordData == random_select_word[0])\
                    .filter(Word.wordType == random_select_word[1]).filter(Word.sentenceId != sentenceId)
                Word_entry = [pq.sentenceId for pq in Word_query]

                if Word_entry:
                    recommend_word = random_select_word[0]
                    if random_select_word[1] == 'P':
                        recommend_word += '다'
                    random_select_setencdId = random.choice(Word_entry)
                    Recommend_sentence = db_session.query(Sentence).filter(Sentence.sentenceId == random_select_setencdId).first()
                    recommend_OtoD['sentenceId'] = Recommend_sentence.sentenceId
                    recommend_OtoD['sentenceData'] = Recommend_sentence.sentenceData
                    recommend_OtoD['standard'] = Recommend_sentence.standard
                    break

    os.remove("./uploadFile/" + filename)

    # response해줄 틀린 단어 리스트
    wordList = []

    for w in Wrong_word_list:
        if w[1] == "P":
            wordList.append(w[0]+"다")
        else:
            wordList.append(w[0])

    # 결과 데이터를 모두 json으로 묶음
    return jsonify(
        status = "success",
        score = Correct_rate,
        wordList = wordList,
        userBlank = userBlankList,
        standardBlank = standardBlankList,
        wrongIndex = Wrong_word_index_list,
        resultData = receiveData
    )

###############################################################
