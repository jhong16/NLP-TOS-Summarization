import argparse
import os.path
import sys

from lexrank import Summarizer
from model import loadl, load
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

	sentences = parse_tos(filename)
	# model = loadl(sentences)
	model = load(fp)
	fp.close()

	# compressor = SentenceCompress()
	# compressor.syntax_parse(sentences)

	summarizer = Summarizer()

	summarizer.create_graph(sentences)
	scores = summarizer.power_method()
	ranking = summarizer.rank_sentences(scores)
	
	for sentence, rank in ranking:
		print(sentence, rank)

# might become command line tool? or should it be a library?
if __name__ == '__main__':
	sys.exit(main())