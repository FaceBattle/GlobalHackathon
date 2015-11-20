__author__ = 'danielpazinato'

from Database import *
from Page import *
from Post import *

def main_word_every_page(word, list_pages):
    for page in list_pages:
        print page.name
        print page.get_list_post_from_index(word)
        print page.page_main_words(word)

#initialize db
db = Database("fb")
db.load()

list_pages = []
for page in db.list_of_pages:
    list_pages.append(db.get_page(page))

word = "france"
main_word_every_page(word, list_pages)
