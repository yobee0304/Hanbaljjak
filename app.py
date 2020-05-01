from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

# API1
@app.route('/sentence')
def sentenceControl():

    return 'sentece success'

# API2
@app.route('/phoneme')
def phonemeControl():

    return 'phoneme success'

# API3
@app.route('/result')
def resultControl():

    return 'result success'

# Main
if __name__ == '__main__':
    app.run()