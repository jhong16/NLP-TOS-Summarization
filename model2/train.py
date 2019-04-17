import string
import sys
import utils
import json
import numpy as np
from sklearn.linear_model import Perceptron

def main(training_file):
	with open(training_file) as json_file:
		json_stuff = json.load(json_file)
	X = np.asarray(json_stuff["features"])
	y = np.asarray(json_stuff["labels"])
	clf = Perceptron(tol=1e-3, random_state = 0)

	clf.fit(X,y)

	i = 1
	for y2 in y:
		if y2 == 1:
			print(i)
			i = i + 1
	print(y)
	print(clf.score(X,y))

if __name__ == "__main__":
	training_file = sys.argv[1]
	main(training_file)