from lexrank import Summarizer
from model import Sentence, Word
from sentence_compress import SentenceCompress
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

    # maybe compress_sentences should be an option when initializing summary model?
    def compress_sentences(self):
        compressor = SentenceCompress()
        compressor.syntax_parse(self.sentences[:30]) # self.sentences is a list of Sentences
        sentences = compressor.compress()
        self.sentences = []
        for sentence in sentences:
            if len(sentence) > 0:
                words = parse.word_tokenize_sent(sentence)
                self.sentences.append(Sentence(sentence, words))

def load(fp):
    """Takes in a file descriptor, normalizes and returns a Summary Model
    """
    data = fp.read()
    sent_tokenized = parse.sentence_tokenize_tos(data)
    return SummaryModel(sent_tokenized)
