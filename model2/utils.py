import string

str_translator = str.maketrans('', '', string.punctuation + '”' + '“' + '’' + '´')

def removePunc(word):
	return word.translate(str_translator)

def checkHasCapital(word):
	for letter in word:
		if letter.isupper():
			return True
	return False