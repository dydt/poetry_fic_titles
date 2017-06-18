from nltk import ngrams
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from collections import Counter, defaultdict
import re
import os
import csv
import math

class PoemGrammer(object):

    def __init__(self, poems_folder, threshold):
        self.stemmer = SnowballStemmer("english")
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = set(stopwords.words('english'))
        self.frequencies = self.word_frequencies('wordfrequencyinfo.csv', 
                                                 4500)
        self.n_grams = self.all_ngrams(poems_folder)
        self.viable_grams = self.filter_frequencies(threshold)

    def word_frequencies(self, freq_file, default_val):
        frequencies = defaultdict(lambda: default_val)
        with open(freq_file, 'rb') as words:
            freq_csv = csv.DictReader(words)
            for row in freq_csv:
                key = self.stemmer.stem(self.lemmatizer.lemmatize(row['Word']))
                frequencies[key] = float(row['Frequency'])
        return frequencies

    def compute_frequencies(self, n_gram):
        total = 0
        for word in n_gram: 
            if word in self.stopwords:
                continue
            stemmed_word = self.stemmer.stem(self.lemmatizer.lemmatize(word, pos='v'))
            score = 100/math.sqrt(self.frequencies[stemmed_word])
            total += score
        return total

    def prepare_poem(self, f):
        poem = open(f, 'r').read()
        poem = poem.decode('utf-8', errors='replace')
        sentences = re.split(r'[.?]', poem)
        return sentences

    def all_ngrams(self, filepath):
        all_poem_ngrams = Counter()
        for f in os.listdir(filepath):
            sentences = self.prepare_poem(filepath + f)
            poem_ngrams = self.extract_from_text(sentences)
            all_poem_ngrams += poem_ngrams
        
        # Filter out n_grams that appear more than once
        # and ones with a stopword as last word
        singlets = [k for k, v in all_poem_ngrams.items() 
                        if v == 1 and k[-1] not in self.stopwords]

        return singlets

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

    def filter_frequencies(self, threshold):
        return set(filter(lambda x: self.compute_frequencies(x) > threshold, self.n_grams))


if __name__ == '__main__':
    crush = PoemGrammer('poems/', 2)
    with open('frequencies.txt', 'w') as f:
        for n_gram in crush.n_grams:
            f.write(' '.join(n_gram) + ',' + str(crush.compute_frequencies(n_gram)) + '\n')
    with open('viable_grams.txt', 'w') as f:
        for n_gram in crush.viable_grams:
            f.write(' '.join(n_gram)+ '\n')