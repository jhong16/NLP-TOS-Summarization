import argparse
import os.path
import sys

from highlight import highlight_phrases
from lexrank import Summarizer
from summary_model import load
from parse import parse_tos
# from sentence_compress import SentenceCompress

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
	parser.add_argument("--percent", type=float, default=0.2, help="Desired length as percentage of original ToS")
	# I should make this a nicer number to use, like percentage or number of words
	parser.add_argument("--compression_level", type=int, default=500, help="Approximate desired maximum length of sentences in characters.")
	parser.add_argument("--path_to_jar", type=str, default=None, help="The parser jar file")
	parser.add_argument("--path_to_models_jar", type=str, default=None, help="The parser model jar file")
	args = parser.parse_args()
	filename = args.input_tos_file

	if not os.path.isfile(filename):
		print(f"File not found: {filename}")
		sys.exit(1)
	
	fp = open(filename, 'r')
	model = load(fp)
	fp.close()

	# BTW this is slow.
	model.compress_sentences(beta=args.compression_level, path_to_jar=args.path_to_jar, path_to_models_jar=args.path_to_models_jar)
	
	model.rank_sentences()
	model.rake_sentences()
	# Print the 10 most common words
	# print(model.common_words(10))

	compliance_summary = model.keyword_summary("must")

	percent = args.percent
	short_summary = model.shorten(percent)
	print(f"{percent*100}% of the Summary")
	for sentence in short_summary:
		print(sentence.sentence)
	with open('output.txt', 'w') as f:
		f.write('\n'.join([s.sentence for s in short_summary]))

	html_output = highlight_phrases(short_summary)
	# html_output = highlight_phrases(model.sentences)

	# f_name = args.input_tos_file.replace(".txt", ".html")
	f_name = "output.html"
	fd = open(f_name, "w")
	fd.write(html_output)


# might become command line tool? or should it be a library?
if __name__ == '__main__':
	sys.exit(main())