__author__ = 'luizfernando2'


import facepy
import sys
import json
from dateutil.parser import parse
token =  "1666547706896513|gA92jKY9tThz_JZEeeY5zgyJRhY"


def remove_paging_stuff(original_json):
    if 'likes' in original_json:
        original_json['likes'].pop('paging', None)
        original_json['likes'].pop('data', None)
    if 'comments' in original_json:
        original_json['comments'].pop('paging', None)
        original_json['comments'].pop('data', None)


def get_posts_from_page(page_id):
    graph = facepy.GraphAPI(token)
    page_path = page_id + '/posts?fields=attachments{description,title,type,url},id,message,type,created_time,likes.limit(1).summary(true),comments.limit(1).summary(true)&limit=100'
    posts_iterator = graph.get(path=page_path, page=True)

    list_of_posts = []
    error_count = 0
    while True:
        try:
            entry = next(posts_iterator)
        except StopIteration:
            break
        except:
            error_count += 1
            if error_count == 5:
                break
            else:
                continue

        entry = entry['data']
        for dict in entry:
            remove_paging_stuff(dict)
        list_of_posts += entry
        date = parse(entry[-1]["created_time"])

        print(date.year, date.month, date.day)
        if date.year < 2015:
            break

    my_json = {'data':list_of_posts}
    print(sys.getsizeof(list_of_posts))
    with open("FacebookHistory2/" + page_id + ".json", "w") as f:
        json.dump(my_json, f)


pages_list = ['FoxNews']

for page in pages_list:
    get_posts_from_page(page)