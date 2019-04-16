import json
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--input_file', '-i',
    help="JSON file for input. Uses format from: https://github.com/tosdr/tosdr.org/wiki/api-1-all.json")
parser.add_argument('--output', '-o',
    help="Output file name. Will be a JSON file.")

args = parser.parse_args()
assert args.input_file is not None
assert args.output is not None

with open(args.input_file, "r") as f:
    data = json.load(f)

my_data = {}
for k in data:
    if type(data[k]) is dict:
        if 'documents' in data[k].keys():
            if len(data[k]["documents"]) != 0:
                docs = data[k]["documents"]
                my_data[k] = {doc["name"]: doc["url"] for doc in docs}

with open(args.output, "w") as f:
    json.dump(my_data, f)

