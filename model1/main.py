import sys
from parse import parse_tos
from lexrank import Summarizer

# might become command line tool? or should it be a library?
if __name__ == '__main__':
	filename = sys.argv[1]

	sentences = parse_tos(filename)

	summarizer = Summarizer()

	summarizer.create_graph(sentences)