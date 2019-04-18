from highlighter import rake, highlight
from lexrank import Summarizer
from model import Sentence, Word, WordBank
from sentence_compress import SentenceCompress
from preprocess import preprocess
import parse


class SummaryModel(object):
    def __init__(self, sentence_tokens):
        self.sentences = list()
        for sentence in sentence_tokens:
            words = parse.word_tokenize_sent(sentence)
            self.sentences.append(Sentence(sentence, words))
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

    # maybe compress_sentences should be an option when initializing summary model?
    def compress_sentences(self):
        compressor = SentenceCompress(alpha=50, beta=500)
        compressor.syntax_parse(self.sentences) # self.sentences is a list of Sentences
        sentences = compressor.compress()
        self.sentences = []
        for sentence in sentences:
            if len(sentence) > 0:
                words = parse.word_tokenize_sent(sentence)
                self.sentences.append(Sentence(sentence, words))

    def highlight_phrases(self):
        for sentence in self.sentences:
            sentence.keywords = rake(sentence.sentence)

        html_output = '''<style>
        body { background-color:white; }
        .red { background-color:#ffcccc; }
        .orange { background-color:#FFFF00; }
        .yellow { background-color:#ff9966; }
        .green { background-color:#66ff66; }
        .blue { background-color:#00ffff; }
        .purple { background-color:#ff99ff; }
        p { background-color:#FFFFFF; }
        </style>'''

        for sentence in self.sentences:
            html_output += highlight(sentence.sentence, sentence.keywords)

        return html_output
                
def load(fp):
    """Takes in a file descriptor, normalizes and returns a Summary Model
    """
    data = fp.read()
    sent_tokenized = parse.sentence_tokenize_tos(data)
    return SummaryModel(sent_tokenized)

    # tos = preprocess('../data/url2html_output.json')
    # return SummaryModel(tos['rovio'])
