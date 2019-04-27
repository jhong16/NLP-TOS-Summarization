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

import train
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


def test(train_dir, test_dir, output_dir, model_file):

    Xtrain, ytrain = train.load_data(train_dir)
    with open(model_file, "rb") as fp:
        clf = pickle.load(fp)

    test_files = utils.get_files(test_dir)

    max_min = normalize(Xtrain)

    for test_file in test_files:
        with open(test_file, "r") as fp:
            test_json = json.load(fp)
        test_sentences = np.asarray(test_json["sentences"])
        Xtest = np.asarray(test_json["features"])

        normalize2(Xtest, max_min)

        y_pred = clf.predict(Xtest)
        print(y_pred)

        output_file = "{}/{}.txt".format(output_dir,
                                         test_file.split('/')[:-1][:-5])

        with open(output_file, "w+") as off:
            index = 0
            for pred in y_pred:
                if pred == 1:
                    off.write(test_sentences[index] + "\n")
                index = index + 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir',
                        help='Training files (JSON) directory')
    parser.add_argument('--test_dir',
                        help="Testing files (to summarize)")
    parser.add_argument('--output_dir', '-o',
                        help="The output directory (where to put the summaries)")
    parser.add_argument('--model_file',
                        help='location of the model file')

    args = parser.parse_args()

    assert args.train_dir is not None
    assert args.test_dir is not None
    assert args.output_dir is not None
    assert args.model_file is not None

    test(args.train_dir, args.test_dir, args.output_dir, args.model_file)
