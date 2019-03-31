from nltk.tree import Tree
from nltk.parse.stanford import StanfordParser

class SentenceCompress:
	def __init__(self):
		self.parser = StanfordParser()

	# takes an array of sentences (which are arrays of strings?)
	def syntax_parse(self, sentences):
		self.parsed_sentences = self.parser.parse_sents(sentences[:10]) # only testing w/ first 10
		for list_iter in self.parsed_sentences:
			for t in list_iter:
				print(t)
				self.traverse_tree(t)

	def word_significance(self, w):
		# I_j(w_i) =
		# tf_ij x idf_i if w_i is verb or common noun
		# tf_ij x idf_i + omega if w_i is proper noun
		# 0 otherwise
		pass

	def traverse_tree(self, tree):
		for node in tree:
			print(node)
			if type(node) == Tree:
				self.traverse_tree(node)
