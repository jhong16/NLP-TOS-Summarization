from model import Sentence, Word
# import model # I don't like that I have to import this
from nltk.tree import Tree
from nltk.parse.stanford import StanfordParser
from math import sqrt
import string, re

class SentenceCompress:
	def __init__(self, omega=0.001, alpha=20, beta=100):
		""" Initialize syntactic parser and parameters for word significance and
			desired sentence length."""
		self.parser = StanfordParser()
		self.omega = omega # Proper noun importance
		self.alpha = alpha # min sentence length in characters
		self.beta = beta # max sentence length in characters
		self.parsed_sentences = None

	def syntax_parse(self, sentences):
		""" Take list of Sentence objects and get syntactic parse trees. """
		self.parsed_sentences = self.parser.raw_parse_sents([s.sentence for s in sentences]) # only testing w/ first 10

	def compress(self):
		""" Apply rules in set 0 and set 1. """
		compressed_sentences = []
		for list_iter in self.parsed_sentences:
			for t in list_iter:
				original = self.tree_to_sentence(t)
				min_len = self.min_length(original)
				max_len = self.max_length(original)
				if len(original) >= min_len:
					self.set_0(t) # probably not goog that this relies on side effects
					t = self.set_1(t, max_len, min_len)
					s = self.tree_to_sentence(t) # could check if this is above min and desired max length
					compressed_sentences.append(s)
		return compressed_sentences

	# input might be Ji hann's word class, which might include POS tag, named entity, that sort of thing 
	# this should be a word object
	def word_significance(self, w): # I_j(w_i)
		# if True: # for now. should be if common noun
		# 	return w.tf * w.idf # tf_ij x idf_i if w_i is verb or common noun
		# elif False: # for now. should if proper noun
		# 	return w.tf * w.idf + self.omega # tf_ij x idf_i + omega if w_i is proper noun
		return 0 # 0 otherwise

	def information_density_measurement(self):
		# TODO: implement (if needed)
		pass

	def min_length(self, sentence):
		""" Desired minimum length of sentence. """
		return min(len(sentence), self.alpha)

	def max_length(self, sentence):
		""" Desired maximum length of sentence, depending on length of original sentence. """
		orig_length = len(sentence)
		if orig_length > self.beta:
			return self.beta + sqrt(orig_length - self.beta)
		return orig_length

	def traverse_tree_set_0(self, tree, phrases):
		""" Trim elements matching phrase types in 'phrases'.
			Should this be iterative? """
		clause_sig = 0
		for index, node in enumerate(tree): # iterate backwards?
			if type(node) == Tree:
				# can I immediately ignore some clauses
				sig = self.traverse_tree_set_0(node, phrases) # if subtree is too significant, don't remove. But what is too significant?
				# assign importance to clause, based on returned importance and importance of clause types
				clause_sig += sig
				# remove adverbs, parenthetical statements, and fragments
				if node.label() in phrases: # should check that adverb is not negative
					tree[index] = None
			else: # word string
				# return word_significance
				word_sig = self.word_significance(node) # I need to have a fast way of looking up word object
				if word_sig > self.omega:
					clause_sig += word_sig
		return clause_sig

	def set_0(self, tree):
		""" Get rid of clauses that very likely arne't important. No need for iteration. """
		phrases = ['ADVP', 'PRN', 'FRAG', 'INTJ']
		self.traverse_tree_set_0(tree, phrases)

	def set_1_find_xp_levels(self, tree, decl_clause, level, found_xp):
		""" Get number of levels of outermost XP pattern.
			Pattern is [XP [XP ...] ... ] where XP is NP, VP, or S. """
		clause_sig = 0
		max_levels = level
		for index, node in enumerate(tree):
			if type(node) == Tree:
				if index == 0 and node.label() == decl_clause:
					found_xp = True
					levels = self.set_1_find_xp_levels(node, decl_clause, level+1, found_xp)
					max_levels = max(levels, max_levels)
				elif not found_xp: # shouldn't traverse if found outer level XP pattern already. just return max levels
					levels = self.set_1_find_xp_levels(node, decl_clause, level, found_xp)
		return max_levels

	def set_1_remove_outer_xp(self, tree, decl_clause):
		""" remove outermost tree in XP pattern. Find first subtree of type decl_clause and return.
			Iterate left to right, because if there's multiple options then return the leftmost subtree.
		"""
		for index, node in enumerate(tree):
			if type(node) == Tree:
				if node.label() == decl_clause:
					# remove outer S by returning child.
					for index2, child_node in enumerate(node):
						if type(child_node) == Tree and child_node.label() == decl_clause:
							return node[index2]
					# return tree[index,0] # not necessarily at 0 index...
				else: # keep going down the tree...
					subtree = self.set_1_remove_outer_xp(node, decl_clause)
					if subtree is not None:
						return subtree
		return None # return self? idk

	def set_1_trailing(self, tree, phrase_type):
		""" Get rid of first trailing (deepest rightmost) PP or SBAR. Iteration is reversed so
			rightmost elements will be looked at first. """
		for index, node in reversed(list(enumerate(tree))):
			if type(node) == Tree:
				if index == len(tree)-1 and node.label() == phrase_type:
					tree[index] = None
					return True
				else:
					found = self.set_1_trailing(node, phrase_type)
					if found:
						return True
		return False

	def set_1(self, tree, max_len, min_len):
		""" Iteratively remove clauses and phrases in an attempt to reduce sentence to
			less than max_len. """
		XPs = ['S', 'NP', 'VP']
		for clause in XPs:
			current_sentence_len = len(self.tree_to_sentence(tree))
			if (current_sentence_len < max_len):
				break
			levels = self.set_1_find_xp_levels(tree, clause, 0, False)
			while levels > 1:
				current_sentence_len = len(self.tree_to_sentence(tree))
				if (current_sentence_len < max_len):
					break
				tree = self.set_1_remove_outer_xp(tree, clause)
				levels = self.set_1_find_xp_levels(tree, clause, 0, False)
		trailing = ['PP', 'SBAR']
		for phrase in trailing:
			current_sentence_len = len(self.tree_to_sentence(tree))
			if (current_sentence_len < max_len):
				break
			self.set_1_trailing(tree, phrase)
		return tree

	def tree_to_sentence_helper(self, tree, sentence_str):
		""" Recursive helper to convert nltk tree, which may have nodes with value 'None',
			to sentence """
		for index, node in enumerate(tree):
			if type(node) == Tree:
				sentence_str = self.tree_to_sentence_helper(node, sentence_str)
			elif node != None:
				if node[0] in string.punctuation:
					return sentence_str + node
				else:
					return sentence_str + ' ' + node
		return sentence_str

	def tree_to_sentence(self, tree):
		""" convert nltk tree, which may have nodes with value 'None', to sentence. """
		s = self.tree_to_sentence_helper(tree, '').strip()
		if len(s) == 0:
			return s
		if s[0] in string.punctuation:
			s = s.lstrip(string.punctuation)
		if s[0].islower():
			s = s[0].upper() + s[1:]
		if s[-1] not in string.punctuation:
			s = s + '.'
		return s

# Sets based on what's safest to remove. The higher the set number, the more important the clause probably is, and removing it
# should be more based on word importance and level of compression wanted.

# Set 0
# - parenthetical elements. I'm not sure if I can find this with stanford parser so it might be some kind of preprocessing.
# - adverbs except negative some temporal or degree adverbs. ADVP.
# - adjectives of what kind? different than Chinese
# - Interjections and fragments? entire sentence may be interjection though, that should probably be removed in preprocessing.

# Set 1
# - children of NP nodes except temporal nouns and proper nouns and the last noun word? does this make sense for English?
# - can I try to get rid of some things in really long lists if word importance is low enough?
# - constructions of form [XP [XP ..] ...], remove higher XP, where XP is NP, VP or S (requires choosing subtree and getting rid of rest)
# - trailing prepositional phrases (PP) and SBARs

# will I be assigning importance to clauses, and then running over tree again to choose what to ignore, or doing it on the fly?
# do I need a function to go over trimmed tree and reconstruct it? let's hope it will still make sense.

# start from deepest rightmost node when iteratively getting rid of things?
