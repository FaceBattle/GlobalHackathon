from Database import *
from Page import *
from Post import *

db = Database("fb")

metainfo = {}
metainfo["likes"] = 1000

#HOW TO CREATE A PAGE
page = db.create_page("ABC", metainfo)

bbcnews_urls = ["http://www.bbc.com/news/uk-34644273?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook",
                "http://www.bbc.com/news/science-environment-34638603?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook",
                "http://www.bbc.com/sport/0/rugby-union/34671255?ns_mchannel=social&#38;ns_campaign=bbc_sport&#38;ns_source=facebook&#38;ns_linkname=sport"]


#ADDING POST TO A PAGE
for url in bbcnews_urls:
    metainfo["title"] = "article_title"
    metainfo["likes"] = 10
    metainfo["shares"] = 10
    page.add_post(url, metainfo)
    print "done:" + url

#GET LIST OF POST THAT CONTAIN A WORD
word = "rugby"
list_post = page.get_list_post_from_index(word)

print "These post have the word: " + word
for id in list_post:
    post = page.get_post(id)
    if post.metainfo.has_key("title"):
        print post.metainfo["title"]
    else:
        print id


db.save()
