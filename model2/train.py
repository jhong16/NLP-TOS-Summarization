import string
import sys
import utils
import json
import numpy as np
import argparse
from sklearn.linear_model import Perceptron
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score

def normalize2(data_points, max_min):
    num_of_features = len(data_points[0])
    max_features = max_min[0]
    min_features = max_min[1]
    for features in data_points:
        for i in range(num_of_features):
            features[i] = (features[i] - min_features[i]) / (max_features[i] - min_features[i])

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
            features[i] = (features[i] - min_features[i]) / (max_features[i] - min_features[i])

    return (max_features, min_features)  

def main(training_files, to_summarize, output_file):

    X = None
    y = None
    for training_file in training_files:
        json_stuff = json.load(training_file)
        X2 = np.asarray(json_stuff["features"])
        y2 = np.asarray(json_stuff["labels"])
        if X is None:
            X = X2
        else:
            X = np.append(X, X2, axis=0)

        if y is None:
            y = y2
        else:
            y = np.append(y, y2, axis=0)

    # clf = Perceptron(tol=-100000, random_state = 0, max_iter = 50000, penalty='l2')
    # clf = LinearSVC()
    clf = KNeighborsClassifier(n_neighbors=1)

    max_min = normalize(X)

    clf.fit(X,y)
    print(clf.score(X,y))

    # k-FOLD cross validation error
    k_scores = cross_val_score(clf, X, y, cv = 3)
    print("3-fold CV:\nAccuracy: %0.2f (+/0 %0.2f)" % (k_scores.mean(), k_scores.std() * 2))

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
    parser.add_argument('--training_files', '-tf',
                        dest='tf',
                        help="Training files (JSON)",
                        type=argparse.FileType("r"),
                        nargs="+")

    parser.add_argument('--to_summarize', '-ts', dest='ts', help="The file to summarize")
    parser.add_argument('--output_file', '-of', dest='of', help="The output file, the summary")
    args = parser.parse_args()

    main(args.tf, args.ts, args.of)