import sys
from parse import parse_tos
from sentence_compress import SentenceCompress
from lexrank import Summarizer

# might become command line tool? or should it be a library?
if __name__ == '__main__':
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		sys.exit("Usage: python main.py <input_tos_file.txt>")

	sentences = parse_tos(filename)

	compressor = SentenceCompress()
	compressor.syntax_parse(sentences[:10])

	summarizer = Summarizer()

	summarizer.create_graph(sentences)
	scores = summarizer.power_method()
	ranking = summarizer.rank_sentences(scores)
	
	# for sentence, rank in ranking:
	# 	print(sentence, rank)
