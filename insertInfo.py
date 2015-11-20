__author__ = 'danielpazinato'

import json
import FBPost
import os
from Database import *
from Page import *
from Post import *


def getPostFromJSON(file_name):

    list_post_obj = []
    with open("FacebookHistory2/" + file_name) as f:
        my_json = json.load(f)
        for i in xrange(len(my_json['data'])):
            single_post = my_json['data'][i]
            post_obj = FBPost.FBPost(single_post)
            list_post_obj.append(post_obj)

    return list_post_obj



db_name = "fb"
db = Database("fb")
db.save()
db.load()

pages = os.listdir("FacebookHistory2/")
pages = [file for file in pages if file.endswith(".json")]
pages = ["cnn.json"]

for page_name in pages:
    list_post_obj = getPostFromJSON(page_name)
    page_name = page_name[:-5]

    metainfo1 = {}
    page = db.create_page(page_name, metainfo1)
    print "PAGE NAME:"+ page_name
    #ADDING POST TO A PAGE
    MAX = 5000
    if len(list_post_obj) > MAX:
        list_post_obj = list_post_obj[0:MAX]
    for post_obj in list_post_obj:
        metainfo = {}
        metainfo["title"] = post_obj.title
        metainfo["like_count"] = post_obj.like_count
        metainfo["created_time"] = post_obj.created_time
        metainfo["url"] = post_obj.url
        metainfo["id"] = post_obj.id
        metainfo["message"] = post_obj.message + " " + metainfo["title"] + " " + post_obj.description
        #print post_obj.url
        #print post_obj.message
        #url = ""
        #if post_obj.url == "":
        page.add_post(metainfo["message"], metainfo)


        #print "done:" + metainfo["title"]

    db.save()



