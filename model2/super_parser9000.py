import sys
from nltk import sent_tokenize

"""
input_file is the tos txt file
output_file is the file we will write to
"""

def main(input_file, output_file):
    temp_f = open("temp.txt", "w+")
    with open(input_file, "r") as tos:    
        with open(output_file, "w+") as preprocessed_tos:
            paragrah_towrite = False
            for line in tos:
                if paragrah_towrite:
                    preprocessed_tos.write("<PARAGRAPH>" + "\n")
                    paragrah_towrite = False

                if (line == "\n" or line == ""):
                    paragrah_towrite = True
                    continue
                sentences = sent_tokenize(line)
                for i in range(len(sentences)):
                    preprocessed_tos.write(sentences[i] + "\n")
                    temp_f.write(sentences[i] + "\n")

    temp_f.close()

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)