from types import List

from nltk import translate

class Metric:
  @staticmethod
  def sentence_score(expected: str, actual: str) -> float:
    raise NotImplementedError
  
  @staticmethod
  def corpus_score(expected_corpus: List, actual_corpus: List) -> float:
    raise NotImplementedError

class BLEU(Metric):
  @staticmethod
  def sentence_score(expected: str, actual: str) -> float:
    raise NotImplementedError
  
  @staticmethod
  def corpus_score(expected_corpus: List, actual_corpus: List) -> float:
    raise NotImplementedError

class ROUGE(Metric):
  @staticmethod
  def sentence_score(expected: str, actual: str) -> float:
    raise NotImplementedError
  
  @staticmethod
  def corpus_score(expected_corpus: List, actual_corpus: List) -> float:
    raise NotImplementedError