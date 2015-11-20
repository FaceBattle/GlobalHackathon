__author__ = 'danielpazinato'

import os
import cPickle
from Page import *

class Database:

    db_name = ""
    list_of_pages = set([])

    def __init__(self, db_name = ""):
        self.db_name = db_name
        self.list_of_pages = set([])

    def get_list_of_pages(self):
        return self.list_of_pages

    def create_page(self, name, metainfo):
        path = os.getcwd()+'/pages/'+ name
        print(name, path)
        self.list_of_pages.add(name)
        if not os.path.exists(path):
            page = Page(name, metainfo)
            page.save()
        else :
            page = self.get_page(name)
        return page

    def get_page(self, name):
        page = Page(name)
        page.load()
        return page


    def load(self):
        path = os.getcwd()+"/pages/"+self.db_name
        tmp_dict = cPickle.load(open(path,'rb'))
        self.__dict__.update(tmp_dict)

    def save(self):
        path = os.getcwd()+"/pages/"+self.db_name
        cPickle.dump(self.__dict__,open(path,'wb'),2)