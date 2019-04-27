import argparse
import datetime
import json
import os
import pickle
import string
import sys

import numpy as np
from sklearn.linear_model import Perceptron
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC

import utils


def load_data(data_directory):
    training_files = utils.get_files(data_directory)

    X = None
    y = None
    for training_file in training_files:
        with open(training_file, 'r') as fp:
            data = json.load(fp)
        X2 = np.asarray(data["features"])
        y2 = np.asarray(data["labels"])

        if X is None:
            X = X2
        else:
            X = np.append(X, X2, axis=0)

        if y is None:
            y = y2
        else:
            y = np.append(y, y2, axis=0)

    return X, y


def train(train_dir, classifier_type, model_output):
    X, y = load_data(train_dir, "features", "labels")
    classifier = None
    if classifier_type == 'perceptron':
        classifier = Perceptron(tol=-100000,
                                random_state=0,
                                max_iter=50000,
                                penalty='l2')
    if classifier_type == 'svm':
        classifier = LinearSVC()

    if classifier_type == 'knn':
        classifier = KNeighborsClassifier(n_neighbors=1)

    classifier.fit(X, y)

    if model_output is None:
        model_output = './{}_{}.model'.format(
            classifier_type, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

    with open(model_output, "w") as fp:
        pickle.dump(classifier, fp)

    print(classifier.score(X, y))

    # k-FOLD cross validation error
    k_scores = cross_val_score(classifier, X, y, cv=3)
    print("3-fold CV:\nAccuracy: %0.2f (+/- %0.2f)" %
          (k_scores.mean(), k_scores.std() * 2))

    return (X, y, model_output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir',
                        help='Training files (JSON) directory')
    parser.add_argument('--classifier_type', '-c',
                        dest='classifier_type',
                        choices=['knn, svm, perceptron'], default='knn',
                        help="Which classifier to use.")
    parser.add_argument('--model_output', dest='model',
                        default=None, help='where to output the model file')
    parser.add_argument('--log', help='Log file name')
    args = parser.parse_args()

    assert args.train_dir is not None

    X, y, model_file = train(args.train_dir,
                             args.classifier_type,
                             args.model_output)

    print("Model stored in {}".format(model_file))
