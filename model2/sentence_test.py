from nltk import sent_tokenize

with open("./NLP-TOS-Summarization/data/twitter_tos.txt", "r") as tos:
  with open("./sentence_test_results.txt", "w") as preprocessed_tos:
    for line in tos:
      if (line == "\n"):
        # Put into paragraph hash set
        continue
      sentences = sent_tokenize(line)
      for i in range(len(sentences)):
        preprocessed_tos.write(sentences[i] + "\n")