import os
from argparse import ArgumentParser
import feature_creation as fc

def main(input_dir, truth_dir, output_dir):
    filenames = []
    for (dirpath, dirnames, filenames) in os.walk(input_dir):
        filenames.extend(filenames)
        break

    for file in filenames:
        input_file = "{}/{}".format(input_dir, file)
        truth_file = "{}/{}".format(truth_dir, file)
        output_file = "{}/{}".format(output_dir, file)
        fc.main(input_file, truth_file, output_file)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input_dir', '-i',
                        help="Input directory")
    parser.add_argument('--ground_truth_dir', '-g',
                        dest='truth_dir',
                        help="Ground truth directory")
    parser.add_argument('--output_dir', '-o',
                        help="Output directory")
    args = parser.parse_args()

    assert args.input_dir is not None
    assert args.truth_dir is not None
    assert args.output_dir is not None

    main(args.input_dir, args.truth_dir, args.output_dir)
