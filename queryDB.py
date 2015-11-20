__author__ = 'danielpazinato'

from Database import *

class MyQuery(object):
    def __init__(self):
        self.db = Database("fb")
        self.db.load()

        list_pages = []
        for page in self.db.list_of_pages:
            list_pages.append(self.db.get_page(page))
        self.list_pages = list_pages

    def main_word_every_page(self, word):
        for page in self.list_pages:
            print page.name
            print page.get_list_post_from_index(word)
            list_main_words, sentimental = page.page_main_words(word)
            for l in list_main_words:
                print l[2],
            print
            print sentimental

    def get_number_of_posts_for_word(self, word):
        mydict = {}
        for page in self.list_pages:
            mydict[page.name] = len(page.get_list_post_from_index(word))*1.0/page.last_id_added
        return mydict



