import os
import json
from argparse import ArgumentParser

def output_path(output_dir, filename):
    return '{}/{}'.format(output_dir, filename)

def main(input_file, output_dir):
    with open(input_file, 'r') as fp:
        input_data = json.load(fp)
    
    meta = {}
    file_id = 0
    for company in input_data:
        for doc in input_data[company]:
            output_file = "{:06d}.txt".format(file_id)

            meta[output_file] = "{}__{}".format(company, doc)

            with open(output_path(output_dir, output_file), "w") as fp:
                fp.write(input_data[company][doc])

            file_id += 1
    
    # generate key file
    with open("{}/files.json".format(output_dir), "w") as fp:
        json.dump(meta, fp)

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
