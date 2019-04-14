from lexrank import Summarizer
import parse


class SummaryModel(object):
    def __init__(self, sentence_tokens):
        self.sentences = list()
        for sentence in sentence_tokens:
            words = parse.word_tokenize_sent(sentence)
            self.sentences.append(Sentence(sentence, words))

    def __repr__(self):
        s = ""
        for sentence in self.sentences:
            s += str(sentence) + "\n"
        return s

    def rank_sentences(self):
        """Uses the Summarizer to create a ranking"""
        sent_matrix = list()
        for sentence in self.sentences:
            words = sentence.word_list()
            sent_matrix.append(words)
        summarizer = Summarizer()
        summarizer.create_graph(sent_matrix)
        scores = summarizer.power_method()
        for i in range(0, len(self.sentences)):
            self.sentences[i].rank = scores[i]



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


def load(fp):
    """Takes in a file descriptor, normalizes and returns a Summary Model
    """
    data = fp.read()
    sent_tokenized = parse.sentence_tokenize_tos(data)
    return SummaryModel(sent_tokenized)
