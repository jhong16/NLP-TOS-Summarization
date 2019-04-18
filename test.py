from nltk import sent_tokenize
import argparse
import sys

from evaluation.metrics import BLEU_sentence_score, ROUGE_sentence_score

def test(ground_truth_file, model_output_file):
	with open(ground_truth_file, 'r') as f:
		ground_truth_sentences = f.read()

	with open(model_output_file, 'r') as f:
		model_output_sentences = f.read()

	bleu_score = BLEU_sentence_score(ground_truth_sentences, model_output_sentences)
	rouge_score = ROUGE_sentence_score(ground_truth_file, model_output_sentences)
	return bleu_score, rouge_score

def main():
	parser = argparse.ArgumentParser(description="Test summaries against ground truth.")
	parser.add_argument("ground_truth_file", help="Filename of ground truth")
	parser.add_argument("model_summary_file", help="Filename of generated summary that is being tested.")
	args = parser.parse_args()

	ground_truth_file = args.ground_truth_file
	model_summary_file = args.model_summary_file

	bleu_score, rouge_score = test(ground_truth_file, model_summary_file)
	print(bleu_score)

if __name__ == '__main__':
	sys.exit(main())
