__author__ = 'danielpazinato'

from Database import *
from Page import *
from Post import *

def main_word_every_page(word, list_pages):
    for page in list_pages:
        print page.name
        print page.get_list_post_from_index(word)
        list_main_words, sentimental = page.page_main_words(word)
        for l in list_main_words:
            print l[2],
        print
        print sentimental

#initialize db
db = Database("fb")
db.load()

list_pages = []
for page in db.list_of_pages:
    list_pages.append(db.get_page(page))

print list_pages
word = "france"
main_word_every_page(word, list_pages)
