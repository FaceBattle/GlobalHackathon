__author__ = 'danielpazinato'

import nltk
from nltk.probability import *
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from goose import Goose
import cPickle
import os
import string
from Post import *
from nltk.stem.lancaster import LancasterStemmer
import wikiwords
from math import log, sqrt
from textblob import TextBlob

from vaderSentiment.vaderSentiment import sentiment as vaderSentiment


class Page:

    stemmer = LancasterStemmer()

    def __init__(self, name = "", metainfo = None,index_words = None, frequency_word = None):

        if metainfo is None:
            metainfo = {}
        if index_words is None:
            index_words = {}
        if frequency_word is None:
            frequency_word = {}

        self.name = name
        self.metainfo = metainfo
        self.index_words = index_words
        self.frequency_word = frequency_word
        self.last_id_added = 0

        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        self.db_path_meta = os.path.join(APP_ROOT, "pages/"+self.name+'/metadata')

        # print("Page " + name + "created")

    def update_index(self, post_text, post_frequencies):
        """
        PRIVATE
        Update index_words and frequency_word
        Args:
        """
        post_id = self.last_id_added
        for word in post_text:
                if self.index_words.has_key(word):
                    if self.index_words[word][-1] != post_id:
                        self.index_words[word].append(post_id)
                else:
                    self.index_words[word] = [post_id]

        for key, value in post_frequencies.iteritems():
            if self.frequency_word.has_key(key):
                self.frequency_word[key] += value
            else:
                self.frequency_word[key] = value


    def get_list_post_from_index(self, word):
        word = self.stemmer.stem(word)
        if self.index_words.has_key(word):
            return self.index_words[word]
        return []

    def add_post(self, text, metainfo):

        """
        Extract the frequency of words of text and create a Post
        TODO extract related words
        Args:
            text (str): main text or the post
            metainfo (dictionary): title, number of likes and shares, etc
        """
        text = text.encode('ascii','ignore')

        #sentimental analysis
        t = TextBlob(text)
        metainfo["polarity"] = t.sentiment.polarity
        metainfo["subjectivity"] = t.sentiment.subjectivity

        vader = vaderSentiment(text)
        metainfo["vader"] = vader

        text = text.translate(string.maketrans("",""), string.punctuation)

        #removing stop words
        stop = stopwords.words('english')

        #frequency in english language
        english_freq = {}
        reverse_stem = {}
        list_words = []
        for i in text.split():
            i = i.lower()
            if i not in stop:
                freq = wikiwords.freq(i, lambda x: 0.000001)
                st = self.stemmer.stem(i)
                if not reverse_stem.has_key(st):
                    reverse_stem[st] = i
                if english_freq.has_key(st):english_freq[st] += freq
                else: english_freq[st] = freq
                list_words.append(st)

        #get frequencies of words
        frequencies = FreqDist(list_words)
        main_words = []
        for word, count in frequencies.items():
            english_freq[word] /= count
            #print reverse_stem[word] + ": " + str(english_freq[word])
            tf_idf = (-1.0)*log(count+0.1)/(log(english_freq[word]))
            main_words.append([tf_idf, count, reverse_stem[word], word])

        #select just most important words
        main_words.sort(reverse=True)
        NUM_MAX = 100
        if len(main_words) > NUM_MAX:
            main_words = main_words[0:NUM_MAX]

        #create dict
        final_main_words = {}
        for w in main_words:
            final_main_words[w[3]] = w[0:3]

        self.last_id_added += 1
        id = self.last_id_added

        post = Post(id, self.name, metainfo, frequencies, final_main_words, reverse_stem)
        post.save()
        self.update_index(list_words, frequencies)

        self.save()

        return post

    def add_post_url(self, url, metainfo):
        g = Goose()
        try:
            article = g.extract(url=url)
        except TypeError:
            print "TypeError inf trying to add post"
            return
        else:
            metainfo["title"] = article.title
            if article.cleaned_text != "":
                text = metainfo["title"] + " " + article.cleaned_text
            else:
                text =  metainfo["title"] + " " + metainfo["description"] + " " + metainfo["message"]
            text = text.encode('ascii','ignore')
            print text
            return self.add_post(text, metainfo)

    def page_main_words(self, word):
        list_post = self.get_list_post_from_index(word)
        page_main_words = {}
        sentimental = [0,0]
        for id in list_post:
            post = self.get_post(id)
            main_words = post.main_words
            sentimental[0] += post.metainfo["polarity"]
            sentimental[1] += post.metainfo["subjectivity"]
            for key,info in main_words.items():
                if page_main_words.has_key(key):
                    page_main_words[key][0] += info[0]
                    page_main_words[key][1] += info[1]
                else:
                    page_main_words[key] = info
        if len(list_post) != 0:
            sentimental[0] /= len(list_post)
            sentimental[1] /= len(list_post)



        #transform in list
        list_main_words = []
        for key,info in page_main_words.items():
            #info[0] = (-1.0)*info[1]/log(wikiwords.freq(info[2], lambda x: 0.000001))
            #print info
            list_main_words.append(info)

        list_main_words.sort(reverse=True)
        return list_main_words, sentimental

    def get_post(self, id):
            post = Post(id, self.name)
            post.load()
            return post


    def load(self):
        path = self.db_path_meta
        tmp_dict = cPickle.load(open(path,'rb'))
        self.__dict__.update(tmp_dict)

    def save(self):
        path = self.db_path_meta
        if not os.path.exists(path):
            APP_ROOT = os.path.dirname(os.path.abspath(__file__))
            os.makedirs(os.path.join(APP_ROOT, "pages/"+self.name))
            open(path,"w+")
        cPickle.dump(self.__dict__,open(path,'wb'),2)

    def __del__(self):
        self.save()


