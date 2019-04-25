import re

def highlight(sentence, keywords, colors, levels):
    output_string = "<p>"
    new_sentence = sentence
    if len(levels) < len(colors) + 1:
        colors = colors[0:len(levels)-1]
    for keyword in keywords:
        for i in range(0, len(colors)):
            if keyword[1] < levels[i] and keyword[1] > levels[i+1]:
                # print(levels[i], colors[i], levels[i+1])
                match = re.search(keyword[0], sentence, flags=re.IGNORECASE)
                if match is not None:
                    new_sentence = re.sub(keyword[0], f"<span class='{colors[i]}'>{match[0]}</span>", sentence, flags=re.IGNORECASE)
    output_string += new_sentence
    output_string += "</p>"

    return output_string


def highlight_phrases(sentences):
    scores = list()
    for sentence in sentences:
        keyword_scores = [x[1] for x in sentence.keywords]
        scores.extend(keyword_scores)

    distribution = lambda lst, sz: [lst[i:i+sz][-1] for i in range(0, len(lst), sz)]
    n = int(len(scores)/20)

    levels = list(set(distribution(sorted(scores, reverse=True), n)))
    levels.append(max(scores))
    levels = sorted(levels, reverse=True)

    highlights = dict()
    colors = ["purple", "blue", "green", "yellow"]

    html_output = '''<style>
    body { background-color:white; }
    .red { background-color:#ffcccc; }
    .orange { background-color:#FFFF00; }
    .yellow { background-color:#ff9966; }
    .green { background-color:#66ff66; }
    .blue { background-color:#00ffff; }
    .purple { background-color:#ff99ff; }
    p { background-color:#FFFFFF; }
    </style>'''

    for sentence in sentences:
        html_output += highlight(sentence.sentence, sentence.keywords, colors, levels)

    return html_output