import parse
import RAKE

from lexrank import Summarizer

class Sentence(object):
    def __init__(self, sentence, words, index, rank=None, ne=None):
        self.sentence = sentence
        self.words = [Word(word) for word in words]
        self.rank = rank
        self.named_entities = dict() # start_p: phrase
        self.keywords = None
        self.index = index
        self.keywords = None

    def __repr__(self):
        s = ""
        s += f"Sentence: {str(self.sentence)}\n"
        s += f"Rank: {self.rank}\n  "
        return s

    def word_list(self):
        """Returns a list of the literal words"""
        return [word.token for word in self.words]

    def rake_sentence(self):
        rake = RAKE.Rake(RAKE.SmartStopList())
        # self.keywords = rake.run(self.sentence, maxWords=5, minFrequency=1)
        self.keywords = rake.run(self.sentence)


class WordBank(object):
    def __init__(self, sentences):
        sent_matrix = list()
        for sentence in sentences:
            words = sentence.word_list()
            sent_matrix.append(words)
        self.word_dict = dict()
        self.tf = Summarizer().compute_tf(sent_matrix)
        self.idf = Summarizer().compute_idf(sent_matrix)
        for word, tf in self.tf.items():
            idf = self.idf[word]
            self.word_dict[word] = Word(word, tf=tf, idf=idf)

    def __repr__(self):
        s = ""
        for word, value in self.word_dict.items():
            s += f"{word}: {value}\n"
        return s

    def top(self, n):
        top_dict = dict()
        for key, value in sorted(self.tf.items(), key=lambda x:x[1], reverse=True)[:n]:
            top_dict[key] = value
        return top_dict

class Word(object):
    def __init__(self, token, tf=None, idf=None):
        self.token = token
        self.tf = tf
        self.idf = idf

    def __repr__(self):
        s = ""
        s += f"tf: {str(self.tf)}, idf: {str(self.idf)}"
        return s
