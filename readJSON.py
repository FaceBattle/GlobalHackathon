__author__ = 'danielpazinato'

import json

import FBPost


def read_JSON(file_name):
    with open(file_name) as f:
        my_json = json.load(f)

        single_post = my_json['data'][0]
        post_obj = FBPost(single_post)
        print(post_obj.message, post_obj.like_count)


read_JSON('TMZ.json')
