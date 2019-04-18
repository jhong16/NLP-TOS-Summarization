from argparse import ArgumentParser

def main(input_file, output_dir):
    pass    


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input_file', '-i',
                        help="JSON file for input.")
    parser.add_argument('--output_dir', '-o',
                        help="""
                             Output directory (where the text files will be store).
                             """)

    args = parser.parse_args()

    assert args.input_file is not None
    assert args.output_dir is not None

    main(args.input_file, args.output_dir)
