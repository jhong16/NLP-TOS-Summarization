# from types import List

from nltk.translate import bleu_score
import rouge

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
  # TODO: fix this so that it actually gives results
  evaluator = rouge.Rouge(metrics=['rouge-n', 'rouge-l'],
      max_n = 4,
      limit_length = True,
      length_limit=100,
      length_limit_type='words',
      apply_avg="Avg")
  return evaluator.get_scores([actual], [expected])
  
# def ROUGE_corpus_score(expected_corpus: List, actual_corpus: List) -> float:
def ROUGE_corpus_score(expected_corpus, actual_corpus):
  raise NotImplementedError
