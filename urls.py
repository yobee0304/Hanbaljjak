from Controller.homeControl import homeControl
from Controller.sentenceControl import sentenceControl
from Controller.resultControl import resultControl
from Controller.totalControl import totalControl
from Controller.customerSentenceControl import customerSentenceControl
from Controller.insSentenceControl import insSentenceControl
from Controller.delSentenceControl import delSentenceControl

# url mapping
urls = [
    ('/', homeControl, ["GET"]),
    ('/getSentence', sentenceControl, ["GET"]),
    ('/getResult', resultControl, ["GET", "POST"]),
    ('/getTotal', totalControl, ["GET"]),
    ('/getCustomSentence', customerSentenceControl, ["GET"]),
    ('/insertSentence', insSentenceControl, ["GET", "POST"]),
    ('/deleteSentence', delSentenceControl, ["GET", "POST"])
]