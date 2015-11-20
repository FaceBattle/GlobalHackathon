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
from math import log

class Page:

    name = ""
    metainfo = {}
    index_words = {}
    frequency_word = {}
    last_id_added = 0
    stemmer = LancasterStemmer()

    def __init__(self, name = "", metainfo = {},index_words = {}, frequency_word = {}):
        self.name = name
        self.metainfo = metainfo
        self.index_words = index_words
        self.frequency_word = frequency_word

    def __update_index(self, post_text, post_frequencies):
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
            tf_idf = (-1.0)*count/log(english_freq[word])
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
        self.__update_index(list_words, frequencies)

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
        for id in list_post:
            post = self.get_post(id)
            main_words = post.main_words
            for key,info in main_words.items():
                if page_main_words.has_key(key):
                    page_main_words[key][0] += info[0]
                    page_main_words[key][1] += info[1]
                else:
                    page_main_words[key] = info

        #transform in list
        list_main_words = []
        for key,info in page_main_words.items():
            list_main_words.append(info)

        list_main_words.sort(reverse=True)
        return list_main_words

    def get_post(self, id):
            post = Post(id, self.name)
            post.load()
            return post


    def load(self):
        path = os.getcwd()+"/pages/"+self.name+'/metadata'
        tmp_dict = cPickle.load(open(path,'rb'))
        self.__dict__.update(tmp_dict)

    def save(self):
        path = os.getcwd()+"/pages/"+self.name+'/metadata'
        if not os.path.exists(path):
            os.makedirs(os.getcwd()+"/pages/"+self.name)
            open(path,"w+")
        cPickle.dump(self.__dict__,open(path,'wb'),2)

    def __del__(self):
        self.save()


