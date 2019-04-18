import argparse
import os.path
import sys

from highlighter import highlight_phrases
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

	# model.compress_sentences()
	
	model.rank_sentences()
	# print(model)
	# Print the 10 most common words
	# print(model.common_words(10))

	percent = .02
	short_summary = model.shorten(percent)
	# print(f"{percent*100}% of the Summary")
	# for sentence in short_summary:
	# 	print(sentence.sentence)

	# html_output = highlight_phrases(short_summary)
	html_output = highlight_phrases(model.sentences)

	# f_name = args.input_tos_file.replace(".txt", ".html")
	f_name = "output.html"
	fd = open(f_name, "w")
	fd.write(html_output)


# might become command line tool? or should it be a library?
if __name__ == '__main__':
	sys.exit(main())