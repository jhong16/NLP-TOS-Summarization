from argparse import ArgumentParser

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
