from argparse import ArgumentParser
from os import walk

def main(input_dir):
    path = ""
    filenames = []
    for (dirpath, dirnames, filenames) in walk(input_dir):
        path = dirpath
        filenames.extend(filenames)
        break

    for name in filenames:
        with open("{path}/{file}".format(path=path, file=name), "w") as fp:
            fp.write("")



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input_dir', '-i',
                        help="Input directory (where the text files are stored).")
    args = parser.parse_args()

    assert args.input_dir is not None

    main(args.input_dir)