from flask import Flask
from Controller import ttsControl

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

# TTS REST API
@app.route('TTS')용
def play_text():

    ttsControl.TTS("안녕하세요. 반갑습니다.");

    return 'playing'

if __name__ == '__main__':
    app.run()
