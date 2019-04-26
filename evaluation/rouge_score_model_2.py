from pyrouge import Rouge155

def main(system_file, model_file):
  r = Rouge155()

  r.system_dir = "../data/smmry_tosdr_corpus/smmry_input/"
  r.model_dir = "../data/smmry_tosdr_corpus/smmry_output/"
  r.system_filename_pattern = '(' + system_file + ').txt'
  r.model_filename_pattern = '#ID#.txt'

  output = r.convert_and_evaluate()
  with open(system_file + "_ROUGE.txt", "w") as f:
    f.write(output)
  # output_dict = r.output_to_dict(output)

if __name__ == "__main__":
  system_file = sys.argv[1]
  model_file = sys.argv[2]
  main(system_file, model_file)