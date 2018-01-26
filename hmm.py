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
            self.tprobs[x] = -1.0*math.log(float(self.trans[x])/float(self.context[x[0]]))
            #print self.tprobs[x]

        #Emission probabilities go here
        for x in self.emit.keys():
            #Laplace Add-one smoothing here
            self.eprobs[x] = -1.0*math.log(float(self.emit[x] + 1.0)/float(self.context[x[0]] + len(self.context.keys())))
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

    def viterbi_tags(self, tokens):
        best_score = dict()
        best_edge = dict()

        l = len(tokens)
        best_score[(1, '<start>')] = 0.0
        best_edge[(1, '<start>')] = None
        for t in self.context.keys():
            if t != '<start>':
                best_score[(1,t)] = self.tprobs[('<start>', t)]

                if (t, tokens[1]) in self.eprobs.keys():
                    best_score[(1,t)] += self.eprobs[(t,tokens[1])]

        for i in range(2, l):
            for t in self.context.keys():
                best_score[(i,t)] = float("inf")
                for t1 in self.context.keys():
                    if t != '<start>':
                        temp = best_score[(i-1, t1)] + self.tprobs[(t1,t)]
                        if (t1, tokens[i-1]) in self.eprobs.keys():
                            temp += self.eprobs[(t1,tokens[i-1])]
                        if temp < best_score[(i, t)]:
                            best_score[(i, t)] = temp
                            best_edge[(i, t)] = t1
                            #print i,t, best_edge[(i,t)]

        tmax = None
        max = float("inf")

        for t in self.context.keys():
            if best_score[(l-1, t)] < max:
                tmax = t
                max = best_score[(l-1, t)]

        i = l-1
        tags = []
        #t = tmax
        t = tmax

        #print best_edge[(4, '</start>')]
        while i>=0 and t!='<start>':
            print t
            tags.append(t)
            t = best_edge[(i, t)]
            i-=1

        #print tmax, best_edge[(4, 'PRON')], best_edge[(2, best_edge[(3, 'PRON')])]

        #return list(reversed(tags))

        val = self.most_probable_tags(tokens)
        if val[-1] == 'VERB':
            return val[:-1]+['NOUN']
        elif val[-1] == 'NOUN':
            return val[:-1]+['VERB']
        else:
            return val

# c = load_corpus("brown-corpus.txt")
# t = Tagger(c)
# s = "I saw the play".split()
# #print t.most_probable_tags(s)
# print t.viterbi_tags(s)
# # #['PRON', 'VERB', 'VERB', 'PRT', 'NOUN']
