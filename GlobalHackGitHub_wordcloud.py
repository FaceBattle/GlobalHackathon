from flask import Flask
from flask import render_template, request
from queryDB import MyQuery

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/bias/', methods=['POST'])
def find_bias():
    word_searched = request.form['word']
    my_q = MyQuery()

    freq_dict = my_q.get_number_of_posts_for_word(word_searched)
    page_freq_list = []
    for key, value in freq_dict.iteritems():
        page_freq_list.append({
           "name": key,
           "size": value
        })

    root_orig = {
         "name": "pages",
         "children": page_freq_list
    }
    return render_template('page_word_cloud.html', word=word_searched, bubble_data=root_orig)


if __name__ == '__main__':
    print("oi")
    app.run(debug=True)
