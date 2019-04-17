import RAKE

def rake(sentence):
    # print(sentence)
    rake = RAKE.Rake(RAKE.SmartStopList())
    keywords = rake.run(sentence, maxWords=5, minFrequency=1)
    # print(keywords)
    return keywords

def highlight(sentence, keywords):
    output_string = "<p>"
    new_sentence = sentence.lower()
    for keyword in keywords:
        if keyword[1] > 8:
            new_sentence = new_sentence.replace(keyword[0], f"<span class='purple'>{keyword[0]}</span>")
        elif keyword[1] > 5:
            new_sentence = new_sentence.replace(keyword[0], f"<span class='blue'>{keyword[0]}</span>")
    output_string += new_sentence
    output_string += "</p>"

    return output_string

