import argparse
import json
import os
import string
import sys
import datetime

import numpy as np
from sklearn.linear_model import Perceptron
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
import pickle

import utils


def normalize2(data_points, max_min):
    num_of_features = len(data_points[0])
    max_features = max_min[0]
    min_features = max_min[1]
    for features in data_points:
        for i in range(num_of_features):
            features[i] = (features[i] - min_features[i]) / \
                (max_features[i] - min_features[i])


def normalize(data_points):
    num_of_features = len(data_points[0])
    min_features = np.array([float("inf")]*num_of_features)
    max_features = np.array([float("-inf")]*num_of_features)

    for features in data_points:
        for i in range(num_of_features):
            if features[i] < min_features[i]:
                min_features[i] = features[i]
            if features[i] > max_features[i]:
                max_features[i] = features[i]

    for features in data_points:
        for i in range(num_of_features):
            features[i] = (features[i] - min_features[i]) / \
                (max_features[i] - min_features[i])

    return (max_features, min_features)


def load_data(train_dir):
    path = ''
    filenames = []

    for (dirpath, dirnames, filenames) in os.walk(train_dir):
        path = dirpath
        filenames.extend(filenames)
        break

    training_files = []
    for filename in filenames:
        training_files.append('{}/{}'.format(path, filename))

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


def train(train_dir, classifier_type, model_output):
    X, y = load_data(train)
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

    return (X, y, model_output)


def main(X, y, model_output):
    max_min = normalize(X)
    clf = pickle.load(model_output)
    print(clf.score(X, y))

    # k-FOLD cross validation error
    k_scores = cross_val_score(clf, X, y, cv=3)
    print("3-fold CV:\nAccuracy: %0.2f (+/- %0.2f)" %
          (k_scores.mean(), k_scores.std() * 2))

    with open(to_summarize, "r") as tsf:
        tf_json_stuff = json.load(tsf)
    tf_sentences = np.asarray(tf_json_stuff["sentences"])
    tf_X = np.asarray(tf_json_stuff["features"])

    normalize2(tf_X, max_min)

    tf_y_guesses = clf.predict(tf_X)
    print(tf_y_guesses)

    with open(output_file, "w+") as off:
        index = 0
        for guess in tf_y_guesses:
            if guess == 1:
                off.write(tf_sentences[index] + "\n")
            index = index + 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir',
                        help='Training files (JSON) directory')
    parser.add_argument('--test_dir',
                        help="Testing files (to summarize)")
    parser.add_argument('--output_dir', '-o',
                        help="The output directory (where to put the summaries)")
    parser.add_argument('--classifier_type', '-c',
                        dest='classifier_type',
                        choices=['knn, svm, perceptron'], default='knn',
                        help="Which classifier to use.")
    parser.add_argument('--model_output', dest='model',
                        default=None, help='where to output the model file')
    parser.add_argument('--log', help='Log file name')
    args = parser.parse_args()

    assert args.train_dir is not None
    assert args.test_dir is not None
    assert args.output_dir is not None

    X, y, model_file = train(
        args.train_dir, args.classifier_type, args.model_output)

    main(X, y, clf)
