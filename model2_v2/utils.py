import string
import os
import numpy as np
import json

str_translator = str.maketrans(
    '', '', string.punctuation + '”' + '“' + '’' + '´')


def removePunc(word):
    return word.translate(str_translator)


def checkHasCapital(word):
    for letter in word:
        if letter.isupper():
            return True
    return False


def get_files(directory):
    path = ''

    filenames = []

    for (dirpath, dirnames, filenames) in os.walk(directory):
        path = dirpath
        filenames.extend(filenames)
        break

    files = ['{}/{}'.format(path, filename) for filename in filenames]

    return files