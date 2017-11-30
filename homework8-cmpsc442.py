############################################################
# CMPSC 442: Homework 8
############################################################

student_name = "Devansh Modi"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.



############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    #Open the file
    with open(path) as fileng:
        lines = fileng.readlines() #Get line

    lines = [x.strip() for x in lines]

    #Split each line into tuples
    l = [i.split() for i in lines]
    res = []
    for pair in l:
        y = [tuple(x.split('=')) for x in pair]
        res.append(y)

    return res

class Tagger(object):

    def __init__(self, sentences):
        pass

    def most_probable_tags(self, tokens):
        pass

    def viterbi_tags(self, tokens):
        pass

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
