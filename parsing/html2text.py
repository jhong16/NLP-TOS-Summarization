from bs4 import BeautifulSoup
from argparse import ArgumentParser
from os import walk

argparser = ArgumentParser()
argparser.add_argument('-d', '--data_dir', help='Path to HTML data directory. All files should have extension `.html`')
argparser.add_argument('-o', '--output_dir', help='Path to output directory.')

args = argparser.parse_args()

assert args.data_dir is not None
assert args.output_dir is not None

path = ""
filenames = []
for (dirpath, dirnames, filenames) in walk(args.data_dir):
    path = dirpath
    filenames.extend(filenames)
    break

for name in filenames:
    with open("{path}/{filename}".format(path=path, filename=name), "r") as fp:
        soup = BeautifulSoup(fp, features="html.parser")

    with open("{output}/{filename}.txt".format(output=args.output_dir, filename=name[:-4]), "w") as fp:
        fp.write(soup.text)
