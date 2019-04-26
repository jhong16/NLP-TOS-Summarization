import os
from argparse import ArgumentParser
from nltk import sent_tokenize
import super_parser9000 as p9000

def main(input_dir, output_dir):
    filenames = []
    for (dirpath, dirnames, filenames) in os.walk(input_dir):
        filenames.extend(filenames)
        break
    
    
    for file in filenames:
        input_file = "{}/{}".format(input_dir, file)
        output_file = "{}/{}".format(output_dir, file)
        p9000.main(input_file, output_file)

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
