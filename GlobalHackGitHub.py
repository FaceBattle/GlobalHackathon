from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/bias/', methods=['POST'])
def find_bias():
    word_searched = request.form['word']
    root_orig = {
         "name": "pages",
         "children": [
             {"name": "aljazeera", "size": 3938},
             {"name": "barackobama", "size": 743},
             {"name": "bbcnews", "size": 24593},
             {"name": "berniesanders", "size": 16540},
             {"name": "CarlyFiorina", "size": 7074},
             {"name": "cnn", "size": 1302},
             {"name": "dawndotcom", "size": 24593},
             {"name": "DonaldTrump", "size": 1302},
             {"name": "FoxNews", "size": 1302},
             {"name": "hillaryclinton", "size": 24593},
             {"name": "nytimes", "size": 1302},
             {"name": "sydneymorningherald", "size": 4896},
             {"name": "TMZ", "size": 763}
         ]
    };

    return render_template('page.html', word=word_searched, bubble_data=root_orig)


if __name__ == '__main__':
    app.run()
