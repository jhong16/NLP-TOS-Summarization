import os
from argparse import ArgumentParser
import requests

METHOD = 'POST'
URL = 'http://api.smmry.com/'
PARAMS = {}
DATA = ''


def main(key, input_dir, output_dir):

    path = ""
    filenames = []
    for (dirpath, dirnames, filenames) in os.walk(input_dir):
        path = dirpath
        filenames.extend(filenames)
        break

    for name in filenames:
        with open("{}/{}".format(path, name), "r") as fp:
            text = fp.read()

        data = {'sm_api_input': text}
        res = req.request(method=METHOD,
                          url=URL,
                          data=data)
        print(res)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--smmry_api_key', '-k',
                        dest='key',
                        help='Your SMMRY API key. For more info, visit https://smmry.com/api')
    parser.add_argument('--input_dir', '-i',
                        help='Path to directory of text files for summarization.')
    parser.add_argument('-output_dir', '-o',
                        help='Path to output directory.')

    args = parser.parse_args()

    assert args.key is not None
    assert args.input_dir is not None
    assert args.output_dir is not None

    main(args.key, args.input_dir, args.output_dir)
