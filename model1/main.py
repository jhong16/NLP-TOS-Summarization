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
	parser.add_argument("--percent", type=float, default=0.2, help="Desired length as percentage of original ToS")
	# I should make this a nicer number to use, like percentage or number of words
	parser.add_argument("--compression_level", type=int, default=500, help="Approximate desired maximum length of sentences in characters.")
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
	# print(model)
	# Print the 10 most common words
	# print(model.common_words(10))

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