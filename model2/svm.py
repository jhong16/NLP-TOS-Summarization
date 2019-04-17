import string
import sys
import utils
import json
import numpy as np
from sklearn.svm import LinearSVC
from argparse import ArgumentParser
from sklearn.model_selection import cross_val_score

def main(training_file):
    with open(training_file) as json_file:
        training_data = json.load(json_file)
    X = np.asarray(training_data["features"])
    y = np.asarray(training_data["labels"])
    clf = LinearSVC()

    clf.fit(X, y)

    i = 1
    for y2 in y:
        if y2 == 1:
            i = i + 1
    print(y)
    print(clf.score(X, y))

    # Cross-validation error
    scores = cross_val_score(clf, cv = 1)
    print(scores)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--training_file', '-tf',
                        dest='tf',
                        help="Training file (JSON)")

    args = parser.parse_args()

    assert args.tf is not None

    main(args.tf)
