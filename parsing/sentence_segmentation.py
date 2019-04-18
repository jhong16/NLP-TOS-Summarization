from os import walk
import spacy
from argparse import ArgumentParser

nlp = spacy.load("en_core_web_sm")

def make_path(path, name):
    return "{}/{}".format(path, name)

def main(input_dir, output_dir):
    nlp = spacy.load("en_core_web_sm")
    path = ""
    filenames = []
    for (dirpath, dirnames, filenames) in walk(input_dir):
        path = dirpath
        filenames.extend(filenames)
        break
    
    for name in filenames:
        with open(make_path(input_dir, name), "r") as fp:
            doc = nlp(fp.read())
        open(make_path(output_dir, name), "w").close()
        with open(make_path(output_dir, name), "a") as fp:
            for sent in doc.sents:
                fp.write(sent.text)
                fp.write("\n")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input_dir', '-i',
                        help="Directory of input files")
    parser.add_argument('--output_dir', '-o',
                        help="Directory for output files")
    
    args = parser.parse_args()

    assert args.input_dir is not None
    assert args.output_dir is not None

    main(args.input_dir, args.output_dir)