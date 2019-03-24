import numpy as np
from parse import parse_stop_words
from math import log

class Summarizer():
	def __init__(self):
		self.stop_words = set(parse_stop_words("../data/stopwords.txt"))
		self.sentences = None
		self.term_freq = None
		self.inverse_doc_freq = None
		self.graph = None

	# adjacency matrix, since graph is dense
	def create_graph(self, sentences):
		self.sentences = sentences
		self.term_freq = self.compute_tf()
		self.inverse_doc_freq = self.compute_idf()

		n = len(self.sentences)
		self.graph = np.zeros((n, n))

		for u in range(n):
			for v in range(n):
				# add edge value, which is similarity
				self.graph[u][v] = self.compute_similarity(sentences[u], sentences[v])

		# TODO: implement
		# then iterate again to compute ranking based on weights
		for u in range(n):
			for v in range(n):
				pass

	# TODO: implement
	def compute_similarity(self, sentence1, sentence2):
		return 0

	# compute term frequency (could still be useful)
	# should this actually be number of times word occurs in sentence?
	def compute_tf(self):
		total_words = sum(len(s) for s in self.sentences)
		term_freq = dict() # sum(s.count() for s in sentences)

		# find frequencies of words in document and in individual sentence
		for s in self.sentences:
			for word in s:
				if word not in self.stop_words:
					if word in term_freq:
						term_freq[word] += 1.0
					else:
						term_freq[word] = 1.0

		# compute term frequency ratio
		for word in term_freq:
			term_freq[word] /= total_words

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
			inverse_doc_freq[word] = log(N/inverse_doc_freq[word])

		return inverse_doc_freq

	def tf_idf(self, word1, word2):
		return self.term_freq[word1] * self.inverse_doc_freq[word2]
