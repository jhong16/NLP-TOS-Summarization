from nltk import sent_tokenize, word_tokenize

# takes text file
def parse_tos(filename):
	with open(filename, 'r') as f:
		data = f.read()
	
	return word_tokenize_tos(sentence_tokenize_tos(data))

# takes a file of raw ToS text, returns list of sentences
def sentence_tokenize_tos(data):
	return sent_tokenize(data)

# takes list of sentences, returns list of lists of words
def word_tokenize_tos(full_sentences):
	return [word_tokenize(s) for s in full_sentences]

# takes text file of list of stopwords separated by newline
def word_tokenize_sent(full_sentence):
	return word_tokenize(full_sentence)

# add punctuation to stop words?
def parse_stop_words(filename):
	with open(filename, 'r') as f:
		data = f.readlines()
	return [stop_word.strip() for stop_word in data]

def utf_encode(sentences):
	return [s.encode('utf-8') for s in sentences]

# get tf, idf, POS tag, etc. here?