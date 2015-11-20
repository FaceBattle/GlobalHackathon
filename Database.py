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

        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(APP_ROOT, "pages/"+self.db_name)

    def get_list_of_pages(self):
        return self.list_of_pages

    def create_page(self, name, metainfo):
        path = self.db_path

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
        path = self.db_path

        tmp_dict = cPickle.load(open(path,'rb'))
        self.__dict__.update(tmp_dict)

    def save(self):
        path = self.db_path

        cPickle.dump(self.__dict__,open(path,'wb'),2)