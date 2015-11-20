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
        my_pos_dict = {}
        my_word_dict = {}
        maxi = - 10
        mini = 10
        for page in self.list_pages:
            # print page.name
            # print page.get_list_post_from_index(word)
            list_main_words, sentimental = page.page_main_words(word)
            my_pos_dict[page.name] = sentimental[0]
            my_word_dict[page.name] = list_main_words[:30]
            maxi = max(maxi,sentimental[0])
            mini = min(mini,sentimental[0])

        #normalize
        for key in my_pos_dict.keys():
            my_pos_dict[key] = 1.0*(my_pos_dict[key] - mini)/(maxi - mini)

        return my_pos_dict, my_word_dict

    def get_number_of_posts_for_word(self, word):
        mydict = {}
        for page in self.list_pages:
            mydict[page.name] = len(page.get_list_post_from_index(word))*1.0/page.last_id_added
        return mydict
