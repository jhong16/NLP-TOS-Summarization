from pyrouge import Rouge155

def main():# system_file, model_file):
  r = Rouge155()

  r.system_dir = "../model2/Rovio/"
  r.model_dir = "../model2/1NN_Summary/"
  r.system_filename_pattern = '(rovio).txt'
  r.model_filename_pattern = '#ID#.txt'

  output = r.convert_and_evaluate()
  print output
  # output_dict = r.output_to_dict(output)

if __name__ == "__main__":
  # system_file = sys.argv[1]
  # model_file = sys.argv[2]
  # main(system_file, model_file)
  main()