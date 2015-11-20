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

    pos_dict_orig, pos_dict_normed, word_dict = my_q.main_word_every_page(word_searched)

    matches, trash = my_q.matching_people(word_searched)

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

    new_word_dict = {}
    for key, value in word_dict.iteritems():
        words_array = []
        for word in value:
            words_array.append(
                {
                    "text": word[2], "weight": word[0]
                }
            )
        new_word_dict[key] = words_array

    return render_template('page.html',
                           word=word_searched, bubble_data=root_orig,
                            freq_dict=freq_dict,
                           pos_dict=pos_dict_normed, pos_dict_orig=pos_dict_orig,
                           word_dict=new_word_dict,
                           matches=matches)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
