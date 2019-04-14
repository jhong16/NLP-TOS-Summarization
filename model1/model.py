import parse


class SummaryModel(object):
    def __init__(self, sentence_tokens):
        self.sentences = list()
        for sentence in sentence_tokens:
            words = parse.word_tokenize_tos(sentence)
            self.sentences.append(Sentence(sentence, words))

    def __repr__(self):
        s = ""
        for sentence in self.sentences:
            s += str(sentence) + "\n"
        return s

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
        s += f"Rank: {self.rank}\n"
        return s

class Word(object):
    def __init__(self, token, idf=None, tf=None):
        self.token = token
        self.idf = idf
        self.tf = tf


def loadl(sentences: list):
    """
    loads a list of list of words.
    """
    # print(sentences[0])
    # return SummaryModel()
    pass

def load(fp):
    """Takes in a file descriptor, normalizes and returns a Summary Model
    """
    data = fp.read()
    sent_tokenized = parse.sentence_tokenize_tos(data)
    return SummaryModel(sent_tokenized)
