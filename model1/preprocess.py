from parse import word_tokenize_tos, sentence_tokenize_tos
import json, string

def split_lists(tos):
	""" Makes sure list elements are split into separate sentences correctly. """
	added_count = 0
	for i, sentence in enumerate(tos[:]):
		if not sentence.startswith(' ---') and '---' in sentence:
			parts = sentence.split('---')
			tos[i+added_count] = parts[0]
			for j in range(1, len(parts)):
				tos.insert(i + added_count + j, '<li>' + parts[j])
			added_count += len(parts)-1
	return tos

def get_sentence_data(filename):
	""" takes filename of JSON file parsed with parsing/url2html.py """

	with open(filename, 'r') as f:
		data = json.load(f)

	tos = dict()
	# what if having list 
	for website_name in data:
		website = data[website_name]
		for url in website: # there should only be one
			tos[website_name] = sentence_tokenize_tos(website[url])
			tos[website_name] = split_lists(tos[website_name])

	return tos

# remove all really short sentences and sentences with mostly meaningless characters
def eliminate(tos):
	final_tos = []
	for sentence in tos:
		if sentence.count('\n') > 3:
			continue
		tmp_sentence = sentence.translate(str.maketrans('', '', string.punctuation))
		tmp_sentence = tmp_sentence.replace('\n', '')
		tmp_sentence = tmp_sentence.replace('\t', '')
		tmp_sentence = tmp_sentence.replace(' ', '')
		if len(tmp_sentence) >= len(sentence) * 0.50 and len(tmp_sentence) >= 20:
			final_tos.append(sentence)
	return final_tos

# concatenate the line introducing the list with the list item, so that the item stands on its own.
def format_code_of_conduct_list_item(head_sentence, list_item):
	item = list_item.lstrip('<li>').strip()
	item = item[0].lower() + item[1:] # start out lower case, should work in most cases
	item = item.rstrip(string.punctuation)
	return head_sentence + ' ' + item + '.'

# deal with special case of negated list situation
def code_of_conduct_negate(tos):
	""" if find list_elem, look at previous sentence and see if 'not' occurs within the
		last six words """
	in_list = False
	for i, sentence in enumerate(tos):
		if not in_list and sentence.startswith('<li>') and i > 0:
			prev_words = word_tokenize_tos([tos[i-1].strip()])[0]
			if len(prev_words) > 6 and prev_words[-1][-1] == ':' and 'not' in prev_words[-6:]:
				head_sentence = tos[i-1].rstrip()[:-1]
				# print(format_code_of_conduct_list_item(head_sentence, tos[i]))
				j = i
				while tos[j].startswith('<li>') and j < len(tos):
					tos[j] = format_code_of_conduct_list_item(head_sentence, tos[j])
					print(tos[j])
					j += 1
			else:
				tos[i] = tos[i].lstrip('<li>')
		elif in_list and not sentence.startswith('<li>'):
			in_list = False
	return tos

def preprocess(filename):
	""" Preprocess ToS in file of format
		{<COMPANY_NAME>: { <DOCUMENT_URL>: <DOCUMENT_TEXT> } """
	documents = get_sentence_data(filename)
	processed_documents = dict()
	for website, tos in documents.items():
		tos = eliminate(tos)
		tos = code_of_conduct_negate(tos)
		processed_documents[website] = tos
	return processed_documents

# for now
if __name__ == '__main__':
	# should I be calling parsing url2html code here?
	preprocess('../data/url2html_output.json')
