__author__ = 'danielpazinato'

from Database import *
from nltk.stem.lancaster import LancasterStemmer

class MyQuery(object):
    def __init__(self):
        self.db = Database("fb")
        self.db.load()

        list_pages = []
        for page in self.db.list_of_pages:
            list_pages.append(self.db.get_page(page))
        self.list_pages = list_pages
        self.stemmer = LancasterStemmer()

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
        pages_mains_words = []
        for page in self.list_pages:
            # print page.name
            # print page.get_list_post_from_index(word)
            main_words, sentimental = page.page_main_words(word)
            pages_mains_words.append(main_words[0:30])


        maxi = - 1000
        mini = 1000
        matrix = []
        for i in xrange(len(pages_mains_words)):
            diff = []
            for j in xrange(len(pages_mains_words)):
                diff.append([])
            matrix.append(diff)

        for i in xrange(len(pages_mains_words)-1):
            for j in xrange(i+1,len(pages_mains_words)):
                dist = self.equal_words(pages_mains_words[i],pages_mains_words[j])
                matrix[i][j]= dist
                maxi = max(maxi, dist)
                mini = min(mini, dist)
        print str(maxi) +" " + str(mini)
        mini = mini*0.9
        maxi = maxi*1.1
        for i in xrange(len(pages_mains_words)-1):
            for j in xrange(i+1,len(pages_mains_words)):
                matrix[i][j] = (1.0*matrix[i][j] - mini)/ (maxi-mini)
        return matrix
