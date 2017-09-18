from nltk import ngrams
from nltk.corpus import stopwords, brown
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from collections import Counter, defaultdict
import re
import os

class PoemGrammer(object):

    def __init__(self, poems_folder):
        self.stemmer = SnowballStemmer("english")
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = set(stopwords.words('english'))
        self.corpus = brown

        self.n_grams = self.all_ngrams(poems_folder)

    def viable_grams(self):
        return self.filter_ngrams().keys()

    def prepare_poem(self, f):
        poem = open(f, 'r').read()
        poem = poem.decode('utf-8', errors='replace')
        poem = re.sub('\n', ' ', poem)
        sentences = sent_tokenize(poem)
        return sentences

    def all_ngrams(self, filepath):
        all_poem_ngrams = Counter()
        for f in os.listdir(filepath):
            sentences = self.prepare_poem(filepath + f)
            poem_ngrams = self.extract_from_text(sentences)
            all_poem_ngrams += poem_ngrams
        
        # Filter out n_grams that appear more than once
        # and ones with a stopword as last word
        singlets = set([k for k, v in all_poem_ngrams.items()
                        if v == 1 and k[-1] not in self.stopwords])

        return singlets

    def corpus_grammer(self, corpus_output_file):
        with open(corpus_output_file, 'w') as f:
            for sentence in self.corpus.sents():
                sentence = ' '.join(sentence)
                sentence = re.sub(r'[^\w\s\'\"]', '', sentence)
                sentence = re.sub(r'\d', '', sentence)
                sentence = sentence.lower()
                for i in range(3, 11):
                    grams = ngrams(sentence.split(), i)
                    for gram in grams:
                        f.write(' '.join(gram) + '\n')

    def extract_from_text(self, sentences):
        ngrams_counter = Counter()
        for sentence in sentences:
            sentence = re.sub(r'[^\w\s\']', '', sentence)
            sentence = re.sub(r'\d', '', sentence)
            sentence = sentence.lower()
            for i in range(3, 11):
                grams = ngrams(sentence.split(), i)
                ngrams_counter.update(grams)
        return ngrams_counter

    def filter_ngrams(self):
        return set(filter(lambda x: x not in self.corpus_grams, self.n_grams))


if __name__ == '__main__':
    crush = PoemGrammer('poems/')
    crush.corpus_grammer('brown_ngrams.txt')

