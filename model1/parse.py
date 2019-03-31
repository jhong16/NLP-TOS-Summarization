from nltk import sent_tokenize, word_tokenize

# takes text file
def parse_tos(filename):
	# how do I figure out where sentences end??
	with open(filename, 'r') as f:
		data = f.read()
	
	return word_tokenize_tos(sentence_tokenize_tos(data))

def sentence_tokenize_tos(data):
	# return utf_encode(sent_tokenize(data.decode('utf-8'))) // this was needed for python2
	return sent_tokenize(data)

def word_tokenize_tos(full_sentences):
	return [word_tokenize(s) for s in full_sentences]

# add punctuation to stop words?
def parse_stop_words(filename):
	with open(filename, 'r') as f:
		data = f.readlines()
	return [stop_word.strip() for stop_word in data]

def utf_encode(sentences):
	return [s.encode('utf-8') for s in sentences]