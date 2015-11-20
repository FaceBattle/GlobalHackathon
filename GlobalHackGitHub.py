from flask import Flask
from flask import render_template, request
from queryDB import MyQuery
from FBDownloader import get_post
import json

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

    main_posts = my_q.main_post_every_page(word_searched)
    post_class_dict = {}
    for key, value in main_posts.iteritems():
        post_obj = get_post(value)
        post_class_dict[key] = post_obj
    mat = []
    maxdist = 0
    for i,key1 in enumerate(pos_dict_normed.keys()):
        mat.append([])
        for j,key2 in enumerate(pos_dict_normed.keys()):
            mat[i].append(((freq_dict[key1]-freq_dict[key2])**2 + (pos_dict_normed[key1]-pos_dict_normed[key2])**2)**(0.5))
            maxdist = max(maxdist, mat[i][j])
    for i,key1 in enumerate(pos_dict_normed.keys()):
        for j,key2 in enumerate(pos_dict_normed.keys()):
            mat[i][j] = maxdist-mat[i][j]
            mat[i][j] = ((1.0*mat[i][j])/maxdist)*97 + 3
    matches = {}
    for i, key1 in enumerate(pos_dict_normed.keys()):
        matches[key1] = {}
        for j, key2 in enumerate(pos_dict_normed.keys()):
            matches[key1][key2] = mat[i][j]/100

    #matches, trash = my_q.matching_people(word_searched)


    groups = {}
    for key in pos_dict_normed.keys():
        if freq_dict[key] > 0.2 and pos_dict_normed[key] > 0.6:
            groups[key] = 0
        elif freq_dict[key] > 0.2 and pos_dict_normed[key] < 0.4:
            groups[key] = 1
        else:
            groups[key] = 2

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
                           matches=matches, important_posts=json.dumps(post_class_dict))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
