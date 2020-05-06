from Controller.homeControl import homeControl
from Controller.sentenceControl import sentenceControl
from Controller.resultControl import resultControl
from Controller.totalControl import totalControl

# url mapping
urls = [
    ('/', homeControl, ["GET"]),
    ('/sentence', sentenceControl, ["GET"]),
    ('/result', resultControl, ["GET", "POST"]),
    ('/total', totalControl, ["GET"]),
]