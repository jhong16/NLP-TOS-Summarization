import os

from summary_model import load

def main():
    input_directory = "../data/smmry_tosdr_corpus/smmry_input"
    output_directory = "../data/smmry_tosdr_corpus/model1_output"
    if os.path.isdir(input_directory):
        print("wooo")
    if os.path.isdir(output_directory):
        print("weee")

    input_files = os.listdir(input_directory)
    # print(type(input_files))
    print(input_files)
    
    for input_file in input_files:
        if input_file == "000033.txt":
            continue
        if input_file == "000005.txt":
            continue
        input_full = os.path.join(input_directory, input_file)
        output_full = os.path.join(output_directory, input_file)
        print(input_full)
        # print(output_full)
        try:
            with open(input_full, 'r') as fp:
	            model = load(fp)
            # model.compress_sentences(beta=args.compression_level, path_to_jar=args.path_to_jar, path_to_models_jar=args.path_to_models_jar)
            model.compress_sentences(beta=500, path_to_jar=None, path_to_models_jar=None)
            model.rank_sentences()
            model.rake_sentences(maxWords=2, minFrequency=1)
            short_summary = model.top_sent(7)
            # print(f"{percent*100}% of the Summary")
            for sentence in short_summary:
                print(sentence.sentence)
            with open(output_full, 'w') as f:
                f.write('\n'.join([s.sentence for s in short_summary]))
        except Exception as booo:
            print(f"Something wrong...: {booo}")



if __name__ == "__main__":
    main()