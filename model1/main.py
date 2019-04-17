import argparse
import os.path
import sys

from summary_model import load


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

	# UNCOMMENT for sentence compression. Btw it's very slow.
	# model.compress_sentences()

	model.rank_sentences()
	print(model)

if __name__ == '__main__':
	sys.exit(main())
