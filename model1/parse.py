from nltk import sent_tokenize, word_tokenize

# takes text file
def parse_tos(filename):
	# how do I figure out where sentences end??
	with open(filename, 'r') as f:
		data = f.read()

	full_sentences = utf_encode(sent_tokenize(data.decode('utf-8')))
	split_sentences = []
	for s in full_sentences:
		split_sentences.append(word_tokenize(s))

	return split_sentences

def parse_stop_words(filename):
	with open(filename, 'r') as f:
		data = f.readlines()
	stop_words = []
	for line in data:
		stop_words.append(line.strip())
	return stop_words

def utf_encode(sentences):
	for i in range(len(sentences)):
		sentences[i] = sentences[i].encode('utf-8')
	return sentences