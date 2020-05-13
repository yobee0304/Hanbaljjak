from Controller.homeControl import homeControl
from Controller.sentenceControl import sentenceControl
from Controller.resultControl import resultControl
from Controller.totalControl import totalControl

# url mapping
urls = [
    ('/', homeControl, ["GET"]),
    ('/getSentence', sentenceControl, ["GET"]),
    ('/getResult', resultControl, ["GET", "POST"]),
    ('/getTotal', totalControl, ["GET"]),
]