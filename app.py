from flask import Flask
from Controller import phoControl

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

# API1
@app.route('/sentence')
def sentenceControl():

    return 'sentece success'

# API2
@app.route('/result')
def phonemeControl():

    return 'result success'

# API3
@app.route('/total')
def resultControl():

    return 'total success'

# Main
if __name__ == '__main__':
    app.run()