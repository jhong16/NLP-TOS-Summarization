import os
from argparse import ArgumentParser
from nltk import sent_tokenize

from nltk import sent_tokenize


def parse(input_file, output_file):
    """
    :param input_file - tos text file
    :param output_file - file to write to
    """
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

def main(input_dir, output_dir):
    filenames = []
    for (dirpath, dirnames, filenames) in os.walk(input_dir):
        filenames.extend(filenames)
        break
    
    
    for file in filenames:
        input_file = "{}/{}".format(input_dir, file)
        output_file = "{}/{}".format(output_dir, file)
        parse(input_file, output_file)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input_dir', '-i',
                        help="Input directory")
    parser.add_argument('--output_dir', '-o',
                        help="Output directory")
    args = parser.parse_args()

    assert args.input_dir is not None
    assert args.output_dir is not None

    main(args.input_dir, args.output_dir)
