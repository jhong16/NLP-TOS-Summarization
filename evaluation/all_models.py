import os
import rouge_score_model_2

directory = '/home/tangc/Documents/NLP/Project/NLP-TOS-Summarization/evaluation/'

with open("all_model_ROUGE_1.txt", "w") as dump:
  for filename in os.listdir(directory):
    if filename.endswith(".txt"):
      # Used to automate ROUGE score calculation
      # rouge_score_model_2.main(filename[:-4], filename[:-4])
      f = open(filename)
      lines = f.read()
      dump.write(filename + "-----\n" + lines + "\n\n")