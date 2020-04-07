from gtts import gTTS

# TTS
# 구글 TTS API(gTTS) 사용
def TTS(text):

    tts = gTTS(text=text, lang='ko')

    f = open("SoundFile", 'wb')
    tts.write_to_fp(f)
    f.close()

    return 'success'
