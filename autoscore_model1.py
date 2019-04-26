import os
from PyRouge.PyRouge.pyrouge import Rouge
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
    smmry_out_directory = "data/smmry_tosdr_corpus/smmry_output"
    model_out_directory = "data/smmry_tosdr_corpus/model1_output"
    score_directory = "data/smmry_tosdr_corpus/model1_scores"
    if os.path.isdir(smmry_out_directory):
        print("wooo")
    if os.path.isdir(model_out_directory):
        print("weee")
    if os.path.isdir(score_directory):
        print("waaa")

    model_files = os.listdir(model_out_directory)
    # print(type(input_files))
    print(model_files)
    
    output_file = "scores.txt"

    final_output = os.path.join(score_directory, output_file)

    output = ""

    for model_file in model_files:
        model_summary = os.path.join(model_out_directory, model_file)
        smmry_summary = os.path.join(smmry_out_directory, model_file)
        # print(model_summary)
        # print(smmry_summary)
        ground_truth_file = smmry_summary
        model_summary_file = model_summary

        with open(ground_truth_file, "r") as fd:
            ground_truth_string = fd.read()

        with open(model_summary_file, "r") as fd:
            model_summary_string = fd.read()
        
        r = Rouge()

        output += f"{str(model_file)}\n"
        try:
            [precision, recall, f_score] = r.rouge_l([ground_truth_string], [model_summary_string])
            output += f"Rouge Precision is: {str(precision)}\n"
            output += f"Rouge Recall is: {str(recall)}\n"
            output += f"Rouge F Score is: {str(f_score)}\n"
        except ZeroDivisionError:
            output += f"Whoops, rouge division by zero.\n"

        bleu_score, rouge_score = test(ground_truth_file, model_summary_file)
        output += f"Bleu: {bleu_score}\n\n"
        print(output)


    fd = open(final_output, "w")
    fd.write(output)
    fd.close()

if __name__ == "__main__":
    main()