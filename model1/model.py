import parse


class Sentence(object):
    def __init__(self, sentence, words, rank=None, ne=None):
        self.sentence = sentence
        self.words = list()
        for word in words:
            self.words.append(Word(word))
        self.rank = rank
        self.named_entities = dict() # start_p: phrase

    def __repr__(self):
        s = ""
        s += f"Sentence: {str(self.sentence)}\n"
        s += f"Rank: {self.rank}\n  "
        return s

    def word_list(self):
        """Returns a list of the literal words"""
        word_list = list()
        for word in self.words:
            word_list.append(word.token)
        return word_list

class Word(object):
    def __init__(self, token, idf=None, tf=None):
        self.token = token
        self.idf = idf
        self.tf = tf
