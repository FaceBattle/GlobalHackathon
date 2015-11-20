import json

import FBPost


def read_JSON(file_name):
    with open("FacebookHistory2/" + file_name) as f:
        my_json = json.load(f)

        for single_post in my_json['data'][:5]:
            post_obj = FBPost.FBPost(single_post)
            if post_obj.url:
                print post_obj.url

post_obj = read_JSON('berniesanders.json')
