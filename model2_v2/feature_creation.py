import json
import math
import os
import sys
from argparse import ArgumentParser

import numpy as np

import utils


"""
input_file is the preprocessed txt file we made using super_parser9000.py
input_file2 is the ground truth
output_file is a json we will write out features and labels too

The features:
0: number of words ignoring the stopwords
1: number of commas in the sentence
2: Order of sentence from top of document (normalized by the total number of sentences there are in the entire ToS)
3: Order of sentence from beginning of each paragraph (normalized by total number of sentences within each paragraph)
4: Number of words with capitals
5: Number of words with full capitals
6: Relative paragraph order from top of document (Normalized)
7: sentence tf-idf
"""


def feature_creation(input_file, input_file2, output_file):

    # set of stopwords
    stopwords = set()
    with open("stopwords.txt", "r") as stop_f:
        for line in stop_f:
            stopwords.add(utils.removePunc(line).lower().strip())

    # the 2d feature matrix to print
    write_data = list()

    # the sentences in a list
    sentences = list()

    # the sentences considered in the summary
    sentences_set = set()

    # the ground truth in a list
    labels = list()

    # used for labeling the training data
    LINE_INDEX_IN_SUMMARY = set()

    # index is current paragraph
    # a tuple of (current_num_words_in_para, current_num_lines_in_para)
    paragraph_info = list()

    # number of times a word appear overall
    word_appear = dict()

    # number of times a word appears in a sentence
    word_appear_in_sentence = dict()
    tf = dict()
    idf = dict()

    total_lines = 0
    total_words = 0
    total_paragraphs = 1
    current_paragraph = 0
    current_num_words_in_para = 0
    current_num_lines_in_para = 0

    with open(input_file, "r") as input_f:
        for line in input_f:
            if line == "" or line == "\n":
                continue
            if line.strip() == "<PARAGRAPH>":
                paragraph_info.append(
                    (current_num_words_in_para, current_num_lines_in_para))

                current_num_words_in_para = 0
                current_num_lines_in_para = 0
                current_paragraph = current_paragraph + 1
                total_paragraphs = total_paragraphs + 1
                continue
            words = line.strip().split()
            sentences.append(line.strip())
            words_in_sentence = set()

            for word in words:
                new_word = utils.removePunc(word).lower()
                if new_word not in stopwords:
                    current_num_words_in_para = current_num_words_in_para + 1
                    total_words = total_words + 1
                    words_in_sentence.add(new_word)
                    if new_word not in word_appear:
                        word_appear[new_word] = 1
                    else:
                        word_appear[new_word] = word_appear[new_word] + 1

            for word in words_in_sentence:
                if word not in word_appear_in_sentence:
                    word_appear_in_sentence[word] = 1
                else:
                    word_appear_in_sentence[word] = word_appear_in_sentence[word] + 1

            current_num_lines_in_para = current_num_lines_in_para + 1
            total_lines = total_lines + 1

        paragraph_info.append(
            (current_num_words_in_para, current_num_lines_in_para))
        current_paragraph = current_paragraph + 1
        total_paragraphs = total_paragraphs + 1

        for word in word_appear:
            tf[word] = word_appear[word] / total_words

        for word in word_appear_in_sentence:
            idf[word] = math.log10(total_lines / word_appear_in_sentence[word])

        current_paragraph = 0
        current_num_words_in_para = 0
        current_num_lines_in_para = 0
        current_line = 0
        input_f.seek(0)

        for line in input_f:
            if line.strip() == "<PARAGRAPH>":
                current_num_words_in_para = 0
                current_num_lines_in_para = 0
                current_paragraph = current_paragraph + 1
                continue
            elif line == "" or line == "\n":
                continue
            else:
                features = [None] * 8
                words = line.strip().split()
                num_words = 0
                num_commas = 0
                num_one_cap = 0
                num_full_cap = 0
                current_tf = 0
                current_idf = 0

                for word in words:
                    word2 = word.strip()
                    if ',' in word2:
                        num_commas = num_commas + 1
                    if utils.checkHasCapital(word2):
                        num_one_cap = num_one_cap + 1
                    if utils.removePunc(word2).isupper():
                        num_full_cap = num_full_cap + 1

                    word2 = utils.removePunc(word2).lower()
                    if word2 not in stopwords:
                        current_num_words_in_para = current_num_words_in_para + 1
                        num_words = num_words + 1
                        current_tf = current_tf + tf[word2]
                        current_idf = current_idf + idf[word2]

                    if num_words == 0:
                        current_tf = 0
                        current_idf = 0
                    else:
                        current_tf = current_tf / num_words
                        current_idf = current_idf / num_words

                    tf_idf = current_tf * current_idf

                features[0] = num_words
                features[1] = num_commas
                features[2] = current_line / total_lines
                features[3] = current_num_lines_in_para / \
                    paragraph_info[current_paragraph][1]
                features[4] = num_one_cap
                features[5] = num_full_cap
                features[6] = current_paragraph / total_paragraphs
                features[7] = tf_idf

                write_data.append(features)

                current_line = current_line + 1
                current_num_lines_in_para = current_num_lines_in_para + 1

    with open(input_file2, "r") as temp_f:
        for line in temp_f:
            line = line.rstrip()
            sentences_set.add(line)

    index = 1
    for line in sentences:
        if line in sentences_set:
            LINE_INDEX_IN_SUMMARY.add(index)
        index = index + 1

    index = 1
    while index <= total_lines:
        if index in LINE_INDEX_IN_SUMMARY:
            labels.append(1)
        else:
            labels.append(-1)
        index = index + 1

    json_dump_data = dict()
    json_dump_data["sentences"] = sentences
    json_dump_data["features"] = write_data
    json_dump_data["labels"] = labels

    with open(output_file, "w+") as out_file:
        json.dump(json_dump_data, out_file)


def main(input_dir, truth_dir, output_dir):
    filenames = []
    for (dirpath, dirnames, filenames) in os.walk(input_dir):
        filenames.extend(filenames)
        break

    for file in filenames:
        input_file = "{}/{}".format(input_dir, file)
        truth_file = "{}/{}".format(truth_dir, file)
        output_file = "{}/{}".format(output_dir, file)
        feature_creation(input_file, truth_file, output_file)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input_dir', '-i',
                        help="Input directory")
    parser.add_argument('--ground_truth_dir', '-g',
                        dest='truth_dir',
                        help="Ground truth directory")
    parser.add_argument('--output_dir', '-o',
                        help="Output directory")
    args = parser.parse_args()

    assert args.input_dir is not None
    assert args.truth_dir is not None
    assert args.output_dir is not None

    main(args.input_dir, args.truth_dir, args.output_dir)
