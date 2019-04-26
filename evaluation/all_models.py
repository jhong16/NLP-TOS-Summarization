import os
import rouge_score_model_2

in_directory = '/home/tangc/Documents/NLP/Project/NLP-TOS-Summarization/data/smmry_tosdr_corpus/smmry_input/'
out_directory = '/home/tangc/Documents/NLP/Project/NLP-TOS-Summarization/data/smmry_tosdr_corpus/smmry_output/'

for filename in os.listdir(in_directory):
  if filename.endswith(".txt"):
    rouge_score_model_2.main(filename[:-4], filename[:-4])