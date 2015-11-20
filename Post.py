__author__ = 'danielpazinato'
import os
import cPickle

class Post:

    id = 0
    page = ""
    # face_id, title, data, nLikes, nShares, sentimental
    metainfo = {}
    frequency_word = {}
    main_words = {}
    reverse_stem = {}

    def __init__(self, id = 0, page = "", metainfo = {}, frequency_word = {}, main_words = {}, reverse_stem = {}):
        self.id = id
        self.page = page
        self.metainfo = metainfo
        self.frequency_word = frequency_word
        self.main_words = main_words
        self.reverse_stem = reverse_stem

    def get_related_words(self, word):
        if self.related_words.has_key(word):
            return self.related_words[word]
        return -1

    def load(self):
        path = os.getcwd()+"/pages/"+self.page+"/"+str(self.id)
        tmp_dict = cPickle.load(open(path,'rb'))
        self.__dict__.update(tmp_dict)

    def save(self):
        path = os.getcwd()+"/pages/"+self.page+"/"+str(self.id)
        if not os.path.exists(path):
            open(path,"w+")
        cPickle.dump(self.__dict__,open(path,'wb'),2)
