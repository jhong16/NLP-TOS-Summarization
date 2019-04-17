from bs4 import BeautifulSoup
from argparse import ArgumentParser
from os import walk


def main(data_dir, output_dir):
    path = ""
    filenames = []
    for (dirpath, dirnames, filenames) in walk(data_dir):
        path = dirpath
        filenames.extend(filenames)
        break

    for name in filenames:
        with open("{path}/{file}".format(path=path, filename=name), "r") as fp:
            soup = BeautifulSoup(fp, features="html.parser")

        with open("{out_dir}/{file}.txt".format(out_dir=output_dir,
                                                file=name[:-4]), "w") as fp:
            fp.write(soup.text)


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument('--data_dir', '-d',
                           help="""
                                Path to HTML data directory. 
                                All files should have extension `.html`
                                """)
    argparser.add_argument('-output_dir', '-o',
                           help='Path to output directory.')

    args = argparser.parse_args()

    assert args.data_dir is not None
    assert args.output_dir is not None
    main(args.data_dir, args.output_dir)
