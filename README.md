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