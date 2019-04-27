# NLP-TOS-Summarization

#### Installation instructions

- Clone repository. Go to root directory.
- ```pip install -r requirements.txt```
- Additional work may need to be done to set up [NLTK](https://www.nltk.org/install.html) since you may need to download data.
- For sentence compression, download the [Stanford Parser](https://nlp.stanford.edu/software/lex-parser.shtml)
    - Note: working version (3.9.2)
    - Place zip in known location
    - Unzip
- Set 'CLASSPATH' environment variable: 
    - ```export CLASSPATH=$CLASSPATH:<path to stanford-parser directory>```

For help running model 1, `cd` into `model1` and type ```python main.py -h``` for command line options.

#### Model 2 Installation Instructions
Ensure that you are using Python 3

1. Start with the original Terms of Service/Legal text in a .txt file, and navigate to within the model2 directory

2. Run the text file through the `super_parser9000.py` to normalize the text formatting. The script take two arguments, the name/path of the text you wish to re-format, and the name you wish to bestow upon the re-formatted text file the script returns.

3. Now, we extract the features that will be used in the training (or testing) of the data file. Run the file `feature_creation.py` with the first argument being the name/path to the original ground truth text, the second argument being the name/path to the re-formatted text file the `super_parser9000.py` returned, and the third argument being what you wish the returned JSON file to be named.

4. To train the model, comment in which supervised machine learning model you wish to use in the `train.py` file, and run with the following arguments and flags:
- -tf -- the path to the myriad of files that you wish to train the model
- -ts -- the path to the JSON file previously created by `feature_creation.py` that will be tested on
- -of -- the path to where you wish the model's output summary to be placed


#### ROUGE scores
The ROUGE metrics were calculated by using the [pyrouge wrapper](https://github.com/andersjo/pyrouge) around the original Rouge.1.5.5.pl file, and are reliant on Python 2.7
