from lexrank import Summarizer
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


class Sentence(object):
    def __init__(self, sentence, words, rank=None, ne=None):
        self.sentence = sentence
        self.words = [Word(word) for word in words]
        self.rank = rank
        self.named_entities = dict() # start_p: phrase

    def __repr__(self):
        s = ""
        s += f"Sentence: {str(self.sentence)}\n"
        s += f"Rank: {self.rank}\n  "
        return s

    def word_list(self):
        """Returns a list of the literal words"""
        return [word.token for word in self.words]


class WordBank(object):
    def __init__(self, sentences):
        sent_matrix = list()
        for sentence in sentences:
            words = sentence.word_list()
            sent_matrix.append(words)
        self.tf = Summarizer().compute_tf(sent_matrix)

    def __repr__(self):
        s = ""
        for word, tf in sorted(self.tf.items(), key=lambda x:x[1], reverse=True):
            s += f"{word}: {tf}\n"
        return s

    def top(self, n):
        top_dict = dict()
        for key, value in sorted(self.tf.items(), key=lambda x:x[1], reverse=True)[:n]:
            top_dict[key] = value
        return top_dict

class Word(object):
    def __init__(self, token):
        self.token = token


def load(fp):
    """Takes in a file descriptor, normalizes and returns a Summary Model
    """
    data = fp.read()
    sent_tokenized = parse.sentence_tokenize_tos(data)
    return SummaryModel(sent_tokenized)
