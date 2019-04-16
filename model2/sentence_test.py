from nltk import sent_tokenize
import sys

def parse(text_file):
  with open("../data/" +  text_file, "r") as tos:
    with open("./sentence_test_results.txt", "w") as preprocessed_tos:
      for line in tos:
        if (line == "\n"):
          # Put into paragraph hash set
          continue
        sentences = sent_tokenize(line)
        for i in range(len(sentences)):
          preprocessed_tos.write(sentences[i] + "\n")


if __name__ == "__main__":
  parse(sys.argv[1])