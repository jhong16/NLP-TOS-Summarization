from types import List

from nltk.translate import bleu_score

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
    ref = [expected.split()]
    hyp = actual.split()
    return bleu_score.sentence_bleu(ref, hyp)
  
  @staticmethod
  def corpus_score(expected_corpus: List[str], actual_corpus: List[str]) -> float:
    refs = [[e.split()] for e in expected_corpus]
    hyps = [a.split() for a in actual_corpus]
    return bleu_score.corpus_bleu(refs, hyps)

class ROUGE(Metric):
  @staticmethod
  def sentence_score(expected: str, actual: str) -> float:
    raise NotImplementedError
  
  @staticmethod
  def corpus_score(expected_corpus: List, actual_corpus: List) -> float:
    raise NotImplementedError