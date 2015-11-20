from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/bias/', methods=['POST'])
def find_bias():
    word_searched = request.form['word']
    print(word_searched)
    return render_template('page.html', word=word_searched)


if __name__ == '__main__':
    app.run()
