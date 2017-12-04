
############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from collections import defaultdict
import math

############################################################
# Hidden Markov Models
############################################################

def load_corpus(path):
    #Open the file
    with open(path) as fileng:
        lines = fileng.readlines() #Get line

    lines = [x.strip() for x in lines]
    #Split each line into tuples
    l = [i.split() for i in lines]
    res = list()
    for pair in l:
        y = [tuple(x.split('=')) for x in pair]
        res.append(y)

    return res
# c = load_corpus("brown-corpus.txt")
# print c[1402]
class Tagger(object):

    def __init__(self, sentences):
        self.context = defaultdict(int)
        self.trans = defaultdict(int)
        self.emit = defaultdict(int)

        self.tprobs = dict()
        self.eprobs = dict()

        for line in sentences:
            previous = "<start>"
            self.context[previous]+=1
            for word,tag in line:
                self.trans[(previous, tag)]+=1
                self.context[tag]+=1
                self.emit[(tag, word)]+=1
                previous = tag
            self.trans[(previous, "</start>")]+=1

        #Store all the transition probabilities
        for x in self.trans.keys():
            self.tprobs[x] = -1*math.log(float(self.trans[x])/float(self.context[x[0]]))
            #print self.tprobs[x]

        #Emission probabilities go here
        for x in self.emit.keys():
            #Laplace Add-one smoothing here
            self.eprobs[x] = -1*math.log(float(self.emit[x] + 1.0)/float(self.context[x[0]] + len(self.context.keys())))
            #print "E", x, float(self.emit[x] + 1.0)/float(self.context[x[0]] + len(self.context.keys()))

    def most_probable_tags(self, tokens):
        res = []
        for word in tokens:
            checkKeys = filter(lambda x: x[1] == word, self.eprobs.keys())
            checkValue = min([self.eprobs[x] for x in checkKeys])
            answer = filter(lambda x: self.eprobs[x] == checkValue, checkKeys)
            answer = [x[0] for x in answer]
            res.extend(answer)

        return res
    
    #TODO: Add the Viterbi Algorithm
    def viterbi_tags(self, tokens):
        pass


c = load_corpus("brown-corpus.txt")
t = Tagger(c)
print t.most_probable_tags(["The", "blue", "bird", "sings"])
#['DET', 'NOUN', 'VERB', '.']
