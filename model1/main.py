import argparse
import os.path
import sys

from highlight import highlight_phrases
from lexrank import Summarizer
from summary_model import load
from parse import parse_tos
from sentence_compress import SentenceCompress

from nltk.translate.bleu_score import corpus_bleu, sentence_bleu


def pattern(seq):
        storage = {}
        for length in range(1,int(len(seq)/2+1)):
                valid_strings = {}
                for start in range(0,int(len(seq)-length+1)):
                        valid_strings[start] = tuple(seq[start:start+length])
                candidates = set(valid_strings.values())
                if len(candidates) != len(valid_strings.values()):
                        print("Pattern found for " + str(length))
                        storage = valid_strings
                else:
                        print("No pattern found for " + str(length))
                        return set(filter(lambda x: storage.values().count(x) > 1, storage.values()))
        return storage

def main():
	parser = argparse.ArgumentParser(description="First Model of Sentence Summarization")
	parser.add_argument("input_tos_file", help="The Raw Terms of Service File")
	# parser.add_argument("--summarize", required=True, type=float, help="Percentage to reduce original text size to")
	args = parser.parse_args()
	filename = args.input_tos_file

	if not os.path.isfile(filename):
		print(f"File not found: {filename}")
		sys.exit(1)
	
	fp = open(filename, 'r')
	model = load(fp)
	fp.close()

	# BTW this is slow.
	model.compress_sentences(beta=args.compression_level)
	
	model.rank_sentences()
	model.rake_sentences()
	for sentence in model.sentences:
		print(sentence.keywords)
	# print(model)
	# Print the 10 most common words
	# print(model.common_words(10))

	# percent = args.summarize
	# short_summary = model.shorten(percent)
	# print(f"{percent*100}% of the Summary")
	# for sentence in short_summary:
	# 	print(sentence.sentence)
	# 	print()

	# top_sent = model.top_sent(7)
	# bleu_format_sys = list()
	# for sentence in top_sent:
	# 	# print(sentence)
	# 	bleu_format_sys.extend(sentence.word_list())
	# print(len(bleu_format_sys))

	compliance_summary = model.keyword_summary("must")
	# common_words = set()
	# for sentence in compliance_summary:
	# 	# print(f"{set(sentence.word_list())}\n")
	# 	if len(common_words) == 0:
	# 		common_words = set(sentence.word_list())
	# 	else:
	# 		common_words = common_words.intersection(set(sentence.word_list()))
	# print(common_words)

	# common_duals = list()
	# for i in range(0,len(compliance_summary)-1):
	# 	lower_words1 = [word.lower() for word in compliance_summary[i].word_list()]
	# 	lower_words2 = [word.lower() for word in compliance_summary[i+1].word_list()]
	# 	common_words = set(lower_words1)
	# 	common_words = common_words.intersection(set(lower_words2))
	# 	common_duals.extend(list(common_words))
	# print(common_duals)

	# from collections import Counter
	# print(Counter(common_duals))

	# common_keywords = list()
	# for sentence in compliance_summary:
	# 	keywords = rake(sentence.sentence)
	# 	print([word[0] for word in keywords])

	# compliance_summary = model.keyword_summary("right")
	# for sentence in compliance_summary:
	# 	print(sentence.sentence + '\n')
	
	# word_splat = list()
	# for i in range(0,len(model.sentences)):
	# 	lower_words1 = [word.lower() for word in model.sentences[i].word_list()]
	# 	word_splat.extend(lower_words1)

	# from collections import Counter
	# print(Counter(word_splat))

	# sequence = list()
	# for sentence in compliance_summary:
	# 	# print([word.token for word in sentence.words])
	# 	sequence.extend([word.token for word in sentence.words])

	# pattern(sequence)

	# print(f"{percent*100}% of the Summary")
	# for sentence in top_sent:
		# print(sentence)
		# print()

	# smmry_file = "twitter_smmry.txt"
	# with open(smmry_file, "r") as fd:
	# 	baseline_model = load(fd)
	
	# bleu_format_key = list()
	# for sentence in baseline_model.sentences:
	# 	bleu_format_key.append(sentence.word_list())
	# print(len(bleu_format_key))

	# score = sentence_bleu(bleu_format_key, bleu_format_sys, weights=(0, 0, 0, 1))
	# print(score)
	# percent = .02
	percent = args.percent
	short_summary = model.shorten(percent)
	print(f"{percent*100}% of the Summary")
	for sentence in short_summary:
		print(sentence.sentence)
	with open('output.txt', 'w') as f:
		f.write('\n'.join([s.sentence for s in short_summary]))

	# html_output = highlight_phrases(short_summary)
	html_output = highlight_phrases(model.sentences)

	# f_name = args.input_tos_file.replace(".txt", ".html")
	f_name = "output.html"
	fd = open(f_name, "w")
	fd.write(html_output)


# might become command line tool? or should it be a library?
if __name__ == '__main__':
	sys.exit(main())