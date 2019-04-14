from nltk.tree import Tree
from nltk.parse.stanford import StanfordParser
from math import sqrt

class SentenceCompress:
	def __init__(self, omega=0.001, alpha=2, beta=30):
		self.parser = StanfordParser()
		self.omega = omega # Proper noun importance. should experiment with this?
		self.alpha = alpha # min sentence length
		self.beta = beta # max sentence length

	# takes an array of sentences (which are arrays of strings?)
	def syntax_parse(self, sentences):
		self.parsed_sentences = self.parser.parse_sents(sentences) # only testing w/ first 10
		for list_iter in self.parsed_sentences:
			for t in list_iter:
				print(t)
				self.traverse_tree(t)

	# input might be Ji hann's word class, which might include POS tag, named entity, that sort of thing 
	def word_significance(self, w):
		# I_j(w_i) =
		# tf_ij x idf_i if w_i is verb or common noun
		# tf_ij x idf_i + omega if w_i is proper noun
		# 0 otherwise
		return 0

	def information_density_measurement(self):
		pass

	def min_length(self, sentence):
		return min(len(sentence), self.alpha)

	def max_length(self, sentence):
		orig_length = len(sentence)
		if orig_length > self.beta:
			return self.beta + sqrt(orig_length - self.beta)
		return orig_length

	def traverse_tree(self, tree):
		clause_sig = 0
		for node in tree:
			# print(node)
			if type(node) == Tree:
				print(node.label())
				# can I immediately ignore some clauses
				sig = self.traverse_tree(node)
				clause_sig += sig
				# assign importance to clause, based on returned importance and importance of clause types
				# how should I get
			else: # word string
				print(node)
				# return word_significance
				word_sig = self.word_significance(node)
				if word_sig > self.omega:
					clause_sig += word_sig
		return clause_sig

# Sets based on what's safest to remove. The higher the set number, the more important the clause probably is, and removing it
# should be more based on word importance and level of compression wanted.

# Set 0
# - parenthetical elements. I'm not sure if I can find this with stanford parser so it might be some kind of preprocessing.
# - adverbs except negative some temporal or degree adverbs
# - adjectives of what kind? different than Chinese

# Set 1
# - children of NP nodes except temporal nouns and proper nouns and the last noun word? does this make sense for English?
# - can I try to get rid of some things in really long lists if word importance is low enough?

# Set 2
# - prepositional phrases

# will I be assigning importance to clauses, and then running over tree again to choose what to ignore, or doing it on the fly?
# do I need a function to go over trimmed tree and reconstruct it? let's hope it will still make sense.

# mention in presentation that I had to think about English rules instead of Chinese rules