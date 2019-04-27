# from types import List

from nltk.translate import bleu_score
from PyRouge.PyRouge.pyrouge import Rouge

# def BLEU_sentence_score(expected: str, actual: str) -> float:
def BLEU_sentence_score(expected, actual):
  """
  Score an output sentence compared to the expected sentence.
  Uses the BLEU metric.
  """
  ref = [expected.split()]
  hyp = actual.split()
  return bleu_score.sentence_bleu(ref, hyp)
  
# def BLEU_corpus_score(expected_corpus: List[str], actual_corpus: List[str]) -> float:
def BLEU_corpus_score(expected_corpus, actual_corpus):
  """
  Score a model's output for an entire corpus compared to the expected output.
  Uses the BLEU metric.
  """
  refs = [[e.split()] for e in expected_corpus]
  hyps = [a.split() for a in actual_corpus]
  return bleu_score.corpus_bleu(refs, hyps)

# def ROUGE_sentence_score(expected: str, actual: str) -> float:
def ROUGE_sentence_score(expected, actual):
  r = Rouge()
  [precision, recall, f_score] = r.rouge_l([expected], [actual])
  return precision, recall, f_score
  
# def ROUGE_corpus_score(expected_corpus: List, actual_corpus: List) -> float:
def ROUGE_corpus_score(expected_corpus, actual_corpus):
  raise NotImplementedError
