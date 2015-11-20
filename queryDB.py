__author__ = 'danielpazinato'

from Database import *
from nltk.stem.lancaster import LancasterStemmer
from copy import deepcopy
from Queue import PriorityQueue
from UnionFind import *
import random
class MyQuery(object):
    def __init__(self):
        self.db = Database("fb")
        self.db.load()

        list_pages = []
        for page in self.db.list_of_pages:
            list_pages.append(self.db.get_page(page))
        self.list_pages = list_pages
        self.stemmer = LancasterStemmer()

    def main_post_every_page(self, word):
        my_post_dict = {}
        for page in self.list_pages:
            list = page.get_list_post_from_index(word)
            if list == []:
                continue
            post_id = list[int(len(list)/2)]
            id = page.get_post(post_id).metainfo["id"]
            my_post_dict[page.name] = id
        return my_post_dict

    def main_word_every_page(self, word):
        my_pos_dict = {}
        my_pos_dict_normed = {}
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
            my_pos_dict_normed[key] = 1.0*(my_pos_dict[key] - mini)/(maxi - mini)

        return my_pos_dict, my_pos_dict_normed, my_word_dict

    def get_number_of_posts_for_word(self, word):
        mydict = {}
        maxi = - 10
        mini = 10

        for page in self.list_pages:
            mydict[page.name] = len(page.get_list_post_from_index(word))*1.0/page.last_id_added
            maxi = max(maxi,mydict[page.name])
            mini = min(mini,mydict[page.name])
        for key in mydict.keys():
            mydict[key] = 1.0*(mydict[key] - mini)/(maxi - mini)

        return mydict

    def equal_words(self, p1, p2):
        #print p1
        #print p2
        #print "-------------------"
        num = 0
        for w1 in p1:
            for w2 in p2:
                if self.stemmer.stem(str(w1[2])) == self.stemmer.stem(str(w2[2])): num += 1
        return num

    def matching_people(self,word):
        pages_mains_words = {}
        result = {}
        num_page = {}
        n = 0
        for page in self.list_pages:
            # print page.name
            # print page.get_list_post_from_index(word)
            num_page[page.name] = n
            n += 1
            main_words, sentimental = page.page_main_words(word)
            main_words = main_words[0:50]
            for i in range(len(main_words)):
               main_words[i] = main_words[i][2]
            pages_mains_words[page.name] = set(main_words)
            result[page.name] = {}

        mini = 0
        maxi = -100
        for i in xrange(len(self.list_pages)):
            name1 = self.list_pages[i].name
            set1 = pages_mains_words[name1]
            for j in xrange(len(self.list_pages)):
                if i != j:
                    name2 = self.list_pages[j].name
                    set2 = pages_mains_words[name2]
                    for w in set1:
                        if w in set2:
                            if result[name1].has_key(name2):
                                result[name1][name2] += 1
                            else:
                                result[name1][name2] = 1
                            maxi = max(maxi, result[name1][name2])

        maxi = 1.1*maxi
        print maxi
        print result
        pq = PriorityQueue()
        result2 = deepcopy(result)
        for key in result.keys():
            for key2 in result[key]:
                result[key][key2] = result[key][key2]/maxi
                if result[key][key2] < 0.20: result2[key].__delitem__(key2)
                else:
                    result2[key][key2] = result[key][key2]
                    pq.put([-result[key][key2],key,key2])


        return result, result2



