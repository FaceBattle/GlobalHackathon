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
        mydict_sentimental = {}
        maxi = -10
        mini = 10
        mydict_main_words = {}
        for page in self.list_pages:
            # print page.name
            # print page.get_list_post_from_index(word)
            list_main_words, sentimental = page.page_main_words(word)
            mydict_sentimental[page.name] = sentimental[0]
            maxi = max(maxi,sentimental[0])
            mini = min(mini,sentimental[0])
            mydict_main_words[page.name] = list_main_words
            # for l in list_main_words:
            #     print l[2],
            # print
            # print sentimental

        #normalize
        for key in mydict_sentimental.keys():
            mydict_sentimental[key] = 1.0*(mydict_sentimental[key] - mini)/(maxi - mini)

        return mydict_sentimental, mydict_main_words

    def get_number_of_posts_for_word(self, word):
        mydict = {}
        for page in self.list_pages:
            mydict[page.name] = len(page.get_list_post_from_index(word))*1.0/page.last_id_added
        return mydict
