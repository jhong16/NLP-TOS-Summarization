import argparse
import os.path
import sys

from lexrank import Summarizer
from summary_model import load
from parse import parse_tos
from sentence_compress import SentenceCompress


def main():
	parser = argparse.ArgumentParser(description="First Model of Sentence Summarization")
	parser.add_argument("input_tos_file", help="The Raw Terms of Service File")
	args = parser.parse_args()
	filename = args.input_tos_file

	if not os.path.isfile(filename):
		print(f"File not found: {filename}")
		sys.exit(1)
	
	fp = open(filename, 'r')
	model = load(fp)
	fp.close()

	# compressor = SentenceCompress()
	# compressor.syntax_parse(sentences)

	model.rank_sentences()
	# print(model)
	# print(model.word_bank)
	# Print the 10 most common words
	# print(model.common_words(10))
	html_output = model.highlight_phrases()
	# print(html_output)

	# f_name = args.input_tos_file.replace(".txt", ".html")
	f_name = "output.html"
	# print(f_name)
	fd = open(f_name, "w")
	fd.write(html_output)


# might become command line tool? or should it be a library?
if __name__ == '__main__':
	sys.exit(main())