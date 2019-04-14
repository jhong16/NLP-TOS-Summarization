import numpy as np
from parse import parse_stop_words
from math import log, sqrt
from operator import itemgetter
import string

class Summarizer(object):
	def __init__(self):
		self.stop_words = set(parse_stop_words("../data/stopwords.txt")) | set(string.punctuation)
		self.sentences = None
		self.term_freq = None
		self.inverse_doc_freq = None
		self.graph = None
		self.epsilon = 0.1
		self.threshold = 0.1

	# adjacency matrix, since graph is dense
	def create_graph(self, sentences):
		self.sentences = sentences
		self.term_freq = self.compute_tf(sentences)
		self.inverse_doc_freq = self.compute_idf()

		n = len(self.sentences)
		self.graph = np.zeros((n, n))
		self.degrees = np.zeros(n)

		for u in range(n):
			for v in range(n):
				# add edge value, which is similarity
				self.graph[u][v] = self.compute_similarity(sentences[u], sentences[v])

				if self.graph[u][v] > self.threshold:
					self.graph[u][v] = 1.0
					self.degrees[u] += 1
				else:
					self.graph[u][v] = 0.0

		# TODO: implement
		# then iterate again to compute ranking based on weights
		for u in range(n):
			for v in range(n):
				# do I want this? setting to 1 seems extreme
				if self.degrees[u] == 0:
					self.degrees[u] = 1

				self.graph[u][v] = self.graph[u][v] / self.degrees[u]

		return self.graph

	# TODO: implement
	def compute_similarity(self, sentence1, sentence2):
		return self.idf_modified_cosine(sentence1, sentence2)

	# compute term frequency (could still be useful)
	# should this actually be number of times word occurs in sentence?
	def compute_tf(self, sentences):
		total_words = sum(len(s) for s in sentences)
		term_freq = dict() # sum(s.count() for s in sentences)

		# find frequencies of words in document and in individual sentence
		for s in sentences:
			for word in s:
				if word not in self.stop_words:
					if word in term_freq:
						term_freq[word] += 1.0
					else:
						term_freq[word] = 1.0

		# compute term frequency ratio
		for word in term_freq:
			term_freq[word] /= float(total_words)

		return term_freq

	# for this purpose, is idf = log(total # of sentences / # of sentences containing word?)
	def compute_idf(self):
		N = len(self.sentences)
		inverse_doc_freq = dict()

		for s in self.sentences:
			for word in s:
				if word not in self.stop_words:
					if word in inverse_doc_freq:
						inverse_doc_freq[word] += 1.0
					else:
						inverse_doc_freq[word] = 1.0

		for word in inverse_doc_freq:
			inverse_doc_freq[word] = log(N / inverse_doc_freq[word])

		return inverse_doc_freq

	def idf_modified_cosine(self, sentence1, sentence2):
		unique_words_1 = set(sentence1) - self.stop_words
		unique_words_2 = set(sentence2) - self.stop_words
		common_words = unique_words_1 & unique_words_2

		numerator = 0
		for w in common_words:
			# did I not do term_freq in the right way?
			# should it be more on a sentence level?
			numerator += (self.term_freq[w] * self.inverse_doc_freq[w]) ** 2

		sum1 = 0
		sum2 = 0
		for w1 in unique_words_1:
			sum1 += (self.term_freq[w1] * self.inverse_doc_freq[w1]) ** 2
		for w2 in unique_words_2:
			sum2 += (self.term_freq[w2] * self.inverse_doc_freq[w2]) ** 2
		denominator = sqrt(sum1) * sqrt(sum2)

		return numerator / float(denominator)

	def power_method(self):
		n = len(self.sentences)
		transposed_graph = self.graph.T
		p_t = np.full(n, 1.0 / float(n))

		delta = 1.0
		while delta > self.epsilon:
			p_prev = p_t
			p_t = np.dot(transposed_graph, p_prev)
			delta = np.linalg.norm(np.subtract(p_t, p_prev))

		return p_t

	def rank_sentences(self, p_vector):
		assert len(p_vector) == len(self.sentences)
		sentence_to_ranking = dict()
		for i in range(len(self.sentences)):
			sentence_to_ranking[' '.join(self.sentences[i])] = p_vector[i]

		ranked = sorted(sentence_to_ranking.items(), key=itemgetter(1), reverse=True)

		return ranked
