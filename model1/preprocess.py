from parse import word_tokenize_tos, sentence_tokenize_tos
import json, string

def split_lists(tos):
	final_tos = tos.copy()
	added_count = 0
	for i, sentence in enumerate(tos[:]):
		if not sentence.startswith('---') and '---' in sentence:
			# print(sentence)
			parts = sentence.split('---')
			tos[i+added_count] = parts[0]
			tos.insert(i+added_count+1, '<li>' + parts[1])
			print(parts[1:])
			# final_tos[i+added_count] = parts[0]
			# final_tos.insert(i+added_count+1, parts[1])
			added_count += 1

			# # print(parts)
			# final_tos[i+added_count] = parts[0]
			# for j in range(1,len(parts)):
			# 	final_tos.insert(i+added_count+j, '<li>' + parts[j])
			# 	# print("list sentence", sentence, final_tos[i+added_count+j])
			# added_count += len(parts)-1
		# else:
		# 	final_tos[i+added_count] = sentence
	# return final_tos
	return tos

# takes filename of JSON file parsed with parsing/url2html.py
def get_sentence_data(filename):
	# call parsing functions?
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
	# if find list_elem, look at previous sentence and see if 'not' occurs within the last five words...
	# last five not including ':' I guess
	in_list = False
	for i, sentence in enumerate(tos):
		if not in_list and sentence.startswith('<li>') and i > 0:
			prev_words = word_tokenize_tos([tos[i-1].strip()])[0]
			# print("prev_words", prev_words[-5:])
			if len(prev_words) > 6 and prev_words[-1][-1] == ':' and 'not' in prev_words[-6:]:
				head_sentence = tos[i-1].rstrip()[:-1]
				print(format_code_of_conduct_list_item(head_sentence, tos[i]))
				j = i
				while tos[j].startswith('<li>') and j < len(tos):
					tos[j] = format_code_of_conduct_list_item(head_sentence, tos[j])
					print("!!!!!", tos[j])
					j += 1
			else:
				tos[i] = tos[i].lstrip('<li>')
		elif in_list and not sentence.startswith('<li>'):
			in_list = False
	return tos

def preprocess(filename):
	documents = get_sentence_data(filename)
	for website, tos in documents.items():
		if website == 'rovio': # for now
			tos = eliminate(tos)
			tos = code_of_conduct_negate(tos)
			# for sentence in tos:
			# 	print(sentence)

# for now
if __name__ == '__main__':
	# should I be calling parsing url2html code here?
	preprocess('../data/url2html_output.json')


# Example of negation of code of conduct list items using Rovio ToS:
# You agree that you will not, under any circumstances use, either directly or indirectly, any cheats, exploits, automation software, bots, hacks, mods or any unauthorized third-party software designed to modify or interfere with the Services.
# You agree that you will not, under any circumstances use the Services in violation of any applicable law or regulation.
# You agree that you will not, under any circumstances use the Services for commercial purposes, including, but not limited to, to advertising, or solicitation, or transmission of any commercial advertisements such as spam emails, chain letters, pyramid or other get-rich-quick schemes.
# You agree that you will not, under any circumstances use the Services for fraudulent or abusive purposes including, but not limited to, using the Services to impersonate any person or entity, or otherwise misrepresent your affiliation with a person, entity or the Services.
# You agree that you will not, under any circumstances disrupt, overburden, or aid or assist in the disruption or overburdening of any computer or servers used to offer or support the Services.
# You agree that you will not, under any circumstances attempt to gain unauthorized access to the Services, to accounts registered to others or to the computers, servers, or networks connected to the Services by any means other than the user interface provided by Rovio, including, but not limited to, by circumventing or modifying, attempting to circumvent or modify, or encouraging or assisting any other person to circumvent or modify, any security, technology, device, encryption, or software that is part of the Services.
# You agree that you will not, under any circumstances post any information, content or other material (or post links to any information or content) that contains nudity, excessive violence or is abusive, threatening, obscene, defamatory, libelous, or racially, sexually, religiously offensive or otherwise objectionable.
# You agree that you will not, under any circumstances engage in ongoing toxic behavior, such as repeatedly posting information on an unsolicited basis.
# You agree that you will not, under any circumstances attempt to, or harass, abuse, or harm, or advocate or incite harassment, abuse, or harm of another person, group, including Rovio employees, directors, officers, and customer service representatives.
# You agree that you will not, under any circumstances make available through the Services any material or information that infringes any copyright, trademark, patent, trade secret, right of privacy, right of publicity, or other right of any person or entity, or which impersonates any other person, including, but not limited to, a Rovio employee, director or officer.
# You agree that you will not, under any circumstances unless specifically authorized by law, attempt to decompile, reverse engineer, disassemble or hack any of the Services, or to defeat or overcome any of the encryption technologies or security measures or data transmitted, processed or stored by Rovio, or to obtain any information from the Services using any method not expressly permitted by Rovio.
# You agree that you will not, under any circumstances solicit or attempt to solicit login information or any other login credentials or personal information from other users of the Services.
# You agree that you will not, under any circumstances harvest, scrape or collect any information about or regarding other people that use the Services, including, but not limited to, through use of pixel tags, cookies, GIFs or similar items that are sometimes also referred to as spyware.
# You agree that you will not, under any circumstances post anyone's private information, including personally identifiable information/personal data (whether in text, image or video form), identification documents, or financial information through the Services.
# You agree that you will not, under any circumstances engage in any act that Rovio deems to conflict with the spirit or intent of the Services or make improper use of Rovio´s support services.