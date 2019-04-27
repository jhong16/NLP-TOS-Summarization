# from highlight import highlight
from lexrank import Summarizer
from model import Sentence, Word, WordBank
from sentence_compress import SentenceCompress
from preprocess import preprocess
import parse
import re


class SummaryModel(object):
    def __init__(self, sentence_tokens):
        self.sentences = list()
        for i, sentence in enumerate(sentence_tokens):
            words = parse.word_tokenize_sent(sentence)
            self.sentences.append(Sentence(sentence, words, i))
        self.word_bank = WordBank(self.sentences)
        

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

    def common_words(self, top_n):
        return self.word_bank.top(top_n)

    def compress_sentences(self, alpha=50, beta=500, path_to_jar=None, path_to_models_jar=None):
        compressor = SentenceCompress(alpha=alpha, beta=beta, path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar, word_bank=self.word_bank)
        compressor.syntax_parse(self.sentences) # self.sentences is a list of Sentences
        sentences = compressor.compress()
        self.sentences = []
        for i, sentence in enumerate(sentences):
            if len(sentence) > 0:
                words = parse.word_tokenize_sent(sentence)
                self.sentences.append(Sentence(sentence, words, i))

    def shorten(self, percentage):
        if percentage < 0.01 or percentage > 1:
            print("Invalid Percentage")
            return
        ranks = [sentence.rank for sentence in self.sentences]
        threshold = sorted(ranks, reverse=True)[0:int(len(ranks) * percentage)][-1]

        short_summary = list()
        for sentence in self.sentences:
            if sentence.rank > threshold:
                short_summary.append(sentence)
        return short_summary

    def top_sent(self, num):
        sent_rank = list()
        for sentence in self.sentences:
            sent_rank.append((sentence, sentence.rank))
        
        top_rank = sorted(sent_rank, key=lambda x: x[1], reverse=True)[0:num]
        order_top = [x[0] for x in top_rank]
        return order_top

    def keyword_summary(self, keyword):
        summary = list()
        for sentence in self.sentences:
            match = re.search(keyword, sentence.sentence, flags=re.IGNORECASE)
            if match is not None:
                summary.append(sentence)
        return summary
    
    def rake_sentences(self, maxWords=5, minFrequency=1):
        for sentence in self.sentences:
            sentence.rake_sentence(maxWords=maxWords, minFrequency=minFrequency)

    def top_keyword_sent(self, num):
        sent_rank = list()
        for sentence in self.sentences:
            sent_rank.append((sentence, sentence.keywords_rank))

        top_rank = sorted(sent_rank, key=lambda x: x[1], reverse=True)[0:num]
        order_top = [x[0] for x in top_rank]
        return order_top

def load(fp):
    """Takes in a file descriptor, normalizes and returns a Summary Model
    """
    data = fp.read()
    sent_tokenized = parse.sentence_tokenize_tos(data)
    return SummaryModel(sent_tokenized)

    # to use processed html files:
    # tos = preprocess('../data/url2html_output.json')
    # return SummaryModel(tos['rovio'])
