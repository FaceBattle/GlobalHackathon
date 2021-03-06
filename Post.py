__author__ = 'danielpazinato'
import os
import cPickle

class Post:
    def __init__(self, id = 0, page = "", metainfo = None, frequency_word = None, main_words = None, reverse_stem = None):
        if metainfo is None:
            metainfo = {}
        if frequency_word is None:
            frequency_word = {}
        if main_words is None:
            main_words = {}
        if reverse_stem is None:
            reverse_stem = {}

        self.id = id
        self.page = page
        self.metainfo = metainfo
        self.frequency_word = frequency_word
        self.main_words = main_words
        self.reverse_stem = reverse_stem

        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        self.db_post_path = os.path.join(APP_ROOT, "pages/"+self.page+"/"+str(self.id))

    def load(self):
        path = self.db_post_path
        tmp_dict = cPickle.load(open(path,'rb'))
        self.__dict__.update(tmp_dict)

    def save(self):
        path = self.db_post_path
        if not os.path.exists(path):
            open(path,"w+")
        cPickle.dump(self.__dict__,open(path,'wb'),2)
